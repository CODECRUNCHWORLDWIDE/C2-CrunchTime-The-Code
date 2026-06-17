# Week 4 — Exercises

Four drills. Each is UMPIRE-narrated, recorded, and graded by [`timed_runner.py`](./timed_runner.py).

| # | Drill | Pattern | Difficulty | Target solve time |
|---|-------|---------|------------|------------------:|
| 1 | [Linked list cycle](./drill-01-linked-list-cycle.md) | Floyd's detection | Easy | 15 min |
| 2 | [Cycle start](./drill-02-cycle-start.md) | Floyd's + `2k=k+nC` lemma | Medium | 25 min |
| 3 | [Middle of linked list](./drill-03-middle-of-list.md) | Speed-2 midpoint | Easy | 15 min |
| 4 | [Happy number](./drill-04-happy-number.md) | Floyd's on a functional graph | Easy/Medium | 20 min |

Do them in order. Drill 1 is the simplest application of Floyd's; Drill 2 builds on it with the lemma; Drill 3 is the most common variant (midpoint, no cycle); Drill 4 transfers the pattern to a non-linked-list structure.

After all four drills pass `timed_runner.py`, move on to [the challenge](../04-challenges/challenge-01-reorder-linked-list.md) — which uses Drill 3 (find midpoint) as one of three sub-steps.

Run the harness:

```bash
pytest exercises/timed_runner.py -v
```

Each drill has its own write-up template at the bottom of the drill file. Use it.
