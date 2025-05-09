"""Left-censored events MCMC kernel for DiscreteTimeStateTransitionModel"""

from functools import partial
from typing import NamedTuple

import tensorflow as tf
import tensorflow_probability as tfp

from gemlib.mcmc.discrete_time_state_transition_model.left_censored_events_impl import (  # noqa: E501
    UncalibratedLeftCensoredEventTimesUpdate,
)
from gemlib.mcmc.sampling_algorithm import (
    ChainState,
    LogProbFnType,
    SamplingAlgorithm,
)


class LeftCensoredEventsState(NamedTuple):
    max_timepoint: int
    max_events: int


class LeftCensoredEventsInfo(NamedTuple):
    is_accepted: bool
    log_acceptance_correction: float
    target_log_prob: float
    unit: int
    timepoint: int
    direction: int
    num_events: int
    seed: tuple[int, int]


class LeftCensoredEventsPosition(NamedTuple):
    initial_conditions: tf.Tensor
    events: tf.Tensor


def _get_state_tuple(
    initial_conditions_varname: str,
    events_varname: str,
    position: NamedTuple,
):
    return LeftCensoredEventsPosition(
        getattr(position, initial_conditions_varname),
        getattr(position, events_varname),
    )


def _repack_state_tuple(
    initial_conditions_varname: str,
    events_varname: str,
    new_structure: LeftCensoredEventsPosition,
    original_structure: NamedTuple,
):
    return original_structure.__class__(
        **{
            initial_conditions_varname: new_structure.initial_conditions,
            events_varname: new_structure.events,
        }
    )


def left_censored_events_mh(
    incidence_matrix: tf.Tensor,
    transition_index: int,
    max_timepoint: int,
    max_events: int,
    events_varname: str,
    initial_conditions_varname: str,
    name: str | None = None,
):
    """Update initial conditions and events for DiscreteTimeStateTransitionModel

    In observations of a DiscreteTimeStateTransitionModel realisation,
    there may be uncertainty about the initial conditions and hence the number
    of events occurring in the early part of the timeseries.  This MCMC kernel
    provides a means of updating these left-censored events.

    Args
    ----
    incidence_matrix: the state-transition graph incidence matrix
    transition_index: the index of the transition in `incidence_matrix` to
                      update
    max_timepoint: max timepoint up to which to propose moves
    max_events: max number of events per unit/timepoint to move
    events_varname: the name of the random variable holding the events
                    timeseries in a NamedTuple supplied to both the `init` and
                    `step` functions.
    initial_conditions_varname: the name of the random variable representing the
                                initial conditions in a NamedTuple supplied to
                                both the `init` and `step` functions.
    name: name of the kernel.

    Returns
    -------
    A instance of SamplingAlgorithm
    """

    canonize = partial(
        _get_state_tuple, initial_conditions_varname, events_varname
    )
    uncanonize = partial(
        _repack_state_tuple, initial_conditions_varname, events_varname
    )

    def _build_kernel(target_log_prob_fn):
        return tfp.mcmc.MetropolisHastings(
            inner_kernel=UncalibratedLeftCensoredEventTimesUpdate(
                target_log_prob_fn,
                transition_index,
                incidence_matrix,
                max_timepoint,
                max_events,
                name,
            )
        )

    def init_fn(target_log_prob_fn: LogProbFnType, target_state: NamedTuple):
        kernel = _build_kernel(target_log_prob_fn)
        results = kernel.bootstrap_results(canonize(target_state))
        chain_state = ChainState(
            position=target_state,
            log_density=results.accepted_results.target_log_prob,
        )
        kernel_state = LeftCensoredEventsState(
            max_timepoint=max_timepoint, max_events=max_events
        )

        return chain_state, kernel_state

    def step_fn(target_log_prob_fn, target_and_kernel_state, seed):
        kernel = _build_kernel(target_log_prob_fn)
        target_chain_state, kernel_state = target_and_kernel_state

        new_target_position, results = kernel.one_step(
            canonize(target_chain_state.position),
            kernel.bootstrap_results(canonize(target_chain_state.position)),
            seed=seed,
        )

        new_chain_and_kernel_state = (
            ChainState(
                position=uncanonize(
                    new_target_position, target_chain_state.position
                ),
                log_density=results.accepted_results.target_log_prob,
            ),
            kernel_state,
        )

        return new_chain_and_kernel_state, LeftCensoredEventsInfo(
            is_accepted=results.is_accepted,
            log_acceptance_correction=results.proposed_results.log_acceptance_correction,
            target_log_prob=results.proposed_results.target_log_prob,
            unit=results.proposed_results.unit,
            timepoint=results.proposed_results.timepoint,
            direction=results.proposed_results.direction,
            num_events=results.proposed_results.num_events,
            seed=seed,
        )

    return SamplingAlgorithm(init_fn, step_fn)
