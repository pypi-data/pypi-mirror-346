"""Unit tests for MwgStep"""

from collections.abc import Callable
from typing import NamedTuple

import pytest
import tensorflow as tf

from gemlib.mcmc.mwg_step import MwgStep, _project_position


class SamplingAlgorithmMock(NamedTuple):
    init: Callable
    step: Callable


class ChainStateMock(NamedTuple):
    position: NamedTuple
    log_density: float
    log_density_grad: float


def structure_assertion(expected_structure):
    def init_fn(_target_log_prob_fn, position):
        position = tf.nest.map_structure(
            lambda x, _: x, position, expected_structure, check_types=False
        )

        return (
            ChainStateMock(
                position=position, log_density=0.0, log_density_grad=()
            ),
            (),
        )

    def step_fn(_target_log_prob_fn, chain_and_kernel_state, _seed):
        cs, ks = chain_and_kernel_state

        tf.nest.map_structure(
            lambda x, _: x, cs.position, expected_structure, check_types=False
        )

        return chain_and_kernel_state, ()

    return SamplingAlgorithmMock(init_fn, step_fn)


class Position(NamedTuple):
    alpha: float
    beta: float
    gamma: float


@pytest.fixture
def position() -> Position:
    return Position(0.1, 0.1, 0.1)


def test_project_position(position):
    # Test target is a singleton tuple
    target, target_compl = _project_position(position, varnames=["alpha"])
    assert isinstance(target, tuple)
    assert isinstance(target_compl, tuple)
    assert len(target) == 1
    assert set(target_compl._fields) == {"beta", "gamma"}

    # Test target is a duple
    target, target_compl = _project_position(
        position, varnames=["alpha", "beta"]
    )
    assert isinstance(target, tuple)
    assert isinstance(target_compl, tuple)
    assert set(target._fields) == {"alpha", "beta"}
    assert len(target_compl) == 1

    # Test target is a float
    target, target_compl = _project_position(position, varnames="alpha")
    assert isinstance(target, float)
    assert set(target_compl._fields) == {"beta", "gamma"}


@pytest.mark.parametrize(
    "target_names,shape_example",
    [("alpha", 1.0), (["alpha"], [1.0]), (["alpha", "beta"], [1.0, 2.0])],
)
def test_mwg_state_shape(position, shape_example, target_names):
    def log_prob(_alpha, _beta, _gamma):
        return 1.0

    kernel = MwgStep(
        structure_assertion(shape_example), target_names=target_names
    )
    cks = kernel.init(log_prob, position)
    kernel.step(log_prob, cks, seed=None)
