# Week 9 — Exercises

Five exercises, in order. Each has a page with the brief, the constraints, the
worked solution and the acceptance checklist, and a runnable file beside it that
ends by printing `All checks passed.`

| # | Exercise | Sub-shape | Difficulty | Target time |
|---|----------|-----------|------------|------------:|
| 1 | [The Gate Tag Tree](./exercise-01-gate-tag-tree.md) | A prefix tree from nested dicts, and the two queries people conflate | Easy | 35 min |
| 2 | [The Ferry Desk Lookahead](./exercise-02-ferry-desk-lookahead.md) | Collecting under a prefix, stopping early at a limit | Easy-Medium | 35 min |
| 3 | [The Callsign Stub](./exercise-03-callsign-stub.md) | A count at every node — precompute at build, read at query | Medium | 40 min |
| 4 | [The Beacon Flash Period](./exercise-04-beacon-flash-period.md) | The border table, and the arithmetic that reads a repeat out of it | Medium | 45 min |
| 5 | [The Stripped Manifest Line](./exercise-05-stripped-manifest-line.md) | A tree and a memo together — the week's composition | Medium | 45 min |

Do them in order. Exercise 1 is the structure with nothing on top, and it settles
the difference between "is this registered" and "is anything registered below
here" — a distinction the rest of the week depends on. Exercise 2 puts the limit
*inside* the walk. Exercise 3 stores something other than letters at a node,
which is the move that makes tries useful rather than merely tidy. Exercise 4
leaves trees entirely for the border table, and prints the cost difference
instead of asserting it. Exercise 5 is the composition the week has been building
towards, and it is the direct preparation for
[Challenge 1](../challenges/challenge-01-cold-store-aisle-sweep.md).

Run any of them directly:

```bash
python exercise-01-gate-tag-tree-solution.py
```

No packages, no arguments, no input.

## A note on what is being graded

Two things beyond correctness, and both are habits this week installs.

**The reserved key.** Every tree here stores at least one thing that is not a
letter — the end marker, and in Exercise 3 a count as well. Your write-up has to
say how you know that key cannot collide with real data. It is the one way a
dict-of-dicts trie fails silently, and "I used an asterisk" is not the answer;
"no code in this register contains an asterisk, and the builder refuses one that
does" is.

**The cost, as a number.** Three of these five exercises print a comparison or
node count, and they do it because a claim like "the trie saves work" is worth
nothing without one. Your Evaluate section should quote the number the file
printed, not the asymptotic bound alone.

---

After all five pass, move on to
[Challenge 1 — The Cold Store Aisle Sweep](../challenges/challenge-01-cold-store-aisle-sweep.md),
which is Exercise 5's composition applied to a grid.
