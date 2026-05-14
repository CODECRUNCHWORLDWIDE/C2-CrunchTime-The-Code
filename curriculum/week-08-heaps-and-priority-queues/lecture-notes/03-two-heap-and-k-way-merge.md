# Lecture 3 — Two-Heap, k-Way Merge, and Lazy Deletion

> **Duration:** ~2 hours.
> **Outcome:** You can write the two-heap running-median template from memory, defend the balance invariant out loud, implement k-way merge of sorted streams via a heap of size k, and apply lazy deletion to maintain a heap under arbitrary removal in amortized `O(log n)`.

Lectures 1 and 2 installed the size-k template and the heap-of-tuples idiom. This lecture installs the **three patterns that ship the rest of Phase-2 heap work**:

- **Two-heap pattern** — a running median (and other order-statistic) maintained as a stream of integers arrives. Max-heap of the lower half; min-heap of the upper half; balanced.
- **k-way merge** — merge `k` sorted streams into one sorted output. Heap of size `k`, one element per active source.
- **Lazy deletion** — remove an arbitrary element from a heap in amortized `O(log n)` by marking it stale and skipping on pop. The trick that turns the "heap update" problem from `O(n)` into a one-liner.

These three patterns plus the size-k template from Lecture 1 cover every Phase-2 heap problem you will see in mocks or the capstone.

---

## 1. The two-heap pattern — running median

The canonical problem (LC 295): support `add_num(x)` and `find_median()` on a stream of integers. Both operations should be cheap (sub-linear). The intended solution is two heaps.

### The setup

Conceptually, partition the stream into two halves:

- The **lower half** — the smaller values seen so far.
- The **upper half** — the larger values seen so far.

If we can keep the lower half in a *max-heap* (so we can peek the maximum of the lower half in `O(1)`) and the upper half in a *min-heap* (so we can peek the minimum of the upper half in `O(1)`), then:

- **The median is either the top of one heap (if the total count is odd) or the average of the two tops (if even).** `O(1)` to read.
- **Inserting a new value** is `O(log n)` — push to the appropriate heap, then rebalance.
- **The invariant** is that the two heap sizes differ by at most 1.

### The template

```python
import heapq
from typing import List


class MedianFinder:
    """Running median of a stream of integers.

    Invariants:
    - `lower` is a MAX-heap (stored with negated values, since heapq is min-only).
      It holds the smaller half of the stream seen so far.
    - `upper` is a MIN-heap. It holds the larger half.
    - |len(lower) - len(upper)| <= 1.
    - When the sizes differ, `lower` is the larger heap.
    """

    def __init__(self) -> None:
        self.lower: List[int] = []   # max-heap (negated)
        self.upper: List[int] = []   # min-heap

    def add_num(self, num: int) -> None:
        # Step 1: tentatively push to `lower` (negated for max-heap semantics).
        # Step 2: move the max of `lower` to `upper`, to maintain the
        #         "lower's max <= upper's min" invariant.
        # Step 3: if `upper` has grown larger than `lower`, move one back.
        heapq.heappush(self.lower, -num)
        heapq.heappush(self.upper, -heapq.heappop(self.lower))
        if len(self.upper) > len(self.lower):
            heapq.heappush(self.lower, -heapq.heappop(self.upper))

    def find_median(self) -> float:
        if len(self.lower) > len(self.upper):
            return float(-self.lower[0])
        return (-self.lower[0] + self.upper[0]) / 2.0
```

20 lines. Memorize the shape.

Five observations:

1. **`lower` stores negated values.** `heapq.heappush(self.lower, -num)` puts the value in. `-self.lower[0]` reads the max back out. Forgetting either negation is the most common bug.
2. **The push-then-rebalance is a *three-step* pattern**: push to `lower`, move `lower`'s max to `upper`, then rebalance sizes. This guarantees the invariant "every element of `lower` is `<=` every element of `upper`" because the moved element is the largest in `lower` after the push.
3. **The size invariant prefers `lower`** when the total count is odd. This is convention — you could symmetrically prefer `upper`. Pick one and stick with it; both work, but mixing them is a bug.
4. **`find_median` is `O(1)`** — direct array reads on `self.lower[0]` and `self.upper[0]`. No heap operations.
5. **`add_num` is `O(log n)`** — at most three heap operations per call, each `O(log n)`.

### Why this works — the invariant defense

> "The two-heap invariant has three parts. First, every element of `lower` is `<=` every element of `upper` — proved by induction on insertions: each `add_num` pushes to `lower` then moves `lower`'s max to `upper`, so the maximum of `lower` after the move is at most the minimum of `upper` (because the just-moved element was the previous `lower`-max, and the new `lower`-max is smaller). Second, the size difference is at most 1, and `lower` is the larger heap when they differ — maintained by the explicit rebalance. Third, the median is either `lower[0]` (odd count) or the average of `lower[0]` and `upper[0]` (even count) — direct from the partition definition. Both `add_num` and `find_median` are `O(log n)` and `O(1)` respectively; together they meet the spec's per-operation cost requirement."

Memorize that paragraph. It is the 45-second interview defense.

### Two common bugs

**Bug A — pushing directly without the rebalance hop.**

```python
def add_num_wrong(self, num: int) -> None:
    if not self.lower or num <= -self.lower[0]:
        heapq.heappush(self.lower, -num)        # smaller; goes to lower
    else:
        heapq.heappush(self.upper, num)         # larger; goes to upper
    # NOTE: the rebalance step is missing -- this is the bug.
```

The problem: after enough inserts, one heap can grow arbitrarily larger than the other and the median becomes wrong. The fix is the explicit size rebalance at the end.

**Bug B — forgetting that `lower` is negated.**

```python
def find_median_wrong(self) -> float:
    if len(self.lower) > len(self.upper):
        return float(self.lower[0])              # WRONG: returns -num, not num
    return (self.lower[0] + self.upper[0]) / 2.0
```

`self.lower[0]` is the *negated* value (the most-negative number, since `lower` is a min-heap of negated values). Reading it directly gives `-max(lower)`, not `max(lower)`. The fix is `-self.lower[0]`.

The senior framing: when a heap stores negated values, *every* read of `h[0]` must be negated. Document this with a comment on the field declaration to make the discipline visible.

---

## 2. Two-heap extensions — order statistics beyond the median

The two-heap pattern generalizes from the *median* (the 50th percentile) to any *fixed-percentile* order statistic.

### The 75th percentile

Maintain a 3:1 size ratio between `lower` and `upper`. The 75th percentile is the boundary.

```python
class PercentileFinder:
    """Running approximate 75th percentile."""

    def __init__(self) -> None:
        self.lower: List[int] = []   # max-heap; 75% of stream
        self.upper: List[int] = []   # min-heap; 25% of stream

    def add_num(self, num: int) -> None:
        heapq.heappush(self.lower, -num)
        heapq.heappush(self.upper, -heapq.heappop(self.lower))
        # Maintain 3:1 ratio (approximately).
        while 3 * len(self.upper) > len(self.lower):
            heapq.heappush(self.lower, -heapq.heappop(self.upper))

    def find_p75(self) -> float:
        if not self.lower:
            return 0.0
        return float(-self.lower[0])
```

The asymptotic cost is the same — `O(log n)` per insert. The constant factor and the exact rebalance are different.

### "Sliding window median" — two heaps plus lazy deletion

The harder variant: a sliding window of size `w` over a stream; report the median of the current window after each insertion. The window expires older elements as new ones arrive.

The naive approach — re-build the two heaps from scratch after each slide — is `O(n × w)`. The clever approach uses **lazy deletion** (§4) to remove expired elements from the heaps without paying the `O(n)` linear-search cost.

We will cover this in §4. The senior framing is that the two-heap pattern + lazy deletion is the canonical Phase-3 problem in this family.

---

## 3. k-way merge

The canonical problem (LC 23): merge `k` sorted lists into one sorted list. The Phase-2 framing: "merge `k` sorted streams."

### The setup

Each source emits values in sorted order. We want to emit *all* values across all sources in global sorted order.

The brute-force approach — concatenate then sort — is `O(N log N)` where `N` is the total element count. It ignores the structure (each source is already sorted).

The heap-based approach is `O(N log k)`:

1. Initialize a heap with one element from each source.
2. Pop the minimum (the smallest unemitted element across all sources). Emit it.
3. Push the *next* element from the source that just emitted, if any.
4. Repeat until the heap is empty.

The heap holds at most `k` elements at any time — one per active source. Each `heappush`/`heappop` is `O(log k)`. There are `N` total pops. Total: `O(N log k)`.

### The template

```python
import heapq
from typing import Iterator, List, Tuple


def k_way_merge(sources: List[List[int]]) -> Iterator[int]:
    """Merge k sorted lists into one sorted stream.

    Each source is a sorted list. The output yields elements in global sorted
    order, lazily — no materialization of the full merged list.

    Tuple shape: (value, source_index, element_index).
    The source_index is the tiebreaker — prevents comparison fall-through to
    the element_index (which would also work but is less explicit).
    """
    h: List[Tuple[int, int, int]] = []
    # Seed the heap with the first element of every non-empty source.
    for src_i, src in enumerate(sources):
        if src:
            heapq.heappush(h, (src[0], src_i, 0))
    # Repeatedly pop the min and refill from the same source.
    while h:
        value, src_i, idx = heapq.heappop(h)
        yield value
        if idx + 1 < len(sources[src_i]):
            next_idx = idx + 1
            heapq.heappush(h, (sources[src_i][next_idx], src_i, next_idx))
```

17 lines. Memorize the shape.

Five observations:

1. **The heap holds at most `k` tuples** — one per active source. As sources drain, the heap shrinks.
2. **Each tuple carries `(value, src_i, idx)`.** The value is the priority; `src_i` is the source index (tiebreaker and lookup); `idx` is the position within that source.
3. **The seed phase is one pass through `sources`.** `O(k log k)` to build the heap of size `k`.
4. **The main loop pops, emits, and refills.** Each iteration emits one element. Total: `N` iterations.
5. **The function returns an iterator** — values are yielded lazily. The full merged list is never materialized. For large `N`, this is a meaningful memory win.

### Why `O(N log k)` beats `O(N log N)`

The defense sentence:

> "Concatenate-then-sort is `O(N log N)` because it ignores the per-source sorting. The heap-based merge is `O(N log k)` because we only need to maintain a partial order over `k` active candidates (one per source). The heap's height is `log k`, not `log N`. For `k = 100` and `N = 10⁶`: `N log k ≈ 7 × 10⁶`; `N log N ≈ 2 × 10⁷`. About 3× faster, and the memory profile is `O(k)` heap state instead of `O(N)` for the concatenated buffer."

This is the "use the structure" senior signal — the input is already sorted; the algorithm should exploit that.

### `heapq.merge` — the built-in

The one-line answer:

```python
import heapq
from typing import Iterator, List

def k_way_merge_builtin(sources: List[List[int]]) -> Iterator[int]:
    """One-liner using heapq.merge."""
    return heapq.merge(*sources)
```

`heapq.merge` does exactly the same algorithm internally and returns an iterator. Know it exists; the manual implementation is what interviews grade.

### Variant — merge `k` sorted linked lists (LC 23)

The same algorithm with a different input shape. Each source is a linked list node `ListNode(val, next)`; the heap tuple is `(node.val, list_index, node)`. After popping, refill with `(popped_node.next.val, list_index, popped_node.next)` if `popped_node.next` is not `None`.

Watch out for the tiebreaker: when two nodes have equal `val`, the heap falls through to comparing `ListNode` objects, which do not implement `__lt__`. The `list_index` slot is mandatory.

```python
import heapq
from typing import List, Optional, Tuple


class ListNode:
    def __init__(self, val: int = 0, nxt: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = nxt


def merge_k_linked_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """Merge k sorted linked lists; return the head of the merged list."""
    h: List[Tuple[int, int, ListNode]] = []
    for i, node in enumerate(lists):
        if node is not None:
            heapq.heappush(h, (node.val, i, node))
    dummy = ListNode(0)
    tail = dummy
    while h:
        _, i, node = heapq.heappop(h)
        tail.next = node
        tail = node
        if node.next is not None:
            heapq.heappush(h, (node.next.val, i, node.next))
    return dummy.next
```

20 lines. Challenge 1 is this exact problem.

---

## 4. Lazy deletion — the canonical heap trick

The fundamental limitation of `heapq`: there is no `remove(x)` operation. To remove an arbitrary element, you would have to linearly scan the array (`O(n)`), call `_siftup` or `_siftdown` on the changed slot (`O(log n)`) — total `O(n)`. For most problems, this is too slow.

The trick: **do not remove eagerly**. Instead, mark the element as stale in an external `removed` set. When `heappop` returns a stale element, throw it away and pop again. This is **lazy deletion**.

### The template

```python
import heapq
from typing import Dict, Iterable, List


class LazyHeap:
    """Min-heap supporting amortized O(log n) arbitrary deletion.

    Uses a counter map to handle duplicates correctly. `remove(x)` increments
    the stale count for `x`; `pop` and `peek` clean the top by skipping any
    entry whose stale count is positive.
    """

    def __init__(self, items: Iterable[int] = ()) -> None:
        self._h: List[int] = list(items)
        heapq.heapify(self._h)
        self._stale: Dict[int, int] = {}    # value -> count of pending removals
        self._size: int = len(self._h)

    def __len__(self) -> int:
        return self._size

    def push(self, x: int) -> None:
        heapq.heappush(self._h, x)
        self._size += 1

    def remove(self, x: int) -> None:
        """Mark one occurrence of x as stale; the next pop will skip it.

        Raises ValueError if x is not in the heap (no stale credit available).
        """
        if x not in self and not self._has_real(x):
            raise ValueError(f"{x!r} not in heap")
        self._stale[x] = self._stale.get(x, 0) + 1
        self._size -= 1
        self._cleanup_top()

    def pop(self) -> int:
        """Pop the minimum, skipping any stale entries."""
        self._cleanup_top()
        if not self._h:
            raise IndexError("pop from empty LazyHeap")
        self._size -= 1
        return heapq.heappop(self._h)

    def peek(self) -> int:
        self._cleanup_top()
        if not self._h:
            raise IndexError("peek from empty LazyHeap")
        return self._h[0]

    def __contains__(self, x: int) -> bool:
        return self._has_real(x)

    def _has_real(self, x: int) -> bool:
        """Heuristic; for true membership testing maintain a Counter."""
        return x in self._h and self._stale.get(x, 0) < self._h.count(x)

    def _cleanup_top(self) -> None:
        while self._h and self._stale.get(self._h[0], 0) > 0:
            self._stale[self._h[0]] -= 1
            heapq.heappop(self._h)
```

About 50 lines. The class is exercised in the SOLUTIONS file with duplicate values.

### Why amortized `O(log n)`

Each element is pushed at most once and (lazily) popped at most twice — once for real, once when the cleanup loop discards a stale entry. The amortized work per element is constant in terms of heap-operation count; each heap operation is `O(log n)`. Therefore the amortized cost per `push`, `pop`, or `remove` is `O(log n)`.

The worst-case for a *single* `pop` is `O(s log n)` where `s` is the number of stale entries currently at the top. In the amortized analysis, this cost is paid off by the prior `remove` calls.

### Where lazy deletion is canonical

Three problem families:

1. **Sliding-window median.** The window slides; the leftmost element expires. Lazy-delete it from the two heaps; pop with cleanup on the median query.
2. **Dijkstra with decrease-key.** When a shorter path is discovered, the old `(dist, node)` entry in the frontier is now stale. Push the new entry; the old one will be discarded on its (eventual) pop.
3. **Top-k with updatable priorities.** "Sort jobs by priority; priorities change over time." Mark the old entry stale; push the new one.

The senior framing: "I would use lazy deletion via an external stale-counter and clean the top on `pop` and `peek`. Amortized `O(log n)` per operation. The pure alternative — an indexed heap with `decrease_key` in `O(log n)` — is also `O(log n)` but requires implementing the heap from scratch; for an interview, the lazy approach is the right tradeoff."

---

## 5. The scheduler pattern — heap with cooldown

A natural composition of the size-k template and lazy deletion. The canonical problem: LC 621, Task Scheduler.

**Spec.** Given a list of tasks (each a single character) and an integer `n` (the cooldown), return the minimum number of time units to complete all tasks. The same task cannot be run twice within `n` time units of itself; otherwise, the CPU runs idle.

**The intended solution.** A max-heap of `(count, task)` pairs (most-frequent task first), plus a cooldown queue of `(ready_time, count, task)` for tasks currently cooling. At each step:

1. If the heap is non-empty, pop the most-frequent task; execute it; decrement its count; if the count is still positive, push it onto the cooldown queue with `ready_time = now + n + 1`.
2. If the heap is empty (every active task is on cooldown), advance `now` to the soonest ready time.
3. Promote all cooldown-queue entries with `ready_time <= now` back to the heap.

```python
import heapq
from collections import Counter, deque
from typing import List, Tuple


def least_interval(tasks: List[str], n: int) -> int:
    """Return the minimum time to complete all tasks with cooldown n."""
    counts = Counter(tasks)
    # Max-heap by count (negate for heapq's min-only semantics).
    h: List[int] = [-c for c in counts.values()]
    heapq.heapify(h)
    cooldown: deque[Tuple[int, int]] = deque()   # (ready_time, neg_count)
    time = 0
    while h or cooldown:
        time += 1
        # Promote any tasks whose cooldown has expired.
        while cooldown and cooldown[0][0] <= time:
            _, neg_count = cooldown.popleft()
            heapq.heappush(h, neg_count)
        if h:
            neg_count = heapq.heappop(h)
            if neg_count + 1 < 0:
                # Still more of this task; cool it down.
                cooldown.append((time + n + 1, neg_count + 1))
    return time
```

24 lines. Challenge 2 is this exact problem.

The senior framing: "The heap holds *ready* tasks; the cooldown queue holds *cooling* tasks. Each `time` tick: promote any expired cooling tasks, then run the most-frequent ready task. Total time is bounded by `sum(counts)` (running) plus the unavoidable idle slots; the heap-plus-deque structure makes the simulation linear in the total time."

---

## 6. The three patterns side-by-side

Three templates, three invariants, three time complexities. Memorize the table.

| Pattern | Heap shape | Invariant | Time per op |
|---------|------------|-----------|-------------|
| **Size-k top-k** (Lec 1) | Size-k min-heap | Heap contains the k largest seen so far | `O(log k)` amortized |
| **k-closest** (Lec 2) | Size-k max-heap (negated) | Heap contains the k closest seen so far | `O(log k)` amortized |
| **Two-heap median** | Max-heap + min-heap, balanced | `lower.max <= upper.min`; `||lower| - |upper|| <= 1` | `O(log n)` per insert |
| **k-way merge** | Heap of size k of `(value, src_i, idx)` | Each active source contributes exactly one heap entry | `O(log k)` per emit |
| **Lazy deletion** | Heap + external stale-counter | Stale entries are skipped on pop/peek | `O(log n)` amortized |
| **Scheduler** | Heap of ready + deque of cooling | Ready tasks are eligible to run *now*; cooling are not | `O(log m)` where m = #distinct tasks |

The discriminator that interviewers grade: name the right pattern in 30 seconds, defend the invariant, write the template.

---

## 7. The 30-second recognition signals (final)

Building on Lectures 1 and 2, the complete heap-recognition decision tree:

```
prompt mentions "top k" / "k largest" / "k smallest"?
├── Yes ──→ size-k min-heap (top-k template; Lecture 1)
└── No
    ├── "k closest" / "k nearest"                ──→ size-k max-heap with distance (Lecture 2)
    ├── "top k by frequency"                     ──→ heap-of-tuples + Counter (Lecture 2)
    ├── "running median" / "support add+median"  ──→ two-heap (this lecture §1)
    ├── "running p75 / pXX percentile"           ──→ two-heap with size ratio (this lecture §2)
    ├── "merge k sorted lists / streams"         ──→ k-way merge (this lecture §3)
    ├── "remove an arbitrary element from heap"  ──→ lazy deletion (this lecture §4)
    ├── "schedule the next task with cooldown"   ──→ scheduler (this lecture §5)
    ├── "shortest path, weighted, non-negative"  ──→ Dijkstra (C5; same heap template)
    ├── "the maximum" (just one)                 ──→ NOT a heap; use max()
    └── otherwise — re-read; the pattern is probably not a heap
```

By Sunday, this tree should be reflexive. The Match step on any heap problem is the 30 seconds it takes to read down the tree until a match fires.

---

## 8. The defense sentences (one per pattern)

**Top-k (Lec 1):**
> "Size-k min-heap. The minimum of the heap is the k-th largest seen so far — the bar for the next candidate. `O(n log k)` time, `O(k)` space."

**k-closest (Lec 2):**
> "Size-k max-heap with distance-squared as the priority. The maximum of the heap is the farthest of the k closest — the bar for eviction. `O(n log k)` time, `O(k)` space."

**Two-heap median (this lecture):**
> "Max-heap of the lower half, min-heap of the upper half, balanced so sizes differ by at most one. Push-then-rebalance to maintain `lower.max <= upper.min`. `O(log n)` per add, `O(1)` per median query."

**k-way merge (this lecture):**
> "Heap of size k of `(value, src_i, idx)` tuples — one per active source. Pop the min, emit, refill from the same source. `O(N log k)` total."

**Lazy deletion (this lecture):**
> "External stale-counter; mark on `remove`, skip on `pop` and `peek`. Amortized `O(log n)` per operation because each element is pushed once and popped at most twice."

**Scheduler (this lecture):**
> "Max-heap of ready tasks by count, deque of cooling tasks by ready-time. Each tick: promote any expired cooling tasks, run the most-frequent ready task, cool the remaining count. Linear in the total run time."

Memorize all six. They are the spoken outputs of the Match step.

---

## 9. Self-check

Without notes, answer:

1. **Why does the two-heap median template use a *max*-heap for the lower half?** (To peek the maximum of the lower half in `O(1)`; combined with the min-heap of the upper half's `O(1)` minimum peek, the median is `O(1)` to compute.)
2. **What is the two-heap rebalance discipline?** (After pushing to `lower`, move `lower`'s max to `upper`. If `upper`'s size now exceeds `lower`'s, move one back. Convention: when sizes differ, `lower` is the larger heap.)
3. **What is the time complexity of k-way merge, and why?** (`O(N log k)` where `N` is the total element count. The heap holds at most `k` elements at any time; each `heappush` and `heappop` is `O(log k)`; there are `N` total emissions.)
4. **Why is `O(N log k)` better than `O(N log N)` for k-way merge?** (We only need to maintain partial order over `k` candidates at a time, not `N`. The heap's height is `log k`, not `log N`. For `k << N`, the saving is meaningful.)
5. **What is lazy deletion's amortized complexity, and why?** (Amortized `O(log n)` per operation. Each element is pushed at most once and popped at most twice (once for real, once when the cleanup loop discards a stale entry). The amortized work per element is constant in terms of heap-operation count.)
6. **When is lazy deletion the wrong choice?** (When stale entries accumulate faster than they are popped — for example, in a long-running heap where `remove` is called much more often than `pop`. The heap can grow unbounded with stale entries. The fix is periodic compaction (rebuild the heap) or an indexed-heap with eager removal.)

If you can answer all six without hesitation, the lecture sequence is closed. Proceed to the exercises.

---

## 10. Putting it all together — the four-template summary

By Sunday of Week 8, you should be able to write each of these from memory:

1. **The size-k top-k template** (Lecture 1 §4). Eleven lines. `O(n log k)`.
2. **The heap-of-tuples idiom with a counter tiebreaker** (Lecture 2 §2). The four-rule discipline.
3. **The two-heap median template** (this lecture §1). 20 lines. Two invariants, three rebalance steps.
4. **The k-way merge template** (this lecture §3). 17 lines. Heap of size k of `(value, src_i, idx)`.

Plus the meta-rule: when in doubt, mention `heapq.nlargest`, `heapq.nsmallest`, or `heapq.merge` as the "production" answer; implement the manual version to show the template.

These four templates plus lazy deletion (§4) cover every heap problem you will see in Mock #2, the capstone, and FAANG onsites. The work this week is fluency.

---

## 11. Why this is the final Phase-2 data-structure lecture

Week 9 is Mock #2 — a full simulated onsite. The heap problems in Mock #2 are graded on:

- **Match-step recognition.** 30 seconds to name the pattern; 30 seconds to defend it.
- **Implement-step correctness.** Can you write the template from memory without a bug.
- **Evaluate-step defense.** Can you explain why `O(n log k)` beats `O(n log n)`, or why two heaps beat one sorted list.

This lecture (and Lectures 1 and 2) install the templates. The exercises drill them. The mini-project consolidates them into two UMPIRE write-ups. By Sunday Week 8, the heap is a *small, sharp tool* — invariant clear, complexity defended, template reflexive.

That is the bar. The exercises are next.

---

## Further reading

- **`heapq.merge` — Python docs**: <https://docs.python.org/3/library/heapq.html#heapq.merge> — the built-in k-way merge.
- **Wikipedia — k-way merge**: <https://en.wikipedia.org/wiki/K-way_merge_algorithm> — covers the heap approach and the alternative tournament tree.
- **Wikipedia — Selection algorithm** (running median section): <https://en.wikipedia.org/wiki/Selection_algorithm> — covers the two-heap approach in the context of order statistics.
- **LeetCode 295 (Find Median from Data Stream)**: the canonical two-heap problem; Exercise 3 covers this exactly.
- **LeetCode 23 (Merge k Sorted Lists)**: the canonical k-way merge; Challenge 1.
- **LeetCode 621 (Task Scheduler)**: the canonical scheduler; Challenge 2.
- **LeetCode 480 (Sliding Window Median)**: the canonical two-heap + lazy deletion problem; mentioned in §4 as the Phase-3 extension.

The lecture sequence is closed. Next: the exercises.
