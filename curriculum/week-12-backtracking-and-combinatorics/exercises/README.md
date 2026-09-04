# Week 12 — Exercises

Four exercises, in order. Each has a page with the brief, the constraints, the
worked solution and the acceptance checklist, and a runnable file beside it that
ends by printing `All checks passed.`

| # | Exercise | Sub-shape | Difficulty | Target time |
|---|----------|-----------|------------|------------:|
| 1 | [The Glaze Sample Set](./exercise-01-glaze-sample-set.md) | Choose, explore, undo — with the recording at every node | Easy | 30 min |
| 2 | [The Firing Order](./exercise-02-firing-order.md) | When an index is not enough, and the undo grows a second half | Easy-Medium | 30 min |
| 3 | [The Clay Weigh-Out](./exercise-03-clay-weigh-out.md) | Two prunes: one saves work, one fixes the answer | Medium | 40 min |
| 4 | [The Repeat Bin Picks](./exercise-04-repeat-bin-picks.md) | Deduplication, and the plausible wrong fix | Medium | 40 min |

Do them in order. Every page is the same three lines with one thing added, and
the order is the argument.

Exercise 1 is the template with nothing on top, and it settles where the
recording goes — at every node, because a subset is finished the moment you stop
adding to it. Exercise 2 changes what is being enumerated and with it the
bookkeeping: an order can put any unused item next, so an index cannot track it,
and the undo has to grow a second half. Exercise 3 cuts the walk short, twice,
for two entirely different reasons. Exercise 4 removes duplicates, and its
plausible wrong fix returns exactly as many answers as the right one.

Run any of them directly:

```bash
python exercise-01-glaze-sample-set.py
```

No packages, no arguments, no input.

## A note on what is being graded

**Every one of these four ships a wrong version alongside the right one**, and
that is the design of the week rather than a flourish. Backtracking fails
quietly: it does not raise, it does not hang, it returns a list of the right
sort of thing with the wrong things in it. Four specific quiet failures, seen
once each:

- **No undo** — the right number of subsets, the wrong subsets.
- **Half an undo** — exactly one answer where there should be six.
- **No index rule** — six ways where three exist, because orderings are being
  counted as combinations.
- **Skipping repeats everywhere** — the right *count*, only eight of which are
  distinct, and a pick that should exist quietly missing.

Your write-ups should name which failure the page is guarding against and what
its symptom looks like. "The undo restores the state" is a sentence anyone can
write; "without it, the count is right and the contents are not" is the one that
means you have run it.

**And say the growth out loud.** Four of these enumerate something exponential
or factorial. Naming the number — `2 ** n`, `n!` — before writing code is the
first line of the memo, because it is what decides whether the walk is a
reasonable answer at all.

---

After all four pass, move on to
[Challenge 1 — The Kiln Firing Trail](../challenges/challenge-01-kiln-firing-trail.md),
which is Exercise 1's template on a grid, with the visited set that Exercise 2's
used set was practice for.
