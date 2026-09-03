# Week 8 — Heaps and Priority Queues

```
┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐
│ F │  │ R │  │ A │  │ M │  │ E │
└───┘  └───┘  └───┘  └───┘  └───┘
```

> *Week 7 installed DFS — the recursion stack, the three-color invariant, the post-order trick. Week 8 installs the **heap** — `heapq`, the min-heap-as-list invariant, the heap-of-tuples idiom for custom keys, the two-heap median pattern, k-way merge, k-closest points, and lazy deletion. By Sunday you can write `heapq.heappush` / `heapq.heappop` and the two-heap median template from memory, you can defend each against `sorted(...)[k]`, and the prompt-to-pattern reflex "top-k / closest-k / median of a stream" produces the heap one-liner without hesitation.*

Welcome to Week 8 of **C2 · CrunchTime — The Code** — the fourth week of Phase 2. Last week installed DFS and topological sort. This week installs the **priority queue** abstraction and its concrete implementation in CPython: the **`heapq` module**, a binary min-heap stored as a flat list, with `heappush` and `heappop` in `O(log n)`.

Heaps have a reputation for being *easy to misuse*. The algorithm itself is short — `heapq.heappush(h, x)` is a one-liner — but the *recognition* is subtler than DFS or BFS: half of all heap problems are not phrased as "use a priority queue." They are phrased as "top-k," "k closest," "median of a stream," "merge sorted lists," "schedule the next task." The Research constraints work this week is learning to convert each of those phrasings into the same answer: *heap, size k, push then pop, or push then peek*.

By Sunday of Week 8 you will:

- **Recognize** a heap problem in 30 seconds and classify it as **top-k / k-closest / running-median / k-way-merge / lazy-deletion / scheduler** in the next sentence.
- **Write** the canonical `heapq` operations from memory, defend the min-heap invariant out loud, and explain why `heappush` and `heappop` are both `O(log n)`.
- **Write** the **top-k template** with a size-k min-heap. Defend why `O(n log k)` beats both `sorted(...)[:k]` (`O(n log n)`) and quickselect (`O(n)` average but `O(n²)` worst).
- **Apply the heap-of-tuples idiom** for custom keys — `(priority, tiebreaker, payload)` — and explain why the tiebreaker is mandatory when payloads are not comparable.
- **Implement the two-heap pattern** for the running median: a max-heap of the lower half, a min-heap of the upper half, balanced so that their sizes differ by at most one.
- **Implement k-way merge** of sorted streams using a heap of size k that holds one element per stream.
- **Implement lazy deletion** — the canonical trick for "remove an arbitrary element from a heap" without paying `O(n)` to search. Mark the slot stale; skip stale entries on pop.
- Have solved **three heap exercises** — the crest watch shortlist, the k-closest shape, the oven probe midline — each with a FRAME write-up.
- Have shipped **one challenge** (the hut roll call — the canonical k-way merge) plus an optional stretch (the dye vat rotation — heap-with-cooldown).
- Have shipped the quiz, the homework, and the **mini-project**: one top-k write-up and one two-heap write-up, fully FRAME-narrated.

---

## Learning objectives

By the end of this week, you will be able to:

- **Name the pattern** for a heap problem in 30 seconds from the canonical signals: "top k," "k largest," "k smallest," "k closest," "median of a stream," "merge k sorted," "running statistics on a stream," "schedule the next task," "minimum element among n active sources."
- **Distinguish a heap from sorting** in one sentence: a heap maintains a *partial order* with `O(log n)` insert / extract-min; sorting establishes a *total order* in `O(n log n)`. If you only need the top k of n elements and `k << n`, the heap is `O(n log k)` — strictly cheaper than `O(n log n)`.
- **Implement** the canonical `heapq` operations without notes — `heappush`, `heappop`, `heapify`, `heappushpop`, `heapreplace`, `nlargest`, `nsmallest`.
- **Apply the heap-of-tuples idiom** correctly, including the tiebreaker slot. State the rule out loud: *"Heap items are compared lexicographically by tuple order; if priorities tie, Python compares the next element; if that element is not comparable, you get a `TypeError`. The fix is to insert a unique counter or `id(obj)` as the tiebreaker."*
- **Implement the two-heap median template** — max-heap of the lower half (negate values in `heapq`), min-heap of the upper half, rebalance after each insert so sizes differ by at most one.
- **Implement k-way merge** with a heap of size k that holds one tuple per active source — `(value, source_index, item_index)` — and refill after each pop.
- **Implement lazy deletion** — mark items stale in an external `removed` set or counter, skip them on `heappop`. The cleaner alternative to `O(n)` linear search inside a heap.
- **Choose between a heap, a sort, and a quickselect** for a given top-k problem. Heap is `O(n log k)` and stable on streams; sort is `O(n log n)` and simple; quickselect is `O(n)` average but `O(n²)` worst and not stream-friendly.
- **Recognize when a heap does *not* apply** — when the answer requires random access (use an array), when the order is total and stable (use sort), when k is close to n (sort is simpler and competitive).

---

## Prerequisites

- **Weeks 1-7 complete.** You have shipped two DFS write-ups; you can deliver FRAME without notes on a graph-traversal problem.
- **Comfortable with Python tuple comparison.** `(1, "a") < (1, "b")` returns `True` because tuples compare lexicographically. The heap-of-tuples idiom rests entirely on this rule.
- **Comfortable with `list` mutation semantics.** `heapq` operates *in place* on a Python list. Passing the same list to `heappush` and reading it afterward mutates the caller's list — this is intentional but trips up beginners.
- **Comfortable with `O(log n)` arguments.** A heap is a complete binary tree of height `log₂ n`; every `heappush` and `heappop` walks one root-to-leaf or leaf-to-root path. The `log n` factor is the tree height.

---

## Topics covered

- The **heap invariant** — a min-heap is an array `h` such that `h[i] <= h[2i+1]` and `h[i] <= h[2i+2]` whenever the children exist
- The canonical `heapq` operations — `heappush`, `heappop`, `heapify`, `heappushpop`, `heapreplace`, `nlargest`, `nsmallest`, `merge`
- The **top-k template** — bounded min-heap of size k; push then conditionally pop; `O(n log k)`
- The **heap-of-tuples idiom** — `(priority, tiebreaker, payload)` for custom keys; why the tiebreaker is mandatory
- The **two-heap pattern** for running median — max-heap (negated) + min-heap, balanced; `O(log n)` per insert, `O(1)` per query
- **k-way merge** — heap of size k, one element per source; `O(N log k)` where N is total elements
- **k-closest points** — distance-squared as the priority; max-heap (negated) of size k
- **Lazy deletion** — external "removed" set; skip stale entries on pop; amortized `O(log n)`
- **Why `heapq` is a min-heap only** — and how to simulate a max-heap (negate keys, or wrap in a comparator class)
- **Why `sorted` is *not* always the right answer** — the `O(n log k)` vs `O(n log n)` discriminator
- **The CPython `heapq` source** — sift-up and sift-down in `Lib/heapq.py`; a 30-line read worth the time

---

## Weekly schedule (intensive · 36h)

| Day | Focus | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project | Self-Study | Daily Total |
|-----|-------|---------:|----------:|-----------:|----------:|---------:|-------------:|-----------:|------------:|
| Monday | `heapq` + top-k template; exercise 1 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Tuesday | Heap-of-tuples + k-closest; exercise 2 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Wednesday | Two-heap median + lazy deletion; exercise 3 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Thursday | Mini-project drafting; challenge ramp | 0h | 1h | 1h | 0.5h | 1h | 1.5h | 1h | 6h |
| Friday | Challenge (the hut roll call) | 0h | 0h | 2h | 0.5h | 1h | 1.5h | 1h | 6h |
| Saturday | Mini-project — top-k + two-heap write-ups | 0h | 0h | 0h | 0.5h | 1h | 3h | 0h | 4.5h |
| Sunday | Quiz + retro + push | 0h | 0h | 0h | 0.5h | 0h | 4h | 0h | 4.5h |
| **Total** | | **6h** | **7h** | **3h** | **3h** | **6h** | **10h** | **3.5h** | **38.5h** |

(The week budgets ~36 hours; the table sums slightly higher to absorb the Phase-2 ramp. Drop 0.5h from Self-Study if 36h is your hard cap.)

**Mastery (10h/wk):** spread the same content over three calendar weeks. The mini-project lands in calendar Week 25 of the mastery pathway. See the [mastery study plan](../study-plans/mastery-1-year.md).

---

## How to navigate this week

| File | What's inside |
|------|---------------|
| [README.md](./README.md) | This overview |
| [resources.md](./resources.md) | Free readings + `heapq` references + glossary additions |
| [lecture-notes/01-heapq-and-top-k.md](./lecture-notes/01-heapq-and-top-k.md) | The `heapq` module, the min-heap invariant, the top-k template, the four common bug patterns |
| [lecture-notes/02-heap-of-tuples-and-k-closest.md](./lecture-notes/02-heap-of-tuples-and-k-closest.md) | Custom keys via tuples; the tiebreaker rule; k-closest-points; max-heap simulation by negation |
| [lecture-notes/03-two-heap-and-k-way-merge.md](./lecture-notes/03-two-heap-and-k-way-merge.md) | Two-heap running median, k-way merge, lazy deletion, scheduler patterns |
| [exercises/README.md](./exercises/README.md) | Index of the five exercises, in order |
| [exercises/exercise-01-sluice-gate-order.md](./exercises/exercise-01-sluice-gate-order.md) | The sluice gate order — `heapify`, `heappush`, `heappop`, reading the front |
| [exercises/exercise-02-crest-watch-shortlist.md](./exercises/exercise-02-crest-watch-shortlist.md) | The crest watch shortlist — six entries held while forty thousand go past |
| [exercises/exercise-03-tool-bench-slots.md](./exercises/exercise-03-tool-bench-slots.md) | The tool bench rota — a max-heap out of `heapq`, by negation |
| [exercises/exercise-04-rescue-intake-queue.md](./exercises/exercise-04-rescue-intake-queue.md) | The rescue intake desk — a heap of tuples, and the tiebreaker that stops it crashing |
| [exercises/exercise-05-tide-log-stitch.md](./exercises/exercise-05-tide-log-stitch.md) | The estuary ledger — one heap entry per source, not one per row |
| [challenges/README.md](./challenges/README.md) | Index of the two challenges |
| [challenges/challenge-01-hut-roll-call-stitch.md](./challenges/challenge-01-hut-roll-call-stitch.md) | The hut roll call — the k-way merge as a generator, read only as far as needed |
| [challenges/challenge-02-dye-vat-rotation.md](./challenges/challenge-02-dye-vat-rotation.md) | The dye vat rotation — greedy scheduling on two heaps with a cooldown |
| [quiz.md](./quiz.md) | 10 pattern-recognition questions |
| [homework/README.md](./homework/README.md) | Six practice problems (~5 hrs), each with its answer stated and a runnable file beside it |
| [mini-project/README.md](./mini-project/README.md) | **The repair cafe desk** — every idiom of the week in one working system, plus two write-ups |

---

## Stretch goals

- **Skim twenty problem titles from any practice set** and, for each, predict in five seconds which shape it is: bounded top-k, heap of tuples, two-heap statistic, k-way merge, or scheduler. The prediction is the rep; being wrong quickly is fine.
- **Re-derive the canonical top-k template from scratch** without re-reading Lecture 1. If you cannot, you do not yet own the template. Re-read and re-derive until you can.
- **Read the first 100 lines of CPython's `Lib/heapq.py`** — the sift-up and sift-down implementations are short enough to internalize, and the module docstring contains the cleanest free explanation of the heap invariant.
- **Find one production-engineering heap story.** Examples: the Linux kernel's `CFS` scheduler uses a red-black tree but the same priority-queue abstraction; Dijkstra's algorithm uses a min-heap as its frontier; load-shedding in web servers prioritizes inflight requests by deadline. The "where does a heap live in real systems?" question lifts you out of the puzzle frame and into the engineering one.

---

## What "done" looks like for Week 8

A learner who has shipped Week 8 has, in their portfolio repo:

- Three FRAME write-ups for the exercises, with recordings >= 10 minutes.
- One FRAME write-up for the hut roll call challenge.
- The quiz answered (score recorded).
- The homework problems committed.
- **Two mini-project write-ups** (one top-k, one two-heap), each with a 30-second pattern-recognition memo at the top, under `frame-writeups/c2-week-08/mini-project/`.
- A push log showing daily commits Mon-Sun.

If all of that is present and pushed, Phase 2's fourth week is closed. You are ready for Week 9 — Mock #2.

---

## A note on the Phase 2 ramp

Week 8 is the *data-structure* week sandwiched between two algorithm weeks (DFS in W7, Mock #2 in W9). The heap is a small, sharp tool — six operations, one invariant — but the *Research constraints recognition* is what separates strong candidates from weak ones. Half of all heap problems do not say "heap" anywhere in the prompt; they say "top k" or "closest" or "median." Owning the recognition is the work this week.

If you find yourself ahead by Friday, the right stretch is **not** another exercise — it is a second-pass parametric mini-project problem from Week 7 (the DFS portfolio benefits from polish before Mock #2). The Phase-2 retrospective at the end of Week 9 will be much easier if the W6, W7, and W8 mini-projects are all polished by Sunday Week 8.

If you find yourself *behind* by Wednesday, skip Exercise 3 (two-heap median) for now and prioritize Exercise 2 (k-closest) — k-closest is the most heavily-graded Phase-2 heap problem in Mock #2, and the two-heap pattern can be picked up in 45 minutes once the size-k template is fluent.

---

## Up next

[Week 9 — Mock Interview #2](../week-09-mock-interview-2/) — once your three heap write-ups are pushed, your top-k template is reflexive, and you can write the two-heap median from memory without consulting the lecture.

---

*If you find errors in this material, please open an issue or send a PR. Future learners will thank you.*
