# Week 4 — Homework

Six problems. ~5 hours total. Each commits to your portfolio repo. The last problem this week is the **Phase-1 retrospective** — read it Monday so you know what you're collecting evidence for all week.

---

## Problem 1 — Find the Duplicate Number (LeetCode 287) (75 min)

The most beautiful application of Floyd's outside of linked-list cycle detection. The problem looks like an array question; the solution is a fast/slow-pointer cycle detection on a functional graph.

**Problem.** Given an array `nums` of length `n + 1` where each integer is in the range `[1, n]`, exactly one number appears two or more times. Return that duplicate number. You must use **O(1) extra space** and may not modify the array.

**The insight.** Define the function `f(i) = nums[i]`. Starting from index `n` (an arbitrary starting point), the sequence `n, f(n), f(f(n)), ...` is a walk on a functional graph. Because some integer appears twice, the walk *must* enter a cycle. The cycle entrance is the duplicate.

Apply Floyd's:

1. Phase 1: walk slow by 1 step (slow = nums[slow]) and fast by 2 steps. They meet inside the cycle.
2. Phase 2: restart a finder from the original start (`n` or 0, depending on indexing) and walk both at speed 1. They meet at the cycle entrance — which is the duplicate.

**Acceptance:**

- A file `umpire-writeups/c2-week-04/hw-01-find-duplicate.md` with the UMPIRE write-up.
- Match section names the **functional-graph cycle** insight and compares against the O(n)-space `seen = set()` alternative.
- Evaluate section justifies **O(n) time, O(1) space** and the spec's "may not modify the array" constraint.
- Recording ≥15 minutes.
- Tests passing on at least: `[1, 3, 4, 2, 2] → 2`, `[3, 1, 3, 4, 2] → 3`, `[1, 1] → 1`, `[1, 4, 4, 2, 4] → 4`.

This problem is the highest-yield interview problem in the fast/slow family. The "functional graph" framing transfers directly to the homework's bonus problems.

---

## Problem 2 — Remove Nth From End (Single Pass) (45 min)

**Problem.** Given the head of a singly-linked list and an integer `n`, remove the nth node from the end of the list and return the modified head. Use **one pass** and **O(1) space**.

The two-pass naive: count length first, then walk to `length - n`. Rejected by the spec (one pass).

The single-pass trick: advance `fast` by `n` steps first. Then walk `slow` (starting at a dummy node) and `fast` in lockstep until `fast.next` is None. Slow now points to the node *before* the one to remove. Splice it out.

**Acceptance:**

- A file `umpire-writeups/c2-week-04/hw-02-remove-nth-from-end.md` with the UMPIRE write-up.
- Match section names this as a **fixed-gap fast/slow variant** (different mechanic from Floyd's but same family).
- Working code with tests for at least: `[1,2,3,4,5], n=2 → [1,2,3,5]`, `[1], n=1 → []`, `[1,2], n=1 → [1]`, `[1,2], n=2 → [2]`.
- Use of a **dummy head node** to handle the "remove the first node" case cleanly. Skipping the dummy is the #1 source of bugs on this problem.

---

## Problem 3 — Palindrome Linked List (LeetCode 234) (45 min)

**Problem.** Given the head of a singly-linked list, return `True` if it's a palindrome.

The clean solution is *almost identical* to the Reorder List challenge from this week:

1. Find the middle (Drill 3).
2. Reverse the second half (in place).
3. Walk left half and reversed right half in lockstep, comparing values. Any mismatch → False.

The structural reuse with Reorder List is the point of this homework problem. **Your Match section must call out the parallel to Reorder List explicitly.**

**Acceptance:**

- A file `umpire-writeups/c2-week-04/hw-03-palindrome-list.md`.
- Match section compares with the Reorder List challenge — same first two sub-steps, third sub-step differs (compare vs merge).
- Implementation is **in place**, O(1) extra space.
- Tests for at least: `[1,2,2,1] → True`, `[1,2] → False`, `[1] → True`, `[1,0,0,1] → True`, `[1,2,3,2,1] → True`.
- Bonus credit: in Review, describe how to **restore the list** after the in-place modification (so the function is non-destructive). Interviewers ask for this as a follow-up.

---

## Problem 4 — Behavioral story #4 (45 min)

The story bank continues. Week 4's topic is interview-adjacent — perfect setup for the behavioral content of Week 13.

**Acceptance:**

- A file `behavioral/story-04.md` in your portfolio repo.
- Topic: **"Tell me about a time you got difficult feedback and acted on it."** This is the canonical "growth" behavioral question; it shows up in every loop.
- Format: STAR (Situation, Task, Action, Result).
- 200–400 words.
- Read it aloud at least twice. The story should naturally invoke the *meta-skill* you've practiced this week — watching yourself on a recording, extracting one behavior change. That cross-mapping ("I do this to my own performance, weekly") is the engineering-mindset signal behavioral interviewers want to hear.

---

## Problem 5 — System-design ground zero #4 (45 min)

Fourth 300-word warm-up.

**Acceptance:**

- A file `system-design/notes-week-04.md` containing a 300-word answer to: **"How would you design a system that detects, in real time, when a user's session has gone idle (no activity in 30 minutes)?"**
- Do not look up the canonical answer first. Write what you'd say in an interview today.
- After writing, search "session timeout sliding window" and "TTL cache for sessions" and read one free article on each. Note three things you'd add — *especially* if it mentions Redis TTL, sliding window timers, or eventual-consistency issues with distributed session stores.

The connection to this week: "detecting that something hasn't happened" is a *passive* version of cycle detection — you're waiting for a chain of activity to stop. Same family of mental model.

---

## Problem 6 — Phase-1 retrospective (60 min)

This is the closing artifact for Phase 1. A short retrospective at `study-plan/phase-1-retrospective.md`, 500–700 words.

**Answer these, honestly:**

1. **Which of the four Phase-1 patterns is most automatic in your hands?** (Two-pointer / hash map / sliding window / fast-slow.) Be specific: name one problem from that pattern you can solve cold in <15 minutes.

2. **Which is least automatic?** Be specific: name one problem from that pattern where you still hesitate at Match.

3. **Look at your four weeks of recordings, all of them.** What is the *one* behavior that has visibly improved since Week 1? What is the *one* that has not?

4. **Mock #1 happened this week.** What did the recording show that you didn't expect? What did it confirm that you already suspected?

5. **The Match section is the under-practiced UMPIRE step in Weeks 1–2 and the over-practiced one in Week 3.** Where is Match in your hands now — fluent, mechanical, or rote? (Mechanical = the *right amount of automatic*. Rote = automatic without thinking, which can produce wrong matches under pressure. Fluent = automatic but flexible.)

6. **What's your specific behavior change for Mock #2 in Week 9?** Should be one sentence, testable. (See Lecture 2 §9.)

7. **Phase 2 starts next week with binary search.** Binary search is the pattern most candidates think they know but actually don't — the "binary search on answer" idiom is what Week 5 will teach. What's your honest current state with binary search? (Honest options: "comfortable on sorted arrays, never tried parametric"; "I always get the loop bounds wrong"; "I haven't written one since college.")

The retrospective is the artifact a future-you will read before Mock #3 (Week 14) and Mock #4 (Week 15). Past-you's honest assessment will be more useful than re-running the drills. Write it accordingly.

---

## Time budget

| Problem | Time |
|--------:|----:|
| 1 — Find the Duplicate Number | 75 min |
| 2 — Remove Nth From End (single pass) | 45 min |
| 3 — Palindrome Linked List | 45 min |
| 4 — Behavioral story #4 | 45 min |
| 5 — System-design warm-up #4 | 45 min |
| 6 — Phase-1 retrospective | 60 min |
| **Total** | **5h 15min** |

---

By the end of Week 4 your portfolio repo's commit history should show ~50-65 commits total (the cumulative count through Week 3 + ~10-15 commits this week, including the mock-interview recording link, the self-feedback note, and the retrospective). The cadence is the artifact; keep the streak.

The mock recording itself is large — don't commit the raw video to git. Commit a `recording-link.md` that points to the video's hosted URL (YouTube unlisted, Google Drive, Loom). The link plus the self-feedback write-up is what reviewers will look at.

Up next: [Week 5 — Binary Search Beyond Sorted Arrays](../week-05/).
