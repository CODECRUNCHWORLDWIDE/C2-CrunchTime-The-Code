# Week 6 — Challenges

Two challenges. Do at least the first; the second is the harder and the more
interesting.

| # | Challenge | Sub-shape | Difficulty | Target time |
|---|-----------|-----------|------------|------------:|
| 1 | [Trunk Splice](./challenge-01-trunk-splice.md) | Searching from both ends, and the arithmetic that says whether a node is on a shortest route | Hard | 75 min |
| 2 | [Tide Gate](./challenge-02-tide-gate.md) | When a cell is not a state, and what has to go in the visited set instead | Hard | 90 min |

Challenge 1 composes the node-BFS template from Exercise 1 with two things the
exercises did not need: a search run from both ends at once, and a test —
`from_start[node] + from_finish[node] == shortest` — that decides whether a given
node lies on *some* shortest route. The second half is where most attempts go
wrong, because it is arithmetic rather than search, and it is easy to write
something plausible that is subtly not the same claim.

Challenge 2 is the harder idea. The gate's state is not "which square am I on"
but "which square, with the tide at which stage" — and the moment that is true,
a visited set keyed on the square alone starts rejecting positions it has never
actually seen. Nothing crashes. The answer is simply too large, or `None` where
a route exists. Getting the state right *before* writing the loop is the whole
challenge; the code afterwards is Exercise 2 again.

Both have a runnable worked solution beside the page:

```bash
python challenge-01-trunk-splice.py
```

If you are stuck past sixty minutes on either, stop and re-read the constraints
section on the page. On Challenge 1 the answer is the arithmetic sentence; on
Challenge 2 it is the sentence about what a state is. Neither problem can be
derived without its sentence, and trying to write code before you have it is the
source of every wrong attempt.

The challenges differ from the exercises in two ways:

1. **You design the state.** The function names are given; what goes into the
   queue and the visited set is yours to choose and yours to defend.
2. **Longer target time.** Seventy-five to ninety minutes against forty. There is
   more than one valid path, and the reasoning step is most of the work.
