# Drill 2 — Find First and Last Position

> **Pattern:** Binary search — variants 2 + 3 — lower bound and upper bound on duplicates
> **Difficulty:** Easy/Medium
> **Target solve time:** 20 minutes (with full UMPIRE narration)
> **Why second:** the canonical "duplicate handling" template. Two lower-bound calls compose into find-first-and-last cleanly; this is the cleanest exercise of the half-open convention.

## Problem statement

Given a sorted (ascending) array `arr` of integers (possibly with duplicates) and an integer `target`, return `[first, last]` — the leftmost and rightmost indices of `target` in `arr`. If `target` is not present, return `[-1, -1]`.

You must solve it in `O(log n)` time.

**Examples:**

- `arr = [5, 7, 7, 8, 8, 10]`, `target = 8` → `[3, 4]`
- `arr = [5, 7, 7, 8, 8, 10]`, `target = 6` → `[-1, -1]`
- `arr = []`, `target = 0` → `[-1, -1]`
- `arr = [1]`, `target = 1` → `[0, 0]`
- `arr = [2, 2, 2, 2]`, `target = 2` → `[0, 3]`

## UMPIRE checklist for this drill

- [ ] **U:** Restate. Confirm sorted ascending. Confirm duplicates allowed. Confirm empty-array case. Confirm `O(log n)` time required.
- [ ] **M:** Variant 2 (lower bound) applied twice — once for `arr[i] >= target` (gives `first`), once for `arr[i] > target` (gives one past `last`). The 30-second memo: *"Binary search lower-bound template, half-open convention `[lo, hi)`, applied twice. Auxiliary state: three integer pointers. Why two searches: each lower bound is `O(log n)`; total is `O(log n)`. Why not linear scan after finding one match: scanning duplicates can be `O(n)` in the worst case (`[2,2,2,2,2,2]`). Two binary searches is robust."*
- [ ] **P:** Two lower-bound searches.
  1. `first = lower_bound(arr, target)`. If `first == len(arr)` or `arr[first] != target`, return `[-1, -1]`.
  2. `last_plus_1 = lower_bound(arr, target + 1)`. `last = last_plus_1 - 1`.
  Return `[first, last]`.
  Edge case: empty array — first search returns `0 == len(arr)`, triggers the absent path.
- [ ] **I:** Write the code, narrating each line. Speak the boundary defense: *"Half-open convention `[lo, hi)` with `lo < hi`. Shrink `lo = mid + 1` (left bound moves past mid because mid was tested False) and `hi = mid` (right bound stays at mid because mid is the new candidate). Post-loop `lo == hi == first true position`."*
- [ ] **R:** Trace on `[5, 7, 7, 8, 8, 10]`, target = 8.
  First search: lower_bound for 8. lo=0, hi=6, mid=3, arr[3]=8, not < 8, hi=3. lo=0, hi=3, mid=1, arr[1]=7, < 8, lo=2. lo=2, hi=3, mid=2, arr[2]=7, < 8, lo=3. lo=3, hi=3, exit. first=3.
  Second search: lower_bound for 9. lo=0, hi=6, mid=3, arr[3]=8, < 9, lo=4. lo=4, hi=6, mid=5, arr[5]=10, not < 9, hi=5. lo=4, hi=5, mid=4, arr[4]=8, < 9, lo=5. lo=5, hi=5, exit. last_plus_1=5. last=4. Return [3, 4]. ✓
- [ ] **E:** **Time O(log n)** — two lower-bound calls, each `O(log n)`. Total `O(log n)`. **Space O(1)**. Tradeoff: a single binary search for *any* occurrence plus linear expansion is `O(log n + k)` where `k` is the duplicate count — worst case `O(n)`. Two lower-bound calls are strictly `O(log n)`. Best case `O(log n)`; worst case `O(log n)`.

## Acceptance criteria

- Code passes the [`timed_runner.py`](timed_runner.py) test cases for `find_first_and_last`.
- UMPIRE write-up at `umpire-writeups/c2-week-05/drill-02-find-first-and-last.md`.
- Your Match section names the **half-open convention** and the **two-lower-bound trick** explicitly.
- Your Implement section either writes the `lower_bound` helper once and calls it twice, *or* inlines it twice — both are acceptable; the rubric grades whichever you defend more clearly.
- Recording **≥ 12 minutes**.

## Function signature (for the runner)

```python
def find_first_and_last(arr: list[int], target: int) -> list[int]:
    """Return [first, last] indices of target in arr, or [-1, -1] if absent."""
    ...
```

## Common bugs you should catch in Review

- **Mixing conventions.** Using `<=` in the loop guard with a half-open initialization (`hi = len(arr)`) runs off the array. Pick one convention per *variant* and stick to it.
- **Returning `lo - 1` for first.** First is `lo` from the first lower-bound search; last is `lo - 1` from the second. Don't transpose.
- **Forgetting the absent check.** After the first search, if `first == len(arr)` or `arr[first] != target`, the target is absent; return `[-1, -1]` immediately. Without this check, the second search returns nonsense.
- **Trying to do upper bound with the same template as lower bound without changing the predicate.** The trick is the predicate (`< target` vs `<= target`), not the template. Lower bound for `target + 1` *is* the same as upper bound for `target`.

## Self-feedback template

After you finish, listen to your recording at 1.5×:

1. Did you state the **half-open convention** explicitly?
2. Did you justify why two lower-bound calls are correct rather than one lower + one upper?
3. How clean was the absent-target handling?

## What to commit

```
umpire-writeups/c2-week-05/
├── drill-02-find-first-and-last.md
└── drill_02_solution.py
```

When done, push and move on to [Drill 3](drill-03-search-in-rotated.md).
