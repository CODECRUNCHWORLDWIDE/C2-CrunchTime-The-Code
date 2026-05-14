"""Mini-Project Problem 1 starter - Trie (Implement Trie, LC 208).

This is the starter for the mini-project's first write-up. Copy this file
into your portfolio repository and fill in the three method bodies. The
write-up itself lives in `umpire-writeups/c2-week-09/mini-project/`.

Pattern: Dict-of-dict trie; the canonical insert / search / starts_with API.
Target solve time: 30 minutes including the full UMPIRE write-up.

Spec
----
Implement the Trie class:

- Trie() initializes the trie object.
- insert(word: str) -> None inserts the string `word` into the trie.
- search(word: str) -> bool returns True iff `word` was previously inserted.
- starts_with(prefix: str) -> bool returns True iff any previously inserted
  word has `prefix` as a prefix.

Constraints (LeetCode):
- 1 <= word.length, prefix.length <= 2000.
- word and prefix consist only of lowercase English letters.
- At most 3 * 10^4 calls in total to insert, search, and starts_with.

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate the three operations. Note the discriminator between
        search and starts_with (the END flag).
- [ ] M: Trie pattern; dict-of-dict form. END = "$" sentinel. Reject
        set[str] because it cannot answer starts_with in less than O(n*L).
- [ ] P: Three method bodies. __init__ creates an empty dict.
        insert walks-and-creates via setdefault.
        search walks-and-checks-END.
        starts_with walks-only.
- [ ] I: Use dict.setdefault; explicit `in` checks on walks.
- [ ] R: Trace insert("apple") + search("apple") + search("app") +
        starts_with("app") + insert("app") + search("app").
- [ ] E: insert / search: O(L). starts_with: O(P). Space O(N) where N is
        total inserted character count. Trade vs set[str].

References
----------
- Lecture 1, sections 3 and 8:
  ../lecture-notes/01-trie-basics-and-autocomplete.md
- Exercise 1 (warm-up): ../exercises/exercise-01-implement-trie.py
- LeetCode 208: https://leetcode.com/problems/implement-trie-prefix-tree/
"""

from __future__ import annotations

from typing import Any, Dict


END: str = "$"


class Trie:
    """Dict-of-dict trie with insert / search / starts_with.

    The constructor initializes the trie with an empty root dict. Each
    inserted word becomes a path from the root; the END sentinel marks the
    terminal node of every inserted word.

    Fill in the bodies; the signatures and docstrings are part of the spec.
    """

    def __init__(self) -> None:
        """Initialize an empty trie."""
        # TODO: self.root: Dict[str, Any] = {}
        self.root: Dict[str, Any] = {}

    def insert(self, word: str) -> None:
        """Insert `word` into the trie."""
        # TODO: walk the word, setdefault on each character, mark END at
        # the terminal node.
        _ = word
        return None

    def search(self, word: str) -> bool:
        """Return True iff `word` was previously inserted."""
        # TODO: walk the word; on missing child, return False; at the end,
        # return END in node.
        _ = word
        return False

    def starts_with(self, prefix: str) -> bool:
        """Return True iff any inserted word has `prefix` as a prefix."""
        # TODO: walk the prefix; on missing child, return False; at the
        # end, return True (terminal not required).
        _ = prefix
        return False


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 problem-01-trie-starter.py`.
# Mirror of the LeetCode 208 sample harness with a few additional edge
# cases that the rubric tests against.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a battery of asserts against the Trie class."""
    failures = 0
    # Cases follow (operation, argument, expected) where None means no return.
    cases: list[tuple[str, list[tuple[str, str, bool | None]]]] = [
        (
            "LC 208 canonical example",
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
            "Shared-prefix family",
            [
                ("insert", "car", None),
                ("insert", "cart", None),
                ("insert", "cat", None),
                ("search", "car", True),
                ("search", "cart", True),
                ("search", "cat", True),
                ("search", "ca", False),
                ("starts_with", "ca", True),
                ("starts_with", "carz", False),
            ],
        ),
        (
            "Single-character edge",
            [
                ("insert", "a", None),
                ("search", "a", True),
                ("starts_with", "a", True),
                ("search", "b", False),
                ("starts_with", "b", False),
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
                    f"[{marker}] {label}: {op_name}({arg!r}) "
                    f"-> {actual}, expected {expected}"
                )
            else:
                print(f"[{marker}] {label}: {op_name}({arg!r}) -> {actual}")
    if failures:
        raise AssertionError(f"{failures} assertion(s) failed; implement Trie.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
