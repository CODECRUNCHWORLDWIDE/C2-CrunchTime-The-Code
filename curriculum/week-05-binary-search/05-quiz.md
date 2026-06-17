# Week 5 — Pattern-Recognition Quiz

Ten short prompts. **Do not solve them.** For each, decide whether it's binary search or not — and if binary search, name the variant (classic / lower bound / upper bound / rotated / parametric / partition predicate). One-line justification per answer. Lectures closed. Time yourself — 45 seconds per question is the target (slightly longer than Phase 1 quizzes; parametric recognition is harder).

Answer key at the bottom.

---

**Q1.** "Given a sorted (ascending) array of distinct integers and a target value, return the index of the target if present, or -1 otherwise. O(log n) time required."

**Q2.** "Given an integer array `weights` and an integer `D`, partition the array into `D` contiguous groups so that the maximum group sum is minimized. Return that minimum maximum sum."

**Q3.** "Given a string `s`, return the longest palindromic substring."

**Q4.** "Given a sorted array of integers with duplicates and a target, return `[first, last]` — the leftmost and rightmost indices of the target. O(log n) time required."

**Q5.** "Given an integer array `nums` of length n+1 containing integers in `[1, n]`, exactly one integer appears twice. Find that duplicate. O(1) extra space, may not modify the array."

**Q6.** "Given a rotated sorted array of distinct integers and a target, return the index of the target if present, or -1 otherwise. O(log n) time."

**Q7.** "Given `m` packages with positive weights and `D` days, find the minimum ship capacity such that all packages can be shipped within `D` days, where packages must be loaded in order."

**Q8.** "Given a sorted array `arr` and a target `t`, return all pairs of indices (i, j) with i < j such that `arr[i] + arr[j] == t`."

**Q9.** "Given an n x n matrix where each row and each column is sorted ascending, return the kth smallest element. Better than O(n²) time."

**Q10.** "Given two sorted arrays `nums1` and `nums2`, return the median of the merged sorted array. O(log(min(m, n))) time required."

---

## Answer key

<details>
<summary>Click after attempting all ten</summary>

1. **Binary search — variant 1 (classic, find any).** "Sorted array + target + O(log n)" is the canonical triple signal. Closed-interval template; return mid on match, -1 otherwise. This is Drill 1.

2. **Binary search on the answer — parametric (Pattern A: minimize the maximum).** Reframe: find the smallest `k` such that `feasible(k) = (we can partition into D groups, each with sum <= k)` is True. Interval: `[max(weights), sum(weights)]`. Monotone because a larger cap never makes the partitioning harder. LeetCode 410, "Split Array Largest Sum" — homework problem.

3. **NOT binary search — expand around center, or DP.** No sorted structure, no monotone predicate on a bounded answer space. The pattern is expand-around-center for O(n²) time, or Manacher's algorithm for O(n). Out of scope for Week 5.

4. **Binary search — variants 2 + 3 (lower / upper bound), two searches.** "Sorted with duplicates" + "first and last" is the dual lower-bound trick. Two `O(log n)` lower-bound calls; total `O(log n)`. This is Drill 2.

5. **NOT binary search** (despite the "O(1) extra space" tell). The structural pattern is **fast/slow on a functional graph** — same as Week 4's homework Problem 1 (LeetCode 287, "Find the Duplicate Number"). Define `f(i) = nums[i]`; the duplicate is the entrance of the cycle in this functional graph. Floyd's, not binary search. (Misdirection: there *is* a binary-search-on-the-answer solution for this problem too — count `nums[i] <= k` and search for the boundary — but that variant is `O(n log n)`, strictly worse than the `O(n)` fast/slow approach. The interview-correct answer is Floyd's.)

6. **Binary search — variant 1 with "which half sorted?" branch.** "Rotated sorted array + target + O(log n)" is the canonical signal. The discriminator `arr[lo] <= arr[mid]` tells you which half is sorted; then check whether target is in it. This is Drill 3.

7. **Binary search on the answer — parametric (Pattern A: minimize the threshold).** Reframe: find the smallest capacity `c` such that `feasible(c) = (days_needed(c) <= D)`. Interval: `[max(weights), sum(weights)]`. Same shape as Q2; this is LeetCode 1011, "Capacity to Ship Packages in D Days" — homework problem.

8. **NOT binary search — two-pointer converging** (Week 1) or hash map (Week 2). The pair-sum-target problem on a sorted array is two-pointer; on an unsorted array it is hash map. Binary search would search for `t - arr[i]` for each `i`, giving `O(n log n)` — strictly worse than two-pointer's `O(n)` once the array is sorted.

9. **Binary search on values + count predicate.** "n x n row- and column-sorted matrix + kth smallest + better than O(n²)" is the canonical Drill 4 signal. Binary-search the value range using `count_le(v)` via the staircase walk. Total `O(n log M)`.

10. **Binary search on the partition.** "Two sorted arrays + median + O(log(min(m, n)))" is the canonical Median of Two Sorted Arrays signal. Search the partition index of the shorter array using the partition predicate (`left1 <= right2 AND left2 <= right1`). This is the week's challenge.

</details>

---

## How to score

| Score | Meaning |
|------:|---------|
| 9-10 | Binary-search pattern recognition is interview-ready, including parametric and the negative-space rejections. Move on. |
| 7-8 | Good — re-read [Lecture 2 §6](./02-lecture-notes/02-binary-search-on-the-answer.md) for the parametric questions you missed. Most learners miss one of Q2 or Q7; that is normal on the first pass. |
| 5-6 | Redo Drills 4 and 5 with stricter Match sections. The parametric recognition needs more reps before Mock #2. |
| <5 | The pattern recognition is not yet automatic. Re-read both lectures, re-do all five drills with the four-element memo, then retake the quiz. |

This quiz is about **fluency**, not difficulty. The discriminating questions are Q2 and Q7 — both parametric problems that do not mention "binary search" or "log n" in the prompt. Recognizing them is the senior-level skill being measured.

The negative-space questions (Q3, Q5, Q8) are also discriminators. Q5 in particular is a trap: the constraints look like binary-search-on-the-answer (`O(1)` space, may not modify the array), but the optimal answer is fast/slow on a functional graph. Knowing which pattern to *reject* is as important as knowing which to apply.

When done, the [homework](./06-homework.md) is next.
