"""Test sparse distance"""

import numpy as np
import pytest
import tensorflow as tf

from .sp_dist import pdist, sparse_pdist


@pytest.mark.parametrize("dtype", [np.float32, np.float64])
def test_pdist(dtype):
    coords = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=dtype)

    expected = np.sqrt(
        np.array(
            [
                [0.0, 1.0, 1.0, 2.0],
                [1.0, 0.0, 2.0, 1.0],
                [1.0, 2.0, 0.0, 1.0],
                [2.0, 1.0, 1.0, 0.0],
            ],
            dtype=dtype,
        )
    )

    actual = pdist(coords, coords)

    assert tf.reduce_all(actual == expected)


def test_sparse_pdist(coords):
    N = coords.shape[-2]
    BATCH_SIZE = 32
    MAX_DIST = 0.101

    def include_fn(x):
        return tf.math.less(tf.zeros_like(x), x) & tf.math.less(
            x, tf.cast(MAX_DIST, x.dtype)
        )

    sparse_coords = sparse_pdist(
        coords, include_fn=include_fn, batch_size=BATCH_SIZE
    )

    expected_nnz = tf.reduce_sum(
        tf.cast(include_fn(pdist(coords, coords)), tf.int32)
    )

    assert sparse_coords.shape == [N, N]
    assert sparse_coords.values.shape[-1] == expected_nnz
