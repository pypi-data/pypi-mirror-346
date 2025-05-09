"""Sampler for discrete-space occult events"""

from collections.abc import Callable
from typing import NamedTuple

import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import samplers
from tensorflow_probability.python.mcmc.internal import util as mcmc_util

from gemlib.distributions.discrete_markov import (
    compute_state,
)
from gemlib.mcmc.discrete_time_state_transition_model.right_censored_events_proposal import (  # noqa:E501
    add_occult_proposal,
    del_occult_proposal,
)
from gemlib.mcmc.sampling_algorithm import Position
from gemlib.util import transition_coords

tfd = tfp.distributions
Tensor = tf.Tensor

__all__ = ["UncalibratedOccultUpdate"]


PROB_DIRECTION = 0.5


class OccultKernelResults(NamedTuple):
    log_acceptance_correction: float
    target_log_prob: float
    unit: int
    timepoint: int
    is_add: bool
    event_count: int
    seed: tuple[int, int]


def _nonzero_rows(m):
    return tf.cast(tf.reduce_sum(m, axis=-1) > 0.0, m.dtype)


def _maybe_expand_dims(x):
    """If x is a scalar, give it at least 1 dimension"""
    x = tf.convert_to_tensor(x)
    if x.shape == ():
        return tf.expand_dims(x, axis=0)
    return x


def _add_events(events, unit, timepoint, target_transition_id, event_count):
    """Adds `x_star` events to metapopulation `m`,
    time `t`, transition `x` in `events`.
    """
    ut, tp, tt, ec = (
        _maybe_expand_dims(z)
        for z in [unit, timepoint, target_transition_id, event_count]
    )
    ut, tp, tt, ec = (
        tf.reshape(
            z,
            (
                tf.reduce_prod(z.shape[:-1]),
                z.shape[-1],
            ),
        )
        for z in [ut, tp, tt, ec]
    )
    indices = tf.stack([tp, ut, tt], axis=-1)

    updated_events = tf.tensor_scatter_nd_add(
        events, indices, tf.cast(ec, events.dtype)
    )
    return tf.reshape(updated_events, shape=tf.shape(events))


class UncalibratedOccultUpdate(tfp.mcmc.TransitionKernel):
    """UncalibratedOccultUpdate"""

    def __init__(
        self,
        target_log_prob_fn: Callable[[Position], float],
        incidence_matrix: Tensor,
        initial_conditions: Tensor,
        target_transition_id: int,
        count_max: int,
        t_range,
        name=None,
    ):
        """An uncalibrated random walk for event times.
        :param target_log_prob_fn: the log density of the target distribution
        :param target_event_id: the position in the last dimension of the events
                                tensor that we wish to move
        :param t_range: a tuple containing earliest and latest times between
                         which to update occults.
        :param seed: a random seed
        :param name: the name of the update step
        """
        self._parameters = dict(locals())
        self._name = name or "uncalibrated_occult_update"
        self._dtype = tf.convert_to_tensor(initial_conditions).dtype

    @property
    def target_log_prob_fn(self):
        return self._parameters["target_log_prob_fn"]

    @property
    def incidence_matrix(self):
        return self._parameters["incidence_matrix"]

    @property
    def target_transition_id(self):
        return self._parameters["target_transition_id"]

    @property
    def initial_conditions(self):
        return self._parameters["initial_conditions"]

    @property
    def count_max(self):
        return self._parameters["count_max"]

    @property
    def t_range(self):
        return self._parameters["t_range"]

    @property
    def name(self):
        return self._parameters["name"]

    @property
    def parameters(self):
        """Return `dict` of ``__init__`` arguments and their values."""
        return self._parameters

    @property
    def is_calibrated(self):
        return False

    def one_step(self, current_events, previous_kernel_results, seed=None):  # noqa: ARG002
        """One update of event times.
        :param current_events: a [T, M, R] tensor containing number of events
                               per time t, metapopulation m,
                               and transition r.
        :param previous_kernel_results: an object of type
                                        UncalibratedRandomWalkResults.
        :returns: a tuple containing new_state and UncalibratedRandomWalkResults
        """
        with tf.name_scope("occult_rw/onestep"):
            current_events = tf.convert_to_tensor(current_events)

            incidence_matrix = tf.convert_to_tensor(self.incidence_matrix)
            initial_conditions = tf.convert_to_tensor(self.initial_conditions)

            seed = samplers.sanitize_seed(seed, salt="occult_rw")
            proposal_seed, add_del_seed = samplers.split_seed(seed)
            t_range_slice = slice(*self.t_range)

            state = compute_state(
                initial_conditions,
                current_events,
                self.incidence_matrix,
            )
            src_dest_ids = transition_coords(incidence_matrix)[
                self.target_transition_id, :
            ]

            # Pull out the section of events and state that are within
            # the requested time interval - we focus on this, and insert
            # updated values back into the full events at the end.
            range_events = current_events[t_range_slice]
            state_slice = state[t_range_slice]

            def add_occult_fn():
                with tf.name_scope("true_fn"):
                    proposal = add_occult_proposal(
                        count_max=self.count_max,
                        events=range_events[..., self.target_transition_id],
                        src_state=state_slice[..., src_dest_ids[0]],
                    )
                    update = proposal.sample(seed=proposal_seed)

                    next_events = _add_events(
                        events=range_events,
                        unit=update.unit,
                        timepoint=update.timepoint,
                        target_transition_id=self.target_transition_id,
                        event_count=tf.cast(
                            update.event_count, range_events.dtype
                        ),
                    )

                    next_dest_state = compute_state(
                        state_slice[0], next_events, incidence_matrix
                    )
                    reverse = del_occult_proposal(
                        count_max=self.count_max,
                        events=next_events[..., self.target_transition_id],
                        dest_state=next_dest_state[..., src_dest_ids[1]],
                    )
                    q_fwd = tf.reduce_sum(proposal.log_prob(update))
                    q_rev = tf.reduce_sum(reverse.log_prob(update))
                    log_acceptance_correction = q_rev - q_fwd

                return (
                    update,
                    next_events,
                    log_acceptance_correction,
                    True,
                )

            def del_occult_fn():
                with tf.name_scope("false_fn"):
                    proposal = del_occult_proposal(
                        count_max=self.count_max,
                        events=range_events[..., self.target_transition_id],
                        dest_state=state_slice[..., src_dest_ids[1]],
                    )
                    update = proposal.sample(seed=proposal_seed)

                    next_events = _add_events(
                        events=range_events,
                        unit=update.unit,
                        timepoint=update.timepoint,
                        target_transition_id=self.target_transition_id,
                        event_count=tf.cast(
                            -update.event_count, range_events.dtype
                        ),
                    )

                    next_src_state = compute_state(
                        state_slice[0], next_events, incidence_matrix
                    )
                    reverse = add_occult_proposal(
                        count_max=self.count_max,
                        events=next_events[..., self.target_transition_id],
                        src_state=next_src_state[..., src_dest_ids[0]],
                    )
                    q_fwd = tf.reduce_sum(proposal.log_prob(update))
                    q_rev = tf.reduce_sum(reverse.log_prob(update))
                    log_acceptance_correction = q_rev - q_fwd

                return (
                    update,
                    next_events,
                    log_acceptance_correction,
                    False,
                )

            u = tfd.Uniform().sample(seed=add_del_seed)
            delta, next_range_events, log_acceptance_correction, is_add = (
                tf.cond(
                    (u < PROB_DIRECTION)
                    & (tf.math.count_nonzero(range_events) > 0),
                    del_occult_fn,
                    add_occult_fn,
                )
            )

            # Update current_events with the new next_range_events tensor
            next_events = tf.tensor_scatter_nd_update(
                current_events,
                indices=tf.range(t_range_slice.start, t_range_slice.stop)[
                    :, tf.newaxis
                ],
                updates=next_range_events,
            )
            next_target_log_prob = self.target_log_prob_fn(next_events)

            return (
                next_events,
                OccultKernelResults(
                    log_acceptance_correction=log_acceptance_correction,
                    target_log_prob=next_target_log_prob,
                    unit=delta.unit,
                    timepoint=delta.timepoint,
                    is_add=is_add,
                    event_count=delta.event_count,
                    seed=seed,
                ),
            )

    def bootstrap_results(self, init_state):
        with tf.name_scope("uncalibrated_event_times_rw/bootstrap_results"):
            if not mcmc_util.is_list_like(init_state):
                init_state = [init_state]

            init_state = [
                tf.convert_to_tensor(x, dtype=self._dtype) for x in init_state
            ]
            init_target_log_prob = self.target_log_prob_fn(*init_state)
            return OccultKernelResults(
                log_acceptance_correction=tf.constant(
                    0.0, dtype=init_target_log_prob.dtype
                ),
                target_log_prob=init_target_log_prob,
                unit=tf.zeros((), dtype=tf.int32),
                timepoint=tf.zeros((), dtype=tf.int32),
                is_add=tf.constant(True),
                event_count=tf.zeros((), dtype=tf.int32),
                seed=samplers.zeros_seed(),
            )
