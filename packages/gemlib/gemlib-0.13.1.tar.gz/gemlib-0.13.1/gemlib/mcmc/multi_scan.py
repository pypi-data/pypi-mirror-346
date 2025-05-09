"""MultiScanKernel calls one_step a number of times on an inner kernel"""

from functools import partial
from typing import NamedTuple
from warnings import warn

import tensorflow as tf
from tensorflow_probability.python.internal import samplers

from .sampling_algorithm import LogProbFnType, Position, SamplingAlgorithm

__all__ = ["multi_scan"]


class MultiScanKernelState(NamedTuple):
    last_results: NamedTuple


class MultiScanKernelInfo(NamedTuple):
    last_results: NamedTuple


def multi_scan(
    num_updates: int, sampling_algorithm: SamplingAlgorithm
) -> SamplingAlgorithm:
    """Performs multiple applications of a kernel

    :obj:`sampling_algorithm` is invoked :obj:`num_updates` times
    returning the state and info after the last step.

    Args:
      num_updates: integer giving the number of updates
      sampling_algorithm: an instance of :obj:`SamplingAlgorithm`

    Returns:
      An instance of :obj:`SamplingAlgorithm`
    """
    warn(
        "Use of `multi_scan` is deprecated, and will be removed in future.\
    Instead, please make use of SamplingAlgorithm.__mul__.",
        DeprecationWarning,
        stacklevel=2,
    )

    num_updates_ = tf.convert_to_tensor(num_updates)

    def init_fn(target_log_prob_fn, position):
        cs, ks = sampling_algorithm.init(target_log_prob_fn, position)
        return cs, MultiScanKernelState(ks)

    def step_fn(
        target_log_prob_fn: LogProbFnType,
        current_state: tuple[Position, MultiScanKernelState],
        seed=None,
    ):
        seeds = samplers.split_seed(
            seed, n=num_updates, salt="multi_scan_kernel"
        )
        step_fn = partial(sampling_algorithm.step, target_log_prob_fn)

        def body(i, state, _):
            state, info = step_fn(state, tf.gather(seeds, i, axis=-2))
            return i + 1, state, info

        def cond(i, *_):
            return i < num_updates_

        chain_state, kernel_state = current_state

        init_state, init_info = step_fn(
            (chain_state, kernel_state.last_results), seed
        )  # unrolled first it

        _, last_state, last_info = tf.while_loop(
            cond, body, loop_vars=(1, init_state, init_info)
        )

        return (
            (last_state[0], MultiScanKernelState(last_state[1])),
            MultiScanKernelInfo(last_info),
        )

    return SamplingAlgorithm(init_fn, step_fn)
