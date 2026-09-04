# Week 11 — Exercises

Four exercises, in order. Each has a page with the brief, the constraints, the
worked solution and the acceptance checklist, and a runnable file beside it that
ends by printing `All checks passed.`

| # | Exercise | Sub-shape | Difficulty | Target time |
|---|----------|-----------|------------|------------:|
| 1 | [Ferry Ramp Manifests](./exercise-01-ferry-ramp-manifests.md) | 1D counting, and the whole prefix table rather than one answer | Easy | 35 min |
| 2 | [The Survey Station Walk](./exercise-02-survey-station-walk.md) | 1D optimisation with a stated tie-break | Medium | 40 min |
| 3 | [The Stencil Line](./exercise-03-stencil-line-split.md) | 1D over a string, against a code book | Medium | 45 min |
| 4 | [The Terrace Route Table](./exercise-04-terrace-route-table.md) | 2D counting with blocked cells | Medium | 40 min |

Do them in order. Exercise 1 returns the whole table rather than a single number,
which is the habit the rest of the week depends on — a dynamic-programming answer
is a table, and reading it back is how you check yourself. Exercise 2 adds a
tie-break, so "best" stops being a single comparison. Exercise 3 moves the same
1D shape onto a string, where the transitions come from a dictionary rather than
from arithmetic. Exercise 4 is the first two-dimensional table, and
[Homework 2](../homework/README.md) is that same table with `min` where this one
has `+`.

Run any of them directly:

```bash
python exercise-01-ferry-ramp-manifests.py
```

No packages, no arguments, no input.

## A note on what is being graded

**Say what one table entry means, in a sentence, before writing a recurrence.**
That sentence is the whole of the Frame step for this pattern, and a recurrence
written without it is a guess that happens to work on the example. "Entry `k` is
the number of distinct stint sequences that load exactly `k` vehicles" is the
sentence; `dp[k] = dp[k-1] + dp[k-2] + dp[k-3]` is what follows from it.

**Then say the fill order and why it is safe.** Every recurrence here reads
entries that must already be written, and the argument for why they are is one
line — usually that the index it reads is strictly smaller. It is also the first
thing to check when a table comes out full of zeroes.

---

After all four pass, move on to
[Challenge 1 — The Timetable Amendment Slip](../challenges/challenge-01-timetable-amendment.md).
