"""Test `gemlib` utility functions."""

import numpy as np
import pytest

from gemlib.util import (
    batch_gather,
    states_from_transition_idx,
    transition_coords,
)


@pytest.fixture
def svir_incidence():
    """Fixture for SVIR incidence matrix."""

    return np.array(
        [  # SI   SV VI IR
            [-1, -1, 0, 0],  # S
            [0, 1, -1, 0],  # V
            [1, 0, 1, -1],  # I
            [0, 0, 0, 1],  # R
        ]
    )


@pytest.fixture
def sirs_incidence():
    """Fixture for SIRS incidence matrix."""

    return np.array(
        [  #  SI  IR  RS
            [-1, 0, 1],  # S
            [1, -1, 0],  # I
            [0, 1, -1],  # R
        ],
    )


def test_transition_coords_svir(svir_incidence):
    # Test svir
    coords = transition_coords(svir_incidence)
    expected = np.array([[0, 2], [0, 1], [1, 2], [2, 3]])
    np.testing.assert_equal(coords, expected)


def test_transition_coords_sirs(sirs_incidence):
    # Test SIRS
    coords = transition_coords(sirs_incidence)
    expected = np.array([[0, 1], [1, 2], [2, 0]])
    np.testing.assert_equal(coords, expected)


def test_states_from_transition_idx(svir_incidence):
    """Ensure source and destination enums are correct."""
    # S->I
    assert states_from_transition_idx(0, svir_incidence) == (0, 2)
    # S->V
    assert states_from_transition_idx(1, svir_incidence) == (0, 1)
    # V->I
    assert states_from_transition_idx(2, svir_incidence) == (1, 2)
    # I->R
    assert states_from_transition_idx(3, svir_incidence) == (2, 3)


def test_batch_gather():
    arr = np.random.uniform(low=0, high=1, size=[20, 100, 30, 20])

    indices = np.array([[2, 3], [4, 7], [15, 10]])

    slice_arr = batch_gather(arr, indices)

    np.testing.assert_array_equal(
        slice_arr, arr[..., indices[:, 0], indices[:, 1]]
    )
