"""Transform a sampling algorithm"""

from typing import Callable, Iterable  # noqa: UP035

import tensorflow as tf

from gemlib.mcmc.mcmc_util import is_list_like

from .sampling_algorithm import (
    ChainAndKernelState,
    ChainState,
    LogProbFnType,
    Position,
    SamplingAlgorithm,
    SeedType,
)


def _transform_tlp_fn(
    bijectors: list, target_log_prob_fn: Callable, disable_bijector_caching=True
):
    if not is_list_like(bijectors):
        bijectors = [bijectors]

    def fn(*transformed_position):
        if disable_bijector_caching:
            transformed_position = tf.nest.map_structure(
                lambda x: tf.identity(x),
                transformed_position,
            )

        untransformed_position = tf.nest.map_structure(
            lambda x, bij: bij.forward(x),
            transformed_position,
            bijectors,
            check_types=False,
        )
        tlp = target_log_prob_fn(*untransformed_position) - tf.reduce_sum(
            tf.nest.map_structure(
                lambda x, bij: bij.inverse_log_det_jacobian(x),
                untransformed_position,
                bijectors,
                check_types=False,
            )
        )

        return tlp

    return fn


def transform_sampling_algorithm(
    bijectors: Iterable, sampling_algorithm: SamplingAlgorithm
):
    r"""Transform a sampling algorithm.

    This wrapper transforms `sampling_algorithm` with respect to the
    probability measure on which it acts.  `transform_sampling_algorithm`
    is particularly useful for unbounding parameter spaces in order to use
    algorithms such as Hamiltonian Monte Carlo or the No-U-Turn-Samplers (NUTS).

    It does this by applying the change-of-variables formula, such that for
    :math:`Y = g(X)`,

    .. math::

      f_Y(y)=f_X(g^{-1}(y))\left|\frac{\mathrm{d}g^{-1}(y)}{\mathrm{d}y}\right|

    Args:
      bijectors: a structure of TensorFlow Probability bijectors compatible with
               `position`
      sampling_algorithm: a sampling algorithm

    Returns:
      A new :obj:`SamplingAlgorithm` representing a kernel working on the
      transformed space.

    Examples:
        Instantiate a transformed hmc kernel::

          import tensorflow_probability as tfp
          from gemlib.mcmc import transform_sampling_algorithm
          from gemlib.mcmc import hmc

          kernel = transform_sampling_algorithm(
              bijectors=[tfp.bijectors.Exp(), tfp.bijectors.Exp()],
              sampling_algorithm=hmc(step_size=0.1, num_leapfrog_steps=16),
          )
    """

    def init_fn(
        target_log_prob_fn: LogProbFnType, position: Position, **kwargs
    ):
        transformed_tlp = _transform_tlp_fn(bijectors, target_log_prob_fn)

        transformed_position = tf.nest.map_structure(
            lambda x, bij: bij.inverse(x),
            position,
            bijectors,
            check_types=False,
        )
        chain_state, kernel_state = sampling_algorithm.init(
            transformed_tlp, transformed_position, **kwargs
        )

        new_chain_state = ChainState(
            position=position,
            log_density=chain_state.log_density
            + tf.reduce_sum(
                tf.nest.map_structure(
                    lambda bij, x: bij.inverse_log_det_jacobian(x),
                    bijectors,
                    position,
                    check_types=False,
                )
            ),
            log_density_grad=(),
        )

        return new_chain_state, kernel_state

    def step_fn(
        target_log_prob_fn: LogProbFnType,
        chain_and_kernel_state: ChainAndKernelState,
        seed: SeedType,
        **kwargs,
    ):
        chain_state, kernel_state = chain_and_kernel_state

        # Transform to a unconstrained space (inverse transform)
        transformed_tlp_fn = _transform_tlp_fn(bijectors, target_log_prob_fn)
        transformed_position = tf.nest.map_structure(
            lambda x, bij: bij.inverse(x),
            chain_state.position,
            bijectors,
            check_types=False,
        )
        transformed_tlp = chain_state.log_density + tf.reduce_sum(
            tf.nest.map_structure(
                lambda x, bij: bij.inverse_log_det_jacobian(x),
                chain_state.position,
                bijectors,
                check_types=False,
            )
        )

        transformed_chain_state = ChainState(
            position=transformed_position,
            log_density=transformed_tlp,
            log_density_grad=(),
        )
        (new_chain_state, new_kernel_state), info = sampling_algorithm.step(
            transformed_tlp_fn,
            (transformed_chain_state, kernel_state),
            seed=seed,
            **kwargs,
        )

        # Transform back to the constrained space
        constrained_new_position = tf.nest.map_structure(
            lambda x, bij: bij.forward(x),
            new_chain_state.position,
            bijectors,
            check_types=False,
        )
        constrained_log_density = new_chain_state.log_density + tf.reduce_sum(
            tf.nest.map_structure(
                lambda x, bij: bij.inverse_log_det_jacobian(x),
                constrained_new_position,
                bijectors,
                check_types=False,
            )
        )
        new_chain_state = ChainState(
            position=constrained_new_position,
            log_density=constrained_log_density,
            log_density_grad=(),
        )

        return (new_chain_state, new_kernel_state), info

    return SamplingAlgorithm(init_fn, step_fn)
