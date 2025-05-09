"""Test Initial Conditions sampler"""

from typing import NamedTuple

import numpy as np
import pytest
import tensorflow as tf

from .left_censored_events_mh import left_censored_events_mh


class ExampleEventsInitCond(NamedTuple):
    seir_events: tf.Tensor
    seir_initial_state: tf.Tensor


class TestLeftCensoredEventsMH:
    """Test left censored event times Metropolis-Hastings"""

    @pytest.fixture(scope="class")
    def state(self, seir_metapop_example):
        return ExampleEventsInitCond(
            seir_metapop_example["events"],
            seir_metapop_example["initial_conditions"],
        )

    @pytest.fixture(scope="class")
    def tlp(self, seir_metapop_example):
        def fn(*_):
            return tf.constant(0.0, dtype=seir_metapop_example["events"].dtype)

        return fn

    @pytest.fixture(scope="class")
    def kernel(self, seir_metapop_example):
        kernel = left_censored_events_mh(
            incidence_matrix=seir_metapop_example["incidence_matrix"],
            transition_index=1,
            max_timepoint=7,
            max_events=10,
            events_varname="seir_events",
            initial_conditions_varname="seir_initial_state",
            name="test_left_censored_events_mh",
        )

        return kernel

    def test_shape(self, state, tlp, kernel):
        """Test that shapes do not get altered in the kernel"""
        cs, ks = kernel.init(tlp, state)
        seed = [0, 0]
        (new_cs, new_ks), info = kernel.step(tlp, (cs, ks), seed)

        assert cs.position.seir_events.shape == state.seir_events.shape
        assert (
            cs.position.seir_initial_state.shape
            == state.seir_initial_state.shape
        )
        assert tf.nest.map_structure(lambda *_: True, ks, new_ks)

    def test_mcmc(self, state, tlp, kernel):
        """Test that multiple invocations of the kernel result in valid
        event timeseries, and also definitely move around.
        """
        seeds = tf.random.split([0, 1], num=100)

        def one_step(chain_and_kernel_state, seed):
            new_chain_state, _ = kernel.step(tlp, chain_and_kernel_state, seed)
            return new_chain_state

        cs, ks = tf.function(
            lambda: tf.scan(
                one_step, elems=seeds, initializer=kernel.init(tlp, state)
            ),
            jit_compile=True,
        )()

        samples = cs.position

        tf.debugging.assert_non_negative(samples.seir_events)
        tf.debugging.assert_non_negative(samples.seir_initial_state)

        assert (
            np.mean((samples.seir_events[1:] - samples.seir_events[:-1]) ** 2)
            > 0.0
        )
        assert (
            np.mean(
                (
                    samples.seir_initial_state[1:]
                    - samples.seir_initial_state[:-1]
                )
                ** 2
            )
            > 0.0
        )
