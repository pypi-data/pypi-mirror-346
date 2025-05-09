"""Utility functions for model implementation code."""

import numpy as np
import tensorflow as tf


def batch_gather(arr, indices):
    """Gather `indices` from the right-most dimensions of `arr`.

    This function gathers elements on the right-most `indices` of `tensor`

    Args
    ----
        arr: an N-dimensional tensor
        indices: an iterable of N-dimensional coordinates into the rightmost
             `indices.shape[-1]` dimensions of `arr`

    Returns
    -------
    A tensor of dimension `rank(arr) - indices.shape[-1]` of gathered values in
    `arr`.
    """

    arr = tf.convert_to_tensor(arr)
    # TF shapes and indices are 32 bit
    indices = tf.cast(tf.convert_to_tensor(indices), tf.int32)

    index_dims = indices.shape[-1]

    # Flatten the dims which we are indexing - this is cheap, as no data needs
    # to be copied.  `flat_arr` is just a "view" of `arr`.
    flat_shape = arr.shape[:-index_dims].as_list() + [
        np.prod(arr.shape[-index_dims:])
    ]
    flat_arr = tf.reshape(arr, shape=flat_shape)

    # Compute the stride for each dim in the indices
    flat_coord_stride = tf.math.cumprod(
        tf.concat(
            [arr.shape[arr.shape.rank - (index_dims - 1) :], [1]], axis=0
        ),
        axis=0,
        reverse=True,
    )
    flat_indices = tf.linalg.matvec(indices, flat_coord_stride)

    return tf.gather(flat_arr, flat_indices, axis=-1)


def transition_coords(incidence_matrix, dtype=tf.int32):
    """Compute coordinates of transitions in a Markov transition matrix

    Args
    ----
        incidence_matrix: a (batch of) `[S, R]` matrix describing R
                          transitions between S states.

    Returns
    -------
    a [..., R, 2] tensor of coordinates of the transitions in a square
        transition matrix.
    """
    with tf.name_scope("transition_coords"):
        incidence_matrix = tf.convert_to_tensor(incidence_matrix)

        is_src_dest = tf.stack(
            [incidence_matrix < 0, incidence_matrix > 0], axis=-1
        )

        coords = tf.reduce_sum(
            tf.cumsum(
                tf.cast(is_src_dest, dtype),
                exclusive=True,
                reverse=True,
                axis=-3,
            ),
            axis=-3,
        )

        return coords


def states_from_transition_idx(transition_index, incidence_matrix):
    """Return source and destination state indices given a transition index.

    Given the index of a transition in `stoichiometry`, return
    the indices of the source and destination states.

    Note: this algorithm depends on the stoichiometry matrix
    describing a state transition model and taking the values `[-1, 0, 1]`.

    Args:
    ----
        event_index: the index (row id) of the event in `stoichiometry`
        incidence_matrix: a `[S, R]` matrix relating transitions to states

    Returns:
    -------
        a tuple of integers denoting indices of `(src, dest)`.

    """
    transition_index = tf.convert_to_tensor(transition_index, tf.int32)
    coords = transition_coords(incidence_matrix)[..., transition_index, :]

    return coords[..., 0], coords[..., 1]
