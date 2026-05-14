# Challenge 2 — Task Scheduler (LeetCode 621)

> **Difficulty:** Medium / Hard. **Target solve time:** 60 minutes including UMPIRE write-up.

The canonical "heap + auxiliary structure" problem. Builds on the size-k template (Exercise 1) and the heap-of-tuples idiom (Lecture 2). The optional Phase-2 stretch — useful if you have energy left after Challenge 1.

---

## Problem spec

Given a list of CPU tasks (each represented by a single uppercase letter) and a non-negative integer `n` (the cooldown), return the minimum number of time units needed to complete all tasks.

Two constraints on the schedule:

1. Each time unit, the CPU runs at most one task.
2. The same task cannot be run twice within `n` time units of itself. If no other task is available, the CPU is idle.

**Constraints (LeetCode):**

- `1 <= len(tasks) <= 10⁴`.
- Tasks are uppercase letters `A`-`Z`.
- `0 <= n <= 100`.

**Examples:**

- Input: `tasks = ["A", "A", "A", "B", "B", "B"], n = 2`. Output: `8`. Schedule: `A B idle A B idle A B`.
- Input: `tasks = ["A", "C", "A", "B", "D", "B"], n = 1`. Output: `6`. Schedule: `A B C D A B`.
- Input: `tasks = ["A", "A", "A", "B", "B", "B"], n = 0`. Output: `6`. No idle slots needed.

---

## Why this is the canonical scheduler pattern

Three reasons.

1. **It is the simplest production-shaped scheduling problem.** The OS analogue: "run the next-highest-priority task; if it just ran, wait." The same heap-plus-cooldown structure powers job queues, rate limiters, and exponential-backoff retries.

2. **There are two valid solution shapes.** The simulation (heap + cooldown queue) is the natural fit and runs in `O(L log m)` where `L` is the total time and `m` is the number of distinct tasks. The closed-form math solution — based on the count of the most-frequent task — is `O(L)` but harder to derive and less general. Naming both is the senior signal.

3. **It composes with multiple Week-8 patterns.** The heap holds `(count, task)` tuples (Lecture 2); the cooldown queue is a deque holding `(ready_time, count, task)` (a small lazy-deletion adjacent); the rebalance happens once per tick. Three Week-8 primitives in one problem.

---

## 30-second pattern-recognition memo

```markdown
> **30-second pattern-recognition memo (scheduler):**
> This is a scheduler problem because we run tasks by priority (count) under a constraint (cooldown).
> Algorithm choice: max-heap of (count, task) tuples for ready tasks + deque of (ready_time, count, task) for cooling tasks.
> Edge model: each tick — promote any expired cooling tasks back to the heap, run the top, push to cooling if count > 1.
> Cycle handling: when the heap is empty but cooling has entries, advance `time` to the earliest `ready_time`; do not idle one step at a time.
> Why not closed-form math: the math works for this exact spec but does not generalize to "n-aware-priorities" or "deadlines"; the simulation is more honest.
```

---

## The intended simulation algorithm

```python
import heapq
from collections import Counter, deque
from typing import List, Tuple


def least_interval(tasks: List[str], n: int) -> int:
    """Return the minimum time to finish all tasks under the cooldown."""
    counts = Counter(tasks)
    # Max-heap by count (negate for heapq's min-only semantics).
    # Tiebreaker: the negated character. Not strictly needed for correctness
    # (we do not need stability) but cleaner.
    h: List[Tuple[int, str]] = [(-c, t) for t, c in counts.items()]
    heapq.heapify(h)
    cooldown: deque[Tuple[int, int, str]] = deque()    # (ready_time, neg_count, task)
    time = 0
    while h or cooldown:
        time += 1
        # Promote any tasks whose cooldown has expired.
        while cooldown and cooldown[0][0] <= time:
            _, neg_count, task = cooldown.popleft()
            heapq.heappush(h, (neg_count, task))
        if h:
            neg_count, task = heapq.heappop(h)
            if neg_count + 1 < 0:
                # Still more of this task; cool it down.
                cooldown.append((time + n + 1, neg_count + 1, task))
        # If h is empty and cooldown has entries, the loop just advances time.
    return time
```

About 25 lines. The `while h or cooldown` loop runs once per CPU tick; each iteration does `O(log m)` work (one heap push + pop, plus the deque promote which is amortized `O(1)` per task).

### Walkthrough on `tasks = ["A", "A", "A", "B", "B", "B"], n = 2`

- counts = `{A: 3, B: 3}`. h = `[(-3, A), (-3, B)]` (heap order).
- t=1: cooldown empty. Pop (-3, A). neg_count + 1 = -2 < 0; cool to (1 + 2 + 1, -2, A) = (4, -2, A). cooldown = [(4, -2, A)].
- t=2: cooldown[0][0]=4 > 2. Pop (-3, B). Cool to (5, -2, B). cooldown = [(4, -2, A), (5, -2, B)].
- t=3: heap empty; cooldown still has entries, both ready_time > 3. Advance time, no work.
- t=4: cooldown[0][0]=4 <= 4; promote A. h = [(-2, A)]. Pop (-2, A). Cool to (4 + 2 + 1, -1, A) = (7, -1, A).
- t=5: cooldown[0][0]=5 <= 5; promote B. h = [(-2, B)]. Pop (-2, B). Cool to (8, -1, B).
- t=6: heap empty; cooldown both > 6. Advance.
- t=7: promote A. Pop. -1 + 1 = 0 not < 0; no cool.
- t=8: promote B. Pop. -1 + 1 = 0; no cool.
- Done. Return 8.

### Closed-form math alternative

For `tasks = ["A", "A", "A", "B", "B", "B"], n = 2`:

- Let `f` be the count of the most-frequent task (here 3).
- Let `m` be the number of tasks tied for that maximum (here 2: A and B).
- Slots used by the most-frequent tasks plus their idle / fill slots: `(f - 1) * (n + 1) + m = 2 * 3 + 2 = 8`.

The formula: `max(len(tasks), (f - 1) * (n + 1) + m)`.

```python
from collections import Counter
from typing import List


def least_interval_math(tasks: List[str], n: int) -> int:
    """Closed-form O(L) solution; works for this exact spec only."""
    counts = Counter(tasks)
    f = max(counts.values())                       # most-frequent count
    m = sum(1 for c in counts.values() if c == f)  # how many tasks tie
    return max(len(tasks), (f - 1) * (n + 1) + m)
```

Four lines. `O(L)` time. The formula derivation is non-trivial; the simulation is the easier first solution to write.

In the write-up, **name both**, defend the simulation as the more general answer.

---

## Acceptance criteria

- [ ] Function signature matches `least_interval(tasks: List[str], n: int) -> int`.
- [ ] Returns the documented example outputs (8, 6, 6).
- [ ] Returns `len(tasks)` when `n = 0` (no cooldown).
- [ ] Handles `n = 100` with all distinct tasks (cooldown larger than the task count; still `len(tasks)`).
- [ ] Heap operations: `heappush`, `heappop`, `heapify` only.
- [ ] The write-up names *both* the simulation (`O(L log m)`) and the closed-form math (`O(L)`); defends one.
- [ ] Time complexity: simulation is `O(L log m)`. Math is `O(L)`. Space: `O(m)` for the heap and the counts.

---

## Hints (read only if stuck)

<details>
<summary>Hint 1 — what is in the heap</summary>

The heap holds *ready* tasks — those that can run now. Each entry is `(-count, task_letter)`. We use negated counts so `heapq` (min-heap) extracts the most-frequent task first.

</details>

<details>
<summary>Hint 2 — what is in the cooldown queue</summary>

A deque of `(ready_time, neg_count, task)` tuples. Tasks enter the deque when they just ran and still have count > 0. They are promoted back to the heap when `time >= ready_time`.

The deque maintains FIFO order, which is also the natural order of `ready_time` because tasks are pushed in time order. The deque is *not* a heap; it does not need to be sorted by anything other than insertion order.

</details>

<details>
<summary>Hint 3 — what to do when the heap is empty</summary>

If `h` is empty but `cooldown` has entries, the CPU is idle. Just increment `time` and loop. The next iteration's promote-loop will pull the earliest ready task back to the heap.

An optimization: instead of incrementing one tick at a time, jump `time` to `cooldown[0][0]` directly. This shaves a constant factor on long idle stretches.

</details>

<details>
<summary>Hint 4 — the closed-form derivation</summary>

The most-frequent task runs `f` times; between any two of its occurrences, there must be at least `n` other slots (filled or idle). That gives a minimum schedule of `(f - 1) * (n + 1)` slots, *plus* the slots for the `m` tasks that tie for the maximum (they each get one final slot at the end). Total: `(f - 1) * (n + 1) + m`.

But this can be less than `len(tasks)` when there are many distinct low-frequency tasks (because some of those fill the cooldown gaps). The final answer is `max(len(tasks), (f - 1) * (n + 1) + m)`.

</details>

---

## What "great" looks like

A learner who has shipped this challenge *well* has:

- A full UMPIRE write-up with the 30-second memo.
- Both the simulation and the closed-form math named in Match; the simulation defended as the general answer.
- A trace on the documented example showing the heap and cooldown state at each tick.
- Time complexity: `O(L log m)` for simulation; `O(L)` for math.
- Recording ≥ 15 minutes.

A learner who has shipped this challenge *poorly* has:

- Only the closed-form math, without explaining the derivation or naming the simulation.
- The simulation without the cooldown-empty optimization (one-tick-at-a-time advances; correct but slow).
- The heap without a tiebreaker on the task letter (works because letters compare cleanly, but the discipline is what matters).

---

## Cross-references

- **Lecture 2 §6** — the `PriorityQueue` class; the scheduler is the application.
- **Lecture 3 §5** — the scheduler-with-cooldown pattern in detail.
- **Lecture 3 §4** — lazy deletion. The cooldown queue is *adjacent* to lazy deletion: stale-by-time rather than stale-by-flag.
- **Challenge 1 — Merge k Sorted Lists** — the other heap challenge this week. The two pair well: one is "merge k streams" (Challenge 1), the other is "schedule k tasks" (Challenge 2); both rest on heap-of-tuples.

When done with both challenges, move on to the [mini-project](../mini-project/README.md).
