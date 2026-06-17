# Challenge 1 — 3-Sum

> **Pattern:** Pin + Two-pointer converging
> **Difficulty:** Medium
> **Target solve time:** 90 minutes (this one is *the* canonical interview problem; expect to revisit it across the course)

## Problem statement

Given an integer array `nums`, return **all unique triplets** `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.

The solution set must **not contain duplicate triplets**.

**Examples:**

- `nums = [-1, 0, 1, 2, -1, -4]` → `[[-1, -1, 2], [-1, 0, 1]]`
- `nums = [0, 0, 0]` → `[[0, 0, 0]]`
- `nums = [0, 1, 1]` → `[]`

## Acceptance criteria

- [ ] Code passes against the test cases below (write your own pytest file, or extend `timed_runner.py`).
- [ ] Solution is `O(n²)` time or better. A naïve `O(n³)` does not pass.
- [ ] No duplicate triplets in the output even with duplicates in the input.
- [ ] Output triplets may be in any order; the inner triplets may be in any order. The acceptance check normalizes.
- [ ] **Your UMPIRE write-up explicitly addresses the deduplication strategy.** This is the discriminating step — most candidates produce duplicates and lose points.

## UMPIRE outline

- **U:** Confirm unique-triplets requirement. Confirm "unique" means as sets of values, not as index tuples. Walk one example with duplicates: `[-1, 0, 1, 2, -1, -4]`.
- **M:** This is "pin + two-pointer." Sort the array first, then for each pinned `i`, run converging two-pointer on the remainder for `target = -nums[i]`. Skip duplicates at each pointer to ensure unique output.
- **P:** Sort. For `i` from 0 to n-3: skip duplicates (`if i > 0 and nums[i] == nums[i-1]: continue`). Set `l = i+1, r = n-1`. Loop while `l < r`. Sum = `nums[i] + nums[l] + nums[r]`. Match → record, then advance both *past duplicates*. Smaller → `l++`. Larger → `r--`.
- **I:** Implement. Watch the three deduplication checks (on `i`, on `l` after a match, on `r` after a match).
- **R:** Trace on `[-1, 0, 1, 2, -1, -4]`. After sorting: `[-4, -1, -1, 0, 1, 2]`. Pin -4 → no triplets. Pin -1 (first) → finds `[-1, -1, 2]` and `[-1, 0, 1]`. Pin -1 (second) → skipped (duplicate). Pin 0 → no new triplets. Done.
- **E:** **O(n²)** time (outer loop n; inner converging pointer scans n). **O(1)** extra space (excluding output and the sort).

## Function signature

```python
def three_sum(nums: list[int]) -> list[list[int]]:
    ...
```

## Test cases to verify

```python
import pytest

def normalize(lst):
    return sorted(tuple(sorted(t)) for t in lst)

@pytest.mark.parametrize("nums, expected", [
    ([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]]),
    ([0, 0, 0], [[0, 0, 0]]),
    ([0, 1, 1], []),
    ([0, 0, 0, 0], [[0, 0, 0]]),
    ([-2, 0, 1, 1, 2], [[-2, 0, 2], [-2, 1, 1]]),
    ([], []),
    ([1, 2, 3], []),
])
def test_three_sum(nums, expected):
    assert normalize(three_sum(nums)) == normalize(expected)
```

## Common bugs

- **Forgot to sort** — converging pointers require sorted input.
- **No outer-loop dedup** — produces duplicate triplets when input has duplicates.
- **No inner-loop dedup after match** — advances exactly one position, finds same triplet again from the next equal element.
- **Skipping outer dedup on the first iteration** — `if i > 0 and nums[i] == nums[i-1]` (not `if nums[i] == nums[i-1]`).

## Why this matters

3-Sum is one of the most commonly asked interview problems. Every senior engineer has seen it. If you can UMPIRE this with confidence — especially the deduplication discussion — you have demonstrated a meaningful skill.

When you re-do C2 (mastery pathway) or revisit prep before a real interview, **re-run UMPIRE on this problem.** Don't memorize the solution; re-derive it. The act of re-derivation is what cements the pattern.

Commit your solution and write-up. Move on to [Challenge 2](./challenge-02-trapping-rain-water.md).
