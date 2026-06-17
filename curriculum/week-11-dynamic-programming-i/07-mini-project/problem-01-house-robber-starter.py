"""Mini-Project Problem 1 - House Robber (LeetCode 198).

Pattern: 1D optimization DP; the canonical take-or-skip recurrence from
Lecture 1 sections 2 and 5.
Difficulty: Medium.
Target solve time: 4 hours including the full UMPIRE write-up.

Problem statement
-----------------
You are a professional robber planning to rob houses along a street. Each
house has a certain amount of money stashed; the only constraint is that
adjacent houses have security systems that will automatically contact the
police if both are robbed on the same night.

Given an integer array `nums` representing the amount of money at each
house, return the maximum amount of money you can rob tonight without
alerting the police.

Constraints (LeetCode):
- 1 <= len(nums) <= 100.
- 0 <= nums[i] <= 400.

Examples
--------
>>> rob_memoized([1, 2, 3, 1])
4
>>> rob_tabulated([2, 7, 9, 3, 1])
12
>>> rob_memoized([2, 1, 1, 2])
4

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. Given a list of house values, return the maximum total
        value selecting a subset such that no two adjacent indices are
        both selected. Confirm: nums is non-empty (LC guarantees).
- [ ] M: 1D optimization DP. State = "max loot considering houses 0..i."
        Recurrence: dp[i] = max(dp[i-1], dp[i-2] + nums[i]).
        Two triggers: overlapping subproblems and optimal substructure.
        Why not greedy: the locally optimal house (largest) does not
        extend globally. Counter-example: [2, 7, 9, 3, 1] -- greedy by
        largest picks 9, then must skip 7 and 3, can take 1 -> 10. The
        optimum is 2 + 9 + 1 = 12.
- [ ] P: Both implementations follow the four-step pipeline.
        Memoized: write the recursion, decorate with @lru_cache.
        Tabulated: build dp[] array; dp[0] = nums[0]; dp[1] = max(nums[0],
        nums[1]); loop i from 2 to n - 1.
- [ ] I: Type hints on every function; docstring on every function.
        For the memoized form, the function must take a Tuple[int, ...]
        because @lru_cache requires hashable arguments.
- [ ] R: Trace nums = [2, 7, 9, 3, 1]:
        dp[0] = 2, dp[1] = max(2, 7) = 7
        dp[2] = max(dp[1], dp[0] + 9) = max(7, 11) = 11
        dp[3] = max(dp[2], dp[1] + 3) = max(11, 10) = 11
        dp[4] = max(dp[3], dp[2] + 1) = max(11, 12) = 12. Correct.
- [ ] E: O(n) time, O(n) space for memoized (cache + stack);
        O(n) time, O(1) space for tabulated with rolling pair.

References
----------
- Lecture 1, sections 2 and 5 (the pipeline + house robber):
  ../lecture-notes/01-the-dp-pipeline-and-1d-states.md
- LeetCode 198: https://leetcode.com/problems/house-robber/
- Python functools.lru_cache: https://docs.python.org/3/library/functools.html#functools.lru_cache
"""

from __future__ import annotations

import functools
from typing import List, Tuple


# ---------------------------------------------------------------------------
# Implementation 1: top-down memoization with functools.lru_cache.
# ---------------------------------------------------------------------------


def rob_memoized(nums: List[int]) -> int:
    """Maximum loot from a list of houses via top-down memoization.

    The four-step pipeline calls this Step 2: write the recursion, decorate
    with @lru_cache. The outer function converts the list to a hashable
    tuple and invokes the inner cached helper.

    Replace the body of the inner helper. The outer wrapper is provided.
    """
    nums_tuple: Tuple[int, ...] = tuple(nums)

    @functools.lru_cache(maxsize=None)
    def rob_at(i: int) -> int:
        """Maximum loot considering houses 0..i (inclusive). i may be negative."""
        # TODO: handle the base case (i < 0 -> no houses left -> 0)
        # Hint:
        #   if i < 0:
        #       return 0

        # TODO: handle the i == 0 base case (single house)
        # Hint:
        #   if i == 0:
        #       return nums_tuple[0]

        # TODO: return max(skip, take) per the recurrence
        # Hint:
        #   return max(rob_at(i - 1), rob_at(i - 2) + nums_tuple[i])
        _ = i, nums_tuple
        return 0

    return rob_at(len(nums) - 1)


# ---------------------------------------------------------------------------
# Implementation 2: bottom-up tabulation with rolling-pair space reduction.
# ---------------------------------------------------------------------------


def rob_tabulated(nums: List[int]) -> int:
    """Maximum loot from a list of houses via bottom-up tabulation.

    The four-step pipeline calls this Steps 3 and 4: write the table, then
    reduce to a rolling pair. O(n) time, O(1) space.

    Replace the body. The signature and docstring are part of the spec.
    """
    # TODO: handle empty input (defensively, even though LC guarantees non-empty)
    # Hint:
    #   if not nums:
    #       return 0

    # TODO: initialize the rolling pair
    # Hint:
    #   prev2, prev1 = 0, 0

    # TODO: iterate through nums, updating the rolling pair
    # Hint:
    #   for num in nums:
    #       prev2, prev1 = prev1, max(prev1, prev2 + num)

    # TODO: return prev1
    _ = nums
    return 0


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 problem-01-house-robber-starter.py`.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a battery of asserts against both implementations."""
    failures = 0
    cases: List[Tuple[str, List[int], int]] = [
        ("LC 198 example 1", [1, 2, 3, 1], 4),
        ("LC 198 example 2", [2, 7, 9, 3, 1], 12),
        ("single house", [5], 5),
        ("two houses", [5, 10], 10),
        ("all zeros", [0, 0, 0, 0], 0),
        ("alternating large/small", [10, 1, 10, 1, 10], 30),
        ("descending", [9, 5, 3, 1], 12),
        ("ascending", [1, 3, 5, 7, 9], 15),  # 1 + 5 + 9
        ("greedy trap", [2, 1, 1, 2], 4),     # 2 + 2 = 4, not 1 + 1 = 2
    ]
    for label, nums, expected in cases:
        for impl_name, impl in (("memoized", rob_memoized), ("tabulated", rob_tabulated)):
            actual = impl(nums)
            marker = "OK  " if actual == expected else "FAIL"
            if actual != expected:
                failures += 1
                print(
                    f"[{marker}] {impl_name} {label}: rob({nums}) -> {actual}, expected {expected}"
                )
            else:
                print(f"[{marker}] {impl_name} {label}: rob({nums}) -> {actual}")
    if failures:
        raise AssertionError(
            f"{failures} assertion(s) failed; implement rob_memoized and rob_tabulated."
        )
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
