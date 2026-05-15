# Lecture 3 — State-Space Reduction and Recognition

> **Duration:** ~2 hours.
> **Outcome:** You can walk the diagonal-fill iteration order for longest palindromic subsequence, defend the rolling-array reduction in general, and walk the week-level recognition flowchart from a constraint signal to a specific DP shape (1D counting, 1D optimization, 1D boolean, 2D grid, 2D string-pair, single-string-two-ends) without rehearsal.

Lecture 1 installed the four-step pipeline and the 1D-DP suite. Lecture 2 installed 2D DP and the grid and string-pair shapes. This lecture closes the week with two threads: **state-space reduction in general** (when can you reduce the table to a rolling array, and how), and **the longest palindromic subsequence** (LPS) — the discriminating problem that requires a non-row-major iteration order. The lecture closes with the week's recognition flowchart, which is the artifact you should be able to recite in the quiz.

---

## 1. Longest palindromic subsequence (LC 516) — the diagonal-fill DP

> *Given a string `s`, find the longest palindromic subsequence's length in `s`. A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.*

**Match.** Brute force: at each pair `(i, j)` representing the substring `s[i..j]`, decide what `dp[i][j]` should be. If `s[i] == s[j]`, the palindromic subsequence extends both ends — `dp[i][j] = dp[i + 1][j - 1] + 2`. Otherwise, we drop one end — `dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])`. Overlapping subproblems and optimal substructure both hold. 2D DP.

**State semantics.** `dp[i][j] = length of the LPS in s[i..j]` (substring from index `i` to `j` inclusive). The base case is `dp[i][i] = 1` (a single character is a palindrome of length 1). The answer is `dp[0][n - 1]`.

**The iteration-order discriminator.** The recurrence reads `dp[i + 1][j - 1]` — the cell *below and to the left* of `(i, j)`. The standard row-major iteration (top to bottom, left to right) reads `dp[i + 1][j - 1]` *before* it has been written. The iteration must be reordered.

Two correct orderings:

- **By substring length.** Fill all `dp[i][j]` with `j - i = 0` first (the base cases), then `j - i = 1`, then `j - i = 2`, and so on up to `j - i = n - 1`. The recurrence at length `L = j - i` reads cells at lengths `L - 2` (`dp[i + 1][j - 1]`) and `L - 1` (`dp[i + 1][j]` and `dp[i][j - 1]`), all of which have been filled.
- **By row, bottom-up.** Iterate `i` from `n - 1` down to `0`; for each `i`, iterate `j` from `i + 1` to `n - 1`. The recurrence at `(i, j)` reads `dp[i + 1][...]` (already filled in a previous outer iteration) and `dp[i][j - 1]` (already filled in the current outer iteration). Correct.

Both orderings produce the same table. The by-substring-length form is more transparent for the lecture; the by-row form is shorter in code.

**Tabulation (by-substring-length).**

```python
from __future__ import annotations

from typing import List


def longest_palindromic_subsequence(s: str) -> int:
    """Length of the longest palindromic subsequence in s."""
    n = len(s)
    if n == 0:
        return 0

    dp: List[List[int]] = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1                              # base case: length-1 substrings

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                if length == 2:
                    dp[i][j] = 2                  # base case: length-2 match
                else:
                    dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

    return dp[0][n - 1]
```

Twenty lines. The outer loop iterates substring *length*; the inner loop iterates the *start index* `i`, with `j = i + length - 1` derived. The length-2 special case is the canonical bug source: when `length == 2` and `s[i] == s[j]`, the answer is 2 (not `dp[i + 1][j - 1] + 2 = 0 + 2 = 2` — which is the same value but requires reading `dp[i + 1][j - 1]` which for `length == 2` is `dp[i + 1][j - 1]` where `i + 1 == j` and `j - 1 == i`, i.e., `dp[j][i]` which is *outside the upper triangle* and equals 0). The if-branch handles this explicitly.

**Trace on `s = "bbbab"`.**

```
n = 5

After base cases (length = 1):
     b  b  b  a  b
b   [1, 0, 0, 0, 0]
b   [0, 1, 0, 0, 0]
b   [0, 0, 1, 0, 0]
a   [0, 0, 0, 1, 0]
b   [0, 0, 0, 0, 1]

length = 2:
  dp[0][1]: s[0]='b' == s[1]='b', length 2, value 2
  dp[1][2]: s[1]='b' == s[2]='b', value 2
  dp[2][3]: s[2]='b' != s[3]='a', max(dp[3][3], dp[2][2]) = 1
  dp[3][4]: s[3]='a' != s[4]='b', max(dp[4][4], dp[3][3]) = 1

length = 3:
  dp[0][2]: s[0]='b' == s[2]='b', dp[1][1] + 2 = 1 + 2 = 3
  dp[1][3]: s[1]='b' != s[3]='a', max(dp[2][3], dp[1][2]) = 2
  dp[2][4]: s[2]='b' == s[4]='b', dp[3][3] + 2 = 1 + 2 = 3

length = 4:
  dp[0][3]: s[0]='b' != s[3]='a', max(dp[1][3], dp[0][2]) = 3
  dp[1][4]: s[1]='b' == s[4]='b', dp[2][3] + 2 = 1 + 2 = 3

length = 5:
  dp[0][4]: s[0]='b' == s[4]='b', dp[1][3] + 2 = 2 + 2 = 4

Answer: dp[0][4] = 4 (the LPS is "bbbb")
```

**Defense.** "LPS is a 2D single-string-two-ends DP. The state is `dp[i][j] = LPS of s[i..j]`. The recurrence is: match extends `dp[i+1][j-1]` by 2; no-match takes the max of dropping either end. The iteration order is *by substring length*, not row-major, because the recurrence reads cells below and to the left. `O(n^2)` time, `O(n^2)` space."

---

## 2. The "trick" — LPS as LCS

There is a slick alternative form. The longest palindromic subsequence of `s` is **the LCS of `s` and `reverse(s)`**.

Why does this work? A palindromic subsequence reads the same forward and backward. So it is a common subsequence of `s` and its reverse. The longest such common subsequence is the longest palindromic subsequence.

```python
from __future__ import annotations


def lps_via_lcs(s: str) -> int:
    """LPS computed as LCS of s and reverse(s)."""
    from typing import List
    n = len(s)
    t = s[::-1]
    dp: List[List[int]] = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[n][n]
```

Twelve lines. The iteration is row-major (the LCS recurrence permits it); the trick is reducing LPS to LCS by reversing the input.

The trade: the LCS form is easier to write (row-major; reuses the LCS template) but reads less transparently as "LPS" to a human reader. The direct LPS form is more *honest* but requires the non-row-major iteration. Both are correct; senior candidates mention both.

---

## 3. State-space reduction — the general principle

The space-reduction trick was illustrated in Lectures 1 and 2 on specific problems. The general principle:

**If the recurrence reads `dp[state]` only at states "close to" the current state, the table can be reduced.**

For 1D DP that reads only `dp[i - 1]` and `dp[i - 2]`: reduce to two scalars. Rolling pair. `O(1)` space.

For 2D DP that reads only `dp[i - 1][...]` and `dp[i][...]`: reduce to two rows (or one row with careful management). Rolling row. `O(min(m, n))` space.

For 2D DP that reads `dp[i - k][...]` for some bounded `k`: reduce to `k + 1` rows. The 0/1 knapsack with item-count constraint is the typical example; covered in Week 12.

For DP that reads arbitrary `dp[state]` (e.g., LPS, which reads `dp[i + 1][j - 1]`): generally *not reducible* to better than `O(states)` space, because the entire table must be retained.

The check is mechanical: look at the recurrence, identify the set of states it reads, and decide whether those states can be "kept alive" in a window smaller than the full table.

---

## 4. Recognition flowchart — the week's signature artifact

The flowchart you should be able to walk in 30 seconds on any DP problem.

```
Step 1 — Is it DP at all?
  Does the brute-force recursion revisit the same arguments many times?
    Yes -> overlapping subproblems. Continue.
    No  -> not DP. Consider greedy / divide-and-conquer / brute-force with pruning.

  Does the optimum of the full problem compose from optima of subproblems?
    Yes -> optimal substructure. Continue.
    No  -> not DP. Consider backtracking with branch-and-bound.

Step 2 — How many state parameters?
  One parameter -> 1D DP. dp is a list. Lecture 1.
  Two parameters -> 2D DP. dp is a 2D list. Lecture 2.
  Three or more -> the state design needs work. Most interview DP is 1D or 2D.

Step 3 — What flavor of recurrence?
  Sum / count        -> counting DP. dp[i] = dp[i-1] + dp[i-2] or similar.
  Min / max          -> optimization DP. dp[i] = min(...) or max(...).
  Boolean / possible -> reachability DP. dp[i] = any(...) over preceding states.

Step 4 — What is the iteration order?
  1D, left to right            -> almost always correct.
  2D, row-major                -> correct for most 2D DPs.
  2D, by substring length      -> required for LPS-like substring/palindromic DPs.
  2D, bottom-up by row         -> alternative for LPS-like; correct when recurrence
                                  reads dp[i+1][...].

Step 5 — Can the space be reduced?
  Only previous row needed     -> rolling array, O(min(m, n)) space.
  Only previous two values     -> rolling pair, O(1) space.
  Otherwise                    -> O(states) space is the bound.
```

The flowchart is the artifact. Memorize the five steps and the prompts at each step. The quiz tests every branch.

---

## 5. Worked example — Decode Ways (LC 91) through the flowchart

Walk the flowchart on Decode Ways without re-reading Lecture 1.

> *A message containing letters from A–Z is encoded to numbers using the mapping 'A' -> '1', ..., 'Z' -> '26'. Given a string `s` containing only digits, return the number of ways to decode it.*

**Step 1.** Does the brute-force recursion revisit? Yes — `decode(s, i)` and `decode(s, i + 1)` both call `decode(s, i + 2)` in many cases. Overlapping subproblems. Does the optimum compose? Yes — the number of ways to decode `s[:i]` is the sum of contributions from each valid last-character choice. Optimal substructure (in the counting sense). DP confirmed.

**Step 2.** How many state parameters? One — the prefix length `i`. 1D DP.

**Step 3.** What flavor? Counting (sum of contributions from each valid choice). Sum recurrence.

**Step 4.** Iteration order? 1D, left to right. Standard.

**Step 5.** Space reduction? The recurrence reads `dp[i - 1]` and `dp[i - 2]`. Rolling pair. `O(1)` space.

Five-step walk: 1D-counting-left-to-right-rolling-pair. The 30-second classification. The implementation follows in 5 minutes; the recognition is the part graded.

---

## 6. Worked example — Edit Distance (LC 72) through the flowchart

**Step 1.** Brute-force recursion: `edit(s1, s2, i, j) = ...`. Revisits the same `(i, j)` from many paths. Overlapping subproblems. Optimum composes. Optimal substructure. DP.

**Step 2.** Two state parameters (`i`, `j`). 2D DP.

**Step 3.** Optimization (min over three options). Min recurrence.

**Step 4.** Iteration order: row-major. The recurrence reads `dp[i - 1][...]` and `dp[i][j - 1]` — both filled before the current cell in row-major order.

**Step 5.** Space reduction: only the previous row plus the current row up to `dp[i][j - 1]` is read. Rolling rows. `O(min(m, n))` space.

Five-step walk: 2D-optimization-row-major-rolling-rows. Classification in 30 seconds. Implementation in 10 minutes.

---

## 7. The negative-space rejection — when DP does **not** apply

The fifth thing a senior candidate says about DP is when it does **not** apply. Two cases the quiz tests:

**Case A — no overlapping subproblems.** Example: "given an array, return the sum of its elements." The brute-force `sum(arr) = sum(arr[:-1]) + arr[-1]` has no overlapping subproblems (each prefix is computed once). Not DP — it is a single-pass loop.

**Case B — no optimal substructure.** Example: "given a graph, find the longest simple path between two vertices." The optimum on a subpath is *not* necessarily extendable: a longer path through a vertex might re-use a vertex already on a shorter sub-optimum. The longest simple path is NP-hard and has no polynomial DP. The recognition skill: when "no-revisit" or "use each element once" constraints make subproblems context-dependent, optimal substructure fails. Not DP.

A third common rejection: **greedy works** (optimal substructure holds, but a single forward pass suffices without revisiting prior choices). Activity selection, interval scheduling, Huffman coding — all greedy, not DP. Greedy is faster (`O(n log n)` for sorting plus `O(n)` linear pass); DP is `O(n^2)` or worse. If greedy applies, use it.

The discriminator: in a greedy problem, you can prove that the locally optimal choice at each step leads to a globally optimal solution. In a DP problem, the locally optimal choice depends on choices made later, and you must explore both directions.

---

## 8. Closing — the week as a recognition curriculum

Three takeaways from Lecture 3 and the week:

1. **DP is a process, not a guess.** The four-step pipeline (recursion, memoize, tabulate, reduce) produces a correct answer in 15–20 minutes on every DP this week. Trust the pipeline. Do not try to "see the answer."
2. **The state semantics is the senior signal.** Naming the state in words — "ways to reach step `i`", "LCS of `s1[:i]` and `s2[:j]`", "LPS of `s[i..j]`" — demonstrates that you understand why the recurrence has its shape. Interviewers grade this hard.
3. **The recognition flowchart is the artifact.** Five steps: is it DP, how many parameters, what flavor, what iteration order, can space be reduced. Memorize the five steps. Walk them aloud in 30 seconds. The week's mini-project grades the walk.

Week 12 installs the second half of DP: 0/1 knapsack, unbounded knapsack, longest increasing subsequence (LIS), and the Phase-2 capstone retrospective. The four-step pipeline carries forward; the new shapes are *bounded-choice DPs* (knapsack) and *patience-sorting DPs* (LIS in `O(n log n)`).

[Back to the README](../README.md). Resources, quiz, homework, and the mini-project await.
