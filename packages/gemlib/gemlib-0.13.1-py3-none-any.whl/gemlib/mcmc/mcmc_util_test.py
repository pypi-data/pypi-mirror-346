"""Test MCMC utilities"""

from typing import NamedTuple

import tensorflow as tf

from .mcmc_util import get_flattening_bijector


def test_get_flattening_bijector_scalar():
    val = tf.constant(0.1, dtype=tf.float32)

    bijector = get_flattening_bijector(val)

    flat_val = bijector(val)

    assert flat_val.shape[-1] == 1
    assert flat_val == tf.constant(0.1)


def test_get_flattening_bijector_list():
    val = [
        tf.constant(0.1, dtype=tf.float32),
        tf.constant(0.2, dtype=tf.float32),
    ]

    bijector = get_flattening_bijector(val)

    flat_val = bijector(val)

    flat_shape = 2
    assert flat_val.shape[-1] == flat_shape
    assert all(flat_val == tf.constant([0.1, 0.2], tf.float32))


def test_get_flattening_bijector_namedtuple():
    class Struct(NamedTuple):
        foo: float
        bar: float
        baz: float

    val = Struct(
        tf.constant(0.1, dtype=tf.float32),
        tf.constant([0.2, 0.3], dtype=tf.float32),
        tf.constant([[0.4, 0.5], [0.6, 0.7]], dtype=tf.float32),
    )

    bijector = get_flattening_bijector(val)

    flat_val = bijector(val)

    flat_shape = 7
    assert flat_val.shape[-1] == flat_shape
    assert all(
        flat_val == tf.constant([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], tf.float32)
    )
