# Week 10 — Homework

Six problems, all original, all with a runnable worked answer beside this page.
Allow about five and a half hours. Do each with the lectures closed; open the
worked answer only after your own version runs, or after fifteen minutes stuck on
one step.

The six cover the week's whole range: union-find as a grouping tool and as a
diagnosis, a spanning tree, a search where the cost is a maximum rather than a
sum, all-pairs distances, and a search where the cost multiplies.

| # | Problem | Sub-shape | Est. time |
|---|---------|-----------|----------:|
| 1 | [The Claim Slip Merge](#problem-1--the-claim-slip-merge) | Union-find over a shared attribute | 50 min |
| 2 | [The Kerb Step Route](#problem-2--the-kerb-step-route) | Minimising the worst step, not the total | 60 min |
| 3 | [The Mast Trench Network](#problem-3--the-mast-trench-network) | Minimum spanning tree with a non-obvious cost | 55 min |
| 4 | [The Radiator Loop Check](#problem-4--the-radiator-loop-check) | Union-find as a diagnosis, naming both faults | 50 min |
| 5 | [The Market Stall Reach](#problem-5--the-market-stall-reach) | All pairs at once, rather than one search per start | 50 min |
| 6 | [The Relay Reliability](#problem-6--the-relay-reliability) | The same search where cost multiplies and bigger is better | 55 min |

Every worked answer runs on its own with no arguments and no packages, and ends
by printing `All checks passed.` Run one like this:

```bash
python problem-01-claim-slip-merge-solution.py
```

---

## Problem 1 — The Claim Slip Merge

**The brief.** A station lost-property office writes a claim slip every time
somebody rings about a missing bag. Each slip has a name and one or more phone
numbers. The same person rings back from a different phone, and now there are two
slips.

Two slips belong to the same person when they **share at least one phone number**,
and that spreads: slip A shares a number with slip B, slip B shares a different
number with slip C, so all three are one person.

**Constraints.** **The name is not the key.** Two different people can share a
name, and the shipped data has exactly that case in it. Merging on the name is
the wrong answer that passes a careless test.

**Answer.** Union-find over the **phone numbers**, not the slips. Keep a map from
each number to the first slip that mentioned it; for every later slip, union it
with that slip. Numbers do the joining because the numbers are what is shared.

Then group the slips by root and read the name off any member of the group — they
all agree, because they are one person by construction.

**Signatures.** `Slips` with the union-find, `merged_claims(slips)`,
`phone_owner(records, phone)`.

**Watch for.** Grouping by name — the shipped data punishes it. Building the
union over slips directly without the number-to-slip map, which misses the
transitive case. A number nobody claimed returns `None`, not an empty string.

**Worked answer.** [`problem-01-claim-slip-merge-solution.py`](./problem-01-claim-slip-merge-solution.py)

---

## Problem 2 — The Kerb Step Route

**The brief.** A market square is paved in blocks, each surveyed to a height in
millimetres. A wheelchair crosses from the north-west corner to the south-east
corner, one block at a time, north, south, east or west. Stepping between two
blocks means climbing the difference in their heights.

**Nobody cares about the total climb.** What matters is the **single worst step**
on the route, because that is the one that stops the chair. Make it as small as
possible.

**Constraints.** The cost of a route is a **maximum**, not a sum. That one change
breaks every instinct built up on shortest-path problems, and it is the whole
reason this problem is here.

**Answer.** Two answers, and the write-up should name both.

The first is a **search where the accumulated cost is a maximum**: the frontier is
ordered by the worst step so far, and extending a route costs
`max(worst_so_far, this_step)` rather than `worst_so_far + this_step`. Everything
else about the search is unchanged, which is the point worth making.

The second is a **decision procedure plus a search over the answer**: ask "is
there a route where no step exceeds `limit`?" — which is a plain reachability
question — and binary-search `limit`. `route_within` is that decision procedure,
and having it in the file lets you check the first answer against the second.

On the shipped square the answer is **6**: no route at limit 5, a route at limit 6.

**Signatures.** `gentlest_route(square)`, `route_within(square, limit)`.

**Watch for.** Summing the steps, which answers a different and easier question.
Comparing heights rather than the difference between them. A one-block square is
zero, not an error.

**Worked answer.** [`problem-02-kerb-step-route-solution.py`](./problem-02-kerb-step-route-solution.py)

---

## Problem 3 — The Mast Trench Network

**The brief.** Six weather masts stand on a moor. Every mast has to end up wired
to every other, directly or through its neighbours. A trenching machine digs
between two masts, and the price is set by the machine's boom: **it swings once,
so a trench costs whichever is larger — the east-west gap or the north-south
gap.** Not the two added together, and not the straight-line distance.

**Constraints.** Every pair could be trenched, so the surveyor is choosing five
trenches from fifteen candidates. The cost function is the trap: it is a maximum
of two differences, and every wrong answer here comes from using the sum instead.

**Answer.** Build all fifteen candidate trenches with the boom cost, sort them
cheapest first, and accept a trench only when its two masts are **not already
joined** — union-find answering that question in near-constant time. Stop after
five, which for six masts is one fewer than the mast count.

Total on this moor: **13 metres across five trenches**, and the longest single
trench — the one that sizes the boom you have to hire — is Beacon Ridge to Ewe
Crag at 4 metres.

The data includes one pair, Alder Hill to Drum Rig, where the boom cost is 6 and
the sum of the two gaps is 11. That row is in the output on purpose: it is the
evidence that the cost rule matters.

**Signatures.** `boom_cost(first, second)`, `cheapest_network(masts)`,
`longest_trench(chosen)`.

**Watch for.** Adding the two gaps. Accepting a trench between masts already
joined, which builds a ring and costs money for nothing. Forgetting that the
answer is `n - 1` trenches, not `n`.

**Worked answer.** [`problem-03-mast-trench-network-solution.py`](./problem-03-mast-trench-network-solution.py)

---

## Problem 4 — The Radiator Loop Check

**The brief.** A plumber surveys the heating in an old building. Radiators are
numbered from zero and each pipe run joins two of them. Good pipework is a tree:
every radiator fed, and no ring letting water go round without ever reaching the
far end.

**Two faults are possible and they are independent**, so a plain true-or-false
answer loses information. Name both:

```text
"tree"            every radiator fed, no ring
"loop"            there is a ring, but everything is still fed
"split"           no ring, but some radiators are unreachable
"loop and split"  both
```

**Constraints.** Reporting one bit where there are two facts is the wrong answer
the problem is built to reject. A survey can be a ring *and* have an orphaned
wing, and the plumber needs to know which of the two they are dealing with — the
fixes are different.

**Answer.** Union-find, one pass over the runs. A run whose two radiators are
**already joined** closes a ring — that run is a loop-closer. After the pass,
count the distinct roots: more than one means the system is split.

Both facts come out of the same walk, which is why they cost nothing extra to
report separately.

`loop_closing_runs` returns the runs you could cut — the ones that closed a ring —
which is the actionable half of the answer.

**Signatures.** `Pipework` with the union-find,
`survey_pipework(radiator_count, runs)`,
`loop_closing_runs(radiator_count, runs)`.

**Watch for.** Returning a boolean. Counting roots before the pass rather than
after. A building with zero pipe runs and one radiator is a tree; with zero runs
and three radiators it is split.

**Worked answer.** [`problem-04-radiator-loop-check-solution.py`](./problem-04-radiator-loop-check-solution.py)

---

## Problem 5 — The Market Stall Reach

**The brief.** A covered market has numbered stalls joined by aisles. Pushing a
loaded barrow along an aisle takes a known number of seconds, and an aisle is
walkable both ways at the same cost.

The market wants the **quietest pitch**: the stall from which the fewest other
stalls are within a barrow-push budget.

**Constraints.** The question is about **every pair** of stalls, not about one
starting point. That is what decides the algorithm, and saying so is the
recognition step.

**Answer.** All-pairs distances in one go: start from the direct aisle times, then
for every possible intermediate stall, check whether going via it is quicker than
what you have. Three nested loops, and the intermediate stall must be the
**outermost** of the three — that ordering is the whole correctness argument and
it is the thing to get right before writing anything else.

Then count, per stall, how many others are within the budget, and take the
smallest count.

With a budget of 10 seconds the quietest pitch is **stall 6, reaching one other
stall**.

Running one search per stall gives the same answer. On a market this size it
costs about the same; the write-up should say at what size that stops being true
and why.

**Signatures.** `push_times(stall_count, aisles)`,
`neighbours_within(times, stall, budget)`,
`quietest(stall_count, aisles, budget)`.

**Watch for.** Putting the intermediate stall in an inner loop — the answer is
then wrong in a way that looks plausible on small inputs. Counting the stall
itself among its neighbours. Unreachable pairs must stay at infinity rather than
becoming a large number that later arithmetic treats as real.

**Worked answer.** [`problem-05-market-stall-reach-solution.py`](./problem-05-market-stall-reach-solution.py)

---

## Problem 6 — The Relay Reliability

**The brief.** A harbour passes messages between boats by short-range radio. Each
hop works some fraction of the time — a hop of 0.9 gets through nine times in ten.
A relay through several boats works only if **every** hop works, so the chance of
the whole relay is the hops **multiplied**, never added.

Find the most reliable relay from one boat to another.

**Constraints.** Multiplying makes a route worse the longer it gets, and the job
is to make the number **as large as possible** rather than as small as possible.
Both of those invert the usual search, and inverting exactly one of them is the
most common wrong answer.

**Answer.** The same search shape as a shortest path, with two changes and no
others: combine costs by multiplying instead of adding, and take the **best**
frontier entry as the largest rather than the smallest. Reliabilities are between
0 and 1, so multiplying can only shrink a route — which is what makes the greedy
argument hold, exactly as non-negative edge weights do in the additive case.

That sentence is what the write-up is really for. It is also why the same trick
does not survive a hop with reliability above 1, and saying so shows you
understand the argument rather than the recipe.

From Anvil: Cutter at 0.9 in one hop, Dredger at 0.4 in two, Ebb at 0.36 in
three, and Fluke unreachable.

**Signatures.** `build_radio(hops)`, `best_relay(hops, start, end)`,
`relay_rows(hops, boats, start)`.

**Watch for.** Adding the reliabilities, which can exceed 1 and means nothing.
Taking the smallest frontier entry, which finds the *worst* relay confidently.
Starting the source at 0 rather than 1 — the multiplicative identity is 1, and
starting at 0 makes every relay impossible. An unreachable boat returns `None`.

**Worked answer.** [`problem-06-relay-reliability-solution.py`](./problem-06-relay-reliability-solution.py)

---

## Rubric (5 axes, 4 points each)

| Axis | What "great" looks like |
|------|--------------------------|
| Frame the problem | The memo names the structure and — for problems 2 and 6 — exactly which part of the usual search changed and which part did not. |
| Reason about options | Four to six bullets before any code, with the alternative named and costed. |
| Assemble the solution | Idiomatic Python; union-find with both path compression and union by size, and a sentence on why each is there; type hints throughout. |
| Measure it | A trace on at least two inputs, one of them degenerate or unreachable. |
| Evaluate the cost | Time, space, best/average/worst, the trade-off and the improvement — in the problem's own numbers. |

Twenty points per problem, 120 for the set. Score yourself honestly; the number
is only useful if it is true.

---

## How to submit

Commit your write-ups under `frame-writeups/c2-week-10/homework/`, one file per
problem:

```
frame-writeups/c2-week-10/homework/
├── problem-1-claim-slip-merge.md
├── problem-2-kerb-step-route.md
├── problem-3-mast-trench-network.md
├── problem-4-radiator-loop-check.md
├── problem-5-market-stall-reach.md
└── problem-6-relay-reliability.md
```

Each file is 100–200 lines: the five FRAME sections plus a five-line memo at the
top. The code is part of the Assemble section, not a separate file.

When the set is done, push and move on to the
[mini-project](../mini-project/README.md).

---

## Time budget

| Problem | Solve | Write-up | Total |
|---------|------:|---------:|------:|
| 1 — Claim Slip Merge | 35 min | 15 min | 50 min |
| 2 — Kerb Step Route | 45 min | 15 min | 60 min |
| 3 — Mast Trench Network | 40 min | 15 min | 55 min |
| 4 — Radiator Loop Check | 35 min | 15 min | 50 min |
| 5 — Market Stall Reach | 35 min | 15 min | 50 min |
| 6 — Relay Reliability | 40 min | 15 min | 55 min |

About five and a half hours. Problems 2 and 6 are the two that pay off most in a
real round, because both are the same search with one thing changed — and being
able to say which thing is the difference between knowing an algorithm and
knowing what it is made of.
