"""Mini-Project Problem 2 starter - KMP strStr (LC 28).

This is the starter for the mini-project's second write-up. Copy this file
into your portfolio repository and fill in the two function bodies. The
write-up itself lives in `umpire-writeups/c2-week-09/mini-project/`.

Pattern: KMP via the failure function from Lecture 3.
Target solve time: 40 minutes including the full UMPIRE write-up.

Spec
----
Implement strStr via the KMP algorithm.

- build_failure(pattern: str) -> List[int]
    Builds the KMP failure function (a.k.a. prefix function) for `pattern`.
    fail[i] is the length of the longest proper prefix of pattern[:i+1]
    that is also a suffix of pattern[:i+1].

- str_str(haystack: str, needle: str) -> int
    Returns the index of the first occurrence of `needle` in `haystack`,
    or -1 if `needle` is not a substring of `haystack`. By the LC 28 spec,
    returns 0 when `needle` is empty.

Constraints (LeetCode):
- 1 <= len(haystack), len(needle) <= 10^4.
- haystack and needle consist of only lowercase English letters.

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. Find the first occurrence of needle in haystack; -1 if
        absent; 0 if needle is empty.
- [ ] M: KMP via failure function. The naive O(n*m) scanner is replaced
        by O(n + m). Failure function captures "where can the pattern
        pointer resume on a mismatch without losing the partial match."
- [ ] P: Build the failure array in one linear pass over pattern.
        Walk the haystack in one linear pass; on a mismatch, fall back
        along the failure chain; on a full match, return i - j + 1.
- [ ] I: Two loops, each O(n + m) amortized. The inner-while in each
        decreases the relevant pointer; each decrease is paid for by a
        previous increase.
- [ ] R: Trace on "ABABDABACDABABCABAB" with pattern "ABABCABAB". The
        failure array is [0, 0, 1, 2, 0, 1, 2, 3, 4]; the match is at
        index 10.
- [ ] E: O(n + m) time, O(m) space for the failure array. Trade vs the
        naive O(nm); production alternative is str.find (CPython 3.10+
        is already linear-time).

References
----------
- Lecture 3, sections 3 and 4:
  ../lecture-notes/03-kmp-and-z-algorithm.md
- KMP on Wikipedia:
  https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm
- LeetCode 28:
  https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/
"""

from __future__ import annotations

from typing import List


def build_failure(pattern: str) -> List[int]:
    """Build the KMP failure (prefix) function for `pattern`.

    fail[i] = length of the longest proper prefix of pattern[:i+1] that is
    also a suffix of pattern[:i+1].

    Replace the body with your solution.
    """
    # TODO: two-pointer linear-time build.
    # Hint:
    #   fail = [0] * len(pattern); k = 0
    #   for i in range(1, len(pattern)):
    #       while k > 0 and pattern[k] != pattern[i]:
    #           k = fail[k - 1]
    #       if pattern[k] == pattern[i]:
    #           k += 1
    #       fail[i] = k
    #   return fail
    _ = pattern
    return [0] * len(pattern)


def str_str(haystack: str, needle: str) -> int:
    """Return the index of the first occurrence of `needle` in `haystack`,
    or -1 if `needle` is not a substring of `haystack`.

    By the LC 28 spec, returns 0 when `needle` is empty.

    Replace the body with your solution.
    """
    # TODO: handle the empty-needle case; build the failure array; run
    # the matcher.
    # Hint:
    #   if not needle: return 0
    #   fail = build_failure(needle)
    #   j = 0
    #   for i, ch in enumerate(haystack):
    #       while j > 0 and needle[j] != ch:
    #           j = fail[j - 1]
    #       if needle[j] == ch:
    #           j += 1
    #       if j == len(needle):
    #           return i - j + 1
    #   return -1
    _ = haystack, needle
    return -1


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 problem-02-kmp-starter.py`.
# Tests both `build_failure` (against hand-computed values) and `str_str`
# (against the LC 28 sample cases plus a few edge cases).
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run asserts against build_failure and str_str."""
    failures = 0

    print("-- build_failure --")
    failure_cases: list[tuple[str, list[int]]] = [
        ("", []),
        ("A", [0]),
        ("AB", [0, 0]),
        ("ABABAC", [0, 0, 1, 2, 3, 0]),
        ("ABCDABD", [0, 0, 0, 0, 1, 2, 0]),
        ("ABABCABAB", [0, 0, 1, 2, 0, 1, 2, 3, 4]),
        ("AAAA", [0, 1, 2, 3]),
        ("AABAACAABAA", [0, 1, 0, 1, 2, 0, 1, 2, 3, 4, 5]),
    ]
    for pattern, expected in failure_cases:
        actual = build_failure(pattern)
        marker = "OK  " if actual == expected else "FAIL"
        if actual != expected:
            failures += 1
            print(
                f"[{marker}] build_failure({pattern!r}) "
                f"-> {actual}, expected {expected}"
            )
        else:
            print(f"[{marker}] build_failure({pattern!r}) -> {actual}")

    print("-- str_str --")
    str_str_cases: list[tuple[str, str, int]] = [
        ("sadbutsad", "sad", 0),
        ("leetcode", "leeto", -1),
        ("hello", "ll", 2),
        ("aaaaa", "bba", -1),
        ("abc", "", 0),
        ("a", "a", 0),
        ("mississippi", "issi", 1),
        ("mississippi", "issip", 4),
        ("ABABDABACDABABCABAB", "ABABCABAB", 10),
        ("aabaaabaaac", "aabaaac", 4),
    ]
    for haystack, needle, expected in str_str_cases:
        actual = str_str(haystack, needle)
        marker = "OK  " if actual == expected else "FAIL"
        if actual != expected:
            failures += 1
            print(
                f"[{marker}] str_str({haystack!r}, {needle!r}) "
                f"-> {actual}, expected {expected}"
            )
        else:
            print(f"[{marker}] str_str({haystack!r}, {needle!r}) -> {actual}")

    if failures:
        raise AssertionError(
            f"{failures} assertion(s) failed; implement build_failure and str_str."
        )
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
