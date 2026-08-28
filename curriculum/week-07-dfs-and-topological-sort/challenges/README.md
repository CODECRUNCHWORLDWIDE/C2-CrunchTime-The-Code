# Week 7 — Challenges

Two challenges. The first is required and is the hardest depth-first
application of the week. The second is the optional stretch — do it if you
finish the first with time to spare.

| # | Challenge | What it drills | Difficulty | Target time | Required? |
|---|-----------|----------------|------------|------------:|:---------:|
| 1 | [Chokepoint mains](./challenge-01-chokepoint-mains.md) | Discovery times and low-links on an explicit stack; the pipes whose failure splits the network | Hard | 120 min | yes |
| 2 | [Consist reconstruction](./challenge-02-consist-reconstruction.md) | Deriving the constraints before sorting them, and separating "forced" from "merely possible" | Hard | 90 min | optional |

Both build directly on the exercises:

- **Challenge 1** takes the explicit-stack walk from
  [Exercise 2](../exercises/exercise-02-conveyor-reachability.md) and makes it
  carry two numbers per station instead of a visited mark. The low-link is
  computed **on the way back up**, which is the same post-order move as
  [Exercise 5](../exercises/exercise-05-firmware-install-order.md) — only there
  the work-on-finish appends a name, and here it takes a minimum.
- **Challenge 2** takes Kahn's algorithm from
  [Exercise 4](../exercises/exercise-04-refit-order.md) and puts the hard part
  *before* it: the constraints are not handed to you, you have to read them out
  of the sightings, and getting that step wrong costs you the whole problem
  however good your topological sort is.

If you are still stuck on Challenge 1 after an hour, stop and re-read
[Lecture 1 §4](../lecture-notes/01-recursive-dfs.md) on pre-order against
post-order, then
[Lecture 2 §4](../lecture-notes/02-iterative-dfs.md) on carrying post-order work
on an explicit stack. The low-link cannot be derived until the post-order shape
is clear; writing code before that is where every wrong attempt starts.

Challenge 2 is **optional** if you are short of time. If you can only do one,
do Challenge 1 — it is the one Mock #2 draws from most often. Challenge 2 is
the natural follow-up, and what it strengthens is the recognition step: seeing
a graph in a problem that never mentions one.

Both have cousins in the homework.
[Problem 1](../homework/problem-01-hose-clusters.md) shares the connectivity
walk with Exercise 1;
[Problem 2](../homework/problem-02-prep-step-audit.md) and
[Problem 3](../homework/problem-03-safe-forwarding.md) share the loop machinery
with Exercise 3 and the counting run with Exercise 4.
