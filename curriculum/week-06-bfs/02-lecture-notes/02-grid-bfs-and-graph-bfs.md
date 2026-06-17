# Lecture 2 — Grid BFS and Graph BFS

> **Duration:** ~2 hours.
> **Outcome:** You can recognize a BFS problem and classify it as grid-BFS or node-BFS in 30 seconds; you can write the multi-source BFS seed in one line; you can apply bidirectional BFS to a "shortest path between two known endpoints" problem and defend the complexity argument.

Lecture 1 covered the canonical BFS template. This lecture covers the **two sub-shapes** the algorithm appears in — **grid-BFS** and **node-BFS** — and the two high-leverage variants every interview-ready candidate should know: **multi-source BFS** and **bidirectional BFS**.

The shift in framing: in Lecture 1, BFS was an abstract graph algorithm. Here, we map it onto the two concrete surface forms that account for ~90% of BFS interview problems. Every drill this week is one or the other (Drill 1 is node-BFS on a tree; Drill 2 is grid-BFS; Drill 3 is multi-source grid-BFS; Drill 4 is node-BFS with bidirectional as the stretch; Drill 5 is node-BFS on a tree with level tracking).

By the end of this lecture you should be able to read a graph problem and, within 30 seconds, say one of two things out loud: **"grid-BFS"** (and immediately name the directions and the in-bounds check) or **"node-BFS"** (and immediately name the `neighbors(node)` function). Then add one of the two variants: **"multi-source — seed with all starting cells"** or **"bidirectional — expand the smaller frontier"**.

---

## 1. The grid sub-shape

A **grid-BFS** problem has an `R × C` matrix as input, where cells are nodes and edges connect orthogonally (4-directional) or with diagonals (8-directional) to walkable neighbors. The graph is **implicit** — it is never built as an adjacency list. The neighbor function is computed on the fly.

The canonical neighbor function for grid-BFS:

```python
DIRS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIRS_8 = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

def grid_neighbors(grid, r, c, dirs=DIRS_4):
    R, C = len(grid), len(grid[0])
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0:   # walkable
            yield (nr, nc)
```

Five lines. The pattern of *(direction offset, in-bounds check, walkability check)* repeats verbatim in every grid-BFS problem this week and beyond. Memorize the shape.

### Common grid variants

| Variant | What changes |
|---------|--------------|
| 4-directional moves (orthogonal) | `DIRS_4` |
| 8-directional moves (with diagonals) | `DIRS_8` |
| Chess knight moves | 8 knight offsets: `[(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]` |
| Walkable defined by `0` (free) / `1` (wall) | `grid[nr][nc] == 0` |
| Walkable defined by `1` (land) / `0` (water) | `grid[nr][nc] == 1` (e.g., "number of islands") |
| Walkable depends on adjacent cell value | replace the literal with the predicate |

The interview-tell move on a grid-BFS problem is **stating the direction set and the walkability predicate out loud in Plan**. Two short lines. Most candidates skip them and end up with a 4-direction loop on an 8-direction problem.

### The visited set on a grid

The visited set stores `(r, c)` tuples. Tuples are hashable; lists are not. The visited set is `O(R × C)` in the worst case. A common optimization for *write-on-the-grid* problems is to mutate the input — set `grid[r][c] = 1` to mark "visited" — saving the `O(R × C)` set memory. Interviewers split on whether mutating input is acceptable; ask before doing it. The visited-set version is always defensible.

---

## 2. The node sub-shape

A **node-BFS** problem has an explicit graph (adjacency list, edge list, or `dict[node, list[node]]`) or an implicit graph where the neighbor function is non-trivial. Examples:

- **Word Ladder (LC 127):** nodes are words; an edge connects two words that differ by exactly one letter. The neighbor function is "all words in the dictionary one letter different from `word`." Implicit; computed via a wildcard-bucket index.
- **Open the Lock (LC 752):** nodes are 4-digit combinations; an edge connects two combinations one rotation apart. Implicit; eight neighbors per node (each digit can rotate up or down).
- **Network Delay Time (LC 743):** nodes are servers; an edge is a directed link with a weight. *Not BFS on the canonical form* — Dijkstra. But the *unweighted* version (count of hops) is node-BFS.
- **Course Schedule II (LC 210):** nodes are courses; an edge is a prerequisite. Topological sort via Kahn's algorithm — uses a queue but with extra state (in-degree). Covered Week 7 (DFS).

### The neighbor function

For an explicit adjacency list `adj: dict[node, list[node]]`:

```python
def neighbors_fn(node):
    return adj.get(node, [])
```

For Word Ladder with a wildcard index:

```python
def build_bucket_index(word_list):
    """Map each '*ot', 'h*t', 'ho*'-style pattern to the words that match."""
    bucket = {}
    for word in word_list:
        for i in range(len(word)):
            pattern = word[:i] + '*' + word[i+1:]
            bucket.setdefault(pattern, []).append(word)
    return bucket

def neighbors_fn(word, bucket):
    for i in range(len(word)):
        pattern = word[:i] + '*' + word[i+1:]
        for w in bucket.get(pattern, []):
            if w != word:
                yield w
```

The wildcard bucket precomputes all "one letter different" relationships in `O(N × L²)` where `N` is the dictionary size and `L` is the word length. After that, neighbor lookup is `O(L × bucket_size)`. Without the index, each neighbor call would be `O(N × L)` and the total BFS would be `O(N² × L)` — usually too slow. The bucket is the standard optimization; we walk through it in Drill 4.

### The visited set on a node graph

For an explicit adjacency list, the visited set stores node identifiers (strings, ints, whatever the graph's "node type" is — must be hashable). For Word Ladder, visited stores words (strings). For Open the Lock, visited stores 4-character combination strings.

Same `O(V)` space, same `O(1)` membership check.

---

## 3. The two preconditions for BFS finding shortest paths

BFS finds shortest paths if and only if **both** of the following hold:

1. **Every edge has unit cost.** (Or, equivalently, every edge has the *same* cost — units do not matter, only that they are identical.)
2. **The graph is finite, or you halt before exhausting it.** Infinite graphs (e.g., the chess knight's reachable cells on an unbounded board) work too, but you must have a termination condition (a target, a distance bound, etc.).

If precondition 1 fails, use Dijkstra (non-negative weights) or Bellman-Ford (possibly negative). If precondition 2 fails and you have no termination condition, you cannot run BFS — the queue would never empty.

The discriminating Match-step move: **state the unit-edge assumption out loud**. *"Every move costs 1 — every move is one cell, one letter change, one lock rotation. BFS finds shortest paths under unit-cost edges; that is why it applies here."*

---

## 4. Multi-source BFS

**Multi-source BFS** is the variant where the queue is seeded with multiple starting nodes. The algorithm is identical to single-source BFS — the only thing that changes is the initial seed shape.

```python
def multi_source_bfs(starts, neighbors_fn):
    queue = deque(starts)
    visited = set(starts)
    dist = {s: 0 for s in starts}
    while queue:
        node = queue.popleft()
        for nbr in neighbors_fn(node):
            if nbr not in visited:
                visited.add(nbr)
                dist[nbr] = dist[node] + 1
                queue.append(nbr)
    return dist
```

Twelve lines. **The only line that differs from single-source BFS is the initial seed.** Everything else is identical.

### What multi-source BFS computes

For each reachable node, the **minimum distance to *any* of the seed nodes**. That is the key property: not "distance to seed 0" or "distance to seed 1" — but the *minimum* over all seeds, computed in a single pass.

### Why it works

The proof is the same level-monotonicity argument from Lecture 1 §3. The invariant "queue entries differ in distance by at most one" still holds when the queue starts with multiple zero-distance nodes — every seed is at distance 0 from itself, so the queue starts with `len(starts)` entries all at distance 0. The induction goes through unchanged.

### Canonical use cases

- **Rotting oranges (LC 994).** Every rotten orange is a source; the answer is "after how many minutes is no fresh orange left?" Multi-source BFS over the rotten cells; the answer is the max distance reached. This is Drill 3.
- **0-1 matrix (LC 542).** Every cell containing 0 is a source; the answer is "distance to the nearest 0 for every cell." Multi-source BFS over all 0-cells; the answer is the `dist` dictionary.
- **As far from land as possible (LC 1162).** Every land cell is a source; the answer is "what is the maximum-distance water cell?" Multi-source BFS over the land cells; the answer is `max(dist.values())`.
- **Walls and gates (LC 286).** Every gate is a source; fill in the distances to the nearest gate for every empty cell.

The pattern is consistent: when the prompt says "starting from any of these cells" or "spread from multiple sources," it is multi-source BFS.

### The seed-shape recognition

The interview signal: **the prompt names a *set* of starts, not a single start**. The phrasing varies — "all rotten oranges," "all gates," "all land cells," "every infected node" — but the structural cue is the plural. Recognize it; seed the queue with the plural.

```python
# Single-source
queue = deque([source])

# Multi-source (the only change)
queue = deque(sources)
```

One character (the `s`) is the entire difference.

---

## 5. Worked example: rotting oranges (LC 994)

This is **the** canonical multi-source BFS problem and Drill 3 of this week. Memorize the structure.

### Problem

`grid[r][c]` is `0` (empty), `1` (fresh orange), or `2` (rotten orange). Every minute, every fresh orange adjacent (4-directional) to a rotten orange becomes rotten. Return the number of minutes until no fresh oranges remain, or `-1` if some fresh orange is unreachable.

### The reframe

> "Compute the minimum minutes for each fresh orange to become rotten, by running multi-source BFS from all initially rotten oranges simultaneously. The answer is the maximum distance reached, unless some fresh orange has no path to any rotten — in which case return `-1`."

### Step 1 — Seed

Walk the grid; every cell with `grid[r][c] == 2` is a seed. Push it onto the queue with distance 0. Also count the number of fresh oranges (`fresh_count`) for the impossible-case check.

### Step 2 — BFS

Standard 4-directional grid-BFS. Mutate the grid (set freshly-rotten cells to `2`) instead of a visited set — small optimization, allowed here because the problem permits input mutation.

### Step 3 — Answer

After BFS, walk the grid. If any `1` remains, return `-1`. Else return the max distance reached.

### Code

```python
from collections import deque

def oranges_rotting(grid: list[list[int]]) -> int:
    R, C = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 2:
                queue.append((r, c, 0))
            elif grid[r][c] == 1:
                fresh += 1
    DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    minutes = 0
    while queue:
        r, c, t = queue.popleft()
        minutes = max(minutes, t)
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                queue.append((nr, nc, t + 1))
    return -1 if fresh > 0 else minutes
```

Eighteen lines. The seed loop on lines 5-10 is the only multi-source-specific code.

### Complexity

- **Time: `O(R × C)`.** Every cell is visited at most once.
- **Space: `O(R × C)`.** Queue can hold up to one BFS level, bounded by `R × C`.

Defense:

> "**O(R × C) time** because every cell enters the queue at most once — multi-source BFS visits each cell exactly once. **O(R × C) space** for the queue. Tradeoff: a naive simulation that loops 'each minute, mark every adjacent fresh orange as rotten, repeat until stable' is `O(R² × C²)` in the worst case (a single rotten orange in the corner of an `R × C` grid takes `R + C` minutes, each minute scans the entire grid). Multi-source BFS replaces the outer 'simulate minutes' loop with a single graph traversal — strictly better. Best/avg/worst all `O(R × C)`."

---

## 6. The four parametric variants of multi-source

| Variant | Seed | Answer extracted from |
|---------|------|----------------------|
| **Spread from sources** (rotting oranges) | All "source" cells | `max(dist.values())` after checking `fresh_count == 0` |
| **Distance to nearest source** (0-1 matrix) | All "source" cells | `dist[r][c]` for each cell |
| **Furthest from sources** (as far from land) | All "source" cells | `max(dist.values())` |
| **Fill from boundaries** (walls and gates) | All "gate" cells | `dist[r][c]` for each empty cell |

All four use the same template. The choice of "answer extracted from" varies; the BFS itself does not.

---

## 7. Bidirectional BFS

**Bidirectional BFS** is the variant where BFS expands from *both* the source and the target simultaneously. The two searches halt when their frontiers meet.

### Why it is faster

For a graph with branching factor `b` and shortest-path distance `d`, single-source BFS visits `O(b^d)` nodes. Bidirectional BFS, by meeting in the middle, visits `O(b^(d/2)) + O(b^(d/2)) = O(b^(d/2))` — exponentially fewer for large `d`.

For Word Ladder with `N` words of length `L`, single-source BFS is `O(N × L²)`. Bidirectional BFS is roughly `O(sqrt(N) × L²)` in practice — usually 4-10x faster for moderate `N`. The complexity argument is not strictly `sqrt(N)` (it depends on the branching factor), but the speedup is real.

### Preconditions

Bidirectional BFS applies if and only if:

1. **Both endpoints are known.** You cannot expand backward from the target if you do not know the target.
2. **The graph is undirected, or you can compute "predecessors of `n`" cheaply.** For undirected graphs, predecessors = neighbors, so it is automatic. For directed graphs, you may need to build a reverse adjacency list.
3. **The graph is finite or has an explicit cutoff.** Otherwise either frontier could expand forever before meeting.

### The template

```python
from collections import deque

def bidirectional_bfs(start, end, neighbors_fn):
    """Return shortest-path length from start to end, or -1 if no path."""
    if start == end:
        return 0
    frontier_start = {start}
    frontier_end = {end}
    visited = {start, end}
    level = 0
    while frontier_start and frontier_end:
        level += 1
        # always expand the smaller frontier
        if len(frontier_start) > len(frontier_end):
            frontier_start, frontier_end = frontier_end, frontier_start
        next_frontier = set()
        for node in frontier_start:
            for nbr in neighbors_fn(node):
                if nbr in frontier_end:
                    return level
                if nbr not in visited:
                    visited.add(nbr)
                    next_frontier.add(nbr)
        frontier_start = next_frontier
    return -1
```

Twenty lines. Three things to highlight:

1. **Always expand the smaller frontier.** This is the optimization — it keeps the total work balanced. The swap on line 11 implements it.
2. **Termination check is `nbr in frontier_end`.** When the smaller frontier produces a neighbor that is already in the larger frontier, the two searches have met. Return the combined level.
3. **`visited` includes nodes from *both* searches.** This is what prevents re-expansion.

### When to use it

Bidirectional BFS is **not** the default. Use it when:

- The graph is large (`V >= 10⁴`) and single-source BFS times out.
- Both endpoints are known.
- The branching factor is moderate (4-30 neighbors per node) — the speedup is most dramatic in this range.

For interview problems on small graphs (`V <= 10³`), single-source BFS is cleaner and fast enough. The interview-tell on Word Ladder is **mentioning that bidirectional is the production optimization** but defending single-source if the interviewer accepts it. Demonstrating awareness without over-engineering is the senior signal.

---

## 8. When to choose grid vs node — the decision

In real interviews, the grid vs node distinction is almost always obvious from the problem statement. The trap is in the *implicit* cases:

- **Chess knight on a board** — the board is a grid, but the moves are not adjacency. Treat it as node-BFS with `neighbors(r, c) = [(r + dr, c + dc) for dr, dc in KNIGHT_OFFSETS if in_bounds]`. The grid coordinates are the node IDs, but the algorithm is more naturally framed as node-BFS because the neighbor function is non-trivial.
- **Word Ladder** — the graph is "words as nodes, one-letter-changes as edges." It is node-BFS, not grid-BFS, even though words can be indexed by character position.
- **2-D puzzle states** — for the 8-puzzle, state is a 3x3 board, but the "graph" is "states reachable by sliding the empty square." Node-BFS on the implicit state graph.

The cleanest mental model: **grid-BFS is the special case of node-BFS where the node ID is an `(r, c)` tuple and the neighbor function is a direction-offset loop.** Everything else is node-BFS.

For interview purposes, the distinction is mostly cosmetic — the visited set and queue are the same. What varies is the neighbor function and (sometimes) the seed shape. Both are part of Plan; both should be stated out loud in 30-second Match.

---

## 9. Common pitfalls

### Pitfall 1 — quadratic blowup from list-as-queue

```python
queue = [start]
while queue:
    node = queue.pop(0)        # O(n) — silent quadratic
```

`list.pop(0)` is `O(n)`. With `V` dequeue calls, total is `O(V²)`. Use `collections.deque.popleft()` — `O(1)`.

### Pitfall 2 — late visited-set update

```python
queue = deque([start])
visited = set()
while queue:
    node = queue.popleft()
    if node in visited:
        continue
    visited.add(node)          # at dequeue time — wrong
    for nbr in neighbors_fn(node):
        queue.append(nbr)
```

A node can be enqueued multiple times before any copy is dequeued. Use enqueue-time marking; visit-check at enqueue.

### Pitfall 3 — using `list` for the visited set

```python
visited = [start]              # WRONG — O(n) membership
if nbr not in visited:         # this is O(n) per call
    ...
```

Membership testing on a `list` is `O(n)`. Use `set`.

### Pitfall 4 — unbounded queue on infinite graphs

```python
# Chess knight on infinite board, BFS without bound
queue = deque([(0, 0, 0)])
visited = {(0, 0)}
while queue:
    r, c, d = queue.popleft()
    if (r, c) == target:
        return d
    for dr, dc in KNIGHT:
        nr, nc = r + dr, c + dc
        if (nr, nc) not in visited:
            visited.add((nr, nc))
            queue.append((nr, nc, d + 1))   # could expand forever
```

On an unbounded board, the BFS can wander far from the target before finding it. Solutions: (a) bound the search region geometrically (the knight needs at most `|x| + |y|` moves, so search within that radius); (b) use bidirectional BFS from both ends; (c) exploit symmetry (the answer to `(x, y)` equals the answer to `(|x|, |y|)`). The challenge problem uses (a) and (c).

### Pitfall 5 — wrong neighbor function for grid orientation

```python
# Counted (row, col) as (x, y) — wrong
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
for dx, dy in DIRS:
    nx, ny = r + dx, c + dy        # mixing axes
```

`(row, col)` and `(x, y)` are different conventions: `(x, y)` is Cartesian (right, up); `(row, col)` is matrix (down, right). Stick to one. The community standard for grid BFS is `(row, col)` with `dr` increasing downward and `dc` increasing rightward.

### Pitfall 6 — treating diagonals as unit cost when they should be √2

For algorithmic BFS we treat all moves as unit cost. This is *correct* for "minimum number of moves" but *incorrect* for "minimum Euclidean distance traveled." If the problem asks for Euclidean distance, BFS gives the wrong answer; you need Dijkstra with non-unit costs. The Match step should explicitly state which is being measured.

---

## 10. Worked example end-to-end: word ladder (LC 127)

We will work this in full UMPIRE, abbreviated.

**[U — 2 minutes]**

> "I am given `beginWord`, `endWord`, and a list `wordList`. Find the length of the shortest transformation sequence from `beginWord` to `endWord` where each step changes exactly one letter and every intermediate word is in `wordList`. Return 0 if no such sequence exists. Confirm: `endWord` must be in `wordList`. Confirm: the transformation length counts `beginWord` and `endWord`. Walk an example: `begin='hit'`, `end='cog'`, `wordList=['hot','dot','dog','lot','log','cog']`. Path: `hit → hot → dot → dog → cog`. Length 5."

**[M — 30 seconds]**

> "Node-BFS on an implicit graph. The 30-second memo: *Words are nodes; an edge connects two words that differ by exactly one letter. The graph is implicit — we generate neighbors via a wildcard-bucket index. BFS finds the shortest transformation length because every edge has unit cost. Why not DFS: DFS would find a path but not necessarily the shortest. Why not weighted-graph algorithms: edges are unit-cost. The high-end optimization is bidirectional BFS — expand from both `beginWord` and `endWord` and meet in the middle.*"

**[P — 2 minutes]**

> "Three things.
> 1. **Build the wildcard-bucket index.** For each word, for each position `i`, create the pattern `word[:i] + '*' + word[i+1:]`. Map each pattern to the words that match it. This precomputes all 'one letter different' adjacencies in `O(N × L²)`.
> 2. **BFS from `beginWord`.** Level-tracking idiom: `level = 1` (count `beginWord`). Each level dequeues all words at that level, generates neighbors via the bucket lookup, and enqueues unvisited ones at `level + 1`.
> 3. **Termination.** When `endWord` is dequeued, return `level`. After loop, return 0.
> Edge case: `endWord` not in `wordList` — return 0 immediately."

**[I — 3 minutes]**

```python
from collections import deque, defaultdict

def ladder_length(beginWord: str, endWord: str, wordList: list[str]) -> int:
    word_set = set(wordList)
    if endWord not in word_set:
        return 0
    L = len(beginWord)
    bucket = defaultdict(list)
    for word in word_set:
        for i in range(L):
            pattern = word[:i] + '*' + word[i+1:]
            bucket[pattern].append(word)
    queue = deque([beginWord])
    visited = {beginWord}
    level = 1
    while queue:
        for _ in range(len(queue)):
            word = queue.popleft()
            if word == endWord:
                return level
            for i in range(L):
                pattern = word[:i] + '*' + word[i+1:]
                for nbr in bucket[pattern]:
                    if nbr not in visited:
                        visited.add(nbr)
                        queue.append(nbr)
        level += 1
    return 0
```

**[R — 1 minute]**

> "Trace on `begin='hit'`, `end='cog'`, `list=['hot','dot','dog','lot','log','cog']`.
> Bucket index: `'*it':['hit']`, `'h*t':['hit','hot']`, `'hi*':['hit']`, `'*ot':['hot','dot','lot']`, `'h*t':[...]`, `'ho*':['hot']`, etc. After building, every 'one letter different' pair is grouped under one bucket pattern.
> Level 1: dequeue 'hit'. Not 'cog'. Patterns '*it', 'h*t', 'hi*'. Neighbors: 'hot' (via 'h*t'). Enqueue. Visited: {'hit', 'hot'}.
> Level 2: dequeue 'hot'. Patterns '*ot', 'h*t', 'ho*'. Neighbors: 'dot', 'lot' (via '*ot'). Enqueue both. Visited: {'hit', 'hot', 'dot', 'lot'}.
> Level 3: dequeue 'dot'. Neighbors: 'dog' (via 'do*'). Enqueue. Dequeue 'lot'. Neighbors: 'log' (via 'lo*'). Enqueue. Visited: {..., 'dog', 'log'}.
> Level 4: dequeue 'dog'. Neighbors: 'cog' (via '*og'). Enqueue. Dequeue 'log'. Neighbor 'cog' already in visited from this level — skip (actually, we added cog at this iteration). Visited: {..., 'cog'}.
> Level 5: dequeue 'cog' (and 'log' was dequeued at level 4 in the inner loop). 'cog' == endWord; return level = 5. ✓"

**[E — 1 minute]**

> "**Time `O(N × L²)`** where `N` is dictionary size and `L` is word length. Building the bucket index is `O(N × L²)` (each word generates `L` patterns of length `L`). BFS visits each word at most once and examines `L` patterns per word, each with up to `O(N)` matches — but amortized across the BFS each edge is examined at most twice, giving `O(N × L²)` total. **Space `O(N × L²)`** for the bucket index. Tradeoff: brute-force neighbor enumeration is `O(N × L)` per word, giving total `O(N² × L)` — strictly worse for large `N`. Bidirectional BFS would cut the expected time roughly by `sqrt(branching factor)` — worth mentioning as a stretch."

---

## 11. The recognition signals — the 30-second match for sub-shapes

Sub-shape recognition signals:

1. **Input is a 2-D matrix (`R × C`).** → Grid-BFS.
2. **Input is a list of edges, an adjacency dict, or "words / states with a transformation rule."** → Node-BFS.
3. **Input is a tree (with `left` / `right` or `children`).** → Node-BFS (level-order family — Drills 1, 5).
4. **Prompt mentions "multiple starts" / "spread from all" / plural sources.** → Multi-source. Seed accordingly.
5. **Both source and target are known and the graph is large.** → Consider bidirectional BFS in your Match step.

The 30-second decision flow:

```
prompt is BFS (passed Lecture 1 §13 test)?
├── grid input?
│      ├── single start ──→ grid-BFS, single-source
│      └── multiple starts ──→ grid-BFS, multi-source seed
└── node input?
       ├── tree?  ──→ node-BFS, level-tracking idiom for "by level" outputs
       ├── adjacency list with single source ──→ node-BFS, per-node distance idiom
       ├── implicit graph (words / states) ──→ node-BFS with custom neighbors_fn
       └── two known endpoints + large graph ──→ consider bidirectional BFS
```

---

## 12. The defense sentence for each sub-shape

In Mock #2 (Week 9), if you draw a BFS problem, the interview tell is whether you state the sub-shape and the neighbor function *out loud, in order*, before writing code.

**For grid-BFS:**

> "Grid-BFS — nodes are `(r, c)` cells; edges connect orthogonally to walkable neighbors. `DIRS = [(-1,0), (1,0), (0,-1), (0,1)]`. Walkability predicate: `0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0`. Visited is a `set` of `(r, c)` tuples; queue is a `deque` of `(r, c, dist)`. Multi-source if the prompt names a *set* of starts."

**For node-BFS:**

> "Node-BFS — nodes are [strings / state objects / integers]; the neighbor function is `neighbors(node) = [...]`. The graph is [explicit / implicit / wildcard-indexed]. Visited is a `set` of node IDs; queue is a `deque`. Level tracking via outer `for _ in range(len(queue))` if the answer is a level count."

That sentence is roughly 20-25 seconds spoken aloud. Practice it.

---

## 13. Self-check

Without notes, answer:

1. **State the two sub-shapes of BFS and one representative problem each.** (Grid-BFS — shortest path in a binary matrix. Node-BFS — Word Ladder. Both use the same algorithm with different `neighbors_fn`.)
2. **Write the multi-source BFS seed in one line.** (`queue = deque(sources); visited = set(sources); dist = {s: 0 for s in sources}`.)
3. **What is the complexity of multi-source BFS?** (`O(V + E)` time, same as single-source — multi-source visits each node exactly once.)
4. **State the bidirectional BFS termination condition.** (When the smaller frontier produces a neighbor that is already in the larger frontier — the two searches have met. The combined level is the answer.)
5. **When does bidirectional BFS apply?** (Both endpoints known; graph undirected or with cheap predecessor function; graph finite or bounded.)
6. **When does BFS not find shortest paths?** (When edges are not unit-cost. Use Dijkstra for non-negative weights.)

If you can answer all six without hesitation, proceed to the drills.

---

## 14. Why this is the highest-yield Phase 2 graph skill

BFS is the *foundation* of every graph algorithm. Dijkstra is BFS with a priority queue; A* is Dijkstra with a heuristic; topological sort can be Kahn's BFS or Tarjan's DFS; bidirectional search is BFS-with-meeting. Every graph algorithm in C5 (AI / Data Science track) builds on BFS or its DFS dual.

For Phase 2 interview prep specifically, BFS shows up in:

- Mock #2 (Week 9): one BFS problem is the median allocation.
- The capstone (Week 15): BFS is on the "patterns you must own" list.
- Every FAANG onsite: at least one graph problem; BFS or DFS.

The drill: Drills 1-5 cover both sub-shapes, plus level tracking and multi-source. Homework problems 1-2 reinforce. The mini-project writes one of each.  Six at-bats this week. By Sunday the "BFS? grid or node? multi-source?" cadence should be reflexive.

---

## Further reading

- **CSES Competitive Programmer's Handbook — Chapter 12 ("Graph traversal")**: <https://cses.fi/book/book.pdf>
- **GeeksforGeeks — "Bidirectional Search"**: a single-page explainer with code; the complexity-halving argument is laid out cleanly.
- **LeetCode 200, 994, 1091, 127, 286, 542, 752, 1162** — the eight problems that anchor grid-BFS, node-BFS, multi-source, and bidirectional families. Drills and homework cover four of them; the others are stretch.

Next: the [drills](../03-exercises/00-overview.md). Drill 3 (Rotting Oranges) is the canonical multi-source problem of the week — do not skip it. Drill 4 (Word Ladder) is the canonical node-BFS problem. Then the [challenge](../04-challenges/challenge-01-minimum-knight-moves.md) — Minimum Knight Moves on an infinite board, the hardest BFS application in the standard repertoire.
