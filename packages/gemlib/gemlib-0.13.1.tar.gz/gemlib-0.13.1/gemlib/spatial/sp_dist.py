"""Compute a sparse distance matrix given coordinates"""

from collections.abc import Callable

import numpy as np
import tensorflow as tf
from tensorflow import sparse as ts
from tqdm import tqdm

__all__ = ["pdist", "sparse_pdist"]


def pdist(a, b):
    """Compute the Euclidean distance between a and b

    Args:
        a: a :code:`[N, D]` tensor of coordinates
        b: a :code:`[M, D]` tensor of coordinates

    Returns:
        A :code:`[N, M]` matrix of squared distances between
        coordinates.
    """
    ra = tf.reshape(tf.reduce_sum(a * a, 1), [-1, 1])
    rb = tf.reshape(tf.reduce_sum(b * b, 1), [1, -1])

    Dsq = ra - 2 * tf.matmul(a, b, transpose_b=True) + rb
    return tf.math.sqrt(Dsq)


def include_all(x: np.typing.NDArray):
    x_ = tf.convert_to_tensor(x)
    return tf.fill(x_.shape, True)


@tf.function(jit_compile=False, autograph=False)
def compress_distance(a, b, include_fn):
    """Return a sparse tensor containing all distances
    between :code:`a` and :code:`b` less than :code:`max_dist`.
    """
    d_slice = pdist(a, b)
    is_valid = include_fn(d_slice)
    return tf.where(is_valid), d_slice[is_valid]


def sparse_pdist(
    coords: np.typing.NDArray,
    max_dist: float = np.inf,
    include_fn: Callable[[np.typing.NDArray], bool] = include_all,
    batch_size: int | None = None,
):
    """Compute a sparse distance matrix

    Compute a sparse Euclidean distance matrix between all pairs of
    :code:`coords` such that the distance is less than :code:`max_dist`.

    Args:
        coords: a :code:`[N, D]` array of coordinates
        max_dist: the maximum distance to return
        include_fn: a callable that takes a float representing the distance
                    between two points, and returns :code:`True` if the
                    distance should be included as a "non-zero" element
                    of the returned sparse matrix.
        batch_size: If memory is limited, compute the distances in batches
                    of :code:`[batch_size, N]` stripes.

    Returns:
        A sparse tensor of Euclidean distances less than :code:`max_dist`.

    Example:

        >>> import numpy as np
        >>> from gemlib.spatial import sparse_pdist
        >>> coords = np.random.uniform(size=(1000, 2))
        >>> d_sparse = sparse_pdist(coords, max_dist=0.01, batch_size=200)
        >>> d_sparse
        SparseTensor(indices=tf.Tensor(
        [[  0   0]
         [  1   1]
         [  2   2]
         ...
         [997 997]
         [998 998]
         [999 999]], shape=(1316, 2), dtype=int64), values=tf.Tensor(
        [0.00000000e+00 2.22044605e-16 0.00000000e+00 ... 0.00000000e+00
         0.00000000e+00 0.00000000e+00], shape=(1316,), dtype=float64),
        dense_shape=tf.Tensor([1000 1000], shape=(2,), dtype=int64))

    """
    if batch_size is None:
        batch_size = coords.shape[0]

    batched_coords = tf.data.Dataset.from_tensor_slices(coords).batch(
        batch_size
    )

    dist_nz = []
    pbar = tqdm(total=coords.shape[-2])

    def is_valid(x):
        return (
            tf.math.less(tf.zeros_like(x), x)
            & tf.math.less(x, max_dist)
            & include_fn(x)
        )

    for batch in batched_coords.prefetch(tf.data.experimental.AUTOTUNE):
        indices, values = compress_distance(batch, coords, is_valid)
        with tf.device("CPU"):  # Force results into host mem
            dist_nz.append(
                tf.SparseTensor(
                    indices.numpy(),
                    values.numpy(),
                    [batch.shape[0], coords.shape[0]],
                )
            )
        pbar.update(batch_size)

    with tf.device("CPU"):  # Force concatenation in host mem
        res = ts.concat(-2, dist_nz)

    return res
