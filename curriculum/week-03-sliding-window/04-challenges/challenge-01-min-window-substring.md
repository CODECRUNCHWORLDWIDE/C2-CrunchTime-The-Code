# Challenge 1 — Minimum Window Substring

> **Pattern:** Sliding window, variable-size, shape B + frequency invariant + `need/formed` counter
> **Difficulty:** Hard
> **Target solve time:** 120 minutes
> **Why hard:** the *invariant* takes longer to articulate than the code takes to write. Most candidates can get to a correct-looking solution; few can explain *why* the `need/formed` integer is the right state choice in 30 seconds. That explanation is the interview discriminator.

## Problem statement

Given two strings `s` and `t` of lengths `m` and `n` respectively, return **the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window**. If there is no such substring, return the empty string `""`.

The test cases are generated so that the answer is unique.

A **substring** is a contiguous non-empty sequence of characters within the string.

**Examples:**

- `s = "ADOBECODEBANC"`, `t = "ABC"` → `"BANC"` (length 4)
- `s = "a"`, `t = "a"` → `"a"`
- `s = "a"`, `t = "aa"` → `""` (s doesn't have two a's)
- `s = "ab"`, `t = "b"` → `"b"`
- `s = "ADOBECODEBANC"`, `t = "AABC"` → `"ADOBECODEBA"` *(would need two A's; this is illustrative, not from the official LC test set)*

## Acceptance criteria

- [ ] Code passes the test cases at the bottom (write your own pytest file, or extend `timed_runner.py`).
- [ ] Solution is **O(m + n) time** and **O(m + n) space** (or O(alphabet) for the bounded-character version). The naive O(m·n) brute force does not pass.
- [ ] Your UMPIRE write-up explicitly justifies the **`need/formed` counter** as the choice of auxiliary state. That is the interview tell.
- [ ] Your write-up explicitly handles **duplicate characters in `t`**. If `t = "AABC"`, the window needs two A's, not one. This is the most common bug.
- [ ] Recording ≥30 minutes — yes, half an hour. The first time you solve this, the recording will be long; that's the right shape.

## The key insight: why a single `formed` integer is the right state

A naive approach: maintain a `window_counts` dict and check on every shrink whether `window_counts >= need` (a multiset containment check). That comparison is `O(|alphabet|)` or `O(|t|)` per shrink, which makes the algorithm `O(n · |alphabet|)` — too slow for large inputs *and* clumsy to reason about.

The insight: **track how many *distinct characters in `t`* are currently *fully satisfied* in the window.** Call that integer `formed`. Let `required = len(need)` be the count of distinct characters in `t`. Then:

> **Invariant:** `formed == required` iff the window contains all characters of `t` with at least the required multiplicities.

`formed` flips at most twice per character per pass — once when its count in the window first reaches the target (`window_counts[ch] == need[ch]`), once when its count later drops below the target. Total flips across the whole algorithm: at most `2 · |distinct chars in t|` = O(|t|). So the inner-loop work is amortized O(1) per character processed.

That's the discriminator. Internalize it.

## UMPIRE outline

- **U:** Restate. Confirm: substring (contiguous), every character of `t` must appear in the window with at least its multiplicity in `t` (so duplicates matter). Return the *minimum-length* such window; empty string if none. Walk `s = "ADOBECODEBANC"`, `t = "ABC"`: candidates include `"ADOBEC"` length 6, `"BECODEBA"` length 8, `"CODEBA"` length 6, `"DEBANC"` length 6, `"BANC"` length 4. Answer: `"BANC"`.
- **M:** Sliding window, variable-size, **shape B (shortest)**, with a **frequency invariant** and a **`need/formed` counter**. The 30-second memo: *"Sliding window because we want the shortest contiguous substring with a multiset-containment property. Variable-size shape B — shrink while property holds. The property: 'every character of t is in the window with at least the required count.' Auxiliary state: a Counter `need` for t's character requirements, a `dict` `window_counts` for the current window's frequencies, and two integers `required` (distinct characters in t) and `formed` (distinct characters currently satisfied). The invariant `formed == required` tracks the property in O(1) per update."*
- **P:**
  1. Build `need = Counter(t)`, `required = len(need)`.
  2. Initialize `window_counts = {}`, `left = 0`, `formed = 0`, `best = (inf, 0, 0)` (length, l, r).
  3. Outer `for right, ch in enumerate(s)`:
     a. Increment `window_counts[ch]`.
     b. If `ch in need` *and* `window_counts[ch] == need[ch]`, `formed += 1`.
     c. While `formed == required`:
        - If `right - left + 1 < best[0]`, update `best`.
        - Decrement `window_counts[s[left]]`.
        - If `s[left] in need` *and* `window_counts[s[left]] < need[s[left]]`, `formed -= 1`.
        - `left += 1`.
  4. Return `s[best[1]:best[2]+1]` or `""` if `best[0] == inf`.
- **I:** Implement. Three traps to watch:
  - The `==` (not `>=`) on the `formed += 1` check. Incrementing more than once per character would over-count.
  - The `<` (not `<=`) on the `formed -= 1` check. Decrement only when the count *drops below* the requirement.
  - The order inside the shrink: **record first, then remove**, otherwise you measure the post-removal window.
- **R:** Trace `s = "ADOBECODEBANC"`, `t = "ABC"`:
  - `need = {A:1, B:1, C:1}`, `required = 3`.
  - r=0 'A': window={A:1}, formed=1.
  - r=1 'D': window={A:1, D:1}.
  - r=2 'O': window={A:1, D:1, O:1}.
  - r=3 'B': window={A:1, D:1, O:1, B:1}, formed=2.
  - r=4 'E': window={A:1, D:1, O:1, B:1, E:1}.
  - r=5 'C': window={A:1, D:1, O:1, B:1, E:1, C:1}, formed=3. Enter shrink:
    - best = (6, 0, 5) i.e. `"ADOBEC"`.
    - Remove A → window[A]=0 < need[A]=1, formed=2. left=1. Exit shrink.
  - r=6..10: traverse 'O', 'D', 'E', 'B', 'A'. At r=10 ('A'): window[A] becomes 1 again, formed=3.
  - Shrink: best vs. window length (10 - 1 + 1 = 10) — no update. Remove D, O, B, ... gradually. (The detailed trace continues; the key event is at r=12.)
  - r=12 'C': window now has A, B, C all with count ≥ 1; formed=3. Shrink steps eventually arrive at left=9 with window `"BANC"` length 4. best updates to (4, 9, 12). ✓
- **E (graded):** **Time O(m + n)** where `m = len(s)`, `n = len(t)`. Building `need` is O(n). Each character in `s` is processed at most twice: once when `right` reaches it (O(1) amortized for the formed update), once when `left` passes it. **Space O(m + n)** — or O(|alphabet|) if we bound the character set; in practice O(|t| + |distinct chars in s|). Tradeoffs: brute force is O(m² · n) (for each (l, r), build a Counter and compare); a smarter brute force is O(m · n); sliding window with naive multiset comparison is O(m · |alphabet|); sliding window with `need/formed` is O(m + n) — strictly best. Improvement: a variant that **only iterates over indices of characters in `t`** (skip non-relevant indices) can speed the constant factor but doesn't change the asymptotic.

## Function signature

```python
def min_window_substring(s: str, t: str) -> str:
    """Return the minimum-length contiguous substring of s containing every
    character of t (with multiplicities), or '' if none exists."""
    ...
```

## Test cases to verify

```python
import pytest

@pytest.mark.parametrize("s, t, expected", [
    ("ADOBECODEBANC", "ABC", "BANC"),
    ("a", "a", "a"),
    ("a", "aa", ""),
    ("ab", "b", "b"),
    ("ab", "a", "a"),
    ("", "ABC", ""),
    ("ABC", "", ""),
    ("aaflslflsldkalskaaa", "aaa", "aaa"),
    ("cabwefgewcwaefgcf", "cae", "cwae"),
])
def test_min_window(s, t, expected):
    assert min_window_substring(s, t) == expected
```

## Common bugs

- **Treating `t` as a set instead of a multiset.** If `t = "aa"`, the window needs two `a`'s. Forgetting this is the #1 bug. The `need = Counter(t)` + `window_counts[ch] == need[ch]` check is what handles it.
- **Updating `formed` on every increment after reaching target.** The right rule: `formed += 1` *only when* `window_counts[ch]` newly equals `need[ch]`. Going from 2 to 3 of `'a'` when `need['a'] == 1` should *not* re-increment `formed`.
- **Updating `formed` on every decrement.** Symmetric. Decrement only when the count *drops below* the requirement, not every time it decreases.
- **Recording inside the shrink in the wrong order.** Record first, then remove. Otherwise the recorded window is shorter than the one that satisfied the property.
- **Returning the length instead of the substring.** Read the spec — it asks for the substring.
- **Forgetting the no-solution sentinel.** If `best[0]` remains `inf`, return `""`.

## The "why O(m + n)?" defense

Out loud, in your Evaluate section:

> "**Why O(m + n).** The outer `for` loop runs `m` times. The inner `while` shrink loop has `left` carrying forward across outer iterations, so `left` advances at most `m` times in total. Every character update to `window_counts` is O(1). The `formed` integer flips at most twice per distinct character in `t`, contributing O(|distinct chars in t|) ≤ O(n) extra work. Total: O(m + n) time, O(m + n) space."

Memorize the shape of that sentence. Saying it cleanly is the difference between "solved Minimum Window Substring" and "demonstrated mastery of the sliding-window pattern."

## Why this matters

Minimum Window Substring is the canonical *hardest sliding-window problem in the standard interview corpus*. It's asked by every major company. If you can UMPIRE it cold — especially the `need/formed` invariant — you have demonstrated something senior engineers respect.

When you revisit Week 3 in mastery pathway, or before a real interview, **re-derive this problem rather than re-reading your old solution**. The act of re-derivation is what cements the pattern. Memorized solutions evaporate under pressure; re-derived ones don't.

## Stretch

**Smallest Window Containing All Characters with At Most K Replacements** — same shape, the property allows up to K mismatches. Comes up in some advanced contest problems. Bookmark; we don't formally cover it in C2.

**Substring with Concatenation of All Words** (LeetCode 30) — a generalization where the alphabet is words instead of characters. Same template; the auxiliary state becomes a `Counter` over words rather than chars. Try it after this challenge if you want a harder reinforcement.

---

This concludes Week 3's exercises and challenge. Take the [quiz](../05-quiz.md), do the [homework](../06-homework.md), then ship the [mini-project](../07-mini-project/00-overview.md) — six write-ups with 30-second memos.
