"""Test event time samplers"""

# ruff: noqa: PLR2004

import numpy as np
import pytest
import tensorflow as tf
import tensorflow_probability as tfp

from gemlib.distributions.discrete_markov import compute_state
from gemlib.mcmc.discrete_time_state_transition_model.right_censored_events_impl import (  # noqa: E501
    UncalibratedOccultUpdate,
    _add_events,
)
from gemlib.mcmc.discrete_time_state_transition_model.right_censored_events_proposal import (  # noqa: E501
    _slice_min,
    add_occult_proposal,
    del_occult_proposal,
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


def test_slice_min():
    min_unit_0 = _slice_min([0, 1, 2, 3, 4], 2)
    min_unit_1 = _slice_min([5, 6, 7, 8, 9], 3)

    # noqa: PLR2004
    assert min_unit_0 == 2
    assert min_unit_1 == 8


def test_add_occult_proposal(evaltest, discrete_two_unit_sir_example):
    model_params = discrete_two_unit_sir_example["model_params"]

    incidence_matrix = model_params["incidence_matrix"]
    initial_state = model_params["initial_state"]

    events = discrete_two_unit_sir_example["draw"]

    state = compute_state(initial_state, events, incidence_matrix)
    si_events = events[..., 0]
    s_state = state[..., 0]

    proposal = add_occult_proposal(
        count_max=10,
        events=si_events,
        src_state=s_state,
    )

    simple_proposal = evaltest(lambda: proposal.sample(seed=[0, 0]))
    simple_lp = evaltest(lambda: proposal.log_prob(simple_proposal))

    # Shapes
    assert simple_proposal.unit.shape == ()
    assert simple_proposal.timepoint.shape == ()
    assert simple_proposal.event_count.shape == ()
    assert np.isfinite(simple_lp)

    def propose_and_apply(_):
        move = proposal.sample(seed=[0, 0])
        new_events = _add_events(
            events=events,
            unit=move.unit,
            timepoint=move.timepoint,
            target_transition_id=0,
            event_count=move.event_count,
        )
        new_state = compute_state(initial_state, new_events, incidence_matrix)
        return new_events, new_state, move.event_count

    proposals = evaltest(
        lambda: tf.vectorized_map(propose_and_apply, elems=tf.range(100))
    )

    tf.debugging.assert_non_negative(proposals[0])
    tf.debugging.assert_non_negative(proposals[1])


def test_del_occult_proposal(evaltest, discrete_two_unit_sir_example):
    model_params = discrete_two_unit_sir_example["model_params"]

    incidence_matrix = model_params["incidence_matrix"]
    initial_state = model_params["initial_state"]

    events = discrete_two_unit_sir_example["draw"]

    state = compute_state(initial_state, events, incidence_matrix)

    si_events = events[..., 0]
    i_state = state[..., 1]

    proposal = del_occult_proposal(
        count_max=10,
        events=si_events,
        dest_state=i_state,
    )

    simple_proposal = evaltest(lambda: proposal.sample(seed=[0, 0]))
    simple_lp = evaltest(lambda: proposal.log_prob(simple_proposal))

    # Shapes
    assert simple_proposal.unit.shape == ()
    assert simple_proposal.timepoint.shape == ()
    assert simple_proposal.event_count.shape == ()
    assert np.isfinite(simple_lp)

    def propose_and_apply(_):
        move = proposal.sample(seed=[0, 0])
        new_events = _add_events(
            events=events,
            unit=move.unit,
            timepoint=move.timepoint,
            target_transition_id=0,
            event_count=-move.event_count,
        )
        new_state = compute_state(initial_state, new_events, incidence_matrix)
        return new_events, new_state, move.event_count

    proposals = evaltest(
        lambda: tf.vectorized_map(propose_and_apply, elems=tf.range(100))
    )

    tf.debugging.assert_non_negative(proposals[0])
    tf.debugging.assert_non_negative(proposals[1])


@pytest.mark.parametrize("evaltest", ["graph", "jit_compile"], indirect=True)
def test_uncalibrated_occults_update(evaltest, discrete_two_unit_sir_example):
    dtype = discrete_two_unit_sir_example["dtype"]

    model_params = discrete_two_unit_sir_example["model_params"]

    incidence_matrix = model_params["incidence_matrix"]
    initial_state = model_params["initial_state"]
    transitions = tf.convert_to_tensor(discrete_two_unit_sir_example["draw"])[
        :14
    ]

    num_times = transitions.shape[-3]

    kernel = UncalibratedOccultUpdate(
        target_log_prob_fn=lambda _: tf.constant(1.0, dtype),
        incidence_matrix=incidence_matrix,
        initial_conditions=initial_state,
        target_transition_id=0,
        count_max=10,
        t_range=[0, num_times],
        name="test_uncalibrated_occults_update",
    )

    def test_fn(position):
        init_results = kernel.bootstrap_results(position)
        print("init_results:", init_results)

        def scan_fn(a, x):
            return kernel.one_step(*a, seed=x)

        return tf.scan(
            scan_fn,
            elems=tf.unstack(tfp.random.split_seed([0, 0], n=500), axis=-1),
            initializer=(position, init_results),
        )

    samples, results = evaltest(lambda: test_fn(transitions))

    tf.debugging.assert_non_negative(samples)
    assert np.mean(results.event_count) > 0.0
