"""Test state transition model utils"""

from gemlib.func_util import maybe_combine_fn


def test_maybe_combine_fn():
    fns = [lambda t, x: [t, x], lambda t, x: [t + 1, x + 1]]

    fn = maybe_combine_fn(fns)

    res = fn(1, 2)

    assert res == ([1, 2], [2, 3])
