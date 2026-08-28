# Challenge 1 — Mock #4, the Full Loop

> **Format:** A recorded simulated onsite loop under full real-interview conditions. **Time:** ~2 hours for the loop (45-min coding + 45-min design + 20-min behavioral, with short breaks), plus ~2 hours of two-pass review and write-up. **Difficulty:** This is a loop, not a problem — the difficulty is the *conditions* and the *stamina*, not any single algorithm.

This is the keystone of Week 15 and the close of the four-mock arc. Mock #1 (W4) was your first time on camera; Mock #2 (W9) raised it to a real unseen problem with a partner; Mock #3 (W14) raised it to near-real conditions. Mock #4 closes the gap entirely: **full real conditions, the full loop, no scaffolding.** The next mock after this one is a real interview.

The full protocol lives in [Lecture 2](../lecture-notes/02-mock-4-under-real-conditions-and-the-onsite-loop.md). This file is the deliverable framing: how to run the loop, what to record, how to review it, the fallback coding problem, and how to write the closing trajectory across all four mocks.

---

## The conditions (full real — non-negotiable)

- **A stranger interviewer, ideally.** Book a real interviewing.io (<https://interviewing.io/blog>) or Pramp (<https://www.pramp.com/>) session if you can. The "stranger judging me" pressure is the one variable a peer or solo mock cannot reproduce — and it is the one that decides whether your prep holds.
- **Dress as if real.** Wear what you would wear to the actual interview. Set up the rig — camera at eye level, quiet room, water — exactly as on the day.
- **No notes. None.** No template file, no cheat sheet, no LeetCode tab. If you cannot recall a template, narrate the gap and code what you remember.
- **A hard stop per round.** When a round's timer hits zero, you stop mid-line.
- **The full loop, required.** A coding round, a system-design round, and a behavioral round — back to back. This is the first mock where all three are required.

---

## The loop sequence

| Round | Length | What happens |
|-------|--------|--------------|
| **Coding** | 45 min | One unseen Medium, full FRAME, the standard allocation. |
| Break | 5 min | Stand up, reset — real loops have gaps. |
| **System design** | 45 min | A junior-level prompt (use Challenge 2's framework; pick a prompt you have not written up). |
| Break | 5 min | Reset again. |
| **Behavioral** | 20 min | 2–3 questions across the eight Week-13 categories, answered in STAR from your bank. |

If scheduling a stranger for all three rounds is impossible, the acceptable fallback is: the **coding round with a stranger** (Flavor B), and the **design + behavioral rounds solo** on the same day. The non-negotiable is that all three round types happen, recorded, in one sitting.

---

## How to pick the coding problem

**If running for real (recommended):** pick a *different* unseen Medium than the fallback below. Use a stranger (Pramp / interviewing.io) who selects it, or a peer who picks one you have not seen, or — last resort — a random unseen Medium from across the catalog's patterns (graph, DP, two-pointer, heap). Reading the fallback below disqualifies it for your real attempt.

**If you have no other option (solo, need a problem now):** use the fallback below, but only if it is genuinely unseen for you.

---

## Fallback coding problem (solo mode only, and only if genuinely unseen)

### The Overnight Leak Survey

> **Pattern:** Grid traversal, connected components (flood fill).
> **Difficulty:** Medium — a clean graph representative for the final mock.

A water utility surveys a rectangular district overnight. Every street block carries a pressure sensor, and the survey comes back as a rectangular grid of readings in kilopascals **relative to nominal** — so a reading can be negative.

A block is **wet** when its reading is *strictly below* a `threshold` you are given. Wet blocks that touch **horizontally or vertically** (never diagonally) form a single **leak zone**.

The crew can only dispatch to a leak they have fully bounded. A zone with a block on the **outer border of the surveyed grid** may continue into streets nobody measured, so it is *unbounded* and the crew ignores it — no matter how large it is. Every other zone is **interior** and dispatchable.

Return a pair: **how many interior zones there are**, and **how many blocks are in the largest interior zone**. If there are no interior zones at all, return `(0, 0)`.

One more rule, and it is graded: **the survey grid belongs to the caller. Do not modify it.** The utility replays the same grid against several thresholds.

```python
def survey_leak_zones(pressure: list[list[int]], threshold: int) -> tuple[int, int]:
    """Return (interior_zone_count, largest_interior_zone_size) for the survey.
    Interior means the zone touches no cell on the grid's outer border.
    Returns (0, 0) when no interior zone exists. Must not mutate `pressure`."""
```

**Constraints.**

- The grid is rectangular: every row has the same length. `0 <= rows <= 1200` and `0 <= cols <= 1200`, so up to 1,440,000 blocks. That bound is chosen to kill the obvious wrong shape — re-scanning the whole grid once per zone is `O((rows·cols)²)`, about 2×10¹² operations, and will not finish. One sweep that visits each block a constant number of times is the only thing that fits.
- The same bound rules out plain recursion. A single wet zone can snake through most of a 1200×1200 grid — hundreds of thousands of blocks deep — and Python's default recursion limit is 1000. Write the traversal **iteratively**, with an explicit stack or a `deque`, and say out loud in Research constraints that the bound is why.
- `-2000 <= pressure[r][c] <= 2000` and `threshold` is in the same range. Readings are relative to nominal, so **negative values are ordinary and `0` is a perfectly normal reading**. If your wetness test leans on truthiness or assumes positives, this bound is what catches you.
- `rows` may be `0`, and a row may be empty. An empty survey has no zones.

**Examples.** Wet blocks are shown below the threshold; everything else is dry.

- `threshold = 30`, and

  ```
  [[10, 10, 10, 50, 50, 50],
   [10, 50, 50, 10, 10, 50],
   [50, 50, 50, 10, 50, 50],
   [50, 10, 50, 50, 50, 50],
   [50, 50, 50, 50, 50, 50]]
  ```

  → `(2, 3)`. Three zones exist. The top-left one — `(0,0)`, `(0,1)`, `(0,2)`, `(1,0)` — has **four** blocks, the most of any zone, but it sits on row 0 and column 0, so it is unbounded and does not count at all. The interior zones are `(1,3)`, `(1,4)`, `(2,3)` (three blocks) and the lone `(3,1)` (one block). This example exists to punish the reflex answer: if you report `4` as the largest, you sized the zone the crew cannot dispatch to.

- `threshold = 10`, and

  ```
  [[90, 90, 90, 90, 90],
   [90,  1,  1, 90, 90],
   [90, 90,  1, 90, 90],
   [90, 90,  1,  1,  1],
   [90, 90, 90, 90, 90]]
  ```

  → `(0, 0)`. There is exactly one zone, six blocks, and it *starts* at the interior block `(1,1)` — but it snakes down and right to `(3,4)`, which is on the last column. Deciding "interior" from the block you started at is the single most common bug here. You have to walk the **whole** zone before you can classify it.

- `threshold = 10`, and `[[80, 80, 80, 80], [80, -5, 0, 80], [80, 80, 80, 80]]` → `(1, 2)`. The readings `-5` and `0` are both below the threshold and both wet. If `0` came out dry in your solution, your wetness test is truthiness, not comparison.

- `threshold = 10`, and `[[9, 9, 9], [9, 10, 9], [9, 9, 9]]` → `(0, 0)`. The centre reads exactly `10`, and the rule is *strictly* below, so the centre is dry. The eight blocks around it form one ring-shaped zone that lies entirely on the border. Strict versus non-strict is a one-character bug and a whole wrong answer.

- `threshold = 10`, and `[[5, 5], [5, 5]]` → `(0, 0)`. Every block is wet, and every block in a 2×2 grid is on the border. Any grid with fewer than three rows or three columns can never produce an interior zone — worth noticing in Research constraints rather than discovering in Examine (verify).

- `threshold = 5`, and `[[8, 8, 8, 8, 8, 8, 8], [8, 2, 8, 2, 8, 2, 8], [8, 8, 8, 8, 8, 8, 8]]` → `(3, 1)`. Three separate single-block zones, all interior. The count is 3 and the largest is 1 — a check that you are returning both numbers and not conflating them.

- `pressure = []` → `(0, 0)`. Empty survey.

**Practice elsewhere.** The underlying pattern also appears as [LeetCode 200 · Number of Islands](https://leetcode.com/problems/number-of-islands/), though the contract there differs from ours — theirs counts every component, permits mutating the grid, and returns a single integer.

The intended shape: sweep every block once; when you meet a wet block you have not visited, walk its entire zone with an iterative BFS or DFS, counting its blocks and noticing whether any of them sits on the border; classify the zone only after the walk finishes. Time `O(rows·cols)` — each block is enqueued at most once. Space `O(rows·cols)` for the visited grid and, in the worst case, the frontier. The reference solve is below — **do not read it before the mock if you are using this as your problem.**

<details>
<summary>Reference solution (read only AFTER your mock)</summary>

> **30-second pattern-recognition memo (grid connected components):**
> A rectangular grid, a per-cell predicate, and "group the touching ones" →
> flood fill. Sweep every cell; each unvisited wet cell seeds one zone, and I
> walk the whole zone before I classify it, because the border test is a
> property of the zone and not of the seed. A separate `visited` grid rather
> than overwriting readings, because the caller keeps the survey. Iterative,
> because 1200×1200 makes recursion depth a real risk. Time O(rows·cols),
> space O(rows·cols). Why not union-find: it also works, at O(rows·cols·α),
> but it costs a second pass to recover per-root sizes and border flags — the
> single BFS reads more directly.

```python
from collections import deque


def survey_leak_zones(pressure: list[list[int]], threshold: int) -> tuple[int, int]:
    """Count interior leak zones and size the largest. O(rows*cols) time and space.

    A zone is a 4-connected group of blocks reading strictly below `threshold`.
    A zone is interior when none of its blocks lies on the grid's outer border.
    `pressure` is never modified.
    """
    if not pressure or not pressure[0]:
        return (0, 0)

    rows, cols = len(pressure), len(pressure[0])
    visited = [[False] * cols for _ in range(rows)]
    interior_zones = 0
    largest = 0

    for seed_r in range(rows):
        for seed_c in range(cols):
            if visited[seed_r][seed_c] or pressure[seed_r][seed_c] >= threshold:
                continue

            # Walk the entire zone first; only then decide whether it counts.
            frontier = deque([(seed_r, seed_c)])
            visited[seed_r][seed_c] = True
            blocks = 0
            reaches_border = False

            while frontier:
                r, c = frontier.popleft()
                blocks += 1
                if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                    reaches_border = True
                for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                    if (
                        0 <= nr < rows
                        and 0 <= nc < cols
                        and not visited[nr][nc]
                        and pressure[nr][nc] < threshold
                    ):
                        visited[nr][nc] = True   # mark on enqueue, not on pop
                        frontier.append((nr, nc))

            if not reaches_border:
                interior_zones += 1
                largest = max(largest, blocks)

    return (interior_zones, largest)


if __name__ == "__main__":
    district = [
        [10, 10, 10, 50, 50, 50],
        [10, 50, 50, 10, 10, 50],
        [50, 50, 50, 10, 50, 50],
        [50, 10, 50, 50, 50, 50],
        [50, 50, 50, 50, 50, 50],
    ]
    snapshot = [row[:] for row in district]
    assert survey_leak_zones(district, 30) == (2, 3)
    assert district == snapshot, "the caller's survey must come back untouched"

    # The zone seeded at (1,1) leaks out to the last column: unbounded.
    assert survey_leak_zones(
        [
            [90, 90, 90, 90, 90],
            [90, 1, 1, 90, 90],
            [90, 90, 1, 90, 90],
            [90, 90, 1, 1, 1],
            [90, 90, 90, 90, 90],
        ],
        10,
    ) == (0, 0)

    # Negative and zero readings are ordinary and both wet.
    assert survey_leak_zones(
        [[80, 80, 80, 80], [80, -5, 0, 80], [80, 80, 80, 80]], 10
    ) == (1, 2)

    # Strictly below: a reading equal to the threshold is dry.
    assert survey_leak_zones([[9, 9, 9], [9, 10, 9], [9, 9, 9]], 10) == (0, 0)

    # No grid narrower than three blocks can hold an interior zone.
    assert survey_leak_zones([[5, 5], [5, 5]], 10) == (0, 0)

    # Three separate one-block zones: count 3, largest 1.
    assert survey_leak_zones(
        [[8, 8, 8, 8, 8, 8, 8], [8, 2, 8, 2, 8, 2, 8], [8, 8, 8, 8, 8, 8, 8]], 5
    ) == (3, 1)

    assert survey_leak_zones([], 0) == (0, 0)
    assert survey_leak_zones([[]], 0) == (0, 0)
    print("all tests passed")
```

Two details worth narrating in a real round. **Mark on enqueue, not on pop** — if you only mark when a block comes off the frontier, a block with two wet neighbours gets queued twice and its zone is over-counted. And **the border flag belongs to the zone, not to the seed** — accumulate it across the walk, then test it once at the end.

Union-find is the valid alternative to name: union adjacent wet blocks, then group by root to get sizes and OR the border flags per root. Same asymptotics, more bookkeeping. Say why you rejected it.

</details>

For the **system-design round**, pick a prompt from Challenge 2 (pastebin / rate limiter / news feed at small scale) that you have *not* already written up. For the **behavioral round**, have a peer or the platform ask 2–3 questions, or — solo — draw 2–3 of the eight Week-13 categories at random and answer to camera.

---

## After the loop — the artifacts

Immediately (5 minutes per round, while fresh): free-write raw observations into `mocks/mock-04/immediate-notes.md`, separated by round. Do not grade.

Saturday (two passes, across all three rounds):

1. **Pass 1 — 1.5×, whole recording, timestamp doc.** 15–20 timestamps of *patterns* across the loop, tagged by round. Save as `mocks/mock-04/timestamps.md`.
2. **Pass 2 — 1.0×, flagged segments only.** For each, *what happened* + *what to do differently*.

Then the self-feedback write-up at `frame-writeups/c2-week-15/mock-04-self-feedback.md`.

---

## The self-feedback structure

```markdown
# Mock #4 — Self-Feedback (Full Loop)

**Date:** YYYY-MM-DD
**Flavor:** A (peer) / B (platform/stranger) / C (solo)
**Rounds:** coding / system design / behavioral
**Outcome per round:** [solved / solved with bug / didn't finish | scoped / partial | strong / rambled]

## What I felt during the loop
[3–5 honest sentences. Note the stamina cost of back-to-back rounds.]

## Coding round — graded
[Research-constraints memo under 30s? Narration? Recovery? Complexity unprompted?]

## System-design round — graded
[Scoped requirements first? Capacity estimate? High-level design? Trade-offs named?]

## Behavioral round — graded
[STAR structure? Quantified result? First-person "I"? Self-aware?]

## Trajectory across Mock #1 → #2 → #3 → #4
[Pull the one behavior change named after each of #1, #2, #3. Did you make them?
For each: gone / improved / still present in #4? This is the closing
self-correction record — the most predictive artifact in the portfolio. Be
honest: a weakness still present after four mocks is named, not hidden.]

## The ONE weakness I carry into real interviews
[One sentence. This seeds the weakness self-diagnosis in the personalized
study plan (homework Part 1).]

## What I'm not going to change
[One or two things I noticed but am deliberately not over-correcting.]
```

---

## Rubric

Total possible: 100; passing: 70.

| Dimension | Points | What "full credit" looks like |
|-----------|-------:|-------------------------------|
| Full conditions held | 15 | Stranger if obtainable, dressed as if real, no notes, hard stop — verifiable from the recording |
| Full loop run | 15 | All three round types (coding + design + behavioral) recorded in one sitting |
| Coding round | 20 | Research-constraints memo under 30s; narration; complexity unprompted; recovery audible if one occurred |
| System-design round | 15 | Requirements scoped first; capacity estimate; a clear design; one trade-off named |
| Behavioral round | 10 | STAR; quantified result; first-person "I" |
| Two-pass review done | 10 | Pass-1 timestamps + pass-2 prescriptions both present, across all rounds |
| Four-mock trajectory | 15 | Honest comparison across all four; prior behavior changes assessed; the carry-forward weakness named |

A passing mock is one run under the real conditions and *watched honestly* — not one where every round went perfectly. An unfinished coding round plus an honest trajectory and a clear carry-forward weakness passes; three flawless rounds with a skipped trajectory section fails. The trajectory is the point.

---

## The Mock #1 → #4 reflection (the closing arc)

This is the last mock of the course, so the trajectory section is also a reflection on the whole arc. Three or four sentences answering:

- What is the one habit that genuinely improved across the four mocks? (Name the Mock where it was a weakness and the Mock where it became reflexive.)
- What is the one weakness that is *still* present, and what is the specific drill for it in your personalized plan?
- If you watched Mock #1 and Mock #4 back to back, what would a stranger notice most?

That reflection is the bridge from the course to the real search. It goes, near-verbatim, into the homework's final reflection and seeds the study plan's weakness diagnosis.

---

## Acceptance

Challenge 1 is complete when, under `mocks/mock-04/` and `frame-writeups/c2-week-15/`:

- The recording link is committed (the video is too big to commit; commit the link).
- The immediate notes, pass-1 timestamps, and self-feedback write-up are all present.
- The self-feedback grades all three rounds, includes the four-mock trajectory, and names the one weakness carried forward.

Then move to [Challenge 2 — System-Design Mock](./challenge-02-system-design-mock.md) (or fold it into this loop's design round).
