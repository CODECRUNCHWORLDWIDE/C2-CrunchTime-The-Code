"""Exercise 3 - Find Median from Data Stream (LeetCode 295).

Pattern: Two-heap balance; the running-median template from Lecture 3.
Difficulty: Hard.
Target solve time: 30 minutes with full UMPIRE narration.

Problem statement
-----------------
Design a data structure that supports two operations:

- `add_num(num: int) -> None`: add the integer `num` to the data structure.
- `find_median() -> float`: return the median of all elements added so far.

The median is the middle value when the data is sorted (odd count) or the
average of the two middle values (even count).

Constraints (LeetCode):
- -10^5 <= num <= 10^5.
- There will be at least one element before any `find_median` call.
- At most 5 * 10^4 calls total.

Examples
--------
>>> mf = MedianFinder()
>>> mf.add_num(1); mf.add_num(2); mf.find_median()
1.5
>>> mf.add_num(3); mf.find_median()
2.0

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. Stream of integers; support add and median queries.
        Median is either the middle element (odd count) or the average of
        the two middle (even count). The stream is unbounded; we cannot
        sort on every query.
- [ ] M: Two-heap pattern. Max-heap `lower` of the smaller half; min-heap
        `upper` of the larger half. Invariants:
        - lower.max <= upper.min (every lower element <= every upper element)
        - |len(lower) - len(upper)| <= 1, with lower as the larger when
          they differ.
        Median is lower[0] (odd, lower bigger) or
        (-lower[0] + upper[0]) / 2 (even).
        Why two heaps not one sorted list: O(log n) per add vs O(n) for
        insertion into a sorted list. O(1) per median query for both.
- [ ] P: add_num(x):
          1. heappush(lower, -x)             # push to max-heap (negated)
          2. heappush(upper, -heappop(lower)) # move max of lower to upper
          3. if len(upper) > len(lower): heappush(lower, -heappop(upper))
        find_median():
          1. if len(lower) > len(upper): return -lower[0]
          2. else: return (-lower[0] + upper[0]) / 2.0
- [ ] I: Two list attributes (`self.lower`, `self.upper`). Three heapq
        calls per add. Two reads per median.
- [ ] R: Trace on the examples and edge cases:
          - Single add then median: median is the element itself.
          - Many adds in monotone-increasing or -decreasing order.
- [ ] E: O(log n) per add (three heap operations of size <= n).
        O(1) per find_median (direct array reads). O(n) total space.
        Tradeoff vs single sorted-list-with-bisect: O(log n) bisect lookup
        but O(n) insert; the two-heap is strictly cheaper for adds.

References
----------
- Lecture 3, section 1: ../lecture-notes/03-two-heap-and-k-way-merge.md
- LeetCode 295: https://leetcode.com/problems/find-median-from-data-stream/
- heapq docs: https://docs.python.org/3/library/heapq.html
"""

from __future__ import annotations

import heapq
from typing import List


class MedianFinder:
    """Running median of a stream of integers.

    Replace the bodies of add_num and find_median with your solution.
    The class layout, constructor, and method signatures are part of the
    spec.

    Invariants the implementation must maintain:
    - self.lower is a MAX-heap (stored with negated values).
    - self.upper is a MIN-heap.
    - len(self.lower) - len(self.upper) is 0 or 1.
    - max of self.lower (= -self.lower[0]) <= min of self.upper (= self.upper[0])
      whenever both are non-empty.
    """

    def __init__(self) -> None:
        self.lower: List[int] = []
        self.upper: List[int] = []

    def add_num(self, num: int) -> None:
        """Insert `num` into the data structure."""
        # TODO: implement the three-step push-then-rebalance.
        # Hint:
        #   heapq.heappush(self.lower, -num)
        #   heapq.heappush(self.upper, -heapq.heappop(self.lower))
        #   if len(self.upper) > len(self.lower):
        #       heapq.heappush(self.lower, -heapq.heappop(self.upper))
        _ = num
        return None

    def find_median(self) -> float:
        """Return the current median."""
        # TODO: implement the two-case median read.
        # Hint:
        #   if len(self.lower) > len(self.upper):
        #       return float(-self.lower[0])
        #   return (-self.lower[0] + self.upper[0]) / 2.0
        return 0.0


# ---------------------------------------------------------------------------
# Self-test block.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a battery of asserts against MedianFinder."""
    failures = 0

    # Case 1: documented example.
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(2)
    if abs(mf.find_median() - 1.5) > 1e-9:
        failures += 1
        print(f"[FAIL] case 1: median after 1, 2 should be 1.5, got {mf.find_median()}")
    else:
        print(f"[OK  ] case 1: median after 1, 2 = {mf.find_median()}")
    mf.add_num(3)
    if abs(mf.find_median() - 2.0) > 1e-9:
        failures += 1
        print(f"[FAIL] case 1b: median after 1, 2, 3 should be 2.0, got {mf.find_median()}")
    else:
        print(f"[OK  ] case 1b: median after 1, 2, 3 = {mf.find_median()}")

    # Case 2: single element.
    mf2 = MedianFinder()
    mf2.add_num(42)
    if abs(mf2.find_median() - 42.0) > 1e-9:
        failures += 1
        print(f"[FAIL] case 2: single-element median should be 42, got {mf2.find_median()}")
    else:
        print(f"[OK  ] case 2: single element = {mf2.find_median()}")

    # Case 3: monotone increasing.
    mf3 = MedianFinder()
    for x in [1, 2, 3, 4, 5]:
        mf3.add_num(x)
    if abs(mf3.find_median() - 3.0) > 1e-9:
        failures += 1
        print(f"[FAIL] case 3: median of 1..5 should be 3.0, got {mf3.find_median()}")
    else:
        print(f"[OK  ] case 3: median of 1..5 = {mf3.find_median()}")

    # Case 4: monotone decreasing.
    mf4 = MedianFinder()
    for x in [5, 4, 3, 2, 1]:
        mf4.add_num(x)
    if abs(mf4.find_median() - 3.0) > 1e-9:
        failures += 1
        print(f"[FAIL] case 4: median of 5..1 should be 3.0, got {mf4.find_median()}")
    else:
        print(f"[OK  ] case 4: median of 5..1 = {mf4.find_median()}")

    # Case 5: ties.
    mf5 = MedianFinder()
    for x in [7, 7, 7, 7]:
        mf5.add_num(x)
    if abs(mf5.find_median() - 7.0) > 1e-9:
        failures += 1
        print(f"[FAIL] case 5: median of 7,7,7,7 should be 7.0, got {mf5.find_median()}")
    else:
        print(f"[OK  ] case 5: median of 7,7,7,7 = {mf5.find_median()}")

    # Case 6: negatives.
    mf6 = MedianFinder()
    for x in [-5, -3, -1, 0, 2]:
        mf6.add_num(x)
    if abs(mf6.find_median() - (-1.0)) > 1e-9:
        failures += 1
        print(f"[FAIL] case 6: median of -5,-3,-1,0,2 should be -1.0, got {mf6.find_median()}")
    else:
        print(f"[OK  ] case 6: median of -5,-3,-1,0,2 = {mf6.find_median()}")

    # Case 7: alternating queries.
    mf7 = MedianFinder()
    mf7.add_num(1)
    if abs(mf7.find_median() - 1.0) > 1e-9:
        failures += 1
        print(f"[FAIL] case 7a: median after 1 should be 1.0")
    else:
        print(f"[OK  ] case 7a: median after 1 = {mf7.find_median()}")
    mf7.add_num(10)
    if abs(mf7.find_median() - 5.5) > 1e-9:
        failures += 1
        print(f"[FAIL] case 7b: median after 1, 10 should be 5.5")
    else:
        print(f"[OK  ] case 7b: median after 1, 10 = {mf7.find_median()}")
    mf7.add_num(5)
    if abs(mf7.find_median() - 5.0) > 1e-9:
        failures += 1
        print(f"[FAIL] case 7c: median after 1, 10, 5 should be 5.0")
    else:
        print(f"[OK  ] case 7c: median after 1, 10, 5 = {mf7.find_median()}")

    if failures:
        raise AssertionError(f"{failures} case(s) failed; implement MedianFinder.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
