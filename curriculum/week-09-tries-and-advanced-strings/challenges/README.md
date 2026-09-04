# Week 9 — Challenges

Two challenges. Do at least the first; the second is shorter and catches a
mistake almost everybody makes.

| # | Challenge | Sub-shape | Difficulty | Target time |
|---|-----------|-----------|------------|------------:|
| 1 | [The Cold Store Aisle Sweep](./challenge-01-cold-store-aisle-sweep.md) | One tree over the whole word list, one walk of the grid | Hard | 70 min |
| 2 | [The Berth Ledger Shorthand](./challenge-02-berth-ledger-shorthand.md) | The longest matching stem, not the first one | Medium-Hard | 55 min |

Challenge 1 is the composition the week exists for: a grid walk whose pruning
comes from a prefix tree, so that the walk stops early for every code at once
rather than once per code. It ships both versions and prints both step counts, so
the argument is a number rather than a paragraph.

Challenge 2 is shorter and its whole difficulty is one line. Walking a name
against a tree of stems and returning the first stem you meet is the natural way
to write it, it is wrong, and it passes any test data where no stem is a prefix
of another. The register on that page has two such pairs on purpose.

Both have a runnable worked solution beside the page:

```bash
python challenge-01-cold-store-aisle-sweep.py
```

Each challenge page contains the brief, the constraints including the alternative
to reject, a real captured run, the full solution, the bugs it prevents, and an
acceptance checklist.

The challenges differ from the exercises in two ways:

1. **You design the representation.** The function names are given; what a node
   carries, and what the walk remembers as it goes, are yours to choose and yours
   to defend.
2. **Longer target time.** Fifty-five to seventy minutes against forty. Both have
   a correct-but-slow version that is worth writing first, and both pages ask you
   to keep it and compare.

If you are stuck past ninety minutes on Challenge 1, the thing to check is the
unmarking: a walk that marks a bin on entry and never unmarks it on the way back
out produces confident, wrong, much smaller answers.
