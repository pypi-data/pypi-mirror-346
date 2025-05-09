"""Tensor utilities"""

from functools import reduce as ft_reduce

import tensorflow as tf

__all__ = ["broadcast_fn_to", "broadcast_together"]


def broadcast_together(*tensors):
    """Broadcast tensors together

    Args:
      *tensors: tensors

    Returns:
      a tuple of tensors broadcast to have common shape
    """
    shapes = [tf.shape(x) for x in tensors]

    common_shape = ft_reduce(
        lambda a, x: tf.broadcast_dynamic_shape(a, x), shapes
    )
    broadcast_tensors = [tf.broadcast_to(x, common_shape) for x in tensors]

    if len(tensors) == 1:
        return broadcast_tensors[0]

    return tuple(broadcast_tensors)


def broadcast_fn_to(func, shape):
    """Transform function `func` such that its outputs broadcast to `shape`"""

    def wrapped(*args, **kwargs):
        retval = func(*args, **kwargs)
        if isinstance(retval, tuple):
            return tuple(tf.broadcast_to(x, shape) for x in retval)
        return (tf.broadcast_to(retval, shape),)

    return wrapped
