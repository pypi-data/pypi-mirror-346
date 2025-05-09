"""Test the adaptive random walk metropolis sampling algorithm"""

import numpy as np
import pytest
import tensorflow as tf
import tensorflow_probability as tfp

from .adaptive_random_walk_metropolis import adaptive_rwmh
from .mcmc_sampler import mcmc

tfd = tfp.distributions

NUM_SAMPLES = 1000


@tfp.distributions.JointDistributionCoroutine
def simple_model():
    yield tfp.distributions.Normal(loc=0.0, scale=1.0, name="foo")
    yield tfp.distributions.Normal(loc=1.0, scale=1.0, name="bar")
    yield tfp.distributions.Normal(loc=2.0, scale=1.0, name="baz")


def get_seed():
    # jax.random.PRNGKey(42)
    return [0, 0]


def split_seed(seed, n):
    n = tf.convert_to_tensor(n)
    return tfp.random.split_seed(seed, n=n)


@pytest.mark.parametrize("dtype", [np.float32, np.float64])
def test_adaptive_rwmh_univariate_shapes(dtype, evaltest):
    distribution = tfd.Normal(
        loc=tf.constant(0.0, dtype), scale=tf.constant(1.0, dtype)
    )

    kernel = adaptive_rwmh(initial_scale=tf.constant(2.38, dtype))

    (cs, ks) = evaltest(
        lambda: kernel.init(distribution.log_prob, tf.constant(0.1, dtype))
    )
    (cs1, ks1), info = evaltest(
        lambda: kernel.step(distribution.log_prob, (cs, ks), seed=[0, 0])
    )

    tf.nest.assert_same_structure(
        cs, cs1, check_types=True, expand_composites=True
    )
    tf.nest.assert_same_structure(
        ks, ks1, check_types=True, expand_composites=True
    )


@pytest.mark.parametrize("dtype", [np.float32, np.float64])
def test_adaptive_rwmh_bivariate_shapes(dtype, evaltest):
    def log_prob(x1, x2):
        x1_lp = tfd.Normal(
            loc=tf.constant(0.0, dtype), scale=tf.constant(1.0, dtype)
        ).log_prob(x1)
        x2_lp = tfd.Normal(
            loc=tf.constant(1.0, dtype), scale=tf.constant(2.0, dtype)
        ).log_prob(x2)
        return x1_lp + x2_lp

    kernel = adaptive_rwmh(initial_scale=tf.constant(2.38, dtype))

    (cs, ks) = evaltest(
        lambda: kernel.init(
            log_prob, [tf.constant(0.1, dtype), tf.constant(1.1, dtype)]
        )
    )
    (cs1, ks1), info = evaltest(
        lambda: kernel.step(log_prob, (cs, ks), seed=[0, 0])
    )

    tf.nest.assert_same_structure(
        cs, cs1, check_types=True, expand_composites=True
    )
    tf.nest.assert_same_structure(
        ks, ks1, check_types=True, expand_composites=True
    )


@pytest.mark.parametrize("evaltest", ["graph", "jit_compile"], indirect=True)
@pytest.mark.parametrize("dtype", [np.float32, np.float64])
def test_adaptive_rwmh_univariate_mcmc(dtype, evaltest):
    distribution = tfd.Normal(
        loc=tf.constant(0.0, dtype), scale=tf.constant(1.0, dtype)
    )

    kernel = adaptive_rwmh(initial_scale=tf.constant(2.38, dtype))

    samples, info = evaltest(
        lambda: mcmc(
            2000,
            sampling_algorithm=kernel,
            target_density_fn=distribution.log_prob,
            initial_position=tf.constant(0.1, dtype),
            seed=[0, 0],
        )
    )

    accept_eps = 0.1
    assert np.abs(np.mean(info.is_accepted[1000:]) - 0.44) < accept_eps

    mean_eps = 0.2
    assert np.abs(np.mean(samples[1000:]) - 0.0) < mean_eps

    var_eps = 0.05
    assert np.abs(np.std(samples[1000:]) - 1.0) < var_eps


@pytest.mark.parametrize("evaltest", ["graph", "jit_compile"], indirect=True)
@pytest.mark.parametrize("dtype", [np.float32, np.float64])
def test_adaptive_rwmh_multivariate_mcmc(dtype, evaltest):
    def log_prob(x1, x2, x3):
        x1_lp = tfd.Normal(
            loc=tf.constant(0.0, dtype), scale=tf.constant(0.1, dtype)
        ).log_prob(x1)
        x2_lp = tfd.Normal(
            loc=tf.constant(1.0, dtype), scale=tf.constant(0.2, dtype)
        ).log_prob(x2)
        x3_lp = tfd.Normal(
            loc=tf.constant(2.0, dtype), scale=tf.constant(0.4, dtype)
        ).log_prob(x3)

        return x1_lp + x2_lp + x3_lp

    kernel = adaptive_rwmh(initial_scale=tf.constant(1.5, dtype))

    samples, info = evaltest(
        lambda: mcmc(
            2000,
            sampling_algorithm=kernel,
            target_density_fn=log_prob,
            initial_position=[
                tf.constant(0.1, dtype),
                tf.constant(-0.1, dtype),
                tf.constant(0.5, dtype),
            ],
            seed=[0, 0],
        )
    )

    accept_eps = 0.1
    assert np.abs(np.mean(info.is_accepted[1000:]) - 0.234) < accept_eps

    print("means: ", [np.mean(x[1000:]) for x in samples])
    mean_eps = 0.2
    assert all(
        np.abs(np.mean(x[1000:]) - y) / (y + 1) < mean_eps
        for x, y in zip(samples, [0.0, 1.0, 2.0], strict=True)
    )

    var_eps = 0.05
    assert all(
        np.abs(np.std(x[1000:]) - y) < var_eps
        for x, y in zip(samples, [0.1, 0.2, 0.4], strict=True)
    )
