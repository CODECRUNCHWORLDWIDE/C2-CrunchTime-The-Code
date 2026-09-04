# Homework Problem 3 — The Ridge Line

> **Topic:** halving an **unsorted** sequence, using a local rule that guarantees the half you keep still contains an answer
> **Lecture:** [01 — The Binary-Search Template](../lecture-notes/01-the-binary-search-template.md)
> **Difficulty:** Medium
> **Target time:** 40 minutes
> **Why this one:** every binary search so far leaned on the data being sorted. This one does not, and it still runs in about twenty reads on a million stations. It is the cheapest possible demonstration that bisection needs a *rule that eliminates half*, not a sorted list — and it is the structural warm-up for [Challenge 1](../challenges/challenge-01-order-book-boundary.md), where you have to invent the rule yourself.

## The Brief

A survey drone flies in a straight line and records the ground height at
evenly spaced **stations**. The post-processing throws away flat runs, so no
two neighbouring stations ever record the same height.

A **ridge** is a station strictly higher than the station on its left and the
station on its right. Off either end of the line there is nothing at all, so
treat the ground beyond the ends as infinitely low — which means the first
station only has to beat its right-hand neighbour, and the last only has to
beat its left-hand one.

```
station:    0    1    2    3    4    5    6
height:    12   30   25   41   55   48    9
                 ^ridge              ^ridge
```

Two ridges there, and **either one is a correct answer**. That is a real part
of the contract, not sloppiness: the surveyor wants somewhere to put a mast,
and any local high point will do.

Now the interesting part. That list is not sorted, so there is no value to
bisect on. But there is still a rule that throws away half the stations after
reading one of them.

Stand at any station and look right. If the ground is **rising** — the next
station is higher — then walk that way. Either you keep rising until the line
ends, in which case that last station is a ridge, or you eventually stop
rising, and the station where you stop is a ridge. Either way, **a ridge
exists somewhere to the right**, so everything to the left can go.

If the ground is falling instead, the mirror argument says a ridge exists at
this station or to its left.

One read, half the stations gone. That is bisection, on data with no order in
it at all.

Return the ridge as a pair, `(index, height)`. Return `None` for an empty
line.

Two contract decisions:

- A **single-station** line is a ridge. Both its neighbours are off the end,
  and off the end is infinitely low.
- The return is a pair, not a bare index. Reading the height back out is what
  stops you returning a station you never actually verified.

## Starter

Save this as `problem-03-ridge-line.py` and fill in every `TODO`.

```python
"""problem-03-ridge-line.py — find a ridge on an unsorted transect.

Bisection without a sorted sequence: the rule that halves the line is
"the ground is still rising here".

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

# ---- Given data ----
TRANSECT: list[int] = [12, 30, 25, 41, 55, 48, 9]


# ---- Your task ----
def find_ridge(elevations: list[int]) -> tuple[int, int] | None:
    """Return a station that is strictly higher than both its neighbours.

    Args:
        elevations: Ground heights at evenly spaced stations. Adjacent
            stations never record the same height.

    Returns:
        (index, elevation) for some ridge, or None for an empty transect.
        The ground off either end counts as infinitely low.
    """
    # TODO: guard the empty line
    # TODO: half-open shape with hi = len(elevations) - 1
    # TODO: compare elevations[mid] against elevations[mid + 1], nothing else
    # TODO: no equality test and no early return — this converges on lo == hi
    ...


def is_ridge(elevations: list[int], index: int) -> bool:
    """Return True when the station at `index` beats both its neighbours."""
    # TODO: off the ends counts as infinitely low, so use float("-inf")
    ...


# ---- Self-check ----
if __name__ == "__main__":
    for transect in ([12, 30, 25, 41, 55, 48, 9], [8, 5, 3], [3, 5, 8], [7]):
        print(f"{transect} -> {find_ridge(transect)}")

    for transect in (
        TRANSECT,
        [3, 8, 5],
        [8, 5, 3],
        [3, 5, 8],
        [4, 9],
        [9, 4],
        [7],
        [-120, -45, -300],
    ):
        found = find_ridge(transect)
        assert found is not None
        index, elevation = found
        assert transect[index] == elevation
        assert is_ridge(transect, index), (transect, found)
    assert find_ridge([]) is None
    assert TRANSECT[0] == 12  # the transect was never reordered
    print("All checks passed.")
```

One idea you need before you start, and it is a subtle one.

**The rule is weaker than monotonicity, and that is fine.** "The ground falls
here" is *not* a one-way property — along a real line it flips back and forth
many times. What the argument gives you is something weaker and completely
sufficient: **whichever half you keep is guaranteed to still contain a
ridge**. Bisection does not actually require a single flip; it requires that
discarding half never discards every answer. Being able to state that
distinction is what this problem is really drilling, and it is why it warms you
up for the challenge, where the property genuinely is one-way and you have to
prove it.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-05-binary-search/homework/problem-03-ridge-line.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `find_ridge(elevations)` returns `(index, elevation)` for a station strictly
   higher than both its neighbours, treating off-the-end as infinitely low.
2. It returns `None` for an empty line, without indexing anything.
3. It reads about `log2(len(elevations))` stations. No scan, no `max`.
4. `is_ridge(elevations, index)` returns whether a station really is a ridge,
   and uses `float("-inf")` for the off-the-end neighbours.
5. Your tests assert the **ridge property**, never a fixed index. A test that
   hard-codes `(4, 55)` for the seven-station line is marked down even though
   it passes.
6. The loop compares `elevations[mid]` with `elevations[mid + 1]` and nothing
   else. No comparison against zero anywhere.
7. The search is half-open with `hi = len(elevations) - 1`, and it converges on
   `lo == hi` with no early return.
8. Both functions keep their type hints and docstrings.

## Constraints

- **`0 <= len(elevations) <= 1_000_000`.** A million stations is a long line,
  and a linear scan for the highest point would read every one of them. A
  ridge — *any* ridge — is reachable in about twenty reads. That gap is what
  makes `O(n)` unacceptable here and `O(log n)` the requirement.

- **`-500 <= elevations[i] <= 9_000`.** Heights are **signed**: the line can run
  below sea level. This is the bound that catches a solution seeding a running
  maximum at `0`, and it is why the off-the-end neighbours must be a real
  infinity rather than a number you picked.

- **Neighbouring stations always differ.** This is what makes the rule
  well-defined: at any midpoint with a right-hand neighbour, the ground is
  strictly rising or strictly falling, never level, so "keep climbing" always
  has a direction to point. Allow equal neighbours and a plateau gives the rule
  nothing to say, and the guarantee that a ridge survives in the half you keep
  quietly fails.

- **Any ridge is a correct answer.** Several stations may qualify, and the
  contract does not name one. That is why the tests have to assert the property
  rather than an index — and writing property assertions instead of equality
  assertions is itself a graded skill here. You will need it again in Week 12.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-03-ridge-line.py
[12, 30, 25, 41, 55, 48, 9] -> (4, 55)
[8, 5, 3] -> (0, 8)
[3, 5, 8] -> (2, 8)
[7] -> (0, 7)
All checks passed.
```

The first line has two ridges — station 1 at 30, and station 4 at 55 — and the
uphill rule happens to land on the second. Both are correct. If your solution
prints `(1, 30)` there, it is not wrong; it is a different valid answer, which
is exactly why the checks below the printout test the property instead of the
number.

Lines two and three are the mirror pair. On strictly falling ground the first
station wins, because there is nothing to its left; on strictly rising ground
the last station wins, because there is nothing to its right. A loop that
never lets `lo` reach the end fails the third case.

## Steps

1. Save the starter and run it. Both functions return `Ellipsis`, so the first
   assert about `found is not None` fails. Expected.
2. Write `is_ridge` first, even though the search does not use it. It is what
   your tests will check, and writing the property down makes the search
   easier to reason about.
3. Guard the empty line on the first line of `find_ridge`.
4. Set `lo, hi = 0, len(elevations) - 1` and loop `while lo < hi`.
5. The body is one comparison. If `elevations[mid] < elevations[mid + 1]`, the
   ground is rising, so a ridge lies strictly to the right: `lo = mid + 1`.
   Otherwise it is falling here, so `mid` itself might be the ridge:
   `hi = mid`.
6. After the loop `lo == hi`, and that station is a ridge. Return
   `(lo, elevations[lo])`.
7. Convince yourself `mid + 1` is always a legal index inside the loop. It is,
   and the reason is worth stating: the guard is `lo < hi`, and the rounded-down
   midpoint of a non-empty interval is always strictly less than `hi`.
8. Run it, then hand-trace `[3, 5, 8]` and `[8, 5, 3]` and check both endpoints
   are reachable.

## The Solution

```python
"""problem-03-ridge-line-solution.py - find a ridge on an unsorted transect.

Bisection without a sorted sequence. The rule that halves the search is not
"the target is bigger than the midpoint" but "the ground is still rising
here, so a ridge lies somewhere to the right".

The self-checks at the bottom are the starter's, unchanged. They assert the
RIDGE PROPERTY rather than a fixed index, because a transect may hold
several ridges and any of them is a correct answer. When they all pass the
file prints "All checks passed."
"""

# ---- Given data ----
TRANSECT: list[int] = [12, 30, 25, 41, 55, 48, 9]


# ---- Your task ----
def find_ridge(elevations: list[int]) -> tuple[int, int] | None:
    """Return a station that is strictly higher than both its neighbours.

    Args:
        elevations: Ground heights at evenly spaced stations. Adjacent
            stations never record the same height.

    Returns:
        (index, elevation) for some ridge, or None for an empty transect.
        The ground off either end counts as infinitely low.
    """
    if not elevations:
        return None

    lo, hi = 0, len(elevations) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if elevations[mid] < elevations[mid + 1]:
            lo = mid + 1  # still climbing, so a ridge lies to the right
        else:
            hi = mid  # falling here, so mid or something left of it is a ridge
    return lo, elevations[lo]


def is_ridge(elevations: list[int], index: int) -> bool:
    """Return True when the station at `index` beats both its neighbours."""
    left = elevations[index - 1] if index > 0 else float("-inf")
    right = elevations[index + 1] if index + 1 < len(elevations) else float("-inf")
    return left < elevations[index] > right


# ---- Self-check ----
if __name__ == "__main__":
    for transect in ([12, 30, 25, 41, 55, 48, 9], [8, 5, 3], [3, 5, 8], [7]):
        print(f"{transect} -> {find_ridge(transect)}")

    for transect in (
        TRANSECT,
        [3, 8, 5],
        [8, 5, 3],
        [3, 5, 8],
        [4, 9],
        [9, 4],
        [7],
        [-120, -45, -300],
    ):
        found = find_ridge(transect)
        assert found is not None
        index, elevation = found
        assert transect[index] == elevation
        assert is_ridge(transect, index), (transect, found)
    assert find_ridge([]) is None
    assert TRANSECT[0] == 12  # the transect was never reordered
    print("All checks passed.")
```

**The invariant is the whole proof, and it is one sentence.** *The interval
`[lo, hi]` always contains at least one ridge.* It is true at the start, because
the whole line contains one — the highest station is always a ridge, and there
is always a highest station. And each iteration preserves it: if the ground
rises at `mid`, then walking right from `mid + 1` must eventually stop rising
or hit the end, and either way that gives a ridge inside `[mid + 1, hi]`. If
the ground falls at `mid`, the mirror argument puts a ridge inside `[lo, mid]`.
When the interval narrows to one station, that station is the ridge.

**Note what is *not* claimed.** The predicate "the ground falls at station
`i`" is not one-way — it flips back and forth all along a real line. Bisection
does not need it to be one-way. It needs the weaker guarantee that the half you
keep still holds an answer, which is what the invariant states. Say that
distinction out loud; on the challenge the property genuinely is one-way, and
knowing which situation you are in is the difference between a proof and a
hope.

**`hi = mid`, not `mid - 1`, because `mid` is still a candidate.** When the
ground falls at `mid`, `mid` itself may be the ridge — its left neighbour has
not been examined. Excluding it loses the answer on `[9, 4]`, where station 0
is the only ridge there is.

**`mid + 1` can never run off the end.** Inside the loop, `lo < hi`, and
`mid = lo + (hi - lo) // 2` rounds down, so `mid < hi <= len - 1`. Therefore
`mid + 1 <= hi`, always a legal index. That is the reason there is no bounds
check in the body, and it is worth being able to state rather than trusting.

**There is no equality test and no early return.** Like the wrap search in
[Exercise 3](../exercises/exercise-03-ring-buffer-probe.md), this loop
converges on a boundary rather than hunting a value. Every iteration reads one
station, and the answer arrives when the interval closes.

**A single station is a ridge, and it costs no code.** With one station,
`lo == hi == 0` before the loop starts, the loop never runs, and the answer is
station 0 — correct, because both of its neighbours are off the end and off
the end is infinitely low. The empty line is the only case that needs a branch.

**`float("-inf")` in `is_ridge` is not decoration.** Heights run to `-500`,
so any real number you might pick as an off-the-end sentinel is a height some
station could record. The infinity is smaller than every one of them, by
definition, and it is why `[-120, -45, -300]` — an entirely below-sea-level
line — comes out right.

## Run it

Copy the worked answer on this page into `problem-03-ridge-line.py` and run it:

```bash
python problem-03-ridge-line.py
```

It is the same program you are writing, under a name that will not collide
with your own `problem-03-ridge-line.py`.

## Common bugs to catch

- **`IndexError: list index out of range` on the empty line.** You reached for
  `elevations[0]` or built the interval before guarding:

  ```text
  Traceback (most recent call last):
      lo, hi = 0, len(elevations) - 1
      ...
      if elevations[mid] < elevations[mid + 1]:
         ~~~~~~~~~~^^^^^
  IndexError: list index out of range
  ```

  With an empty list `hi` is `-1`, so `lo < hi` is false and the loop never
  runs — but the `return elevations[lo]` afterwards still fires. Guard the
  empty case first and return `None`.

- **`[3, 5, 8]` returns `(1, 5)`.** You wrote `hi = mid - 1` on the falling
  branch, or you compared against `elevations[mid - 1]` instead of
  `elevations[mid + 1]`. On strictly rising ground the answer is the *last*
  station, and a loop that cannot reach the end will never find it.

- **`[9, 4]` returns `(1, 4)` and `is_ridge` says `False`.** You wrote
  `lo = mid` on the falling branch and `hi = mid - 1` on the rising one — the
  two rules swapped. Read the argument again: rising means go right, falling
  means stay.

- **The program hangs.** You wrote `lo = mid` on the rising branch. With
  `lo = 0, hi = 1`, `mid` is `0`, and `lo = mid` changes nothing. The rising
  branch must exclude `mid`, because the comparison has just proved `mid` is
  not the answer — its right-hand neighbour is higher.

- **`[-120, -45, -300]` comes back as `None` or as the wrong station.** You
  compared heights against `0` somewhere, or used `0` as the off-the-end
  sentinel. The whole line is below sea level, and that is legal input.

- **Your test says `assert find_ridge(TRANSECT) == (4, 55)`.** It passes
  against this solution and fails against an equally correct one — for
  instance, a version that scans from the left and returns `(1, 30)`. When a
  contract says "any", the test asserts the property. This is graded.

- **You returned a bare index.** The contract asks for a pair. Reading the
  height back out is a cheap way of proving to yourself that you looked at the
  station you are reporting.

## Under the hood

<details>
<summary>Under the hood — why a ridge always exists, and the two-dimensional version</summary>

**A ridge always exists, and the proof is two lines.**

Take the highest station on the line — there is always at least one, since the
line is finite and non-empty. Both of its neighbours are no higher than it, and
neighbouring stations are never equal, so both are strictly lower. Off-the-end
neighbours are infinitely low, so the argument holds at the ends too.
Therefore the highest station is a ridge, so at least one ridge exists.

This matters for more than tidiness. It is what makes the invariant true at
the start, and it is what lets the function promise a non-`None` answer for
every non-empty line. A search that can find something is much easier to reason
about than one that might not.

**Finding *the* highest station is genuinely `O(n)`.**

Worth being precise about what the logarithm bought and what it did not. Any
*ridge* takes about twenty reads. The *global maximum* takes a million, because
you cannot rule out an unseen station being higher without looking at it — no
local rule can eliminate half the line when the question is global. The
contract asking for "a ridge" rather than "the peak" is not a softening; it is
the difference between a logarithmic problem and a linear one, and noticing
which of the two a prompt is asking for is a Recognise-step skill.

**The two-dimensional version, and why it is much harder.**

Give the drone a grid instead of a line and ask for a cell strictly higher than
all four of its neighbours. The obvious extension — bisect on the middle row,
then the middle column — does not work, because the argument that a peak
survives in the half you keep breaks down. The known solution bisects on a
column, finds the maximum *of that column* in `O(rows)`, and recurses on one
side, giving `O(rows · log columns)`. It is a good example of a pattern that
extends but not for free, and of why "just do it in both dimensions" deserves
suspicion.
</details>

## Acceptance checklist

- [ ] `python problem-03-ridge-line.py` prints four rows then
      `All checks passed.`
- [ ] The output matches the expected output character for character.
- [ ] You can state the invariant — "the interval always contains a ridge" —
      and the two cases that preserve it.
- [ ] You can say why the weaker guarantee is enough, and why the predicate is
      **not** one-way.
- [ ] The comparison is against `elevations[mid + 1]` and nothing else, with no
      `0` anywhere.
- [ ] Your tests assert the ridge property rather than a fixed index.
- [ ] The empty line is guarded before any indexing.
- [ ] Committed to Git with a message like `Add Week 5 homework 3: ridge line`.

## Stretch

- **Count how many stations you read.** Prove the logarithm to yourself.

  ```python
  def find_ridge_counting(elevations: list[int]) -> tuple[int, int]:
      """Return (ridge index, stations read)."""
      lo, hi, reads = 0, len(elevations) - 1, 0
      while lo < hi:
          mid = lo + (hi - lo) // 2
          reads += 1
          if elevations[mid] < elevations[mid + 1]:
              lo = mid + 1
          else:
              hi = mid
      return lo, reads
  ```

  ```text
  line of        7 stations:  3 reads
  line of    1_000 stations: 10 reads
  line of 1_000_000 stations: 20 reads
  ```

  Then find the global maximum of the same million-station line and count that
  instead. The two numbers are the whole argument for reading the contract
  carefully.

- **Find a ridge nearest the middle.** The surveyor would rather not put the
  mast at the very end of the line. Work out whether your search can be
  steered — and discover that it cannot, cheaply: the rule tells you where *a*
  ridge is, never where all of them are. Say what you would do instead, and
  what it would cost.

- **Break the guarantee.** Allow neighbouring stations to record the same
  height, feed in `[3, 3, 3, 3]`, and watch the rule stop discriminating. Then
  work out whether *any* `O(log n)` method can survive plateaus. It cannot, and
  the reason is the same one as in
  [Problem 4](./problem-04-duplicated-manifest.md): equal probes carry no
  information, so there is nothing to bisect on.

Next: [Homework Problem 4 — The Duplicated Manifest](./problem-04-duplicated-manifest.md).
