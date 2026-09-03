# Week 9 — Homework

Six problems, all original, all with a runnable worked answer beside this page.
Allow about five hours. Do each with the lectures closed; open the worked answer
only after your own version runs, or after fifteen minutes stuck on one step.

The six cover every shape the week teaches: a wildcard walk, a chain of prefixes,
the border table, a tree built backwards, a tree that queries itself, and a walk
carrying a budget.

| # | Problem | Sub-shape | Est. time |
|---|---------|-----------|----------:|
| 1 | [The Smudged Stencil](#problem-1--the-smudged-stencil) | Prefix tree with a single-character wildcard | 45 min |
| 2 | [The Growable Dock Sign](#problem-2--the-growable-dock-sign) | Every prefix must itself be a word | 40 min |
| 3 | [The Splice Point](#problem-3--the-splice-point) | The border table, and a scan that never backs up | 55 min |
| 4 | [The Radio Tail Watch](#problem-4--the-radio-tail-watch) | A tree built backwards, walked from the newest letter | 50 min |
| 5 | [The Double-Stamped Label](#problem-5--the-double-stamped-label) | A tree queried against its own contents | 55 min |
| 6 | [The One-Key Typo Desk](#problem-6--the-one-key-typo-desk) | A walk carrying a budget of one mismatch | 50 min |

Every worked answer runs on its own with no arguments and no packages, and ends
by printing `All checks passed.` Run one like this:

```bash
python problem-01-smudged-stencil-solution.py
```

---

## Problem 1 — The Smudged Stencil

**The brief.** Depot crates carry a stencilled code. Rain smudges letters, and
the clerk types a question mark where a letter is unreadable. **One question mark
stands for exactly one letter** — never for none, and never for two. Given the
register of real codes and a smudged pattern, list every code the pattern could
be, A to Z.

**The data.** Eight stencils: `CRATE GRATE GRAPE CRANE PLATE SLATE SLATS PLAN`.

**Constraints.** The wildcard is exactly one letter, so a four-character pattern
can only match a four-character code. `??` matches nothing here, because no code
is two letters long — and that is a real answer, not an empty one.

**Answer.** Build a prefix tree over the codes, then walk it one character at a
time. On a letter, descend that one branch. On a `?`, **descend every branch**.
At the end of the pattern, collect the codes at nodes marked as ends.

The reason the tree beats scanning the register is what happens on `?????`: a
scan tries every code against every position, while the tree's five-wildcard walk
visits each node once and stops dead on any branch that runs out of depth. Sorted
output falls out of walking the branches in order rather than needing a sort.

On this data `?????` gives **seven** codes — every five-letter stencil — and
`PL??` gives one, `PLAN`.

**Signatures.** `build_stencil_tree(codes)`, `matches(root, pattern)`.

**Watch for.** Letting `?` match zero characters or two — the length has to be
exact. Returning codes from nodes that are merely *on the way* rather than marked
as ends: `PL??` must not return `PLATE`. And a pattern longer than every code
returns an empty list, not an error.

**Worked answer.** [`problem-01-smudged-stencil-solution.py`](./problem-01-smudged-stencil-solution.py)

---

## Problem 2 — The Growable Dock Sign

**The brief.** A dock sign is built by sliding letter tiles on, one at a time,
left to right. **Every stage has to be a code the harbour already recognises** —
you cannot show a half-finished word to the public. Find the longest sign that
can be built this way, and report the whole build, stage by stage.

**The data.** Fourteen codes, including the chains `B BE BER BERT BERTH`,
`D DO DOC DOCK DOCKS`, and `Q QU QUAY`, plus the orphan `TIDE`.

**Constraints.** `DOCKS` is five letters and so is `BERTH`, so the tie has to
resolve by a stated rule. `TIDE` is longer than `QUAY` and buildable at no stage
past its first letter — length alone is not the answer.

**Answer.** Build the prefix tree, then walk **only through nodes marked as
ends**. The moment a node on the path is not itself a code, that branch is dead —
there is no point looking further down it, because every deeper sign would have
to pass through the stage you just rejected.

That early stop is the whole idea. Checking each code's prefixes separately does
the same work repeatedly; the tree does the chain once and shares it between
every code that starts the same way.

Longest here is **BERTH**, in five stages.

**Signatures.** `build_register_tree(codes)`, `longest_build(root)`.

**Watch for.** Walking past a non-end node "just in case" — that is the pruning,
and without it the answer is `TIDE`. Ties between two equally long chains need a
rule, and the file states one rather than trusting dictionary order. An empty
register gives an empty build.

**Worked answer.** [`problem-02-growable-dock-sign-solution.py`](./problem-02-growable-dock-sign-solution.py)

---

## Problem 3 — The Splice Point

**The brief.** A cable spool is labelled with the colour bands printed along it,
one letter per band. A splice code is a short band sequence the workshop wants to
find. Report **every** position where the code appears — **including positions
that overlap an earlier hit**, because a splice can share bands with its
neighbour.

**The data.** Label `RGRGRGBRGRGRGR`, code `RGRGR`. Plus a 4000-band label built
from a repeating pattern, to make the cost visible.

**Constraints.** Overlaps count. On `BBBB` looking for `BB` the answer is
`[0, 1, 2]`, not `[0, 2]`, and getting that right is what stops you advancing by
the code's whole length after a hit.

**Answer.** The **border table**: for each position in the code, the length of
the longest proper prefix that is also a suffix ending there. On a mismatch it
says how far back to slide the code without moving the position in the label at
all — so the label is read once, forwards, and never backed up.

The nested-loop version re-reads bands it has already seen. On a label built from
a repeating pattern that is nearly all of them, which is exactly the case here
and exactly why the long label is in the data.

On the shipped label the hits are `[0, 7, 9]` — 7 and 9 overlap.

**Signatures.** `border_table(code)`, `splice_points(label, code)`.

**Watch for.** Advancing by the code length after a hit, which drops every
overlap. Building the table with `>=` where `>` belongs, which makes a border
claim a prefix is its own proper prefix. An empty code, or a code longer than the
label, returns an empty list.

**Worked answer.** [`problem-03-splice-point-solution.py`](./problem-03-splice-point-solution.py)

---

## Problem 4 — The Radio Tail Watch

**The brief.** A harbour radio desk receives letters one at a time, forever.
Certain words are **call words** the duty officer must be told about, and a call
word counts **only when it lands at the very end** of what has arrived so far.

**The data.** Call words `PAN PANPAN MAY MAYDAY`; the stream `QPANPANZMAYDAY`.

**Constraints.** The stream never ends, so nothing may be re-scanned from the
start. `PANPAN` contains `PAN`, so one letter can complete two different call
words at different times — and the answer at each letter is which call word ended
*there*.

**Answer.** Build the tree out of the call words **spelled backwards**. Then a
walk from the newest letter backwards through the stream is an ordinary walk down
a prefix tree, and it stops as soon as no branch matches.

That inversion is the whole trick and it is worth a paragraph in the write-up:
the interesting end of a stream is the newest letter, and a prefix tree only walks
forwards, so you reverse the words rather than the stream.

**Signatures.** `TailWatch` with the letter-at-a-time interface.

**Watch for.** Storing the whole stream and re-searching it — correct, and
unbounded in memory on a stream that does not end. Reporting a call word that
ends anywhere but at the newest letter. And the walk must stop at the deepest
matching branch rather than walking the whole history back.

**Worked answer.** [`problem-04-radio-tail-watch-solution.py`](./problem-04-radio-tail-watch-solution.py)

---

## Problem 5 — The Double-Stamped Label

**The brief.** A boatyard stamps part labels from a set of metal dies, one die per
registered code. Some labels were stamped with two or more dies in a row, so the
label reads as one code but is really several registered codes joined end to end.
Find every registered code that is **exactly two or more other registered codes**
laid end to end, longest first.

**The data.** Eleven die codes including `FIN`, `BOARD`, `FINBOARD`, `KEEL`,
`SON`, `KEELSON`, `BOARDKEELSON`, `MAST`, `MASTFIN`, `FINBOARDMAST`, `RUDDER`.

**Constraints.** "Two or more" is the rule, so a code is not double-stamped by
being itself. `FINBOARDMAST` is three dies, which is why the rule is not "exactly
two". And `BOARDKEELSON` is made from `BOARD` plus `KEELSON`, which is itself
made from two dies — the decomposition does not have to be into single dies only.

**Answer.** Build the tree over all the codes, then for each code walk it against
**the tree it is a member of**, splitting wherever a registered code ends and
recursing on the remainder. Count the pieces; two or more means double-stamped.

The subtlety is that a code must not match itself as its own only piece, which is
what the "two or more" count is really enforcing.

Five codes qualify here, longest first: `BOARDKEELSON`, `FINBOARDMAST`,
`FINBOARD`, `KEELSON`, `MASTFIN`.

**Signatures.** `build_die_tree(codes)`, `is_double_stamped(root, code)`,
`double_stamped(codes)`.

**Watch for.** Counting a code as made of one piece — itself. Missing the
three-piece cases by only ever trying one split. Re-walking the same suffix
repeatedly on a large register, which is where memoising the suffix pays.

**Worked answer.** [`problem-05-double-stamped-label-solution.py`](./problem-05-double-stamped-label-solution.py)

---

## Problem 6 — The One-Key Typo Desk

**The brief.** The yard office types four-letter locker codes all day, and the
commonest mistake is hitting one neighbouring key. The desk answers one question:
which real codes are **exactly one letter** away from what was typed?

Exactly one. A code that matches perfectly is not an answer, because nothing was
mistyped. A code two letters away is not an answer either.

**The data.** Lockers `HOLD HOLE HULL BOLT BOLD BOAT OARS`; typed strings
including `HOLD`, `BOLD`, `BOAT`, `HULL`, and the wrong-length `HOL` and `HOLDS`.

**Constraints.** Only substitutions count — no insertions, no deletions — so a
code of a different length is never an answer. `HOL` and `HOLDS` both return
nothing, and that is the constraint doing its job rather than a gap in the data.

**Answer.** Walk the tree carrying a **budget of one swap**. While the budget is
unspent the walk may branch into every letter other than the typed one, spending
the budget as it does. Once it is spent the walk must follow the typed letters
exactly. At the end, accept only nodes that are marked as ends **and** whose
budget was actually spent.

That last clause is the one people miss: a walk that never spends the budget has
found the typed code itself, which is not a typo.

`HOLD` gives `BOLD` and `HOLE`; `BOAT` gives only `BOLT`; `HULL` gives nothing.

**Signatures.** `build_locker_tree(codes)`, `one_key_away(root, typed)`.

**Watch for.** Returning the exact match — the budget must be spent. Allowing the
budget to go negative, which quietly turns this into two-letter matching. Walking
a branch after the budget is spent and the letters diverge.

**Worked answer.** [`problem-06-one-key-typo-desk-solution.py`](./problem-06-one-key-typo-desk-solution.py)

---

## Rubric (5 axes, 4 points each)

| Axis | What "great" looks like |
|------|--------------------------|
| Frame the problem | The memo names the structure — prefix tree, border table, reversed tree, budgeted walk — and what a node means in this problem. |
| Reason about options | Four to six bullets before any code, with the scan-everything alternative named and costed rather than dismissed. |
| Assemble the solution | Idiomatic Python; one clear representation for a node; type hints on every function. |
| Measure it | A trace on at least two inputs, one of them a degenerate case. |
| Evaluate the cost | Time, space, best/average/worst, the trade-off, and the improvement — in terms of the register's own size, not abstract n. |

Twenty points per problem, 120 for the set. Score yourself honestly; the number
is only useful if it is true.

---

## How to submit

Commit your write-ups under `frame-writeups/c2-week-09/homework/`, one file per
problem:

```
frame-writeups/c2-week-09/homework/
├── problem-1-smudged-stencil.md
├── problem-2-growable-dock-sign.md
├── problem-3-splice-point.md
├── problem-4-radio-tail-watch.md
├── problem-5-double-stamped-label.md
└── problem-6-one-key-typo-desk.md
```

Each file is 100–200 lines: the five FRAME sections plus a five-line memo at the
top. The code is part of the Assemble section, not a separate file.

When the set is done, push and move on to the
[mini-project](../mini-project/README.md).

---

## Time budget

| Problem | Solve | Write-up | Total |
|---------|------:|---------:|------:|
| 1 — Smudged Stencil | 35 min | 10 min | 45 min |
| 2 — Growable Dock Sign | 30 min | 10 min | 40 min |
| 3 — Splice Point | 40 min | 15 min | 55 min |
| 4 — Radio Tail Watch | 35 min | 15 min | 50 min |
| 5 — Double-Stamped Label | 40 min | 15 min | 55 min |
| 6 — One-Key Typo Desk | 35 min | 15 min | 50 min |

About five hours, and Mock #2 grades the recognition step rather than the code.
