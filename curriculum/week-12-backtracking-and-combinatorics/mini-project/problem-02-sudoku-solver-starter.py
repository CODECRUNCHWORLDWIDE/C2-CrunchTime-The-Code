"""Mini-project Problem 2 - Sudoku Solver (LeetCode 37).

Pattern: backtracking with three pruning sets per row, column, and 3x3 box.
See Lecture 3 section 3.

Problem statement
-----------------
Write a program to solve a sudoku puzzle by filling the empty cells.

A sudoku solution must satisfy all of the following rules:
- Each of the digits 1-9 must occur exactly once in each row.
- Each of the digits 1-9 must occur exactly once in each column.
- Each of the digits 1-9 must occur exactly once in each of the nine 3x3
  sub-boxes of the grid.

The '.' character indicates empty cells. You may assume the input has
exactly one unique solution.

Constraints (LeetCode):
- board.length == board[i].length == 9.
- Each board[i][j] is either '.' or a digit '1'-'9'.
- The input puzzle has a unique solution.

UMPIRE checklist
----------------
- [ ] U: Restate. Fill the '.' cells of a 9x9 sudoku board with digits 1-9
        such that every row, column, and 3x3 box contains each digit exactly
        once. Mutate the board in place; return None. The input is
        guaranteed to have exactly one solution.
- [ ] M: Backtracking with three pruning sets. State = (board) plus
        rows[9], cols[9], boxes[9] each Set[str]. Precompute the constraint
        sets from the initial filled cells; precompute the list of empty
        cells. Recurse over the empty cells in order; for each, try digits
        1-9, check three sets in O(1), place if valid, recurse, undo on
        failure. Return True on the first complete board; the recursion
        unwinds.
- [ ] P: Pre-scan: for r, c in range(9): if board[r][c] == '.', append
        (r, c) to empties; else add board[r][c] to rows[r], cols[c],
        boxes[box_index(r, c)]. Define backtrack(idx): if idx == len(empties),
        return True. r, c = empties[idx]; b = box_index(r, c). For d in
        "123456789": if d not in rows[r], cols[c], boxes[b]: place d in
        board and three sets; if backtrack(idx + 1): return True; undo d.
        Return False.
- [ ] I: Use box_index(r, c) = (r // 3) * 3 + (c // 3). Use a list of
        Set[str] for rows, cols, boxes - lookup and insertion are O(1).
        Mutate board[r][c] in place.
- [ ] R: Trace the LC 37 sample. Expected: a complete valid board.
- [ ] E: Worst-case time O(9^M) where M is the number of empty cells -
        exponential in M. The pruning sets cut this drastically; LC 37
        cases solve in microseconds. Space O(81) for sets + O(M) recursion.

References
----------
- Lecture 3, section 3 (sudoku solver):
  ../lecture-notes/03-grid-backtracking-and-constraint-satisfaction.md
- LeetCode 37: https://leetcode.com/problems/sudoku-solver/
- Peter Norvig - Solving Every Sudoku Puzzle: https://norvig.com/sudoku.html
"""

from __future__ import annotations

from typing import List


def solve_sudoku(board: List[List[str]]) -> None:
    """Solve the sudoku puzzle by mutating the board in place.

    The harness passes `board` as a 9x9 grid of '.' and '1'-'9'. The
    function must mutate the board so that every cell contains a digit
    and the row, column, and box constraints are all satisfied. Returns
    None.

    Replace the body with your solution. The signature and docstring above
    are part of the spec.
    """
    # TODO: implement the cell-iteration plus digit-trial backtracking.
    # Hint:
    #   rows: List[set] = [set() for _ in range(9)]
    #   cols: List[set] = [set() for _ in range(9)]
    #   boxes: List[set] = [set() for _ in range(9)]
    #   empties: List[Tuple[int, int]] = []
    #
    #   def box_index(r: int, c: int) -> int:
    #       return (r // 3) * 3 + (c // 3)
    #
    #   for r in range(9):
    #       for c in range(9):
    #           if board[r][c] == '.':
    #               empties.append((r, c))
    #           else:
    #               d = board[r][c]
    #               rows[r].add(d); cols[c].add(d); boxes[box_index(r, c)].add(d)
    #
    #   def backtrack(idx: int) -> bool:
    #       if idx == len(empties):
    #           return True
    #       r, c = empties[idx]; b = box_index(r, c)
    #       for d in "123456789":
    #           if d in rows[r] or d in cols[c] or d in boxes[b]:
    #               continue
    #           board[r][c] = d
    #           rows[r].add(d); cols[c].add(d); boxes[b].add(d)
    #           if backtrack(idx + 1):
    #               return True
    #           board[r][c] = '.'
    #           rows[r].remove(d); cols[c].remove(d); boxes[b].remove(d)
    #       return False
    #
    #   backtrack(0)
    _ = board  # silence unused-variable lint
    return None


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 problem-02-sudoku-solver-starter.py`.
# ---------------------------------------------------------------------------


def _is_valid_solution(board: List[List[str]]) -> bool:
    """Check that the board is a valid completed sudoku."""
    for r in range(9):
        if set(board[r]) != set("123456789"):
            return False
    for c in range(9):
        if set(board[r][c] for r in range(9)) != set("123456789"):
            return False
    for br in range(3):
        for bc in range(3):
            cells = [
                board[br * 3 + dr][bc * 3 + dc]
                for dr in range(3)
                for dc in range(3)
            ]
            if set(cells) != set("123456789"):
                return False
    return True


def _matches_givens(filled: List[List[str]], original: List[List[str]]) -> bool:
    """Verify that the solver did not overwrite the pre-filled cells."""
    for r in range(9):
        for c in range(9):
            if original[r][c] != '.' and original[r][c] != filled[r][c]:
                return False
    return True


def _clone(board: List[List[str]]) -> List[List[str]]:
    return [row[:] for row in board]


def _run_self_tests() -> None:
    """Run the LC 37 sample puzzle plus an easy case."""
    failures = 0

    # Case 1: LC 37 sample puzzle.
    lc_sample: List[List[str]] = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]
    original = _clone(lc_sample)
    solve_sudoku(lc_sample)
    label = "LC 37 sample"
    if _is_valid_solution(lc_sample) and _matches_givens(lc_sample, original):
        print(f"[OK  ] {label}: valid solution, givens preserved")
    else:
        failures += 1
        print(f"[FAIL] {label}: board after solve = ")
        for row in lc_sample:
            print(f"        {row}")
        if not _is_valid_solution(lc_sample):
            print("       Reason: board does not satisfy sudoku constraints")
        if not _matches_givens(lc_sample, original):
            print("       Reason: a pre-filled cell was overwritten")

    # Case 2: nearly-complete puzzle (only one empty cell).
    one_empty: List[List[str]] = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "."],
    ]
    original = _clone(one_empty)
    solve_sudoku(one_empty)
    label = "single empty cell"
    if _is_valid_solution(one_empty) and one_empty[8][8] == "9":
        print(f"[OK  ] {label}: filled to 9")
    else:
        failures += 1
        print(f"[FAIL] {label}: got board[8][8] = {one_empty[8][8]}, expected 9")

    if failures:
        raise AssertionError(f"{failures} assertion(s) failed; implement solve_sudoku.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
