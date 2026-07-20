# Drill 5 — Koko Eats Bananas

> **Pattern:** Binary search on the **answer** (parametric search) — the canonical instance
> **Difficulty:** Medium
> **Target solve time:** 30 minutes (with full UMPIRE narration)
> **Why fifth and last:** the highest-yield interview skill of the week. Most candidates can write classic binary search; few recognize parametric search on a prompt that does not mention an array. If you can deliver this drill with the reframe-interval-predicate-return cadence cleanly, you have what Mock #2 grades.

## Problem statement

Koko has `piles[i]` bananas in pile `i`. Each hour, Koko chooses a pile and eats up to `k` bananas from it. If the pile has fewer than `k` bananas, she eats all remaining bananas and moves to the next hour. Guards return in `h` hours (`h >= len(piles)`).

Return the **minimum** integer `k` such that Koko can finish all piles within `h` hours.

**Examples:**

- `piles = [3, 6, 7, 11]`, `h = 8` → `4` (at `k=4`: 1+2+2+3 = 8 hours; at `k=3`: 1+2+3+4 = 10 hours, too many)
- `piles = [30, 11, 23, 4, 20]`, `h = 5` → `30` (must finish each pile in one hour)
- `piles = [30, 11, 23, 4, 20]`, `h = 6` → `23`
- `piles = [1]`, `h = 1` → `1`
- `piles = [1000000000]`, `h = 1000000000` → `1`

## UMPIRE checklist for this drill

- [ ] **U:** Restate. Confirm "each hour" means Koko picks one pile and eats up to `k`. Confirm "fewer than k" — she eats whatever remains and the hour is consumed (no carry-over). Confirm `h >= len(piles)` (so `k = max(piles)` always works). Walk an example by hand at `piles = [3, 6, 7, 11]`, `h = 8`, `k = 4`: pile 1 (3 bananas, 1 hour, total 1); pile 2 (6 bananas, 2 hours, total 3); pile 3 (7 bananas, 2 hours, total 5); pile 4 (11 bananas, 3 hours, total 8). Exactly h.
- [ ] **M:** Binary search on the answer (parametric). The 30-second memo, four-element cadence:
  > *"Reframe: find the smallest rate `k` such that Koko finishes within `h` hours.*
  > *Interval: `lo = 1` (must eat something); `hi = max(piles)` (at this rate every pile finishes in one hour, so total hours = n ≤ h).*
  > *Predicate: `feasible(k)` returns True iff total hours at rate `k` ≤ h. Monotone in `k` because a larger rate never increases hours per pile.*
  > *Return: post-loop `lo` is the smallest rate satisfying the predicate — the minimum eating speed."*
- [ ] **P:** Two functions.
  1. `feasible(k)`: walk piles, accumulating `hours += ceil(pile / k) = (pile + k - 1) // k`. Early-return False if `hours > h`. Final return `hours <= h`.
  2. `min_eating_speed(piles, h)`: half-open template. `lo = 1`, `hi = max(piles)`. While `lo < hi`: `mid = lo + (hi-lo)//2`. If `feasible(mid)`: `hi = mid`. Else: `lo = mid + 1`. Return `lo`.
  Edge case: `len(piles) == 1` — `lo = 1`, `hi = piles[0]`, and the answer is `ceil(piles[0] / h)`.
- [ ] **I:** Write the code, narrating each line. Speak the monotonicity claim: *"`feasible(k)` is monotone because increasing `k` never increases `ceil(pile / k)` for any pile; therefore the total hours is non-increasing in `k`; therefore the predicate `hours <= h` flips from False to True exactly once over `[1, max(piles)]`."*
- [ ] **R:** Trace on `piles = [3, 6, 7, 11]`, `h = 8`. lo=1, hi=11. mid=6. feasible(6): ceil(3/6)=1, ceil(6/6)=1, ceil(7/6)=2, ceil(11/6)=2. Total 6. 6 <= 8 → True. hi=6. lo=1, hi=6. mid=3. feasible(3): ceil(3/3)=1, ceil(6/3)=2, ceil(7/3)=3, ceil(11/3)=4. Total 10. 10 > 8 → False. lo=4. lo=4, hi=6. mid=5. feasible(5): ceil(3/5)=1, ceil(6/5)=2, ceil(7/5)=2, ceil(11/5)=3. Total 8. 8 <= 8 → True. hi=5. lo=4, hi=5. mid=4. feasible(4): ceil(3/4)=1, ceil(6/4)=2, ceil(7/4)=2, ceil(11/4)=3. Total 8. 8 <= 8 → True. hi=4. lo=4, hi=4, exit. Return 4. ✓
- [ ] **E:** **Time O(n log M)** where `n = len(piles)` and `M = max(piles)`. Binary search runs `log₂ M` iterations; each calls `feasible`, which is `O(n)`. **Space O(1)** — pointers and accumulators. Tradeoff: brute force tries `k = 1, 2, ..., max(piles)` linearly — `O(n · max(piles))`. Binary search on the answer is `O(n log max(piles))`, exponentially better for large rates. Best/avg/worst all `O(n log M)`.

## Acceptance criteria

- Code passes the [`timed_runner.py`](timed_runner.py) test cases for `min_eating_speed`.
- UMPIRE write-up at `umpire-writeups/c2-week-05/drill-05-koko-bananas.md`.
- Your Match section delivers the **four-element parametric cadence** (reframe, interval, predicate, return). This is the rubric for the week.
- Your Match section states the **monotonicity claim** in one sentence. (Without it, you have not earned the parametric framing.)
- Your Implement section uses the ceiling-divide idiom `(pile + k - 1) // k`, not `math.ceil(pile / k)`. The integer form is what most interview environments accept; `math.ceil` on floats has precision issues at large magnitudes.
- Recording **≥ 20 minutes**.

## Function signature (for the runner)

```python
def min_eating_speed(piles: list[int], h: int) -> int:
    """Return the smallest k such that Koko can finish all piles within h hours."""
    ...
```

## Common bugs you should catch in Review

- **Picking `hi = sum(piles)` instead of `max(piles)`.** Works (sum is also a valid upper bound) but is needlessly wide — adds `log₂ n` iterations. Pick the tightest bound that is provably valid.
- **Picking `hi = max(piles) // h`.** Wrong — too small. The answer could equal `max(piles)` (when `h == len(piles)`), so `hi` must be at least `max(piles)`.
- **Using `math.ceil(pile / k)`.** Float precision can fail at `pile = 10⁹`, `k = 7`. Use integer ceiling: `(pile + k - 1) // k`. Same answer, no float.
- **`feasible(k)` returns the hours count instead of a bool.** The predicate is boolean; misusing the return type leads to wrong branching. Be explicit.
- **Not stating monotonicity.** "Binary search on the answer" without "and here is why the predicate is monotone" is a missing-half answer. Interviewers grade on the monotonicity claim.
- **Off-by-one with `lo = mid` vs `lo = mid + 1`.** The lower-bound template uses `lo = mid + 1` (exclude tested-False mid) and `hi = mid` (keep tested-True mid). Drill 4 used the same template; copy it.

## Self-feedback template

1. Did you deliver the **four-element parametric cadence** cleanly? Time it on playback. Should be ≤ 30 seconds.
2. Did you state the **monotonicity claim** explicitly?
3. Did your Match section include the interval-justification ("`hi = max(piles)` because at that rate every pile finishes in one hour")?
4. Did your bounds check go through *before* you wrote the search loop? (Verbalize `feasible(lo)` and `feasible(hi)` to confirm the predicate flips inside `[lo, hi]`.)

## What to commit

```
umpire-writeups/c2-week-05/
├── drill-05-koko-bananas.md
└── drill_05_solution.py
```

When done, push and move on to [the challenge](../challenges/challenge-01-median-of-two-sorted-arrays.md).

This concludes the five drills. The parametric cadence you just practiced is what the mini-project asks you to deliver, in writing, five times over. By Sunday it should be reflexive.
