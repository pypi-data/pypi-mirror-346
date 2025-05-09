"""Functions for chain binomial simulation."""

from collections.abc import Callable

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import prefer_static as ps
from tensorflow_probability.python.internal import samplers

from gemlib.util import transition_coords

Tensor = tf.Tensor
tfd = tfp.distributions

__all__ = [
    "make_transition_prob_matrix_fn",
    "compute_state",
    "discrete_markov_simulation",
    "discrete_markov_log_prob",
]


def _gen_index(state_shape, trm_coords):
    """Generate indices for broadcasting transition rates."""
    with tf.name_scope("gen_index"):
        trm_coords = tf.convert_to_tensor(trm_coords)
        i_shp = (
            state_shape[:-1] + [trm_coords.shape[0]] + [len(state_shape) + 1]
        )
        b_idx = np.array(list(np.ndindex(*i_shp[:-1])))[:, :-1]
        m_idx = tf.tile(trm_coords, [tf.reduce_prod(i_shp[:-2]), 1])

        idx = tf.concat([b_idx, m_idx], axis=-1)
        return tf.reshape(idx, i_shp)


def _make_transition_matrix(rates, rate_coords, state_shape):
    """Create a transition rate matrix.

    Args
        rates: batched transition rate tensors  [b1, b2, n_rates]
        rate_coords: coordinates of rates in resulting transition matrix
        state_shape: the shape of the state tensor with ns states
    Returns
        a tensor of shape [..., ns, ns]
    """

    indices = _gen_index(state_shape, rate_coords)
    output_shape = state_shape + [state_shape[-1]]
    rate_tensor = tf.scatter_nd(
        indices=indices,
        updates=rates,
        shape=output_shape,
        name="build_markov_matrix",
    )
    return rate_tensor


def _approx_expm(rates):
    """Approximates a full Markov transition matrix
    :param rates: un-normalised rate matrix (i.e. diagonal zero)
    :returns: approximation to Markov transition matrix
    """
    with tf.name_scope("approx_expm"):
        total_rates = tf.reduce_sum(rates, axis=-1, keepdims=True)
        prob = 1.0 - tf.math.exp(-total_rates)
        partial_matrix = tf.math.multiply_no_nan(rates / total_rates, prob)
        return tf.linalg.set_diag(
            partial_matrix, 1.0 - tf.reduce_sum(partial_matrix, axis=-1)
        )


def make_transition_prob_matrix_fn(
    transition_rate_fn: Callable[[float, float], tuple[float, ...]],
    time_delta: float,
    incidence_matrix: float,
) -> Callable[[float, float], tuple[float, ...]]:
    time_delta = tf.convert_to_tensor(time_delta)
    incidence_matrix = tf.convert_to_tensor(incidence_matrix)

    def fn(t: float, state: float) -> tuple[float, ...]:
        t = tf.convert_to_tensor(t)
        state = tf.convert_to_tensor(state)

        if t.shape == ():
            rates = transition_rate_fn(t, state)
        else:
            rates = tf.vectorized_map(
                lambda elems: transition_rate_fn(*elems), elems=(t, state)
            )
        # `rate_matrix` needs to be a tensor of shape
        # `[M, S, S]` where `M` is the number of population units,
        # and `S` is the number of states.  Then, `rate_matrix[m, i, j]`
        # gives the transition rate for transitioning from state `i` to
        # state `j` in unit `m`.
        rate_matrix = _make_transition_matrix(
            tf.stack(rates, axis=-1),
            transition_coords(incidence_matrix),
            state.shape,
        )
        # Set diagonal to be the negative of the sum of other elements in
        #   each row
        transition_matrix = _approx_expm(rate_matrix * time_delta)

        return transition_matrix

    return fn


@tf.custom_gradient
def _multinomial_log_prob(
    total_count: Tensor, probs: Tensor, counts: Tensor
) -> Tensor:
    """Compute the log-PMF of the Multinomial distribution.

    Given `total_count` and `probs`, compute the probability
    mass function of the Multinomial distribution for outcome
    `counts`.  This function customises the gradient to ensure
    a finite value even if one or more of the counts is 0 with
    a corresponding probability 0.

    Args
    ====
    total_count: the total number of trials
    probs: a probability vector determining the trial outcomes
    counts: the outcome vector with elements corresponding to `probs`

    Returns
    =======
    A Tensor containing the log probability mass function value at
    `counts`.
    """
    log_p = tf.math.log(probs)
    log_unnorm_prob = tf.reduce_sum(
        tf.math.multiply_no_nan(log_p, counts), axis=-1
    )

    def grad_fn(upstream):  # noqa: ARG001
        return None, tf.math.multiply_no_nan(1.0 / probs, counts), None

    neg_log_normalizer = tf.stop_gradient(
        tfp.math.log_combinations(total_count, counts)
    )
    return log_unnorm_prob + neg_log_normalizer, grad_fn


def compute_state(initial_state, events, incidence_matrix, closed=False):
    """Compute a state tensor from initial state and event tensor.

    Args
    ----
        initial_state: a tensor of shape [M, S]
        events: a tensor of shape [T, M, R]
        incidence_matrix: a incidence_matrix matrix of shape [S,R] describing
            how transitions update the state.
        closed: if `True`, return state in close interval [0, T], otherwise
                [0, T)

    Returns
    -------
        a tensor of shape [T, M, S] if `closed=False` or [T+1, M, S] if
        `closed=True` describing the state of the system for each batch
        M at time T.
    """
    with tf.name_scope("compute_state"):
        if isinstance(incidence_matrix, tf.Tensor):
            incidence_matrix = ps.cast(incidence_matrix, dtype=events.dtype)
        else:
            incidence_matrix = tf.convert_to_tensor(
                incidence_matrix, dtype=events.dtype
            )
        increments = tf.einsum("...tmr,sr->...tms", events, incidence_matrix)

        if closed is False:
            cum_increments = tf.cumsum(increments, axis=-3, exclusive=True)
        else:
            cum_increments = tf.cumsum(increments, axis=-3, exclusive=False)
            cum_increments = tf.concat(
                [tf.zeros_like(cum_increments[..., 0:1, :, :]), cum_increments],
                axis=-3,
            )
        state = cum_increments + tf.expand_dims(initial_state, axis=-3)
        return state


def chain_binomial_propagate(transition_matrix_fn):
    """Propagates the state of a population according to discrete time dynamics.

    :param transition_matrix_fn: a function returning a Markov transition
        probability matrix of shape `[S, S]` for `S` states.
    :param time_step: the time step
    :param incidence_matrix: a `[S, R]` tensor giving the state transition graph
    :returns : a function that propagate `state[t]` -> `state[t+time_step]`
    """

    def propagate_fn(t, state, seed):
        markov_transition_matrix = transition_matrix_fn(t, state)
        num_states = markov_transition_matrix.shape[-1]
        prev_probs = tf.zeros_like(markov_transition_matrix[..., :, 0])
        counts = tf.zeros(
            markov_transition_matrix.shape[:-1].as_list() + [0],
            dtype=markov_transition_matrix.dtype,
        )
        total_count = state
        # This for loop is ok because there are (currently) only 4 states (SEIR)
        # and we're only actually creating work for 3 of them. Even for as many
        # as a ~10 states it should probably be fine, just increasing the size
        # of the graph a bit.
        seeds = samplers.split_seed(seed, n=num_states - 1, salt="propagate_fn")
        for i in range(num_states - 1):
            probs = markov_transition_matrix[..., :, i]
            binom = tfd.Binomial(
                total_count=total_count,
                probs=tf.clip_by_value(probs / (1.0 - prev_probs), 0.0, 1.0),
            )
            sample = binom.sample(seed=seeds[i])
            counts = tf.concat([counts, sample[..., tf.newaxis]], axis=-1)
            total_count -= sample
            prev_probs += probs

        counts = tf.concat([counts, total_count[..., tf.newaxis]], axis=-1)

        # Counts is a `[M, S, S]` tensor, where each inner dimension represents
        # a draw from a Multinomial random variable. Each element
        # `counts[m, i, j]` gives the number of transitions from state `i` to
        # state `j` in each unit `m`. We now sum over the `i` axis to get the
        # new state.
        new_state = tf.reduce_sum(counts, axis=-2)

        # `new_state` is of shape `[M, S]`
        return counts, new_state

    return propagate_fn


def discrete_markov_simulation(
    transition_prob_matrix_fn,
    state,
    start,
    end,
    time_step,
    seed=None,
):
    """Simulates from a discrete time Markov state transition model using
    multinomial sampling across rows of the transition matrix"""
    state = tf.convert_to_tensor(state)

    propagate = chain_binomial_propagate(transition_prob_matrix_fn)

    times = tf.range(start, end, time_step, dtype=state.dtype)
    state = tf.convert_to_tensor(state)

    output = tf.TensorArray(state.dtype, size=times.shape[0])

    def cond(i, *_):
        return i < times.shape[0]

    def body(i, state, output, seed):
        seed, next_seed = samplers.split_seed(seed)
        event_counts, state = propagate(times[i], state, seed)
        output = output.write(i, event_counts)
        return i + 1, state, output, next_seed

    _, state, output, _ = tf.while_loop(
        cond, body, loop_vars=(0, state, output, seed)
    )

    # `output.stack()` returns a `[T, M, S, S]` tensor of event numbers.
    return times, output.stack()


def discrete_markov_log_prob(
    events,
    init_state,
    init_step,
    time_delta,
    transition_prob_matrix_fn,
    incidence_matrix,
):
    """Calculates an unnormalised log_prob function for a discrete time epidemic
    model.

    :param events: a `[M, T, X]` batch of transition events for metapopulation
                   `M` times `T`, and transitions `X`.
    :param init_state: a vector of shape `[M, S]` the initial state of the
                       epidemic for `M` metapopulations and `S` states
    :param init_step: the initial time step, as an offset to
                      `range(events.shape[-2])`
    :param time_delta: the size of the time step.
    :param transition_prob_matrix_fn: a function that takes a state and returns
        a Markov transition rate matrix.
    :param incidence_matrix: a `[S, R]` matrix describing the state update for
                             each transition.
    :return: a scalar log probability for the epidemic.
    """
    with tf.name_scope("discrete_markov_log_prob"):
        events = tf.convert_to_tensor(events)
        init_state = tf.convert_to_tensor(init_state)
        init_step = tf.convert_to_tensor(init_step)
        time_delta = tf.convert_to_tensor(time_delta)

        num_times = events.shape[-3]
        num_units = events.shape[-2]
        num_states = init_state.shape[-1]

        # Transition probabilities
        state_timeseries = compute_state(
            init_state, events, incidence_matrix
        )  # MxTxS
        times = tf.range(
            init_step,
            time_delta * tf.cast(num_times, time_delta.dtype)
            + tf.cast(init_step, time_delta.dtype),
            time_delta,
        )
        transition_prob_matrix = transition_prob_matrix_fn(
            times, state_timeseries
        )

        # Event matrix
        event_matrix = _make_transition_matrix(
            events,
            transition_coords(incidence_matrix),
            [num_times, num_units, num_states],
        )
        event_matrix = tf.linalg.set_diag(
            event_matrix,
            state_timeseries - tf.reduce_sum(event_matrix, axis=-1),
            name="event_matrix_set_diag",
        )

        with tf.name_scope("draw_multinomial"):
            logp = _multinomial_log_prob(
                state_timeseries, transition_prob_matrix, event_matrix
            )

        with tf.name_scope("reduce_and_return"):
            return tf.reduce_sum(logp)


def events_to_full_transitions(events, initial_state):
    """Creates a state tensor given matrices of transition events
    and the initial state

    :param events: a tensor of shape [t, c, s, s] for t timepoints, c
                   metapopulations and s states.
    :param initial_state: the initial state matrix of shape [c, s]
    """

    def f(state, events):
        survived = tf.reduce_sum(state, axis=-2) - tf.reduce_sum(
            events, axis=-1
        )
        new_state = tf.linalg.set_diag(events, survived)
        return new_state

    return tf.scan(
        fn=f, elems=events, initializer=tf.linalg.diag(initial_state)
    )
