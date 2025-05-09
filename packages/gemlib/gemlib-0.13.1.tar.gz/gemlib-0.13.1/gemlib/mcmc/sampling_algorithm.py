"""Base MCMC datatypes"""

from __future__ import annotations

from collections.abc import Callable
from functools import partial
from typing import Any, NamedTuple

import tensorflow as tf
import tensorflow_probability as tfp

split_seed = tfp.random.split_seed


__all__ = [
    "ChainState",
    "KernelState",
    "ChainAndKernelState",
    "LogProbFnType",
    "KernelInfo",
    "KernelInitFnType",
    "KernelStepFnType",
    "Position",
    "SamplingAlgorithm",
    "SeedType",
]


# Type aliases
Position = NamedTuple
KernelInfo = NamedTuple


class ChainState(NamedTuple):
    """Represent the state of an MCMC probability space"""

    position: Position
    log_density: float
    log_density_grad: float | None = ()


class KernelState(NamedTuple):
    """Represent the state of a stateful MCMC kernel"""

    pass


class ChainAndKernelState(NamedTuple):
    chain_state: ChainState
    kernel_state: KernelState


LogProbFnType = Callable[[Position], float]

KernelInitFnType = Callable[[LogProbFnType, Position], ChainAndKernelState]

SeedType = tuple[int, int]

KernelStepFnType = Callable[
    [LogProbFnType, ChainAndKernelState, SeedType],
    tuple[ChainAndKernelState, KernelInfo],
]


def _maybe_flatten(x: list[Any]):
    """Flatten a list if `len(x) <= 1`"""
    if len(x) == 0:
        return None
    if len(x) == 1:
        return x[0]
    return x


def _squeeze(x: list[Any]):
    if len(x) == 1:
        return x[0]
    return x


def _maybe_list(x):
    if isinstance(x, list):
        return x
    return [x]


def _maybe_tuple(x):
    if type(x) is tuple:
        return x
    return (x,)


class KernelInitMonad:
    """KernelInitMonad is a Writer monad allowing us to build an initial
    state tuple for a Metropolis-within-Gibbs algorithm
    """

    def __init__(self, fn: KernelInitFnType):
        """The monad 'unit' function"""
        self._fn = fn

    def __call__(self, *args, **kwargs):
        """Monad ``run'' function"""
        return self._fn(*args, **kwargs)

    def then(self, next_kernel_init_fn: KernelInitMonad):
        """Monad combination, i.e. Haskell fish operator"""

        @KernelInitMonad
        def compound_init_fn(
            target_log_prob_fn: LogProbFnType,
            initial_position: ChainState,
        ) -> KernelInitFnType:
            _, self_kernel_state = self(target_log_prob_fn, initial_position)
            next_chain_state, next_kernel_state = next_kernel_init_fn(
                target_log_prob_fn, initial_position
            )

            return (
                next_chain_state,
                _maybe_list(self_kernel_state) + [next_kernel_state],
            )

        return compound_init_fn

    def __rshift__(self, next_kernel: KernelInitMonad):
        return self.then(next_kernel)


class KernelStepMonad:
    """StepMonad is a state monad that allows us to chain MCMC kernels
    together.
    """

    def __init__(self, fn: KernelStepFnType):
        """The monad 'unit' function"""
        self._fn = fn  # Make private

    def __call__(self, *args, **kwargs):
        """Apply the state transformer computation to a state."""
        return self._fn(*args, **kwargs)

    def then(self, next_kernel_fn: KernelStepMonad):
        """The monad 'bind' operator which allows chaining.
        ma >> mb :: ma -> mb -> mc
        """

        @KernelStepMonad
        def compound_step_kernel(
            target_log_prob_fn: LogProbFnType,
            chain_and_kernel_state: ChainAndKernelState,
            seed: SeedType,
        ) -> tuple[ChainAndKernelState, KernelInfo]:
            self_seed, next_seed = split_seed(seed)

            chain_state, kernel_state = chain_and_kernel_state

            self_kernel_state = _squeeze(kernel_state[:-1])
            next_kernel_state = kernel_state[-1]

            (chain_state, self_kernel_state), self_info = self._fn(
                target_log_prob_fn,
                (chain_state, self_kernel_state),
                seed=self_seed,
            )

            (chain_state, next_kernel_state), next_info = next_kernel_fn(
                target_log_prob_fn,
                (chain_state, next_kernel_state),
                seed=next_seed,
            )

            return (
                (
                    chain_state,
                    _maybe_list(self_kernel_state) + [next_kernel_state],
                ),
                _maybe_list(self_info) + [next_info],
            )

        return compound_step_kernel

    def __rshift__(self, next_kernel: KernelStepMonad):
        return self.then(next_kernel)


class SamplingAlgorithm:
    """Represent a sampling algorithm"""

    def __init__(
        self,
        init_fn: KernelInitFnType | KernelInitMonad,
        step_fn: KernelStepFnType | KernelStepMonad,
    ):
        if isinstance(init_fn, KernelInitMonad) and isinstance(
            step_fn, KernelStepMonad
        ):
            self._init: KernelInitMonad = init_fn
            self._step: KernelStepMonad = step_fn
        else:
            self._init: KernelInitMonad = KernelInitMonad(init_fn)
            self._step: KernelStepMonad = KernelStepMonad(step_fn)

    def init(self, *args, **kwargs):
        """Initialize and MCMC chain"""
        return self._init(*args, **kwargs)

    def step(self, *args, **kwargs):
        """Function to invoke the MCMC kernel"""
        return self._step(*args, **kwargs)

    def then(self, next_kernel: SamplingAlgorithm):
        """Sequential combinator"""
        return SamplingAlgorithm(
            init_fn=(self._init >> next_kernel._init),
            step_fn=(self._step >> next_kernel._step),
        )

    def __rshift__(self, next_kernel: SamplingAlgorithm):
        return self.then(next_kernel)

    def __mul__(self, n: int):
        """Performs multiple applications of a kernel

        :obj:`sampling_algorithm` is invoked :obj:`n` times
        returning the state and info after the last step.

        Args:
            num_updates: integer giving the number of updates
            sampling_algorithm: an instance of :obj:`SamplingAlgorithm`

        Returns:
            An instance of :obj:`SamplingAlgorithm`
        """
        return _repeat_sampling_algorithm(n, self)


def _repeat_sampling_algorithm(
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

    num_updates_ = tf.convert_to_tensor(num_updates)

    def init_fn(target_log_prob_fn, position):
        cs, ks = sampling_algorithm.init(target_log_prob_fn, position)
        return cs, ks

    def step_fn(
        target_log_prob_fn: LogProbFnType,
        current_state: tuple[Position, NamedTuple],
        seed=None,
    ):
        seeds = tfp.random.split_seed(
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
            (chain_state, kernel_state), seed
        )  # unrolled first it

        _, last_state, last_info = tf.while_loop(
            cond, body, loop_vars=(1, init_state, init_info)
        )

        return last_state, last_info

    return SamplingAlgorithm(init_fn, step_fn)
