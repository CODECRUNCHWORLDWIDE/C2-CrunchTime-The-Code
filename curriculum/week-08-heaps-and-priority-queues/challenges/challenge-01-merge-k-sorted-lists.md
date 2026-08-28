# Challenge 1 — Merge k Sorted Lists (LeetCode 23)

> **Difficulty:** Hard. **Target solve time:** 60 minutes including FRAME write-up.

The canonical k-way-merge problem. Every Phase-2 onsite includes at least one variant of this; the FAANG onsite frequency is on par with "Two Sum" for entry-level questions, except this one is asked of mid-to-senior candidates and graded on the *defense* of the asymptotic improvement, not just the code.

---

## Problem spec

You are given an array of `k` linked lists, each sorted in non-decreasing order. Merge all the lists into one sorted linked list and return its head.

```
ListNode:
    val: int
    next: ListNode | None
```

The input is `lists: List[ListNode | None]` — note that individual lists can be `None` (empty).

**Constraints (LeetCode):**

- `k == len(lists)`, with `0 <= k <= 10⁴`.
- Each list is sorted in non-decreasing order.
- The sum of list lengths is up to `10⁴` elements (so `N`, the total element count, is up to `10⁴`).
- `-10⁴ <= node.val <= 10⁴`.

**Examples:**

- Input: `lists = [[1, 4, 5], [1, 3, 4], [2, 6]]` (each inner list represents a linked list).
- Output: `[1, 1, 2, 3, 4, 4, 5, 6]`.

- Input: `lists = []` → Output: empty list (return `None`).
- Input: `lists = [[]]` → Output: empty list.

---

## Why this is the canonical k-way merge

Three reasons.

1. **The brute-force solution is `O(N log N)`** — concatenate all lists, sort, rebuild. This works and gets partial credit on LeetCode, but it ignores the input structure (each list is *already sorted*). The interviewer wants you to exploit that.

2. **The heap-based solution is `O(N log k)`** — strictly faster when `k << N`. For `k = 100, N = 10⁴`: `N log k ≈ 6.6 × 10⁴`; `N log N ≈ 1.3 × 10⁵`. About 2× faster. The senior signal is naming both bounds and defending the choice.

3. **There is a third valid solution: divide-and-conquer pairwise merging** — `O(N log k)` time, `O(log k)` recursion depth, no heap. Mentioning this alternative is graded — it shows you know more than one path through the problem.

---

## 30-second pattern-recognition memo

Use this exact shape at the top of your write-up.

```markdown
> **30-second pattern-recognition memo (k-way merge):**
> This is a k-way-merge problem because we are given k sorted streams and asked for the global sorted output.
> Algorithm choice: heap of size k of `(value, list_index, node)`; the list_index is the tiebreaker that prevents comparison from falling through to ListNode (which has no `__lt__`).
> Edge model: each list head is the initial seed; after each pop, refill from `node.next` if non-null.
> Why not concatenate-then-sort: `O(N log N)` vs `O(N log k)`; the heap exploits the per-list sortedness.
> Why not divide-and-conquer pairwise merge: same `O(N log k)` time, slightly more code, no heap; mention as alternative.
```

Read aloud; should hit 25-30 seconds.

---

## The intended algorithm

```python
import heapq
from typing import List, Optional, Tuple


class ListNode:
    def __init__(self, val: int = 0, nxt: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = nxt


def merge_k_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """Merge k sorted linked lists into one sorted list."""
    h: List[Tuple[int, int, ListNode]] = []
    # Seed the heap with the head of every non-empty list.
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

About 20 lines. The structure mirrors the array-of-arrays version from Lecture 3 §3 exactly; the only difference is that the "next element" is `node.next` rather than `sources[src_i][idx + 1]`.

### Walkthrough on `lists = [[1, 4, 5], [1, 3, 4], [2, 6]]`

- Seed: push `(1, 0, head_0)`, `(1, 1, head_1)`, `(2, 2, head_2)`. h = three items.
- Pop: min by first slot is `1`; tie between `(1, 0, ...)` and `(1, 1, ...)`; the tiebreaker is the list index `0`. Pop `(1, 0, node_0)`. Output 1. Push `(4, 0, node_0.next)`.
- Pop: min is `(1, 1, node_1)`. Output 1. Push `(3, 1, node_1.next)`.
- Pop: min is `(2, 2, node_2)`. Output 2. Push `(6, 2, node_2.next)`.
- Pop: min is `(3, 1, ...)`. Output 3. Push `(4, 1, ...)`.
- Pop: tie at 4; list indices 0 and 1. Push `(5, 0, ...)` after popping `(4, 0, ...)`. Output 4.
- Pop: `(4, 1, ...)`. Output 4. `node.next` is None for list 1; skip push.
- Pop: `(5, 0, ...)`. Output 5. None next; skip.
- Pop: `(6, 2, ...)`. Output 6. None next; skip.
- Heap empty; return `dummy.next`.

Output sequence: `1, 1, 2, 3, 4, 4, 5, 6`. Correct.

### Why the list-index tiebreaker is mandatory

Without it:

```python
heapq.heappush(h, (node.val, node))   # WRONG -- no tiebreaker
# When two nodes have equal val, the heap compares ListNode objects.
# ListNode has no __lt__. TypeError.
```

The `list_index` slot fixes this. Coordinates compare cleanly; `ListNode` is never reached.

### Edge cases the spec covers

1. `lists = []` → return `None`. The for-loop is empty; the while-loop body is never entered; `dummy.next` is `None`.
2. `lists = [None, None, None]` → return `None`. The for-loop skips all entries (the `if node is not None` guard); same as above.
3. `lists = [[1]]` → return the head with value 1. Trivial single-list case.
4. All lists identical: `lists = [[1, 1, 1], [1, 1, 1]]` → return six `1`s in a row. The tiebreaker handles equal values across lists.

---

## Acceptance criteria

- [ ] Function signature matches `merge_k_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]`.
- [ ] Returns `None` for empty input, all-None input, and `[[]]`.
- [ ] Returns the correct merged list for the documented example.
- [ ] Heap operations are limited to `heapq.heappush`, `heapq.heappop`, `heapq.heapify` (no manual sift code).
- [ ] The heap-tuple includes a tiebreaker slot (the list index) — defended in the write-up.
- [ ] The write-up names *both* the `O(N log N)` brute force and the `O(N log k)` heap solution; defends the heap.
- [ ] (Bonus) The write-up mentions the divide-and-conquer pairwise-merge alternative as a third valid path.
- [ ] Time complexity: `O(N log k)`. Space: `O(k)` for the heap plus `O(1)` extra (the dummy node and a `tail` pointer).

---

## Hints (read only if stuck)

<details>
<summary>Hint 1 — what is in the heap</summary>

The heap should hold *one element per active source*. For k sorted lists, that means at most k elements at any time. Each heap element is `(value, list_index, node_reference)`. The `list_index` is the tiebreaker; the `node_reference` is how you reach the *next* element of that list.

</details>

<details>
<summary>Hint 2 — what to do after each pop</summary>

After popping `(value, i, node)`, append `node` to the output and push `(node.next.val, i, node.next)` if `node.next is not None`. The "refill from the same source" pattern is what keeps the heap at size at most `k`.

</details>

<details>
<summary>Hint 3 — the dummy-node trick</summary>

Linked-list construction always uses a dummy head. Create `dummy = ListNode(0)`; maintain a `tail = dummy` pointer; append each popped node by setting `tail.next = node; tail = node`. At the end, return `dummy.next`. This avoids the special case of "the first popped node is the head."

</details>

<details>
<summary>Hint 4 — alternative: divide-and-conquer</summary>

The recursive pairwise merge: split the input array of lists in half; merge each half (recursively); then merge the two resulting lists with the standard two-pointer merge from Merge Two Sorted Lists (LC 21). The recursion depth is `O(log k)`; each level does `O(N)` work; total `O(N log k)`. Same asymptotic as the heap, no heap needed. Mention this in your write-up.

</details>

---

## Worked solution sketch

<details>
<summary>Click after attempting</summary>

The complete code is in the §"intended algorithm" block above. The full FRAME write-up follows the same five sections.

### FRAME

**[F]** Restate. K sorted linked lists; merge into one sorted list. Edge cases: empty input, all-None input, single-list input.

**[R]** K-way merge with a heap of size k. The tuple is `(val, list_index, node)`; the list_index is the tiebreaker. Alternative: divide-and-conquer pairwise merge in `O(log k)` levels.

**[A]** (1) Seed the heap with the head of every non-empty list. (2) Build a dummy + tail. (3) Loop: pop the min, append to tail, refill from `node.next`. (4) Return `dummy.next`.

**[M]** See §"intended algorithm" above.

**[E · verify]** Trace on `[[1, 4, 5], [1, 3, 4], [2, 6]]` (above). Edge case `[]`: return `None`. Edge case `[None, None]`: skip both in the for-loop; return `None`.

**[E · cost]** **Time `O(N log k)`** — `N` total elements, each one push and one pop, each `O(log k)`. **Space `O(k)`** for the heap. Tradeoff vs brute-force-then-sort: `O(N log N)`; the heap wins when `k << N`. Tradeoff vs pairwise divide-and-conquer: same `O(N log k)` time, `O(log k)` recursion depth, slightly cleaner code; either is acceptable.

### Common bugs

1. **Forgetting the list-index tiebreaker.** `TypeError` when two nodes have equal values.
2. **Forgetting to push the next node after a pop.** The output stops after the first `k` elements.
3. **Pushing `node.next` instead of `(node.next.val, i, node.next)`.** The heap loses its tuple shape.
4. **Forgetting to check `node.next is not None` before the refill push.** AttributeError on the next iteration.

</details>

---

## What "great" looks like

A learner who has shipped this challenge *well* has:

- A full FRAME write-up with the 30-second memo at the top.
- Both `O(N log N)` and `O(N log k)` named in Research constraints; the heap defended.
- The divide-and-conquer pairwise-merge alternative mentioned.
- Code that uses `heapq` correctly with the tiebreaker.
- A trace on at least the three-list example, plus two edge cases.
- Recording ≥ 15 minutes.

A learner who has shipped this challenge *poorly* has:

- No memo at the top; the Research constraints step is just "use a heap."
- The brute-force concatenate-then-sort version, with no mention of the heap.
- The heap version without a tiebreaker (works on the LeetCode test cases but fails on equal-value cross-list ties).
- No mention of the divide-and-conquer alternative.

If you produced the "poorly" version, re-read Lecture 3 §3 and re-attempt.

---

## Cross-references

- **Lecture 3 §3** — the k-way-merge template on arrays of arrays. This challenge is the linked-list variant.
- **Exercise 1** — the size-k template. The structural pair: top-k bounds the heap; k-way-merge sizes the heap by the number of sources.
- **Mini-project Problem 2 (when you get there)** — a heap-of-tuples problem that is *not* a k-way merge; useful as a contrast.

When done, run [the quiz](../quiz.md) (if you have not already), then move on to [Challenge 2 — Task Scheduler](./challenge-02-task-scheduler.md) if you have time, or directly to the [mini-project](../mini-project/README.md).
