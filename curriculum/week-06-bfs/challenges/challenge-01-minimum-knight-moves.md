# Challenge 1 — Minimum Knight Moves (LeetCode 1197)

> **Pattern:** Node-BFS on an *infinite implicit graph*, with symmetry pruning and (optionally) bidirectional BFS
> **Difficulty:** Hard
> **Target solve time:** 90 minutes (first time; 45 minutes on revisit)
> **Why hard:** the graph is infinite. Naive BFS works in principle but allocates an unbounded visited set; without pruning, the algorithm is fragile on adversarial inputs. The senior signal is recognizing the *symmetry of the problem* (`(x, y)` ≡ `(|x|, |y|)`) and using it to halve (then quarter) the search space, plus optionally bringing in bidirectional BFS for the high-end optimization.

## Problem statement

In an **infinite** chess board with coordinates ranging from `-infinity` to `+infinity`, a knight is positioned at `(0, 0)`. Return the **minimum number of knight moves** to reach the target cell `(x, y)`.

A knight has 8 possible moves: `(±2, ±1)` and `(±1, ±2)` — eight `L`-shaped jumps.

Per the LC spec: `-300 <= x, y <= 300`. The answer is guaranteed to exist (the knight can always reach any cell on an infinite board).

**Examples:**

- `x = 2, y = 1` → `1` (one knight move)
- `x = 5, y = 5` → `4`
- `x = 0, y = 0` → `0`
- `x = 1, y = 1` → `2` (knight cannot reach `(1, 1)` in one move; two moves needed)
- `x = -1, y = -1` → `2` (symmetric to `(1, 1)`)

## Acceptance criteria

- [ ] Code passes the test cases at the bottom (write your own pytest file, or extend `timed_runner.py`).
- [ ] Solution is **`O(max(|x|, |y|)²)`** time and **`O(max(|x|, |y|)²)`** space — single-source BFS with search-region bounding. Naive uncapped BFS is accepted but is "barely passable"; the bounded version is the senior signal.
- [ ] Your FRAME write-up **explicitly states the symmetry argument** (`f(x, y) = f(|x|, |y|)`) in the Research constraints section. Naming the symmetry is the senior-level signal.
- [ ] Your write-up handles the **edge cases**: `(0, 0)` returns 0; `(1, 1)`, `(2, 2)`, and other "small distance, two moves required" cases trace correctly.
- [ ] Recording **≥ 45 minutes** — yes, three quarters of an hour. First time on this problem is long; that is the right shape.

## The decomposition (the interview tell)

The clean approach has two structural insights and one technique:

**Insight 1 — Symmetry.** The answer depends only on `(|x|, |y|)`. A knight move is symmetric in both axes: if `(dx, dy)` is a valid knight move, so are `(-dx, dy)`, `(dx, -dy)`, `(-dx, -dy)`. So any path from `(0, 0)` to `(x, y)` has a mirror image path to `(|x|, |y|)` of the same length. Reduce to the first-quadrant subproblem.

**Insight 2 — Bounded search region.** From `(0, 0)`, after `k` knight moves, the knight is at most `2k` cells away in any direction (each move changes a coordinate by at most 2). So the answer is at least `ceil(max(|x|, |y|) / 2)`. Equally, a knight can always reach `(x, y)` in at most `|x| + |y|` moves (by a careful sequence). The search region can be bounded by `[-1, x + 1] × [-1, y + 1]` (a small buffer for "go past and come back") after we have reduced to the first quadrant. This makes the visited set bounded.

**Technique — BFS, single-source, with the pruning above.** Initialize at `(0, 0)`. Use a bounded grid for visited tracking. Eight knight offsets. Return the level at which `(x, y)` is dequeued.

Once the algorithm is bounded:

- The search region is at most `(|x| + 2) × (|y| + 2)`.
- Each cell is visited at most once.
- Each visit examines 8 neighbors in `O(1)`.

Total `O(|x| × |y|)` time, same space. For LC's `|x|, |y| <= 300`, that is `~9 × 10⁴` cells — comfortable.

```
First-quadrant reduction:
(x, y) = (-5, 3)  --> reduce to (5, 3) by symmetry
                      same answer.

Bounded search region:
After reduction, search within [-2, x+2] x [-2, y+2].
We allow a small negative buffer because the knight may need to
step into negative coordinates briefly even when reaching a positive
target (e.g., (1, 1) requires going to (-1, 2) or (2, -1) then back).
```

The discriminator: most candidates try unbounded BFS and either time out on adversarial `(x, y)` or accidentally allow the visited set to grow unboundedly. The interview-tell move is **stating the symmetry and the search-region bound** before writing code.

## FRAME outline

- **F:** Restate. Confirm infinite board. Confirm 8 knight moves. Confirm `(0, 0)` start. Walk `(2, 1)` by hand: one move. Walk `(5, 5)` by hand and intuit: cannot be done in fewer than 4 moves; verify each move sequence sums correctly. Confirm the spec's constraint `-300 <= x, y <= 300` — the bound matters for the search-region choice.

- **R:** Node-BFS on an infinite implicit graph with symmetry pruning. The 30-second memo:
  > *"Node-BFS — nodes are `(r, c)` coordinates; edges are the 8 knight offsets. BFS finds shortest path because every move has unit cost. Two optimizations: (a) symmetry reduce to first quadrant — `f(x, y) = f(|x|, |y|)` because knight moves are symmetric in both axes; (b) bound the search region to `[-2, x+2] × [-2, y+2]` — the answer is at most `|x| + |y|` moves, and the knight never strays more than 2 cells outside the target rectangle in an optimal path. Why not DFS: would not find the shortest. Why not Dijkstra: edges are unit-cost. Stretch: bidirectional BFS, expand from both `(0, 0)` and `(x, y)` and meet in the middle — exponentially faster in the worst case."*

- **A:** Four things.
  1. **Symmetry reduction.** `x, y = abs(x), abs(y)`.
  2. **Trivial case.** `if (x, y) == (0, 0): return 0`. `if (x, y) == (1, 1): return 2`. (The latter is a corner case where the search-region bound gets tight; explicit-handling avoids edge-case bugs.)
  3. **Search-region bound.** Define `MAX = max(x, y) + 2`. Visited cells must satisfy `-2 <= r <= MAX` and `-2 <= c <= MAX`.
  4. **BFS.** Queue = `deque([(0, 0, 0)])`. Visited = `{(0, 0)}`. Eight knight offsets. Loop: dequeue `(r, c, d)`. If `(r, c) == (x, y)`, return `d`. For each offset, compute `(nr, nc)`. If within bound and unvisited, enqueue with `d + 1`.

- **M:** Make the solution. Sentinel-bound and visited-set discipline are the most error-prone parts. Write the bounds check explicitly: `-2 <= nr <= MAX and -2 <= nc <= MAX`.

- **E (verify):** Trace on `(5, 5)`. After symmetry: still `(5, 5)`. MAX = 7. BFS from `(0, 0)`:
  Level 0: `(0,0)`.
  Level 1: 8 knight offsets. Valid (in bound, unvisited): `(1,2), (2,1), (-1,2), (2,-1), (1,-2), (-2,1)` and others. Filter by bound `[-2, 7]`: all included.
  Level 2: 16+ expansions. Reach `(4, 3), (3, 4), (4, 5)`, etc.
  Level 3: reach `(5, 4)` from `(4, 2) + (1, 2)`, or `(3, 5)` from `(4, 3) + (-1, 2)`, etc. Cannot reach `(5, 5)` yet.
  Level 4: reach `(5, 5)` via, e.g., `(3, 4) + (2, 1)`. Return 4. ✓

  Trace on `(1, 1)`. After symmetry: `(1, 1)`. Cannot reach in 1 move. Level 2 expansions of `(1, 1)`'s neighbors via `(2, -1) + (-1, 2)` or similar — return 2. ✓

  Trace on `(0, 0)`. Early return 0. ✓

- **E (graded):** **Time `O(max(|x|, |y|)²)`** — bounded search region of `(MAX + 4)²` cells; each visited at most once; constant 8 neighbors per visit. **Space `O(max(|x|, |y|)²)`** for the visited set. Tradeoff: unbounded BFS is `O(answer² × 8^answer)` in pathological setups — but in practice `O(|x| × |y|)`. The bounded version is strictly safer. Bidirectional BFS: expected `O(max(|x|, |y|)) ` work with constant overhead; better for large coordinates. Best case `O(1)` (target = origin); worst case `O(|x| × |y|)`.

## Function signature

```python
def min_knight_moves(x: int, y: int) -> int:
    """Return the minimum number of knight moves from (0, 0) to (x, y)."""
    ...
```

## Test cases to verify

```python
import pytest

@pytest.mark.parametrize("x, y, expected", [
    (0, 0, 0),
    (2, 1, 1),
    (1, 2, 1),
    (1, 1, 2),
    (5, 5, 4),
    (-5, 5, 4),
    (5, -5, 4),
    (-5, -5, 4),
    (0, 1, 3),
    (1, 0, 3),
    (2, 2, 4),
    (4, 4, 4),
    (6, 6, 4),
    (300, 300, 200),
    (300, 0, 150),
])
def test_min_knight_moves(x, y, expected):
    assert min_knight_moves(x, y) == expected
```

## Common bugs you should catch in Examine (verify)

- **Not reducing by symmetry.** Without the `x, y = abs(x), abs(y)` line, the search can expand into the wrong quadrant and either time out or return a stale answer. The symmetry reduction is line one.
- **Forgetting the small negative buffer.** Bounding visited to `0 <= r <= x` and `0 <= c <= y` is too tight — for `(1, 1)`, the optimal first move is `(2, -1)` (going negative) and the second move is `(-1, 2)`. Bound `[-2, MAX]` includes those steps.
- **Wrong knight offsets.** Eight moves: `(±1, ±2)` and `(±2, ±1)`. Forgetting any one of them produces a knight that cannot reach some squares.
- **Adding to visited at dequeue time.** Same bug pattern from Exercise 2 — multiple enqueues of the same cell. Add at enqueue time.
- **Not handling `(0, 0)` as a special case.** Without the early return, the BFS still works (the first dequeue is `(0, 0, 0)`, which matches the target), but the explicit early return is cleaner.
- **Bidirectional BFS without proper termination.** If you implement bidirectional, the meet condition is "the smaller frontier produces a neighbor that is already in the larger frontier." The total level is `level_a + level_b - 1` or similar; check the exact accounting with a small trace.

## The "why O(max(|x|, |y|)²)?" defense

Out loud, in your Examine (cost) section:

> "**Why `O(max(|x|, |y|)²)` time, same space.** We bound the search region to `(|x| + 4) × (|y| + 4)` — derived from the observation that the knight cannot need more than `|x| + |y|` moves and never strays more than 2 cells outside the target rectangle in an optimal path. Each cell in the bounded region is visited at most once (visited-set invariant), and each visit examines 8 neighbors in `O(1)`. The unbounded version's complexity is unbounded in the worst case; the bounded version is provably linear in the search-region area. The senior signal is that **the bounded version's correctness follows from the symmetry of the knight's moves** — without that observation we would have no principled bound and the algorithm would be fragile."

Memorize the shape of that sentence. Saying it cleanly is the difference between "solved Minimum Knight Moves" and "demonstrated mastery of BFS on implicit graphs."

## Why this matters

Minimum Knight Moves is a representative member of a class of problems that show up regularly in real onsites:

1. **BFS on an implicit infinite graph** — the same pattern powers sliding puzzle solvers, robot navigation on infinite grids, and game-state-space searches.
2. **Symmetry as an algorithmic primitive** — recognizing that two states are isomorphic and unifying them is a senior-level move. The 8-puzzle's "canonical form" trick is the same skill.
3. **Bounded search regions** — knowing how to bound the visited set is the difference between "BFS works" and "BFS works on adversarial inputs." Production-grade BFS in real systems (route planners, recommendation engines) always has bounds.

When you revisit this challenge before Mock #2, **re-derive the search-region bound from scratch** rather than re-reading your old solution. The derivation is the skill.

## Stretch

**Bidirectional BFS.** Expand simultaneously from `(0, 0)` and `(x, y)`. Maintain two frontiers; halt when they meet. The complexity drops to roughly `O(sqrt(|x| × |y|))` work in the worst case — much faster for large coordinates. The trade is implementation complexity; the senior signal is mentioning the technique even if you do not implement it.

**Open the Lock (LC 752).** A 4-digit combination lock with forbidden states; BFS on the state graph (8 neighbors per state — each of 4 digits can rotate up or down). Same node-BFS template with a different `neighbors_fn`. Useful warm-up for Mock #2.

**Bus Routes (LC 815).** BFS on a "graph of routes," where two routes are adjacent if they share a stop. The senior insight is that nodes should be *routes*, not *stops* — otherwise the state space explodes. Same template; different modeling.

---

This concludes Week 6's challenges. Take the [quiz](../quiz.md), do the [homework](../homework/README.md), then ship the [mini-project](../mini-project/README.md) — one grid-BFS write-up and one node-BFS write-up.
