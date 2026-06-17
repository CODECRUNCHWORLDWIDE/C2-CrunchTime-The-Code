# Week 3 — Homework

Six problems. ~5 hours total. Each commits to your portfolio repo.

---

## Problem 1 — UMPIRE on a wild sliding-window problem (90 min)

Pick *one* problem you've never seen before, tagged "Sliding Window" on any free practice site (LeetCode, HackerRank, Exercism). Difficulty: Easy or Medium. **Do not read other people's solutions before solving.**

Suggested candidates if you need a starter list (all free on LeetCode):

- **Maximum Average Subarray I** (Easy, LC 643) — direct fixed-size warm-up; faster than Drill 1 once you've internalized the pattern.
- **Longest Repeating Character Replacement** (Medium, LC 424) — shape A with a clever "max-freq character" twist.
- **Subarray Product Less Than K** (Medium, LC 713) — shape C (count of subarrays) with positive integers.
- **Find All Anagrams in a String** (Medium, LC 438) — direct sister to Drill 3, returns indices instead of a boolean.
- **Longest Substring with At Most Two Distinct Characters** (Medium, LC 159) — direct sister to Drill 5; same template, different framing.
- **Max Consecutive Ones III** (Medium, LC 1004) — shape A: at most K zeros allowed in the window.
- **Number of Substrings Containing All Three Characters** (Medium, LC 1358) — shape A-into-count.

**Acceptance:**

- Recording of your full UMPIRE solve, ≥15 minutes.
- UMPIRE write-up in `umpire-writeups/c2-week-03/wild-01-<problem-slug>.md`.
- Tests passing (you write them).
- The write-up's Match section follows the **30-second pattern-recognition memo** shape from this week.
- The write-up's Evaluate section explicitly states the amortized O(n) defense.
- The write-up explicitly notes: how long did Match take? Did you correctly identify the sub-shape (fixed / variable A / variable B / variable C)?

---

## Problem 2 — The "exactly K" trick (60 min)

This is a reformulation exercise. The goal: take a *count-of-subarrays-with-exactly-K-distinct* problem and convert it to a difference of two at-most-K sliding windows.

**Problem.** Implement `subarrays_with_k_distinct(nums: list[int], k: int) -> int`, returning the number of contiguous subarrays of `nums` with **exactly** `k` distinct integers.

The trick: **exactly K = atMost(K) − atMost(K − 1)**. Implement `atMost(k)` once as a shape-C sliding window, then call it twice.

**Acceptance:**

- A file `umpire-writeups/c2-week-03/exactly-k.md` with the UMPIRE write-up.
- Working code with tests for at least these cases:
  - `nums = [1, 2, 1, 2, 3]`, `k = 2` → `7`
  - `nums = [1, 2, 1, 3, 4]`, `k = 3` → `3`
  - `nums = [1]`, `k = 1` → `1`
  - `nums = []`, `k = 1` → `0`
- Your write-up explicitly explains *why* the `exactly = atMost(K) − atMost(K - 1)` identity works. (Hint: every subarray contributes to `atMost(k)` for all `k >= its-distinct-count`; subtracting removes the over-counts.)

This is one of the highest-yield interview tricks of the sliding-window family. Worth the hour.

---

## Problem 3 — Re-narrate Week 2's Drill 1 with sliding-window awareness (30 min)

Take your **Two Sum (Unsorted)** write-up from Week 2. Add a short paragraph at the end of the Match section: *"Why this is NOT a sliding-window problem."* Two to four sentences.

**Acceptance:**

- Edit `umpire-writeups/c2-week-02/drill-01-two-sum-unsorted.md`.
- New paragraph at the end of Match section addresses: (a) why "find a pair summing to target" is not a contiguous-slice problem; (b) why even if we *could* phrase it as a window, the answer (indices, plural) is not a length or count of windows.

The point of this exercise is to make the *negative space* of pattern recognition visible in your portfolio. Pattern matching is what you do; pattern rejection is what you *don't* do.

---

## Problem 4 — Behavioral story #3 (45 min)

The story bank continues.

**Acceptance:**

- A file `behavioral/story-03.md` in your portfolio repo.
- Topic: **"Tell me about a time you noticed a pattern across multiple problems and applied it."**
- Format: STAR (Situation, Task, Action, Result).
- 200–400 words.
- Read it aloud at least twice. The story should naturally invoke the kind of pattern-recognition thinking you've drilled this week: "I'd seen something similar before — same shape with different inputs — and I used the same algorithm." That cross-mapping *is* the engineering skill behavioral interviewers are probing for.

---

## Problem 5 — System-design ground zero #3 (45 min)

Third 300-word warm-up.

**Acceptance:**

- A file `system-design/notes-week-03.md` containing a 300-word answer to: **"How would you design a system that detects, in real time, when a service's error rate exceeds 1% over the most recent 60 seconds?"**
- Do not look up the canonical answer first. Write what you'd say in an interview today.
- After writing, search "sliding window rate limiter" or "time-bucketed counter" and read one free article. Note three things you'd add — *especially* if it mentions ring buffers, time-bucketed counters, or the difference between fixed and sliding windows in time-series.

The connection to this week: the same word ("sliding window") appears in algorithms *and* in distributed-systems design, and they are not the same thing. Recognizing that the algorithmic pattern (your week's drill) generalizes to a system-design concept (time-windowed counters over a stream of events) is the engineering bridge we're building.

---

## Problem 6 — Week 3 reflection (45 min)

A short reflection. 300–400 words at `study-plan/week-03-reflection.md`.

**Answer:**

1. How long did Match take, on average, by Drill 5? (Should be <30 seconds. Be honest.)
2. Which sub-shape (fixed / variable A / variable B / variable C) felt most natural? Which felt forced? Why?
3. The 30-second pattern-recognition memo — did you find it formulaic, useful, or both? Why?
4. Re-read your Week 1 reflection. Has your *Match* discipline visibly improved? Give one specific example.
5. What's one specific thing you'll do differently in Week 4 (fast-and-slow pointers)?

---

## Time budget

| Problem | Time |
|--------:|----:|
| 1 — Wild sliding-window problem | 90 min |
| 2 — Exactly K trick | 60 min |
| 3 — Negative-space note on W2 Drill 1 | 30 min |
| 4 — Behavioral story #3 | 45 min |
| 5 — System-design warm-up #3 | 45 min |
| 6 — Week 3 reflection | 45 min |
| **Total** | **5h 15min** |

---

By the end of Week 3 your portfolio repo's commit history should show ~40-45 commits total (10-15 from Week 1, +10-15 from Week 2, +10-15 from Week 3). The cadence is the artifact; keep the streak.

Up next: [Week 4 — Fast-and-Slow Pointers + First Mock](../week-04-fast-and-slow-pointers/) (coming soon).
