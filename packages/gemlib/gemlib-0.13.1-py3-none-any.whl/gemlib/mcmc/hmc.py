"""Base Hamiltonian Monte Carlo"""

from collections.abc import Iterable
from typing import NamedTuple

import tensorflow as tf
import tensorflow_probability as tfp
import tensorflow_probability.python.experimental.mcmc.preconditioning_utils as pu  # noqa: E501

from .sampling_algorithm import ChainState, SamplingAlgorithm

tfd = tfp.distributions
tfde = tfp.experimental.distributions


class HmcKernelState(NamedTuple):
    step_size: float
    num_leapfrog_steps: float
    mass_matrix: Iterable


def hmc(
    step_size: float = 0.1,
    num_leapfrog_steps: int = 16,
    mass_matrix: Iterable | None = None,
) -> SamplingAlgorithm:
    """Hamiltonian Monte Carlo

    Args:
      step_size: the step size to take
      num_leapfrog_steps: number of leapfrog steps to take
      mass_matrix: a mass matrix (defaults to :obj:`diag(1)` if :obj:`None`)

    Returns:
      A :obj:`SamplingAlgorithm`

    References:
      Michael Betancourt. A Conceptual Introduction to Hamiltonian
      Monte Carlo. arXiv, 2017. https://arxiv.org/abs/1701.02434

    """

    step_size = tf.convert_to_tensor(step_size)
    mass_matrix = (
        tf.convert_to_tensor(mass_matrix) if mass_matrix is not None else None
    )

    def _make_momentum_distribution(position):
        # return None
        if mass_matrix is None:
            return pu.make_momentum_distribution(
                position, tf.constant([], dtype=tf.int32)
            )

        else:
            return tfde.MultivariateNormalPrecisionFactorLinearOperator(
                precision_factor=tf.linalg.LinearOperatorFullMatrix(
                    mass_matrix
                ),
                precision=tf.linalg.LinearOperatorFullMatrix(mass_matrix),
            )

    def _build_kernel(target_log_prob_fn, momentum_distribution):
        return tfp.experimental.mcmc.PreconditionedHamiltonianMonteCarlo(
            target_log_prob_fn=target_log_prob_fn,
            step_size=step_size,
            num_leapfrog_steps=num_leapfrog_steps,
            momentum_distribution=momentum_distribution,
            store_parameters_in_results=True,
        )

    def init_fn(target_log_prob_fn, initial_position):
        kernel = _build_kernel(
            target_log_prob_fn, _make_momentum_distribution(initial_position)
        )
        results = kernel.bootstrap_results(initial_position)

        # Repack the results data structure into our own
        chain_state = ChainState(
            position=initial_position,
            log_density=results.accepted_results.target_log_prob,
            log_density_grad=results.accepted_results.grads_target_log_prob,
        )
        kernel_state = results

        return chain_state, kernel_state

    def step_fn(target_log_prob_fn, chain_and_kernel_state, seed):
        chain_state, kernel_state = chain_and_kernel_state

        # Pack kernel state into results here
        seed = tfp.random.sanitize_seed(seed)

        kernel = _build_kernel(
            target_log_prob_fn,
            _make_momentum_distribution(chain_state.position),
        )

        new_position, results = kernel.one_step(
            chain_state.position,
            kernel.bootstrap_results(chain_state.position),
            seed,
        )

        info = results

        chain_state = ChainState(
            position=new_position,
            log_density=results.accepted_results.target_log_prob,
            log_density_grad=results.accepted_results.grads_target_log_prob,
        )

        return (chain_state, results), info

    return SamplingAlgorithm(init_fn, step_fn)
