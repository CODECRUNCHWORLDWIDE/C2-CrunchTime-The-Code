# Week 8 — Exercises

Five exercises, in order. Each has a page with the brief, the constraints, the
worked solution and the acceptance checklist, and a runnable file beside it that
ends by printing `All checks passed.`

| # | Exercise | Sub-shape | Difficulty | Target time |
|---|----------|-----------|------------|------------:|
| 1 | [The Sluice Gate Order](./exercise-01-sluice-gate-order.md) | `heapify`, `heappush`, `heappop`, reading the front | Beginner | 45 min |
| 2 | [The Crest Watch Shortlist](./exercise-02-crest-watch-shortlist.md) | Bounded top-k — the heap's size is the answer | Beginner-Medium | 30 min |
| 3 | [The Tool Bench Rota](./exercise-03-tool-bench-slots.md) | A max-heap out of `heapq`, by negation | Beginner-Medium | 35 min |
| 4 | [The Rescue Intake Desk](./exercise-04-rescue-intake-queue.md) | Heap of tuples, and the tiebreaker that stops it crashing | Medium | 35 min |
| 5 | [The Estuary Ledger](./exercise-05-tide-log-stitch.md) | k-way merge — one entry per source, not one per row | Medium | 35 min |

Do them in order. Exercise 1 gets the first surprise out of the way — a heap is
not a sorted list — and everything after it is that page with more on top.
Exercise 2 is where the heap's size bound becomes the argument. Exercise 3 is the
negation. Exercise 4 is the tuple, and the `TypeError` that arrives only on a busy
day. Exercise 5 is the merge, which
[Challenge 1](../challenges/challenge-01-hut-roll-call-stitch.md) then makes lazy.

Run any one of them directly:

```bash
python exercise-01-sluice-gate-order-solution.py
```

No packages, no arguments, no input.

## A note on what is being graded

Phase 1 graded you mostly on *correctness*. Phase 2 adds the **defence** axis: for
every heap exercise, your write-up must say which sub-shape you used — bounded
top-k, negated max-heap, heap of tuples, k-way merge, lazy deletion — why, and
what the failure mode of the wrong choice would have been. The recording catches
whether you say it; the write-up catches whether you can write it.

For Week 8 specifically the defence includes:

- **Why a heap and not `sorted(...)`.** Say the `O(n log k)` against `O(n log n)`
  discriminator out loud, and say the space difference too — it is usually the
  stronger half of the argument.
- **Why a min-heap for the k largest.** The heap holds the k largest so far, and
  the smallest of them is the bar every new candidate has to clear. Getting this
  the right way round is the whole of Exercise 2.
- **The tiebreaker rule** whenever the heap holds tuples with a payload that
  cannot be compared. Exercise 4 shows what happens without it.

Defence is the difference between "the code works" and "the code is robust."
Drill the second one.

---

After all five pass, move on to
[Challenge 1 — The Hut Roll Call](../challenges/challenge-01-hut-roll-call-stitch.md),
which is Exercise 5 again with the merge made lazy.
