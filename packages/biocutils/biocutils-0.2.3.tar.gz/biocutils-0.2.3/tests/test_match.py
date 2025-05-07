from biocutils import match, map_to_index
import numpy
import pytest


def test_match_simple():
    x = ["A", "C", "B", "D", "A", "A", "C", "D", "B"]
    levels = ["D", "C", "B", "A"]

    mm = match(x, levels)
    assert list(mm) == [3, 1, 2, 0, 3, 3, 1, 0, 2]
    assert mm.dtype == numpy.dtype("int8")

    mm2 = match(x, map_to_index(levels))
    assert (mm == mm2).all()


def test_match_duplicates():
    x = [5, 1, 2, 3, 5, 6, 7, 7, 2, 1]
    mm = match(x, [1, 2, 3, 3, 5, 6, 1, 7, 6])
    assert list(mm) == [4, 0, 1, 2, 4, 5, 7, 7, 1, 0]

    mm = match(x, [1, 2, 3, 3, 5, 6, 1, 7, 6], duplicate_method="last")
    assert list(mm) == [4, 6, 1, 3, 4, 8, 7, 7, 1, 6]


def test_match_none():
    mm = match(["A", None, "B", "D", None, "A", "C", None, "B"], ["D", "C", "B", "A"])
    assert list(mm) == [3, -1, 2, 0, -1, 3, 1, -1, 2]

    mm = match(["A", "B", "D", "A", "C", "B"], ["D", None, "C", "B", None, "A"])
    assert list(mm) == [5, 3, 0, 5, 2, 3]


def test_match_dtype():
    mm = match(["A", "F", "B", "D", "F", "A", "C", "F", "B"], ["D", "C", "B", "A"], dtype=numpy.dtype("int32"))
    assert list(mm) == [3, -1, 2, 0, -1, 3, 1, -1, 2]
    assert mm.dtype == numpy.dtype("int32")

    mm = match(["A", "B", "D", "A", "C", "B"], ["D", "C", "B", "A"], dtype=numpy.dtype("uint32"))
    assert list(mm) == [3, 2, 0, 3, 1, 2]
    assert mm.dtype == numpy.dtype("uint32")


def test_match_fail_missing():
    x = match(["A", "E", "B", "D", "E"], ["D", "C", "B", "A"])
    assert list(x) == [3, -1, 2, 0, -1]

    with pytest.raises(ValueError, match="cannot find"):
        match(["A", "E", "B", "D", "E"], ["D", "C", "B", "A"], fail_missing=True)

    with pytest.raises(ValueError, match="cannot find"):
        match(["A", "E", "B", "D", "E"], ["D", "C", "B", "A"], dtype=numpy.uint32)

    x = match(["A", "C", "B", "D", "C"], ["D", "C", "B", "A"], fail_missing=True)
    assert list(x) == [3, 1, 2, 0, 1]
