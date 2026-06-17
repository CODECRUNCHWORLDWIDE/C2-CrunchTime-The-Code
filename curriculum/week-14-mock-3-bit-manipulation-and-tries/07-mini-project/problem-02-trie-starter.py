"""Mini-Project Problem 2 - Add and Search Word (LeetCode 211).

Pattern: trie with a wildcard branching walk from Lecture 2 section 7.
Difficulty: Medium.
Target solve time: 2 hours including the full UMPIRE write-up.

Problem statement
-----------------
Design a data structure that supports adding new words and finding if a
string matches any previously added string.

Implement the WordDictionary class:
- WordDictionary() initializes the object.
- add_word(word) adds `word` to the data structure.
- search(word) returns True iff there is any string in the data structure
  that matches `word`. `word` may contain dots '.' where a dot matches any
  single letter.

Constraints (LeetCode):
- 1 <= word.length <= 25.
- word in add_word consists of lowercase English letters.
- word in search consists of lowercase English letters and dots '.'.
- At most 2 dots in search words for the hard cases; up to 10^4 calls.

Examples
--------
>>> wd = WordDictionary()
>>> wd.add_word("bad")
>>> wd.add_word("dad")
>>> wd.add_word("mad")
>>> wd.search("pad")
False
>>> wd.search("bad")
True
>>> wd.search(".ad")
True
>>> wd.search("b..")
True

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. Store words; answer membership queries where '.' matches any
        one letter. Confirm: a match must consume the whole query and end at a
        terminal node.
- [ ] M: Trie with a wildcard branching walk. add_word is a plain trie insert.
        search recurses: at a normal char, descend the one matching child; at
        '.', recurse into ALL children and OR the results; at end-of-word,
        return is_end. Why a trie over a set: a set cannot do wildcard or
        prefix matching. O(L) without wildcards; up to O(26^L) for all-dots.
- [ ] P: WordNode: {children: dict, is_end: bool}. add_word: walk/create, set
        is_end. search(word): recursive _search(word, i, node). At i == len:
        return node.is_end. If word[i] == '.': any(_search over all children).
        Else: descend node.children[word[i]] if present, else False.
- [ ] I: Type hints; docstrings. The '.' branch is the only difference from a
        plain trie search - factor the recursion cleanly.
- [ ] R: add bad/dad/mad. search("pad")=False (no 'p' child at root).
        search(".ad")=True ('.' tries b/d/m; 'd'->a->d terminal matches).
        search("b..")=True (b -> '.' tries a -> '.' tries d, terminal).
- [ ] E: add_word O(L). search O(L) without dots; worst case O(26^d * L) where
        d is the number of dots. Space O(total characters added).

References
----------
- Lecture 2, section 7 (trie with wildcards):
  ../lecture-notes/02-bitmasks-bitmask-dp-and-tries-at-speed.md
- LeetCode 211: https://leetcode.com/problems/design-add-and-search-words-data-structure/
"""

from __future__ import annotations

from typing import Dict, List, Tuple


class WordNode:
    """A single trie node: a map of child characters plus an end-of-word flag."""

    def __init__(self) -> None:
        self.children: Dict[str, "WordNode"] = {}
        self.is_end: bool = False


class WordDictionary:
    """Trie supporting add_word and wildcard ('.') search.

    Replace the method bodies with your solution. The class shape, the
    signatures, and the docstrings are part of the spec.
    """

    def __init__(self) -> None:
        self.root = WordNode()

    def add_word(self, word: str) -> None:
        """Insert `word` (lowercase letters only) into the trie."""
        # TODO: walk from the root, creating children as needed, mark is_end.
        # Hint:
        #   node = self.root
        #   for ch in word:
        #       node = node.children.setdefault(ch, WordNode())
        #   node.is_end = True
        _ = word

    def search(self, word: str) -> bool:
        """Return True iff `word` (which may contain '.') matches a stored word."""
        # TODO: delegate to the recursive helper starting at index 0, root.
        # Hint:
        #   return self._search(word, 0, self.root)
        _ = word
        return False

    def _search(self, word: str, i: int, node: "WordNode") -> bool:
        """Recursive match: '.' tries all children; a letter descends one."""
        # TODO: base case - consumed the whole word -> must be a terminal.
        # Hint:
        #   if i == len(word):
        #       return node.is_end
        #   ch = word[i]
        #   if ch == ".":
        #       return any(self._search(word, i + 1, child)
        #                  for child in node.children.values())
        #   if ch not in node.children:
        #       return False
        #   return self._search(word, i + 1, node.children[ch])
        _ = (word, i, node)
        return False


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 problem-02-trie-starter.py`.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run the LC 211 worked example plus extra wildcard coverage."""
    failures = 0
    results: List[Tuple[str, bool, bool]] = []

    wd = WordDictionary()
    for w in ("bad", "dad", "mad"):
        wd.add_word(w)

    results.append(("search('pad')", wd.search("pad"), False))
    results.append(("search('bad')", wd.search("bad"), True))
    results.append(("search('.ad')", wd.search(".ad"), True))
    results.append(("search('b..')", wd.search("b.."), True))
    results.append(("search('..d')", wd.search("..d"), True))
    results.append(("search('...')", wd.search("..."), True))
    results.append(("search('....') too long", wd.search("...."), False))
    results.append(("search('ba') prefix not word", wd.search("ba"), False))

    wd.add_word("a")
    results.append(("search('a') single", wd.search("a"), True))
    results.append(("search('.') single wildcard", wd.search("."), True))

    for label, actual, expected in results:
        marker = "OK  " if actual == expected else "FAIL"
        if actual != expected:
            failures += 1
        print(f"[{marker}] {label}: got {actual}, expected {expected}")

    if failures:
        raise AssertionError(
            f"{failures} assertion(s) failed; implement WordDictionary.add_word/search."
        )
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
