from functools import singledispatch
from typing import Any, Sequence, Union


@singledispatch
def subset_sequence(x: Any, indices: Sequence[int]) -> Any:
    """
    Subset ``x`` by ``indices`` to obtain a new object. The default method
    attempts to use ``x``'s ``__getitem__`` method.

    Args:
        x:
            Any object that supports ``__getitem__`` with an integer sequence.

        indices:
            Sequence of non-negative integers specifying the integers of interest.
            All indices should be less than ``len(x)``.

    Returns:
        The result of slicing ``x`` by ``indices``. The exact type
        depends on what ``x``'s ``__getitem__`` method returns.
    """
    return x[indices]


@subset_sequence.register
def _subset_sequence_list(x: list, indices: Sequence) -> list:
    return type(x)(x[i] for i in indices)


@subset_sequence.register
def _subset_sequence_range(x: range, indices: Sequence) -> Union[list, range]:
    if isinstance(indices, range):
        # We can just assume that all 'indices' are in [0, len(x)),
        # so no need to handle out-of-range indices.
        return range(
            x.start + x.step * indices.start,
            x.start + x.step * indices.stop,
            x.step * indices.step
        )
    else:
        return [x[i] for i in indices]
