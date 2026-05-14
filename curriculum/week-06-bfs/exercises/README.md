# Week 6 — Exercises

Five drills. Each is UMPIRE-narrated, recorded, and graded by [`timed_runner.py`](timed_runner.py).

| # | Drill | Pattern | Difficulty | Target solve time |
|---|-------|---------|------------|------------------:|
| 1 | [Level order traversal](drill-01-level-order.md) | Node-BFS on a tree, level-tracking idiom | Easy | 15 min |
| 2 | [Shortest path in a binary matrix](drill-02-shortest-path-grid.md) | Grid-BFS, 8-directional, per-node distance | Medium | 25 min |
| 3 | [Rotting oranges](drill-03-rotting-oranges.md) | Multi-source grid-BFS | Medium | 25 min |
| 4 | [Word ladder](drill-04-word-ladder.md) | Node-BFS on an implicit graph + wildcard bucket index | Medium/Hard | 35 min |
| 5 | [Binary tree right side view](drill-05-binary-tree-right-side-view.md) | Node-BFS on a tree, level-tracking with last-node emit | Medium | 20 min |

Do them in order. Drills 1 and 5 cement level tracking on trees. Drills 2 and 3 install grid-BFS with the single-source vs multi-source distinction. Drill 4 is the node-BFS-on-strings problem that anchors the rest of the week — it is the prep for the Word Ladder homework variants and the bidirectional-BFS discussion.

After all five drills pass `timed_runner.py`, move on to [the challenge](../challenges/challenge-01-minimum-knight-moves.md) — Minimum Knight Moves, the canonical "BFS on an infinite implicit graph" problem.

Run the harness:

```bash
pytest exercises/timed_runner.py -v
```

Each drill has its own write-up template at the bottom of the drill file. Use it.

## A note on what is being graded

Phase 1's drills graded you mostly on *correctness*. Phase 2's drills add a second axis: **invariant defense**. For every BFS drill, your write-up must state the visited-set invariant and justify enqueue-time marking in one sentence. The recording catches whether you say it; the write-up catches whether you can write it.

Invariant defense is the difference between "the code works" and "the code is robust." Interviewers test for the latter. Drill on the latter.
