"""Continuous time state transition model"""

from collections.abc import Callable

import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import reparameterization

from gemlib.distributions.continuous_markov import (
    EventList,
    compute_state,
    continuous_markov_simulation,
    continuous_time_log_likelihood,
)
from gemlib.func_util import maybe_combine_fn
from gemlib.tensor_util import broadcast_fn_to

# aliasing for convenience
tfd = tfp.distributions
Tensor = tf.Tensor
DTYPE = tf.float32


class ContinuousTimeStateTransitionModel(tfd.Distribution):
    """Continuous time state transition model."""

    def __init__(
        self,
        transition_rate_fn: list[Callable[[Tensor], Tensor]]
        | Callable[[Tensor], Tensor],
        incidence_matrix: Tensor,
        initial_state: Tensor,
        num_steps: int,
        initial_time: float = 0.0,
        validate_args: bool = False,
        allow_nan_stats: bool = True,
        name: str = "ContinuousTimeStateTransitionModel",
    ):
        """
        Initializes a ContinuousTimeStateTransitionModel object.

        Args:
          transition_rate_fn: Either a list of callables of the form
            :code:`fn(t: float, state: Tensor) -> Tensor` or a Python callable
            of the form :code:`fn(t: float, state: Tensor) -> tuple(Tensor,...)`
            .  In the first
            (preferred) form, each callable in the list  corresponds to the
            respective transition in :code:`incidence_matrix`.  In the second
            form, the callable should return a :code:`tuple` of transition rate
            tensors corresponding to transitions in :code:`incidence_matrix`.
            **Note**: the second form will be deprecated in future releases of
            :code:`gemlib`.
          incidence_matrix: Matrix representing the incidence of transitions
                            between states.
          initial_state: A :code:`[N, S]` tensor containing the initial state of
            the population of :code:`N` units in :code:`S` epidemiological
            classes.
          num_steps: the number of markov jumps for a single iteration.
            initial_time: Initial time of the model. Defaults to 0.0.
          name: Name of the model. Defaults to
                  "ContinuousTimeStateTransitionModel".

        """
        parameters = dict(locals())

        self._incidence_matrix = tf.convert_to_tensor(incidence_matrix)
        self._initial_state = tf.convert_to_tensor(initial_state)
        self._initial_time = tf.convert_to_tensor(
            initial_time, dtype=self._initial_state.dtype
        )
        self._transition_rate_fn = maybe_combine_fn(transition_rate_fn)

        dtype = EventList(
            time=self._initial_time.dtype,
            transition=tf.int32,
            unit=tf.int32,
        )

        super().__init__(
            dtype=dtype,
            reparameterization_type=reparameterization.FULLY_REPARAMETERIZED,
            validate_args=validate_args,
            allow_nan_stats=allow_nan_stats,
            parameters=parameters,
            name=name,
        )

    @property
    def transition_rate_fn(self):
        """Transition rate function for the model."""
        return self._parameters["transition_rate_fn"]

    @property
    def incidence_matrix(self):
        """Incidence matrix for the model."""
        return self._parameters["incidence_matrix"]

    @property
    def initial_state(self):
        """Initial state of the model."""
        return self._parameters["initial_state"]

    @property
    def num_steps(self):
        """Number of events to simulate."""
        return self._parameters["num_steps"]

    @property
    def initial_time(self):
        """Initial wall clock for the model. Sets the time scale."""
        return self._parameters["initial_time"]

    def compute_state(
        self, event_list: EventList, include_final_state: bool = False
    ) -> Tensor:
        """Given an event list `event_list`, compute a timeseries
           of state given the model.

        Args
        ----
            event_list: the event list, assumed to be sorted by time.
            include_final_state: should the final state be included in the
                returned timeseries?  If `True`, then the time dimension of
                the returned tensor will be 1 greater than the length of the
                event list.  If `False` (default) these will be equal.

        Return
        ------
        A `[T, N, S]` tensor where `T` is the number of events, `N` is the
        number of units, and `S` is the number of states.
        """
        return compute_state(
            self.incidence_matrix,
            self.initial_state,
            event_list,
            include_final_state,
        )

    # Bypass the reshaping that tfd.Distribution._call_sample_n does
    # def _call_sample_n(self, sample_shape, seed) -> EventList:
    #     return self._sample_n(sample_shape, seed)

    def _sample_n(self, n: int, seed=None) -> EventList:
        """
        Samples n outcomes from the continuous time state transition model.

        Args:
            n (int): The number of realisations of the Markov process to sample
                     (currently ignored).
            seed (int, optional): The seed value for random number generation.
                                  Defaults to None.

        Returns:
            EventList: A list of n outcomes sampled from the continuous time
                           state transition model.
        """
        n = tf.convert_to_tensor(n)
        seeds = tfp.random.split_seed(
            seed, n=n, salt="ContinuousTimeStateTransitionModel"
        )

        def one_sample(seed):
            return continuous_markov_simulation(
                transition_rate_fn=broadcast_fn_to(
                    self._transition_rate_fn,
                    tf.shape(self._initial_state)[:-1],
                ),
                incidence_matrix=self._incidence_matrix,
                initial_state=self._initial_state,
                initial_time=self._initial_time,
                num_markov_jumps=self.num_steps,
                seed=seed,
            )

        outcome = tf.map_fn(
            one_sample,
            elems=seeds,
            parallel_iterations=16,
            fn_output_signature=self.dtype,
        )

        return outcome

    def _log_prob(self, value: EventList) -> float:
        """
        Computes the log probability of the given outcomes.

        Args:
            value (EventList): an EventList object representing the
                                   outcomes.

        Returns:
            float: The log probability of the given outcomes.
        """
        value = tf.nest.map_structure(lambda x: tf.convert_to_tensor(x), value)

        batch_shape = tf.shape(value.time)[:-1]

        flat_shape = (tf.reduce_prod(batch_shape), value.time.shape[-1])

        value = tf.nest.map_structure(
            lambda x: tf.reshape(x, flat_shape), value
        )

        def one_log_prob(x):
            return continuous_time_log_likelihood(
                transition_rate_fn=broadcast_fn_to(
                    self._transition_rate_fn,
                    tf.shape(self._initial_state)[:-1],
                ),
                incidence_matrix=self.incidence_matrix,
                initial_state=self.initial_state,
                initial_time=self.initial_time,
                event_list=x,
            )

        log_probs = tf.map_fn(
            one_log_prob, elems=value, fn_output_signature=value.time.dtype
        )

        return tf.reshape(log_probs, batch_shape)

    def _event_shape_tensor(self) -> EventList:
        return EventList(
            time=tf.constant([self.num_steps], dtype=tf.int32),
            transition=tf.constant([self.num_steps], dtype=tf.int32),
            unit=tf.constant([self.num_steps], dtype=tf.int32),
        )

    def _event_shape(self) -> EventList:
        return EventList(
            time=tf.TensorShape([self.num_steps]),
            transition=tf.TensorShape([self.num_steps]),
            unit=tf.TensorShape([self.num_steps]),
        )

    def _batch_shape_tensor(self) -> EventList:
        return EventList(
            time=tf.constant([]),
            transition=tf.constant([]),
            unit=tf.constant([]),
        )

    def _batch_shape(self) -> EventList:
        return EventList(
            time=tf.TensorShape([]),
            transition=tf.TensorShape([]),
            unit=tf.TensorShape([]),
        )
