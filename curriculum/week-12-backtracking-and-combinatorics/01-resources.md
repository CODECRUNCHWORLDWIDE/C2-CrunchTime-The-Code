# Week 12 — Resources

Every resource is **free** and **publicly accessible**.

## Required reading (work it into your week)

- **Backtracking — Wikipedia**: <https://en.wikipedia.org/wiki/Backtracking> — the canonical written description of the technique. The "Description of the method" section is the textbook version of the choose-explore-unchoose template; the "Examples" section walks the eight-queens puzzle and the constraint-satisfaction framing. The "Pseudocode" subsection mirrors the three-line template almost verbatim — read it twice and walk it aloud.
- **Eight queens puzzle — Wikipedia**: <https://en.wikipedia.org/wiki/Eight_queens_puzzle> — N-Queens at N=8, the historical case. The "Solutions" section gives the 12 unique solutions (92 with rotations and reflections); the "Solution by backtracking" subsection is the canonical algorithm and reads cleanly after Lecture 3.
- **Sudoku solving algorithms — Wikipedia**: <https://en.wikipedia.org/wiki/Sudoku_solving_algorithms> — the backtracking section is the baseline solver Week 12 implements; the "Stochastic search" and "Constraint programming" sections are Phase-3 stretches. The "Optimizations of brute-force algorithms" subsection lists the cell-iteration-order heuristics (most-constrained cell first) that the LC 37 solution does not require but a senior candidate mentions.
- **Constraint satisfaction problem — Wikipedia**: <https://en.wikipedia.org/wiki/Constraint_satisfaction_problem> — the formal framing of N-Queens, sudoku, and many backtracking problems as CSPs (variables, domains, constraints). Reading the "Resolution of CSPs" section reveals that backtracking is the baseline algorithm for the entire CSP family.
- **Peter Norvig — "Solving Every Sudoku Puzzle"**: <https://norvig.com/sudoku.html> — the canonical written treatment of sudoku as constraint propagation plus backtracking. The Python code is short (less than 100 lines), the article is short (about 5,000 words), and the combination of the two is the senior-grade reference. Phase-3 stretch reading; do not implement during Week 12.
- **PEP 8 (recurring)**: <https://peps.python.org/pep-0008/>
- **Big-O Cheat Sheet (recurring)**: <https://www.bigocheatsheet.com/>

## On the pattern itself

Backtracking appears in interview prompts under several surface forms. The recognition skill is mapping the surface form to the underlying enumeration shape.

- **"Return all possible ..."** — combinatorial enumeration. The path at each leaf is one solution. State: usually `(start_index, path)`. Examples: subsets (LC 78), permutations (LC 46), combinations (LC 77), combination sum (LC 39), palindrome partitioning (LC 131).
- **"Find one valid ..."** — constraint satisfaction. The first leaf reached is the answer; the recursion returns `True` and unwinds. State: usually `(current_position, partial_configuration)`. Examples: N-Queens (LC 51 — though LC 51 actually asks for *all* configurations; the count-only variant is LC 52), sudoku (LC 37), word search (LC 79).
- **"Does there exist a ..."** — feasibility check. Same shape as constraint satisfaction; the first leaf reached confirms existence. Returns `True` on first success. Example: word search (LC 79 — the prompt is "return True if the word exists in the grid," which is a feasibility framing).
- **"Generate all valid ..."** — same as enumeration but with constraints inside the recursion. The constraint check happens before the choose step; an invalid candidate is skipped without a recursive call. Examples: generate parentheses (LC 22), restore IP addresses (LC 93).

If a prompt says "return all" and the brute-force enumeration has a clear branching decision at each step — backtracking. If it says "count the number of" with a clear branching decision — try DP first (counting often allows caching). If it says "find one valid" with constraints that prune — backtracking with early-return. If it says "find the minimum / maximum" — try DP or greedy first; backtracking is the fallback when neither applies.

## Free practice platforms

- **LeetCode — Backtracking tag** (free): <https://leetcode.com/tag/backtracking/>
- **LeetCode — Subsets** (LC 78): <https://leetcode.com/problems/subsets/> — the canonical backtracking warm-up; Exercise 1 exactly.
- **LeetCode — Permutations** (LC 46): <https://leetcode.com/problems/permutations/> — the canonical permutation backtracking; Exercise 2 exactly.
- **LeetCode — Combination Sum** (LC 39): <https://leetcode.com/problems/combination-sum/> — backtracking with sum-based pruning; Exercise 3.
- **LeetCode — Word Search** (LC 79): <https://leetcode.com/problems/word-search/> — 2D-grid backtracking with visited set; Challenge 1.
- **LeetCode — N-Queens** (LC 51): <https://leetcode.com/problems/n-queens/> — constraint satisfaction with three pruning sets; Challenge 2.
- **LeetCode — Palindrome Partitioning** (LC 131): <https://leetcode.com/problems/palindrome-partitioning/> — string-partitioning backtracking; mini-project Problem 1.
- **LeetCode — Sudoku Solver** (LC 37): <https://leetcode.com/problems/sudoku-solver/> — the canonical CSP backtracking; mini-project Problem 2.
- **LeetCode — Combinations** (LC 77): <https://leetcode.com/problems/combinations/> — the canonical "k-of-n" backtracking; homework.
- **LeetCode — Generate Parentheses** (LC 22): <https://leetcode.com/problems/generate-parentheses/> — constraint-aware backtracking; homework.
- **LeetCode — Restore IP Addresses** (LC 93): <https://leetcode.com/problems/restore-ip-addresses/> — backtracking with string-piece constraints; homework.
- **LeetCode — Letter Combinations of a Phone Number** (LC 17): <https://leetcode.com/problems/letter-combinations-of-a-phone-number/> — the canonical "Cartesian product" backtracking; homework.
- **LeetCode — Subsets II** (LC 90): <https://leetcode.com/problems/subsets-ii/> — deduplication variant of subsets; homework.
- **HackerRank — Recursion and Backtracking**: <https://www.hackerrank.com/domains/algorithms?filters%5Bsubdomains%5D%5B%5D=recursion>
- **CSES Problem Set — Introductory section**: <https://cses.fi/problemset/> — problems 7 (creating strings), 8 (apple division), and 25 (chessboard and queens) are all backtracking; ~30 minutes each.

## On the three-line template

The shape you should be able to walk in your head on every backtracking problem.

| Line | What you do | What you produce | Cost |
|------|-------------|------------------|------|
| 1. Choose | Append to the path; mark a cell visited; add to the used set | The state mutated for the recursive call | `O(1)` |
| 2. Recurse | Call the function with the mutated state and a smaller subproblem | The exploration of one branch of the decision tree | recursive |
| 3. Unchoose | Pop the path; unmark the cell; remove from the used set | The state restored to its pre-choose form | `O(1)` |

Three observations:

1. **The invariant is the discipline.** On entry to a call, the state has some value `S`. On exit from the call, the state must equal `S`. The choose-recurse-unchoose template guarantees this; any deviation produces aliased paths or incorrect results.
2. **The deep-copy at leaves is mandatory.** When a leaf is reached (the path is a valid solution), the path must be copied (`path[:]` or `list(path)`) before being appended to the results list. Without the copy, every entry in the results list aliases the same list, which is empty after the final unchoose.
3. **The "without explicit unchoose" form is shorter but allocates more.** Passing `path + [nums[i]]` to the recursive call creates a new list at each level, so there is no shared state to undo. The form is cleaner but allocates `O(n)` per recursive call instead of `O(1)`; for `n = 20`, the allocation matters. Senior candidates write the explicit-unchoose form and explain the alternative.

### The canonical three-line template on subsets

```python
from __future__ import annotations

from typing import List


def subsets(nums: List[int]) -> List[List[int]]:
    """Return all 2^n subsets of nums in any order."""
    result: List[List[int]] = []
    path: List[int] = []

    def backtrack(start: int) -> None:
        # Every node is a valid subset; record before exploring further.
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])      # CHOOSE
            backtrack(i + 1)          # RECURSE (start = i + 1: no reuse, no duplicates)
            path.pop()                # UNCHOOSE

    backtrack(0)
    return result
```

Memorize the three-line cadence. The body of each line is one statement; the *invariant* (state on entry equals state on exit) is the part interviewers grade.

## On the three combinatorial warm-ups

A short table of the three combinatorial enumerations you should be able to write from memory.

| Problem | State | Recurrence | Output size |
|---------|-------|------------|------------:|
| Subsets | `(start_index, path)` | At each `i >= start`, choose `nums[i]`, recurse with `i + 1`, unchoose. Record at every node. | `2^n` |
| Permutations | `(used_set, path)` | At each `i in 0..n-1` not in `used`, choose `nums[i]`, recurse, unchoose. Record at leaves where `len(path) == n`. | `n!` |
| Combinations | `(start_index, path)` | At each `i >= start`, choose `nums[i]`, recurse with `i + 1`, unchoose. Record at leaves where `len(path) == k`. | `C(n, k)` |

Three observations:

1. **Subsets and combinations share the recurrence shape; they differ only in when to record.** Subsets records at every node; combinations records only at leaves of the right length. The state design (`start_index`) is identical; the recording condition is the discriminator.
2. **Permutations uses a `used` set, not a `start_index`.** Because order matters in permutations, every unused element must be available at every level. The `used` set tracks which elements are currently on the path; an alternative is an index-list parameter, but the set form is clearer.
3. **Output size grows fast.** Subsets: `2^n` (16 for n=4, 1024 for n=10, `~10^6` for n=20). Permutations: `n!` (24 for n=4, 3.6M for n=10, `~10^18` for n=20 — infeasible). Combinations: `C(n, k)` (peaks at `k = n/2`, but generally smaller). The complexity bound `O(output_size * path_length)` is the canonical defense.

## On pruning — the four families

The four kinds of pruning that turn backtracking from `O(b^d)` to something tractable.

| Family | What you check | When you prune |
|--------|----------------|----------------|
| Feasibility | Can the partial state be extended to a valid leaf? | If no — prune the entire subtree before recursing. |
| Optimality | Can the partial state improve the best-so-far? | If no — prune. (Requires tracking the best-so-far; branch-and-bound.) |
| Symmetry | Is the partial state equivalent to a previously-explored state? | If yes — prune. (Requires a canonical-form check or a hash of explored states.) |
| Constraint propagation | Does the partial state violate any constraint? | If yes — prune. The most common form; N-Queens and sudoku are the canonical examples. |

Three observations:

1. **Feasibility pruning is the most common in interview prompts.** Combination sum: if `remaining < 0`, prune. Word search: if the next cell does not match the next character, prune. Sudoku: if the candidate digit violates row, column, or box, prune. The check is `O(1)` in each case; the savings are exponential.
2. **Sort-first is the canonical setup for feasibility pruning on numeric inputs.** Combination sum: sort `nums` ascending; in the inner loop, `break` (not `continue`) as soon as `nums[i] > remaining` — every later `nums[j]` is also too large. The sort plus break turns the loop from `O(n)` to `O(k)` where `k` is the position of the first too-large element.
3. **Constraint-propagation pruning requires the right state representation.** N-Queens with three sets (column, diag1, diag2) lets each constraint check run in `O(1)`. N-Queens without the sets requires walking the partial board on every check, which is `O(row)` and turns the whole algorithm from microseconds to seconds. The state design is the senior-grade move.

## On deduplication — sort plus index-skip

When the input has duplicate elements and the output should have no duplicate solutions, the canonical idiom:

```python
nums.sort()
def backtrack(start: int) -> None:
    # ... record path ...
    for i in range(start, len(nums)):
        # Skip duplicates at the SAME level (not at the same path).
        if i > start and nums[i] == nums[i - 1]:
            continue
        path.append(nums[i])
        backtrack(i + 1)
        path.pop()
```

The discriminator is `i > start`, not `i > 0`. The condition "skip duplicates at the same level" allows the first occurrence of a duplicate to be chosen (which produces one valid solution for the duplicate group) but rejects subsequent occurrences at the same depth (which would produce identical solutions).

This idiom appears in subsets II (LC 90), permutations II (LC 47), combination sum II (LC 40), and many others. The signature is "sort plus `if i > start and nums[i] == nums[i - 1]: continue`."

## On the 2D-grid backtracking template

Word search and similar problems extend the three-line template to a 2D grid with directional iteration.

```python
from __future__ import annotations

from typing import List


def word_search(board: List[List[str]], word: str) -> bool:
    """Return True iff word can be traced through the board with four-direction moves."""
    rows = len(board)
    cols = len(board[0]) if rows else 0
    visited: set[tuple[int, int]] = set()

    def backtrack(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        if (r, c) in visited or board[r][c] != word[idx]:
            return False

        visited.add((r, c))                     # CHOOSE
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if backtrack(r + dr, c + dc, idx + 1):   # RECURSE
                return True
        visited.remove((r, c))                  # UNCHOOSE
        return False

    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0):
                return True
    return False
```

Twenty-three lines. The `visited` set prevents cycles; the four-direction loop is the canonical neighbor iterator; the `unchoose` step (`visited.remove((r, c))`) restores the state for the next outer-loop start cell.

Memorize the shape. The in-place variant uses `board[r][c] = '#'` to mark visited (and `board[r][c] = word[idx]` to restore) and saves the `O(rows * cols)` set space; mention it as the space-optimal form.

## Glossary additions

- **Backtracking** — a recursive technique for enumerating all solutions to a combinatorial problem by exploring a decision tree depth-first and undoing choices that lead to dead ends. The choose-explore-unchoose template is the canonical form.
- **Choose-explore-unchoose** — the three-line backtracking template. Choose: mutate the state. Explore: recurse. Unchoose: undo the mutation. The invariant is that the state on entry equals the state on exit.
- **Decision tree** — the tree of choices implicit in a backtracking recursion. Each node is a partial state; each edge is a choice. The depth equals the path length; the branching factor equals the number of choices at each level.
- **Leaf** — a node in the decision tree where no further choice is possible — either because the path is complete (a valid solution) or because the constraints prune all candidates (a dead end). Valid leaves contribute to the output.
- **Pruning** — eliminating a subtree from the search without exploring it. Four families: feasibility, optimality, symmetry, constraint-propagation.
- **Constraint satisfaction problem (CSP)** — a problem defined by variables, domains, and constraints. N-Queens and sudoku are the canonical CSPs; backtracking is the baseline algorithm for the CSP family.
- **State** — the parameters that fully determine a partial solution. For combinatorial enumeration, the state is usually `(start_index, path)` or `(used_set, path)`. For constraint satisfaction, the state is usually `(current_position, partial_configuration)`.
- **Path** — the current sequence of choices on the recursion stack. The path is mutable; mutations are made on choose and reversed on unchoose. A deep copy is appended to the results list at each valid leaf.
- **Visited set** — a data structure (Python `set`) tracking which positions or elements are currently on the path. Prevents cycles in grid backtracking and re-selection in permutations.
- **Pruning set** — a data structure that supports `O(1)` constraint checks. N-Queens uses three sets (column, diag1, diag2); sudoku uses three sets per row/column/box; constraint propagation uses one set per variable.
- **Permutation** — an ordered arrangement of all elements. `n!` permutations of an `n`-element list. Order matters; `[1, 2]` and `[2, 1]` are distinct.
- **Combination** — an unordered selection of `k` elements from `n`. `C(n, k)` combinations of an `n`-element list. Order does not matter; `[1, 2]` and `[2, 1]` are the same.
- **Subset** — an unordered selection of any number of elements from `n`. `2^n` subsets of an `n`-element list. Equivalent to "combinations for every `k` from 0 to `n`."

## Cheatsheet — the backtracking recognition flowchart

A short decision flowchart you should be able to walk in 30 seconds.

```
Does the prompt ask for ALL solutions, or to ENUMERATE a configuration space?
  No  -> probably not backtracking. Consider DP (count, optimum) or greedy.
  Yes -> next question.

Is the decision space at each level discrete and finite?
  No  -> probably not backtracking. Continuous-space problems use other techniques.
  Yes -> next question.

Is the path (the sequence of choices) part of the output?
  No  -> consider DP first. Backtracking is the fallback when DP fails.
  Yes -> backtracking. Identify the state next.

What is the state?
  (start_index, path)        -> combinatorial enumeration (subsets, combinations, combination sum).
  (used_set, path)           -> permutations (order matters).
  (position, partial_config) -> constraint satisfaction (N-Queens, sudoku, word search).

What pruning applies?
  Feasibility            -> sort-first plus early break; the most common.
  Constraint propagation -> use pruning sets for O(1) checks; N-Queens, sudoku.
  Optimality             -> track best-so-far; branch-and-bound.
  Symmetry               -> canonical-form check; rare in interview prompts.

What recording discipline?
  At every node     -> subsets (every node is a valid subset).
  At leaves only    -> permutations, combinations, palindrome partitioning.
  First leaf only   -> word search, sudoku (return True on first success).
```

Read aloud; should hit 25–30 seconds. The order matters — the questions narrow the backtracking shape in the same order they would surface in an interview prompt.
