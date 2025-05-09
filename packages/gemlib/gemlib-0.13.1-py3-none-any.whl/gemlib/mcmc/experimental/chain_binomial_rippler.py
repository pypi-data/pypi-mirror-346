"""Chain binomial process rippler algorithm"""

import warnings
from collections import namedtuple

import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import prefer_static, samplers
from tensorflow_probability.python.mcmc.internal import util as mcmc_util

from gemlib.distributions.hypergeometric import Hypergeometric
from gemlib.distributions.uniform_integer import UniformInteger

tfd = tfp.distributions

__all__ = ["chain_binomial_rippler", "default_initial_ripple"]


def _compute_state(initial_state, events, stoichiometry, closed=False):
    """Computes a state tensor from initial state and event tensor

    :param initial_state: a tensor of shape [S, M]
    :param events: a tensor of shape [T, R, M]
    :param stoichiometry: a stoichiometry matrix of shape [R, S] describing
                          how transitions update the state.
    :param closed: if `True`, return state in close interval [0, T], otherwise
                   [0, T)
    :return: a tensor of shape [T, S, M] if `closed=False` or [T+1, S, M] if
             `closed=True`
             describing the state of the
             system for each batch M at time T.
    """
    if isinstance(stoichiometry, tf.Tensor):
        stoichiometry = prefer_static.cast(stoichiometry, dtype=events.dtype)
    else:
        stoichiometry = tf.convert_to_tensor(stoichiometry, dtype=events.dtype)

    increments = tf.einsum("...trm,rs->...tsm", events, stoichiometry)

    if closed is False:
        cum_increments = tf.cumsum(increments, axis=-3, exclusive=True)
    else:
        cum_increments = tf.cumsum(increments, axis=-3, exclusive=False)
        cum_increments = tf.concat(
            [tf.zeros_like(cum_increments[..., 0:1, :, :]), cum_increments],
            axis=-2,
        )
    state = cum_increments + tf.expand_dims(initial_state, axis=-3)
    return state


def _log_factorial(x):
    """Computes x!"""
    return tf.math.lgamma(x + 1.0)


def _log_choose(n, k):
    """Computes nCk"""
    return _log_factorial(n) - _log_factorial(k) - _log_factorial(n - k)


# Basic rippler sampling functions
def _pstep(z, x, p, ps, seed=None, validate_args=False):
    """Compute the p-step of Rippler.

    Since there are two possible distributions to draw from,
    but both are Binomial, we compute `offset`, `total_count`, and
    `prob` parameters for both branches, and select which we need
    based on p <= ps.

    :param z: current $z$
    :param x: current $x$
    :param p: current probability
    :param ps: new probability
    """
    with tf.name_scope("_pstep"):
        offset = tf.where(ps <= p, tf.zeros(1, dtype=z.dtype), z)
        prob = tf.where(ps <= p, ps / p, 1 - (1 - ps) / (1 - p))
        total_count = tf.where(
            ps <= p, tf.cast(z, p.dtype), tf.cast(x - z, p.dtype)
        )
        z_prime = offset + tfd.Binomial(
            total_count=total_count,
            probs=prob,
            validate_args=validate_args,
            name="_pstep_Binomial",
        ).sample(seed=seed)
        return z_prime


def _xstep(z_prime, x, xs, ps, seed=None):
    """Computes the x-step of the Rippler algorithm.

    Both xs >= x and xs < x are sampled and results selected.
    """
    with tf.name_scope("_xstep"):
        seeds = samplers.split_seed(seed, salt="_xstep")

        # xs >= x
        # Switch off `validate_args` because `xs-x` may be -ve.
        z_new_geq = z_prime + tfd.Binomial(
            xs - x,
            probs=ps,
            validate_args=False,
            name="_xstep_Binomial",
        ).sample(seed=seeds[0])

        # xs < x - explicitly vectorize
        def safe_hypergeom(N, K, n):  # noqa: N803
            # xs is clipped to min(x, xs) to avoid errors in the Hypergeometric
            # sampler these values won't be selected anyway due to the
            # xs >= x condition below.
            return Hypergeometric(
                N=N,
                K=K,
                n=tf.math.minimum(N, n),
                validate_args=False,
                name="_xstep_Hypergeom",
            )

        z_new_lt = safe_hypergeom(x, z_prime, xs).sample(seed=seeds[1])

        return tf.where(xs >= x, z_new_geq, z_new_lt)


def _dispatch_update(z, x, p, xs, ps, seed=None):
    r"""Dispatches update function based on values of
       parameters.

    :param z: current $z$
    :param x: current $x$
    :param p: $p$ current probability
    :param xs: $x^\star$ new state
    :param ps: $p_star$ new probability

    :returns: an updated number of events
    """
    with tf.name_scope("dispatch_update"):
        p = tf.convert_to_tensor(p)
        ps = tf.convert_to_tensor(ps)
        z = tf.cast(z, p.dtype)
        x = tf.cast(x, p.dtype)
        xs = tf.cast(xs, p.dtype)

        seeds = samplers.split_seed(seed, salt="_dispatch_update")

        z_prime = _pstep(z, x, p, ps, seed=seeds[0])
        z_new = _xstep(z_prime, x, xs, ps, seed=seeds[1])

        return z_new


# Tests
def test_dispatch():
    tf.debugging.assert_scalar(
        _dispatch_update(z=10, x=100, p=0.1, xs=100, ps=0.1)
    )
    tf.debugging.assert_scalar(
        _dispatch_update(z=10, x=100, p=0.1, xs=100, ps=0.05)
    )
    tf.debugging.assert_scalar(
        _dispatch_update(z=10, x=100, p=0.1, xs=100, ps=0.2)
    )
    tf.debugging.assert_scalar(
        _dispatch_update(z=10, x=100, p=0.1, xs=50, ps=0.1)
    )
    tf.debugging.assert_scalar(
        _dispatch_update(z=10, x=100, p=0.1, xs=50, ps=0.05)
    )
    tf.debugging.assert_scalar(
        _dispatch_update(z=10, x=100, p=0.1, xs=50, ps=0.2)
    )
    tf.debugging.assert_scalar(
        _dispatch_update(z=10, x=100, p=0.1, xs=200, ps=0.1)
    )
    tf.debugging.assert_scalar(
        _dispatch_update(z=10, x=100, p=0.1, xs=200, ps=0.05)
    )
    tf.debugging.assert_scalar(
        _dispatch_update(z=10, x=100, p=0.1, xs=200, ps=0.2)
    )


def default_initial_ripple(model, current_events, current_state, seed):
    """Produces the initial ripple.

    :param model: an instance of `DiscreteTimeStateTransitionModel`
    :param current_events: a tensor of events in [T, R, M] order
    :param current_state: a tensor of state in [T, S, M] order
    :param seed: the seed to initialise the ripple

    :returns: a tuple of `(proposed_time_idx, new_events_t, current_state_t)`
    """
    init_time_seed, init_pop_seed, init_events_seed = samplers.split_seed(
        seed, n=3, salt="_initial_ripple"
    )

    # Choose timepoint, t
    proposed_time_idx = UniformInteger(low=0, high=model.num_steps).sample(
        seed=init_time_seed
    )
    current_state_t = tf.gather(current_state, proposed_time_idx, axis=-3)

    # Choose subpopulation - KCategorical?
    proposed_pop_idx = UniformInteger(
        low=0, high=current_events.shape[-1]
    ).sample(seed=init_pop_seed)

    # Choose new infection events at time t
    proposed_transition_rates = tf.stack(
        model.transition_rate_fn(
            proposed_time_idx, tf.transpose(current_state_t)
        ),
        axis=0,
    )
    prob_t = 1.0 - tf.math.exp(
        -tf.gather(proposed_transition_rates[0], proposed_pop_idx, axis=-1)
        * model.time_delta,
    )  # First event to perturb.

    required_state = tf.gather(current_state_t[0], proposed_pop_idx, axis=-1)
    new_si_events_t = tfd.Binomial(
        total_count=required_state,
        probs=prob_t,  # Perturb SI events here
    ).sample(seed=init_events_seed)

    new_events_t = tf.tensor_scatter_nd_update(
        current_events[proposed_time_idx],
        [[0, proposed_pop_idx]],
        [new_si_events_t],
    )

    return proposed_time_idx, new_events_t, current_state_t


def chain_binomial_rippler(model, current_events, initial_ripple_fn, seed=None):
    init_seed, ripple_seed = samplers.split_seed(
        seed, salt="chain_binomial_rippler"
    )

    src_states = model.source_states
    # Transpose to [T, S/R, M]
    current_events = tf.transpose(current_events, perm=(0, 2, 1))

    # Calculate current state
    current_state = _compute_state(
        initial_state=tf.transpose(model.initial_state),
        events=current_events,
        stoichiometry=tf.transpose(model.incidence_matrix),
    )

    # Begin the ripple by sampling a time point, and perturbing the
    # events at that timepoint
    (
        proposed_time_idx,
        new_events_t,
        current_state_t,
    ) = initial_ripple_fn(model, current_events, current_state, init_seed)
    new_events = tf.tensor_scatter_nd_update(
        current_events, indices=[[proposed_time_idx]], updates=[new_events_t]
    )

    # Propagate from t+1 up to end of the timeseries
    def draw_events(time, new_state_t, current_events_t, current_state_t, seed):
        with tf.name_scope("draw_events"):
            # Calculate transition rates for current and new states
            def transition_probs(time, state):
                rates = tf.stack(
                    model.transition_rate_fn(time, tf.transpose(state)), axis=-2
                )
                return 1.0 - tf.math.exp(-rates * model.time_delta)

            current_p = transition_probs(time, current_state_t)
            new_p = transition_probs(time, new_state_t)

            new_events = _dispatch_update(
                z=current_events_t,
                x=prefer_static.gather(current_state_t, indices=src_states),
                p=current_p,
                xs=prefer_static.gather(new_state_t, indices=src_states),
                ps=new_p,
                seed=seed,
            )
            tf.debugging.assert_non_negative(new_events)

            return new_events

    def time_loop_body(t, new_events_t, new_state_t, new_events_buffer, seed):
        sample_seed, next_seed = samplers.split_seed(
            seed, salt="time_loop_body"
        )

        # Propagate new_state[t] to new_state[t+1]
        new_state_t1 = new_state_t + tf.einsum(
            "...ik,ji->...jk", new_events_t, model.incidence_matrix
        )
        # tf.debugging.assert_non_negative(new_state_t1, summarize=100)

        # Gather current states and events, and draw new events
        new_events_t1 = draw_events(
            t + 1,
            new_state_t1,
            current_events[t + 1],
            current_state[t + 1],
            sample_seed,
        )

        # Update new_events_buffer
        new_events_buffer = tf.tensor_scatter_nd_update(
            new_events_buffer, indices=[[t + 1]], updates=[new_events_t1]
        )

        return t + 1, new_events_t1, new_state_t1, new_events_buffer, next_seed

    def time_loop_cond(t, _1, _2, new_events_buffer, _3):
        t_stop = t < (model.num_steps - 1)
        delta_stop = tf.reduce_any(new_events_buffer != current_events)
        return t_stop & delta_stop

    _, _, _, new_events, _ = tf.while_loop(
        time_loop_cond,
        time_loop_body,
        loop_vars=(
            proposed_time_idx,
            new_events_t,
            current_state_t,
            new_events,
            ripple_seed,
        ),
    )  # new_events.shape = [T, R, M]

    new_events = tf.transpose(new_events, perm=(0, 2, 1))

    return (
        new_events,
        {
            "delta": tf.transpose(
                new_events_t - current_events[proposed_time_idx]
            ),
            "timepoint": proposed_time_idx,
            "initial_ripple": new_events_t,
            "current_state_t": tf.transpose(current_state_t),
        },
    )


# The Chain Binomial Rippler kernel
CBRResults = namedtuple(
    "CBRResults",
    [
        "target_log_prob",
        "is_accepted",
        "delta",
        "current_state_t",
        "initial_ripple",
        "timepoint",
        "proposed_state",
        "proposed_target_log_prob",
        "seed",
    ],
)


class CBRKernel(tfp.mcmc.TransitionKernel):
    def __init__(
        self,
        target_log_prob_fn,
        model,
        initial_ripple_fn=default_initial_ripple,
        ripple_decay_rate=0.1,
        name=None,
    ):
        self._target_log_prob_fn = target_log_prob_fn
        self._model = model

        name = mcmc_util.make_name(name, "CBRKernel", "")

        self._parameters = {
            "target_log_prob_fn": target_log_prob_fn,
            "model": model,
            "initial_ripple_fn": initial_ripple_fn,
            "ripple_decay_rate": ripple_decay_rate,
            "name": name,
        }

    @property
    def is_calibrated(self):
        return True

    @property
    def target_log_prob(self):
        return self._target_log_prob_fn

    @property
    def model(self):
        return self._model

    @property
    def name(self):
        return self._parameters["name"]

    @property
    def initial_ripple_fn(self):
        return self._parameters["initial_ripple_fn"]

    def one_step(self, current_state, previous_results, seed=None):
        with tf.name_scope("CBRKernel/one_step"):
            seed_rippler, seed_u, seed_results = samplers.split_seed(
                seed, n=3, salt="cbr_kernel"
            )

            if mcmc_util.is_list_like(current_state):
                current_state_parts = list(current_state)
            else:
                current_state_parts = [current_state]

            if len(current_state_parts) > 1:
                warnings.warn(
                    "CBRKernel.boostrap_results: multiple state parts detected,\
 but only the first will be used",
                    stacklevel=2,
                )

            current_state_part = tf.convert_to_tensor(
                current_state_parts[0], name="current_state"
            )

            proposed_state, proposal_trace = chain_binomial_rippler(
                self.model,
                current_state_part,
                initial_ripple_fn=self.initial_ripple_fn,
                seed=seed_rippler,
            )

            proposed_target_log_prob = self.target_log_prob(proposed_state)

            delta_logp = (
                proposed_target_log_prob - previous_results.target_log_prob
            )

            def accept():
                return (
                    proposed_state,
                    CBRResults(
                        target_log_prob=proposed_target_log_prob,
                        is_accepted=tf.constant(True),
                        delta=proposal_trace["delta"],
                        current_state_t=proposal_trace["current_state_t"],
                        initial_ripple=proposal_trace["initial_ripple"],
                        timepoint=proposal_trace["timepoint"],
                        proposed_state=proposed_state,
                        proposed_target_log_prob=proposed_target_log_prob,
                        seed=seed_results,
                    ),
                )

            def reject():
                return (
                    current_state_part,
                    CBRResults(
                        target_log_prob=previous_results.target_log_prob,
                        is_accepted=tf.constant(False),
                        delta=proposal_trace["delta"],
                        current_state_t=proposal_trace["current_state_t"],
                        initial_ripple=proposal_trace["initial_ripple"],
                        timepoint=proposal_trace["timepoint"],
                        proposed_state=proposed_state,
                        proposed_target_log_prob=proposed_target_log_prob,
                        seed=seed_results,
                    ),
                )

            u = tf.math.log(
                tfd.Uniform(low=tf.zeros(1, dtype=delta_logp.dtype)).sample(
                    seed=seed_u
                )
            )
            new_state, results = tf.cond(u < delta_logp, accept, reject)

            def maybe_flatten(x):
                if mcmc_util.is_list_like(current_state):
                    return type(current_state)(new_state)
                return x

            new_state = maybe_flatten(new_state)
            return new_state, results

    def bootstrap_results(self, current_state):
        with tf.name_scope("CBRKernel/bootstrap_results"):
            if mcmc_util.is_list_like(current_state):
                current_state_parts = list(current_state)
            else:
                current_state_parts = [current_state]

            if len(current_state_parts) > 1:
                warnings.warn(
                    "CBRKernel.boostrap_results: multiple state parts detected,\
 but only the first will be used",
                    stacklevel=2,
                )
            state_part = current_state_parts[0]

            num_pop = state_part.shape[-3]
            num_transitions = state_part.shape[-1]
            num_states = self.model.incidence_matrix.shape[-2]

            target_log_prob = self.target_log_prob(state_part)

            return CBRResults(
                target_log_prob=target_log_prob,
                is_accepted=tf.constant(False),
                delta=tf.zeros((num_pop, num_transitions), state_part.dtype),
                current_state_t=tf.zeros(
                    [num_pop, num_states], state_part.dtype
                ),
                initial_ripple=tf.zeros(
                    (num_transitions, num_pop), state_part.dtype
                ),
                timepoint=tf.constant(0, dtype=tf.int32),
                proposed_state=state_part,
                proposed_target_log_prob=target_log_prob,
                seed=samplers.zeros_seed(),
            )
