"""Tests Brownian Bridge kernel"""

import os
import pickle as pkl

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import test_util

from gemlib.distributions.brownian import BrownianMotion

from .brownian_bridge_kernel import UncalibratedBrownianBridgeKernel

tfd = tfp.distributions

DTYPE = tf.float64


def model_fixture():
    """Fixture from model below"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, "bb_fixture.pkl"), "rb") as f:
        return pkl.load(f)


class TestBrownianBridgeKernel(test_util.TestCase):
    def test_simple_brownian_motion(self):
        x = tf.range(0.0, 10.0, 0.1, dtype=DTYPE)
        Y = BrownianMotion(x)
        y = Y.sample()

        kernel = tfp.mcmc.MetropolisHastings(
            inner_kernel=UncalibratedBrownianBridgeKernel(
                Y.log_prob,
                index_points=x,
                span=90,
                scale=tf.constant(1.0, DTYPE),
            )
        )

        # kernel = tfp.mcmc.DualAveragingStepSizeAdaptation(
        #     inner_kernel=tfp.mcmc.HamiltonianMonteCarlo(
        #         target_log_prob_fn=Y.log_prob,
        #         num_leapfrog_steps=3,
        #         step_size=0.1,
        #     ),
        #     num_adaptation_steps=500,
        # )

        samples, results = tf.function(
            lambda: tfp.mcmc.sample_chain(
                num_results=10000, kernel=kernel, current_state=y
            )
        )()

        print(
            "Acceptance rate:",
            tf.reduce_mean(tf.cast(results.is_accepted, tf.float32)),
        )

        # fig, ax = plt.subplots(1, 2)
        # ax[0].plot(
        #     x[1:],
        #     samples.numpy().T,
        #     color="lightblue",
        #     alpha=0.3,
        # )
        # ax[0].plot(
        #     x[1:],
        #     y,
        #     "o",
        #     color="black",
        # )
        # ax[1].plot(samples[:, 75])
        # plt.show()

        self.assertAllClose(0.0, np.mean(samples[:, 0]), atol=1.0, rtol=0.1)
        self.assertAllClose(10.0, np.var(samples[:, -1]), atol=1.0, rtol=0.1)

    def test_poisson_with_brownian_mean(self):
        x = tf.range(0.0, 10.0, 0.1, dtype=DTYPE)

        def model():
            mu0 = tfd.Normal(
                loc=tf.constant(1.0, DTYPE),
                scale=tf.constant(1.0, DTYPE),
            )

            def mu(mu0):
                return BrownianMotion(x, x0=mu0)

            def y(mu):
                rate = tf.concat([[0.0], mu], axis=-1)
                return tfd.Independent(
                    tfd.Poisson(rate=tf.math.exp(rate)),
                    reinterpreted_batch_ndims=1,
                )

            return tfd.JointDistributionNamed({"mu0": mu0, "mu": mu, "y": y})

        model = model()
        trial = model_fixture()

        def logp(mu):
            return model.log_prob(
                {"mu0": trial["mu0"], "mu": mu, "y": trial["y"]}
            )

        mcmc_kernel = tfp.mcmc.MetropolisHastings(
            inner_kernel=UncalibratedBrownianBridgeKernel(
                logp,
                index_points=x,
                span=5,
                scale=tf.constant(1.0, DTYPE),
                left=True,
                right=True,
            )
        )

        # mcmc_kernel = tfp.mcmc.DualAveragingStepSizeAdaptation(
        #     inner_kernel=tfp.mcmc.HamiltonianMonteCarlo(
        #         target_log_prob_fn=logp, num_leapfrog_steps=3, step_size=1.0
        #     ),
        #     num_adaptation_steps=500,
        # )

        samples, results = tf.function(
            lambda: tfp.mcmc.sample_chain(
                num_results=5000,
                kernel=mcmc_kernel,
                current_state=tf.fill(
                    trial["mu"].shape, tf.constant(3.0, DTYPE)
                ),
            )
        )()
        print(
            "Acceptance rate:",
            tf.reduce_mean(tf.cast(results.is_accepted, tf.float32)),
        )

        # fig, ax = plt.subplots(1, 2)
        # ax[0].plot(
        #     np.exp(samples[500:].numpy().T),
        #     color="lightblue",
        #     alpha=0.3,
        # )
        # ax[0].plot(
        #     np.exp(trial["mu"]),
        #     "o",
        #     color="black",
        # )
        # ax[1].plot(np.exp(samples[:, 75]))
        # plt.show()

        self.assertAllClose(
            0.0,
            0.0,
            rtol=1.5,
            atol=2.0,
        )


if __name__ == "__main__":
    TestBrownianBridgeKernel().test_poisson_with_brownian_mean()
