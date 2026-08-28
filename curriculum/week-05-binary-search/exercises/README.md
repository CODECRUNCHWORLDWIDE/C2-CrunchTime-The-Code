# Week 5 — Exercises

Five drills. Each is FRAME-narrated, recorded, and graded by [`timed_runner.py`](timed_runner.py).

| # | Drill | Pattern | Difficulty | Target solve time |
|---|-------|---------|------------|------------------:|
| 1 | [The Ladder Seat](exercise-01-ladder-seat.md) | Variant 1 — closed interval, find any, on a **descending** sequence | Easy | 12 min |
| 2 | [The Scan Window](exercise-02-scan-window.md) | Variants 2 + 3 — lower bound applied twice to a run of duplicates | Easy/Medium | 20 min |
| 3 | [The Ring Buffer Probe](exercise-03-ring-buffer-probe.md) | Rotated sequence — wrap point plus a rotated-index accessor | Medium | 25 min |
| 4 | [The Quote Rank](exercise-04-quote-rank.md) | Binary search on **values** with a monotone counting predicate | Medium/Hard | 35 min |
| 5 | [The Paving Reach](exercise-05-paving-reach.md) | Binary search on the **answer** (parametric) | Medium | 30 min |

Do them in order. Drills 1, 2, 3 cement the classic templates — and each one carries a deliberate twist, so none of them can be typed from muscle memory. Exercise 4 makes the leap to "binary search on values" with a counting predicate. Exercise 5 is the canonical parametric problem — the highest-yield interview skill of the week.

After all five drills pass `timed_runner.py`, move on to [the challenge](../challenges/challenge-01-order-book-boundary.md) — The Merged Book Boundary, the hardest binary-search shape in the course.

Run the harness:

```bash
pytest exercises/timed_runner.py -v
```

The harness imports your solutions from a module called `solutions` sitting next to it; point it somewhere else with `C2_WEEK05_SOLUTIONS=my.module`. Functions you have not written yet are reported as skipped, so you can run it after Exercise 1 and watch the skips turn into passes across the week.

Each drill has its own write-up template at the bottom of the drill file. Use it.

## A note on what is being graded

Phase 1's drills graded you mostly on *correctness*. Phase 2's drills add a second axis: **boundary defense**. For every drill, your write-up must state the boundary convention you chose (`closed [lo, hi]` or `half-open [lo, hi)`) and justify the shrink rules in one sentence. The recording catches whether you say it; the write-up catches whether you can write it.

Boundary defense is the difference between "the code works" and "the code is robust." Interviewers test for the latter. Drill on the latter.

## A note on the contracts

Every drill this week defines its own **absent** and **degenerate** cases, and none of them uses an in-band sentinel. `None` means absent; `0` and `-1` are legitimate values in several of these problems and cannot double as failure codes. Read each contract before you write the signature — three of the five return something other than a bare index, and the harness checks all of it.
