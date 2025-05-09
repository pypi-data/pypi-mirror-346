"""MCMC utility functions"""

import tensorflow as tf
import tensorflow_probability as tfp


def is_list_like(x):
    return isinstance(x, list | tuple)


def get_flattening_bijector(example):
    """A bijector that converts a data structure to a 1-D tensor"""

    flat_example = tf.nest.flatten(example)

    split = tfp.bijectors.Split(
        [tf.reduce_prod(tf.shape(x)) for x in flat_example], axis=-1
    )
    reshape = tfp.bijectors.JointMap(
        [tfp.bijectors.Reshape(tf.shape(x)) for x in flat_example]
    )
    restructure = tfp.bijectors.Restructure(
        output_structure=tf.nest.pack_sequence_as(
            example, range(len(flat_example))
        )
    )

    return tfp.bijectors.Invert(
        tfp.bijectors.Chain([restructure, reshape, split])
    )
