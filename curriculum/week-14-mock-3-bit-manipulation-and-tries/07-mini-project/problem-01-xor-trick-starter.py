"""Mini-Project Problem 1 - Single Number III (LeetCode 260).

Pattern: bit manipulation; the two-single-numbers partition from Lecture 1
section 6 (XOR the array, isolate a distinguishing bit, partition, XOR each
half).
Difficulty: Medium.
Target solve time: 2 hours including the full UMPIRE write-up.

Problem statement
-----------------
Given an integer array `nums` in which exactly two elements appear only once
and all the other elements appear exactly twice, find the two elements that
appear only once. You may return the answer in any order. Your algorithm
should run in linear runtime and use only constant extra space.

Constraints (LeetCode):
- 2 <= len(nums) <= 3 * 10^4.
- -2^31 <= nums[i] <= 2^31 - 1.
- Exactly two elements appear once; every other element appears twice.

Examples
--------
>>> sorted(single_number_iii([1, 2, 1, 3, 2, 5]))
[3, 5]
>>> sorted(single_number_iii([-1, 0]))
[-1, 0]
>>> sorted(single_number_iii([0, 1]))
[0, 1]

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. Two values appear once; all others appear twice. Return the
        two singletons. Confirm: constant space, linear time required.
- [ ] M: Bit manipulation - XOR-cancellation plus partition. XOR everything ->
        a ^ b (duplicates cancel). a != b, so a ^ b has a set bit; isolate the
        lowest with x & -x. Partition by that bit: a and b differ there so they
        split apart; every duplicate pair shares all bits so it stays together.
        XOR each group to recover a and b. Why not a hash map: O(n) space,
        forbidden.
- [ ] P: 1) xor_all = XOR of nums. 2) diff_bit = xor_all & -xor_all.
        3) a = XOR of the elements with diff_bit set. 4) b = xor_all ^ a.
- [ ] I: O(n) time, O(1) space. Type hints; docstring.
- [ ] R: Trace [1, 2, 1, 3, 2, 5]: xor_all = 3 ^ 5 = 6 (110); diff_bit = 6 & -6
        = 2 (010); group with bit 1 set: 2, 3, 2 -> XOR = 3 = a; b = 6 ^ 3 = 5.
- [ ] E: O(n) time, O(1) space. The partition-by-a-distinguishing-bit move is
        the reusable technique; isolate the bit with x & -x.

References
----------
- Lecture 1, section 6 (two single numbers):
  ../lecture-notes/01-bit-manipulation-and-xor-tricks.md
- LeetCode 260: https://leetcode.com/problems/single-number-iii/
"""

from __future__ import annotations

from typing import List, Tuple


def single_number_iii(nums: List[int]) -> List[int]:
    """Return the two elements that each appear once; all others appear twice.

    Implement the partition-by-a-bit technique: XOR all to get a ^ b, isolate
    one differing bit with x & -x, partition the array by that bit, and XOR
    each group to recover a and b. O(n) time, O(1) space.

    Replace the body with your solution. The signature and docstring above
    are part of the spec.
    """
    # TODO: step 1 - XOR everything to get a ^ b
    # Hint:
    #   xor_all = 0
    #   for num in nums:
    #       xor_all ^= num

    # TODO: step 2 - isolate one bit where a and b differ
    # Hint:
    #   diff_bit = xor_all & -xor_all

    # TODO: step 3 - partition by that bit; XOR one group to get `a`
    # Hint:
    #   a = 0
    #   for num in nums:
    #       if num & diff_bit:
    #           a ^= num

    # TODO: step 4 - recover `b` as xor_all ^ a; return [a, b]
    _ = nums  # silence unused-variable lint until you wire it up
    return []


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 problem-01-xor-trick-starter.py`.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a battery of asserts against single_number_iii (order-insensitive)."""
    failures = 0
    cases: List[Tuple[str, List[int], List[int]]] = [
        ("LC 260 example 1", [1, 2, 1, 3, 2, 5], [3, 5]),
        ("LC 260 example 2", [-1, 0], [-1, 0]),
        ("LC 260 example 3", [0, 1], [0, 1]),
        ("singletons far apart", [4, 4, 7, 7, 2, 9], [2, 9]),
        ("negatives", [-3, -3, -8, 5], [-8, 5]),
        ("includes zero", [0, 6, 6, 11], [0, 11]),
    ]
    for label, nums, expected in cases:
        actual = sorted(single_number_iii(nums))
        marker = "OK  " if actual == sorted(expected) else "FAIL"
        if actual != sorted(expected):
            failures += 1
            print(
                f"[{marker}] {label}: single_number_iii({nums}) -> {actual}, "
                f"expected {sorted(expected)}"
            )
        else:
            print(f"[{marker}] {label}: single_number_iii({nums}) -> {actual}")
    if failures:
        raise AssertionError(f"{failures} assertion(s) failed; implement single_number_iii.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
