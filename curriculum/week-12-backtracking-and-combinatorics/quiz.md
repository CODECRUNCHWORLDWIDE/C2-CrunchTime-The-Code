# Week 12 — Pattern-Recognition Quiz

Ten short prompts. **Do not solve them.** For each, decide what shape applies — backtracking (combinatorial enumeration / permutation / partition / constraint satisfaction) or DP (counting / optimization) or neither — and name the state and the pruning (if any) in one line. Lectures closed. Time yourself — 45 seconds per question is the target.

Answer key at the bottom.

---

**Q1.** "Given an array `nums` of unique integers, return all possible subsets."

**Q2.** "Given an array `nums` of unique integers, count the number of subsets whose sum is at most `k`."

**Q3.** "Given two integers `n` and `k`, return all combinations of `k` numbers from `[1, n]`."

**Q4.** "Given a string `s`, partition `s` such that every substring of the partition is a palindrome, and return all possible partitions."

**Q5.** "Given an `m x n` grid of characters and a word, return True iff the word can be traced through the grid using four-direction adjacency, with no cell reused per trace."

**Q6.** "Given an integer `n`, return all distinct ways to place `n` non-attacking queens on an `n x n` chessboard."

**Q7.** "Given a 9x9 sudoku board with some cells pre-filled and others empty (marked '.'), fill the empty cells so that the resulting board is a valid sudoku solution."

**Q8.** "Given an array `nums` of distinct positive integers and a target integer, return all unique combinations of `nums` summing to the target. Each integer may be used unlimited times."

**Q9.** "Given an integer `n`, return the number of distinct ways to climb a staircase with `n` steps if you can take 1 or 2 steps at a time."

**Q10.** "Given a digit string, return all letter combinations that the number could represent under the phone-keypad mapping."

---

## Answer key

<details>
<summary>Click after attempting all ten</summary>

1. **Backtracking — combinatorial enumeration (subsets).** State: `(start_index, path)`. No pruning needed; record at every node (every node is a valid subset). 2^n subsets. LC 78; Exercise 1.

2. **DP — counting (not backtracking).** The prompt asks for the count, not the subsets themselves. State: `dp[i][s] = number of subsets of nums[:i] summing to s`. Subset-sum counting DP. Backtracking would enumerate 2^n subsets to count them — exponentially slower. The negative-space rejection.

3. **Backtracking — combinatorial enumeration (combinations).** State: `(start_index, path)`. Pruning: `last = n - (k - len(path)) + 1` to skip subtrees that cannot reach length k. Record at leaves where `len(path) == k`. C(n, k) combinations. LC 77; homework.

4. **Backtracking — string partitioning.** State: `(start_index, path)` where path is the list of palindromic pieces. Pruning: palindrome check on each candidate piece (constraint-propagation). Record at leaves where `start == n`. LC 131; mini-project Problem 1.

5. **Backtracking — 2D-grid feasibility (word search).** State: `(row, col, word_index)`. Pruning: bounds, visited set, character match. Return True on first success; the recursion unwinds. LC 79; Challenge 1.

6. **Backtracking — constraint satisfaction (N-Queens).** State: `(row, cols, diag1, diag2, path)`. Pruning: three sets (column, two diagonals) for O(1) constraint checks. Record at leaves where `row == n`. LC 51; Challenge 2.

7. **Backtracking — constraint satisfaction (sudoku).** State: the board (mutated in place) plus three constraint sets per row, column, box. Pruning: three set membership checks per candidate digit. Return True on first complete board. LC 37; mini-project Problem 2.

8. **Backtracking — combinatorial enumeration with reuse (combination sum).** State: `(start_index, remaining_target, path)`. Pruning: sort + break when `candidates[i] > remaining`. Reuse: recurse with `start = i` (not `i + 1`). Record when `remaining == 0`. LC 39; Exercise 3.

9. **DP — counting (not backtracking).** The prompt asks for the count, not the configurations. State: `dp[i] = number of ways to reach step i`. Recurrence: `dp[i] = dp[i-1] + dp[i-2]`. This is climbing stairs from W11; the negative-space rejection — every "count the number of ways" prompt should go to DP first.

10. **Backtracking — combinatorial enumeration (Cartesian product).** State: `(digit_index, path)`. No pruning (every letter in the digit group is valid). Record at leaves where `digit_index == len(digits)`. LC 17; homework.

</details>

---

## How to score

| Score | Meaning |
|------:|---------|
| 9-10 | Backtracking recognition is interview-ready, including the negative-space rejections (Q2, Q9) and the constraint-satisfaction sub-shape (Q6, Q7). Move on. |
| 7-8 | Good — re-read [Lecture 3 §6](./lecture-notes/03-grid-backtracking-and-constraint-satisfaction.md) for the negative-space rejections. Most learners miss Q2 (counting subsets is DP, not backtracking) or Q9 (counting climbing-stairs is DP) first time; that is normal. |
| 5-6 | Redo Exercises 1, 2, and 3 with stricter Research constraints sections. The combinatorial-vs-counting distinction and the prune-and-skip discipline need more reps. |
| <5 | The pattern recognition is not yet automatic. Re-read all three lectures, re-do all three exercises with the state and the prune stated aloud, then retake the quiz. |

This quiz is about **fluency**, not difficulty. The discriminating questions are Q2 and Q9 (counting prompts that go to DP, not backtracking), Q4 (string partitioning is backtracking, not DP), and Q7 (sudoku is backtracking, not search). Q2 and Q9 are the most-missed; senior candidates over-apply backtracking to any "return all" prompt without checking whether "count" alone is asked.

Q1 (subsets) and Q3 (combinations) are the cleanest direct-template questions. Q6 (N-Queens) and Q7 (sudoku) test recognition of the constraint-satisfaction sub-shape.

When done, the [homework](./homework/README.md) is next.
