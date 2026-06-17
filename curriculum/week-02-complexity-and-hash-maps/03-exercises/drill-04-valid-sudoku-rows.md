# Drill 4 — Valid Sudoku (Rows / Cols / Boxes)

> **Pattern:** Hash set × 3 (one per axis of constraint)
> **Difficulty:** Medium
> **Target solve time:** 25 minutes
> **Why fourth:** the first drill where you maintain *multiple* hash structures simultaneously. Practice in keeping state organized.

## Problem statement

Determine if a 9 × 9 Sudoku board is **valid** under these rules — note: we are validating, not solving, and **empty cells (denoted `'.'`) are allowed**:

1. Each row contains the digits `1-9` without repetition.
2. Each column contains the digits `1-9` without repetition.
3. Each of the 9 sub-boxes (3 × 3) of the grid contains the digits `1-9` without repetition.

The board is given as a `9 × 9` list of lists of characters (digits `'1'-'9'` or `'.'` for empty).

**Examples:**

- A standard solved board → `True`
- A board with `'8'` appearing twice in the first column → `False`
- A board with all `'.'`s → `True` (no constraint violations)

## UMPIRE checklist

- [ ] **U:** Restate. Confirm: 9×9 board, characters not integers, `'.'` is empty and *does not* count as a value. We are *validating* — not checking solvability. Repeats within row, column, or 3×3 box are the only failure modes.
- [ ] **M:** Three hash *sets* per axis — `rows[i]`, `cols[j]`, `boxes[(i//3, j//3)]`. Single pass over the 81 cells; for each non-empty cell, check all three sets; if any contains the value, return False; else add to all three.
- [ ] **P:** Initialize `rows = [set() for _ in range(9)]`, `cols = [set() for _ in range(9)]`, `boxes = {}` (or `defaultdict(set)`). Double-loop `i, j` over the 9×9 grid. Skip `'.'`. Box key is `(i // 3, j // 3)`. Membership check, then add. Return True at the end.
- [ ] **I:** Implement. Use `defaultdict(set)` for boxes to avoid the "key not found" branch.
- [ ] **R:** Trace at least the row check: two `'5'`s in row 0 → first one adds, second one's membership returns True → function returns False. Trace a clean row → adds, never finds, falls through.
- [ ] **E (graded):** Time **O(1)** — the board is fixed at 81 cells; each cell does at most three constant-time set operations. (For a general n×n Sudoku, it's O(n²).) Space **O(1)** for the same reason — each set holds at most 9 elements. Tradeoff: you could use bitmasks instead of sets (one 9-bit int per row / col / box), reducing constant-factor memory but not the class. Improvement: none meaningful at this size; the operation is fast.

## Acceptance criteria

- Code passes `timed_runner.py` for `is_valid_sudoku`.
- Write-up at `umpire-writeups/c2-week-02/drill-04-valid-sudoku-rows.md`.
- Evaluate section discusses *both* "fixed-size board O(1)" and "general n×n board O(n²)" framings. This is the interview discriminator.
- Recording ≥12 minutes.

## Function signature

```python
def is_valid_sudoku(board: list[list[str]]) -> bool:
    """Return True iff the partially-filled 9x9 board violates no Sudoku rule."""
    ...
```

## Common bugs to catch in Review

- **Wrong box key.** `(i, j) // 3` is invalid Python; you need `(i // 3, j // 3)` — separate integer divisions per axis.
- **Counting `'.'` as a value.** Skip empty cells — they're allowed to repeat.
- **Mistreating characters vs integers.** Cells are characters: `'5'`, not `5`. Comparing `cell == 5` is always False.
- **Using one shared set instead of three.** Each axis needs its own. Combining row + col + box into one set treats a row-9 conflict as the same as a column-9 conflict — usually wrong.
- **Allocating sets inside the loop body.** Hoist them outside.

## A cleaner one-pass alternative

Instead of three separate structures, you can encode each "I've seen value X in row r" as a *string* `f"r{r}={X}"`, and just maintain one set of those strings:

```python
def is_valid_sudoku(board: list[list[str]]) -> bool:
    seen = set()
    for i in range(9):
        for j in range(9):
            v = board[i][j]
            if v == '.':
                continue
            r = f"r{i}={v}"
            c = f"c{j}={v}"
            b = f"b{i//3},{j//3}={v}"
            if r in seen or c in seen or b in seen:
                return False
            seen.add(r); seen.add(c); seen.add(b)
    return True
```

It compresses three sets into one. The complexity class is identical; the code is debatably cleaner or worse depending on taste. **Mention this alternative in your Evaluate section** — that's the "I considered another structure" judgment signal.

## Stretch

**Sudoku Solver** (LeetCode 37). Backtracking — Week 8's territory. Bookmark it.

Next: [Drill 5 — Longest Consecutive Sequence](./drill-05-longest-consecutive-sequence.md).
