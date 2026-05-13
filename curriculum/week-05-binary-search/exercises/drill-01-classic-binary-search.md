# Drill 1 — Classic Binary Search

> **Pattern:** Binary search — variant 1, closed interval, find any
> **Difficulty:** Easy
> **Target solve time:** 12 minutes (with full UMPIRE narration)
> **Why first:** the cleanest possible application of the canonical loop. If you can UMPIRE this in 12 minutes including the boundary defense, you have the template.

## Problem statement

Given a sorted (ascending) array `arr` of integers and an integer `target`, return the index of `target` in `arr` if present, or `-1` if absent.

You must solve it in `O(log n)` time. Linear scan (`O(n)`) is rejectable.

**Examples:**

- `arr = [-1, 0, 3, 5, 9, 12]`, `target = 9` → `4`
- `arr = [-1, 0, 3, 5, 9, 12]`, `target = 2` → `-1`
- `arr = [1]`, `target = 1` → `0`
- `arr = [1]`, `target = 0` → `-1`
- `arr = []`, `target = 5` → `-1`

## UMPIRE checklist for this drill

Before you write a line of code, say *each of these* out loud, in order. Recorder running.

- [ ] **U:** Restate. Confirm sorted ascending. Confirm distinct elements (Drill 2 handles duplicates). Confirm the empty-array case returns `-1`. Confirm `O(log n)` time is part of the spec.
- [ ] **M:** Variant 1 — classic binary search, closed-interval convention. The 30-second memo: *"This is a binary-search problem because the array is sorted and we need to locate a target — the canonical fit. Closed-interval convention `[lo, hi]` with `lo <= hi`. Auxiliary state: three integer pointers. Why not linear scan: `O(n)` is rejectable when the array is already sorted. Why not hash set: hash sets are `O(1)` lookup but `O(n)` to build; for a single query, binary search ties or beats linear scan and beats hash-set construction."*
- [ ] **P:** Initialize `lo = 0`, `hi = len(arr) - 1`. Loop while `lo <= hi`. Inside: `mid = lo + (hi - lo) // 2`. If `arr[mid] == target`, return mid. If `arr[mid] < target`, `lo = mid + 1`. If `arr[mid] > target`, `hi = mid - 1`. After loop, return `-1`. Edge case: empty array — the loop never enters; returns `-1`.
- [ ] **I:** Write the code, narrating each line. Speak the boundary defense sentence: *"Closed-interval convention `[lo, hi]` with `lo <= hi`. Both shrink rules exclude `mid` (`+1` and `-1`), guaranteeing strict progress."*
- [ ] **R:** Trace on `[-1, 0, 3, 5, 9, 12]`, target = 9. lo=0, hi=5, mid=2, arr[2]=3 < 9, lo=3. lo=3, hi=5, mid=4, arr[4]=9, return 4. ✓ Trace on target = 2. lo=0, hi=5, mid=2, arr[2]=3 > 2, hi=1. lo=0, hi=1, mid=0, arr[0]=-1 < 2, lo=1. lo=1, hi=1, mid=1, arr[1]=0 < 2, lo=2. lo=2, hi=1, loop exits, return -1. ✓
- [ ] **E:** **Time O(log n)** — each iteration halves the search interval; `⌈log₂ n⌉` iterations bound. **Space O(1)** — three pointers, no recursion. Tradeoff: linear scan is `O(n)`/`O(1)`; binary search trades the same space for `O(log n)` time *if* the array is sorted. Best case `O(1)` (target at first midpoint); worst case `O(log n)`.

## Acceptance criteria

- Code passes the [`timed_runner.py`](timed_runner.py) test cases for `binary_search`.
- A UMPIRE write-up exists at `umpire-writeups/c2-week-05/drill-01-classic-binary-search.md` in your portfolio repo.
- Your Match section names the **closed-interval convention** explicitly and contains the four-element memo.
- Your Implement section uses the **overflow-safe mid formula** `mid = lo + (hi - lo) // 2`. (Python does not need it, but the habit transfers to other languages and is what interviewers grade.)
- Your Evaluate section states the **`O(log n)` time defense sentence**.
- Recording **≥ 10 minutes.** If you finished in 4 minutes, you skipped Match or Evaluate. Re-do it.

## Function signature (for the runner)

```python
def binary_search(arr: list[int], target: int) -> int:
    """Return the index of target in arr, or -1 if absent. O(log n) time, O(1) space."""
    ...
```

## Common bugs you should catch in Review

- **Using `(lo + hi) // 2` instead of `lo + (hi - lo) // 2`.** Works in Python (arbitrary-precision ints), crashes in C/Java/Rust on `lo + hi > INT_MAX`. The habit is what matters.
- **Off-by-one initialization.** `hi = len(arr)` is wrong for the closed convention; it puts an out-of-bounds index into the search interval. Use `hi = len(arr) - 1` with `<=`.
- **Missing the `<=`** in the loop guard. Using `<` with the closed convention skips the last-remaining element. Use `<=` with closed; `<` with half-open.
- **Infinite loop on `lo = mid`.** The closed convention requires `lo = mid + 1` and `hi = mid - 1` — both exclude `mid`. Anything else loops forever on the last-remaining-element case.
- **Returning `lo` after the loop.** This drill is variant 1 (find any). The return on miss is `-1`, *not* `lo`. Variants 2/3 return `lo`; do not transpose.

## Self-feedback template

After you finish, listen to your recording at 1.5×. Write three notes:

1. Did you state the **closed-interval convention** before writing the code? (If not, you missed the boundary-defense beat.)
2. Did you use the overflow-safe `mid` formula? (Even though Python does not need it.)
3. How long did Match take? (Should be <30 seconds on this problem — it is the textbook signal.)

Add those notes to the end of your UMPIRE write-up.

## What to commit to your portfolio repo

```
crunchtime-interview-prep-<you>/
└── umpire-writeups/
    └── c2-week-05/
        ├── drill-01-classic-binary-search.md   # write-up
        └── drill_01_solution.py                 # your solution
```

When done, push and move on to [Drill 2](drill-02-find-first-and-last.md).
