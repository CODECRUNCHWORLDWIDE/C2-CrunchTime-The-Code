# Challenge 1 — Subarray Sum Equals K

> **Pattern:** Prefix sums + hash map (frequency)
> **Difficulty:** Medium
> **Target solve time:** 90 minutes
> **Why hard:** the *reformulation* (subarray sum → difference of prefix sums) is the discriminator. Most candidates write the O(n²) version and stall. Recognizing the prefix-sum + hash-map combo is the interview tell.

## Problem statement

Given an integer array `nums` and an integer `k`, return the **total number of non-empty subarrays** whose sum equals `k`. A subarray is a contiguous slice `nums[i..j]`.

The array can contain negative numbers, so you cannot assume monotonic prefix sums (this is why sliding window does not apply — that's why we use hash map).

**Examples:**

- `nums = [1, 1, 1]`, `k = 2` → `2` (subarrays `[0..1]` and `[1..2]`)
- `nums = [1, 2, 3]`, `k = 3` → `2` (subarrays `[0..1]` and `[2..2]`)
- `nums = [1, -1, 0]`, `k = 0` → `3` (subarrays `[0..1]`, `[1..2]`, `[2..2]`)
- `nums = [3, 4, 7, 2, -3, 1, 4, 2]`, `k = 7` → `4`

## Acceptance criteria

- [ ] Code passes the test cases at the bottom (write your own pytest file, or extend `timed_runner.py`).
- [ ] Solution is **O(n) time** and **O(n) space**. The naive O(n²) does not pass.
- [ ] Your UMPIRE write-up **explicitly derives the prefix-sum reformulation** — that is the interview tell.
- [ ] Recording ≥20 minutes.

## The key reformulation (work this out before reading the solution)

Define the prefix sum array:

```
S[0] = 0
S[i] = nums[0] + nums[1] + ... + nums[i-1]    for i = 1..n
```

So `S[i]` is the sum of the first `i` elements (`S[0] = 0` represents the empty prefix).

A subarray `nums[i..j]` (inclusive on both ends, 0-indexed) has sum `S[j+1] - S[i]`.

So the question "how many subarrays sum to k?" becomes "**how many pairs `(i, j)` with `i ≤ j` satisfy `S[j+1] - S[i] = k`?**" — i.e., "how many pairs of prefix-sum indices have a difference of `k`?"

That's a *two-sum-style* question over the prefix sums. And the two-sum-style question has an O(n) hash-map solution. We're done — the only work left is implementation.

## UMPIRE outline

- **U:** Restate. Confirm subarrays are *contiguous* and *non-empty*; negatives are allowed; multiple subarrays may overlap. Walk one example by hand.
- **M:** Prefix sums + hash map of *prefix-sum frequencies*. For each index, check how many prior prefix sums equal `running - k`.
- **P:**
  1. Initialize `counts = {0: 1}` (the empty prefix has sum 0; this is the seed that makes "subarray starting at index 0" work).
  2. Initialize `running = 0`, `answer = 0`.
  3. For each `x in nums`:
     a. `running += x`.
     b. `answer += counts.get(running - k, 0)`.
     c. `counts[running] = counts.get(running, 0) + 1`.
  4. Return `answer`.
- **I:** Implement. Order inside the loop matters: **update running first; query the map; then insert the new running value.** Inserting first would let the current index match itself.
- **R:** Trace on `[1, -1, 0]` with `k = 0`. Walk through:
  | step | x | running | running-k | counts.get | answer | counts after |
  |-----:|--:|--------:|----------:|-----------:|-------:|--------------|
  | init |   | 0       |           |            | 0      | {0:1}        |
  | 1    | 1 | 1       | 1         | 0          | 0      | {0:1, 1:1}   |
  | 2    | -1| 0       | 0         | 1          | 1      | {0:2, 1:1}   |
  | 3    | 0 | 0       | 0         | 2          | 3      | {0:3, 1:1}   |
- **E:** **O(n) time** — single pass, O(1) average hash-map ops. **O(n) space** — the counts map can hold up to n+1 distinct prefix sums. Tradeoff: brute force O(n²)/O(1); fails the time bound. No improvement obvious; O(n) is the lower bound.

## Function signature

```python
def subarray_sum_equals_k(nums: list[int], k: int) -> int:
    """Return the number of contiguous non-empty subarrays of nums that sum to k."""
    ...
```

## Test cases to verify

```python
import pytest

@pytest.mark.parametrize("nums, k, expected", [
    ([1, 1, 1], 2, 2),
    ([1, 2, 3], 3, 2),
    ([1, -1, 0], 0, 3),
    ([3, 4, 7, 2, -3, 1, 4, 2], 7, 4),
    ([1], 1, 1),
    ([1], 0, 0),
    ([0, 0, 0, 0], 0, 10),       # any subarray of zeros sums to 0; C(5,2) = 10
    ([], 0, 0),
])
def test_subarray_sum(nums, k, expected):
    assert subarray_sum_equals_k(list(nums), k) == expected
```

## Common bugs

- **Forgetting the `{0: 1}` seed.** Without it, subarrays starting at index 0 are missed. The seed represents "the empty prefix has sum 0; we've seen it once."
- **Insert before query.** The current running sum, freshly inserted, would match itself if `k = 0`. Always query first, insert after.
- **Counting subarrays as pairs of indices but forgetting subarrays of length 1.** The seed handles this; the same `S[j+1] - S[j] = nums[j]` falls naturally out of the math.
- **Trying to use sliding window.** Negative numbers break the window invariant. This is hash-map territory specifically *because* negatives are allowed.

## The "why is this O(n)?" defense

Out loud, in your Evaluate section:

> "**Why O(n).** Single pass through `nums`. Each iteration does O(1) average work: one arithmetic add, one hash-map get, one hash-map insert. So total work is `O(n) × O(1) = O(n)`. Space is the hash map, which holds at most `n + 1` distinct prefix sums."

That's a confident, correct, two-sentence Evaluate. Write it down. Memorize the shape.

## Why this matters

Subarray-Sum-Equals-K is the **canonical prefix-sum + hash-map problem.** A surprising number of interview problems are subarray-property questions in disguise:

- "Count subarrays with at most k distinct elements" (sliding window — Week 3)
- "Count subarrays divisible by k" (prefix sums mod k + hash map)
- "Continuous subarray sum is a multiple of k" (same — LeetCode 523)
- "Subarray product less than k" (sliding window for positive integers)

Recognizing the **prefix-sum + hash-map** combo is one of the highest-yield pattern matches in the entire course. UMPIRE this challenge twice: once now, once at the end of Week 11 (DP) when you can compare with DP framings.

## Stretch

**LeetCode 974 — Subarray Sums Divisible by K.** Same shape; the key is `running % k` instead of `running`, with the hash map counting residue frequencies. Try it after this challenge.

Commit your solution and write-up. Move on to [Challenge 2](challenge-02-lru-cache.md).
