# Challenge 1 — Mock #3, the Timed Round

> **Format:** A recorded full-loop mock under near-real conditions. **Time:** 45-minute hard clock for the round, plus ~90 minutes of two-pass review and write-up. **Difficulty:** This is a mock, not a problem — the difficulty is the *conditions*, not the algorithm.

This is the keystone of Week 14. Mock #1 (Week 4) was your first time on camera; Mock #2 (Week 9) raised the bar to a real unseen problem. Mock #3 raises it to **near-real conditions**: video on, a hard 45-minute clock, and *no peeking at anything*. It is the closest you have come to the real screen.

The full protocol lives in [Lecture 3](../lecture-notes/03-the-mock-interview-protocol-mock-3-and-tries-review.md). This file is the deliverable framing: how to run it, what to record, how to review it, and how to write the trajectory comparison across all three mocks.

---

## The conditions (non-negotiable)

- **Video on.** Screen + face + audio, all three tracks. The face track is required by Mock #3, not optional.
- **Hard 45-minute clock.** When the timer hits zero, you stop mid-line. No extensions, no "let me just finish this function."
- **No peeking.** No LeetCode tab. No notes. No re-reading the lectures. No glancing at the trie template. If you cannot recall the binary-trie shape from memory, narrate the gap and code what you remember — the gap is *data*.
- **An unseen problem.** Pick a Medium you have not solved. The pattern should be in the bit / trie family or a mix, but it does not have to be — Mock #3 tests recognition across the whole catalog under pressure.

---

## How to pick the problem

**If running for real (recommended):** pick a *different* unseen Medium than the fallback below. Use a peer (Flavor A) who selects a problem you have not seen, or a platform (Flavor B, interviewing.io / Pramp) that selects for you, or — last resort — a random Medium from the LeetCode Bit Manipulation tag (<https://leetcode.com/tag/bit-manipulation/>) or Trie tag (<https://leetcode.com/tag/trie/>) that you have not opened. The point of a mock is the *unseen* problem; reading the fallback below disqualifies it for your real attempt.

**If you have no other option (solo, no platform, need a problem now):** use the fallback below — but only if you have not already studied it this week. Note that Maximum XOR is Exercise 3, so if you have done the exercise, this fallback is *not* unseen for you and you must pick something else.

---

## Fallback problem (solo mode only, and only if genuinely unseen)

### Maximum XOR of Two Numbers in an Array (LC 421)

Given an integer array `nums`, return the maximum value of `nums[i] ^ nums[j]` where `0 <= i <= j < len(nums)`.

```
Input:  nums = [3, 10, 5, 25, 2, 8]
Output: 28
Explanation: the maximum is 5 ^ 25 == 28.
```

**Constraints:**

- `1 <= len(nums) <= 2 * 10**5`
- `0 <= nums[i] <= 2**31 - 1`

The intended solution is the binary trie (`O(n · 32)`) over the `O(n**2)` brute force. The full FRAME walkthrough is in [SOLUTIONS.md, Solution 3](../exercises/SOLUTIONS.md) — do **not** read it before the mock if you are using this as your problem. If you have already done Exercise 3, this is not unseen; pick a different Medium (e.g., LC 137 Single Number II, LC 260 Single Number III, LC 201 Bitwise AND of Numbers Range, or any unseen Medium from the trie tag).

---

## During the round — the 45-minute allocation

| Phase | Wall-clock | What's happening |
|------:|:----------:|------------------|
| 0:00 – 0:03 | 3 min | **F.** Read aloud. Restate. One or two clarifying questions. Walk an example. |
| 0:03 – 0:05 | 2 min | **R.** Name the limits and the pattern. The 30-second memo. |
| 0:05 – 0:10 | 5 min | **A.** Sketch the approach, data structures, complexity target. |
| 0:10 – 0:25 | 15 min | **M.** Write the code. Narrate each line. Narrate the pauses. |
| 0:25 – 0:35 | 10 min | **E · verify.** Trace at least two examples. Find at least one bug. |
| 0:35 – 0:43 | 8 min | **E · cost.** Time and space. Trade-offs. One variant. |
| 0:43 – 0:45 | 2 min | Wrap-up. Summarize. Thank the interviewer. |

Guidelines, not rules — but the structure is the discipline. Bank saved Research constraints time in Examine (verify).

---

## After the round — the artifacts

Immediately (5 minutes, while fresh): free-write raw observations into `mocks/mock-03/immediate-notes.md`. Do not grade.

Saturday (two passes):

1. **Pass 1 — 1.5×, whole recording, timestamp doc.** 10–15 timestamps of *patterns*, not every filler word. Save as `mocks/mock-03/timestamps.md`.
2. **Pass 2 — 1.0×, flagged segments only.** For each, write *what happened* + *what to do differently*.

Then the self-feedback write-up at `frame-writeups/c2-week-14/mock-03-self-feedback.md`.

---

## The self-feedback structure

```markdown
# Mock #3 — Self-Feedback

**Date:** YYYY-MM-DD
**Problem:** [name + LeetCode link]
**Flavor:** A (peer) / B (platform) / C (solo)
**Duration:** 45 minutes
**Outcome:** [solved / solved with bug / didn't finish]

## What I felt during the mock
[3–5 honest sentences.]

## What the recording shows
[5–8 observations, each with a wall-clock timestamp from pass 2.]

## The Research-constraints memo — graded
[Under 30 seconds? Named the sub-shape, the bound, one rejected alternative?]

## The thinking-aloud — graded
[Did I go silent? When? Did I narrate pauses?]

## The recovery moves — graded
[When the first approach hit a wall, did I narrate the recovery audibly?]

## The Examine (cost) section — graded
[Did I state time + space + a trade-off + one variant, unprompted?]

## Trajectory across Mock #1 → #2 → #3
[The new section. Pull the one behavior change you named after Mock #1 and
after Mock #2. Did you actually make them? Is the Mock #1 weakness gone,
improving, or still present? 3–4 sentences. This is the self-correction
record a senior engineer reads.]

## ONE behavior change for Mock #4
[One sentence. Specific. Testable.]

## What I'm not going to change
[One or two things you noticed but are deliberately not over-correcting.]
```

---

## Rubric

Total possible: 100; passing: 70.

| Dimension | Points | What "full credit" looks like |
|-----------|-------:|-------------------------------|
| Conditions held | 15 | Video on, hard 45-min clock honored, no peeking — verifiable from the recording |
| Research-constraints memo delivered | 20 | Under 30 seconds; sub-shape named; complexity stated; one alternative rejected |
| Thinking-aloud | 15 | No silent stretch over 20 seconds; pauses narrated |
| Recovery audible | 10 | At least one course-correction narrated out loud (if one occurred) |
| Examine (cost) unprompted | 15 | Time + space + trade-off + one variant, stated without being asked |
| Two-pass review done | 10 | Pass 1 timestamps + pass 2 prescriptions both present |
| Trajectory section | 15 | Honest comparison across all three mocks; prior behavior changes assessed |

A passing mock is one you ran under the real conditions and *watched honestly* — not one where you solved the problem. A solved problem with a skipped Examine (cost) and no trajectory section fails; an unfinished problem with a clean Research-constraints memo, an audible recovery, and an honest trajectory passes.

---

## The one-behavior-change rule (still binding)

Pick exactly **one** change for Mock #4. Specific. Testable. "I will state the complexity bound out loud before the interviewer asks" is good. "I will be more confident" is not. Over three mocks, three deliberate changes compound; ten attempted at once compound to zero.

---

## Acceptance

Challenge 1 is complete when, under `mocks/mock-03/` and `frame-writeups/c2-week-14/`:

- The recording link is committed (the video file is too big to commit; commit the link).
- The immediate notes, pass-1 timestamps, and self-feedback write-up are all present.
- The self-feedback includes the trajectory section and names one behavior change for Mock #4.

Then move to [Challenge 2 — Sum of Two Integers](./challenge-02-sum-of-two-integers.md).
