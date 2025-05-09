"""Function for continuous time simulation"""

from collections.abc import Callable
from typing import NamedTuple

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import prefer_static as ps

from gemlib.util import batch_gather, transition_coords

# aliasing for convenience
tfd = tfp.distributions
Tensor = tf.Tensor
DTYPE = tf.float32


class EventList(NamedTuple):
    """Tracker of an event in an epidemic simulation

    Attributes:
        time (float): The time at which the event occurred.
        transition (int): The type of transition that occurred.
        unit (int): The unit involved in the event.
    """

    time: float
    transition: int
    unit: int


def _one_hot_expand_state(condensed_state: tf.Tensor) -> tf.Tensor:
    """Expand the state of the epidemic to a one-hot representation
    Args:
        epidemic_state: The state of the epidemic
    Returns:
        The one-hot representation of the epidemic state
    """
    # Create one-hot encoded vectors for each state
    one_hot_states = tf.one_hot(
        tf.range(len(condensed_state)),
        depth=len(condensed_state),
        dtype=tf.float32,
    )
    # Repeat each one-hot state based on its corresponding count
    repeated_states = tf.repeat(one_hot_states, condensed_state, axis=0)

    # Reshape and transpose to get state per row representation
    return repeated_states


def _total_flux(transition_rates, state, incidence_matrix):
    """Multiplies `transition_rates` by source `state`s to return
       the total flux along transitions given `state`.

    Args
    ----
        transition_rates: a `[R,N]` tensor of per-unit transition rates
                          for `R` transitions and `N` aggregation units.
        state: a `[N, S]` tensor of `N` aggregation units and `S` states.
        incidence_matrix: a `[S, R]` matrix describing the change in `S` for
                          each transition `R`.

    Returns
    -------
    A [R,N] tensor of total flux along each transition, taking into account the
    availability of units in the source state.
    """

    source_state_idx = transition_coords(incidence_matrix)[:, 0]
    source_states = batch_gather(state, indices=source_state_idx[:, tf.newaxis])
    transition_rates = tf.stack(transition_rates, axis=-1)

    return tf.einsum("...nr,...nr->...rn", transition_rates, source_states)


def compute_state(
    incidence_matrix: Tensor,
    initial_state: Tensor,
    event_list: EventList,
    include_final_state: bool = False,
):
    """Given an event list `event_list`, compute a timeseries
       of state given the model.

    Args
    ----
        incidence_matrix: a `[S,R]` graph incidence matrix for `S`
            compartments and `R` transitions.
        initial_state: a `[N,S]` representing the initial state of `N`
            units by `S` compartments.
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
    event_list = event_list.__class__(
        *[tf.convert_to_tensor(x) for x in event_list]
    )

    initial_state = tf.convert_to_tensor(initial_state)
    incidence_matrix = tf.convert_to_tensor(incidence_matrix)

    num_times = event_list.time.shape[-1]
    num_units = initial_state.shape[-2]
    num_reactions = incidence_matrix.shape[-1] + 1  # R + pad for ghost events

    # The technique to handle batch dimensions in the event_list is to
    # flatten the batch dimensions.  That way we can guarantee
    # that the output dense events have shape [B, T, N, R].
    batch_dims = event_list.time.shape[:-1]
    flat_batch_shape = tf.TensorShape(ps.reduce_prod(batch_dims))

    # Compute one-hot encoding of event timeseries
    event_tensor_shape = flat_batch_shape + tf.TensorShape(
        (num_times, num_units, num_reactions)
    )  # [B, T, N, R]

    hot_indices = tf.stack(
        [
            tf.repeat(
                tf.range(flat_batch_shape[0]), num_times
            ),  # B 0,0,...,1,1
            tf.tile(tf.range(num_times), flat_batch_shape),  # T 0,1,...,0,1
            tf.reshape(
                event_list.unit, [-1]
            ),  # N (flat_batch_shape * num_times)
            tf.reshape(
                event_list.transition, [-1]
            ),  # R (flat_batch_shape * num_times)
        ],
        axis=-1,
    )

    event_tensor = tf.scatter_nd(
        indices=hot_indices,
        updates=tf.ones(hot_indices.shape[0], initial_state.dtype),
        shape=event_tensor_shape,
    )[..., :-1]  # Clip last dimension to remove ghost events

    # Compute deltas and cumsum over the state
    delta = tf.linalg.matmul(event_tensor, incidence_matrix, transpose_b=True)
    if include_final_state is False:
        delta = delta[..., :-1, :, :]

    batched_initial_state = tf.broadcast_to(
        initial_state[tf.newaxis, tf.newaxis, ...],  # Add B and T dimensions
        shape=flat_batch_shape + (1,) + initial_state.shape,
    )
    state = tf.cumsum(
        tf.concat([batched_initial_state, delta], axis=-3), axis=-3
    )

    return tf.reshape(state, shape=batch_dims + state.shape[-3:])


def exponential_propogate(
    transition_rate_fn: Callable, incidence_matrix: Tensor
) -> EventList:
    """Generates a function for propogating an epidemic forward in time

    Closure over the transition rate function and the incidence matrix
    which outline the epidemic dynamics and model structure. The returned
    function can be used to simulate the epidemic forward in time one step.

    Args:
        transition_rate_fn (Callable): a function that takes the current
            state of the epidemic and returns the transition rates for each
            unit/meta-population.
        incidence_matrix (tensor): A `[R, S]` matrix that describes the graph
            structure of the state transition mode. The rows correspond to the
            `R` transitions and the columns correspond to the `S` states.

    Returns:
        EventList: A NamedTuple that describes the next event in the
            epidemic.
    """
    tr_incidence_matrix = tf.transpose(incidence_matrix)

    def propogate_fn(time: float, state: Tensor, seed: int) -> list:
        """Propogates the state of the epidemic forward in time

        Args:
            time (float): Wall clock of the epidemic - can easily recover
            the time delta
            state (tensor): `[N,S]` representing the current state.

        Returns:
            EventList: The next event in the epidemic.
        """
        seed_exp, seed_cat = tfp.random.split_seed(seed, n=2)
        num_units = state.shape[-2]

        # compute event rates for all possible events
        transition_rates = _total_flux(
            transition_rate_fn(time, state), state, incidence_matrix
        )

        # simulate next time
        t_next = tfd.Exponential(rate=tf.reduce_sum(transition_rates)).sample(
            seed=seed_exp
        )

        # use categorical distribution to get event type and indiviudal id
        event_id = tfd.Categorical(
            probs=tf.reshape(transition_rates, shape=(-1,)),
            dtype=tf.int32,
        ).sample(seed=seed_cat)

        unit_idx = tf.math.floormod(event_id, num_units)
        transition_idx = tf.math.floordiv(event_id, num_units)

        # update the state
        new_state = tf.tensor_scatter_nd_add(
            state,
            [[unit_idx]],
            [tr_incidence_matrix[transition_idx]],
        )

        return (
            time + t_next,
            new_state,
            EventList(time + t_next, transition_idx, unit_idx),
        )

    return propogate_fn


def continuous_markov_simulation(
    transition_rate_fn: Callable,
    initial_state: Tensor,
    incidence_matrix: Tensor,
    num_markov_jumps: int,
    initial_time: float = 0.0,
    seed=None,
) -> EventList:
    """
    Simulates a continuous-time Markov process

    Args:
        transition_rate_fn (Callable): A function that computes the transition
            rates given the current state and incidence matrix.
        initial_state (Tensor): A [N, S] tensor, respresenting a population of N
                        units and S states.
        num_markov_jumps (int): The number of iterations to simulate.
        incidence_matrix (Tensor): The `[S,R]` incidence matrix representing the
            state transition model with S states and R transitions.
        seed (Optional[List(int,int)): The random seed.
    Returns:
        EventList: An object containing the simulated epidemic events.

    """
    initial_state = tf.convert_to_tensor(initial_state)
    incidence_matrix = tf.convert_to_tensor(incidence_matrix)
    dtype = initial_state.dtype
    seed = tfp.random.sanitize_seed(seed, salt="continuous_markov_simulation")

    propagate_fn = exponential_propogate(transition_rate_fn, incidence_matrix)

    accum = EventList(
        time=tf.TensorArray(dtype, size=num_markov_jumps, dynamic_size=False),
        transition=tf.TensorArray(
            tf.int32, size=num_markov_jumps, dynamic_size=False
        ),
        unit=tf.TensorArray(
            tf.int32, size=num_markov_jumps, dynamic_size=False
        ),
    )

    def cond(i, time, state, *_):
        transition_rates = _total_flux(
            transition_rate_fn(time, state), state, incidence_matrix
        )
        cont = (i < num_markov_jumps) & (tf.reduce_sum(transition_rates) > 0.0)
        return cont

    def body(i, time, state, seed, accum):
        next_seed, this_seed = tfp.random.split_seed(seed, salt="body")
        next_time, next_state, event = propagate_fn(time, state, this_seed)
        accum = EventList(
            *[x.write(i, y) for x, y in zip(accum, event, strict=True)]
        )
        return i + 1, next_time, next_state, next_seed, accum

    actual_markov_jumps, _, _, _, accum = tf.while_loop(
        cond, body, loop_vars=(0, initial_time, initial_state, seed, accum)
    )

    output = tf.nest.map_structure(lambda x: x.stack(), accum)

    # Pad unused parts of the output TensorArrays if the
    # loop terminates before num_markov_jumps
    mask = tf.range(num_markov_jumps) < actual_markov_jumps
    output = EventList(
        time=tf.where(mask, output.time, np.inf),
        unit=tf.where(mask, output.unit, 0),
        transition=tf.where(mask, output.transition, incidence_matrix.shape[1]),
    )

    return output


def continuous_time_log_likelihood(
    transition_rate_fn: Callable,
    incidence_matrix: Tensor,
    initial_state: Tensor,
    initial_time: float,
    event_list: EventList,
) -> float:
    """
    Computes the log-likelihood of a continuous-time Markov process
    given the transition rate function,
    incidence matrix, initial state, number of jumps, and event data.

    Args:
        transition_rate_fn (Callable): A function that computes the
        transition rate given the current state and time.
        incidence_matrix: The incidence matrix representing
        the connections between states in `[S,R]` format.
        initial_state: The initial state of the process as a `[N,R]`.
        num_jumps (int): The number of jumps to simulate.
        event (EventList): The event data containing the times
        and states.

    Returns:
        Tensor: The log-likelihood of the continuous-time Markov process.
    """
    # construct the epidemic states [T, N, S]
    states = compute_state(
        incidence_matrix=incidence_matrix,
        initial_state=initial_state,
        event_list=event_list,
    )

    # compute the transition rates for each of the states in the event
    time = tf.concat([[initial_time], event_list.time], axis=-1)
    rates = tf.vectorized_map(
        fn=lambda x: transition_rate_fn(*x),
        elems=(time[:-1], states),
    )  # R-tuple of [T,N] tensors

    total_flux = _total_flux(rates, states, incidence_matrix)

    indices = tf.stack(
        [
            tf.range(event_list.time.shape[0]),
            tf.clip_by_value(  # Clip due to ghost events (values zeroed later)
                event_list.transition,
                clip_value_min=0,
                clip_value_max=incidence_matrix.shape[-1] - 1,
            ),
            event_list.unit,
        ],
        axis=-1,
    )

    # compute event specific rate - get indices of the event that happened
    event_rate = tf.gather_nd(total_flux, indices)

    # compute total rate per timestep
    total_rate = tf.reduce_sum(total_flux, axis=(-2, -1))
    # total_rate = tf.einsum("tns -> t", total_flux)

    # compute time deltas
    time_delta = time[1:] - time[:-1]

    # compute the log-likelihood
    loglik_t = -total_rate * time_delta + tf.math.log(event_rate)

    # Zero out for any inf times (i.e. possible padding of event_list chunk)
    loglik_t = tf.where(
        tf.math.is_finite(time_delta), loglik_t, tf.zeros_like(loglik_t)
    )

    return tf.reduce_sum(loglik_t)
