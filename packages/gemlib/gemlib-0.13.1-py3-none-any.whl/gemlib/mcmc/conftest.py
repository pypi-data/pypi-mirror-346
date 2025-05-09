"""Pytest config"""

import numpy as np
import pytest
import tensorflow as tf


@pytest.fixture(scope="module")
def seir_metapop_example():
    """Outcome of a simulation from a 3-metapopulation SEIR model
    with mixing, implemented in https://colab.research.google.com/drive/1Q1PUcOnYlvCGHzRUBUAp4CxYhZ8RJzg8?usp=sharing
    """

    connectivity = np.array(
        [[0.0, 0.5, 0.25], [0.5, 0.0, 0.1], [0.25, 0.1, 0.0]], dtype=np.float32
    )

    incidence_matrix = np.array(
        [
            [-1, 0, 0],
            [1, -1, 0],
            [0, 1, -1],
            [0, 0, 1],
        ],
        dtype=np.float32,
    )

    initial_conditions = np.array(
        [  # S    E  I  R
            [99, 0, 1, 0],  # n=0
            [100, 0, 0, 0],  # n=1
            [100, 0, 0, 0],  # n=2
        ],
        np.float32,
    )

    params = {
        "beta": np.float32(0.02),
        "psi": np.float32(0.6),
        "nu": np.float32(0.5),
        "gamma": np.float32(0.2),
    }

    def trf(_, state):
        within = state[:, 2]  # states are enumerated S, E, I, R from 0
        between = params["psi"] * tf.linalg.matvec(
            connectivity, state[:, 2] / tf.reduce_sum(state, axis=-1)
        )
        si_rate = params["beta"] * (within + between)
        ei_rate = tf.broadcast_to(params["nu"], si_rate.shape)
        ir_rate = tf.broadcast_to(params["gamma"], si_rate.shape)

        return si_rate, ei_rate, ir_rate

    events = np.array(
        [
            [[3.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            [[1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            [[3.0, 2.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            [[5.0, 4.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            [[16.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            [[6.0, 11.0, 1.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            [[24.0, 5.0, 2.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]],
            [[18.0, 16.0, 4.0], [3.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            [[7.0, 16.0, 14.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]],
            [[9.0, 11.0, 6.0], [1.0, 1.0, 0.0], [0.0, 0.0, 0.0]],
            [[2.0, 9.0, 4.0], [5.0, 0.0, 2.0], [0.0, 0.0, 0.0]],
            [[3.0, 10.0, 2.0], [2.0, 3.0, 0.0], [0.0, 0.0, 0.0]],
            [[1.0, 5.0, 10.0], [9.0, 0.0, 1.0], [0.0, 0.0, 0.0]],
            [[1.0, 4.0, 7.0], [9.0, 4.0, 0.0], [0.0, 0.0, 0.0]],
            [[0.0, 3.0, 4.0], [8.0, 7.0, 1.0], [0.0, 0.0, 0.0]],
        ],
        dtype=np.float32,
    )
    return {
        "params": params,
        "connectivity": connectivity,
        "transition_rate_fn": trf,
        "initial_conditions": initial_conditions,
        "events": events,
        "incidence_matrix": incidence_matrix,
    }
