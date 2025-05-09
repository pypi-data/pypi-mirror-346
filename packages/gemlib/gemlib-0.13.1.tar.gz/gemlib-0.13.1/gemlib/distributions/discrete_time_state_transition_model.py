"""Describes a DiscreteTimeStateTransitionModel."""

from collections.abc import Callable

import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import (
    dtype_util,
    reparameterization,
    samplers,
)

from gemlib.distributions.discrete_markov import (
    compute_state,
    discrete_markov_log_prob,
    discrete_markov_simulation,
    make_transition_prob_matrix_fn,
)
from gemlib.func_util import maybe_combine_fn
from gemlib.tensor_util import broadcast_fn_to
from gemlib.util import batch_gather, transition_coords

Tensor = tf.Tensor
tla = tf.linalg
tfd = tfp.distributions


class DiscreteTimeStateTransitionModel(tfd.Distribution):
    """Discrete-time state transition model

    A discrete-time state transition model assumes a population of
    individuals is divided into a number of mutually exclusive states,
    where transitions between states occur according to a Markov process.
    Such models are commonly found in epidemiological and ecological
    applications, where rapid implementation and modification is necessary.

    This class provides a programmable implementation of the discrete-time
    state transition model, compatible with TensorFlow Probability.


    Example
    -------
    A homogeneously mixing SIR model implementation::

        import numpy as np
        import tensorflow as tf
        from gemlib.distributions import DiscreteTimeStateTransitionModel

        # Initial state, counts per compartment (S, I, R), for one
        #   population
        initial_state = np.array([[99, 1, 0]], np.float32)

        incidence_matrix = np.array(
            [
                [-1, 0],
                [1, -1],
                [0, 1],
            ],
            dtype=np.float32,
        )


        def si_rate(t, state):
            return 0.28 * state[:, 1] / tf.reduce_sum(state, axis=-1)


        def ir_rate(t, state):
            return 0.14


        # Instantiate model
        sir = DiscreteTimeStateTransitionModel(
            transition_rate_fn=[si_rate, ir_rate],
            incidence_matrix=incidence_matrix,
            initial_state=initial_state,
            num_steps=100,
        )

        # One realisation of the epidemic process
        sim = sir.sample(seed=[0, 0])

    """

    def __init__(
        self,
        transition_rate_fn: list[Callable] | Callable,
        incidence_matrix: Tensor,
        initial_state: Tensor,
        num_steps: int,
        initial_step: int = 0,
        time_delta: float = 1.0,
        validate_args: bool = False,
        allow_nan_stats: bool = True,
        name: str = "DiscreteTimeStateTransitionModel",
    ):
        """Initialise a discrete-time state transition model.

        Args:
          transition_rate_fn: Either a list of callables of the form :code:`fn(
            t: float, state: Tensor) -> Tensor` or a Python callable of the
            form :code:`fn(t: float, state: Tensor) -> tuple(Tensor,...)`.
            In the
            first (preferred) form, each callable in the list  corresponds to
            the respective transition in :code:`incidence_matrix`.  In the
            second form, the callable should return a :code:`tuple` of
            transition rate tensors corresponding to transitions in
            :code:`incidence_matrix`.  **Note**: the second form will be
            deprecated in future releases of :code:`gemlib`.
          incidence_matrix: :code:`Tensor` representing the stochiometry matrix
            for the state transition model where rows represent the transitions
            and columns represent states.
          initial_state: :code:`Tensor` representing an initial state of counts
            per compartment.  The inner dimension is equal to the first
            dimension of :code:`incidence_matrix`.
          initial_step: Python :code:`float` representing an offset giving the
            time :code:`t` of the first time step in the model.
          time_delta: Python :code:`float` representing the size of the time
            step to be used.
          num_steps: Python :code:`int` representing the number of time steps
             across which the model runs.

        """
        parameters = dict(locals())
        with tf.name_scope(name):
            self._incidence_matrix = tf.convert_to_tensor(
                incidence_matrix, dtype=initial_state.dtype
            )
            self._source_states = _compute_source_states(incidence_matrix)
            initial_state = tf.convert_to_tensor(initial_state)

            self._transition_prob_matrix_fn = make_transition_prob_matrix_fn(
                broadcast_fn_to(
                    maybe_combine_fn(transition_rate_fn),
                    tf.shape(initial_state)[:-1],
                ),
                tf.convert_to_tensor(time_delta, initial_state.dtype),
                self._incidence_matrix,
            )

            super().__init__(
                dtype=initial_state.dtype,
                reparameterization_type=reparameterization.FULLY_REPARAMETERIZED,
                validate_args=validate_args,
                allow_nan_stats=allow_nan_stats,
                parameters=parameters,
                name=name,
            )

        self.dtype = initial_state.dtype

    @property
    def transition_rate_fn(self):
        return self._parameters["transition_rate_fn"]

    @property
    def incidence_matrix(self):
        return self._parameters["incidence_matrix"]

    @property
    def initial_state(self):
        return self._parameters["initial_state"]

    @property
    def initial_step(self):
        return self._parameters["initial_step"]

    @property
    def source_states(self):
        return self._source_states

    @property
    def time_delta(self):
        return self._parameters["time_delta"]

    @property
    def num_steps(self):
        return self._parameters["num_steps"]

    @property
    def num_units(self):
        return tf.convert_to_tensor(self._parameters["initial_state"]).shape[-2]

    def _batch_shape(self):
        return tf.TensorShape([])

    def _event_shape(self):
        shape = tf.TensorShape(
            [
                tf.get_static_value(self.num_steps),  # T
                tf.convert_to_tensor(self.initial_state).shape[-2],  # M
                tf.convert_to_tensor(self.incidence_matrix).shape[-1],  # S
            ]
        )
        return shape

    def compute_state(
        self, events: Tensor, include_final_state: bool = False
    ) -> Tensor:
        """Computes a state timeseries given a transition events

        Args:
            events: a :code:`[self.num_steps, self.num_units, self.num_events]`
                    shaped tensor of events
            include_final_state: should the result include the final state?  If
                                 :code:`False` (default), then
                                 :code:`result.shape[1] == events.shape[1]`.
                                 If :code:`True`, then
                                 :code:`results.shape[1] == events.shape[1] + 1`

        Returns:
            A tensor of shape :code:`[self.num_steps, self.num_units, \
self.num_states]`
            giving the number of individuals in each state at
            each time point each unit.
        """
        return compute_state(
            incidence_matrix=self.incidence_matrix,
            initial_state=self.initial_state,
            events=events,
            closed=include_final_state,
        )

    def transition_prob_matrix(self, events: Tensor = None) -> Tensor:
        """Compute the Markov transition probability matrix

        Args:
            events: a :code:`[num_steps, num_units, num_transition]` tensor

        Returns:
            If :code:`events is None`, then return the
            :code:`[num_units, num_states, num_states]` transition probability
            matrix associated with the initial state.  Otherwise, return a
            :code:`[num_steps, num_units, num_states, num_states]` tensor
            representing the transition probability matrix at each timestep.
        """
        if events is None:
            return self._transition_prob_matrix_fn(
                self.initial_step, self.initial_state
            )

        state = self.compute_state(events)
        times = tf.range(
            self.initial_step,
            self.initial_step + self.time_delta * self.num_steps,
            self.time_delta,
        )

        return tf.vectorized_map(
            lambda elems: self._transition_prob_matrix_fn(*elems),
            elems=(times, state),
        )

    def _sample_n(self, n, seed=None):
        """Runs a simulation from the epidemic model

        :param param: a dictionary of model parameters
        :param state_init: the initial state
        :returns: a tuple of times and simulated states.
        """
        n = tf.convert_to_tensor(n)
        seeds = samplers.split_seed(
            seed, n=n, salt="DiscreteTimeStateTransitionModel"
        )

        def one_sample(seed):
            _, events = discrete_markov_simulation(
                transition_prob_matrix_fn=self._transition_prob_matrix_fn,
                state=self.initial_state,
                start=self.initial_step,
                end=self.initial_step + self.num_steps * self.time_delta,
                time_step=self.time_delta,
                seed=seed,
            )
            return events

        sim = tf.map_fn(
            one_sample,
            elems=seeds,
            parallel_iterations=16,
            fn_output_signature=self.dtype,
        )
        # `sim` is `[T, M, S, S]`, and we need to pick out
        # elements `[..., i, j]` for all our relevant transitions
        # `i->j`.  `batch_gather` computes these coordinates and
        # invokes tf.gather.
        indices = transition_coords(self.incidence_matrix)
        sim = batch_gather(sim, indices)

        # `sim` is now `[T, M, R]` structure for T times,
        # M population units, and R transitions.
        return sim

    def _log_prob(self, y):
        dtype = dtype_util.common_dtype(
            [y, self.initial_state], dtype_hint=self.dtype
        )
        y = tf.convert_to_tensor(y, dtype)

        batch_shape = tf.shape(y)[:-3]
        flat_shape = tf.concat(
            [[tf.reduce_prod(batch_shape)], self.event_shape_tensor()], axis=0
        )
        y = tf.reshape(y, flat_shape)

        def one_log_prob(y):
            return discrete_markov_log_prob(
                events=y,
                init_state=tf.convert_to_tensor(self.initial_state, y.dtype),
                init_step=tf.convert_to_tensor(self.initial_step, y.dtype),
                time_delta=tf.convert_to_tensor(self.time_delta, y.dtype),
                transition_prob_matrix_fn=self._transition_prob_matrix_fn,
                incidence_matrix=tf.convert_to_tensor(
                    self.incidence_matrix, y.dtype
                ),
            )

        log_probs = tf.vectorized_map(
            one_log_prob,
            elems=y,  # fn_output_signature=y.dtype
        )

        return tf.reshape(log_probs, batch_shape)


def _compute_source_states(incidence_matrix, dtype=tf.int32):
    """Computes the indices of the source states for each
       transition in a state transition model.

    :param incidence_matrix: incidence matrix in `[S, R]` orientation
                          for `S` states and `R` transitions.
    :returns: a tensor of shape `(R,)` containing source state indices.
    """
    incidence_matrix = tf.transpose(incidence_matrix)

    source_states = tf.reduce_sum(
        tf.cumsum(
            tf.clip_by_value(
                -incidence_matrix, clip_value_min=0, clip_value_max=1
            ),
            axis=-1,
            reverse=True,
            exclusive=True,
        ),
        axis=-1,
    )

    return tf.cast(source_states, dtype)
