"""Exercise 2 — Counting Bits (LeetCode 338).

Pattern: bit DP.

PROBLEM
-------
Given an integer `n`, return an array `ans` of length `n + 1` such that for
each i (0 <= i <= n), ans[i] is the number of 1 bits in the binary
representation of i.

FOLLOW-UP
---------
Solve it in a single pass, in O(n) time, without calling a built-in popcount
per element.

CONSTRAINTS
-----------
- 0 <= n <= 10**5

EXAMPLES
--------
- count_bits(2) -> [0, 1, 1]
      0 -> 0b0  (0 ones)
      1 -> 0b1  (1 one)
      2 -> 0b10 (1 one)
- count_bits(5) -> [0, 1, 1, 2, 1, 2]

FRAME CHECKLIST
----------------
- Frame: for each i in 0..n, store popcount(i) at index i.
- Research constraints: the naive per-element popcount is O(n log n); the
  follow-up wants O(n). That points at bit DP. Recurrence
  dp[i] = dp[i >> 1] + (i & 1): i >> 1 drops the low bit (== i // 2), whose
  count is already computed; i & 1 adds the dropped bit back.
  (Equivalent recurrence: dp[i] = dp[i & (i - 1)] + 1.)
- Assess options: allocate dp = [0] * (n + 1); fill i = 1..n with the
  recurrence; dp[0] = 0 is correct by initialization.
- Make the solution: see below.
- Examine (verify): trace n = 5 -> [0, 1, 1, 2, 1, 2]; check n = 0 -> [0].
- Examine (cost): O(n) time (O(1) per index; dp[i >> 1] is always already
  filled), O(n) output space.
"""

from typing import List


def count_bits(n: int) -> List[int]:
    """Return [popcount(0), popcount(1), ..., popcount(n)] in O(n) time."""
    # TODO: allocate dp of length n + 1 and fill it with
    #       dp[i] = dp[i >> 1] + (i & 1) for i in 1..n.
    raise NotImplementedError


if __name__ == "__main__":
    assert count_bits(0) == [0]
    assert count_bits(1) == [0, 1]
    assert count_bits(2) == [0, 1, 1]
    assert count_bits(5) == [0, 1, 1, 2, 1, 2]
    # Cross-check against the built-in popcount for a larger range.
    assert count_bits(50) == [i.bit_count() for i in range(51)]
    print("exercise-02-counting-bits: all tests passed")
