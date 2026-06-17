# Drill 3 — Two Sum II (Sorted Array)

> **Pattern:** Two-pointer, converging
> **Difficulty:** Easy/Medium
> **Target solve time:** 20 minutes

This is the canonical example walked through in Lecture 2. Re-solve it yourself; *do not look at the lecture's solution before you finish.* The point is reps, not novelty.

## Problem statement

Given a **1-indexed** array of integers `nums` that is already **sorted in non-decreasing order**, find two numbers such that they add up to a specific `target`. Return the indices as `[index1, index2]` (1-indexed), with `index1 < index2`.

You may assume each input has **exactly one solution**, and you may not use the same element twice.

**Examples:**

- `nums = [2, 7, 11, 15]`, `target = 9` → `[1, 2]` (note: 1-indexed)
- `nums = [2, 3, 4]`, `target = 6` → `[1, 3]`
- `nums = [-1, 0]`, `target = -1` → `[1, 2]`

## UMPIRE checklist

- [ ] **U:** Confirm 1-indexed output (this is the most common bug). Confirm sorted ascending, exactly one solution.
- [ ] **M:** Two-pointer converging. Sorted + pair + target = textbook.
- [ ] **P:** `l=0, r=n-1`. Loop while `l<r`. Sum. Match → return `[l+1, r+1]`. Smaller → `l++`. Larger → `r--`.
- [ ] **I:** Watch the `+1` on the return. Add a defensive `return [-1, -1]` after the loop.
- [ ] **R:** Trace on `[2, 7, 11, 15]` target=9.
- [ ] **E:** **O(n)** / **O(1)**. Hash-map alternative would be O(n)/O(n) — strictly worse here because of sortedness.

## Acceptance criteria

- Code passes `timed_runner.py` for `two_sum_sorted`.
- Write-up committed.
- Recording ≥10 minutes.
- **Bonus discussion section in your write-up:** What changes if the array isn't sorted? What changes if multiple solutions exist?

## Function signature

```python
def two_sum_sorted(nums: list[int], target: int) -> list[int]:
    """1-indexed result. Returns [i, j] with i < j and nums[i-1] + nums[j-1] == target."""
    ...
```

## Common bugs to catch in Review

- **0-indexed instead of 1-indexed** on the return.
- **Wrong pointer advanced** on `sum < target` (advance `l`, not `r`).
- **Off-by-one on initial `r`:** `r = len(nums)` causes `nums[r]` to be out of bounds on first iteration.

Next: [Drill 4 — Remove Duplicates](./drill-04-remove-duplicates.md).
