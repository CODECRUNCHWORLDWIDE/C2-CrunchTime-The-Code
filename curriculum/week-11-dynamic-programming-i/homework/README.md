# Week 11 — Homework

Six practice problems plus the rubric. Allow ~5 hours total. Do the problems on your own with the lectures *closed*; consult the lecture or the resources only after a 15-minute stuck-period on a single problem.

The problems are chosen to drill the six Week-11 sub-patterns: 1D counting, 1D optimization (../take-or-skip), 1D conditional transition, 2D grid optimization, 2D subsequence (LCS variant), and 2D three-way-min (edit distance variant). By Sunday, the recognition step on each should be reflexive.

| # | Problem | Pattern | Source | Est. time |
|---|---------|---------|--------|----------:|
| 1 | Decode Ways | 1D DP — conditional transition | LeetCode 91 | 50 min |
| 2 | Minimum Path Sum | 2D grid optimization DP | LeetCode 64 | 40 min |
| 3 | Maximum Product Subarray | 1D DP — track both min and max | LeetCode 152 | 50 min |
| 4 | Distinct Subsequences | 2D DP — counting subsequences | LeetCode 115 | 60 min |
| 5 | Interleaving String | 2D boolean DP — string merge | LeetCode 97 | 50 min |
| 6 | Delete Operation for Two Strings | 2D DP — LCS in disguise | LeetCode 583 | 30 min |

Problems 1, 3, and 6 are the high-yield 1D and 2D drills; problem 2 is the grid rep; problem 4 is the rare counting-subsequence DP; problem 5 is the boolean 2D rep.

---

## Problem 1 — Decode Ways (LC 91)

**Spec.** A message containing letters from A–Z is encoded to numbers using the mapping 'A' -> '1', ..., 'Z' -> '26'. Given a string `s` containing only digits, return the number of ways to decode it.

**Constraints.** `1 <= s.length <= 100`; `s` contains only digits and may contain leading zeros.

**Pattern.** 1D DP with conditional transitions (Lecture 1 §6).

**Hint.** State: `dp[i] = ways to decode s[:i]`. Two conditional branches: add `dp[i - 1]` if `s[i - 1]` is in `'1'..'9'`; add `dp[i - 2]` if `s[i - 2 : i]` is in `'10'..'26'`. Base case: `dp[0] = 1`.

**Acceptance.** Function signature `num_decodings(s: str) -> int`. Time: `O(../n)`. Space: `O(../n)` for the array; reducible to `O(../1)` with a rolling pair.

**Variant.** Memoization with `@functools.lru_cache(../maxsize=None)` is the easier-to-write form; tabulation with rolling pair is the optimization. Discuss the trade.

---

## Problem 2 — Minimum Path Sum (LC 64)

**Spec.** Given an `m x n` grid filled with non-negative numbers, find a path from top-left to bottom-right that *minimizes* the sum of all numbers along its path. You can only move down or right.

**Constraints.** `1 <= m, n <= 200`; `0 <= grid[i][j] <= 200`.

**Pattern.** 2D grid optimization DP (Lecture 2 §2 variant).

**Hint.** State: `dp[i][j] = minimum path sum from (0, 0) to (i, j)`. Recurrence: `dp[i][j] = grid[i][j] + min(dp[i - 1][j], dp[i][j - 1])`. Base cases: `dp[0][0] = grid[0][0]`; first row is cumulative sum left-to-right; first column is cumulative sum top-to-bottom.

**Acceptance.** Function signature `min_path_sum(grid: List[List[int]]) -> int`. Time: `O(../mn)`. Space: `O(../n)` rolling row.

**Variant.** In-place modification of `grid` to use `O(../1)` extra space. Mention by name.

---

## Problem 3 — Maximum Product Subarray (LC 152)

**Spec.** Given an integer array `nums`, find a contiguous non-empty subarray within the array that has the largest product, and return the product.

**Constraints.** `1 <= len(../nums) <= 2 * 10^4`; `-10 <= nums[i] <= 10`.

**Pattern.** 1D DP that tracks **both** the running maximum *and* the running minimum at each index (because a negative number can flip a small minimum into a large maximum).

**Hint.** Track two scalars: `max_so_far` and `min_so_far`. At each `nums[i]`, the new `max_ending_here = max(nums[i], nums[i] * max_so_far, nums[i] * min_so_far)`; the new `min_ending_here = min(../...)`. Update the global max. The discriminator versus the maximum-subarray problem (Kadane's algorithm): products can flip sign with negative numbers, so tracking only the max is wrong.

**Acceptance.** Function signature `max_product(nums: List[int]) -> int`. Time: `O(../n)`. Space: `O(../1)`.

**Variant.** A full 2D DP `dp[i][0] = max, dp[i][1] = min` is equivalent and is the textbook form. The two-scalar form is the rolling-pair reduction.

---

## Problem 4 — Distinct Subsequences (LC 115)

**Spec.** Given two strings `s` and `t`, return the number of distinct subsequences of `s` which equals `t`.

**Constraints.** `1 <= s.length, t.length <= 1000`; `s` and `t` consist of English letters.

**Pattern.** 2D DP — counting subsequences (Lecture 2 §3 variant; LCS in shape but counting instead of length).

**Hint.** State: `dp[i][j] = number of distinct subsequences of s[:i] that equal t[:j]`. Recurrence: if `s[i - 1] == t[j - 1]`, then `dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j]` (use this match, or skip `s[i - 1]`); otherwise `dp[i][j] = dp[i - 1][j]` (skip `s[i - 1]`). Base case: `dp[i][0] = 1` (empty target has one subsequence — the empty subsequence).

**Acceptance.** Function signature `num_distinct(s: str, t: str) -> int`. Time: `O(../mn)`. Space: `O(../mn)`; reducible to `O(min(m, n))`.

**Variant.** The recurrence is *very close* to LCS but **counts** instead of taking the max. This is the canonical example that the same table shape supports different recurrences.

---

## Problem 5 — Interleaving String (LC 97)

**Spec.** Given strings `s1`, `s2`, and `s3`, return `True` iff `s3` is formed by an interleaving of `s1` and `s2`. An interleaving picks characters from `s1` and `s2` in order without rearranging within each string.

**Constraints.** `0 <= s1.length, s2.length <= 100`; `s1.length + s2.length == s3.length`.

**Pattern.** 2D boolean DP.

**Hint.** State: `dp[i][j] = True iff s3[:i + j] is an interleaving of s1[:i] and s2[:j]`. Recurrence: `dp[i][j] = (dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]) or (dp[i][j - 1] and s2[j - 1] == s3[i + j - 1])`. Base case: `dp[0][0] = True`; first row and column initialize via the running match against `s3`.

**Acceptance.** Function signature `is_interleave(s1: str, s2: str, s3: str) -> bool`. Time: `O(../mn)`. Space: `O(min(m, n))` rolling row.

**Variant.** BFS / DFS with memoization is the alternative — equivalent in complexity but slower in practice. Mention by name.

---

## Problem 6 — Delete Operation for Two Strings (LC 583)

**Spec.** Given two strings `word1` and `word2`, return the minimum number of deletions required to make `word1` and `word2` equal. You can delete one character from either string at each step.

**Constraints.** `1 <= word1.length, word2.length <= 500`; lowercase English letters.

**Pattern.** 2D DP — LCS in disguise.

**Hint.** The minimum number of deletions to make the strings equal is `m + n - 2 * LCS(word1, word2)`. The LCS is the largest set of characters that *do not need to be deleted*; the rest are deleted from one side or the other.

**Acceptance.** Function signature `min_distance_deletions(word1: str, word2: str) -> int`. Time: `O(../mn)`. Space: `O(min(m, n))`.

**Variant.** A direct DP `dp[i][j] = deletions to make word1[:i] and word2[:j] equal` is also correct; the recurrence is `dp[i - 1][j - 1]` if match, `1 + min(dp[i - 1][j], dp[i][j - 1])` otherwise (no replace option, since only deletion is allowed). The two forms produce the same answer; the LCS-based form is cleaner.

---

## Rubric

For each problem, your write-up is graded on five dimensions:

| Dimension | Weight | What "yes" looks like |
|-----------|-------:|----------------------|
| Research constraints (pattern recognition) | 25% | 30-second memo at the top; pattern named in one of the six shapes; alternative rejected with reason |
| Assess options | 15% | Numbered steps; state semantics stated in words; recurrence stated in formula |
| Make the solution (../correctness) | 25% | All LC sample cases pass; no off-by-one on the table dimension; the index-offset (`s[i - 1]`, not `s[i]`) is correct |
| Make the solution (../style) | 10% | Type hints everywhere; docstrings on every function; PEP 8; idiomatic Python |
| Examine (../defense) | 25% | Time + space bounds with derivation; one variant mentioned; trade against a non-DP alternative stated |

The Research constraints weight is the highest for a reason. Phase 2 grades recognition heavily; you can have a working implementation and still lose the rep if you cannot defend the choice over the alternative.

---

## Suggested order

1. **Problem 1** first — Decode Ways is the highest-recognition-density 1D DP. The conditional-transition pattern cements the Lecture 1 §6 template.
2. **Problem 2** second — Minimum Path Sum is the canonical 2D grid optimization. The min-over-two recurrence is the simplest 2D rep.
3. **Problem 6** third — Delete Operation is LCS in disguise. Quick rep on the LCS template.
4. **Problem 3** fourth — Maximum Product Subarray is the rare 1D DP that requires tracking two scalars. The discriminator vs. Kadane's algorithm is the recognition rep.
5. **Problem 4** fifth — Distinct Subsequences is the counting-subsequence DP. The "same table shape, different recurrence" lesson is the work.
6. **Problem 5** last — Interleaving String is the 2D boolean DP. Save for the latter half of the week; the state design (`dp[i][j]` against `s3[i + j - 1]`) is the work.

If time runs out, prioritize Problems 1, 2, and 6. They are the three patterns most likely to appear on Mock #2.

---

## Acceptance

The week's homework is complete when:

- All six problems have a committed implementation under `homework/c2-week-11/`.
- All six problems have a FRAME write-up under `frame-writeups/c2-week-11/homework/`.
- The quiz is taken and scored.
- The score is in the retrospective: which sub-pattern needs the most reps before Mock #2.

The retrospective is the single most useful artifact this week. The pattern most candidates need more reps on after W11 is "the state semantics in words" — the recurrence is easy to memorize, but the discipline of saying out loud "the state is `dp[i][j] = ...`" before writing the recurrence separates the senior signal from the junior one. Drill the verbal Research-constraints step in writing, then drill it aloud.
