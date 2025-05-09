"""Test mcmc_sampler"""

from typing import NamedTuple

import tensorflow as tf

from .mcmc_sampler import mcmc
from .test_util import CountingKernelInfo, counting_kernel


class DummyPosition(NamedTuple):
    x: float
    y: float


NUM_SAMPLES = 100


def test_mcmc():
    sampling_algorithm = counting_kernel()

    initial_position = DummyPosition(0.0, -100.0)

    def tlp(x, y):  # noqa: ARG001
        return tf.constant(0.0)

    samples, info = mcmc(
        num_samples=NUM_SAMPLES,
        sampling_algorithm=sampling_algorithm,
        target_density_fn=tlp,
        initial_position=initial_position,
        seed=[0, 0],
    )
    print(samples)
    tf.debugging.assert_equal(
        samples,
        DummyPosition(
            x=tf.range(1.0, 1.0 + NUM_SAMPLES, delta=1.0),
            y=tf.range(-99.0, -99.0 + NUM_SAMPLES, delta=1.0),
        ),
    )
    tf.debugging.assert_equal(
        info, CountingKernelInfo(tf.fill(NUM_SAMPLES, True))
    )
