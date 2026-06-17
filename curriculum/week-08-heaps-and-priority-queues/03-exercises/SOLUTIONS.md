# Week 8 — Worked Solutions

Three worked solutions, each with UMPIRE narration. **Attempt every exercise on your own first.** If you read this file before drafting your own, you forfeit the recognition rep — and recognition is what Phase 2 is grading.

The solutions below are written in the same voice you should be using in your portfolio write-ups. Read them as templates, not as the answer.

---

## Solution 1 — Kth Largest Element in an Array (LC 215)

### Understand

We are given an integer array `nums` and an integer `k`. We must return the *k*-th largest element. The k-th in *sorted order*, meaning ties count toward the rank (e.g., the 2nd largest of `[7, 7, 7, 7]` is `7`, not "no answer").

Hand-walk `nums = [3, 2, 1, 5, 6, 4], k = 2`: sorted descending is `[6, 5, 4, 3, 2, 1]`; the 2nd is `5`.

### Match

Top-k pattern via a size-k min-heap. The 30-second memo:

> *Size-k min-heap. The heap holds the k largest values seen so far; the minimum of the heap (`h[0]`) is the k-th largest — the bar for new candidates. Why min-heap-for-largest: the min is the eviction bar. Why not `sorted(nums)[-k]`: `O(n log n)` vs `O(n log k)`; the heap wins when `k << n`. Why not quickselect: `O(n)` expected but `O(n²)` worst-case; the heap is the safer interview answer.*

### Plan

1. Initialize `h: List[int] = []`.
2. For each `x in nums`: if `len(h) < k`, `heappush(h, x)`. Else if `x > h[0]`, `heappushpop(h, x)`.
3. After the loop, return `h[0]`.

### Implement

```python
import heapq
from typing import List


def find_kth_largest(nums: List[int], k: int) -> int:
    h: List[int] = []
    for x in nums:
        if len(h) < k:
            heapq.heappush(h, x)
        elif x > h[0]:
            heapq.heappushpop(h, x)
    return h[0]
```

### Review

Trace 1 — `nums = [3, 2, 1, 5, 6, 4], k = 2`.

- x=3: h=[]; len<2; push. h=[3].
- x=2: h=[3]; len<2; push. h=[2, 3].
- x=1: h=[2,3]; 1 > 2? No. Skip.
- x=5: 5 > 2? Yes. heappushpop(5). h=[3, 5].
- x=6: 6 > 3? Yes. heappushpop(6). h=[5, 6].
- x=4: 4 > 5? No. Skip.
- Return h[0] = 5. Correct.

Trace 2 — `nums = [7, 7, 7, 7], k = 2`. After all four iterations, h=[7, 7]. Return 7. Ties handled correctly.

Common bug caught in Review: comparing `x < h[0]` instead of `x > h[0]`. That would keep the *smallest* k elements and `h[0]` would be the k-th *smallest* — the opposite of the spec. The defense sentence "the min is the eviction bar for the k LARGEST" prevents this.

### Evaluate

> **Time `O(n log k)`**: `n` iterations of the outer loop; each does at most one `heappushpop` of cost `O(log k)`.
>
> **Space `O(k)`**: the heap holds at most `k` elements.
>
> **Tradeoff vs sorting**: `sorted(nums)[-k]` is `O(n log n)`. The heap wins when `k << n`. For `n = 10⁵, k = 10`, the heap is about 5× faster.
>
> **Tradeoff vs quickselect**: quickselect is `O(n)` expected but `O(n²)` worst-case. The heap is the safer answer. In production, `heapq.nlargest(k, nums)[-1]` is the one-liner.

---

## Solution 2 — K Closest Points to Origin (LC 973)

### Understand

Given `points = [[x_i, y_i]]` and integer `k`, return the `k` points closest to the origin by Euclidean distance. Order in the answer is unspecified; the *set* of points is unique by spec.

Hand-walk `points = [[3, 3], [5, -1], [-2, 4]], k = 2`. Distances²: 18, 26, 20. The two smallest are 18 and 20 → points `[3, 3]` and `[-2, 4]`.

### Match

Top-k variant with a distance key — size-k max-heap (negated). The 30-second memo:

> *Size-k max-heap of `(-d², x, y)` tuples. The heap holds the k closest seen so far; the root (most-negative `-d²`, equivalently largest `d²`) is the farthest of the k — the eviction bar. Any new point with smaller `d²` replaces it. Why distance-squared: monotone with distance; skipping `sqrt` avoids float error. Why heap-of-tuples: the `x, y` coordinates ride along as the payload; integers tiebreak cleanly.*

### Plan

1. Initialize `h: List[tuple] = []`.
2. For each `(x, y)`: compute `d2 = x² + y²`. If `len(h) < k`, push `(-d2, x, y)`. Else if `-d2 > h[0][0]`, `heappushpop`.
3. Return `[[x, y] for (_, x, y) in h]`.

### Implement

```python
import heapq
from typing import List


def k_closest(points: List[List[int]], k: int) -> List[List[int]]:
    if k <= 0:
        return []
    h: List[tuple] = []
    for x, y in points:
        d2 = x * x + y * y
        if len(h) < k:
            heapq.heappush(h, (-d2, x, y))
        elif -d2 > h[0][0]:
            heapq.heappushpop(h, (-d2, x, y))
    return [[x, y] for (_, x, y) in h]
```

### Review

Trace 1 — `points = [[1, 3], [-2, 2]], k = 1`.

- (1, 3): d2=10. len<1; push (-10, 1, 3). h=[(-10, 1, 3)].
- (-2, 2): d2=8. -8 > -10? Yes. heappushpop. h=[(-8, -2, 2)].
- Return [[-2, 2]]. Correct.

Trace 2 — `points = [[3, 3], [5, -1], [-2, 4]], k = 2`.

- (3, 3): d2=18. push (-18, 3, 3). h=[(-18, 3, 3)].
- (5, -1): d2=26. push (-26, 5, -1). h=[(-26, 5, -1), (-18, 3, 3)] (min-heap ordering by first slot).
- (-2, 4): d2=20. -20 > -26? Yes (less negative). heappushpop (-20, -2, 4). The root (-26, 5, -1) is evicted; (-20, -2, 4) takes its place. h=[(-20, -2, 4), (-18, 3, 3)].
- Return [[-2, 4], [3, 3]]. Correct.

Common bug caught in Review: comparing `d2 < -h[0][0]` instead of `-d2 > h[0][0]`. Mathematically equivalent, but the negation discipline is what generalizes to other max-heap-by-key problems; mixing the two forms is the bug source.

### Evaluate

> **Time `O(n log k)`**: n points, each does at most one `heappushpop` of cost `O(log k)`.
>
> **Space `O(k)`**: heap holds at most k tuples.
>
> **Tradeoff vs `sorted(points, key=...)[:k]`**: `O(n log n)` vs `O(n log k)`. Heap wins when `k << n`.
>
> **Tradeoff vs `heapq.nsmallest(k, points, key=lambda p: p[0]**2 + p[1]**2)`**: same algorithm internally. Mention as the production one-liner; the manual implementation is what interviews grade.
>
> **Tradeoff vs `heapify(all) + nsmallest(k)`**: `O(n + k log n)`; competitive when `k` is close to `n`.

---

## Solution 3 — Find Median from Data Stream (LC 295)

### Understand

Design a class with two methods: `add_num(num)` adds an integer to the data structure; `find_median()` returns the median of all elements added so far. The stream can be long (up to 5 × 10⁴ calls); we cannot sort on every query.

Hand-walk: add 1, add 2, median is 1.5 (average of the two). Add 3, median is 2 (middle of three).

### Match

Two-heap pattern. The 30-second memo:

> *Max-heap `lower` of the smaller half (negated for `heapq`'s min-only semantics); min-heap `upper` of the larger half. Invariants: every `lower` element ≤ every `upper` element; size difference ≤ 1, with `lower` the larger when they differ. Median is `-lower[0]` (odd, lower bigger) or `(-lower[0] + upper[0]) / 2` (even). Why two heaps not a sorted list: `O(log n)` per add vs `O(n)`; `O(1)` per median.*

### Plan

1. Constructor: `self.lower: List[int] = []; self.upper: List[int] = []`.
2. `add_num(num)`:
   1. `heappush(lower, -num)` — tentative push to max-heap (negated).
   2. `heappush(upper, -heappop(lower))` — move the max of lower to upper. This maintains "every lower ≤ every upper" because the just-popped value is the previous max of lower.
   3. If `len(upper) > len(lower)`: `heappush(lower, -heappop(upper))` — rebalance.
3. `find_median()`:
   1. If `len(lower) > len(upper)`: return `-lower[0]` (cast to float).
   2. Else return `(-lower[0] + upper[0]) / 2`.

### Implement

```python
import heapq
from typing import List


class MedianFinder:

    def __init__(self) -> None:
        self.lower: List[int] = []   # max-heap (negated)
        self.upper: List[int] = []   # min-heap

    def add_num(self, num: int) -> None:
        heapq.heappush(self.lower, -num)
        heapq.heappush(self.upper, -heapq.heappop(self.lower))
        if len(self.upper) > len(self.lower):
            heapq.heappush(self.lower, -heapq.heappop(self.upper))

    def find_median(self) -> float:
        if len(self.lower) > len(self.upper):
            return float(-self.lower[0])
        return (-self.lower[0] + self.upper[0]) / 2.0
```

### Review

Trace 1 — add 1, 2; query.

- add 1: heappush(lower, -1). lower=[-1]. heappush(upper, -heappop(lower)) → heappush(upper, 1). lower=[], upper=[1]. len(upper)=1 > len(lower)=0 → heappush(lower, -heappop(upper)) → heappush(lower, -1). lower=[-1], upper=[].
- add 2: heappush(lower, -2). lower=[-2, -1] (min-heap of negatives; root is the most-negative -2). heappush(upper, -heappop(lower)) → heappop(lower) returns -2; heappush(upper, 2). lower=[-1], upper=[2]. Sizes balanced. No rebalance.
- find_median: len(lower)=1, len(upper)=1; even branch. Return (-(-1) + 2) / 2 = (1 + 2) / 2 = 1.5. Correct.

Trace 2 — continue, add 3.

- add 3: heappush(lower, -3). lower=[-3, -1] (root -3). heappush(upper, -heappop(lower)) → heappop returns -3; heappush(upper, 3). lower=[-1], upper=[2, 3]. len(upper)=2 > len(lower)=1 → heappush(lower, -heappop(upper)) → heappop(upper) returns 2; heappush(lower, -2). lower=[-2, -1], upper=[3].
- find_median: len(lower)=2, len(upper)=1; odd branch. Return -lower[0] = -(-2) = 2.0. Correct.

Trace 3 — single element. add 42. heappush(lower, -42). heappush(upper, -heappop(lower)) → upper=[42], lower=[]. Rebalance: lower gets it back. lower=[-42], upper=[]. find_median: len(lower)=1 > len(upper)=0 → return 42.0. Correct.

Common bug caught in Review: forgetting the negation on read. `return float(self.lower[0])` would return `-42`, not `42`. The discipline "every read of `lower[0]` must be negated" prevents this.

### Evaluate

> **Time `O(log n)` per `add_num`**: at most three heap operations, each `O(log n)` since heaps hold at most `n/2 + 1` elements.
>
> **Time `O(1)` per `find_median`**: direct array reads on `lower[0]` and `upper[0]`.
>
> **Space `O(n)`** for the two heaps combined.
>
> **Tradeoff vs single sorted list with bisect**: `bisect.insort` is `O(n)` per add (list-shift cost); query is `O(1)`. The two-heap is strictly cheaper for adds when adds dominate.
>
> **Tradeoff vs sorted multiset (e.g., a balanced BST)**: same `O(log n)` per add and `O(log n)` query; the two-heap is simpler to implement and CPython has no built-in balanced BST.
>
> **Extension**: for the sliding-window median variant (LC 480), combine the two-heap with lazy deletion (Lecture 3 §4) — mark the expiring element stale and clean the heap tops on query.

---

## What the three solutions have in common

The structural lesson of Week 8: every heap problem rests on the **same six operations** (`heappush`, `heappop`, `heapify`, `heappushpop`, `heapreplace`, `arr[0]` peek) plus **one invariant** (heap order). The differences are:

1. **Bounding** — size-k (Sol 1, Sol 2) vs unbounded (Sol 3).
2. **Direction** — min-heap natively (Sol 1) vs max-heap by negation (Sol 2, half of Sol 3).
3. **Tuple shape** — bare int (Sol 1), 3-tuple `(-d², x, y)` (Sol 2), bare-int-but-two-heaps (Sol 3).
4. **Operation count** — one pass through input (Sol 1, Sol 2) vs streaming with rebalance (Sol 3).

Read all three solutions side-by-side at least once. The structural parallels are what build the Match-step reflex.

---

## Up next

After all three exercises pass, run the [quiz](../05-quiz.md) and then start the [challenge](../04-challenges/challenge-01-merge-k-sorted-lists.md). The challenge is the canonical k-way merge — Lecture 3 §3 applied to linked lists.
