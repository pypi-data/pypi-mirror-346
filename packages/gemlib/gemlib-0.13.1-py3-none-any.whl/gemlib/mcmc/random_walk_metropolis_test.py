"""Test the random walk metropolis kernel"""

import numpy as np
import pytest
import tensorflow as tf
import tensorflow_probability as tfp

from gemlib.mcmc.mcmc_sampler import mcmc
from gemlib.mcmc.mwg_step import MwgStep
from gemlib.mcmc.random_walk_metropolis import RwmhInfo, rwmh

NUM_SAMPLES = 1000


def split_seed(seed, n):
    n = tf.convert_to_tensor(n)
    return tfp.random.split_seed(seed, n=n)


def tree_map(fn, *args, **kwargs):
    return tf.nest.map_structure(fn, *args, **kwargs)


def tree_flatten(tree):
    return tf.nest.flatten(tree)


def get_seed():
    # jax.random.PRNGKey(42)
    return [0, 0]


def compare_shape_and_dtype(x, y):
    x = tf.convert_to_tensor(x)
    y = tf.convert_to_tensor(y)

    is_same_dtype = x.dtype == y.dtype
    is_same_shape = x.shape == y.shape

    return is_same_dtype and is_same_shape


@tfp.distributions.JointDistributionCoroutine
def simple_model():
    yield tfp.distributions.Normal(loc=0.0, scale=1.0, name="foo")
    yield tfp.distributions.Normal(loc=1.0, scale=1.0, name="bar")
    yield tfp.distributions.Normal(loc=2.0, scale=1.0, name="baz")


def test_rwmh_1kernel():
    seed = get_seed()

    initial_position = simple_model.sample(seed=seed)

    kernel = rwmh(scale=0.3)

    state = kernel.init(simple_model.log_prob, initial_position)
    new_state, results = kernel.step(simple_model.log_prob, state, seed)

    assert tree_map(lambda _1, _2: None, new_state, state)

    expected_results = RwmhInfo(
        is_accepted=True, proposed_state=new_state[0].position
    )
    assert all(
        tree_map(
            lambda x, y: compare_shape_and_dtype(x, y),
            results,
            expected_results,
        )
    )


def test_rwmh_2kernel():
    seed = get_seed()

    initial_position = simple_model.sample(seed=seed)

    kernel = MwgStep(rwmh(scale=0.3), ["foo"]) >> MwgStep(
        rwmh(scale=0.1), ["bar", "baz"]
    )

    state = kernel.init(simple_model.log_prob, initial_position)
    new_state, results = kernel.step(simple_model.log_prob, state, seed)

    assert tree_map(lambda *_: None, state, new_state)

    expected_results = [
        RwmhInfo(is_accepted=True, proposed_state=(0.1,)),
        RwmhInfo(is_accepted=True, proposed_state=(0.1, 0.1)),
    ]

    assert all(
        tree_map(
            compare_shape_and_dtype,
            expected_results,
            results,
            check_types=False,
        )
    )


def test_rwmh_3kernel():
    seed = get_seed()

    initial_position = simple_model.sample(seed=seed)

    kernel = (
        MwgStep(rwmh(scale=0.3), ["foo"])
        >> MwgStep(rwmh(scale=0.1), ["bar"])
        >> MwgStep(rwmh(scale=0.2), ["baz"])
    )

    state = kernel.init(simple_model.log_prob, initial_position)
    new_state, results = kernel.step(simple_model.log_prob, state, seed)

    assert tree_map(lambda *_: None, new_state, state)

    expected_results = [
        RwmhInfo(is_accepted=True, proposed_state=(0.1,)),
        RwmhInfo(is_accepted=True, proposed_state=(0.1,)),
        RwmhInfo(is_accepted=True, proposed_state=(0.1,)),
    ]
    assert all(
        tree_map(
            compare_shape_and_dtype,
            results,
            expected_results,
            check_types=False,
        )
    )


@pytest.mark.parametrize("evaltest", ["graph", "jit_compile"], indirect=True)
def test_rwmh_1kernel_mcmc(evaltest):
    seed = get_seed()

    initial_position = simple_model.sample(seed=seed)

    kernel = rwmh(scale=1.8)

    posterior, info = evaltest(
        lambda: mcmc(
            NUM_SAMPLES,
            sampling_algorithm=kernel,
            target_density_fn=simple_model.log_prob,
            initial_position=initial_position,
            seed=get_seed(),
        ),
    )

    # Test results
    np.testing.assert_approx_equal(
        np.mean(info.is_accepted), 0.23, significant=1
    )
    np.testing.assert_allclose(
        tree_map(lambda x: np.mean(x), posterior),
        [0.0, 1.0, 2.0],
        rtol=0.1,
        atol=0.3,
    )
    np.testing.assert_allclose(
        tree_map(lambda x: np.var(x), posterior),
        [1.0, 1.0, 1.0],
        rtol=0.1,
        atol=0.2,
    )


@pytest.mark.parametrize("evaltest", ["graph", "jit_compile"], indirect=True)
def test_rwmh_2kernel_mcmc(evaltest):
    seed = get_seed()

    initial_position = simple_model.sample(seed=seed)

    kernel = MwgStep(rwmh(scale=2.3), ["foo"]) >> MwgStep(
        rwmh(scale=1.8), ["bar", "baz"]
    )

    posterior, info = evaltest(
        lambda: mcmc(
            NUM_SAMPLES,
            sampling_algorithm=kernel,
            target_density_fn=simple_model.log_prob,
            initial_position=initial_position,
            seed=get_seed(),
        ),
    )

    # Test results
    np.testing.assert_allclose(
        [np.mean(x.is_accepted) for x in info],
        [0.45, 0.33],
        atol=0.05,
        rtol=0.15,
    )
    np.testing.assert_allclose(
        tree_map(lambda x: np.mean(x), posterior),
        [0.0, 1.0, 2.0],
        rtol=0.1,
        atol=0.2,
    )
    np.testing.assert_allclose(
        tree_map(lambda x: np.var(x), posterior),
        [1.0, 1.0, 1.0],
        rtol=0.1,
        atol=0.2,
    )


@pytest.mark.parametrize("evaltest", ["graph", "jit_compile"], indirect=True)
def test_rwmh_3kernel_mcmc(evaltest):
    seed = get_seed()

    initial_position = simple_model.sample(seed=seed)

    kernel = (
        MwgStep(rwmh(scale=2.3), ["foo"])
        >> MwgStep(rwmh(scale=2.3), ["bar"])
        >> MwgStep(rwmh(scale=2.3), ["baz"])
    )

    posterior, info = evaltest(
        lambda: mcmc(
            NUM_SAMPLES,
            sampling_algorithm=kernel,
            target_density_fn=simple_model.log_prob,
            initial_position=initial_position,
            seed=get_seed(),
        ),
    )

    # Test results
    np.testing.assert_allclose(
        [np.mean(x.is_accepted) for x in info],
        [0.45, 0.45, 0.45],
        atol=0.05,
        rtol=0.15,
    )
    np.testing.assert_allclose(
        tree_map(lambda x: np.mean(x), posterior),
        [0.0, 1.0, 2.0],
        rtol=0.1,
        atol=0.2,
    )
    np.testing.assert_allclose(
        tree_map(lambda x: np.var(x), posterior),
        [1.0, 1.0, 1.0],
        rtol=0.1,
        atol=0.2,
    )
