"""Test for Chain Binomial Rippler Kernel"""

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import test_util

from gemlib.distributions import DiscreteTimeStateTransitionModel

from .chain_binomial_rippler import CBRKernel

tfd = tfp.distributions

MIN_EVENTS = 10


def _make_model():
    incidence_matrix = np.array([[-1, 1, 0], [0, -1, 1]], dtype=np.float32)
    init_state = np.array(
        [[999.0, 1.0, 0.0], [1000.0, 0.0, 0.0]], dtype=np.float32
    )

    contact_matrix = np.array([[0, 1], [1, 0]], dtype=np.float32)

    init_state = tf.convert_to_tensor(init_state)
    contact_matrix = tf.convert_to_tensor(contact_matrix)

    def hazard_fn(_, state):
        si = (
            0.3 * state[..., 1]
            + 0.1 * tf.linalg.matvec(contact_matrix, state[..., 1])
        ) / tf.reduce_sum(state, axis=-1)
        ir = tf.broadcast_to(tf.constant([0.14]), si.shape)
        return [si, ir]

    model = DiscreteTimeStateTransitionModel(
        transition_rate_fn=hazard_fn,
        initial_state=init_state,
        initial_step=0,
        time_delta=1.0,
        num_steps=70,
        stoichiometry=incidence_matrix,
    )

    return model


@test_util.test_all_tf_execution_regimes
class CBRSIRTest(test_util.TestCase):
    def setUp(self):
        self.incidence_matrix = np.array(
            [[-1, 0], [1, -1], [0, 1]], dtype=np.float32
        )

        self.init_state = np.array(
            [[999.0, 1.0, 0.0], [1000.0, 0.0, 0.0]], dtype=np.float32
        )

        self.C = np.array([[0, 1], [1, 0]], dtype=np.float32)

        model = self._make_model(self.incidence_matrix, self.init_state, self.C)

        while True:
            events = self.evaluate(model.sample())
            if tf.reduce_sum(events[..., 1]) > MIN_EVENTS:
                break

        observation_process = tfd.Independent(
            distribution=tfd.Binomial(total_count=events[..., 1], probs=0.5),
            reinterpreted_batch_ndims=1,
        )

        self.sir = events
        self.observed_cases = self.evaluate(
            observation_process.sample(seed=[0, 0])
        )

    def _make_model(self, incidence_matrix, init_state, contact_matrix):
        init_state = tf.convert_to_tensor(init_state)
        contact_matrix = tf.convert_to_tensor(contact_matrix)

        def hazard_fn(_, state):
            si = (
                0.3 * state[..., 1]
                + 0.1 * tf.linalg.matvec(contact_matrix, state[..., 1])
            ) / tf.reduce_sum(state, axis=-1)
            ir = tf.broadcast_to(tf.constant([0.14]), si.shape)
            return si, ir

        model = DiscreteTimeStateTransitionModel(
            transition_rate_fn=hazard_fn,
            initial_state=init_state,
            initial_step=0,
            time_delta=1.0,
            num_steps=70,
            incidence_matrix=incidence_matrix,
        )

        return model

    def test_cbr_kernel(self):
        model = self._make_model(
            self.incidence_matrix,
            self.init_state,
            self.C,
        )

        def tlp_fn(current_events):
            observation_process = tfd.Binomial(
                total_count=tf.gather(current_events, indices=1, axis=-1),
                probs=0.5,
            )
            return tf.reduce_sum(
                observation_process.log_prob(self.observed_cases)
            )

        kernel = CBRKernel(tlp_fn, model=model)
        pkr = self.evaluate(
            kernel.bootstrap_results(tf.convert_to_tensor(self.sir))
        )
        samples, results = kernel.one_step(self.sir, pkr)
