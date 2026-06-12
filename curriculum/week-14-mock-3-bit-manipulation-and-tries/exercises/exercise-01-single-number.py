"""Exercise 1 - Single Number (LeetCode 136).

Pattern: bit manipulation; XOR-cancellation, the canonical warm-up from
Lecture 1 sections 3 and 4.
Difficulty: Easy.
Target solve time: 15 minutes with full UMPIRE narration.

Problem statement
-----------------
Given a non-empty array of integers `nums`, every element appears twice
except for one. Find that single one. You must implement a solution with
linear runtime complexity and use only constant extra space.

Constraints (LeetCode):
- 1 <= len(nums) <= 3 * 10^4.
- -3 * 10^4 <= nums[i] <= 3 * 10^4.
- Each element appears twice except for one element which appears once.

Examples
--------
>>> single_number([2, 2, 1])
1
>>> single_number([4, 1, 2, 1, 2])
4
>>> single_number([1])
1

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. Given an array where every value appears twice except one,
        return the lone value. Confirm: exactly one value is unpaired; all
        others appear exactly twice.
- [ ] M: Bit manipulation - XOR-cancellation. The tells: "constant extra
        space" (rules out a hash map / Counter) plus "every element appears
        twice except one." XOR every element; pairs self-cancel (x ^ x = 0);
        the survivor is the answer (x ^ 0 = x). Why not a hash map: O(n)
        space, forbidden. Why not a sort: O(n log n) and mutates input.
- [ ] P: Initialize an accumulator to 0 (the XOR identity). XOR every element
        into it. Return the accumulator.
- [ ] I: A single pass with `result ^= num`. O(n) time, O(1) space.
- [ ] R: Trace [4, 1, 2, 1, 2]: 0^4=4, 4^1=5, 5^2=7, 7^1=6, 6^2=4. Return 4.
        Or group: 4 ^ (1^1) ^ (2^2) = 4 ^ 0 ^ 0 = 4.
- [ ] E: O(n) time, O(1) space. Trade vs. hash map: same time, O(n) space.
        Trade vs. sort: O(n log n). The constant-space constraint is the
        tell that selects XOR over both alternatives.

References
----------
- Lecture 1, sections 3 and 4 (the XOR identities + single number):
  ../lecture-notes/01-bit-manipulation-and-xor-tricks.md
- LeetCode 136: https://leetcode.com/problems/single-number/
- XOR properties: https://en.wikipedia.org/wiki/Exclusive_or
"""

from __future__ import annotations

from typing import List, Tuple


def single_number(nums: List[int]) -> int:
    """Return the element that appears exactly once; all others appear twice.

    Implement with XOR-cancellation: XOR every element into an accumulator
    initialized to 0 (the XOR identity). Paired elements cancel; the unique
    element survives. O(n) time, O(1) space.

    Replace the body with your solution. The signature and docstring above
    are part of the spec.
    """
    # TODO: initialize the accumulator to the XOR identity
    # Hint:
    #   result = 0

    # TODO: XOR every element in
    # Hint:
    #   for num in nums:
    #       result ^= num
    #   return result
    _ = nums  # silence unused-variable lint until you wire it up
    return 0


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 exercise-01-single-number.py`.
# Also discovered by `pytest`.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a battery of asserts against the single_number function."""
    failures = 0
    cases: List[Tuple[str, List[int], int]] = [
        ("LC 136 example 1", [2, 2, 1], 1),
        ("LC 136 example 2", [4, 1, 2, 1, 2], 4),
        ("LC 136 example 3 (single element)", [1], 1),
        ("negative unique", [-1, 5, 5], -1),
        ("zero is the unique", [0, 7, 7], 0),
        ("unique at the end", [3, 3, 9], 9),
        ("larger array", [10, 10, 20, 30, 20], 30),
        ("all-but-one paired, big", [1, 1, 2, 2, 3, 3, 4, 4, 99], 99),
    ]
    for label, nums, expected in cases:
        actual = single_number(nums)
        marker = "OK  " if actual == expected else "FAIL"
        if actual != expected:
            failures += 1
            print(
                f"[{marker}] {label}: single_number({nums}) -> {actual}, expected {expected}"
            )
        else:
            print(f"[{marker}] {label}: single_number({nums}) -> {actual}")
    if failures:
        raise AssertionError(f"{failures} assertion(s) failed; implement single_number.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
