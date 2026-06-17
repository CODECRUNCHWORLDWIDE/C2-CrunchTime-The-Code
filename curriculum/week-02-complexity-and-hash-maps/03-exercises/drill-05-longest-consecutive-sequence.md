# Drill 5 — Longest Consecutive Sequence

> **Pattern:** Hash set + "only start from a sequence root"
> **Difficulty:** Medium
> **Target solve time:** 30 minutes
> **Why fifth:** the "this *looks* like O(n log n) but is actually O(n)" interview discriminator. The pattern recognition saves you a complexity class.

## Problem statement

Given an unsorted array of integers `nums`, return the **length of the longest consecutive elements sequence**. The numbers in the sequence must be consecutive *integers* (e.g., 4, 5, 6, 7), but they may appear in any order in the array.

You must write an algorithm that runs in **O(n) time**.

**Examples:**

- `nums = [100, 4, 200, 1, 3, 2]` → `4` (the sequence `[1, 2, 3, 4]`)
- `nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]` → `9` (sequence `[0..8]`)
- `nums = []` → `0`
- `nums = [1, 2, 0, 1]` → `3` (sequence `[0, 1, 2]`; the duplicate `1` doesn't add length)
- `nums = [9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6]` → `7` (sequence `[3..9]`)

## UMPIRE checklist

- [ ] **U:** Restate. Confirm: integers (can be negative), duplicates allowed but don't extend, empty array returns 0. The "consecutive" means differ by 1, regardless of order in the array. **O(n) time is required.**
- [ ] **M:** Hash set with the "only start from a sequence root" trick. A sequence's *root* is the smallest element — i.e., a value `x` for which `x - 1` is *not* in the set. For each root, count how far the sequence extends by incrementing. Each element is touched at most twice across the whole algorithm (once when checking `x - 1`, once when extending from a root). **O(n).** Naive approach (sort, scan) is O(n log n) and the prompt explicitly forbids it.
- [ ] **P:** Build `nums_set = set(nums)`. Initialize `best = 0`. For each `x in nums_set`: if `x - 1 not in nums_set`, this is a root — `length = 1`; loop `while x + length in nums_set: length += 1`; update `best`. Return `best`.
- [ ] **I:** Implement. Iterate over `nums_set`, not `nums`, to avoid re-running the inner loop on duplicates.
- [ ] **R:** Trace on `[100, 4, 200, 1, 3, 2]`. The roots are 100, 1, 200. From 1: `1, 2, 3, 4` — length 4. From 100: length 1. From 200: length 1. Best = 4.
- [ ] **E (graded):** **Time O(n).** Critical claim: even with the nested `while`, total inner-loop iterations across all roots sum to at most n (each element is "extended into" at most once across the algorithm). **Space O(n)** for the set. Tradeoffs: sort + scan is O(n log n)/O(1); a `Counter` doesn't help here because we need membership, not multiplicity. Improvement: none — O(n) is the lower bound.

## Acceptance criteria

- Code passes `timed_runner.py` for `longest_consecutive`.
- Write-up at `umpire-writeups/c2-week-02/drill-05-longest-consecutive-sequence.md`.
- Evaluate section **explicitly defends the O(n) claim** — that's the discriminator.
- Recording ≥15 minutes.

## Function signature

```python
def longest_consecutive(nums: list[int]) -> int:
    """Return the length of the longest run of consecutive integers, in O(n) time."""
    ...
```

## Common bugs to catch in Review

- **Iterating over `nums` instead of `nums_set`.** Duplicates re-run the inner loop, making the algorithm worst-case O(n²). Iterate the set.
- **Forgetting the root check.** Without `if x - 1 not in nums_set`, every element starts an inner loop. The element at the *middle* of a long sequence runs an O(k) inner loop for sequence length k. Total: O(n²). The root check is what gets you O(n).
- **Off-by-one on `length`.** Start at 1 (the root itself counts). The inner loop condition is `x + length in nums_set`, increment length, repeat. When the inner loop exits, `length` is the *count* of elements in the sequence, not the highest index.
- **Returning the sequence itself instead of its length.**

## The O(n) defense — say this out loud

> "**Why this is O(n) and not O(n²):** the inner `while` loop only runs when we hit a sequence *root* (a value `x` with no predecessor in the set). The inner loop walks the sequence to its end — but each non-root element is encountered exactly *once*, at the moment we extend through it. So summing the inner-loop iterations across *all* roots gives at most n total inner steps. Plus n outer steps over the set. **2n = O(n).**"

If you can deliver that sentence cleanly, you have demonstrated the interview-worthy understanding. If you can't, the algorithm probably looks right but you can't *defend* it under pressure — which is the failure mode this drill catches.

## Stretch

**Longest Consecutive Sequence with Union-Find** (advanced). Same problem, different data structure — a disjoint-set forest. Higher constants but the same O(n α(n)) complexity, where α is the inverse Ackermann (effectively O(1)). Bookmark for after Week 7 (DFS / Union-Find territory).

---

That's all five drills. After this, take the [quiz](../05-quiz.md), then start the [challenges](../04-challenges/00-overview.md), [homework](../06-homework.md), and [mini-project](../07-mini-project/00-overview.md).
