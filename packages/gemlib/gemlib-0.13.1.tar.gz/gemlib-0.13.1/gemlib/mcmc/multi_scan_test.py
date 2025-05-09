"""Test modules for multiscan kernel"""

from typing import NamedTuple

import numpy as np
import tensorflow as tf

from .mcmc_sampler import mcmc
from .multi_scan import multi_scan
from .test_util import CountingKernelInfo, counting_kernel


class DummyPosition(NamedTuple):
    x: float


def test_one_multi_scan():
    multi_scan_iterations = 100

    sampler = multi_scan(multi_scan_iterations, counting_kernel())

    def tlp(x):
        return x

    initial_position = DummyPosition(0.0)

    state = sampler.init(tlp, initial_position)
    (chain_state, kernel_state), info = sampler.step(
        target_log_prob_fn=tlp, current_state=state, seed=[0, 0]
    )

    tf.debugging.assert_equal(
        chain_state.position, np.float32(multi_scan_iterations)
    )
    tf.debugging.assert_equal(
        chain_state.log_density, np.float32(multi_scan_iterations)
    )
    tf.debugging.assert_equal(kernel_state, multi_scan_iterations)
    tf.debugging.assert_equal(info, CountingKernelInfo(True))


def test_many_multi_scan():
    num_samples = 5
    multi_scan_iterations = 100

    sampler = multi_scan(multi_scan_iterations, counting_kernel())

    def tlp(x):
        return x

    initial_position = DummyPosition(0.0)

    samples, info = mcmc(
        num_samples=num_samples,
        sampling_algorithm=sampler,
        target_density_fn=tlp,
        initial_position=initial_position,
        seed=[0, 0],
    )

    tf.debugging.assert_equal(
        samples,
        tf.range(
            100.0,
            100.0 + (num_samples * multi_scan_iterations),
            delta=multi_scan_iterations,
        ),
    )
    tf.debugging.assert_equal(
        info, CountingKernelInfo(tf.fill(num_samples, True))
    )
