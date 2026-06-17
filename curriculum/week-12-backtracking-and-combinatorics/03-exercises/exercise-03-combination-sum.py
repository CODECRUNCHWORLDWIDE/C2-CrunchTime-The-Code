"""Exercise 3 - Combination Sum (LeetCode 39).

Pattern: backtracking with sum-based pruning; the canonical "sort + break"
optimization from Lecture 2.
Difficulty: Medium.
Target solve time: 30 minutes with full UMPIRE narration.

Problem statement
-----------------
Given an array of distinct integers `candidates` and a target integer
`target`, return a list of all unique combinations of `candidates` where
the chosen numbers sum to `target`. You may return the combinations in
any order. The same number may be chosen from `candidates` an unlimited
number of times. Two combinations are unique if the frequency of at
least one of the chosen numbers is different.

Constraints (LeetCode):
- 1 <= len(candidates) <= 30.
- 2 <= candidates[i] <= 40.
- All elements of candidates are distinct.
- 1 <= target <= 40.

Examples
--------
>>> sorted(combination_sum([2, 3, 6, 7], 7))
[[2, 2, 3], [7]]
>>> sorted(combination_sum([2, 3, 5], 8))
[[2, 2, 2, 2], [2, 3, 3], [3, 5]]

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. Given distinct positive integers and a positive target,
        return every multiset (combination with repetition allowed) of
        candidates summing to target. Order within each multiset is
        non-decreasing (by sorting candidates first); order of multisets
        in the output is unconstrained.
- [ ] M: Backtracking with reuse and sum-based pruning. State =
        (start_index, remaining_target, path). Reuse rule: recurse with
        start = i (not i + 1). Pruning: sort candidates, break loop on
        candidates[i] > remaining.
- [ ] P: Sort candidates first. backtrack(start, remaining) records
        path[:] when remaining == 0; otherwise iterates i from start,
        breaks if candidates[i] > remaining, chooses, recurses with
        (i, remaining - candidates[i]), unchooses.
- [ ] I: Sort first; the prune depends on monotonicity. Reuse means
        recurse with i, not i + 1. Do not forget the deep-copy at the
        record step.
- [ ] R: Trace candidates = [2, 3, 6, 7], target = 7. Expected:
        [[2, 2, 3], [7]] (two combinations).
- [ ] E: Time is hard to bound tightly. Loose worst case
        O(N^(target / min_candidate)) where N = len(candidates).
        Space is O(target / min_candidate) for the recursion stack and
        path. The sort plus break cuts the constant by ~10-100x.

References
----------
- Lecture 2, section 1 (combination sum + sum-based pruning):
  ../lecture-notes/02-pruning-and-deduplication-and-string-partitioning.md
- LeetCode 39: https://leetcode.com/problems/combination-sum/
"""

from __future__ import annotations

from typing import List, Tuple


def combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    """Return all combinations of candidates summing to target (reuse allowed).

    The harness passes `candidates` as a list of distinct positive integers
    and `target` as a positive integer. The output must contain every
    multiset of candidates summing to target exactly once.

    Replace the body with your solution. The signature and docstring above
    are part of the spec.
    """
    # TODO: implement the backtracking with sort-plus-break pruning.
    # Hint:
    #   candidates.sort()
    #   result: List[List[int]] = []
    #   path: List[int] = []
    #   def backtrack(start: int, remaining: int) -> None:
    #       if remaining == 0:
    #           result.append(path[:])
    #           return
    #       for i in range(start, len(candidates)):
    #           if candidates[i] > remaining:
    #               break
    #           path.append(candidates[i])
    #           backtrack(i, remaining - candidates[i])    # reuse: i, not i + 1
    #           path.pop()
    #   backtrack(0, target)
    #   return result
    _ = candidates  # silence unused-variable lint
    _ = target
    return []


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 exercise-03-combination-sum.py`.
# ---------------------------------------------------------------------------


def _canonicalize(result: List[List[int]]) -> List[Tuple[int, ...]]:
    """Sort each multiset and the list of multisets for order-independent comparison."""
    return sorted(tuple(sorted(c)) for c in result)


def _run_self_tests() -> None:
    """Run a battery of asserts against the combination_sum function."""
    failures = 0

    # Case 1: LC 39 example 1.
    actual = _canonicalize(combination_sum([2, 3, 6, 7], 7))
    expected = _canonicalize([[2, 2, 3], [7]])
    label = "LC 39 example 1 (cand=[2,3,6,7], target=7)"
    if actual == expected:
        print(f"[OK  ] {label}: 2 combinations")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {actual}, expected {expected}")

    # Case 2: LC 39 example 2.
    actual = _canonicalize(combination_sum([2, 3, 5], 8))
    expected = _canonicalize([[2, 2, 2, 2], [2, 3, 3], [3, 5]])
    label = "LC 39 example 2 (cand=[2,3,5], target=8)"
    if actual == expected:
        print(f"[OK  ] {label}: 3 combinations")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {actual}, expected {expected}")

    # Case 3: LC 39 example 3 (no combinations).
    actual = combination_sum([2], 1)
    expected: List[List[int]] = []
    label = "LC 39 example 3 (cand=[2], target=1)"
    if _canonicalize(actual) == _canonicalize(expected):
        print(f"[OK  ] {label}: 0 combinations")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {actual}, expected {expected}")

    # Case 4: single candidate equal to target.
    actual = _canonicalize(combination_sum([5], 5))
    expected = _canonicalize([[5]])
    label = "single = target (cand=[5], target=5)"
    if actual == expected:
        print(f"[OK  ] {label}: 1 combination")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {actual}, expected {expected}")

    # Case 5: candidate dividing target.
    actual = _canonicalize(combination_sum([3], 9))
    expected = _canonicalize([[3, 3, 3]])
    label = "divisor (cand=[3], target=9)"
    if actual == expected:
        print(f"[OK  ] {label}: 1 combination")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {actual}, expected {expected}")

    # Case 6: every candidate larger than target.
    actual = combination_sum([10, 20, 30], 5)
    label = "all too large (cand=[10,20,30], target=5)"
    if actual == []:
        print(f"[OK  ] {label}: 0 combinations")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {actual}, expected []")

    # Case 7: unsorted input must still work.
    actual = _canonicalize(combination_sum([7, 2, 6, 3], 7))
    expected = _canonicalize([[2, 2, 3], [7]])
    label = "unsorted (cand=[7,2,6,3], target=7)"
    if actual == expected:
        print(f"[OK  ] {label}: 2 combinations")
    else:
        failures += 1
        print(
            f"[FAIL] {label}: got {actual}, expected {expected} -- "
            "did you sort candidates inside the function?"
        )

    # Case 8: small case with many combinations.
    actual = _canonicalize(combination_sum([2, 3, 4, 5], 10))
    expected = _canonicalize([
        [2, 2, 2, 2, 2],
        [2, 2, 2, 4],
        [2, 2, 3, 3],
        [2, 3, 5],
        [2, 4, 4],
        [3, 3, 4],
        [5, 5],
    ])
    label = "rich (cand=[2,3,4,5], target=10)"
    if actual == expected:
        print(f"[OK  ] {label}: 7 combinations")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {actual}, expected {expected}")

    if failures:
        raise AssertionError(
            f"{failures} assertion(s) failed; implement combination_sum."
        )
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
