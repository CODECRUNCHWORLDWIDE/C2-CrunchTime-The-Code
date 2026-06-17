"""Exercise 2 - Word Break (LeetCode 139).

Pattern: Trie + memoization composition from Lecture 2.
Difficulty: Medium.
Target solve time: 35 minutes with full UMPIRE narration.

Problem statement
-----------------
Given a string `s` and a list of strings `word_dict`, return True if `s` can
be segmented into a space-separated sequence of one or more dictionary words.

Note that the same word in the dictionary may be reused multiple times in
the segmentation.

Constraints (LeetCode):
- 1 <= len(s) <= 300.
- 1 <= len(word_dict) <= 1000.
- 1 <= len(word) <= 20 for each word in word_dict.
- s and word_dict consist of only lowercase English letters.
- All strings in word_dict are unique.

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
- [ ] U: Restate. Segment s into space-separated dictionary words; reuse
        allowed; return True iff possible. The output is boolean, not the
        segmentation itself.
- [ ] M: Trie + memoization composition. The trie indexes the dictionary
        by prefix; at each starting position i, walk the trie character by
        character and recurse whenever END is reached. Memo on i to cut
        repeated subproblems.
- [ ] P: Build the trie once. Recursive helper can_break(i): if i ==
        len(s), True. If i in memo, return memo[i]. Walk the trie from i
        as long as s[j] is in node; whenever END in node, recurse on j.
        Memoize the result at i.
- [ ] I: Build trie via setdefault; END = "$"; memo: Dict[int, bool].
        Recursion bottoms out at i == len(s).
- [ ] R: Trace "leetcode" with ["leet", "code"]. At i = 0 walk "leet";
        END at j = 4; recurse on i = 4. At i = 4 walk "code"; END at
        j = 8; recurse on i = 8. At i = 8, i == len(s), True. Propagate
        True up.
- [ ] E: Time O(n^2) where n = len(s). Each position triggers at most one
        trie descent of length up to n - i; sum gives O(n^2). Memo prevents
        re-work. Space O(n + sum(len(w) for w in word_dict)).

References
----------
- Lecture 2, section 2 (worked example):
  ../lecture-notes/02-word-break-and-aho-corasick.md
- LeetCode 139: https://leetcode.com/problems/word-break/
- LeetCode 140 (variant): https://leetcode.com/problems/word-break-ii/
"""

from __future__ import annotations

from typing import Any, Dict, List


END: str = "$"


def word_break(s: str, word_dict: List[str]) -> bool:
    """Return True iff `s` segments into space-separated words from `word_dict`.

    Replace the body with your solution. The signature and docstring above
    are part of the spec.
    """
    # TODO: build a trie from word_dict; memoize on start index; recurse.
    # Hint:
    #   trie = _build_trie(word_dict)
    #   memo: Dict[int, bool] = {}
    #   return _can_break(s, 0, trie, memo)
    _ = s, word_dict  # silence unused-variable lint until you wire it up
    return False


def _build_trie(words: List[str]) -> Dict[str, Any]:
    """Construct a dict-of-dict trie from `words` and return the root."""
    # TODO: for each word, walk via setdefault, mark END at the terminal.
    root: Dict[str, Any] = {}
    _ = words  # silence unused-variable lint until you wire it up
    return root


def _can_break(s: str, i: int, trie: Dict[str, Any], memo: Dict[int, bool]) -> bool:
    """Return True iff s[i:] can be segmented into trie words."""
    # TODO: base case i == len(s); memo check; walk the trie from i;
    # whenever END is encountered, recurse on j.
    _ = s, i, trie, memo  # silence unused-variable lint until you wire it up
    return False


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 exercise-02-word-break.py`.
# Also discovered by `pytest`.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a battery of asserts against word_break.

    The asserts cover the canonical edge cases. When word_break is
    unimplemented (returns False), several asserts will fail loudly -- that
    is the signal to implement.
    """
    cases: list[tuple[str, list[str], bool]] = [
        ("leetcode", ["leet", "code"], True),
        ("applepenapple", ["apple", "pen"], True),
        ("catsandog", ["cats", "dog", "sand", "and", "cat"], False),
        ("a", ["a"], True),
        ("a", ["b"], False),
        ("aaaaaaa", ["aaaa", "aaa"], True),
        ("aaaaaaab", ["aaaa", "aaa"], False),
        ("cars", ["car", "ca", "rs"], True),
        ("", ["x"], True),  # empty string segments vacuously
        ("abcd", ["a", "abc", "b", "cd"], True),
        ("abcd", ["a", "abc", "b"], False),
        # Many overlapping prefixes -- the canonical performance test where
        # the trie keeps the inner loop honest at O(L) per descent.
        (
            "a" * 50 + "b",
            ["a", "aa", "aaa", "aaaa", "aaaaa", "aaaaaa", "aaaaaaa", "aaaaaaaa"],
            False,
        ),
        (
            "a" * 50,
            ["a", "aa", "aaa", "aaaa", "aaaaa", "aaaaaa", "aaaaaaa", "aaaaaaaa"],
            True,
        ),
    ]
    failures = 0
    for i, (s, words, expected) in enumerate(cases, start=1):
        actual = word_break(s, words)
        marker = "OK  " if actual == expected else "FAIL"
        label = (s if len(s) <= 20 else s[:17] + "...")
        if actual != expected:
            failures += 1
            print(
                f"[{marker}] case {i}: word_break({label!r}, len={len(words)}) "
                f"-> {actual}, expected {expected}"
            )
        else:
            print(f"[{marker}] case {i}: word_break({label!r}) -> {actual}")
    if failures:
        raise AssertionError(f"{failures} case(s) failed; implement word_break.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
