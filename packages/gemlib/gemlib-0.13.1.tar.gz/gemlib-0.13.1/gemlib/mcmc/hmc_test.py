"""Tests for HMC sampler"""

import numpy as np
import pytest
import tensorflow as tf
import tensorflow_probability as tfp

from gemlib.mcmc.hmc import hmc
from gemlib.mcmc.mcmc_sampler import mcmc

tfd = tfp.distributions

NUM_SAMPLES = 5000


@pytest.fixture(params=[np.float32, np.float64])
def simple_model(request):
    dtype = request.param
    one = tf.constant(1.0, dtype)

    @tfp.distributions.JointDistributionCoroutine
    def model():
        yield tfp.distributions.Normal(
            loc=tf.constant(0.0, dtype), scale=one, name="foo"
        )
        yield tfp.distributions.Normal(loc=one, scale=one, name="bar")
        yield tfp.distributions.Normal(
            loc=tf.constant(2.0, dtype), scale=one, name="baz"
        )

    return model


def test_hmc(evaltest, simple_model):
    mcmc_init_state = simple_model.sample(seed=[0, 0])
    dtype = mcmc_init_state[0].dtype

    algorithm = hmc(step_size=tf.constant(0.1, dtype), num_leapfrog_steps=8)

    state = evaltest(
        lambda: algorithm.init(simple_model.log_prob, mcmc_init_state)
    )
    new_state, info = evaltest(
        lambda: algorithm.step(simple_model.log_prob, state, [0, 0])
    )

    tf.nest.assert_same_structure(state, new_state)


@pytest.mark.parametrize("evaltest", ["graph", "jit_compile"], indirect=True)
def test_hmc_mcmc(evaltest, simple_model):
    mcmc_init_state = simple_model.sample(seed=[0, 0])
    dtype = mcmc_init_state[0].dtype

    algorithm = hmc(step_size=tf.constant(1.2, dtype), num_leapfrog_steps=8)

    samples, info = evaltest(
        lambda: mcmc(
            NUM_SAMPLES,
            sampling_algorithm=algorithm,
            target_density_fn=simple_model.log_prob,
            initial_position=mcmc_init_state,
            seed=[0, 0],
        )
    )

    np.testing.assert_allclose(np.mean(info.is_accepted), 0.7, atol=0.1)
    np.testing.assert_allclose(
        np.array([np.mean(x) for x in samples]),
        np.array([0.0, 1.0, 2.0]),
        atol=1e-1,
    )
    np.testing.assert_allclose(
        np.array([np.var(x) for x in samples]),
        np.array([1.0, 1.0, 1.0]),
        atol=1e-1,
        rtol=1e-1,
    )
