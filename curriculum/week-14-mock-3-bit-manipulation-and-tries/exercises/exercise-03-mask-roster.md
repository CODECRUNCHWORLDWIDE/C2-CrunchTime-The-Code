# Exercise 3 — The Mask Roster

> **Topic:** a whole set in one integer, and every set operation as arithmetic
> **Lecture:** [02 — Bitmasks, Subset Enumeration and Bit DP](../lecture-notes/02-bitmasks-and-subset-enumeration-and-bit-dp.md)
> **Difficulty:** Medium
> **Target time:** 40 minutes
> **Why this one:** it is the bridge back to Week 12. Enumerating every subset there was a recursive walk; here it is `range(1 << n)`, one line. Seeing the same answer arrive two completely different ways is what makes the representation stick.

## The Brief

A depot's night crew is drawn from a small pool. Rather than keeping a list of
who is on, the rota holds **one integer per shift**: bit 0 is the first name in
the pool, bit 1 the second, and so on. A lit bit means that person is on.

That turns every question about a shift into arithmetic:

```text
who is on          walk the lit bits
how many are on    count the lit bits
is A inside B      B & A == A
every shift        range(1 << pool size)
```

## Starter

The worked answer on this page carries the pool and the self-checks.

```text
bit 0 = Ash    bit 1 = Bo    bit 2 = Cass    bit 3 = Dov
```

Work out the mask for "Ash and Cass" before writing anything. It is bits 0 and
2, which is 5, which is `0101` — and reading that binary right to left rather
than left to right is the thing to get straight now.

## Requirements

1. `roster_of(mask, pool)` returns the names on shift, in pool order.
2. `mask_of(names, pool)` returns the mask for a list of names.
3. `every_shift(pool)` returns every possible shift as a mask.
4. `on_count(mask)` counts the lit bits.
5. `covers(bigger, smaller)` says whether one shift includes another.
6. `shifts_covering(mask, pool)` returns every shift that covers a given one.

## Constraints

- **Bit 0 is the first name.** The binary printed left to right reads the pool
  right to left, and getting it backwards produces answers that look entirely
  plausible. Say the direction in the memo.
- **A mask that does not fit the pool is refused.** Otherwise the two have got
  out of step and every answer after it is quietly wrong.
- **`covers` is one AND.** `bigger & smaller == smaller` — ANDing keeps only the
  bits in both, so if that is still all of `smaller`, nothing in it was missing.
  Writing it as a loop over names is correct and misses the page.
- **Naming somebody twice lights the same bit once.** That is a property of the
  representation, not a bug to guard against, and it is worth noticing.
- **This is for small pools.** One machine integer holds one bit per person. Say
  that out loud rather than discovering it at twenty thousand names.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-03-mask-roster.py
POOL  ['Ash', 'Bo', 'Cass', 'Dov']
    bit 0=Ash   bit 1=Bo   bit 2=Cass   bit 3=Dov

EVERY SHIFT
     0  0000  0  (nobody)
     1  0001  1  Ash
     2  0010  1  Bo
     3  0011  2  Ash, Bo
     4  0100  1  Cass
     5  0101  2  Ash, Cass
     6  0110  2  Bo, Cass
     7  0111  3  Ash, Bo, Cass
     8  1000  1  Dov
     9  1001  2  Ash, Dov
    10  1010  2  Bo, Dov
    11  1011  3  Ash, Bo, Dov
    12  1100  2  Cass, Dov
    13  1101  3  Ash, Cass, Dov
    14  1110  3  Bo, Cass, Dov
    15  1111  4  Ash, Bo, Cass, Dov

    Ash and Cass    : mask 5 (0101)
    shifts covering : [5, 7, 13, 15]

All checks passed.
```

Sixteen shifts for four people, listed by counting from 0 to 15. That is the
same sixteen subsets
[Week 12's Exercise 1](../../week-12-backtracking-and-combinatorics/exercises/exercise-01-glaze-sample-set.md)
produced with a recursive walk, three lines of choose-explore-undo and a trail.
Here it is `range(1 << 4)`.

Both are right. The walk generalises to problems where the choices are not
independent; the counting does not, and it is far faster where it applies. Being
able to say which is which is the whole of this page.

## Steps

1. Read the self-checks. They are the spec.
2. Work out the mask for Ash and Cass by hand: 5.
3. Write the memo: one bit per person, bit 0 first, and the four operations.
4. Write `roster_of` and `mask_of`, then check they round-trip **both ways** for
   every shift. That pair of checks catches the reversed-bit-order mistake
   immediately.
5. Write `covers` as one AND, and check it against a set-based version on all
   256 pairs of shifts.
6. Add the range checks, then write the FRAME pass — with the comparison to Week
   12's walk in it.

## The Solution

```python
"""exercise-03-mask-roster-solution.py - a whole roster in one integer.

A depot's night crew is drawn from a small pool. Rather than keeping a list of
who is on, the rota holds ONE INTEGER per shift: bit 0 is the first name in the
pool, bit 1 the second, and so on. A lit bit means that person is on.

That turns every question about a shift into arithmetic. Who is on is a walk
over the lit bits. How many are on is a bit count. Is this shift a subset of
that one is a single AND. And enumerating every possible shift is counting from
0 upwards.

The point of the page is the correspondence, so every function comes in two
forms - the mask form and the plain-set form - and the checks assert they
agree. The mask version is not always shorter. It is always faster, and on a
pool of twenty it is the difference between an integer and a set of strings.

Note the limit that comes with it: one machine integer holds one bit per
person, so this representation is for SMALL pools. Say that out loud rather
than discovering it.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
POOL: tuple[str, ...] = ("Ash", "Bo", "Cass", "Dov")


# ---- Your task ----
def roster_of(mask: int, pool: tuple[str, ...]) -> list[str]:
    """Return the people a mask puts on shift, in pool order.

    Args:
        mask: The shift, one bit per person.
        pool: The names, in bit order.

    Returns:
        The names whose bit is lit.

    Raises:
        ValueError: If the mask lights a bit the pool has no name for, which
            means the two have got out of step and every answer after it would
            be quietly wrong.
    """
    if not 0 <= mask < (1 << len(pool)):
        raise ValueError(f"mask {mask} does not fit a pool of {len(pool)}")
    return [name for index, name in enumerate(pool) if mask >> index & 1]


def mask_of(names: list[str], pool: tuple[str, ...]) -> int:
    """Return the mask for a list of names.

    Args:
        names: The people on shift, in any order.
        pool: The names, in bit order.

    Returns:
        The mask. Naming somebody twice is harmless - a bit is lit or it is
        not - which is itself worth noticing about this representation.

    Raises:
        ValueError: If a name is not in the pool.
    """
    mask = 0
    for name in names:
        if name not in pool:
            raise ValueError(f"{name!r} is not in the pool")
        mask |= 1 << pool.index(name)
    return mask


def every_shift(pool: tuple[str, ...]) -> list[int]:
    """Return every possible shift, as masks.

    Args:
        pool: The names, in bit order.

    Returns:
        Every mask from 0 to 2 ** len(pool) - 1. Enumerating subsets is
        counting - which is the whole reason this representation is worth
        knowing, and it is one line against a recursive walk.
    """
    return list(range(1 << len(pool)))


def on_count(mask: int) -> int:
    """Return how many people a mask puts on shift.

    Args:
        mask: The shift. Must not be negative.

    Returns:
        The number of lit bits, counted by clearing the lowest one each turn.

    Raises:
        ValueError: If `mask` is negative.
    """
    if mask < 0:
        raise ValueError("a shift mask cannot be negative")
    count = 0
    while mask:
        mask &= mask - 1
        count += 1
    return count


def covers(bigger: int, smaller: int) -> bool:
    """Say whether every person on the smaller shift is also on the bigger one.

    Args:
        bigger: The shift that might cover the other.
        smaller: The shift that might be covered.

    Returns:
        True when `smaller` is a subset of `bigger`. The whole test is
        `bigger & smaller == smaller`: ANDing keeps only the bits in both, so
        if that is still all of `smaller`, nothing in it was missing.
    """
    return bigger & smaller == smaller


def shifts_covering(mask: int, pool: tuple[str, ...]) -> list[int]:
    """Return every shift that covers `mask`.

    Args:
        mask: The shift that must be covered.
        pool: The names, in bit order.

    Returns:
        The masks of every shift including everybody in `mask`.

    Raises:
        ValueError: If the mask does not fit the pool.
    """
    roster_of(mask, pool)          # borrows its range check
    return [shift for shift in every_shift(pool) if covers(shift, mask)]


# ---- Self-check ----
if __name__ == "__main__":
    print(f"POOL  {list(POOL)}")
    print("    " + "   ".join(f"bit {index}={name}" for index, name in enumerate(POOL)))
    print()

    print("EVERY SHIFT")
    for shift in every_shift(POOL):
        names = roster_of(shift, POOL)
        shown = ", ".join(names) if names else "(nobody)"
        print(f"    {shift:>2}  {shift:0{len(POOL)}b}  {on_count(shift)}  {shown}")
    print()

    night = mask_of(["Ash", "Cass"], POOL)
    print(f"    Ash and Cass    : mask {night} ({night:0{len(POOL)}b})")
    print(f"    shifts covering : {shifts_covering(night, POOL)}")
    print()

    # Sixteen shifts for four people, and that is 2 ** 4.
    assert len(every_shift(POOL)) == 16

    # The two representations round-trip, both ways, for every shift.
    for shift in every_shift(POOL):
        assert mask_of(roster_of(shift, POOL), POOL) == shift
    for names in ([], ["Ash"], ["Bo", "Dov"], list(POOL)):
        assert roster_of(mask_of(names, POOL), POOL) == [n for n in POOL if n in names]

    # Bit 0 is the first name in the pool. Getting this backwards is the most
    # common mistake and every answer still looks plausible.
    assert roster_of(1, POOL) == ["Ash"]
    assert roster_of(1 << 3, POOL) == ["Dov"]

    # The count agrees with the roster length everywhere.
    for shift in every_shift(POOL):
        assert on_count(shift) == len(roster_of(shift, POOL))

    # Naming somebody twice lights the same bit once.
    assert mask_of(["Ash", "Ash"], POOL) == mask_of(["Ash"], POOL)

    # Covering agrees with the set-based answer, on every pair of shifts.
    for bigger in every_shift(POOL):
        for smaller in every_shift(POOL):
            by_set = set(roster_of(smaller, POOL)) <= set(roster_of(bigger, POOL))
            assert covers(bigger, smaller) == by_set

    # Nobody covers nobody, and everybody covers everybody.
    assert covers(0, 0) and covers(15, 0) and covers(15, 15)
    assert not covers(0, 1)

    # Ash and Cass is bits 0 and 2, so mask 5, and four shifts cover it.
    assert night == 0b0101
    assert len(shifts_covering(night, POOL)) == 4

    # A mask that does not fit the pool is refused rather than silently
    # dropping the people it cannot name.
    for bad in (16, -1):
        try:
            roster_of(bad, POOL)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for mask {bad}")

    # A name that is not in the pool is refused too.
    try:
        mask_of(["Ash", "Wren"], POOL)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for a name not in the pool")

    print("All checks passed.")
```

Every function here has a plain-set twin in the checks, and the two are asserted
to agree on every input. That is deliberate: bit tricks are exactly the kind of
code that is obviously right and quietly wrong, and the set version is slow,
readable and easy to be sure of.

## Run it

Download the solution beside this page and run it:

```bash
python exercise-03-mask-roster.py
```

No third-party packages, no arguments, no input. It prints all sixteen shifts,
the covering shifts for one of them, and then `All checks passed.`

## Common bugs to catch

- **Bit 0 as the last name.** Symptom: every answer plausible and every answer
  wrong. The round-trip check in both directions is what catches it.
- **`1 << index` written as `index << 1`.** Symptom: bits at 0, 2, 4, 6 and a
  pool that appears to have gaps.
- **`covers` as `bigger | smaller == bigger`.** Symptom: it works. It is the same
  test written the other way round, and saying why both hold is a good check of
  whether you understand it.
- **Forgetting the range check.** Symptom: a mask of 20 on a pool of four
  silently drops the bit nobody is named for.
- **`on_count` on a negative mask.** Symptom: the clearing loop never ends.
- **Enumerating shifts with a recursive walk.** Symptom: correct, and this page
  had one job.

## Acceptance checklist

- [ ] Sixteen shifts for four people.
- [ ] `roster_of` and `mask_of` round-trip in both directions, for every shift.
- [ ] `roster_of(1, pool)` is the **first** name.
- [ ] `on_count` agrees with the roster length for every shift.
- [ ] `covers` agrees with the set-based test on all 256 pairs.
- [ ] "Ash and Cass" is mask 5, covered by four shifts.
- [ ] A mask outside the pool's range raises `ValueError`.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Enumerate every **subset of a given shift**, not of the whole pool. There is a
  well-known one-line idiom for it — `sub = (sub - 1) & mask` — and deriving why
  it works is a genuinely good half-hour.
- Add "who is on both shifts" and "who is on either" as one-line functions, and
  say which set operation each corresponds to.
- Take a pool of twenty and compare the memory of the mask against the set of
  strings. Then say at what pool size you would stop using masks, and why.
