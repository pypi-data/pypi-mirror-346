import warnings
from typing import Callable, Tuple, Sequence
import numpy

from .DelayedOp import DelayedOp
from ._isometric import ISOMETRIC_OP_WITH_ARGS, _execute
from .extract_dense_array import extract_dense_array
from .extract_sparse_array import extract_sparse_array
from .create_dask_array import create_dask_array
from .chunk_grid import chunk_grid
from .is_sparse import is_sparse
from .is_masked import is_masked

__author__ = "ltla"
__copyright__ = "ltla"
__license__ = "MIT"


class BinaryIsometricOp(DelayedOp):
    """Binary isometric operation involving two n-dimensional seed arrays with the same dimension extents.
    This is based on Bioconductor's ``DelayedArray::DelayedNaryIsoOp`` class.

    The data type of the result is determined by NumPy casting given the ``seed`` and ``value``
    data types. It is probably safest to cast at least one array to floating-point
    to avoid problems due to integer overflow.

    This class is intended for developers to construct new :py:class:`~delayedarray.DelayedArray.DelayedArray`
    instances. In general, end users should not be interacting with ``BinaryIsometricOp`` objects directly.
    """

    def __init__(self, left, right, operation: ISOMETRIC_OP_WITH_ARGS):
        """ 
        Args:
            left:
                Any object satisfying the seed contract,
                see :py:meth:`~delayedarray.DelayedArray.DelayedArray` for details.

            right:
                Any object of the same dimensions as ``left`` that satisfies the seed contract,
                see :py:meth:`~delayedarray.DelayedArray.DelayedArray` for details.

            operation:
                String specifying the operation.
        """

        if left.shape != right.shape:
            raise ValueError("'left' and 'right' shapes should be the same")

        ldummy = numpy.zeros(1, dtype=left.dtype)
        rdummy = numpy.zeros(1, dtype=right.dtype)
        with warnings.catch_warnings():  # silence warnings from divide by zero.
            warnings.simplefilter("ignore")
            dummy = _execute(ldummy, rdummy, operation)
        dtype = dummy.dtype

        self._left = left
        self._right = right
        self._op = operation
        self._dtype = dtype
        self._sparse = is_sparse(self._left) and is_sparse(self._right) and dummy[0] == 0

    @property
    def shape(self) -> Tuple[int, ...]:
        """
        Returns:
            Tuple of integers specifying the extent of each dimension of this
            object.  As the name of the class suggests, this is the same as the
            shapes of the ``left`` and ``right`` objects.
        """
        return self._left.shape

    @property
    def dtype(self) -> numpy.dtype:
        """
        Returns:
            NumPy type for the data after the operation. This may or may not be
            the same as the ``left`` or ``right`` objects, depending on how
            NumPy does the casting for the requested operation.
        """
        return self._dtype

    @property
    def left(self):
        """
        Returns:
            The seed object on the left-hand-side of the operation.
        """
        return self._left

    @property
    def right(self):
        """
        Returns:
            The seed object on the right-hand-side of the operation.
        """
        return self._right

    @property
    def operation(self) -> ISOMETRIC_OP_WITH_ARGS:
        """
        Returns:
            Name of the operation.
        """
        return self._op

 
def _extract_array(x: BinaryIsometricOp, subset: Tuple[Sequence[int], ...], f: Callable):
    ls = f(x._left, subset)
    rs = f(x._right, subset)
    return _execute(ls, rs, x._op)


@extract_dense_array.register
def extract_dense_array_BinaryIsometricOp(x: BinaryIsometricOp, subset: Tuple[Sequence[int], ...]):
    """See :py:meth:`~delayedarray.extract_dense_array.extract_dense_array`."""
    return _extract_array(x, subset, extract_dense_array)


@extract_sparse_array.register
def extract_sparse_array_BinaryIsometricOp(x: BinaryIsometricOp, subset: Tuple[Sequence[int], ...]):
    """See :py:meth:`~delayedarray.extract_sparse_array.extract_sparse_array`."""
    return _extract_array(x, subset, extract_sparse_array)


@create_dask_array.register
def create_dask_array_BinaryIsometricOp(x: BinaryIsometricOp): 
    """See :py:meth:`~delayedarray.create_dask_array.create_dask_array`."""
    ls = create_dask_array(x._left)
    rs = create_dask_array(x._right)
    return _execute(ls, rs, x._op)


@chunk_grid.register
def chunk_grid_BinaryIsometricOp(x: BinaryIsometricOp):
    """See :py:meth:`~delayedarray.chunk_grid.chunk_grid`."""
    lchunk = chunk_grid(x._left)
    rchunk = chunk_grid(x._right)

    # Favor the chunking for the more expensive grid, to avoid being penalized
    # heavily from suboptimal chunking for that array. 
    #
    # Technically, we could optimize for the case where multiple dimensions
    # have the same boundaries, in which case we should favor full extraction
    # of the other dimensions and just iterate over the common dimensions.
    # This avoids any chunk discrepancies but seems like a pretty unlikely case
    # - if two arrays of the same shape disagree on the chunk boundaries of one
    # dimension, they'd probably disagree on the others as well.
    # 
    # The other solution is to figure out some high-dimensional caching scheme
    # for the partially consumed chunks. Sounds like a royal pain.
    if lchunk.cost > rchunk.cost:
        return lchunk
    else:
        return rchunk


@is_sparse.register
def is_sparse_BinaryIsometricOp(x: BinaryIsometricOp):
    """See :py:meth:`~delayedarray.is_sparse.is_sparse`."""
    return x._sparse


@is_masked.register
def is_masked_BinaryIsometricOp(x: BinaryIsometricOp):
    """See :py:meth:`~delayedarray.is_masked.is_masked`."""
    return is_masked(x._left) or is_masked(x._right)
