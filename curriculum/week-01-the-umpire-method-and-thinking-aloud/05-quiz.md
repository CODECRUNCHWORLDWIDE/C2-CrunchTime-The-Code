# Week 1 — Pattern-Recognition Quiz

Ten short prompts. **Do not solve them.** For each, name the pattern and a one-line justification. Lectures closed. Time yourself — 30 seconds per question is the target.

Answer key at the bottom.

---

**Q1.** "Given a sorted array of integers and a target, return the indices of the two numbers that add up to the target."

**Q2.** "Given a string, determine whether it reads the same forwards and backwards considering only alphanumeric characters."

**Q3.** "Given an array of meeting time intervals, determine if a person can attend all meetings."

**Q4.** "Given an array, remove duplicates in place and return the new length."

**Q5.** "Given the head of a linked list, determine whether it has a cycle."

**Q6.** "Given a string `s` and a string `t`, find the smallest substring of `s` that contains all characters of `t`."

**Q7.** "Given two sorted arrays, merge them into a single sorted array."

**Q8.** "Given an integer array, return all unique triplets that sum to zero."

**Q9.** "Given an array of integers and a window size `k`, return the maximum element in each contiguous window of size `k`."

**Q10.** "Given an unsorted array of integers, return the indices of the two numbers that add to a target."

---

## Answer key

<details>
<summary>Click after attempting all ten</summary>

1. **Two-pointer (converging).** Sorted + pair + target — textbook. O(n) with two pointers.
2. **Two-pointer (converging).** Two pointers from each end, skip non-alphanumerics, compare lowercase.
3. **(Out of scope this week — intervals.)** This is the *intervals* pattern, covered in Week 10. Acceptable answer in Week 1: "I'd sort by start time, then check adjacent intervals." That's the right instinct.
4. **Two-pointer (same-direction).** Read pointer scans; write pointer advances on new uniques.
5. **(Out of scope this week — fast/slow pointers.)** Floyd's tortoise and hare, covered in Week 4. Acceptable Week-1 answer: "Two pointers, one moving faster than the other, meeting if there's a cycle."
6. **(Out of scope this week — sliding window.)** Covered Week 3. *Not* two-pointer despite using two indices — the window expands and contracts based on whether `t` is covered.
7. **Two-pointer (two-input).** One pointer per array, take the smaller front element each step.
8. **Pin + two-pointer (converging).** Sort, then for each pinned element run converging two-pointer for the negative complement.
9. **(Out of scope this week — sliding window with monotonic deque.)** Week 3 + Week 9. Acceptable Week-1 answer: "I'd need a deque to maintain the window max in O(1); each element enters/leaves at most once."
10. **Hash map (not two-pointer).** Unsorted, indices matter. Sorting would scramble indices, so two-pointer doesn't directly apply. Covered Week 2.

</details>

---

## How to score

| Score | Meaning |
|------:|---------|
| 9–10 | You can recognize a two-pointer problem at sight. Move on. |
| 7–8 | Good — re-read the cases you missed in [Lecture 3](./02-lecture-notes/03-arrays-and-two-pointers.md). |
| 5–6 | Re-read Lecture 3 and re-do Drills 1, 3, and 4 before Week 2. |
| <5 | The pattern recognition isn't yet automatic. Don't move to Week 2 yet — repeat the drills, re-record yourself. |

This quiz is **not** about solving the problems. It's about recognizing the pattern instantly. That speed is what survives interview pressure.

When done, the [homework](./06-homework.md) is next.
