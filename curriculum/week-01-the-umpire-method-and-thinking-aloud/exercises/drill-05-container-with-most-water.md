# Drill 5 — Container With Most Water

> **Pattern:** Two-pointer, converging (with a tracked maximum)
> **Difficulty:** Medium
> **Target solve time:** 25 minutes

The first **medium** of the week. This one is famous because the greedy two-pointer move is *non-obvious* — the proof that it works is worth doing out loud in Evaluate.

## Problem statement

You're given an integer array `heights` where `heights[i]` is the height of a vertical line at position `i`. Find two lines that, together with the x-axis, form a container that holds the most water. Return the maximum amount of water the container can store.

You may **not** tilt the container. The container's water level is the **shorter** of the two chosen lines, and the width is the distance between them.

**Examples:**

- `heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]` → `49` (between indices 1 and 8: width 7, min height 7)
- `heights = [1, 1]` → `1`
- `heights = [4, 3, 2, 1, 4]` → `16` (between indices 0 and 4: width 4, min height 4)

## UMPIRE checklist

- [ ] **U:** Restate. Confirm "shorter line determines height." Confirm we return the **area**, not the indices. Confirm minimum length 2.
- [ ] **M:** Two-pointer converging with a tracked maximum. Move the pointer at the **shorter** line; that's the greedy choice.
- [ ] **P:** Start `l=0, r=n-1, best=0`. Loop while `l<r`. Compute area = `min(h[l], h[r]) * (r-l)`. Update `best`. Move whichever pointer points at the shorter height (if equal, move either). Return `best`.
- [ ] **I:** Watch the area formula. Pay attention to tie-breaking when `h[l] == h[r]`.
- [ ] **R:** Trace on `[1, 8, 6, 2, 5, 4, 8, 3, 7]`. Show the area at each step. Verify max=49.
- [ ] **E:** **O(n)** time, **O(1)** space.
- [ ] **E (extra):** **Prove (or sketch) why moving the shorter pointer is correct.** This is the interview tell — most candidates can write the code but can't explain why moving the shorter side never misses a better answer.

## The proof you must articulate

> "Suppose `h[l] < h[r]`. The current area is `h[l] * (r - l)`. If I keep `l` and move `r` inward, the width strictly decreases, and the height is bounded above by `h[l]` (the new shorter side might be even smaller, but never larger than `h[l]`). So no future area with this same `l` can beat the current one. Therefore moving `l` forward is the only way to possibly find a larger area. Same logic if `h[r] < h[l]`."

Saying that out loud in an interview is the difference between "solved it" and "demonstrated mastery."

## Acceptance criteria

- Code passes `timed_runner.py` for `max_area`.
- Write-up committed, **with** the correctness sketch in the Evaluate section.
- Recording ≥15 minutes.

## Function signature

```python
def max_area(heights: list[int]) -> int:
    ...
```

## Common bugs

- **Area formula error:** `min(h[l], h[r]) * (r - l)` — not `*r` not `*(r - l + 1)`.
- **Moving the taller side:** Plausible-looking but wrong. The proof above explains why.
- **Forgetting to track max:** Just returning the last area is wrong.

## Stretch

LeetCode 42 — **Trapping Rain Water.** Same array shape, very different algorithm. Don't attempt yet; it's [Challenge 2](../challenges/challenge-02-trapping-rain-water.md). But notice both problems concern arrays of heights and water — same building blocks, different patterns.

After all five drills, take the [quiz](../quiz.md), then start [homework](../homework.md) and the [mini-project](../mini-project/README.md).
