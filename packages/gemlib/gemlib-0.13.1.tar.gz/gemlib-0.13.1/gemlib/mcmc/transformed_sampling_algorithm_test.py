"""Test transform_sampling_algorithm"""

import numpy as np
import pytest
import scipy as sp
import tensorflow as tf
import tensorflow_probability as tfp

from gemlib.mcmc.mcmc_sampler import mcmc
from gemlib.mcmc.random_walk_metropolis import rwmh
from gemlib.mcmc.transformed_sampling_algorithm import (
    _transform_tlp_fn,
    transform_sampling_algorithm,
)

tfd = tfp.distributions
tfb = tfp.bijectors


def is_same_shape(x, y):
    return tf.reduce_all(
        tf.nest.flatten(
            tf.nest.map_structure(lambda a, b: tf.shape(a) == tf.shape(b), x, y)
        )
    )


def test_gradients_exist():
    """Check gradients are not None for transformed tlp"""

    def log_prob_fn(x, y):
        return tfd.Gamma(concentration=2, rate=2).log_prob(x) + tfd.Normal(
            loc=0, scale=1.5
        ).log_prob(y)

    transformed_log_prob_fn = _transform_tlp_fn(
        bijectors=[tfb.Exp(), tfb.Identity()],
        target_log_prob_fn=log_prob_fn,
        disable_bijector_caching=True,
    )

    output = tfp.math.value_and_gradient(transformed_log_prob_fn, *(1.0, 1.0))

    assert all(x is not None for x in tf.nest.flatten(output))


def test_sampling_algorithm(evaltest):
    Y = tfd.LogNormal(loc=0.0, scale=1.0)

    kernel = transform_sampling_algorithm(
        tfb.Exp(),
        rwmh(scale=0.1),
    )

    (cs, ks) = evaltest(lambda: kernel.init(Y.log_prob, 2.0))
    (cs1, ks1), info = evaltest(
        lambda: kernel.step(Y.log_prob, (cs, ks), seed=[0, 0])
    )

    tf.nest.assert_same_structure(cs, cs1)
    tf.nest.assert_same_structure(ks, ks1)
    assert is_same_shape(
        cs, cs1
    ), f"Shapes differ.\n\nFirst structure: {cs}\n\nSecond structure: {cs1}"
    assert is_same_shape(ks, ks1)

    eps = 1.0e-6

    assert np.abs(cs.log_density - Y.log_prob(2.0)) < eps
    assert np.abs(cs1.log_density - Y.log_prob(cs1.position)) < eps


@pytest.mark.parametrize("evaltest", ["graph", "jit_compile"], indirect=True)
def test_transformed_mcmc(evaltest):
    """Draw samples from a lognormal distribution using
    a log-transformed RWMH kernel"""

    Y = tfd.LogNormal(loc=0.0, scale=1.0)

    kernel = transform_sampling_algorithm(
        tfb.Exp(),
        rwmh(scale=3.0),
    )

    samples, results = evaltest(
        lambda: mcmc(
            5000,
            sampling_algorithm=kernel,
            target_density_fn=Y.log_prob,
            initial_position=1.0,
            seed=[0, 0],
        )
    )
    accept_rate = 0.4
    eps = 0.1
    assert (np.mean(results.is_accepted) - accept_rate) < eps

    ks = sp.stats.kstest(
        samples.numpy()[::10], sp.stats.lognorm.cdf, args=(1.0,)
    )
    alpha = 0.05
    assert ks.pvalue > alpha


@pytest.mark.parametrize("evaltest", ["graph", "jit_compile"], indirect=True)
def test_transformed_mcmc_2d(evaltest):
    """Draw samples from a bivariate Gamma distribution"""

    def log_prob(x, y):
        return tf.reduce_sum(
            tfd.Gamma(concentration=[2, 2], rate=[2, 2]).log_prob([x, y])
        )

    kernel = transform_sampling_algorithm(
        [tfb.Exp(), tfb.Exp()], rwmh(scale=[1.5, 1.5])
    )

    samples, results = evaltest(
        lambda: mcmc(
            5000,
            sampling_algorithm=kernel,
            target_density_fn=log_prob,
            initial_position=[1.0, 1.0],
            seed=[0, 0],
        )
    )

    accept_rate = 0.3
    eps = 0.1
    assert np.abs(np.mean(results.is_accepted) - accept_rate) < eps

    ks0 = sp.stats.kstest(
        samples[0].numpy()[::10],
        sp.stats.gamma.cdf,
        args=(2.0, 0.0, 0.5),
    ).pvalue
    ks1 = sp.stats.kstest(
        samples[1].numpy()[::10],
        sp.stats.gamma.cdf,
        args=(2.0, 0.0, 0.5),
    ).pvalue

    alpha = 0.05

    assert ks0 > alpha
    assert ks1 > alpha


@pytest.mark.parametrize("evaltest", ["graph", "jit_compile"], indirect=True)
def test_partial_transformed_mcmc_2d(evaltest):
    """Compute gradients for transformed kernels"""

    # create a target log prob function
    def log_prob(x, y):
        return tfd.Gamma(concentration=2, rate=2).log_prob(x) + tfd.Normal(
            loc=0, scale=1.5
        ).log_prob(y)

    kernel = transform_sampling_algorithm(
        [tfb.Exp(), tfb.Identity()], rwmh(scale=[2.0, 2.0])
    )

    samples, results = evaltest(
        lambda: mcmc(
            10000,
            sampling_algorithm=kernel,
            target_density_fn=log_prob,
            initial_position=[1.0, 1.0],
            seed=[0, 0],
        )
    )

    accept_rate = 0.3
    eps = 0.1
    assert np.abs(np.mean(results.is_accepted) - accept_rate) < eps

    ks0 = sp.stats.kstest(
        samples[0].numpy()[::10],
        sp.stats.gamma.cdf,
        args=(2.0, 0.0, 0.5),
    ).pvalue
    ks1 = sp.stats.kstest(
        samples[1].numpy()[::10],
        sp.stats.norm.cdf,
        args=(0.0, 1.5),
    ).pvalue

    alpha = 0.05

    assert ks0 > alpha
    assert ks1 > alpha
