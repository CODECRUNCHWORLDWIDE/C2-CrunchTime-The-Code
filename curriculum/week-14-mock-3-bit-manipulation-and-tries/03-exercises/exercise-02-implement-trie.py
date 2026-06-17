"""Exercise 2 - Implement Trie (Prefix Tree) (LeetCode 208).

Pattern: trie at speed; the insert / search / starts_with template from
Lecture 2 section 5. The Week-9 recognition is assumed; this week the clock
is the test - target under five minutes for the three operations.
Difficulty: Medium.
Target solve time: 20 minutes with full UMPIRE narration (the three
operations themselves should take under five once you have the shape).

Problem statement
-----------------
A trie (pronounced "try") is a tree data structure used to efficiently
store and retrieve keys in a set of strings. Implement the Trie class:

- Trie() initializes the trie object.
- insert(word) inserts the string `word` into the trie.
- search(word) returns True iff `word` is in the trie (was inserted before).
- starts_with(prefix) returns True iff there is a previously inserted string
  that has the prefix `prefix`.

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
- [ ] U: Restate. Build a prefix tree supporting insert, exact search, and
        prefix search. Confirm: search is exact (the word must have been
        inserted and is a terminal); starts_with only needs the path to exist.
- [ ] M: Trie at speed. Each node holds a dict of child characters plus an
        is_end flag. insert walks/creates the path and marks the terminal;
        search walks and checks is_end; starts_with walks and checks
        reachability. Factor the shared walk into one helper. Why a trie over
        a hash set: prefix queries are O(P); a set cannot answer them in less
        than O(n * L). All three ops are O(L) worst-case.
- [ ] P: TrieNode: {children: dict, is_end: bool}. insert: walk, create
        missing children, set is_end. _walk(s): follow children; return the
        node or None. search: _walk(word) is not None and node.is_end.
        starts_with: _walk(prefix) is not None.
- [ ] I: Type hints; docstrings. Do NOT write the walk loop twice - factor it.
- [ ] R: insert("apple"); search("apple")=True; search("app")=False (path
        exists but is_end is False at 'p'); starts_with("app")=True; then
        insert("app"); search("app")=True (is_end now set).
- [ ] E: insert/search/starts_with all O(L), L = word/prefix length, worst
        case (no probabilistic failure mode). Space O(total characters
        inserted) in the worst case of no shared prefixes.

References
----------
- Lecture 2, section 5 (trie at speed):
  ../lecture-notes/02-bitmasks-bitmask-dp-and-tries-at-speed.md
- Week 9 Lecture 1 (the original trie install):
  ../../week-09-tries-and-advanced-strings/lecture-notes/01-trie-basics-and-autocomplete.md
- LeetCode 208: https://leetcode.com/problems/implement-trie-prefix-tree/
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple


class TrieNode:
    """A single trie node: a map of child characters plus an end-of-word flag."""

    def __init__(self) -> None:
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end: bool = False


class Trie:
    """Prefix tree supporting insert, exact search, and prefix search.

    Replace the method bodies with your solution. The class shape, the
    signatures, and the docstrings are part of the spec. Factor the shared
    walk into the _walk helper rather than duplicating the loop.
    """

    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert `word` into the trie, creating nodes as needed."""
        # TODO: walk from the root, creating a child for each missing char,
        #       then mark the final node as a terminal.
        # Hint:
        #   node = self.root
        #   for ch in word:
        #       if ch not in node.children:
        #           node.children[ch] = TrieNode()
        #       node = node.children[ch]
        #   node.is_end = True
        _ = word

    def search(self, word: str) -> bool:
        """Return True iff `word` was previously inserted (exact match)."""
        # TODO: walk to the end of `word`; it is present iff the node exists
        #       AND is a terminal.
        # Hint:
        #   node = self._walk(word)
        #   return node is not None and node.is_end
        _ = word
        return False

    def starts_with(self, prefix: str) -> bool:
        """Return True iff some inserted word has the prefix `prefix`."""
        # TODO: a prefix exists iff the walk reaches a node at all.
        # Hint:
        #   return self._walk(prefix) is not None
        _ = prefix
        return False

    def _walk(self, s: str) -> Optional["TrieNode"]:
        """Walk the trie along `s`; return the terminal node or None.

        The shared helper for search and starts_with - implement it once.
        """
        # TODO: follow children character by character; bail to None on a miss.
        # Hint:
        #   node = self.root
        #   for ch in s:
        #       if ch not in node.children:
        #           return None
        #       node = node.children[ch]
        #   return node
        _ = s
        return None


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 exercise-02-implement-trie.py`.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run the LC 208 worked example plus extra coverage."""
    failures = 0
    results: List[Tuple[str, bool, bool]] = []

    trie = Trie()
    trie.insert("apple")
    results.append(("search('apple') after insert", trie.search("apple"), True))
    results.append(("search('app') before insert", trie.search("app"), False))
    results.append(("starts_with('app')", trie.starts_with("app"), True))
    results.append(("starts_with('apx')", trie.starts_with("apx"), False))
    trie.insert("app")
    results.append(("search('app') after insert", trie.search("app"), True))

    trie.insert("application")
    results.append(("search('application')", trie.search("application"), True))
    results.append(("starts_with('appl')", trie.starts_with("appl"), True))
    results.append(("search('appl') is not a word", trie.search("appl"), False))
    results.append(("starts_with('b') unseen", trie.starts_with("b"), False))
    results.append(("search('') empty not inserted", trie.search(""), False))

    for label, actual, expected in results:
        marker = "OK  " if actual == expected else "FAIL"
        if actual != expected:
            failures += 1
        print(f"[{marker}] {label}: got {actual}, expected {expected}")

    if failures:
        raise AssertionError(
            f"{failures} assertion(s) failed; implement Trie.insert/search/starts_with."
        )
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
