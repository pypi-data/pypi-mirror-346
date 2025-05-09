"""Markov chain Monte Carlo inference

`Markov-chain Monte Carlo (MCMC)
<https://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo>`_ is an algorithm used
for drawing from random variables when the probability density function is known
only up to a normalising constant.  This makes MCMC appropriate for sampling
from complex Bayesian posteriors.

:code:`gemlib.mcmc` provides a suite of composable MCMC kernels for use in both
general Bayesian hierarchical probability models and different types of state
transition model.  In particular, it provides a framework for composing
Metropolis-within-Gibbs algorithms which are especially useful for
semi-continuous probability spaces such as in Bayesian hierarchical state
transition models.
"""

import gemlib.mcmc.discrete_time_state_transition_model as discrete_time
from gemlib.mcmc.adaptive_hmc import adaptive_hmc, make_initial_running_variance
from gemlib.mcmc.adaptive_random_walk_metropolis import adaptive_rwmh
from gemlib.mcmc.deprecated.compound_kernel import CompoundKernel
from gemlib.mcmc.deprecated.h5_posterior import Posterior
from gemlib.mcmc.deprecated.multi_scan_kernel import MultiScanKernel
from gemlib.mcmc.hmc import hmc
from gemlib.mcmc.mcmc_sampler import mcmc
from gemlib.mcmc.multi_scan import multi_scan
from gemlib.mcmc.mwg_step import MwgStep
from gemlib.mcmc.random_walk_metropolis import rwmh
from gemlib.mcmc.sampling_algorithm import (
    ChainAndKernelState,
    ChainState,
    LogProbFnType,
    Position,
    SamplingAlgorithm,
    SeedType,
)
from gemlib.mcmc.transformed_sampling_algorithm import (
    transform_sampling_algorithm,
)

__all__ = [
    "CompoundKernel",
    "MultiScanKernel",
    "Posterior",
    "ChainState",
    "ChainAndKernelState",
    "Position",
    "MwgStep",
    "LogProbFnType",
    "SamplingAlgorithm",
    "SeedType",
    "adaptive_hmc",
    "adaptive_rwmh",
    "discrete_time",
    "hmc",
    "make_initial_running_variance",
    "mcmc",
    "multi_scan",
    "rwmh",
    "transform_sampling_algorithm",
]
