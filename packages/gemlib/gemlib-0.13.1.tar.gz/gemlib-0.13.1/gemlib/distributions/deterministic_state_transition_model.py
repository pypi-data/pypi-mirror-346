"""Describes a DeterministicStateTransitionModel"""

from collections.abc import Callable
from typing import NamedTuple

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import reparameterization

from gemlib.distributions.continuous_markov import _total_flux
from gemlib.func_util import maybe_combine_fn
from gemlib.tensor_util import broadcast_fn_to

tfd = tfp.distributions

Tensor = tf.Tensor

__all__ = ["DeterministicStateTransitionModel"]


class Results(NamedTuple):
    times: Tensor
    states: Tensor


class DeterministicStateTransitionModel(tfd.Distribution):
    """Deterministic state transition model

    A deterministic (ODE) state transmission model represented by a set of ODEs
    specified by a state transition graph with nodes representing state, and
    transtion rates representing edges.

    This class provides a programmable implementation of the deterministic
    state transition model, compatible with TensorFlow Probability.

    Examples:
      A deterministic metapopulation SIR model::

        import numpy as np
        import tensorflow as tf
        from gemlib.distributions import \
DeterministicTimeStateTransitionModel

        initial_state = np.array([[99, 1, 0]], np.float32)

        incidence_matrix = np.array(
            [
                [-1,  0],
                [ 1, -1],
                [ 0,  1],
            ],
            dtype=np.float32,
        )

        def si_rate(t, state):
            return 0.28 * state[:,1] / tf.reduce_sum(state, axis=-1)

        def ir_rate(t, state):
            return 0.14

        #Instantiate model
        sir = DeterministicStateTransitionModel(
                transition_rate_fn=[si_rate, ir_rate],
                incidence_matrix=incidence_matrix,
                initial_state=initial_state,
                num_steps=100,
                initial_time=0,
                time_delta=1.0,
                )

        #One realisation of the epidemic process
        sir_sim = sir.sample(seed=[0, 0])

    """

    def __init__(
        self,
        transition_rate_fn: list[Callable[[float, Tensor], Tensor], ...]
        | Callable[[float, Tensor], tuple[Tensor]],
        incidence_matrix: Tensor,
        initial_state: Tensor,
        num_steps: int | None = None,
        initial_time: float | None = 0.0,
        time_delta: float | None = 1.0,
        times: Tensor = None,
        solver: str | None = "DormandPrince",
        solver_kwargs: dict = None,
        validate_args: bool | None = False,
        name: str = "DeterministicStateTransitionModel",
    ):
        """A deterministic (ODE) state transition model.

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
          incidence_matrix: a :code:`[S, R]` matrix describing the change in
            :code:`S` resulting from transitions :code:`R`.
          initial_state: a :code:`[...,N, S]` (batched) tensor with the state
            values for :code:`N` units and :code:`S` states.
          num_steps: python integer representing the size of the time step to be
            used.
          initial_time: an offset giving the time of the first time step in the
            model.
          time_delta: the size of the time step to be used.
          times: a 1-D tensor of times for which the ODE solutions are required.
          solver: a string giving the ODE solver method to use.  Can be "rk45"
            (default) or "BDF".  See the `TensorFlow Probability documentation`_
            for details.
          solver_kwargs: a dictionary of keyword argument to supply to the
            solver. See the solver documentation for details.
          validate_args: check that the values of the parameters supplied to the
            constructor are all within the domain of the ODE function
          name: the name of this distribution.

        .. _TensorFlow Probability documentation:
           https://www.tensorflow.org/probability/api_docs/python/tfp/math/ode

        """

        parameters = dict(locals())

        if (num_steps is not None) and (times is not None):
            raise ValueError(
                "Must specify exactly one of `num_steps` or `times`"
            )

        if num_steps is not None:
            self._times = tf.range(
                initial_time, time_delta * num_steps, time_delta
            )
        elif times is not None:
            self._times = tf.convert_to_tensor(times)
        else:
            raise ValueError("Must specify either `num_steps` or `times`")

        dtype = Results(
            times=tf.convert_to_tensor(self._times).dtype,
            states=tf.convert_to_tensor(initial_state).dtype,
        )

        self._transition_rate_fn = maybe_combine_fn(transition_rate_fn)

        super().__init__(
            dtype=dtype,
            reparameterization_type=reparameterization.FULLY_REPARAMETERIZED,
            validate_args=validate_args,
            allow_nan_stats=True,
            parameters=parameters,
            name=name,
        )

        self._solution = self._solve()

    @property
    def transition_rate_fn(self):
        return self.parameters["transition_rate_fn"]

    @property
    def incidence_matrix(self):
        return self.parameters["incidence_matrix"]

    @property
    def initial_state(self):
        return self.parameters["initial_state"]

    @property
    def num_steps(self):
        return self.parameters["num_steps"]

    @property
    def initial_time(self):
        return self.parameters["initial_time"]

    @property
    def time_delta(self):
        return self.parameters["time_delta"]

    @property
    def times(self):
        return self.parameters["times"]

    @property
    def solver(self):
        return self.parameters["solver"]

    @property
    def solver_kwargs(self):
        return self.parameters["solver_kwargs"]

    def _event_shape(self):
        times = tf.convert_to_tensor(self._times)
        initial_state = tf.convert_to_tensor(self.initial_state)
        shape = Results(
            times=tf.TensorShape(times.shape),
            states=tf.TensorShape(times.shape + initial_state.shape),
        )

        return shape

    def _event_shape_tensor(self):
        times = tf.convert_to_tensor(self.times)
        initial_state = tf.convert_to_tensor(self.initial_state)

        return Results(
            times=tf.constant(times.shape, tf.int32),
            states=tf.constant(
                [
                    times.shape[-1],
                    initial_state.shape[-2],
                    initial_state.shape[-1],
                ],
                tf.int32,
            ),
        )

    def _batch_shape(self):
        return Results(
            times=tf.TensorShape(()),
            states=tf.TensorShape(()),
        )

    def _batch_shape_tensor(self):
        return Results(
            times=tf.constant(()),
            states=tf.constant(()),
        )

    def _solve(self):
        solver_kwargs = {} if self.solver_kwargs is None else self.solver_kwargs

        if self.solver == "DormandPrince":
            solver = tfp.math.ode.DormandPrince(**solver_kwargs)
        elif self.solver == "BDF":
            solver = tfp.math.ode.BDF(**solver_kwargs)
        else:
            raise ValueError("`solver` must be one of 'DormandPrince' or 'BDF'")

        def gradient_fn(t, state):
            rates = broadcast_fn_to(
                self._transition_rate_fn, tf.shape(self.initial_state)[:-1]
            )(t, state)
            flux = _total_flux(rates, state, self.incidence_matrix)  # [...,R,N]
            derivs = tf.linalg.matmul(self.incidence_matrix, flux)
            return tf.linalg.matrix_transpose(derivs)

        solver_results = solver.solve(
            ode_fn=gradient_fn,
            initial_time=tf.convert_to_tensor(self.initial_time),
            initial_state=tf.convert_to_tensor(self.initial_state),
            solution_times=tf.convert_to_tensor(self._times),
        )

        return Results(
            times=solver_results.times,
            states=solver_results.states,
        )

    def _sample_n(self, sample_shape=(), seed=None):  # noqa: ARG002
        # Batch sampling an ODE model will yield identical results
        # so we can just broadcast out instead.
        batch_results = tf.nest.map_structure(
            lambda x, s: tf.broadcast_to(x, tf.TensorShape(sample_shape) + s),
            self._solution,
            self.event_shape,
        )

        return batch_results

    def _log_prob(self, value, atol=1e-6, rtol=1e-6):
        value = tf.nest.map_structure(lambda x: tf.convert_to_tensor(x), value)

        def approx_equal(x, y):
            diff = x - y
            eps = atol + rtol * tf.abs(y)
            return tf.reduce_all(diff < eps)

        is_approx_equal = tf.math.logical_and(
            *tf.nest.map_structure(approx_equal, self._solution, value)
        )

        return tf.where(
            is_approx_equal,
            tf.zeros(is_approx_equal.shape, value.times.dtype),
            tf.fill(
                is_approx_equal.shape,
                -tf.convert_to_tensor(np.inf, value.times.dtype),
            ),
        )
