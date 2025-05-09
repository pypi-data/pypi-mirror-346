"""A dummy kernel that simply logs the shape of the state"""

from typing import NamedTuple

import tensorflow as tf

from gemlib.mcmc.experimental.sampling_algorithm import (
    ChainState,
    SamplingAlgorithm,
)


class TraceKernelState(NamedTuple):
    pass


class TraceKernelInfo(NamedTuple):
    name: str
    shapes: tuple


def trace_kernel(name=None):
    def init_fn(target_log_prob_fn, position):
        print(f"{name}/init target:", position)

        chain_state = ChainState(
            position=position, log_density=target_log_prob_fn(*position)
        )
        kernel_state = ()
        return chain_state, kernel_state

    def step_fn(target_log_prob_fn, position, seed):  # noqa: ARG001
        shapes = tf.map_structure(lambda x: tf.shape(x), position)
        print(f"{name}/step target shape:", shapes)

        chain_state = ChainState(
            position=position, log_density=target_log_prob_fn(*position)
        )
        kernel_state = TraceKernelState()
        return (chain_state, kernel_state), TraceKernelInfo(name, shapes)

    return SamplingAlgorithm(init_fn, step_fn)
