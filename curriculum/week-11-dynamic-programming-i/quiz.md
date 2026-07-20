# Week 11 — Pattern-Recognition Quiz

Ten short prompts. **Do not solve them.** For each, decide which Week-11 shape applies — 1D DP (counting / optimization / boolean) or 2D DP (grid / string-pair / single-string-two-ends) or none of the above — and name the recurrence in one line. Lectures closed. Time yourself — 45 seconds per question is the target.

Answer key at the bottom.

---

**Q1.** "Given an integer `n`, count the number of distinct ways to reach step `n` if you can move 1, 2, or 3 steps at a time."

**Q2.** "Given an array of non-negative integers representing the maximum jump length from each position, return True iff you can reach the last index starting from the first index."

**Q3.** "Given two strings `s1` and `s2`, return the length of their longest common substring (contiguous, not subsequence)."

**Q4.** "Given an `m x n` grid filled with non-negative numbers, find a path from top-left to bottom-right that minimizes the sum of all numbers along its path. You can only move down or right."

**Q5.** "Given a string of digits, count the number of ways to decode it under the mapping 'A' -> '1', 'B' -> '2', ..., 'Z' -> '26'."

**Q6.** "Given an array of integers, return the length of the longest strictly increasing subsequence."

**Q7.** "Given a string `s`, return True iff `s` can be split into a sequence of dictionary words."

**Q8.** "Given an array of stock prices indexed by day, return the maximum profit you can achieve from at most one buy-sell transaction."

**Q9.** "Given two strings `s1` and `s2`, return the minimum number of character insertions, deletions, or replacements to transform `s1` into `s2`."

**Q10.** "Given a string `s`, find the longest palindromic substring (contiguous, not subsequence) in `s`."

---

## Answer key

<details>
<summary>Click after attempting all ten</summary>

1. **1D counting DP — three-way recurrence.** State: `dp[i] = ways to reach step i`. Recurrence: `dp[i] = dp[i-1] + dp[i-2] + dp[i-3]`. The climbing-stairs variant. Lecture 1 §4.

2. **1D boolean DP (reachability)** — or alternatively a greedy `O(n)` pass. State: `dp[i] = True iff index i is reachable`. Recurrence: `dp[i] = any(dp[j] and j + nums[j] >= i for j in range(i))`. The greedy form (tracking the maximum reachable index) is `O(n)` and dominates; the DP form is `O(n^2)` and is the recognition-grade answer here. The discriminator: this is the rare DP problem where greedy is strictly faster.

3. **2D DP — substring (not subsequence).** State: `dp[i][j] = length of the longest common SUBSTRING ending at s1[i-1] and s2[j-1]`. Recurrence: match -> `dp[i-1][j-1] + 1`; no-match -> 0 (reset). The answer is `max(dp[i][j])` over the table, not `dp[m][n]`. The discriminator from LCS: substring vs. subsequence. Lecture 2 §5.

4. **2D grid DP — optimization (min).** State: `dp[i][j] = min path sum from (0,0) to (i,j)`. Recurrence: `dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])`. The minimum-path variant of unique paths. Lecture 2 §2.

5. **1D DP — counting with conditional transition.** State: `dp[i] = ways to decode s[:i]`. Recurrence: `dp[i] = (dp[i-1] if s[i-1] valid) + (dp[i-2] if s[i-2:i] valid)`. The two conditional branches. Lecture 1 §6.

6. **1D DP — optimization.** State: `dp[i] = length of LIS ending at index i`. Recurrence: `dp[i] = 1 + max(dp[j] for j < i if nums[j] < nums[i])`. `O(n^2)` time. Phase-3 stretch: the patience-sorting `O(n log n)` variant. Not on the W11 syllabus (LIS is W12); flag it.

7. **1D boolean DP — segmentation.** State: `dp[i] = True iff s[:i] is segmentable`. Recurrence: `dp[i] = any(dp[j] and s[j:i] in word_set for j in range(i))`. Exercise 3 exactly. Lecture 1 §7.

8. **Not a Week-11 DP — single-pass scan.** Track minimum price seen so far; track maximum profit as `price - min_so_far`. `O(n)` time, `O(1)` space. The DP form is `dp[i] = max(dp[i-1], prices[i] - min(prices[:i+1]))` but it collapses to the single-pass form. The senior signal: recognize that the DP is trivial and the algorithm is simpler.

9. **2D DP — three-way min (edit distance).** State: `dp[i][j] = min edits to convert s1[:i] to s2[:j]`. Recurrence: match -> `dp[i-1][j-1]`; no-match -> `1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])`. Challenge 1 exactly. Lecture 2 §4.

10. **2D DP — substring (palindromic).** State: `dp[i][j] = True iff s[i..j] is a palindrome`. Recurrence: `dp[i][j] = (s[i] == s[j]) and (length <= 2 or dp[i+1][j-1])`. Iteration order: by substring length. The discriminator from longest palindromic *subsequence*: this requires contiguity. The substring vs. subsequence distinction (Lecture 2 §5) is the most-missed Phase-2 detail. Phase-3 problem; the recognition-grade answer here is "diagonal-fill 2D DP, but for substrings instead of subsequences."

</details>

---

## How to score

| Score | Meaning |
|------:|---------|
| 9-10 | DP recognition is interview-ready, including the negative-space rejections (Q8) and the subsequence-vs-substring discrimination (Q3 and Q10). Move on. |
| 7-8 | Good — re-read [Lecture 1 §6-7](./lecture-notes/01-the-dp-pipeline-and-1d-states.md) and [Lecture 2 §5](./lecture-notes/02-2d-dp-and-the-grid-and-string-shapes.md) for the sub-shape questions you missed. Most learners miss Q8 (greedy not DP) or Q3 (substring vs. subsequence) first time; that is normal. |
| 5-6 | Redo Exercises 2 and 3 with stricter Match sections. The 2D string-pair DP and the segmentation DP need more reps before Mock #2. |
| <5 | The pattern recognition is not yet automatic. Re-read all three lectures, re-do all three exercises with the recurrence stated aloud, then retake the quiz. |

This quiz is about **fluency**, not difficulty. The discriminating questions are Q8 (negative-space — not DP at all, just a single-pass scan), Q3 (substring not subsequence), and Q10 (substring palindromic, different from LPS). Q8 is the most-missed; senior candidates over-apply DP to any optimization problem.

Q1 (climbing stairs three-way) and Q5 (decode ways) are the cleanest direct-template questions. Q4 (minimum path sum) and Q9 (edit distance) test recognition of the 2D grid and 2D string-pair shapes.

When done, the [homework](./homework.md) is next.
