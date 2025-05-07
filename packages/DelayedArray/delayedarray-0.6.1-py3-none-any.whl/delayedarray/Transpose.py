from typing import Callable, Optional, Tuple, Sequence, Any
from numpy import dtype, transpose
import numpy
import copy

from .DelayedOp import DelayedOp
from .SparseNdarray import SparseNdarray
from .extract_dense_array import extract_dense_array
from .extract_sparse_array import extract_sparse_array
from .create_dask_array import create_dask_array
from .chunk_grid import chunk_grid
from .is_sparse import is_sparse
from .is_masked import is_masked


__author__ = "ltla"
__copyright__ = "ltla"
__license__ = "MIT"


class Transpose(DelayedOp):
    """Delayed transposition, based on Bioconductor's ``DelayedArray::DelayedAperm`` class.

    This will create a matrix transpose in the 2-dimensional case; for a high-dimensional array, it will permute the
    dimensions.

    This class is intended for developers to construct new :py:class:`~delayedarray.DelayedArray.DelayedArray`
    instances. In general, end users should not be interacting with ``Transpose`` objects directly.
    """

    def __init__(self, seed, perm: Optional[Tuple[int, ...]]):
        """
        Args:
            seed:
                Any object that satisfies the seed contract,
                see :py:class:`~delayedarray.DelayedArray.DelayedArray` for details.

            perm:
                Tuple of length equal to the dimensionality of ``seed``,
                containing the permutation of dimensions.  If None, the
                dimension ordering is assumed to be reversed.
        """

        curshape = seed.shape
        ndim = len(curshape)
        if perm is not None:
            if len(perm) != ndim:
                raise ValueError(
                    "Dimensionality of 'seed' and 'perm' should be the same."
                )
        else:
            perm = (*range(ndim - 1, -1, -1),)

        final_shape = []
        for x in perm:
            final_shape.append(curshape[x])

        self._seed = seed
        self._perm = perm
        self._shape = (*final_shape,)

    @property
    def shape(self) -> Tuple[int, ...]:
        """
        Returns:
            Tuple of integers specifying the extent of each dimension of the
            transposed object.
        """
        return self._shape

    @property
    def dtype(self) -> dtype:
        """
        Returns:
            NumPy type for the transposed contents, same as ``seed``.
        """
        return self._seed.dtype

    @property
    def seed(self):
        """
        Returns:
            The seed object.
        """
        return self._seed

    @property
    def perm(self) -> Tuple[int, ...]:
        """
        Returns:
            Permutation of dimensions in the transposition.
        """
        return self._perm


def _simplify_transpose(x: Transpose) -> Any:
    seed = x.seed
    if not type(seed) is Transpose:
        # Don't use isinstance, we don't want to collapse for Transpose
        # subclasses that might be doing god knows what.
        return x

    new_perm = []
    noop = True
    for i, p in enumerate(x.perm):
        new_p = seed.perm[p]
        if new_p != i:
            noop = False
        new_perm.append(new_p)
    if noop:
        return seed.seed

    new_x = copy.copy(x)
    new_x._seed = seed.seed
    new_x._perm = (*new_perm,)
    return new_x


def _extract_array(x: Transpose, subset: Tuple[Sequence[int], ...], f: Callable):
    permsub = [None] * len(subset)
    for i, j in enumerate(x._perm):
        permsub[j] = subset[i]

    target = f(x._seed, (*permsub,))
    return transpose(target, axes=x._perm)


@extract_dense_array.register
def extract_dense_array_Transpose(x: Transpose, subset: Tuple[Sequence[int], ...]) -> numpy.ndarray:
    """See :py:meth:`~delayedarray.extract_dense_array.extract_dense_array`."""
    return _extract_array(x, subset, extract_dense_array)


@extract_sparse_array.register
def extract_sparse_array_Transpose(x: Transpose, subset: Tuple[Sequence[int], ...]) -> SparseNdarray:
    """See :py:meth:`~delayedarray.extract_sparse_array.extract_sparse_array`."""
    return _extract_array(x, subset, extract_sparse_array)


@create_dask_array.register
def create_dask_array_Transpose(x: Transpose):
    """See :py:meth:`~delayedarray.create_dask_array.create_dask_array`."""
    target = create_dask_array(x._seed)
    return transpose(target, axes=x._perm)


@chunk_grid.register
def chunk_grid_Transpose(x: Transpose):
    """See :py:meth:`~delayedarray.chunk_grid.chunk_grid`."""
    chunks = chunk_grid(x._seed)
    return chunks.transpose(x._perm)


@is_sparse.register
def is_sparse_Transpose(x: Transpose):
    """See :py:meth:`~delayedarray.is_sparse.is_sparse`."""
    return is_sparse(x._seed)


@is_masked.register
def is_masked_Transpose(x: Transpose):
    """See :py:meth:`~delayedarray.is_masked.is_masked`."""
    return is_masked(x._seed)
