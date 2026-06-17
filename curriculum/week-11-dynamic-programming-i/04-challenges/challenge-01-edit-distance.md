# Challenge 1 — Edit Distance (Deep Dive, LeetCode 72)

> **Difficulty:** Medium-Hard (with the deep-dive treatment). **Target solve time:** 75 minutes including UMPIRE write-up and the rolling-array reduction.

This is the deep-dive version of the canonical 2D string-pair DP. The work this week is to **implement both** the standard `O(mn)`-space tabulation and the `O(min(m, n))`-space rolling-row reduction, and to defend the trade between them in the Evaluate section. Most Phase-2 onsite problems on DP ask exactly this kind of trade — "can you reduce the space?" is the senior signal.

---

## Problem spec

Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`.

You have the following three operations permitted on a word:

- Insert a character.
- Delete a character.
- Replace a character.

**Constraints (LeetCode):**

- `0 <= word1.length, word2.length <= 500`.
- `word1` and `word2` consist of lowercase English letters.

---

## Why this is the canonical 2D string-pair DP

Three reasons.

1. **The three-way min is the cleanest illustration of "choose among multiple precursors."** Most 2D DPs draw from one or two precursor states; edit distance draws from three (insert, delete, replace), and each precursor corresponds to a real operation with a clear name. Articulating the correspondence — `dp[i][j - 1]` is insert; `dp[i - 1][j]` is delete; `dp[i - 1][j - 1]` is replace — is the discriminating implementation detail.

2. **The base cases are non-zero.** Unlike LCS (where `dp[0][...]` and `dp[...][0]` are both 0), edit distance has `dp[i][0] = i` (deleting `i` characters to convert to an empty string) and `dp[0][j] = j` (inserting `j` characters to convert from an empty string). Forgetting this is the single most common LC 72 bug.

3. **The rolling-array reduction is the canonical "reduce space" interview question.** The recurrence reads `dp[i - 1][j - 1]`, `dp[i - 1][j]`, and `dp[i][j - 1]` — the cell to the upper-left, the cell above, and the cell to the left. Two rows suffice (or one row with a scalar to track the upper-left value before it is overwritten).

---

## 30-second pattern-recognition memo

Use this exact shape at the top of your write-up.

```markdown
> **30-second pattern-recognition memo (Edit Distance / 2D three-way-min DP):**
> Two-string optimization problem. State = "min edits to convert s1[:i]
> into s2[:j]." Recurrence has two cases: match -> dp[i-1][j-1]; no-match
> -> 1 + min(insert dp[i][j-1], delete dp[i-1][j], replace dp[i-1][j-1]).
> Base cases non-zero: dp[i][0] = i (delete i times), dp[0][j] = j (insert
> j times). O(mn) time, O(mn) space with the table; O(min(m, n)) with
> rolling rows. Why not LCS-style two-predecessor: edit distance counts
> operations, and the three operations have different precursor states.
```

Read aloud; should hit 25–30 seconds.

---

## The intended algorithms

### Algorithm A — Standard tabulation (O(mn) space)

```python
from __future__ import annotations

from typing import List


def min_distance(word1: str, word2: str) -> int:
    """Minimum number of edits to convert word1 to word2."""
    m, n = len(word1), len(word2)
    dp: List[List[int]] = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i][j - 1],       # insert
                    dp[i - 1][j],       # delete
                    dp[i - 1][j - 1],   # replace
                )

    return dp[m][n]
```

Twenty lines. The two base-case loops are non-negotiable; without them, the DP is wrong for strings with empty prefixes.

### Algorithm B — Rolling-row reduction (O(min(m, n)) space)

```python
from __future__ import annotations

from typing import List


def min_distance_rolling(word1: str, word2: str) -> int:
    """O(min(m, n)) space via two rolling rows."""
    # Ensure word2 is the shorter string
    if len(word1) < len(word2):
        word1, word2 = word2, word1
    m, n = len(word1), len(word2)

    prev: List[int] = list(range(n + 1))    # dp[0][j] = j
    curr: List[int] = [0] * (n + 1)

    for i in range(1, m + 1):
        curr[0] = i                          # dp[i][0] = i
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(
                    curr[j - 1],             # insert
                    prev[j],                 # delete
                    prev[j - 1],             # replace
                )
        prev, curr = curr, [0] * (n + 1)

    return prev[n]
```

Twenty-four lines. The swap `prev, curr = curr, [0] * (n + 1)` at the end of each outer iteration shifts the rolling window forward. Allocating a fresh `curr` per outer iteration is a touch wasteful but is easier to read than reusing the same buffer (which requires explicit zeroing).

---

## Trade-off — when to use which

| Dimension | Algorithm A (O(mn) space) | Algorithm B (rolling rows) |
|-----------|---------------------------|----------------------------|
| Time | O(mn) | O(mn) |
| Space | O(mn) | O(min(m, n)) |
| Memory locality | Worse (jumps between rows) | Better (two adjacent rows) |
| Backtracking the operations | Easy (walk the table) | Hard (table is destroyed) |
| Code complexity | Lower | Higher |

The discriminating factor for interviews: **if the interviewer asks "can you reduce the space?", reach for Algorithm B**. If they ask "and can you also output the actual sequence of operations?", reach for Algorithm A — the table is needed for backtracking.

---

## Common bugs

1. **Missing base-case initialization.** `dp[i][0]` and `dp[0][j]` must be explicitly set; zero-initialization is wrong for edit distance. The canonical failure mode: `word1 = "abc", word2 = ""` returns 0 instead of 3.
2. **Index off-by-one.** `word1[i - 1]`, not `word1[i]`. The table is dimension `(m + 1) x (n + 1)` to include the empty-prefix base cases.
3. **Min over the wrong set.** The no-match case is `min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1])` plus 1. Including or excluding the wrong cells is the canonical bug. A useful mnemonic: insert moves *across* (`j - 1`), delete moves *down* (`i - 1`), replace moves *diagonally* (`i - 1, j - 1`).
4. **Rolling-row off-by-one.** When using the rolling form, `prev[j - 1]` is the diagonal precursor (corresponds to `dp[i - 1][j - 1]`). Beginners read `prev[j]` instead — that is the `dp[i - 1][j]` precursor (delete). Mixing the two destroys correctness silently; the table version is easier to debug.

---

## UMPIRE write-up structure

Your write-up should hit every section. The Evaluate section is the discriminating part.

### Understand

Restate the problem. Confirm "edit distance" semantics: insert, delete, replace, each cost 1. The Levenshtein distance.

### Match

The 30-second memo. Name the pattern, the recurrence, the base cases, the complexity.

### Plan

1. Build the `(m + 1) x (n + 1)` DP table.
2. Initialize the base cases: `dp[i][0] = i`, `dp[0][j] = j`.
3. Fill the table row by row via the two-case recurrence.
4. Return `dp[m][n]`.

### Implement

Algorithm A. Then Algorithm B as the optimization. Both must be correct on the LC 72 examples.

### Review

Trace `word1 = "horse", word2 = "ros"`:

```
     ""  r  o  s
""    0  1  2  3
h     1  1  2  3
o     2  2  1  2
r     3  2  2  2
s     4  3  3  2
e     5  4  4  3

Answer: dp[5][3] = 3.
```

The three operations: replace `h` with `r` (horse -> rorse), delete `r` (rorse -> rose), delete `e` (rose -> ros). Three edits, matching `dp[5][3] = 3`.

### Evaluate

- **Time:** `O(mn)` for both. For `m, n = 500`, this is `2.5e5` operations — well within any LC time limit.
- **Space:** `O(mn)` for A, `O(min(m, n))` for B.
- **Trade vs. LCS:** the table shape is identical; only the recurrence differs (max over two for LCS; min over three plus 1 for edit distance). Recognizing this similarity is the senior-grade Match move.
- **Trade vs. greedy:** greedy left-to-right matching is *wrong*. Counter-example: `word1 = "ab", word2 = "ba"`. Greedy would replace both characters (cost 2); the optimum is delete + insert (cost 2) or replace + replace (cost 2) — both options actually cost the same here, but for `word1 = "abc", word2 = "cab"`, greedy replaces three (cost 3) while the optimum is shift-by-one with a single replace plus an insert (cost 2). DP is required.
- **Trade vs. Hamming distance:** Hamming distance counts only substitutions and requires equal-length strings. Edit distance allows insertions and deletions and works on different-length strings.

---

## Acceptance

This challenge is shipped when:

- A `min_distance.py` implementation (Algorithm A) passes all LC 72 sample cases.
- A `min_distance_rolling.py` implementation (Algorithm B) passes the same cases with `O(min(m, n))` space.
- A UMPIRE write-up under `umpire-writeups/c2-week-11/challenge-01-edit-distance/` is committed with the 30-second memo at the top and a recording >= 12 minutes.
- The Evaluate section explicitly states the trade between Algorithm A and Algorithm B and gives one concrete scenario for each (backtracking the operations -> A; large inputs with memory constraint -> B).

---

## Stretch — print the actual edit sequence

If you ship the challenge with time remaining, modify Algorithm A to *return* the actual sequence of operations. The technique: walk the table from `(m, n)` backwards to `(0, 0)`, at each cell choosing the predecessor that matches the value at the current cell. The walk produces the operations in reverse; reverse the list before returning.

```python
def min_distance_with_ops(word1: str, word2: str) -> tuple[int, list[str]]:
    """Return both the edit distance and the list of operations."""
    # ... same DP table construction as Algorithm A ...
    # Then walk backward:
    ops: list[str] = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and word1[i - 1] == word2[j - 1]:
            i, j = i - 1, j - 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            ops.append(f"insert {word2[j - 1]} at position {i}")
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            ops.append(f"delete {word1[i - 1]} at position {i - 1}")
            i -= 1
        else:
            ops.append(f"replace {word1[i - 1]} with {word2[j - 1]} at position {i - 1}")
            i, j = i - 1, j - 1
    return dp[m][n], list(reversed(ops))
```

The Phase-3 onsite extension. The "print the operations" question discriminates the candidate who memorized the DP from the candidate who understands the table.
