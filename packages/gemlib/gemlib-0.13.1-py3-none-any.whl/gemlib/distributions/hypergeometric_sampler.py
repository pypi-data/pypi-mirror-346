"""Hypergeometric sampling algorithm"""

# ruff: noqa: N803

import numpy as np
import tensorflow as tf
from tensorflow_probability.python.internal import (
    batched_rejection_sampler as brs,
)
from tensorflow_probability.python.internal import (
    dtype_util,
    samplers,
    tensor_util,
)
from tensorflow_probability.python.internal import prefer_static as ps


def sample_hypergeometric(num_samples, N, K, n, seed=None):
    dtype = dtype_util.common_dtype([N, K, n], tf.float32)
    N = tensor_util.convert_nonref_to_tensor(N, dtype, name="N")
    K = tensor_util.convert_nonref_to_tensor(K, dtype, name="K")
    n = tensor_util.convert_nonref_to_tensor(n, dtype, name="n")
    good_params_mask = (N >= 1.0) & (N >= K) & (n <= N)
    N = tf.where(good_params_mask, N, 100.0)
    K = tf.where(good_params_mask, K, 50.0)
    n = tf.where(good_params_mask, n, 50.0)
    sample_shape = ps.concat(
        [
            [num_samples],
            ps.broadcast_shape(
                ps.broadcast_shape(ps.shape(N), ps.shape(K)), ps.shape(n)
            ),
        ],
        axis=0,
    )

    # First Transform N, K, n such that
    # N / 2 >= K, N / 2 >= n
    is_k_small = 0.5 * N >= K
    is_n_small = n <= 0.5 * N
    previous_K = K
    previous_n = n
    K = tf.where(is_k_small, K, N - K)
    n = tf.where(is_n_small, n, N - n)

    # TODO: Can we write this in a more numerically stable way?
    def _log_hypergeometric_coeff(x):
        return (
            tf.math.lgamma(x + 1.0)
            + tf.math.lgamma(K - x + 1.0)
            + tf.math.lgamma(n - x + 1.0)
            + tf.math.lgamma(N - K - n + x + 1.0)
        )

    p = K / N
    q = 1 - p
    a = n * p + 0.5
    c = tf.math.sqrt(2.0 * a * q * (1.0 - n / N))
    k = tf.math.floor((n + 1) * (K + 1) / (N + 2))
    g = _log_hypergeometric_coeff(k)
    diff = tf.math.floor(a - c)
    x = (a - diff - 1) / (a - diff)
    diff = tf.where(
        (n - diff) * (p - diff / N) * tf.math.square(x)
        > (diff + 1.0) * (q - (n - diff - 1) / N),
        diff + 1.0,
        diff,
    )
    # TODO: Can we write this difference of lgammas more numerically stably?
    h = (a - diff) * tf.math.exp(
        0.5 * (g - _log_hypergeometric_coeff(diff)) + np.log(2.0)
    )
    b = tf.math.minimum(tf.math.minimum(n, K) + 1, tf.math.floor(a + 5 * c))

    def generate_and_test_samples(seed):
        v_seed, u_seed = samplers.split_seed(seed)
        U = samplers.uniform(sample_shape, dtype=dtype, seed=u_seed)
        V = samplers.uniform(sample_shape, dtype=dtype, seed=v_seed)
        # Guard against 0.

        X = a + h * (V - 0.5) / (1.0 - U)
        samples = tf.math.floor(X)
        good_sample_mask = (samples >= 0.0) & (samples < b)
        T = g - _log_hypergeometric_coeff(samples)
        # Uses slow pass since we are trying to do this in a vectorized way.
        good_sample_mask = good_sample_mask & (2 * tf.math.log1p(-U) <= T)
        return samples, good_sample_mask

    samples = brs.batched_las_vegas_algorithm(
        generate_and_test_samples, seed=seed
    )[0]
    samples = tf.where(good_params_mask, samples, np.nan)
    # Now transform the samples depending on if we constrained N and / or k
    samples = tf.where(
        ~is_k_small & ~is_n_small,
        samples + previous_K + previous_n - N,
        tf.where(
            ~is_k_small,
            previous_n - samples,
            tf.where(~is_n_small, previous_K - samples, samples),
        ),
    )
    return samples
