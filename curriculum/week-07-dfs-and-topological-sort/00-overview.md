# Week 7 — Depth-First Search and Topological Sort

```
┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐
│ U │  │ M │  │ P │  │ I │  │ R │  │ E │
└───┘  └───┘  └───┘  └───┘  └───┘  └───┘
```

> *Week 6 installed BFS — the queue, the visited set, the level-monotonic shortest-path argument. Week 7 installs the dual: **DFS** — the recursion stack, the three node colors (white / gray / black), and the post-order trick that turns "is this graph acyclic, and if so what is a topological order?" into a single linear-time pass. By Sunday you can write the recursive DFS template, the iterative version with an explicit stack, and Kahn's BFS-style topological sort, all from memory, and you can defend each against its alternative out loud.*

Welcome to Week 7 of **C2 · CrunchTime — The Code** — the third week of Phase 2. Last week installed BFS and the level-monotonicity argument. This week installs DFS and its three highest-leverage applications: **connectivity** (the easy case), **cycle detection** (the gray-set invariant), and **topological sort** (the post-order trick, plus Kahn's BFS-shaped alternative).

DFS has a reputation for being "the harder one" relative to BFS — and that is partly true. The recursion is short, but the *state* you carry on the call stack is heavier, the bug patterns are subtler, and the negative-space recognition ("is this DFS or BFS?") is graded harder in Phase 2 mocks. The work this week is to install the canonical templates (recursive + iterative + Kahn) and the three-color invariant so cleanly that a topological-sort prompt produces the post-order one-liner without hesitation.

By Sunday of Week 7 you will:

- **Recognize** a DFS problem in 30 seconds and classify it as **connectivity / path-existence / cycle detection / topological sort / backtracking** in the next sentence.
- **Write** the canonical recursive DFS template from memory, defend the visited-set as the invariant, and explain why DFS is `O(V + E)` time with `O(V)` recursion-stack space.
- **Write** the iterative DFS with an explicit stack — the version that does not hit Python's recursion limit on long chains — and defend why pre-order pushes the children in reverse for the same visit order as the recursive version.
- **Apply the three-color invariant** (white = unvisited, gray = on the current stack, black = finished) to detect cycles in a directed graph. The gray set is the cycle-detection invariant; defending it cleanly is the senior signal.
- **Compute a topological order** by both methods: **DFS post-order** (Tarjan-style — finish a node, prepend to the order) and **Kahn's algorithm** (BFS-shaped — queue every zero-in-degree node, decrement neighbors). Defend which to use when.
- Have solved **three DFS exercises** — recursive connectivity, iterative path existence, and Course Schedule II (the canonical topological sort) — each with a UMPIRE write-up.
- Have shipped **one challenge** (Critical Connections / bridges via Tarjan's low-link — the canonical hard DFS application) plus an optional stretch (Alien Dictionary — topological sort on a derived edge set).
- Have shipped the quiz, the homework, and the **mini-project**: one DFS write-up (cycle detection or connectivity) and one topological-sort write-up, fully UMPIRE-narrated.

---

## Learning objectives

By the end of this week, you will be able to:

- **Match** a DFS problem in 30 seconds by recognizing the canonical signals: "any path," "all paths," "connected components," "cycle detection," "is this a DAG," "topological order," "valid sequence given prerequisites," "longest path in a tree."
- **Distinguish DFS from BFS** in one sentence per problem: DFS for connectivity / cycle / topo sort / any-path / backtracking; BFS for shortest-path / level-by-level / multi-source spread. Both are `O(V + E)`; the choice is on output shape, not asymptotics.
- **Implement** three canonical templates without notes:
  - Recursive DFS with a visited set and a `dfs(node)` helper.
  - Iterative DFS with an explicit stack — the version that survives Python's default recursion limit of 1000.
  - Kahn's BFS-shaped topological sort with an in-degree array and a queue.
- **Apply the three-color invariant** for cycle detection in a directed graph. State the invariant out loud: *"A node is gray if and only if it is on the current DFS path. A back-edge to a gray node is a cycle. A back-edge to a black node is not a cycle — that subtree is already finished."*
- **Compute a topological order via DFS post-order** and defend the construction: *"A node is appended to the order only after all of its descendants have finished — this guarantees the reverse-order property of a DAG topological sort."*
- **Choose between DFS post-order and Kahn's algorithm** for topological sort. DFS post-order is recursive, cleaner for small graphs, and gives a natural cycle-detection by-product (the gray check). Kahn's is iterative, cleaner for streaming inputs, and gives a natural "report all valid orders" extension.
- **Recognize when DFS does *not* apply** — shortest path on unweighted graphs (use BFS), shortest path on weighted graphs (Dijkstra), level-by-level outputs (BFS).
- **Apply DFS to a tree problem** — the special case where there are no cycles and the visited set is implicit. The recursion templates collapse to "visit left, visit right, do something with the return values" — the foundation of every tree-DP problem in Phase 3.

---

## Prerequisites

- **Weeks 1-6 complete.** You have shipped two BFS write-ups; you can deliver UMPIRE without notes on a queue + visited-set problem.
- **Comfortable with Python recursion.** DFS is the algorithm where recursion-limit bugs first appear. Run `python3 -c "import sys; print(sys.getrecursionlimit())"` once; the default is 1000. For LeetCode inputs with `V ~ 10⁵`, you will need either iterative DFS or `sys.setrecursionlimit(10**6)` plus the patience to debug stack overflows.
- **Comfortable with `dict[node, list[node]]`.** The adjacency list is the canonical graph representation this week. If a problem gives you an edge list, the first line of code is usually `adj = collections.defaultdict(list); for u, v in edges: adj[u].append(v)`.
- **Comfortable with `collections.deque`.** Kahn's algorithm uses a queue; the `popleft()` discipline from Week 6 applies unchanged.

---

## Topics covered

- The canonical recursive DFS template — `dfs(node)`, visited set, the three-line body
- The iterative DFS template — explicit stack, push-children-in-reverse for pre-order parity
- The **three-color invariant** — white / gray / black — for cycle detection in a directed graph
- **Topological sort via DFS post-order** — Tarjan-style; the post-order trick
- **Topological sort via Kahn's algorithm** — BFS-shaped; in-degree array; queue of zero-in-degree nodes
- **Cycle detection in an undirected graph** — the parent-pointer technique (a back-edge to a non-parent is a cycle)
- **Cycle detection in a directed graph** — the gray-set technique (a back-edge to a gray node is a cycle)
- **DFS on a tree** — the recursion-as-tree-traversal collapse; no visited set needed
- **The post-order vs pre-order distinction** — when to compute on the way down vs on the way up
- **Why DFS does not find shortest paths** — and what BFS adds (the level-monotonicity argument from Week 6)
- **Stack-overflow defense** — `sys.setrecursionlimit` is a workaround; iterative DFS is the fix

---

## Weekly schedule (intensive · 36h)

| Day | Focus | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project | Self-Study | Daily Total |
|-----|-------|---------:|----------:|-----------:|----------:|---------:|-------------:|-----------:|------------:|
| Monday | Recursive DFS + connectivity; exercise 1 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Tuesday | Iterative DFS + cycle detection; exercise 2 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Wednesday | Topological sort (DFS + Kahn); exercise 3 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Thursday | Mini-project drafting; challenge ramp | 0h | 1h | 1h | 0.5h | 1h | 1.5h | 1h | 6h |
| Friday | Challenge (Critical Connections) | 0h | 0h | 2h | 0.5h | 1h | 1.5h | 1h | 6h |
| Saturday | Mini-project — DFS + topo write-ups | 0h | 0h | 0h | 0.5h | 1h | 3h | 0h | 4.5h |
| Sunday | Quiz + retro + push | 0h | 0h | 0h | 0.5h | 0h | 4h | 0h | 4.5h |
| **Total** | | **6h** | **7h** | **3h** | **3h** | **6h** | **10h** | **3.5h** | **38.5h** |

(The week budgets ~36 hours; the table sums slightly higher to absorb the Phase-2 ramp. Drop 0.5h from Self-Study if 36h is your hard cap.)

**Mastery (10h/wk):** spread the same content over three calendar weeks. The mini-project lands in calendar Week 22 of the mastery pathway. See the [mastery study plan](../study-plans/mastery-1-year.md).

---

## How to navigate this week

| File | What's inside |
|------|---------------|
| [README.md](./00-overview.md) | This overview |
| [resources.md](./01-resources.md) | Free readings + DFS + topo references + glossary additions |
| [lecture-notes/01-recursive-dfs.md](./02-lecture-notes/01-recursive-dfs.md) | The canonical recursive DFS template, visited-set discipline, pre/post-order, the four bug patterns |
| [lecture-notes/02-iterative-dfs.md](./02-lecture-notes/02-iterative-dfs.md) | The explicit-stack DFS — the version that survives recursion-limit failures |
| [lecture-notes/03-topological-sort.md](./02-lecture-notes/03-topological-sort.md) | DFS post-order, Kahn's algorithm, the three-color invariant, cycle detection in directed graphs |
| [exercises/README.md](./03-exercises/00-overview.md) | Index of the three DFS exercises and SOLUTIONS |
| [exercises/exercise-01-number-of-provinces.py](./03-exercises/exercise-01-number-of-provinces.py) | Connectivity / connected components — recursive DFS warm-up |
| [exercises/exercise-02-has-path.py](./03-exercises/exercise-02-has-path.py) | Iterative DFS — path existence with an explicit stack |
| [exercises/exercise-03-course-schedule-ii.py](./03-exercises/exercise-03-course-schedule-ii.py) | Topological sort — Kahn or DFS post-order; the canonical Phase-2 topo problem |
| [exercises/SOLUTIONS.md](./03-exercises/SOLUTIONS.md) | Worked solutions with UMPIRE narration; consult after attempting each exercise |
| [challenges/README.md](./04-challenges/00-overview.md) | Index of weekly challenges |
| [challenges/challenge-01-critical-connections.md](./04-challenges/challenge-01-critical-connections.md) | Bridges via Tarjan's low-link — the canonical hard DFS application |
| [challenges/challenge-02-alien-dictionary.md](./04-challenges/challenge-02-alien-dictionary.md) | Topological sort on a derived edge set — the canonical "model the problem as a graph" stretch |
| [quiz.md](./05-quiz.md) | 10 pattern-recognition questions |
| [homework.md](./06-homework.md) | Six practice problems (~5 hrs) — one connectivity, one cycle detection, one topo, one tree-DFS, plus behavioral and design warm-ups |
| [mini-project/README.md](./07-mini-project/00-overview.md) | **One DFS write-up + one topological-sort write-up, fully UMPIRE-narrated** — the week's deliverable |

---

## Stretch goals

- **Read the LeetCode "Depth-First Search" tag** and skim 20 titles. For each, predict in 5 seconds: connectivity? cycle? topo? backtracking? tree DFS? Stretches the Match-step muscle.
- **Re-derive the canonical recursive template from scratch** without re-reading Lecture 1. If you cannot, you do not yet own the template. Re-read and re-derive until you can.
- **Find one production-engineering DFS story.** Examples: build-system dependency resolution (topo sort), garbage-collector reachability (DFS on the object graph), module loader cycle detection. The "where does DFS live in real systems?" question lifts you out of the LeetCode frame.
- **Read about Tarjan's strongly-connected-components algorithm** (one paragraph). It is the natural next step after cycle detection and post-order topo. Out of scope this week; covered in C5.

---

## What "done" looks like for Week 7

A learner who has shipped Week 7 has, in their portfolio repo:

- Three UMPIRE write-ups for the exercises, with recordings ≥ 10 minutes.
- One UMPIRE write-up for the Critical Connections challenge.
- The quiz answered (score recorded).
- The homework problems committed.
- **Two mini-project write-ups** (one DFS, one topological sort), each with a 30-second pattern-recognition memo at the top, under `umpire-writeups/c2-week-07/mini-project/`.
- A push log showing daily commits Mon-Sun.

If all of that is present and pushed, Phase 2's third week is closed. You are ready for Week 8 — backtracking.

---

## A note on the Phase 2 ramp

Week 7 is, content-wise, *the* graph week. By Sunday you will have shipped BFS (W6) and DFS (W7) — the two algorithms that anchor every graph problem in the standard interview repertoire. Week 8 (backtracking) is the recursive cousin of DFS where the visited set is replaced by an "undo" step. Week 9 is Mock #2 — at least one graph problem is graded.

If you find yourself ahead by Friday, the right stretch is **not** another exercise — it is to write a second-pass parametric mini-project problem from Week 6 (the BFS / DFS pair forms the navigable Phase-2 graph portfolio). The Phase-2 retrospective at the end of Week 9 will be much easier if both the Week 6 and Week 7 mini-projects are polished by Sunday Week 7.

If you find yourself *behind* by Wednesday, skip Exercise 2 (iterative DFS) for now and prioritize Exercise 3 (topological sort) — topo is the most heavily-graded Phase-2 pattern in Mock #2, and iterative DFS can be picked up in 30 minutes once recursive DFS is fluent.

---

## Up next

[Week 8 — Backtracking](../week-08/) — once your two DFS write-ups are pushed, your three-color invariant is clean, and you can write Kahn's algorithm from memory without consulting the lecture.

---

*If you find errors in this material, please open an issue or send a PR. Future learners will thank you.*
