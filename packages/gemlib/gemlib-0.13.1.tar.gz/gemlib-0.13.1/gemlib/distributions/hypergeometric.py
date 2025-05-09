"""Hypergeometric random variable"""

# ruff: noqa: N803, N802

import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import (
    dtype_util,
    parameter_properties,
    reparameterization,
)

from gemlib.distributions.hypergeometric_sampler import sample_hypergeometric

tfd = tfp.distributions

__all__ = ["Hypergeometric"]


def _log_factorial(x):
    """Computes x!"""
    return tf.math.lgamma(x + 1.0)


def _log_choose(n, k):
    """Computes nCk"""
    return _log_factorial(n) - _log_factorial(k) - _log_factorial(n - k)


class Hypergeometric(tfd.Distribution):
    def __init__(
        self,
        N,
        K,
        n,
        validate_args=False,
        allow_nan_stats=True,
        name="Hypergeometric",
    ):
        """Hypergeometric distribution

        Args:
        ----
          N: Population size
          K: number of units of interest in the population
          n: size of sample drawn from the population
          validate_args: should arguments be validated for correctness
          allow_nan_stats: allow NaN to be returned for mode, mean, variance...

        """
        parameters = dict(locals())
        with tf.name_scope(name):
            dtype = dtype_util.common_dtype([N, K, n], tf.float32)
            self._N = tf.cast(N, dtype=dtype)
            self._K = tf.cast(K, dtype=dtype)
            self._n = tf.cast(n, dtype=dtype)
            self._n_positive_mask = N > 0.0
            super().__init__(
                dtype=dtype,
                reparameterization_type=reparameterization.FULLY_REPARAMETERIZED,
                validate_args=validate_args,
                allow_nan_stats=allow_nan_stats,
                parameters=parameters,
                name=name,
            )
            if validate_args is True:
                tf.debugging.assert_non_negative(
                    N, message="N must be non-negative"
                )
                tf.debugging.assert_less_equal(K, N, message="K must be <= N")
                tf.debugging.assert_less_equal(n, N, message="n must be <= N")

    @classmethod
    def _parameter_properties(cls, dtype, num_classes=None):  # noqa: ARG003
        return {
            "N": parameter_properties.ParameterProperties(
                default_constraining_bijector_fn=parameter_properties.BIJECTOR_NOT_IMPLEMENTED
            ),
            "K": parameter_properties.ParameterProperties(),
            "n": parameter_properties.ParameterProperties(),
        }

    @staticmethod
    def _param_shapes(sample_shape):
        return dict(
            zip(
                ("N", "K", "n"),
                ([tf.convert_to_tensor(sample_shape, dtype=tf.int32)] * 3),
                strict=False,
            )
        )

    @classmethod
    def _params_event_ndims(cls):
        return {"N": 0, "K": 0, "n": 0}

    @property
    def N(self):
        """Population size"""
        return self._parameters["N"]

    @property
    def K(self):
        """Number of units of interest in population"""
        return self._parameters["K"]

    @property
    def n(self):
        """Sample size"""
        return self._parameters["n"]

    def _default_event_space_bijector(self):
        return

    def _event_shape_tensor(self):
        return tf.constant([], dtype=tf.int32)

    def _event_shape(self):
        return tf.TensorShape([])

    def _sample_n(self, n, seed=None):
        with tf.name_scope(self.name + "/sample_n"):
            sample = sample_hypergeometric(n, self.N, self.K, self.n, seed=seed)
            sample = tf.where(self._n_positive_mask, sample, 0.0)
            return sample

    def _log_prob(self, x):
        numerator = _log_choose(self._K, x) + _log_choose(
            self._N - self._K, self._n - x
        )
        denominator = _log_choose(self._N, self._n)
        return numerator - denominator

    def _mode(self):
        return tf.math.floor((self._n + 1) * (self._K + 1) / (self._N + 2))

    def _mean(self):
        return self._n * self._K / self._N

    def _variance(self):
        n = self._n
        N = self._N
        K = self._K

        return n * (K / N) * (N - K) / N * (N - n) / (N - 1)
