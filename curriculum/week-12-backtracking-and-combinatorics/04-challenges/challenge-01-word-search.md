# Challenge 1 — Word Search (LC 79)

> *Given an `m x n` grid of characters `board` and a string `word`, return `True` iff `word` exists in the grid. The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.*

**Constraints (LeetCode).**

- `m == len(board)`, `n == len(board[0])`.
- `1 <= m, n <= 6`.
- `1 <= len(word) <= 15`.
- `board` and `word` consist of lowercase and uppercase English letters.

**The deliverable.** A full UMPIRE write-up published to `umpire-writeups/c2-week-12/challenge-01/`, recorded as a `>= 10`-minute video walkthrough, with the code committed under `challenges/c2-week-12/word-search.py`.

---

## Understand

Re-read the prompt twice. Note the four required behaviors:

1. **The word may start anywhere on the board.** The outer loop iterates every cell as a candidate starting point.
2. **Moves are four-directional (up, down, left, right).** No diagonal moves; no skipping cells.
3. **Each cell may be used at most once per traced word.** The visited set is path-local; cells used in a failed branch must be available for a different branch.
4. **The first match suffices.** Return `True` on first success; the outer loop short-circuits and the recursion unwinds.

Hand-walk on `board = [["A","B","C","E"], ["S","F","C","S"], ["A","D","E","E"]], word = "SEE"`:

```
Start cells with board[r][c] == 'S':
  (1, 0): 'S'
  (1, 3): 'S'

From (1, 0):
  Try neighbors for 'E': (0, 0)='A', (2, 0)='A', (1, 1)='F'. None match. Fail.

From (1, 3):
  Try neighbors for 'E': (0, 3)='E' OK; (2, 3)='E' OK.
    From (0, 3): visited = {(1,3), (0,3)}.
      Try neighbors for 'E': (0, 2)='C', (1, 3) visited. Fail.
    From (2, 3): visited = {(1,3), (2,3)}.
      Try neighbors for 'E': (2, 2)='E' OK.
        visited = {(1,3), (2,3), (2,2)}. len(word) = 3. SUCCESS.

Return True.
```

The traced path is `(1, 3) -> (2, 3) -> (2, 2)`, which spells `S -> E -> E`. The first success unwinds.

The senior-grade observation: brute-force enumeration of paths is `O((m*n) * 4^L)` where `L = len(word)`. For `m*n = 36, L = 15`, that is `~10^11` — infeasible. The character-match prune at each step cuts this drastically because most paths fail within the first few characters.

---

## Match

The 30-second pattern-recognition memo (put this at the top of your write-up):

> *Feasibility problem on a 2D grid. Backtracking with a visited set. State = (row, col, word_index). At each cell, check four early-out conditions in order: leaf (word_index == len(word)), bounds, visited, character match. Mark visited; recurse into four neighbors with word_index + 1; unmark on backtrack. Outer loop iterates every cell as a starting point. Return True on first success; the recursion unwinds. Worst-case time O(m * n * 4^L); space O(L) for recursion plus visited set. The in-place variant (board[r][c] = '#') saves the visited set.*

**Why not DP?** Two reasons:

1. The **path** is part of the state — the visited set is path-specific. The same `(r, c, idx)` triple reached via different paths has different "available" neighbors. The DP cache key would need to include the visited set, which is unique per call. The cache never hits.
2. The prompt asks "does the word exist," not "count the words" or "find the longest match." Feasibility plus path-dependent state is the backtracking signature.

**Why not BFS?** BFS finds shortest paths; the prompt does not ask for a shortest path. BFS does not handle the "each cell at most once" constraint naturally — a BFS visited set is global, not path-local; cells used in one BFS branch are unavailable in another. Backtracking with `unchoose` is the correct discipline.

---

## Plan

1. Extract `rows = len(board)` and `cols = len(board[0])`. Handle the empty-board edge case (return `False` if `rows == 0` or `cols == 0`).
2. Initialize `visited: Set[Tuple[int, int]] = set()`.
3. Define `backtrack(r, c, idx) -> bool`:
   - **Leaf check:** if `idx == len(word)`, return `True`.
   - **Bounds check:** if `r < 0 or r >= rows or c < 0 or c >= cols`, return `False`.
   - **Visited check:** if `(r, c) in visited`, return `False`.
   - **Match check:** if `board[r][c] != word[idx]`, return `False`.
   - **Choose:** `visited.add((r, c))`.
   - **Recurse:** for each of the four neighbors `(r+dr, c+dc)`, call `backtrack(r+dr, c+dc, idx+1)`. If any returns `True`, propagate `True` immediately.
   - **Unchoose:** `visited.remove((r, c))`. Return `False`.
4. For each starting cell `(r, c)`, call `backtrack(r, c, 0)`. Return `True` on first success.
5. After the outer loop, return `False`.

The four early-out checks must be ordered: leaf first (cheapest), bounds second (next cheapest), visited third (set lookup is `O(1)`), match last (same `O(1)` cost as visited but allows reading `board[r][c]` only after the cell is known to be valid).

---

## Implement

```python
from __future__ import annotations

from typing import List, Set, Tuple


def exist(board: List[List[str]], word: str) -> bool:
    """Return True iff word can be traced through the board using 4-direction adjacency."""
    rows = len(board)
    cols = len(board[0]) if rows else 0
    if rows == 0 or cols == 0 or not word:
        return False

    visited: Set[Tuple[int, int]] = set()

    def backtrack(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        if (r, c) in visited:
            return False
        if board[r][c] != word[idx]:
            return False
        visited.add((r, c))
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if backtrack(r + dr, c + dc, idx + 1):
                return True
        visited.remove((r, c))
        return False

    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0):
                return True
    return False
```

Twenty-nine lines. The four early-out conditions are ordered for cheapest-first; the four-direction loop is the canonical neighbor iterator; the outer loop iterates every starting cell.

**The in-place variant.** A space-optimal alternative replaces the `visited` set with in-place mutation of the board:

```python
def exist_inplace(board: List[List[str]], word: str) -> bool:
    """Word search with in-place visited marking. O(L) space, not O(rows * cols)."""
    rows = len(board)
    cols = len(board[0]) if rows else 0

    def backtrack(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[idx]:
            return False
        tmp = board[r][c]
        board[r][c] = '#'
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if backtrack(r + dr, c + dc, idx + 1):
                board[r][c] = tmp
                return True
        board[r][c] = tmp
        return False

    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0):
                return True
    return False
```

Twenty-six lines. The `tmp` variable captures the original character; restoring on both success and failure paths. The marker `'#'` works because it cannot equal any letter in `word`, so the match check rejects revisits without an explicit visited check.

The two forms are equivalent in correctness. The in-place form saves `O(rows * cols)` worst-case space (when most cells are visited) at the cost of temporarily mutating the input. The set form is more honest (no input mutation) and is what most production code would write; the in-place form is the senior-grade interview move.

---

## Review

Trace `board = [["A","B","C","E"], ["S","F","C","S"], ["A","D","E","E"]], word = "ABCCED"`.

```
Start (0,0): board[0][0]='A' == word[0]='A'. visited={(0,0)}.
  Try (-1,0): out of bounds.
  Try (1,0): board[1][0]='S' != word[1]='B'. Fail.
  Try (0,-1): out of bounds.
  Try (0,1): board[0][1]='B' == word[1]='B'. visited={(0,0),(0,1)}.
    Try (-1,1): out of bounds.
    Try (1,1): 'F' != 'C'. Fail.
    Try (0,0): in visited. Fail.
    Try (0,2): 'C' == word[2]='C'. visited={(0,0),(0,1),(0,2)}.
      Try (-1,2): out of bounds.
      Try (1,2): 'C' == word[3]='C'. visited={...,(1,2)}.
        Try (0,2): visited. Fail.
        Try (2,2): 'E' != word[4]='C'? Wait, word[4]='E'. board[2][2]='E'==word[4]='E'.
                   visited={...,(2,2)}.
          Try (1,2): visited.
          Try (3,2): out of bounds.
          Try (2,1): 'D' == word[5]='D'. visited={...,(2,1)}. len(word)=6.
            idx=6 == len(word). Return True.
          (propagates True up the stack)
        Return True.
      Return True.
    Return True.
  Return True.
Return True.
```

Path: `(0,0) -> (0,1) -> (0,2) -> (1,2) -> (2,2) -> (2,1)` spells `A -> B -> C -> C -> E -> D`. Match.

Also trace the failure case `board = [["A","B","C","E"], ["S","F","C","S"], ["A","D","E","E"]], word = "ABCB"`:

```
Start (0,0): 'A' matches.
  Try (0,1): 'B' matches.
    Try (0,2): 'C' matches.
      Try neighbors for 'B': (0,1) visited, (0,3)='E', (1,2)='C'. None match 'B'. Fail.
      Unchoose (0,2).
    Try (1,1): 'F' != 'C'. Fail.
    Unchoose (0,1).
  Try (1,0): 'S' != 'B'. Fail.
  Unchoose (0,0).
(No other starting cells have 'A'.)
Wait, (2,0) is also 'A'.
Start (2,0): 'A' matches.
  Try (2,1): 'D' != 'B'. Fail.
  Try (1,0): 'S' != 'B'. Fail.
  Unchoose.
Return False.
```

No path spells `"ABCB"`. The output is `False`.

---

## Evaluate

- **Time:** `O(m * n * 4^L)` worst case where `m, n` are the grid dimensions and `L = len(word)`. The outer loop iterates `m * n` cells; from each starting cell, the recursion branches up to 4 ways per level for up to `L` levels. The character-match prune cuts this drastically in practice — most paths fail within the first 1–2 characters.
- **Space:** `O(L)` for the recursion stack. The `visited` set is at most `L` cells (the cells currently on the path). The in-place variant has `O(L)` recursion-stack space and `O(1)` additional state (the `tmp` variable per frame).
- **Trade-off:** vs. building a trie of the board's contents — the trie form is the canonical optimization when there are *many* words to search (Word Search II, LC 212). For a single word (LC 79), the trie overhead is not worth it.

---

## Stretch

- **Implement the trie-backed variant** for Word Search II (LC 212), which searches for multiple words simultaneously. The trie pre-organizes the word set; the grid backtracking descends both the trie and the grid in lockstep. This is the senior-grade demonstration that the W9 trie material composes with the W12 backtracking material.
- **Add a fast pre-check** that returns `False` immediately if the board does not contain enough of each character in `word`. Count characters in the board (one pass) and in `word`; if any character in `word` appears more times than in the board, return `False`. The pre-check is `O(m*n + L)` and rejects impossible cases before the recursion starts.
- **Optimize the starting-cell order** by trying cells that match `word[0]` and have the most-rare character match first. A heuristic: count occurrences of each character in the board; start from cells where `board[r][c] == word[0]` ordered by ascending count of `word[L - 1]` in the board (or another rarity metric). The heuristic can cut runtime by 2–10x on adversarial inputs. Phase-3 stretch.

---

## What "passing" looks like

Your write-up is graded on five dimensions:

| Dimension | Weight | What "yes" looks like |
|-----------|-------:|----------------------|
| Match (Pattern Recognition) | 25% | 30-second memo at the top; "backtracking on a 2D grid with a visited set"; alternatives rejected (DP, BFS) with reason |
| Plan | 15% | Numbered steps; the four early-out conditions in the right order; the four-direction iterator |
| Implement (Correctness) | 25% | All LC sample cases pass; the unchoose step is present; the leaf check is the first condition |
| Implement (Style) | 10% | Type hints everywhere; docstring on every function; PEP 8; idiomatic Python |
| Evaluate (Defense) | 25% | `O(m * n * 4^L)` time with derivation; in-place variant mentioned; trade against trie-based form (LC 212) named |

The mini-project will ask you to compose the visited-set discipline with the cell-iteration discipline of sudoku. Practice both forms (set and in-place) so the choice is reflexive.
