# Lecture 2 — Heap of Tuples and k-Closest

> **Duration:** ~2 hours.
> **Outcome:** You can write the heap-of-tuples idiom with a correct tiebreaker from memory, defend why the tiebreaker is mandatory, implement the k-closest-points template via a size-k max-heap, and choose between negation and the wrapper class for max-heap semantics.

Lecture 1 installed the `heapq` API and the top-k template for plain integers. This lecture installs the **heap-of-tuples idiom** — the convention that lets a heap store `(priority, tiebreaker, payload)` triples so the payload can be anything (a string, a 2-D point, a custom object). Every real-world heap holds tuples, not bare integers. The discipline you install this lecture is the one most interview submissions get subtly wrong.

The two applications we cover end-to-end: **k-closest-points-to-origin** (the canonical Phase-2 heap problem; LC 973) and a custom-priority **task queue** (the production-engineering framing). Both rest on the same idiom.

---

## 1. Why heap-of-tuples

A bare-integer heap is a teaching device. Real problems have *keys* and *payloads*:

- "Find the 100 most-frequent words" — key is the count; payload is the word.
- "Find the 5 closest points to the origin" — key is the distance; payload is the `(x, y)` pair.
- "Find the next task to run" — key is the priority (or deadline); payload is the task object.

In Python, the natural representation is a tuple: `(key, ..., payload)`. The heap compares items lexicographically — first by element 0, then element 1, then element 2 — so the first slot determines the order. This works **out of the box** for `heapq` because tuples implement `__lt__` from the standard library.

```python
import heapq
from typing import List, Tuple

# Heap entries: (count, word). Sorts by count, then alphabetically by word.
h: List[Tuple[int, str]] = []
heapq.heappush(h, (3, "banana"))
heapq.heappush(h, (5, "apple"))
heapq.heappush(h, (3, "apple"))

print(heapq.heappop(h))   # (3, "apple") — count 3 wins, "apple" < "banana"
print(heapq.heappop(h))   # (3, "banana")
print(heapq.heappop(h))   # (5, "apple")
```

Notice: when two items have equal count (`3`), the heap falls through to comparing the second slot (`"apple"` vs `"banana"`). Strings have a natural `__lt__`, so the comparison succeeds. The output order is "stable in the lexicographic sense" — equal counts produce alphabetical order.

This is the **good** case. The bad case is when the payload does not have a natural `__lt__`.

---

## 2. The tiebreaker — the rule that prevents `TypeError`

```python
import heapq
from typing import Any

class Task:
    def __init__(self, name: str, priority: int) -> None:
        self.name = name
        self.priority = priority

h = []
heapq.heappush(h, (3, Task("A", 3)))
heapq.heappush(h, (3, Task("B", 3)))
# TypeError: '<' not supported between instances of 'Task' and 'Task'
```

Two tuples have equal first elements. The heap falls through to comparing the second — `Task("A", 3) < Task("B", 3)`. `Task` does not implement `__lt__`. Python raises `TypeError`.

The **tiebreaker rule**: when payloads are not naturally comparable, insert a unique, comparable slot *between* the priority and the payload.

```python
import heapq
from typing import List, Tuple, Any

counter = 0
h: List[Tuple[int, int, Any]] = []

def push(priority: int, payload: Any) -> None:
    global counter
    heapq.heappush(h, (priority, counter, payload))
    counter += 1

push(3, Task("A", 3))
push(3, Task("B", 3))
push(1, Task("C", 1))

while h:
    p, _, t = heapq.heappop(h)
    print(p, t.name)
# Prints:
# 1 C
# 3 A
# 3 B  (FIFO order among equal priorities because the counter is monotonically increasing)
```

The counter guarantees uniqueness, gives a deterministic order, and is `int`-comparable. The heap never reaches the payload comparison.

Three rules for tiebreakers:

1. **Always unique.** A duplicate tiebreaker re-triggers payload comparison. Use a monotonic counter or `id(obj)`.
2. **Always comparable.** `int` is the safe default. `str` works if the choice is meaningful (e.g., alphabetical ordering among ties). `float` works but introduces `nan`-comparison risk.
3. **Insertion order = FIFO** when the tiebreaker is a monotonically increasing counter. Random tiebreakers (e.g., `id(obj)`) give arbitrary order; deliberate tiebreakers (e.g., a secondary natural key) give the order the problem asks for.

The interview defense:

> "I use a `(priority, counter, payload)` tuple in the heap. The counter is a monotonically increasing integer; it guarantees the heap never reaches the payload comparison, which would `TypeError` because my payload class does not implement `__lt__`. The counter also gives FIFO order among equal priorities — which the spec required."

Memorize that sentence. It is the single most common heap-of-tuples question in interviews.

---

## 3. Simulating a max-heap

Python's `heapq` is min-only. There are two idiomatic ways to get max-heap semantics.

### Way 1 — negate the key (idiomatic Python)

```python
import heapq
from typing import List

# Max-heap of integers via negation.
h: List[int] = []
for x in [3, 1, 4, 1, 5, 9, 2, 6]:
    heapq.heappush(h, -x)

while h:
    print(-heapq.heappop(h))
# Prints 9, 6, 5, 4, 3, 2, 1, 1 — descending order.
```

Three observations:

- **Negation works for numeric keys only.** For strings or custom keys, this does not apply.
- **Negate on push *and* on pop.** Forgetting the second negation is a common bug.
- **For tuples, negate the priority slot.** `heapq.heappush(h, (-priority, counter, payload))`. The negation is local to the priority; the tiebreaker and payload are unchanged.

### Way 2 — wrap in a class with reversed `__lt__` (idiomatic Java, more readable)

```python
from dataclasses import dataclass, field
from typing import Any
import heapq

@dataclass(order=True)
class MaxItem:
    """Wrap a value so that 'less than' is reversed — max-heap semantics."""
    key: int
    payload: Any = field(compare=False)

    def __lt__(self, other: "MaxItem") -> bool:  # type: ignore[override]
        return self.key > other.key

h = []
for x in [3, 1, 4, 1, 5, 9, 2, 6]:
    heapq.heappush(h, MaxItem(x, payload=f"item-{x}"))

while h:
    item = heapq.heappop(h)
    print(item.key, item.payload)
# Prints in descending order of key.
```

Six observations:

- **The `dataclass(order=True)` generates `__lt__`** based on field order, but we override it to reverse the comparison.
- **`payload` is `compare=False`** — the heap never compares payloads, so the wrapper does not need them to be `__lt__`-able.
- **The wrapper is more verbose** but more readable when the data has a non-numeric key or multiple keys.
- **The wrapper composes** — a max-heap of complex objects is the wrapper's natural use case.
- **Use negation for numeric one-shot heaps**; use the wrapper for complex heaps with multiple fields.
- **Performance:** the wrapper is slightly slower because every comparison goes through a Python method call instead of a built-in integer comparison. For `n < 10⁵`, the difference is invisible.

In interviews, the negation is the faster answer to write. Mention the wrapper alternative; implement the negation.

---

## 4. The k-closest-points template

The canonical Phase-2 heap problem. LC 973, Exercise 2.

**Problem.** Given `n` points on a 2-D plane and an integer `k`, return the `k` points closest to the origin `(0, 0)`. Distance is Euclidean (but we use distance-*squared* to avoid `sqrt`).

**The setup.**

- Each point is `[x, y]`.
- The priority is `x² + y²` (distance squared). We do not take the square root — it is monotone, so it does not change the order, and avoiding it eliminates floating-point error.
- We want the `k` *closest* points — the `k` with the *smallest* priorities.

**Two valid implementations.**

### Implementation A — max-heap of size k (the production idiom)

The senior approach: keep a size-k *max*-heap. The maximum of the heap is the "farthest of the k closest" — the bar to clear. Any new point with smaller distance evicts it.

```python
import heapq
from typing import List

def k_closest_max_heap(points: List[List[int]], k: int) -> List[List[int]]:
    """Return the k closest points to the origin via a size-k max-heap."""
    if k <= 0:
        return []
    # Max-heap via negation: store (-dist_sq, x, y).
    h: List[tuple] = []
    for x, y in points:
        d2 = x * x + y * y
        if len(h) < k:
            heapq.heappush(h, (-d2, x, y))
        elif -d2 > h[0][0]:
            # The new point is closer than the current farthest of the k.
            heapq.heappushpop(h, (-d2, x, y))
    return [[x, y] for (_, x, y) in h]
```

Fifteen lines. Memorize the shape.

- **Heap stores `(-d2, x, y)`** — negated distance to simulate a max-heap.
- **`len(h) < k` fills the heap;** `else` branch maintains the bound.
- **`-d2 > h[0][0]`** means the new point's *negated* distance is *larger* than the heap-root's negated distance — equivalently, the new point's *actual* distance is *smaller*. The new point is closer; evict the farthest.
- **Tiebreaker:** `(x, y)` is implicitly the tiebreaker. Coordinates are `int`, so they compare cleanly. No explicit counter needed.
- **`O(n log k)` time, `O(k)` space.** This is the streaming-friendly answer.

### Implementation B — min-heap of all `n`, pop `k`

A simpler implementation that runs in `O(n + k log n)`. Useful when `k` is close to `n`.

```python
import heapq
from typing import List

def k_closest_min_heap(points: List[List[int]], k: int) -> List[List[int]]:
    """Return the k closest points via a global min-heap of size n."""
    if k <= 0:
        return []
    h: List[tuple] = [(x * x + y * y, x, y) for x, y in points]
    heapq.heapify(h)              # O(n)
    return [[x, y] for (_, x, y) in heapq.nsmallest(k, h)]
```

Six lines. `heapify` is `O(n)`; `nsmallest` is `O(n log k)` internally but in this case operates on an already-heapified list which makes it slightly faster.

**Choosing between them.**

| Condition | Better choice |
|-----------|---------------|
| `k << n` (e.g., `k = 10`, `n = 10⁵`) | Max-heap of size k — `O(n log k)` |
| `k ≈ n` (e.g., `k = n/2`) | Min-heap of all n — `O(n + k log n)` |
| Streaming input (unknown `n`) | Max-heap of size k — `O(k)` memory |
| Input fits in memory and `n` is small | Either; pick what reads cleaner |

The discriminating senior signal: name both, defend the one you chose.

### Implementation C — `heapq.nsmallest` with a key function

The one-line answer:

```python
import heapq
from typing import List

def k_closest_nsmallest(points: List[List[int]], k: int) -> List[List[int]]:
    """One-liner using heapq.nsmallest with a key function."""
    return heapq.nsmallest(k, points, key=lambda p: p[0] * p[0] + p[1] * p[1])
```

`heapq.nsmallest` internally maintains a size-k max-heap (via a private `_HeapItem` wrapper) — exactly the template from Implementation A. The one-liner is what production code looks like; the manual implementation is what interviews grade.

The senior framing: "I would write the manual version in an interview to demonstrate the template; in production I would use `nsmallest` because it's tested and reads cleanly."

---

## 5. The four common bugs in heap-of-tuples

### Bug 1 — forgetting the tiebreaker

Covered in §2. The fix is a monotonic counter.

### Bug 2 — sorting the heap with `sorted()` and assuming it stays a heap

```python
import heapq
h = [3, 1, 4, 1, 5]
heapq.heapify(h)
# h is now a valid heap.
h.sort()
# h is now a sorted list. It is also a valid heap (sorted -> heap), but the
# heap-order is now coincidentally also sorted. Future heappushes may break this.
heapq.heappush(h, 0)
# h is still a valid heap (sift-up restored the invariant).
# But h is no longer sorted -- it never had to be.
```

The trap: a sorted list happens to be a valid heap, but a valid heap is **not** necessarily sorted. Beginners sort the heap, get the "right" answer for one query, then break when subsequent inserts disrupt the (coincidentally) sorted order.

The fix: never `sorted()` a heap. If you need a sorted view, pop everything: `result = [heapq.heappop(h) for _ in range(len(h))]`. This is `O(n log n)` — the same as sorting from scratch.

### Bug 3 — using `pop()` instead of `heapq.heappop()`

```python
import heapq
h = [3, 1, 4, 1, 5]
heapq.heapify(h)
minimum = h.pop(0)        # WRONG -- removes h[0] but does not restore the invariant
```

`list.pop(0)` removes the first element in `O(n)` (it shifts everything). It also does not restore the heap invariant — the new `h[0]` is whatever was at `h[1]`, which may violate the invariant against `h[3]` and `h[4]`.

The fix: always use `heapq.heappop(h)`. It pops the minimum, swaps the last element to position 0, shrinks the list, then sifts down to restore the invariant. `O(log n)`.

### Bug 4 — comparing tuples with negated keys, then forgetting to negate on read

```python
import heapq
h = []
for x in [3, 1, 4, 1, 5]:
    heapq.heappush(h, (-x, x))     # Max-heap via negation of the priority slot

while h:
    largest = heapq.heappop(h)[0]
    print(largest)
# Prints -5, -4, -3, -1, -1 -- negated values
```

The fix: negate on read.

```python
while h:
    largest = -heapq.heappop(h)[0]
    print(largest)
# Prints 5, 4, 3, 1, 1
```

Or, more cleanly, store the original value in a later slot:

```python
heapq.heappush(h, (-x, x))         # priority is -x, payload is x

while h:
    _, original = heapq.heappop(h)
    print(original)
```

The senior framing: store both the comparison key and the original value when they differ. Reading the original off the payload slot is cleaner than re-negating.

---

## 6. A scheduler with priorities — the production framing

The interview problem (LC 973) is one shape. The production application is another: a job scheduler that runs the next-highest-priority task. The same heap-of-tuples idiom powers both.

```python
import heapq
from typing import Any, List, Tuple

class PriorityQueue:
    """A priority queue with a stable tiebreaker.

    Items with lower priority value run first. Among equal priorities, items
    are processed in FIFO insertion order.
    """

    def __init__(self) -> None:
        self._h: List[Tuple[int, int, Any]] = []
        self._counter: int = 0

    def push(self, priority: int, payload: Any) -> None:
        heapq.heappush(self._h, (priority, self._counter, payload))
        self._counter += 1

    def pop(self) -> Any:
        """Remove and return the highest-priority (lowest-value) payload."""
        if not self._h:
            raise IndexError("pop from empty PriorityQueue")
        _, _, payload = heapq.heappop(self._h)
        return payload

    def peek(self) -> Any:
        """Return the highest-priority payload without removing it."""
        if not self._h:
            raise IndexError("peek from empty PriorityQueue")
        return self._h[0][2]

    def __len__(self) -> int:
        return len(self._h)
```

Six methods, 25 lines. The class is tested in the SOLUTIONS file. Two things worth noticing:

1. **The counter survives across calls** as an instance attribute. A bare `counter = 0` at module scope would be shared across instances — a subtle bug.
2. **The tiebreaker is FIFO** (monotonic counter). For LIFO (last-in-first-out among equal priorities), use a *decreasing* counter (`self._counter -= 1` and start at `0`).

This is the structural foundation of every priority-driven scheduler — operating system schedulers, network packet schedulers, GUI event loops. The same six-method API; only the priority function changes.

---

## 7. Worked example end-to-end: K Closest Points (LC 973)

We will work this in full UMPIRE, abbreviated. Exercise 2 is this exact problem.

**[U — 1 minute]**

> "I am given a list of `points`, each `[x, y]`, and an integer `k`. Return the `k` points closest to the origin `(0, 0)`. Distance is Euclidean. The answer can be in any order. Walk an example: `points = [[1, 3], [-2, 2]], k = 1`. Distances-squared: `1 + 9 = 10` and `4 + 4 = 8`. Closest: `[-2, 2]`. Constraints: `1 <= k <= n <= 10⁴`; coordinates fit in `int`."

**[M — 30 seconds]**

> "Top-k variant with a distance key. The 30-second memo: *size-k max-heap. Priority is `-d²` (negate to simulate a max-heap with `heapq`). The heap holds the `k` closest seen so far; the root (most negative `-d²`, equivalently largest `d²`) is the farthest of the `k` — the bar to clear. Any new point with smaller `d²` evicts it. Why not sort: `O(n log n)` vs `O(n log k)`; the heap is strictly cheaper when `k << n`. Why not `nsmallest`: same algorithm internally; mention the one-liner alternative, implement the manual version to show the template.*"

**[P — 1 minute]**

> "Initialize: empty heap `h`. For each `[x, y] in points`: compute `d2 = x² + y²`. If `len(h) < k`, push `(-d2, x, y)`. Else if `-d2 > h[0][0]` (equivalently `d2 < -h[0][0]` — new point is closer), `heappushpop(h, (-d2, x, y))`. After the loop, return `[[x, y] for (_, x, y) in h]`. Tiebreaker: `(x, y)` coordinates compare cleanly. Edge case: `k == n` — heap fills exactly; every point is in the answer."

**[I — 2 minutes]**

```python
import heapq
from typing import List

def k_closest(points: List[List[int]], k: int) -> List[List[int]]:
    """Return the k points closest to the origin via a size-k max-heap."""
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

**[R — 1 minute]**

> "Trace on `points = [[1, 3], [-2, 2]], k = 1`. Iter 1: `len(h)=0 < 1`, push `(-10, 1, 3)`. h = `[(-10, 1, 3)]`. Iter 2: `d2 = 8`; `-8 > -10`? Yes. `heappushpop((-8, -2, 2))`. h = `[(-8, -2, 2)]`. Return `[[-2, 2]]`. Correct.
> Trace on `points = [[3, 3], [5, -1], [-2, 4]], k = 2`. Distances²: 18, 26, 20. Closest two: 18 and 20 (points `[3, 3]` and `[-2, 4]`). After processing: h should contain those two with `-d²` values `-18` and `-20`. h[0] is whichever is larger in negated form, i.e., `-18`. Return any order — both points are in the answer. Correct.
> Edge case `k == len(points)`: every point ends up in `h`. Heap holds all `n` points; return all of them. Correct."

**[E — 1 minute]**

> "**Time `O(n log k)`** — n points, each does at most `O(log k)` work (a push-then-pop on a size-k heap). **Space `O(k)`** — the heap holds at most k tuples. **Tradeoff vs sorting `sorted(points, key=...)[:k]`**: `O(n log k)` vs `O(n log n)`. For `n = 10⁴, k = 10`: `n log k ≈ 3 × 10⁴`, `n log n ≈ 1.3 × 10⁵`. About 4× faster. **Tradeoff vs `heapify` + `nsmallest`**: `O(n + k log n)`; competitive when `k` is close to `n`. **Improvement**: quickselect gives `O(n)` expected but `O(n²)` worst-case; not stream-friendly. The size-k heap is the safer interview answer."

That is UMPIRE on K Closest Points, end-to-end, in about 6 minutes.

---

## 8. The 30-second recognition signals (lecture 2 additions)

Building on Lecture 1's decision tree, add the heap-of-tuples discriminators:

1. **Does the prompt say "k closest" or "k nearest"?** Top-k with a distance key. Size-k max-heap.
2. **Does the prompt have a "natural priority" plus a payload?** Heap-of-tuples. Priority in slot 0; tiebreaker in slot 1; payload in slot 2.
3. **Does the prompt say "top k by frequency"?** Heap-of-tuples where slot 0 is the count. Use `collections.Counter(arr).items()` to get `(value, count)` pairs; push `(-count, value)` for a max-heap by count.
4. **Does the prompt require *stable* order among ties?** The monotonic counter tiebreaker is mandatory. Without it, the order among equal priorities is implementation-defined.
5. **Does the prompt have a *custom object* as the item?** The tiebreaker is mandatory unless the object implements `__lt__`. The senior answer: insert the counter; never rely on the payload's `__lt__`.

The 30-second decision tree (extended):

```
prompt mentions "k closest" / "k nearest"?
├── Yes ──→ size-k max-heap with distance key
└── No
    ├── "top k by frequency"                     ──→ heap-of-tuples; slot 0 = (-count)
    ├── "next task by priority"                  ──→ scheduler; heap-of-tuples + tiebreaker
    ├── "merge k sorted"                         ──→ k-way merge (Lecture 3)
    ├── "running median"                         ──→ two-heap (Lecture 3)
    └── otherwise — Lecture 3 or not-a-heap
```

---

## 9. Self-check

Without notes, answer:

1. **Why is the tiebreaker mandatory in a heap of `(priority, payload)` tuples?** (When two items share a priority, the heap falls through to comparing payloads. If payloads do not implement `__lt__`, Python raises `TypeError`. The tiebreaker is a unique, comparable slot that prevents the fall-through.)
2. **What is the canonical tiebreaker, and why?** (A monotonically increasing integer counter. Unique (counter never repeats), comparable (`int`), and gives FIFO order among equal priorities — which is usually what the spec wants.)
3. **What are the two ways to simulate a max-heap?** (Negate keys on push and pop; or wrap items in a class with `__lt__` reversed. Negation is more idiomatic in Python; the wrapper is more readable for complex multi-field keys.)
4. **What is the time complexity of the k-closest-points size-k max-heap solution?** (`O(n log k)` time, `O(k)` space. n points, each does at most `O(log k)` work.)
5. **When is `heapify + nsmallest` better than the size-k max-heap?** (When `k` is close to `n`. `heapify` is `O(n)`; `nsmallest(k)` adds `O(k log n)`. For `k = n`, total `O(n + n log n) = O(n log n)` — same as sorting. The size-k heap shines when `k << n`.)
6. **Why do we use distance-*squared* instead of distance?** (Distance squared is monotone with distance: `d1² < d2² ⟺ d1 < d2`. Skipping `sqrt` avoids floating-point error and is faster. The priority order is identical.)

If you can answer all six without hesitation, proceed to [Lecture 3 — Two-Heap, k-Way Merge, and Lazy Deletion](./03-two-heap-and-k-way-merge.md).

---

## 10. A small composition — k most frequent words

A composition of the heap-of-tuples and top-k templates. LC 692.

**Problem.** Given a list of words and an integer `k`, return the `k` most frequent words. If two words have the same frequency, the lexicographically smaller word ranks first.

**Why it is the canonical composition.** The frequency is the primary key; the alphabetical order is the *deterministic* tiebreaker (and it is *reversed* — smaller word ranks first, which means it should be "larger" in our heap-eviction sense).

```python
import heapq
from collections import Counter
from typing import List, Tuple


def top_k_frequent(words: List[str], k: int) -> List[str]:
    """Return the k most frequent words; ties broken alphabetically (smaller first)."""
    counts = Counter(words)
    # Size-k min-heap of (count, word) — but we want the k LARGEST counts.
    # When count ties, the smaller word should rank HIGHER (i.e., the LARGER
    # word should be evicted first). So we compare words in REVERSE order.
    # Trick: make the heap's "smallest" be the candidate for eviction.
    # Slot 0: count. We want largest count to win, so slot 0 holds count.
    # Slot 1: word. We want smaller word to win on ties; for a MIN-heap
    #         eviction model, the LARGER word should be the eviction candidate.
    #         So we store the word as-is, and the min-heap evicts the smaller
    #         (count, word) tuple — which is either smaller count OR same count
    #         with smaller word. The first is correct; the second is BACKWARDS.
    # Fix: negate the word's order by storing a reverse-comparable wrapper, or
    # restructure: use a max-heap-by-count, min-heap-by-word combined.
    # The cleanest version: sort the Counter items by (-count, word).
    return [w for w, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]]
```

For large `n`, the sort is `O(n log n)`. A pure-heap version is more involved because the count and word have *opposite* tiebreaker directions:

```python
def top_k_frequent_heap(words: List[str], k: int) -> List[str]:
    """Same problem; size-k heap with a custom comparator."""
    counts = Counter(words)
    # Size-k MIN-heap where the eviction candidate is the LOWEST (count, -word).
    # We negate the word's order by storing it as a NegStr wrapper, or simpler:
    # store (count, word) and on eviction, evict the LOWEST count; on ties,
    # evict the LARGEST word. That gives us a min-heap by (count, REVERSED-word).
    # Use a wrapper to reverse the word order in the comparison.
    h: List[Tuple[int, str]] = []
    for word, count in counts.items():
        # Compare entries as (count, -word). Since strings cannot be negated,
        # use a tuple-like wrapper that compares words in reverse.
        # Simplest path: build the heap of size > k with (count, word),
        # then sort the result. Acceptable for n <= 10⁵.
        pass
    # For clarity, fall back to the sort-based version in interviews unless
    # the interviewer explicitly asks for the pure-heap version.
    return [w for w, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]]
```

The senior framing in interviews: "The sort-based version is `O(n log n)` and obviously correct; the heap-based version is `O(n log k)` but requires a custom comparator because the two tiebreaker directions conflict. I would write the sort-based version first; if asked to optimize, I would write a `class Entry` with a reversed `__lt__` for the word slot."

This is the "name both, defend the choice" pattern from Lecture 1 §6, applied to a slightly harder problem.

---

## 11. Why this matters for Mock #2

The Match-step recognition graded in Mock #2 includes:

- "Is this top-k or top-1?" — top-1 is `max()`, not a heap.
- "Is this top-k or merge-k?" — top-k is a size-k heap; merge-k is a heap of size k *of streams* (Lecture 3).
- "Is the priority direction correct?" — beginners reverse it.
- "Is the tiebreaker correct?" — beginners forget it entirely.

The exercises this week drill all four. By Sunday, the heap-of-tuples reflex should be:

1. **Identify the priority slot.** (Count? Distance? Deadline? Custom?)
2. **Decide the direction.** (Min-heap for "smallest first"; max-heap via negation for "largest first.")
3. **Add the tiebreaker.** (Monotonic counter if FIFO is fine; a secondary natural key if the spec demands a specific order.)
4. **Choose the bounding strategy.** (Size-k for top-k; unbounded for full priority queue.)

Four decisions, made in 30 seconds, every time.

---

## Further reading

- **`heapq` examples — Python docs**: <https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes> — the "Priority Queue Implementation Notes" section is essentially this lecture in three paragraphs.
- **`dataclasses` decorator — Python docs**: <https://docs.python.org/3/library/dataclasses.html> — the `order=True` parameter generates `__lt__` automatically; useful for the wrapper-class approach.
- **LeetCode 973 (K Closest Points to Origin)**: the canonical k-closest problem; Exercise 2 covers this exactly.
- **LeetCode 692 (Top K Frequent Words)**: the canonical heap-of-tuples problem with a tiebreaker direction conflict.

Next: [Lecture 3 — Two-Heap, k-Way Merge, and Lazy Deletion](./03-two-heap-and-k-way-merge.md).
