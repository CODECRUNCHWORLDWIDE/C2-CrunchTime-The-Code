# Challenge 1 — Critical Connections in a Network (LeetCode 1192)

> **Pattern:** DFS post-order with Tarjan's low-link; bridge detection on an undirected graph
> **Difficulty:** Hard
> **Target solve time:** 90 minutes (first time; 45 minutes on revisit)
> **Why hard:** the algorithm is short but its correctness depends on a non-obvious invariant — the *low-link* value of a node, defined as the smallest discovery time reachable from the node's subtree via at most one back-edge. Naive DFS does not detect bridges; you need the low-link computation. Most candidates have not seen this in a textbook before the interview; deriving it under pressure is the senior signal.

## Problem statement

There are `n` servers numbered from `0` to `n - 1` connected by undirected, unweighted connections forming a network where `connections[i] = [a, b]` represents a connection between servers `a` and `b`. Any server can reach other servers directly or indirectly through the network.

A **critical connection** is a connection that, if removed, will make some servers unable to reach others.

Return all critical connections in the network in any order.

Per the LC spec: `2 <= n <= 10⁵`; `n - 1 <= len(connections) <= 10⁵`. There are no repeated connections.

**Examples:**

- `n = 4`, `connections = [[0,1],[1,2],[2,0],[1,3]]` → `[[1,3]]` (removing `1—3` isolates server 3; the triangle `0—1—2—0` has no critical edges because the cycle provides redundancy.)
- `n = 2`, `connections = [[0,1]]` → `[[0,1]]` (the only edge — removing it disconnects).
- `n = 6`, `connections = [[0,1],[1,2],[2,0],[3,4],[4,5],[3,5],[1,3]]` → `[[1,3]]`.

## Acceptance criteria

- [ ] Code passes the test cases at the bottom (write your own pytest file under `exercises/` or extend the existing self-tests).
- [ ] Solution is **`O(V + E)`** time and **`O(V + E)`** space — Tarjan's low-link algorithm in a single DFS pass.
- [ ] Your UMPIRE write-up **explicitly defines low-link** in the Match section. *"`low[u]` is the smallest discovery time reachable from `u`'s DFS subtree, possibly via at most one back-edge"* — that exact sentence.
- [ ] Your write-up handles the **edge cases**: the graph is given to be connected per spec, but your trace should cover the trivial cases (`n = 2, single edge`; the triangle with no bridges; a star with all-bridges).
- [ ] Recording **≥ 45 minutes** — yes, three quarters of an hour. First time on this problem is long; that is the right shape.

## The decomposition (the interview tell)

The clean approach has one structural insight and one technique:

**Insight — Tarjan's low-link.** Two arrays per node:

- `disc[u]` = the discovery time of `u`, the iteration count when DFS first enters `u`.
- `low[u]` = the smallest discovery time reachable from `u`'s subtree via tree-edges and *at most one* back-edge.

The bridge test: edge `(u, v)` (tree-edge in the DFS, where `v` is a child of `u`) is a **bridge** if and only if `low[v] > disc[u]`. Reading: "no node in `v`'s subtree can reach back above `u` via any back-edge — `v`'s subtree is hanging off `u` by exactly the one tree-edge, so removing it disconnects."

**Technique — DFS post-order with two-array maintenance.**

```
def dfs(u, parent):
    disc[u] = low[u] = timer; timer += 1
    for v in adj[u]:
        if v == parent: continue       # the half-edge back to parent
        if disc[v] == UNVISITED:
            dfs(v, u)
            low[u] = min(low[u], low[v])     # post-order propagation
            if low[v] > disc[u]:
                bridges.append((u, v))
        else:
            low[u] = min(low[u], disc[v])    # back-edge to ancestor
```

Eight lines of body. The post-order `low[u] = min(low[u], low[v])` after the recursive call is the critical step — it bubbles up the lowest reachable discovery time from the subtree.

```
Bridge tree (with discovery times) for example 1:
                    0 [disc=0, low=0]
                    |
                    1 [disc=1, low=0]   <-- 1's subtree reaches 0 via tree-edges
                   / \
                  2   3 [disc=3, low=3]
                  [disc=2, low=0]
                  +----- back-edge to 0 (closes the triangle)

Test: for edge (1, 3): low[3]=3 > disc[1]=1 -> BRIDGE.
      for edge (0, 1): low[1]=0, but 0 is parent, not a tree-edge from 1.
                       Equivalently, low[1] = 0 = disc[0], so no bridge.
      for edge (1, 2): low[2]=0 (via back-edge to 0), 0 <= disc[1]=1, no bridge.
```

The discriminator: most candidates have not seen low-link before. The interview-tell move is **defining low-link out loud in Match** — the exact sentence in the acceptance criteria — before writing code. Naming the invariant before implementing it is the senior signal.

## UMPIRE outline

- **U:** Restate. Confirm the graph is undirected and connected by spec. Walk example 1 by hand: triangle `0-1-2` has redundancy (any one edge can be removed and the triangle still connects); the appendage `1-3` is the only single point of failure. Confirm the output may be in any order; pairs may be in any orientation.

- **M:** DFS post-order with Tarjan's low-link. The 30-second memo:
  > *"Tarjan's bridge algorithm. Maintain `disc[u]` (DFS discovery time) and `low[u]` (smallest discovery time reachable from `u`'s subtree via at most one back-edge). For tree-edge `(u, v)`: recurse; then `low[u] = min(low[u], low[v])`; if `low[v] > disc[u]`, edge is a bridge. For back-edge `(u, v)` to an already-visited non-parent: `low[u] = min(low[u], disc[v])`. Why not removing each edge and running connectivity-DFS: `O(E × (V + E))` = quadratic in edges, too slow at `E = 10⁵`. Why low-link: linear time, single DFS pass. Why DFS not BFS: post-order propagation is the natural recursion shape; BFS has no post-order."*

- **P:** Four bullets.
  1. **Build the adjacency list.** `adj: dict[int, list[int]] = defaultdict(list); for u, v in connections: adj[u].append(v); adj[v].append(u)`.
  2. **Allocate `disc` and `low` arrays.** Both `[-1] * n` (using `-1` as the unvisited sentinel).
  3. **DFS from any node (e.g., 0).** Maintain `timer` as a closure variable; on entry, set `disc[u] = low[u] = timer; timer += 1`. Iterate neighbors: skip parent; if unvisited, recurse and post-order update + bridge test; else update via back-edge.
  4. **Disconnected handling.** The spec guarantees connected, but defensively iterate over `range(n)` in case.

- **I:** Implement. The parent-pointer discipline and the timer maintenance are the most error-prone parts. Use `sys.setrecursionlimit(10**6)` because `n = 10⁵` exceeds the default 1000-frame limit.

- **R:** Trace on example 1.
  - dfs(0, -1): disc[0]=0, low[0]=0, timer=1.
  - dfs(1, 0): disc[1]=1, low[1]=1, timer=2.
  - dfs(2, 1): disc[2]=2, low[2]=2, timer=3. Neighbor 0 visited, not parent → low[2] = min(2, disc[0]=0) = 0. Neighbor 1 is parent, skip. Return.
  - Back in dfs(1, 0): low[1] = min(1, low[2]=0) = 0. Test low[2]=0 > disc[1]=1? No. Not a bridge.
  - dfs(3, 1): disc[3]=3, low[3]=3, timer=4. Neighbor 1 is parent, skip. Return.
  - Back in dfs(1, 0): low[1] = min(0, low[3]=3) = 0. Test low[3]=3 > disc[1]=1? Yes → bridge `(1, 3)`.
  - Back in dfs(0, -1): low[0] = min(0, low[1]=0) = 0. Test low[1]=0 > disc[0]=0? No. Not a bridge.
  - Result: bridges = [(1, 3)]. ✓

- **E (graded):** **Time `O(V + E)`** — single DFS pass; each node entered once; each edge examined twice. **Space `O(V + E)`** — adjacency list + disc + low + recursion stack. Tradeoff: the naive "remove each edge, check connectivity" is `O(E × (V + E))` — quadratic in edges and infeasible at `E = 10⁵`. Tarjan's algorithm is the only linear-time algorithm for bridges; the trade against alternatives is purely "implement correctly," with no asymptotic option.

## Function signature

```python
def critical_connections(n: int, connections: list[list[int]]) -> list[list[int]]:
    """Return all bridges in the undirected graph as a list of [u, v] pairs."""
    ...
```

## Test cases to verify

```python
import pytest


def normalize(edges: list[list[int]]) -> set[tuple[int, int]]:
    return {tuple(sorted(e)) for e in edges}


@pytest.mark.parametrize(
    "n, connections, expected",
    [
        (4, [[0, 1], [1, 2], [2, 0], [1, 3]], [[1, 3]]),
        (2, [[0, 1]], [[0, 1]]),
        (5, [[1, 0], [2, 0], [3, 2], [4, 2], [4, 3]], [[0, 1], [0, 2]]),
        (6, [[0, 1], [1, 2], [2, 0], [3, 4], [4, 5], [3, 5], [1, 3]], [[1, 3]]),
        # Star graph: every edge is a bridge.
        (5, [[0, 1], [0, 2], [0, 3], [0, 4]], [[0, 1], [0, 2], [0, 3], [0, 4]]),
        # A single triangle has no bridges.
        (3, [[0, 1], [1, 2], [2, 0]], []),
    ],
)
def test_critical_connections(n, connections, expected):
    actual = critical_connections(n, connections)
    assert normalize(actual) == normalize(expected)
```

## Common bugs you should catch in Review

- **Forgetting the parent-pointer exclusion.** When DFS descends from `u` to `v`, the very next iteration sees the back-half-edge `v → u`. Without `if v == parent: continue`, this is mistakenly treated as a back-edge and `low[v]` gets set to `disc[u]`, masking real bridges.
- **Using `low[u] = min(low[u], low[v])` for back-edges.** Back-edges go to *already visited* nodes; the correct update is `low[u] = min(low[u], disc[v])` (note `disc`, not `low`). The reason: a back-edge gives you direct reach to an ancestor's discovery time, not to whatever the ancestor's subtree has bubbled up.
- **Off-by-one on the bridge test.** The test is `low[v] > disc[u]` — strict inequality. Using `>=` would incorrectly classify every tree-edge as a bridge (because `low[v] >= disc[v] > disc[u]` for a child).
- **Recursion-limit crash on large `n`.** `sys.setrecursionlimit(10**6)` at the top is mandatory for `n = 10⁵`. Alternatively, convert to iterative DFS with state-tag — much harder to get right; not worth the time in a 90-minute window.
- **Forgetting that the graph may have parallel edges in *some* problem variants.** LC 1192 says "no repeated connections," but a more robust solution counts the *edge* not the *neighbor pair* (track edge IDs). For LC 1192 specifically the simpler parent-pointer approach is sufficient.
- **Mutating the adjacency list during iteration.** Don't. Iterate `adj[u][:]` (a copy) if you must, but the algorithm does not require mutation — only the disc/low arrays change.

## The "why `O(V + E)`?" defense

Out loud, in your Evaluate section:

> "**Why `O(V + E)` time, same space.** Tarjan's algorithm is a single DFS pass: every vertex enters DFS once (so the visited check via `disc[u] != -1` is `O(V)` aggregate), and every edge is examined at most twice (once from each endpoint). The bridge test on each tree-edge is `O(1)`. There is no asymptotic alternative — bridges *require* a global view of the graph's cycle structure, which `O(V + E)` is the proven lower bound for. The naive 'remove each edge and re-check connectivity' is `O(E × (V + E))` — quadratic in edges. The senior signal here is that the **low-link invariant is what reduces the global cycle question to a local post-order computation** — without that invariant, the algorithm is exponential."

Memorize the shape of that sentence. Saying it cleanly is the difference between "solved Critical Connections" and "demonstrated mastery of DFS post-order on a hard application."

## Why this matters

Tarjan's bridge algorithm is a representative member of a class of problems that show up regularly in real interviews:

1. **DFS post-order with a numerical invariant** — the same pattern powers Tarjan's strongly-connected-components algorithm, articulation point detection (a one-line change from bridges), the longest path in a DAG, and tree-DP problems where the answer at each node aggregates children.
2. **Low-link as an algorithmic primitive** — Tarjan's SCC, Kosaraju's SCC, biconnected components, and 2-SAT all build on low-link or its variants. Recognizing low-link as "the smallest discovery time reachable from a subtree" is a senior-level move in any graph interview.
3. **Linear-time algorithms on graph structure** — bridges, articulation points, SCCs, and topological sort are all `O(V + E)`. The pattern of "single DFS pass + post-order propagation" is the unifying technique. Master this, and the whole family becomes one algorithm with different post-order computations.

When you revisit this challenge before Mock #2, **re-derive the low-link invariant from scratch** rather than re-reading your old solution. The derivation is the skill.

## Stretch

**Articulation points.** A vertex `u` is an articulation point (cut vertex) if removing it disconnects the graph. The test is *almost* the same as bridges: for the DFS root, it is articulation iff it has more than one DFS-tree child; for non-roots, it is articulation iff some child `v` has `low[v] >= disc[u]` (note `>=`, not `>`). One-line change from the bridge code. Useful warm-up for Mock #2 if Critical Connections is the live problem.

**Tarjan's SCC algorithm.** Tarjan's strongly-connected-components algorithm uses the same low-link primitive in a single DFS pass, plus an auxiliary stack of "open SCCs." Reading the full algorithm is a 30-minute investment that pays off in any directed-graph interview. Out of scope this week; covered in C5.

**Biconnected components.** Biconnected components are maximal subgraphs where every two edges lie on a common cycle. The decomposition is computed by the same low-link DFS, plus a stack of "open biconnected components." Bonus problem: implement and test biconnected component listing on the example graphs above.

---

This concludes Challenge 1. If you have time, attempt [Challenge 2 — Alien Dictionary](./challenge-02-alien-dictionary.md) — topological sort on a derived edge set, the canonical "model the problem as a graph" stretch. Then take the [quiz](../05-quiz.md), do the [homework](../06-homework.md), then ship the [mini-project](../07-mini-project/00-overview.md) — one DFS write-up and one topological-sort write-up.
