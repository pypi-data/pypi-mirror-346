"""Constrained Event Move kernel for DiscreteTimeStateTransitionModel"""

from collections.abc import Callable
from typing import NamedTuple
from warnings import warn

import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import samplers
from tensorflow_probability.python.mcmc.internal import util as mcmc_util

from gemlib.distributions.discrete_markov import compute_state
from gemlib.distributions.kcategorical import UniformKCategorical
from gemlib.distributions.uniform_integer import UniformInteger
from gemlib.mcmc.sampling_algorithm import (
    Position,
)
from gemlib.util import transition_coords

tfd = tfp.distributions

__all__ = ["UncalibratedEventTimesUpdate"]


# Proposal mechanism
def events_state_count_bounding_fn(dmax):
    """Compute upper bound for number of possible event moves

    Args
        ----
        dmax: maximum possible extent in time
        events: a [T, M] tensor of transition events
        src_state: a [T, M] tensor of corresponding source state
        dest_state: a [T, M] tensor of corresponing destination state
        timepoints: a [M] tensor of timepoints
        delta_t: a [M] tensor of time deltas where `abs(delta_t) <= dmax`

    Returns
        -------
        A [M] tensor of the maximum number of transition events
        that can be moved from `time` to `time+delta` without
        violating `src_state >= 0` and `dest_state >= 0`.
    """

    def fn(events, src_state, dest_state, timepoints, delta):
        # Compute indices of elements in src_state and dest_state to gather
        timerange = tf.range(dmax, dtype=tf.int32)
        candidate_times = tf.where(
            delta[tf.newaxis, :] < 0,
            timepoints[tf.newaxis, :] - timerange[:, tf.newaxis],
            timepoints[tf.newaxis, :] + timerange[:, tf.newaxis] + 1,
        )
        # Clip time indices to ensure we don't access elements outside the time
        # extent
        candidate_times = tf.clip_by_value(
            candidate_times, 0, events.shape[-2] - 1
        )

        # Compute tensor of indices into src_state and dest_state
        src_dest_indices = tf.stack(
            [
                candidate_times,
                tf.broadcast_to(
                    tf.range(events.shape[-1])[tf.newaxis, :],
                    candidate_times.shape,
                ),  # Make unit indices broadcast over rows of time_window
            ],
            axis=-1,
        )  # Dimension is [dmax, M, 2] -- inner dim is coordinates into *_state

        # Gather
        src_max = tf.gather_nd(src_state, src_dest_indices)
        dest_max = tf.gather_nd(dest_state, src_dest_indices)

        # Pick out required bounds
        state_max = tf.where(delta < 0, src_max, dest_max)
        state_max = tf.reduce_min(state_max, axis=-2)

        # Take min of bounds and available events
        bound_indices = tf.stack(
            [timepoints, tf.range(events.shape[-1])], axis=-1
        )
        timepoint_events = tf.gather_nd(events, bound_indices)
        bound = tf.minimum(state_max, timepoint_events)

        return bound

    return fn


def _is_within(x, low, high):
    """Tests `low <= x < high`"""
    return tf.math.logical_and(
        tf.math.greater_equal(x, low), tf.math.less(x, high)
    )


def _timepoint_selector(events, name):
    timepoint_probs = tf.linalg.normalize(
        tf.linalg.matrix_transpose(
            tf.cast(events > 0.0, events.dtype),
        ),
        ord=1,
        axis=-1,
    )[0]

    return tfd.Independent(
        tfd.Categorical(
            probs=timepoint_probs,
        ),
        reinterpreted_batch_ndims=1,
        name=name,
    )


def _delta_selector(delta_max, timepoints, events, name):
    delta_max = tf.convert_to_tensor(delta_max)
    timepoints = tf.convert_to_tensor(timepoints)
    events = tf.convert_to_tensor(events)

    candidate_deltas = tf.concat(
        [tf.range(-delta_max, 0), tf.range(1, delta_max + 1)], axis=0
    )
    valid_candidates = _is_within(  # ensure timepoint + delta is valid
        candidate_deltas[..., tf.newaxis, :] + timepoints[..., tf.newaxis],
        low=0,
        high=events.shape[-2],
    )

    probs = tf.linalg.normalize(  # turn valid deltas into sampling probs
        tf.cast(valid_candidates, events.dtype), ord=1, axis=-1
    )[0]

    return tfd.Independent(
        tfd.FiniteDiscrete(outcomes=candidate_deltas, probs=probs),
        reinterpreted_batch_ndims=1,
        name=name,
    )


def _make_event_count_selector(src_dest_ids, count_bounding_fn, count_max):
    count_max = tf.convert_to_tensor(count_max)

    def fn(events, state, timepoints, delta):
        bound = tf.cast(
            count_bounding_fn(
                events=events,
                src_state=state[:, :, src_dest_ids[0]],
                dest_state=state[:, :, src_dest_ids[1]],
                timepoints=timepoints,
                delta=delta,
            ),
            count_max.dtype,
        )
        bound = tf.minimum(bound, count_max)  # Upper bound on number of events

        # Select number of events to move
        return tfd.Independent(
            UniformInteger(low=1, high=bound + 1, float_dtype=events.dtype),
            reinterpreted_batch_ndims=1,
            name="event_count",
        )

    return fn


def discrete_move_events_proposal(
    incidence_matrix: tf.Tensor,
    target_transition_id: int,
    num_units: int,
    delta_max: int,
    count_max: int,
    initial_conditions: tf.Tensor,
    events: tf.Tensor,
    count_bounding_fn: Callable[
        [tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor], tf.Tensor
    ],
    name=None,
):
    """Build a proposal mechanism for moving discrete transition events

    Args
    ----
    incidence_matrix: a `[S,R]` matrix representing the state transition model
    target_transition_id: the id (column) of the transition to update
    num_units: number of units to update simultaneously
    delta_max: maximum time delta through which to move transitions
    count_max: absolute maximum number of transition events to move
    initial_conditions: a `[M,S]` matrix representing `M` units and `S` states
    events: a `[T, M, R]` tensor giving the number of events that occur for each
            time $t=0,...,T-1$, unit $m=0,...,M-1$, and transition $r=0,...,R-1$
    count_bounding_fn: a callable taking `events`, `src_state`, `dest_state`,
                       `timepoints`, and `delta_t` and returning tensor of
                       length `num_units` of the maximum possible events that
                       can be moved.

    Returns
    -------
    An instance of `tfd.JointDistributionCoroutine` which samples a proposal
    """
    incidence_matrix = tf.convert_to_tensor(incidence_matrix)
    count_max = tf.get_static_value(count_max, partial=False)
    initial_conditions = tf.convert_to_tensor(initial_conditions)
    events = tf.convert_to_tensor(events)

    def proposal():
        target_events = tf.gather(events, target_transition_id, axis=-1)
        state = compute_state(initial_conditions, events, incidence_matrix)

        src_dest_ids = transition_coords(incidence_matrix)[target_transition_id]

        # Select units to update if they have events
        nonzero_units = tf.reduce_any(target_events > 0, axis=-2)
        units = yield tfd.JointDistribution.Root(
            UniformKCategorical(
                k=num_units,
                mask=nonzero_units,
                float_dtype=events.dtype,
                name="unit",
            )
        )

        # Select out the units of interest
        events_subset = tf.gather(target_events, units, axis=-1)  # [..., T]
        state_subset = tf.gather(
            state, units, axis=-2
        )  # [..., T, num_units, S]

        # Select timepoint to update
        timepoints = yield _timepoint_selector(events_subset, "timepoint")

        # Select distance to move, clipping if a delta would move us out of
        # the valid range [0, events_subset.shape[-2])
        delta = yield _delta_selector(
            delta_max, timepoints, events_subset, "delta"
        )

        # Compute number of events to move
        count_selector = _make_event_count_selector(
            src_dest_ids, count_bounding_fn, count_max
        )
        yield count_selector(events_subset, state_subset, timepoints, delta)

    return tfd.JointDistributionCoroutine(proposal, name=name)


class EventTimesKernelResults(NamedTuple):
    log_acceptance_correction: float
    target_log_prob: float
    fwd_proposed_move: NamedTuple
    rev_proposed_move: NamedTuple
    seed: list[int]


def _apply_move(event_tensor, event_id, move):
    """Apply `move` to `event_tensor`

    Args
    ----
        event_tensor: shape [T, M, R]
        event_id: the event id to move
        move: a data structure with fields ["unit", "timepoint", "delta",
              "counts"]

    Returns
    -------
    a copy of `event_tensor` with `move` applied
    """

    indices = tf.stack(
        [move.timepoint, move.unit, tf.broadcast_to(event_id, move.unit.shape)],
        axis=-1,  # All meta-populations
    )  # Event

    # Subtract `count` from the `event_tensor[timepoint, :, event_id]`
    count = tf.cast(move.event_count, event_tensor.dtype)
    new_state = tf.tensor_scatter_nd_sub(event_tensor, indices, count)

    # Add `count` to [move.timpoint+delta, :, event_id]
    indices = tf.stack(
        [
            move.timepoint + move.delta,
            move.unit,
            tf.broadcast_to(event_id, move.unit.shape),
        ],
        axis=-1,
    )
    new_state = tf.tensor_scatter_nd_add(new_state, indices, count)
    return new_state


def _reverse_move(move):
    return move._replace(
        timepoint=move.timepoint + move.delta, delta=-move.delta
    )


class UncalibratedEventTimesUpdate(tfp.mcmc.TransitionKernel):
    """UncalibratedEventTimesUpdate"""

    def __init__(
        self,
        target_log_prob_fn: Callable[[Position], float],
        incidence_matrix: tf.Tensor,
        initial_conditions: tf.Tensor,
        target_transition_id: int,
        num_units: int,
        delta_max: int,
        count_max: int,
        name: str = None,
    ):
        """An uncalibrated random walk for event times.
        :param target_log_prob_fn: the log density of the target distribution
        :param target_event_id: the position in the first dimension of the
                                events tensor that we wish to move
        :param prev_event_id: the position of the previous event in the events
                              tensor
        :param next_event_id: the position of the next event in the events
                              tensor
        :param initial_state: the initial state tensor
        :param seed: a random seed
        :param name: the name of the update step
        """
        self._name = name
        self._parameters = {
            "target_log_prob_fn": target_log_prob_fn,
            "incidence_matrix": incidence_matrix,
            "initial_conditions": initial_conditions,
            "target_transition_id": target_transition_id,
            "num_units": num_units,
            "delta_max": delta_max,
            "count_max": count_max,
            "name": name,
        }

    @property
    def target_log_prob_fn(self):
        return self._parameters["target_log_prob_fn"]

    @property
    def incidence_matrix(self):
        return self._parameters["incidence_matrix"]

    @property
    def initial_conditions(self):
        return self._parameters["initial_conditions"]

    @property
    def target_transition_id(self):
        return self._parameters["target_transition_id"]

    @property
    def num_units(self):
        return self._parameters["num_units"]

    @property
    def delta_max(self):
        return self._parameters["delta_max"]

    @property
    def count_max(self):
        return self._parameters["count_max"]

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

    def _proposal(self, events):
        return discrete_move_events_proposal(
            incidence_matrix=self.incidence_matrix,
            target_transition_id=self.target_transition_id,
            num_units=self.num_units,
            delta_max=self.delta_max,
            count_max=self.count_max,
            initial_conditions=self.initial_conditions,
            events=events,
            count_bounding_fn=events_state_count_bounding_fn(self.delta_max),
            name=self.name,
        )

    def one_step(self, current_events, previous_kernel_results, seed=None):  # noqa: ARG002
        """One update of event times.
        :param current_events: a [T, M, X] tensor containing number of events
                               per time t, metapopulation m,
                               and transition x.
        :param previous_kernel_results: an object of type
                                        UncalibratedRandomWalkResults.
        :returns: a tuple containing new_state and UncalibratedRandomWalkResults
        """
        with tf.name_scope("uncalibrated_event_times_rw/onestep"):
            seed = samplers.sanitize_seed(
                seed, salt="uncalibrated_event_times_rw"
            )

            step_events = current_events
            if mcmc_util.is_list_like(current_events):
                step_events = current_events[0]
                warn(
                    "Batched event times updates are not supported.  Using \
first event item only.",
                    stacklevel=2,
                )
            fwd_proposal_dist = self._proposal(step_events)
            fwd_proposed_move = fwd_proposal_dist.sample(seed=seed)
            fwd_prob = fwd_proposal_dist.log_prob(fwd_proposed_move)

            # Propagate the proposal into events
            proposed_events = _apply_move(
                event_tensor=step_events,
                event_id=self.target_transition_id,
                move=fwd_proposed_move,
            )

            next_target_log_prob = self.target_log_prob_fn(proposed_events)

            # Compute the reverse move
            rev_proposed_move = _reverse_move(fwd_proposed_move)

            rev_prob = self._proposal(proposed_events).log_prob(
                rev_proposed_move
            )
            log_acceptance_correction = rev_prob - fwd_prob

            if mcmc_util.is_list_like(current_events):
                proposed_events = [proposed_events]

            return (
                proposed_events,
                EventTimesKernelResults(
                    log_acceptance_correction=log_acceptance_correction,
                    target_log_prob=next_target_log_prob,
                    fwd_proposed_move=fwd_proposed_move,
                    rev_proposed_move=rev_proposed_move,
                    seed=seed,
                ),
            )

    def bootstrap_results(self, init_state):
        with tf.name_scope("uncalibrated_event_times_rw/bootstrap_results"):
            if mcmc_util.is_list_like(init_state):
                init_state = init_state[0]
                warn(
                    "Batched event times updates are not supported.  Using \
first event item only.",
                    stacklevel=2,
                )

            init_state = tf.convert_to_tensor(init_state)
            init_target_log_prob = self.target_log_prob_fn(init_state)

            proposal_example = self._proposal(init_state).sample(seed=[0, 0])

            return EventTimesKernelResults(
                log_acceptance_correction=tf.zeros_like(init_target_log_prob),
                target_log_prob=init_target_log_prob,
                fwd_proposed_move=proposal_example,
                rev_proposed_move=proposal_example,
                seed=samplers.zeros_seed(),
            )
