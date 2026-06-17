"""Exercise 2 - K Closest Points to Origin (LeetCode 973).

Pattern: Size-k max-heap (via negation); heap-of-tuples; the k-closest template
from Lecture 2.
Difficulty: Medium.
Target solve time: 25 minutes with full UMPIRE narration.

Problem statement
-----------------
Given an array `points` where `points[i] = [x_i, y_i]` represents a point on
the 2-D plane, and an integer `k`, return the `k` closest points to the
origin `(0, 0)`.

Distance is Euclidean; ties in distance are not constrained (any valid
ordering is accepted).

The answer is guaranteed to be unique (except for the order that it is in).

Constraints (LeetCode):
- 1 <= k <= len(points) <= 10^4.
- -10^4 <= x_i, y_i <= 10^4.

Examples
--------
>>> sorted_pts(k_closest([[1, 3], [-2, 2]], 1))
[[-2, 2]]
>>> sorted_pts(k_closest([[3, 3], [5, -1], [-2, 4]], 2))
[[-2, 4], [3, 3]]
>>> sorted_pts(k_closest([[0, 1], [1, 0]], 2))
[[0, 1], [1, 0]]

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. K closest by Euclidean distance. Use distance-SQUARED
        (skip sqrt; monotone) to avoid floating-point error. Output order
        unspecified.
- [ ] M: Top-k variant with a distance key -> size-k MAX-heap (negated).
        Heap holds the k CLOSEST seen so far; the max (h[0][0] is the most
        negative -d^2, equivalently the LARGEST d^2) is the FARTHEST of the
        k -- the eviction bar. Why max-heap-for-closest: the max is the
        bar; any closer point evicts it. Why not sort: O(n log n) vs
        O(n log k). Why not heapq.nsmallest with key=: same algorithm
        internally; mention but implement manually for the template rep.
- [ ] P: For each [x, y]: d2 = x*x + y*y. If len(h) < k, push (-d2, x, y).
        Else if -d2 > h[0][0], heappushpop((-d2, x, y)). After the loop,
        return [[x, y] for (_, x, y) in h].
- [ ] I: Heap entries are 3-tuples (-d2, x, y). Coordinates serve as
        implicit tiebreaker (int, comparable).
- [ ] R: Trace on each example. Edge case: k == len(points) -- heap fills
        exactly; return all points.
- [ ] E: O(n log k) time, O(k) space. Tradeoff vs sort by key: O(n log n);
        heap wins when k << n. Tradeoff vs heapify+nsmallest:
        O(n + k log n), competitive when k ~ n.

References
----------
- Lecture 2, section 4: ../lecture-notes/02-heap-of-tuples-and-k-closest.md
- LeetCode 973: https://leetcode.com/problems/k-closest-points-to-origin/
- heapq.nsmallest: https://docs.python.org/3/library/heapq.html#heapq.nsmallest
"""

from __future__ import annotations

import heapq
from typing import List


def k_closest(points: List[List[int]], k: int) -> List[List[int]]:
    """Return the k points closest to the origin via a size-k max-heap.

    Replace the body with your solution. The signature and docstring
    above are part of the spec. Output order is unspecified.
    """
    # TODO: implement the size-k max-heap template.
    # Hint:
    #   h: List[tuple] = []
    #   for x, y in points:
    #       d2 = x * x + y * y
    #       if len(h) < k:
    #           heapq.heappush(h, (-d2, x, y))
    #       elif -d2 > h[0][0]:
    #           heapq.heappushpop(h, (-d2, x, y))
    #   return [[x, y] for (_, x, y) in h]
    _ = points, k  # silence unused-variable lint until you wire it up
    return []


def sorted_pts(pts: List[List[int]]) -> List[List[int]]:
    """Helper for deterministic test comparison; sorts points by (x, y)."""
    return sorted(pts, key=lambda p: (p[0], p[1]))


# ---------------------------------------------------------------------------
# Self-test block.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a battery of asserts against the public function.

    Output order is unspecified, so we compare *sets* of points after sorting.
    """
    cases: list[tuple[list[list[int]], int, list[list[int]]]] = [
        ([[1, 3], [-2, 2]], 1, [[-2, 2]]),
        ([[3, 3], [5, -1], [-2, 4]], 2, [[-2, 4], [3, 3]]),
        ([[0, 1], [1, 0]], 2, [[0, 1], [1, 0]]),
        ([[1, 1]], 1, [[1, 1]]),
        ([[0, 0], [1, 0], [0, 1], [1, 1]], 1, [[0, 0]]),
        ([[1, 0], [0, 1], [-1, 0], [0, -1]], 4, [[-1, 0], [0, -1], [0, 1], [1, 0]]),
        # k == n: every point is in the answer.
        ([[3, 3], [5, -1], [-2, 4]], 3, [[-2, 4], [3, 3], [5, -1]]),
    ]
    failures = 0
    for i, (pts, k, expected) in enumerate(cases, start=1):
        actual = sorted_pts(k_closest(pts, k))
        expected_sorted = sorted_pts(expected)
        marker = "OK  " if actual == expected_sorted else "FAIL"
        if actual != expected_sorted:
            failures += 1
            print(f"[{marker}] case {i}: expected {expected_sorted}, got {actual}")
        else:
            print(f"[{marker}] case {i}: {actual}")
    if failures:
        raise AssertionError(f"{failures} case(s) failed; implement k_closest.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
