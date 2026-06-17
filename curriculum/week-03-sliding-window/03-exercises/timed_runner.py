"""
Week 3 — pytest grader for the five UMPIRE sliding-window drills.

Place your solutions in this folder (or any folder on PYTHONPATH) with these
exact function names:

    drill_01_solution.window_averages(nums, k)
    drill_02_solution.longest_substring_no_repeat(s)
    drill_03_solution.check_inclusion(s1, s2)
    drill_04_solution.min_size_subarray_sum(target, nums)
    drill_05_solution.total_fruit(fruits)

Then run:

    pytest exercises/timed_runner.py -v

Acceptance criterion for the week: all tests pass on a fresh checkout.

If you implemented the function with a different name, edit the import lines
below. The point is the test logic, not the import shape.
"""

from __future__ import annotations

import importlib
import math
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


def _approx_equal_lists(got, expected, tol=1e-6):
    """Float-list comparison with a per-element tolerance."""
    if len(got) != len(expected):
        return False
    return all(math.isclose(a, b, abs_tol=tol) for a, b in zip(got, expected))


# ----- Drill 1 - Window averages (fixed-size) ---------------------------


@pytest.mark.parametrize(
    "nums, k, expected",
    [
        ([1, 3, 2, 6, -1, 4, 1, 8, 2], 5, [2.2, 2.8, 2.4, 3.6, 2.8]),
        ([1, 2, 3, 4], 2, [1.5, 2.5, 3.5]),
        ([5], 1, [5.0]),
        ([1, 2], 3, []),
        ([], 1, []),
        ([4, 4, 4, 4], 2, [4.0, 4.0, 4.0]),
        ([1, 2, 3, 4, 5], 5, [3.0]),
    ],
)
def test_drill_01_window_averages(nums, k, expected):
    mod = _load("drill_01_solution")
    got = mod.window_averages(list(nums), k)
    assert _approx_equal_lists(got, expected), f"got {got}, expected {expected}"


# ----- Drill 2 - Longest substring without repeating characters ---------


@pytest.mark.parametrize(
    "s, expected",
    [
        ("abcabcbb", 3),
        ("bbbbb", 1),
        ("pwwkew", 3),
        ("", 0),
        ("a", 1),
        ("dvdf", 3),
        ("abba", 2),
        ("tmmzuxt", 5),
    ],
)
def test_drill_02_longest_substring_no_repeat(s, expected):
    mod = _load("drill_02_solution")
    assert mod.longest_substring_no_repeat(s) == expected


# ----- Drill 3 - Permutation in string (fixed-size, frequency) ----------


@pytest.mark.parametrize(
    "s1, s2, expected",
    [
        ("ab", "eidbaooo", True),
        ("ab", "eidboaoo", False),
        ("abc", "ccccbabcaaabc", True),
        ("a", "a", True),
        ("ab", "a", False),
        ("hello", "ooolleoooleh", False),
        ("adc", "dcda", True),
    ],
)
def test_drill_03_check_inclusion(s1, s2, expected):
    mod = _load("drill_03_solution")
    assert mod.check_inclusion(s1, s2) is expected


# ----- Drill 4 - Minimum size subarray sum (shape B) --------------------


@pytest.mark.parametrize(
    "target, nums, expected",
    [
        (7, [2, 3, 1, 2, 4, 3], 2),
        (4, [1, 4, 4], 1),
        (11, [1, 1, 1, 1, 1, 1, 1, 1], 0),
        (15, [1, 2, 3, 4, 5], 5),
        (213, [12, 28, 83, 4, 25, 26, 25, 2, 25, 25, 25, 12], 8),
        (3, [1, 1], 0),
        (6, [10, 2, 3], 1),
    ],
)
def test_drill_04_min_size_subarray_sum(target, nums, expected):
    mod = _load("drill_04_solution")
    assert mod.min_size_subarray_sum(target, list(nums)) == expected


# ----- Drill 5 - Fruit into baskets (at most 2 distinct) ----------------


@pytest.mark.parametrize(
    "fruits, expected",
    [
        ([1, 2, 1], 3),
        ([0, 1, 2, 2], 3),
        ([1, 2, 3, 2, 2], 4),
        ([3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4], 5),
        ([], 0),
        ([1], 1),
        ([1, 1, 1, 1], 4),
        ([1, 2, 1, 2, 1, 2, 1], 7),
    ],
)
def test_drill_05_total_fruit(fruits, expected):
    mod = _load("drill_05_solution")
    assert mod.total_fruit(list(fruits)) == expected


# -----------------------------------------------------------------------------
# Run with:
#     pytest exercises/timed_runner.py -v
#
# Or, to run only one drill:
#     pytest exercises/timed_runner.py::test_drill_02_longest_substring_no_repeat -v
#
# Add `--durations=10` to see which tests take longest - useful when checking
# you haven't accidentally written an O(n*k) or O(n^2) solution where O(n) is
# required.
# -----------------------------------------------------------------------------
