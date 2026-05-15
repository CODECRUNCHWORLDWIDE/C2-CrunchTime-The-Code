# Week 10 — Worked Solutions

Three worked solutions, each with UMPIRE narration. **Attempt every exercise on your own first.** If you read this file before drafting your own, you forfeit the recognition rep — and recognition is what Phase 2 is grading.

The solutions below are written in the same voice you should be using in your portfolio write-ups. Read them as templates, not as the answer.

---

## Solution 1 — Network Delay Time (LC 743)

### Understand

We have a directed weighted graph; we send a signal from node `k`; we return the time at which the *last* node receives it. The "last node" is the one with the largest shortest-distance from `k`. If any node is unreachable, return `-1`.

Hand-walk on the LC 743 example 1:

```
graph:
  2 -> 1 (weight 1)
  2 -> 3 (weight 1)
  3 -> 4 (weight 1)
source: k = 2

Dijkstra from 2:
  heap: [(0, 2)]
  pop (0, 2); dist = {2: 0}; push (1, 1), (1, 3)
  pop (1, 1); dist = {2: 0, 1: 1}; no outgoing
  pop (1, 3); dist = {2: 0, 1: 1, 3: 1}; push (2, 4)
  pop (2, 4); dist = {2: 0, 1: 1, 3: 1, 4: 2}; no outgoing
Result: max(dist.values()) = 2.
```

### Match

Heap-Dijkstra. The 30-second memo:

> *Single-source shortest paths on a non-negative-weight graph. That is Dijkstra, heap-based. Edge weights are non-negative (constraint `0 <= w_i <= 100`); `n <= 100` and `len(times) <= 6000`. `O((V + E) log V)` time with `heapq`; the lazy-delete guard `if d > dist[node]: continue` skips stale heap entries. Why not BFS: weights are non-uniform. Why not Bellman-Ford: weights are non-negative; Dijkstra is faster.*

### Plan

1. Build adjacency list `graph: Dict[int, List[Tuple[int, int]]]` from `times`.
2. Initialize `dist: Dict[int, float]` as a defaultdict with `inf` default; set `dist[k] = 0`.
3. Initialize heap `[(0, k)]`.
4. While heap: pop; lazy-delete guard; relax outgoing edges; push improvements.
5. Return `max(dist.values())` if `len(dist) == n`, else `-1`.

### Implement

```python
from __future__ import annotations

import heapq
from collections import defaultdict
from typing import Dict, List, Tuple


def network_delay_time(times: List[List[int]], n: int, k: int) -> int:
    """Return min time for a signal from `k` to reach all `n` nodes, or -1."""
    graph: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    dist: Dict[int, float] = defaultdict(lambda: float("inf"))
    dist[k] = 0
    heap: List[Tuple[float, int]] = [(0.0, k)]

    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        for neighbor, weight in graph.get(node, []):
            new_dist = d + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    if len(dist) < n:
        return -1
    return int(max(dist.values()))
```

### Review

Trace on the LC 743 example: matches the hand-walk above. Edge case — `times = []` and `n = 1`: `dist = {1: 0}`, `len(dist) == 1 == n`, return `0`. Edge case — source isolated from `n - 1` other nodes: `len(dist) < n`, return `-1`.

The two discriminators against common bugs (Lecture 1 §8):

- The **lazy-delete guard** (`if d > dist[node]: continue`) prevents re-relaxing already-settled nodes. Without it, the algorithm still works but does `O(E)` extra heap pops in pathological cases — borderline TLE on LeetCode.
- The **`defaultdict(lambda: float("inf"))`** form means we never need explicit "if `node` not in `dist`" checks. The relaxation `if new_dist < dist[neighbor]` does the right thing for both seen and unseen neighbors.

### Evaluate

- **Time:** `O((V + E) log V)`. Each vertex is settled at most once (`V` heap pops); each edge is relaxed at most once and may push onto the heap (`E` heap pushes); each heap operation is `O(log V)`. For LC 743 constraints (`V <= 100`, `E <= 6000`), this is `~ 6100 * 7 ≈ 4 * 10^4` operations — trivially fast.
- **Space:** `O(V)` for the distance dictionary; `O(E)` worst-case for the heap (each relaxation may push a duplicate entry).
- **Trade vs Bellman-Ford:** Bellman-Ford is `O(V E)` and handles negative weights; for this problem (non-negative weights, sparse graph), Dijkstra is faster by a factor of `log V`. Mention by name; reject for speed.
- **Trade vs Floyd-Warshall:** Floyd-Warshall is `O(V^3)` and gives all-pairs shortest paths; for this single-source problem it is overkill. For the variant "minimum over all sources of the network-delay" it would be the right reach.

---

## Solution 2 — Cheapest Flights Within K Stops (LC 787)

### Understand

We have a directed weighted graph; we want the cheapest path from `src` to `dst` using at most `k` *intermediate* stops, which means at most `k + 1` edges. If no valid path exists, return `-1`.

Hand-walk on LC 787 example 1: `n = 4`, flights as given, `src = 0`, `dst = 3`, `k = 1`.

```
Initial: dist = [0, inf, inf, inf].

Pass 1 (allows 1 edge):
  prev = [0, inf, inf, inf]
  Edge (0, 1, 100): prev[0] + 100 = 100 < inf, so dist[1] = 100.
  Edge (1, 2, 100): prev[1] = inf, no update.
  Edge (2, 0, 100): prev[2] = inf, no update.
  Edge (1, 3, 600): prev[1] = inf, no update.
  Edge (2, 3, 200): prev[2] = inf, no update.
  After: dist = [0, 100, inf, inf].

Pass 2 (allows 2 edges = 1 stop):
  prev = [0, 100, inf, inf]
  Edge (0, 1, 100): no change.
  Edge (1, 2, 100): prev[1] + 100 = 200 < inf, so dist[2] = 200.
  Edge (1, 3, 600): prev[1] + 600 = 700 < inf, so dist[3] = 700.
  After: dist = [0, 100, 200, 700].

Result: dist[3] = 700.
```

The discriminating observation: in Pass 2, the edge `(2, 3, 200)` does *not* update `dist[3]` to `400` because `prev[2]` is still `inf` (the snapshot is from before Pass 2). If we used the live `dist` instead of the snapshot, we would update `dist[3]` to `400`, which corresponds to a 3-edge path `0 -> 1 -> 2 -> 3` exceeding the 2-edge budget.

### Match

Bellman-Ford bounded by `K + 1` passes with the **snapshot idiom**. The 30-second memo:

> *Single-source shortest path with a hop-count constraint. Bellman-Ford bounded by `K + 1` outer passes, with each pass snapshotting `dist` before relaxing. The snapshot is non-negotiable: without it, a single pass can chain multiple just-updated values within itself and exceed the hop budget. Time `O(K * E)`; space `O(V)`. Why not vanilla Dijkstra: settles a node at its overall-cheapest distance, ignoring the hop budget. Why not unconstrained Bellman-Ford: `V - 1` passes overshoot the `K + 1` bound.*

### Plan

1. Initialize `dist = [inf] * n`; set `dist[src] = 0`.
2. Loop `k + 1` times:
   a. `prev = dist[:]` (snapshot).
   b. For each `(u, v, w)` in `flights`: if `prev[u] + w < dist[v]`, set `dist[v] = prev[u] + w`.
3. Return `int(dist[dst])` if `dist[dst] != inf`, else `-1`.

### Implement

```python
from __future__ import annotations

from typing import List


def find_cheapest_price(
    n: int, flights: List[List[int]], src: int, dst: int, k: int
) -> int:
    """Cheapest fare from `src` to `dst` using at most `k` intermediate stops."""
    dist: List[float] = [float("inf")] * n
    dist[src] = 0.0

    for _ in range(k + 1):
        prev = dist[:]
        for u, v, w in flights:
            if prev[u] + w < dist[v]:
                dist[v] = prev[u] + w

    return int(dist[dst]) if dist[dst] != float("inf") else -1
```

Eighteen lines including imports and docstring. The structure mirrors Lecture 2 §2 exactly.

### Review

Trace example 1 above. Edge case — example 3 (`k = 0`): only Pass 1 runs; only direct edges from `src` can update `dist`. `dist[2] = 500` (via the direct `0 -> 2` edge); the indirect `0 -> 1 -> 2` is blocked by the hop limit. Returns `500`. Edge case — unreachable: `dist[dst]` stays `inf`; return `-1`.

The most common bug: forgetting the snapshot. Without `prev = dist[:]`, the algorithm would accept paths of length up to `(k + 1)`-times-anything within a single pass — wrong on LC 787 example 1 (would return `500` instead of `700` because Pass 1 would chain `0 -> 1 -> 3` and Pass 2 would chain `0 -> 1 -> 2 -> 3` for `400`, beating `700`).

### Evaluate

- **Time:** `O(K * E)`. For LC 787 constraints (`K <= V - 1 <= 99`, `E <= V(V-1)/2 = 4950`), worst-case is `~ 5 * 10^5` operations — trivially fast.
- **Space:** `O(V)` for `dist` and `prev`.
- **Trade vs modified Dijkstra with state `(node, hops)`:** also correct, faster on graphs where target is reachable in few hops, harder to write right under pressure. Mention by name; the Bellman-Ford form is the safer interview answer.
- **Variant:** The `K + 1` bound is the discriminator. If the problem said "at most `K` *edges*" instead of "at most `K` *stops*," the bound would be `K` passes instead of `K + 1`. Misreading this is a common LC 787 bug.

---

## Solution 3 — Number of Provinces (LC 547)

### Understand

We have an `n x n` symmetric adjacency matrix; we count the number of connected components in the corresponding undirected graph. A diagonal `1` is the trivial self-edge (every city is connected to itself); off-diagonal `1`s are real edges.

Hand-walk on LC 547 example 1:

```
Matrix:
  [1, 1, 0]
  [1, 1, 0]
  [0, 0, 1]

uf = UnionFind(3). components = 3.
Walk upper triangle: (0, 1) is 1 -> union(0, 1); components becomes 2.
                     (0, 2) is 0; skip.
                     (1, 2) is 0; skip.
Return uf.components = 2.
```

### Match

DSU components-count (Sub-shape 1 from Lecture 3 §4). The 30-second memo:

> *Components-count on an undirected graph given as an adjacency matrix. DSU with path compression and union by rank is the canonical reach; `O(n^2 alpha(n))` time, `O(n)` space. Why not BFS/DFS: also correct, comparable complexity, but the DSU is shorter for the "iterate matrix upper triangle and union" formulation. The `components` counter (decremented on each successful union) makes the final return `O(1)`.*

### Plan

1. Build `UnionFind(n)`.
2. Iterate `i` in `0..n-1`; for each `j` in `i + 1..n-1`: if `is_connected[i][j] == 1`, call `uf.union(i, j)`.
3. Return `uf.components`.

### Implement

```python
from __future__ import annotations

from typing import List


class UnionFind:
    """DSU with path compression and union by rank."""

    def __init__(self, n: int) -> None:
        self.parent: List[int] = list(range(n))
        self.rank: List[int] = [0] * n
        self.components: int = n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
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


def find_circle_num(is_connected: List[List[int]]) -> int:
    """Return the number of provinces in `is_connected`."""
    n = len(is_connected)
    uf = UnionFind(n)
    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j] == 1:
                uf.union(i, j)
    return uf.components
```

Thirty-five lines. The `UnionFind` class is reused verbatim across Week 10 and Phase 2 generally; commit it to the portfolio as a stand-alone module.

### Review

Trace example 1: matches the hand-walk above. Edge case — single city (`n = 1`, matrix `[[1]]`): `uf.components` starts at `1`; no unions; return `1`. Edge case — all-isolated (`n = 4`, identity matrix): `uf.components` stays at `4`; return `4`. Edge case — all-connected (`n = 3`, all-ones matrix): three unions, only two are successful (the third would be a no-op since all are already in the same set); `components` decremented twice; return `1`.

The most common bug: walking the *full* matrix instead of the upper triangle. The diagonal entries are `1`s (`is_connected[i][i] == 1`) — calling `union(i, i)` on these is a no-op (`uf.union` returns `False` on equal arguments), so the bug is invisible; but the lower-triangle entries are duplicates of the upper-triangle entries, so walking them doubles the work without changing the answer. Walking `j > i` is the discipline.

### Evaluate

- **Time:** `O(n^2 alpha(n))`. The matrix walk is `O(n^2 / 2) = O(n^2)`; each cell triggers at most one `union`, which is amortized `O(alpha(n))`. The product is the bound. For `n <= 200`, that is `~ 2 * 10^4 * 4 ≈ 8 * 10^4` operations — trivially fast.
- **Space:** `O(n)` for the `parent` and `rank` arrays.
- **Trade vs BFS/DFS:** BFS from each unvisited vertex is `O(V + E)`. For an `n x n` adjacency matrix, `E` is up to `n^2`, so BFS is `O(n^2)`. Same asymptotic; DSU is slightly shorter to write. The discriminator is *streaming* — if the unions arrived one at a time (LC 305 — Number of Islands II), DSU is the *only* clean choice; BFS would need re-running on the full graph after each addition. Mention this in Evaluate.
- **Variant:** The "components after a sequence of operations" generalization is the streaming variant. Same template; report `uf.components` after each operation. Phase-2 stretch but the template is identical.

---

## Closing notes

Three observations across the three solutions:

1. **The recognition step is the discriminator.** Each problem could have been solved by 2-3 different algorithms; the choice is the senior signal. Defending why Dijkstra, why Bellman-Ford, why DSU is more important than the implementation itself.

2. **The lazy-delete idiom and the snapshot idiom are non-obvious.** Both are easy to omit; both produce subtly wrong (slow or incorrect) results. Memorize them.

3. **DSU with path compression and union by rank is twenty lines.** You should be able to write it from memory in under five minutes; commit it as a stand-alone module in your portfolio and reuse across W10 and the rest of Phase 2.

When done, the [homework](../homework.md) is next.
