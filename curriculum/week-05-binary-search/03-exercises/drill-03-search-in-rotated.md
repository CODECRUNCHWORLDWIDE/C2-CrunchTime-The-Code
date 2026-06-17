# Drill 3 — Search in Rotated Sorted Array

> **Pattern:** Binary search — variant 1 with the "which half is sorted?" branch
> **Difficulty:** Medium
> **Target solve time:** 25 minutes (with full UMPIRE narration)
> **Why third:** the canonical "modified array" binary-search problem. Same `O(log n)`, same template, one extra branch — recognize that the rotation does not break the bisection invariant.

## Problem statement

You are given a *rotated* sorted (ascending) array `arr` with **distinct** integers, and a target value. Originally sorted, the array was rotated at some unknown pivot — for example, `[0, 1, 2, 4, 5, 6, 7]` rotated at index 3 becomes `[4, 5, 6, 7, 0, 1, 2]`. Return the index of `target` if present, or `-1` if absent.

You must solve it in `O(log n)` time.

**Examples:**

- `arr = [4, 5, 6, 7, 0, 1, 2]`, `target = 0` → `4`
- `arr = [4, 5, 6, 7, 0, 1, 2]`, `target = 3` → `-1`
- `arr = [1]`, `target = 0` → `-1`
- `arr = [1, 3]`, `target = 3` → `1`
- `arr = [3, 1]`, `target = 1` → `1`
- `arr = [5, 1, 3]`, `target = 3` → `2`

## UMPIRE checklist for this drill

- [ ] **U:** Restate. Confirm rotated sorted with **distinct** elements (LC 81 handles duplicates and is in the homework). Confirm we do not need to find the pivot first. Confirm `O(log n)` required.
- [ ] **M:** Variant 1 with the "which half is sorted?" branch. The 30-second memo: *"Binary search on a rotated sorted array. At every midpoint, at least one of the two halves `[lo, mid]` and `[mid, hi]` is fully sorted. The discriminator is `arr[lo] <= arr[mid]`: if True, the left half is sorted; otherwise the right half is. After identifying the sorted half, check whether the target lies in it; if yes, recurse into it, else recurse into the other half. Auxiliary state: three pointers. Why not 'find pivot first': two binary searches is `O(log n)` but the single-pass version is also `O(log n)` and is the cleaner algorithm."*
- [ ] **P:** Closed-interval convention. Initialize `lo = 0`, `hi = len(arr) - 1`. Loop while `lo <= hi`. Inside: `mid = lo + (hi - lo) // 2`. If `arr[mid] == target`, return mid. Else, branch:
  - If `arr[lo] <= arr[mid]` (left half sorted): if `arr[lo] <= target < arr[mid]`, `hi = mid - 1`; else `lo = mid + 1`.
  - Else (right half sorted): if `arr[mid] < target <= arr[hi]`, `lo = mid + 1`; else `hi = mid - 1`.
  After loop, return `-1`. Edge cases: single element (loop runs once with `mid = 0`); rotation point at index 0 (no actual rotation — works identically to classic).
- [ ] **I:** Write the code, narrating each line. Speak the discriminator: *"`arr[lo] <= arr[mid]` with `<=` not `<` — handles the single-element interval at the boundary."*
- [ ] **R:** Trace on `[4, 5, 6, 7, 0, 1, 2]`, target = 0. lo=0, hi=6, mid=3, arr[3]=7, != 0. arr[0]=4 <= arr[3]=7, left half [0,3] sorted. Is 0 in [4, 7)? No. lo=4. lo=4, hi=6, mid=5, arr[5]=1, != 0. arr[4]=0 <= arr[5]=1, left half [4,5] sorted. Is 0 in [0, 1)? Yes. hi=4. lo=4, hi=4, mid=4, arr[4]=0, return 4. ✓
- [ ] **E:** **Time O(log n)** — each iteration halves the search space; the added "which half sorted?" branch is `O(1)`. **Space O(1)**. Tradeoff: brute-force linear scan is `O(n)`/`O(1)`; "find pivot then binary search" is two `O(log n)` passes = `O(log n)`. The single-pass version above is also `O(log n)` with constant factor 1 instead of 2. Best `O(1)` (target at first mid); worst `O(log n)`.

## Acceptance criteria

- Code passes the [`timed_runner.py`](./timed_runner.py) test cases for `search_rotated`.
- UMPIRE write-up at `umpire-writeups/c2-week-05/drill-03-search-in-rotated.md`.
- Your Match section names the **"which half is sorted?"** discriminator explicitly.
- Your Implement section uses `<=` (not `<`) in the discriminator. Note the edge case where `lo == mid`.
- Recording **≥ 15 minutes**.

## Function signature (for the runner)

```python
def search_rotated(arr: list[int], target: int) -> int:
    """Search for target in a rotated sorted array (distinct elements). Returns index or -1."""
    ...
```

## Common bugs you should catch in Review

- **Using `<` instead of `<=` in the discriminator.** When `lo == mid` (single-element left interval), `arr[lo] < arr[mid]` is False, and you incorrectly conclude "right half sorted." The fix is `<=`. Trace the single-element case to confirm.
- **Wrong target-in-range check.** The sorted half includes `arr[lo]` and `arr[mid]` (closed-closed) but for the *exclusion* check we use `arr[lo] <= target < arr[mid]` — half-open because we already handled `arr[mid] == target` above. Same for the right half.
- **Forgetting the initial `arr[mid] == target` check.** If you skip it, the discriminator is never reached when the target *is* at mid, and the algorithm misses it.
- **Trying to find the pivot first.** Works but doubles the constant factor and adds complexity. The single-pass version is cleaner and is the interview-preferred form.
- **Assuming the array is rotated.** If the rotation point is index 0 (no actual rotation), the algorithm still works — `arr[lo] <= arr[mid]` is always True, left half is always sorted, and you binary-search normally. Don't add a special case for "is it actually rotated?"; you do not need it.

## Self-feedback template

1. Did you state the "which half is sorted?" discriminator out loud in Match?
2. Did you catch the `<=` vs `<` distinction during Review (not before)? (If you knew it cold, great. If you debugged it in Review, that is also great — the catch is the skill.)
3. How long did the trace take? (The Review trace on this problem is longer than on Drills 1-2; budget 3-4 minutes for it.)

## What to commit

```
umpire-writeups/c2-week-05/
├── drill-03-search-in-rotated.md
└── drill_03_solution.py
```

When done, push and move on to [Drill 4](./drill-04-kth-element-in-sorted-matrix.md).
