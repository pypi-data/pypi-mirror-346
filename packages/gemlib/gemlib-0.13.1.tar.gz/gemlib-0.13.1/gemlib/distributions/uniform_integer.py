"""The UniformInteger distribution class"""

import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import (
    dtype_util,
    parameter_properties,
    reparameterization,
    samplers,
)

tfd = tfp.distributions


class UniformInteger(tfd.Distribution):
    def __init__(
        self,
        low,
        high,
        validate_args=False,
        allow_nan_stats=True,
        float_dtype=tf.float32,
        name="UniformInteger",
    ):
        """Integer uniform distribution.

        Args:
        ----
          low: Integer tensor, lower boundary of the output interval. Must have
            `low <= high`.
          high: Integer tensor, _inclusive_ upper boundary of the output
            interval.  Must have `low <= high`.
          validate_args: Python `bool`, default `False`. When `True`
            distribution parameters are checked for validity despite possibly
            degrading runtime performance. When `False` invalid inputs may
            silently render incorrect outputs.
          allow_nan_stats: Python `bool`, default `True`. When `True`,
           statistics (e.g., mean, mode, variance) use the value "`NaN`" to
           indicate the result is undefined. When `False`, an exception is
           raised if one or more of the statistic's batch members are undefined.
          dtype: returned integer dtype when sampling.
          float_dtype: returned float dtype of log probability.
          name: Python `str` name prefixed to Ops created by this class.

        Example 1: sampling
        ```python
        import tensorflow as tf
        from gemlib.distributions.uniform_integer import UniformInteger

        tf.random.set_seed(10402302)
        X = UniformInteger(0, 10, dtype=tf.int32)
        x = X.sample([3, 3], seed=1)
        tf.print("samples:", x, "=", [[8, 4, 8], [2, 7, 9], [6, 0, 9]])
        ```

        Example 2: log probability
        ```python
        import tensorflow as tf
        from gemlib.distributions.uniform_integer import UniformInteger

        X = UniformInteger(0, 10, float_dtype=tf.float32)
        lp = X.log_prob([[8, 4, 8], [2, 7, 9], [6, 0, 9]])
        total_lp = tf.math.round(tf.math.reduce_sum(lp) * 1e5) / 1e5
        tf.print("total lp:", total_lp, "= -20.72327")
        ```

        Raises:
        ------
          InvalidArgument if `low > high` and `validate_args=False`.

        """
        parameters = dict(locals())
        with tf.name_scope(name):
            dtype = dtype_util.common_dtype([low, high], tf.int32)
            self._low = tf.convert_to_tensor(low)
            self._high = tf.convert_to_tensor(high)

            super().__init__(
                dtype=dtype,
                reparameterization_type=reparameterization.FULLY_REPARAMETERIZED,
                validate_args=validate_args,
                allow_nan_stats=allow_nan_stats,
                parameters=parameters,
                name=name,
            )
        if validate_args is True:
            tf.assert_greater(
                self.high, self.low, "Condition low < high failed"
            )

    @classmethod
    def _parameter_properties(cls, dtype, num_classes=None):  # noqa: ARG003
        return {
            "low": parameter_properties.ParameterProperties(
                default_constraining_bijector_fn=parameter_properties.BIJECTOR_NOT_IMPLEMENTED,
            ),
            "high": parameter_properties.ParameterProperties(
                default_constraining_bijector_fn=parameter_properties.BIJECTOR_NOT_IMPLEMENTED,
            ),
        }

    @property
    def low(self):
        """Lower boundary of the output interval."""
        return self._low

    @property
    def high(self):
        """Upper boundary of the output interval."""
        return self._high

    @property
    def float_dtype(self):
        return self._parameters["float_dtype"]

    def _event_shape_tensor(self):
        return tf.constant([], dtype=tf.int32)

    def _event_shape(self):
        return tf.TensorShape([])

    def _sample_n(self, n, seed=None):
        with tf.name_scope("sample_n"):
            low = tf.convert_to_tensor(self.low)
            high = tf.convert_to_tensor(self.high)
            shape = tf.concat(
                [[n], self._batch_shape_tensor(low=low, high=high)], axis=0
            )
            samples = samplers.uniform(shape=shape, dtype=tf.float32, seed=seed)

            return low + tf.cast(
                tf.cast(high - low, tf.float32) * samples,
                low.dtype,
            )

    def _prob(self, x):
        with tf.name_scope("prob"):
            low = tf.cast(self.low, self.float_dtype)
            high = tf.cast(self.high, self.float_dtype)
            x = tf.cast(x, dtype=self.float_dtype)

            return tf.where(
                tf.math.is_nan(x),
                x,
                tf.where(
                    (x < low) | (x >= high),
                    tf.zeros_like(x),
                    tf.ones_like(x) / (high - low),
                ),
            )

    def _log_prob(self, x):
        with tf.name_scope("log_prob"):
            res = tf.math.log(self._prob(x))
            return res
