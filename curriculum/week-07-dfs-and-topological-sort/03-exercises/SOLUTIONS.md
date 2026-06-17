# Week 7 — Worked Solutions

Three worked solutions, each with UMPIRE narration. **Attempt every exercise on your own first.** If you read this file before drafting your own, you forfeit the recognition rep — and recognition is what Phase 2 is grading.

The solutions below are written in the same voice you should be using in your portfolio write-ups. Read them as templates, not as the answer.

---

## Solution 1 — Number of Provinces (LC 547)

### Understand

We are given an `n × n` symmetric binary matrix where `is_connected[i][j] == 1` means city `i` and city `j` are directly connected. The diagonal is 1 (every city is connected to itself). We must return the number of *provinces* — maximal groups of directly-or-indirectly connected cities.

Confirm: the matrix encodes an undirected graph as an adjacency matrix. Connected components in an undirected graph are an exact reframe.

Hand-walk `[[1,1,0],[1,1,0],[0,0,1]]`: cities 0 and 1 are connected; city 2 is alone. Two provinces.

### Match

DFS-for-connectivity on an adjacency matrix. The 30-second memo:

> *Graph-DFS on an adjacency matrix. Nodes are cities (indices `0..n-1`); edges are matrix `1`-entries off the diagonal. The answer counts the number of times we start a fresh DFS from an unvisited city — each fresh start covers exactly one province. Why recursive DFS: `n ≤ 200`, well below Python's 1000-frame recursion limit. Why not BFS: same asymptotic; DFS is shorter to write. Why not union-find: `O(n² × α(n))` is no better than `O(n²)`; DFS has the cleaner correctness story.*

### Plan

1. Initialize `visited: set[int] = set()` and `provinces = 0`.
2. Outer loop `for i in range(n)`. If `i in visited`, skip. Otherwise increment `provinces` and run `dfs(i)`.
3. `dfs(node)`: add `node` to `visited`; for each `nbr` in `0..n-1`, if `is_connected[node][nbr] == 1` and `nbr not in visited`, recurse on `nbr`.
4. Return `provinces`.

### Implement

```python
from typing import List


def find_circle_num(is_connected: List[List[int]]) -> int:
    n = len(is_connected)
    visited: set[int] = set()
    provinces = 0

    def dfs(node: int) -> None:
        visited.add(node)
        for nbr in range(n):
            if is_connected[node][nbr] == 1 and nbr not in visited:
                dfs(nbr)

    for i in range(n):
        if i not in visited:
            provinces += 1
            dfs(i)
    return provinces
```

### Review

Trace 1 — `[[1,1,0],[1,1,0],[0,0,1]]`. i=0: not visited → provinces=1; dfs(0). visited={0}; col=0 (self, visited), col=1 (connected, unvisited) → dfs(1). visited={0,1}; col=0 (visited), col=1 (visited), col=2 not connected. Return. Return. i=1: visited; skip. i=2: not visited → provinces=2; dfs(2). visited={0,1,2}; no new neighbors. Return. Loop done. Return 2. ✓

Trace 2 — `[[1]]`. i=0: not visited → provinces=1; dfs(0). visited={0}. Return. Return 1. ✓

Common bug caught in Review: forgetting `is_connected[node][nbr] == 1` and accidentally treating *every* column index as a neighbor. The matrix's 0/1 values are the edges; the matrix indices are the nodes.

### Evaluate

> **Time `O(n²)`**: the adjacency matrix has `n²` entries; across all DFS calls, every cell is examined exactly once. The outer loop is `O(n)`; the DFS bodies together iterate every matrix cell once.
>
> **Space `O(n)`**: visited set holds up to `n` cities; the recursion stack holds up to `n` frames in the pathological case of a single chain.
>
> **Tradeoff vs BFS**: same asymptotic; DFS is structurally shorter. Tradeoff vs union-find: `O(n² × α(n))` is asymptotically the same; DFS has a cleaner correctness story. Best case `O(n²)` (mandatory matrix read); worst case `O(n²)`. No asymptotic improvement available.

---

## Solution 2 — Has Path (LC 1971)

### Understand

Given `n` vertices and a list of undirected edges, plus a `source` and `destination`, return `True` if there is a path from `source` to `destination`. The graph has no self-loops and no duplicate edges. `n` can be up to `2 × 10⁵`.

The phrase "bi-directional" is undirected — each edge connects two vertices in both directions.

Hand-walk:

- `n=3`, edges `[[0,1],[1,2],[2,0]]`, source 0, dest 2. A triangle; path exists. → `True`.
- `n=6`, edges `[[0,1],[0,2],[3,5],[5,4],[4,3]]`, source 0, dest 5. Two components: `{0,1,2}` and `{3,4,5}`. → `False`.

### Match

Iterative DFS with an explicit stack on an undirected graph. The 30-second memo:

> *Path existence on an undirected graph — iterative DFS. Sub-shape: build an adjacency list from the edge list (defaultdict + for loop). Visited is a `set[int]`. Why iterative: `n` can reach `2 × 10⁵`, so a chain-shaped adversarial input would blow Python's 1000-frame recursion limit. Why DFS: same asymptotic as BFS; DFS suffices for "any path" and is shorter to write. Why not union-find: works equally well; DFS exercises the iterative-stack technique this week is grading.*

### Plan

1. Build adjacency list.
2. Handle the trivial case `source == destination` → return `True`.
3. Initialize `stack = [source]`, `visited: set[int] = set()`.
4. Loop: pop `node`. If `node in visited`, continue. Add to `visited`. If `node == destination`, return `True`. Push unvisited neighbors.
5. After loop, return `False`.

### Implement

```python
from collections import defaultdict
from typing import Dict, List


def valid_path(n: int, edges: List[List[int]], source: int, destination: int) -> bool:
    if source == destination:
        return True
    adj: Dict[int, List[int]] = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    stack: List[int] = [source]
    visited: set[int] = set()
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        if node == destination:
            return True
        for nbr in adj[node]:
            if nbr not in visited:
                stack.append(nbr)
    return False
```

### Review

Trace 1 — `n=3`, triangle, source=0, dest=2. adj: `{0:[1,2], 1:[0,2], 2:[1,0]}`. stack=[0]. Pop 0; mark; not dest. Push 2, then 1 (unvisited). stack=[2,1]. Pop 1; mark; not dest. Push 2 (unvisited — but already in stack from earlier). Wait: we pushed 2 from node 0, then we push 2 again from node 1. The stack now has [2, 2]. Pop 2; mark; is dest → return `True`. ✓ (The duplicate `2` on the stack is harmless — when we pop it again, the pop-time visited check filters it.)

Trace 2 — `n=6`, two components, source=0, dest=5. adj: 0↔1, 0↔2, 3↔5, 5↔4, 4↔3. stack=[0]. Pop 0; mark; not dest. Push 2, 1. stack=[2,1]. Pop 1; mark; not dest. Push 0 (visited, skip-on-push). stack=[2]. Pop 2; mark; not dest. Push 0 (visited). stack=[]. Loop exits. Return `False`. ✓

Trace 3 — `source == destination`. Trivial early return. ✓

Trace 4 — 2000-node chain. The recursive DFS would have crashed; iterative DFS handles it cleanly because the stack lives on the heap. ✓

Common bugs caught in Review:

- Using `list.pop(0)` (BFS, not DFS, and quadratic). Use `stack.pop()`.
- Forgetting the pop-time visited check (a node can be on the stack multiple times from different predecessors).
- Recursive DFS without `setrecursionlimit` (crashes on chain-shaped inputs at `n > 1000`).

### Evaluate

> **Time `O(V + E)`**: every vertex is popped at most a few times (each pop after the first is filtered as visited; the count is bounded by the in-degree of the vertex); every edge is examined at most twice (once from each endpoint).
>
> **Space `O(V + E)`**: adjacency list is `O(V + E)`; visited set is `O(V)`; stack is `O(V)` worst case.
>
> **Tradeoff vs BFS**: same complexity; DFS is shorter for "any path." Tradeoff vs recursive DFS: same asymptotic but avoids Python's 1000-frame recursion limit for `V > 10³`. Tradeoff vs union-find: `O((V + E) × α(V))`; union-find is preferred for streaming-edge problems.

---

## Solution 3 — Course Schedule II (LC 210)

### Understand

`num_courses` courses labeled `0..num_courses-1`. Each `[a, b]` in `prerequisites` means "b must be taken before a." Return *any* valid topological order; return `[]` if the prerequisite graph has a cycle.

The graph model: edge `b → a` for `[a, b]`. The in-degree of `a` counts its prerequisites.

Hand-walk: `num_courses=4`, `prerequisites=[[1,0],[2,0],[3,1],[3,2]]`. Graph: `0→1`, `0→2`, `1→3`, `2→3`. Valid orders: `[0,1,2,3]`, `[0,2,1,3]`. Either is acceptable.

### Match

Topological sort via Kahn's algorithm. The 30-second memo:

> *Topological sort on a directed graph. Two algorithms: Kahn's (BFS-shaped, iterative, in-degree array) and DFS post-order (recursive, three-color invariant). I choose **Kahn** because it is iterative — no recursion-limit risk — and the in-degree array is a clean inspectable invariant. Cycle detection by exhaustion: if `len(order) != num_courses`, the unprocessed nodes form a cycle. The graph: edge `b → a` for `[a, b]`. Why not DFS post-order: works equally well; Kahn is the iterative default. Why not naive permutation search: `O(V!)` — wildly infeasible.*

### Plan

1. Build adjacency list `adj` and `in_degree` array.
2. Seed queue with every course of in-degree zero.
3. While queue: pop, append to order, decrement out-neighbor in-degrees, queue any that drop to zero.
4. If `len(order) != num_courses`, return `[]` (cycle); else return `order`.

### Implement

```python
from collections import defaultdict, deque
from typing import Dict, List


def find_order(num_courses: int, prerequisites: List[List[int]]) -> List[int]:
    adj: Dict[int, List[int]] = defaultdict(list)
    in_degree: List[int] = [0] * num_courses
    for a, b in prerequisites:
        adj[b].append(a)
        in_degree[a] += 1
    queue: deque[int] = deque(c for c in range(num_courses) if in_degree[c] == 0)
    order: List[int] = []
    while queue:
        c = queue.popleft()
        order.append(c)
        for nxt in adj[c]:
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                queue.append(nxt)
    return order if len(order) == num_courses else []
```

### Review

Trace 1 — `num_courses=2, prerequisites=[[1,0]]`. adj={0:[1]}, in_degree=[0,1]. Initial queue=[0]. Pop 0 → order=[0]. Decrement in_degree[1]→0; queue=[1]. Pop 1 → order=[0,1]. Queue empty. len(order)==2 → return [0,1]. ✓

Trace 2 — `num_courses=4, prerequisites=[[1,0],[2,0],[3,1],[3,2]]`. adj={0:[1,2], 1:[3], 2:[3]}, in_degree=[0,1,1,2]. Initial queue=[0]. Pop 0; order=[0]; in_degree[1]→0 (queue 1); in_degree[2]→0 (queue 2). Queue=[1,2]. Pop 1; order=[0,1]; in_degree[3]→1. Pop 2; order=[0,1,2]; in_degree[3]→0 (queue 3). Pop 3; order=[0,1,2,3]. Return. ✓

Trace 3 — `num_courses=2, prerequisites=[[0,1],[1,0]]`. adj={0:[1], 1:[0]}, in_degree=[1,1]. Initial queue is empty (no zero in-degree). Loop skipped. len(order)=0 ≠ 2 → return []. ✓ (Cycle correctly detected.)

Common bugs caught in Review:

- Reversing the edge direction. `[a, b]` means "b before a" → edge `b → a`, not `a → b`. Read the prompt twice.
- Using `queue.pop(0)` (quadratic). Use `deque.popleft()`.
- Forgetting the cycle check `len(order) != num_courses`. Without it, you return a partial order that omits the cyclic nodes — wrong answer on cyclic inputs.

### Evaluate

> **Time `O(V + E)`**: building the adjacency list and in-degree array is `O(V + E)`; the queue loop visits each node once and each edge's target once.
>
> **Space `O(V + E)`**: adjacency list plus in-degree array plus queue.
>
> **Tradeoff vs DFS post-order**: same asymptotic; Kahn is iterative (no recursion-limit risk for `V > 10³`); naturally extends to "enumerate all valid topological orders" via backtracking on choice of zero-in-degree node. DFS post-order is cleaner if you need SCCs as a follow-up. Best/avg/worst all `O(V + E)`.

---

## A note on the difference from BFS

The Kahn template *looks* like BFS — `deque`, `popleft`, level-style outer loop — but it is *not* a shortest-path algorithm. Kahn does not produce a level-by-level traversal; it produces a topological order. The queue is processing "nodes whose prerequisites have all been processed," which is a fundamentally different invariant from BFS's "nodes at the current distance from the source."

The senior signal in interview is recognizing that Kahn is *structurally BFS-shaped but semantically topological*. Saying *"this is Kahn's algorithm — a BFS-shaped topological sort, not a shortest-path BFS"* is the cadence interviewers reward.

---

## Cross-references to the lectures

- Exercise 1 → Lecture 1 (recursive DFS), §7 (worked example).
- Exercise 2 → Lecture 2 (iterative DFS), §2 (canonical template) and §7 (worked example).
- Exercise 3 → Lecture 3 (topological sort), §4 (Kahn) and §6 (worked example).

After all three exercises pass, attempt the [challenge](../04-challenges/challenge-01-critical-connections.md) — Critical Connections via Tarjan's bridges, the canonical hard DFS application.
