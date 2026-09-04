# Homework Problem 1 — The Kiln Firing Schedule

> **Topic:** binary search on the answer, where the answers come in fixed steps instead of every whole number
> **Lecture:** [02 — Binary Search on the Answer](../lecture-notes/02-binary-search-on-the-answer.md)
> **Difficulty:** Medium
> **Target time:** 60 minutes
> **Why this one:** [Exercise 5](../exercises/exercise-05-paving-reach.md) searched every whole metre. Here the rate card only sells kilns in 5-litre steps, so two thirds of the answer space is not for sale. Handling that cleanly — rather than searching everything and rounding at the end and hoping — is a small decision that shows up constantly in real pricing problems.

## The Brief

A pottery studio fires unglazed pots in a gas kiln. The pots wait on a loading
rail in a fixed order, and the kiln is packed from the front: each firing
takes a **run of pots from the front of whatever is left**, as many as fit in
the kiln, and then the door closes. Pots are never reordered and never split
across two firings.

```
rail:  9  14  6  21  3  11         (litres each, front of the rail on the left)

a 30-litre kiln:
  firing 1:  9 + 14 + 6 = 29 litres     (21 would not fit, so the door closes)
  firing 2:  21 + 3     = 24 litres
  firing 3:  11         = 11 litres     -> three firings
```

The studio is renting a kiln for the season. Kilns are only sold in **whole
5-litre sizes** — 5, 10, 15, 20 and so on — and a bigger one costs more.

Return the **smallest legal kiln** that clears the rail within the firings
booked, together with **how many firings that kiln actually needs**.

Two contract decisions that are not the obvious defaults:

- The second number is what the chosen kiln **really needs**, not the budget
  you were given. Book five firings and the answer may still be a kiln that
  finishes in four. Handing the budget back is the mistake this contract is
  shaped to catch.
- An empty rail returns `(0, 0)`. No pots, no kiln, no firings. Not `(5, 0)`,
  not `None`.

And one thing to work out for yourself before writing code: the answer space
is every fifth number, not every number. You can either search the **step
count** and multiply by 5 at the end, or search every integer and round each
midpoint. One of those can never produce an illegal volume. Pick it, and be
able to say why.

## Starter

Save this as `problem-01-kiln-firing-schedule.py` and fill in every `TODO`.

```python
"""problem-01-kiln-firing-schedule.py — the cheapest kiln to rent.

Binary search on an answer space that is not the integers: kilns are sold
in whole 5-litre steps.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

# ---- Given data ----
RAIL: list[int] = [9, 14, 6, 21, 3, 11]
STEP = 5  # kilns are sold in whole 5-litre increments


# ---- Your task ----
def firings_needed(pieces: list[int], volume: int) -> int:
    """Return how many firings a kiln of this volume needs to clear the rail.

    Args:
        pieces: Piece volumes in litres, in loading order.
        volume: The kiln's volume, at least as large as the biggest piece.

    Returns:
        The number of firings the front-loading packer closes.
    """
    # TODO: one pass; close a firing when the next piece will not fit
    # TODO: remember the part-full firing at the end
    ...


def min_kiln_volume(pieces: list[int], firings: int) -> tuple[int, int] | None:
    """Return the smallest legal kiln volume that clears the rail in time.

    Args:
        pieces: Piece volumes in litres, in loading order.
        firings: How many firings the studio has booked.

    Returns:
        (volume, firings_used), (0, 0) for an empty rail, or None when no
        kiln at all can clear the rail within the budget.
    """
    # TODO: the two contract branches first — empty rail, impossible budget
    # TODO: search the STEP COUNT, not the volume
    # TODO: lo = steps to hold the biggest piece, hi = steps to hold everything
    # TODO: report the firings the winning kiln really uses
    ...


# ---- Self-check ----
if __name__ == "__main__":
    for booked in (1, 2, 3, 5, 0):
        print(f"{booked} firings booked -> {min_kiln_volume(RAIL, booked)}")

    assert min_kiln_volume(RAIL, 3) == (30, 3)
    assert min_kiln_volume(RAIL, 2) == (35, 2)
    assert min_kiln_volume(RAIL, 4) == (25, 4)
    assert min_kiln_volume(RAIL, 5) == (25, 4)
    assert min_kiln_volume(RAIL, 6) == (25, 4)
    assert min_kiln_volume(RAIL, 1) == (65, 1)
    assert min_kiln_volume(RAIL, 0) is None
    assert min_kiln_volume([5, 5, 5], 1) == (15, 1)
    assert min_kiln_volume([4], 2) == (5, 1)
    assert min_kiln_volume([20], 1) == (20, 1)
    assert min_kiln_volume([], 0) == (0, 0)
    assert min_kiln_volume([], 3) == (0, 0)
    assert min_kiln_volume([9], 0) is None
    assert RAIL[0] == 9  # the rail was never reordered
    print("All checks passed.")
```

One idea you need before you start.

**Rounding up with integers.** `-(-x // step)` is the smallest whole number of
steps that holds `x`. Read it inside out: `-x // step` rounds *down* on a
negative number, which is rounding away from zero on the original, and the
outer minus flips it back. So `-(-64 // 5)` is `13`, meaning thirteen 5-litre
steps — a 65-litre kiln. It is exact at every size, which
`math.ceil(64 / 5)` is not once the numbers get large.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-05-binary-search/homework/problem-01-kiln-firing-schedule.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `firings_needed(pieces, volume)` returns the number of firings the
   front-loading packer closes, in one pass over the pots.
2. `min_kiln_volume(pieces, firings)` returns
   `(volume, firings_used)`, where `volume` is always a multiple of 5.
3. `firings_used` is what the returned kiln actually needs — never the budget.
4. An empty rail returns `(0, 0)`, before anything calls `max`.
5. A budget of zero firings on a non-empty rail returns `None`.
6. The search runs over the **step count**, so no midpoint is ever an illegal
   volume.
7. The interval is `lo` = steps to hold the biggest pot, `hi` = steps to hold
   the whole rail, and you can justify both ends.
8. Both functions keep their type hints and docstrings.

## Constraints

- **`0 <= len(pieces) <= 200_000`.** A season's greenware. The feasibility
  check is one pass, so the whole search is `O(n log S)` where `S` is the total
  volume on the rail. Anything quadratic inside the check is 4 × 10¹⁰
  operations and will not finish. The empty rail is in range on purpose — it is
  the degenerate case the contract names.

- **`1 <= pieces[i] <= 5_000`.** Every pot occupies volume, which is what lets
  the bottom of the search interval be pinned at the smallest legal kiln that
  holds the **largest** pot. Below that, one pot never fits at all and the
  packer would loop forever trying to close a firing around it.

- **`0 <= firings <= 200_000`.** Zero is a legal budget and it is the
  impossible branch whenever the rail is non-empty, because a non-empty rail
  always needs at least one firing. A budget larger than the pot count is also
  legal and simply saturates — which is the case that catches a solution that
  hands the budget back.

- **Kilns come in 5-litre steps.** The rate card is the rate card. A search
  that returns 33 has ignored it. This bound is the twist: it makes the answer
  space one fifth as dense as the integers, so the search depth is
  `log2(S / 5)` rather than `log2(S)`.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-01-kiln-firing-schedule.py
1 firings booked -> (65, 1)
2 firings booked -> (35, 2)
3 firings booked -> (30, 3)
5 firings booked -> (25, 4)
0 firings booked -> None
All checks passed.
```

Two rows repay a second look. The first: the whole rail is 64 litres, and 64
is not a legal kiln, so a single firing needs a 65-litre one — the rounding is
visible in the answer. The fourth: five firings were booked and the answer
still uses four, because 25 is already the smallest legal kiln and it needs
four firings. Handing back `(25, 5)` there would be a contract error, not an
arithmetic one.

## Steps

1. Save the starter and run it. Both functions return `Ellipsis`. Expected.
2. Write `firings_needed` first and test it alone: at 30 litres on the sample
   rail it should give `3`, at 25 it should give `4`, and at 65 it should give
   `1`.
3. Watch the end of that function. The loop closes a firing when the next pot
   will not fit — which leaves the last, part-full firing uncounted. Add it,
   and make sure an empty rail still returns `0` rather than `1`.
4. Now the contract branches: empty rail returns `(0, 0)`; `firings < 1` on a
   non-empty rail returns `None`.
5. Set the interval in **steps**: `lo = -(-max(pieces) // 5)`,
   `hi = -(-sum(pieces) // 5)`. Say out loud why the top of that interval
   always works — one kiln big enough for everything is one firing.
6. Run the ordinary smallest-such-that search over the step count: half-open,
   `hi = mid` when the kiln at `mid * 5` is fast enough, `lo = mid + 1` when it
   is not.
7. Return `lo * 5` and one more call to `firings_needed` at that volume. That
   second call is the contract's second number, and it is why you cannot just
   return the budget.
8. Trace `firings = 5` by hand and confirm you understand why the answer stops
   moving once the budget is generous.

## The Solution

```python
"""problem-01-kiln-firing-schedule-solution.py - the cheapest kiln to rent.

Binary search on the answer, over an answer space that is not the integers:
kilns are sold in whole 5-litre steps, so the search runs over the STEP
COUNT and multiplies by 5 at the end. That way no midpoint is ever an
illegal volume and no rounding is needed inside the loop.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
RAIL: list[int] = [9, 14, 6, 21, 3, 11]
STEP = 5  # kilns are sold in whole 5-litre increments


# ---- Your task ----
def firings_needed(pieces: list[int], volume: int) -> int:
    """Return how many firings a kiln of this volume needs to clear the rail.

    Args:
        pieces: Piece volumes in litres, in loading order.
        volume: The kiln's volume, at least as large as the biggest piece.

    Returns:
        The number of firings the front-loading packer closes.
    """
    firings = 0
    load = 0
    for piece in pieces:
        if load + piece > volume:
            firings += 1  # the door closes, and this piece starts the next one
            load = 0
        load += piece
    return firings + 1 if load else firings


def min_kiln_volume(pieces: list[int], firings: int) -> tuple[int, int] | None:
    """Return the smallest legal kiln volume that clears the rail in time.

    Args:
        pieces: Piece volumes in litres, in loading order.
        firings: How many firings the studio has booked.

    Returns:
        (volume, firings_used), (0, 0) for an empty rail, or None when no
        kiln at all can clear the rail within the budget.
    """
    if not pieces:
        return 0, 0
    if firings < 1:
        return None  # a non-empty rail always needs at least one firing

    lo = -(-max(pieces) // STEP)  # steps: the smallest kiln one piece fits in
    hi = -(-sum(pieces) // STEP)  # steps: the smallest kiln the whole rail fits in
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if firings_needed(pieces, mid * STEP) <= firings:
            hi = mid
        else:
            lo = mid + 1
    return lo * STEP, firings_needed(pieces, lo * STEP)


# ---- Self-check ----
if __name__ == "__main__":
    for booked in (1, 2, 3, 5, 0):
        print(f"{booked} firings booked -> {min_kiln_volume(RAIL, booked)}")

    assert min_kiln_volume(RAIL, 3) == (30, 3)
    assert min_kiln_volume(RAIL, 2) == (35, 2)
    assert min_kiln_volume(RAIL, 4) == (25, 4)
    assert min_kiln_volume(RAIL, 5) == (25, 4)
    assert min_kiln_volume(RAIL, 6) == (25, 4)
    assert min_kiln_volume(RAIL, 1) == (65, 1)
    assert min_kiln_volume(RAIL, 0) is None
    assert min_kiln_volume([5, 5, 5], 1) == (15, 1)
    assert min_kiln_volume([4], 2) == (5, 1)
    assert min_kiln_volume([20], 1) == (20, 1)
    assert min_kiln_volume([], 0) == (0, 0)
    assert min_kiln_volume([], 3) == (0, 0)
    assert min_kiln_volume([9], 0) is None
    assert RAIL[0] == 9  # the rail was never reordered
    print("All checks passed.")
```

**Searching the step count is what makes the granularity disappear.** `lo` and
`hi` are counts of 5-litre steps, so every midpoint the loop tries is a real
product on the rate card once you multiply by 5. Nothing is rounded inside the
loop, so there is nowhere for a rounding bug to hide. The alternative —
searching every integer volume and rounding each midpoint up before testing it
— can work, and it has a subtle failure mode: two different midpoints round to
the same legal volume, so the interval can stop shrinking. Choosing
coordinates in which the problem has no awkward cases is nearly always
cheaper than defending against them.

**The four-part reframe.**

> *Reframe:* find the smallest step count `t` such that a kiln of `5t` litres
> clears the rail within the firings booked.
> *Interval:* `lo` is the smallest `t` whose kiln holds the biggest single pot,
> because below that one pot never fits at all; `hi` is the smallest `t` whose
> kiln holds the entire rail, because that kiln always finishes in one firing.
> *Predicate:* `firings_needed(pieces, 5t) <= firings`. Monotone in `t`,
> because a bigger kiln never forces the packer to close a firing it would
> otherwise have kept open.
> *Return:* the post-loop `lo`, times 5, plus one more predicate call for the
> firings that kiln really uses.

**The packing loop closes a firing one pot too late, on purpose.** Read it
again: it adds to the load, and only when the *next* pot will not fit does it
count a firing and reset. So the last, part-full firing is never counted
inside the loop — hence `return firings + 1 if load else firings`. Writing it
this way keeps the empty rail correct for free, which is the sort of thing
worth noticing rather than patching afterwards.

**Why the top of the interval always works.** A kiln that holds the whole rail
fires everything at once. So if the budget is at least 1 — which the guard has
already established — the top of the interval satisfies the predicate, and a
smallest-such-that search is guaranteed to land somewhere. That is the
feasibility check the lecture asks for; here it is satisfied by the guard
rather than needing its own test.

**`firings < 1` is the only impossible case, and it is not the one people
guess.** The tempting guard is `len(pieces) > firings` — copied from
[Exercise 5](../exercises/exercise-05-paving-reach.md), where one section per
night made it right. It is wrong here: a firing takes as many pots as fit, so
six pots can clear in a single firing given a big enough kiln. The only way to
fail is to have no firings at all. Two problems, near-identical shapes,
different impossibility conditions — which is exactly why the contract has to
be read rather than recognised.

**The second number costs one extra call and cannot be skipped.** After the
loop, `lo * 5` is the volume; `firings_needed` at that volume is what it
really uses. With a generous budget the two differ, and the difference is the
studio's actual schedule.

## Run it

Copy the worked answer on this page into `problem-01-kiln-firing-schedule.py` and run it:

```bash
python problem-01-kiln-firing-schedule.py
```

It is the same program you are writing, under a name that will not collide
with your own `problem-01-kiln-firing-schedule.py`.

## Common bugs to catch

- **`ValueError: max() iterable argument is empty`.** You built the interval
  before handling the empty rail:

  ```text
  Traceback (most recent call last):
      lo = -(-max(pieces) // STEP)
             ~~~^^^^^^^^
  ValueError: max() iterable argument is empty
  ```

  The contract says `(0, 0)`. That branch is the first line of the function.

- **`ZeroDivisionError: integer division or modulo by zero`.** Your packer
  divides by the kiln volume, and a search that starts at zero steps offers it
  a zero-litre kiln:

  ```text
  Traceback (most recent call last):
      firings = -(-piece // volume)
                 ~~~~~~~^^~~~~~~~~~
  ZeroDivisionError: integer division or modulo by zero
  ```

  Two things to fix. The packer here is a running total, not a division — pots
  are not split, so there is no `ceil` in this problem at all. And `lo` starts
  at the steps needed for the biggest pot, never at zero.

- **`min_kiln_volume(RAIL, 5)` returns `(25, 5)`.** You returned the budget as
  the second number. It is right whenever the budget is tight and wrong
  whenever it is generous, which makes it the kind of bug that passes a casual
  test. Call the predicate once more at the winning volume.

- **`min_kiln_volume(RAIL, 1)` returns `(64, 1)`.** You searched volumes rather
  than steps and forgot to round the result. 64 litres is not on the rate card.
  Search the step count and the illegal answers become unreachable.

- **`min_kiln_volume(RAIL, 0)` returns `(65, 1)`.** The impossible branch is
  missing. Every midpoint fails the predicate, `lo` climbs to the top of the
  interval, and you confidently recommend renting the biggest kiln on the card
  for a season with no firings booked in it.

- **`min_kiln_volume([], 0)` returns `(5, 0)`.** You guarded `max` but not the
  contract. No pots means no kiln, and the answer is `(0, 0)`.

- **`firings_needed` returns one too many on an empty rail.** You wrote
  `return firings + 1` unconditionally. With nothing on the rail there is no
  part-full firing to count. The `if load` is doing real work.

- **The answer is one step too big on every input.** You wrote `hi = mid - 1`
  in a half-open loop. This is a smallest-such-that search: `hi = mid` on
  success. Off by one step here is off by five litres in the answer, which
  reads plausibly and costs the studio money.

## Under the hood

<details>
<summary>Under the hood — where the log(S/5) comes from, and the rounding alternative</summary>

**Cost.**

Time is `O(n log(S / 5))`, where `n` is the number of pots and `S` is the total
volume on the rail. The search halves an interval of `S / 5` steps — about
17 iterations at the top of the constraints — and each iteration walks all `n`
pots once. Space is `O(1)`.

Notice what the granularity bought: dividing the answer space by five removes
`log2(5) ≈ 2.3` iterations. That is a real saving and a small one. The
granularity's importance is about *correctness* — never returning a volume
nobody sells — far more than about speed, and saying so is more honest than
claiming a speedup as the motivation.

**The rounding alternative, and its trap.**

You can search every integer volume and round each midpoint up to the next
multiple of 5 before testing it:

```python
mid = lo + (hi - lo) // 2
legal = -(-mid // STEP) * STEP
if firings_needed(pieces, legal) <= firings:
    hi = legal          # not `mid`
else:
    lo = legal + 1      # not `mid + 1`
```

It works, and only if you are careful to shrink the interval using the
**rounded** value rather than the raw midpoint. Shrink with the raw midpoint
and two consecutive iterations can round to the same legal volume, the
interval stops shrinking, and the loop hangs. Both spellings are defensible in
an interview; the step-count version is defensible in one sentence, and this
one needs three.

**The same shape, three different budgets.**

| Problem | Budget shape | Impossible when |
| --- | --- | --- |
| [Exercise 5](../exercises/exercise-05-paving-reach.md) | one section per night | `nights < len(sections)` |
| This page | a firing takes as many pots as fit | `firings < 1` |
| [Problem 2](./problem-02-relay-handoff.md) | exactly this many blocks, all non-empty | `riders > len(legs)` or `riders < 1` |

Three problems, one predicate machine, three different impossibility
conditions — every one of them read off the contract rather than off the
pattern. The pattern tells you which loop to write. Only the contract tells you
when the answer does not exist.

</details>

## Acceptance checklist

- [ ] `python problem-01-kiln-firing-schedule.py` prints five rows then
      `All checks passed.`
- [ ] The output matches the expected output character for character.
- [ ] The search runs over the step count, and you can say in one sentence why
      that cannot return an illegal volume.
- [ ] You can deliver the four-part reframe in about thirty seconds.
- [ ] You can state the monotonicity claim in one sentence.
- [ ] The empty-rail branch runs before `max`, and the impossible branch is
      `firings < 1` rather than a copied `len(pieces) > firings`.
- [ ] The second number comes from a predicate call, not from the budget.
- [ ] Committed to Git with a message like
      `Add Week 5 homework 1: kiln firing schedule`.

## Stretch

- **Print the firing plan.** The studio wants a sheet for the wall.

  ```python
  def firing_plan(pieces: list[int], volume: int) -> list[list[int]]:
      """Return the pots loaded into each firing, in order."""
      plan: list[list[int]] = [[]]
      load = 0
      for piece in pieces:
          if load + piece > volume:
              plan.append([])
              load = 0
          plan[-1].append(piece)
          load += piece
      return plan if plan[-1] else plan[:-1]
  ```

  ```text
  30-litre kiln: [[9, 14, 6], [21, 3], [11]]
  25-litre kiln: [[9, 14], [6], [21, 3], [11]]
  ```

  Check that `len(firing_plan(...))` always equals `firings_needed(...)`. Two
  independent routes to the same number is the cheapest test there is.

- **Charge for it.** Suppose a kiln costs 40 currency units per 5-litre step
  per season, and each firing costs 12 in gas. Write the function that returns
  the cheapest **total**, not the smallest kiln.

  ```text
  budget 5 firings: 25L kiln + 4 firings = 248
  budget 5 firings: 30L kiln + 3 firings = 276
  ```

  The smallest kiln is no longer automatically the best answer, and — more
  importantly — total cost is **not monotone** in kiln size, so bisection stops
  being valid. Work out what you would do instead. Recognising when the pattern
  stops applying is the point of the exercise.

- **Allow pots to be split across firings.** Now the cost is a sum of ceilings,
  exactly like [Exercise 5](../exercises/exercise-05-paving-reach.md). Rewrite
  the predicate, and check whether the interval's lower bound can be relaxed.
  It can, and working out why is a good test of whether you understood what
  the bound was protecting against.

Next: [Homework Problem 2 — The Relay Handoff](./problem-02-relay-handoff.md).
