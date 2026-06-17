# Week 6 — Resources

Every resource is **free** and **publicly accessible**.

## Required reading (work it into your week)

- **Breadth-first search — Wikipedia**: <https://en.wikipedia.org/wiki/Breadth-first_search> — the canonical reference; the pseudocode in the "Pseudocode" section is the closest thing to a textbook template in free material.
- **`collections.deque` — Python docs**: <https://docs.python.org/3/library/collections.html#collections.deque> — read the table of operation complexities. `popleft()` and `append()` are both `O(1)`; that is the reason BFS uses `deque` and not `list`.
- **Big-O Cheat Sheet (recurring)**: <https://www.bigocheatsheet.com/>
- **PEP 8 (recurring)**: <https://peps.python.org/pep-0008/>

## On the pattern itself

BFS is described under many names. The recognition skill is mapping the surface form to the underlying pattern:

- **Breadth-first search** — the textbook name.
- **Level-order traversal** — the name when applied to a tree. Same algorithm; the "graph" is a tree (no cycles, but still uses the queue).
- **Flood fill** — the name when applied to a grid where every cell is visited from a single starting cell. A special case of BFS where the answer is the count of reachable cells, not a distance.
- **Multi-source BFS** — the name when the queue is seeded with multiple starts. The algorithm is identical; the seed shape is the variation.
- **0-1 BFS** — a variant for graphs with edge weights in `{0, 1}`. Uses `deque.appendleft()` for zero-cost edges. Out of scope this week; covered in C5.
- **Bidirectional BFS** — advance from both endpoints, halt when frontiers meet. The advanced-but-still-interview-relevant variant.

If a write-up mentions "Dijkstra," "A*," or "uniform-cost search" — those are different algorithms for weighted graphs. BFS works only on unweighted graphs (or equivalently, graphs where every edge has unit cost).

## Free practice platforms

- **LeetCode — Breadth-First Search tag** (free): <https://leetcode.com/tag/breadth-first-search/>
- **LeetCode — Graph tag** (free): <https://leetcode.com/tag/graph/> — BFS problems mixed with DFS and weighted-graph problems. Filter by difficulty.
- **HackerRank — Graph Theory domain**: <https://www.hackerrank.com/domains/algorithms?filters%5Bsubdomains%5D%5B%5D=graph-theory>
- **Codeforces — BFS tag**: <https://codeforces.com/problemset?tags=bfs>
- **CSES Problem Set — Graph Algorithms section**: <https://cses.fi/problemset/> — a Finnish university free problem bank; the Graph Algorithms section is the cleanest free curriculum on BFS / DFS / shortest paths.

## On grid-BFS specifically

The 2-D grid is the most common BFS surface in interviews. Two short reads, both free:

- **GeeksforGeeks — "BFS for 2D grid"**: search the phrase; multiple short articles. Pick one and skim. The vocabulary is consistent across the family.
- **Competitive Programmer's Handbook (Laaksonen) — Chapter 12 ("Graph traversal")**: <https://cses.fi/book/book.pdf> — a free PDF textbook from the CSES author. Chapter 12 covers BFS and DFS in clean pseudocode; Chapter 13 covers shortest paths. The book is free and excellent.

## On the difference between BFS and DFS

DFS is next week. The recognition skill — "BFS or DFS?" — is the highest-yield Match-step question for any graph problem. The general rule:

| Question | BFS or DFS? |
|----------|-------------|
| Shortest path? | **BFS** (on unweighted) |
| Any path? | DFS (cheaper to code; same big-O) |
| All paths? | DFS (BFS works but uses more memory) |
| Connectivity / connected components? | Either |
| Cycle detection? | **DFS** (the recursion stack makes back-edges natural) |
| Topological sort? | **DFS** (Kahn's algorithm uses BFS but with extra state) |
| Level-order outputs? | **BFS** (the levels are explicit) |
| Spread / infection / level-by-level expansion? | **BFS** (multi-source if needed) |

Memorize the first row and the last two rows; the rest you can derive in interview.

## Videos on the pattern (free, no signup)

- **NeetCode — "BFS Algorithm"** (YouTube — free): search "neetcode bfs"; the 10-minute walkthrough is enough.
- **NeetCode — "Rotting Oranges"** (YouTube — free): the canonical multi-source BFS problem; if you have not seen the pattern in video form, watch this before Drill 3.
- **MIT 6.006 — Lecture on BFS** (free OCW): the rigorous version; the proof that BFS finds shortest paths on unweighted graphs is laid out cleanly.

## On bidirectional BFS

The advanced variant covered in Lecture 2 §7. One canonical free reading:

- **GeeksforGeeks — "Bidirectional Search"**: search the phrase. The article covers the meet-in-the-middle idea, the complexity argument (`O(b^(d/2))` instead of `O(b^d)`), and the implementation skeleton.

The vocabulary item to install: **two frontiers**. Bidirectional BFS maintains two sets — `frontier_start` and `frontier_end` — and expands the smaller of the two on each iteration. Termination is when a node is in both frontiers. The interview-tell is recognizing that the source *and* target are both fully known (you cannot bidirectional-search if you do not know the target).

## Glossary cheat sheet

Keep this tab open. Builds on Weeks 1-5.

| Term | One-line definition |
|------|---------------------|
| **Graph** | A set of nodes and edges; can be directed or undirected, weighted or unweighted |
| **Adjacency list** | `dict[node, list[node]]` — the canonical edge representation for sparse graphs |
| **BFS** | A traversal that visits nodes in order of distance from the source, using a FIFO queue |
| **Queue / `deque`** | The FIFO data structure backing BFS; Python's `collections.deque` gives `O(1)` `popleft()` and `append()` |
| **Visited set** | A `set[node]` recording which nodes have been queued; prevents re-enqueuing and breaks cycles |
| **Level** | The set of nodes at the same BFS distance from the source; tracked with an outer `for _ in range(len(queue))` loop |
| **Grid-BFS** | BFS on an implicit graph where nodes are `(r, c)` cells and edges are 4- or 8-directional offsets |
| **Node-BFS** | BFS on an explicit adjacency list, or on an implicit graph where neighbors come from a `neighbors(node)` function (e.g., word ladder) |
| **Multi-source BFS** | BFS where the initial queue contains multiple seed nodes; computes minimum distance from *any* seed |
| **Bidirectional BFS** | BFS expanded from both source and target simultaneously; halts when frontiers meet |
| **Unweighted graph** | A graph where every edge has the same "cost" (typically 1); BFS finds shortest paths only on these |
| **Implicit graph** | A graph whose nodes and edges are not stored but generated on demand (e.g., chess knight moves, word transformations) |
| **State space** | The set of all reachable nodes; for grid-BFS this is `R * C`; for word ladder it is bounded by the dictionary size |

## What you will be glad you read

Two things, both short, both this week:

1. **The "Pseudocode" section of the BFS Wikipedia article** — three minutes. The takeaway: the canonical template is six lines.
2. **Chapter 12 of Laaksonen's CSES handbook** — twenty minutes. The cleanest pseudocode treatment of BFS and DFS side-by-side in free material.

If you read nothing else this week, read those two and skim five problem titles in the LeetCode BFS tag.

---

*Broken link? Open an issue.*
