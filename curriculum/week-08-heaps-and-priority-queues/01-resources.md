# Week 8 — Resources

Every resource is **free** and **publicly accessible**.

## Required reading (work it into your week)

- **`heapq` — Heap queue algorithm — Python docs**: <https://docs.python.org/3/library/heapq.html> — the canonical reference. Read the module docstring at the top and the "Examples" section. The first paragraph contains the cleanest one-sentence statement of the heap invariant in free material.
- **`heapq` source code — CPython `Lib/heapq.py`**: <https://github.com/python/cpython/blob/main/Lib/heapq.py> — about 600 lines including the docstring. The two functions to read are `_siftup` (lines roughly 200-240 in current CPython) and `_siftdown` (roughly 160-200). Together they implement the entire heap and run in `O(log n)` per call. Reading them once removes 90% of the mystery from the module.
- **Binary heap — Wikipedia**: <https://en.wikipedia.org/wiki/Binary_heap> — the textbook reference; the "Building a heap" section explains why `heapify` is `O(n)`, not `O(n log n)`. This is a question that gets asked in interviews.
- **PEP 8 (recurring)**: <https://peps.python.org/pep-0008/>
- **Big-O Cheat Sheet (recurring)**: <https://www.bigocheatsheet.com/>

## On the pattern itself

A heap is described under many names. The recognition skill is mapping the surface form to the underlying pattern:

- **Binary heap** — the textbook data structure. Complete binary tree, heap-order invariant.
- **Priority queue** — the abstract data type a heap implements. "Insert with priority, extract the minimum (or maximum)."
- **`heapq`** — Python's implementation. Min-heap stored as a flat list. The default; what you reach for first.
- **`PriorityQueue`** — the thread-safe wrapper in `queue.PriorityQueue`. Slower; use `heapq` unless you need cross-thread safety.
- **Fibonacci heap, pairing heap, d-ary heap** — alternative implementations with different asymptotics. Out of scope for interviews; mentioned only so you can name them.
- **Top-k pattern** — "find the k largest / k smallest of n elements." The canonical heap application; `O(n log k)`.
- **k-closest pattern** — "find the k points closest to the origin / k strings most similar to the query." Same shape as top-k, with a distance / similarity key.
- **Two-heap pattern (running median)** — "support `add(x)` and `median()` on a stream." Max-heap of the lower half, min-heap of the upper half, balanced.
- **k-way merge** — "merge k sorted streams into one sorted stream." Heap of size k, one element per source.
- **Lazy deletion** — "remove an arbitrary element from a heap" without `O(n)` linear search. Mark stale; skip on pop.
- **Scheduler pattern** — "execute the next task by some priority, with a cooldown or readiness condition." Heap of ready tasks, queue of cooling-down tasks.

If a write-up mentions "top," "largest," "smallest," "closest," "median," or "merge sorted" — it is almost certainly a heap problem. If it mentions "shortest path on a weighted graph" — it is Dijkstra, which also uses a heap (covered in C5).

## Free practice platforms

- **LeetCode — Heap (Priority Queue) tag** (free): <https://leetcode.com/tag/heap-priority-queue/>
- **LeetCode — Top K Frequent Elements**: <https://leetcode.com/problems/top-k-frequent-elements/> — the canonical top-k problem; Exercise 1 variant.
- **HackerRank — Heap domain**: <https://www.hackerrank.com/domains/data-structures?filters%5Bsubdomains%5D%5B%5D=heap>
- **Codeforces — Data structures tag**: <https://codeforces.com/problemset?tags=data+structures> — filter for heap / priority-queue problems.
- **CSES Problem Set — Sorting and Searching section**: <https://cses.fi/problemset/> — several problems whose intended solution is a heap or a multiset.

## On the `heapq` API specifically

The eight operations you should know cold.

| Operation | Signature | Complexity | One-liner mnemonic |
|-----------|-----------|-----------:|--------------------|
| `heappush(h, x)` | push `x`, restore invariant | `O(log n)` | sift-up |
| `heappop(h)` | pop and return the min | `O(log n)` | swap, sift-down |
| `heapify(arr)` | convert list to heap in place | `O(n)` | Floyd's bottom-up |
| `heappushpop(h, x)` | push `x` then pop; one heap pass | `O(log n)` | fused; cheaper than separate calls |
| `heapreplace(h, x)` | pop then push `x`; one heap pass | `O(log n)` | fused; assumes h is non-empty |
| `nlargest(k, it)` | top-k largest from iterable | `O(n log k)` | size-k min-heap internally |
| `nsmallest(k, it)` | top-k smallest from iterable | `O(n log k)` | size-k max-heap internally |
| `merge(*iterables)` | k-way merge of sorted iterables | `O(N log k)` | heap of size k internally |

`heappushpop` and `heapreplace` are the operations beginners do not know exist. They are strictly cheaper than `heappush` followed by `heappop` because they do one heap pass instead of two. The size-k top-k template uses `heappushpop` in its tightest form:

```python
import heapq
from typing import Iterable, List

def top_k(it: Iterable[int], k: int) -> List[int]:
    """Return the k largest elements from it, in unspecified order."""
    h: List[int] = []
    for x in it:
        if len(h) < k:
            heapq.heappush(h, x)
        else:
            heapq.heappushpop(h, x)
    return h
```

Ten lines. Memorize the shape. The `heappushpop` in the else branch is the optimization most beginners miss.

## On the heap-of-tuples idiom

The single most important interview convention.

```python
import heapq
from typing import List, Tuple

# Priority queue of tasks: lower priority value runs first.
# Tuple shape: (priority, tiebreaker, payload).
counter = 0
h: List[Tuple[int, int, str]] = []
for priority, name in [(5, "B"), (3, "A"), (3, "C")]:
    heapq.heappush(h, (priority, counter, name))
    counter += 1

while h:
    p, _, name = heapq.heappop(h)
    print(p, name)
# Prints: 3 A, 3 C, 5 B (stable on insertion order via the counter tiebreaker)
```

The **tiebreaker** matters when two items have equal priority and the payload is not naturally comparable. Common tiebreakers:

- An incrementing counter (gives FIFO order among equal priorities; the example above).
- `id(payload)` (gives an arbitrary but stable order; cheaper than a counter).
- A secondary natural key from the payload (e.g., the index in the original list).

Without a tiebreaker, comparing two tasks with equal priority would fall through to comparing the payloads themselves. If the payload is a custom object that does not implement `__lt__`, Python raises `TypeError: '<' not supported between instances of 'Task' and 'Task'`. The tiebreaker is the convention that prevents this.

## On the two-heap median pattern

The cleanest illustration of `heapq` being min-only.

```python
import heapq
from typing import List

class MedianFinder:
    """Running median of a stream of integers."""

    def __init__(self) -> None:
        # Max-heap of the lower half (negate values to simulate max-heap).
        self.lower: List[int] = []
        # Min-heap of the upper half.
        self.upper: List[int] = []

    def add_num(self, num: int) -> None:
        # Push to lower (as negative), then move the largest to upper.
        heapq.heappush(self.lower, -num)
        heapq.heappush(self.upper, -heapq.heappop(self.lower))
        # Rebalance: keep |lower| >= |upper|.
        if len(self.upper) > len(self.lower):
            heapq.heappush(self.lower, -heapq.heappop(self.upper))

    def find_median(self) -> float:
        if len(self.lower) > len(self.upper):
            return float(-self.lower[0])
        return (-self.lower[0] + self.upper[0]) / 2.0
```

Six methods, two heaps. The negation trick (`-num` going in, `-` again coming out) is how you simulate a max-heap with `heapq`. The rebalance discipline (`|lower| - |upper| in {0, 1}`) is the invariant. Memorize both.

## On lazy deletion

The trick that turns "remove an arbitrary element from a heap" from `O(n)` to amortized `O(log n)`.

```python
import heapq
from typing import List, Set

class LazyHeap:
    """Heap that supports lazy deletion via a 'removed' set."""

    def __init__(self) -> None:
        self.h: List[int] = []
        self.removed: Set[int] = set()
        self.size = 0

    def push(self, x: int) -> None:
        heapq.heappush(self.h, x)
        self.size += 1

    def remove(self, x: int) -> None:
        """Mark x as removed; the next pop will skip it."""
        self.removed.add(x)
        self.size -= 1

    def pop(self) -> int:
        while self.h and self.h[0] in self.removed:
            self.removed.discard(self.h[0])
            heapq.heappop(self.h)
        self.size -= 1
        return heapq.heappop(self.h)

    def peek(self) -> int:
        while self.h and self.h[0] in self.removed:
            self.removed.discard(self.h[0])
            heapq.heappop(self.h)
        return self.h[0]
```

The `removed` set is a hash set of stale items; `pop` and `peek` clean the top before returning. The amortized complexity is `O(log n)` per operation because every item is pushed and popped at most twice (once for real, once lazily).

For duplicate values, replace the `Set[int]` with a `Dict[int, int]` of (value -> stale count) and decrement on a real pop. The exercise SOLUTIONS file has the duplicates variant.

## On k-way merge

The canonical implementation.

```python
import heapq
from typing import Iterable, Iterator, List, Tuple

def k_way_merge(sources: List[List[int]]) -> Iterator[int]:
    """Merge k sorted lists into one sorted stream.

    Each source is a sorted list; the output yields elements in sorted order.
    """
    h: List[Tuple[int, int, int]] = []
    for i, src in enumerate(sources):
        if src:
            heapq.heappush(h, (src[0], i, 0))
    while h:
        val, src_i, idx = heapq.heappop(h)
        yield val
        if idx + 1 < len(sources[src_i]):
            nxt = sources[src_i][idx + 1]
            heapq.heappush(h, (nxt, src_i, idx + 1))
```

Ten lines. The heap holds at most k tuples — one per active source. The `src_i` and `idx` are stored so we know which source to refill from after each pop. The tiebreaker is the source index `src_i`, which prevents comparison from falling through to the payload (which here is an integer and would compare fine, but the discipline is what matters).

For an existing implementation, `heapq.merge(*sources)` does the same in one line. Know it exists; the manual implementation is what gets asked in interviews.

## Videos on the pattern (free, no signup)

- **NeetCode — "Heap / Priority Queue"** (YouTube — free): search "neetcode heap"; the 12-minute walkthrough is enough for the size-k template.
- **NeetCode — "Find Median from Data Stream"** (YouTube — free): the canonical two-heap problem; if you have not seen the pattern in video form, watch this before Exercise 3.
- **MIT 6.006 — Lecture on heaps and heapsort** (free OCW): <https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/> — the rigorous version; the proof that `heapify` is `O(n)` (not `O(n log n)`) is laid out cleanly.

## On the negation trick for max-heaps

Python's `heapq` is **min-only**. The standard trick to simulate a max-heap is to negate keys on the way in and out.

```python
import heapq
from typing import List

# Max-heap via negation.
h: List[int] = []
for x in [3, 1, 4, 1, 5, 9, 2, 6]:
    heapq.heappush(h, -x)

while h:
    print(-heapq.heappop(h))
# Prints 9, 6, 5, 4, 3, 2, 1, 1 — descending order.
```

For non-numeric keys, the cleaner pattern is to wrap the item in a small class with `__lt__` inverted:

```python
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class MaxItem:
    """Wrap a value so that 'less than' is reversed — for max-heap semantics."""
    key: int
    payload: Any = field(compare=False)

    def __lt__(self, other: "MaxItem") -> bool:  # type: ignore[override]
        return self.key > other.key
```

The wrapper is more verbose but more readable; the negation is more idiomatic in Python. Both are accepted in interviews. Pick negation unless the payload's natural `__lt__` matters.

## Glossary cheat sheet

Keep this tab open. Builds on Weeks 1-7.

| Term | One-line definition |
|------|---------------------|
| **Heap** | A complete binary tree maintained as an array with the heap-order invariant |
| **Min-heap** | Heap where every parent is `<=` its children; the root is the global minimum |
| **Max-heap** | Heap where every parent is `>=` its children; simulated in `heapq` via negation |
| **Heap invariant** | `h[i] <= h[2i+1]` and `h[i] <= h[2i+2]` for every valid `i` (min-heap) |
| **`heapq.heappush(h, x)`** | Insert `x` while maintaining the invariant; `O(log n)` |
| **`heapq.heappop(h)`** | Remove and return the minimum; `O(log n)` |
| **`heapq.heapify(arr)`** | Convert an arbitrary list to a heap *in place*; `O(n)` via Floyd's bottom-up |
| **`heapq.heappushpop(h, x)`** | Push then pop in a single heap pass; `O(log n)` |
| **`heapq.heapreplace(h, x)`** | Pop then push in a single heap pass; `O(log n)` |
| **`heapq.nlargest(k, it)`** | Top-k largest; internally a size-k min-heap |
| **`heapq.nsmallest(k, it)`** | Top-k smallest; internally a size-k max-heap |
| **`heapq.merge(*its)`** | k-way merge of sorted iterables; lazy iterator |
| **Heap-of-tuples** | `(priority, tiebreaker, payload)` idiom for custom-key heaps |
| **Tiebreaker** | The second slot in a heap-tuple; prevents `TypeError` on equal priorities |
| **Top-k template** | Size-k min-heap; push then `heappushpop`; `O(n log k)` |
| **Two-heap pattern** | Max-heap of lower half + min-heap of upper half; running median in `O(log n)` |
| **k-way merge** | Heap of size k, one element per source; `O(N log k)` |
| **Lazy deletion** | Mark stale, skip on pop; amortized `O(log n)` |

## What you will be glad you read

Three things, all short, all this week:

1. **The module docstring at the top of `Lib/heapq.py`** — ten minutes. The cleanest free explanation of the heap invariant and why the array layout works.
2. **The "Examples" section of the `heapq` docs** — five minutes. The `nlargest`, `nsmallest`, and `merge` examples are the templates you will reach for.
3. **Two LeetCode problem statements at the "Heap (Priority Queue)" tag** — five minutes each. Predict the algorithm before reading the solution. The recognition reps are what build Match-step muscle.

If you read nothing else this week, read those three and skim five problem titles in the LeetCode Heap tag.

---

*Broken link? Open an issue.*
