# Drill 4 — Kth Smallest Element in a Sorted Matrix

> **Pattern:** Binary search on **values** + monotone `count_le(v)` predicate
> **Difficulty:** Medium/Hard
> **Target solve time:** 35 minutes (with full UMPIRE narration)
> **Why fourth:** the bridge from "binary search on indices" to "binary search on the answer." The matrix is not linearly sorted, so there is no array index to search — but the *value* space is bounded and a count predicate is monotone. This is the structural insight that opens Drill 5.

## Problem statement

You are given an `n × n` integer matrix where each row is sorted ascending and each column is sorted ascending (but the matrix as a whole is *not* linearly sorted). Return the `k`-th smallest element in the matrix when all elements are considered.

You must solve it better than `O(n²)` time. (The naive flatten-and-sort is `O(n² log n)` for `n²` elements; we want `O(n log M)` where `M` is the value range.)

**Examples:**

- `matrix = [[1,5,9], [10,11,13], [12,13,15]]`, `k = 8` → `13`
- `matrix = [[-5]]`, `k = 1` → `-5`
- `matrix = [[1,2], [1,3]]`, `k = 2` → `1`
- `matrix = [[1,3,5], [6,7,12], [11,14,14]]`, `k = 6` → `11`

## UMPIRE checklist for this drill

- [ ] **U:** Restate. Confirm rows sorted ascending **and** columns sorted ascending. Confirm that "kth smallest" includes duplicates (the second of two equal values *is* a distinct rank). Walk an example by hand to confirm understanding of "kth smallest in a 2-D matrix with both row- and column-sorted structure."
- [ ] **M:** Binary search on **values**, not on indices. The 30-second memo: *"This is a binary-search-on-values problem because the matrix is not linearly sorted — there is no array index to bisect. The value range is bounded by `[matrix[0][0], matrix[n-1][n-1]]`. The predicate is `feasible(v) = (count_le(v) >= k)` — monotone in v because raising `v` never decreases the count. The post-loop value `lo` is the smallest v with `count_le(v) >= k`, which coincides with an actual matrix entry because `count_le` jumps only at matrix entries. `count_le(v)` is `O(n)` via the staircase walk from the bottom-left corner. Total `O(n log M)`."*
- [ ] **P:** Two functions. `count_le(v)`: walk from `(n-1, 0)`. If `matrix[r][c] <= v`, account for entire column above (`count += r + 1`), move right (`c += 1`). Else move up (`r -= 1`). Stop when `r < 0` or `c >= n`. `kth_smallest`: half-open template, `lo = matrix[0][0]`, `hi = matrix[n-1][n-1]`. While `lo < hi`: `mid = lo + (hi-lo)//2`; if `count_le(mid) >= k`, `hi = mid`; else `lo = mid + 1`. Return `lo`.
- [ ] **I:** Write the code, narrating each line. Speak the post-loop assertion: *"`lo` is the smallest integer `v` with `count_le(v) >= k`. Since `count_le` jumps by `>=1` only at matrix entries, the boundary value is itself a matrix entry — specifically, the kth smallest."*
- [ ] **R:** Trace on `matrix = [[1,5,9], [10,11,13], [12,13,15]]`, k = 8. lo=1, hi=15. mid=8. count_le(8): start (2,0). matrix[2][0]=12 > 8, up. (1,0)=10 > 8, up. (0,0)=1 <= 8, count += 1, right. (0,1)=5 <= 8, count += 1, right. (0,2)=9 > 8, up. c=3 stops. count=2. 2 < 8, lo=9. lo=9, hi=15. mid=12. count_le(12): start (2,0). 12 <= 12, count += 3 (whole column), right. (2,1)=13 > 12, up. (1,1)=11 <= 12, count += 2, right. (1,2)=13 > 12, up. (0,2)=9 <= 12, count += 1, right. c=3 stops. count=6. 6 < 8, lo=13. lo=13, hi=15. mid=14. count_le(14): start (2,0). 12 <= 14, count += 3, right. (2,1)=13 <= 14, count += 3, right. (2,2)=15 > 14, up. (1,2)=13 <= 14, count += 2, right. c=3 stops. count=8. 8 >= 8, hi=14. lo=13, hi=14. mid=13. count_le(13): start (2,0). 12 <= 13, count += 3, right. (2,1)=13 <= 13, count += 3, right. (2,2)=15 > 13, up. (1,2)=13 <= 13, count += 2, right. c=3 stops. count=8. 8 >= 8, hi=13. lo=13, hi=13, exit. Return 13. ✓
- [ ] **E:** **Time O(n log M)** where `M = matrix[n-1][n-1] - matrix[0][0]`. Binary search runs `log₂ M` iterations; each calls `count_le`, which is `O(n)` (staircase walk monotonically decreases `r` or increases `c`, bounded by `2n` steps). **Space O(1)** — three pointers in the search, two pointers in the staircase. Tradeoff: flatten-and-sort is `O(n² log n)` — strictly worse. Min-heap of size `k` is `O(k log k + (n² - k) log k) = O(n² log k)` — also worse for typical `k`. Binary search on values is the canonical optimization for this family.

## Acceptance criteria

- Code passes the [`timed_runner.py`](timed_runner.py) test cases for `kth_smallest` and `count_le`.
- UMPIRE write-up at `umpire-writeups/c2-week-05/drill-04-kth-element-in-sorted-matrix.md`.
- Your Match section names the **"binary search on values"** insight and the **monotone count predicate** explicitly.
- Your Implement section includes a worked trace of `count_le` on at least one value to demonstrate the staircase walk.
- Recording **≥ 20 minutes**.

## Function signatures (for the runner)

```python
def count_le(matrix: list[list[int]], v: int) -> int:
    """Return the number of matrix entries <= v, using the staircase walk. O(n)."""
    ...

def kth_smallest(matrix: list[list[int]], k: int) -> int:
    """Return the kth smallest element of the matrix. O(n log M)."""
    ...
```

## Common bugs you should catch in Review

- **Wrong direction in the staircase walk.** Starting at `(n-1, 0)` (bottom-left) lets you move right (cell `<= v`, accumulate column) or up (cell `> v`). Starting at `(0, 0)` does not work — both directions could move you closer to the answer, and you cannot decide which without a comparison. Memorize: bottom-left start.
- **Forgetting the half-open convention.** The kth_smallest search is lower-bound shape; use `[lo, hi)` with `<`. Mixing with closed `<=` causes off-by-one at the boundary value.
- **Counting wrong on the staircase.** When `matrix[r][c] <= v`, the entire column from row 0 to row r is `<= v` (because the column is sorted ascending). So `count += r + 1`, not `count += 1`. Forgetting the `+ 1` is a common bug.
- **Using `> k` instead of `>= k`.** We want the smallest `v` such that `count_le(v) >= k`. Using `> k` shifts the boundary by one and produces the (k-1)-th smallest. Trace at least one example to catch this.
- **Returning the count instead of the value.** The post-loop value is `lo`, which is a *matrix value*, not a count. Don't return `k` or the count.

## Self-feedback template

1. Did you articulate the **"binary search on values"** insight in Match? (This is the bridge to parametric search; if you slipped into "binary search on indices" thinking, you missed the structural shift.)
2. Did the staircase walk feel mechanical or did you re-derive it? (First time, re-deriving is fine. By Mock #2 in Week 9, it should be reflexive.)
3. How long did the Review trace take? (This trace is longer than Drills 1-3; budget 5-7 minutes.)

## What to commit

```
umpire-writeups/c2-week-05/
├── drill-04-kth-element-in-sorted-matrix.md
└── drill_04_solution.py
```

When done, push and move on to [Drill 5](drill-05-koko-bananas.md).
