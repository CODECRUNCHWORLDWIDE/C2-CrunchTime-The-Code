"""Mini-project Problem 1 - Palindrome Partitioning (LeetCode 131).

Pattern: backtracking with string-partition state and palindrome-check
constraint-propagation prune. See Lecture 2 section 4.

Problem statement
-----------------
Given a string `s`, partition `s` such that every substring of the partition
is a palindrome. Return all possible palindrome partitionings of `s`.

Constraints (LeetCode):
- 1 <= len(s) <= 16.
- s contains only lowercase English letters.

Examples
--------
>>> sorted(map(tuple, partition("aab")))
[('a', 'a', 'b'), ('aa', 'b')]
>>> sorted(map(tuple, partition("a")))
[('a',)]

UMPIRE checklist
----------------
- [ ] U: Restate. Partition s into pieces such that every piece is a
        palindrome; return every such partition. The single-character
        partition ([s[0], s[1], ..., s[n-1]]) is always valid because every
        single character is a palindrome.
- [ ] M: Backtracking with string-partition state. State =
        (start_index, path). At each level, try every end > start;
        if s[start:end] is a palindrome, choose, recurse with start = end,
        unchoose. Record path[:] at leaves where start == n.
- [ ] P: backtrack(0). For each end from start + 1 to n, check palindrome,
        choose s[start:end], recurse(end), unchoose.
- [ ] I: Use a helper is_palindrome(left, right) that checks s[left:right + 1]
        in O(right - left + 1) two-pointer style.
- [ ] R: Trace s = "aab" by hand. Expected: [["a", "a", "b"], ["aa", "b"]].
- [ ] E: Worst-case time O(N * 2^N) - 2^(N-1) possible partitions of length-N
        string, each requiring O(N) palindrome checks. Space O(N) for
        recursion plus output. The precomputed palindrome table optimization
        is O(N^2) extra space for O(1) per check; net win only for large N.

References
----------
- Lecture 2, section 4 (palindrome partitioning):
  ../lecture-notes/02-pruning-and-deduplication-and-string-partitioning.md
- LeetCode 131: https://leetcode.com/problems/palindrome-partitioning/
"""

from __future__ import annotations

from typing import List, Tuple


def partition(s: str) -> List[List[str]]:
    """Return all palindrome partitions of s.

    The harness passes `s` as a lowercase ASCII string of length 1..16.
    The output must contain every valid partition exactly once. Order of
    partitions is unconstrained; order of pieces within each partition is
    fixed by their left-to-right position in s.

    Replace the body with your solution. The signature and docstring above
    are part of the spec.
    """
    # TODO: implement the choose-explore-unchoose template with palindrome prune.
    # Hint:
    #   n = len(s)
    #   result: List[List[str]] = []
    #   path: List[str] = []
    #
    #   def is_palindrome(left: int, right: int) -> bool:
    #       while left < right:
    #           if s[left] != s[right]:
    #               return False
    #           left += 1
    #           right -= 1
    #       return True
    #
    #   def backtrack(start: int) -> None:
    #       if start == n:
    #           result.append(path[:])
    #           return
    #       for end in range(start + 1, n + 1):
    #           if not is_palindrome(start, end - 1):
    #               continue
    #           path.append(s[start:end])
    #           backtrack(end)
    #           path.pop()
    #
    #   backtrack(0)
    #   return result
    _ = s  # silence unused-variable lint
    return []


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 problem-01-palindrome-partitioning-starter.py`.
# ---------------------------------------------------------------------------


def _canonicalize(result: List[List[str]]) -> List[Tuple[str, ...]]:
    """Convert to a sorted list of tuples for order-independent comparison."""
    return sorted(tuple(p) for p in result)


def _run_self_tests() -> None:
    """Run a battery of asserts against the partition function."""
    failures = 0

    # Case 1: LC 131 example 1.
    actual = _canonicalize(partition("aab"))
    expected = _canonicalize([["a", "a", "b"], ["aa", "b"]])
    label = 'LC 131 example 1 (s="aab")'
    if actual == expected:
        print(f"[OK  ] {label}: 2 partitions")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {actual}, expected {expected}")

    # Case 2: LC 131 example 2.
    actual = _canonicalize(partition("a"))
    expected = _canonicalize([["a"]])
    label = 'LC 131 example 2 (s="a")'
    if actual == expected:
        print(f"[OK  ] {label}: 1 partition")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {actual}, expected {expected}")

    # Case 3: full palindrome.
    actual = _canonicalize(partition("abba"))
    expected = _canonicalize([
        ["a", "b", "b", "a"],
        ["a", "bb", "a"],
        ["abba"],
    ])
    label = 'full palindrome (s="abba")'
    if actual == expected:
        print(f"[OK  ] {label}: 3 partitions")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {actual}, expected {expected}")

    # Case 4: all distinct characters - only the singleton partition.
    actual = _canonicalize(partition("abcd"))
    expected = _canonicalize([["a", "b", "c", "d"]])
    label = 'all distinct (s="abcd")'
    if actual == expected:
        print(f"[OK  ] {label}: 1 partition")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {actual}, expected {expected}")

    # Case 5: all same character.
    actual = _canonicalize(partition("aaa"))
    expected = _canonicalize([
        ["a", "a", "a"],
        ["a", "aa"],
        ["aa", "a"],
        ["aaa"],
    ])
    label = 'all same (s="aaa")'
    if actual == expected:
        print(f"[OK  ] {label}: 4 partitions")
    else:
        failures += 1
        print(f"[FAIL] {label}: got {actual}, expected {expected}")

    # Case 6: every partition output must be a list of palindromes
    # covering s in order.
    s = "raceacar"
    actual = partition(s)
    label = f's="{s}" structural validation'
    invalid = []
    for partition_result in actual:
        joined = "".join(partition_result)
        if joined != s:
            invalid.append(f"pieces do not concatenate to s: {partition_result}")
            continue
        for piece in partition_result:
            if piece != piece[::-1]:
                invalid.append(f"piece is not a palindrome: {piece} in {partition_result}")
    if not invalid:
        print(f"[OK  ] {label}: {len(actual)} partitions, all valid")
    else:
        failures += 1
        for msg in invalid[:5]:
            print(f"[FAIL] {label}: {msg}")
        if len(invalid) > 5:
            print(f"[FAIL] ... and {len(invalid) - 5} more invalid partitions")

    if failures:
        raise AssertionError(f"{failures} assertion(s) failed; implement partition.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
