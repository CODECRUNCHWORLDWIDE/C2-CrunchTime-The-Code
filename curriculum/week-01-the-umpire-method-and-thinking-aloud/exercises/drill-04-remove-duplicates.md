# Drill 4 — Remove Duplicates from Sorted Array

> **Pattern:** Two-pointer, same-direction (read/write)
> **Difficulty:** Easy
> **Target solve time:** 20 minutes

First exposure to the **same-direction** sub-shape. Notice how different it feels from the converging shape — both pointers start at the beginning, only one moves on each iteration.

## Problem statement

Given an integer array `nums` sorted in non-decreasing order, **remove the duplicates in-place** so that each unique element appears only once. The order of unique elements should remain the same. Return the count `k` of unique elements.

The first `k` elements of `nums` after modification must contain the unique elements in their original order. Elements beyond index `k` do not matter.

**Examples:**

- `nums = [1, 1, 2]` → returns `2`; `nums` becomes `[1, 2, _]`
- `nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]` → returns `5`; `nums` becomes `[0, 1, 2, 3, 4, _, _, _, _, _]`

## UMPIRE checklist

- [ ] **U:** Restate: in-place mutation. Return is the count of uniques, not the modified array. Order preserved.
- [ ] **M:** Two-pointer same-direction. `read` walks all positions; `write` advances only when we find a new unique.
- [ ] **P:** Handle empty input. Set `write = 1`. Loop `read` from 1 to n-1. If `nums[read] != nums[read-1]`, copy to `nums[write]` and advance `write`. Return `write`.
- [ ] **I:** Implement. Note: you can also compare `nums[read]` to `nums[write-1]` for clarity — both work.
- [ ] **R:** Trace on `[0, 0, 1, 1, 1, 2]`. Watch the write pointer.
- [ ] **E:** **O(n)** time, **O(1)** space.

## Acceptance criteria

- Code passes `timed_runner.py` for `remove_duplicates`.
- Write-up committed.
- Recording ≥10 minutes.
- Your trace table in Review must show **both** `read` and `write` values at each step.

## Function signature

```python
def remove_duplicates(nums: list[int]) -> int:
    """Modify nums in place; return the count k of unique elements at the front."""
    ...
```

## Common bugs to catch in Review

- **Starting `write = 0`:** The first element is always unique; you should skip past it. `write = 1` is correct.
- **Comparing `nums[read]` to itself:** `if nums[read] != nums[read]` is always False. Compare to `nums[read-1]` or `nums[write-1]`.
- **Returning the modified array** instead of `k`. Read the spec carefully.

## Stretch

Variant: **Remove Duplicates II** — allow each element to appear **at most twice**. (LeetCode 80.) Same pattern, the comparison becomes `nums[read] != nums[write-2]`. Try it.

Next: [Drill 5 — Container With Most Water](drill-05-container-with-most-water.md).
