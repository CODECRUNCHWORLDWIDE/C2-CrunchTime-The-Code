# Week 7 — Resources

Every resource is **free** and **publicly accessible**.

## Required reading (work it into your week)

- **Depth-first search — Wikipedia**: <https://en.wikipedia.org/wiki/Depth-first_search> — the canonical reference; the pseudocode in the "Pseudocode" section is the closest thing to a textbook template in free material. Read the section on "Output of a depth-first search" and the "Vertex orderings" subsection (pre-order, post-order, reverse post-order).
- **Topological sorting — Wikipedia**: <https://en.wikipedia.org/wiki/Topological_sorting> — covers both Kahn's algorithm and the DFS-based algorithm side-by-side; the pseudocode is the cleanest free reference.
- **`sys.setrecursionlimit` — Python docs**: <https://docs.python.org/3/library/sys.html#sys.setrecursionlimit> — the function you will reach for the first time you blow the default 1000-frame stack on a deep DFS. Read the "stack overflow" caveat; raising the limit is a workaround, not a fix.
- **PEP 8 (recurring)**: <https://peps.python.org/pep-0008/>
- **Big-O Cheat Sheet (recurring)**: <https://www.bigocheatsheet.com/>

## On the pattern itself

DFS is described under many names. The recognition skill is mapping the surface form to the underlying pattern:

- **Depth-first search** — the textbook name.
- **Pre-order / in-order / post-order traversal** — the three orderings DFS produces on a tree. Pre-order processes a node *before* descending; post-order processes *after*; in-order is binary-tree-specific (left, root, right).
- **Backtracking** — DFS where the visited set is replaced by an "undo" step at the end of each recursive call. Covered in Week 8.
- **Topological sort** — a linear ordering of the nodes of a DAG such that every edge goes from earlier to later in the order. Two algorithms: DFS post-order (Tarjan-style) and Kahn's BFS-shaped algorithm.
- **Tarjan's strongly-connected-components** — an `O(V + E)` algorithm built on DFS post-order plus the low-link concept. Out of scope this week; covered in C5.
- **Bridge / articulation point detection** — finding edges (bridges) or nodes (articulation points) whose removal disconnects the graph. Built on Tarjan's low-link technique. The week's challenge.

If a write-up mentions "shortest path" without "weighted," it is almost certainly BFS, not DFS. If it mentions "topological order," "prerequisites," "valid sequence," "build order," "course schedule" — it is topological sort.

## Free practice platforms

- **LeetCode — Depth-First Search tag** (free): <https://leetcode.com/tag/depth-first-search/>
- **LeetCode — Topological Sort tag** (free): <https://leetcode.com/tag/topological-sort/>
- **LeetCode — Graph tag** (free): <https://leetcode.com/tag/graph/> — DFS problems mixed with BFS and weighted-graph problems. Filter by difficulty.
- **HackerRank — Graph Theory domain**: <https://www.hackerrank.com/domains/algorithms?filters%5Bsubdomains%5D%5B%5D=graph-theory>
- **Codeforces — DFS and similar tag**: <https://codeforces.com/problemset?tags=dfs+and+similar>
- **CSES Problem Set — Graph Algorithms section**: <https://cses.fi/problemset/> — the Finnish university free problem bank; the Graph Algorithms section has both DFS and topological-sort problems.

## On topological sort specifically

The two-algorithm split is worth internalizing. Both run in `O(V + E)` time. The choice between them is on output shape and code structure.

- **GeeksforGeeks — "Topological Sorting"**: <https://www.geeksforgeeks.org/topological-sorting/> — covers the DFS-based approach with a worked example. Read it once for the post-order argument.
- **GeeksforGeeks — "Kahn's algorithm for Topological Sorting"**: <https://www.geeksforgeeks.org/kahns-algorithm-for-topological-sorting/> — covers the BFS-shaped approach with the in-degree array. Read it once for the BFS-shaped framing.
- **Competitive Programmer's Handbook (Laaksonen) — Chapter 16 ("Directed graphs")**: <https://cses.fi/book/book.pdf> — a free PDF textbook; Chapter 16 covers topological sort, cycle detection, and SCCs in clean pseudocode.

The decision rule for the week:

| Question | Algorithm |
|----------|-----------|
| Need a topological order, any one | Either; Kahn is simpler to write iteratively |
| Need to detect "is this a DAG?" with no order required | Either; the gray-set technique in DFS is the cleanest |
| Need *all* topological orders | Kahn's, with backtracking on choice of zero-in-degree node |
| Need to detect cycles in an undirected graph | DFS with parent pointer (not topo sort) |
| Need to detect cycles in a directed graph | DFS with three-color invariant |
| Need SCCs (strongly-connected components) | Tarjan's or Kosaraju's — both built on DFS post-order; out of scope |

## On the difference between BFS and DFS

The recognition skill from Week 6 — "BFS or DFS?" — is the highest-yield Match-step question for any graph problem. The fuller table this week, with the new DFS rows filled in:

| Question | BFS or DFS? |
|----------|-------------|
| Shortest path on unweighted graph? | **BFS** |
| Any path? | **DFS** (cheaper to code; same big-O) |
| All paths? | **DFS** (BFS works but uses more memory) |
| Connectivity / connected components? | Either; **DFS** if recursive is allowed |
| Cycle detection (undirected)? | **DFS** with parent-pointer technique |
| Cycle detection (directed)? | **DFS** with three-color invariant |
| Topological sort? | **DFS post-order** or **Kahn** (BFS-shaped, with in-degrees) |
| Strongly-connected components? | **DFS** (Tarjan or Kosaraju) |
| Level-order outputs? | **BFS** |
| Spread / infection / level-by-level expansion? | **BFS** (multi-source if needed) |
| Backtracking / generate all valid configurations? | **DFS** (Week 8) |

Memorize the first three rows and the topological-sort row; the rest you can derive in interview.

## Videos on the pattern (free, no signup)

- **NeetCode — "DFS Algorithm"** (YouTube — free): search "neetcode dfs"; the 10-minute walkthrough is enough.
- **NeetCode — "Course Schedule"** (YouTube — free): the canonical topological-sort problem; if you have not seen the pattern in video form, watch this before Exercise 3.
- **MIT 6.006 — Lecture on DFS** (free OCW): <https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/> — the rigorous version; the post-order topo argument is laid out cleanly with proofs.
- **MIT 6.006 — Lecture on Topological Sort and DAG Shortest Paths** (free OCW): the same course; the lecture on DAGs gives the "topo first, then relax edges in order" framing that anchors several weighted-DAG algorithms in C5.

## On cycle detection

Two distinct algorithms, depending on whether the graph is directed.

**Undirected:** a back-edge from `u` to a non-parent `v` is a cycle. The "non-parent" check is the discriminator — every edge `(u, v)` in an undirected graph corresponds to two directed edges `u → v` and `v → u`; we have to exclude the back-edge that is just the return trip.

```python
def has_cycle_undirected(adj: dict[int, list[int]]) -> bool:
    visited: set[int] = set()
    def dfs(node: int, parent: int) -> bool:
        visited.add(node)
        for nbr in adj[node]:
            if nbr not in visited:
                if dfs(nbr, node):
                    return True
            elif nbr != parent:
                return True
        return False
    for v in adj:
        if v not in visited:
            if dfs(v, -1):
                return True
    return False
```

**Directed:** the three-color invariant. White (`0`) = unvisited; gray (`1`) = on the current path; black (`2`) = finished. A directed edge to a gray node is a cycle.

```python
def has_cycle_directed(adj: dict[int, list[int]]) -> bool:
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[int, int] = {v: WHITE for v in adj}
    def dfs(node: int) -> bool:
        color[node] = GRAY
        for nbr in adj.get(node, []):
            if color[nbr] == GRAY:
                return True
            if color[nbr] == WHITE and dfs(nbr):
                return True
        color[node] = BLACK
        return False
    for v in adj:
        if color[v] == WHITE:
            if dfs(v):
                return True
    return False
```

Memorize both shapes. The undirected version uses a parent pointer; the directed version uses three colors. Confusing one for the other is the most common cycle-detection bug.

## Glossary cheat sheet

Keep this tab open. Builds on Weeks 1-6.

| Term | One-line definition |
|------|---------------------|
| **DFS** | A traversal that visits nodes in depth-first order; recursive or explicit-stack |
| **Recursion stack** | Python's call stack; default limit is 1000 frames; raise with `sys.setrecursionlimit` |
| **Visited set** | A `set[node]` recording which nodes have been entered by DFS; prevents revisiting |
| **Pre-order** | Process a node *before* descending into its children |
| **Post-order** | Process a node *after* all descendants have finished |
| **Reverse post-order** | Post-order reversed — yields a topological order on a DAG |
| **Back-edge** | An edge from a descendant to an ancestor in the DFS tree |
| **Tree-edge / forward-edge / cross-edge** | The four DFS edge classifications in a directed graph |
| **Three-color invariant** | White / gray / black DFS state for directed cycle detection |
| **DAG** | Directed acyclic graph — a directed graph with no cycles |
| **Topological order** | A linear ordering of a DAG's nodes such that every edge goes earlier-to-later |
| **Kahn's algorithm** | A BFS-shaped topological sort using in-degrees; iterative |
| **In-degree** | The number of incoming edges to a node |
| **Out-degree** | The number of outgoing edges from a node |
| **SCC** | Strongly-connected component — a maximal subgraph where every node reaches every other |
| **Bridge** | An edge in an undirected graph whose removal disconnects the graph |
| **Articulation point** | A node whose removal disconnects the graph |
| **Low-link** | Tarjan's auxiliary value: the smallest discovery time reachable from a node's subtree |

## What you will be glad you read

Two things, both short, both this week:

1. **The "Pseudocode" and "Vertex orderings" sections of the DFS Wikipedia article** — five minutes. The takeaway: pre-order, post-order, reverse post-order are three views of the same traversal.
2. **Chapter 16 of Laaksonen's CSES handbook** — twenty minutes. The cleanest pseudocode treatment of cycle detection, topo sort, and SCCs in free material.

If you read nothing else this week, read those two and skim five problem titles in the LeetCode Topological Sort tag.

---

*Broken link? Open an issue.*
