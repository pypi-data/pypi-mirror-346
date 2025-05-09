"""MultiScanKernel calls one_step a number of times on an inner kernel"""

import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import samplers

mcmc = tfp.mcmc


class MultiScanKernel(mcmc.TransitionKernel):
    def __init__(self, num_updates, inner_kernel, name=None):
        """Performs multiple steps of an inner kernel
           returning the state and results after the last step.

        :param num_updates: integer giving the number of updates
        :param inner_kernel: an instance of a `tfp.mcmc.TransitionKernel`
        """
        self._parameters = {
            "num_updates": num_updates,
            "inner_kernel": inner_kernel,
            "name": name,
        }

    @property
    def is_calibrated(self):
        return True

    @property
    def num_updates(self):
        return self._parameters["num_updates"]

    @property
    def inner_kernel(self):
        return self._parameters["inner_kernel"]

    @property
    def name(self):
        return self._parameters["name"]

    def one_step(self, current_state, prev_results, seed=None):
        seed = samplers.sanitize_seed(seed, salt="MultiScanKernel")

        def body(i, state, results, seed):
            this_seed, next_seed = samplers.split_seed(seed)
            state, results = self.inner_kernel.one_step(
                state, results, this_seed
            )
            return i + 1, state, results, next_seed

        def cond(i, *_):
            return i < self.num_updates

        _, next_state, next_results, _ = tf.while_loop(
            cond, body, (0, current_state, prev_results, seed)
        )
        return next_state, next_results

    def bootstrap_results(self, current_state):
        return self.inner_kernel.bootstrap_results(current_state)
