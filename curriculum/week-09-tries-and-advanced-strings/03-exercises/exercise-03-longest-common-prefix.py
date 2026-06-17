"""Exercise 3 - Longest Common Prefix (LeetCode 14).

Pattern: Three solutions; vertical scan, horizontal scan, trie walk.
Difficulty: Easy.
Target solve time: 25 minutes for all three solutions with full UMPIRE
narration on the choice.

Problem statement
-----------------
Write a function to find the longest common prefix string amongst an array
of strings. If there is no common prefix, return an empty string "".

Constraints (LeetCode):
- 1 <= len(strs) <= 200.
- 0 <= len(strs[i]) <= 200.
- strs[i] consists of only lowercase English letters.

Examples
--------
>>> lcp_vertical(["flower", "flow", "flight"])
'fl'
>>> lcp_vertical(["dog", "racecar", "car"])
''
>>> lcp_horizontal(["flower", "flow", "flight"])
'fl'
>>> lcp_trie(["flower", "flow", "flight"])
'fl'

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. The LCP is the longest string that is a prefix of every
        input. "" if no common prefix or if any input is "".
- [ ] M: Three valid solutions:
        - Vertical: scan column-by-column; O(n * L) where L is the LCP.
        - Horizontal: pairwise LCP; O(n * L).
        - Trie: build trie + walk while single-child non-terminal; O(N).
        The default for one-shot LC 14 is vertical; the trie generalizes
        to incremental / multi-query.
- [ ] P (vertical): iterate i over indices of strs[0]; for each i, check
        every other string at index i; return on first mismatch.
- [ ] P (horizontal): seed prefix = strs[0]; for each s, shrink prefix
        until s.startswith(prefix); return prefix.
- [ ] P (trie): build a trie of all strings; walk from root while node
        has exactly one child and is not a terminal; the path is the LCP.
- [ ] I: Implement all three. Each is short; the discriminator is which
        you would default to.
- [ ] R: Trace each solution on ["flower", "flow", "flight"].
- [ ] E: Vertical and horizontal: O(n * L) time, O(L) space.
        Trie: O(N) build + O(L) walk = O(N) time, O(N) space.
        For one-shot LC 14, vertical is the lightest and what to default
        to. The trie is the right answer for the incremental / multi-query
        generalization.

References
----------
- Lecture 2, section 1 (worked example):
  ../lecture-notes/02-word-break-and-aho-corasick.md
- LeetCode 14: https://leetcode.com/problems/longest-common-prefix/
"""

from __future__ import annotations

from typing import Any, Dict, List


END: str = "$"


def lcp_vertical(strs: List[str]) -> str:
    """Vertical scan: walk column-by-column over the inputs.

    Replace the body with your solution. The signature and docstring above
    are part of the spec.
    """
    # TODO: iterate i over indices of strs[0]; for each i, check every
    # other string at index i; return strs[0][:i] on first mismatch.
    # Hint:
    #   if not strs: return ""
    #   for i in range(len(strs[0])):
    #       ch = strs[0][i]
    #       for s in strs[1:]:
    #           if i >= len(s) or s[i] != ch:
    #               return strs[0][:i]
    #   return strs[0]
    _ = strs  # silence unused-variable lint until you wire it up
    return ""


def lcp_horizontal(strs: List[str]) -> str:
    """Horizontal scan: pairwise-shrink the candidate prefix.

    Replace the body with your solution.
    """
    # TODO: seed prefix = strs[0]; for each s in strs[1:], shrink prefix
    # until s.startswith(prefix) or prefix is empty.
    _ = strs  # silence unused-variable lint until you wire it up
    return ""


def lcp_trie(strs: List[str]) -> str:
    """Trie walk: build a trie of all strings; descend on single-child
    non-terminal nodes.

    Replace the body with your solution.
    """
    # TODO: handle empty list and empty-string-in-list early. Build the
    # trie via setdefault; walk from the root while the node has exactly
    # one child and is not a terminal; collect the path.
    # Hint:
    #   if not strs: return ""
    #   if any(s == "" for s in strs): return ""
    #   root: Dict[str, Any] = {}
    #   for s in strs:
    #       node = root
    #       for ch in s:
    #           node = node.setdefault(ch, {})
    #       node[END] = True
    #   out: List[str] = []
    #   node = root
    #   while len(node) == 1 and END not in node:
    #       ch, child = next(iter(node.items()))
    #       out.append(ch); node = child
    #   return "".join(out)
    _ = strs  # silence unused-variable lint until you wire it up
    return ""


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 exercise-03-longest-common-prefix.py`.
# Also discovered by `pytest`.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a battery of asserts against all three LCP implementations.

    The asserts cover the canonical edge cases. When the functions are
    unimplemented (return ""), several asserts will fail loudly -- that is
    the signal to implement.
    """
    cases: list[tuple[list[str], str]] = [
        (["flower", "flow", "flight"], "fl"),
        (["dog", "racecar", "car"], ""),
        (["interspecies", "interstellar", "interstate"], "inters"),
        (["throne", "throne"], "throne"),
        (["a"], "a"),
        (["", "b"], ""),
        ([""], ""),
        (["abab", "aba", "abc"], "ab"),
        (["car", "carry", "carryon"], "car"),  # off-by-one trap for the trie walk
        (["prefix", "prefix"], "prefix"),
        (["x", "y"], ""),
        (["aaa", "aa", "a"], "a"),
    ]
    failures = 0
    for impl_name, impl in [
        ("lcp_vertical", lcp_vertical),
        ("lcp_horizontal", lcp_horizontal),
        ("lcp_trie", lcp_trie),
    ]:
        print(f"-- {impl_name} --")
        for i, (strs, expected) in enumerate(cases, start=1):
            actual = impl(strs)
            marker = "OK  " if actual == expected else "FAIL"
            if actual != expected:
                failures += 1
                print(
                    f"[{marker}] case {i}: {impl_name}({strs!r}) "
                    f"-> {actual!r}, expected {expected!r}"
                )
            else:
                print(f"[{marker}] case {i}: {impl_name}({strs!r}) -> {actual!r}")
    if failures:
        raise AssertionError(f"{failures} case(s) failed; implement all three.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
