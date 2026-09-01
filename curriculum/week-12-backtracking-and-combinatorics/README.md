# Week 12 — Backtracking and Combinatorics

```
┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐
│ F │  │ R │  │ A │  │ M │  │ E │
└───┘  └───┘  └───┘  └───┘  └───┘
```

> *Week 11 installed the dynamic-programming pipeline — the disciplined route from a brute-force recursion through `functools.lru_cache` to a bottom-up tabulation. Week 12 installs the **other** disciplined recursion: **backtracking**, the choose-explore-unchoose template that enumerates every solution to a combinatorial decision problem. Subsets, permutations, combinations, combination sum, palindrome partitioning, word search, N-Queens, sudoku solver. The Research-constraints skill: what tells you "this is a backtracking problem" — the prompt asks for **all** solutions, not the count or the optimum; the search tree has clear branching; constraints prune entire subtrees. State + pruning + visited-set patterns. The mechanical template: `choose -> recurse -> unchoose`. By Sunday you can read a problem and say, in 30 seconds, "this enumerates subsets / permutations / partitions, the decision at each level is `<X>`, the prune is `<Y>`, the unchoose step is `<Z>`," and you can ship the recursion with the path-array mutation discipline that does not produce duplicate or aliased outputs.*

Welcome to Week 12 of **C2 · CrunchTime — The Code** — the eighth week of Phase 2 and the second of the two enumerated-search weeks. Last week installed dynamic programming — the disciplined recursion that **caches** intermediate answers and rolls them into a table. This week installs **backtracking** — the disciplined recursion that **does not** cache, because the problem demands enumeration of **all** solutions, not just the optimum. The two recursions are siblings: same call structure, opposite output discipline. A senior candidate can name which sibling applies in 30 seconds and write the right one in 15 minutes.

The misconception this week corrects: learners who finished Week 11 reach for `@lru_cache` on every recursive prompt. Backtracking problems break this reflex because the **path matters**, not just the final value at the leaf. The state at each node is mutable; caching a mutable path is wrong; the same `(i, partial_path)` pair never recurs *with the same continuation* anyway, so memoization buys nothing. The recognition shift this week: when the prompt says "return all subsets," "list every permutation," "find one valid board," "enumerate every partition" — it is backtracking, not DP.

The mechanical template is three lines: `choose`, `recurse`, `unchoose`. The `choose` step appends to the path or marks a cell visited; the `recurse` step descends with the same path, mutated; the `unchoose` step pops the path back to its pre-choose state. The discipline is: the path on entry to a function call must equal the path on exit. Any function that fails this invariant produces aliased or duplicate results.

By Sunday of Week 12 you will:

- **Recognize** a backtracking problem in 30 seconds by checking three boxes: the prompt asks for **all** solutions (or one valid configuration); the decision space at each level is discrete and finite; pruning is possible at internal nodes (constraints can eliminate entire subtrees early).
- **Write** the choose-explore-unchoose template from memory, with the path-mutation discipline that returns a deep copy of the path at every leaf and pops the path on exit from each recursive frame.
- **Articulate the difference between backtracking and DP** out loud. DP caches `(state) -> value` because the same state recurs with the same continuation; backtracking does not cache because the **path** is part of the output, the same `(remaining-input, partial-path)` pair never recurs, and the optimization target is "every solution," not "one optimum."
- **Implement subsets, permutations, combinations** from memory. The three are the canonical scaffolding of every other backtracking problem; if these three are reflexive, combination sum and palindrome partitioning are 10-minute variants.
- **Implement combination sum** as a backtracking with **pruning by partial sum** and **deduplication by sorting plus index-skip**. The prune is the senior signal — without it the recursion explores branches that cannot lead to a solution.
- **Implement word search** as a backtracking on a 2D grid with a `visited` set (or in-place character mutation) for the cycle prevention. State: `(row, col, word_index)`. The visited discipline is the discriminator from DFS-with-memoization.
- **Implement palindrome partitioning** as a backtracking that splits a string into all palindromic partitions. The decision at each level is the **length** of the next piece; the prune is the palindrome check on each candidate piece.
- **Implement N-Queens** as a backtracking on a chessboard with three pruning sets (column, two diagonals). The state representation (one row per recursive level) is the senior-grade move; placing one queen per row makes the row constraint implicit.
- **Implement the sudoku solver** as a backtracking that picks the next empty cell and tries digits 1–9 with three constraint checks (row, column, 3x3 box). The cell-iteration order plus the box-coordinate computation are the discriminators.
- Have solved **three backtracking exercises** — subsets (the canonical warm-up), permutations (the canonical second), combination sum (the canonical prune-and-skip).
- Have shipped **one challenge** (word search with full FRAME narration) plus an optional stretch (N-Queens with all three pruning sets defended).
- Have shipped the quiz, the homework, and the **mini-project**: one combinatorial enumeration (palindrome partitioning) plus one constraint-satisfaction (sudoku solver), each with the choose-explore-unchoose template narrated end to end.

---

## Learning objectives

By the end of this week, you will be able to:

- **Match a backtracking problem to its shape in 30 seconds.** The signal hierarchy: does the prompt ask for **all** solutions or to enumerate a configuration space (not the count, not the optimum); is the decision space at each level discrete and finite; can constraints prune internal subtrees; is the path part of the output? The four answers fully classify backtracking versus DP versus brute-force-with-pruning.
- **Implement the three-line template** as a reflex. Line 1: `choose` — append to the path or mark a cell visited. Line 2: `recurse` — call the function with the mutated state. Line 3: `unchoose` — pop the path or unmark the cell. The invariant: the state on entry equals the state on exit.
- **Defend the deep-copy discipline at leaves.** Appending `path[:]` (or `list(path)` or `tuple(path)`) to the results list copies the path *now*, before subsequent recursive calls mutate it. Forgetting the copy produces a results list where every entry aliases the same list and ends up empty after the final unchoose. The single most common backtracking bug.
- **Implement subsets** as a backtracking. State: `(start_index, path)`. Recurrence: at each `i` from `start` to `n - 1`, choose `nums[i]`, recurse with `start = i + 1`, unchoose. Record the path at every node (not just leaves) because every node is a valid subset.
- **Implement permutations** as a backtracking with a **used** set. State: `(used_set, path)`. Recurrence: at each `i` from `0` to `n - 1`, if `i` is not used, choose `nums[i]` and mark `i` used, recurse, unchoose and unmark. Record the path at the leaves only (path length equals `n`).
- **Implement combinations** as a backtracking. State: `(start_index, path)`. Recurrence: at each `i` from `start` to `n - 1`, choose `nums[i]`, recurse with `start = i + 1`, unchoose. Record at leaves where `len(path) == k`.
- **Implement combination sum** as a backtracking with **sum-based pruning**. State: `(start_index, remaining_target, path)`. Recurrence: at each `i` from `start` to `n - 1`, if `nums[i] <= remaining`, choose, recurse with `remaining - nums[i]` (and `start = i` because reuse is allowed), unchoose. Prune the entire `nums[i] > remaining` branch by sorting `nums` and breaking the inner loop early.
- **Implement palindrome partitioning** as a backtracking. State: `(start_index, path)`. Recurrence: at each `end` from `start + 1` to `n`, if `s[start:end]` is a palindrome, choose, recurse with `start = end`, unchoose. Record at the leaves where `start == n`.
- **Implement word search** as a 2D-grid backtracking with a `visited` set. State: `(row, col, word_index)`. Recurrence: at the current cell, if the character matches and the cell is unvisited, mark visited, recurse into the four neighbors, unmark.
- **Implement N-Queens** as a backtracking with three pruning sets. State: `(row, cols_used, diag1_used, diag2_used, path)`. Place one queen per row; for each candidate column, check three constraint sets in `O(1)` before recursing.
- **Implement the sudoku solver** as a backtracking that finds the next empty cell and tries digits 1–9. State: `(board)`. Recurrence: find next empty cell; for each digit 1–9, if it does not violate row, column, or box constraints, place the digit, recurse, undo. Return True on the first successful completion.
- **Articulate when backtracking is the only path.** Three cases: (1) the prompt asks for **all** solutions (DP cannot enumerate, only count); (2) the prompt asks for **one** valid configuration in a constraint-satisfaction problem (N-Queens, sudoku — no greedy structure, no overlapping subproblems); (3) the state space is too large for full enumeration but constraints prune aggressively (word search on a 10×10 grid). When any of the three signals fires, reach for backtracking.

---

## Prerequisites

- **Weeks 1–11 complete.** You have shipped FRAME write-ups for the heap pair (W8), the trie pair (W9), the graph pair (W10), and the DP pair (W11). You can write a recursion from memory and you can name the difference between memoization and tabulation.
- **Comfortable with recursion and the call stack.** Specifically, the discipline that a function's **local variables** are restored on return — but **mutable arguments** are not. The choose-explore-unchoose template depends on understanding that `path.append(x)` mutates the caller's list, not a local copy, and so an `unchoose` step (`path.pop()`) is required to restore the invariant.
- **Comfortable with list slicing and copying.** `path[:]` is a shallow copy; `list(path)` is a shallow copy; `copy.deepcopy(path)` is unnecessary for a list of ints or strings. The leaf-copy step `result.append(path[:])` is the one-line idiom; forgetting the `[:]` is the canonical bug.
- **Comfortable with set operations.** `visited.add(cell)`, `visited.remove(cell)`, `if cell in visited`. The N-Queens pruning sets, the word search visited set, and the permutations used set are all the same primitive.
- **Comfortable with 2D-grid traversal.** `for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]` is the canonical four-neighbor iterator; bounds checks (`0 <= r < rows and 0 <= c < cols`) precede the cell-content check. Identical to W7 (BFS/DFS on grids).

---

## Topics covered

- **The choose-explore-unchoose template** — the three-line backtracking recurrence; the invariant that the state on entry equals the state on exit
- **The leaf-copy discipline** — `result.append(path[:])` to deep-copy the path at each leaf; forgetting the copy produces an aliased result list
- **Subsets (LC 78)** — the canonical backtracking warm-up; record the path at every node, not just leaves
- **Permutations (LC 46)** — the canonical second backtracking; uses a `used` set to prevent re-selecting elements
- **Combinations (LC 77)** — the canonical third; records at leaves where `len(path) == k`
- **Combination sum (LC 39)** — backtracking with sum-based pruning; the prune is the senior signal
- **Subsets II / permutations II / combination sum II** — deduplication by sorting plus index-skip; the canonical "skip duplicates at the same level" idiom
- **Palindrome partitioning (LC 131)** — backtracking that splits a string into palindromic pieces; the per-level decision is the length of the next piece
- **Word search (LC 79)** — 2D-grid backtracking with a `visited` set; the in-place character mutation is the space-optimal variant
- **N-Queens (LC 51)** — backtracking with three pruning sets (column, two diagonals); placing one queen per row makes the row constraint implicit
- **Sudoku solver (LC 37)** — backtracking on a 9×9 grid with three constraint checks per candidate digit
- **Backtracking vs. DP — the recognition flowchart** — when caching helps (DP) versus when it does not (backtracking); the rule of thumb that "all solutions" or "one valid configuration" beats "the count" or "the optimum" almost always
- **Pruning — the four families** — feasibility (current state cannot reach a valid leaf), optimality (current state cannot improve the best so far), symmetry (current state is equivalent to an already-explored state), constraint-propagation (current state violates a constraint)

---

## Weekly schedule (intensive · 36h)

| Day | Focus | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project | Self-Study | Daily Total |
|-----|-------|---------:|----------:|-----------:|----------:|---------:|-------------:|-----------:|------------:|
| Monday | The choose-explore-unchoose template; subsets; exercise 1 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Tuesday | Permutations and combinations; exercise 2 prep | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Wednesday | Combination sum with pruning; exercise 3 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Thursday | Mini-project drafting; challenge ramp | 0h | 1h | 1h | 0.5h | 1h | 1.5h | 1h | 6h |
| Friday | Challenge (Word Search) | 0h | 0h | 2h | 0.5h | 1h | 1.5h | 1h | 6h |
| Saturday | Mini-project — palindrome partitioning + sudoku | 0h | 0h | 0h | 0.5h | 1h | 3h | 0h | 4.5h |
| Sunday | Quiz + retro + push | 0h | 0h | 0h | 0.5h | 0h | 4h | 0h | 4.5h |
| **Total** | | **6h** | **7h** | **3h** | **3h** | **6h** | **10h** | **3.5h** | **38.5h** |

(The week budgets ~36 hours; the table sums slightly higher to absorb the Phase-2 ramp. Drop 0.5h from Self-Study if 36h is your hard cap.)

**Mastery (10h/wk):** spread the same content over three calendar weeks. The mini-project lands in calendar Week 36 of the mastery pathway. See the [mastery study plan](../study-plans/mastery-1-year.md).

---

## How to navigate this week

| File | What's inside |
|------|---------------|
| [README.md](./README.md) | This overview |
| [resources.md](./resources.md) | Free readings + backtracking references + the three-line template cheatsheet + glossary additions |
| [lecture-notes/01-the-backtracking-template-and-the-three-warmups.md](./lecture-notes/01-the-backtracking-template-and-the-three-warmups.md) | The choose-explore-unchoose template, subsets, permutations, combinations, the leaf-copy discipline |
| [lecture-notes/02-pruning-and-deduplication-and-string-partitioning.md](./lecture-notes/02-pruning-and-deduplication-and-string-partitioning.md) | Combination sum, the four pruning families, deduplication by sorting plus index-skip, palindrome partitioning |
| [lecture-notes/03-grid-backtracking-and-constraint-satisfaction.md](./lecture-notes/03-grid-backtracking-and-constraint-satisfaction.md) | Word search, N-Queens, sudoku solver, the backtracking-vs-DP recognition flowchart |
| [exercises/README.md](./exercises/README.md) | Index of the three backtracking exercises and SOLUTIONS |
| [exercises/exercise-01-subsets.py](./exercises/exercise-01-subsets.py) | LC 78 — the canonical backtracking warm-up |
| [exercises/exercise-02-permutations.py](./exercises/exercise-02-permutations.py) | LC 46 — the canonical permutation backtracking |
| [exercises/exercise-03-combination-sum.py](./exercises/exercise-03-combination-sum.py) | LC 39 — backtracking with sum-based pruning |
| [exercises/SOLUTIONS.md](./exercises/SOLUTIONS.md) | Worked solutions with FRAME narration; consult after attempting each exercise |
| [challenges/README.md](./challenges/README.md) | Index of weekly challenges |
| [challenges/challenge-01-word-search.md](./challenges/challenge-01-word-search.md) | LC 79 deep-dive — 2D-grid backtracking with the visited-set discipline |
| [challenges/challenge-02-n-queens.md](./challenges/challenge-02-n-queens.md) | LC 51 — N-Queens with three pruning sets |
| [quiz.md](./quiz.md) | 10 pattern-recognition questions |
| [homework.md](./homework/README.md) | Six practice problems (~5 hrs) — three combinatorial, three constraint-satisfaction |
| [mini-project/README.md](./mini-project/README.md) | **Palindrome partitioning + sudoku solver** — the week's deliverable |

---

## Stretch goals

- **Read the LeetCode "Backtracking" tag** and skim 30 titles. For each, predict in 5 seconds: enumeration of all solutions, one valid configuration, or count-only (which would be DP)? Stretches the Research-constraints muscle harder than any exercise this week.
- **Re-derive the three-line template** without re-reading Lecture 1. State the template aloud; if you cannot, you do not yet own it. Re-read and re-derive until you can.
- **Read the Wikipedia "Backtracking" article** end-to-end (about 15 minutes). The "Description of the method" section is the canonical written defense of the choose-explore-unchoose template; the "Examples" section walks N-Queens and the eight queens puzzle.
- **Implement N-Queens with bitmask pruning sets** instead of Python sets. Three integers (one per direction: column, diag1, diag2) replace the three sets; the bit at position `c` indicates "column `c` is used" or "diag with offset `c` is used." Faster in practice; the bit-twiddling is a Phase-3 stretch.
- **Read the "Knight's tour problem" Wikipedia article.** The closed-tour and open-tour variants are the canonical "find one valid configuration on a chessboard" backtracking; Warnsdorf's heuristic for choosing the next move is the canonical optimization. Phase-3 stretch.
- **Implement sudoku with constraint propagation** (Peter Norvig's method). At each cell, narrow the candidate digit set by propagating "this digit is taken in this row/column/box." The combination of backtracking and constraint propagation is the senior-grade sudoku solver. Phase-3 stretch.

---

## What "done" looks like for Week 12

A learner who has shipped Week 12 has, in their portfolio repo:

- Three FRAME write-ups for the exercises, with recordings >= 10 minutes.
- One FRAME write-up for the Word Search challenge.
- The quiz answered (score recorded).
- The homework problems committed.
- **Two mini-project write-ups** (palindrome partitioning + sudoku solver), each with a 30-second pattern-recognition memo at the top, under `frame-writeups/c2-week-12/mini-project/`.
- A push log showing daily commits Mon–Sun.

If all of that is present and pushed, Phase 2's eighth week is closed. You are ready for Week 13 — behavioral interviews and communication under pressure (the bit-manipulation and tries patterns return in Week 14's Mock #3).

---

## A note on the Phase 2 ramp

Week 12 is the *enumeration-week* — the second of the two recursion-heavy weeks. The three-line template is the highest-leverage Research-constraints skill for any combinatorial enumeration problem in Phase 3; almost every onsite asks at least one "enumerate all X" or "find one valid Y" prompt, and the recognition of "this is backtracking, not DP" is the senior signal. Implementation fluency on the three warm-ups (subsets, permutations, combinations) and the prune-and-skip variant (combination sum) is the second-most-important outcome; N-Queens and sudoku are recognition-grade this week (know the state design, know the pruning sets, implement under pressure but do not optimize for speed).

If you find yourself ahead by Friday, the right stretch is **not** another exercise — it is re-implementing subsets three different ways (recursive with choose-explore-unchoose, recursive without explicit unchoose by passing `path + [nums[i]]`, iterative with bit enumeration over `2**n`) and comparing the code clarity and the produced output ordering. The three forms produce the same set of subsets in different orders; understanding why is the kind of meta-pattern that distinguishes senior candidates.

If you find yourself *behind* by Wednesday, skip Exercise 3 (Combination Sum) for now and prioritize Exercise 1 (Subsets) and Exercise 2 (Permutations) — those are the two warm-ups that show up most often in Mock #2, and Combination Sum can be picked up in 30 minutes once the warm-up template is fluent.

---

## Up next

[Week 13 — Behavioral & Communication](../week-13-behavioral-and-communication/) — once your three backtracking write-ups are pushed, your three-line template is articulate, and you can name the prune sets for N-Queens from memory without consulting the lecture.

---

*If you find errors in this material, please open an issue or send a PR. Future learners will thank you.*
