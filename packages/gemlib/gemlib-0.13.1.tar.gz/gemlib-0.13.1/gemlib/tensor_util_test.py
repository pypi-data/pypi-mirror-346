"""Test tensor utilities"""

import tensorflow as tf

from gemlib.tensor_util import broadcast_fn_to, broadcast_together


def test_broadcast_together():
    foo = [[1.0], [0.1]]
    bar = tf.constant([[2.0, 3.0, 4.0], [5.0, 6.0, 7.0]])
    baz = 8.0

    # All together
    result = broadcast_together(foo, bar, baz)

    assert all(x.shape == bar.shape for x in result)

    # Scalar and un-tuple
    result = broadcast_together(baz)
    assert result.shape == ()

    # One tensor and un-tuple
    result = broadcast_together(foo)
    assert result.shape == (2, 1)


def test_broadcast_fn_to():
    def func():
        return tf.constant([[1], [2], [3]]), tf.constant(4)

    bcast_func = broadcast_fn_to(func, shape=(3, 1))

    output = bcast_func()

    assert output[0].shape == output[1].shape
