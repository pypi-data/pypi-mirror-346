"""Class for writing posterior samples"""

import math
from datetime import datetime
from warnings import warn

import numpy as np
import zarr

import gemlib

__all__ = ["ZarrPosterior"]

CHUNK_BASE = 100 * 1024 * 1024  # Multiplier by which chunks are adjusted
CHUNK_MIN = 128 * 1024  # Soft lower limit (128k)
CHUNK_MAX = 300 * 1024 * 1024  # Hard upper limit


def _guess_chunks(shape: tuple[int, ...], typesize: int) -> tuple[int, ...]:
    """Guess an appropriate chunk layout for an array, given its shape and
    the size of each element in bytes.  Will allocate chunks only as large
    as MAX_SIZE.  Chunks are generally close to some power-of-2 fraction of
    each axis, slightly favoring bigger values for the last index.
    Undocumented and subject to change without warning.
    """
    ndims = len(shape)
    # require chunks to have non-zero length for all dimensions
    chunks = np.maximum(np.array(shape, dtype="=f8"), 1)

    # Determine the optimal chunk size in bytes using a PyTables expression.
    # This is kept as a float.
    dset_size = np.product(chunks) * typesize
    target_size = CHUNK_BASE * (2 ** np.log10(dset_size / (1024.0 * 1024)))

    if target_size > CHUNK_MAX:
        target_size = CHUNK_MAX
    elif target_size < CHUNK_MIN:
        target_size = CHUNK_MIN

    idx = 0
    while True:
        # Repeatedly loop over the axes, dividing them by 2.  Stop when:
        # 1a. We're smaller than the target chunk size, OR
        # 1b. We're within 50% of the target chunk size, AND
        # 2. The chunk is smaller than the maximum chunk size
        chunk_bytes = np.product(chunks) * typesize
        if (
            chunk_bytes < target_size
            or abs(chunk_bytes - target_size) / target_size < 0.5  # noqa: PLR2004
        ) and chunk_bytes < CHUNK_MAX:
            break

        if np.product(chunks) == 1:
            break  # Element size larger than CHUNK_MAX

        chunks[idx % ndims] = math.ceil(chunks[idx % ndims] / 2.0)
        idx += 1

    return tuple(int(x) for x in chunks)


def _maybe_tf_dtype(dtype):
    if hasattr(dtype, "as_numpy_dtype"):
        return dtype.as_numpy_dtype
    return dtype


def _maybe_to_numpy(val):
    if hasattr(val, "numpy"):
        return val.numpy()
    return val


class ZarrPosterior:
    def __init__(self, filename, sample_dict, results_dict, num_samples):
        """Constructs a posterior output object

        :param filename: the name of the backend HDF5 file
        :param sample_dict: a dictionary containing `key`:`shape_tuple`
        :param results_dict: a dictionary containing `key`:`shape_tuple`
        :param num_samples: total number of samples
        """
        warn(
            "ZarrPosterior is obsolete and will be removed in 2025.  \
Please migrate to the SamplingAlgorithm framework instead.",
            FutureWarning,
            stacklevel=2,
        )
        self._num_samples = num_samples
        self._archive = zarr.open(
            filename,
            "w",
        )

        self._sample_group = self._archive.create_group("samples")
        self._create_data_tree(sample_dict, self._sample_group)

        self._results_group = self._archive.create_group("results")
        self._create_data_tree(results_dict, self._results_group)

        self._archive.attrs["created_at"] = str(datetime.now())
        self._archive.attrs["inference_library"] = "gemlib"
        self._archive.attrs["inference_library_version"] = gemlib.__version__

    def __getitem__(self, path):
        return self._archive[path]

    def _create_data_tree(self, data_dict, group):
        for k, v in data_dict.items():
            if isinstance(v, dict):
                subgroup = group.create_group(k)
                self._create_data_tree(v, subgroup)

            else:
                dtype = _maybe_tf_dtype(v.dtype)
                chunks = _guess_chunks(
                    shape=(self._num_samples,) + v.shape,
                    typesize=np.dtype(dtype).itemsize,
                )
                dset_shape = (0,) + v.shape

                group.create_dataset(
                    k,
                    shape=dset_shape,
                    chunks=chunks,
                    dtype=dtype,
                )

    def _append(self, sample_dict, dset):
        for k, v in sample_dict.items():
            if isinstance(v, dict):
                self._append(v, dset[k])
            else:
                dset[k].append(_maybe_to_numpy(v))

    def append(self, samples_dict, results_dict):
        self._append(samples_dict, self._sample_group)
        self._append(results_dict, self._results_group)
