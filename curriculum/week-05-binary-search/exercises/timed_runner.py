"""
Week 5 - pytest grader for the five UMPIRE binary-search drills.

Place your solutions in this folder (or any folder on PYTHONPATH) with these
exact function names:

    drill_01_solution.binary_search(arr, target)

    drill_02_solution.find_first_and_last(arr, target)

    drill_03_solution.search_rotated(arr, target)

    drill_04_solution.count_le(matrix, v)
    drill_04_solution.kth_smallest(matrix, k)

    drill_05_solution.min_eating_speed(piles, h)

Then run:

    pytest exercises/timed_runner.py -v

Acceptance criterion for the week: all tests pass on a fresh checkout.

If you implemented with different names, edit the import / call sites below.
The point is the test logic, not the import shape.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

# Make this folder importable so drill_NN_solution.py modules are found.
sys.path.insert(0, str(Path(__file__).parent))


def _load(module_name: str):
    """Import a drill module lazily so missing solutions skip rather than fail collection."""
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        pytest.skip(f"{module_name} not found - write your solution first.")


# -----------------------------------------------------------------------------
# Drill 1 - Classic binary search
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "arr, target, expected",
    [
        ([-1, 0, 3, 5, 9, 12], 9, 4),
        ([-1, 0, 3, 5, 9, 12], 2, -1),
        ([1], 1, 0),
        ([1], 0, -1),
        ([], 5, -1),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 1, 0),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10, 9),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 11, -1),
        ([5], 5, 0),
        ([-10, -5, 0, 5, 10], 0, 2),
    ],
)
def test_drill_01_binary_search(arr, target, expected):
    mod = _load("drill_01_solution")
    assert mod.binary_search(arr, target) == expected


# -----------------------------------------------------------------------------
# Drill 2 - Find first and last
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "arr, target, expected",
    [
        ([5, 7, 7, 8, 8, 10], 8, [3, 4]),
        ([5, 7, 7, 8, 8, 10], 6, [-1, -1]),
        ([], 0, [-1, -1]),
        ([1], 1, [0, 0]),
        ([1], 2, [-1, -1]),
        ([2, 2, 2, 2], 2, [0, 3]),
        ([1, 2, 3, 4, 5], 3, [2, 2]),
        ([1, 1, 1, 1, 1, 2], 1, [0, 4]),
        ([1, 2, 2, 2, 2, 3], 2, [1, 4]),
        ([1, 2, 3, 4, 5], 6, [-1, -1]),
        ([1, 2, 3, 4, 5], 0, [-1, -1]),
    ],
)
def test_drill_02_find_first_and_last(arr, target, expected):
    mod = _load("drill_02_solution")
    assert mod.find_first_and_last(arr, target) == expected


# -----------------------------------------------------------------------------
# Drill 3 - Search in rotated sorted array
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "arr, target, expected",
    [
        ([4, 5, 6, 7, 0, 1, 2], 0, 4),
        ([4, 5, 6, 7, 0, 1, 2], 3, -1),
        ([1], 0, -1),
        ([1], 1, 0),
        ([1, 3], 3, 1),
        ([3, 1], 1, 1),
        ([5, 1, 3], 3, 2),
        ([4, 5, 6, 7, 8, 1, 2, 3], 8, 4),
        ([6, 7, 0, 1, 2, 4, 5], 0, 2),
        ([1, 2, 3, 4, 5, 6, 7], 4, 3),   # no rotation
        ([1, 2, 3, 4, 5, 6, 7], 8, -1),   # no rotation, absent
    ],
)
def test_drill_03_search_rotated(arr, target, expected):
    mod = _load("drill_03_solution")
    assert mod.search_rotated(arr, target) == expected


# -----------------------------------------------------------------------------
# Drill 4 - Kth smallest in a sorted matrix
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "matrix, v, expected_count",
    [
        ([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8, 2),
        ([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 13, 8),
        ([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 15, 9),
        ([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 0, 0),
        ([[-5]], -5, 1),
        ([[-5]], -6, 0),
        ([[1, 2], [1, 3]], 1, 2),
        ([[1, 2], [1, 3]], 2, 3),
    ],
)
def test_drill_04_count_le(matrix, v, expected_count):
    mod = _load("drill_04_solution")
    assert mod.count_le(matrix, v) == expected_count


@pytest.mark.parametrize(
    "matrix, k, expected",
    [
        ([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8, 13),
        ([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 1, 1),
        ([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 9, 15),
        ([[-5]], 1, -5),
        ([[1, 2], [1, 3]], 2, 1),
        ([[1, 2], [1, 3]], 3, 2),
        ([[1, 3, 5], [6, 7, 12], [11, 14, 14]], 6, 11),
        ([[1, 2], [3, 4]], 4, 4),
    ],
)
def test_drill_04_kth_smallest(matrix, k, expected):
    mod = _load("drill_04_solution")
    assert mod.kth_smallest(matrix, k) == expected


# -----------------------------------------------------------------------------
# Drill 5 - Koko eats bananas
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "piles, h, expected",
    [
        ([3, 6, 7, 11], 8, 4),
        ([30, 11, 23, 4, 20], 5, 30),
        ([30, 11, 23, 4, 20], 6, 23),
        ([1], 1, 1),
        ([1000000000], 1000000000, 1),
        ([312884470], 968709470, 1),
        ([1, 1, 1, 1, 1, 1, 1], 7, 1),
        ([1, 1, 1, 1, 1, 1, 1], 8, 1),
        ([5, 5, 5, 5], 4, 5),
        ([5, 5, 5, 5], 8, 3),    # 2+2+2+2 hours = 8
        ([10, 10, 10, 10], 4, 10),
        ([805306368, 805306368, 805306368], 1000000000, 3),
    ],
)
def test_drill_05_min_eating_speed(piles, h, expected):
    mod = _load("drill_05_solution")
    assert mod.min_eating_speed(piles, h) == expected


# -----------------------------------------------------------------------------
# Run with:
#     pytest exercises/timed_runner.py -v
#
# Or, to run only one drill:
#     pytest exercises/timed_runner.py::test_drill_05_min_eating_speed -v
#
# Add `--durations=10` to see which tests take longest - useful when checking
# that your binary-search loop hasn't accidentally degenerated into linear
# scan because of a wrong shrink rule. The runner doesn't enforce O(log n)
# mechanically - that's on your code review of your own solution and your
# interviewer's eye in Mock #2.
# -----------------------------------------------------------------------------
