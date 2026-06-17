# Week 5 — Exercises

Five drills. Each is UMPIRE-narrated, recorded, and graded by [`timed_runner.py`](./timed_runner.py).

| # | Drill | Pattern | Difficulty | Target solve time |
|---|-------|---------|------------|------------------:|
| 1 | [Classic binary search](./drill-01-classic-binary-search.md) | Variant 1 — closed interval, find any | Easy | 12 min |
| 2 | [Find first and last](./drill-02-find-first-and-last.md) | Variants 2 + 3 — lower / upper bound on duplicates | Easy/Medium | 20 min |
| 3 | [Search in rotated sorted array](./drill-03-search-in-rotated.md) | Variant 1 + "which half sorted?" | Medium | 25 min |
| 4 | [Kth element in a sorted matrix](./drill-04-kth-element-in-sorted-matrix.md) | Binary search on values + `count_le` predicate | Medium/Hard | 35 min |
| 5 | [Koko eats bananas](./drill-05-koko-bananas.md) | Binary search on the answer (parametric) | Medium | 30 min |

Do them in order. Drills 1, 2, 3 cement the classic templates. Drill 4 makes the leap to "binary search on values" with a counting predicate. Drill 5 is the canonical parametric problem — the highest-yield interview skill of the week.

After all five drills pass `timed_runner.py`, move on to [the challenge](../04-challenges/challenge-01-median-of-two-sorted-arrays.md) — Median of Two Sorted Arrays, the canonical hard binary-search application.

Run the harness:

```bash
pytest exercises/timed_runner.py -v
```

Each drill has its own write-up template at the bottom of the drill file. Use it.

## A note on what is being graded

Phase 1's drills graded you mostly on *correctness*. Phase 2's drills add a second axis: **boundary defense**. For every drill, your write-up must state the boundary convention you chose (`closed [lo, hi]` or `half-open [lo, hi)`) and justify the shrink rules in one sentence. The recording catches whether you say it; the write-up catches whether you can write it.

Boundary defense is the difference between "the code works" and "the code is robust." Interviewers test for the latter. Drill on the latter.
