# Week 5 — Challenges

One challenge this week. It is the canonical hard binary-search problem in the standard interview repertoire — the kind of problem that, when solved cleanly, signals senior-level binary-search fluency.

| # | Challenge | Pattern | Difficulty | Target solve time |
|---|-----------|---------|------------|------------------:|
| 1 | [Median of Two Sorted Arrays](challenge-01-median-of-two-sorted-arrays.md) | Binary search on partition — variant 2 applied to a partition predicate | Hard | 90 min |

The challenge composes the lower-bound template (from Drills 1-2) with a non-obvious *partition predicate*. The boundary defense for this problem is the strictest of the week — read the prompt twice, draw the partition out by hand, and commit to a convention before writing code.

Why this matters: Median of Two Sorted Arrays is the LeetCode-Hard binary-search problem cited most often in real onsite interviews. If you can deliver UMPIRE on it cleanly in 90 minutes the first time and 45 minutes the second time, you have demonstrated a level of binary-search mastery few candidates reach in a 15-week prep cycle.

If you find yourself stuck past the 60-minute mark, **stop and re-read Lecture 1 §6 (lower bound) and Lecture 2 §3 (the three-step recipe)**. Then restart Plan with the partition predicate written out by hand. The algorithm cannot be derived without the picture; trying to write code before the picture is the source of every wrong attempt.

The challenge has a structural cousin in the homework — **Find Peak Element** (LC 162) — which is the same "binary search on a non-sorted array via a monotone-flip predicate" idea applied to a much easier shape. If Median feels overwhelming, do Find Peak first as a warm-up, then return.
