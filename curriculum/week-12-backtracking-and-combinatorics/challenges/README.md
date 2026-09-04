# Week 12 — Challenges

Two challenges. Challenge 1 is the required deliverable; Challenge 2 is the
stretch.

| # | Challenge | Sub-shape | Difficulty | Target time |
|---|-----------|-----------|------------|------------:|
| 1 | [The Kiln Firing Trail](./challenge-01-kiln-firing-trail.md) | Backtracking on a grid, with a visited set that has to be undone | Hard | 75 min |
| 2 | [The Warped Drying Rack](./challenge-02-drying-rack-sensors.md) | Constraint satisfaction with three pruning sets | Hard | 75 min |

Challenge 1 is [Exercise 1](../exercises/exercise-01-glaze-sample-set.md)'s
template on a grid, with [Exercise 2](../exercises/exercise-02-firing-order.md)'s
used set doing the work — a walk that must not enter the same cell twice on one
trail, and must release it when it backs out. The exercises made both halves of
that undo fail on purpose; this is where forgetting one produces a plausible
number rather than an obvious mess.

Challenge 2 is the constraint-satisfaction shape. Three sets track what is
already claimed, and every one of them is checked before descending rather than
after — which is the same decision
[Homework 6](../homework/README.md) measures at six orders of magnitude.

Both have a runnable worked solution beside the page:

```bash
python challenge-01-kiln-firing-trail.py
```

**How these differ from the exercises.** You choose the state: what goes in the
trail, what goes in the sets, and what is checked before a branch is entered
rather than after. The write-up has to defend those choices and name what it
rejected. Allocate the full target time; the reasoning is most of it.
