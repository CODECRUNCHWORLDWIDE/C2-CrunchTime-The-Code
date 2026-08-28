"""Exercise 1 — Single Number (LeetCode 136).

Pattern: XOR fold.

PROBLEM
-------
Given a non-empty array of integers `nums`, every element appears TWICE
except for one element, which appears exactly once. Find that single element.

You must implement a solution with LINEAR runtime complexity and use only
CONSTANT extra space.

CONSTRAINTS
-----------
- 1 <= len(nums) <= 3 * 10**4
- -3 * 10**4 <= nums[i] <= 3 * 10**4
- Each element appears exactly twice except for one element that appears once.

EXAMPLES
--------
- single_number([2, 2, 1])        -> 1
- single_number([4, 1, 2, 1, 2])  -> 4
- single_number([1])              -> 1

FRAME CHECKLIST
----------------
- Frame: a multiset where every value is paired except one survivor.
- Research constraints: the binding limits are LINEAR time and CONSTANT
  space. That points at an XOR fold. Pairs cancel (a ^ a == 0); the survivor
  remains (a ^ 0 == a); order is irrelevant (XOR is commutative and
  associative). Reject the hash-map answer (O(n) space) and sort-then-scan
  (O(n log n) time, mutates input).
- Assess options: seed an accumulator at 0; XOR every element into it;
  return it.
- Make the solution: see below.
- Examine (verify): trace [4, 1, 2, 1, 2] -> 4; check the single-element
  case [1].
- Examine (cost): O(n) time, O(1) space. Strictly beats the hash-map
  alternative on space, which is what the constant-space constraint demands.
"""

from typing import List


def single_number(nums: List[int]) -> int:
    """Return the one element that appears exactly once; all others appear twice."""
    # TODO: XOR-fold the array into a single accumulator and return it.
    raise NotImplementedError


if __name__ == "__main__":
    assert single_number([2, 2, 1]) == 1
    assert single_number([4, 1, 2, 1, 2]) == 4
    assert single_number([1]) == 1
    assert single_number([0, 0, 7]) == 7
    assert single_number([-1, -1, -2]) == -2
    assert single_number([5, 3, 5, 3, 9]) == 9
    print("exercise-01-single-number: all tests passed")
