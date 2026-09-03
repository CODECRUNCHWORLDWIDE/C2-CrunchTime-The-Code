# Challenge 1 — The Balanced Shift

> **Topic:** prefix sums plus a hash map carrying two payloads — turning a question about every window into a question about every position
> **Lecture:** [02 — The Hash Map Pattern](../lecture-notes/02-the-hash-map-pattern.md)
> **Difficulty:** Medium
> **Target time:** 2 hours
> **Why this one:** the *reformulation* is the discriminator. "The sum over a window" becomes "the difference of two running totals", and at that moment a question about windows turns into a lookup and the nested loop evaporates. Most candidates write the `O(n^2)` version and stall there. On top of that, this contract asks one map to remember two different things about each key, with two different update rules — which is exactly where a memorised solution comes apart.

## The Brief

Here is a trick you can do with a shopping receipt.

Write down the running total after every line. Now the cost of lines 3 through 7
is not something you have to add up — it is just *the running total after line 7
minus the running total after line 2*. Two numbers you already wrote down. You
never touch lines 3, 4, 5 or 6 at all.

Those running totals have a name: **prefix sums**. And once you have them, every
question about a stretch of the receipt becomes a question about two numbers.

That is the whole idea of this challenge.

A distribution warehouse logs, for each hour of operation, its **net pallet
movement**: pallets received minus pallets shipped. The number is negative on an
hour when more went out than came in.

A **shift window** is any contiguous, non-empty run of hours `net_moves[i..j]`,
inclusive at both ends. A window is **balanced against `target`** when its hours
sum to exactly `target`.

Return two things at once, as a tuple:

1. **How many** windows are balanced against `target`. Windows may overlap and
   may nest; every distinct `(i, j)` pair counts separately.
2. **Which window the floor manager should look at first** — the balanced window
   with the **smallest end hour `j`**. If several balanced windows end at that
   same hour, return the **shortest** of them, that is, the one with the largest
   start `i`.

If no window is balanced, return `(0, None)`.

Now watch the reformulation, because everything else follows from it. Write
`S[b]` for the total of the first `b` hours, with `S[0] = 0` standing for the
empty prefix — zero hours, zero movement. The window `net_moves[i..j]` sums to
`S[j+1] - S[i]`. So:

> "How many windows are balanced?" becomes
> **"how many pairs of prefix indices `a < b` satisfy `S[b] - S[a] = target`?"**

Rearrange that into a lookup: `S[a] = S[b] - target`. Sweep `b` from 1 to `n`,
and at each step ask how many *earlier* prefix indices carried the value
`S[b] - target`. That is a hash-map question, answered in `O(1)` average, and
the inner loop is gone.

Two consequences fall straight out of the rearrangement:

- The count contributed at step `b` is the **frequency** of `S[b] - target`
  among earlier prefixes. Sum those frequencies over all `b` and you have the
  total.
- The window reported at step `b` is `(a, b - 1)`. Its end `j = b - 1` grows
  with `b`, so the **first `b` at which any match occurs** gives the smallest
  `j` — and among the several `a` that may match at that `b`, the largest `a`
  gives the shortest window. So the map needs, per prefix value, both **how many
  times** it has occurred and **the most recent index** at which it did.

Two payloads, two update rules: the count accumulates, the index overwrites.

## Starter

Create `challenge-01-balanced-shifts.py` in your practice repo and paste this
in. Fill in the `TODO`.

```python
"""challenge-01-balanced-shifts.py — counting balanced shift windows.

Fill in the TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the function is correct. They also cross-check
every answer against a brute-force reference, so a passing run means your
fast solution agrees with the definition, not merely with a list of
expected values.
"""


def balanced_shifts(
    net_moves: list[int], target: int
) -> tuple[int, tuple[int, int] | None]:
    """Count balanced windows and name the one to look at first.

    Args:
        net_moves: Net pallet movement for each hour of operation. Negative
            on an hour when more went out than came in.
        target: The sum a window must hit to be balanced.

    Returns:
        (count, earliest) where count is how many contiguous non-empty
        windows sum to target, and earliest is the (i, j) of the balanced
        window with the smallest end j, breaking ties toward the largest
        start i. (0, None) when no window is balanced.
    """
    # TODO: seed the map with the empty prefix, then one pass.
    # Per hour, in this order: advance the running sum, QUERY the map,
    # then WRITE the map. The two payloads update differently.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    checks: list[tuple[list[int], int, tuple[int, tuple[int, int] | None]]] = [
        ([3, -1, 4, -3, 1, 2], 3, (5, (0, 0))),
        ([2, 0, 3], 3, (2, (2, 2))),
        ([0, 0, 0], 0, (6, (0, 0))),
        ([1, -1, 1, -1, 1], 1, (6, (0, 0))),
        ([10, -10, 10, -10], 0, (4, (0, 1))),
        ([-2, -3, 5, -5], -5, (3, (0, 1))),
        ([4, -7, 2], -7, (1, (1, 1))),
        ([0], 0, (1, (0, 0))),
        ([7], 7, (1, (0, 0))),
        ([3], 0, (0, None)),
        ([5, 5], 3, (0, None)),
        ([], 0, (0, None)),
    ]

    def brute_force(
        net_moves: list[int], target: int
    ) -> tuple[int, tuple[int, int] | None]:
        """Reference answer straight from the definition. O(n^2), obviously right."""
        windows = [
            (start, end)
            for start in range(len(net_moves))
            for end in range(start, len(net_moves))
            if sum(net_moves[start : end + 1]) == target
        ]
        if not windows:
            return (0, None)
        return (len(windows), min(windows, key=lambda w: (w[1], -w[0])))

    for net_moves, target, expected in checks:
        found = balanced_shifts(list(net_moves), target)
        assert found == expected, (net_moves, target, found, expected)
        assert found == brute_force(net_moves, target), (net_moves, target)
        count, earliest = found
        window = "none" if earliest is None else f"{earliest[0]}..{earliest[1]}"
        print(f"target {target:3d}  ->  {count:2d} balanced, first {window:>6}   {net_moves}")

    print("All checks passed.")
```

Three words before you start.

**Prefix sum.** The total of everything up to a point. `S[3]` is hours 0, 1 and
2 added up. There are `n + 1` of them, because `S[0] = 0` is the total of no
hours at all, and that one turns out to matter.

**Seed.** Putting something into the map *before* the loop starts. Here the seed
is the empty prefix: value 0, seen once, at prefix index 0. Without it, no window
that starts at hour 0 is ever found.

**Frequency.** How many times a value has been seen. Not whether — how many. The
difference is what makes this challenge `O(n)` rather than `O(n^2)`: when a
prefix value has occurred five times before, that one lookup contributes five
windows at once.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-02-complexity-and-hash-maps/challenges/challenge-01-balanced-shifts.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `balanced_shifts` returns a tuple `(count, earliest)` — both parts, always.
2. `count` counts every distinct `(i, j)` pair whose window sums to `target`.
   Overlapping and nested windows each count separately.
3. `earliest` is the balanced window with the smallest end `j`; among those, the
   one with the largest start `i`.
4. With no balanced window the answer is `(0, None)` — a real integer zero and a
   `None`, not `None` for the whole tuple.
5. Windows are non-empty. The empty window sums to 0 and is never counted.
6. It runs in `O(n)` time and `O(n)` space. The `O(n^2)` enumeration does not
   pass, even though the shipped self-check contains one as a reference.
7. Negative values and negative targets work.
8. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(net_moves) <= 200_000`.** Round-the-clock hourly logging is about
  8,800 hours a year, so this is roughly twenty-odd years of record. The bound
  rejects the double loop: enumerating every window is `n(n+1)/2`, about
  `2 x 10^10` sums, which will not finish. Name that number before you write
  anything — it is the reason the reformulation is worth two hours of your time.

- **`-1000 <= net_moves[h] <= 1000`.** **Values may be negative, and that is the
  point of the problem.** With negatives, the running sum is not monotonic, so
  you cannot grow a window and then shrink it from the left to restore an
  invariant — which is precisely why Week 3's sliding-window technique does not
  apply here and a hash map does. If this constraint read `0 <= net_moves[h]`,
  this would be a different problem in a different week.

- **`abs(target) <= 200_000_000`.** That is the largest magnitude any window sum
  can reach — 200,000 hours at 1000 each — so the bound is exactly "a target
  that is reachable, and no larger". Python integers are arbitrary precision, so
  there is nothing to guard here; say out loud that in a fixed-width language
  you would want 64-bit accumulators, because `2 x 10^8` fits comfortably in 32
  bits and it is the *prefix* sums getting there that you would have to check.

- **The map stores the most recent index per prefix value, not the earliest.**
  That is the opposite of what Exercise 1 wanted, and reversing it by reflex is
  the single most likely way to fail this challenge. It follows from the
  tie-break: at the first `b` that matches, the *largest* `a` gives the shortest
  window, and the largest `a` is the most recently recorded one.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python challenge-01-balanced-shifts-solution.py
target   3  ->   5 balanced, first   0..0   [3, -1, 4, -3, 1, 2]
target   3  ->   2 balanced, first   2..2   [2, 0, 3]
target   0  ->   6 balanced, first   0..0   [0, 0, 0]
target   1  ->   6 balanced, first   0..0   [1, -1, 1, -1, 1]
target   0  ->   4 balanced, first   0..1   [10, -10, 10, -10]
target  -5  ->   3 balanced, first   0..1   [-2, -3, 5, -5]
target  -7  ->   1 balanced, first   1..1   [4, -7, 2]
target   0  ->   1 balanced, first   0..0   [0]
target   7  ->   1 balanced, first   0..0   [7]
target   0  ->   0 balanced, first   none   [3]
target   3  ->   0 balanced, first   none   [5, 5]
target   0  ->   0 balanced, first   none   []
All checks passed.
```

Three rows deserve attention.

**`[2, 0, 3]` with target 3 gives `(2, (2, 2))`.** Two windows balance: `(1,2)`
which is `0 + 3`, and `(2,2)` which is `3`. **Both end at hour 2.** The tie-break
sends you to the larger start, so `(2, 2)`. This is the row that forces the
"most recent index, not earliest" rule into your design.

**`[0, 0, 0]` with target 0 gives `6`.** Every one of the six windows sums to
zero: `(0,0) (0,1) (0,2) (1,1) (1,2) (2,2)`. This is the degenerate case and it
catches a wrongly seeded map — a bad seed typically reports 3 here, or 10.

**`[1, -1, 1, -1, 1]` with target 1 gives `6`.** This is the row that punishes a
sliding window. A window-based solution grows until the sum reaches 1, then
tries to shrink — but shrinking past a `-1` *raises* the sum, so the invariant
it depends on never held in the first place.

## Steps

1. Create the file, paste the starter, and run it. Every case fails.
2. Before writing anything, work `[2, 0, 3]` with target 3 by hand on paper.
   Write the prefix sums, then the pairs that differ by 3, then which pair the
   tie-break picks. If you cannot do it on paper you cannot debug it in code.
3. Write the version that only counts. Seed the map with `{0: 1}` for now — a
   frequency and nothing else — advance, query, add. Run it and check the counts
   against the expected output, ignoring the window half.
4. Now widen the value to a tuple `(frequency, most_recent_index)` and set
   `earliest` at the first match. The count code does not change.
5. Run. All twelve cases should pass, and each one is also cross-checked against
   the brute-force reference, so a pass means you agree with the *definition*.
6. Break it on purpose three times, and read each failure: remove the seed
   (`[7]` with target 7 answers `(0, None)`); move the write above the query
   (`[0]` with target 0 answers `2`); store the earliest index instead of the
   most recent (`[2, 0, 3]` answers `(2, (1, 2))`). That last one is the
   important one, because eleven of the twelve cases still pass.
7. Write your own generator: random values in `[-3, 3]`, lengths up to 200,
   cross-checked against the reference. Twenty minutes there finds the tie-break
   bugs that hand-written cases miss.

## The Solution

```python
"""challenge-01-balanced-shifts-solution.py — counting balanced shift windows.

A window's sum is the difference of two prefix sums, so "which windows sum to
the target" becomes "which pairs of prefix sums differ by the target" — and
that is a lookup, not a search. One map from prefix value to (how many times
it has occurred, the most recent index it occurred at) answers both halves of
the question in one pass.

Time: O(n) — one pass, one addition, one lookup and one write per hour.
Space: O(n) — the map holds at most n + 1 distinct prefix values.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""


def balanced_shifts(
    net_moves: list[int], target: int
) -> tuple[int, tuple[int, int] | None]:
    """Count balanced windows and name the one to look at first.

    Args:
        net_moves: Net pallet movement for each hour of operation. Negative
            on an hour when more went out than came in.
        target: The sum a window must hit to be balanced.

    Returns:
        (count, earliest) where count is how many contiguous non-empty
        windows sum to target, and earliest is the (i, j) of the balanced
        window with the smallest end j, breaking ties toward the largest
        start i. (0, None) when no window is balanced.
    """
    # The empty prefix has value 0, has occurred once, and lives at index 0.
    seen: dict[int, tuple[int, int]] = {0: (1, 0)}
    running = 0
    count = 0
    earliest: tuple[int, int] | None = None

    for end, moved in enumerate(net_moves):
        running += moved
        needed = running - target
        if needed in seen:
            frequency, most_recent = seen[needed]
            count += frequency
            if earliest is None:
                earliest = (most_recent, end)
        frequency, _ = seen.get(running, (0, 0))
        seen[running] = (frequency + 1, end + 1)

    return (count, earliest)


# ---- Self-check ----
if __name__ == "__main__":
    checks: list[tuple[list[int], int, tuple[int, tuple[int, int] | None]]] = [
        ([3, -1, 4, -3, 1, 2], 3, (5, (0, 0))),
        ([2, 0, 3], 3, (2, (2, 2))),
        ([0, 0, 0], 0, (6, (0, 0))),
        ([1, -1, 1, -1, 1], 1, (6, (0, 0))),
        ([10, -10, 10, -10], 0, (4, (0, 1))),
        ([-2, -3, 5, -5], -5, (3, (0, 1))),
        ([4, -7, 2], -7, (1, (1, 1))),
        ([0], 0, (1, (0, 0))),
        ([7], 7, (1, (0, 0))),
        ([3], 0, (0, None)),
        ([5, 5], 3, (0, None)),
        ([], 0, (0, None)),
    ]

    def brute_force(
        net_moves: list[int], target: int
    ) -> tuple[int, tuple[int, int] | None]:
        """Reference answer straight from the definition. O(n^2), obviously right."""
        windows = [
            (start, end)
            for start in range(len(net_moves))
            for end in range(start, len(net_moves))
            if sum(net_moves[start : end + 1]) == target
        ]
        if not windows:
            return (0, None)
        return (len(windows), min(windows, key=lambda w: (w[1], -w[0])))

    for net_moves, target, expected in checks:
        found = balanced_shifts(list(net_moves), target)
        assert found == expected, (net_moves, target, found, expected)
        assert found == brute_force(net_moves, target), (net_moves, target)
        count, earliest = found
        window = "none" if earliest is None else f"{earliest[0]}..{earliest[1]}"
        print(f"target {target:3d}  ->  {count:2d} balanced, first {window:>6}   {net_moves}")

    print("All checks passed.")
```

**The seed is one line and half the correctness.**

```python
seen: dict[int, tuple[int, int]] = {0: (1, 0)}
```

Read it as English: the empty prefix has value 0, it has occurred once, and it
lives at prefix index 0. That entry is what lets a window starting at hour 0 be
found, because such a window's `a` *is* the empty prefix. Delete this line and
`[7]` with target 7 answers `(0, None)` — the single-hour window that is the
entire answer becomes invisible. Seed with index `-1` instead of `0` and you
report windows starting at hour `-1`.

**The order inside the loop is load-bearing: advance, query, write.**

```python
running += moved       # advance
needed = running - target
if needed in seen: ... # query
seen[running] = ...    # write
```

Query before write, or the current prefix matches itself. With `target = 0` and
input `[0]`, writing first means `running` is already in the map when you look
for `running - 0`, and the count comes out as 2 instead of 1. Same rule as
Exercise 1 — ask the structure before you tell it anything — and it is the third
time this week it has mattered.

**Two payloads, two update rules, in one line.**

```python
frequency, _ = seen.get(running, (0, 0))
seen[running] = (frequency + 1, end + 1)
```

The frequency **accumulates**: `+ 1` on every occurrence. The index
**overwrites**: it is always set to the current prefix index, discarding the
previous one. Getting one of the two rules right and the other wrong is the
signature failure of this challenge, and it is quiet — if you accumulate the
index or overwrite the frequency, most cases still pass.

**Why the frequency, and not just membership?** Because one lookup can be worth
many windows. When `needed` has occurred five times among the earlier prefixes,
five different `a` values pair with the current `b`, and all five windows are
balanced. Adding `frequency` in one step is what keeps this linear; discovering
those five by looking for them would put the inner loop back.

**Why the most recent index, and not the earliest?** The tie-break asks for the
*shortest* window among those ending earliest. The window is `(a, b - 1)`, so a
larger `a` is a shorter window, and the largest `a` recorded so far is the most
recent one. Store the earliest instead and every count stays correct while the
returned window is wrong — the hardest class of bug on this page, because
eleven of twelve tests still pass.

**`earliest` is set once and never updated.** The loop walks `b` upward, and
`j = b - 1` grows with `b`, so the *first* `b` that matches gives the smallest
possible `j`. Guarding with `if earliest is None` freezes it there. Update it on
every match instead and you end up reporting the last balanced window rather
than the first.

**The empty window never gets counted, and it is worth checking that on paper.**
On `[]` the seed exists but the loop never runs, so `count` stays at 0 and
`earliest` stays `None`. On any input, the seed is only ever read as an `a`, and
an `a` always pairs with a `b > a`, which is a window of at least one hour. The
empty prefix is a bookkeeping device, not a window.

**The cost, said properly.** *Time `O(n)`*: one pass, and each hour does one
addition, one map lookup and one map write, all `O(1)` average. *Space `O(n)`*:
the map holds at most `n + 1` distinct prefix values. *Best, average and worst
are all `O(n)`*: there is no early exit, because the count needs every hour even
after the window has been found. *Tradeoff*: the `O(n^2)` enumeration is `O(1)`
space and fails the time bound — a real memory win that this constraint does not
let you take. There is no sliding-window alternative at all, because negatives
break the monotonic invariant a window relies on. *Improvement*: none; every
hour must be read, so `O(n)` is the floor.

**The worked trace, following the map rather than the answer.** `seen` maps a
prefix value to `(frequency, most recent index)`.

| step | `moved` | `running` | `needed` | found | `count` | `earliest` | `seen` after |
|-----:|--------:|----------:|---------:|-------|--------:|------------|--------------|
| seed |         | 0         |          |       | 0       | `None`     | `{0: (1, 0)}` |
| b=1  | 2       | 2         | -1       | no    | 0       | `None`     | `{0: (1,0), 2: (1,1)}` |
| b=2  | 0       | 2         | -1       | no    | 0       | `None`     | `{0: (1,0), 2: (2,2)}` |
| b=3  | 3       | 5         | 2        | `(2, 2)` | 2    | `(2, 2)`   | `{0: (1,0), 2: (2,2), 5: (1,3)}` |

At `b = 3` the map says prefix value 2 has been seen **twice**, most recently at
index **2**. The frequency 2 adds both balanced windows in one step — that is
the whole reason this is `O(n)`. The index 2 gives the window
`(2, b - 1) = (2, 2)`, the shorter of the two ending at hour 2, exactly as the
tie-break requires.

Look at what happened at `b = 2`. Prefix value 2 was already in the map from
`b = 1`, and the write **overwrote** its index from 1 to 2 while
**incrementing** its frequency from 1 to 2. Two payloads, two rules, in one
line. Had you kept the earliest index, step 3 would have reported `(1, 2)` — a
balanced window, correctly counted, and the wrong one to return.

## Download and run

Download
[challenge-01-balanced-shifts-solution.py](./challenge-01-balanced-shifts-solution.py)
and run it:

```bash
python challenge-01-balanced-shifts-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `challenge-01-balanced-shifts.py`. Note that the shipped file carries
the brute-force reference too — every answer is checked against the definition
as well as against a table of expected values, which is a habit worth stealing
for your own tests.

## Common bugs to catch

- **`AssertionError` on `([7], 7, ...)`, got `(0, None)`.** No seed.

  ```text
  Traceback (most recent call last):
      assert found == expected, (net_moves, target, found, expected)
             ^^^^^^^^^^^^^^^^^
  AssertionError: ([7], 7, (0, None), (1, (0, 0)))
  ```

  Without `{0: (1, 0)}` in the map before the loop, no window that starts at
  hour 0 is ever found — and on a one-hour log, that is every window there is.
  This is the smallest input that catches a missing seed, so put it in your
  tests first.

- **`AssertionError` on `([0], 0, ...)`, got `(2, (0, 0))`.** You wrote to the
  map before you queried it, so the freshly written prefix matched itself.
  Advance, query, write — in that order.

- **`AssertionError` on `([2, 0, 3], 3, ...)`, got `(2, (1, 2))`.** You stored
  the earliest index per prefix value instead of the most recent:

  ```text
  Traceback (most recent call last):
      assert found == expected, (net_moves, target, found, expected)
             ^^^^^^^^^^^^^^^^^
  AssertionError: ([2, 0, 3], 3, (2, (1, 2)), (2, (2, 2)))
  ```

  The count is right, the window is a genuinely balanced window, and it is still
  the wrong answer. Eleven of the twelve checks pass with this bug in place,
  which is why this specific case exists.

- **`AssertionError` on `([0, 0, 0], 0, ...)`, got `(3, (0, 0))`.** You set the
  frequency to 1 on every write instead of incrementing it. The count of nested
  windows collapses to a count of distinct prefix values.

- **`earliest` reports the last window instead of the first.** You updated it on
  every match. It must be set exactly once, at the first `b` that matches — guard
  with `if earliest is None`.

- **`TypeError: cannot unpack non-sequence int`.** You started with a plain
  frequency map and widened it halfway:

  ```text
  Traceback (most recent call last):
      frequency, most_recent = seen[needed]
      ^^^^^^^^^^^^^^^^^^^^^^
  TypeError: cannot unpack non-sequence int
  ```

  One of your writes still stores a bare integer. Widen the seed and every write
  together, or none of them.

- **Reaching for a sliding window.** If you find yourself writing
  `while window_sum > target: shrink()`, stop and re-read the constraint on
  negative values. Growing and shrinking depends on the sum moving in one
  direction as the window grows, and with negatives it does not. This problem is
  hash-map territory *because* of the negatives.

- **Counting the empty window.** On `([], 0)` the seed exists and the loop never
  runs, so the count must stay at 0. It is easy to write a version that reports
  1 by treating the seed as a window in its own right. Verify it on paper.

## Under the hood

<details>
<summary>Under the hood — why prefix sums turn window questions into lookups, and four problems this same map solves</summary>

**The identity, stated once and used forever.**

```text
sum(net_moves[i..j]) == S[j+1] - S[i]
```

That is all a prefix sum is. It costs `O(n)` to build the totals and then every
window sum is one subtraction. The reason it is such a high-yield pattern is
that it converts a question about `O(n^2)` windows into a question about `O(n)`
positions, and questions about positions are what hash maps are good at.

The subtlety worth internalising is the off-by-one. There are `n` hours and
`n + 1` prefixes, because the empty prefix is real. Nearly every bug in this
family is a confusion between "hour index" and "prefix index", which is why the
solution names the loop variable `end` (an hour) and writes `end + 1` (a
prefix) when it stores.

**Why you never build the array.** You could compute `S` as a list and then
sweep it. The solution keeps a single `running` integer instead, because the
sweep only ever needs the current prefix and the map of earlier ones. Same
complexity class, `O(1)` instead of `O(n)` for that particular structure, and
one fewer thing to index wrongly.

**Four problems that are this one with a line changed.** Once the reformulation
is reflexive, this whole family opens up:

- *Count windows whose sum is a multiple of `k`.* Same shape, keyed on
  `running % k` instead of on `running`. Two prefixes with the same remainder
  bracket a window divisible by `k`.
- *Find the longest window with a given sum.* Same map, but store the
  **earliest** index per prefix value rather than the most recent, and track a
  maximum instead of a count. Note how the payload rule flips — that is not a
  coincidence, it falls straight out of whether you want the window long or
  short.
- *Count windows containing equal numbers of two categories.* Map one category
  to `+1` and the other to `-1`, and it is this problem with `target = 0`.
- *Locate the point where a running balance first repeats.* The same map,
  queried for presence instead of frequency.

Every one of those is this challenge with one line different. It is worth
FRAMEing this problem twice: once now, and once at the end of Week 11, when you
can compare the prefix-sum framing against a dynamic-programming one and say
which you would reach for and why.

**Where the memory actually goes, and when it bites.** The map holds one entry
per *distinct prefix value*. On a log that oscillates — `[1, -1, 1, -1, ...]` —
there are only two distinct prefix values however long the log is, and the map
stays tiny. On a log of all positive values every prefix is distinct and the map
holds `n + 1` entries. So `O(n)` is an honest upper bound and the typical case
can be far better. Saying "`O(n)` worst case, and in practice `O(d)` for `d`
distinct prefix values" is the more informative sentence.

**Fixed-width overflow, the thing Python hides from you.** The constraint caps
`abs(target)` at `2 x 10^8`, which fits in a 32-bit integer with room to spare.
The prefix sums get there too. But in C or Java you would want to say out loud
that the accumulator should be 64-bit anyway, because the *intermediate* running
sum is what grows, and a log that swings hard in both directions can visit large
magnitudes on its way to a small answer. Python's integers grow to fit, so this
costs you nothing here and one sentence in an interview.

</details>

## Acceptance checklist

- [ ] `python challenge-01-balanced-shifts.py` prints twelve rows then `All checks passed.`
- [ ] The rows match the expected output character for character.
- [ ] The map is seeded with the empty prefix before the loop.
- [ ] The loop order is advance, query, write.
- [ ] The frequency accumulates and the index overwrites.
- [ ] `earliest` is assigned exactly once.
- [ ] Every answer also agrees with the brute-force reference in the self-check.
- [ ] Your solution is `O(n)` time and `O(n)` space, with exactly one loop.
- [ ] You can explain in one paragraph why the map stores the most recent index,
      and what breaks if it stores the earliest.
- [ ] You wrote a randomised generator that cross-checks against the reference.
- [ ] Committed to Git with a message like `Add Week 2 challenge 1: balanced shifts`.

## Stretch

- **Find the longest balanced window instead of the earliest-ending one, and
  watch the payload rule flip.**

  ```python
  def longest_balanced_shift(net_moves: list[int], target: int) -> tuple[int, int] | None:
      """Return the (i, j) of the longest balanced window, ties toward the smaller i."""
      first_at: dict[int, int] = {0: 0}
      running = 0
      best: tuple[int, int] | None = None
      for end, moved in enumerate(net_moves):
          running += moved
          needed = running - target
          if needed in first_at:
              window = (first_at[needed], end)
              if best is None or (end - window[0]) > (best[1] - best[0]):
                  best = window
          if running not in first_at:
              first_at[running] = end + 1
      return best

  print(longest_balanced_shift([3, -1, 4, -3, 1, 2], 3))
  print(longest_balanced_shift([2, 0, 3], 3))
  print(longest_balanced_shift([5, 5], 3))
  ```

  ```text
  (1, 5)
  (1, 2)
  None
  ```

  One payload, not two, and the rule inverted: keep the **earliest** index per
  prefix value, because a smaller `a` is a longer window. On `[2, 0, 3]` the
  answer is now `(1, 2)` — the very window the main solution deliberately
  rejects. Same map, opposite tie-break, opposite update rule. If you can say
  why in one sentence, you understand this family rather than this problem.

- **Count windows whose sum is a multiple of `k`, keyed on the remainder.**

  ```python
  def windows_divisible_by(net_moves: list[int], k: int) -> int:
      """Return how many non-empty windows have a sum divisible by k."""
      counts: dict[int, int] = {0: 1}
      running = 0
      total = 0
      for moved in net_moves:
          running += moved
          remainder = running % k
          total += counts.get(remainder, 0)
          counts[remainder] = counts.get(remainder, 0) + 1
      return total

  print(windows_divisible_by([3, -1, 4, -3, 1, 2], 3))
  print(windows_divisible_by([5, 5, 5], 5))
  ```

  ```text
  5
  6
  ```

  The key changed from `running` to `running % k` and nothing else did. Python's
  `%` returns a non-negative result for a positive `k` even when `running` is
  negative, which is exactly what you want here and is *not* what C or Java do —
  a genuine language difference worth knowing before it costs you an hour.

- **Cross-check against a generator, which is how you should have tested it
  anyway.**

  ```python
  import random

  def brute(net_moves: list[int], target: int) -> tuple[int, tuple[int, int] | None]:
      windows = [(i, j) for i in range(len(net_moves)) for j in range(i, len(net_moves))
                 if sum(net_moves[i:j + 1]) == target]
      if not windows:
          return (0, None)
      return (len(windows), min(windows, key=lambda w: (w[1], -w[0])))

  rng = random.Random(20260226)
  mismatches = 0
  for _ in range(400):
      log = [rng.randint(-3, 3) for _ in range(rng.randint(0, 40))]
      target = rng.randint(-4, 4)
      if balanced_shifts(list(log), target) != brute(log, target):
          mismatches += 1
  print(f"{mismatches} mismatches over 400 random logs")
  ```

  ```text
  0 mismatches over 400 random logs
  ```

  A brute-force reference that is obviously correct and obviously too slow is
  the perfect oracle. Small random inputs find tie-break bugs that hand-written
  cases miss, because you cannot write a hand case for a rule you have
  misunderstood.
Next: [Challenge 2 — The Texture Residency Board](./challenge-02-residency-board.md).
