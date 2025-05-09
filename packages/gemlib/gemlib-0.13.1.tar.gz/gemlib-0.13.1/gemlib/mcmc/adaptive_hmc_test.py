"""Tests for HMC sampler"""

from typing import NamedTuple

import numpy as np
import pytest
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import unnest

from gemlib.mcmc.adaptive_hmc import adaptive_hmc, make_initial_running_variance
from gemlib.mcmc.mcmc_sampler import mcmc
from gemlib.mcmc.sampling_algorithm import (
    ChainAndKernelState,
    ChainState,
    LogProbFnType,
    Position,
    SeedType,
)

tfd = tfp.distributions

NUM_SAMPLES = 5000


class ShimKernelState(NamedTuple):
    pass


class ShimKernelInfo(NamedTuple):
    pass


def shim_kernel():
    """Test shim to ensure that adaptive_hmc recalculates gradients
    if they are not included in the chain_state passed to `step`"""

    def init_fn(target_log_prob_fn: LogProbFnType, position: Position):
        chain_state = ChainState(
            position=position,
            log_density=target_log_prob_fn(*position),
            log_density_grad=(),
        )
        kernel_state = ShimKernelState()

        return ChainAndKernelState(chain_state, kernel_state)

    def step_fn(
        _target_log_prob_fn: LogProbFnType,
        chain_and_kernel_state: ChainAndKernelState,
        _seed: SeedType,
    ):
        cs, ks = chain_and_kernel_state

        next_cs = ChainState(
            position=cs.position,
            log_density=cs.log_density,
            log_density_grad=(),
        )

        return ChainAndKernelState(next_cs, ks), ShimKernelInfo()


@pytest.fixture(params=[np.float32, np.float64])
def test_initial_running_variance(request):
    dtype = request.param

    class Pos(NamedTuple):
        alpha: int
        beta: int

    position = Pos(
        np.array((0.0, 2.0), dtype=dtype), np.array(4.0, dtype=dtype)
    )
    variance = Pos(
        np.array((1.0, 5.0), dtype=dtype), np.array(10.0, dtype=dtype)
    )

    # Test with variance
    rv = make_initial_running_variance(position)
    assert rv.mean() == position
    assert rv.variance() == variance

    # Test without variance
    rv = make_initial_running_variance(position, variance)
    assert rv.mean() == position
    assert rv.variance() == variance


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


def test_adaptive_hmc(evaltest, simple_model):
    mcmc_init_state = simple_model.sample(seed=[0, 0])
    dtype = mcmc_init_state[0].dtype

    initial_running_variance = make_initial_running_variance(mcmc_init_state)

    algorithm = adaptive_hmc(
        initial_step_size=tf.constant(0.1, dtype),
        num_leapfrog_steps=8,
        num_step_size_adaptation_steps=NUM_SAMPLES // 3 + 50,
        num_mass_matrix_estimation_steps=NUM_SAMPLES // 3,
        initial_running_variance=initial_running_variance,
    )

    # Test init and step compatibility
    state = evaltest(
        lambda: algorithm.init(simple_model.log_prob, mcmc_init_state)
    )
    new_state, info = evaltest(
        lambda: algorithm.step(simple_model.log_prob, state, [0, 0])
    )

    tf.nest.assert_same_structure(state, new_state)

    # Test step recalculates gradients if they are missing
    state = state._replace(
        chain_state=state.chain_state._replace(log_density_grad=())
    )
    new_state, info = evaltest(
        lambda: algorithm.step(simple_model.log_prob, state, [0, 0])
    )
    assert new_state.chain_state.log_density_grad != ()


@pytest.mark.parametrize("evaltest", ["graph", "jit_compile"], indirect=True)
def test_adaptive_hmc_mcmc(evaltest, simple_model):
    mcmc_init_state = simple_model.sample(seed=[0, 0])
    dtype = mcmc_init_state[0].dtype

    initial_running_variance = make_initial_running_variance(mcmc_init_state)

    algorithm = adaptive_hmc(
        initial_step_size=tf.constant(0.1, dtype),
        num_leapfrog_steps=8,
        num_step_size_adaptation_steps=NUM_SAMPLES // 3 + 50,
        num_mass_matrix_estimation_steps=NUM_SAMPLES // 3,
        initial_running_variance=initial_running_variance,
    )

    samples, info = evaltest(
        lambda: mcmc(
            NUM_SAMPLES,
            sampling_algorithm=algorithm,
            target_density_fn=simple_model.log_prob,
            initial_position=mcmc_init_state,
            seed=[0, 0],
        )
    )

    np.testing.assert_allclose(
        np.mean(unnest.get_innermost(info, "is_accepted")), 0.7, atol=0.1
    )
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
