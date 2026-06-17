# Challenge 2 — Partition to K Equal Sum Subsets (Deep Dive, LeetCode 698)

> **Difficulty:** Medium-Hard. **Target solve time:** 60 minutes including UMPIRE write-up. **Stretch — ship only if you are ahead after Challenge 1 and the Mock #3 work.**

This is the deep-dive version of the canonical **bitmask DP**. The work this week is to recognize that the state is a *subset of a small universe* (the `n <= 16` constraint is the tell), implement the bitmask DP, and defend the `O(2^n * n)` bound against the alternative backtracking solution. Bitmask DP is recognition-grade for Phase 2 and re-installed in Phase 3; this challenge installs the shape.

---

## Problem spec

Given an integer array `nums` and an integer `k`, return `True` iff it is possible to divide `nums` into `k` non-empty subsets whose sums are all equal.

**Constraints (LeetCode):**

- `1 <= k <= len(nums) <= 16`.
- `1 <= nums[i] <= 10^4`.
- The frequency of each element is in `[1, 4]`.

The `len(nums) <= 16` is the loud tell: `2^16 = 65536` subsets is small enough to enumerate, which is exactly the bitmask-DP regime.

---

## Why this is the canonical bitmask DP

Three reasons.

1. **The `n <= 16` constraint *is* the recognition cue.** When `n` is this small and the problem is about partitioning / subsets / covering, the state is almost always "which elements have I used," encoded as a bitmask. Reading `n <= 16` (or `<= 20`) and immediately thinking "bitmask DP" is the senior Match move.

2. **The state collapses cleverly.** A naive state would be `(set of used elements, which subset I'm filling, how full it is)`. But the *current partial-subset sum* is recoverable from the used set alone: `sum(used) % target` tells you how full the current subset is, because subsets are filled one at a time and each completes at exactly `target`. So the state reduces to a single bitmask — `dp[mask] = can the elements in `mask` be partitioned into a whole number of complete subsets plus one partially-filled subset?` This collapse from three dimensions to one is the discriminating insight.

3. **It is the bridge from backtracking (Week 12) to bitmask DP.** The same problem can be solved by backtracking (try to fill `k` buckets one element at a time, prune when a bucket overflows). The bitmask DP is the *memoized* version of that search, where the memo key is the used-set. Seeing the two as the same search with and without caching is the Week-11-meets-Week-12 connection.

---

## 30-second pattern-recognition memo

Use this exact shape at the top of your write-up.

```markdown
> **30-second pattern-recognition memo (Partition to K Equal Sum Subsets /
> bitmask DP):** Partition nums into k equal-sum subsets. n <= 16 is the
> tell -> the state is a subset of the elements, encoded as a bitmask.
> target = total / k (must divide evenly, and max element <= target).
> dp[mask] = True iff the used set `mask` forms a whole number of completed
> subsets plus a current partial subset of sum (sum(mask) % target).
> Transition: from a reachable mask, add any unused element that does not
> overflow the current partial subset. O(2^n * n) time, O(2^n) space.
> Why not pure backtracking: same worst case, but the bitmask DP memoizes
> the used-set so overlapping search states are not re-explored.
```

Read aloud; should hit 25–30 seconds.

---

## The intended algorithm

### Bitmask DP

```python
from __future__ import annotations

from typing import List


def can_partition_k_subsets(nums: List[int], k: int) -> bool:
    """True iff nums can be split into k subsets of equal sum. Bitmask DP."""
    total = sum(nums)
    if total % k != 0:
        return False
    target = total // k
    if max(nums) > target:
        return False

    n = len(nums)
    full = (1 << n) - 1

    # subset_sum[mask] = sum of the chosen elements (precompute for O(1) lookup).
    subset_sum = [0] * (1 << n)
    for mask in range(1, 1 << n):
        low = mask & -mask                 # isolate the lowest set bit
        idx = low.bit_length() - 1         # its element index
        subset_sum[mask] = subset_sum[mask ^ low] + nums[idx]

    # dp[mask] = True iff `mask` is reachable as (completed subsets) + (one partial).
    dp = [False] * (1 << n)
    dp[0] = True

    for mask in range(1 << n):
        if not dp[mask]:
            continue
        current_partial = subset_sum[mask] % target   # how full the current subset is
        for i in range(n):
            if mask & (1 << i):
                continue                                # element i already used
            if current_partial + nums[i] <= target:     # fits in the current subset
                dp[mask | (1 << i)] = True

    return dp[full]
```

The cleverness is `current_partial = subset_sum[mask] % target`. Because we always finish one subset before starting the next, the running sum modulo `target` is exactly the fill level of the subset currently in progress. When `current_partial + nums[i] <= target`, element `i` fits; the transition marks the larger mask reachable. If `dp[full]` is `True`, all `n` elements were placed into exactly `k` complete subsets.

---

## The trace intuition

`nums = [4, 3, 2, 3, 5, 2, 1], k = 4`. `total = 20`, `target = 5`. `max(nums) = 5 <= 5`, so it is feasible to check.

```
dp[0] = True. current_partial = 0.
  From {}, add 4 -> dp[{4}] = True (partial sum 4).
  From {4}, partial = 4; add 1 -> partial 5 (completes a subset), dp[{4,1}] = True.
  From {4,1}, partial = 0 (5 % 5); add 3 -> dp[{4,1,3a}] = True (new subset, partial 3).
  ... continue until dp[full] is reached via the subsets {4,1}, {3,2}, {3,2}, {5}.
Answer: dp[full] = True.
```

The four subsets `{4,1}, {3,2}, {3,2}, {5}` each sum to `5`. The DP finds a reachable path from the empty set to the full set where every completion lands exactly on a multiple of `target`.

---

## Trade-off — bitmask DP vs. backtracking

| Dimension | Bitmask DP | Backtracking (k buckets) |
|-----------|-----------|--------------------------|
| Time | O(2^n * n) | exponential worst case, heavily pruned |
| Space | O(2^n) | O(n) recursion depth |
| Determinism of bound | Tight, predictable | Hard to bound; depends on pruning |
| Code complexity | Moderate | Moderate |
| Practical speed | Consistent | Often faster with good pruning (sort descending, skip duplicates, fill-then-recurse) |

The honest trade: **backtracking with strong pruning is often faster in practice** for this specific problem (sorting descending and skipping equal elements prunes aggressively), while the **bitmask DP gives a clean, predictable `O(2^n * n)` bound** that does not depend on the input distribution. In an interview, name both: "I'll write the bitmask DP for a guaranteed bound; if asked to optimize the constant factor, backtracking with descending-sort pruning often wins on real inputs." That two-sided answer is the senior signal.

---

## Common bugs

1. **Skipping the divisibility and max-element guards.** If `total % k != 0`, the answer is immediately `False`. If `max(nums) > target`, no subset can hold the largest element — `False`. Forgetting either guard sends the DP into impossible states.
2. **Wrong partial-sum computation.** `current_partial = subset_sum[mask] % target` only works because subsets complete at exactly `target`. If you track the partial sum incorrectly (e.g., not modulo `target`), the transition's fit-check is wrong.
3. **Iterating masks in the wrong order.** The transition adds an element (`mask -> mask | (1 << i)`), so masks must be visited in *increasing* order, guaranteeing `dp[mask]` is finalized before it feeds a larger mask.
4. **Index extraction from the lowest set bit.** `low = mask & -mask; idx = low.bit_length() - 1` is the idiom to get the element index of the lowest set bit when precomputing `subset_sum`. Off-by-one here corrupts every subset sum.

---

## UMPIRE write-up structure

### Understand

Restate: partition into `k` equal-sum subsets. Confirm `n <= 16`, the divisibility requirement, and that each element belongs to exactly one subset.

### Match

The 30-second memo. Name bitmask DP, the state collapse (three dimensions to one via `sum % target`), and the backtracking alternative.

### Plan

1. Guard: `total % k == 0` and `max(nums) <= target`.
2. Precompute `subset_sum[mask]` for `O(1)` partial-sum lookup.
3. DP over masks in increasing order; transition adds any unused element that fits the current partial subset.
4. Return `dp[full]`.

### Implement

The bitmask DP above. Optionally also the pruned backtracking, to support the Evaluate trade.

### Review

Walk the trace on `nums = [4, 3, 2, 3, 5, 2, 1], k = 4` (`target = 5`), showing a reachable path to `dp[full]` through the four equal-sum subsets.

### Evaluate

- **Time:** `O(2^n * n)`; for `n = 16`, `2^16 * 16 ≈ 10^6` — fast.
- **Space:** `O(2^n)` for `dp` and `subset_sum`.
- **The state-collapse defense:** why a single bitmask suffices (the partial-subset sum is recoverable as `sum(mask) % target`).
- **Trade vs. backtracking:** the DP gives a tight, distribution-independent bound; pruned backtracking is often faster in practice but harder to bound. Name both.

---

## Acceptance

This challenge is shipped when:

- A `can_partition_k_subsets` bitmask-DP implementation passes the LC 698 sample cases.
- A UMPIRE write-up under `umpire-writeups/c2-week-14/challenge-02-partition-k-subsets/` is committed with the 30-second memo at the top and a recording >= 12 minutes.
- The Evaluate section explains the state collapse and the trade against pruned backtracking.

---

## Stretch — the general bitmask-DP template

If you ship this with time remaining, abstract the pattern: write a short note in your portfolio listing three more bitmask-DP problems and their state semantics — **Shortest Path Visiting All Nodes (LC 847)** (`dp[mask][last]` = shortest path visiting `mask` ending at `last`), **Minimum Cost to Connect Two Groups (LC 1595)**, and **Maximum Compatibility Score Sum (LC 1947)**. Naming the state for each in one sentence cements the recognition that "`n <= 20` plus subsets/assignment" is the bitmask-DP signal. Phase-3 onsite preparation.
