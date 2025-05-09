"""An adaptive random walk Metropolis Hastings algorithm"""

from typing import NamedTuple

import tensorflow as tf
import tensorflow_probability as tfp

from .mcmc_util import get_flattening_bijector, is_list_like
from .sampling_algorithm import (
    ChainState,
    LogProbFnType,
    Position,
    SamplingAlgorithm,
)

tfd = tfp.distributions

RunningCovariance = tfp.experimental.stats.RunningCovariance
Tensor = tf.Tensor


class AdaptiveRwmhKernelState(NamedTuple):
    scale: float
    adaptation_quantity: float
    running_covariance: RunningCovariance
    is_adaptive: bool
    is_accepted: bool
    num_steps: bool


class AdaptiveRwmhInfo(NamedTuple):
    scale: float
    adaptation_quantity: float
    running_covariance: RunningCovariance
    is_adaptive: bool
    is_accepted: bool
    num_steps: bool
    proposed_state: Tensor
    log_acceptance: Tensor


def adaptive_rwmh(
    initial_scale: float = 0.1,
    initial_running_covariance: Tensor | None = None,
    lambda0: float = 0.1,
    adapt_prob: float = 0.95,
) -> SamplingAlgorithm:
    """An Adaptive Random Walk Metropolis Hastings algorithm

    This algorithm implements an adaptive random walk Metropolis
    Hastings algorithm as described in Sherlock et al. 2010.

    Args:
      initial_scale: the initial value of the covariance scalar
      initial_running_covariance: an initial covariance matrix of shape `[p,p]`
                                where `p` is the length of the vector of
                                concatenated parameters
      lambda0: the scaling for the non-adaptive covariance matrix
      adapt_prob: probability we draw using the adaptive covariance matrix
      adaptation_quantity: the amount to add or subtract from the covariance
                           scaling parameter.  Defaults to `2.38/d^{-1/2}`.
      name: an optional name for the kernel

    Returns:
      A :obj:`SamplingAlgorithm`

    References:
      Chris Sherlock, Paul Fearnhead, Gareth O. Roberts. "The Random Walk
      Metropolis: Linking Theory and Practice Through a Case Study."
      Statistical Science, 25(2) 172-190 May 2010.
    """

    def init_fn(target_log_prob_fn: LogProbFnType, position: Position):
        position_parts = position if is_list_like(position) else [position]

        # Flatten and concatenate
        flattening_bijector = get_flattening_bijector(position_parts)
        flat_position = flattening_bijector(position_parts)
        flat_size = flat_position.shape[-1]

        # The initial_variance has 3 possibilities:
        # 1. a scalar, which is broadcast down the diagonal of
        #    the covariance matrix.
        # 2. a structure compatible with `position` of elements
        #    corresponding to variances of each variable in `position`.
        # 3. a full covariance matrix of dimension `(flat_position.shape[-1],
        #    flat_position.shape[-1])` giving the covariance matrix for all
        #    parameters in the flattened and concatenated `position`.

        if initial_running_covariance is None:
            initial_running_covariance_ = (
                tfp.experimental.stats.RunningCovariance(
                    num_samples=10,
                    mean=flat_position,
                    sum_squared_residuals=0.1
                    * tf.linalg.diag(tf.ones_like(flat_position)),
                    event_ndims=1,
                )
            )
        else:
            initial_running_covariance_ = initial_running_covariance

        if initial_scale is None:
            initial_scale_ = 2.38 / tf.math.sqrt(
                tf.cast(flat_size, flat_position.dtype)
            )
        else:
            initial_scale_ = tf.convert_to_tensor(
                initial_scale, flat_position.dtype
            )

        chain_state = ChainState(
            position=position_parts
            if is_list_like(position)
            else position_parts[0],
            log_density=target_log_prob_fn(*position_parts),
            log_density_grad=(),
        )

        kernel_state = AdaptiveRwmhKernelState(
            scale=initial_scale_,
            adaptation_quantity=initial_scale_ / 100.0,
            running_covariance=initial_running_covariance_,
            is_adaptive=False,
            is_accepted=False,
            num_steps=tf.constant(0, tf.int32),
        )

        return chain_state, kernel_state

    def step_fn(target_log_prob_fn, chain_and_kernel_state, seed):
        mh_seed, adapt_seed, accept_seed = tfp.random.split_seed(seed, n=3)

        cs, ks = chain_and_kernel_state

        position_parts = (
            cs.position if is_list_like(cs.position) else [cs.position]
        )

        flatten = get_flattening_bijector(position_parts)
        flat_position = flatten(position_parts)
        flat_size = flat_position.shape[-1]
        dtype = flat_position.dtype

        # Update the covariance matrix
        next_running_covariance = ks.running_covariance.update(flat_position)
        next_adapt_scale = tf.where(
            ks.is_accepted,
            ks.scale
            + 2.3  # Magic number from Alg 6 of Sherlock et al.
            * ks.adaptation_quantity
            / tf.math.sqrt(tf.cast(ks.num_steps, dtype)),
            ks.scale
            - ks.adaptation_quantity
            / tf.math.sqrt(tf.cast(ks.num_steps, dtype)),
        )
        next_scale = tf.where(ks.is_adaptive, next_adapt_scale, ks.scale)

        # Covariances
        static_covariance = tf.linalg.diag(
            tf.ones_like(flat_position) / flat_size * lambda0**2
        )
        adaptive_covariance = (
            next_scale**2 * next_running_covariance.covariance()
        )

        # Choose either scaled empirical covariance or static covariance
        is_adaptive = tfd.Bernoulli(probs=adapt_prob, dtype=tf.bool).sample(
            seed=adapt_seed
        )
        covariance_matrix = tf.where(
            is_adaptive,
            adaptive_covariance,
            static_covariance,
        )

        # Do the proposal
        flat_proposed_position = tfd.MultivariateNormalTriL(
            loc=flat_position,
            scale_tril=tf.linalg.cholesky(covariance_matrix),
        ).sample(seed=mh_seed)

        # Accept/reject
        proposed_log_prob = target_log_prob_fn(
            *flatten.inverse(flat_proposed_position)
        )
        log_acceptance = proposed_log_prob - cs.log_density
        is_accept = tfd.Bernoulli(
            probs=tf.math.exp(log_acceptance), dtype=tf.bool
        ).sample(seed=accept_seed)
        next_position = tf.where(
            is_accept, flat_proposed_position, flat_position
        )
        next_log_prob = tf.where(is_accept, proposed_log_prob, cs.log_density)

        next_position = flatten.inverse(next_position)
        if not is_list_like(cs.position):
            next_position = next_position[0]

        new_chain_state = ChainState(
            position=next_position,
            log_density=next_log_prob,
            log_density_grad=(),
        )

        new_kernel_state = ks._replace(
            scale=next_scale,
            running_covariance=next_running_covariance,
            is_adaptive=is_adaptive,
            is_accepted=is_accept,
            num_steps=ks.num_steps + 1,
        )

        return (new_chain_state, new_kernel_state), AdaptiveRwmhInfo(
            *new_kernel_state,
            proposed_state=flatten.inverse(flat_proposed_position),
            log_acceptance=log_acceptance,
        )

    return SamplingAlgorithm(init_fn, step_fn)
