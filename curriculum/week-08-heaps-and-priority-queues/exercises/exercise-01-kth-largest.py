"""Exercise 1 - Kth Largest Element in an Array (LeetCode 215).

Pattern: Size-k min-heap; the top-k template from Lecture 1.
Difficulty: Easy / Medium.
Target solve time: 20 minutes with full UMPIRE narration.

Problem statement
-----------------
Given an integer array `nums` and an integer `k`, return the k-th largest
element in the array.

Note: this is the k-th largest in *sorted order*, not the k-th distinct
element.

Constraints (LeetCode):
- 1 <= k <= len(nums) <= 10^5.
- -10^4 <= nums[i] <= 10^4.

Examples
--------
>>> find_kth_largest([3, 2, 1, 5, 6, 4], 2)
5
>>> find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4)
4
>>> find_kth_largest([1], 1)
1

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. K-th largest in sorted order; ties count toward the rank.
- [ ] M: Top-k pattern -> size-k MIN-heap. The heap holds the k largest seen
        so far; the minimum of the heap (h[0]) is the k-th largest. Why
        min-heap-for-largest: the min is the eviction bar -- any new value
        larger than h[0] should replace it. Why not sort: O(n log n) vs
        O(n log k). Why not quickselect: O(n) expected but O(n^2) worst.
- [ ] P: For each x in nums: if len(h) < k, push; else if x > h[0],
        heappushpop. After the loop, return h[0].
- [ ] I: Use heapq.heappush and heapq.heappushpop. Initialize h as an empty
        list.
- [ ] R: Trace on each example. Edge case: nums has exactly k elements;
        h fills exactly and h[0] is the global minimum, which is the k-th
        largest.
- [ ] E: O(n log k) time, O(k) space. Tradeoff vs sort: O(n log n);
        the heap wins when k << n. Tradeoff vs quickselect: expected O(n)
        but O(n^2) worst.

References
----------
- Lecture 1, section 6 (worked example): ../lecture-notes/01-heapq-and-top-k.md
- LeetCode 215: https://leetcode.com/problems/kth-largest-element-in-an-array/
- heapq docs: https://docs.python.org/3/library/heapq.html
"""

from __future__ import annotations

import heapq
from typing import List


def find_kth_largest(nums: List[int], k: int) -> int:
    """Return the k-th largest element via a size-k min-heap.

    Replace the body with your solution. The signature and docstring
    above are part of the spec.
    """
    # TODO: implement the size-k min-heap template.
    # Hint:
    #   h: List[int] = []
    #   for x in nums:
    #       if len(h) < k:
    #           heapq.heappush(h, x)
    #       elif x > h[0]:
    #           heapq.heappushpop(h, x)
    #   return h[0]
    _ = nums, k  # silence unused-variable lint until you wire it up
    return 0


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 exercise-01-kth-largest.py`.
# Also discovered by `pytest`.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a battery of asserts against the public function.

    The asserts cover the canonical edge cases. When `find_kth_largest`
    is unimplemented (returns 0 by default), most asserts will fail loudly --
    that is the signal to implement.
    """
    cases: list[tuple[list[int], int, int]] = [
        ([3, 2, 1, 5, 6, 4], 2, 5),
        ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4),
        ([1], 1, 1),
        ([1, 2], 1, 2),
        ([1, 2], 2, 1),
        ([7, 7, 7, 7], 2, 7),  # ties count toward the rank
        ([-1, -2, -3, -4, -5], 3, -3),
        ([0, 0, 0, 0, 0, 1], 1, 1),
        ([5, 4, 3, 2, 1], 5, 1),
        (list(range(1, 101)), 1, 100),
        (list(range(1, 101)), 100, 1),
        (list(range(1, 101)), 50, 51),
    ]
    failures = 0
    for i, (arr, k, expected) in enumerate(cases, start=1):
        actual = find_kth_largest(arr, k)
        marker = "OK  " if actual == expected else "FAIL"
        if actual != expected:
            failures += 1
            print(f"[{marker}] case {i}: expected {expected}, got {actual}")
        else:
            print(f"[{marker}] case {i}: {actual}")
    if failures:
        raise AssertionError(f"{failures} case(s) failed; implement find_kth_largest.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
