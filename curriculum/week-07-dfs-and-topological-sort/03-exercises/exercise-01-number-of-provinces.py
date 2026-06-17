"""Exercise 1 - Number of Provinces (LeetCode 547).

Pattern: Recursive DFS on an adjacency matrix; connected components.
Difficulty: Easy / Medium.
Target solve time: 20 minutes with full UMPIRE narration.

Problem statement
-----------------
There are `n` cities. Some are connected, others are not. A "province" is a
group of directly or indirectly connected cities (i.e., a connected
component).

You are given an `n x n` matrix `is_connected` where:
- `is_connected[i][j] == 1` if the i-th city and the j-th city are directly
  connected.
- `is_connected[i][j] == 0` otherwise.
- The matrix is symmetric: `is_connected[i][j] == is_connected[j][i]`.
- The diagonal is 1: every city is "connected to itself."

Return the total number of provinces.

Constraints (LeetCode):
- 1 <= n <= 200.
- is_connected[i][i] == 1.
- is_connected[i][j] == is_connected[j][i].

Examples
--------
>>> find_circle_num([[1, 1, 0], [1, 1, 0], [0, 0, 1]])
2
>>> find_circle_num([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
3
>>> find_circle_num([[1]])
1

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. Confirm symmetric matrix; diagonal is 1.
- [ ] M: Connectivity on an undirected graph -> DFS-for-connectivity. Sub-shape:
        adjacency matrix; nodes are integers 0..n-1; edges are off-diagonal 1s.
        Why recursive DFS: the problem caps n at 200, well below Python's
        default recursion limit of 1000. Why not iterative: not needed at this
        scale. Why not union-find: works equally well in O(n^2) with a slightly
        larger constant; DFS is structurally simpler.
- [ ] P: Outer loop over cities; on first unvisited city, increment counter and
        DFS to mark its province; continue.
- [ ] I: Recursive DFS body adds to visited at function entry; iterates columns
        of the matrix row to find neighbors.
- [ ] R: Trace on the three examples above. Edge case: n = 1 -> exactly 1
        province.
- [ ] E: O(n^2) time (we read every matrix cell at most once across all DFS
        calls). O(n) space for the visited set and the recursion stack.
        Tradeoff vs BFS: same complexity, more code. Tradeoff vs union-find:
        slightly worse constant but cleaner correctness story.

References
----------
- Lecture 1, section 7 (worked example): ../lecture-notes/01-recursive-dfs.md
- LeetCode 547: https://leetcode.com/problems/number-of-provinces/
"""

from __future__ import annotations

from typing import List


def find_circle_num(is_connected: List[List[int]]) -> int:
    """Return the number of provinces (connected components).

    Replace the body with your DFS solution. The signature and docstring
    above are part of the spec.
    """
    # TODO: implement recursive DFS for connectivity.
    # Hint: use a nested helper `def dfs(node: int) -> None:` that captures
    # `visited` from the enclosing scope. Add to visited on function entry.
    # Iterate columns of `is_connected[node]` to find neighbors.
    _ = is_connected  # silence unused-variable lint until you wire it up
    return 0


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 exercise-01-number-of-provinces.py`.
# Also discovered by `pytest`.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a small battery of asserts against the public function.

    The asserts intentionally cover the canonical edge cases. When `find_circle_num`
    is unimplemented (returns 0 by default), most asserts will fail loudly --
    that is the signal to implement.
    """
    cases: list[tuple[list[list[int]], int]] = [
        ([[1, 1, 0], [1, 1, 0], [0, 0, 1]], 2),
        ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 3),
        ([[1]], 1),
        ([[1, 1], [1, 1]], 1),
        ([[1, 0], [0, 1]], 2),
        (
            [
                [1, 1, 0, 0],
                [1, 1, 0, 0],
                [0, 0, 1, 1],
                [0, 0, 1, 1],
            ],
            2,
        ),
        (
            [
                [1, 1, 0, 0, 0],
                [1, 1, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 1, 1],
                [0, 0, 0, 1, 1],
            ],
            3,
        ),
        # Fully connected chain: 0-1-2-3-4 (each adjacent to its neighbors).
        (
            [
                [1, 1, 0, 0, 0],
                [1, 1, 1, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 1, 1, 1],
                [0, 0, 0, 1, 1],
            ],
            1,
        ),
    ]
    failures = 0
    for i, (grid, expected) in enumerate(cases, start=1):
        actual = find_circle_num(grid)
        marker = "OK " if actual == expected else "FAIL"
        if actual != expected:
            failures += 1
            print(f"[{marker}] case {i}: expected {expected}, got {actual}")
        else:
            print(f"[{marker}] case {i}: {actual}")
    if failures:
        raise AssertionError(f"{failures} case(s) failed; implement find_circle_num.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
