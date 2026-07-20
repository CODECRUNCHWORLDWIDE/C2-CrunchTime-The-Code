# Week 6 — Breadth-First Search

```
┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐
│ U │  │ M │  │ P │  │ I │  │ R │  │ E │
└───┘  └───┘  └───┘  └───┘  └───┘  └───┘
```

> *Week 5 trained the first logarithmic-time pattern of Phase 2. Week 6 trains the first **graph** pattern — **BFS**, the canonical "shortest path on an unweighted graph" algorithm. The lecture work is short; the recognition work is heavier. By Sunday you can write the canonical queue + visited-set template without notes, distinguish grid-BFS from node-BFS in 30 seconds, defend "BFS finds shortest paths only because the graph is unweighted" out loud, and apply multi-source BFS as the high-leverage idiom of the week.*

Welcome to Week 6 of **C2 · CrunchTime — The Code** — the second week of Phase 2. Last week installed binary search and the parametric idiom. This week installs BFS: queue-based level-by-level traversal, the visited-set invariant, and the two surface shapes (grid and node) that show up in every Phase-2 graph interview.

BFS has a reputation for being "the easy one" relative to DFS — and that is partly true. The template is shorter and the bugs are fewer. But the *recognition* is harder than candidates expect, because the surface forms vary wildly: a 2-D grid with obstacles, a string-transformation puzzle, a binary tree level traversal, a "minimum number of moves" board problem — all four are the same algorithm, with the same template, with the same invariant. The work this week is to install that recognition reflex so you read any of those prompts and write the queue + visited block without thinking about it.

By Sunday of Week 6 you will:

- **Recognize** a BFS problem in 30 seconds, classify it as **grid-BFS** or **node-BFS**, and pick the right neighbor-generation function for the sub-shape.
- **Write** the canonical queue + visited-set template from memory, defend the visited-set as an invariant out loud, and explain why BFS finds shortest paths on an unweighted graph and *only* on an unweighted graph.
- **Apply multi-source BFS** — the high-leverage Week-6 idiom — by seeding the queue with multiple starts. The rotting-oranges and 0/1 matrix families compile to one line of seed code.
- **Distinguish** when to track distance level-by-level (an outer `for _ in range(len(queue))` loop) and when to store `(node, dist)` on the queue. Both work; only one defends cleanly per problem family.
- Have solved **five BFS drills** spanning both sub-shapes — level-order traversal, shortest path in a grid, rotting oranges (multi-source), word ladder (node-BFS on a string graph), and binary tree right-side view (per-level visibility).
- Have shipped one challenge (Minimum Knight Moves on an infinite board — the canonical "BFS on an implicit graph"), the quiz, and the homework.
- Have shipped the mini-project: **one grid-BFS write-up and one node-BFS write-up, fully UMPIRE-narrated**, with the two sub-shapes laid side-by-side for portfolio review.

---

## Learning objectives

By the end of this week, you will be able to:

- **Match** a BFS problem in 30 seconds by recognizing the canonical signals: "shortest path," "minimum number of moves," "level order," "spread / infection / fire," "unweighted graph," "fewest steps to reach …".
- **Distinguish** grid-BFS from node-BFS in one sentence. Grid-BFS: the graph is implicit; neighbors come from 4- or 8-direction offsets on `(r, c)` cells. Node-BFS: the graph is explicit (adjacency list) or implicit-on-strings (word ladder), neighbors come from a `neighbors(node)` function.
- **Implement** the canonical BFS template — `deque` queue, `visited` set, level counter — without notes, in under 90 seconds.
- **Defend** the visited-set as an invariant: every node enters the queue at most once; the queue size is bounded by `O(V)`; the total work is `O(V + E)`.
- **Apply multi-source BFS** by seeding the initial queue with multiple starts. Recognize the idiom from prompts like "starting from all fresh oranges simultaneously" or "distance from every zero in the matrix."
- **Choose** between level-tracking (outer loop over `len(queue)`) and per-node distance (queue of `(node, dist)` tuples) and defend the choice. Level tracking pairs with "by level" outputs (right side view, level order). Per-node distance pairs with "shortest path to a specific target" outputs.
- **Recognize** when BFS does *not* apply — weighted graphs (use Dijkstra), graphs with no monotone-cost structure (use DFS / iterative deepening), problems where the answer is not a distance (use DFS, backtracking, or DP).
- **Apply bidirectional BFS** as the high-end optimization for "shortest path between two known endpoints in a large graph" — the technique that turns Word Ladder from `O(N · L²)` into roughly `O(sqrt) · N · L²)`.

---

## Prerequisites

- **Weeks 1-5 complete.** You have shipped five binary-search write-ups; you can deliver UMPIRE without notes on a parametric problem.
- **Comfortable with `collections.deque`.** BFS uses `deque` because `popleft()` is `O(1)` and `pop()` on a `list` is `O(n)`. If you have never used `deque`, run `python -c "from collections import deque; help(deque)"` once before Drill 1.
- **Comfortable with hash sets.** The visited set is a `set[Hashable]` — node identities must be hashable. Tuples are hashable; lists are not. Plan accordingly when grid cells are coordinates.
- **A working pytest setup.** Drills are graded by [`timed_runner.py`](exercises/timed_runner.py).

---

## Topics covered

- The canonical BFS template: `deque`, `visited` set, the four-line loop body
- The two sub-shapes: **grid-BFS** (implicit graph on `(r, c)` cells) and **node-BFS** (explicit or implicit graph on hashable nodes)
- **Level tracking:** outer `for _ in range(len(queue))` loop — the idiom for "by level" outputs
- **Per-node distance:** `(node, dist)` tuples on the queue — the idiom for "shortest path to one target"
- **Multi-source BFS:** seed the queue with multiple starts — the rotting-oranges / 0-1-matrix idiom
- **Bidirectional BFS:** advance from both endpoints, halt when the frontiers meet — the Word Ladder optimization
- **Why BFS finds shortest paths on unweighted graphs** — the level-monotonicity argument
- **Why BFS does not find shortest paths on weighted graphs** — and what Dijkstra adds (one paragraph; depth in C5)
- **When BFS does not apply** — weighted graphs, problems where the answer is not a distance, problems where the state space is exponential without aggressive pruning

---

## Weekly schedule (intensive · 36h)

| Day | Focus | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project | Self-Study | Daily Total |
|-----|-------|---------:|----------:|-----------:|----------:|---------:|-------------:|-----------:|------------:|
| Monday | Template + level tracking; drills 1-2 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Tuesday | Multi-source + grid sub-shape; drill 3 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Wednesday | Node-BFS + bidirectional; drills 4-5 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Thursday | Mini-project drafting; challenge ramp | 0h | 1h | 1h | 0.5h | 1h | 1.5h | 1h | 6h |
| Friday | Challenge (Minimum Knight Moves) | 0h | 0h | 2h | 0.5h | 1h | 1.5h | 1h | 6h |
| Saturday | Mini-project — grid + node write-ups | 0h | 0h | 0h | 0.5h | 1h | 3h | 0h | 4.5h |
| Sunday | Quiz + retro + push | 0h | 0h | 0h | 0.5h | 0h | 4h | 0h | 4.5h |
| **Total** | | **6h** | **7h** | **3h** | **3h** | **6h** | **10h** | **3.5h** | **38.5h** |

(The week budgets ~36 hours; the table sums slightly higher to absorb the Phase-2 ramp. Drop 0.5h from Self-Study if 36h is your hard cap.)

**Mastery (10h/wk):** spread the same content over three calendar weeks. The mini-project lands in calendar Week 19 of the mastery pathway. See the [mastery study plan](../study-plans/mastery-1-year.md).

---

## How to navigate this week

| File | What's inside |
|------|---------------|
| [README.md](./README.md) | This overview |
| [resources.md](./resources.md) | Free readings + BFS references + glossary additions |
| [lecture-notes/01-the-bfs-template.md](./lecture-notes/01-the-bfs-template.md) | The canonical queue + visited-set template, level tracking, the four bug patterns |
| [lecture-notes/02-grid-bfs-and-graph-bfs.md](./lecture-notes/02-grid-bfs-and-graph-bfs.md) | The two sub-shapes; multi-source BFS; bidirectional BFS |
| [exercises/README.md](./exercises/README.md) | Index of the five BFS drills |
| [exercises/drill-01-level-order.md](./exercises/drill-01-level-order.md) | Binary tree level-order traversal — the cleanest "by level" exercise |
| [exercises/drill-02-shortest-path-grid.md](./exercises/drill-02-shortest-path-grid.md) | Shortest path in a binary matrix — grid-BFS with obstacles |
| [exercises/drill-03-rotting-oranges.md](./exercises/drill-03-rotting-oranges.md) | Multi-source BFS — the canonical "spread" problem |
| [exercises/drill-04-word-ladder.md](./exercises/drill-04-word-ladder.md) | Node-BFS on a string graph with a wildcard-bucket neighbor index |
| [exercises/drill-05-binary-tree-right-side-view.md](./exercises/drill-05-binary-tree-right-side-view.md) | Level tracking — emit the last node at each depth |
| [exercises/timed_runner.py](./exercises/timed_runner.py) | Pytest harness for the five drills |
| [challenges/README.md](./challenges/README.md) | Index of weekly challenges |
| [challenges/challenge-01-minimum-knight-moves.md](./challenges/challenge-01-minimum-knight-moves.md) | BFS on an infinite implicit graph — the canonical hard BFS problem |
| [quiz.md](./quiz.md) | 10 pattern-recognition questions |
| [homework.md](./homework.md) | Six practice problems (~5 hrs) — two grid, two node, one bidirectional, plus the behavioral and design warm-ups |
| [mini-project/README.md](./mini-project/README.md) | **One grid-BFS write-up + one node-BFS write-up, fully UMPIRE-narrated** — the week's deliverable |

---

## Stretch goals

- **Read the LeetCode "Breadth-First Search" tag** and skim 20 titles. For each, predict in 5 seconds: grid? node? multi-source? bidirectional? Stretches the Match-step muscle.
- **Re-derive the canonical template from scratch** without re-reading Lecture 1. If you cannot, you do not yet own the template. Re-read and re-derive until you can.
- **Find one production-engineering BFS story.** Examples: web crawler frontier, social-graph "people you may know," package-manager dependency level ordering. The "where does BFS live in real systems?" question lifts you out of the LeetCode frame.
- **Read about 0-1 BFS** (deque-based; `appendleft` for zero-cost edges, `append` for one-cost). It is the natural next step between BFS and Dijkstra. Out of scope for the drills but worth knowing the name.

---

## What "done" looks like for Week 6

A learner who has shipped Week 6 has, in their portfolio repo:

- Five UMPIRE write-ups for the drills, all with recordings >= 10 minutes.
- One UMPIRE write-up for the Minimum Knight Moves challenge.
- The quiz answered (score recorded).
- The homework problems committed.
- **Two mini-project write-ups** (one grid, one node), each with a 30-second pattern-recognition memo at the top, under `umpire-writeups/c2-week-06/mini-project/`.
- A push log showing daily commits Mon-Sun.

If all of that is present and pushed, Phase 2's second week is closed. You are ready for Week 7 — DFS.

---

## A note on the Phase 2 ramp

Week 6 is, content-wise, lighter than Week 5 — BFS has fewer template variants than binary search and fewer subtle off-by-one bugs. The compensation is on the *recognition* side: BFS problems disguise themselves more aggressively. A "minimum number of moves" knight problem reads like math; a "rotting oranges" prompt reads like a story; a "word ladder" prompt reads like a puzzle. All three compile to the same algorithm. The work this week is to install that translation reflex so you read any of those prompts and write the queue + visited block without thinking.

If you find yourself ahead by Friday, the right stretch is **not** another drill — it is to write a second-pass parametric mini-project problem from Week 5 (we did warn you Phase 2 grades Match harder than candidates expect). The Phase 2 retrospective at the end of Week 9 will be much easier if the Week 5 mini-project is *also* polished by Sunday Week 6.

---

## Up next

[Week 7 — DFS](../week-07/) — once your two BFS write-ups are pushed, your visited-set invariants are clean, and you can write the canonical loop from memory without consulting the lecture.

---

*If you find errors in this material, please open an issue or send a PR. Future learners will thank you.*
