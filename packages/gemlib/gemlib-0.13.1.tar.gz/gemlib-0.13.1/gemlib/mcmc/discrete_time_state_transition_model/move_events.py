"""Move partially-censored events in DiscreteTimeStateTransitionModel"""

from typing import NamedTuple

import tensorflow as tf
import tensorflow_probability as tfp

from gemlib.mcmc.discrete_time_state_transition_model.move_events_impl import (
    UncalibratedEventTimesUpdate,
)
from gemlib.mcmc.sampling_algorithm import ChainState, SamplingAlgorithm

Tensor = tf.Tensor


class MoveEventsState(NamedTuple):
    num_units: int
    delta_max: int
    count_max: int


class MoveEventsInfo(NamedTuple):
    is_accepted: bool
    initial_conditions: float
    proposed_events: Tensor
    proposed_log_density: float
    log_accept_ratio: float
    seed: tuple[int, int]


def move_events(
    incidence_matrix: Tensor,
    transition_index: int,
    num_units: int,
    delta_max: int,
    count_max: int,
    name: str | None = None,
):
    r"""Move partially-censored transition events

    This kernel provides an MCMC algorithm that moves partially-censored
    transition events in a DiscreteTimeStateTransitionModel event timeseres.
    It caters for the situation in which a transition is known to have occurred
    (e.g. as a result of a subsequent case detection), but the time at
    which it occurred is unknown.

    Args:
      incidence_matrix: the state-transition graph incidence matrix
      transition_index: the index of the transition in `incidence_matrix`
                        to update.
      num_units: the number of epidemiological units to update at once
      delta_max: the maximum time interval over which to move transition
                 times.
      count_max: the maximum number of transitions to move at once.
      name: the name of the kernel.

    Returns:
      An instance of :obj:`SamplingAlgorithm` with members
      :obj:`init(tlp_fn: LogProbFnType, position: Position,
      initial_conditions: Tensor)` and :obj:`step(tlp_fn: LogProbFnType,
      cks: ChainAndKernelState, seed: SeedType, initial_conditions: Tensor)`.
      :obj:`initial_conditions` is an extra keyword
      argument required to be passed to the :obj:`init` and :obj:`step`
      functions.

    References:
      Philip D O'Neill and Gareth O Roberts (1999) Baysian inference for
      partially observed stochastic epidemics. _Journal of the Royal
      Statistical Society: Series A (Statistics in Society), **162**\ :121--129.

      Jewell *et al.* (2023) Bayesian inference for high-dimensional discrete-
      time epidemic models: spatial dynamics of the UK COVID-19 outbreak.
      Pre-print arXiv:2306.07987
    """

    def _build_kernel(target_log_prob_fn, initial_conditions):
        return tfp.mcmc.MetropolisHastings(
            inner_kernel=UncalibratedEventTimesUpdate(
                target_log_prob_fn,
                incidence_matrix=incidence_matrix,
                initial_conditions=initial_conditions,
                target_transition_id=transition_index,
                num_units=num_units,
                delta_max=delta_max,
                count_max=count_max,
                name=name or "move_events",
            )
        )

    def init_fn(target_log_prob_fn, position, initial_conditions):
        kernel = _build_kernel(target_log_prob_fn, initial_conditions)
        results = kernel.bootstrap_results(position)
        chain_state = ChainState(
            position=position,
            log_density=results.accepted_results.target_log_prob,
        )
        kernel_state = MoveEventsState(num_units, delta_max, count_max)

        return chain_state, kernel_state

    def step_fn(
        target_log_prob_fn, target_and_kernel_state, seed, initial_conditions
    ):
        target_chain_state, kernel_state = target_and_kernel_state

        kernel = _build_kernel(target_log_prob_fn, initial_conditions)

        new_position, results = kernel.one_step(
            target_chain_state.position,
            kernel.bootstrap_results(target_chain_state.position),
            seed=seed,
        )

        new_chain_and_kernel_state = (
            ChainState(
                position=new_position,
                log_density=results.accepted_results.target_log_prob,
            ),
            kernel_state,
        )

        return new_chain_and_kernel_state, MoveEventsInfo(
            is_accepted=results.is_accepted,
            initial_conditions=initial_conditions,
            proposed_events=results.proposed_state,
            proposed_log_density=results.proposed_results.target_log_prob,
            log_accept_ratio=results.log_accept_ratio,
            seed=seed,
        )

    return SamplingAlgorithm(init_fn, step_fn)
