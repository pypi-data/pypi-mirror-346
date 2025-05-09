"""Implementation of the Random Walk Metropolis algorithm"""

from collections.abc import Callable
from typing import NamedTuple, TypeVar

import tensorflow_probability as tfp

from .sampling_algorithm import ChainState, SamplingAlgorithm

Tensor = TypeVar("Tensor")


class RwmhInfo(NamedTuple):
    """Represents the information about a random walk Metropolis-Hastings (RWMH)
    step.

    This can be expanded to include more information in the future (as needed
    for a specific kernel).

    Attributes
    ----------
    is_accepted: Indicates whether the proposal was accepted or not.
    proposed_state: the proposed state
    """

    is_accepted: bool
    proposed_state: Tensor


class RwmhKernelState(NamedTuple):
    """Represents the kernel state of an arbitrary MCMC kernel.

    Attributes
    ----------
        scale (float): The scale parameter for the RWMH kernel.
    """

    scale: float


def rwmh(scale: int = 1.0):
    """Random walk Metropolis Hastings MCMC kernel

    Args:
      scale: the random walk scaling parameter.  Should broadcast with the
             state.
    Returns:
      an instance of :obj:`SamplingAlgorithm`
    """

    def _build_kernel(log_prob_fn):
        """Partial"""
        return tfp.mcmc.RandomWalkMetropolis(
            target_log_prob_fn=log_prob_fn,
            new_state_fn=tfp.mcmc.random_walk_normal_fn(scale=scale),
        )

    def init_fn(target_log_prob_fn, target_state):
        kernel = _build_kernel(target_log_prob_fn)
        results = kernel.bootstrap_results(target_state)

        chain_state = ChainState(
            position=target_state,
            log_density=results.accepted_results.target_log_prob,
            log_density_grad=(),
        )
        kernel_state = RwmhKernelState(scale=scale)

        return chain_state, kernel_state

    def step_fn(
        target_log_prob_fn: Callable[[NamedTuple], float],
        target_and_kernel_state: tuple[ChainState, RwmhKernelState],
        seed,
    ) -> Callable[[ChainState], tuple[ChainState, RwmhInfo]]:
        # This could be replaced with BlackJAX easily
        kernel = _build_kernel(target_log_prob_fn)

        target_chain_state, kernel_state = target_and_kernel_state

        new_target_position, results = kernel.one_step(
            target_chain_state.position,
            kernel.bootstrap_results(target_chain_state.position),
            seed=seed,
        )

        new_chain_and_kernel_state = (
            ChainState(
                position=new_target_position,
                log_density=results.accepted_results.target_log_prob,
                log_density_grad=(),
            ),
            kernel_state,
        )

        return new_chain_and_kernel_state, RwmhInfo(
            results.is_accepted, results.proposed_state
        )

    return SamplingAlgorithm(init_fn, step_fn)
