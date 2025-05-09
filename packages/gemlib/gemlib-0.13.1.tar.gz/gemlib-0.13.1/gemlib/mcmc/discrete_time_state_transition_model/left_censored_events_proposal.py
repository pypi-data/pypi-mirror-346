"""Implements a proposal for left-censored events"""

import tensorflow as tf
import tensorflow_probability as tfp
import tensorflow_probability.python.internal.prefer_static as ps

from gemlib.distributions.discrete_markov import compute_state
from gemlib.distributions.kcategorical import UniformKCategorical
from gemlib.distributions.uniform_integer import UniformInteger
from gemlib.util import states_from_transition_idx

tfd = tfp.distributions


def _mask_max(x, t, axis=0):
    """Fills all elements where `i>t` along axis `axis`
    of `x` with `x.dtype.max`.
    """
    mask = tf.cast(tf.range(x.shape[axis]) > t, x.dtype) * x.dtype.max
    return x + mask[:, tf.newaxis]


def left_censored_event_time_proposal(
    events,
    initial_state,
    transition,
    incidence_matrix,
    num_units,
    max_timepoint,
    max_events,
    dtype=tf.int32,
    name=None,
):
    """Propose to move `transition` events into or out of a randomly selected
    time-window [0, max_timepoint] (n.b. inclusive!) subject to bounds imposed
    by a state-transition process described by `stoichiometry`.  The event
    timeseries describes the number of events occuring along `R` transitions in
    `M` coupled units across `T` timepoints between `S` states.

    :param events: a [T, M, R] tensor describing number of events for each
                    transition in each unit at each timepoint.
    :param initial_state: a [M, S] tensor describing the initial values of the
                           state at the first timepoint.
    :param transition: the transition for which we wish to move events backwards
                        or forwards in time.
    :param incidence_matrix: a [S, R] matrix describing the change in the value
                             of each state in response to an event along each
                             transition.
    :param num_units: number of units to propose for (currently restricted to
                      1!)
    :param max_timepoint: events are moved to and from time window `[0,
                          max_timepoint]`
    :param dtype=tf.int32: the return type of the update.
    :param name: name of the returned JointDistributionNamed.
    :returns: a JointDistributionNamed object for which `sample()` returns the
              id of a unit, distance and direction through which to move events,
              and number of events.
    """
    assert (
        num_units == 1
    ), "LeftCensoredEventTimeProposal with `num_units!=1` is not supported"

    time_range = tf.range(0, max_timepoint + 1)
    incidence_matrix = tf.convert_to_tensor(incidence_matrix)
    transition = tf.convert_to_tensor(transition, tf.int32)
    max_events = tf.convert_to_tensor(max_events, events.dtype)

    # Identify the source and destination states for `transition`
    src_state_idx, dest_state_idx = states_from_transition_idx(
        transition,
        incidence_matrix,
    )
    dtype = events.dtype

    def unit():
        """Draw unit to update"""
        with tf.name_scope("unit"):
            return UniformKCategorical(
                num_units,
                mask=ps.ones(events.shape[-2], dtype=events.dtype),
                float_dtype=events.dtype,
                name="unit",
            )

    def timepoint():
        """Draw timepoint to move events to or from"""
        with tf.name_scope("timepoint"):
            return UniformInteger(
                low=[0], high=[max_timepoint + 1], float_dtype=dtype
            )

    def direction():
        r"""Do we move events from [-\infty, 0) into [0, max_timepoint]
           or vice versa?
        0=move from past into present
        1=move from present into past
        """
        with tf.name_scope("direction"):
            return UniformInteger(low=[0], high=[2], float_dtype=dtype)

    def num_events(unit, timepoint, direction):
        """Draw a number of events to move to/from `timepoint` in `unit`
        from the past into the present or vice versa according to `direction`.
        The number of possible events is bounded by the topology of the state
        transition model or a user-configurable `max_events`, whichever is the
        minimum.
        """
        with tf.name_scope("num_events"):
            # Events is a [num_timepoints, num_units, num_transitions] tensor.
            # We need to gather on the first 2 dimensions,
            # i.e. events[time_range, unit, :]
            unit_events = tf.gather(events, unit, axis=-2)  # Tx1xS
            unit_time_events = tf.gather(unit_events, time_range, axis=-3)
            # Initial state is a [M, S] tensor.  We gather the
            unit_initial_state = tf.gather(initial_state, unit, axis=-2)
            state = compute_state(
                unit_initial_state,
                unit_time_events,
                incidence_matrix,
            )  # TxMxS

            def pull_from_past():
                r"""Choose number of A->B transition events to move from
                pre-history into the events time-window, subject to the bound
                $$
                \phi(m,t,B) = \min (1, b_1,\dots, b_T, n_{\max})
                $$
                """
                with tf.name_scope("pull_from_past"):
                    state_ = state[..., dest_state_idx]  # TxM
                    state_ = _mask_max(state_, timepoint + 1, axis=-2)
                    x_bound = tf.minimum(
                        tf.reduce_min(state_, axis=-2), max_events
                    )
                    return x_bound

            def push_to_past():
                r"""Choose number of A->B transition events to move from events
                time-window into pre-history, subject to bound
                $$
                \phi{mtA} = \min (1, a_1,\dots, a_t, y^{AB}_{mt}, n_{\max})
                $$
                """
                # Extract vector of source state values over [0, max_timepoint]
                # for the selected metapopulation
                state_ = state[..., src_state_idx]  # TxM
                state_ = _mask_max(state_, timepoint, axis=-2)

                # Pushing to past is also bound by
                # events[timepoint, unit, transition]
                gather_indices = tf.stack(
                    [timepoint, unit, transition[tf.newaxis]],
                    axis=-1,
                )
                num_available_events = tf.gather_nd(events, gather_indices)

                x_bound = tf.concat(
                    [
                        state_,
                        num_available_events[tf.newaxis, :],
                        max_events[tf.newaxis, tf.newaxis],
                    ],
                    axis=-2,
                )
                x_bound = tf.reduce_min(x_bound, axis=0)

                return x_bound

            x_bound = tf.cast(
                tf.cond(
                    direction == 0,
                    true_fn=pull_from_past,
                    false_fn=push_to_past,
                ),
                tf.int32,
            )

            # tf.minimum is to cater for conditions where
            # `events[unit,timepoint,target]` == 0.  If it does,
            # we effectively return an identity proposal.
            return UniformInteger(
                low=tf.math.minimum(
                    1, x_bound
                ),  # x_bound may be 0 if no events
                high=x_bound + 1,  # are available
                float_dtype=dtype,
            )

    return tfd.JointDistributionNamed(
        {
            "unit": unit,
            "timepoint": timepoint,
            "direction": direction,
            "num_events": num_events,
        },
        name=name,
    )
