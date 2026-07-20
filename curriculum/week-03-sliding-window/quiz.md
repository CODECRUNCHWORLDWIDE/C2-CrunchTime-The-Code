# Week 3 — Pattern-Recognition Quiz

Ten short prompts. **Do not solve them.** For each, decide whether it's sliding window or not — and if sliding window, name the sub-shape (fixed-size, variable shape A "longest," variable shape B "shortest," or variable shape C "count"). One-line justification per answer. Lectures closed. Time yourself — 30 seconds per question is the target.

Answer key at the bottom.

---

**Q1.** "Given an array of integers `nums` and an integer `k`, return the maximum sum of any contiguous subarray of length `k`."

**Q2.** "Given a string `s`, return the length of the longest substring that contains all unique characters."

**Q3.** "Given an array of positive integers `nums` and an integer `target`, return the minimum length of a contiguous subarray whose sum is at least `target`."

**Q4.** "Given a sorted array of integers and a target, return the indices of the two numbers that add up to the target."

**Q5.** "Given a string `s` and an integer `k`, return the length of the longest substring of `s` that contains at most `k` distinct characters."

**Q6.** "Given an array of integers (which may include negatives) and an integer `k`, return the number of contiguous subarrays whose sum equals `k`."

**Q7.** "Given a string `s` and a string `p`, return all starting indices of `p`'s anagrams in `s`."

**Q8.** "Given a string `s`, return the longest palindromic substring."

**Q9.** "Given two strings `s` and `t`, return the shortest substring of `s` that contains every character of `t` (counting multiplicities)."

**Q10.** "Given an integer array `nums` and a window size `k`, return the maximum element of each contiguous window of size `k`."

---

## Answer key

<details>
<summary>Click after attempting all ten</summary>

1. **Sliding window — fixed-size.** `k` is given upfront; the algorithm slides a window of size `k` and tracks the running sum. O(n).

2. **Sliding window — variable, shape A (longest).** Contiguous + "longest with property" = shape A. Invariant: all characters in the window are unique. Auxiliary state: a `dict` mapping char → most recent index in window. O(n). This is Drill 2.

3. **Sliding window — variable, shape B (shortest).** Contiguous + "shortest with property" = shape B. Invariant *maintained during shrink*: `running >= target`. Positivity required for sliding window to apply. O(n). This is Drill 4.

4. **NOT sliding window — two-pointer (converging).** Sorted + pair + target = Week 1's pattern. The indices move *toward each other*, not in the same direction. O(n). A common confusion: both patterns use two indices; the geometry of motion is the discriminator.

5. **Sliding window — variable, shape A (longest with at-most-K distinct).** Canonical at-most-K-distinct template. Invariant: `len(counts) <= k`. Auxiliary state: frequency Counter. O(n).

6. **NOT sliding window — prefix sums + hash map.** The negatives break the sliding-window invariant (shrinking doesn't monotonically decrease the sum). Use the Week 2 challenge shape: prefix sums + hash-map frequency. O(n)/O(n). This is the classic "looks like sliding window but isn't."

7. **Sliding window — fixed-size with frequency invariant.** Window size is `len(p)`; the invariant is `window_counts == Counter(p)`. The `Counter`-equality check (with the zero-key discipline) is the auxiliary state. O(n). Sister problem to Drill 3.

8. **NOT sliding window — dynamic programming (or expand-around-center).** Palindromic substring problems have a center, not a monotone window. Common variants are O(n²) DP or the O(n) Manacher's algorithm (out of scope for C2). Will be revisited in Week 11.

9. **Sliding window — variable, shape B + frequency invariant.** This is *Minimum Window Substring*, the Week 3 challenge. The `need/formed` integer pair is the auxiliary state. O(m + n).

10. **Sliding window — fixed-size with a monotonic deque for the max.** Window size `k`, max of each window. Naive `max(window)` per slide is O(n·k); the deque trick makes it O(n). The deque mechanic is Week 9 (top-K), but the **window** part is this week. Acceptable Week-3 answer: "sliding window fixed-size; the max maintenance is a deque trick I'll learn properly in Week 9."

</details>

---

## How to score

| Score | Meaning |
|------:|---------|
| 9–10 | Sliding-window pattern recognition is interview-ready. Move on. |
| 7–8 | Good — re-read [Lecture 1 §8 and §9](lecture-notes/01-the-sliding-window-pattern.md) for the cases you missed (especially Q4, Q6, and Q8 — the negative-space questions). |
| 5–6 | Redo Drills 2, 4, and 5 with stricter Match sections (the 30-second memo) before Week 4. |
| <5 | The pattern recognition is not yet automatic. Re-read both lectures and re-do all five drills with recorder running. |

This quiz is about **fluency**, not difficulty. Every question is something you should be able to answer in under 30 seconds once the patterns are in muscle memory.

When done, the [homework](homework.md) is next.
