# Challenge 2 — Trapping Rain Water

> **Pattern:** Two-pointer + invariant on the running max
> **Difficulty:** Hard
> **Target solve time:** 120 minutes
> **Why hard:** the loop invariant is *non-obvious*. Most people solve it once with DP, then years later learn the O(1)-space two-pointer version. We do the latter.

## Problem statement

Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

**Examples:**

- `heights = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]` → `6`
- `heights = [4, 2, 0, 3, 2, 5]` → `9`
- `heights = []` → `0`
- `heights = [3]` → `0`
- `heights = [3, 3, 3]` → `0`

## The naïve solutions (don't submit these)

**O(n²):** For each index `i`, compute `max(heights[:i])` and `max(heights[i:])`; water at `i` is `min(left_max, right_max) - heights[i]`. Sum. Easy to write, wasteful.

**O(n) time / O(n) space:** Pre-compute two arrays `left_max[i]` and `right_max[i]`. Then a single pass adds `min(left_max[i], right_max[i]) - heights[i]` at each position. This is what most candidates produce first and it's a fine answer if you can defend it.

**O(n) time / O(1) space:** The two-pointer version. **This is what we want.**

## The two-pointer key insight

Maintain `left_max` and `right_max` (single integers, not arrays). Move pointers inward. At each step:

- If `heights[left] < heights[right]`: the water level at `left` is bounded above by `left_max` (because somewhere on the right there is at least `heights[right] > heights[left]`, so the right is not the bottleneck). Add `left_max - heights[left]` to the answer. Then update `left_max` and advance `left`.
- If `heights[right] <= heights[left]`: symmetric. Update `right_max` and decrement `right`.

The invariant: **at each step we know the bottleneck for whichever side we process.** That's why we only need single integers, not arrays.

## UMPIRE outline

- **U:** Restate. Confirm the picture: bars of heights, water trapped between them. Walk the canonical example by hand on a whiteboard.
- **M:** Two-pointer with running maxes on each side.
- **P:** Initialize `l=0, r=n-1, left_max=0, right_max=0, water=0`. Loop while `l<r`. Take the smaller side, update its max, compute water there, advance.
- **I:** Implement. Pay attention to the `if/else` ordering — this is where bugs hide.
- **R:** Trace `[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]`. Verify water=6 at the end. Show each iteration's `l, r, left_max, right_max, water`.
- **E:** **O(n)** / **O(1)**. Compare against the O(n)/O(n) DP version. Discuss when each is preferable.

## Acceptance criteria

- [ ] Code passes all the provided test cases.
- [ ] Solution is **O(n) time, O(1) auxiliary space** (excluding input).
- [ ] Your write-up explicitly justifies the two-pointer invariant — *why* moving the smaller side is correct.
- [ ] Recording ≥20 minutes. The first time you solve this, you will pause. That's expected.

## Function signature

```python
def trap(heights: list[int]) -> int:
    ...
```

## Test cases

```python
import pytest

@pytest.mark.parametrize("heights, expected", [
    ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
    ([4, 2, 0, 3, 2, 5], 9),
    ([], 0),
    ([3], 0),
    ([3, 3, 3], 0),
    ([5, 4, 1, 2], 1),
    ([0, 0, 0], 0),
    ([1, 0, 1], 1),
])
def test_trap(heights, expected):
    assert trap(list(heights)) == expected
```

## Common bugs

- **Updating max *after* computing water:** You must update `left_max` (or `right_max`) **before** adding `left_max - heights[left]`, otherwise you can get negative contributions.
  - Actually, the simpler discipline: update max first, then add `max - h`. If `h > max`, this is 0; otherwise it's the trapped water.
- **Wrong comparison:** `heights[left] < heights[right]` (strict) vs `<=` (non-strict). With strict, the equal-height case enters the *right* branch, which works correctly. Test with `[1, 0, 1]`.
- **Off-by-one termination:** `while l < r` is right. `<=` causes a spurious final iteration.

## Why this matters

Trapping Rain Water is the canonical "this looks like DP but is actually two-pointer" problem. Senior interviewers love it because it discriminates between candidates who memorize and candidates who *think*. If you can UMPIRE this with the O(1)-space invariant, you have demonstrated something nontrivial.

When you submit your write-up, ask a peer to **read your Evaluate section without reading your code first** and reconstruct the algorithm from your prose. If they can, your write-up is strong. If they can't, the explanation needs work.

---

This concludes Week 1's exercises and challenges. Take the [quiz](../quiz.md), do the [homework](../homework.md), then ship the [mini-project](../mini-project/README.md) — your portfolio repo's first commit.
