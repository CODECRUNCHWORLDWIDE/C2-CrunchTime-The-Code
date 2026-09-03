# Week 12 — Homework

Six problems, all original, all with a runnable worked answer beside this page.
Allow about five hours. Do each with the lectures closed; open the worked answer
only after your own version runs, or after fifteen minutes stuck on one step.

The six carry on from the exercises: a fixed-size choice, a fixed-depth product,
a count-based prune, a fixed split with three prunes, both dedup rules at once,
and the constraint-satisfaction shape.

| # | Problem | Sub-shape | Est. time |
|---|---------|-----------|----------:|
| 1 | [The Tasting Panel](#problem-1--the-tasting-panel) | Subsets of a fixed size, and the short-branch prune | 40 min |
| 2 | [The Dial Board](#problem-2--the-dial-board) | One level per position, every option at each | 35 min |
| 3 | [The Sluice Pairing](#problem-3--the-sluice-pairing) | Pruning on a count rather than a set | 50 min |
| 4 | [The Grid Reference Split](#problem-4--the-grid-reference-split) | Fixed depth, variable width, three prunes | 55 min |
| 5 | [The Tare Weight Picks](#problem-5--the-tare-weight-picks) | Both rules at once — each item once, and no duplicates | 55 min |
| 6 | [The Test Tray Fill](#problem-6--the-test-tray-fill) | Constraint satisfaction, and where the check goes | 55 min |

Every worked answer runs on its own with no arguments and no packages, and ends
by printing `All checks passed.` Run one like this:

```bash
python problem-01-tasting-panel-solution.py
```

---

## Problem 1 — The Tasting Panel

**The brief.** A pottery co-operative picks a tasting panel from its members.
The panel holds exactly `size` people, and **who** is on it matters while the
order does not.

**The data.** Six members — Ada, Bram, Cato, Devi, Enid, Fen — and a panel of
three.

**Constraints.** A panel of zero is one panel, the empty one. A panel bigger than
the roster cannot be formed at all.

**Answer.** [Exercise 1](../exercises/exercise-01-glaze-sample-set.md) with the
size fixed, which changes two things. The recording moves from every node to the
nodes where the trail is full. And a new prune becomes possible: **once there are
not enough members left to fill the panel, the branch is dead however it
continues**, so it can be abandoned before it is walked.

Six choose three is 20 panels. The prune does not change that; it changes the
number of nodes, and the file prints both so the saving is a number.

**Signatures.** `panels(members, size)`, `panels_unpruned(members, size)`,
`panels_with(members, size, member)`, `panel_count(members, size)`.

**Watch for.** Recording at every node as in Exercise 1 — you get all 64 subsets
rather than the 20 panels. Pruning with `<` where `<=` belongs, which drops the
panels that use exactly the remaining members. Each member should sit on exactly
10 of the 20, which is a check worth doing because it does not depend on your
implementation.

The sizes across the whole roster come out as 1, 6, 15, 20, 15, 6, 1 and sum to
64 — Exercise 1's answer arrived at from the other direction.

**Worked answer.** [`problem-01-tasting-panel-solution.py`](./problem-01-tasting-panel-solution.py)

---

## Problem 2 — The Dial Board

**The brief.** An old works telephone has letters printed on its dial keys.
Somebody remembers which **keys** they pressed for an extension but not which
letter each press was meant to be. List every extension the presses could have
meant.

**The data.** The dial, with keys 1 and 0 carrying no letters at all, and the
presses `273`.

**Constraints.** A key carrying no letters cannot contribute a character, so a
press on 1 or 0 is refused rather than skipped — skipping it would silently
shorten every answer. No presses means nobody dialled, so the answer is an empty
list rather than a list holding the empty string. That is a decision, and the
opposite convention would make the count 1 rather than 0.

**Answer.** One level per press rather than one per item, and at each level try
every letter on that key. Nothing is skipped and nothing is pruned — every branch
runs to the bottom.

That makes this the cleanest place to see that the **shape of the tree comes
from the problem**, not from the template. The three lines are the same three
lines they have been all week.

`273` gives 36 extensions: `3 × 4 × 3`, one factor per key.

**Signatures.** `extensions(presses, dial)`, `extension_count(presses, dial)`,
`extensions_matching(presses, dial, opening)`.

**Watch for.** Skipping a letterless key instead of refusing it. Treating the
empty press string as one empty extension. The answers should come out in dial
order without a sort — if you need to sort them, the loop is wrong.

**Worked answer.** [`problem-02-dial-board-solution.py`](./problem-02-dial-board-solution.py)

---

## Problem 3 — The Sluice Pairing

**The brief.** A drainage board runs a bank of sluices. Every gate **opened**
must be **closed** before the run ends, and a gate can never be closed that was
not opened — the linkage will not allow it. List every legal sequence of opens
and closes.

**The data.** Three gates.

**Constraints.** Zero gates is one run, the empty one.

**Answer.** The interesting part is that the walk prunes on a **count** rather
than a set. There is no list of which gates are open, because the gates are
interchangeable — only how many are open matters. Two rules:

```text
open a gate     while any remain unopened
close a gate    while more have been opened than closed
```

Between them, every branch the walk takes is legal, so nothing has to be checked
at the end.

The alternative — generate every sequence of opens and closes and filter — gets
the same five answers for **127 nodes against 22**. The file prints both.

Three gates give five runs, and the counts across gate numbers are 1, 1, 2, 5,
14, 42, 132 — the Catalan numbers, which is worth naming because it tells you the
answer grows fast but nothing like `2 ** 2n`.

**Signatures.** `legal_runs(gates)`, `legal_runs_by_filter(gates)`,
`is_legal(run)`, `deepest_standing(run)`.

**Watch for.** Allowing a close when none is open — that is the whole constraint.
Recording before the run is complete. `is_legal` is written independently of the
generator on purpose: a verifier that shares the generator's assumptions verifies
nothing.

**Worked answer.** [`problem-03-sluice-pairing-solution.py`](./problem-03-sluice-pairing-solution.py)

---

## Problem 4 — The Grid Reference Split

**The brief.** A survey stamps grid references onto marker posts as four numbers
separated by dots. On old posts the dots have worn away. Given the digits, list
every reference the post could have been — **exactly four fields**, each from 0
to 255, none with a leading zero.

**The data.** Eight worn posts, including `25525511135`, `0000`, `010010` and a
fourteen-digit run.

**Constraints.** `0` is a field; `00` and `01` are not. `256` is not.

**Answer.** Fixed depth — four — with one, two or three digits at each level.
Three prunes, and **only one is an optimisation**:

```text
length prune   with `fields` left and `digits` left, dead unless
               fields <= digits <= 3 * fields          ← optional
value prune    a field over 255 is not a field         ← correctness
zero prune     a multi-digit field cannot start with 0 ← correctness
```

Telling those apart is the exercise. The length prune is what makes the
fourteen-digit post cost **1 node instead of 53**.

`010010` is the post to check by hand: it reads **two** ways, `0.10.0.10` and
`0.100.1.0`, and neither uses a leading zero. A solution that allows them finds
several more.

**Signatures.** `is_field(digits)`, `references(run)`, `references_unpruned(run)`,
`readable(run)`.

**Watch for.** Accepting `01` as 1. Forgetting that all four fields must be used
**and** all the digits consumed — checking one without the other passes on most
posts. Trying a fourth digit in a field.

**Worked answer.** [`problem-04-grid-reference-split-solution.py`](./problem-04-grid-reference-split-solution.py)

---

## Problem 5 — The Tare Weight Picks

**The brief.** A works store keeps a bag of tare weights, some of them
identical — two 3lb weights are two separate lumps of iron, and either can go on
the pan, but a pan holding one is the same pan as one holding the other. Pick
weights summing to a target, using **each lump at most once**, and list the
distinct pans.

**The data.** A bag of nine weights with two 3s and two 1s, and a target of 8.

**Constraints.** Every weight positive; a target of zero is made by the empty
pan.

**Answer.** [Exercise 3](../exercises/exercise-03-clay-weigh-out.md) and
[Exercise 4](../exercises/exercise-04-repeat-bin-picks.md) in one problem, and
the two rules pull in opposite directions:

- from Exercise 3, the sum prune and a forwards-only walk — but recursing on
  `index + 1` rather than `index`, because a lump is used once;
- from Exercise 4, sort the bag and skip a repeat at the same level.

**Those are two different bugs and they look alike.** The file ships both wrong
walks: recursing on the same index invents `2+2+2+2` off a bag holding one 2,
and dropping the dedup reports the same pan once per set of lumps. Seven distinct
pans; the two wrong walks find 16 and 10.

**Signatures.** `tare_pans(bag, target)`, `tare_pans_reusing(bag, target)`,
`tare_pans_undeduped(bag, target)`, `fewest_lumps(bag, target)`.

**Watch for.** Getting one of the two rules and not the other — each alone
produces a plausible answer. The check that catches reuse is that no pan uses
more lumps of a weight than the bag holds; the check that catches missing dedup
is that every pan appears once. Two assertions, because they are two claims.

**Worked answer.** [`problem-05-tare-weight-picks-solution.py`](./problem-05-tare-weight-picks-solution.py)

---

## Problem 6 — The Test Tray Fill

**The brief.** A glaze test tray is a square grid of wells. Every **row** must
hold each glaze exactly once, and so must every **column**. Some wells are
already filled. Finish the tray, or say it cannot be finished.

**The data.** A four-glaze tray part-filled from a previous session, and a
spoiled tray with two `A`s already sharing a column.

**Constraints.** The wells already filled are not moved. A tray that is already
spoiled is reported as spoiled, which is a better answer than "no solution
found".

**Answer.** This differs from every other walk of the week in one way: it does
not choose **which** well to fill. It fills them in a fixed order and chooses
only what goes in them. That keeps the state small — one set per row and one per
column — and makes the legality test a lookup rather than a scan.

The prune **is** the legality test, applied before descending rather than after.

That one decision is worth more here than anywhere else in the course:

```text
wells filled, pruning early :          25
wells filled, checking late :  15,836,737
```

Same tray, same answer, six orders of magnitude. If you write one sentence about
pruning all week, write it about this.

**Signatures.** `check_tray(tray, glazes)`, `already_spoiled(tray, glazes)`,
`fill_tray(tray, glazes)`, `fill_tray_late_check(tray, glazes)`.

**Watch for.** Undoing two of the three things you changed — the well, the row
set and the column set all have to go back. Scanning the row and column to test
legality instead of keeping sets, which is correct and turns a lookup into a
scan. Reporting "no solution" for a tray that was spoiled before the walk began.

**Worked answer.** [`problem-06-test-tray-fill-solution.py`](./problem-06-test-tray-fill-solution.py)

---

## Rubric (5 axes, 4 points each)

| Axis | What "great" looks like |
|------|--------------------------|
| Frame the problem | The memo names what one node of the tree is, where the answer is recorded, and how many answers there could be — before any code. |
| Reason about options | Four to six bullets before coding, separating the prunes that are optimisations from the prunes that are correctness rules. |
| Assemble the solution | Choose, explore, undo, with the undo restoring *everything* the choose changed; type hints throughout. |
| Measure it | A trace on at least two inputs, one degenerate — and for the pages that count nodes, the number quoted rather than described. |
| Evaluate the cost | Time, space, best/average/worst, the trade-off and the improvement. Say what the walk costs *before* pruning and what the prune actually buys. |

Twenty points per problem, 120 for the set. Score yourself honestly; the number
is only useful if it is true.

---

## How to submit

Commit your write-ups under `frame-writeups/c2-week-12/homework/`, one file per
problem:

```
frame-writeups/c2-week-12/homework/
├── problem-1-tasting-panel.md
├── problem-2-dial-board.md
├── problem-3-sluice-pairing.md
├── problem-4-grid-reference-split.md
├── problem-5-tare-weight-picks.md
└── problem-6-test-tray-fill.md
```

Each file is 100–200 lines: the five FRAME sections plus a five-line memo at the
top. The code is part of the Assemble section, not a separate file.

When the set is done, push and move on to the
[mini-project](../mini-project/README.md).

---

## Time budget

| Problem | Solve | Write-up | Total |
|---------|------:|---------:|------:|
| 1 — Tasting Panel | 25 min | 15 min | 40 min |
| 2 — Dial Board | 20 min | 15 min | 35 min |
| 3 — Sluice Pairing | 35 min | 15 min | 50 min |
| 4 — Grid Reference Split | 40 min | 15 min | 55 min |
| 5 — Tare Weight Picks | 40 min | 15 min | 55 min |
| 6 — Test Tray Fill | 40 min | 15 min | 55 min |

About five hours. Problems 5 and 6 are the two that pay off most: 5 because two
rules that look alike are two different bugs, and 6 because it is the clearest
demonstration in the whole course of what pruning at the right moment is worth.
