# Week 12 — Mini-Project: Palindrome Partitioning + Sudoku Solver

The week's deliverable. Two backtracking write-ups demonstrating the two halves of the lecture material: **combinatorial enumeration with constraint pruning** (palindrome partitioning) and **constraint satisfaction** (sudoku solver).

The mini-project is graded on the **same five dimensions** as the homework — Match, Plan, Implement (Correctness), Implement (Style), Evaluate. The weights are identical. The difference is that the mini-project asks for the **full UMPIRE narration** end-to-end, recorded and committed under `umpire-writeups/c2-week-12/mini-project/`, with both starter files completed and shipped under `mini-project/c2-week-12/`.

This is the artifact graders use to judge whether you have internalized backtracking. Half a week's homework is the warm-up; the mini-project is the proof.

---

## Problem 1 — Palindrome Partitioning (LC 131)

> *Given a string `s`, partition `s` such that every substring of the partition is a palindrome. Return all possible palindrome partitionings of `s`.*

**Constraints (LeetCode).** `1 <= len(s) <= 16`; `s` contains only lowercase English letters.

**The pattern.** Backtracking — string partitioning with palindrome constraint (Lecture 2 §4).

**The state.** `(start_index, path)` where `path` is the list of palindromic pieces. At each level, try every `end` from `start + 1` to `n`; if `s[start:end]` is a palindrome, choose, recurse, unchoose. Record at leaves where `start == n`.

**The pruning.** Constraint-propagation — the palindrome check on each candidate piece. The check is `O(end - start)` per call; an optional optimization is to precompute a 2D boolean palindrome table in `O(n^2)` time and space.

**The starter file.** [problem-01-palindrome-partitioning-starter.py](./problem-01-palindrome-partitioning-starter.py)

**What to ship.**

1. A complete implementation of `partition(s: str) -> List[List[str]]`.
2. A 30-second pattern-recognition memo at the top of the write-up.
3. A worked trace on at least one example (`s = "aab"` or `s = "raceacar"`).
4. The time and space complexity with derivation.
5. One mentioned variant (precomputed palindrome table) and its trade-off.

**Acceptance.** The included self-test block passes. The output for `s = "aab"` is `[["a", "a", "b"], ["aa", "b"]]` (order-independent). The output for `s = "a"` is `[["a"]]`. The output for `s = "abba"` is `[["a", "b", "b", "a"], ["a", "bb", "a"], ["abba"]]`.

---

## Problem 2 — Sudoku Solver (LC 37)

> *Write a program to solve a sudoku puzzle by filling the empty cells. A sudoku solution must satisfy: each of the digits 1-9 must occur exactly once in each row, each column, and each of the nine 3x3 sub-boxes of the grid. The '.' character indicates empty cells. You may assume there will be only one unique solution.*

**Constraints (LeetCode).** The board is a 9x9 grid of characters where each cell is either '.' or a digit '1'-'9'. The input is guaranteed to have a unique solution.

**The pattern.** Backtracking — constraint satisfaction with three pruning sets (Lecture 3 §3).

**The state.** The board itself (mutated in place) plus three `Set[str]` per row, column, and box. The recursion finds the next empty cell; for each digit 1–9, checks the three constraint sets; places the digit if all three pass; recurses; undoes on failure.

**The pruning.** Constraint-propagation — three `O(1)` set membership checks per candidate digit (row, column, 3x3 box). Without the sets, every check would walk the board for `O(81)` cost; with the sets, the check is `O(1)`.

**The starter file.** [problem-02-sudoku-solver-starter.py](./problem-02-sudoku-solver-starter.py)

**What to ship.**

1. A complete implementation of `solve_sudoku(board: List[List[str]]) -> None` that mutates `board` in place.
2. A 30-second pattern-recognition memo at the top of the write-up.
3. A discussion of the box-index formula `(r // 3) * 3 + (c // 3)` — why it produces a unique index for each of the nine 3x3 boxes.
4. The worst-case time complexity with derivation, and the actual runtime on the LC 37 sample puzzle (microseconds for the precomputed-set form).
5. One mentioned variant — the most-constrained-cell heuristic, or Peter Norvig's constraint-propagation method — and its trade-off.

**Acceptance.** The included self-test block passes. The LC 37 sample puzzle solves correctly. The board is mutated in place (the function returns `None`).

---

## How to do the write-up

For each problem, produce one Markdown file under `umpire-writeups/c2-week-12/mini-project/`:

1. **`problem-01-palindrome-partitioning.md`** — UMPIRE narration for Problem 1.
2. **`problem-02-sudoku-solver.md`** — UMPIRE narration for Problem 2.

Each write-up has the canonical six sections:

- **Understand:** restate the problem in your words; identify the inputs and outputs; note any tricky edge cases (e.g., a length-1 string is a valid palindrome partition of itself).
- **Match:** the 30-second pattern-recognition memo at the top; name the state design, the pruning, the recording rule.
- **Plan:** numbered steps; pseudocode is optional but encouraged.
- **Implement:** the working code, with type hints everywhere.
- **Review:** a worked trace on one example; verify the output by hand.
- **Evaluate:** time and space with derivation; one variant mentioned with its trade-off.

The recording is the single most useful artifact in the mini-project. A 10–15 minute video walkthrough — you reading your write-up aloud, talking through the state design, the pruning, the leaf-copy discipline — is the closest simulation of an interview that a portfolio can provide.

---

## How this connects to the rest of the curriculum

Palindrome partitioning is the canonical **string-partition backtracking**. The state design (`(start_index, path)`) and the constraint-propagation prune (palindrome check) generalize to:

- Word break II (LC 140) — same state, dictionary lookup as the prune.
- Restore IP addresses (LC 93, homework) — same state, value-and-length validation as the prune.
- Split array largest sum (LC 410) — DP version of the same shape.

Sudoku is the canonical **constraint-satisfaction backtracking**. The state design (pruning sets per dimension) generalizes to:

- N-Queens (LC 51, challenge) — three pruning sets per row, both diagonals.
- Word search (LC 79, challenge) — visited set as the pruning set.
- Solving any Latin-square or graph-coloring problem — pruning set per constraint dimension.

The two together — combinatorial enumeration plus constraint satisfaction — cover the two halves of the backtracking universe. By Sunday of Week 12 you have the template and the two largest applications in your write-up portfolio.

---

## Acceptance for the week

The week's mini-project is complete when:

- Both `mini-project/c2-week-12/problem-01-palindrome-partitioning.py` and `mini-project/c2-week-12/problem-02-sudoku-solver.py` are committed with passing self-tests.
- Both `umpire-writeups/c2-week-12/mini-project/problem-01-palindrome-partitioning.md` and `umpire-writeups/c2-week-12/mini-project/problem-02-sudoku-solver.md` are committed.
- A recording of at least one of the two write-ups is committed or linked (10–15 minutes).
- The Week 12 retrospective notes the most-useful and the most-challenging part of the mini-project.

The retrospective is the artifact you re-read in Week 16 (before Mock #3) and in Week 20 (before the Phase 2 capstone). It is the canonical evidence that the week's pattern recognition stuck.

---

*If you find errors in this mini-project, please open an issue or send a PR. Future learners will thank you.*
