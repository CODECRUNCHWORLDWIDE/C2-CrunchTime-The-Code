# Week 11 — Worked Solutions

Three worked solutions, each with UMPIRE narration. **Attempt every exercise on your own first.** If you read this file before drafting your own, you forfeit the recognition rep — and recognition is what Phase 2 is grading.

The solutions below are written in the same voice you should be using in your portfolio write-ups. Read them as templates, not as the answer.

---

## Solution 1 — Climbing Stairs (LC 70)

### Understand

We have an integer `n` and we want to count the number of distinct ways to climb `n` stairs taking 1-step or 2-step moves. A "way" is a sequence of 1s and 2s summing to `n`.

Hand-walk on `n = 5`:

```
Ways to reach step 5:
  1+1+1+1+1, 1+1+1+2, 1+1+2+1, 1+2+1+1, 2+1+1+1,
  1+2+2, 2+1+2, 2+2+1
Count: 8
```

### Match

1D counting DP. The 30-second memo:

> *Counting problem on a 1D state. State = "number of ways to reach step i." Recurrence: dp[i] = dp[i-1] + dp[i-2] (one-step from i-1 or two-step from i-2). Overlapping subproblems (the recursion `f(i) = f(i-1) + f(i-2)` revisits the same arguments). Optimal substructure (the count composes from sub-counts). O(n) time with tabulation; O(1) space with rolling pair. Why not naive recursion: O(2^n). Why not memoization: same O(n) time but O(n) stack and cache.*

### Plan

1. Handle the base cases `n <= 2`.
2. Initialize the rolling pair `prev2 = 1, prev1 = 2` (corresponding to `dp[1] = 1, dp[2] = 2`).
3. Loop from `i = 3` to `n` inclusive, updating the rolling pair.
4. Return `prev1` (the value of `dp[n]` after the final update).

### Implement

```python
from __future__ import annotations


def climb_stairs(n: int) -> int:
    """Return the number of distinct ways to climb n stairs."""
    if n <= 2:
        return n
    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        prev2, prev1 = prev1, prev2 + prev1
    return prev1
```

### Review

Trace `n = 5`:

```
Initial: prev2 = 1, prev1 = 2
i = 3: prev2, prev1 = 2, 1 + 2 = 3
i = 4: prev2, prev1 = 3, 2 + 3 = 5
i = 5: prev2, prev1 = 5, 3 + 5 = 8
Return prev1 = 8.
```

Matches the hand-enumeration above.

### Evaluate

- **Time:** `O(n)`. Single loop from 3 to n.
- **Space:** `O(1)`. Two scalar variables.
- **Trade-off:** vs. naive recursion `O(2^n)` (impractical for n = 45 — ~3.5e13 operations). vs. memoized recursion `O(n)` time and space — same time, more space, plus recursion stack. Tabulation strictly dominates for this problem.

---

## Solution 2 — Longest Common Subsequence (LC 1143)

### Understand

We have two strings `s1` and `s2`; return the length of their longest common subsequence. A subsequence allows skipping characters but preserves order. The LCS of `"abcde"` and `"ace"` is `"ace"` of length 3.

Hand-walk the table on `s1 = "abcde", s2 = "ace"`:

```
     ""  a  c  e
""    0  0  0  0
a     0  1  1  1
b     0  1  1  1
c     0  1  2  2
d     0  1  2  2
e     0  1  2  3

Answer: dp[5][3] = 3.
```

### Match

2D string-pair DP. The 30-second memo:

> *Two-string optimization problem. State = "length of LCS of s1[:i] and s2[:j]." Recurrence has two cases: match -> dp[i-1][j-1] + 1; no-match -> max(dp[i-1][j], dp[i][j-1]). The third predecessor `dp[i-1][j-1]` in the no-match case is dominated and is dropped. O(mn) time with tabulation; O(min(m, n)) space with rolling rows. Why not brute-force recursion: O(2^(m+n)). Why not memoization: same O(mn) time, O(mn) space; tabulation matches space and skips function-call overhead.*

### Plan

1. Extract `m = len(s1), n = len(s2)`.
2. Initialize a `(m + 1) x (n + 1)` DP table with zeros (zero-initializes the base cases).
3. Iterate `i` from 1 to `m`, `j` from 1 to `n`.
4. If `s1[i - 1] == s2[j - 1]`: `dp[i][j] = dp[i - 1][j - 1] + 1`.
5. Else: `dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])`.
6. Return `dp[m][n]`.

### Implement

```python
from __future__ import annotations

from typing import List


def longest_common_subsequence(text1: str, text2: str) -> int:
    """Length of the longest common subsequence of text1 and text2."""
    m, n = len(text1), len(text2)
    dp: List[List[int]] = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]
```

### Review

Trace the corner of the example above: `i = 5, j = 3` reads `s1[4] = 'e'` and `s2[2] = 'e'`. Match. `dp[5][3] = dp[4][2] + 1 = 2 + 1 = 3`. Correct.

Trace the no-match corner: `i = 2, j = 1` reads `s1[1] = 'b'` and `s2[0] = 'a'`. No match. `dp[2][1] = max(dp[1][1], dp[2][0]) = max(1, 0) = 1`. Correct.

### Evaluate

- **Time:** `O(mn)`. Double loop over the table.
- **Space:** `O(mn)` for the table. Reducible to `O(min(m, n))` with rolling rows (Lecture 2 §6).
- **Trade-off:** vs. brute-force recursion `O(2^(m+n))` — impractical for `m, n = 1000`. vs. memoized recursion — same `O(mn)` time and space but slower in practice due to function-call overhead.

---

## Solution 3 — Word Break (LC 139)

### Understand

We have a string `s` and a list of dictionary words. Return `True` iff `s` can be segmented into a sequence of dictionary words. Words can be reused.

Hand-walk on `s = "leetcode", word_dict = ["leet", "code"]`:

```
dp[0] = True (empty prefix; base case)
i = 4: try j = 0: dp[0] = T and s[0:4] = "leet" in dict -> dp[4] = T
i = 8: try j = 4: dp[4] = T and s[4:8] = "code" in dict -> dp[8] = T

Return dp[8] = True.
```

### Match

1D boolean DP. The 30-second memo:

> *Segmentation feasibility. 1D boolean DP. State = "True iff s[:i] is segmentable." Recurrence: OR over all valid split points j, where dp[j] is True and s[j:i] is in the word set. O(n^2 * L) time where L is average word length (substring slice + hash). O(n) space. Why convert word_dict to a set: O(1)-expected lookup. Why not greedy: greedy left-to-right matching fails when a longer match precludes a valid segmentation (the "dog" / "sand"/"andog" failure mode). Why not BFS: same asymptotic; DP form is shorter and reuses no auxiliary data structures.*

### Plan

1. Convert `word_dict` to a set.
2. Initialize `dp = [False] * (n + 1)` with `dp[0] = True`.
3. Iterate `i` from 1 to `n`. For each `i`, iterate `j` from 0 to `i - 1`.
4. If `dp[j]` and `s[j:i]` in the set, set `dp[i] = True` and break.
5. Return `dp[n]`.

### Implement

```python
from __future__ import annotations

from typing import List


def word_break(s: str, word_dict: List[str]) -> bool:
    """Return True iff s can be segmented into a sequence of dictionary words."""
    word_set = set(word_dict)
    n = len(s)
    dp: List[bool] = [False] * (n + 1)
    dp[0] = True

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[n]
```

### Review

Trace `s = "catsandog", word_dict = ["cats", "dog", "sand", "and", "cat"]`:

```
dp[0] = T
i = 3: try j = 0: s[0:3] = "cat" in set -> dp[3] = T.
i = 4: try j = 0: s[0:4] = "cats" in set -> dp[4] = T.
i = 6: try j = 3: dp[3] = T and s[3:6] = "san" not in set.
       try j = 4: dp[4] = T and s[4:6] = "sa" not in set.
       dp[6] = F.
i = 7: try j = 3: dp[3] = T and s[3:7] = "sand" in set -> dp[7] = T.
i = 8: try j = 4: dp[4] = T and s[4:8] = "sand" in set -> dp[8] = T.
       (Also j = 7: dp[7] = T and s[7:8] = "o" not in set.)
i = 9: try j = 0..8; no valid split (the suffix "og" / "dog" attempt fails:
       s[6:9] = "dog" but dp[6] = F; s[7:9] = "og" not in set; etc.)
       Wait -- dp[7] = T and s[7:9] = "og" not in set; dp[8] = T and s[8:9] = "g" not in set.
       dp[9] = F.

Return dp[9] = False.
```

The "dog" trap is the discriminator: `s[6:9] = "dog"` is in the set, but `dp[6] = False`, so the split is rejected. The DP correctly identifies that "catsandog" cannot be segmented even though every individual sub-word is in the dictionary.

### Evaluate

- **Time:** `O(n^2 * L)` where `L` is the average length of `s[j:i]` (the substring slice and the set-lookup hash). For `n = 300`, `L ≤ 20`, this is `~ 9e4 * 20 = 1.8e6` operations — fast.
- **Space:** `O(n)` for the DP array plus `O(W * L)` for the set, where `W = len(word_dict)`.
- **Trade-off:** vs. greedy — incorrect on the LC 139 example 3 (would pick "cats" first and fail). vs. BFS over the prefix graph — same asymptotic; DP form is shorter.

---

## Closing — common bugs and how to avoid them

Across all three exercises:

1. **Off-by-one on the table dimension.** LCS uses `(m + 1) x (n + 1)` because `dp[0][...]` and `dp[...][0]` are the empty-prefix base cases. Indexing `s1[i]` instead of `s1[i - 1]` is the canonical bug.
2. **Forgetting to convert the list to a set.** Word break with `word_dict` as a list is `O(n^2 * W * L)`; with a set it is `O(n^2 * L)`. For LC 139 the difference is the time-limit pass/fail boundary.
3. **The base case `dp[0] = True`** in word break. Without it, the entire table fills with `False` and the answer is always wrong.
4. **The rolling-pair simultaneous assignment.** Climbing stairs requires `prev2, prev1 = prev1, prev2 + prev1` on one line; the two-line `prev2 = prev1; prev1 = prev2 + prev1` is wrong because the second line uses the just-updated `prev2`.
5. **Returning the wrong table cell.** `dp[m][n]` for LCS and edit distance; `dp[n]` for 1D DPs; `dp[0][n - 1]` for LPS. Mixing these up costs the problem.

After this set of three, the pattern recognition for any 1D or 2D DP should be reflexive. The week's mini-project (house robber + unique paths) is the proof.

Move on to the [quiz](../quiz.md), then the [homework](../homework.md), then the [mini-project](../mini-project/README.md).
