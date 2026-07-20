# Week 7 — Homework

Six problems. ~5 hours total. Each commits to your portfolio repo. One connectivity, one cycle detection, one topological sort, one tree-DFS, plus the behavioral and design warm-ups.

---

## Problem 1 — Number of Connected Components in an Undirected Graph (LeetCode 323) (45 min)

The canonical "connected components from an edge list" problem. The structural cousin of Exercise 1 — same `n` cities, but encoded as an edge list instead of an adjacency matrix.

**Problem.** Given `n` nodes labeled `0..n-1` and an array of undirected edges, return the number of connected components.

**The insight.** Build an adjacency list from the edge list. Walk the nodes; when finding an unvisited node, run DFS (recursive or iterative) and increment the component counter. Identical structure to Exercise 1; the only difference is the graph representation.

**Acceptance:**

- A file `umpire-writeups/c2-week-07/hw-01-connected-components.md` with the UMPIRE write-up.
- Match section explicitly compares against Exercise 1 (adjacency matrix vs adjacency list — same algorithm, different graph representation).
- Evaluate section justifies **`O(V + E)` time, `O(V + E)` space** (the adjacency list dominates).
- Recording ≥ 15 minutes.
- Tests passing on: `n=5, edges=[[0,1],[1,2],[3,4]] → 2`, `n=5, edges=[[0,1],[1,2],[2,3],[3,4]] → 1`, `n=1, edges=[] → 1`, `n=4, edges=[] → 4`.

This problem and Exercise 1 share the connectivity template. Your Match section should call out the structural parallel — the algorithm is the same; only the input format differs.

---

## Problem 2 — Course Schedule (LeetCode 207) (45 min)

The cycle-detection-only variant of Exercise 3. Return `True` if all courses can be finished (DAG), else `False`.

**Problem.** Given `numCourses` and a list of `[a, b]` prerequisites, return whether all courses can be completed.

**The insight.** Two equivalent approaches: (a) the three-color DFS invariant from Lecture 3 §2, or (b) Kahn's algorithm checking `len(order) == numCourses`. Either works; defend your choice. The cleaner answer for "just yes/no" is the three-color DFS — it returns early on the first cycle. Kahn's runs to completion regardless.

**Acceptance:**

- File `umpire-writeups/c2-week-07/hw-02-course-schedule.md`.
- Match section names **directed cycle detection** explicitly and compares the two algorithms.
- Working code with tests: `numCourses=2, prerequisites=[[1,0]] → True`, `numCourses=2, prerequisites=[[1,0],[0,1]] → False`, `numCourses=3, prerequisites=[[1,0],[2,1]] → True`, `numCourses=3, prerequisites=[[0,1],[1,2],[2,0]] → False`.

This is the cleanest "is this graph a DAG?" variant. After Problems 1 and 2, the connectivity-and-cycle recognition should be reflexive for any directed-graph problem.

---

## Problem 3 — Find Eventual Safe States (LeetCode 802) (60 min)

A directed-graph problem that requires recognizing the **reverse topological sort** framing. Harder than Course Schedule because the question is not "is there a cycle?" but "which nodes can reach a terminal (no-outgoing-edges) node without ever entering a cycle?"

**Problem.** Given a directed graph as an adjacency list `graph[i]` = nodes that `i` has edges to. A node is *safe* if every walk starting from it eventually leads to a terminal node. Return all safe nodes in ascending order.

**The insight.** Two equivalent approaches:

1. **DFS with three-color invariant.** A node is safe iff it has no path to any cycle. Run three-color DFS; a node is safe iff the DFS from it finishes (no back-edge encountered). Mark each finished node as safe; failed (back-edge-encountering) nodes are unsafe.
2. **Kahn on the reversed graph.** Reverse every edge. Now terminal nodes (out-degree 0 in the original) become source nodes (in-degree 0 in the reverse). Run Kahn on the reverse; every node Kahn processes is safe. Nodes never processed are unsafe (they participate in a cycle in the original).

Choose one and defend it.

**Acceptance:**

- File `umpire-writeups/c2-week-07/hw-03-eventual-safe-states.md`.
- Match section names **both equivalent approaches** and defends the choice.
- Evaluate section justifies `O(V + E)` time and space.
- Tests: `graph=[[1,2],[2,3],[5],[0],[5],[],[]] → [2,4,5,6]`, `graph=[[1,2,3,4],[1,2],[3,4],[0,4],[]] → [4]`.

This problem is the bridge between Exercise 3 and the challenges. The senior signal is recognizing that "safe" decomposes as "cannot reach a cycle," which is topo-sort-shaped.

---

## Problem 4 — Validate Binary Search Tree (LeetCode 98) (45 min)

The canonical tree-DFS problem. Two structural patterns: in-order traversal (values must come out sorted) or recursive bounds (every node's value must lie in `(lo, hi)` and the children narrow the bounds).

**Problem.** Given the root of a binary tree, return `True` if it is a valid BST. A BST has: every left descendant's value is strictly less than the node's value; every right descendant's value is strictly greater.

**The insight.** The simpler approach is the **bounds approach**: recurse with `(lo, hi)` bounds; at each node check `lo < node.val < hi`; recurse left with `(lo, node.val)` and right with `(node.val, hi)`. Initial call is `(-inf, +inf)`. The in-order approach also works but requires either materializing the list (extra space) or tracking the previous value with a mutable closure variable (subtle).

**Acceptance:**

- File `umpire-writeups/c2-week-07/hw-04-validate-bst.md`.
- Match section names **tree-DFS with bounds** explicitly; comment briefly on the in-order alternative.
- Evaluate section justifies `O(N)` time and `O(H)` space (where `H` is the tree's height).
- Tests: standard BST → `True`; tree with a deep descendant violating the root-bound → `False`; single node → `True`; empty → `True`.

This problem is **the** canonical tree-DFS interview problem. Mock #2 routinely draws from this template; expect a 1-2 minute solve once you own the bounds pattern.

---

## Problem 5 — Behavioral story #7 (45 min)

The story bank continues.

**Acceptance:**

- A file `behavioral/story-07.md` in your portfolio repo.
- Topic: **"Tell me about a time you had to refactor or rewrite a piece of code that you (or someone else) wrote earlier."**
- Format: STAR (Situation, Task, Action, Result).
- 200-400 words.
- Read it aloud at least twice.
- Bonus credit: the story should connect to the *meta-skill* of "recursive code vs iterative code" — a refactor from recursive DFS to iterative DFS (motivated by recursion-limit risk or production performance) is a textbook engineering decision. The connection is: every "I refactored X" story is a "two-approaches-different-tradeoffs" decision; recursive-to-iterative is a clean specific instance.

---

## Problem 6 — System-design ground zero #7 (45 min)

Seventh 300-word warm-up.

**Acceptance:**

- A file `system-design/notes-week-07.md` containing a 300-word answer to: **"How would you design a build system that resolves and executes ~50,000 build targets in parallel, respecting prerequisite dependencies?"**
- Do not look up the canonical answer first. Write what you would say in an interview today.
- After writing, search "Bazel architecture" or "build system topological sort" and read one free article (try the Bazel design docs or the Make manual's "How Make Reads a Makefile" section). Note three things you would add — *especially* if the article mentions topological sort over the dependency graph.

The connection to this week: build systems are *topological sort + parallel execution* at scale. The "build graph" is a DAG of targets; the "topological order" is the legal order of compilation; the "ready queue" is the set of zero-pending-prerequisite targets that can run in parallel. The interview-tell on this prompt is mentioning the topological-sort framing *and* the parallelism layer (Kahn's natural extension: every node in the ready queue at the same time can be processed in parallel — that is exactly what `make -j N` does).

---

## Time budget

| Problem | Time |
|--------:|----:|
| 1 — Number of Connected Components | 45 min |
| 2 — Course Schedule | 45 min |
| 3 — Find Eventual Safe States | 60 min |
| 4 — Validate Binary Search Tree | 45 min |
| 5 — Behavioral story #7 | 45 min |
| 6 — System-design warm-up #7 | 45 min |
| **Total** | **4h 45min** |

---

By the end of Week 7 your portfolio repo's commit history should show ~95-115 commits total (the cumulative count through Week 6 + ~15-20 commits this week, including the mini-project's two write-ups and the Critical Connections challenge write-up). The cadence is the artifact; keep the streak.

Up next: [Week 8 — Backtracking](../week-08/).
