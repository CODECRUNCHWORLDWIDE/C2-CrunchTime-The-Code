"""
Week 1 — pytest grader for the five UMPIRE drills.

Place your solutions in this folder (or any folder on PYTHONPATH) with these
exact function names:

    drill_01_solution.reverse_string_in_place(s)
    drill_02_solution.is_palindrome(s)
    drill_03_solution.two_sum_sorted(nums, target)
    drill_04_solution.remove_duplicates(nums)
    drill_05_solution.max_area(heights)

Then run:

    pytest exercises/timed_runner.py -v

Acceptance criterion for the week: all tests pass on a fresh checkout.

If you implemented the function with a different name, edit the import lines
below. The point is the test logic, not the import shape.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

# Make this folder importable so drill_NN_solution.py modules are found.
sys.path.insert(0, str(Path(__file__).parent))


def _load(module_name: str):
    """Import a drill module lazily so missing solutions skip rather than break collection."""
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        pytest.skip(f"{module_name} not found — write your solution first.")


# ----- Drill 1 — Reverse string in place ---------------------------------


@pytest.mark.parametrize(
    "input_chars, expected",
    [
        (["h", "e", "l", "l", "o"], ["o", "l", "l", "e", "h"]),
        (["a"], ["a"]),
        ([], []),
        (["a", "b"], ["b", "a"]),
        (["a", "b", "c", "d", "e"], ["e", "d", "c", "b", "a"]),
    ],
)
def test_drill_01_reverse_string(input_chars, expected):
    mod = _load("drill_01_solution")
    s = list(input_chars)
    result = mod.reverse_string_in_place(s)
    assert result is None, "Drill 1 must mutate in place and return None"
    assert s == expected


# ----- Drill 2 — Valid palindrome ----------------------------------------


@pytest.mark.parametrize(
    "s, expected",
    [
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        ("", True),
        (".,", True),
        ("0P", False),
        ("a", True),
        ("ab", False),
    ],
)
def test_drill_02_valid_palindrome(s, expected):
    mod = _load("drill_02_solution")
    assert mod.is_palindrome(s) == expected


# ----- Drill 3 — Two Sum II (sorted, 1-indexed) --------------------------


@pytest.mark.parametrize(
    "nums, target, expected",
    [
        ([2, 7, 11, 15], 9, [1, 2]),
        ([2, 3, 4], 6, [1, 3]),
        ([-1, 0], -1, [1, 2]),
        ([1, 2, 3, 4, 4, 9, 56, 90], 8, [4, 5]),
    ],
)
def test_drill_03_two_sum_sorted(nums, target, expected):
    mod = _load("drill_03_solution")
    assert mod.two_sum_sorted(list(nums), target) == expected


# ----- Drill 4 — Remove duplicates in place ------------------------------


@pytest.mark.parametrize(
    "nums, expected_k, expected_prefix",
    [
        ([1, 1, 2], 2, [1, 2]),
        ([0, 0, 1, 1, 1, 2, 2, 3, 3, 4], 5, [0, 1, 2, 3, 4]),
        ([1], 1, [1]),
        ([], 0, []),
        ([1, 2, 3], 3, [1, 2, 3]),
    ],
)
def test_drill_04_remove_duplicates(nums, expected_k, expected_prefix):
    mod = _load("drill_04_solution")
    arr = list(nums)
    k = mod.remove_duplicates(arr)
    assert k == expected_k, "returned k mismatch"
    assert arr[:k] == expected_prefix, "first k elements mismatch"


# ----- Drill 5 — Container With Most Water -------------------------------


@pytest.mark.parametrize(
    "heights, expected",
    [
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
        ([1, 1], 1),
        ([4, 3, 2, 1, 4], 16),
        ([1, 2, 1], 2),
        ([2, 3, 4, 5, 18, 17, 6], 17),
    ],
)
def test_drill_05_max_area(heights, expected):
    mod = _load("drill_05_solution")
    assert mod.max_area(list(heights)) == expected


# -----------------------------------------------------------------------------
# Run with:
#     pytest exercises/timed_runner.py -v
#
# Or, to run only one drill:
#     pytest exercises/timed_runner.py::test_drill_03_two_sum_sorted -v
#
# Add `--durations=10` to see which tests take longest — useful when checking
# you haven't accidentally written an O(n^2) solution.
# -----------------------------------------------------------------------------
