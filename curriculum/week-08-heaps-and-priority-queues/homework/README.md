# Week 8 — Homework

Six problems, all original, all with a runnable worked answer beside this page.
Allow about five hours. Do each problem with the lectures closed; open the
worked answer only after your own version runs, or after fifteen minutes stuck
on one step.

The six cover every heap sub-shape the week teaches, so that by Sunday the
recognition step is reflexive: a bounded shortlist, a repeated-merge cost, a
k-way merge over sorted sources, a spacing scheduler, a two-heap unlock loop,
and a two-heap running statistic.

| # | Problem | Sub-shape | Est. time |
|---|---------|-----------|----------:|
| 1 | [The Dawn Chorus Shortlist](#problem-1--the-dawn-chorus-shortlist) | Bounded top-k with a two-direction tiebreak | 35 min |
| 2 | [The Splice Drum Tape](#problem-2--the-splice-drum-tape) | Repeated merge of the two smallest | 30 min |
| 3 | [The Germination Grid Rank](#problem-3--the-germination-grid-rank) | k-way merge, stopping at rank k | 50 min |
| 4 | [The Night Rota](#problem-4--the-night-rota) | Max-heap scheduler with a held-back slot | 50 min |
| 5 | [The Grant Round](#problem-5--the-grant-round) | Two heaps: locked by cost, unlocked by payout | 60 min |
| 6 | [The Oven Probe Midline](#problem-6--the-oven-probe-midline) | Two heaps: the running middle | 45 min |

Every worked answer runs on its own with no arguments and no packages, and ends
by printing `All checks passed.` Run one like this:

```bash
python problem-01-dawn-chorus-shortlist-solution.py
```

---

## Problem 1 — The Dawn Chorus Shortlist

**The brief.** A recorder logs one line per bird detection through a spring
morning — 33 detections across eight species. The survey wants the **five
most-heard species**, most first, and **alphabetical** between species heard the
same number of times.

**The data.**

```text
wren 9 · robin 8 · blackcap 5 · song thrush 4 · chiffchaff 3
dunnock 2 · goldcrest 1 · nuthatch 1
```

**Constraints.** The two halves of the sort rule pull in **opposite
directions**: count downwards, name upwards. A string cannot be negated, so the
usual "negate the key" trick only half works — and noticing that before you write
it is the point of the problem.

**Answer.** `heapq.nsmallest(size, counts.items(), key=lambda kv: (-kv[1], kv[0]))`.
The key sorts by negated count, so higher counts come first among the "smallest"
keys, and then by name ascending — which is exactly the rule. `nsmallest` holds
`size` entries rather than sorting all eight species, and the negation lives only
in the key, never in the data.

**Signatures.** `shortlist(detections, size)`, `heard_once(detections)`,
`share_of_dawn(detections, species)`.

**Watch for.** Sorting twice to get the two directions — it works, and it says you
did not see the single-key answer. A species never heard has a share of `0.0`,
not an error. `size = 0` returns an empty list; a size above the species count
returns all eight.

**Worked answer.** [`problem-01-dawn-chorus-shortlist-solution.py`](./problem-01-dawn-chorus-shortlist-solution.py)

---

## Problem 2 — The Splice Drum Tape

**The brief.** A cable crew joins several drums of fibre into one continuous run.
Each join costs tape equal to the **combined length of the two pieces being
joined**, so the *order* of the joins changes the bill. Report the cheapest total
and the cost of each join along the way.

**The data.** Drums of 12, 9, 30, 21, 5 and 16 metres.

**Constraints.** Every join reduces the count by one, so there are always exactly
`n - 1` joins whatever order you pick. The order is the only lever.

**Answer.** Always join the **two shortest pieces** available. Heapify the drums,
then repeatedly pop two, push their sum, and record that sum as the join's cost.
Why it is optimal is the sentence the write-up needs: a piece's length is paid for
once per join it takes part in, so the pieces that go through the most joins
should be the shortest ones — and joining the two shortest first is what pushes
the long pieces to the end.

Total on this data: **226 m**, against **378 m** for the worst order. The
difference is 152 m of tape on six drums.

**Signatures.** `splice_costs(drums)`, `worst_order_cost(drums)`,
`run_length(drums)`.

**Watch for.** One drum needs no joins and costs nothing — not an error, and not
the drum's own length. No drums at all costs nothing too. `run_length` is just
the sum, and it is there to check the joins conserved the fibre.

**Worked answer.** [`problem-02-splice-drum-tape-solution.py`](./problem-02-splice-drum-tape-solution.py)

---

## Problem 3 — The Germination Grid Rank

**The brief.** A seed lab runs four trays of four slots. Every tray's counts rise
**left to right**, and every slot's counts rise **tray to tray**. The lab wants
the **k-th lowest count** in the whole grid and the slot it came from.

**The data.**

```text
tray 1    2   6  11  17
tray 2    5   6  14  21
tray 3    9  13  15  26
tray 4   12  19  23  30
```

**Constraints.** Two slots can tie — there are two 6s here — so the answer is a
count *and* a position, and the tie has to resolve to one of them by a stated
rule rather than by luck.

**Answer.** Each tray is an already-sorted source, so this is a k-way merge that
**stops after k pops**. Seed a heap with the first count of each tray, then pop k
times, pushing the next count from whichever tray the pop came from. Sorting all
sixteen is correct and costs `O(n log n)`; the merge costs `O(k log t)` for t
trays and never looks at the counts past rank k. On a four-by-four grid that
saves nothing; on a thousand trays it is the whole answer.

Rank 7 on this grid is **12, in tray 4 slot 1**.

**Signatures.** `nth_lowest(grid, rank)`, `merged_counts(grid)`,
`slot_of_rank(grid, rank)`.

**Watch for.** A rank outside `1..16` raises `ValueError` rather than returning
something. Ragged trays — rows of different lengths — must not crash the merge.
The row-and-column ordering is *not* a full sort of the grid: tray 2's first
count (5) is lower than tray 1's second (6), which is exactly why a row-by-row
scan gets the wrong answer.

**Worked answer.** [`problem-03-germination-grid-rank-solution.py`](./problem-03-germination-grid-rank-solution.py)

---

## Problem 4 — The Night Rota

**The brief.** A night shelter needs one volunteer per night. Each volunteer has
agreed to a number of nights, and the house rule is that **nobody works two
nights in a row**. Build a rota that uses everybody's agreed nights, or say
plainly that no rota exists.

**The data.** Ama 4 nights, Beto 3, Cass 2, Dev 1 — ten nights to fill.

**Constraints.** "No rota exists" is a real answer and has to be returned as
`None`, not raised and not fudged. One person on five of six nights cannot be
spaced out, and the function must say so.

**Answer.** Greedy on a max-heap: **whoever has the most nights left works
tonight**, plus one held-back slot for last night's volunteer so they cannot be
picked again immediately. After picking, decrement, then return *last night's*
volunteer to the heap — the hold-back is one night deep, which is exactly the
rule.

The greedy is right because the volunteer with the most nights left is the one
most likely to be stranded at the end; every night given to somebody else is a
night they cannot use.

Rota on this data: `Ama Beto Ama Beto Ama Cass Ama Beto Cass Dev`.

**Signatures.** `build_rota(nights_agreed)`, `rota_is_legal(rota)`,
`nights_worked(rota)`.

**Watch for.** Returning `None` after building a partial rota rather than
detecting the impossibility. `rota_is_legal` must be written independently of
`build_rota` — a verifier that shares the builder's assumptions verifies nothing.
A single night, a zero pledge, and nobody at all are all valid inputs.

**Worked answer.** [`problem-04-night-rota-spacing-solution.py`](./problem-04-night-rota-spacing-solution.py)

---

## Problem 5 — The Grant Round

**The brief.** A community fund holds a reserve. Every project has an **unlock** —
the reserve the fund must already hold before the trustees will sign it off — and
a **payout** that goes back into the reserve when the project finishes. The fund
may back only a few projects in a round, and each one it backs may unlock the
next. Which ones, and what does the reserve close at?

**The data.**

```text
project        unlock   payout
Roof repair         0       30
Kiln rebuild       40       90
Tool shed          25       20
Van service        10       45
Server rack       120      200

opening reserve 15 · three picks allowed
```

**Constraints.** Greedy on payout alone is wrong — the biggest payout may be
locked. Greedy on unlock alone is wrong too — the cheapest unlock may pay almost
nothing. The answer needs both, which is why it is two heaps.

**Answer.** A **min-heap of projects by unlock**, so the cheapest still-locked
project is always next in line, and a **max-heap of the projects already
unlocked**, so the biggest payout is always on top. Each round: move everything
the current reserve now unlocks from the first heap into the second, then take
the biggest payout available. If nothing is unlocked, stop — no further reserve is
coming.

On this data the fund backs **Van service, Kiln rebuild, Server rack** and closes
at **350** from an opening 15. Roof repair pays 30 and is never taken, because
three picks is three picks and the fund can afford to be choosy.

**Signatures.** `grant_round(projects, reserve, picks)`,
`locked_out(projects, reserve, picks)`, `best_single(projects, reserve)`.

**Watch for.** Looping on when the unlocked heap is empty — that is the stopping
condition, and it is not the same as running out of picks. Zero picks returns the
opening reserve untouched. More picks than projects backs all of them and stops.

**Worked answer.** [`problem-05-grant-round-picks-solution.py`](./problem-05-grant-round-picks-solution.py)

---

## Problem 6 — The Oven Probe Midline

**The brief.** A bakery's deck oven reports its crown temperature every few
minutes. The baker wants the **midline after every reading** — the middle value of
everything seen so far. With an even number of readings there are two middle
values; this bakery wants the **lower** of the two, plus **how far apart they
are**, because a wide gap means the oven is swinging.

**The data.** 214, 231, 205, 240, 226, 219, 236, 208 degrees.

**Constraints.** The midline is wanted after *every* reading, so re-sorting the
history each time costs `O(n² log n)` over the run — that is the alternative to
name and reject.

**Answer.** Two heaps holding the two halves. The **lower half in a max-heap**, so
its biggest value is on top; the **upper half in a min-heap**, so its smallest is
on top. The two tops are the two middle readings — the midline is the lower one,
the spread is their difference. After every push, rebalance so the halves differ
in size by at most one; that invariant is what the whole structure rests on.

Insert and rebalance are `O(log n)`; reading the midline is `O(1)`.

**Signatures.** `Midline` with `add`, `midline`, `spread`;
`midline_trace(readings)`, `widest_swing(readings)`.

**Watch for.** Pushing straight onto the half you think it belongs in without
comparing against the tops — the halves stop being halves and the answer drifts
without ever crashing. Rebalancing by size alone, ignoring the values, has the
same symptom. Before any reading the midline is `None` and the spread is `0`; four
identical readings have a spread of `0`, which is a real answer and not a
degenerate one.

**Worked answer.** [`problem-06-oven-probe-midline-solution.py`](./problem-06-oven-probe-midline-solution.py)

---

## Rubric (5 axes, 4 points each)

| Axis | What "great" looks like |
|------|--------------------------|
| Frame the problem | The 30-second memo names the sub-shape — bounded top-k, repeated merge, k-way merge, spacing scheduler, two-heap unlock, two-heap statistic — and the invariant that goes with it. |
| Reason about options | Four to six bullets of algorithm before any code is written, including the alternative you rejected. |
| Assemble the solution | Idiomatic Python; `heapq` operations only, no hand-written sift code; type hints on every function. |
| Measure it | A trace on at least one example, and one common bug named and avoided. |
| Evaluate the cost | Time, space, best/average/worst, the trade-off, and the improvement — with the sentence that defends the heap against sorting. |

Twenty points per problem, 120 for the set. Score yourself honestly; the number
is only useful if it is true.

---

## How to submit

Commit your write-ups under `frame-writeups/c2-week-08/homework/`, one file per
problem:

```
frame-writeups/c2-week-08/homework/
├── problem-1-dawn-chorus-shortlist.md
├── problem-2-splice-drum-tape.md
├── problem-3-germination-grid-rank.md
├── problem-4-night-rota-spacing.md
├── problem-5-grant-round-picks.md
└── problem-6-oven-probe-midline.md
```

Each file is 100–200 lines: the five FRAME sections plus a five-line memo at the
top. The code is part of the Assemble section, not a separate file.

When the set is done, push and move on to the
[mini-project](../mini-project/README.md).

---

## Time budget

| Problem | Solve | Write-up | Total |
|---------|------:|---------:|------:|
| 1 — Dawn Chorus Shortlist | 25 min | 10 min | 35 min |
| 2 — Splice Drum Tape | 20 min | 10 min | 30 min |
| 3 — Germination Grid Rank | 40 min | 10 min | 50 min |
| 4 — Night Rota | 35 min | 15 min | 50 min |
| 5 — Grant Round | 45 min | 15 min | 60 min |
| 6 — Oven Probe Midline | 30 min | 15 min | 45 min |

About four and a half hours of work, and the write-ups are the half that Mock #2
actually grades.
