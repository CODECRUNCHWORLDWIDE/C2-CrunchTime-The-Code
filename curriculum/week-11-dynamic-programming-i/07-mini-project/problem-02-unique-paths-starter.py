"""Mini-Project Problem 2 - Unique Paths (LeetCode 62).

Pattern: 2D counting DP; the canonical pull-from-top-and-left recurrence
from Lecture 2 section 2.
Difficulty: Medium.
Target solve time: 4 hours including the full UMPIRE write-up.

Problem statement
-----------------
There is a robot on an `m x n` grid. The robot is initially located at the
top-left corner (i.e., `grid[0][0]`). The robot tries to move to the
bottom-right corner (i.e., `grid[m - 1][n - 1]`). The robot can only move
either down or right at any point in time.

Given the two integers `m` and `n`, return the number of possible unique
paths that the robot can take to reach the bottom-right corner.

Constraints (LeetCode):
- 1 <= m, n <= 100.
- The answer is guaranteed to be less than or equal to 2 * 10^9.

Examples
--------
>>> unique_paths_memoized(3, 7)
28
>>> unique_paths_tabulated(3, 2)
3
>>> unique_paths_memoized(1, 1)
1

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. Count distinct paths from (0,0) to (m-1, n-1) moving only
        down or right. Confirm: 1 <= m, n; no obstacles in this version.
- [ ] M: 2D counting DP. State = "number of paths from (0,0) to (i,j)."
        Recurrence: dp[i][j] = dp[i-1][j] + dp[i][j-1]. Base cases: first
        row and first column all 1s. Two triggers fire. O(mn) time,
        O(min(m, n)) space with rolling row.
        Why not combinatorics: the closed form is C(m + n - 2, m - 1) and
        is faster (O(min(m, n)) time), but specific to this problem; a
        variant with obstacles (LC 63) breaks the closed form, and DP
        generalizes.
        Why not BFS: BFS reaches every cell once but does not sum paths;
        a BFS with state (cell, path_count) is the DP in disguise.
- [ ] P: Both implementations follow the four-step pipeline.
        Memoized: recursion paths(i, j) = paths(i-1, j) + paths(i, j-1)
        with base case paths(0, j) = paths(i, 0) = 1.
        Tabulated: build (m, n) table; iterate row by row.
- [ ] I: Type hints on every function; docstring on every function.
        For the memoized form, the function takes two ints (both hashable).
- [ ] R: Trace m = 3, n = 3:
        Row 0: [1, 1, 1]
        Row 1: [1, 2, 3]
        Row 2: [1, 3, 6]
        Answer: dp[2][2] = 6.
- [ ] E: O(mn) time for both implementations.
        Memoized: O(mn) space (cache + stack).
        Tabulated: O(mn) for full table, O(min(m, n)) with rolling row.

References
----------
- Lecture 2, sections 1 and 2 (2D DP + unique paths):
  ../lecture-notes/02-2d-dp-and-the-grid-and-string-shapes.md
- LeetCode 62: https://leetcode.com/problems/unique-paths/
- Python functools.lru_cache: https://docs.python.org/3/library/functools.html#functools.lru_cache
"""

from __future__ import annotations

import functools
from typing import List, Tuple


# ---------------------------------------------------------------------------
# Implementation 1: top-down memoization with functools.lru_cache.
# ---------------------------------------------------------------------------


@functools.lru_cache(maxsize=None)
def unique_paths_memoized(m: int, n: int) -> int:
    """Number of unique paths from (0,0) to (m-1, n-1) via top-down memoization.

    The four-step pipeline calls this Step 2: write the recursion, decorate
    with @lru_cache. The state is (m, n) where m and n are the remaining
    rows and columns to traverse. O(mn) time, O(mn) space.

    Replace the body. The signature and docstring are part of the spec.
    """
    # TODO: handle the base cases
    # Hint:
    #   if m == 1 or n == 1:
    #       return 1

    # TODO: apply the recurrence (paths from top + paths from left)
    # Hint:
    #   return unique_paths_memoized(m - 1, n) + unique_paths_memoized(m, n - 1)
    _ = m, n
    return 0


# ---------------------------------------------------------------------------
# Implementation 2: bottom-up tabulation with rolling-row space reduction.
# ---------------------------------------------------------------------------


def unique_paths_tabulated(m: int, n: int) -> int:
    """Number of unique paths via bottom-up tabulation with rolling row.

    The four-step pipeline calls this Steps 3 and 4: build the table, then
    reduce to a single rolling row. O(mn) time, O(n) space.

    Replace the body. The signature and docstring are part of the spec.
    """
    # TODO: handle the trivial cases
    # Hint:
    #   if m == 1 or n == 1:
    #       return 1

    # TODO: initialize the rolling row (first row is all 1s)
    # Hint:
    #   dp: List[int] = [1] * n

    # TODO: iterate the remaining rows, updating dp[j] in place
    # Hint:
    #   for _ in range(1, m):
    #       for j in range(1, n):
    #           dp[j] = dp[j] + dp[j - 1]
    #   return dp[n - 1]
    _ = m, n
    return 0


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 problem-02-unique-paths-starter.py`.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a battery of asserts against both implementations."""
    failures = 0
    cases: List[Tuple[str, int, int, int]] = [
        ("LC 62 example 1", 3, 7, 28),
        ("LC 62 example 2", 3, 2, 3),
        ("single cell", 1, 1, 1),
        ("single row", 1, 10, 1),
        ("single column", 10, 1, 1),
        ("2x2", 2, 2, 2),
        ("3x3 (the canonical trace)", 3, 3, 6),
        ("4x4", 4, 4, 20),
        ("5x5", 5, 5, 70),
        ("LC max 100x100", 100, 100, 22750883079422934966181954039568885395604168260154104734000),
    ]
    # Note: the LC max case truncates at 2e9 in the problem statement; the actual
    # combinatorial value is much larger. We test against the true value here to
    # exercise Python's arbitrary-precision integers.
    for label, m, n, expected in cases:
        for impl_name, impl in (
            ("memoized", unique_paths_memoized),
            ("tabulated", unique_paths_tabulated),
        ):
            actual = impl(m, n)
            marker = "OK  " if actual == expected else "FAIL"
            if actual != expected:
                failures += 1
                print(
                    f"[{marker}] {impl_name} {label}: unique_paths({m}, {n}) -> {actual}, expected {expected}"
                )
            else:
                print(f"[{marker}] {impl_name} {label}: unique_paths({m}, {n}) -> {actual}")
    if failures:
        raise AssertionError(
            f"{failures} assertion(s) failed; implement both unique_paths variants."
        )
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
