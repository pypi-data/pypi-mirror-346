"""Test left-censored proposal mechanism"""

# ruff: noqa: F401,F811

import numpy as np
import tensorflow_probability as tfp

from .fixtures import sir_metapop_example
from .left_censored_events_proposal import (
    left_censored_event_time_proposal,
)


def test_initial_conditions_event_time_proposal(sir_metapop_example):
    proposer = left_censored_event_time_proposal(
        events=sir_metapop_example["events"],
        initial_state=sir_metapop_example["initial_conditions"],
        transition=np.int32(0),
        incidence_matrix=sir_metapop_example["incidence_matrix"],
        num_units=1,
        max_timepoint=5,
        max_events=5,
    )

    seeds = tfp.random.split_seed([0, 0], n=100)
    for seed in seeds:
        proposal = proposer.sample(seed=seed)

        assert proposal["unit"].shape == (1,)
        assert proposal["timepoint"].shape == (1,)
        assert proposal["direction"].shape == (1,)
        assert proposal["num_events"].shape == (1,)

    logp = proposer.log_prob(proposal)
    assert logp
