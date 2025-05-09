"""Right-censored events MCMC test"""

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp

from .right_censored_events_mh import right_censored_events_mh


def test_right_censored_events_mh(evaltest, seir_metapop_example):
    events = seir_metapop_example["events"]
    initial_conditions = seir_metapop_example["initial_conditions"]

    def tlp(_):
        return tf.constant(0.0, dtype=events.dtype)

    kernel = right_censored_events_mh(
        incidence_matrix=seir_metapop_example["incidence_matrix"],
        transition_index=0,
        count_max=10,
        t_range=(events.shape[0] - 7, events.shape[0]),
    )

    cs, ks = kernel.init(tlp, events, initial_conditions=initial_conditions)
    seed = [0, 0]
    (new_cs, new_ks), info = kernel.step(
        tlp, (cs, ks), seed, initial_conditions=initial_conditions
    )

    assert cs.position.shape == events.shape
    assert new_cs.position.shape == events.shape
    assert tf.nest.map_structure(lambda _1, _2: True, ks, new_ks)

    seeds = tfp.random.split_seed([0, 1], n=tf.constant(100))

    def one_step(chain_and_kernel_state, seed):
        new_chain_state, _ = kernel.step(
            tlp,
            chain_and_kernel_state,
            seed,
            initial_conditions=initial_conditions,
        )
        return new_chain_state

    cs, ks = evaltest(
        lambda: tf.scan(
            one_step,
            elems=seeds,
            initializer=kernel.init(
                tlp, events, initial_conditions=initial_conditions
            ),
        ),
    )

    samples = cs.position

    tf.debugging.assert_non_negative(samples)
    assert np.mean((samples[1:] - samples[:-1]) ** 2) > 0.0
