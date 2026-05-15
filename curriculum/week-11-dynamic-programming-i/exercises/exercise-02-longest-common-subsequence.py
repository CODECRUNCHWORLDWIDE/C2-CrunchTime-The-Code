"""Exercise 2 - Longest Common Subsequence (LeetCode 1143).

Pattern: 2D string-pair DP; the canonical 2D-DP problem from Lecture 2.
Difficulty: Medium.
Target solve time: 35 minutes with full UMPIRE narration.

Problem statement
-----------------
Given two strings `text1` and `text2`, return the length of their longest
common subsequence. If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original string
with some characters (can be none) deleted without changing the relative
order of the remaining characters. For example, "ace" is a subsequence of
"abcde". A common subsequence of two strings is a subsequence that is common
to both strings.

Constraints (LeetCode):
- 1 <= text1.length, text2.length <= 1000.
- text1 and text2 consist of only lowercase English characters.

Examples
--------
>>> longest_common_subsequence("abcde", "ace")
3
>>> longest_common_subsequence("abc", "abc")
3
>>> longest_common_subsequence("abc", "def")
0

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. Given two strings, return the length of their longest
        common subsequence (subsequence: skipping allowed, order preserved).
- [ ] M: 2D string-pair DP. State = "length of LCS of s1[:i] and s2[:j]."
        Recurrence: match -> dp[i-1][j-1] + 1; no-match ->
        max(dp[i-1][j], dp[i][j-1]). The if/else transition.
        Why not greedy: a locally greedy match may exclude a longer match
        later (e.g., "abc" vs "bcac" -- greedy on 'a' picks the first 'a',
        but the optimum picks 'a' from position 1, then 'c').
        Why not LCS via brute-force recursion: O(2^(m+n)).
- [ ] P: Build a (m+1) x (n+1) table; iterate i from 1 to m and j from 1
        to n; fill via the if/else recurrence. Return dp[m][n].
- [ ] I: Tabulate with the standard row-major iteration. Index offset:
        s1[i-1] (not s1[i]) because dp[0][*] is the empty-prefix base case.
- [ ] R: Trace s1 = "abcde", s2 = "ace" by hand. dp[5][3] should be 3.
- [ ] E: O(mn) time, O(mn) space. Can reduce to O(min(m, n)) space with
        rolling rows (Lecture 2 section 6).

References
----------
- Lecture 2, sections 3 and 6 (LCS + rolling-row reduction):
  ../lecture-notes/02-2d-dp-and-the-grid-and-string-shapes.md
- LeetCode 1143: https://leetcode.com/problems/longest-common-subsequence/
- Wikipedia LCS: https://en.wikipedia.org/wiki/Longest_common_subsequence_problem
"""

from __future__ import annotations

from typing import List, Tuple


def longest_common_subsequence(text1: str, text2: str) -> int:
    """Return the length of the longest common subsequence of text1 and text2.

    The harness passes two non-empty lowercase ASCII strings. Implement with
    the canonical 2D-table form. The rolling-row reduction is a stretch.

    Replace the body with your solution. The signature and docstring above
    are part of the spec.
    """
    # TODO: extract lengths and handle empty edge case
    # Hint:
    #   m, n = len(text1), len(text2)

    # TODO: initialize the (m+1) x (n+1) DP table
    # Hint:
    #   dp: List[List[int]] = [[0] * (n + 1) for _ in range(m + 1)]

    # TODO: fill the table row by row
    # Hint:
    #   for i in range(1, m + 1):
    #       for j in range(1, n + 1):
    #           if text1[i - 1] == text2[j - 1]:
    #               dp[i][j] = dp[i - 1][j - 1] + 1
    #           else:
    #               dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # TODO: return dp[m][n]
    _ = text1, text2  # silence unused-variable lint
    return 0


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 exercise-02-longest-common-subsequence.py`.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a battery of asserts against the longest_common_subsequence function."""
    failures = 0
    cases: List[Tuple[str, str, str, int]] = [
        ("LC 1143 example 1", "abcde", "ace", 3),
        ("LC 1143 example 2", "abc", "abc", 3),
        ("LC 1143 example 3 (disjoint)", "abc", "def", 0),
        ("single char match", "a", "a", 1),
        ("single char no match", "a", "b", 0),
        ("subsequence trick", "bsbininm", "jmjkbkjkv", 1),
        ("repeating chars", "aaaa", "aa", 2),
        ("classic ABCBDAB / BDCAB", "ABCBDAB", "BDCAB", 4),
        ("longer pair", "AGGTAB", "GXTXAYB", 4),
        ("symmetry check", "ace", "abcde", 3),
    ]
    for label, s1, s2, expected in cases:
        actual = longest_common_subsequence(s1, s2)
        marker = "OK  " if actual == expected else "FAIL"
        if actual != expected:
            failures += 1
            print(
                f"[{marker}] {label}: lcs({s1!r}, {s2!r}) -> {actual}, expected {expected}"
            )
        else:
            print(f"[{marker}] {label}: lcs({s1!r}, {s2!r}) -> {actual}")
    if failures:
        raise AssertionError(
            f"{failures} assertion(s) failed; implement longest_common_subsequence."
        )
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
