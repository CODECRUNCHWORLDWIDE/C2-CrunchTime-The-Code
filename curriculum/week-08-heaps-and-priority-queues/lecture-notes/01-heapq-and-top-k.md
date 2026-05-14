# Lecture 1 — `heapq` and the Top-k Template

> **Duration:** ~2 hours.
> **Outcome:** You can write the canonical `heapq` operations from memory, defend the min-heap invariant out loud, implement the size-k top-k template in under five minutes, and explain why `O(n log k)` beats `O(n log n)` when `k << n`.

Last week installed DFS — the recursion-driven graph traversal whose invariant is the visited set. This lecture installs the **heap** — a small, sharp data structure whose invariant is *partial order*. The CPython implementation is `heapq` (`Lib/heapq.py`), a min-heap stored as a flat list, with `heappush` and `heappop` running in `O(log n)`.

By the end of this lecture you should be able to read a problem and, within 30 seconds, say one of three things out loud: "heap — top-k template," "heap — heap-of-tuples for custom key (covered in Lecture 2)," or "heap — running statistic on a stream (covered in Lecture 3)." The fourth thing — "this is *not* a heap problem, here is why" — is just as important and is graded in the quiz.

This lecture covers the foundation: the `heapq` API, the heap invariant, the top-k template, and the four common bugs. Lecture 2 covers custom keys via tuples and the k-closest-points pattern. Lecture 3 covers two-heap (running median), k-way merge, and lazy deletion.

---

## 1. What a heap is

A **binary heap** is a complete binary tree in which every parent is in a fixed order relation with its children. In a **min-heap**, every parent is `<=` its children — so the root is the smallest element in the tree. In a **max-heap**, every parent is `>=` its children — so the root is the largest.

The key engineering trick is that a complete binary tree can be stored as a **flat array** with no pointers. Index 0 is the root; the children of index `i` live at `2i + 1` and `2i + 2`; the parent of index `i` lives at `(i - 1) // 2`. This index arithmetic is what makes `heapq` a *list* rather than a tree of nodes.

Visualization on `[1, 3, 5, 4, 8, 9, 7]`:

```
            1                  array index:  0
           / \                 array value:  [1, 3, 5, 4, 8, 9, 7]
          3   5
         / \ / \
        4  8 9  7
```

Read the array left-to-right; that is the tree level-order. The heap invariant holds: `1 <= 3, 1 <= 5, 3 <= 4, 3 <= 8, 5 <= 9, 5 <= 7`. The root (`1`) is the minimum.

The pattern's power comes from one observation:

> **The heap invariant is *partial* — it constrains parent-child pairs but says nothing about siblings. This makes both insertion (sift-up) and extraction (sift-down) `O(log n)` rather than `O(n)`, because we only walk one root-to-leaf or leaf-to-root path, not the whole tree.**

Three corollaries:

1. **The minimum is always at index 0** (for a min-heap). Reading the minimum is `O(1)` — no traversal needed.
2. **Inserting a new element is `O(log n)`** — append to the end, then sift up by swapping with the parent while the heap invariant is violated. The path length is bounded by the tree height, which is `log₂ n`.
3. **Extracting the minimum is `O(log n)`** — swap the root with the last element, shrink the array by one, then sift the new root down by swapping with the smaller child while the invariant is violated. Same `log₂ n` argument.

The hard part this week is **not** the algorithm — `heapq.heappush` and `heappop` are one-line wrappers around the sift functions. The hard part is the *Match-step recognition*: half of all heap problems do not say "heap" anywhere in the prompt. They say "top k," "k closest," "median of a stream," "merge sorted lists." Owning the recognition is the work.

---

## 2. The canonical `heapq` operations

```python
import heapq
from typing import Iterable, List

# 1. Build a heap from an existing list (in place; O(n)).
arr: List[int] = [5, 3, 8, 1, 4, 9, 2]
heapq.heapify(arr)
# arr is now a valid min-heap; arr[0] == 1.

# 2. Insert (O(log n)).
heapq.heappush(arr, 0)
# arr[0] == 0 after the sift-up.

# 3. Extract the minimum (O(log n)).
minimum = heapq.heappop(arr)
# minimum == 0; arr[0] is the next-smallest.

# 4. Peek (O(1)).
top = arr[0]
# top is the current minimum; no removal.

# 5. Push then pop in one heap pass (O(log n), cheaper than separate calls).
prev_min = heapq.heappushpop(arr, 100)
# 100 is pushed; the minimum is popped; one sift, not two.

# 6. Pop then push in one heap pass (O(log n)).
prev_min2 = heapq.heapreplace(arr, 50)
# The minimum is popped first; 50 is pushed; assumes arr is non-empty.

# 7. Top-k largest from an iterable (O(n log k) with a size-k min-heap).
largest_3 = heapq.nlargest(3, [5, 3, 8, 1, 4, 9, 2])
# largest_3 == [9, 8, 5]

# 8. Top-k smallest from an iterable.
smallest_3 = heapq.nsmallest(3, [5, 3, 8, 1, 4, 9, 2])
# smallest_3 == [1, 2, 3]
```

Eight operations. Memorize the shapes; you will use four of them on most problems.

Six observations:

1. **`heapq` is min-only.** Every operation extracts the *smallest* element by default. To simulate a max-heap, negate the keys (`heapq.heappush(h, -x)`; `x = -heapq.heappop(h)`). Lecture 2 covers this in detail.
2. **`heapify(arr)` is `O(n)`, not `O(n log n)`.** This is Floyd's bottom-up construction — sift down from the last internal node up to the root. The proof is in the Wikipedia "Building a heap" section; the intuition is that most nodes are near the bottom and have short sift-down paths.
3. **`heappushpop` and `heapreplace` are strictly cheaper** than separate `heappush` + `heappop` calls because they do one heap pass instead of two. The size-k top-k template uses `heappushpop` in its tightest form.
4. **`arr[0]` is the canonical peek**, with `O(1)` cost. There is no `heappeek` function — the convention is to read the slot directly.
5. **All operations mutate the list in place.** `heapify(arr)` does not return a new list; it modifies `arr`. This is intentional but trips up beginners.
6. **Heap-of-tuples works out of the box.** Tuples are compared lexicographically; `heappush(h, (3, "task"))` works because Python knows how to compare `(3, "task")` and `(5, "other")`. Lecture 2 covers the tiebreaker convention that prevents `TypeError` when payloads are not comparable.

### Time and space

- **`heappush`, `heappop`, `heappushpop`, `heapreplace`: `O(log n)`** per call. Every operation walks one root-to-leaf or leaf-to-root path; the heap has height `log₂ n`.
- **`heapify`: `O(n)`** per call. Floyd's bottom-up. The proof is that the total work across all sift-downs sums to a geometric series bounded by `n`.
- **`arr[0]` (peek): `O(1)`.** Direct array access.
- **Space: `O(n)`** for the heap itself; no auxiliary structures.

Say the time defense out loud every time:

> "**`heappush` and `heappop` are `O(log n)`** because each walks one root-to-leaf path; the heap has height `log₂ n` since it is a complete binary tree. **`heapify` is `O(n)`** by Floyd's bottom-up argument — most nodes are near the bottom and have short sift-down paths; the total work is a geometric series bounded by `n`. **Peek is `O(1)`** — direct read of `h[0]`. **Space is `O(n)`** for the heap. Trade against sorting: a heap maintains *partial* order with `O(log n)` insert; sorting establishes *total* order in `O(n log n)`. If you only need the minimum or the top-k repeatedly, the heap is strictly cheaper."

That is the sentence interviewers grade. Memorize the cadence.

---

## 3. The heap invariant — said cleanly

The heap invariant is the **invariant** of `heapq`. The interview defense:

> "A min-heap is an array `h` such that `h[parent(i)] <= h[i]` for every valid index `i`, where `parent(i) = (i - 1) // 2`. Equivalently, `h[i] <= h[2i+1]` and `h[i] <= h[2i+2]` whenever the children exist. This is a *partial* order — siblings are unconstrained — which is what makes both insertion and extraction `O(log n)` rather than `O(n)`. The minimum is always at `h[0]`; reading it is `O(1)`. The invariant is restored after every `heappush` (by sift-up) and every `heappop` (by sift-down). Without the invariant, `heappop` would have to scan the entire array — `O(n)` per call — and the heap would be no faster than a list."

Memorize that paragraph. It is roughly 30 seconds spoken aloud. In a mock interview, it is what the interviewer wants to hear during your Match step on any heap problem.

---

## 4. The top-k template — the highest-leverage idiom

This is the single most important template this week. Memorize it.

**Problem shape.** Given a stream or list of `n` elements, find the `k` largest (or `k` smallest, or `k` closest, or `k` most frequent). The trap is that the obvious solution — sort the array and take the last `k` — is `O(n log n)`. The heap-based solution is `O(n log k)`, strictly cheaper when `k << n`.

**Template.**

```python
import heapq
from typing import Iterable, List

def top_k_largest(it: Iterable[int], k: int) -> List[int]:
    """Return the k largest elements from it, in unspecified order.

    Maintains a size-k min-heap. Push each new element; if the heap exceeds
    size k, pop the minimum. The heap always contains the k largest elements
    seen so far.
    """
    if k <= 0:
        return []
    h: List[int] = []
    for x in it:
        if len(h) < k:
            heapq.heappush(h, x)
        else:
            # heappushpop: cheaper than heappush + heappop.
            heapq.heappushpop(h, x)
    return h
```

Eleven lines. Memorize the shape.

Six observations:

1. **The heap is *bounded* at size k.** The `if len(h) < k` branch fills the heap; the `else` branch maintains the bound. The heap never grows larger than k.
2. **The heap is a *min*-heap holding the *largest* k elements.** This is the discriminator that trips up beginners. The minimum of the heap is the *smallest* of the k largest — which is exactly the element to evict when a new candidate arrives.
3. **`heappushpop` is the optimization.** The naive version is `heappush(h, x); heappop(h)` — two heap passes, `2 log k` work. `heappushpop` does it in one pass, `log k` work. For `n = 10⁶` and `k = 100`, the saving is meaningful.
4. **The return order is *unspecified*.** The heap layout is not sorted; if the problem asks for sorted output, append a `sorted(h)` step.
5. **For top-k *smallest*, flip the heap to a max-heap** (negate keys) and use the symmetric template. Or call `heapq.nsmallest(k, it)`, which internally does exactly this.
6. **`heapq.nlargest(k, it)` is the built-in version.** Know it exists; the manual implementation is what gets asked in interviews. The built-in uses the same `O(n log k)` template internally.

### Why `O(n log k)` beats `O(n log n)`

The defense sentence:

> "Sorting the full array is `O(n log n)` — total order on all `n` elements. We only need `k` of them. The heap maintains *partial* order at size `k`; each new element does at most `O(log k)` work (a push-then-pop on a size-k heap). Total: `O(n log k)`. For `n = 10⁶` and `k = 100`, `n log k ≈ 6.6 × 10⁶` vs `n log n ≈ 2 × 10⁷` — about 3× faster. For `k = 10`, about 6× faster. As `k` approaches `n`, the heap loses its advantage and `sorted(...)` becomes simpler — at `k = n/2`, they are roughly equal; at `k = n`, the heap is slightly worse due to constant factors."

This is the senior signal: knowing not just *that* the heap is faster, but *when* it stops being faster. If a problem has `k` close to `n`, sort.

### Why not quickselect?

Quickselect (Hoare's partition-based selection) finds the k-th element in `O(n)` expected time — strictly better than `O(n log k)`. So why use a heap?

Three reasons:

1. **Worst-case `O(n²)`.** Quickselect's pivot can degenerate; introselect (the algorithm behind `numpy.partition`) bounds this at `O(n)` worst case but is harder to implement from scratch.
2. **Not streaming-friendly.** Quickselect needs the full array in memory. The heap supports `n = ∞` streams; quickselect does not.
3. **The interviewer asks for "the k largest," not "the k-th largest."** Quickselect gives you the k-th element and (with extra work) the partition of the array into top-k and bottom-(n-k). The heap gives you the top-k directly as a list. The end-product matters.

In practice: use the heap for streams and "top-k as a list" questions; consider quickselect when `k = 1` (find the median, find the k-th largest) and the input fits in memory. Most interviewers accept the heap.

---

## 5. The four common bug patterns

Heaps have fewer off-by-one bugs than binary search and fewer subtle state bugs than DFS, but the four patterns here cover ~90% of incorrect submissions. Recognize them.

### Bug 1 — using a max-heap mental model with a min-heap implementation

```python
import heapq
# Goal: find the 3 LARGEST elements.
h = []
for x in [5, 3, 8, 1, 4, 9, 2]:
    if len(h) < 3:
        heapq.heappush(h, x)
    elif x < h[0]:                  # WRONG comparison direction
        heapq.heappushpop(h, x)
print(h)                            # Prints [1, 2, 3] -- the 3 smallest, not largest
```

The fix: when keeping the k largest in a *min*-heap, the new candidate enters iff it is **larger** than the heap's minimum.

```python
elif x > h[0]:                      # correct
    heapq.heappushpop(h, x)
```

The mental model trap is "min-heap, so I keep the smallest" — wrong. The min-heap is the *eviction* structure; the smallest is the *next candidate to evict*. The senior framing: "the heap holds the k largest seen so far; the min of the heap is the bar to clear."

### Bug 2 — forgetting that `heapq` is min-only

```python
import heapq
# Goal: find the LARGEST element repeatedly.
h = [3, 1, 4, 1, 5, 9, 2]
heapq.heapify(h)
print(heapq.heappop(h))             # Prints 1 -- the MINIMUM, not the maximum
```

The fix is one of:

1. **Negate the keys:** `heapq.heappush(h, -x)`; `largest = -heapq.heappop(h)`.
2. **Use `heapq.nlargest(k, it)`** for one-shot top-k.
3. **Wrap items in a reverse-`__lt__` class** (more verbose, more readable).

The negation is the idiomatic Python solution; the wrapper is the idiomatic Java solution. Both are accepted.

### Bug 3 — comparing custom objects without a tiebreaker

```python
import heapq

class Task:
    def __init__(self, name: str, priority: int) -> None:
        self.name = name
        self.priority = priority

h = []
heapq.heappush(h, (3, Task("A", 3)))
heapq.heappush(h, (3, Task("B", 3)))  # raises TypeError on the comparison
```

Two tuples with equal first element fall through to comparing the second elements. `Task` does not implement `__lt__`, so Python raises `TypeError`. The fix is a tiebreaker.

```python
counter = 0
heapq.heappush(h, (3, counter, Task("A", 3))); counter += 1
heapq.heappush(h, (3, counter, Task("B", 3))); counter += 1
```

The counter is unique and `int`-comparable, so equal priorities never reach the `Task` comparison. Lecture 2 covers this in detail.

### Bug 4 — building a heap with `heapq.heappush` in a loop instead of `heapify`

```python
import heapq
arr = [5, 3, 8, 1, 4, 9, 2]
h = []
for x in arr:
    heapq.heappush(h, x)
```

This is `O(n log n)` — every push is `O(log n)`, and there are `n` of them. The fix:

```python
import heapq
arr = [5, 3, 8, 1, 4, 9, 2]
heapq.heapify(arr)                  # O(n) in place
```

`heapify` is `O(n)` by Floyd's bottom-up argument. For large inputs, this is the difference between `n log n` and `n` — meaningful at `n = 10⁶`. Asymptotically: `n log n / n = log n`, so the speedup is logarithmic in `n`.

The interview-tell move: **mention `heapify` in Plan** when the input is already a list. *"I will call `heapify` on the input — `O(n)` — rather than push elements one at a time, which would be `O(n log n)`."*

---

## 6. Worked example end-to-end: Kth Largest Element in an Array (LC 215)

We will work this in full UMPIRE, abbreviated. Exercise 1 is this exact problem.

**[U — 1 minute]**

> "I am given an integer array `nums` and an integer `k`. Return the *k-th* largest element in the array. Note that this is the k-th in sorted order, not the k-th distinct element. Walk an example: `nums = [3, 2, 1, 5, 6, 4]`, `k = 2`. Sorted descending: `[6, 5, 4, 3, 2, 1]`. The 2nd largest is `5`. Constraint: `1 <= k <= len(nums) <= 10⁵`."

**[M — 30 seconds]**

> "Top-k pattern. The 30-second memo: *size-k min-heap. The heap holds the k largest elements seen so far; the minimum of the heap is the k-th largest. After processing all `n` elements, return `h[0]`. Why not `sorted(nums)[-k]`: `O(n log n)` vs the heap's `O(n log k)` — strictly faster when `k << n`. Why not quickselect: `O(n)` expected but `O(n²)` worst-case; the heap is the safer interview answer.*"

**[P — 1 minute]**

> "Initialize: empty heap `h`. For each `x in nums`: if `len(h) < k`, push; else if `x > h[0]`, `heappushpop`. After the loop, return `h[0]`. Edge case: `len(nums) == k` — the heap fills exactly and `h[0]` is the minimum of all elements, which is the k-th largest. Edge case: `k == 1` — the heap has one element; `h[0]` is the running maximum. Edge case: `k == len(nums)` — the heap holds every element; `h[0]` is the global minimum."

**[I — 2 minutes]**

```python
import heapq
from typing import List

def find_kth_largest(nums: List[int], k: int) -> int:
    """Return the k-th largest element via a size-k min-heap."""
    h: List[int] = []
    for x in nums:
        if len(h) < k:
            heapq.heappush(h, x)
        elif x > h[0]:
            heapq.heappushpop(h, x)
    return h[0]
```

**[R — 1 minute]**

> "Trace on `nums = [3, 2, 1, 5, 6, 4]`, `k = 2`. Iter 1: `len(h)=0 < 2`, push 3. h=[3]. Iter 2: push 2. h=[2, 3]. Iter 3: `len(h) == 2`; 1 < 2 so skip. Iter 4: 5 > 2; heappushpop(5). h=[3, 5]. Iter 5: 6 > 3; heappushpop(6). h=[5, 6]. Iter 6: 4 < 5; skip. Return h[0] = 5. Correct.
> Trace on `nums = [3, 2, 3, 1, 2, 4, 5, 5, 6]`, `k = 4`. Sorted desc: `[6, 5, 5, 4, 3, 3, 2, 2, 1]`. 4th largest is `4`. After processing: h should be `[4, 5, 5, 6]` in some order. h[0] = 4. Correct.
> Edge case `nums = [1], k = 1`: h = [1] after iter 1; return 1. Correct."

**[E — 1 minute]**

> "**Time `O(n log k)`** — n elements, each does at most `log k` work (a push-then-pop on a size-k heap). **Space `O(k)`** — the heap holds at most k elements. Best case `O(n log k)` — we always have to read all n. Worst case `O(n log k)`. **Tradeoff vs sorting**: `O(n log k)` vs `O(n log n)`. For `n = 10⁵`, `k = 100`: `n log k ≈ 6.6 × 10⁵`, `n log n ≈ 1.6 × 10⁶`. About 2.5× faster. **Tradeoff vs quickselect**: `O(n)` expected but `O(n²)` worst. The heap is safer; the interview-grade answer."

That is UMPIRE on Kth Largest, end-to-end, in about 6 minutes. The exercise is to do this every time.

---

## 7. The 30-second recognition signals

Stop. Read the prompt slowly. Ask these in order:

1. **Does the prompt say "top k," "k largest," "k smallest," "k most frequent"?** Strong signal — top-k template with a size-k heap. This lecture.
2. **Does the prompt say "k closest" or "k nearest"?** Top-k variant with a distance key. Lecture 2.
3. **Does the prompt say "median," "running statistic," or "support `add` and query"?** Two-heap pattern. Lecture 3.
4. **Does the prompt say "merge k sorted lists" or "merge k streams"?** k-way merge. Lecture 3.
5. **Does the prompt say "schedule the next task" or "execute by priority"?** Scheduler pattern — heap of ready tasks. Lecture 3.
6. **Does the prompt say "shortest path on a weighted graph"?** Dijkstra — uses a heap as the frontier. Out of scope this week; covered in C5.
7. **Does the prompt say "the largest element"?** A heap is overkill — `max(arr)` is `O(n)` and simpler.

The 30-second decision tree:

```
prompt mentions "top k" / "k largest" / "k smallest" / "k most frequent"?
├── Yes ──→ size-k min-heap (top-k template; this lecture)
└── No
    ├── "k closest" / "k nearest"                ──→ top-k variant with distance key (Lecture 2)
    ├── "median" / "running statistic"           ──→ two-heap (Lecture 3)
    ├── "merge k sorted"                         ──→ k-way merge with heap of size k (Lecture 3)
    ├── "schedule the next task"                 ──→ scheduler / heap-with-cooldown (Lecture 3)
    ├── "shortest path, weighted, non-negative"  ──→ Dijkstra (C5)
    ├── "the maximum" (just one)                 ──→ NOT a heap; use max() / min()
    └── otherwise — re-read; the pattern is probably not a heap
```

This decision tree is what we want in muscle memory by Sunday.

---

## 8. The defense sentence

In Mock #2 (Week 9), if you draw a top-k problem, the interview tell is whether you can **defend the size-k heap choice in one sentence, on demand**.

> "The heap is a size-k min-heap holding the k largest seen so far. The minimum of the heap is the bar to clear — any new candidate either falls below it (skip) or pushes through (`heappushpop`). Total work is `O(n log k)` — n elements, each at most `O(log k)`. This is strictly cheaper than sorting (`O(n log n)`) when `k << n`. Space is `O(k)`."

That is the cadence interviewers want. Memorize the shape, plug in the names. The cadence carries across all three exercises and the mini-project.

---

## 9. When a heap does not apply

Equally important: knowing when to *reject* the pattern.

- **You need *all* elements in sorted order.** Use sorting (`sorted(arr)`). A heap can produce them one at a time via repeated `heappop`, but that is `O(n log n)` — identical to sorting — and the sorted output is the cleaner answer.
- **You need *random access*.** A heap supports min / push / pop, not "give me the third-smallest in `O(1)`." For random access, use a sorted array or a balanced BST.
- **`k` is close to `n`.** At `k = n/2`, the heap and sorting are roughly tied. At `k = n`, sorting is simpler. The heap shines when `k << n`.
- **You need to *update an existing key's priority*.** `heapq` does not support efficient key updates. Use lazy deletion (Lecture 3) — mark the old entry stale and push the new one — or switch to a custom data structure (Fibonacci heap, indexed heap).
- **You need a *bounded* data structure with eviction.** A heap is one option; `collections.OrderedDict` (for LRU) or `collections.deque(maxlen=k)` (for sliding window) is often simpler.

Recognizing the *negative space* of the pattern matters as much as the positive recognition. Quiz Q3, Q7 are negative-space questions.

---

## 10. Self-check

Without notes, answer:

1. **What is the heap invariant?** (For a min-heap: `h[i] <= h[2i+1]` and `h[i] <= h[2i+2]` whenever the children exist. Equivalently, every parent is `<=` its children. The root is the global minimum.)
2. **What is the time complexity of `heappush`, `heappop`, and `heapify`?** (`heappush`: `O(log n)`. `heappop`: `O(log n)`. `heapify`: `O(n)` by Floyd's bottom-up argument — not `O(n log n)`.)
3. **Why is `heappushpop` cheaper than `heappush` followed by `heappop`?** (One heap pass instead of two. The fused operation pushes the new element only if it would not immediately be popped — saving a sift-up that would be undone by the subsequent sift-down.)
4. **What is the top-k template's complexity, and why?** (`O(n log k)`. The heap is bounded at size `k`; each of `n` elements does at most `O(log k)` work.)
5. **When does `O(n log k)` lose its advantage over `O(n log n)`?** (When `k` is close to `n`. At `k = n/2` the two are roughly tied. At `k = n` sorting is simpler. The heap shines when `k << n`.)
6. **How do you simulate a max-heap with `heapq`?** (Negate keys on push, negate again on pop. Or wrap items in a class with `__lt__` reversed. The negation is more idiomatic in Python.)

If you can answer all six without hesitation, proceed to [Lecture 2 — Heap of Tuples and k-Closest](./02-heap-of-tuples-and-k-closest.md).

---

## 11. A short tour of the CPython source

Time well spent: open `Lib/heapq.py` in your editor and read the top 100 lines. The module is short (about 600 lines including the docstring), well-commented, and conceptually clear.

Key functions, in the order you should read them:

- **`heappush(heap, item)`** — appends `item` to the list, then calls `_siftdown(heap, 0, len(heap) - 1)`. The "sift down" name is misleading; in this codebase, it walks an item *upward* toward the root. CPython's naming has historical reasons. (Roughly lines 130-150 in current CPython.)
- **`heappop(heap)`** — pops the last item, swaps it into the root, returns the old root, then calls `_siftup(heap, 0)` to restore the invariant. (Roughly lines 150-180.)
- **`_siftdown(heap, startpos, pos)`** — walks `pos` upward (yes, despite the name) by repeatedly swapping with the parent while the invariant is violated. (Roughly lines 160-200.)
- **`_siftup(heap, pos)`** — walks `pos` downward by repeatedly swapping with the smaller child while the invariant is violated. (Roughly lines 200-240.)
- **`heapify(x)`** — calls `_siftup` from the last internal node down to index 0; this is Floyd's bottom-up `O(n)` construction.
- **`nlargest(n, iterable, key=None)`** — uses a size-n min-heap internally; the exact template from §4.
- **`nsmallest(n, iterable, key=None)`** — symmetric; uses a size-n max-heap (via a wrapping `_HeapItem` class internally).
- **`merge(*iterables, key=None, reverse=False)`** — k-way merge; uses a heap of size k.

The total reading is 30 minutes well spent. After it, `heapq` stops being a black box.

---

## 12. Worked example: a streaming top-k with a callback

A small variant that tests whether you really own the template. The problem: a stream emits integers one at a time; after each integer, return the current top-k. We cannot store all of them (the stream is unbounded).

```python
import heapq
from typing import Callable, Iterable, List

def streaming_top_k(stream: Iterable[int], k: int, on_top_k: Callable[[List[int]], None]) -> None:
    """Maintain a running top-k of the stream; call on_top_k after each element."""
    if k <= 0:
        return
    h: List[int] = []
    for x in stream:
        if len(h) < k:
            heapq.heappush(h, x)
        elif x > h[0]:
            heapq.heappushpop(h, x)
        # h now contains the top-k of everything seen so far.
        on_top_k(sorted(h, reverse=True))
```

Thirteen lines. Two observations:

1. **The heap layout is not sorted.** The callback wants a sorted view; we `sorted(h, reverse=True)` for that — `O(k log k)` per emission, which is fine because `k` is small.
2. **Memory is bounded at `O(k)`** regardless of stream length. This is the streaming property — a heap-based top-k works on infinite streams; a sort-based top-k does not.

The senior framing: "size-k heap + bounded memory + streaming-friendly" is exactly the combination most real-world top-k problems want. The interview problem (find the k largest in a list) is the simplest case; the streaming variant is the production application.

---

## 13. Why this is the highest-yield Phase-2 data structure

Heaps are the *partial-order* data structure — and partial order is the engineering trick that makes priority queues, schedulers, and streaming statistics fast. Every Phase-2 mock includes at least one problem whose intended solution is a heap; the capstone (Week 15) has one or two.

For Phase 2 interview prep specifically, heaps show up in:

- Mock #2 (Week 9): at least one heap problem is the median allocation, usually top-k or k-closest.
- The capstone (Week 15): the "Heap (Priority Queue)" tag is on the "patterns you must own" list.
- Every FAANG onsite: one streaming-statistic or top-k question; sometimes two.
- C5 (graph algorithms): Dijkstra's algorithm uses a min-heap as its frontier — same `heapq` template, different framing.

The drill: Exercises 1-3 cover top-k, k-closest, and two-heap median. Homework problems 1-2 reinforce. The mini-project writes one top-k + one two-heap write-up. Six at-bats this week. By Sunday the "top-k / closest / median / merge / schedule" cadence should be reflexive.

---

## Further reading

- **`heapq` module — Python docs**: <https://docs.python.org/3/library/heapq.html> — the canonical reference; the module docstring is the cleanest free source.
- **Binary heap — Wikipedia**: <https://en.wikipedia.org/wiki/Binary_heap> — covers the array layout, sift operations, and the `O(n)` heapify proof.
- **CPython `Lib/heapq.py`**: <https://github.com/python/cpython/blob/main/Lib/heapq.py> — read the first 240 lines; the sift functions are the heart of the module.
- **LeetCode 215, 347, 692, 973, 295** — five problems that anchor the heap families. Exercises cover three of them; the others are stretch.

Next: [Lecture 2 — Heap of Tuples and k-Closest](./02-heap-of-tuples-and-k-closest.md).
