"""Gibbs sampling kernel"""

from collections import namedtuple
from warnings import warn

import tensorflow_probability as tfp
from tensorflow_probability.python.internal import (
    samplers,
    structural_tuple,
    unnest,
)
from tensorflow_probability.python.mcmc.internal import util as mcmc_util

__all__ = [
    "CompoundKernel",
    "split_unpinned_by_name",
    "unpinned_and_conditional_model",
]


class CompoundKernelResults(
    mcmc_util.PrettyNamedTupleMixin,
    namedtuple(
        "CompoundKernelResults",
        ["inner_results", "seed"],
    ),
):
    __slots__ = ()


def _make_namedtuple(input_dict):
    return structural_tuple.structtuple(input_dict.keys())(**input_dict)


def split_unpinned_by_name(full_struct_tuple, unpinned_names):
    """Splits a StructTuple of variables into `unpinned` and `pinned`

    :param full_struct_tuple: StructTuple to split
    :param unpinned_names: names of required unpinned vars
    :returns: a tuple `(unpinned: dict, pinned: dict)`
    """
    full_dict = full_struct_tuple._asdict()
    unpinned = _make_namedtuple(
        {k: v for k, v in full_dict.items() if k in unpinned_names}
    )
    pinned = _make_namedtuple(
        {k: v for k, v in full_dict.items() if k not in unpinned_names}
    )
    return unpinned, pinned


def unpinned_and_conditional_model(varnames, vars, joint_model):
    unpinned, pins = split_unpinned_by_name(vars, varnames)
    return unpinned, joint_model.experimental_pin(pins)


def _replace_tlp(current_results, other_results):
    """Replaces tlp in `current_results` with that in `other_results`"""
    other_results_wrapped = unnest.UnnestingWrapper(other_results)

    return unnest.replace_innermost(
        current_results, target_log_prob=other_results_wrapped.target_log_prob
    )


def _maybe_replace_grads(current_results, other_results):
    """Replaces grads in `current_results` with that in `other_results`"""
    other_results_wrapped = unnest.UnnestingWrapper(other_results)
    if hasattr(other_results_wrapped, "grads_target_log_prob"):
        return unnest.replace_innermost(
            current_results,
            grads_target_log_prob=other_results_wrapped.grads_target_log_prob,
        )
    return current_results


class CompoundKernel(tfp.mcmc.TransitionKernel):
    class Step(namedtuple("Step", ["varnames", "build"])):
        """Represents a Step within the CompoundKernel"""

        __slots__ = ()

    def __init__(self, joint_model, kernels, name=None):
        warn(
            "CompoundKernel is deprecated and will be removed in 2025.  \
Please use the new SamplingAlgorithm framework instead.",
            FutureWarning,
            stacklevel=2,
        )
        self._parameters = locals()

    @property
    def is_calibrated(self):
        return True

    @property
    def joint_model(self):
        return self._parameters["joint_model"]

    @property
    def kernels(self):
        return self._parameters["kernels"]

    @property
    def name(self):
        return self._parameters["name"]

    def one_step(self, current_state, previous_results, seed=None):
        seeds = samplers.split_seed(
            seed, n=len(self.kernels), salt="CompoundKernel.one_step"
        )

        next_results = []
        for kernel_tuple, results, seed_ in zip(
            self.kernels, previous_results.inner_results, seeds, strict=True
        ):
            # Create the sub-state and conditioned model to
            # then present to the kernel builder function.
            unpinned, conditional_model = unpinned_and_conditional_model(
                kernel_tuple.varnames, current_state, self.joint_model
            )
            kernel = kernel_tuple.build(conditional_model, current_state)

            # In a Gibbs scheme, we have to re-calculate the current value
            # (and grads) of the conditional log prob, pushing it back into
            # the previous kernel results.
            #
            # A nested CompoundKernel does not have a target_log_prob or grads,
            # so we can't do any replacement.  Fortunately this doesn't matter,
            # as one_step gets called recursively anyway.
            if not isinstance(results, CompoundKernelResults):
                pre_results = kernel.bootstrap_results(unpinned)
                step_results = _replace_tlp(results, pre_results)
                step_results = _maybe_replace_grads(step_results, pre_results)

            new_unpinned, next_kernel_results = kernel.one_step(
                unpinned, step_results, seed=seed_
            )

            # Update the global state
            current_state = current_state._replace(**new_unpinned._asdict())
            next_results.append(next_kernel_results)

        return (
            current_state,
            CompoundKernelResults(inner_results=tuple(next_results), seed=seed),
        )

    def bootstrap_results(self, current_state):
        results = []
        for kernel_tuple in self.kernels:
            unpinned, pins = split_unpinned_by_name(
                current_state, kernel_tuple.varnames
            )
            unpinned, conditional_model = unpinned_and_conditional_model(
                kernel_tuple.varnames, current_state, self.joint_model
            )
            kernel = kernel_tuple.build(conditional_model, current_state)
            results.append(kernel.bootstrap_results(unpinned))

        return CompoundKernelResults(
            inner_results=tuple(results), seed=samplers.zeros_seed()
        )
