# Week 14 — Exercises

Three exercises, in order. Each has a page with the brief, the constraints, the
worked solution and the acceptance checklist, and a runnable file beside it that
ends by printing `All checks passed.`

Mock #3 is on Friday, so this week is deliberately light on exercises and heavy
on the mock. Three is enough to install the three ideas the rest of the week
uses.

| # | Exercise | Sub-shape | Difficulty | Target time |
|---|----------|-----------|------------|------------:|
| 1 | [The Relay Fold](./exercise-01-relay-fold.md) | XOR, and the three properties that make it work | Easy | 30 min |
| 2 | [The Set-Bit Tally](./exercise-02-set-bit-tally.md) | A table where every answer is one step from a smaller one | Easy-Medium | 35 min |
| 3 | [The Mask Roster](./exercise-03-mask-roster.md) | A whole set in one integer, and every set operation as arithmetic | Medium | 40 min |

Do them in order.

Exercise 1 is XOR with nothing on top, and it gets the honest part out of the way
early: the fold alone cannot tell "one unpaired code" from "three", so the
contract needs a count as well. [Homework 1](../homework/README.md) then makes
the fold fail on purpose.

Exercise 2 is the first bit problem whose answer is a *table*, and it introduces
`n &= n - 1` — the single most useful idiom in the week, reused twice in the
homework.

Exercise 3 is the bridge back to Week 12. Enumerating every subset there was a
recursive walk with a trail and an undo; here it is `range(1 << n)`, one line.
Both are right, and saying which generalises and which is faster is the whole
page.

Run any of them directly:

```bash
python exercise-01-relay-fold-solution.py
```

No packages, no arguments, no input.

## A note on what is being graded

**Check with a property, not with examples.** Bit code is exactly the kind that
passes six hand-picked cases and fails the seventh, and the failures are silent —
no exception, just a number that is wrong. Every page this week leans on checks
that need no known-good answer:

- the two counting methods agree on **every** value up to the limit;
- the mask and set versions of `covers` agree on **all 256 pairs** of shifts;
- reversing twice gives back the original;
- swapping pairs twice gives back the original.

Your write-ups should name the property you checked, not the examples you tried.

**And say the width out loud.** Every function here has a register width behind
it, and Python's unbounded integers will happily let you forget. A negative value
has no finite binary width at all, which is why the clearing loop is guarded
rather than trusted — and that guard is a good sentence for the Frame section.

---

After all three pass, move on to
[Challenge 1 — Mock #3](../challenges/challenge-01-mock-3-timed-round.md). It is
the week's keystone; the exercises are the warm-up for it.
