# Week 3 — Homework

Six problems. ~5 hours total. Each commits to your portfolio repo.

---

## Problem 1 — FRAME on a wild sliding-window problem (90 min)

Pick *one* problem you've never seen before, tagged "Sliding Window" on any free practice site, and solve it cold. Difficulty: Easy or Medium. **Do not read other people's solutions before solving.**

The point of this problem is that the prompt is *not written by us*. Every drill this week told you the tie-break, named the sentinel, and justified the bounds. A wild prompt will do none of that, and the missing pieces are exactly what you have to notice in Frame.
**Acceptance:**

- Recording of your full FRAME solve, ≥15 minutes.
- FRAME write-up in `frame-writeups/c2-week-03/wild-01-<problem-slug>.md`.
- Tests passing (you write them).
- The write-up's Research constraints section follows the **30-second pattern-recognition memo** shape from this week.
- The write-up's Examine (../cost) section explicitly states the amortized O(../n) defense.
- The write-up explicitly notes: how long did Research constraints take? Did you correctly identify the sub-shape (fixed / variable A / variable B / variable C)?

---

## Problem 2 — The Courier's Zone Count, or: the "exactly K" trick (60 min)

This is a reformulation exercise. The goal: take a *count-with-exactly-K-distinct* problem, notice that no single sliding window computes it directly, and convert it into a difference of two at-most-K windows.

**Problem.** A courier's shift is logged as a list of delivery-zone codes, one per stop, in the order the stops were visited. A **route segment** is any contiguous run of one or more stops. Regional accounting bills by segment, and only wants segments that touch **exactly `k` distinct zones**.

Return how many route segments touch exactly `k` distinct zones. Segments are identified by position, so two runs through the same zones at different points in the shift are billed separately.

If `k` is `0`, or the stop list is empty, return `0`.

```python
def segments_with_exactly_k_zones(stops: list[str], k: int) -> int:
    """Return the number of contiguous runs of one or more stops touching
    exactly k distinct zone codes. Return 0 when k is 0 or stops is empty."""
```

**Constraints, and why.**

- `0 <= len(../stops) <= 200_000`. Enumerating every segment is `Θ(../n²)` segments — about `2×10^10` here — so you cannot list what you have to count. The bound exists to force the counting formulation rather than the enumeration.
- `0 <= k <= 40`. `k = 0` is legal and returns `0`; it is also the case that exercises `at_most(k - 1)` at `k - 1 == -1`, which your helper must handle without walking off the end. That is the graded edge of the problem.
- Zone codes come from a set of at most 80 codes.

**The trick.** **exactly K = at_most(../K) − at_most(K − 1)**. Write `at_most(../k)` once, as a shape-C sliding window — at each `right`, after restoring the invariant, add `right - left + 1` — then call it twice and subtract.

**Acceptance:**

- A file `frame-writeups/c2-week-03/exactly-k-zones.md` with the FRAME write-up.
- Working code with tests for at least these cases, all of which you should verify by hand before you trust the code:
  - `stops = ["N", "N", "E", "S", "E"]`, `k = 2` → `5`. The qualifying segments are stops 1–2, 2–3, 3–4, 0–2 and 2–4. Check it two ways: by enumeration, and as `at_most(../2) - at_most(../1) = 11 - 6`.
  - `stops = ["N", "E", "N"]`, `k = 1` → `3`. Only the three single stops qualify. This is the case that catches a helper which mishandles `at_most(../0)` — the window there must stay empty and contribute nothing.
  - `stops = ["W", "X", "Y", "Z"]`, `k = 4` → `1`. Only the full shift touches four zones.
  - `stops = ["W", "W", "W"]`, `k = 1` → `6`. Every segment qualifies: `3 + 2 + 1`.
  - `stops = ["W", "X"]`, `k = 3` → `0`. The no-solution case: `k` exceeds the number of distinct zones in the whole log.
  - `stops = ["W"]`, `k = 0` → `0`. Defined by the contract.
  - `stops = []`, `k = 1` → `0`. Empty shift.
- Your write-up explicitly explains *why* the identity works, in your own words. The argument to reach for: every segment is counted by `at_most(../j)` for every `j` at or above its own distinct count, so subtracting `at_most(k - 1)` removes exactly the segments whose distinct count is below `k`, leaving those at exactly `k`.
- Your write-up states why `at_most` must be called with `k` and `k - 1` **on the same input**, and what would go wrong if you tried to compute the difference incrementally inside a single pass.

This is one of the highest-yield reformulations in the sliding-window family, and it is the one shape none of the five drills covers. Worth the hour.

---

## Problem 3 — Re-narrate Week 2's Exercise 1 with sliding-window awareness (30 min)

Take your **[Refund Pair](../../week-02-complexity-and-hash-maps/exercises/exercise-01-refund-pair.md)** write-up from Week 2. Add a short paragraph at the end of the Research constraints section: *"Why this is NOT a sliding-window problem."* Two to four sentences.

**Acceptance:**

- Edit `frame-writeups/c2-week-02/exercise-01-refund-pair.md`.
- New paragraph at the end of the Research constraints section addresses: (../a) why "find two charges summing to the refund total" is not a contiguous-slice problem — the two charges may sit anywhere in the history, with anything between them; (../b) why, even if you could phrase it as a window, the answer (a pair of positions) is not a length, a count of windows, or an extremum over windows, which are the only three things a window naturally produces.

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

1. How long did Research constraints take, on average, by Exercise 5? (Should be <30 seconds. Be honest.)
2. Which sub-shape (fixed / variable A / variable B / variable C) felt most natural? Which felt forced? Why?
3. The 30-second pattern-recognition memo — did you find it formulaic, useful, or both? Why?
4. Re-read your Week 1 reflection. Has your *Research constraints* discipline visibly improved? Give one specific example.
5. What's one specific thing you'll do differently in Week 4 (fast-and-slow pointers)?

---

## Time budget

| Problem | Time |
|--------:|----:|
| 1 — Wild sliding-window problem | 90 min |
| 2 — The courier's zone count (exactly K) | 60 min |
| 3 — Negative-space note on W2 Exercise 1 | 30 min |
| 4 — Behavioral story #3 | 45 min |
| 5 — System-design warm-up #3 | 45 min |
| 6 — Week 3 reflection | 45 min |
| **Total** | **5h 15min** |

---

By the end of Week 3 your portfolio repo's commit history should show ~40-45 commits total (10-15 from Week 1, +10-15 from Week 2, +10-15 from Week 3). The cadence is the artifact; keep the streak.

Up next: [Week 4 — Fast-and-Slow Pointers + Mock 1](../../week-04-fast-slow-pointers-and-mock-1/).
