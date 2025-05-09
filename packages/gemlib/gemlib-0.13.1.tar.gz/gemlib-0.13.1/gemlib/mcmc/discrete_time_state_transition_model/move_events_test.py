"""Test partially censored events move for DiscreteTimeStateTransitionModel"""

import numpy as np
import pytest
import tensorflow as tf
import tensorflow_probability as tfp

from gemlib.mcmc.discrete_time_state_transition_model.move_events import (
    move_events,
)


@pytest.fixture
def random_events():
    """SEIR model with prescribed starting conditions"""
    events = tf.random.uniform(
        [10, 10, 3], minval=0, maxval=100, dtype=tf.float64, seed=0
    )
    return events


@pytest.fixture
def initial_state():
    popsize = tf.fill([10], tf.constant(100.0, tf.float64))
    initial_state = tf.stack(
        [
            popsize,
            tf.ones_like(popsize),
            tf.zeros_like(popsize),
            tf.zeros_like(popsize),
        ],
        axis=-1,
    )
    return initial_state


@pytest.mark.parametrize("evaltest", ["graph", "jit_compile"], indirect=True)
def test_move_events(evaltest, seir_metapop_example):
    def tlp(_):
        return tf.constant(0.0, dtype=seir_metapop_example["events"].dtype)

    kernel = move_events(
        seir_metapop_example["incidence_matrix"],
        transition_index=1,
        num_units=1,
        delta_max=4,
        count_max=10,
    )

    (cs, ks) = kernel.init(
        target_log_prob_fn=tlp,
        position=seir_metapop_example["events"],
        initial_conditions=seir_metapop_example["initial_conditions"],
    )
    seed = [0, 0]
    (new_cs, new_ks), info = kernel.step(
        tlp, (cs, ks), seed, seir_metapop_example["initial_conditions"]
    )

    assert cs.position.shape == seir_metapop_example["events"].shape
    assert new_cs.position.shape == seir_metapop_example["events"].shape
    assert tf.nest.map_structure(lambda _1, _2: True, ks, new_ks)

    seeds = tfp.random.split_seed([0, 1], n=tf.constant(100))

    def one_step(chain_and_kernel_state, seed):
        new_chain_state, _ = kernel.step(
            tlp,
            chain_and_kernel_state,
            seed,
            seir_metapop_example["initial_conditions"],
        )
        return new_chain_state

    cs, ks = evaltest(
        lambda: tf.scan(
            one_step,
            elems=seeds,
            initializer=kernel.init(
                tlp,
                seir_metapop_example["events"],
                seir_metapop_example["initial_conditions"],
            ),
        )
    )
    samples = cs.position
    tf.debugging.assert_non_negative(samples)
    assert np.mean((samples[1:] - samples[:-1]) ** 2) > 0.0
