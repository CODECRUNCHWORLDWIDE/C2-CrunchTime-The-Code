# Drill 2 — Longest Substring Without Repeating Characters

> **Pattern:** Sliding window, variable-size, shape A (longest)
> **Difficulty:** Medium
> **Target solve time:** 25 minutes (full UMPIRE narration)

The most-asked sliding-window problem in real interviews. If only one drill from this week sticks, it should be this one.

## Problem statement

Given a string `s`, return the **length of the longest substring without repeating characters**.

**Examples:**

- `"abcabcbb"` → `3` (the substring `"abc"`)
- `"bbbbb"` → `1` (the substring `"b"`)
- `"pwwkew"` → `3` (the substring `"wke"`; note that `"pwke"` is a subsequence, not a substring)
- `""` → `0`
- `"a"` → `1`
- `"dvdf"` → `3` (the substring `"vdf"`)

## UMPIRE checklist

- [ ] **U:** Restate. Confirm: contiguous substring, not subsequence. Confirm: characters can repeat outside the window but not inside. Empty string returns 0. Walk `"dvdf"`: best is `"vdf"` length 3.
- [ ] **M:** Sliding window, variable-size, shape A. The 30-second memo: *"Sliding window because the prompt asks for the longest contiguous substring with a property. Variable-size — the length is the answer. Invariant: every character inside `s[left..right]` is unique. Auxiliary state: a dict mapping each character to its most recent index in the window (or, equivalently, a set of in-window characters)."*
- [ ] **P:** Initialize `last_seen = {}`, `left = 0`, `best = 0`. Outer `for right, ch in enumerate(s)`: if `ch in last_seen and last_seen[ch] >= left`, jump `left = last_seen[ch] + 1`. Update `last_seen[ch] = right`. Update `best = max(best, right - left + 1)`. Return `best`.
- [ ] **I:** Implement. The `last_seen[ch] >= left` guard is critical — characters with `last_seen` *before* `left` are no longer in the window and must not trigger a left-jump.
- [ ] **R:** Trace on `"dvdf"`. r=0 'd': best=1. r=1 'v': best=2. r=2 'd': last_seen['d']=0 ≥ left=0, left jumps to 1; last_seen['d']=2; best stays 2. r=3 'f': last_seen has no 'f', best=3 (window `"vdf"`). ✓
- [ ] **E (graded):** **Time O(n)** — outer loop is n iterations, the dict update is O(1) average. The amortized argument: `right` advances n times, `left` advances at most n times, total O(n). **Space O(min(n, alphabet))** — at most one entry per distinct character. Tradeoff: brute force (try every (l, r) pair, check uniqueness with a set) is O(n³); the set-based O(n²) is the next step down; sliding window collapses it to O(n). Improvement: none — O(n) is the lower bound.

## Acceptance criteria

- Code passes `timed_runner.py` for `longest_substring_no_repeat`.
- UMPIRE write-up at `umpire-writeups/c2-week-03/drill-02-longest-substring-no-repeat.md`.
- Match section includes the 30-second pattern-recognition memo.
- Recording ≥12 minutes.

## Function signature

```python
def longest_substring_no_repeat(s: str) -> int:
    """Return the length of the longest substring of s with all unique characters."""
    ...
```

## Common bugs to catch in Review

- **Missing the `last_seen[ch] >= left` guard.** Without it, a duplicate from *before* the window jumps `left` backwards (or to an incorrect forward position), corrupting the window.
- **Using a set without updating it on `left` advance.** If you use the explicit-shrink shape (`while ch in seen: seen.remove(s[left]); left += 1`), you must remove the character at `left` *before* incrementing — otherwise `seen` keeps a stale element.
- **Returning the substring instead of its length.** Read the spec.
- **Off-by-one on window length.** `right - left + 1`, not `right - left`. The window includes both endpoints.
- **Using `s.index(ch)` to find the duplicate.** That's O(n) per call → O(n²) overall. Use the dict.

## Stretch

**Longest Substring with At Most K Distinct Characters.** Same shape, different invariant: `len(counts) <= k`. Walked end-to-end in [Lecture 2 §5](../02-lecture-notes/02-the-shrinking-and-growing-mechanics.md). Try it after this drill — solidifies the template.

Next: [Drill 3 — Permutation in String](./drill-03-permutation-in-string.md).
