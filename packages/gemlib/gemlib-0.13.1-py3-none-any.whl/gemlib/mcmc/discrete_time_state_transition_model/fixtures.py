"""Test fixtures"""

import numpy as np
import pytest


@pytest.fixture(scope="module")
def sir_metapop_example():
    """Outcome of a simulation from a 3-metapopulation model
    with mixing, implemented in https://colab.research.google.com/drive/1Q1PUcOnYlvCGHzRUBUAp4CxYhZ8RJzg8?usp=sharing
    """

    incidence_matrix = np.array([[-1, 0], [1, -1], [0, 1]], dtype=np.float32)

    initial_conditions = np.array(
        [[999, 50, 0], [500, 20, 0], [250, 10, 0]], dtype=np.float32
    )

    events = np.array(
        [
            [[11.0, 11.0], [5.0, 4.0], [2.0, 2.0]],
            [[11.0, 6.0], [5.0, 2.0], [4.0, 2.0]],
            [[2.0, 6.0], [11.0, 1.0], [1.0, 0.0]],
            [[10.0, 6.0], [8.0, 4.0], [2.0, 2.0]],
            [[12.0, 7.0], [7.0, 4.0], [6.0, 1.0]],
            [[11.0, 5.0], [5.0, 5.0], [4.0, 1.0]],
            [[13.0, 10.0], [12.0, 6.0], [6.0, 1.0]],
        ],
        dtype=np.float32,
    )

    return {
        "initial_conditions": initial_conditions,
        "events": events,
        "incidence_matrix": incidence_matrix,
    }
