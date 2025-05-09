"""Implementation of Metropolis-within-Gibbs framework"""

from __future__ import annotations

from collections import ChainMap, namedtuple
from collections.abc import Callable
from typing import AnyStr

import tensorflow_probability as tfp

from gemlib.mcmc.mcmc_util import is_list_like
from gemlib.mcmc.sampling_algorithm import (
    ChainAndKernelState,
    ChainState,
    KernelInfo,
    LogProbFnType,
    Position,
    SamplingAlgorithm,
    SeedType,
)

split_seed = tfp.random.split_seed

__all__ = ["MwgStep"]


def _project_position(
    position: Position, varnames: list[AnyStr]
) -> tuple[Position, Position]:
    """Splits `position` into `position[varnames]` and
    `position[~varnames]`
    """
    if varnames is None:
        return position, ()

    varnames_ = varnames if is_list_like(varnames) else [varnames]

    for name in varnames_:
        if name not in position._asdict():
            raise ValueError(f"`{name}` is not present in `position`")

    target = {k: v for k, v in position._asdict().items() if k in varnames_}
    target_compl = {
        k: v for k, v in position._asdict().items() if k not in varnames_
    }

    if is_list_like(varnames):
        target = namedtuple("Target", target.keys())(**target)
    else:
        target = target[varnames]

    return (
        target,
        namedtuple("TargetCompl", target_compl.keys())(**target_compl),
    )


def _inject_dict(
    target: float | tuple | Position,
    target_compl: Position,
    varnames: list[str] | str,
) -> dict:
    if hasattr(target, "_asdict"):  # Position
        target_dict = target._asdict()
        assert set(target_dict.keys()) == set(varnames)
    elif is_list_like(target):  # tuple
        assert varnames is not None
        varnames_ = varnames if is_list_like(varnames) else [varnames]
        target_dict = dict(zip(varnames_, target, strict=True))
    else:  # float
        assert varnames is not None
        varnames_ = varnames if is_list_like(varnames) else [varnames]
        target_dict = {varnames_[0]: target}

    if varnames is None:
        return target_dict

    return target_dict | target_compl._asdict()


def _join_dicts(a: dict, b: dict):
    """Joins two dictionaries `a` and `b`"""
    return dict(ChainMap(a, b))


class MwgStep:  # pylint: disable=too-few-public-methods
    """A Metropolis-within-Gibbs step.

    Transforms a base kernel to operate on a substate of a Markov chain.

    Args:
      sampling_algorithm: a named tuple containing the generic kernel `init`
                        and `step` function.
      target_names: a list of variable names on which the
                        Metropolis-within-Gibbs step is to operate
      kernel_kwargs_fn: a callable taking the chain position as an argument,
                    and returning a dictionary of extra kwargs to
                    `sampling_algorithm.step`.

    Returns:
      An instance of SamplingAlgorithm.

    """

    def __new__(
        cls,
        sampling_algorithm: SamplingAlgorithm,
        target_names: list[str] | None = None,
        kernel_kwargs_fn: Callable[[Position], dict] = lambda _: {},
    ):
        def init(
            target_log_prob_fn: LogProbFnType,
            initial_position: Position,
        ):
            target, target_compl = _project_position(
                initial_position, target_names
            )

            def conditional_tlp(*args):
                tlp_args = _inject_dict(args, target_compl, target_names)
                return target_log_prob_fn(**tlp_args)

            kernel_state = sampling_algorithm.init(
                conditional_tlp, target, **kernel_kwargs_fn(initial_position)
            )

            chain_state = ChainState(
                position=initial_position,
                log_density=kernel_state[0].log_density,
                log_density_grad=kernel_state[0].log_density_grad,
            )

            return chain_state, kernel_state[1]

        def step(
            target_log_prob_fn: LogProbFnType,
            chain_and_kernel_state: ChainAndKernelState,
            seed: SeedType,
        ) -> tuple[ChainAndKernelState, KernelInfo]:
            chain_state, kernel_state = chain_and_kernel_state

            # Split global state and generate conditional density
            target, target_compl = _project_position(
                chain_state.position, target_names
            )

            # Calculate the conditional log density
            def conditional_tlp(*args):
                tlp_args = _inject_dict(args, target_compl, target_names)
                return target_log_prob_fn(**tlp_args)

            chain_substate = chain_state._replace(position=target)

            # Invoke the kernel on the target state
            (new_chain_substate, new_kernel_state), info = (
                sampling_algorithm.step(
                    conditional_tlp,
                    (chain_substate, kernel_state),
                    seed,
                    **kernel_kwargs_fn(chain_state.position),
                )
            )

            # Stitch the global position back together
            new_global_position = chain_state.position.__class__(
                **_inject_dict(
                    new_chain_substate.position, target_compl, target_names
                )
            )
            new_global_state = new_chain_substate._replace(
                position=new_global_position
            )

            return (new_global_state, new_kernel_state), info

        return SamplingAlgorithm(init, step)
