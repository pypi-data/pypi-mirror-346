"""Test ContinuousTimeStateTransitionModel"""

from collections import namedtuple

import numpy as np
import pytest
import tensorflow as tf
import tensorflow_probability as tfp

from gemlib.distributions.continuous_time_state_transition_model import (
    ContinuousTimeStateTransitionModel,
    EventList,
    compute_state,
)

NUM_STEPS = 1999
MIN_EPIDEMIC_LEN = 10
tfd = tfp.distributions


@pytest.fixture
def example_ilm():
    """A simple event list with 4 units, SIR model"""
    return {
        "incidence_matrix": np.array(
            [[-1, 0], [1, -1], [0, 1]], dtype=np.float32
        ),
        "event_list": EventList(
            time=np.array(
                [0.4, 1.3, 1.5, 1.9, 2.3, np.inf, np.inf], dtype=np.float32
            ),
            transition=np.array([0, 0, 1, 1, 1, 2, 2], dtype=np.int32),
            unit=np.array([1, 2, 0, 2, 1, 0, 0], dtype=np.int32),
        ),
        "initial_conditions": np.array(
            [[0, 1, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0]], dtype=np.float32
        ),
    }


@pytest.fixture
def simple_sir_model():
    def rate_fn(_, state):
        si_rate = 0.25 * state[:, 1] / tf.reduce_sum(state, axis=-1)
        ir_rate = tf.broadcast_to([0.14], si_rate.shape)

        return si_rate, ir_rate

    # [3 species, 2 reactions]
    incidence_matrix = np.array([[-1, 0], [1, -1], [0, 1]], dtype=np.float32)

    initial_state = np.array(
        [[999, 1, 0]], dtype=np.float32
    )  # [1 unit, 3 classes]

    return ContinuousTimeStateTransitionModel(
        transition_rate_fn=rate_fn,
        incidence_matrix=incidence_matrix,
        initial_state=initial_state,
        num_steps=NUM_STEPS,
        initial_time=0.0,
    )


@pytest.fixture
def bayesian_sir_model():
    DTYPE = np.float32

    @tfd.JointDistributionCoroutine
    def model():
        # Priors
        beta = yield tfd.Gamma(
            concentration=DTYPE(0.1),
            rate=DTYPE(0.1),
            name="beta",
        )
        gamma = yield tfd.Gamma(
            concentration=DTYPE(2.0), rate=DTYPE(8.0), name="gamma"
        )

        # Epidemic model
        incidence_matrix = np.array(
            [  #  SI  IR
                [-1, 0],  # S
                [1, -1],  # I
                [0, 1],  # R
            ],
            dtype=DTYPE,
        )

        initial_state = np.array([[99, 1, 0]]).astype(DTYPE)

        def transition_rates(_, state):
            si_rate = beta * state[:, 1] / tf.reduce_sum(state, axis=-1)
            ir_rate = tf.fill((state.shape[0],), gamma)
            return si_rate, ir_rate

        NUM_STEPS = 200

        yield ContinuousTimeStateTransitionModel(
            transition_rate_fn=transition_rates,
            incidence_matrix=incidence_matrix,
            initial_state=initial_state,
            num_steps=NUM_STEPS,
            name="sir",
        )

    ModelType = namedtuple("StructTuple", ["beta", "gamma", "sir"])

    example = ModelType(
        beta=0.5,
        gamma=0.14,
        sir=EventList(
            time=np.array(
                [ 3.8722684,  4.0912385,  4.5234103,  4.722512 ,  4.9462056,
                  5.7793403,  5.7914076,  6.028009 ,  6.1961355,  6.8580866,
                  7.6919003,  7.8862953,  8.106527 ,  8.489728 ,  8.565479 ,
                  8.710205 ,  8.7175045,  8.807663 ,  8.824789 ,  8.863979 ,
                  9.035543 ,  9.428677 ,  9.470956 ,  9.492353 ,  9.529175 ,
                  9.57752  ,  9.618181 ,  9.834693 ,  9.88009  ,  9.963752 ,
                  10.158042 , 10.233447 , 10.283622 , 10.464923 , 10.472176 ,
                  10.509909 , 10.713008 , 10.932794 , 10.937864 , 11.025746 ,
                  11.3029   , 11.452712 , 11.45593  , 11.801975 , 11.944026 ,
                  12.169918 , 12.2015085, 12.289305 , 12.379549 , 12.658843 ,
                  12.673543 , 12.675543 , 12.758116 , 12.839079 , 12.887654 ,
                  13.002403 , 13.063832 , 13.06984  , 13.204261 , 13.279876 ,
                  13.368993 , 13.465008 , 13.545585 , 13.6250305, 13.652922 ,
                  13.6884165, 13.722584 , 13.7678585, 13.773789 , 13.814655 ,
                  13.861033 , 14.0029125, 14.039422 , 14.068574 , 14.082346 ,
                  14.352536 , 14.35859  , 14.422744 , 14.575989 , 14.657471 ,
                  14.69332  , 14.700054 , 14.848383 , 14.882924 , 15.0288925,
                  15.093655 , 15.108234 , 15.236706 , 15.322691 , 15.328567 ,
                  15.404174 , 15.421979 , 15.657191 , 15.922981 , 15.9314375,
                  16.213312 , 16.311094 , 16.331137 , 16.50571  , 16.542715 ,
                  16.634466 , 16.743319 , 16.77621  , 16.864067 , 17.02836  ,
                  17.149601 , 17.375605 , 17.418259 , 17.424673 , 17.46273  ,
                  17.503548 , 17.648726 , 17.659864 , 17.879429 , 18.013472 ,
                  18.117981 , 18.781914 , 18.822414 , 18.923925 , 18.97823  ,
                  19.034103 , 19.124441 , 19.150362 , 19.70805  , 19.848843 ,
                  19.925968 , 19.967867 , 20.104042 , 20.159836 , 20.608583 ,
                  21.046917 , 21.156258 , 21.233568 , 21.242342 , 21.574625 ,
                  21.72764  , 21.865955 , 22.06923  , 22.242723 , 23.101812 ,
                  23.451588 , 23.622063 , 23.676891 , 23.758053 , 24.117605 ,
                  24.329521 , 25.265572 , 25.2762   , 25.319914 , 25.386583 ,
                  25.476671 , 25.518967 , 25.865902 , 26.031075 , 26.163708 ,
                  26.169014 , 26.238436 , 26.445032 , 26.973305 , 27.094973 ,
                  27.237108 , 27.26869  , 27.58751  , 27.857409 , 28.816969 ,
                  29.008768 , 29.6066   , 30.18358  , 31.610064 , 32.21432  ,
                  32.693485 , 33.329193 , 33.356907 , 33.576965 , 33.786686 ,
                  34.548702 , 35.99837  , 36.461132 , 36.63711  , 36.97347  ,
                  37.104862 , 38.354027 , 38.914967 , 39.609924 , 39.66717  ,
                  42.54664  , 42.610905 , 42.873867 , 43.515656 , 43.913628 ,
                  45.195133 , 45.952778 , 46.862324 , 47.602505 , 50.113663 ,
                  54.11174  , 56.933784 , np.inf, np.inf, np.inf,
                 ],
                dtype=np.float32,
            ),
            transition=np.array(
              [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
               1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1,
               1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1,
               0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1,
               0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1,
               1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1,
               0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0,
               0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1,
               1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 2,
               2, 2,
               ],
               dtype=np.int32,
            ),
            unit=np.array(
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0,
              ],
              dtype=np.int32,
            ),
        )
    )  # fmt: skip

    return {"model": model, "example": example}


def test_simple_sir_shapes(simple_sir_model):
    """Test expected output shape"""
    tf.debugging.assert_equal(
        simple_sir_model.event_shape_tensor(),
        EventList(
            tf.constant(NUM_STEPS),
            tf.constant(NUM_STEPS),
            tf.constant(NUM_STEPS),
        ),
    )
    tf.debugging.assert_equal(
        simple_sir_model.event_shape,
        EventList(
            tf.TensorShape([NUM_STEPS]),
            tf.TensorShape([NUM_STEPS]),
            tf.TensorShape([NUM_STEPS]),
        ),
    )
    tf.debugging.assert_equal(
        simple_sir_model.batch_shape_tensor(),
        EventList(
            tf.constant([], tf.int32),
            tf.constant([], tf.int32),
            tf.constant([], tf.int32),
        ),
    )
    tf.debugging.assert_equal(
        simple_sir_model.batch_shape,
        EventList(tf.TensorShape([]), tf.TensorShape([]), tf.TensorShape([])),
    )


def test_simple_sir(evaltest, simple_sir_model):
    """Test a simple SIR model"""

    sample = evaltest(lambda: simple_sir_model.sample(seed=[0, 0]))

    assert isinstance(sample, EventList)

    state = evaltest(lambda: simple_sir_model.compute_state(sample))

    tf.debugging.assert_non_negative(state)


def test_compute_state(evaltest, example_ilm):
    expected_state_eager = compute_state(
        example_ilm["incidence_matrix"],
        example_ilm["initial_conditions"],
        example_ilm["event_list"],
        include_final_state=True,
    )

    def compute_state_graph(*args):
        return compute_state(*args)

    expected_state_graph = evaltest(
        lambda: compute_state(
            example_ilm["incidence_matrix"],
            example_ilm["initial_conditions"],
            example_ilm["event_list"],
            True,
        )
    )

    actual_state = np.array(
        [
            [
                [0, 1, 0],  # T=0
                [1, 0, 0],
                [1, 0, 0],
                [1, 0, 0],
            ],
            [
                [0, 1, 0],  # T=1
                [0, 1, 0],
                [1, 0, 0],
                [1, 0, 0],
            ],
            [
                [0, 1, 0],  # T=2
                [0, 1, 0],
                [0, 1, 0],
                [1, 0, 0],
            ],
            [
                [0, 0, 1],  # T=3
                [0, 1, 0],
                [0, 1, 0],
                [1, 0, 0],
            ],
            [
                [0, 0, 1],  # T=4
                [0, 1, 0],
                [0, 0, 1],
                [1, 0, 0],
            ],
            [
                [0, 0, 1],  # T=5
                [0, 0, 1],
                [0, 0, 1],
                [1, 0, 0],
            ],
            [
                [0, 0, 1],  # T=6
                [0, 0, 1],
                [0, 0, 1],
                [1, 0, 0],
            ],
            [
                [0, 0, 1],  # T=7
                [0, 0, 1],
                [0, 0, 1],
                [1, 0, 0],
            ],
        ],
        dtype=np.float32,
    )

    np.testing.assert_array_equal(expected_state_eager, actual_state)
    np.testing.assert_array_equal(expected_state_graph, actual_state)


def test_simple_sir_loglik(evaltest, example_ilm):
    """Test loglikelihood function"""
    # epi constants
    incidence_matrix = example_ilm["incidence_matrix"]
    initial_population = example_ilm["initial_conditions"]

    def rate_fn(_, state):
        si_rate = tf.broadcast_to([0.5], [state.shape[0]])
        ir_rate = tf.broadcast_to([0.7], si_rate.shape)

        return si_rate, ir_rate

    # create an instance of the model
    epi_model = ContinuousTimeStateTransitionModel(
        transition_rate_fn=rate_fn,
        incidence_matrix=incidence_matrix,
        initial_state=initial_population,
        num_steps=NUM_STEPS,
        initial_time=0.0,
    )

    log_lik = evaltest(lambda: epi_model.log_prob(example_ilm["event_list"]))

    # hand calculated log likelihood
    actual_loglik = -7.256319192936088

    np.testing.assert_almost_equal(log_lik, desired=actual_loglik, decimal=5)


def test_simple_sir_consistency(evaltest, homogeneous_sir_params):
    """Using an instance of the ContinuousTimeStateTransitionModel"""

    model_params = homogeneous_sir_params(0.8, 0.14)
    model = ContinuousTimeStateTransitionModel(**model_params)

    sample = evaltest(lambda: model.sample(seed=[0, 0]))

    evaltest(lambda: model.log_prob(sample))


def test_loglik_mle(evaltest, cont_time_homogeneous_sir_example):
    # Create sample
    actuals = list(cont_time_homogeneous_sir_example["true_params"].values())

    def opt_fn(log_rate_parameters):
        """Return negative log likelihood"""

        beta, gamma = tf.unstack(tf.math.exp(log_rate_parameters))
        model_params = cont_time_homogeneous_sir_example["model_params_fn"](
            beta, gamma
        )
        model = ContinuousTimeStateTransitionModel(**model_params)

        return -model.log_prob(cont_time_homogeneous_sir_example["draw"])

    initial_parameters = np.array(
        [-2.0, -2.0], dtype=cont_time_homogeneous_sir_example["dtype"]
    )
    opt = evaltest(
        lambda: tfp.optimizer.nelder_mead_minimize(
            opt_fn,
            initial_vertex=initial_parameters,
            func_tolerance=1e-6,
            position_tolerance=1e-3,
        )
    )

    assert opt.converged
    np.testing.assert_allclose(
        np.exp(opt.position), actuals, atol=0.2, rtol=0.1
    )


def test_tfp_jd_integration(evaltest, bayesian_sir_model):
    model = bayesian_sir_model["model"]
    example = bayesian_sir_model["example"]

    evaltest(lambda: model.sample(seed=[20240714, 1139]))

    conditioned_model = model.experimental_pin(sir=example.sir)
    lp = evaltest(lambda: conditioned_model.log_prob(beta=0.5, gamma=0.14))

    np.testing.assert_approx_equal(lp, 10.0128927)


def test_batch_sample(evaltest, homogeneous_sir_params):
    """Test batched.sample method"""

    model = ContinuousTimeStateTransitionModel(
        **homogeneous_sir_params(0.5, 0.14)
    )

    sample_shape = (3, 2)
    sims = evaltest(lambda: model.sample(sample_shape=sample_shape))

    expected_shape = sample_shape + (model.num_steps,)

    assert sims.time.shape == expected_shape
    assert sims.transition.shape == expected_shape
    assert sims.unit.shape == expected_shape


def test_batch_log_prob(evaltest, homogeneous_sir_params):
    """Test operability of batched log prob method"""

    model = ContinuousTimeStateTransitionModel(
        **homogeneous_sir_params(0.5, 0.14)
    )

    sample_shape = (3, 2)
    sims = evaltest(lambda: model.sample(sample_shape=sample_shape))
    log_probs = evaltest(lambda: model.log_prob(sims))

    assert log_probs.shape == sample_shape
