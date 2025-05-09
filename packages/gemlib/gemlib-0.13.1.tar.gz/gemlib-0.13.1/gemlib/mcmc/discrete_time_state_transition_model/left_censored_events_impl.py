"""Metropolis Hastings implementation for left-censored events
in a discrete-time metapopulation epidemic model
"""

from typing import NamedTuple

import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import prefer_static as ps
from tensorflow_probability.python.internal import samplers
from tensorflow_probability.python.mcmc.internal import util as mcmc_util

from .left_censored_events_proposal import (
    left_censored_event_time_proposal,
)

tfd = tfp.distributions

__all__ = ["UncalibratedLeftCensoredEventTimesUpdate"]

LEFT_CENSORED_EVENT_TIMES_UPDATE_TUPLE_LEN = 2


def _update_state(update, current_state, transition_idx, incidence_matrix):
    current_initial_conditions, current_events = current_state
    update = {k: tf.convert_to_tensor(v) for k, v in update.items()}

    # -1 is moving events forward in time
    sign = tf.gather(
        [-1, 1],
        update["direction"],
    )
    events_delta = update["num_events"] * sign

    # Update initial conditions
    to_stack = [
        tf.broadcast_to(update["unit"], [current_initial_conditions.shape[-1]]),
        ps.range(current_initial_conditions.shape[-1]),
    ]
    indices = tf.stack(
        to_stack,
        axis=-1,
    )
    new_initial_conditions = tf.tensor_scatter_nd_add(
        current_initial_conditions,
        indices=indices,
        updates=tf.cast(
            tf.cast(
                events_delta, incidence_matrix.dtype
            )  # TODO sort this out: casts are usually a code smell!
            * ps.gather(incidence_matrix, transition_idx, axis=-1),
            current_initial_conditions.dtype,
        ),
    )

    # Update events
    indices = tf.stack(
        [
            update["timepoint"],
            update["unit"],
            ps.broadcast_to(transition_idx, update["unit"].shape),
        ],
        axis=-1,
    )
    new_events = tf.tensor_scatter_nd_sub(
        current_events,
        indices=indices,
        updates=tf.cast(events_delta, dtype=current_events.dtype),
    )

    return new_initial_conditions, new_events


def _reverse_update(update):
    direction = (update["direction"] + 1) % 2
    return {
        "unit": update["unit"],
        "timepoint": update["timepoint"],
        "direction": direction,
        "num_events": update["num_events"],
    }


class LeftCensoredEventTimeResults(NamedTuple):
    log_acceptance_correction: float
    target_log_prob: float
    unit: int
    timepoint: int
    direction: int
    num_events: int
    seed: tuple[int, int]


class UncalibratedLeftCensoredEventTimesUpdate(tfp.mcmc.TransitionKernel):
    """UncalibratedLeftCensoredEventTimesUpdate"""

    def __init__(
        self,
        target_log_prob_fn,
        transition_index,
        incidence_matrix,
        max_timepoint,
        max_events,
        name=None,
    ):
        """An uncalibrated random walk for initial conditions.
        :param target_log_prob_fn: the log density of the target distribution
        :param transition_index: the index of the transition to adjust
        :param incidence_matrix: the `[S,R]` incidence matrix
        :param max_timepoint: max timepoint up to which to move events
        :param max_events: max number of events per unit/timepoint to move
        """
        self._name = name
        self._parameters = {
            "target_log_prob_fn": target_log_prob_fn,
            "transition_index": transition_index,
            "incidence_matrix": incidence_matrix,
            "max_timepoint": max_timepoint,
            "max_events": max_events,
            "name": name,
        }

    @property
    def target_log_prob_fn(self):
        return self._parameters["target_log_prob_fn"]

    @property
    def transition_index(self):
        return self._parameters["transition_index"]

    @property
    def incidence_matrix(self):
        return self._parameters["incidence_matrix"]

    @property
    def max_timepoint(self):
        return self._parameters["max_timepoint"]

    @property
    def max_events(self):
        return self._parameters["max_events"]

    @property
    def name(self):
        return self._parameters["name"]

    @property
    def parameters(self):
        return self._parameters

    @property
    def is_calibrated(self):
        return False

    def one_step(self, current_state, previous_kernel_results, seed=None):  # noqa: ARG002
        """Update the initial conditions

        :param current_state: a tuple of `(current_initial_conditions,
                              current_events)`
        :param previous_kernel_results: previous kernel results tuple
        :param seed: optional seed tuple `(int32, int32)`
        :returns: new state tuple `(next_initial_conditions, next_events)`
        """
        with tf.name_scope("uncalibrated_left_censored_events_mh/one_step"):
            seed = samplers.sanitize_seed(
                seed, salt="uncalibrated_left_censored_events_mh"
            )

            if (not mcmc_util.is_list_like(current_state)) and (
                len(current_state) == LEFT_CENSORED_EVENT_TIMES_UPDATE_TUPLE_LEN
            ):
                raise ValueError(
                    f"State for LeftCensoredEventTimesUpdate must be a\
 list/tuple of length {LEFT_CENSORED_EVENT_TIMES_UPDATE_TUPLE_LEN}"
                )

            proposal = left_censored_event_time_proposal(
                events=current_state[1],
                initial_state=current_state[0],
                transition=self.transition_index,
                incidence_matrix=self.incidence_matrix,
                num_units=1,
                max_timepoint=self.max_timepoint,
                max_events=self.max_events,
                name=f"{self.name}/fwd_proposal",
            )
            fwd_update = proposal.sample(seed=seed)
            fwd_proposal_log_prob = proposal.log_prob(
                fwd_update, name="fwd_proposal_log_prob"
            )

            next_state = _update_state(
                fwd_update,
                current_state,
                self.transition_index,
                self.incidence_matrix,
            )
            next_target_log_prob = self.target_log_prob_fn(*next_state)

            rev_update = _reverse_update(fwd_update)
            rev_proposal = left_censored_event_time_proposal(
                events=next_state[1],
                initial_state=next_state[0],
                transition=self.transition_index,
                incidence_matrix=self.incidence_matrix,
                num_units=1,
                max_timepoint=self.max_timepoint,
                max_events=self.max_events,
                name=f"{self.name}/rev_proposal",
            )
            rev_proposal_log_prob = rev_proposal.log_prob(rev_update)
            log_acceptance_correction = tf.reduce_sum(
                rev_proposal_log_prob - fwd_proposal_log_prob
            )
            results = (
                next_state,
                LeftCensoredEventTimeResults(
                    log_acceptance_correction=log_acceptance_correction,
                    target_log_prob=next_target_log_prob,
                    unit=fwd_update["unit"],
                    timepoint=fwd_update["timepoint"],
                    direction=fwd_update["direction"],
                    num_events=fwd_update["num_events"],
                    seed=seed,
                ),
            )

            return results

    def bootstrap_results(self, init_state):
        with tf.name_scope(
            "uncalibrated_left_censored_events_mh/boostrap_results"
        ):
            if (not mcmc_util.is_list_like(init_state)) and (
                len(init_state) == 2  # noqa: PLR2004
            ):
                raise ValueError(
                    f"State for LeftCensoredEventTimesUpdate must be a \
list/tuple of length {LEFT_CENSORED_EVENT_TIMES_UPDATE_TUPLE_LEN}"
                )

            initial_conditions = tf.convert_to_tensor(init_state[0])
            events = tf.convert_to_tensor(init_state[1])
            init_target_log_prob = self.target_log_prob_fn(
                initial_conditions, events
            )
            return LeftCensoredEventTimeResults(
                log_acceptance_correction=tf.constant(
                    0.0, dtype=init_target_log_prob.dtype
                ),
                target_log_prob=init_target_log_prob,
                unit=tf.zeros([1], dtype=tf.int32),
                timepoint=tf.zeros([1], dtype=tf.int32),
                direction=tf.constant(0, dtype=tf.int32),
                num_events=tf.ones([1], dtype=tf.int32),
                seed=samplers.zeros_seed(),
            )
