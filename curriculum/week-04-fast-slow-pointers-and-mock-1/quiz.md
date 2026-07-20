# Week 4 — Pattern-Recognition Quiz

Ten short prompts. **Do not solve them.** For each, decide whether it's fast/slow pointers or not — and if fast/slow, name the variant (Floyd's detection, Floyd's + entrance, midpoint, functional-graph, nth-from-end). One-line justification per answer. Lectures closed. Time yourself — 30 seconds per question is the target.

Answer key at the bottom.

---

**Q1.** "Given the head of a singly-linked list, determine whether the list contains a cycle. You must use O(1) extra space."

**Q2.** "Given an array of integers, find the longest contiguous subarray with sum at most k. The array contains only non-negative integers."

**Q3.** "Given the head of a singly-linked list, return the middle node. For even-length lists, return the second of the two middle nodes."

**Q4.** "Given two strings `s` and `t`, return the minimum-length substring of `s` containing every character of `t`."

**Q5.** "Given an array `nums` of length n+1 containing integers in the range `[1, n]`, exactly one integer appears two or more times. Find that duplicate. You must use O(1) extra space and may not modify the array."

**Q6.** "Determine whether the integer `n` is a 'happy number' — does repeated digit-square-summing reach 1?"

**Q7.** "Given the head of a linked list, remove the nth node from the end and return the modified head. Do it in a single pass."

**Q8.** "Given a directed graph with multiple nodes and edges, determine whether the graph contains a cycle."

**Q9.** "Given the head of a linked list, return the node where the cycle begins. If there's no cycle, return None. O(1) extra space."

**Q10.** "Given a string `s`, return `True` if `s` is a palindrome considering only alphanumeric characters and ignoring case."

---

## Answer key

<details>
<summary>Click after attempting all ten</summary>

1. **Fast/slow — Floyd's cycle detection.** "Linked list" + "cycle" + "O(1) space" is the triple signal. Walk slow by 1, fast by 2; meet = cycle, fast hits None = no cycle. O(n) time. This is Drill 1.

2. **NOT fast/slow — sliding window** (Week 3, shape A "longest"). Contiguous + non-negatives + "longest with property" is the canonical sliding-window signal. The misdirection: "two indices on an array" sounds like fast/slow, but the *speed* is the same (both lockstep). Sliding window.

3. **Fast/slow — midpoint with the speed-2 hare.** Single-pass middle of a singly-linked list is the canonical Drill 3 pattern. Upper-middle convention (for even length, return the second of the two middles) is what the loop guard `fast and fast.next` produces. This is Drill 3.

4. **NOT fast/slow — sliding window, variable shape B + frequency invariant** (Week 3 challenge). Different family entirely. The misdirection: "two strings, find a substring" sounds like it could be a pointer family, but the underlying structure is the sliding window with a `need/formed` integer.

5. **Fast/slow on a functional graph — LeetCode 287 ("Find the Duplicate Number").** The map `i → nums[i]` defines a functional graph (each index has exactly one outgoing edge). Floyd's detects the cycle, and the cycle entrance *is* the duplicate. This is one of the most beautiful applications of the pattern; it's in the homework. O(n) time, O(1) space.

6. **Fast/slow on a functional graph.** The map `n → digit_square_sum(n)` is a functional graph. Happy = chain reaches 1; not happy = chain enters a non-1 cycle, detected by Floyd's. O(1) space — the interview tell over the `seen = set()` approach. This is Drill 4.

7. **Fast/slow with a fixed gap — "nth from the end" single-pass.** A variant of the family: advance `fast` by `n` steps first, then walk `slow` and `fast` in lockstep until `fast` reaches the end. Slow lands on the (n+1)th-from-the-end, which is the node *before* the one to remove. Different mechanic from Floyd's, same family. Single-pass + O(1) space is the interview tell. (Homework Problem 2.)

8. **NOT fast/slow — DFS with colors / topological sort** (Week 7). Floyd's needs *each node to have exactly one outgoing edge* (functional graph). A general directed graph has arbitrary out-degree, so Floyd's doesn't apply. Use DFS with three colors (white / gray / black) — the gray-back-edge is the cycle signal.

9. **Fast/slow — Floyd's detection + `2k = k + nC` cycle-entrance lemma.** This is LeetCode 142, Drill 2 of this week. Phase 1 detects, Phase 2 finds the entrance by walking a third pointer from `head` and slow from the meeting point at speed 1 until they meet.

10. **NOT fast/slow — two-pointer converging** (Week 1). Palindrome check is a classic two-pointer-converging problem: `left = 0, right = n-1`, move toward each other comparing characters. *Different geometry of motion* — converging, not same-direction at different speeds.

</details>

---

## How to score

| Score | Meaning |
|------:|---------|
| 9–10 | Fast/slow pattern recognition is interview-ready. Move on. |
| 7–8 | Good — re-read [Lecture 1 §7 and §8](lecture-notes/01-floyds-tortoise-and-hare.md) for the cases you missed (especially Q5, Q7, and Q8 — the negative-space questions). |
| 5–6 | Redo Drills 1, 2, and 4 with stricter Match sections before Mock #1. |
| <5 | The pattern recognition is not yet automatic. Re-read both lectures and re-do all four drills with recorder running before attempting the mock. |

This quiz is about **fluency**, not difficulty. Every question is something you should be able to answer in under 30 seconds once the patterns are in muscle memory. The negative-space questions (Q2, Q4, Q8, Q10) are the discriminators — they're the *not*-fast/slow problems, and being able to *reject* the pattern cleanly is the same skill as recognizing it.

When done, the [homework](homework.md) is next.
