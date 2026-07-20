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
| **Coding** | 45 min | One unseen Medium, full UMPIRE, the standard allocation. |
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

### Number of Islands (LC 200)

A graph / grid-DFS Medium — a clean catalog representative for the final mock.

Given an `m x n` 2D grid of `'1'`s (land) and `'0'`s (water), return the number of islands. An island is a maximal group of land cells connected horizontally or vertically (not diagonally). Assume all four edges of the grid are surrounded by water.

```
Input:
  grid = [
    ["1","1","0","0","0"],
    ["1","1","0","0","0"],
    ["0","0","1","0","0"],
    ["0","0","0","1","1"]
  ]
Output: 3
Explanation: the top-left block is one island, the single middle cell is a
second, and the bottom-right pair is a third.
```

**Constraints:**

- `m == len(grid)`, `n == len(grid[0])`
- `1 <= m, n <= 300`
- `grid[i][j]` is `'0'` or `'1'`.

The intended approach is a grid traversal: scan every cell; when you hit an unvisited `'1'`, increment the island count and flood-fill (DFS or BFS) its whole connected component, marking visited so it is counted once. Time `O(m·n)` — each cell visited a constant number of times. Space `O(m·n)` worst case for the recursion stack / queue. The reference UMPIRE solve is below — **do not read it before the mock if you are using this as your problem.**

<details>
<summary>Reference solution (read only AFTER your mock)</summary>

> **30-second pattern-recognition memo (graph / grid DFS):**
> A grid where I count connected components of `'1'`s → flood fill. Scan every
> cell; each unvisited land cell starts a new island, and I DFS/BFS its whole
> component, marking cells visited so each island is counted once. Time O(m·n),
> space O(m·n). Why not union-find: it also works (O(m·n·α)), but DFS flood-fill
> is the simpler, more direct expression of "count the components."

```python
from typing import List


def num_islands(grid: List[List[str]]) -> int:
    """Count connected components of land in a grid. O(m*n) time, O(m*n) space."""
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])

    def sink(r: int, c: int) -> None:
        # Flood-fill the connected land component starting at (r, c).
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"          # mark visited by sinking the land to water
        sink(r + 1, c)
        sink(r - 1, c)
        sink(r, c + 1)
        sink(r, c - 1)

    islands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                islands += 1       # a new, unvisited land cell starts an island
                sink(r, c)         # consume its whole component
    return islands


if __name__ == "__main__":
    g = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    assert num_islands(g) == 3
    assert num_islands([["1"]]) == 1
    assert num_islands([["0"]]) == 0
    assert num_islands([["1", "0", "1", "0", "1"]]) == 3
    print("all tests passed")
```

The recursive `sink` mutates the grid to mark visited (no separate visited set needed); for very large grids the recursion can hit Python's stack limit, so the interview-grade variant to name is the **iterative** version with an explicit stack, or a BFS with a `deque`. Union-find is the other valid approach — worth naming as the alternative.

</details>

For the **system-design round**, pick a prompt from Challenge 2 (pastebin / rate limiter / news feed at small scale) that you have *not* already written up. For the **behavioral round**, have a peer or the platform ask 2–3 questions, or — solo — draw 2–3 of the eight Week-13 categories at random and answer to camera.

---

## After the loop — the artifacts

Immediately (5 minutes per round, while fresh): free-write raw observations into `mocks/mock-04/immediate-notes.md`, separated by round. Do not grade.

Saturday (two passes, across all three rounds):

1. **Pass 1 — 1.5×, whole recording, timestamp doc.** 15–20 timestamps of *patterns* across the loop, tagged by round. Save as `mocks/mock-04/timestamps.md`.
2. **Pass 2 — 1.0×, flagged segments only.** For each, *what happened* + *what to do differently*.

Then the self-feedback write-up at `umpire-writeups/c2-week-15/mock-04-self-feedback.md`.

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
[Match memo under 30s? Narration? Recovery? Complexity unprompted?]

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
| Coding round | 20 | Match memo under 30s; narration; complexity unprompted; recovery audible if one occurred |
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

Challenge 1 is complete when, under `mocks/mock-04/` and `umpire-writeups/c2-week-15/`:

- The recording link is committed (the video is too big to commit; commit the link).
- The immediate notes, pass-1 timestamps, and self-feedback write-up are all present.
- The self-feedback grades all three rounds, includes the four-mock trajectory, and names the one weakness carried forward.

Then move to [Challenge 2 — System-Design Mock](./challenge-02-system-design-mock.md) (or fold it into this loop's design round).
