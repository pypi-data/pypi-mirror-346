"""Brownian motion as a distribution"""

import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import (
    distribution_util as dist_util,
)
from tensorflow_probability.python.internal import (
    dtype_util,
    reparameterization,
)
from tensorflow_probability.python.internal.tensor_util import (
    convert_nonref_to_tensor,
)

tfd = tfp.distributions


class BrownianMotion(tfd.Distribution):
    def __init__(
        self,
        index_points,
        x0=0.0,
        scale=1.0,
        validate_args=False,
        allow_nan_stats=True,
        name="BrownianMotion",
    ):
        parameters = dict(locals())
        dtype = dtype_util.common_dtype([x0, index_points, scale])
        self._x0 = convert_nonref_to_tensor(x0, dtype_hint=dtype)

        self._index_points = convert_nonref_to_tensor(
            index_points, dtype_hint=dtype
        )
        self._scale = tf.convert_to_tensor(scale, dtype_hint=dtype)

        self._increments = tfd.MultivariateNormalDiag(
            loc=tf.zeros_like(self._index_points[..., 1:]),
            scale_diag=tf.math.sqrt(
                self._index_points[..., 1:] - self._index_points[..., :-1]
            )
            * self._scale,
            validate_args=validate_args,
            allow_nan_stats=allow_nan_stats,
            name="bm_increments",
        )  # iid increments

        with tf.name_scope(name):
            super().__init__(
                dtype=dtype,
                reparameterization_type=reparameterization.FULLY_REPARAMETERIZED,
                validate_args=validate_args,
                allow_nan_stats=allow_nan_stats,
                parameters=parameters,
                name=name,
            )

    def _batch_shape(self):
        return tf.TensorShape(self._x0.shape)

    def _event_shape(self):
        return tf.TensorShape(self._index_points.shape[-1] - 1)

    def _sample_n(self, n, seed=None):
        return self._x0 + tf.math.cumsum(
            self._increments.sample(n, seed=seed), axis=-1
        )

    def _log_prob(self, x):
        path = dist_util.pad(x, axis=-1, front=True, value=self._x0)
        diff = path[..., 1:] - path[..., :-1]
        return self._increments.log_prob(diff)


class BrownianBridge(tfd.Distribution):
    def __init__(
        self,
        index_points,
        x0=0.0,
        x1=0.0,
        scale=1.0,
        validate_args=False,
        allow_nan_stats=True,
        name="BrownianBridge",
    ):
        parameters = dict(locals())
        dtype = dtype_util.common_dtype([index_points, x0, x1, scale])
        self._index_points = convert_nonref_to_tensor(
            index_points, dtype_hint=dtype
        )
        self._x0 = convert_nonref_to_tensor(x0, dtype_hint=dtype)
        self._x1 = convert_nonref_to_tensor(x1, dtype_hint=dtype)
        self._scale = convert_nonref_to_tensor(scale, dtype_hint=dtype)

        self._increments = tfd.MultivariateNormalDiag(
            loc=0.0,
            scale_diag=tf.math.sqrt(
                self._index_points[..., 1:] - self._index_points[..., :-1]
            )
            * self._scale,
            name="bb_increments",
        )

        with tf.name_scope(name):
            super().__init__(
                dtype=dtype,
                reparameterization_type=reparameterization.FULLY_REPARAMETERIZED,
                validate_args=validate_args,
                allow_nan_stats=allow_nan_stats,
                name=name,
            )

    def _batch_shape(self):
        return tf.TensorShape(self._x0.shape)

    def _event_shape(self):
        return tf.TensorShape(self._index_points.shape[-1] - 2)

    def _sample_n(self, n, seed=None):
        """Sampling based on re-leveling pure
        Brownian motion
        """
        z = self._increments.sample(n, seed=seed)
        z = tf.cumsum(z, axis=-1)

        y_ref_0 = tf.stack([tf.zeros_like(z[..., 0]), z[..., -1]], axis=-1)
        y_ref_1 = tf.stack([self._x0, self._x1], axis=-1)
        line = tfp.math.interp_regular_1d_grid(
            x=self._index_points[..., 1:-1],
            x_ref_min=self._index_points[..., 0],
            x_ref_max=self._index_points[..., -1],
            y_ref=y_ref_1 - y_ref_0,
        )
        return z[..., :-1] + line

    def _log_prob(self, x):
        path = dist_util.pad(x, -1, front=True, value=self._x0)
        path = dist_util.pad(path, -1, back=True, value=self._x1)
        diff = path[..., 1:] - path[..., :-1]
        return self._increments.log_prob(diff)
