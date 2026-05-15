# Week 10 — Weighted Graphs and Union-Find

```
┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐
│ U │  │ M │  │ P │  │ I │  │ R │  │ E │
└───┘  └───┘  └───┘  └───┘  └───┘  └───┘
```

> *Week 9 installed the trie — the dict-of-dict prefix tree, the autocomplete walk, the KMP failure function. Week 10 installs the **weighted-graph algorithm family** and the **disjoint-set union** data structure. Dijkstra with a heap (when it is correct, when it fails on negative weights), Bellman-Ford (negative weights OK, negative-cycle detection in pass `V`), Floyd-Warshall (all-pairs, `O(V^3)`, when `V` is small). Minimum spanning trees via Prim (Dijkstra-shaped) and Kruskal (sort-and-union). Union-Find with path compression and union by rank — the near-`O(1)` reach for "number of connected components" / "account merge" / "redundant connection" / "number of islands" variants. By Sunday you can pick the right shortest-path algorithm in 30 seconds based on the constraint signal, write a heap-Dijkstra from memory in under ten minutes, and recognize a DSU problem before the word "components" appears in the prompt.*

Welcome to Week 10 of **C2 · CrunchTime — The Code** — the sixth week of Phase 2. Last week installed the prefix-tree family. This week installs the **weighted-graph family** plus the **disjoint-set union** (also called Union-Find or DSU) data structure. After this week the unweighted-BFS reach from W6 has a weighted sibling for every shape of shortest-path question, and the components-counting reflex from W7 has a near-`O(1)` data-structure backing it for the merge-heavy variants.

Weighted graphs are the highest-leverage Phase-2 topic for FAANG-tier onsites. A typical onsite loop will include one shortest-path or MST problem; the recognition step — *Dijkstra, Bellman-Ford, Floyd-Warshall, or MST?* — is what discriminates senior from junior signal. The implementations themselves are short (heap-Dijkstra is fewer than 25 lines), but choosing the wrong algorithm is unrecoverable; the interviewer is grading the Match step harder than the Implement step this week.

Union-Find sits next to the graph algorithms because it is the *other* tool you reach for when the problem says "connect," "merge," "equivalence class," "number of components after a sequence of unions." The naive components-via-BFS approach from W6 is `O(V + E)` per query; DSU with path compression and union by rank is **amortized near-`O(1)` per operation** (technically `O(alpha(n))` where `alpha` is the inverse Ackermann function — for any realistic `n`, this is below 5). On problems with many union queries (account merge, redundant connection, smallest-string-with-swaps), DSU is the asymptotic win.

By Sunday of Week 10 you will:

- **Recognize** a weighted-graph problem in 30 seconds and classify it as **Dijkstra (non-negative weights, single source)**, **Bellman-Ford (negative weights allowed, negative-cycle detection)**, **Floyd-Warshall (all-pairs, small `V`)**, **MST (Prim or Kruskal)**, or **DSU (components / merge / equivalence)**.
- **Write** a heap-based Dijkstra from memory: `heapq` priority queue of `(distance, node)` tuples, lazy deletion via the `if d > dist[node]: continue` guard, return `dist` dict.
- **Write** a Bellman-Ford in three nested loops: outer pass `V - 1` times, inner over edges; one extra pass detects negative cycles by checking for any relaxable edge.
- **Read** a Floyd-Warshall implementation and explain the three-nested-loop intuition: `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])` for each intermediate vertex `k`.
- **Write** a Kruskal MST: sort edges by weight, iterate; for each edge, union the endpoints if they are not already connected; accumulate weight.
- **Read** a Prim MST and recognize it as a Dijkstra-shaped variant that grows a tree from a start vertex by greedily picking the lightest crossing edge.
- **Write** a Union-Find class with path compression (`find` flattens the tree) and union by rank (the smaller tree is attached under the larger). Defend the amortized `O(alpha(n))` claim out loud.
- **Recognize** the DSU triggers: "number of connected components after a sequence of operations," "is this graph a tree" (`V - 1` edges and one component), "redundant connection" (LC 684), "accounts merge" (LC 721), "smallest string with swaps" (LC 1202), "number of islands II" (LC 305 — streaming variant).
- Have solved **three weighted-graph / DSU exercises** — Network Delay Time (Dijkstra), Cheapest Flights Within K Stops (Bellman-Ford or modified Dijkstra), and a DSU drill (Number of Provinces).
- Have shipped **one challenge** (Cheapest Flights — the constrained-Dijkstra) plus an optional stretch (Smallest String With Swaps — the DSU + sort composition).
- Have shipped the quiz, the homework, and the **mini-project**: one Dijkstra write-up (Network Delay Time) and one DSU write-up (Redundant Connection), fully UMPIRE-narrated.

---

## Learning objectives

By the end of this week, you will be able to:

- **Match** a shortest-path problem in 30 seconds. The signal hierarchy: are weights present (otherwise BFS from W6); are weights non-negative (otherwise Bellman-Ford); is this single-source or all-pairs (Floyd-Warshall for all-pairs with small `V`); is there a hop-count constraint (Bellman-Ford or modified Dijkstra with state `(node, hops)`).
- **Implement Dijkstra** with `heapq` as a `(distance, node)` priority queue, lazy-delete stale entries with the `if d > dist[node]: continue` guard, and defend `O((V + E) log V)` time, `O(V)` space.
- **Defend why Dijkstra fails on negative weights** with the canonical 3-vertex counter-example: `A -1-> B`, `A -2-> C`, `B -(-5)-> C`. The heap pops `(1, B)` first, settles `dist[B] = 1`, then pops `(2, C)`, settles `dist[C] = 2`. But the true distance is `1 + (-5) = -4`. The bug is that the greedy "settle once" invariant breaks when a settled node can be improved by a later, negative-weighted relaxation.
- **Implement Bellman-Ford** in `V - 1` outer passes over the edge list. Defend the bound: any shortest path has at most `V - 1` edges; one outer pass suffices for any single hop; `V - 1` passes propagate the optimum across the longest acyclic path. The `V`-th pass is the negative-cycle detector.
- **Read Floyd-Warshall** as the three-nested-loop DP: for each intermediate vertex `k`, for each `(i, j)`, relax `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`. Defend `O(V^3)` time and `O(V^2)` space; recognize that for `V <= 400` the constant is small enough that Floyd-Warshall beats running Dijkstra `V` times on graphs with non-trivial edge counts.
- **Implement Kruskal MST**: sort edges by weight, walk them in order, accept an edge iff its endpoints are in different DSU components, halt when `V - 1` edges are accepted. Defend `O(E log E)` time (the sort dominates).
- **Implement Prim MST** with a heap: start from any vertex, add all incident edges to the heap, repeatedly pop the lightest edge whose far endpoint is unvisited, mark it visited, push its outgoing edges. Defend `O(E log V)` time.
- **Implement Union-Find** as a class with `parent` and `rank` arrays. `find` recurses to the root and flattens the path on the way back; `union` attaches the lower-rank root under the higher-rank root, breaking ties by incrementing rank. Defend amortized `O(alpha(n))` per operation.
- **Recognize the DSU triggers** in problem prompts: "merge," "connected components," "is this a tree," "redundant," "accounts," "equivalent," "swap any two indices." The discriminator vs. graph BFS is that DSU is preferable when (a) the union queries are *streaming* (you do not have all edges up front), or (b) you want amortized near-`O(1)` per query rather than `O(V + E)` per components-recount.

---

## Prerequisites

- **Weeks 1-9 complete.** You have shipped UMPIRE write-ups for the BFS pair (W6) and the heap pair (W8). You can write a `heapq`-based priority queue in under five minutes without looking at the docs.
- **Comfortable with the W6 BFS template.** Weighted Dijkstra is "BFS but the queue is a heap and edges have weights." If the BFS template still feels uncertain, re-walk W6 §3 before starting this week.
- **Comfortable with the W8 `heapq` idioms.** Specifically the `heappush((distance, node))` tuple pattern and the "lazy delete" idiom (push duplicates; ignore stale ones on pop). Both are reused verbatim in Dijkstra and Prim.
- **Comfortable with adjacency-list representation.** `graph: Dict[int, List[Tuple[int, int]]]` — `graph[u] = [(v, w), ...]` is the canonical form. Variants: `graph[u] = [(v, w), ...]` for directed; `graph[u] = [(v, w), ...]` plus a symmetric `graph[v].append((u, w))` for undirected. Mixing these up is the most common Match-step bug.
- **Comfortable with the difference between expected and worst-case complexity.** `heapq` operations are `O(log n)` worst-case. Hash-map operations are `O(1)` expected. DSU operations are `O(alpha(n))` *amortized* — a single operation may be `O(log n)` worst-case, but a sequence of `n` operations averages out to near-`O(1)` per operation.

---

## Topics covered

- **Dijkstra's algorithm** — heap-based single-source shortest paths on non-negative weights; `O((V + E) log V)` time
- **The "settle once" invariant** — why Dijkstra is greedy-correct on non-negative weights and broken on negative ones
- **Bellman-Ford** — `V - 1` passes of edge relaxation; `O(V E)` time; handles negative weights; pass `V` detects negative cycles
- **Floyd-Warshall** — three-nested-loop all-pairs DP; `O(V^3)` time, `O(V^2)` space; the right reach for small `V` or all-pairs queries
- **The shortest-path picker** — recognition flowchart from the constraint signals: weighted? non-negative? all-pairs? hop-constrained?
- **Minimum spanning trees** — the goal: a subset of `V - 1` edges connecting all vertices with minimum total weight
- **Kruskal's algorithm** — sort edges, union if not already connected; `O(E log E)` time; the cleanest illustration of DSU's leverage
- **Prim's algorithm** — Dijkstra-shaped MST that grows a tree from a start vertex; `O(E log V)` time; preferable on dense graphs
- **Union-Find / Disjoint Set Union** — the `parent[]` + `rank[]` representation; `find` with path compression; `union` by rank
- **Path compression** — the recursive flattening that gives `find` its amortized `O(alpha(n))` behavior
- **Union by rank** — the height-balancing rule that keeps the tree shallow
- **The DSU triggers** — "merge," "components after a sequence of operations," "is this a tree," "accounts merge," "redundant connection," "number of islands II" (streaming)
- **The MST disguises** — "minimum cost to connect all cities," "find the cheapest cable layout," "minimum spanning network of routers" — all MST in disguise

---

## Weekly schedule (intensive · 36h)

| Day | Focus | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project | Self-Study | Daily Total |
|-----|-------|---------:|----------:|-----------:|----------:|---------:|-------------:|-----------:|------------:|
| Monday | Dijkstra basics; heap-Dijkstra; exercise 1 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Tuesday | Bellman-Ford + Floyd-Warshall; exercise 2 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Wednesday | MST + DSU; exercise 3 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Thursday | Mini-project drafting; challenge ramp | 0h | 1h | 1h | 0.5h | 1h | 1.5h | 1h | 6h |
| Friday | Challenge (Cheapest Flights K Stops) | 0h | 0h | 2h | 0.5h | 1h | 1.5h | 1h | 6h |
| Saturday | Mini-project — Dijkstra + DSU write-ups | 0h | 0h | 0h | 0.5h | 1h | 3h | 0h | 4.5h |
| Sunday | Quiz + retro + push | 0h | 0h | 0h | 0.5h | 0h | 4h | 0h | 4.5h |
| **Total** | | **6h** | **7h** | **3h** | **3h** | **6h** | **10h** | **3.5h** | **38.5h** |

(The week budgets ~36 hours; the table sums slightly higher to absorb the Phase-2 ramp. Drop 0.5h from Self-Study if 36h is your hard cap.)

**Mastery (10h/wk):** spread the same content over three calendar weeks. The mini-project lands in calendar Week 30 of the mastery pathway. See the [mastery study plan](../study-plans/mastery-1-year.md).

---

## How to navigate this week

| File | What's inside |
|------|---------------|
| [README.md](./README.md) | This overview |
| [resources.md](./resources.md) | Free readings + Dijkstra / Bellman-Ford / DSU references + glossary additions |
| [lecture-notes/01-dijkstra-and-the-shortest-path-picker.md](./lecture-notes/01-dijkstra-and-the-shortest-path-picker.md) | Heap-Dijkstra, the "settle once" invariant, when it fails, the constraint-signal flowchart |
| [lecture-notes/02-bellman-ford-floyd-warshall-and-mst.md](./lecture-notes/02-bellman-ford-floyd-warshall-and-mst.md) | Bellman-Ford with negative-cycle detection, Floyd-Warshall, Kruskal and Prim |
| [lecture-notes/03-union-find-and-the-dsu-triggers.md](./lecture-notes/03-union-find-and-the-dsu-triggers.md) | DSU with path compression + union by rank, the amortized `alpha(n)` defense, the trigger taxonomy |
| [exercises/README.md](./exercises/README.md) | Index of the three weighted-graph / DSU exercises and SOLUTIONS |
| [exercises/exercise-01-network-delay-time.py](./exercises/exercise-01-network-delay-time.py) | LC 743 — the canonical Dijkstra warm-up |
| [exercises/exercise-02-cheapest-flights-bellman-ford.py](./exercises/exercise-02-cheapest-flights-bellman-ford.py) | LC 787 — Bellman-Ford with a hop constraint |
| [exercises/exercise-03-number-of-provinces.py](./exercises/exercise-03-number-of-provinces.py) | LC 547 — the canonical DSU warm-up |
| [exercises/SOLUTIONS.md](./exercises/SOLUTIONS.md) | Worked solutions with UMPIRE narration; consult after attempting each exercise |
| [challenges/README.md](./challenges/README.md) | Index of weekly challenges |
| [challenges/challenge-01-cheapest-flights-k-stops.md](./challenges/challenge-01-cheapest-flights-k-stops.md) | LC 787 deep-dive — Bellman-Ford vs. Dijkstra-with-state |
| [challenges/challenge-02-smallest-string-with-swaps.md](./challenges/challenge-02-smallest-string-with-swaps.md) | LC 1202 — DSU + sort composition |
| [quiz.md](./quiz.md) | 10 pattern-recognition questions |
| [homework.md](./homework.md) | Six practice problems (~5 hrs) — three Dijkstra-flavored, three DSU-flavored |
| [mini-project/README.md](./mini-project/README.md) | **One Dijkstra write-up + one DSU write-up, fully UMPIRE-narrated** — the week's deliverable |

---

## Stretch goals

- **Read the LeetCode "Shortest Path" tag** and skim 20 titles. For each, predict in 5 seconds: Dijkstra? Bellman-Ford? Floyd-Warshall? BFS-on-unweighted? Stretches the Match-step muscle most directly.
- **Re-derive heap-Dijkstra from scratch** without re-reading Lecture 1. If you cannot, you do not yet own the template. Re-read and re-derive until you can.
- **Read the Wikipedia "Disjoint-set data structure" article** end-to-end (about 25 minutes). The "Path compression" and "Union by rank" sections explain the `alpha(n)` analysis at a level appropriate for a senior interview answer. Tarjan's 1975 paper is cited; you do not need to read it.
- **Implement Prim MST with a heap** from scratch. Most learners ship Kruskal because DSU is the cleaner illustration; Prim is the better fit when the graph is dense (`E` close to `V^2`) and the heap variant amortizes well.
- **Read about Johnson's algorithm** for all-pairs shortest paths on graphs with negative edges. It runs Bellman-Ford once to reweight, then Dijkstra `V` times — `O(V^2 log V + V E)`, beats Floyd-Warshall on sparse graphs. Phase-3 stretch; the recognition cue is "all-pairs shortest paths on a sparse graph with negative edges."

---

## What "done" looks like for Week 10

A learner who has shipped Week 10 has, in their portfolio repo:

- Three UMPIRE write-ups for the exercises, with recordings >= 10 minutes.
- One UMPIRE write-up for the Cheapest Flights K Stops challenge.
- The quiz answered (score recorded).
- The homework problems committed.
- **Two mini-project write-ups** (one Dijkstra, one DSU), each with a 30-second pattern-recognition memo at the top, under `umpire-writeups/c2-week-10/mini-project/`.
- A push log showing daily commits Mon-Sun.

If all of that is present and pushed, Phase 2's sixth week is closed. You are ready for Week 11 — dynamic programming foundations.

---

## A note on the Phase 2 ramp

Week 10 is the *graph-week* sandwiched between W9 (strings) and W11 (dynamic programming). The shortest-path picker is the highest-leverage Match-step skill for the rest of Phase 2 — almost every Phase-3 onsite asks at least one weighted-graph or DSU question, and the *recognition* of which algorithm to reach for is the senior signal. Implementation fluency on heap-Dijkstra and DSU-with-path-compression is the second-most-important outcome; Bellman-Ford and Floyd-Warshall and Prim are *recognition-grade* this week (know them by name, know when to reach for them, implement them if pressed but do not optimize for speed).

If you find yourself ahead by Friday, the right stretch is **not** another exercise — it is reading the disjoint-set Wikipedia article end-to-end, or skimming a competitive-programming explanation of Johnson's algorithm. The Phase-2 retrospective at the end of Week 12 will be much easier if W10 leaves you with a sense of *which* graph algorithm to mention in interviews, not just *that* there is one.

If you find yourself *behind* by Wednesday, skip Exercise 2 (Cheapest Flights — Bellman-Ford) for now and prioritize Exercise 1 (Network Delay Time — Dijkstra) and Exercise 3 (Number of Provinces — DSU) — those are the two patterns that show up most often in Mock #2, and the Bellman-Ford variant can be picked up in 30 minutes once the Dijkstra template is fluent.

---

## Up next

[Week 11 — Dynamic Programming Foundations](../week-11-dp-foundations/) — once your three graph write-ups are pushed, your Dijkstra-vs-Bellman-Ford discriminator is articulate, and you can write a DSU with path compression from memory without consulting the lecture.

---

*If you find errors in this material, please open an issue or send a PR. Future learners will thank you.*
