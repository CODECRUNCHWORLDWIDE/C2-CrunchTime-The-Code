# Week 10 — Exercises

Five exercises, in order. Each has a page with the brief, the constraints, the
worked solution and the acceptance checklist, and a runnable file beside it that
ends by printing `All checks passed.`

| # | Exercise | Sub-shape | Difficulty | Target time |
|---|----------|-----------|------------|------------:|
| 1 | [The Hut Relay Timing](./exercise-01-hut-relay-timing.md) | The shortest-path picker at its plainest, on one-way links | Easy | 35 min |
| 2 | [The Sluice Gate Settling](./exercise-02-sluice-gate-settling.md) | What the settled set is for, shown by removing it | Easy-Medium | 40 min |
| 3 | [The Mooring Chain Groups](./exercise-03-mooring-chain-groups.md) | Union-find, with path compression printed before and after | Easy-Medium | 35 min |
| 4 | [The Greenhouse Pipe Run](./exercise-04-greenhouse-pipe-run.md) | The minimum spanning tree, with union-find deciding what to accept | Medium | 40 min |
| 5 | [The Shunting Rebate Legs](./exercise-05-shunting-rebate-legs.md) | Why the settled set stops being safe once a cost can be negative | Medium | 45 min |

Do them in order — this week's five build in pairs and the order carries an
argument.

Exercise 1 is the search with nothing on top, and it settles the one-way-link
mistake early. Exercise 2 then runs the *same* algorithm with the settled set
deleted, on data where exactly one gate comes out wrong, and prints both tables
side by side. Exercise 5 comes back at the end and runs it again with a negative
cost, where the settled set is not merely unnecessary but **wrong** — two rows,
each one minute high, in a table that otherwise agrees.

Exercises 3 and 4 are the other pair. Union-find on its own, with the parent
array printed before and after a lookup so path compression is a thing you have
watched rather than read about; then the spanning tree, where the whole algorithm
is "sort by price, accept if it joins two things not already joined" and the
second half of that sentence is a union-find query.

Run any of them directly:

```bash
python exercise-01-hut-relay-timing-solution.py
```

No packages, no arguments, no input.

## A note on what is being graded

**Show the invariant, do not assert it.** Three of these five files print
something the algorithm is doing — a settling order, a parent array, two tables
side by side. That is deliberate, and your write-ups should do the same. "The
settled set guarantees the answer is final" is a sentence anyone can write; the
Cut Sluice row is evidence.

**Say which algorithm and why *this* one.** By the end of the week you have four
that all look similar from a distance: the frontier picker, repeated relaxing,
all-pairs, and the spanning tree. Naming the discriminator — negative costs, all
pairs wanted, connect-everything rather than shortest-route — in one sentence is
what Mock #2 grades.

---

After all five pass, move on to
[Challenge 1 — The Reefer Transfer Budget](../challenges/challenge-01-reefer-transfer-budget.md).
