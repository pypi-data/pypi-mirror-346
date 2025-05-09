"""Test initial event times MH"""

# ruff: noqa: F401, F811

from functools import partial
from typing import NamedTuple

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp

from gemlib.distributions.discrete_markov import compute_state
from gemlib.mcmc.discrete_time_state_transition_model.left_censored_events_impl import (  # noqa: E501
    UncalibratedLeftCensoredEventTimesUpdate,
    _update_state,
)

from .fixtures import sir_metapop_example  # Todo: migrate to conftest


def test__update_state_fwd(sir_metapop_example):
    initial_conditions = sir_metapop_example["initial_conditions"]
    events = sir_metapop_example["events"][:, :7, :]
    incidence_matrix = sir_metapop_example["incidence_matrix"]

    # Move SE events from past into present
    update_mock = {
        "unit": tf.constant([0]),
        "timepoint": tf.constant([3]),
        "direction": tf.constant([0]),
        "num_events": tf.constant([5]),
    }
    new_initial_conditions, new_events = _update_state(
        update=update_mock,
        current_state=(initial_conditions, events),
        transition_idx=0,
        incidence_matrix=incidence_matrix,
    )

    # Test events
    assert new_events.numpy()[3, 0, 0] == (events[3, 0, 0] + 5)

    intended_initial_conditions = np.array(
        [[1004, 45, 0], [500, 20, 0], [250, 10, 0]], dtype=np.float32
    )
    new_initial_conditions = new_initial_conditions.numpy()
    np.testing.assert_array_equal(
        new_initial_conditions, intended_initial_conditions
    )

    # Move IR events from present into past
    update_mock = {
        "unit": [1],
        "timepoint": [4],
        "direction": [1],
        "num_events": [5],
    }
    new_initial_conditions, new_events = _update_state(
        update=update_mock,
        current_state=(initial_conditions, events),
        transition_idx=1,
        incidence_matrix=incidence_matrix,
    )
    # Test events
    assert new_events.dtype == events.dtype
    assert new_initial_conditions.dtype == initial_conditions.dtype
    assert new_events.numpy()[4, 1, 1] == (events[4, 1, 1] - 5)

    intended_initial_conditions = np.array(
        [[999, 50, 0], [500, 15, 5], [250, 10, 0]], dtype=np.float32
    )
    new_initial_conditions = new_initial_conditions.numpy()
    np.testing.assert_array_equal(
        new_initial_conditions, intended_initial_conditions
    )


class Position(NamedTuple):
    initial_conditions: np.array
    events: np.array


def test_left_censored_event_times_update(sir_metapop_example):
    def tlp(_1, _2):
        return np.float32(1.0)

    kernel = UncalibratedLeftCensoredEventTimesUpdate(
        target_log_prob_fn=tlp,
        transition_index=0,
        max_timepoint=6,
        max_events=10,
        incidence_matrix=sir_metapop_example["incidence_matrix"],
    )
    current_state = (
        sir_metapop_example["initial_conditions"],
        sir_metapop_example["events"],
    )

    results = kernel.bootstrap_results(current_state)

    for seed in range(19):
        current_state, results = kernel.one_step(
            current_state, results, [seed, seed + 1]
        )
    current_state = [x.numpy() for x in current_state]

    assert np.all(current_state[0] >= 0.0)
    assert np.all(current_state[1] >= 0.0)
