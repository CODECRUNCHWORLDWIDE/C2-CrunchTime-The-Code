# Week 11 — Homework

Six problems, all original, all with a runnable worked answer beside this page.
Allow about five hours. Do each with the lectures closed; open the worked answer
only after your own version runs, or after fifteen minutes stuck on one step.

The six cover the shapes the week teaches that the exercises did not: a 1D count
with a two-step lookahead, a grid optimised rather than counted, a 1D pass that
has to carry two states at once, and three two-string tables.

| # | Problem | Sub-shape | Est. time |
|---|---------|-----------|----------:|
| 1 | [The Ledger Ribbon](#problem-1--the-ledger-ribbon) | 1D count with a two-character lookahead | 45 min |
| 2 | [The Kiln Flue Draw](#problem-2--the-kiln-flue-draw) | The counting grid with `min` where it had `+` | 40 min |
| 3 | [The Gauge Drift Run](#problem-3--the-gauge-drift-run) | One pass carrying two states, because negatives swap them | 50 min |
| 4 | [The Stencil Match Count](#problem-4--the-stencil-match-count) | Two-string counting table | 50 min |
| 5 | [The Two-Clerk Day Book](#problem-5--the-two-clerk-day-book) | Two-string reachability, where greedy is wrong | 55 min |
| 6 | [The Paired Manifest Strike](#problem-6--the-paired-manifest-strike) | Two-string table, then one line of arithmetic | 45 min |

Every worked answer runs on its own with no arguments and no packages, and ends
by printing `All checks passed.` Run one like this:

```bash
python problem-01-ledger-ribbon-solution.py
```

---

## Problem 1 — The Ledger Ribbon

**The brief.** An old adding machine prints a ribbon of digits with **no
separators** between entries. Each entry is one or two digits and names a till
code from 1 to 26. No entry may start with a zero, because the machine never
printed a leading zero — so a `0` on the ribbon can only ever be the second digit
of `10` or `20`.

Count the readings that account for every digit.

**The data.** Ribbons including `1226`, `1010`, `2101`, `111111`, `27`, `06`,
`100` and `2626262626`.

**Constraints.** A reading has to account for **every** digit — no leftovers. An
unreadable ribbon has zero readings, which is a real answer.

**Answer.** Build the count left to right. The number of readings of the first
`n` digits depends on exactly two things: the count for `n - 1` digits, when the
last digit stands alone as a valid entry, and the count for `n - 2`, when the
last two digits together do. Add whichever apply.

Only those two ever matter, so the whole table is two integers rather than a
list.

`1226` reads **five** ways. `100` reads **none** — `10-0` fails because 0 is not
an entry, and `1-00` fails for the same reason twice.

**Signatures.** `is_entry(digits)`, `reading_count(ribbon)`,
`reading_table(ribbon)`, `first_dead_prefix(ribbon)`.

**Watch for.** Treating `06` as 6 — the leading zero is what makes it invalid,
and the whole zero rule follows from it. Six ones give 13 readings, which is a
Fibonacci number and a good check. But `2626262626` gives **32**, not a Fibonacci
number, because `62` is over 26 and only every other pair is an entry — worth
checking by hand, precisely because it looks like it should behave the same way.

The empty ribbon has **one** reading, the empty one. That is not a special case
to add; it is what makes the recurrence start cleanly.

**Worked answer.** [`problem-01-ledger-ribbon-solution.py`](./problem-01-ledger-ribbon-solution.py)

---

## Problem 2 — The Kiln Flue Draw

**The brief.** A bottle kiln is packed as a grid of shelves, each costing a
known number of fuel units. The flue draws from the top-left shelf to the
bottom-right one, and heat only moves **down or right**. Find the cheapest draw —
the total fuel of the shelves the heat passes through, both ends included.

**The data.**

```text
 1   3   1   8
 1   5   1   2
 4   2   1   9
 7   6   3   1
```

**Constraints.** Greedy fails on the **first step**. Down from the corner costs 1
and right costs 3, so a greedy fireman goes down — and the cheapest draw goes
right, along the top row to the cheap third column.

**Answer.** This is [Exercise 4](../exercises/exercise-04-terrace-route-table.md)
with one thing changed. There the answer was how many routes exist and the two
routes arriving at a shelf were combined with `+`; here it is the best one, so
they are combined with `min`. The row-by-row fill, the special first row and
column, the single pass — all identical.

Naming that one line is the whole write-up.

Cheapest draw on this kiln: **11 fuel units**, over seven shelves. The file also
ships `route_count`, which is the same fill with `+` instead of `min` and gives
**20** — so you can run both and see that the shape of a table and what you put
in it are separate decisions.

**Signatures.** `check_kiln(kiln)`, `draw_table(kiln)`, `cheapest_draw(kiln)`,
`draw_route(kiln)`, `route_count(kiln)`.

**Watch for.** Reading a neighbour that has not been filled yet. Forgetting that
the first row and first column each have only one way in. A route always passes
through `height + width - 1` shelves whatever it costs, which is a check that
does not depend on the numbers at all.

**Worked answer.** [`problem-02-kiln-flue-draw-solution.py`](./problem-02-kiln-flue-draw-solution.py)

---

## Problem 3 — The Gauge Drift Run

**The brief.** A tide gauge is checked every day and the check records a **drift
factor** — the number the day's readings must be multiplied by to correct them. A
factor of 1 means the gauge was right. A **negative** factor means the float was
stuck upside down and the readings came out inverted.

Find the run of consecutive days whose factors multiply to the **largest**
number.

**The data.** `2, 3, -2, 4, -1, 2, 2, -3, 1, 2` — a fortnight, with three
inverted days.

**Constraints.** The factors are whole numbers, so the arithmetic stays exact. A
run of one day is allowed, so the answer is never worse than the best single
factor.

**Answer.** The trap is the negatives, and it is a good one: a running product
that is **badly negative** is one negative day away from being the best product
in the record. So tracking the best run so far is not enough.

Carry **both** the best and the worst run ending at each day. On a negative day
they swap — and both candidates must be computed from the *old* pair before
either is written back, which is one line and the most common place to get this
wrong.

**Signatures.** `worst_drift(factors)`, `worst_drift_run(factors)`,
`daily_best(factors)`.

**Watch for.** Tracking only the best: `(2, -3, -4, 1)` then comes out as 2 when
24 is right. A zero cuts the record in two — nothing multiplies across it and
survives — and when every run through it is worse, zero itself is the answer.
`worst_drift_run` is a brute force over every run, shipped so the one-pass
version has something to be checked against on every prefix rather than only on
the whole record.

**Worked answer.** [`problem-03-gauge-drift-run-solution.py`](./problem-03-gauge-drift-run-solution.py)

---

## Problem 4 — The Stencil Match Count

**The brief.** A depot stencils long runs of characters onto crate sides. An
inspector looks for a short mark inside a run, and the mark's characters must
appear **in order but not necessarily next to each other** — the die skips.

Count how many distinct ways the mark can be picked out of the run. Two ways are
distinct when they use different positions, even if they read the same.

**The data.** Run `RABBABRAB`, mark `RAB`.

**Constraints.** Order matters and adjacency does not. `BA` is not in a run where
every `A` precedes every `B`.

**Answer.** A two-dimensional table where every entry has the same shape of
answer. To account for the first `m` characters of the mark using the first `r`
of the run, either the run's character is **not used** — which is the entry one
column left — or it **is used and matches**, which is the entry one row up and
one column left. Add them.

The empty mark is found exactly once, by taking nothing, which is what makes the
first row all ones and lets the recurrence start without a special case.

`RAB` sits inside `RABBABRAB` **eight** ways.

**Signatures.** `match_count(run, mark)`, `match_table(run, mark)`,
`first_match(run, mark)`.

**Watch for.** Filling the table in an order that reads entries not yet written.
Forgetting the "not used" branch, which is taken on *every* cell including the
matching ones. `AAA` contains `AA` three ways, not one — repeats multiply, and
that is the case to check by hand first.

**Worked answer.** [`problem-04-stencil-match-count-solution.py`](./problem-04-stencil-match-count-solution.py)

---

## Problem 5 — The Two-Clerk Day Book

**The brief.** Two clerks share one day book. Each writes their own entries into
it as the day goes on, so the finished book holds both clerks' entries
interleaved — but **each clerk's entries appear in the order that clerk wrote
them**, because neither goes back.

Given both clerks' own records and the finished book, say whether the book could
have been produced this way.

**The data.** Clerk one `ABAB`, clerk two `AABB`, day book `AABABABB`. Plus a
second, smaller book built to catch a greedy reader: clerk one `AA`, clerk two
`AB`, book `AABA`.

**Constraints.** Neither clerk's order may change. The lengths have to add up,
which is worth checking first because it is free.

**Answer.** The obvious approach — walk the book and hand each entry to whichever
clerk has it next — is **wrong**, and wrong in a way that looks right on most
data. When both clerks are due to write the same character, choosing one commits
you.

On the trap book, the greedy reader takes both of clerk one's `A`s and then has
nothing that can write the `B`. It answers **False**; the table answers **True**.
The file ships both so you can run them side by side.

The table is the answer: entry `[a][b]` says whether the first `a` entries of
clerk one and the first `b` of clerk two could have made the first `a + b`
entries of the book. A cell is reachable when the cell above it is and clerk
one's next entry matches, or the cell to its left is and clerk two's does.

**Signatures.** `interleaves(first, second, book)`,
`interleave_table(first, second, book)`,
`greedy_interleaves(first, second, book)`, `split_book(first, second, book)`.

**Watch for.** Reaching for the greedy version because the book is short. Two
empty records make an empty book and nothing else. `split_book` walking the
finished table backwards is what turns "yes it interleaves" into "here is who
wrote each line", which is the part a clerk can act on.

**Worked answer.** [`problem-05-two-clerk-daybook-solution.py`](./problem-05-two-clerk-daybook-solution.py)

---

## Problem 6 — The Paired Manifest Strike

**The brief.** A cargo is listed twice — once by the shipper and once by the
receiving depot. The two disagree, and the clerk strikes lines out of each until
they read the same. Nothing may be added and nothing reordered; only whole lines
struck out.

Report the fewest strikes, counting a strike on either manifest as one.

**The data.**

```text
shipper   SALT  HIDES  TALLOW  OATS  PITCH  ROPE
depot     HIDES  SALT  OATS  TAR  ROPE
```

**Constraints.** `HIDES` is on both manifests and **cannot survive**, because it
comes before `SALT` on one and after it on the other. That is the whole reason
this is not a set intersection, and it is the first thing to check by hand.

**Answer.** The lines that survive are the same on both sides *and in the same
order* on both — the longest run common to the two manifests without needing to
be contiguous. Once that length is known the answer is one line of arithmetic:

```text
strikes = len(shipper) + len(depot) - 2 * len(common run)
```

Deriving that line is the exercise; the table under it is the ordinary two-string
fill — matching lines take the diagonal plus one, mismatching lines take the
better of up and left.

`SALT OATS ROPE` survives, so `6 + 5 - 2 × 3 = 5` strikes.

**Signatures.** `common_run(shipper, depot)`, `run_table(shipper, depot)`,
`strikes_needed(shipper, depot)`, `struck_lines(shipper, depot)`.

**Watch for.** Intersecting the two as sets, which keeps `HIDES` and gives 3.
Counting a strike on both sides as one. Identical manifests need zero strikes;
manifests with nothing in common lose everything on both sides. `struck_lines`
is the useful output — a count alone is not something a clerk can act on.

**Worked answer.** [`problem-06-paired-manifest-strike-solution.py`](./problem-06-paired-manifest-strike-solution.py)

---

## Rubric (5 axes, 4 points each)

| Axis | What "great" looks like |
|------|--------------------------|
| Frame the problem | The memo names the state — what one table entry *means*, in a sentence — and the base case, before any recurrence. |
| Reason about options | Four to six bullets before any code, with the greedy or brute-force alternative named and, where it is wrong, said to be wrong and why. |
| Assemble the solution | Idiomatic Python; the fill order stated and justified; type hints throughout. |
| Measure it | A trace on at least two inputs, one degenerate, and — where the file prints a table — the table read back in the write-up. |
| Evaluate the cost | Time, space, best/average/worst, the trade-off and the improvement. Three of these six reduce to a couple of variables; say which and why. |

Twenty points per problem, 120 for the set. Score yourself honestly; the number
is only useful if it is true.

---

## How to submit

Commit your write-ups under `frame-writeups/c2-week-11/homework/`, one file per
problem:

```
frame-writeups/c2-week-11/homework/
├── problem-1-ledger-ribbon.md
├── problem-2-kiln-flue-draw.md
├── problem-3-gauge-drift-run.md
├── problem-4-stencil-match-count.md
├── problem-5-two-clerk-daybook.md
└── problem-6-paired-manifest-strike.md
```

Each file is 100–200 lines: the five FRAME sections plus a five-line memo at the
top. The code is part of the Assemble section, not a separate file.

When the set is done, push and move on to the
[mini-project](../mini-project/README.md).

---

## Time budget

| Problem | Solve | Write-up | Total |
|---------|------:|---------:|------:|
| 1 — Ledger Ribbon | 30 min | 15 min | 45 min |
| 2 — Kiln Flue Draw | 25 min | 15 min | 40 min |
| 3 — Gauge Drift Run | 35 min | 15 min | 50 min |
| 4 — Stencil Match Count | 35 min | 15 min | 50 min |
| 5 — Two-Clerk Day Book | 40 min | 15 min | 55 min |
| 6 — Paired Manifest Strike | 30 min | 15 min | 45 min |

About four and a half hours. Problems 2, 3 and 5 are the three worth the most:
each one is a familiar algorithm with exactly one thing changed, and being able
to say **which thing** is what separates knowing a recipe from knowing a method.
