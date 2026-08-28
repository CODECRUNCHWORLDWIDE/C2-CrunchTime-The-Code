# Challenge 2 — Longest Palindromic Subsequence (LeetCode 516)

> **Difficulty:** Medium-Hard. **Target solve time:** 60 minutes including FRAME write-up. Optional this week — ship Challenge 1 first.

This is the canonical example of a 2D DP whose recurrence forces a non-row-major iteration order. The work this week is to implement the **by-substring-length** iteration and to defend the order in writing — most failed LC 516 attempts ship with row-major iteration and incorrect results because the recurrence reads `dp[i + 1][j - 1]` before it has been filled.

---

## Problem spec

Given a string `s`, find the longest palindromic subsequence's length in `s`.

A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.

**Constraints (LeetCode):**

- `1 <= s.length <= 1000`.
- `s` consists only of lowercase English letters.

---

## Why this is the canonical diagonal-fill DP

Three reasons.

1. **The recurrence reads `dp[i + 1][j - 1]` — the cell below and to the left.** The standard row-major iteration (top-to-bottom, left-to-right) reads this cell before it has been written. The iteration must be reordered.

2. **The state is "single string, two indices."** Unlike LCS (two strings, two indices) or unique paths (grid, two indices), LPS has a single string and the indices represent the start and end of a substring. The state-design lesson: 2D state does not always mean "pair of strings."

3. **There is a slick LCS-based shortcut.** LPS of `s` equals LCS of `s` and `reverse(s)`. This reduces the problem to a standard LCS, side-stepping the iteration-order question. Both approaches are correct; senior candidates know both and discuss the trade.

---

## 30-second pattern-recognition memo

```markdown
> **30-second pattern-recognition memo (LPS / 2D diagonal-fill DP):**
> Single-string two-index DP. State = "length of LPS in s[i..j]."
> Recurrence: match (s[i] == s[j]) -> dp[i+1][j-1] + 2; no-match ->
> max(dp[i+1][j], dp[i][j-1]). Base case: dp[i][i] = 1. Iteration order:
> by substring length, not row-major, because the recurrence reads cells
> below-and-to-the-left. O(n^2) time, O(n^2) space. Alternative: LPS(s)
> = LCS(s, reverse(s)) -- reduces to a standard LCS with row-major
> iteration.
```

Read aloud; should hit 25–30 seconds.

---

## The intended algorithms

### Algorithm A — Direct LPS with by-substring-length iteration

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
                    dp[i][j] = 2
                else:
                    dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

    return dp[0][n - 1]
```

Twenty lines. The outer loop iterates substring length; the inner loop iterates the start index. The length-2 case must be handled separately because `dp[i + 1][j - 1]` for `length == 2` reads `dp[i + 1][j - 1]` where `i + 1 == j` and `j - 1 == i` — the cell `dp[j][i]` is outside the upper triangle and is 0.

### Algorithm B — LPS via LCS

```python
from __future__ import annotations

from typing import List


def longest_palindromic_subsequence_via_lcs(s: str) -> int:
    """LPS computed as LCS of s and reverse(s)."""
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

Twelve lines. Standard row-major LCS on `s` and `reverse(s)`. The trick is recognizing that a palindromic subsequence of `s` is by definition a common subsequence of `s` and its reverse.

---

## Trade-off — when to use which

| Dimension | Algorithm A (direct) | Algorithm B (LCS) |
|-----------|---------------------|-------------------|
| Time | O(n^2) | O(n^2) |
| Space | O(n^2) | O(n^2), reducible to O(n) with rolling rows |
| Iteration order | By substring length | Row-major |
| Reads as "LPS" to a reader | Yes | No (requires the reduction explained) |
| Code length | 20 lines | 12 lines |

The discriminating factor for interviews: **Algorithm B is shorter and reuses the LCS template you have already memorized**. But it requires the conceptual move "LPS(s) = LCS(s, reverse(s))" to be defended out loud. Algorithm A is the more honest expression of the problem; under interview pressure, ship whichever you can write faster, and mention the other in the Examine section.

---

## Trace on `s = "bbbab"` (the LC 516 example)

```
n = 5. Initialize dp[i][i] = 1 for all i.

length = 2:
  dp[0][1] (s[0]='b'==s[1]='b'): special length-2 match, dp[0][1] = 2
  dp[1][2] (s[1]='b'==s[2]='b'): dp[1][2] = 2
  dp[2][3] (s[2]='b'!=s[3]='a'): max(dp[3][3], dp[2][2]) = max(1, 1) = 1
  dp[3][4] (s[3]='a'!=s[4]='b'): max(dp[4][4], dp[3][3]) = max(1, 1) = 1

length = 3:
  dp[0][2] (s[0]='b'==s[2]='b'): dp[1][1] + 2 = 1 + 2 = 3
  dp[1][3] (s[1]='b'!=s[3]='a'): max(dp[2][3], dp[1][2]) = max(1, 2) = 2
  dp[2][4] (s[2]='b'==s[4]='b'): dp[3][3] + 2 = 1 + 2 = 3

length = 4:
  dp[0][3] (s[0]='b'!=s[3]='a'): max(dp[1][3], dp[0][2]) = max(2, 3) = 3
  dp[1][4] (s[1]='b'==s[4]='b'): dp[2][3] + 2 = 1 + 2 = 3

length = 5:
  dp[0][4] (s[0]='b'==s[4]='b'): dp[1][3] + 2 = 2 + 2 = 4

Answer: dp[0][4] = 4 (the LPS is "bbbb").
```

The trace is the rubric for the Examine · verify section.

---

## Common bugs

1. **Wrong iteration order.** Row-major iteration reads `dp[i + 1][j - 1]` before it is filled. The result is silently wrong (the table fills with mostly zeros). The fix: iterate by substring length, or iterate `i` from `n - 1` down to `0`.
2. **Missing length-2 special case.** When `length == 2` and `s[i] == s[j]`, the answer is 2. The general recurrence `dp[i + 1][j - 1] + 2` reads `dp[i + 1][j - 1]` where `i + 1 > j - 1`, which is below the diagonal and equals 0; so the formula gives 2 by accident, but explicitly handling the case is clearer and avoids the silent dependency on the zero-init.
3. **Off-by-one in the inner loop.** `for i in range(n - length + 1)` is the correct bound; `j = i + length - 1` is then guaranteed to be in `[0, n - 1]`. Beginners write `range(n - length)` and miss the rightmost substring.
4. **Returning the wrong cell.** `dp[0][n - 1]` is the answer (the LPS of the full string). Not `dp[n][n]` (which is out of bounds for the `n x n` table) and not `dp[n - 1][n - 1]` (which is 1, the base case for the rightmost single character).

---

## FRAME write-up structure

### Frame

Restate: find the length of the longest palindromic *subsequence* (not substring). Confirm semantics: a palindromic subsequence reads the same forward and backward; deleting characters is allowed; order is preserved.

### Research constraints

The 30-second memo. Name the pattern, the recurrence, the iteration order, the complexity. Mention both Algorithm A and Algorithm B; commit to one.

### Assess options

1. Initialize a `n x n` DP table with zeros.
2. Set `dp[i][i] = 1` for all `i` (base case).
3. Iterate by substring length from 2 to `n`. For each length, iterate over starting positions `i`.
4. Fill `dp[i][j]` via the match / no-match recurrence with the length-2 special case.
5. Return `dp[0][n - 1]`.

### Make the solution

Algorithm A first. If time remains, ship Algorithm B as the alternative.

### Examine · verify

The trace on `s = "bbbab"` above.

### Examine · cost

- **Time:** `O(n^2)`. Outer loop on length (n - 1 iterations); inner loop on start index (up to n iterations).
- **Space:** `O(n^2)` for the table. Reducible to `O(n)` only via Algorithm B with rolling rows; Algorithm A's recurrence reads `dp[i + 1][j - 1]` which forbids the standard rolling-row reduction.
- **Trade vs. LCS-based form (Algorithm B):** B is shorter and reuses the LCS template; A is more honest about the LPS structure. Discuss both.
- **Trade vs. longest palindromic substring:** the substring variant is a different DP (Phase 3) with a contiguity constraint. The recognition cue: "subsequence" vs. "substring" in the prompt.

---

## Acceptance

This challenge is shipped when:

- A `longest_palindromic_subsequence.py` implementation (Algorithm A or B) passes all LC 516 sample cases.
- A FRAME write-up under `frame-writeups/c2-week-11/challenge-02-longest-palindromic-subsequence/` is committed with the 30-second memo at the top.
- The Examine · cost section explicitly states the trade between Algorithm A and Algorithm B.

---

## Why this challenge is optional

Challenge 2 covers iteration-order discipline — a Phase-3-grade detail. Most Mock #2 problems do not require it; LCS and edit distance (the row-major DPs from Lecture 2) cover the bulk of Phase-2 onsite questions on string DP. Ship Challenge 1 first. Reach for Challenge 2 only if you have time on Friday after Challenge 1 is committed and recorded.

The recognition skill is the higher-leverage outcome: when you see a problem whose state is `(i, j)` with `i` and `j` representing two ends of a single string, the iteration order is the first thing to check. If the recurrence reads `dp[i + 1][...]`, you cannot iterate top-to-bottom; reach for by-substring-length or bottom-up-by-row.
