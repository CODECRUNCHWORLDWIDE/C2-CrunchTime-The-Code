"""Exercise 1 - Subsets (LeetCode 78).

Pattern: combinatorial enumeration; the canonical backtracking warm-up from Lecture 1.
Difficulty: Medium.
Target solve time: 20 minutes with full UMPIRE narration.

Problem statement
-----------------
Given an integer array `nums` of unique elements, return all possible subsets
(the power set). The solution set must not contain duplicate subsets. Return
the solution in any order.

Constraints (LeetCode):
- 1 <= len(nums) <= 10.
- -10 <= nums[i] <= 10.
- All elements of nums are unique.

Examples
--------
>>> sorted(map(sorted, subsets([1, 2, 3])))
[[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. Given a list of unique integers, return every possible
        subset including the empty subset and the full input. There are
        exactly 2^n subsets for an n-element input.
- [ ] M: Combinatorial enumeration. State = (start_index, path). At each
        level, choose nums[i] for i from start to n-1, then recurse with
        start = i + 1 (no reuse). Record path at every node (not just
        leaves) because every node is a valid subset.
- [ ] P: backtrack(start) records path[:], iterates i from start to n-1,
        appends nums[i], recurses with i + 1, pops. Initial call:
        backtrack(0).
- [ ] I: Implement with the choose-explore-unchoose template; do not forget
        the deep-copy slice path[:] at the recording step.
- [ ] R: Trace nums = [1, 2, 3] by hand. Expected order under depth-first
        traversal: [], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3].
- [ ] E: O(2^n * n) time -- 2^n subsets, each requires O(n) deep-copy. O(n)
        recursion stack. Output size dominates. Trade vs. bit-enumeration:
        same asymptotic; backtracking generalizes to subsets II and
        combination sum.

References
----------
- Lecture 1, sections 1 and 2 (the template + subsets):
  ../lecture-notes/01-the-backtracking-template-and-the-three-warmups.md
- LeetCode 78: https://leetcode.com/problems/subsets/
- Backtracking on Wikipedia: https://en.wikipedia.org/wiki/Backtracking
"""

from __future__ import annotations

from typing import List, Tuple


def subsets(nums: List[int]) -> List[List[int]]:
    """Return all 2^n subsets of nums in any order.

    The harness passes `nums` as a list of unique integers. The output must
    contain every subset exactly once, including the empty subset and the
    full input. Order of subsets and order of elements within each subset
    is unconstrained by LeetCode.

    Replace the body with your solution. The signature and docstring above
    are part of the spec.
    """
    # TODO: implement the choose-explore-unchoose template.
    # Hint:
    #   result: List[List[int]] = []
    #   path: List[int] = []
    #   def backtrack(start: int) -> None:
    #       result.append(path[:])      # every node is a valid subset
    #       for i in range(start, len(nums)):
    #           path.append(nums[i])    # CHOOSE
    #           backtrack(i + 1)        # RECURSE
    #           path.pop()              # UNCHOOSE
    #   backtrack(0)
    #   return result
    _ = nums  # silence unused-variable lint until you wire it up
    return []


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 exercise-01-subsets.py`.
# ---------------------------------------------------------------------------


def _canonicalize(result: List[List[int]]) -> List[Tuple[int, ...]]:
    """Sort each subset and the list of subsets for order-independent comparison."""
    return sorted(tuple(sorted(s)) for s in result)


def _run_self_tests() -> None:
    """Run a battery of asserts against the subsets function."""
    failures = 0

    # Case 1: LC 78 example 1.
    actual = _canonicalize(subsets([1, 2, 3]))
    expected = _canonicalize(
        [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
    )
    label = "LC 78 example 1 (nums=[1,2,3])"
    if actual == expected:
        print(f"[OK  ] {label}: 8 subsets")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {actual}, expected {expected}")

    # Case 2: LC 78 example 2 (singleton).
    actual = _canonicalize(subsets([0]))
    expected = _canonicalize([[], [0]])
    label = "LC 78 example 2 (nums=[0])"
    if actual == expected:
        print(f"[OK  ] {label}: 2 subsets")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {actual}, expected {expected}")

    # Case 3: empty input is outside LC 78 constraints; we still test it.
    actual = subsets([])
    expected_count = 1
    label = "edge case (nums=[])"
    if len(actual) == expected_count and actual[0] == []:
        print(f"[OK  ] {label}: 1 subset (the empty set)")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {actual}, expected [[]]")

    # Case 4: four-element input. 2^4 = 16 subsets.
    actual = _canonicalize(subsets([1, 2, 3, 4]))
    label = "four-element (nums=[1,2,3,4])"
    if len(actual) == 16 and len(set(actual)) == 16:
        print(f"[OK  ] {label}: 16 distinct subsets")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {len(actual)} subsets, expected 16 distinct")

    # Case 5: LC 78 max-size input (n=10). 2^10 = 1024 subsets.
    actual = _canonicalize(subsets(list(range(10))))
    label = "max-size LC input (nums=[0..9])"
    if len(actual) == 1024 and len(set(actual)) == 1024:
        print(f"[OK  ] {label}: 1024 distinct subsets")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {len(actual)} subsets, expected 1024 distinct")

    # Case 6: negative numbers should be handled normally.
    actual = _canonicalize(subsets([-1, 0, 1]))
    expected = _canonicalize(
        [[], [-1], [0], [1], [-1, 0], [-1, 1], [0, 1], [-1, 0, 1]]
    )
    label = "negatives (nums=[-1,0,1])"
    if actual == expected:
        print(f"[OK  ] {label}: 8 subsets")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {actual}, expected {expected}")

    if failures:
        raise AssertionError(f"{failures} assertion(s) failed; implement subsets.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
