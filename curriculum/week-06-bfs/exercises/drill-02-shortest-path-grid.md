# Drill 2 — Shortest Path in a Binary Matrix

> **Pattern:** Grid-BFS, 8-directional, per-node distance
> **Difficulty:** Medium
> **Target solve time:** 25 minutes (with full UMPIRE narration)
> **Why second:** the canonical grid-BFS problem. Single source, single target, clear unit-cost edges. After this drill you should be able to write the grid-BFS skeleton (direction set + bounds check + walkability check + visited set) without looking at notes.

## Problem statement

Given an `n × n` binary matrix `grid`, return the length of the shortest **clear path** from cell `(0, 0)` to cell `(n-1, n-1)`. A clear path is a sequence of cells `(r_0, c_0), (r_1, c_1), …, (r_k, c_k)` such that:

- `(r_0, c_0) == (0, 0)` and `(r_k, c_k) == (n-1, n-1)`.
- Every cell in the path has value `0`.
- Consecutive cells are **8-directionally adjacent** (including diagonals).

The path **length** is the number of cells in it (so the minimum possible answer is 1, when `n == 1` and `grid[0][0] == 0`). Return `-1` if no clear path exists.

**Examples:**

- `grid = [[0,1],[1,0]]` → `2` (path `(0,0) → (1,1)` diagonally)
- `grid = [[0,0,0],[1,1,0],[1,1,0]]` → `4` (path `(0,0) → (0,1) → (1,2) → (2,2)`)
- `grid = [[1,0,0],[1,1,0],[1,1,0]]` → `-1` (start is blocked)
- `grid = [[0]]` → `1`

## UMPIRE checklist for this drill

- [ ] **U:** Restate. Confirm 8-directional moves (including diagonals). Confirm path length = number of cells. Confirm start or goal blocked = `-1`. Confirm `n == 1, grid[0][0] == 0` returns 1.
- [ ] **M:** Grid-BFS with per-node distance. The 30-second memo: *"Grid-BFS — nodes are `(r, c)` cells; edges connect 8-directionally to cells with value `0`. The graph is implicit; the neighbor function enumerates eight offsets. BFS finds the shortest path because every move has unit cost. Why not DFS: DFS finds *a* path, not the shortest. Why not Dijkstra: edges are unit-cost; Dijkstra adds a log-factor overhead with no benefit."*
- [ ] **P:** Initialize: if `grid[0][0] != 0` or `grid[n-1][n-1] != 0`, return `-1`. `DIRS = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]`. Queue `[(0, 0, 1)]`, visited `{(0,0)}`. Loop: dequeue `(r, c, d)`. If `(r, c) == (n-1, n-1)`, return `d`. For each direction, compute `(nr, nc)`. If in bounds, walkable, not visited, mark visited and enqueue with `d + 1`. Return `-1` after loop.
- [ ] **I:** Write the code, narrating each line. Speak the invariant: *"Visited is added at *enqueue time*, immediately after the in-bounds and walkability checks. The queue can hold up to `O(R × C)` cells in the worst case."*
- [ ] **R:** Trace on `[[0,0,0],[1,1,0],[1,1,0]]`. Queue=[(0,0,1)]. Dequeue (0,0,1). Eight neighbors; valid (in-bounds, walkable, unvisited): (0,1), (1,0)=1 wall, (1,1)=1 wall. Enqueue (0,1,2). Dequeue (0,1,2). Neighbors: (0,0) visited, (0,2), (1,0)=1 wall, (1,1)=1 wall, (1,2). Enqueue (0,2,3), (1,2,3). Dequeue (0,2,3). Neighbors: (1,1) wall, (1,2) visited, (1,3) oob. No new adds. Dequeue (1,2,3). Neighbors: (2,1) wall, (2,2), (2,3) oob, (0,1) visited, (0,2) visited, (0,3) oob. Enqueue (2,2,4). Dequeue (2,2,4). Goal! Return 4. ✓
- [ ] **E:** **Time `O(N²)`** where `N` is the grid side — every cell visited at most once, 8-neighbor enumeration is `O(1)` per cell. **Space `O(N²)`** for the visited set and queue worst case. Tradeoff: DFS is same asymptotic but does not return shortest. Dijkstra on unit costs is BFS with extra log-factor. Best `O(1)` (start == goal); worst `O(N²)`.

## Acceptance criteria

- Code passes the [`timed_runner.py`](timed_runner.py) test cases for `shortest_path_binary_matrix`.
- UMPIRE write-up at `umpire-writeups/c2-week-06/drill-02-shortest-path-grid.md`.
- Your Match section explicitly states **grid-BFS** and the **8-directional direction set**.
- Your Implement section uses `collections.deque` for the queue and a `set` for visited (or a 2-D boolean array — both acceptable; defend whichever you pick).
- Your Implement section adds to visited **at enqueue time**, not at dequeue time.
- Your Evaluate section states the **`O(N²) / O(N²)` defense sentence** and explicitly rejects Dijkstra-with-unit-costs.
- Recording **≥ 15 minutes**.

## Function signature (for the runner)

```python
def shortest_path_binary_matrix(grid: list[list[int]]) -> int:
    """Return shortest path length from (0,0) to (n-1,n-1), or -1 if none."""
    ...
```

## Common bugs you should catch in Review

- **Using 4-directional moves.** The problem says 8-directional. Read the spec twice; the `DIRS` set has eight entries.
- **Adding to visited at dequeue time.** A cell can be enqueued from up to 8 neighbors; without enqueue-time visiting, you might enqueue it 8 times, blowing up the queue. Add at enqueue.
- **Path length off-by-one.** The path includes `(0, 0)` itself, so starting distance is **1**, not 0. The minimum answer is 1 (for an `n == 1` grid with `grid[0][0] == 0`).
- **Not handling blocked start or goal.** If `grid[0][0] != 0` or `grid[n-1][n-1] != 0`, return `-1` immediately. Otherwise the loop might never terminate (well, it will, by returning `-1` after the queue drains — but the early check is cleaner).
- **Mutating the grid as the visited marker.** Acceptable if you state it; not acceptable on inputs that must be preserved. The explicit `visited` set is always defensible.

## Self-feedback template

1. Did you state **grid-BFS** in Match, with the direction set named?
2. Did you state the **enqueue-time visited invariant**?
3. Did you handle blocked start / goal?
4. Did you use `deque`?

## What to commit

```
umpire-writeups/c2-week-06/
├── drill-02-shortest-path-grid.md
└── drill_02_solution.py
```

When done, push and move on to [Drill 3](drill-03-rotting-oranges.md) — multi-source BFS, the high-leverage idiom of the week.
