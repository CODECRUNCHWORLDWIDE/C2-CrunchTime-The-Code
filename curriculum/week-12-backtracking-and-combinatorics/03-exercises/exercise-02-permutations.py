"""Exercise 2 - Permutations (LeetCode 46).

Pattern: combinatorial enumeration with a `used` set; the canonical second
backtracking from Lecture 1.
Difficulty: Medium.
Target solve time: 20 minutes with full UMPIRE narration.

Problem statement
-----------------
Given an array `nums` of distinct integers, return all the possible
permutations. You can return the answer in any order.

Constraints (LeetCode):
- 1 <= len(nums) <= 6.
- -10 <= nums[i] <= 10.
- All integers of nums are unique.

Examples
--------
>>> sorted(permute([1, 2, 3]))
[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. Given a list of distinct integers, return every ordering
        of every element. There are exactly n! permutations of an
        n-element input.
- [ ] M: Combinatorial enumeration where order matters. State =
        (used_set, path). At each level, iterate every index 0..n-1; skip
        indices already in `used`; choose, recurse, unchoose. Record path
        at leaves only (len(path) == n).
- [ ] P: backtrack() records path[:] at leaves; otherwise iterates i from
        0 to n-1, skips if i in used, marks used, appends nums[i],
        recurses, unmarks, pops.
- [ ] I: Implement with both mutations on choose (used.add, path.append)
        and both on unchoose (path.pop, used.remove). Do not forget the
        deep-copy at the leaf.
- [ ] R: Trace nums = [1, 2, 3] by hand. Expected 6 permutations under
        depth-first traversal.
- [ ] E: O(n! * n) time -- n! permutations, each O(n) to deep-copy. O(n)
        recursion stack plus O(n) used set. Output size dominates.
        Trade vs. itertools.permutations: same asymptotic; backtracking
        generalizes to permutations II (duplicates) and N-Queens.

References
----------
- Lecture 1, section 3 (permutations):
  ../lecture-notes/01-the-backtracking-template-and-the-three-warmups.md
- LeetCode 46: https://leetcode.com/problems/permutations/
- itertools.permutations:
  https://docs.python.org/3/library/itertools.html#itertools.permutations
"""

from __future__ import annotations

import math
from typing import List, Tuple


def permute(nums: List[int]) -> List[List[int]]:
    """Return all n! permutations of nums.

    The harness passes `nums` as a list of distinct integers. The output
    must contain every permutation exactly once. Order of permutations
    is unconstrained by LeetCode.

    Replace the body with your solution. The signature and docstring above
    are part of the spec.
    """
    # TODO: implement the choose-explore-unchoose template with a used set.
    # Hint:
    #   result: List[List[int]] = []
    #   path: List[int] = []
    #   used: set[int] = set()
    #   def backtrack() -> None:
    #       if len(path) == len(nums):
    #           result.append(path[:])
    #           return
    #       for i in range(len(nums)):
    #           if i in used:
    #               continue
    #           used.add(i)
    #           path.append(nums[i])
    #           backtrack()
    #           path.pop()
    #           used.remove(i)
    #   backtrack()
    #   return result
    _ = nums  # silence unused-variable lint until you wire it up
    return []


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 exercise-02-permutations.py`.
# ---------------------------------------------------------------------------


def _canonicalize(result: List[List[int]]) -> List[Tuple[int, ...]]:
    """Convert to a sorted list of tuples for order-independent comparison."""
    return sorted(tuple(p) for p in result)


def _run_self_tests() -> None:
    """Run a battery of asserts against the permute function."""
    failures = 0

    # Case 1: LC 46 example 1.
    actual = _canonicalize(permute([1, 2, 3]))
    expected = _canonicalize(
        [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    )
    label = "LC 46 example 1 (nums=[1,2,3])"
    if actual == expected:
        print(f"[OK  ] {label}: 6 permutations")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {actual}, expected {expected}")

    # Case 2: LC 46 example 2 (pair).
    actual = _canonicalize(permute([0, 1]))
    expected = _canonicalize([[0, 1], [1, 0]])
    label = "LC 46 example 2 (nums=[0,1])"
    if actual == expected:
        print(f"[OK  ] {label}: 2 permutations")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {actual}, expected {expected}")

    # Case 3: LC 46 example 3 (singleton).
    actual = _canonicalize(permute([1]))
    expected = _canonicalize([[1]])
    label = "LC 46 example 3 (nums=[1])"
    if actual == expected:
        print(f"[OK  ] {label}: 1 permutation")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {actual}, expected {expected}")

    # Case 4: four-element input. 4! = 24 permutations.
    actual = _canonicalize(permute([1, 2, 3, 4]))
    label = "four-element (nums=[1,2,3,4])"
    if len(actual) == 24 and len(set(actual)) == 24:
        print(f"[OK  ] {label}: 24 distinct permutations")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {len(actual)}, expected 24 distinct")

    # Case 5: LC 46 max-size input (n=6). 6! = 720 permutations.
    actual = _canonicalize(permute([1, 2, 3, 4, 5, 6]))
    label = "max-size LC input (nums=[1..6])"
    if len(actual) == math.factorial(6) and len(set(actual)) == math.factorial(6):
        print(f"[OK  ] {label}: 720 distinct permutations")
    else:
        failures += 1
        print(
            f"[FAIL] {label}: got {len(actual)}, expected {math.factorial(6)} distinct"
        )

    # Case 6: negatives.
    actual = _canonicalize(permute([-1, 0, 1]))
    expected = _canonicalize(
        [[-1, 0, 1], [-1, 1, 0], [0, -1, 1], [0, 1, -1], [1, -1, 0], [1, 0, -1]]
    )
    label = "negatives (nums=[-1,0,1])"
    if actual == expected:
        print(f"[OK  ] {label}: 6 permutations")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {actual}, expected {expected}")

    if failures:
        raise AssertionError(f"{failures} assertion(s) failed; implement permute.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
