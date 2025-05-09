"""Test the Hypergeometric random vaiable"""

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import test_util

from gemlib.distributions.hypergeometric import Hypergeometric

tfd = tfp.distributions


@test_util.test_all_tf_execution_regimes
class TestHypergeometric(test_util.TestCase):
    def setUp(self):
        self._rng = np.random.RandomState(5)
        super().setUp()

    def test_neg_args(self):
        """Test for invalid arguments"""
        with self.assertRaisesRegex(
            tf.errors.InvalidArgumentError, "N must be non-negative"
        ):
            self.evaluate(Hypergeometric(N=-3, K=1, n=2, validate_args=True))

    def test_sample_n_float32(self):
        """Sample returning float32 args"""

        X = Hypergeometric(345.0, 35.0, 100.0)
        x = X.sample([1000, 1000], seed=1)

        x = self.evaluate(x)
        self.assertDTypeEqual(x, np.float32)
        self.assertAllClose(tf.reduce_mean(x), X.mean(), atol=1e-3, rtol=1e-3)

    def test_sample_n_float64(self):
        """Sample returning float32 args"""

        X = Hypergeometric(
            np.float64(345.0), np.float64(35.0), np.float64(100.0)
        )
        x = X.sample([1000, 1000], seed=1)

        x = self.evaluate(x)
        self.assertDTypeEqual(x, np.float64)
        self.assertAllClose(tf.reduce_mean(x), X.mean(), atol=1e-3, rtol=1e-3)
