# Week 8 — Challenges

Two challenges. Do at least the first; the second is an optional stretch.

| # | Challenge | Pattern | Difficulty | Target solve time |
|---|-----------|---------|------------|------------------:|
| 1 | [Merge k Sorted Lists](./challenge-01-merge-k-sorted-lists.md) (LC 23) | k-way merge with a heap of size k | Hard | 60 min |
| 2 | [Task Scheduler](./challenge-02-task-scheduler.md) (LC 621) | Heap with cooldown queue | Medium / Hard | 60 min |

Challenge 1 is mandatory — it is the canonical k-way merge problem, the structural pair to the size-k top-k template from Exercise 1, and a fixture in the LeetCode "Top 100 Liked" list. Challenge 2 is optional but recommended; it is the canonical "heap + auxiliary structure" problem and the production-engineering framing of the heap pattern.

Each challenge document contains:

- The problem spec with examples and edge cases.
- A "Why this is the canonical X" framing paragraph.
- A Research constraints memo for the template you would write.
- Acceptance criteria — what counts as "done."
- Hints (collapsible) and a worked solution sketch (also collapsible — read after attempting).

The challenges differ from the exercises in two ways:

1. **No starter file.** You design the function signature and the data shape yourself, defending each choice in the write-up.
2. **Longer target solve time.** 60 minutes vs 20-30. The Research constraints step is harder; the Assess options step has multiple valid paths; the Make the solution step has more code.

If a challenge takes more than 90 minutes, stop and read the hints. If it still takes more than 120 minutes, read the solution sketch and re-attempt cold the next day. The point is the rep, not the suffer.
