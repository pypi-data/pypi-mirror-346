import tensorflow as tf
import tensorflow_probability as tfp

from gemlib.distributions.uniform_integer import UniformInteger

tfd = tfp.distributions
Root = tfd.JointDistribution.Root


def _slice_min(state_tensor, start):
    """Compute `min(state_tensor[start:]` in an XLA-safe way

    Args
    ----
    state_tensor: a 1-D tensor
    start: an index into state_tensor

    Return
    ------
    `min(state_tensor[start:]`
    """
    state_tensor = tf.convert_to_tensor(state_tensor)

    masked_state_tensor = tf.where(
        tf.range(tf.shape(state_tensor)[-1]) < start,
        state_tensor.dtype.max,
        state_tensor,
    )

    return tf.reduce_min(masked_state_tensor)


def add_occult_proposal(
    count_max: int,
    events: tf.Tensor,
    src_state: tf.Tensor,
    name=None,
):
    count_max = tf.convert_to_tensor(count_max)
    events = tf.convert_to_tensor(events)
    src_state = tf.convert_to_tensor(src_state)

    num_times = events.shape[-2]
    num_units = events.shape[-1]

    def proposal():
        # Select unit
        with tf.name_scope("unit"):
            unit = yield Root(
                UniformInteger(
                    low=0,
                    high=num_units,
                    float_dtype=events.dtype,
                    name="unit",
                )
            )

        # Select timepoint
        with tf.name_scope("timepoint"):
            timepoint = yield Root(
                UniformInteger(
                    low=0,
                    high=num_times,
                    float_dtype=events.dtype,
                    name="timepoint",
                )
            )

        # event_count is bounded by the minimum value of the source state
        with tf.name_scope("event_count"):
            state_bound = _slice_min(src_state[..., unit], timepoint)
            bound = tf.math.minimum(
                tf.cast(state_bound, count_max.dtype), count_max
            )

            yield UniformInteger(
                low=tf.math.minimum(1, bound),
                high=bound + 1,
                float_dtype=events.dtype,
                name="event_count",
            )

    return tfd.JointDistributionCoroutineAutoBatched(proposal, name=name)


def del_occult_proposal(
    count_max: int,
    events: tf.Tensor,
    dest_state: tf.Tensor,
    name=None,
):
    count_max = tf.convert_to_tensor(count_max)
    events = tf.convert_to_tensor(events)
    dest_state = tf.convert_to_tensor(dest_state)

    def proposal():
        # Select unit to delete events from
        nonzero_units = tf.reduce_any(events > 0, axis=-2)
        unit = yield Root(
            tfd.Categorical(
                probs=tf.linalg.normalize(
                    tf.cast(nonzero_units, events.dtype), ord=1, axis=-1
                )[0],
                name="unit",
            )
        )
        # If there are no events to delete, unit will be events.shape[-1] + 1
        # Therefore clip to ensure we don't get an error in the next stage.
        unit = tf.clip_by_value(
            unit, clip_value_min=0, clip_value_max=tf.shape(events)[-1] - 1
        )

        # Select timepoint to delete events from
        with tf.name_scope("t"):
            unit_events = tf.gather(events, unit, axis=-1)  # T
            probs = tf.linalg.normalize(
                tf.cast(unit_events > 0, dtype=events.dtype), ord=1, axis=-1
            )[0]
            timepoint = yield tfd.Categorical(probs=probs, name="timepoint")

        # Clip if there are no events to delete
        timepoint = tf.clip_by_value(
            timepoint, clip_value_min=0, clip_value_max=tf.shape(events)[-2] - 1
        )
        # Draw num to delete - this is bounded by the minimum value of the
        # destination state over the range [timepoint, num_times)
        with tf.name_scope("event_count"):
            unit_dest_state = tf.gather(dest_state, indices=unit, axis=-1)
            state_bound = _slice_min(unit_dest_state, timepoint + 1)
            bound = tf.math.minimum(state_bound, events[..., timepoint, unit])
            bound = tf.math.minimum(tf.cast(bound, count_max.dtype), count_max)

            yield UniformInteger(
                low=tf.math.minimum(1, bound),
                high=bound + 1,
                float_dtype=events.dtype,
                name="event_count",
            )

    return tfd.JointDistributionCoroutineAutoBatched(proposal, name=name)
