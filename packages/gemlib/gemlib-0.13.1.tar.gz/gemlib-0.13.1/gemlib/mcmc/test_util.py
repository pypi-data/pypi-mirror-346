"""Simple counting kernel for testing"""

from typing import NamedTuple

import tensorflow as tf

from .sampling_algorithm import ChainState, SamplingAlgorithm

__all__ = ["CountingKernelInfo", "CountingKernelState", "counting_kernel"]


class CountingKernelState(NamedTuple):
    invocation: int


class CountingKernelInfo(NamedTuple):
    is_accepted: bool


def counting_kernel():
    def init_fn(target_log_prob_fn, position):
        chain_state = ChainState(
            position=position,
            log_density=target_log_prob_fn(**position._asdict()),
            log_density_grad=(),
        )
        kernel_state = CountingKernelState(tf.constant(0))

        return chain_state, kernel_state

    def step_fn(target_log_prob_fn, chain_and_kernel_state, seed):  # noqa: ARG001
        chain_state, kernel_state = chain_and_kernel_state

        new_position = chain_state.position.__class__(
            **{k: v + 1.0 for k, v in chain_state.position._asdict().items()}
        )

        new_chain_state = ChainState(
            position=new_position,
            log_density=target_log_prob_fn(**new_position._asdict()),
            log_density_grad=(),
        )
        new_kernel_state = CountingKernelState(kernel_state.invocation + 1)

        return (new_chain_state, new_kernel_state), CountingKernelInfo(
            tf.constant(True)
        )

    return SamplingAlgorithm(init_fn, step_fn)
