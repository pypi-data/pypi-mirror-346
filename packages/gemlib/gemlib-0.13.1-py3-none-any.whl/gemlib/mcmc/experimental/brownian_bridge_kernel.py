"""A Brownian Bridge kernel is intended to operate on
a timeseries
"""

# ruff: noqa: B023

import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import samplers
from tensorflow_probability.python.mcmc.internal import util as mcmc_util
from tensorflow_probability.python.mcmc.random_walk_metropolis import (
    UncalibratedRandomWalkResults,
)

from gemlib.distributions.brownian import BrownianBridge, BrownianMotion
from gemlib.distributions.uniform_integer import UniformInteger

tfd = tfp.distributions
mcmc = tfp.mcmc

MIN_SPAN = 3


def _slide_left(x, shift):
    x_right = x[..., -1:]
    y = tf.roll(x, -shift, axis=-1)
    mask = tf.range(x.shape[-1]) >= (x.shape[-1] - shift)
    pad = x_right * tf.cast(mask, x_right.dtype)
    return y * tf.cast(~mask, y.dtype) + pad


def _slide_right(x, shift):
    x_left = x[..., 0:]
    y = tf.roll(x, shift, axis=-1)
    mask = tf.range(x.shape[-1]) < shift
    pad = x_left * tf.cast(mask, x_left.dtype)
    return y * tf.cast(~mask, x_left.dtype) + pad


class UncalibratedBrownianBridgeKernel(mcmc.TransitionKernel):
    def __init__(
        self,
        target_log_prob_fn,
        index_points,
        span=3,
        scale=0.1,
        left=True,
        right=True,
        name="UncalibratedBrownianBridgeKernel",
    ):
        with tf.name_scope(
            mcmc_util.make_name(
                name, "UncalibratedBrownianBridgeKernel", "__init__"
            )
        ):
            if span < MIN_SPAN:
                raise ValueError(
                    f"`span` must be at least {MIN_SPAN} timepoints"
                )
            if scale <= 0.0:
                raise ValueError("`scale` must be positive")

            span_parts = list(span) if mcmc_util.is_list_like(span) else [span]
            self.span_parts = [
                tf.convert_to_tensor(s, name="span") for s in span_parts
            ]

            if mcmc_util.is_list_like(scale):
                scale_parts = list(scale)
            else:
                scale_parts = [scale]
            self.scale_parts = [
                tf.convert_to_tensor(s, name="scale") for s in scale_parts
            ]

            self._index_points = tf.convert_to_tensor(index_points)
            self._left = tf.cast(left, tf.int32)
            self._right = tf.cast(right, tf.int32)

            self.dtype = self.scale_parts[0].dtype
            cls_name = mcmc_util.make_name(
                name, "UncalibratedBrownianBridgeKernel", ""
            )

            self._parameters = {
                "target_log_prob_fn": target_log_prob_fn,
                "index_points": index_points,
                "span": span,
                "scale": scale,
                "left": left,
                "right": right,
                "name": cls_name,
            }

    @property
    def is_calibrated(self):
        return False

    @property
    def name(self):
        return self._parameters["name"]

    @property
    def span(self):
        return self._parameters["span"]

    @property
    def scale(self):
        return self._parameters["scale"]

    @property
    def jitter(self):
        return self._parameters["jitter"]

    @property
    def target_log_prob_fn(self):
        return self._parameters["target_log_prob_fn"]

    def one_step(self, current_state, _, seed=None):
        with tf.name_scope(mcmc_util.make_name(self.name, "bbmh", "one_step")):
            with tf.name_scope("initialize"):
                if mcmc_util.is_list_like(current_state):
                    current_state_parts = list(current_state)
                else:
                    current_state_parts = [current_state]
                current_state_parts = [
                    tf.convert_to_tensor(s, name="current_state")
                    for s in current_state_parts
                ]
            seed = samplers.sanitize_seed(
                seed, salt="UncalibratedBrownianBridgeKernel"
            )

            new_state_parts = []
            log_acceptance_correction_parts = []
            for current_state_part, span_part, scale_part in zip(
                current_state_parts,
                self.span_parts,
                self.scale_parts,
                strict=False,
            ):
                t_low_seed, bridge_seed = samplers.split_seed(seed)

                # Evaluate bridge limits
                t_low = UniformInteger(
                    0 - self._left,
                    current_state_part.shape[-1] - span_part + self._right,
                ).sample(seed=seed)

                # We have 3 cases:
                #  0. If t_low > 0 and t_high < (current_state.shape[-1]-1):
                #     Brownian Bridge
                #  1. If t_low == 0: reverse Brownian motion
                #  2. If t_high >= (current_state.shape[-1]-1): Brownian motion
                def brownian_bridge_proposal():
                    with tf.name_scope("brownian_bridge_proposal"):
                        indices = t_low + tf.range(span_part)
                        current_bridge = tf.gather(
                            current_state_part,
                            indices=indices,
                        )
                        bridge = BrownianBridge(
                            index_points=tf.gather(self._index_points, indices),
                            x0=current_bridge[..., 0],
                            x1=current_bridge[..., -1],
                            scale=scale_part,
                        )
                        new_bridge = bridge.sample(seed=bridge_seed)
                        log_acceptance_correction = bridge.log_prob(
                            current_bridge[1:-1]
                        ) - bridge.log_prob(new_bridge)

                        new_state = tf.tensor_scatter_nd_update(
                            current_state_part,
                            indices=indices[1:-1][:, tf.newaxis],
                            updates=new_bridge,
                            name="update_new_state",
                        )
                        return new_state, log_acceptance_correction

                def brownian_motion_right_proposal():
                    with tf.name_scope("brownian_motion_proposal"):
                        indices = tf.range(
                            current_state_part.shape[0] - span_part,
                            current_state_part.shape[0],
                        )  # Index into current_state_part
                        current_bridge = tf.gather(
                            current_state_part,
                            indices=indices,
                            name="current_state_slice",
                        )
                        bridge = BrownianMotion(
                            index_points=tf.gather(self._index_points, indices),
                            x0=current_bridge[..., 0],
                            scale=scale_part,
                        )
                        new_bridge = bridge.sample(seed=bridge_seed)
                        log_acceptance_correction = bridge.log_prob(
                            current_bridge[1:]
                        ) - bridge.log_prob(new_bridge)
                        new_state = tf.tensor_scatter_nd_update(
                            current_state_part,
                            indices=tf.expand_dims(indices[1:], -1),
                            updates=new_bridge,
                            name="update_new_state",
                        )
                        return new_state, log_acceptance_correction

                def brownian_motion_left_proposal():
                    with tf.name_scope("brownian_motion_left_proposal"):
                        indices = tf.range(span_part)
                        current_bridge = tf.gather(
                            current_state_part,
                            indices=indices,
                            name="current_state_slice",
                        )
                        bridge = BrownianMotion(
                            index_points=tf.gather(self._index_points, indices),
                            x0=current_bridge[..., -1],
                            scale=scale_part,
                        )
                        new_bridge = bridge.sample(seed=bridge_seed)
                        log_acceptance_correction = bridge.log_prob(
                            tf.reverse(
                                current_bridge[:-1],
                                axis=[-1],
                                name="reverse_current_bridge",
                            ),
                        ) - bridge.log_prob(new_bridge)
                        new_state = tf.tensor_scatter_nd_update(
                            current_state_part,
                            indices=tf.expand_dims(indices[:-1], -1),
                            updates=tf.reverse(
                                new_bridge, axis=[-1], name="reverse_new_bridge"
                            ),
                            name="update_new_state",
                        )
                        return new_state, log_acceptance_correction

                case_enum = (  # 0=bridge, 1=right, 2=left
                    tf.cast(
                        t_low == (current_state_part.shape[0] - span_part),
                        tf.int32,
                    )
                    + tf.cast(t_low == -1, tf.int32) * 2
                )

                (
                    new_state,
                    log_acceptance_correction_part,
                ) = tf.switch_case(
                    case_enum,
                    [
                        brownian_bridge_proposal,
                        brownian_motion_right_proposal,
                        brownian_motion_left_proposal,
                    ],
                )

                new_state_parts.append(new_state)
                log_acceptance_correction_parts.append(
                    log_acceptance_correction_part
                )

            target_log_prob = self.target_log_prob_fn(*new_state_parts)

            def maybe_flatten(x):
                return x if mcmc_util.is_list_like(current_state) else x[0]

            return [
                maybe_flatten(new_state_parts),
                UncalibratedRandomWalkResults(
                    log_acceptance_correction=maybe_flatten(
                        log_acceptance_correction_parts
                    ),
                    target_log_prob=target_log_prob,
                    seed=seed,
                ),
            ]

    def bootstrap_results(self, current_state):
        if mcmc_util.is_list_like(current_state):
            current_state_parts = list(current_state)
        else:
            current_state_parts = [current_state]

        init_target_log_prob = self.target_log_prob_fn(*current_state_parts)

        return UncalibratedRandomWalkResults(
            log_acceptance_correction=tf.zeros_like(init_target_log_prob),
            target_log_prob=init_target_log_prob,
            seed=samplers.zeros_seed(),
        )
