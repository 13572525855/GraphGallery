import numpy as np
import tensorflow as tf
import scipy.sparse as sp

from numbers import Number
from graphgallery import config
from tensorflow.keras import backend as K

from graphgallery.utils.is_something import is_sequence, is_interger_scalar, is_tensor_or_variable


def to_int(index):
    """Convert `index` to interger type.

    """
    if is_tensor_or_variable(index):
        return tf.cast(index, config.intx())

    if is_interger_scalar(index):
        index = np.asarray([index])
    elif is_sequence(index):
        index = np.asarray(index)
    elif isinstance(index, np.ndarray):
        pass
    else:
        raise TypeError('`index` should be either `list`, integer scalar or `np.array`!')
    return index.astype(config.intx())


def scipy_sparse_to_sparse_tensor(x):
    """Converts a SciPy sparse matrix to a SparseTensor."""
    sparse_coo = x.tocoo()
    row, col = sparse_coo.row, sparse_coo.col
    data, shape = sparse_coo.data, sparse_coo.shape
    if issubclass(data.dtype.type, np.floating):
        data = data.astype(config.floatx())
    indices = np.concatenate(
        (np.expand_dims(row, axis=1), np.expand_dims(col, axis=1)), axis=1)
    return tf.sparse.SparseTensor(indices, data, shape)


def sparse_tensor_to_scipy_sparse(x):
    """Converts a SparseTensor to a SciPy sparse matrix."""
    # TODO
    return x


def inferer_type(x):
    x = np.asarray(x)
    if x.dtype.kind == 'f':
        return config.floatx()
    elif x.dtype.kind == 'i':
        return config.intx()
    elif x.dtype.kind == 'b':
        return 'bool'
    else:
        raise RuntimeError(f'Invalid types, type `{type(x)}`')


def to_tensor(inputs):
    """Convert input matrices to Tensors (SparseTensors)."""
    def matrix_to_tensor(matrix):
        if any((is_tensor_or_variable(matrix), K.is_sparse(matrix), matrix is None)):
            return matrix
        elif sp.isspmatrix_csr(matrix) or sp.isspmatrix_csc(matrix):
            return scipy_sparse_to_sparse_tensor(matrix)
        elif isinstance(matrix, np.ndarray) or is_sequence(matrix):
            return tf.convert_to_tensor(matrix, dtype=inferer_type(matrix))
        else:
            raise TypeError(f'Invalid type `{type(matrix)}` of inputs data. Allowed data type (Tensor, SparseTensor, np.ndarray, scipy.sparse.sparsetensor, None).')

    # Check `not isinstance(inputs[0], Number)` to avoid like [matrix, [1,2,3]], where [1,2,3] will be converted seperately.
    if is_sequence(inputs) and not isinstance(inputs[0], Number):
        return [to_tensor(matrix) for matrix in inputs]
    else:
        return matrix_to_tensor(inputs)
