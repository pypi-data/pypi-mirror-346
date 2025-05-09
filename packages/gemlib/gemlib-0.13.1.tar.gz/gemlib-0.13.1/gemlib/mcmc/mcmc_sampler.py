"""Higher-order functions to run MCMC"""

from collections.abc import Callable, Iterable
from functools import partial
from typing import Any

import tensorflow as tf
import tensorflow_probability as tfp

from .sampling_algorithm import SamplingAlgorithm

__all__ = ["mcmc"]


def _split_seed(seed, n):
    n = tf.convert_to_tensor(n)
    return tfp.random.split_seed(seed, n=n)


def _tensor_array_from_element(elem, size):
    elem = tf.convert_to_tensor(elem)
    return tf.TensorArray(
        elem.dtype,
        size=size,
        element_shape=elem.shape,
    )


def _scan(fn, init, xs):
    """Scan

    This function is equivalent to

    ```
    scan :: (c -> a -> (c, b)) -> c -> [a] -> (c, [b])
    ```
    """
    # Set up results accumulator
    _, initial_trace = fn(init, xs[0])

    flat_initial_trace = tf.nest.flatten(initial_trace, expand_composites=True)
    trace_arrays = []
    for trace_elem in flat_initial_trace:
        trace_arrays.append(
            _tensor_array_from_element(trace_elem, size=xs.shape[0])
        )

    def trace_one_step(i, trace_arrays, trace):
        return [
            ta.write(i, x)
            for ta, x in zip(
                trace_arrays,
                tf.nest.flatten(trace, expand_composites=True),
                strict=True,
            )
        ]

    def cond(i, _carry, _accum):
        return i < xs.shape[0]

    def body(i, carry, accum):
        new_carry, result = fn(carry, xs[i])
        new_accum = trace_one_step(i, accum, result)
        return i + 1, new_carry, new_accum

    _, final_state, trace_arrays = tf.while_loop(
        cond=cond, body=body, loop_vars=(0, init, trace_arrays)
    )

    stacked_trace = tf.nest.pack_sequence_as(
        initial_trace,
        [ta.stack() for ta in trace_arrays],
        expand_composites=True,
    )

    return final_state, stacked_trace


def mcmc(
    num_samples: int,
    sampling_algorithm: SamplingAlgorithm,
    target_density_fn: Callable[[Any, ...], float],
    initial_position: Iterable,
    seed: tuple[int, int],
    kernel_kwargs_fn=lambda _: {},
):
    """Runs an MCMC using `sampling_algorithm`

    Args:
      num_updates: integer giving the number of updates
      sampling_algorithm: an instance of `SamplingAlgorithm`
      target_density_fn: Python callable which takes an argument like
        `current_state` and returns its (possibly unnormalized) log-density
        under the target distribution.
      initial_position: initial state structured tuple
      seed: an optional list of two scalar ``int`` tensors.
      kernel_kwargs_fn: a callable taking the chain position as an argument,
        and returning a dictionary of extra kwargs


    Returns:
      A tuple containing samples of the Markov chain and information about the
      behaviour of the sampler(s) (e.g. whether kernels accepted or rejected,
      adaptive covariance matrices, etc).
    """

    initial_position = tf.nest.map_structure(
        lambda x: tf.convert_to_tensor(x), initial_position
    )
    initial_state = sampling_algorithm.init(
        target_density_fn,
        initial_position,
        **kernel_kwargs_fn(initial_position),
    )
    kernel_step_fn = partial(sampling_algorithm.step, target_density_fn)

    def one_step(state, rng_key):
        new_state, info = kernel_step_fn(
            state, rng_key, **kernel_kwargs_fn(state)
        )
        return new_state, (new_state[0].position, info)

    keys = _split_seed(seed, num_samples)

    _, trace = _scan(one_step, initial_state, keys)

    return trace
