"""Test fixtures"""

import numpy as np
import pytest


@pytest.fixture(params=[np.float32, np.float64])
def sir_metapop_example(request):
    """Outcome of a simulation from a 3-metapopulation model
    with mixing, implemented in https://colab.research.google.com/drive/1Q1PUcOnYlvCGHzRUBUAp4CxYhZ8RJzg8?usp=sharing
    """
    dtype = request.param

    incidence_matrix = np.array([[-1, 0], [1, -1], [0, 1]], dtype=dtype)

    initial_conditions = np.array(
        [[999, 50, 0], [500, 20, 0], [250, 10, 0]], dtype=dtype
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
        dtype=dtype,
    )

    return {
        "initial_conditions": initial_conditions,
        "events": events,
        "incidence_matrix": incidence_matrix,
    }
