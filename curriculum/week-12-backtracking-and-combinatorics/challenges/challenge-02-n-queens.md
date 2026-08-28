# Challenge 2 — N-Queens

> **Pattern:** Backtracking — constraint satisfaction on a grid
> **Difficulty:** Hard
> **Target solve time:** 45 minutes with full FRAME narration

## Problem statement

A queen attacks along its own row, its own column, and both diagonals through it. Place `n` queens on an `n × n` board so that no queen attacks another, and return **every** arrangement that works. Order of the arrangements does not matter.

Encode one arrangement as a list of `n` strings, one string per row, each `n` characters long. `'Q'` is a queen; `'.'` is an empty square.

**Constraints.**

- `1 <= n <= 12`. At `n = 12` there are 14,200 arrangements — the pruning developed below still returns in well under a second, which is the point of the upper bound.

**Examples.**

- `n = 1` → `[["Q"]]` — the degenerate board.
- `n = 2` → `[]` — two queens on a 2×2 board always share a row, column, or diagonal.
- `n = 3` → `[]` — the smallest non-trivial board with no arrangement.
- `n = 4` → two arrangements: `[[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]`

**Practice elsewhere.** The same task is posed as [LeetCode 51 · N-Queens](https://leetcode.com/problems/n-queens/) if you want a judge to run it against. The statement, constraints, and examples above are written for this course; the two differ, so read ours.

**The deliverable.** A full FRAME write-up published to `frame-writeups/c2-week-12/challenge-02/`, with the code committed under `challenges/c2-week-12/n-queens.py`. Stretch — not required for the week.

---

## Frame

The N-Queens puzzle has been studied since 1848. Two queens attack each other if they share a row, a column, or a diagonal. For N=8, there are 92 distinct solutions (12 fundamental solutions up to rotation and reflection).

Hand-walk on N=4:

```
Two valid configurations:
.Q..       ..Q.
...Q       Q...
Q...       ...Q
..Q.       .Q..
```

Note that the two are rotations of each other. The "fundamental" solution count for N=4 is 1; the "all distinct" count is 2.

The brute-force enumeration places N queens on N² cells: `C(N², N)` configurations. For N=8: `C(64, 8) ≈ 4 billion`. Infeasible. The "one queen per row" discipline reduces this to `N!` permutations of queens-to-columns. For N=8: `40,320`. Feasible but slow. The constraint-propagation pruning cuts this to ~2,000 for N=8. Microseconds.

---

## Research constraints

The 30-second pattern-recognition memo:

> *Constraint satisfaction problem. Backtracking with three pruning sets (cols, diag1, diag2). State = (row, cols, diag1, diag2, path). Place one queen per row (the row constraint is implicit by structure). For each candidate column, check three pruning sets in O(1); if all pass, choose (add to three sets and path), recurse with row + 1, unchoose (remove from three sets and pop path). Record at leaves where row == n. Worst-case time O(N!); the pruning sets cut this to roughly O(N!) / (large constant). Space O(N) for recursion plus three sets of size <= N each.*

**Why three sets, not the board?** Without the sets, checking whether a placement is safe requires walking every previously-placed queen (one per row, so up to N queens) and computing whether they attack the new placement — `O(N)` per check. With the sets, the check is three `O(1)` set membership tests. For N=8, the speedup is ~50x.

**Why diagonal indexing `row - col` and `row + col`?** A diagonal from top-left to bottom-right (`\`) has a constant value of `row - col` for every cell on it. A diagonal from top-right to bottom-left (`/`) has a constant value of `row + col`. The two are independent — a queen at `(r, c)` is on the `\` diagonal indexed by `r - c` and the `/` diagonal indexed by `r + c`. Two queens conflict on the `\` diagonal iff they have the same `r - c`; they conflict on the `/` diagonal iff they have the same `r + c`.

---

## Assess options

1. Initialize `result = []`, `path = []` (where `path[r]` is the column chosen for row `r`), `cols = set()`, `diag1 = set()` (indexed by `row - col`), `diag2 = set()` (indexed by `row + col`).
2. Define a helper `render(path) -> List[str]` that converts a list of column indices to the LC 51 board format (a list of `n` strings of length `n`, each string having a `Q` at the column index and `.` elsewhere).
3. Define `backtrack(row)`:
   - If `row == n`: append `render(path)` to `result`, return.
   - For `col` from `0` to `n - 1`:
     - If `col in cols or (row - col) in diag1 or (row + col) in diag2`: continue.
     - Choose: add `col` to `cols`, `row - col` to `diag1`, `row + col` to `diag2`; append `col` to `path`.
     - Recurse with `backtrack(row + 1)`.
     - Unchoose: pop `path`; remove `col` from `cols`, `row - col` from `diag1`, `row + col` from `diag2`.
4. Call `backtrack(0)`.
5. Return `result`.

The four state mutations on choose must be mirrored by four unchoose steps in reverse order.

---

## Make the solution

```python
from __future__ import annotations

from typing import List, Set


def solve_n_queens(n: int) -> List[List[str]]:
    """Return all solutions to the N-Queens puzzle as a list of board configurations."""
    result: List[List[str]] = []
    path: List[int] = []                    # path[r] = column chosen for row r
    cols: Set[int] = set()
    diag1: Set[int] = set()                 # row - col
    diag2: Set[int] = set()                 # row + col

    def render(path: List[int]) -> List[str]:
        """Convert column-index path to the LC 51 board format."""
        return ["." * c + "Q" + "." * (n - c - 1) for c in path]

    def backtrack(row: int) -> None:
        if row == n:
            result.append(render(path))
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            path.append(col)
            backtrack(row + 1)
            path.pop()
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0)
    return result
```

Twenty-eight lines. The four state mutations on choose; four unchoose steps in reverse; the `render` helper formats the output.

---

## Examine · verify

Trace N=4 step by step:

```
backtrack(0): row=0, cols={}, diag1={}, diag2={}, path=[]
  col=0: cols={0}, diag1={0}, diag2={0}, path=[0]; backtrack(1)
    col=0: in cols, skip.
    col=1: 1-1=0 in diag1, skip.       # \ diagonal conflict with (0,0)
    col=2: cols={0,2}, diag1={0,-1}, diag2={0,3}, path=[0,2]; backtrack(2)
      col=0: in cols, skip.
      col=1: 2+1=3 in diag2, skip.     # / diagonal conflict
      col=2: in cols, skip.
      col=3: 2-3=-1 in diag1, skip.    # \ conflict with (1,2)
      backtrack(2) finds no valid col; returns.
    Unchoose col=2.
    col=3: cols={0,3}, diag1={0,-2}, diag2={0,4}, path=[0,3]; backtrack(2)
      col=0: in cols, skip.
      col=1: cols={0,3,1}, diag1={0,-2,1}, diag2={0,4,3}, path=[0,3,1]; backtrack(3)
        col=0,1,3: in cols, skip.
        col=2: 3-2=1 in diag1, skip.   # \ conflict with (2,1)
        backtrack(3) returns.
      Unchoose col=1.
      col=2: 2+2=4 in diag2, skip.
      col=3: in cols, skip.
      backtrack(2) returns.
    Unchoose col=3.
  Unchoose col=0.
  col=1: cols={1}, diag1={-1}, diag2={1}, path=[1]; backtrack(1)
    col=0: 1+0=1 in diag2, skip.
    col=1: in cols, skip.
    col=2: 1-2=-1 in diag1, skip.
    col=3: cols={1,3}, diag1={-1,-2}, diag2={1,4}, path=[1,3]; backtrack(2)
      col=0: cols={1,3,0}, diag1={-1,-2,2}, diag2={1,4,2}, path=[1,3,0]; backtrack(3)
        col=0: in cols, skip.
        col=1: in cols, skip.
        col=2: cols={1,3,0,2}, diag1={-1,-2,2,1}, diag2={1,4,2,5}, path=[1,3,0,2];
               backtrack(4)
          row == 4 == n. Record render([1,3,0,2]):
            ".Q.."
            "...Q"
            "Q..."
            "..Q."
        Unchoose col=2.
      ... (rest of the trace finds no more from this branch) ...
  ... (symmetric trace for col=1 starting branch yields nothing else) ...
  col=2: ... yields [2,0,3,1] -> "..Q.", "Q...", "...Q", ".Q.."
  col=3: ... no solutions ...

result = [
  [".Q..", "...Q", "Q...", "..Q."],
  ["..Q.", "Q...", "...Q", ".Q.."],
]
```

Two solutions for N=4, as expected. The pruning sets eliminate the bulk of the search.

---

## Examine · cost

- **Time:** Worst case `O(N!)` — `N!` ways to assign N queens to N columns with the row constraint implicit. The pruning sets eliminate most of these; for N=8 the actual recursion is approximately 2,000 nodes versus the naive `N! = 40,320`.
- **Space:** `O(N)` for the recursion stack, `O(N)` for the `path`, `O(N)` each for the three sets — total `O(N)`.
- **Trade-off:** vs. without the pruning sets — every candidate column would require walking the partial path to check for conflicts, an `O(N)` cost per check; the total time is `O(N!) * O(N) = O(N * N!)`. The sets reduce per-check work from `O(N)` to `O(1)`, an N-fold speedup.

---

## Stretch

- **The bitmask form.** Replace the three sets with three integers: bit `c` of `cols` indicates "column `c` is used"; bit `(row - col + N - 1)` of `diag1` (offset to keep non-negative) indicates "diagonal `\` `row - col` is used"; bit `(row + col)` of `diag2` indicates "diagonal `/` `row + col` is used". Membership: `cols & (1 << c)`. Set: `cols |= (1 << c)`. Clear: `cols &= ~(1 << c)`. Roughly 3–5x faster in practice; the bit-twiddling is the Week 13 material.
- **Symmetry-breaking.** The first queen can be restricted to the top half of the first column (rows 0 to N/2 - 1); placements on the bottom half are mirror images. Halves the search space; doubles the output by reflecting each solution. Phase-3 stretch.
- **LC 52 — N-Queens II.** Return only the *count* of solutions, not the configurations. Same recursion; replace `result.append(render(path))` with `counter += 1`. The DP form (memoization) does **not** apply because the state `(row, cols, diag1, diag2)` is unique to every call — the cache never hits. This is the canonical "looks like DP but is actually backtracking" case; mention it.

---

## What "passing" looks like

| Dimension | Weight | What "yes" looks like |
|-----------|-------:|----------------------|
| Research constraints (pattern recognition) | 25% | 30-second memo at the top; "constraint satisfaction with three pruning sets"; the diagonal indexing (`row - col`, `row + col`) defended |
| Assess options | 15% | Numbered steps; the four state mutations on choose mirrored by four unchoose |
| Make the solution (correctness) | 25% | N=4 returns 2 solutions; N=8 returns 92; N=1 returns 1; render is correct |
| Make the solution (style) | 10% | Type hints; docstring; PEP 8 |
| Examine (defense) | 25% | `O(N!)` worst case with pruning-set speedup; bitmask form mentioned; LC 52 connection noted |

The diagonal indexing is the most-missed detail. Most candidates can articulate "one queen per row" and "track columns"; the move that separates senior signal is naming `row - col` and `row + col` as the two diagonal coordinates and defending why each is constant on its diagonal.
