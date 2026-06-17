# Week 14 — Pattern-Recognition Quiz

Ten short prompts. **Do not solve them.** For each, decide which Week-14 shape applies — XOR-cancellation, bitmask-as-set, bitmask DP, plain bit-twiddling, trie (prefix), bitwise trie, or none of the above (re-Match against an earlier week) — and name the key move in one line. Lectures closed. Time yourself — 45 seconds per question is the target.

Answer key at the bottom.

---

**Q1.** "Given a non-empty array where every element appears three times except for one, which appears once, find the single one, using constant extra space."

**Q2.** "Implement a data structure that stores words and answers, for a query string, whether any stored word starts with that string as a prefix."

**Q3.** "Given an array of integers, return the maximum value of `nums[i] XOR nums[j]` over all pairs."

**Q4.** "Given `n <= 14` cities and a cost matrix, find the minimum-cost route that starts at city 0, visits every city exactly once, and returns to city 0."

**Q5.** "Given a positive integer `n`, return True iff `n` is a power of two."

**Q6.** "Given an array `nums` of `n` distinct numbers taken from the range `[0, n]`, return the one number in the range that is missing."

**Q7.** "Given a list of strings, group them so that each group shares a common prefix of at least length 3, and return the largest group."

**Q8.** "Given an array of integers, return the element that appears more than `n/2` times (the majority element), in `O(1)` space."

**Q9.** "Given an array `nums` of length `n <= 16` and a target, return True iff `nums` can be split into two subsets with equal sums."

**Q10.** "Given a sorted array and a target, return the index of the target or -1 if absent."

---

## Answer key

<details>
<summary>Click after attempting all ten</summary>

1. **Bit manipulation — not plain XOR-cancellation.** XOR cancels in *pairs*, so it does not directly handle triples. The canonical move is a per-bit count modulo 3, or the two-accumulator (`ones`, `twos`) state machine. Single number II (LC 137). The discriminator from Q-type XOR: when copies come in threes, plain XOR fails; you count bits mod 3. Lecture 1 §3-4 (the limits of XOR-cancellation).

2. **Trie — prefix query.** `insert` / `starts_with`. State: a trie node per character; `starts_with` walks and checks reachability (not `is_end`). LC 208. Lecture 2 §5.

3. **Bitwise trie.** Insert each number's bits (high to low) into a 0/1 trie; for each number, greedily walk toward the opposite bit. `O(n * B)`. LC 421, Challenge 1. The bridge problem. Lecture 2 §6.

4. **Bitmask DP — Held-Karp.** State `dp[mask][last]` = min cost of a route visiting exactly `mask`, ending at `last`. `n <= 14` is the tell. `O(2^n * n^2)`. The travelling-salesman DP. Lecture 2 §3.

5. **Plain bit-twiddling.** `n > 0 and n & (n - 1) == 0` — a power of two has exactly one set bit, so clearing it yields zero. LC 231. Lecture 1 §7.

6. **Bit manipulation — XOR-of-indices, or the Gauss sum.** XOR all indices `0..n` with all values; matched index/value pairs cancel, the missing index survives. Or `n(n+1)/2 - sum(nums)`. `O(n)` time, `O(1)` space. LC 268. The XOR form is the overflow-safe variant. Lecture 1 §5.

7. **Trie — prefix grouping.** Insert all strings into a trie; the largest group sharing a length-3 prefix is the most-populated node at depth 3. The discriminator: "common prefix" is the trie tell. Not a bit problem. Lecture 2 §5 (trie traversal).

8. **Not a Week-14 pattern — Boyer-Moore majority vote.** A single-pass `O(n)` time, `O(1)` space scan tracking a candidate and a count. The `O(1)` space might *suggest* a bit trick, but the right tool is the majority-vote algorithm (a Phase-1/earlier pattern). The senior signal: recognize this is *not* XOR (XOR would not isolate a `> n/2` element) and reach for Boyer-Moore. The negative-space rejection.

9. **Bitmask DP (or subset-sum DP).** With `n <= 16`, enumerate subsets via bitmask: `dp[mask]` tracks reachable subset sums, or directly check if any submask sums to `total / 2`. Partition equal subset sum (LC 416), here in the bitmask regime. Lecture 2 §3; Challenge 2 is the k-subset generalization.

10. **Not a Week-14 pattern — binary search.** Sorted array plus "find the index" is the Week-5 binary-search tell, not bit manipulation. The `>>` in a midpoint computation (`mid = (lo + hi) >> 1`) is a bit operation but does not make this a bit problem. The negative-space rejection: do not over-apply Week-14 patterns to a classic search.

</details>

---

## How to score

| Score | Meaning |
|------:|---------|
| 9-10 | Week-14 recognition is interview-ready, including the negative-space rejections (Q8 majority vote, Q10 binary search) and the XOR-limit case (Q1 triples). Move on. |
| 7-8 | Good — re-read [Lecture 1 §3-4](./02-lecture-notes/01-bit-manipulation-and-xor-tricks.md) (XOR limits) and [Lecture 2 §3, §6](./02-lecture-notes/02-bitmasks-bitmask-dp-and-tries-at-speed.md) (bitmask DP and the bitwise trie) for the shapes you missed. Most learners miss Q1 (triples break plain XOR) or Q8 (majority vote, not a bit trick) first time; that is normal. |
| 5-6 | Redo Exercises 1 and 2 with stricter Match sections, and re-walk Challenge 1 (Maximum XOR). The XOR-cancellation tells and the bitwise trie need more reps before Mock #4. |
| <5 | The recognition is not yet automatic. Re-read all three lectures, re-do all three exercises with the move stated aloud, then retake the quiz. |

This quiz is about **fluency**, not difficulty. The discriminating questions are Q8 (negative space — majority vote, not a bit trick), Q10 (binary search, not a bit problem), and Q1 (the triple case where plain XOR-cancellation breaks). Q8 is the most-missed; candidates over-apply XOR to any `O(1)`-space array problem.

Q3 (maximum XOR / bitwise trie) and Q4 (Held-Karp bitmask DP) test the two highest-leverage Week-14 shapes. Q2 and Q5 are the cleanest direct-template questions (trie prefix; power-of-two bit test).

When done, the [homework](./06-homework.md) is next.
