"""Utility functions for state transition models"""

from collections.abc import Callable, Iterable
from warnings import warn


def _check_deprecated(fn):
    def dep_fn(*args, **kwargs):
        result = fn(*args, **kwargs)
        if isinstance(result, tuple):
            warn(
                "Returning a tuple of tensors is \
            deprecated. Please instead supply a list of functions returning \
            single tensors.  This functionality will be removed in a future \
            release.",
                DeprecationWarning,
                stacklevel=3,
            )
        return result

    return dep_fn


def maybe_combine_fn(fn: Callable | Iterable[Callable]) -> Callable:
    """Takes an iterable of Callables of the same signature, returning a
    function that combines their results as a tuple."""

    if isinstance(fn, Iterable):

        def fn_combined(*args, **kwargs):
            return tuple([f(*args, **kwargs) for f in fn])

        return fn_combined

    return _check_deprecated(fn)
