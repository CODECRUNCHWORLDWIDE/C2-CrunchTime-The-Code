# Drill 3 — Group Anagrams

> **Pattern:** Hash map, canonical-key (frequency)
> **Difficulty:** Medium
> **Target solve time:** 25 minutes
> **Why third:** the first *frequency / canonical-form* drill. Tests whether you can choose a hash *key* that captures the equivalence relation you care about.

## Problem statement

Given an array of strings `strs`, group the **anagrams** together. You can return the answer in **any order** (groups in any order; strings within groups in any order).

An **anagram** is a word formed by rearranging the letters of another (using all original letters exactly once). `"eat"`, `"tea"`, and `"ate"` are anagrams. `"tan"` and `"nat"` are anagrams. `"bat"` is alone.

**Examples:**

- `strs = ["eat","tea","tan","ate","nat","bat"]` → `[["eat","tea","ate"], ["tan","nat"], ["bat"]]` (any order)
- `strs = [""]` → `[[""]]`
- `strs = ["a"]` → `[["a"]]`

## UMPIRE checklist

- [ ] **U:** Restate. Confirm: anagrams use the *same multiset of characters*; empty string is its own group; single-character strings group themselves; case is significant unless told otherwise (clarify with interviewer).
- [ ] **M:** Hash map with a *canonical-key*. Two strings are anagrams iff they have the same canonical form. The canonical form can be (a) the sorted character tuple, or (b) a 26-element count tuple (for lowercase ASCII). Use the canonical form as the dict key; the value is a list of original strings.
- [ ] **P:** Use `defaultdict(list)`. For each string `s`, compute `key = tuple(sorted(s))` (or a count tuple). Append `s` to `groups[key]`. Return `list(groups.values())`.
- [ ] **I:** Implement with `defaultdict(list)` for clean append.
- [ ] **R:** Trace on `["eat","tea","tan","ate","nat","bat"]`. Sorted forms: `aet, aet, ant, aet, ant, abt`. Groups under each key.
- [ ] **E (graded):** Time **O(n · k log k)** where n is the number of strings and k is the max string length (the sort dominates per-string cost). Space **O(n · k)** for the groups. Tradeoff: a 26-element count tuple replaces the sort with O(k) per string, giving **O(n · k)** total — strictly better than `O(n · k log k)`, but harder to read. Defend either, but know they're not the same complexity. Improvement: count-tuple version is the strict win when alphabet is small.

## Acceptance criteria

- Code passes `timed_runner.py` for `group_anagrams`.
- Write-up at `umpire-writeups/c2-week-02/drill-03-group-anagrams.md`.
- Evaluate section names **both** the sorted-tuple and count-tuple approaches with their complexities.
- Recording ≥12 minutes.

## Function signature

```python
def group_anagrams(strs: list[str]) -> list[list[str]]:
    """Group anagrams together. Group order and within-group order both arbitrary."""
    ...
```

## Common bugs to catch in Review

- **Using a list as a key.** `groups[sorted(s)]` raises `TypeError: unhashable type: 'list'`. Use `tuple(sorted(s))` — tuples are hashable, lists are not.
- **Returning the dict instead of its values.** The function returns `list[list[str]]`, not the dict.
- **Wrong canonical form.** Using `set(s)` as a key fails on `"aab"` vs `"ab"` — both produce the same set `{'a', 'b'}` but they aren't anagrams. The canonical form must preserve *multiplicity*.
- **Forgetting empty-string handling.** `tuple(sorted(""))` is the empty tuple `()`, which is hashable — it works without special casing.

## The "two reasonable solutions" discussion

There are *two* idiomatic solutions:

**Solution A — sort each string:**

```python
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        groups[tuple(sorted(s))].append(s)
    return list(groups.values())
```

Cost per string: O(k log k). Total: **O(n · k log k)** time, **O(n · k)** space.

**Solution B — count tuple for each string:**

```python
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        counts = [0] * 26
        for ch in s:
            counts[ord(ch) - ord('a')] += 1
        groups[tuple(counts)].append(s)
    return list(groups.values())
```

Cost per string: O(k). Total: **O(n · k)** time, **O(n · k)** space.

In an interview, **present Solution A first** (because it's shorter and clearer), **then say** "if we needed faster, we could use a 26-element count tuple instead of the sort, dropping to O(n · k) total." That's the canonical "demonstrate you can do better" move.

## Stretch

**Find All Anagrams in a String** (LeetCode 438). Combines counting with sliding window. We'll see this pattern in Week 3.

Next: [Drill 4 — Valid Sudoku (Rows/Cols/Boxes)](./drill-04-valid-sudoku-rows.md).
