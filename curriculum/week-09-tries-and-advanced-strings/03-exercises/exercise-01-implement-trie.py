"""Exercise 1 - Implement Trie (Prefix Tree) (LeetCode 208).

Pattern: Dict-of-dict trie; insert / search / starts_with from Lecture 1.
Difficulty: Medium.
Target solve time: 20 minutes with full UMPIRE narration.

Problem statement
-----------------
A trie (pronounced as "try") is a tree data structure used to efficiently
store and retrieve keys in a dataset of strings. There are various
applications of this data structure, such as autocomplete and spellchecker.

Implement the Trie class:

- Trie() initializes the trie object.
- void insert(String word) inserts the string word into the trie.
- boolean search(String word) returns True if the string word is in the trie
  (i.e., was inserted before), and False otherwise.
- boolean starts_with(String prefix) returns True if there is a previously
  inserted string word that has the prefix `prefix`, and False otherwise.

Constraints (LeetCode):
- 1 <= word.length, prefix.length <= 2000.
- word and prefix consist only of lowercase English letters.
- At most 3 * 10^4 calls in total to insert, search, and starts_with.

Examples
--------
>>> t = Trie()
>>> t.insert("apple")
>>> t.search("apple")
True
>>> t.search("app")
False
>>> t.starts_with("app")
True
>>> t.insert("app")
>>> t.search("app")
True

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. Three operations: insert, search (exact), starts_with
        (prefix). The discriminator between search and starts_with is the
        terminal flag.
- [ ] M: Trie pattern; dict-of-dict form. Each level is a dict; END = "$"
        marks terminals. Why not set[str]: set cannot answer starts_with in
        less than O(n * L); trie answers it in O(P).
- [ ] P: __init__ creates an empty dict root. insert walks the word,
        setdefault on each char, set END on the final node. search walks
        and checks END at the end. starts_with walks and returns True if
        the walk did not fail.
- [ ] I: Use dict.setdefault on insert; explicit `in` checks on search /
        starts_with.
- [ ] R: Trace insert("apple") + search("apple") + search("app") +
        starts_with("app") + insert("app") + search("app"). All five
        outcomes match the spec.
- [ ] E: insert / search: O(L); starts_with: O(P). Space O(N) where N is
        total inserted character count. Trade vs set[str]: trie wins on
        starts_with; set wins on simplicity if no prefix queries.

References
----------
- Lecture 1, sections 3 and 8 (worked example):
  ../lecture-notes/01-trie-basics-and-autocomplete.md
- LeetCode 208: https://leetcode.com/problems/implement-trie-prefix-tree/
- Wikipedia Trie: https://en.wikipedia.org/wiki/Trie
"""

from __future__ import annotations

from typing import Any, Dict


END: str = "$"


class Trie:
    """Dict-of-dict trie with insert / search / starts_with.

    The harness calls the methods in arbitrary order; each is a short walk
    over a Dict[str, Any]. END = "$" marks terminals; the input alphabet is
    lowercase English letters, so "$" is safely outside the alphabet.

    Replace the bodies with your solution. The signatures and docstrings
    above are part of the spec.
    """

    def __init__(self) -> None:
        """Initialize the trie with an empty root."""
        # TODO: self.root: Dict[str, Any] = {}
        self.root: Dict[str, Any] = {}

    def insert(self, word: str) -> None:
        """Insert `word` into the trie."""
        # TODO: walk the word, setdefault on each character, mark END at
        # the terminal node.
        # Hint:
        #   node = self.root
        #   for ch in word:
        #       node = node.setdefault(ch, {})
        #   node[END] = True
        _ = word  # silence unused-variable lint until you wire it up

    def search(self, word: str) -> bool:
        """Return True iff `word` was previously inserted."""
        # TODO: walk the word; return False on missing child; at the end,
        # return END in node.
        _ = word  # silence unused-variable lint until you wire it up
        return False

    def starts_with(self, prefix: str) -> bool:
        """Return True iff any inserted word has `prefix` as a prefix."""
        # TODO: walk the prefix; return False on missing child; at the end,
        # return True (terminal not required).
        _ = prefix  # silence unused-variable lint until you wire it up
        return False


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 exercise-01-implement-trie.py`.
# Also discovered by `pytest`.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a battery of asserts against the Trie class.

    The asserts cover the canonical edge cases. When the methods are
    unimplemented (return False / no-op), most asserts will fail loudly --
    that is the signal to implement.
    """
    failures = 0
    cases: list[tuple[str, list[tuple[str, str, bool | None]]]] = [
        (
            "canonical apple/app",
            [
                ("insert", "apple", None),
                ("search", "apple", True),
                ("search", "app", False),
                ("starts_with", "app", True),
                ("insert", "app", None),
                ("search", "app", True),
            ],
        ),
        (
            "no false positives on prefixes",
            [
                ("insert", "hello", None),
                ("search", "hell", False),
                ("starts_with", "hell", True),
                ("search", "hellos", False),
                ("starts_with", "world", False),
            ],
        ),
        (
            "single character",
            [
                ("insert", "a", None),
                ("search", "a", True),
                ("starts_with", "a", True),
                ("search", "b", False),
                ("starts_with", "b", False),
            ],
        ),
        (
            "shared prefix family",
            [
                ("insert", "car", None),
                ("insert", "cart", None),
                ("insert", "cat", None),
                ("search", "car", True),
                ("search", "cart", True),
                ("search", "cat", True),
                ("search", "ca", False),
                ("search", "c", False),
                ("starts_with", "ca", True),
                ("starts_with", "cb", False),
                ("starts_with", "cart", True),
                ("starts_with", "carts", False),
            ],
        ),
    ]
    for label, ops in cases:
        t = Trie()
        for op_name, arg, expected in ops:
            if op_name == "insert":
                t.insert(arg)
                continue
            actual = t.search(arg) if op_name == "search" else t.starts_with(arg)
            marker = "OK  " if actual == expected else "FAIL"
            if actual != expected:
                failures += 1
                print(
                    f"[{marker}] {label}: {op_name}({arg!r}) -> {actual}, expected {expected}"
                )
            else:
                print(f"[{marker}] {label}: {op_name}({arg!r}) -> {actual}")
    if failures:
        raise AssertionError(f"{failures} assertion(s) failed; implement Trie.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
