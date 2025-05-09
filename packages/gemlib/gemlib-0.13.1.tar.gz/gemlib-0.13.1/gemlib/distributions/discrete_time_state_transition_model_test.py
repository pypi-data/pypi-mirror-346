# Dependency imports
import numpy as np
import pytest
import tensorflow as tf
import tensorflow_probability as tfp

from gemlib.distributions.discrete_time_state_transition_model import (
    DiscreteTimeStateTransitionModel,
)


def test_simple_sir(evaltest, homogeneous_sir_params):
    model_params = homogeneous_sir_params()

    model = DiscreteTimeStateTransitionModel(**model_params)

    sim = evaltest(lambda: model.sample(seed=[0, 0]))
    evaltest(lambda: model.log_prob(sim))


def test_two_unit_sir(evaltest, two_unit_sir_params):
    model_params = two_unit_sir_params()

    model = DiscreteTimeStateTransitionModel(**model_params)

    sim = evaltest(lambda: model.sample(seed=[0, 0]))
    evaltest(lambda: model.log_prob(sim))


def test_log_prob_and_grads(evaltest, homogeneous_sir_params):
    model_params = homogeneous_sir_params()

    model = DiscreteTimeStateTransitionModel(**model_params)

    eventlist = evaltest(lambda: model.sample(seed=[0, 0]))

    lp_and_grads = evaltest(
        lambda: tfp.math.value_and_gradient(model.log_prob, eventlist)
    )

    assert lp_and_grads[0].dtype == model_params["initial_state"].dtype


def test_eventlist_shapes(evaltest, two_unit_sir_params):
    model_params = two_unit_sir_params()

    model = DiscreteTimeStateTransitionModel(**model_params)

    sim = evaltest(lambda: model.sample(seed=[0, 0]))

    expected_shape = tf.TensorShape(
        [
            model_params["num_steps"],  # T
            model_params["initial_state"].shape[0],  # M
            model_params["incidence_matrix"].shape[1],  # S
        ]
    )

    assert sim.shape == expected_shape
    assert model.num_units == model_params["initial_state"].shape[0]


def test_log_prob(evaltest, discrete_two_unit_sir_example):
    model_params = discrete_two_unit_sir_example["model_params"]

    model = DiscreteTimeStateTransitionModel(**model_params)

    lp = evaltest(lambda: model.log_prob(discrete_two_unit_sir_example["draw"]))

    actual_mean = discrete_two_unit_sir_example["log_prob"]

    assert np.abs(lp - actual_mean) / actual_mean < 1.0e-6  # noqa: PLR2004


def test_transition_prob_matrix(evaltest, discrete_two_unit_sir_example):
    model_params = discrete_two_unit_sir_example["model_params"]

    model = DiscreteTimeStateTransitionModel(**model_params)

    evaltest(lambda: model.transition_prob_matrix())

    evaltest(
        lambda: model.transition_prob_matrix(
            discrete_two_unit_sir_example["draw"]
        )
    )


@pytest.mark.parametrize("evaltest", ["graph", "jit_compile"], indirect=True)
def test_model_constraints(evaltest, homogeneous_sir_params):
    num_sim = 50
    model_params = homogeneous_sir_params()

    model = DiscreteTimeStateTransitionModel(**model_params)

    eventlist = evaltest(
        lambda: model.sample(sample_shape=num_sim, seed=[0, 0])
    )
    ts = evaltest(lambda: model.compute_state(eventlist))

    # Check states are positive
    assert (eventlist.numpy() >= 0.0).all()

    # Check dS/dt + dI/dt + dR/dt = 0 at each time point
    finite_diffs = tf.reduce_sum(
        (ts[:, 1:, ...] - ts[:, :-1, ...]) / model.time_delta
    )

    assert finite_diffs < 1e-06  # noqa: PLR2004


def test_log_prob_mle(evaltest, discrete_two_unit_sir_example):
    """Test maximum likelihood estimation"""

    model_params = discrete_two_unit_sir_example["model_params"]
    events = discrete_two_unit_sir_example["draw"]

    pars = tf.constant(
        list(discrete_two_unit_sir_example["true_params"].values()),
        discrete_two_unit_sir_example["dtype"],
    )

    def logp(_):
        model = DiscreteTimeStateTransitionModel(**model_params)
        return -model.log_prob(events)

    optim_results = evaltest(
        lambda: tfp.optimizer.nelder_mead_minimize(
            logp,
            initial_vertex=tf.zeros_like(pars),
            func_tolerance=1e-4,
        )
    )

    assert optim_results.converged == tf.constant(True)
    assert all((optim_results.position - pars) / pars < 0.1)  # noqa: PLR2004


if __name__ == "__main__":
    tf.test.main()
