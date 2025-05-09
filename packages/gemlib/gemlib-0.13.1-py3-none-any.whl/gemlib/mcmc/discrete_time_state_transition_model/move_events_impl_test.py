"""Test event time samplers"""

# ruff: noqa: PLR2004

import pytest
import tensorflow as tf
import tensorflow_probability as tfp

from gemlib.distributions.discrete_markov import compute_state
from gemlib.mcmc.discrete_time_state_transition_model.move_events_impl import (
    UncalibratedEventTimesUpdate,
    discrete_move_events_proposal,
    events_state_count_bounding_fn,
)


def test_discrete_move_events_proposal(evaltest, sir_metapop_example):
    num_units = 2

    proposal = discrete_move_events_proposal(
        incidence_matrix=sir_metapop_example["incidence_matrix"],
        target_transition_id=1,
        num_units=num_units,
        delta_max=4,
        count_max=10,
        initial_conditions=sir_metapop_example["initial_conditions"],
        events=sir_metapop_example["events"],
        count_bounding_fn=events_state_count_bounding_fn(10),
        name="foo",
    )

    sample = evaltest(lambda: proposal.sample(seed=[0, 1]))
    lp = evaltest(lambda: proposal.log_prob(sample))

    assert sample._fields == ("unit", "timepoint", "delta", "event_count")
    assert sample.unit.shape == (num_units,)
    assert sample.timepoint.shape == (num_units,)
    assert sample.delta.shape == (num_units,)
    assert sample.event_count.shape == (num_units,)

    for k, v in sample._asdict().items():
        assert v.dtype == tf.int32, f"Field `{k}` is not int32"

    assert lp.shape == ()
    assert lp.dtype == sir_metapop_example["incidence_matrix"].dtype


@pytest.mark.parametrize("evaltest", ["graph", "jit_compile"], indirect=True)
def test_uncalibrated_event_time_update(evaltest, sir_metapop_example):
    def tlp(_):
        return tf.constant(0.0, sir_metapop_example["events"].dtype)

    print(
        "sir_metapop_example['events'].shape:",
        sir_metapop_example["events"].shape,
    )
    kernel = UncalibratedEventTimesUpdate(
        target_log_prob_fn=tlp,
        incidence_matrix=sir_metapop_example["incidence_matrix"],
        initial_conditions=sir_metapop_example["initial_conditions"],
        target_transition_id=1,
        delta_max=4,
        num_units=1,
        count_max=10,
    )

    # Test structures are consistent
    pkr = evaltest(
        lambda: kernel.bootstrap_results(sir_metapop_example["events"])
    )
    next_events, results = evaltest(
        lambda: kernel.one_step(
            sir_metapop_example["events"],
            pkr,
            seed=tfp.random.sanitize_seed([0, 0]),
        )
    )
    tf.nest.assert_same_structure(pkr, results, check_types=True)
    tf.nest.assert_same_structure(
        sir_metapop_example["events"], next_events, check_types=True
    )

    # Test that multiple invocations of the kernel do not
    # allow the state to go negative, even if the tlp is not
    # there to guide the sampler.
    seeds = tf.stack(tfp.random.split_seed([0, 1], n=100), axis=0)

    def one_step(state, seed):
        new_state = kernel.one_step(*state, seed=seed)
        return new_state

    events, results = evaltest(
        lambda: tf.scan(
            one_step,
            elems=seeds,
            initializer=(sir_metapop_example["events"], pkr),
        )
    )

    tf.debugging.assert_non_negative(events)
    tf.debugging.assert_non_negative(
        compute_state(
            initial_state=sir_metapop_example["initial_conditions"],
            events=events,
            incidence_matrix=sir_metapop_example["incidence_matrix"],
            closed=True,
        )
    )
