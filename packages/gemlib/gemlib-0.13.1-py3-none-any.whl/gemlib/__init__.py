"""gemlib scientific compute library for epidemics."""

import importlib.metadata

__version__ = importlib.metadata.version(__package__)

from gemlib import distributions, mcmc, util

__all__ = ["mcmc", "distributions", "util"]
