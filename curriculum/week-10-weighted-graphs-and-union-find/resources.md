# Week 10 — Resources

Every resource is **free** and **publicly accessible**.

## Required reading (work it into your week)

- **`heapq` — Python docs**: <https://docs.python.org/3/library/heapq.html> — re-read the "Examples" and "Priority Queue Implementation Notes" sections; the lazy-delete idiom under "Priority Queue Implementation Notes" is the exact pattern Dijkstra uses to handle stale heap entries.
- **CPython `Lib/heapq.py` source**: <https://github.com/python/cpython/blob/main/Lib/heapq.py> — the docstring at the top of the file is the cleanest written explanation of the binary-heap invariant on the open web. The `heappush` and `heappop` C implementations are in `Modules/_heapqmodule.c`; the pure-Python `heapq.py` is the readable reference.
- **Dijkstra's algorithm — Wikipedia**: <https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm> — the "Pseudocode" section uses the priority-queue variant; the "Practical optimizations and infinite graphs" section addresses the lazy-delete question explicitly.
- **Bellman-Ford algorithm — Wikipedia**: <https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm> — required for Lecture 2 §2. The "Detecting and finding negative cycles" subsection is the interview-grade detail.
- **Floyd-Warshall algorithm — Wikipedia**: <https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm> — required for Lecture 2 §3. The three-nested-loop pseudocode is two lines; the loop-order invariant is the discriminating detail.
- **Minimum spanning tree — Wikipedia**: <https://en.wikipedia.org/wiki/Minimum_spanning_tree> — the "Algorithms" section has a clean compare-and-contrast of Kruskal vs. Prim.
- **Disjoint-set data structure — Wikipedia**: <https://en.wikipedia.org/wiki/Disjoint-set_data_structure> — required for Lecture 3. The "Making new sets," "Finding set representatives," and "Merging two sets" subsections are the three operations; the "Time complexity" subsection is the `alpha(n)` defense.
- **PEP 8 (recurring)**: <https://peps.python.org/pep-0008/>
- **Big-O Cheat Sheet (recurring)**: <https://www.bigocheatsheet.com/>

## On the pattern itself

The weighted-graph family appears in interview prompts under many surface forms. The recognition skill is mapping the surface form to the underlying algorithm:

- **Shortest path, single source, non-negative weights** — Dijkstra. The textbook case. `O((V + E) log V)` with a binary heap.
- **Shortest path, single source, may have negative weights** — Bellman-Ford. `O(V E)`. Also the only choice if the problem asks to *detect* a negative cycle.
- **Shortest path, all pairs, small `V`** — Floyd-Warshall. `O(V^3)`. Acceptable when `V <= 400` or so.
- **Shortest path with a hop-count constraint** — Bellman-Ford with the outer loop bounded by `K + 1`, or a modified Dijkstra with state `(node, hops)`. Lecture 2 §2 and Challenge 1.
- **Minimum cost to connect all nodes** — MST. Kruskal (DSU + sort) or Prim (Dijkstra-shaped).
- **Number of connected components** — DSU after a series of unions, or BFS/DFS from W6. DSU wins if the unions are streaming.
- **Equivalence classes / merge accounts / redundant edges** — DSU. The amortized near-`O(1)` per-operation cost is the whole point.
- **"Find," "Union," "Connected," "Group," "Merge"** — DSU triggers, almost without exception.

If a write-up mentions "non-negative weights" and "shortest path" — it is almost certainly Dijkstra. If it mentions "negative weights" or "detect a negative cycle" — it is Bellman-Ford. If it mentions "all-pairs" and `V` is bounded under a few hundred — it is Floyd-Warshall. If it mentions "minimum cost to connect" — it is MST. If it mentions "merge," "components," or "equivalent" — it is DSU.

## Free practice platforms

- **HackerRank — Graph Theory domain**: <https://www.hackerrank.com/domains/algorithms?filters%5Bsubdomains%5D%5B%5D=graph-theory>
- **CSES Problem Set — Graph Algorithms section**: <https://cses.fi/problemset/> — the canonical curated set; several problems whose intended solution is Dijkstra, Bellman-Ford, MST, or DSU.

## On the Dijkstra API specifically

The shape you should be able to write from memory in under ten minutes.

| Function | Signature | Complexity | One-liner mnemonic |
|----------|-----------|-----------:|--------------------|
| `dijkstra(graph, source)` | heap of `(dist, node)` | `O((V + E) log V)` | settle once on non-negative weights |
| `bellman_ford(edges, V, source)` | `V - 1` passes | `O(V E)` | detect negative cycles on pass `V` |
| `floyd_warshall(dist)` | three nested loops | `O(V^3)` | intermediate vertex `k` outermost |
| `kruskal(edges, V)` | sort + DSU | `O(E log E)` | accept iff endpoints in different sets |
| `prim(graph, start)` | heap of edges | `O(E log V)` | Dijkstra-shaped MST |

Three observations:

1. **`O((V + E) log V)` worst-case for Dijkstra, not expected.** The `heapq` operations are `O(log n)` worst-case; the number of operations is bounded by `V + E` (each vertex settles once; each edge causes at most one heap push). The product is the bound.
2. **Bellman-Ford is `O(V E)` always**, not just worst-case. There are `V - 1` outer passes and `E` inner relaxations per pass. There is no early-termination optimization that improves the asymptotic bound, though early-terminating when a pass makes no changes is a common practical speedup.
3. **Floyd-Warshall is `O(V^3)` regardless of edge count.** For sparse graphs running Dijkstra `V` times (`O(V (V + E) log V)`) beats it; for dense graphs Floyd-Warshall is competitive and simpler.

### The canonical heap-Dijkstra

```python
import heapq
from collections import defaultdict
from typing import Dict, List, Tuple

def dijkstra(graph: Dict[int, List[Tuple[int, int]]], source: int) -> Dict[int, float]:
    """Return shortest distances from `source` to every reachable node.

    `graph[u]` is a list of `(v, weight)` outgoing edges. Weights must be
    non-negative; the algorithm is wrong on negative weights (see Lecture 1 §4).
    """
    dist: Dict[int, float] = defaultdict(lambda: float("inf"))
    dist[source] = 0
    heap: List[Tuple[float, int]] = [(0, source)]

    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue  # stale entry from an earlier relaxation
        for neighbor, weight in graph.get(node, []):
            new_dist = d + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    return dict(dist)
```

Twenty lines including the type hints. Memorize the shape. The `if d > dist[node]: continue` guard is the lazy-delete idiom; without it, you waste work re-relaxing already-settled nodes.

## On the Union-Find API specifically

The class you should be able to write from memory in under five minutes.

| Method | Signature | Complexity | One-liner mnemonic |
|--------|-----------|-----------:|--------------------|
| `__init__(n)` | `parent = list(range(n))`; `rank = [0] * n` | `O(n)` | each node is its own parent |
| `find(x)` | recurse to root; flatten path | `O(alpha(n))` amortized | path compression on the way back |
| `union(x, y)` | find both roots; attach shorter under taller | `O(alpha(n))` amortized | union by rank breaks ties |
| `connected(x, y)` | `find(x) == find(y)` | `O(alpha(n))` amortized | two finds, one comparison |

Three observations:

1. **`O(alpha(n))` is amortized**, not worst-case. A single `find` may be `O(log n)` worst-case before path compression flattens the tree. Over a sequence of `n` operations, the amortized cost per operation is below the inverse Ackermann function — for `n < 2^65536`, `alpha(n) <= 4`. In practice you say "near-constant" out loud and "amortized inverse Ackermann" in writing.
2. **Path compression alone gives `O(log n)` amortized.** Union by rank alone gives `O(log n)` worst-case. Combining both gives `O(alpha(n))` amortized. The combined bound is Tarjan-Van Leeuwen (1984); cite by name if asked.
3. **The `parent` array is self-referential at the root.** `parent[root] == root`. Forgetting this gives the canonical bug: an infinite loop in `find` when the root is not detected.

### The canonical Union-Find

```python
from typing import List

class UnionFind:
    """DSU with path compression and union by rank."""

    def __init__(self, n: int) -> None:
        self.parent: List[int] = list(range(n))
        self.rank: List[int] = [0] * n
        self.components: int = n

    def find(self, x: int) -> int:
        """Return the root of `x`'s set; flatten the path on the way back."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Merge the sets containing `x` and `y`. Return False if already joined."""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.components -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        """Return True iff `x` and `y` are in the same set."""
        return self.find(x) == self.find(y)
```

Twenty-five lines. Memorize the shape. The `if self.rank[rx] < self.rank[ry]: rx, ry = ry, rx` swap is the union-by-rank line beginners forget; without it, the tree degenerates into a chain and `find` is `O(n)`.

## Glossary additions

- **Adjacency list** — `Dict[int, List[Tuple[int, int]]]`. The canonical representation for weighted graphs. `graph[u] = [(v, w), ...]` means "edge from `u` to `v` with weight `w`." `O(V + E)` space.
- **Adjacency matrix** — `List[List[float]]` of size `V x V`. `dist[i][j]` is the weight of the edge from `i` to `j` (or `inf` if no edge). `O(V^2)` space. Used by Floyd-Warshall.
- **Relax (verb)** — to attempt to improve a distance estimate. `relax(u, v, w)` updates `dist[v] = min(dist[v], dist[u] + w)`. Dijkstra relaxes each edge once (in expectation); Bellman-Ford relaxes every edge `V - 1` times.
- **Settle (verb)** — to commit a node's shortest-distance estimate as final. Dijkstra settles a node when it is popped from the heap with `d == dist[node]`. The "settle once" invariant is what fails on negative weights.
- **Negative cycle** — a cycle whose total edge weight is negative. Walking the cycle decreases the distance estimate without bound; no shortest path is well-defined.
- **Spanning tree** — a subgraph that touches all vertices and is itself a tree (`V - 1` edges, no cycles). Every connected graph has at least one.
- **Minimum spanning tree (MST)** — a spanning tree with minimum total edge weight. Not necessarily unique.
- **Cut** — a partition of the vertices into two non-empty sets. The "crossing edges" are those with one endpoint in each. The MST cut property: the lightest crossing edge of any cut is in some MST.
- **Disjoint Set Union (DSU)** — the Union-Find data structure. `parent[]` array; `find` to query; `union` to merge.
- **Path compression** — the optimization in `find` that re-points every node on the find path directly to the root. Amortizes the per-`find` cost.
- **Union by rank** — the optimization in `union` that attaches the lower-rank tree under the higher-rank tree. Keeps the tree shallow.
- **Inverse Ackermann function `alpha(n)`** — grows so slowly that `alpha(n) <= 4` for any `n` representable on real computers. The amortized bound on path-compressed, union-by-rank DSU operations.

## Cheatsheet — the shortest-path picker

A short decision flowchart you should be able to walk in 30 seconds.

```
Is the graph weighted?
  No  -> BFS (Week 6)
  Yes -> next question.

Are the weights non-negative?
  Yes -> Dijkstra (heap-based, single source).
  No  -> next question.

Do you need single-source or all-pairs?
  Single source -> Bellman-Ford (V - 1 passes; pass V detects negative cycle).
  All pairs     -> next question.

Is V small (say, <= 400)?
  Yes -> Floyd-Warshall (V^3, V^2 space; the simplest all-pairs algorithm).
  No  -> Johnson's algorithm (Phase-3 stretch). Reweight via Bellman-Ford
         once, then run Dijkstra V times. O(V^2 log V + V E).

Is there a hop-count constraint (at most K stops)?
  -> Bellman-Ford with the outer loop bounded by K + 1, or a modified
     Dijkstra with state (node, hops_used) in the heap.

Are you asked to "connect all nodes" or "find the minimum spanning network"?
  -> MST. Kruskal (sort edges + DSU) or Prim (Dijkstra-shaped).

Are you asked to "merge," "find components after operations," or
"determine equivalence classes"?
  -> Union-Find (DSU) with path compression and union by rank.
```

Read aloud; should hit 25-30 seconds. The order matters — the questions narrow the algorithm choice in the same order they would surface in an interview prompt.
