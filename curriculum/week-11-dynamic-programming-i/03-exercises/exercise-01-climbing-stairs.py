"""Exercise 1 - Climbing Stairs (LeetCode 70).

Pattern: 1D counting DP; the canonical Fibonacci-shaped warm-up from Lecture 1.
Difficulty: Easy.
Target solve time: 20 minutes with full UMPIRE narration.

Problem statement
-----------------
You are climbing a staircase. It takes `n` steps to reach the top. Each time
you can either climb 1 or 2 steps. In how many distinct ways can you climb
to the top?

Constraints (LeetCode):
- 1 <= n <= 45.

Examples
--------
>>> climb_stairs(2)
2
>>> climb_stairs(3)
3
>>> climb_stairs(5)
8

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. Given an integer n, count distinct ways to reach step n
        using 1-step and 2-step moves. Verify n >= 1 (no zero-step case
        in the constraint).
- [ ] M: 1D counting DP. State = "number of ways to reach step i."
        Recurrence: dp[i] = dp[i-1] + dp[i-2] (one-step from i-1 or
        two-step from i-2). Overlapping subproblems + optimal substructure.
        Why not brute-force recursion: O(2^n); for n = 45, ~3.5e13 calls.
- [ ] P: Base cases: dp[1] = 1, dp[2] = 2. Iterate i from 3 to n.
        Return dp[n].
- [ ] I: Choose tabulation with rolling-pair reduction. O(n) time, O(1) space.
- [ ] R: Trace n = 5 by hand: 1, 2, 3, 5, 8. Confirm Fibonacci sequence.
- [ ] E: O(n) time, O(1) space with rolling pair. Trade vs. naive recursion:
        O(2^n) vs. O(n). Trade vs. memoization: same O(n) time but O(n)
        space and recursion stack; tabulation strictly dominates.

References
----------
- Lecture 1, sections 2 and 4 (the pipeline + climbing stairs):
  ../lecture-notes/01-the-dp-pipeline-and-1d-states.md
- LeetCode 70: https://leetcode.com/problems/climbing-stairs/
- Python functools docs: https://docs.python.org/3/library/functools.html
"""

from __future__ import annotations

from typing import List, Tuple


def climb_stairs(n: int) -> int:
    """Return the number of distinct ways to climb n stairs using 1- or 2-steps.

    The harness passes `n` as a positive integer (LeetCode guarantees n >= 1).
    Implement with the rolling-pair form for O(1) space. The full four-step
    pipeline (naive recursion -> memoize -> tabulate -> rolling pair) is
    walked in Lecture 1 section 4 if you want to start from step 1.

    Replace the body with your solution. The signature and docstring above
    are part of the spec.
    """
    # TODO: handle the base cases (n == 1 or n == 2)
    # Hint:
    #   if n <= 2:
    #       return n

    # TODO: implement the rolling-pair recurrence
    # Hint:
    #   prev2, prev1 = 1, 2
    #   for _ in range(3, n + 1):
    #       prev2, prev1 = prev1, prev2 + prev1
    #   return prev1
    _ = n  # silence unused-variable lint until you wire it up
    return 0


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 exercise-01-climbing-stairs.py`.
# Also discovered by `pytest`.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a battery of asserts against the climb_stairs function.

    When the function is unimplemented (returns 0 always), most asserts
    will fail loudly -- that is the signal to implement.
    """
    failures = 0
    cases: List[Tuple[str, int, int]] = [
        ("LC 70 example 1 (n=2)", 2, 2),
        ("LC 70 example 2 (n=3)", 3, 3),
        ("n=1 base", 1, 1),
        ("n=4", 4, 5),
        ("n=5 (the canonical trace)", 5, 8),
        ("n=10", 10, 89),
        ("n=20", 20, 10946),
        ("n=45 (LC max constraint)", 45, 1836311903),
    ]
    for label, n, expected in cases:
        actual = climb_stairs(n)
        marker = "OK  " if actual == expected else "FAIL"
        if actual != expected:
            failures += 1
            print(
                f"[{marker}] {label}: climb_stairs({n}) -> {actual}, expected {expected}"
            )
        else:
            print(f"[{marker}] {label}: climb_stairs({n}) -> {actual}")
    if failures:
        raise AssertionError(f"{failures} assertion(s) failed; implement climb_stairs.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
