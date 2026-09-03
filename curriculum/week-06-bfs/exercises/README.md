# Week 6 — Exercises

Five exercises, in order. Each has a page with the brief, the constraints, the
worked solution and the acceptance checklist, and a runnable file beside it that
ends by printing `All checks passed.`

| # | Exercise | Sub-shape | Difficulty | Target time |
|---|----------|-----------|------------|------------:|
| 1 | [Relay Roster](./exercise-01-relay-roster.md) | Node BFS, one hop at a time, with the level frozen before the queue grows | Easy | 30 min |
| 2 | [Hoist Route](./exercise-02-hoist-route.md) | Grid BFS with obstacles, carrying the distance on the queue | Medium | 40 min |
| 3 | [Siren Reach](./exercise-03-siren-reach.md) | Multi-source grid BFS — one walk, a whole map of answers | Medium | 40 min |
| 4 | [Cable Pull](./exercise-04-cable-pull.md) | The same search on a network big enough to punish the wrong queue | Medium | 45 min |
| 5 | [Feeder Tier Load](./exercise-05-feeder-tier-load.md) | Reducing each level to numbers while it is still one batch | Medium | 35 min |

Do them in order. Exercise 1 installs the level snapshot, which every "by level",
"by tier", "by round" answer for the rest of the course reuses. Exercise 2 puts
the same loop on a grid and teaches the bounds check properly — Python's negative
indexing means a missing bounds check does not crash, it wraps to the far side
and answers a different question. Exercise 3 is the one-line change in the seed
that turns one search into an answer for every source at once. Exercise 4 is
where `list.pop(0)` finally costs real time and you count it instead of taking it
on trust. Exercise 5 reduces a level rather than listing it, and carries the trap
that catches everyone on their first real network: a node wired to two parents is
one node in one tier, however many times it is mentioned.

Run any of them directly:

```bash
python exercise-01-relay-roster-solution.py
```

No packages, no arguments, no input.

## A note on what is being graded

Phase 1 graded you mostly on *correctness*. Phase 2 adds a second axis:
**invariant defence**. For every BFS exercise, your write-up must state the
visited-set invariant and justify enqueue-time marking in one sentence — not
"mark on enqueue" but *why*, and what specifically goes wrong otherwise.

The recording catches whether you say it; the write-up catches whether you can
write it. And the reason it is graded separately is that marking on dequeue
produces correct answers on small inputs, so nothing in your test output will
ever tell you.

---

After all five pass, move on to
[Challenge 1 — Trunk Splice](../challenges/challenge-01-trunk-splice.md), which
searches from both ends at once.
