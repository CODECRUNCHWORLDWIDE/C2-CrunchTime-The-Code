# Challenge 1 — The Merged Book Boundary

> **Topic:** bisecting a **split point** across two sorted lists, instead of bisecting a position inside one
> **Lecture:** [01 — The Binary-Search Template](../lecture-notes/01-the-binary-search-template.md)
> **Difficulty:** Hard
> **Target time:** 90 minutes the first time, 45 on a revisit
> **Why this one:** every search so far handed you the thing to compare. Here you have to invent it — and the thing you invent is not a value at all, it is a place to cut. This is the hardest binary-search shape in the course, and the skill it measures is stating an invariant before writing code rather than after.

## The Brief

A clearing house takes an end-of-session report from each of two venues. Each
report is a list of **position deltas** — a buy is a positive number, a sell is
a negative one — and each venue hands its list over already sorted, smallest
first.

The two reports are never merged into one file. Together they run to millions
of entries, and the risk desk queries them all session long.

The desk works in **ranks**. "Give me the 4th smallest delta across both
reports." Counting from 1, and counting duplicates separately: if the value
`8` appears twice, it occupies two consecutive ranks.

```
venue A:  3   8   8  15
venue B:  1   4   9

combined: 1   3   4   8   8   9  15
rank:     1   2   3   4   5   6   7
```

Rank 4 is `8`. And the desk wants its **successor** too — the value at the
next rank up — because that pair is what a boundary really is. So the answer
for `k = 4` is `(8, 8)`: rank 4 and rank 5 both hold an `8`, one from each
report.

Three contract decisions:

- Return `(kth, next_kth)`.
- At the **last** rank there is no successor, so return `(kth, None)`.
- When `k` is out of range entirely — below 1, or above the combined count —
  return `None` for the whole result. Not an exception. A question with no
  answer still deserves a reply.

Now the hard part, and the reason this is a challenge rather than an exercise.
**You must do it in about `log2` of the shorter list's length.** Merging the
two reports and reading off index `k - 1` is correct, and it is rejected by the
spec: it walks ten million entries and allocates a ten-million-entry list, per
query, thousands of times a session.

So do not search for a *value*. Search for a **cut**.

```
venue A:  [ . . . a[i-1] | a[i] . . . ]      i deltas on the left
venue B:  [ . . . b[j-1] | b[j] . . . ]      j = k - i deltas on the left

the left side holds exactly k deltas
```

Pick how many deltas come from A — call it `i` — and the count from B follows
immediately, because the left side has to hold exactly `k` of them:
`j = k - i`. One number to choose instead of two. That is what turns a
two-dimensional decision into something you can bisect.

A cut is **valid** when everything on the left is no bigger than everything on
the right. Inside each list that is free, because each list is already sorted.
Only the two crossing comparisons need checking:

```
valid  ⟺  a[i-1] <= b[j]  AND  b[j-1] <= a[i]
```

with `-infinity` standing in when an index falls off the left end and
`+infinity` when it falls off the right. At a valid cut, the `k`-th smallest is
`max(a[i-1], b[j-1])` — the largest thing on the left — and its successor is
`min(a[i], b[j])` — the smallest thing on the right. If that minimum is
`+infinity`, there was nothing on the right at all, and the successor is
`None`.

And the reason bisection works: as `i` grows by one, `a[i-1]` moves up or
stays and `b[j]` moves down or stays, so `a[i-1] <= b[j]` can only switch from
true to false and never back. The other condition can only switch the other
way. Two one-way conditions moving in opposite directions meet at exactly one
place, and that place is the valid cut.

## Starter

Save this as `challenge-01-order-book-boundary.py` and fill in every `TODO`.

```python
"""challenge-01-order-book-boundary.py — the rank boundary of two books.

Binary search on a SPLIT, not on a value.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

import random
from math import inf

# ---- Given data ----
VENUE_A: list[int] = [3, 8, 8, 15]
VENUE_B: list[int] = [1, 4, 9]


# ---- Your task ----
def book_boundary(venue_a: list[int], venue_b: list[int], k: int) -> tuple[int, int | None] | None:
    """Return the k-th and (k+1)-th smallest deltas of the combined multiset.

    Args:
        venue_a: One venue's deltas, sorted ascending, duplicates allowed.
        venue_b: The other venue's deltas, sorted ascending.
        k: The 1-based rank the risk desk asked for.

    Returns:
        (kth, next_kth), with next_kth None at the last rank, or None when k
        falls outside 1..len(venue_a) + len(venue_b).
    """
    # TODO: name the shorter list `short` so the search depth is log(min(m, n))
    # TODO: guard k < 1 and k > m + n
    # TODO: clamp the interval so j = k - taken is always a legal count
    # TODO: read the four boundary values with explicit if/else, using ±inf
    # TODO: two branches move the interval, the third returns the answer
    ...


# ---- Self-check ----
if __name__ == "__main__":
    print(f"combined order: {sorted(VENUE_A + VENUE_B)}")
    for rank in (1, 4, 7, 8):
        print(f"k={rank} -> {book_boundary(VENUE_A, VENUE_B, rank)}")

    assert book_boundary(VENUE_A, VENUE_B, 1) == (1, 3)
    assert book_boundary(VENUE_A, VENUE_B, 2) == (3, 4)
    assert book_boundary(VENUE_A, VENUE_B, 4) == (8, 8)
    assert book_boundary(VENUE_A, VENUE_B, 7) == (15, None)
    assert book_boundary(VENUE_A, VENUE_B, 8) is None
    assert book_boundary(VENUE_A, VENUE_B, 0) is None
    assert book_boundary([], [42], 1) == (42, None)
    assert book_boundary([42], [], 1) == (42, None)
    assert book_boundary([], [], 1) is None
    assert book_boundary([1, 2, 3], [10, 20, 30], 3) == (3, 10)
    assert book_boundary([1, 2, 3], [10, 20, 30], 4) == (10, 20)
    assert book_boundary([10, 20, 30], [1, 2, 3], 3) == (3, 10)
    assert book_boundary([5, 5, 5], [5, 5], 3) == (5, 5)
    assert book_boundary([-9, -4, 0], [-7, 2], 2) == (-7, -4)

    rng = random.Random(20250505)
    pairs = 0
    for _ in range(500):
        a = sorted(rng.randrange(-20, 21) for _ in range(rng.randrange(0, 9)))
        b = sorted(rng.randrange(-20, 21) for _ in range(rng.randrange(0, 9)))
        merged = sorted(a + b)
        for rank in range(0, len(merged) + 2):
            if 1 <= rank <= len(merged):
                after = merged[rank] if rank < len(merged) else None
                wanted = (merged[rank - 1], after)
            else:
                wanted = None
            assert book_boundary(a, b, rank) == wanted, (a, b, rank)
        pairs += 1
    print(f"cross-checked {pairs} generated book pairs against a plain merge")
    print("All checks passed.")
```

Two ideas you need before you start.

**Clamping the interval.** `i` cannot roam over all of `0 … m`. Since
`j = k - i` has to be a legal count into the other list — at least 0, at most
`n` — the legal values of `i` are `max(0, k - n)` up to `min(k, m)`. Clamp
before the loop and every out-of-bounds crash on this problem disappears at
once, because the four reads can never ask for an index the clamp did not
allow.

**Infinity as a boundary marker.** `float('-inf')` is smaller than every
integer and `float('inf')` is bigger than every integer, so they make the
off-the-end comparisons come out right without a special case. Do not invent
a "very big number" instead: deltas run to a trillion in either direction, and
every one of those is a legal value.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-05-binary-search/challenges/challenge-01-order-book-boundary.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `book_boundary(venue_a, venue_b, k)` returns `(kth, next_kth)` for the
   combined multiset, with `k` counted from 1.
2. `next_kth` is `None` at the last rank — never `float('inf')`.
3. The whole result is `None` when `k < 1` or `k > len(venue_a) + len(venue_b)`.
   It never raises.
4. The search runs over the **shorter** of the two lists, so its depth is
   `log2(min(m, n))`.
5. The interval is clamped to `[max(0, k - n), min(k, m)]` before the loop.
6. Nothing merges, copies, sorts, or slices either list. Extra space is a fixed
   handful of variables.
7. The argument order does not matter: swapping the two reports gives the same
   answer.
8. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(venue_a) <= 5_000_000` and `0 <= len(venue_b) <= 5_000_000`.**
  Ten million deltas in the worst case. The merge is not merely slower — it
  allocates a ten-million-element list per query, and the desk issues thousands
  of queries per session, so the memory traffic is the binding cost rather than
  the comparison count. The cut search allocates nothing and makes about
  twenty-three comparisons. Either list may be **empty**, and the algorithm has
  to reach that answer through the clamp rather than through a special branch.

- **`-10**12 <= delta <= 10**12`.** Deltas are **signed** and large. This is the
  bound that forces genuine infinities as the off-the-end markers: any
  "impossibly large" integer you invent is a delta some venue could legitimately
  report. It is also why a language with 32-bit integers needs a wider type
  here, which is worth saying out loud even in Python.

- **`k` is 1-based, and out-of-range `k` is legal input.** The desk's UI lets
  somebody type any number. `k = 0` and `k = 8` on a seven-delta book are
  questions with the answer `None`, not crashes.

- **Both lists arrive sorted ascending.** Sorting either one yourself costs
  `O(m log m)` and destroys the entire point — the whole method is built on
  order you were given for free.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python challenge-01-order-book-boundary.py
combined order: [1, 3, 4, 8, 8, 9, 15]
k=1 -> (1, 3)
k=4 -> (8, 8)
k=7 -> (15, None)
k=8 -> None
cross-checked 500 generated book pairs against a plain merge
All checks passed.
```

The `k = 4` row returns the same value twice, and that is correct rather than
a duplicate bug: ranks 4 and 5 both hold an `8`, one from each report. The
cross-check line is the one that matters most — it re-answers every rank of
five hundred generated book pairs with a plain merge and compares. Write that
generator **before** the solution, not after; a reference implementation you
already trust is the cheapest debugging tool on this problem.

## Steps

1. Save the starter and run it. `book_boundary` returns `Ellipsis`, so the
   first `print` shows it and the first assert fails. Expected.
2. **Draw the cut before you type anything.** Two rows, a vertical bar in each,
   the four boundary values labelled `a[i-1]`, `a[i]`, `b[j-1]`, `b[j]`. Write
   the validity condition underneath it. Every wrong attempt at this problem
   starts with code instead of a picture.
3. Swap so the shorter list is the one you search. Rebind names; do not copy
   data.
4. Write the two guards: `k < 1` and `k > m + n`.
5. Clamp: `lo, hi = max(0, k - n), min(k, m)`. Convince yourself on paper that
   `j = k - i` is legal at both ends of that interval.
6. Open a closed-interval loop, `while lo <= hi`. Inside, take `i` at the
   midpoint and set `j = k - i`.
7. Read the four boundary values with explicit `if … else` expressions and
   `±inf`. No `try`/`except`, no negative-index tricks.
8. Three branches. `left_short > right_long` means you took too many from the
   short list, so move `hi` down. `left_long > right_short` means too few, so
   move `lo` up. Otherwise the cut is valid: assemble and return.
9. Assemble carefully: `kth = max(left_short, left_long)`,
   `nxt = min(right_short, right_long)`, and convert `inf` to `None` once, at
   the return.
10. Run the cross-check. Then trace `k = 4` and `k = 7` by hand and compare
    against the traces in The Solution.

## The Solution

```python
"""challenge-01-order-book-boundary-solution.py - the rank boundary of two books.

Binary search on a SPLIT, not on a value. Choose how many deltas from the
shorter report land left of the split; the count from the other report
follows, because the left side must hold exactly k deltas.

The self-checks at the bottom are the starter's, unchanged. The last one
cross-checks the search against a plain merge on generated books, which is
where sentinel bugs surface. When they all pass the file prints
"All checks passed."
"""

import random
from math import inf

# ---- Given data ----
VENUE_A: list[int] = [3, 8, 8, 15]
VENUE_B: list[int] = [1, 4, 9]


# ---- Your task ----
def book_boundary(venue_a: list[int], venue_b: list[int], k: int) -> tuple[int, int | None] | None:
    """Return the k-th and (k+1)-th smallest deltas of the combined multiset.

    Args:
        venue_a: One venue's deltas, sorted ascending, duplicates allowed.
        venue_b: The other venue's deltas, sorted ascending.
        k: The 1-based rank the risk desk asked for.

    Returns:
        (kth, next_kth), with next_kth None at the last rank, or None when k
        falls outside 1..len(venue_a) + len(venue_b).
    """
    short, long = (venue_a, venue_b) if len(venue_a) <= len(venue_b) else (venue_b, venue_a)
    m, n = len(short), len(long)
    if k < 1 or k > m + n:
        return None

    lo, hi = max(0, k - n), min(k, m)
    while lo <= hi:
        taken = lo + (hi - lo) // 2  # deltas taken from the shorter report
        rest = k - taken  # deltas taken from the longer one
        left_short = short[taken - 1] if taken > 0 else -inf
        right_short = short[taken] if taken < m else inf
        left_long = long[rest - 1] if rest > 0 else -inf
        right_long = long[rest] if rest < n else inf

        if left_short > right_long:
            hi = taken - 1  # took too many from the shorter report
        elif left_long > right_short:
            lo = taken + 1  # took too few
        else:
            kth = max(left_short, left_long)
            nxt = min(right_short, right_long)
            return kth, (None if nxt == inf else nxt)
    return None  # unreachable: the clamped interval always holds the crossing


# ---- Self-check ----
if __name__ == "__main__":
    print(f"combined order: {sorted(VENUE_A + VENUE_B)}")
    for rank in (1, 4, 7, 8):
        print(f"k={rank} -> {book_boundary(VENUE_A, VENUE_B, rank)}")

    assert book_boundary(VENUE_A, VENUE_B, 1) == (1, 3)
    assert book_boundary(VENUE_A, VENUE_B, 2) == (3, 4)
    assert book_boundary(VENUE_A, VENUE_B, 4) == (8, 8)
    assert book_boundary(VENUE_A, VENUE_B, 7) == (15, None)
    assert book_boundary(VENUE_A, VENUE_B, 8) is None
    assert book_boundary(VENUE_A, VENUE_B, 0) is None
    assert book_boundary([], [42], 1) == (42, None)
    assert book_boundary([42], [], 1) == (42, None)
    assert book_boundary([], [], 1) is None
    assert book_boundary([1, 2, 3], [10, 20, 30], 3) == (3, 10)
    assert book_boundary([1, 2, 3], [10, 20, 30], 4) == (10, 20)
    assert book_boundary([10, 20, 30], [1, 2, 3], 3) == (3, 10)
    assert book_boundary([5, 5, 5], [5, 5], 3) == (5, 5)
    assert book_boundary([-9, -4, 0], [-7, 2], 2) == (-7, -4)

    rng = random.Random(20250505)
    pairs = 0
    for _ in range(500):
        a = sorted(rng.randrange(-20, 21) for _ in range(rng.randrange(0, 9)))
        b = sorted(rng.randrange(-20, 21) for _ in range(rng.randrange(0, 9)))
        merged = sorted(a + b)
        for rank in range(0, len(merged) + 2):
            if 1 <= rank <= len(merged):
                after = merged[rank] if rank < len(merged) else None
                wanted = (merged[rank - 1], after)
            else:
                wanted = None
            assert book_boundary(a, b, rank) == wanted, (a, b, rank)
        pairs += 1
    print(f"cross-checked {pairs} generated book pairs against a plain merge")
    print("All checks passed.")
```

**One equation removes a whole dimension.** There are two numbers to choose —
how many from each report — but they are not independent: the left side must
hold exactly `k` deltas, so `rest = k - taken`. Choosing `taken` chooses both.
Everything else on this page is a consequence of that one line.

**The monotonicity claim, said properly.** As `taken` rises by one,
`left_short` moves up or stays (you are taking a later element of a sorted
list) and `right_long` moves down or stays (`rest` falls, so the first element
on the right of the long list gets earlier). So `left_short > right_long` can
switch from false to true and never back. The other condition,
`left_long > right_short`, switches the opposite way for the mirror reason.
Two one-way switches running in opposite directions cross exactly once, and
the crossing is the valid cut. That paragraph is the thing an interviewer is
listening for; the code is a consequence of it.

**The clamp is what deletes the bounds checking.** Without it, `rest = k -
taken` can go negative or exceed `n`, and every out-of-range crash on this
problem traces back to that. With `lo = max(0, k - n)` and `hi = min(k, m)`,
`rest` is guaranteed to land in `0 … n` at every midpoint, so the only reads
that ever fall off an end are the deliberate ones the `±inf` guards cover.

**Search the shorter list, or the stated bound is not met.** The swap costs
nothing — it rebinds two names, it does not move data — and it turns
`log2(max(m, n))` into `log2(min(m, n))`. On a five-million by five-element
pair, that is twenty-three iterations versus three.

**`<=`, not `<`, in the validity test.** Look at `[5, 5, 5]` and `[5, 5]`:
every comparison in sight is an equality. A strict comparison rejects the
valid cut, both branches move, and the loop either misses the answer or spins.
Equal values are allowed to sit on either side of the cut, because equal
values genuinely can.

**Trace `k = 4` on the sample books.** The shorter list is
`short = [1, 4, 9]` (`m = 3`), the longer is `long = [3, 8, 8, 15]` (`n = 4`).
`k = 4` is in range. Clamp: `lo = max(0, 4 - 4) = 0`, `hi = min(4, 3) = 3`.

| `lo` | `hi` | `taken` | `rest` | left/right short | left/right long | verdict |
| ---: | ---: | ---: | ---: | :--- | :--- | :--- |
| 0 | 3 | 1 | 3 | 1 / 4 | 8 / 15 | `8 > 4` → too few → `lo = 2` |
| 2 | 3 | 2 | 2 | 4 / 9 | 8 / 8 | valid |

At the valid cut, `kth = max(4, 8) = 8` and `nxt = min(9, 8) = 8`, so the
answer is `(8, 8)`.

**Trace `k = 7`, the last rank.** Clamp: `lo = max(0, 7 - 4) = 3`,
`hi = min(7, 3) = 3`, so there is exactly one candidate and the loop runs
once. `taken = 3`, `rest = 4`. `left_short = 9`, `right_short = +inf` (taken
`== m`), `left_long = 15`, `right_long = +inf` (rest `== n`). Both conditions
hold, so the cut is valid: `kth = max(9, 15) = 15`, `nxt = min(inf, inf) =
inf` → `None`. Answer `(15, None)`. Notice the clamp did the whole job here —
by the time the loop started there was only one legal cut left.

**Converting `inf` to `None` happens once, at the return.** It is the last
line for a reason: the infinities are an internal device for making the
comparisons uniform, and they must not leak into a contract that promises
integers or `None`. A caller who receives `float('inf')` will do arithmetic
with it and get a very confusing bug two functions away.

**The empty-list cases arrive through the clamp, not through a branch.** With
`short = []`, `m = 0`, so `hi = min(k, 0) = 0` and `lo = max(0, k - n)`, which
for a legal `k` is also 0. One candidate, `taken = 0`, both short-side reads
fall off their ends into infinities, and the answer comes straight from the
long list. No `if either list is empty` anywhere.

## Download and run

Download
[challenge-01-order-book-boundary-solution.py](./challenge-01-order-book-boundary-solution.py)
and run it:

```bash
python challenge-01-order-book-boundary-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `challenge-01-order-book-boundary.py`.

## Common bugs to catch

- **`IndexError: list index out of range` inside the loop.** You searched
  `[0, m]` instead of the clamped interval:

  ```text
  Traceback (most recent call last):
      left_long = long[rest - 1] if rest > 0 else -inf
                  ~~~~^^^^^^^^^^
  IndexError: list index out of range
  ```

  With `k = 7` and no clamp, `taken = 0` gives `rest = 7` on a four-element
  list. The `if rest > 0` guard only protects the left end; the right end is
  the clamp's job.

- **The program hangs.** You wrote `hi = taken` or `lo = taken` instead of
  stepping past. This loop is closed-interval, so both moving branches must
  exclude the midpoint. Press `Ctrl-C` and Python points at the guard:

  ```text
  Traceback (most recent call last):
    File "<string>", line 7, in <module>
      while lo <= hi:
            ^^^^^^^^
  KeyboardInterrupt
  ```

- **`([5, 5, 5], [5, 5], 3)` never returns, or returns `None`.** You used
  strict `<` in the validity test. Every comparison on that input is an
  equality, so a strict test calls the valid cut invalid and the loop runs out
  of interval. The invariant is `<=`.

- **`k = 7` returns `(15, inf)`.** You forgot to convert at the return. The
  sentinel leaked into the contract. `float('inf')` is not a delta, and the
  desk cannot do anything with it.

- **`([1, 2, 3], [10, 20, 30], 3)` returns `(3, None)` or crashes.** Your
  sentinel is a made-up big integer rather than a real infinity, or you assumed
  `taken > 0` and `rest > 0`. The disjoint-range inputs drive both counts to
  zero and to their maximum; they exist to break exactly this.

- **`k = 0` raises instead of returning `None`.** The range guard is missing or
  only checks the top end. `k` is 1-based, so both ends need a check, and both
  are legal input.

- **Answers are right but the depth is `log2(max(m, n))`.** You skipped the
  swap. Correct, and it misses the stated bound — which on this problem is part
  of the spec, not a nicety.

- **You produced the merge.** It passes every assert in the self-check and
  fails the requirement. If you write it as a scaffold to test against, keep it
  in the test and out of the answer — which is exactly what the cross-check at
  the bottom of the file does.

## Under the hood

<details>
<summary>Under the hood — the cost, the median wrapper, and why the crossing is guaranteed</summary>

**Cost, precisely.**

Time is `O(log(min(m, n)))`. The clamped interval is at most `min(m, n) + 1`
wide, and each iteration does four guarded reads and two comparisons, all
constant time, with no inner loop. Space is `O(1)`: `lo`, `hi`, `taken`,
`rest` and the four boundary values. The swap rebinds names rather than moving
data, so it is free.

The alternatives, honestly:

| Approach | Time | Space | Note |
| --- | --- | --- | --- |
| Merge both lists | `O(m + n)` | `O(m + n)` | the space is what actually hurts |
| Step a merge `k` times | `O(k)` | `O(1)` | fine for small `k`, and `k` can be 10⁷ |
| Bisect the cut | `O(log(min(m, n)))` | `O(1)` | independent of `k` entirely |

The middle row is worth knowing: if the desk only ever asked for the first
hundred ranks, walking a merge would be simpler and faster, and saying so is a
better answer than reciting the optimal one.

**Why the loop can never fall through.**

The `return None` after the loop is unreachable whenever `k` is in range, and
it is worth being able to say why. Inside the clamped interval, the first
condition is false at `lo` and the second is false at `hi` — that is exactly
what the clamp guarantees — and each is one-way in `taken`. So there is a
crossing point inside the interval, and a closed-interval bisection on a
one-way condition cannot step over it: every iteration keeps the crossing
inside `[lo, hi]`. If your loop *can* fall through, the clamp is wrong, and
that is where to look rather than at the branches.

**The median wrapper is four lines.**

The reason this contract returns a *pair* rather than a single value is that
the pair makes the even case free:

```python
def session_median(a: list[int], b: list[int]) -> float | None:
    """Return the median delta across both books, or None when both are empty."""
    total = len(a) + len(b)
    if total == 0:
        return None
    if total % 2:
        return float(book_boundary(a, b, (total + 1) // 2)[0])
    low, high = book_boundary(a, b, total // 2)
    return (low + high) / 2
```

Note what the wrapper does *not* need: a second search. The even-length median
is the mean of two adjacent ranks, and adjacent ranks are precisely what a
boundary is. Designing the return value so the common caller needs no extra
work is a small piece of API judgement worth naming in your write-up.
</details>

## Acceptance checklist

- [ ] `python challenge-01-order-book-boundary.py` prints the five report
      lines then `All checks passed.`
- [ ] The output matches the expected output character for character.
- [ ] You drew the cut and wrote the validity condition before writing code.
- [ ] You can state the monotonicity argument in one paragraph, out loud.
- [ ] The shorter list is the one searched, and the interval is clamped before
      the loop.
- [ ] The four boundary reads use explicit `if … else` with `±inf`.
- [ ] `inf` is converted to `None` exactly once, at the return.
- [ ] The cross-check against a plain merge passes on all five hundred
      generated pairs.
- [ ] Committed to Git with a message like
      `Add Week 5 challenge 1: merged book boundary`.

## Stretch

- **Add the median wrapper** from Under the hood and check it against
  `statistics.median(a + b)` on generated books.

  ```text
  a=[3, 8, 8, 15]  b=[1, 4, 9]   median 8.0   agrees
  a=[1, 2]         b=[3, 4]      median 2.5   agrees
  ```

  Then say in one sentence why the pair-returning contract made the even case
  free.

- **Return the rank of a value instead of the value of a rank.** The inverse
  question: given a delta, how many entries are at or below it?

  ```python
  def rank_of(venue_a: list[int], venue_b: list[int], delta: int) -> int:
      """Return how many deltas across both books are <= `delta`."""
      import bisect
      return bisect.bisect_right(venue_a, delta) + bisect.bisect_right(venue_b, delta)
  ```

  ```text
  rank_of(books, 8)  = 5
  rank_of(books, 7)  = 3
  ```

  Two lower-bound searches, no cut needed. Work out why the inverse is so much
  easier than the forward question — the answer is that here you are handed
  the value to compare, and there you had to invent one.

- **Generalise to three books.** Take a rank across three sorted reports. The
  cut idea does not extend cleanly, because now two counts are free instead of
  one. Sketch what you would do instead — a value-space search with a counting
  predicate, which is Exercise 4's shape — and note the complexity you would
  end up with. Recognising when a technique stops applying is worth as much as
  applying it.

When your boundary is right, move on to
[Challenge 2 — The Signal Mast Spacing](./challenge-02-signal-mast-spacing.md).
