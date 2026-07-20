# Drill 1 — Average of Every K-Length Subarray

> **Pattern:** Sliding window, fixed-size
> **Difficulty:** Easy
> **Target solve time:** 15 minutes (with full UMPIRE narration)
> **Why first:** the simplest sliding-window problem in existence. If you can't UMPIRE this, you can't UMPIRE anything else this week.

## Problem statement

Given an array of integers `nums` and a window size `k`, return a list of the **averages of every contiguous subarray of length `k`**.

If `k > len(nums)`, return an empty list. Assume `k >= 1`.

**Examples:**

- `nums = [1, 3, 2, 6, -1, 4, 1, 8, 2]`, `k = 5` → `[2.2, 2.8, 2.4, 3.6, 2.8]`
- `nums = [1, 2, 3, 4]`, `k = 2` → `[1.5, 2.5, 3.5]`
- `nums = [5]`, `k = 1` → `[5.0]`
- `nums = [1, 2]`, `k = 3` → `[]`
- `nums = []`, `k = 1` → `[]`

## UMPIRE checklist for this drill

Before you write a line of code, say *each of these* out loud, in order. Recorder running.

- [ ] **U:** Restate. Confirm output is a list of floats, one per starting index `i` from `0` to `len(nums) - k`. Confirm the `k > len(nums)` case returns `[]`, and so does an empty `nums`.
- [ ] **M:** Sliding window, fixed-size. The 30-second memo: *"This is a sliding-window problem because the prompt asks for a value over every contiguous subarray of length k. The window is fixed-size (k is given upfront). The invariant: `window_sum == sum(nums[right-k+1..right])`. Auxiliary state: a single running sum."*
- [ ] **P:** Build the first window's sum from `nums[0..k-1]` (O(k)). Push `window_sum / k` to the result. Then for `right` from `k` to `n-1`: `window_sum += nums[right] - nums[right - k]`; push `window_sum / k`.
- [ ] **I:** Write the code, narrating each line.
- [ ] **R:** Trace on `[1, 3, 2, 6, -1, 4, 1, 8, 2]` with `k = 5`. First sum = 11, avg = 2.2. Slide: +4, -1 → 14, avg 2.8. Slide: +1, -3 → 12, avg 2.4. Slide: +8, -2 → 18, avg 3.6. Slide: +2, -6 → 14, avg 2.8. ✓
- [ ] **E:** **Time O(n)** — the first window is O(k); each of the remaining n-k slides is O(1). Total O(k + n - k) = O(n). **Space O(1)** auxiliary (the running sum); output list is O(n - k + 1) which we don't count as auxiliary.

## Acceptance criteria

- Code passes the [`timed_runner.py`](timed_runner.py) test cases for `window_averages`.
- A UMPIRE write-up exists at `umpire-writeups/c2-week-03/drill-01-fixed-window-average.md` in your portfolio repo.
- Your Match section includes the 30-second pattern-recognition memo (four sentences naming sliding window, fixed-size, the invariant, and the auxiliary state).
- You have a recording of yourself narrating the solve.
- The recording is **at least 8 minutes long.** If you finished in 3 minutes, you skipped Match or Evaluate. Re-do it.

## Function signature (for the runner)

```python
def window_averages(nums: list[int], k: int) -> list[float]:
    """
    Return the averages of every contiguous subarray of length k in nums.
    If k > len(nums), return an empty list.
    """
    ...
```

## Common bugs you should catch in Review

- **Recomputing `sum(nums[i:i+k])` inside the loop.** That's O(k) per iteration → O(n·k) total. The whole point of sliding window is to avoid this. Use the incremental update `window_sum += nums[right] - nums[right - k]`.
- **Integer vs float division.** Python 3's `/` returns a float — good. Make sure you don't accidentally use `//` (integer division) and lose the fractional part.
- **Off-by-one on the loop range.** The slide loop runs `right` from `k` to `n - 1` inclusive (i.e. `range(k, len(nums))`). The first window is `nums[0..k-1]`; the last window is `nums[n-k..n-1]`.
- **Forgetting the empty / `k > n` guard.** Return `[]` early; otherwise `range(k, n)` is empty and you'd push the wrong first average.

## Self-feedback template

After you finish, listen to your recording at 1.5×. Write three notes:

1. Did you deliver the 30-second pattern-recognition memo cleanly? (Should hit four sentences in under 30 seconds.)
2. Did you say the standard amortized-O(n) Evaluate sentence?
3. How long did Match take? (Should be <30 seconds on this problem — fixed-size sliding window is a textbook signal.)

Add those notes to the end of your UMPIRE write-up.

## What to commit to your portfolio repo

```
crunchtime-interview-prep-<you>/
└── umpire-writeups/
    └── c2-week-03/
        ├── drill-01-fixed-window-average.md       # write-up
        └── drill_01_solution.py                    # your solution
```

When done, push and move on to [Drill 2](drill-02-longest-substring-no-repeat.md).
