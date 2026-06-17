"""Exercise 3 - Counting Bits (LeetCode 338).

Pattern: bit manipulation meets dynamic programming; the 1D DP over bits
from Lecture 2 section 4.
Difficulty: Easy/Medium.
Target solve time: 25 minutes with full UMPIRE narration.

Problem statement
-----------------
Given an integer `n`, return an array `ans` of length `n + 1` such that for
each `i` (0 <= i <= n), `ans[i]` is the number of 1s in the binary
representation of `i`.

Constraints (LeetCode):
- 0 <= n <= 10^5.
Follow-up: solve it in O(n) time and without built-in popcount functions.

Examples
--------
>>> count_bits(2)
[0, 1, 1]
>>> count_bits(5)
[0, 1, 1, 2, 1, 2]

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. For every i in 0..n, count its set bits and return the
        list. Confirm: the output length is n + 1 (indices 0 through n).
- [ ] M: 1D DP over bits. The number of set bits in i equals the number in
        (i >> 1) plus the low bit (i & 1): right-shifting drops the lowest
        bit, and dp[i >> 1] is already computed since i >> 1 < i. Recurrence:
        dp[i] = dp[i >> 1] + (i & 1). Why not popcount-each: that is
        O(n log n); this DP is O(n) by reusing subproblems (Week 11 discipline
        applied to bits).
- [ ] P: dp = [0] * (n + 1). dp[0] = 0 (base case, zero-init). Loop i from 1
        to n: dp[i] = dp[i >> 1] + (i & 1). Return dp.
- [ ] I: O(n) time, O(n) output. Type hints; docstring. Do not call
        bin().count or int.bit_count - the follow-up forbids them and the
        DP is the lesson.
- [ ] R: Trace n = 5:
        dp[0]=0; dp[1]=dp[0]+1=1; dp[2]=dp[1]+0=1; dp[3]=dp[1]+1=2;
        dp[4]=dp[2]+0=1; dp[5]=dp[2]+1=2. -> [0,1,1,2,1,2].
- [ ] E: O(n) time, O(n) space (the output). The DP reuses dp[i >> 1], so
        each entry is O(1) work. Beats popcount-each (O(n log n)).

References
----------
- Lecture 2, section 4 (the 1D DP over bits):
  ../lecture-notes/02-bitmasks-bitmask-dp-and-tries-at-speed.md
- LeetCode 338: https://leetcode.com/problems/counting-bits/
"""

from __future__ import annotations

from typing import List, Tuple


def count_bits(n: int) -> List[int]:
    """Return [popcount(i) for i in range(n + 1)] in O(n) time.

    Implement with the 1D DP: dp[i] = dp[i >> 1] + (i & 1). Do not use
    bin().count("1") or int.bit_count() - the follow-up forbids the built-in
    popcount, and reusing subproblems is the lesson.

    Replace the body with your solution. The signature and docstring above
    are part of the spec.
    """
    # TODO: allocate the dp array of length n + 1 (dp[0] = 0 by zero-init)
    # Hint:
    #   dp = [0] * (n + 1)

    # TODO: fill via the recurrence
    # Hint:
    #   for i in range(1, n + 1):
    #       dp[i] = dp[i >> 1] + (i & 1)
    #   return dp
    _ = n  # silence unused-variable lint until you wire it up
    return []


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 exercise-03-counting-bits.py`.
# ---------------------------------------------------------------------------


def _reference_popcount_list(n: int) -> List[int]:
    """Independent reference using bin().count for cross-checking only."""
    return [bin(i).count("1") for i in range(n + 1)]


def _run_self_tests() -> None:
    """Run the LC 338 examples plus a cross-check against a reference."""
    failures = 0
    cases: List[Tuple[str, int, List[int]]] = [
        ("LC 338 example 1 (n=2)", 2, [0, 1, 1]),
        ("LC 338 example 2 (n=5)", 5, [0, 1, 1, 2, 1, 2]),
        ("n=0 edge", 0, [0]),
        ("n=1", 1, [0, 1]),
        ("n=8", 8, [0, 1, 1, 2, 1, 2, 2, 3, 1]),
    ]
    for label, n, expected in cases:
        actual = count_bits(n)
        marker = "OK  " if actual == expected else "FAIL"
        if actual != expected:
            failures += 1
            print(f"[{marker}] {label}: count_bits({n}) -> {actual}, expected {expected}")
        else:
            print(f"[{marker}] {label}: count_bits({n}) -> {actual}")

    # Cross-check against an independent reference for a larger n.
    big = 1000
    if count_bits(big) != _reference_popcount_list(big):
        failures += 1
        print(f"[FAIL] cross-check n={big}: output disagrees with reference popcount")
    else:
        print(f"[OK  ] cross-check n={big}: matches reference popcount")

    if failures:
        raise AssertionError(f"{failures} assertion(s) failed; implement count_bits.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
