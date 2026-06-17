# Challenge 1 — Median of Two Sorted Arrays (LeetCode 4)

> **Pattern:** Binary search on a **partition predicate** — variant 2 (lower bound) applied to the partition index of the shorter array
> **Difficulty:** Hard
> **Target solve time:** 90 minutes (first time; 45 minutes on revisit)
> **Why hard:** the predicate is non-obvious. Most candidates know "binary search the smaller array" but cannot write the loop without one or two false starts. The defense — articulating why the partition predicate is monotone and what the post-loop invariant says — is the senior-level skill being measured.

## Problem statement

You are given two sorted (ascending) integer arrays `nums1` and `nums2` of sizes `m` and `n`. Return the **median** of the combined sorted array. The combined median is defined as:

- The middle element if `m + n` is odd.
- The average of the two middle elements if `m + n` is even.

You must solve it in `O(log(min(m, n)))` time. Anything slower — including the merge-and-take-middle solution at `O(m + n)` — is rejectable.

**Examples:**

- `nums1 = [1, 3]`, `nums2 = [2]` → `2.0` (combined `[1, 2, 3]`, median 2)
- `nums1 = [1, 2]`, `nums2 = [3, 4]` → `2.5` (combined `[1, 2, 3, 4]`, median (2+3)/2)
- `nums1 = [0, 0]`, `nums2 = [0, 0]` → `0.0`
- `nums1 = []`, `nums2 = [1]` → `1.0`
- `nums1 = [2]`, `nums2 = []` → `2.0`
- `nums1 = [1, 5, 9]`, `nums2 = [2, 3, 4, 6, 7, 8]` → `5.0`

## Acceptance criteria

- [ ] Code passes the test cases at the bottom (write your own pytest file, or extend `timed_runner.py`).
- [ ] Solution is **O(log(min(m, n)))** time and **O(1)** extra space. The merge-and-take-middle shortcut at `O(m + n)` is rejectable by spec.
- [ ] Your UMPIRE write-up **explicitly states the partition invariant** in the Match section. (See the "interview tell" subsection below.) Naming the invariant is the senior-level signal.
- [ ] Your write-up handles **all four edge cases**: empty `nums1`, empty `nums2`, every-element-of-A-less-than-every-element-of-B, every-element-of-B-less-than-every-element-of-A.
- [ ] Recording **≥ 45 minutes** — yes, three quarters of an hour. First time on this problem is long; that's the right shape.

## The decomposition (the interview tell)

The clean approach has one structural insight and one technique:

**Insight.** Pick a partition position `i` in `nums1` (`0 <= i <= m`) and let `j = (m + n + 1) // 2 - i`. This places `i` elements of `nums1` on the *left* of the split and `m - i` on the right; similarly `j` and `n - j` for `nums2`. The total number of elements on the left is `(m + n + 1) // 2` — exactly the lower-half count for both odd and even total sizes.

**Invariant.** A partition `(i, j)` is **valid** iff:
- `nums1[i - 1] <= nums2[j]` (the largest on the left of nums1 is ≤ the smallest on the right of nums2), AND
- `nums2[j - 1] <= nums1[i]` (the symmetric condition).

(With sentinels: `nums1[-1] = -inf`, `nums1[m] = +inf`, `nums2[-1] = -inf`, `nums2[n] = +inf`.)

**Technique.** Binary-search `i` over `[0, m]` for the valid partition. The predicate `valid(i)` is monotone: as `i` increases, `nums1[i - 1]` increases (or stays the same) and `nums2[j]` decreases (or stays the same), so once the first condition is satisfied it stays satisfied; the second condition is symmetric. The boundary is exactly the valid partition.

Once the valid partition is found:

- If `m + n` is odd, median = `max(nums1[i - 1], nums2[j - 1])`.
- If `m + n` is even, median = `(max(nums1[i - 1], nums2[j - 1]) + min(nums1[i], nums2[j])) / 2`.

```
nums1: [ a b c d e ]    i = partition index in nums1
nums2: [ p q r s t u v ] j = (m + n + 1) // 2 - i

left half:  [ a b ... (i-1) ] from nums1, [ p q ... (j-1) ] from nums2
right half: [ i i+1 ... ]    from nums1, [ j j+1 ... ]    from nums2

valid iff: max(left half) <= min(right half)
       iff: nums1[i-1] <= nums2[j] AND nums2[j-1] <= nums1[i]
```

The discriminator: most candidates try to merge-and-take-middle, or try a more obvious binary-search variant that fails on edge cases. The interview-tell move is **drawing the partition picture and stating the invariant** before writing code.

## UMPIRE outline

- **U:** Restate. Confirm the median definition (single middle for odd, average of two for even). Confirm `O(log(min(m, n)))` is required. Walk `nums1 = [1, 3], nums2 = [2]` by hand: combined `[1, 2, 3]`, median 2. Walk `nums1 = [1, 2], nums2 = [3, 4]`: combined `[1, 2, 3, 4]`, median 2.5. Confirm the algorithm must handle both parities and all four "empty-array" edges.

- **M:** Binary search on a **partition predicate**. The 30-second memo, four-element parametric cadence:
  > *"Reframe: find the smallest partition index `i` in `[0, m]` such that the partition `(i, j)` with `j = (m + n + 1) // 2 - i` is valid — i.e., the largest left-half element is ≤ the smallest right-half element.*
  > *Interval: `lo = 0`, `hi = m` where `m = min(len(nums1), len(nums2))` (search the shorter array).*
  > *Predicate: `valid(i)` = (`nums1[i - 1] <= nums2[j]` AND `nums2[j - 1] <= nums1[i]`), with sentinels `-inf` / `+inf` for out-of-bounds. Monotone in `i` because `nums1[i - 1]` rises and `nums2[j]` falls as `i` increases — so the boolean flips from False (left-of-nums1 too small) to True (valid) to False (left-of-nums1 too large) but in *one direction* under the right framing (see Plan below).*
  > *Return: the valid `i` defines the partition; compute the median from the four boundary elements."*

  Note on monotonicity: a naive read suggests the predicate is True only in the middle of `[0, m]` — *not* monotone. The clean version is: binary-search for the largest `i` such that `nums1[i - 1] <= nums2[j]` (which *is* monotone — once True, decreasing `i` keeps it True; once False, increasing `i` keeps it False). The other condition `nums2[j - 1] <= nums1[i]` is automatically the "other direction" — they meet at the valid partition. See Plan.

- **P:** Three things.
  1. **Make `nums1` the shorter array.** If not, swap. This ensures `m <= n` and the binary search runs in `O(log min)`.
  2. **Set `lo = 0`, `hi = m`.** Note: `hi = m` (not `m - 1`), and the loop is half-open with `lo <= hi`. Variant: we are searching for the partition position, which can range from 0 (no nums1 in left half) to `m` (all of nums1 in left half), inclusive on both ends. The half-open shape applied to the inclusive range becomes `[0, m]` with `lo <= hi`.
  3. **In the loop, compute `i = (lo + hi) // 2`, `j = (m + n + 1) // 2 - i`.** Sentinel values: `left1 = nums1[i - 1] if i > 0 else -inf`, `right1 = nums1[i] if i < m else +inf`, similarly for `left2`, `right2`. Branches:
     - If `left1 <= right2` and `left2 <= right1`: valid partition. Compute the median and return.
     - Else if `left1 > right2`: too much of nums1 on the left → `hi = i - 1`.
     - Else (`left2 > right1`): too little of nums1 on the left → `lo = i + 1`.
  Edge cases: empty `nums1` — `m = 0`, `i = 0` always, `j = (n + 1) // 2`. Empty `nums2` — after swap, `nums1` is empty; handled by the same edge.

- **I:** Implement. The sentinel handling is the most error-prone part — write it explicitly with the `if i > 0 else float('-inf')` pattern. Do not assume `i > 0` or `j > 0`; the boundary cases trigger them.

- **R:** Trace on `nums1 = [1, 3]`, `nums2 = [2]`. After swap: `nums1 = [2], nums2 = [1, 3]`, `m = 1, n = 2`. Initial `lo = 0, hi = 1`.
  - i = 0, j = (1 + 2 + 1) // 2 - 0 = 2. left1 = -inf, right1 = 2 (nums1[0]). left2 = nums2[1] = 3, right2 = +inf. Check: left1 (-inf) <= right2 (+inf), yes. left2 (3) <= right1 (2), **no**. Branch: too little of nums1 on left → lo = 1.
  - i = 1, j = 2 - 1 = 1. left1 = nums1[0] = 2, right1 = +inf. left2 = nums2[0] = 1, right2 = nums2[1] = 3. Check: left1 (2) <= right2 (3), yes. left2 (1) <= right1 (+inf), yes. Valid. Combined size 3 is odd → median = max(left1, left2) = max(2, 1) = 2. ✓

  Trace on `nums1 = [1, 2], nums2 = [3, 4]`. `m = 2, n = 2`. lo = 0, hi = 2.
  - i = 1, j = (4 + 1) // 2 - 1 = 1. left1 = 1, right1 = 2. left2 = 3, right2 = 4. left1 (1) <= right2 (4), yes. left2 (3) <= right1 (2), **no**. Branch: too little → lo = 2.
  - i = 2, j = 0. left1 = 2, right1 = +inf. left2 = -inf, right2 = 3. left1 (2) <= right2 (3), yes. left2 (-inf) <= right1 (+inf), yes. Valid. Combined size 4 is even → median = (max(2, -inf) + min(+inf, 3)) / 2 = (2 + 3) / 2 = 2.5. ✓

- **E (graded):** **Time O(log(min(m, n)))** — we binary-search the partition index over the shorter array, depth `log₂(min(m, n))`; each iteration is `O(1)` (four comparisons, no inner loop). **Space O(1)** — six scalars (lo, hi, i, j, plus the four sentinel-aware partition values). Tradeoff: merge-and-take-middle is `O(m + n)` time, `O(1)` space — strictly worse on time. A heap-based "kth smallest of two sorted lists" approach is `O((m + n) log(m + n))` — even worse. Binary search on the partition is the optimal approach. Best/avg/worst all `O(log(min(m, n)))`.

## Function signature

```python
def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    """Return the median of the combined sorted arrays in O(log(min(m, n))) time."""
    ...
```

## Test cases to verify

```python
import pytest

@pytest.mark.parametrize("nums1, nums2, expected", [
    ([1, 3], [2], 2.0),
    ([1, 2], [3, 4], 2.5),
    ([0, 0], [0, 0], 0.0),
    ([], [1], 1.0),
    ([2], [], 2.0),
    ([1, 5, 9], [2, 3, 4, 6, 7, 8], 5.0),
    ([1, 2, 3, 4, 5], [6, 7, 8, 9, 10], 5.5),
    ([6, 7, 8, 9, 10], [1, 2, 3, 4, 5], 5.5),
    ([1], [2, 3, 4, 5], 3.0),
    ([100000], [100001], 100000.5),
])
def test_find_median(nums1, nums2, expected):
    assert find_median_sorted_arrays(nums1, nums2) == pytest.approx(expected)
```

## Common bugs you should catch in Review

- **Not swapping to ensure the shorter array is `nums1`.** Without the swap, the binary search could be over the longer array and either be slower than the spec or, with the wrong `j` formula, run off the array.
- **Wrong `j` formula.** `j = (m + n + 1) // 2 - i` for the **lower half count** including the median's left neighbor (in the odd case). Using `j = (m + n) // 2 - i` shifts the partition and produces the wrong median on odd lengths.
- **Sentinel handling.** Omitting `-inf` / `+inf` for boundary partition positions (`i = 0` or `i = m`) causes index errors or wrong comparisons. The sentinels must be infinities (or, equivalently, treat the comparison as "vacuously true" — but the explicit infinity form is clearer).
- **Returning `int` instead of `float`.** Even when both medians come from integer inputs, the average of two ints may be a `.5` float. Use `/ 2` (float division), not `// 2`.
- **Trying the merge-and-take-middle.** `O(m + n)` is correct but rejected by spec. Verbalize this rejection in Match; do not produce the merge solution in Implement.
- **Off-by-one in the partition predicate.** The predicate is `left1 <= right2` and `left2 <= right1` — strict-`<` would miss the case where the four values are equal across the partition.

## The "why O(log(min(m, n)))?" defense

Out loud, in your Evaluate section:

> "**Why O(log(min(m, n))) time, O(1) space.** We binary-search the partition index over the shorter array; the search depth is `log₂(min(m, n))`. Each iteration computes four scalar comparisons in `O(1)` — no inner loop, no auxiliary data structure. The merge-and-take-middle alternative is `O(m + n)` time, same `O(1)` space — strictly worse on time and rejected by spec. The senior signal is that the partition predicate's monotonicity makes the binary search legal; without that observation we would have no comparator and the algorithm would not be expressible."

Memorize the shape of that sentence. Saying it cleanly is the difference between "solved Median of Two Sorted Arrays" and "demonstrated mastery of the boundary-defense skill."

## Why this matters

Median of Two Sorted Arrays is *the* canonical hard binary-search problem. Real onsite interviews ask it at FAANG and FAANG-adjacent companies routinely — not because the algorithm is novel (it has been known for 40 years), but because the problem tests three independent senior-level skills:

1. **Recognizing that the merge solution is rejectable** despite being correct — i.e., honoring the asymptotic spec when a working alternative is available.
2. **Inventing the partition predicate** — the hardest predicate of any Phase 2 problem.
3. **Defending the boundary** — sentinels, swap, half-open vs closed, off-by-one in `j` — all in one problem.

When you revisit this challenge before Mock #2, **re-derive the partition predicate from scratch** rather than re-reading your old solution. The derivation is the skill.

## Stretch

**Find Peak Element** (LC 162) — a much easier "binary search on a non-sorted array via a monotone-flip predicate" problem. Useful warm-up if Median feels overwhelming, or a quick check after Median that the technique transfers. Should take 20 minutes once Median is in muscle memory.

**Median of Data Stream** (LC 295) — a two-heap problem (covered in Week 9). Out of scope for Week 5 but worth knowing it exists; the offline-median problem here and the online-median problem in Week 9 are conceptually adjacent.

---

This concludes Week 5's challenges. Take the [quiz](../05-quiz.md), do the [homework](../06-homework.md), then ship the [mini-project](../07-mini-project/00-overview.md) — five binary-search write-ups with parametric cadence.
