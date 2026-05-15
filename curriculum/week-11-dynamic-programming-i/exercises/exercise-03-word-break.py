"""Exercise 3 - Word Break (LeetCode 139).

Pattern: 1D boolean DP with a string-set check; from Lecture 1 section 7.
Difficulty: Medium.
Target solve time: 30 minutes with full UMPIRE narration.

Problem statement
-----------------
Given a string `s` and a dictionary of strings `wordDict`, return True if
`s` can be segmented into a space-separated sequence of one or more
dictionary words.

Note that the same word in the dictionary may be reused multiple times in
the segmentation.

Constraints (LeetCode):
- 1 <= s.length <= 300.
- 1 <= wordDict.length <= 1000.
- 1 <= wordDict[i].length <= 20.
- s and wordDict[i] consist of lowercase English letters only.
- All the strings in wordDict are unique.

Examples
--------
>>> word_break("leetcode", ["leet", "code"])
True
>>> word_break("applepenapple", ["apple", "pen"])
True
>>> word_break("catsandog", ["cats", "dog", "sand", "and", "cat"])
False

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. Given a string and a word dictionary, return True iff the
        string can be split into a sequence of dictionary words. Words can
        be reused.
- [ ] M: 1D boolean DP. State = "True iff s[:i] is segmentable."
        Recurrence: dp[i] = any(dp[j] and s[j:i] in word_set for j < i).
        Why convert word_dict to a set: O(1) expected lookup vs. O(len)
        linear scan.
        Why not BFS over prefixes: equivalent in complexity (O(n^2)) but
        the DP form is shorter and reuses no extra space.
        Why not greedy left-to-right matching: fails on cases like
        "catsandog" with dict ["cats", "cat", ...] -- greedy picks "cats"
        first, then cannot segment "androg," but the optimum picks "cat"
        first and segments "sandog" as "sand" + "og" -- wait, "og" is not
        in the dictionary; the example actually fails for both strategies.
        Pick a case where greedy fails: dict = ["a", "ab", "bc", "c"],
        s = "abc". Greedy picks "a" then cannot segment "bc"... actually
        "bc" is in the dict. The point: greedy decisions depend on later
        decisions, so DP is required.
- [ ] P: Convert word_dict to a set. Initialize dp[0] = True. Iterate
        i from 1 to n; for each i, iterate j from 0 to i-1; if dp[j] and
        s[j:i] in word_set, set dp[i] = True and break. Return dp[n].
- [ ] I: Standard 1D DP with the boolean OR semantics. Break early on
        first True.
- [ ] R: Trace s = "leetcode", dict = ["leet", "code"]. dp[0] = T; for
        i = 4, j = 0: s[0:4] = "leet" in dict, dp[0] = T -> dp[4] = T.
        For i = 8, j = 4: s[4:8] = "code" in dict, dp[4] = T -> dp[8] = T.
- [ ] E: O(n^2 * L) time where L is average word length (for substring slice
        and hash). O(n) space.

References
----------
- Lecture 1, section 7 (word break):
  ../lecture-notes/01-the-dp-pipeline-and-1d-states.md
- LeetCode 139: https://leetcode.com/problems/word-break/
- Python set complexity: https://wiki.python.org/moin/TimeComplexity
"""

from __future__ import annotations

from typing import List, Tuple


def word_break(s: str, word_dict: List[str]) -> bool:
    """Return True iff s can be segmented into a sequence of dictionary words.

    The harness passes a non-empty string and a non-empty list of dictionary
    words. Implement with the 1D boolean DP. Convert the list to a set first
    for O(1)-expected membership checks.

    Replace the body with your solution. The signature and docstring above
    are part of the spec.
    """
    # TODO: convert the dictionary list to a set
    # Hint:
    #   word_set = set(word_dict)
    #   n = len(s)

    # TODO: initialize the dp array; dp[0] = True (empty prefix base case)
    # Hint:
    #   dp: List[bool] = [False] * (n + 1)
    #   dp[0] = True

    # TODO: fill the dp array via the OR-over-split-points recurrence
    # Hint:
    #   for i in range(1, n + 1):
    #       for j in range(i):
    #           if dp[j] and s[j:i] in word_set:
    #               dp[i] = True
    #               break

    # TODO: return dp[n]
    _ = s, word_dict  # silence unused-variable lint
    return False


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 exercise-03-word-break.py`.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a battery of asserts against the word_break function."""
    failures = 0
    cases: List[Tuple[str, str, List[str], bool]] = [
        ("LC 139 example 1", "leetcode", ["leet", "code"], True),
        ("LC 139 example 2 (reuse)", "applepenapple", ["apple", "pen"], True),
        (
            "LC 139 example 3 (impossible)",
            "catsandog",
            ["cats", "dog", "sand", "and", "cat"],
            False,
        ),
        ("single-letter word", "a", ["a"], True),
        ("single-letter not in dict", "a", ["b"], False),
        ("greedy fails, DP succeeds", "abcd", ["a", "abc", "b", "cd"], True),
        ("long repeating string", "aaaaaaa", ["aaaa", "aaa"], True),
        ("classic catsanddog", "catsanddog", ["cat", "cats", "and", "sand", "dog"], True),
        ("empty-style edge", "a", ["aa"], False),
    ]
    for label, s, words, expected in cases:
        actual = word_break(s, words)
        marker = "OK  " if actual == expected else "FAIL"
        if actual != expected:
            failures += 1
            print(
                f"[{marker}] {label}: word_break({s!r}, {words!r}) -> {actual}, expected {expected}"
            )
        else:
            print(f"[{marker}] {label}: word_break({s!r}, ...) -> {actual}")
    if failures:
        raise AssertionError(f"{failures} assertion(s) failed; implement word_break.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
