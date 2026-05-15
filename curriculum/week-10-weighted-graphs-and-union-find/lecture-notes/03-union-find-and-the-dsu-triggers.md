# Lecture 3 — Union-Find and the DSU Triggers

> **Duration:** ~2 hours.
> **Outcome:** You can write the canonical Union-Find class with path compression and union by rank from memory in under five minutes, defend the amortized `O(alpha(n))` per-operation bound out loud, recognize a DSU problem from the prompt's vocabulary alone, and articulate the four canonical sub-shapes (components-count, redundant-edge, account-merge, streaming-islands).

Lectures 1 and 2 installed the weighted-graph algorithms. This lecture installs the **Union-Find** data structure — also called the **disjoint-set union (DSU)** or, in some older literature, the **disjoint-set forest**. It is a small data structure (twenty-five lines of Python with the two optimizations) and a sharp recognition cue. After this lecture, when the prompt says "merge," "connect," "equivalent," "group," or "components-after-operations," you will reach for DSU before reading the rest of the problem.

The interview register of DSU is unusual. It is **not** typically asked as a from-scratch implementation under pressure — most candidates carry a DSU snippet in their portfolio and adapt it on demand. What *is* asked is the **recognition** ("this is a DSU problem") and the **amortized-complexity defense** ("path compression plus union by rank gives `O(alpha(n))` per operation, where `alpha` is the inverse Ackermann function — below 5 for any realistic input"). Owning both is the senior signal.

---

## 1. What Union-Find solves

The data structure maintains a collection of **disjoint sets** of elements and supports two operations:

- **`find(x)`** — return a canonical representative (the "root") of the set containing `x`. Two elements are in the same set iff `find(x) == find(y)`.
- **`union(x, y)`** — merge the sets containing `x` and `y` into a single set.

The naive implementation (linked-list per set; `find` walks to the head; `union` concatenates) gives `O(n)` per operation. With the two optimizations covered in this lecture — **path compression** in `find` and **union by rank** in `union` — the amortized per-operation cost drops to `O(alpha(n))`, where `alpha` is the inverse Ackermann function. For any `n` representable on real computers, `alpha(n) <= 4`. In practice you say "constant" out loud and "amortized inverse Ackermann" in writing.

Three observations:

1. **DSU does not store the sets explicitly.** You cannot ask "what are the elements of the set containing `x`" in less than `O(n)` — DSU is optimized for `find` and `union`, not for enumeration. If you need to enumerate set contents, group by `find(x)` for every `x` in `O(n alpha(n))` total.
2. **The "set representative" is an implementation detail.** It is just the root of the tree. It is not the smallest element, not the first inserted, not anything meaningful — only the comparator for "same set?" matters.
3. **The structure is incremental.** You can `union` after construction; you cannot easily "un-merge" or split a set. For problems that require both unions and splits, DSU is not the right tool — see the **link-cut tree** (Phase 3 stretch).

---

## 2. The naive implementation (and why it loses)

The textbook naive: each element points to its parent; the root points to itself; `find` walks parent pointers to the root.

```python
class NaiveUF:
    def __init__(self, n: int) -> None:
        self.parent: List[int] = list(range(n))

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> None:
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            self.parent[rx] = ry
```

Twelve lines. Correct. Worst-case `O(n)` per operation: if every `union` attaches the previous root under a new one, the tree degenerates into a chain of length `n`, and `find` walks the chain end-to-end.

The pathological input: `union(0, 1); union(1, 2); union(2, 3); ...; union(n-2, n-1)` — every union extends a chain. After `n - 1` unions, the tree is a path of length `n`, and `find(0)` is `O(n)`.

Two optimizations fix this:

1. **Union by rank** — attach the shorter tree under the taller. Keeps the tree shallow. Without path compression, this alone gives `O(log n)` worst-case `find`.
2. **Path compression** — during `find`, repoint every traversed node directly to the root. Amortizes the cost of future `find`s. Without union by rank, this alone gives `O(log n)` amortized `find`.

**Both together** give the celebrated `O(alpha(n))` amortized per operation. The combined bound is Tarjan-Van Leeuwen (1984).

---

## 3. The canonical Union-Find

```python
from __future__ import annotations

from typing import List


class UnionFind:
    """DSU with path compression and union by rank.

    Path compression: `find` re-points every traversed node directly to
    the root on the way back. This flattens the tree and amortizes the
    cost of future `find` calls.

    Union by rank: `union` attaches the lower-rank tree under the
    higher-rank tree, breaking ties by incrementing the rank of the
    winner. This keeps the tree shallow before compression kicks in.

    Amortized per-operation cost: `O(alpha(n))`, where `alpha` is the
    inverse Ackermann function. For any realistic `n`, `alpha(n) <= 4`.
    """

    def __init__(self, n: int) -> None:
        """Initialize a DSU with `n` singletons."""
        self.parent: List[int] = list(range(n))
        self.rank: List[int] = [0] * n
        self.components: int = n  # number of disjoint sets

    def find(self, x: int) -> int:
        """Return the root of `x`'s set; compress the path on the way back."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Merge `x`'s set with `y`'s. Return True iff a merge happened.

        Returns False if `x` and `y` were already in the same set.
        """
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        # Union by rank: attach the lower-rank root under the higher-rank root.
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

Forty lines with the docstrings; twenty without. Memorize the shape. Three lines deserve close attention:

- **`self.parent[x] = self.find(self.parent[x])`**. The recursive path-compression form. On the way back from the recursive call, we re-point `parent[x]` to the *final* root. The next `find(x)` walks one step to the root. This is the recursive variant; an iterative version with a two-pass walk exists and is preferred in languages without tail-call elimination (Python's recursion limit is the practical constraint — for `n > 10^4`, prefer the iterative form).

- **`if self.rank[rx] < self.rank[ry]: rx, ry = ry, rx`**. The union-by-rank swap. After the swap, `rx` is the higher-rank (or equal-rank) root, and `ry` is the lower-rank root. We then attach `ry` under `rx`.

- **`if self.rank[rx] == self.rank[ry]: self.rank[rx] += 1`**. Rank only increments on equal-rank merges. The rank of a tree is its height *upper bound* — under union by rank, the actual height is `<= rank`. Path compression makes the actual height much smaller than rank, but rank-based balancing keeps the worst case bounded.

The iterative variant of `find` (preferred for large `n`):

```python
def find_iterative(self, x: int) -> int:
    """Iterative path compression: two-pass walk."""
    # Pass 1: walk to the root.
    root = x
    while self.parent[root] != root:
        root = self.parent[root]
    # Pass 2: re-point every node on the walk to the root.
    while self.parent[x] != root:
        self.parent[x], x = root, self.parent[x]
    return root
```

Same asymptotic; avoids the recursion-depth limit. Use this form for `n >= 10^4`.

---

## 4. The four canonical DSU sub-shapes

DSU shows up in four recognizable sub-shapes. Recognizing the sub-shape is more useful than knowing the data structure.

### Sub-shape 1 — Components-count

The simplest. Given a list of edges, count the number of connected components.

```python
def count_components(n: int, edges: List[Tuple[int, int]]) -> int:
    """Count connected components on `n` vertices given the edge list."""
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return uf.components
```

Four lines. The `uf.components` counter (decremented on every successful `union`) makes this `O(1)` after the unions; the alternative `len(set(uf.find(i) for i in range(n)))` is `O(n alpha(n))` and more general but slower.

The canonical problems:

- **Number of Provinces** (LC 547) — given an adjacency matrix, count components. Exercise 3 exactly.
- **Friend Circles** (LC 547 alias) — same problem, older name.
- **Number of Operations to Make Network Connected** (LC 1319) — count components, return `components - 1` (minus the spare edges, if any).

### Sub-shape 2 — Cycle detection / redundant edge

Given an undirected graph that is one edge away from being a tree, find the redundant edge.

```python
def find_redundant_connection(edges: List[List[int]]) -> List[int]:
    """Find the redundant edge in a near-tree undirected graph."""
    n = len(edges)
    uf = UnionFind(n + 1)  # vertices are 1-indexed per LC 684
    for u, v in edges:
        if not uf.union(u, v):
            return [u, v]
    return []
```

Five lines. The `union` returns `False` when `u` and `v` are already in the same set — which means adding this edge would create a cycle. By LC 684's spec, the *last* such edge in the input is the redundant one; since we process in order, the first `False` is the answer.

The canonical problems:

- **Redundant Connection** (LC 684) — the DSU half of the mini-project.
- **Graph Valid Tree** (LC 261) — given `n` vertices and edges, determine if it forms a tree. Two checks: `len(edges) == n - 1` *and* no cycles.

### Sub-shape 3 — Account merge / equivalence class

The pattern where DSU's leverage is largest. Given a list of "groups" (accounts owned by the same person, equivalent email addresses, etc.), merge transitively and emit the final groupings.

```python
def accounts_merge(accounts: List[List[str]]) -> List[List[str]]:
    """Merge accounts that share at least one email."""
    n = len(accounts)
    uf = UnionFind(n)
    email_to_account: Dict[str, int] = {}

    # Phase 1 — union accounts that share an email.
    for i, account in enumerate(accounts):
        for email in account[1:]:
            if email in email_to_account:
                uf.union(i, email_to_account[email])
            else:
                email_to_account[email] = i

    # Phase 2 — group emails by their account's root.
    groups: Dict[int, List[str]] = defaultdict(list)
    for email, idx in email_to_account.items():
        groups[uf.find(idx)].append(email)

    # Phase 3 — assemble the output with the original name at the front.
    out: List[List[str]] = []
    for root, emails in groups.items():
        out.append([accounts[root][0]] + sorted(emails))
    return out
```

Twenty lines. The two-phase structure (union then enumerate) is the canonical DSU-with-output template.

The canonical problems:

- **Accounts Merge** (LC 721) — the canonical statement; homework problem 1.
- **Most Stones Removed With Same Row Or Column** (LC 947) — DSU over `(row, col)` keys; the result is `n - components`.
- **Synonyms / Similar Sentences** (LC 737) — DSU over word strings.

### Sub-shape 4 — Streaming islands

The variant where new vertices arrive one at a time and we need the component count after each addition.

```python
def num_islands_2(m: int, n: int, positions: List[List[int]]) -> List[int]:
    """LC 305: count islands after each cell is added."""
    uf = UnionFind(m * n)
    is_land: Set[int] = set()
    result: List[int] = []
    count = 0
    for r, c in positions:
        idx = r * n + c
        if idx in is_land:
            result.append(count)
            continue
        is_land.add(idx)
        count += 1
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            nbr = nr * n + nc
            if 0 <= nr < m and 0 <= nc < n and nbr in is_land:
                if uf.union(idx, nbr):
                    count -= 1
        result.append(count)
    return result
```

Twenty lines. The pattern: each new cell is its own component (`count += 1`); each successful union with a neighbor decrements the count.

The canonical problems:

- **Number of Islands II** (LC 305) — the streaming variant of LC 200. Locked behind a LeetCode Premium subscription; the problem statement is widely mirrored on free platforms.
- **Bricks Falling When Hit** (LC 803) — reverse-DSU: process in reverse, adding bricks instead of removing them.

---

## 5. Why DSU beats BFS/DFS on components

For a *one-shot* "count the components" question, BFS/DFS from W6 is `O(V + E)` and uses no extra data structure. DSU is also `O((V + E) alpha(V))` and uses an extra `O(V)` array. So BFS/DFS wins, right?

Not quite. DSU wins on two axes:

1. **Streaming queries.** BFS/DFS requires re-running on the full graph after each edge addition — `O(V + E)` per query, `O(Q (V + E))` for `Q` queries. DSU answers each addition in amortized `O(alpha(V))` and maintains `components` as a running counter.

2. **Online problems.** When the edges arrive one at a time and intermediate component counts are needed, BFS/DFS does not have an incremental form. DSU is *natively* incremental.

For the recognition step: if the prompt says "count the components after each of these `Q` operations," reach for DSU. If it says "count the components of this fixed graph," BFS/DFS is the cleaner choice (smaller constant, fewer concepts).

---

## 6. The amortized `alpha(n)` defense — interview voice

Three sentences. Memorize the cadence.

1. **"Union-Find with path compression and union by rank has amortized `O(alpha(n))` per operation, where `alpha` is the inverse Ackermann function."**
2. **"`alpha(n) <= 4` for any `n` representable on real computers — `alpha(2^65536)` is still about 4. So in practice the operations are constant-time."**
3. **"The amortized bound is Tarjan-Van Leeuwen 1984; the precise statement is that any sequence of `m` operations on `n` elements runs in `O(m alpha(n))` total time."**

If the interviewer presses for the bound *without* the inverse Ackermann citation, the next-most-useful answer is "`O(log n)` worst-case for a single operation, `O(alpha(n))` amortized over a sequence." The single-operation bound is `O(log n)` because `find` may walk a tree of depth `log n` before compression flattens it.

For *senior signal*, you can mention three follow-ups:

- "**Path compression alone** gives `O(log n)` amortized per operation; union by rank alone gives `O(log n)` *worst-case* per operation. The combined bound is the Tarjan-Van Leeuwen result."
- "**The `alpha(n)` bound is tight** for this family of structures — Fredman-Saks 1989 proved no comparison-based DSU can do better."
- "**Union by size is an alternative to union by rank** — attach the smaller tree under the larger by element count instead of by rank. Same asymptotic bound; some implementations prefer it for the simpler bookkeeping."

The first follow-up is the most useful; the others are stretch material.

---

## 7. Implementation variants

Three variants come up in interview contexts.

### Variant 1 — DSU keyed by strings (or arbitrary hashable)

The canonical form uses integer indices `0..n-1`. For problems with string keys (account merge, similar sentences), the cleanest pattern is to *map strings to integers* up front, run integer DSU, then map back:

```python
def with_string_keys(strings: List[str]) -> "UnionFind":
    """Build a UF where elements are strings; expose find/union by string."""
    idx_of: Dict[str, int] = {s: i for i, s in enumerate(strings)}
    uf = UnionFind(len(strings))
    # ... use idx_of[s] when calling uf.find / uf.union
    return uf
```

The alternative — a DSU class with `dict` instead of `list` — is also correct but trades the `O(1)` array access for an `O(1)` *expected* dict access. For most problems the array form with an upfront mapping is cleaner.

### Variant 2 — Weighted DSU (DSU with augmented edge weights)

For problems like LC 399 (Evaluate Division), each edge carries a multiplicative weight (`a / b = 2.0`); the DSU must maintain the weight from each element to the root. Implementation outline:

```python
class WeightedUF:
    def __init__(self) -> None:
        self.parent: Dict[str, str] = {}
        self.weight: Dict[str, float] = {}  # weight[x] = ratio from x to parent[x]

    def find(self, x: str) -> Tuple[str, float]:
        """Return (root, weight from x to root); compress with weights."""
        if x != self.parent[x]:
            parent_root, parent_weight = self.find(self.parent[x])
            self.weight[x] *= parent_weight
            self.parent[x] = parent_root
        return self.parent[x], self.weight[x]
```

Eight lines for `find`. The `weight[x] *= parent_weight` accumulates the path-compression weight correctly. This is Phase-3 material; mention by name if the prompt asks for "ratios," "weighted equivalences," or "currency conversion."

### Variant 3 — DSU with rollback (persistent DSU)

For competitive programming problems that require *undoing* a union, the union-by-rank-without-path-compression form supports `O(log n)` rollback via a stack of changes. This is not entry-level interview material; mention by name only.

---

## 8. The DSU triggers — vocabulary recognition

The single most useful recognition skill is the **vocabulary**. The following words in a problem prompt almost always indicate DSU:

| Trigger word | Sub-shape |
|--------------|-----------|
| **"connect," "connected components"** | components-count |
| **"merge," "merging"** | account-merge or components |
| **"equivalent," "equivalence"** | account-merge |
| **"group," "grouping"** | account-merge |
| **"redundant"** | cycle detection |
| **"is this a tree"** | components + edge-count check |
| **"after a series of operations"** | streaming |
| **"online queries"** | streaming |
| **"swap"** (with transitivity) | components on a swap graph |
| **"friend," "friends-of-friends"** | components |

The negative-space rejections:

- **"Find the shortest path between two nodes"** — not DSU. That is Dijkstra or BFS.
- **"Find the longest path"** — not DSU. That is DFS-with-memo or DP.
- **"Topological order"** — not DSU. That is Kahn's algorithm or DFS-post-order (Week 7).
- **"Bipartite check"** — not strictly DSU, but a 2-coloring DSU variant works. Default to BFS-coloring; mention DSU as a stretch.

---

## 9. Putting DSU together with Lecture 2's MST

Kruskal's MST (Lecture 2 §5) uses DSU as its core data structure. The full integration:

```python
def kruskal(edges: List[Tuple[int, int, float]], n: int) -> Tuple[float, List[Tuple[int, int, float]]]:
    """Kruskal's MST using the Lecture-3 UnionFind."""
    edges_sorted = sorted(edges, key=lambda e: e[2])
    uf = UnionFind(n)
    mst: List[Tuple[int, int, float]] = []
    total = 0.0

    for u, v, w in edges_sorted:
        if uf.union(u, v):
            mst.append((u, v, w))
            total += w
            if len(mst) == n - 1:
                break

    return total, mst
```

The `uf.union(u, v)` call is the entire "cycle detection." Without DSU, Kruskal would need an `O(V + E)` cycle-check per edge, blowing the algorithm up to `O(E (V + E))`. With DSU it is `O(E log E + E alpha(V)) = O(E log E)` — dominated by the sort.

This composition is the most useful single example of why DSU exists: the `O(E log E)` MST algorithm is impossible without the near-constant-time cycle check.

---

## 10. Defending DSU in interview voice

Five sentences. Memorize the cadence.

1. **"Union-Find with path compression and union by rank is an amortized-constant-time data structure for the `find` and `union` operations on disjoint sets."**
2. **"`find(x)` returns the root of `x`'s set; `union(x, y)` merges the sets containing `x` and `y`. Two elements are in the same set iff `find(x) == find(y)`."**
3. **"The path-compression rule in `find` re-points every traversed node directly to the root, flattening the tree. The union-by-rank rule in `union` attaches the lower-rank root under the higher-rank root, keeping the tree shallow."**
4. **"The amortized per-operation cost is `O(alpha(n))`, where `alpha` is the inverse Ackermann function — `alpha(n) <= 4` for any realistic `n`. So in practice the operations are constant."**
5. **"DSU is the right reach for problems that ask about merging, components after a sequence of operations, redundant edges, or equivalence classes. It beats BFS/DFS on streaming problems because it is natively incremental."**

That cadence is the senior-grade defense. The implementation is the second part. Both are graded; the recognition is graded more heavily.

---

## What's next

The three lectures are complete. The week's algorithms — Dijkstra, Bellman-Ford, Floyd-Warshall, Kruskal, Prim, Union-Find — are installed. The rest of the week is exercises (Network Delay Time, Cheapest Flights, Number of Provinces), the challenge (Cheapest Flights K Stops), the homework (six problems across the family), and the mini-project (one Dijkstra write-up, one DSU write-up, fully UMPIRE-narrated).

Push hard on the *recognition* exercises — the quiz especially. The implementation patterns are short and quickly memorized; the Match-step recognition is what discriminates Phase 2 from Phase 3.
