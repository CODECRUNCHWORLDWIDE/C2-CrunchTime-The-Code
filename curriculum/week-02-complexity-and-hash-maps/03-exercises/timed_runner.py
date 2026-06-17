"""
Week 2 — pytest grader for the five UMPIRE hash-map drills.

Place your solutions in this folder (or any folder on PYTHONPATH) with these
exact function names:

    drill_01_solution.two_sum_unsorted(nums, target)
    drill_02_solution.contains_duplicate(nums)
    drill_03_solution.group_anagrams(strs)
    drill_04_solution.is_valid_sudoku(board)
    drill_05_solution.longest_consecutive(nums)

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
    """Import a drill module lazily so missing solutions skip rather than fail collection."""
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        pytest.skip(f"{module_name} not found — write your solution first.")


def _normalize_pair(pair):
    """Two-sum may return [i, j] or [j, i]; normalize to a sorted tuple."""
    return tuple(sorted(pair))


def _normalize_groups(groups):
    """Group-anagrams answers may be in any order, inside and out."""
    return sorted(tuple(sorted(g)) for g in groups)


# ----- Drill 1 — Two Sum (unsorted) --------------------------------------


@pytest.mark.parametrize(
    "nums, target, expected_pair",
    [
        ([2, 7, 11, 15], 9, (0, 1)),
        ([3, 2, 4], 6, (1, 2)),
        ([3, 3], 6, (0, 1)),
        ([-1, -2, -3, -4, -5], -8, (2, 4)),
        ([0, 4, 3, 0], 0, (0, 3)),
    ],
)
def test_drill_01_two_sum_unsorted(nums, target, expected_pair):
    mod = _load("drill_01_solution")
    got = mod.two_sum_unsorted(list(nums), target)
    assert _normalize_pair(got) == expected_pair


# ----- Drill 2 — Contains Duplicate --------------------------------------


@pytest.mark.parametrize(
    "nums, expected",
    [
        ([1, 2, 3, 1], True),
        ([1, 2, 3, 4], False),
        ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2], True),
        ([], False),
        ([42], False),
        ([-1, -1], True),
    ],
)
def test_drill_02_contains_duplicate(nums, expected):
    mod = _load("drill_02_solution")
    assert mod.contains_duplicate(list(nums)) is expected


# ----- Drill 3 — Group Anagrams ------------------------------------------


@pytest.mark.parametrize(
    "strs, expected_groups",
    [
        (
            ["eat", "tea", "tan", "ate", "nat", "bat"],
            [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]],
        ),
        ([""], [[""]]),
        (["a"], [["a"]]),
        (["abc", "bca", "cab", "xyz"], [["abc", "bca", "cab"], ["xyz"]]),
    ],
)
def test_drill_03_group_anagrams(strs, expected_groups):
    mod = _load("drill_03_solution")
    got = mod.group_anagrams(list(strs))
    assert _normalize_groups(got) == _normalize_groups(expected_groups)


# ----- Drill 4 — Valid Sudoku --------------------------------------------


_VALID_BOARD = [
    ["5", "3", ".", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"],
]

_INVALID_BOARD_ROW = [
    ["5", "3", ".", ".", "7", ".", ".", ".", "3"],  # two '3's in row 0
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"],
]

_EMPTY_BOARD = [["." for _ in range(9)] for _ in range(9)]


@pytest.mark.parametrize(
    "board, expected",
    [
        (_VALID_BOARD, True),
        (_INVALID_BOARD_ROW, False),
        (_EMPTY_BOARD, True),
    ],
)
def test_drill_04_is_valid_sudoku(board, expected):
    mod = _load("drill_04_solution")
    assert mod.is_valid_sudoku([row[:] for row in board]) is expected


# ----- Drill 5 — Longest Consecutive Sequence ----------------------------


@pytest.mark.parametrize(
    "nums, expected",
    [
        ([100, 4, 200, 1, 3, 2], 4),
        ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9),
        ([], 0),
        ([1, 2, 0, 1], 3),
        ([9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6], 7),
        ([1], 1),
        ([1, 2], 2),
    ],
)
def test_drill_05_longest_consecutive(nums, expected):
    mod = _load("drill_05_solution")
    assert mod.longest_consecutive(list(nums)) == expected


# -----------------------------------------------------------------------------
# Run with:
#     pytest exercises/timed_runner.py -v
#
# Or, to run only one drill:
#     pytest exercises/timed_runner.py::test_drill_01_two_sum_unsorted -v
#
# Add `--durations=10` to see which tests take longest — useful when checking
# you haven't accidentally written an O(n^2) solution where O(n) is required.
# -----------------------------------------------------------------------------
