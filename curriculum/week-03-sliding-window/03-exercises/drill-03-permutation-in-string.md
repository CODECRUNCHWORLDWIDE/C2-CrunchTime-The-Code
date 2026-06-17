# Drill 3 — Permutation in String

> **Pattern:** Sliding window, fixed-size, frequency invariant
> **Difficulty:** Medium
> **Target solve time:** 25 minutes

The first drill that uses a **frequency table as the window's auxiliary state**, and the first that shows fixed-size + Counter as a combination. This shape — match a window's character frequencies against a target's — is the bridge to the Minimum Window Substring challenge.

## Problem statement

Given two strings `s1` and `s2`, return `True` if `s2` contains a **permutation of `s1`** as a contiguous substring; otherwise return `False`.

In other words: does any contiguous substring of `s2` of length `len(s1)` have the same character frequencies as `s1`?

**Examples:**

- `s1 = "ab"`, `s2 = "eidbaooo"` → `True` (the substring `"ba"` is a permutation of `"ab"`)
- `s1 = "ab"`, `s2 = "eidboaoo"` → `False`
- `s1 = "abc"`, `s2 = "ccccbabcaaabc"` → `True` (`"bca"`, `"abc"`, etc.)
- `s1 = "a"`, `s2 = "a"` → `True`
- `s1 = "ab"`, `s2 = "a"` → `False` (s2 too short)

## UMPIRE checklist

- [ ] **U:** Restate. Confirm: we want any *permutation* of `s1`, meaning any reordering with the same character counts. Substring must be contiguous and of length `len(s1)`. Return a boolean, not the substring. If `len(s1) > len(s2)`, return False immediately.
- [ ] **M:** Sliding window, **fixed-size** (`k = len(s1)`), with a frequency invariant. The 30-second memo: *"Sliding window because we check every contiguous substring of `s2` of length `k`. Fixed-size — `k = len(s1)`. The invariant: the window's character-frequency Counter equals `s1`'s Counter. Auxiliary state: two Counters (one for `s1`, one for the current window), or a Counter and a `matches` integer that tracks how many character counts currently agree."*
- [ ] **P:** If `len(s1) > len(s2)`, return False. Build `need = Counter(s1)`. Build `window = Counter(s2[:len(s1)])`. If `window == need`, return True. For `right` from `len(s1)` to `len(s2) - 1`: add `s2[right]` to `window`; remove `s2[right - len(s1)]` from `window` (decrement; delete key if count hits 0). If `window == need`, return True. After the loop, return False.
- [ ] **I:** Implement. The `del window[key]` step when count hits 0 is critical — without it, `window == need` will fail because of zero-count keys lingering in the dict.
- [ ] **R:** Trace `s1 = "ab"`, `s2 = "eidbaooo"`. `need = {a:1, b:1}`. First window `"ei"` → `{e:1, i:1}` ≠ need. Slide to `"id"`. Slide to `"db"`. Slide to `"ba"` → `{b:1, a:1}` == need → return True. ✓
- [ ] **E (graded):** **Time O(n + m)** where `n = len(s2)`, `m = len(s1)`. Building `need` is O(m); the loop is O(n - m) iterations of O(1) work each (assuming the alphabet is bounded). **Space O(alphabet)** — at most 26 entries for lowercase letters; O(1) for a bounded alphabet. Tradeoff: a naive "for each starting index, sort the substring and compare" is O(n·m log m). The Counter-based fixed-window approach is strictly better. Improvement: the **matches-counter trick** (track how many character counts currently agree) avoids comparing Counters on every slide and improves the constant factor — but the asymptotic remains O(n).

## Acceptance criteria

- Code passes `timed_runner.py` for `check_inclusion`.
- Write-up at `umpire-writeups/c2-week-03/drill-03-permutation-in-string.md`.
- Match section names *fixed-size* explicitly and identifies the frequency invariant.
- Recording ≥12 minutes.

## Function signature

```python
def check_inclusion(s1: str, s2: str) -> bool:
    """Return True if any permutation of s1 appears as a contiguous substring of s2."""
    ...
```

## Common bugs to catch in Review

- **Comparing Counters with stale zero-count keys.** `Counter({a:1, b:0})` does **not** equal `Counter({a:1})` when compared with `==` because the latter has no `b` key. Always `del` keys whose count drops to 0. (Or use `Counter` arithmetic, which auto-purges, but that allocates.)
- **Sorting the substring inside the loop.** O(m log m) per iteration → O(n·m log m) total. Defeats the pattern.
- **Off-by-one on the slide loop.** The first window is `s2[0..m-1]`; the loop pushes `right = m, m+1, ..., n-1`. The element to *remove* at each slide is `s2[right - m]`.
- **Forgetting the `len(s1) > len(s2)` guard.** Building a window from `s2[:len(s1)]` would fail silently with truncation, giving wrong results.
- **Calling `Counter(s)` inside the loop.** That's O(m) per iteration. Build the window Counter *once*, then update incrementally.

## Stretch

**Find All Anagrams in a String** (LeetCode 438). The same problem, but return *all* starting indices of permutations of `s1` in `s2`, not just whether one exists. Identical window mechanics; the only change is appending the start index when `window == need` and continuing the loop instead of returning early. Re-use your drill code.

Next: [Drill 4 — Minimum Size Subarray Sum](./drill-04-min-size-subarray-sum.md).
