from functools import singledispatch
from itertools import chain
from typing import Any

import numpy

from .is_list_of_type import is_list_of_type
from .package_utils import is_package_installed

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


@singledispatch
def combine_sequences(*x: Any):
    """Combine vector-like objects (1-dimensional arrays).

    If all elements are :py:class:`~numpy.ndarray`,
    we combine them using numpy's :py:func:`~numpy.concatenate`.

    If all elements are :py:class:`~pandas.Series` objects, they are combined
    using :py:func:`~pandas.concat`.

    For all other scenarios, all elements are coerced to a :py:class:`~list`
    and combined.

    Args:
        x:
            Vector-like objects to combine.
            All elements of ``x`` are expected to be the same class or
            atleast compatible with each other.

    Returns:
        A combined object, ideally of the same type as the first element in ``x``.
    """
    raise NotImplementedError(
        "no `combine_sequences` method implemented for '"
        + type(x[0]).__name__
        + "' objects"
    )


@combine_sequences.register(list)
def _combine_sequences_lists(*x: list):
    return type(x[0])(chain(*x))


@combine_sequences.register(numpy.ndarray)
def _combine_sequences_dense_arrays(*x: numpy.ndarray):
    for y in x:
        if numpy.ma.is_masked(y):
            return numpy.ma.concatenate(x, axis=None)
    return numpy.concatenate(x, axis=None)


@combine_sequences.register
def _combine_sequences_ranges(*x: range):
    for current in x:
        if not isinstance(current, range):
            return list(chain(*x))

    found = None
    for i, current in enumerate(x):
        if len(current) != 0:
            found = i
            start = current.start
            step = current.step
            stop = current.stop
            last = current[-1]
            break

    if found is None:
        return x[0]

    failed = False
    for i in range(found + 1, len(x)):
        current = x[i]
        if len(current) != 0:
            if current[0] != last + step or (len(current) > 1 and step != current.step):
                failed = True
                break
            last = current[-1]
            stop = current.stop

    if not failed:
        return range(start, stop, step)
    return list(chain(*x))


if is_package_installed("pandas") is True:
    from pandas import Series, concat

    @combine_sequences.register(Series)
    def _combine_sequences_pandas_series(*x):
        if not is_list_of_type(x, Series):
            elems = []
            for elem in x:
                if not isinstance(elem, Series):
                    elems.append(Series(elem))
                else:
                    elems.append(elem)
            x = elems
        return concat(x)
