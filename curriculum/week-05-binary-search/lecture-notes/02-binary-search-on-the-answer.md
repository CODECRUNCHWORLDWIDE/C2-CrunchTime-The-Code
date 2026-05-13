# Lecture 2 — Binary Search on the Answer

> **Duration:** ~2 hours.
> **Outcome:** You can recognize a parametric-search problem in 60 seconds, write the monotone predicate `feasible(k)` on demand, pick the search interval `[lo, hi]` defensibly, run the binary search to the boundary, and defend the total complexity (`O((n) log M)` where `M` is the answer-space width).

Lecture 1 covered binary search on a *sorted array* — variants 1, 2, 3. This lecture covers variant 4: binary search on the **answer space**, also called **parametric search**. The technique is the highest-yield interview skill of the week. It is what separates "I know binary search" from "I know what binary search is *for*."

The shift in framing: in Lecture 1, you searched for an index *into an array*. Here, you search for a *value*. The "array" is the interval of possible answers, often `[1, 10⁹]` or `[min(arr), max(arr)]`. The "comparator" is a monotone boolean predicate `feasible(k)`. The mechanic is identical — bisect, halve, return the boundary — but the *recognition* is what most candidates miss.

By the end of this lecture you should be able to read an optimization problem and, within 60 seconds, write down on paper: (a) the answer interval `[lo, hi]`, (b) the monotone predicate `feasible(k)`, and (c) the post-loop assertion. Then the implementation is mechanical.

---

## 1. The reframe: "find the smallest k such that …"

Every parametric-search problem can be rewritten in one canonical shape:

> **Find the smallest integer `k` in `[lo, hi]` such that `feasible(k)` is True.**

(Or its mirror: "find the largest `k` such that `feasible(k)` is True." Both are the same problem with the predicate inverted.)

Three examples that look completely different on the surface but compile to the same shape:

- **Koko Eating Bananas (LC 875).** Find the smallest hourly eating rate `k` such that Koko can finish all piles within `h` hours. Predicate: `feasible(k) = (total_hours_at_rate(k) <= h)`. Search interval: `[1, max(piles)]`.
- **Kth Smallest Element in a Sorted Matrix (LC 378).** Find the smallest value `k` in the matrix such that at least `K` elements are `<= k`. Predicate: `feasible(k) = (count_le(matrix, k) >= K)`. Search interval: `[matrix[0][0], matrix[n-1][n-1]]`.
- **Capacity to Ship Packages in D Days (LC 1011).** Find the smallest ship capacity `k` such that we can ship all packages within `D` days. Predicate: `feasible(k) = (days_needed(weights, k) <= D)`. Search interval: `[max(weights), sum(weights)]`.

In all three, the structure is the same:

```python
def parametric_search(lo: int, hi: int, feasible) -> int:
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

Six lines. Identical to the lower-bound template from Lecture 1. The work is *not* in the binary search; it is in writing `feasible` correctly.

---

## 2. The two preconditions for parametric search

Parametric search applies if and only if **both** of the following hold:

1. **The answer space is integer-bounded.** You can name `lo` and `hi` such that the answer is guaranteed to lie in `[lo, hi]`. (Continuous answer spaces work too with bisection but require epsilon handling — out of scope this week.)
2. **The predicate `feasible(k)` is monotone in `k`.** That is, `feasible(k) = True ⇒ feasible(k+1) = True`. The boolean flips from False to True exactly once over `[lo, hi]`, and never flips back.

If either fails, parametric search does not apply.

Monotonicity is the deeper of the two. The interview test is: *given a candidate answer `k`, would a slightly larger `k` make the answer "more feasible"?* If yes, the predicate is monotone; binary search applies. If no — if making `k` larger could *un-satisfy* the constraints — the predicate is not monotone and the technique fails.

Examples of monotone predicates:

- "Can Koko finish at rate `k` in `h` hours?" — yes, eating faster never takes more hours. Monotone.
- "Can we ship in `D` days with capacity `k`?" — yes, a larger capacity never requires more days. Monotone.
- "Are at least `K` elements `<= k` in the matrix?" — yes, raising `k` never decreases the count. Monotone.

Example of a **non-monotone** predicate (so binary search on the answer does not apply):

- "Is there an interval of length exactly `k` with sum exactly `S`?" — increasing `k` could make True become False (the sums change). Not monotone. Use sliding window or DP.

The monotonicity check is the Match-step skill. In Mock #2 in Week 9, when you read a parametric prompt, **state the monotonicity claim out loud** before you write the predicate:

> "The predicate `feasible(k)` is monotone because a larger `k` never makes the constraints harder to satisfy — specifically, [one-line reason]. Therefore binary search on the answer applies."

That sentence is what the interviewer wants to hear. It is also what most candidates skip.

---

## 3. The three-step recipe

Given a parametric-search problem, the recipe is:

### Step 1 — Identify the answer space `[lo, hi]`

The answer is an integer in some bounded range. Find that range.

- For "find the smallest rate / capacity / size," `lo` is the smallest *possibly valid* answer (often 1, or `max(input)`, or `0`).
- `hi` is an upper bound — frequently the *trivially valid* answer (the largest input, the sum of inputs, the worst case).

Bounds matter. Too-wide bounds make the search slower (more iterations); too-narrow bounds make the search incorrect (miss the answer). When in doubt, **wider is safer than tighter** — `O(log)` is cheap.

### Step 2 — Write `feasible(k)`

Write a boolean function `feasible(k)` that returns True if `k` satisfies the problem's constraints. This is usually *not* a binary search; it is a linear pass, a counting argument, or a small simulation.

The cost of `feasible(k)` dominates the total complexity. If `feasible` is `O(n)`, the total is `O(n log M)` where `M` is the answer-space width. If `feasible` is `O(n²)`, the total is `O(n² log M)`. Be explicit about this in the Evaluate section.

### Step 3 — Run the binary search to the boundary

Use the lower-bound template (variant 2 from Lecture 1). The post-loop value of `lo` is the smallest `k` such that `feasible(k)` is True — the answer.

```python
def parametric_search(lo: int, hi: int, feasible) -> int:
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

The hi bound is *inclusive* in the sense that `feasible(hi)` is guaranteed True at the start — that is the invariant the loop preserves. If you pick `hi` such that `feasible(hi)` is False, the algorithm will return `hi + 1` (wrong) or run off the end.

---

## 4. Worked example: Koko Eating Bananas (LC 875)

This is the **canonical** parametric-search problem and Drill 5 of this week. Memorize the structure.

### Problem

Koko has `piles[i]` bananas in pile `i`. Each hour she eats up to `k` bananas from one pile (if fewer remain, she eats those and moves on). Guards return in `h` hours. Find the smallest `k` such that Koko finishes all piles within `h` hours.

### The reframe

> "Find the smallest `k` in `[1, max(piles)]` such that `total_hours_at_rate(k) <= h`."

### Step 1 — Bounds

- `lo = 1`. Koko must eat at least 1 banana per hour to finish in finite time.
- `hi = max(piles)`. At a rate of `max(piles)`, Koko eats each pile in exactly one hour (since each pile has `<= max(piles)` bananas). Total hours = `len(piles) <= h` is guaranteed (problem constraint). So `feasible(hi) = True`.

### Step 2 — `feasible(k)`

```python
def feasible(k: int) -> bool:
    hours = 0
    for pile in piles:
        hours += (pile + k - 1) // k     # ceil(pile / k)
        if hours > h:
            return False
    return hours <= h
```

`(pile + k - 1) // k` is the ceiling-divide idiom. For a pile of size 7 at rate 3, it takes `⌈7/3⌉ = 3` hours.

The predicate is `O(n)` where `n = len(piles)`. Monotonicity: increasing `k` never increases the per-pile hour count (faster rate, fewer hours), so the sum can only decrease or stay the same. Monotone.

### Step 3 — Binary search

```python
def min_eating_speed(piles: list[int], h: int) -> int:
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible_at_rate(piles, mid, h):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

The full solution:

```python
def min_eating_speed(piles: list[int], h: int) -> int:
    def feasible(k: int) -> bool:
        hours = 0
        for pile in piles:
            hours += (pile + k - 1) // k
            if hours > h:
                return False
        return True

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

Fourteen lines.

### Complexity

- **Time: O(n log M)** where `n = len(piles)` and `M = max(piles)`. The binary search runs `log₂(M)` iterations; each iteration calls `feasible`, which is `O(n)`.
- **Space: O(1)** — three pointers in the search, one accumulator in the predicate.

Defense:

> "**O(n log M)** because we run binary search over the answer interval `[1, max(piles)]` — `log₂(max(piles))` iterations — and each iteration calls `feasible(k)`, which is a single `O(n)` pass over `piles`. The binary-search depth dominates by the `log M` factor; the predicate cost dominates by `n`. Tradeoff: the brute force tries every `k` from 1 to `max(piles)` linearly, which is `O(n M)` — strictly worse. Binary search on the answer is the canonical optimization for this family."

---

## 5. Worked example: Kth Smallest in a Sorted Matrix (LC 378)

A 2-D matrix where each row is sorted ascending and each column is sorted ascending. Find the `K`-th smallest element in the matrix.

### The reframe

> "Find the smallest value `v` in `[matrix[0][0], matrix[n-1][n-1]]` such that `count_le(v) >= K`."

Where `count_le(v)` returns the number of elements `<= v`.

### Why this is binary search on values, not on indices

The matrix is *partially* sorted (rows and columns), but the flattened matrix is not globally sorted. There is no single sorted array to binary-search on. So we binary-search on the *value* — bisecting the integer range `[min, max]` of possible values, using a count predicate.

### `count_le(v)` — `O(n)` via the staircase walk

```python
def count_le(matrix: list[list[int]], v: int) -> int:
    n = len(matrix)
    count = 0
    row, col = n - 1, 0
    while row >= 0 and col < n:
        if matrix[row][col] <= v:
            count += row + 1     # all of column `col` from row 0..row are <= v
            col += 1
        else:
            row -= 1
    return count
```

The "staircase walk" starts at the bottom-left and moves right (when the current cell is `<= v`) or up (when it is `> v`). At each step we account for an entire column-segment in `O(1)`. Total `O(n)` because each step decreases `row` or increases `col` and both are bounded by `n`.

This is Drill 4.

### Binary search wrapper

```python
def kth_smallest(matrix: list[list[int]], k: int) -> int:
    n = len(matrix)
    lo, hi = matrix[0][0], matrix[n-1][n-1]
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if count_le(matrix, mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

### Why `lo` ends up being an actual matrix element

The binary search converges to the smallest `v` such that `count_le(v) >= k`. That value is precisely the kth smallest element of the matrix — because *the count function jumps by ≥ 1 at every actual matrix element* and is constant between consecutive matrix elements. So the boundary value `lo` is itself a matrix element.

This is a subtle point. State it out loud in Review:

> "The post-loop value `lo` is the smallest integer `v` such that at least `k` matrix entries are `<= v`. Because `count_le` is non-decreasing in `v` and jumps only at matrix entries, the boundary value coincides with an actual matrix element — specifically, the kth smallest. The algorithm does not enumerate matrix entries; it just finds the value at which the count crosses `k`."

### Complexity

- **Time: O(n log M)** where `n` is the matrix side and `M = matrix[n-1][n-1] - matrix[0][0]` is the value range.
- **Space: O(1)**.

---

## 6. The recognition signals — the 60-second match

Parametric-search problems are sneakier than classic binary-search problems because the *array* is hidden. The recognition signals:

1. **"Find the smallest / largest k such that …"** — the structural signal. If you can rewrite the problem into this shape, binary search on the answer applies.
2. **"Minimize the maximum X subject to constraints"** — the optimization signal. The answer is the threshold; the constraint becomes the predicate.
3. **"Maximize the minimum Y subject to constraints"** — the mirror form. Same technique, mirrored predicate.
4. **"Find an integer threshold value."** Any time the answer is a bounded integer with a clear "is this enough?" test, parametric search is a candidate.
5. **A counting predicate is natural.** "How many elements are `<= k`?" or "How many groups can we form at threshold `k`?" — the count is monotone in `k`, which feeds parametric search.
6. **The brute force enumerates the answer space linearly.** If the obvious algorithm tries `k = 1, 2, 3, …` until it works, binary search on `k` is the standard upgrade.

When in doubt, ask: *"is there a monotone boolean predicate `feasible(k)` defined on a bounded integer interval, where the answer is the boundary?"* If yes, parametric search. If no, look elsewhere.

The 60-second decision flow:

```
prompt asks "find smallest / largest k such that …"?
├── Yes ──→ likely parametric. Identify the interval and the predicate. Done.
└── No
    ├── prompt asks "minimize the max" or "maximize the min"?  ──→ also parametric
    ├── prompt involves a sorted array with a target?           ──→ classic binary search (Lecture 1)
    └── otherwise                                                ──→ not binary search; another pattern
```

---

## 7. Picking `lo` and `hi` defensibly

A wrong `hi` is the most common parametric-search bug. The fix is to state the bounds *out loud* with their justification.

### Two safe heuristics

- **`hi = a trivially valid answer.`** Something so large that `feasible(hi)` is obviously True. For Koko, `max(piles)` works because at that rate, every pile finishes in one hour, giving `n` total hours, which is `<= h` by problem constraint.
- **`lo = the smallest meaningful answer.`** For Koko, `lo = 1` (zero rate would never finish). For Kth-smallest-matrix, `lo = matrix[0][0]` (anything smaller has count 0).

### When `hi` is hard to bound

For some problems the answer space is huge (e.g., up to `10⁹` or `10¹⁸`). The cost is logarithmic in the width, so `O(log 10¹⁸) ≈ 60` iterations — fine. Pick a generous bound and move on.

If you cannot bound `hi` at all, parametric search may not be the right tool. Reconsider whether the predicate is monotone or whether the problem is actually unbounded.

### Sanity-check the bounds before coding

Before you write the search loop, verbalize:

> "`feasible(lo) = ?`, `feasible(hi) = ?`. The search interval contains the answer iff `feasible(lo) = False` and `feasible(hi) = True` — that is, the predicate flips inside `[lo, hi]`. If `feasible(lo)` is already True, `lo` is the answer (or the problem is degenerate). If `feasible(hi)` is False, the bounds are wrong; widen `hi`."

That check costs five seconds. It catches the wrong-bound bug.

---

## 8. The four parametric variants

Most parametric problems fit one of four patterns. Recognize the shape; the rest is mechanical.

### Pattern A — minimum rate / threshold to satisfy a constraint within a budget

- **Koko Bananas** — minimum eating rate such that all piles finish within `h` hours.
- **Ship Capacity in D Days (LC 1011)** — minimum capacity such that shipping completes within `D` days.
- **Allocate Books / Split Array Largest Sum (LC 410)** — minimum max-sum such that we can partition into `k` groups.

Pattern: `lo = some minimum`, `hi = some maximum`, `feasible(k) = (resource_needed_at_k <= budget)`. Binary-search for smallest `k`.

### Pattern B — count threshold (kth smallest, median in a stream, etc.)

- **Kth Smallest in a Sorted Matrix** — smallest `v` such that `count_le(v) >= k`.
- **Median of Two Sorted Arrays (challenge)** — special case using a partition argument.

Pattern: `lo, hi = value range`, `feasible(v) = (count_le(v) >= k)`. Binary-search for smallest `v`.

### Pattern C — maximize the minimum (the mirror)

- **Aggressive Cows / Magnetic Force Between Two Balls (LC 1552)** — place `m` balls in baskets at positions `pos[i]` to maximize the minimum pairwise distance.
- **Path with Minimum Effort (LC 1631)** — minimize the maximum edge weight in a path (BFS-based predicate).

Pattern: `lo, hi = distance / effort range`, `feasible(d) = (we can place / route at threshold d)`. Binary-search for **largest** `d` where True — equivalently, the smallest `d` where False, minus 1.

### Pattern D — first true on a hidden monotone array

- **First Bad Version (LC 278)** — `n` versions, the first bad one is the cutover. `isBadVersion(k)` is a black-box monotone predicate. Find the smallest `k` with `isBadVersion(k) = True`.

Pattern: `lo = 1, hi = n`, `feasible(k) = is_bad(k)`. Identical to lower bound on a sorted array, with the array replaced by an API call.

All four patterns use the same template. Recognizing which pattern applies takes practice; writing the search once you have the predicate is mechanical.

---

## 9. Common pitfalls

### Pitfall 1 — non-monotone predicate

If `feasible(k)` is True for some `k`, False for `k+1`, and True for `k+2`, binary search will return a wrong boundary. *Always state the monotonicity claim before writing the predicate.* If you cannot articulate why the predicate is monotone, it probably is not — back out and try a different pattern.

### Pitfall 2 — bounds that miss the answer

If you pick `hi` too small (e.g., `hi = sum(piles) // h`), the answer might be outside `[lo, hi]`, and the algorithm returns garbage. Pick `hi` such that `feasible(hi) = True` *by construction*, not by hope. Verify out loud.

### Pitfall 3 — wrong shrink rule for the variant

The template `if feasible(mid): hi = mid else: lo = mid + 1` finds the *smallest* `k` with `feasible(k) = True`. The mirror — finding the *largest* `k` with `feasible(k) = True` — requires the upper-bound template (round-up mid, `lo = mid`, `hi = mid - 1`). Pick consciously.

### Pitfall 4 — predicate that mutates state

`feasible(k)` should be pure — no side effects on global state. If your predicate sorts an array, builds a dict, or otherwise mutates, two calls with the same `k` could disagree. Make `feasible` deterministic.

### Pitfall 5 — off-by-one in the predicate

The bug shifts from the binary search to the predicate. If `feasible(k)` is itself off-by-one (e.g., uses `<` instead of `<=`), the boundary will be wrong by one. Trace the predicate on `lo` and `hi` before integrating.

---

## 10. Worked example end-to-end: Ship Capacity in D Days (LC 1011)

We will work this in full UMPIRE, abbreviated.

**[U — 2 minutes]**

> "I am given an array `weights` and an integer `D`. Each day I can ship a contiguous prefix of the remaining packages, up to the ship's capacity. Find the smallest capacity such that I can ship all packages within `D` days. Confirm: contiguous means in array order — no reordering. Confirm: `weights[i] <= capacity` always (otherwise no capacity works). Walk an example: `weights = [1,2,3,4,5,6,7,8,9,10]`, `D = 5`. The answer is 15: split into `[1,2,3,4,5]`, `[6,7]`, `[8]`, `[9]`, `[10]` — five days, max day-sum 15."

**[M — 30 seconds]**

> "Binary search on the answer. The 30-second memo: *Bounded integer answer, monotone predicate, optimization problem — that is the parametric signal. The interval is `[max(weights), sum(weights)]` — `max(weights)` because the capacity must hold the largest single package; `sum(weights)` because shipping everything in one day always works. The predicate `feasible(c) = (days_needed(weights, c) <= D)` is monotone: larger capacity never increases the day count. Binary-search for the smallest `c` with `feasible(c) = True`.*"

**[P — 1 minute]**

> "Predicate: walk weights, accumulating into a `day_sum`. When adding the next weight would exceed `c`, start a new day. Count days; return `days <= D`. Search: lower-bound template, `lo = max(weights)`, `hi = sum(weights)`. Return `lo`."

**[I — 3 minutes]**

```python
def ship_within_days(weights: list[int], D: int) -> int:
    def days_needed(c: int) -> int:
        days = 1
        load = 0
        for w in weights:
            if load + w > c:
                days += 1
                load = w
            else:
                load += w
        return days

    def feasible(c: int) -> bool:
        return days_needed(c) <= D

    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**[R — 2 minutes]**

> "Trace on `weights = [1,2,3,4,5,6,7,8,9,10]`, `D = 5`.
> `lo = 10, hi = 55`. mid = 32. days_needed(32): pack [1,2,3,4,5,6,7] (sum 28) day 1, [8,9] day 2, [10] day 3. days = 3 <= 5. feasible. hi = 32.
> lo = 10, hi = 32. mid = 21. days_needed(21): [1,2,3,4,5,6] (sum 21) day 1, [7,8] (15) day 2, [9] day 3, [10] day 4. days = 4 <= 5. feasible. hi = 21.
> lo = 10, hi = 21. mid = 15. days_needed(15): [1,2,3,4,5] (15) day 1, [6,7] (13) day 2, [8] day 3, [9] day 4, [10] day 5. days = 5 <= 5. feasible. hi = 15.
> lo = 10, hi = 15. mid = 12. days_needed(12): [1,2,3,4] (10) day 1, [5,6] (11) day 2, [7] day 3, [8] day 4, [9] day 5, [10] day 6. days = 6 > 5. not feasible. lo = 13.
> Continue narrowing… eventually lo = 15. Return 15. ✓"

**[E — 1 minute]**

> "**Time O(n log S)** where `S = sum(weights)`. Binary search runs `log₂(S)` iterations; predicate is `O(n)`. **Space O(1)** — pointers and accumulators. Tradeoff: brute force tries `c = max(weights), max(weights)+1, …` linearly until feasible — `O(n S)`. Parametric search trades that for `O(n log S)`. Best/avg/worst all `O(n log S)` — no input shortcuts the binary search."

---

## 11. The parametric-search defense sentence

In Mock #2 (Week 9), if you draw a parametric problem, the interview tell is whether you state the four elements *out loud, in order*, before writing code:

1. The **reframe** — "find the smallest `k` such that [property]."
2. The **interval** — `lo = …`, `hi = …`, with one-line justification each.
3. The **predicate** — `feasible(k)` returns True iff [property], and is monotone because [reason].
4. The **return** — post-loop `lo` is the answer because [post-loop invariant].

That is the cadence. Memorize the shape. Drill 5 is a script for delivering it.

> "Reframe: find the smallest rate `k` such that Koko finishes within `h` hours.
> Interval: `lo = 1` (must eat *some* bananas per hour); `hi = max(piles)` (at this rate every pile finishes in one hour, so total hours = n ≤ h).
> Predicate: `feasible(k)` returns True iff the total hours needed at rate `k` is `≤ h`. Monotone because a larger `k` never increases the per-pile hour count.
> Return: the post-loop value of `lo` is the smallest `k` where `feasible` is True — i.e., the minimum viable rate."

That paragraph is ~25 seconds spoken aloud. Practice it.

---

## 12. Self-check

Without notes, answer:

1. **What are the two preconditions for binary search on the answer?** (Bounded integer answer space and a monotone predicate.)
2. **State the canonical template for "find smallest k with `feasible(k) = True`."** (Half-open: `lo, hi = ...; while lo < hi: mid = lo + (hi-lo)//2; if feasible(mid): hi = mid else: lo = mid + 1; return lo`.)
3. **How do you choose `hi`?** (Pick a value such that `feasible(hi)` is True by construction — the trivial upper bound. Pick `lo` as the smallest meaningful answer.)
4. **What is the total complexity of parametric search?** (`O(P · log M)` where `P` is the predicate cost and `M` is the answer-space width.)
5. **State the monotonicity claim for Koko Bananas.** (A larger rate never increases the hours required per pile; therefore the total hours is non-increasing in `k`; therefore the predicate `total_hours <= h` flips from False to True at most once.)
6. **When does parametric search not apply?** (When the predicate is not monotone, or when the answer space has no integer bounds, or when there is no `feasible` you can compute polynomially.)

If you can answer all six without hesitation, proceed to the drills.

---

## 13. Why this is the highest-yield interview skill

Parametric search is the *premium* binary-search application. Most candidates can pass a sorted-array find-target test. Few can recognize parametric search on a problem that does not even mention an array.

The interview math: every Phase 2 mock and onsite includes at least one binary-search problem. The classic ones (variants 1-3) are graded as "expected"; the parametric ones (variant 4) are graded as "shows the candidate understands what binary search is *for*." If you ship Week 5 with parametric search in your hands, you are statistically distinguishable from the median candidate at the same level.

The drill: Drill 5 (Koko) and Homework Problem 1 (Ship Capacity) and Mini-Project Problem 4 and 5 are all parametric. Five at-bats this week. By Sunday the reframe-interval-predicate-return cadence should be reflexive.

---

## Further reading

- **Codeforces EDU — "Binary Search," Step 2 ("Searching for the answer")**: <https://codeforces.com/edu/course/2/lesson/6/2> — the cleanest free treatment.
- **LeetCode 875, 1011, 410, 378, 1631, 1552** — six parametric problems covering all four sub-patterns. Drills and homework use four of them; the others are stretch.
- **Wikipedia — Parametric search**: <https://en.wikipedia.org/wiki/Parametric_search> — the formal name comes from optimization theory; the article is more general than interview practice but the framing is the same.

Next: the [drills](../exercises/README.md). Drill 5 (Koko) is the canonical parametric problem of the week — do not skip it. Then the [challenge](../challenges/challenge-01-median-of-two-sorted-arrays.md) — Median of Two Sorted Arrays, the hardest binary-search application in the standard repertoire.
