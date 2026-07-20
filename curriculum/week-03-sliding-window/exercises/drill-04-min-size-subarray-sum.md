# Drill 4 — Minimum Size Subarray Sum

> **Pattern:** Sliding window, variable-size, shape B (shortest)
> **Difficulty:** Medium
> **Target solve time:** 25 minutes

The first drill in **shape B** — shrink *while the property holds*, record the answer *inside* the shrink loop. The sign flip from shape A is the entire point of this drill.

## Problem statement

Given an array of **positive integers** `nums` and an integer `target`, return the **minimum length** of a contiguous subarray whose sum is greater than or equal to `target`. If no such subarray exists, return `0`.

**Examples:**

- `target = 7`, `nums = [2, 3, 1, 2, 4, 3]` → `2` (the subarray `[4, 3]`)
- `target = 4`, `nums = [1, 4, 4]` → `1`
- `target = 11`, `nums = [1, 1, 1, 1, 1, 1, 1, 1]` → `0` (sum of all is only 8)
- `target = 15`, `nums = [1, 2, 3, 4, 5]` → `5` (whole array sums to 15)
- `target = 213`, `nums = [12, 28, 83, 4, 25, 26, 25, 2, 25, 25, 25, 12]` → `8`

## UMPIRE checklist

- [ ] **U:** Restate. Confirm: nums are **positive** (this is what makes sliding window correct — see Match). Minimum length of a contiguous subarray with sum ≥ target. Return 0 if impossible. Walk `target=7, [2,3,1,2,4,3]`: try [2,3,1,2] sum 8 length 4; can shrink to [3,1,2,4] sum 10 length 4; ultimately [4,3] sum 7 length 2 is the answer.
- [ ] **M:** Sliding window, variable-size, **shape B (shortest)**. The 30-second memo: *"Sliding window because we want the shortest contiguous subarray with a sum property. Variable-size — the length is the answer. Critical: this is shape B (shrink while property holds), not shape A. Invariant maintained during shrink: `running >= target`. Auxiliary state: a single running sum. Positivity of nums is what makes the shrink monotonic — with negatives we'd need prefix-sum + hash map instead."*
- [ ] **P:** Initialize `left = 0`, `running = 0`, `best = float('inf')`. Outer `for right, x in enumerate(nums)`: `running += x`. While `running >= target`: update `best = min(best, right - left + 1)`; `running -= nums[left]`; `left += 1`. Return `0` if `best == inf` else `best`.
- [ ] **I:** Order in the shrink loop is critical: **record first, then subtract, then advance left**. Recording after the subtract measures the wrong window.
- [ ] **R:** Trace `target = 7`, `nums = [2,3,1,2,4,3]`. r=0..2: running 2, 5, 6 (no shrink). r=3 (2): running=8, shrink: best=4 (window len 4); running=6, left=1. Exit. r=4 (4): running=10, shrink: best=min(4,4)=4; running=7, left=2. Still ≥7: best=3; running=6, left=3. Exit. r=5 (3): running=9, shrink: best=3; running=7, left=4. Still ≥7: best=2; running=3, left=5. Exit. Return 2. ✓
- [ ] **E (graded):** **Time O(n)** — amortized; `right` advances n times, `left` advances at most n times. The `while` does not make this O(n²) because `left` carries forward across iterations. **Space O(1)**. Tradeoffs: brute force O(n²); prefix-sum + binary search O(n log n)/O(n); sliding window (only valid because nums are positive) O(n)/O(1) — strictly best. Improvement: none — O(n) is the lower bound. *If nums could be negative, sliding window would not apply; switch to prefix-sum + hash map.*

## Acceptance criteria

- Code passes `timed_runner.py` for `min_size_subarray_sum`.
- Write-up at `umpire-writeups/c2-week-03/drill-04-min-size-subarray-sum.md`.
- Match section explicitly names **shape B** and the positivity requirement.
- Recording ≥15 minutes — shape B has more moving parts than shape A; expect the recording to be longer.

## Function signature

```python
def min_size_subarray_sum(target: int, nums: list[int]) -> int:
    """Return the minimal length of a contiguous subarray with sum >= target,
    or 0 if no such subarray exists. Assumes nums are positive integers."""
    ...
```

## Common bugs to catch in Review

- **Record-then-shrink order.** The right order inside the `while` is: record (`best = min(best, right - left + 1)`), then remove (`running -= nums[left]`), then advance (`left += 1`). Doing remove-first records the wrong window length.
- **Initial `best = 0`.** A `min` against 0 will always be 0; the algorithm returns 0 incorrectly. Use `float('inf')` and convert at the end.
- **Using shape A's `while running < target`.** That's the *longest* shape; here we want the *shortest*. The loop condition is `while running >= target`.
- **Forgetting the no-solution sentinel.** If `best` is never updated, return 0 — not `inf`, not `-1`.
- **Applying this to inputs with negatives.** The drill assumes positive integers. With negatives, shrinking from the left can *decrease* the sum below target *and* the algorithm misses valid shorter windows that include the negatives. Use prefix-sum + hash map.

## Stretch

**Subarray Sum at Most K (positive integers).** Same family. Invariant: `running <= K`. Now the goal is to count subarrays, which is shape C: `answer += right - left + 1` after each shrink. Re-use the template from Lecture 2 §3.

Next: [Drill 5 — Fruit Into Baskets](drill-05-fruit-into-baskets.md).
