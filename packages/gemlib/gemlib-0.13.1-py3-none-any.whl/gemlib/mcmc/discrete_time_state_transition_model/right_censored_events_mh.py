"""Right-censored events MCMC kernel for DiscreteTimeStateTransitionModel"""

from typing import NamedTuple

import tensorflow as tf
import tensorflow_probability as tfp

from gemlib.mcmc.discrete_time_state_transition_model.right_censored_events_impl import (  # noqa: E501
    UncalibratedOccultUpdate,
)
from gemlib.mcmc.sampling_algorithm import ChainState, SamplingAlgorithm


class RightCensoredEventsState(NamedTuple):
    count_max: int
    t_range: tuple[int, int]


class RightCensoredEventsInfo(NamedTuple):
    event_count: int
    is_accepted: bool
    is_add: int
    log_acceptance_correction: float
    proposed_state: tf.Tensor
    proposed_log_density: float
    seed: tuple[int, int]
    timepoint: int
    unit: int


def right_censored_events_mh(
    incidence_matrix: tf.Tensor,
    transition_index: int,
    t_range: tuple[int, int],
    count_max: int = 1,
    name: str | None = None,
) -> SamplingAlgorithm:
    r"""Update right-censored events for DiscreteTimeStateTransitionModel

    In a partially-complete epidemic, we may wish to explore the space of
    events that _might_ have occurred, but are not apparent because
    of some detection event that is yet to occur. This MCMC kernel performs
    a single-site "add/delete" move, as described (in continuous time) in
    O'Neill and Roberts (1999).

    Args:
      incidence_matrix: the state-transition graph incidence matrix
      transition_index: the index of the transition in :obj:`incidence_matrix`
        to update
      t_range: the time-range for which to update censored transition events.
        Typically this would be :obj:`[s, num_steps)` where :obj:`s < num_steps`
        for :obj:`num_steps` the total number of timesteps in the model.
      count_max: the max number of transitions to add or delete in any one
        update
      name: name of the kernel

    Returns:
      An instance of :obj:`SamplingAlgorithm` with members
      :obj:`init(tlp_fn: LogProbFnType, position: Position,
      initial_conditions: Tensor)` and :obj:`step(tlp_fn: LogProbFnType,
      cks: ChainAndKernelState, seed: SeedType, initial_conditions: Tensor)`.
      :obj:`initial_conditions` is an extra keyword
      argument required to be passed to the :obj:`init` and :obj:`step`
      functions.

    References:
      1. Philip D O'Neill and Gareth O Roberts (1999) Baysian inference for
         partially observed stochastic epidemics. _Journal of the Royal
         Statistical Society: Series A (Statistics in Society), **162**
         \ :121--129.

      2. Jewell _et al._ (2023) Bayesian inference for high-dimensional
         discrete-time epidemic models: spatial dynamics of the UK COVID-19
         outbreak. Pre-print arXiv:2306.07987
    """

    def _build_kernel(target_log_prob_fn, initial_conditions):
        return tfp.mcmc.MetropolisHastings(
            inner_kernel=UncalibratedOccultUpdate(
                target_log_prob_fn,
                incidence_matrix=incidence_matrix,
                initial_conditions=initial_conditions,
                target_transition_id=transition_index,
                count_max=count_max,
                t_range=t_range,
                name=name,
            ),
        )

    def init_fn(target_log_prob_fn, position, initial_conditions):
        position = tf.convert_to_tensor(position)
        initial_conditions = tf.convert_to_tensor(initial_conditions)

        kernel = _build_kernel(target_log_prob_fn, initial_conditions)
        results = kernel.bootstrap_results(position)
        chain_state = ChainState(
            position=position,
            log_density=results.accepted_results.target_log_prob,
        )
        kernel_state = RightCensoredEventsState(
            count_max=count_max, t_range=t_range
        )

        return chain_state, kernel_state

    def step_fn(
        target_log_prob_fn, target_and_kernel_state, seed, initial_conditions
    ):
        seed = tfp.random.sanitize_seed(seed)
        initial_conditions = tf.convert_to_tensor(initial_conditions)

        target_chain_state, kernel_state = target_and_kernel_state

        kernel = _build_kernel(target_log_prob_fn, initial_conditions)

        new_target_position, results = kernel.one_step(
            target_chain_state.position,
            kernel.bootstrap_results(target_chain_state.position),
            seed=seed,
        )
        new_chain_and_kernel_state = (
            ChainState(
                position=new_target_position,
                log_density=results.accepted_results.target_log_prob,
            ),
            kernel_state,
        )

        pr = results.proposed_results

        return new_chain_and_kernel_state, RightCensoredEventsInfo(
            is_accepted=results.is_accepted,
            unit=pr.unit,
            timepoint=pr.timepoint,
            is_add=pr.is_add,
            event_count=pr.event_count,
            log_acceptance_correction=pr.log_acceptance_correction,
            proposed_state=results.proposed_state,
            proposed_log_density=results.proposed_results.target_log_prob,
            seed=results.seed,
        )

    return SamplingAlgorithm(init_fn, step_fn)
