# Drill 5 — Fruit Into Baskets

> **Pattern:** Sliding window, variable-size, shape A (longest with at-most-K distinct)
> **Difficulty:** Medium
> **Target solve time:** 25 minutes

A classic disguise: the problem is worded in terms of fruit baskets, but the underlying algorithm is **longest substring with at most 2 distinct characters** — the canonical at-most-K-distinct template with `K = 2`.

## Problem statement

You are visiting a row of fruit trees. You're given an integer array `fruits` where `fruits[i]` is the type of fruit growing at the `i`th tree.

You have two baskets. Each basket can hold **only one type of fruit** but can hold any number of pieces of that type. You start at any tree and pick **exactly one fruit from every tree** (including the start) while moving to the right, stopping when you encounter a tree whose fruit can't fit in either basket. Return the **maximum number of fruit** you can pick.

Equivalently: return the **length of the longest contiguous subarray of `fruits` that contains at most 2 distinct values**.

**Examples:**

- `fruits = [1, 2, 1]` → `3` (the whole array; two types)
- `fruits = [0, 1, 2, 2]` → `3` (`[1, 2, 2]`)
- `fruits = [1, 2, 3, 2, 2]` → `4` (`[2, 3, 2, 2]`)
- `fruits = [3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4]` → `5` (`[1, 2, 1, 1, 2]`)
- `fruits = []` → `0`

## UMPIRE checklist

- [ ] **U:** Restate. Confirm: contiguous, at most 2 distinct values, maximum *length*. Empty input returns 0. Walk an example: `[1, 2, 3, 2, 2]` — windows `[2, 3, 2, 2]` length 4 (types {2, 3}) is the longest with ≤ 2 distinct.
- [ ] **M:** Sliding window, **variable-size, shape A**, with at-most-K-distinct template (`K = 2`). The 30-second memo: *"Sliding window because we want the longest contiguous subarray with a property. Variable-size — the length is the answer. Invariant: `len(counts) <= 2`. Auxiliary state: a frequency table `counts` mapping fruit-type → count-in-window. This is the canonical 'longest with at-most-K distinct' template specialized to K=2."*
- [ ] **P:** Initialize `counts = {}`, `left = 0`, `best = 0`. Outer `for right, fruit in enumerate(fruits)`: `counts[fruit] = counts.get(fruit, 0) + 1`. While `len(counts) > 2`: decrement `counts[fruits[left]]`; if it hits 0, `del counts[fruits[left]]`; advance `left`. Update `best = max(best, right - left + 1)`. Return `best`.
- [ ] **I:** Implement. The **`del` step when count hits 0** is critical — without it, `len(counts)` includes zero-count keys and the invariant is wrong.
- [ ] **R:** Trace `[1, 2, 3, 2, 2]`. r=0 (1): counts={1:1}, best=1. r=1 (2): counts={1:1, 2:1}, best=2. r=2 (3): counts={1:1, 2:1, 3:1}, |counts|=3>2, shrink. left=0, counts={2:1, 3:1}, |counts|=2, exit. best=max(2, 2-1+1)=2. r=3 (2): counts={2:2, 3:1}, best=max(2, 3)=3. r=4 (2): counts={2:3, 3:1}, best=max(3, 4)=4. Return 4. ✓
- [ ] **E (graded):** **Time O(n)** — amortized. The `del` and dict updates are O(1) average. **Space O(1)** — the counts dict holds at most 3 entries transiently (before the shrink restores ≤ 2). Tradeoff: brute force is O(n²) — for each starting index, expand right until 3 distinct seen. Sliding window collapses by reusing the shrink work. Improvement: none — O(n) is the lower bound, and we're at it.

## Acceptance criteria

- Code passes `timed_runner.py` for `total_fruit`.
- Write-up at `umpire-writeups/c2-week-03/drill-05-fruit-into-baskets.md`.
- Match section names the **at-most-K-distinct template** explicitly and notes that this drill specializes it to K=2.
- Recording ≥15 minutes — the recording should be a clean two-minute Match section followed by a tight loop body.

## Function signature

```python
def total_fruit(fruits: list[int]) -> int:
    """Return the length of the longest contiguous subarray of fruits
    containing at most 2 distinct values."""
    ...
```

## Common bugs to catch in Review

- **Forgetting `del counts[key]` on zero count.** The `len(counts) > 2` check then never triggers shrinkage past the third distinct fruit because zero-count keys still occupy slots in the dict.
- **Tracking the answer inside the shrink loop.** This is shape A (longest), so the answer is updated *after* the shrink (`best = max(best, right - left + 1)`), once the invariant is restored. Updating inside the shrink measures windows that may still violate the invariant.
- **Hard-coding "two fruit types" instead of using the template.** The template generalizes to K trivially; writing it with `while len(counts) > 2` makes the K = some-other-value extension cost zero.
- **Off-by-one on the window length.** `right - left + 1`, not `right - left`. Endpoints are both inclusive.

## Stretch

**Longest Substring with At Most K Distinct Characters** (general K). Same template; the `2` becomes `k` (a parameter). Try it after the drill. Worth a separate write-up because the *Match* discussion is identical except for naming K — that proves you've internalized the template, not just memorized the 2-distinct case.

After all five drills, take the [quiz](../05-quiz.md), then start the [challenge](../04-challenges/00-overview.md), [homework](../06-homework.md), and the [mini-project](../07-mini-project/00-overview.md).
