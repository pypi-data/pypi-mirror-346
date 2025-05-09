"""Adaptive Hamiltonian Monte Carlo sampling algorithm"""

from enum import IntEnum

import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.experimental.stats import RunningVariance
from tensorflow_probability.python.internal import unnest

from gemlib.mcmc.sampling_algorithm import (
    ChainAndKernelState,
    ChainState,
    LogProbFnType,
    Position,
    SamplingAlgorithm,
    SeedType,
)

__all__ = [
    "RunningVariance",
    "StepSizeAlgorithm",
    "make_initial_running_variance",
    "adaptive_hmc",
]


# Base samplers
class StepSizeAlgorithm(IntEnum):
    SIMPLE = 0
    NESTEROV = 1


PreconditionedHMC = tfp.experimental.mcmc.PreconditionedHamiltonianMonteCarlo
StepSizeKernels = [
    tfp.mcmc.SimpleStepSizeAdaptation,
    tfp.mcmc.DualAveragingStepSizeAdaptation,
]
MassMatrixAdaptation = tfp.experimental.mcmc.DiagonalMassMatrixAdaptation


def make_initial_running_variance(
    position: Position, variance: Position = None
):
    def fn(x, v):
        x = tf.convert_to_tensor(x)
        return RunningVariance.from_stats(
            tf.constant(1.0, x.dtype), mean=x, variance=v
        )

    if variance is None:
        variance = tf.nest.map_structure(lambda x: tf.ones_like(x), position)

    return tf.nest.map_structure(fn, position, variance)


def adaptive_hmc(
    initial_step_size: float,
    num_leapfrog_steps: int,
    num_step_size_adaptation_steps: int,
    num_mass_matrix_estimation_steps: int,
    initial_running_variance: RunningVariance,
    step_size_algorithm: StepSizeAlgorithm = StepSizeAlgorithm.NESTEROV,
    step_size_kwargs: dict | None = None,
) -> SamplingAlgorithm:
    """Adaptive Hamiltonian Monte Carlo sampler

    Implements a Hamiltonian Monte Carlo sampler with adaptive step size
    and mass matrix.

    Args:
      initial_step_size: the initial step size
      num_leapfrog_steps: number of leapfrog steps to perform
      num_step_size_adaptation_steps: the number of steps before adaptation
        stops
      num_mass_matrix_estimation_steps: the number of steps before mass matrix
        estimation stops
      initial_running_variance: an initial running variance, constructed using
        :class:`make_initial_running_variance`
      step_size_algorithm: the algorithm used to adapt the step size
      step_size_kwargs: arguments to pass to the step size adaptation kernel
      name: the name of the kernel

    Returns:
      a SamplingAlgorithm implementing an adaptive Hamiltonian Monte Carlo
      sampler
    """

    if step_size_kwargs is None:
        step_size_kwargs = {}

    def _build_kernel(target_log_prob_fn: LogProbFnType):
        base_hmc_kernel = PreconditionedHMC(
            target_log_prob_fn=target_log_prob_fn,
            step_size=initial_step_size,
            num_leapfrog_steps=num_leapfrog_steps,
            store_parameters_in_results=True,
        )

        StepSizeAlg = StepSizeKernels[step_size_algorithm]
        step_size_adapt = StepSizeAlg(
            inner_kernel=base_hmc_kernel,
            num_adaptation_steps=num_step_size_adaptation_steps,
            **step_size_kwargs,
        )

        kernel = tfp.experimental.mcmc.DiagonalMassMatrixAdaptation(
            inner_kernel=step_size_adapt,
            initial_running_variance=initial_running_variance,
            num_estimation_steps=num_mass_matrix_estimation_steps,
        )

        return kernel

    def init_fn(target_log_prob_fn: LogProbFnType, initial_position: Position):
        kernel = _build_kernel(target_log_prob_fn)
        results = kernel.bootstrap_results(initial_position)

        # Repack the results data structure into our own
        chain_state = ChainState(
            position=initial_position,
            log_density=unnest.get_innermost(results, "target_log_prob"),
            log_density_grad=tuple(
                unnest.get_innermost(results, "grads_target_log_prob")
            ),
        )

        return ChainAndKernelState(chain_state, results)

    def step_fn(
        target_log_prob_fn: LogProbFnType,
        chain_and_kernel_state: ChainAndKernelState,
        seed: SeedType,
    ):
        chain_state, kernel_state = chain_and_kernel_state

        seed = tfp.random.sanitize_seed(seed)

        kernel = _build_kernel(
            target_log_prob_fn,
        )

        # If grads have not been forwarded, recompute them
        if chain_state.log_density_grad == ():
            _, log_density_grad = tfp.math.value_and_gradient(
                target_log_prob_fn,
                *chain_state.position,
            )
        else:
            log_density_grad = chain_state.log_density_grad

        next_results = unnest.replace_innermost(
            kernel_state,
            target_log_prob=chain_state.log_density,
            grads_target_log_prob=list(log_density_grad),
        )

        new_position, results = kernel.one_step(
            chain_state.position,
            next_results,
            seed,
        )

        info = results

        chain_state = ChainState(
            position=new_position,
            log_density=unnest.get_innermost(results, "target_log_prob"),
            log_density_grad=tuple(
                unnest.get_innermost(results, "grads_target_log_prob")
            ),
        )

        return ChainAndKernelState(chain_state, results), info

    return SamplingAlgorithm(init_fn, step_fn)
