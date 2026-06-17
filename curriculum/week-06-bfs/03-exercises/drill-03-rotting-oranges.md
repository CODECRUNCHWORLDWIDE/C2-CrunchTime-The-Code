# Drill 3 — Rotting Oranges

> **Pattern:** Multi-source grid-BFS — the canonical "spread from multiple seeds" problem
> **Difficulty:** Medium
> **Target solve time:** 25 minutes (with full UMPIRE narration)
> **Why third:** the multi-source idiom is the highest-leverage Week-6 technique. Most candidates write single-source BFS first and then bolt on a "for each seed" outer loop — incorrectly increasing complexity from `O(R × C)` to `O(R × C × K)`. The right move is one seed loop that pre-populates the queue with all sources. After this drill the idiom should be reflexive.

## Problem statement

You are given an `m × n` grid where each cell has one of three values:

- `0` — empty.
- `1` — fresh orange.
- `2` — rotten orange.

Every minute, any fresh orange that is **4-directionally adjacent** to a rotten orange becomes rotten. Return the **minimum number of minutes** until no fresh orange is left, or `-1` if some fresh orange can never become rotten.

**Examples:**

- `grid = [[2,1,1],[1,1,0],[0,1,1]]` → `4`
- `grid = [[2,1,1],[0,1,1],[1,0,1]]` → `-1` (the orange at `(2, 0)` has no rotten neighbor path)
- `grid = [[0,2]]` → `0` (no fresh oranges)
- `grid = [[1]]` → `-1` (one fresh orange, no rotten source)
- `grid = [[2]]` → `0`

## UMPIRE checklist for this drill

- [ ] **U:** Restate. Confirm 4-directional spread (not 8). Confirm "every minute, *every* rotten orange spreads simultaneously to all 4 neighbors." Confirm `0` cells block (cannot become rotten). Confirm zero fresh oranges → return 0. Confirm any unreachable fresh orange → return `-1`. Walk an example by hand at `[[2,1,1],[1,1,0],[0,1,1]]`. Min 0: rotten at (0,0). Min 1: (0,1), (1,0) become rotten. Min 2: (0,2), (1,1) become rotten. Min 3: (2,1) becomes rotten. Min 4: (2,2) becomes rotten. Return 4.
- [ ] **M:** Multi-source grid-BFS. The 30-second memo: *"Multi-source grid-BFS — every rotten orange is a seed; BFS expansion from all seeds simultaneously computes, for each fresh orange, the minimum minutes for any rotten neighbor to reach it. The answer is the max distance reached, after confirming every fresh orange is reachable. Why not single-source repeated K times: that is `O(R × C × K)` for `K` rotten oranges; multi-source is `O(R × C)`. Why not simulation: a naive 'each minute, mark adjacent cells' loop is `O((R × C)² )` in the worst case; multi-source BFS is strictly better."*
- [ ] **P:** Three steps.
  1. **Seed.** Walk the grid; for each `(r, c)` with `grid[r][c] == 2`, push `(r, c, 0)` onto the queue. Also count fresh oranges (`fresh_count`).
  2. **BFS.** 4-directional. Mutate the grid in place: when reaching a fresh `(nr, nc)`, set `grid[nr][nc] = 2`, decrement `fresh_count`, track `minutes = max(minutes, t + 1)`.
  3. **Answer.** If `fresh_count > 0`, return `-1`. Else return `minutes`.
  Edge cases: zero fresh oranges → return 0. Empty grid → return 0 (degenerate).
- [ ] **I:** Write the code. Speak the multi-source idiom: *"The queue is seeded with *all* rotten oranges at minute 0. Each entry is `(r, c, t)` — time to reach this cell. BFS processes them level by level; the first time we reach a fresh orange, it converts at time `t + 1`."*
- [ ] **R:** Trace on `[[2,1,1],[1,1,0],[0,1,1]]`. Seed: queue=[(0,0,0)]; fresh=6. Dequeue (0,0,0). Neighbors: (1,0)=1 → set to 2, fresh=5, enqueue (1,0,1). (0,1)=1 → set to 2, fresh=4, enqueue (0,1,1). Dequeue (1,0,1). Neighbors: (0,0) already 2, (2,0)=0 blocked, (1,1)=1 → set to 2, fresh=3, enqueue (1,1,2). Dequeue (0,1,1). Neighbors: (0,0) already 2, (1,1) already 2 (this minute), (0,2)=1 → set to 2, fresh=2, enqueue (0,2,2). Dequeue (1,1,2). Neighbors: (0,1) already 2, (2,1)=1 → set to 2, fresh=1, enqueue (2,1,3). (1,2)=0 blocked. Dequeue (0,2,2). Neighbors: (1,2)=0 blocked, (0,1) already 2. Dequeue (2,1,3). Neighbors: (1,1) already 2, (2,0)=0 blocked, (2,2)=1 → set to 2, fresh=0, enqueue (2,2,4). Dequeue (2,2,4). No more fresh neighbors. Queue empty. fresh=0, minutes=4. Return 4. ✓
- [ ] **E:** **Time `O(R × C)`** — every cell enters the queue at most once; 4-neighbor enumeration is `O(1)`. **Space `O(R × C)`** for the queue worst case. Tradeoff: naive simulation is `O((R × C)²)` in the worst case (one rotten orange in a corner, spreading across an `R × C` grid). Multi-source BFS replaces the outer "minutes" loop with a single graph traversal. Best `O(R × C)` (every cell visited once is mandatory); worst `O(R × C)`.

## Acceptance criteria

- Code passes the [`timed_runner.py`](./timed_runner.py) test cases for `oranges_rotting`.
- UMPIRE write-up at `umpire-writeups/c2-week-06/drill-03-rotting-oranges.md`.
- Your Match section names **multi-source grid-BFS** explicitly and contrasts against single-source-repeated and naive-simulation.
- Your Implement section seeds the queue with **all rotten oranges** in a single pass before the BFS loop.
- Your Implement section either mutates the grid (defensible) or uses a `visited` set (defensible) — state which and why.
- Your Evaluate section states the **`O(R × C) / O(R × C)` defense sentence** and contrasts against the naive simulation.
- Recording **≥ 15 minutes**.

## Function signature (for the runner)

```python
def oranges_rotting(grid: list[list[int]]) -> int:
    """Return minimum minutes for all fresh oranges to rot, or -1 if impossible."""
    ...
```

## Common bugs you should catch in Review

- **Forgetting to count fresh oranges before BFS.** Without the `fresh_count`, you cannot detect the impossible case where some fresh orange is unreachable.
- **Forgetting to handle the zero-fresh case.** If no `1` exists, return 0 — every grid is already in the "done" state.
- **Single-source repeated K times.** Running BFS once per rotten orange and taking the min is `O(R × C × K)`. Multi-source BFS is `O(R × C)`. Use the multi-source seed.
- **Not adding seeds to visited initially.** Without seeding the visited set (or mutating the grid), seeds can be re-enqueued by neighboring seeds — incorrect.
- **Treating diagonal moves as adjacent.** The spec is 4-directional (orthogonal). 8-directional would give a different (smaller) answer.
- **Storing `(r, c, minutes)` but reading `minutes` only at the end.** That works, but a common mistake is to forget the `max(minutes, t + 1)` accumulator and instead return the time of the last cell dequeued, which is correct only if BFS happens to visit the "last" cell last (it does, in this case, but the explicit max is more defensible).

## Self-feedback template

1. Did you say **"multi-source"** in Match?
2. Did you seed the queue with all rotten oranges in one pre-loop pass?
3. Did you handle the impossible case via `fresh_count` check?
4. Did you say *why* multi-source beats single-source-repeated?

## What to commit

```
umpire-writeups/c2-week-06/
├── drill-03-rotting-oranges.md
└── drill_03_solution.py
```

When done, push and move on to [Drill 4](./drill-04-word-ladder.md) — node-BFS on an implicit string graph.
