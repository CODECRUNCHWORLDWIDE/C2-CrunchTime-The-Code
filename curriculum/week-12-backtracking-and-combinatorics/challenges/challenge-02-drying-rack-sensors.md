# Challenge 2 — The Warped Drying Rack

> Topic: constraint satisfaction with an incremental legality test · Lecture: [3](../lecture-notes/03-grid-backtracking-and-constraint-satisfaction.md) · Difficulty: Medium-Hard · Target time: 75 minutes including the FRAME write-up · Why this one: it is where an `O(n)` legality check becomes an `O(1)` one, and where you have to say why that is allowed.

## The Brief

A pottery drying rack is a square grid of slats. One humidity sensor goes on each
row. Two sensors interfere if they share a column, and they interfere if they sit
on the same diagonal, because the draught runs corner to corner.

Some slats are **warped** and will not hold a sensor at all. The warped slats are
given per rack. They are what makes this a real rack rather than a textbook one:
they change which arrangements survive, they are not symmetrical, and they are
the reason the count is worth asking for.

A rack with exactly one arrangement can be set up from the manual. A rack with
none needs a slat replaced before anyone tries.

## Starter

The worked answer on this page carries the rack, the warped slats and the
self-checks.

```text
rack 6x6, warped (0,0) (1,3) (3,1) (5,5)
```

Predict the unwarped count for `n = 4, 5, 6` before you run anything. Two of the
three surprise most people, and being wrong on paper first is the point.

## Requirements

1. `arrangements(size, warped)` returns every legal placement as a tuple of one
   column index per row.
2. `count(...)` and `first(...)` — the number of them, and the smallest in
   reading order, or `None`.
3. `render(...)` draws one arrangement: `S` a sensor, `x` a warped slat, `.` a
   free slat. A human must be able to check the answer by eye.
4. A negative size, or a warped slat that is not on the rack, raises
   `ValueError`.
5. The legality test is **incremental** — `O(1)` per candidate, not a scan of
   everything placed so far.

## Constraints

- **One sensor per row, by construction.** Recursing a row at a time means the
  row constraint can never be violated and never needs checking. Say that in
  your memo; a check you do not need is a check you should not write.
- **Diagonals are named by arithmetic.** A down-right diagonal is constant in
  `col - row`; a down-left one is constant in `col + row`. That is what turns
  the legality test into three set lookups.
- **Undo all four pieces of state**, in the same order they were done. A partial
  undo makes the count too low and is invisible on a small rack.
- **A warped slat is not a placed sensor.** It blocks its own square only — it
  does not block a column or a diagonal.
- `size = 0` has exactly one arrangement: the empty one. Decide that deliberately
  rather than discovering it.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python challenge-02-drying-rack-sensors.py
rack 6x6, warped [(0, 0), (1, 3), (3, 1), (5, 5)]
    arrangements: 2
    first:        (2, 5, 1, 4, 0, 3)

x . S . . .
. . . x . S
. S . . . .
. x . . S .
S . . . . .
. . . S . x

the same rack with no warped slats
    arrangements: 4

small racks
    0x0: 1
    1x1: 1
    2x2: 0
    3x3: 0
    4x4: 2
    5x5: 10

All checks passed.
```

The small-rack table is the part to sit with. `2x2` and `3x3` have **no**
arrangement at all — the constraints are unsatisfiable, not merely tight — and
`5x5` has ten while `6x6` has four. The count does not climb with size, and a
write-up that assumes it does has not understood the pruning.

## Steps

1. Read the self-checks. They are the spec.
2. Write the memo: name the search, the state, and why the row constraint needs
   no check.
3. Implement with a plain "scan everything placed" legality test first, and get
   the unwarped counts right. Correct before clever.
4. Replace the scan with the three sets. The counts must not move — if they do,
   your diagonal arithmetic is wrong, and the two-line version is easier to
   debug against the scan than against the answers.
5. Add the warped slats, then `render`, and check one arrangement by eye.
6. Add the `ValueError` guards, then write the FRAME pass.

## The Solution

```python
"""challenge-02-drying-rack-sensors-solution.py - sensors on a warped rack.

A pottery drying rack is a square grid of slats. One humidity sensor goes on
each row. Sensors interfere when they share a column, and they interfere when
they sit on the same diagonal, because the draught runs corner to corner.

Some slats are warped and will not hold a sensor at all. That is what makes
this rack rather than a textbook: the warped slats are given per rack, they
change which arrangements survive, and they are the reason the count is worth
asking for.

  arrangements  - every legal placement, as one column per row
  count         - how many there are
  first         - the smallest in reading order, or None
  render        - one arrangement drawn, so a human can check it

The count is the interesting number. A rack with one arrangement can be set up
from the manual; a rack with none needs a slat replaced before anybody tries.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

# ---- Given data ----
SIZE = 6

# (row, column) slats that are warped and cannot hold a sensor.
WARPED: set[tuple[int, int]] = {(0, 0), (1, 3), (3, 1), (5, 5)}


# ---- Your task ----
def _place(
    size: int,
    warped: set[tuple[int, int]],
    row: int,
    columns: list[int],
    taken_cols: set[int],
    taken_down: set[int],
    taken_up: set[int],
    found: list[tuple[int, ...]],
) -> None:
    """Place one sensor on `row`, then recurse.

    The three taken-sets are what turn an O(n) legality check into an O(1) one.
    A diagonal running down-right is constant in (col - row); one running
    down-left is constant in (col + row). Those two numbers name the diagonals,
    so membership is a set lookup rather than a scan of everything placed.

    Args:
        size: The rack is size x size.
        warped: Slats that cannot hold a sensor.
        row: The row being filled.
        columns: Column chosen for each row so far.
        taken_cols: Columns already used.
        taken_down: Down-right diagonals already used, keyed col - row.
        taken_up: Down-left diagonals already used, keyed col + row.
        found: Completed arrangements, appended to in place.
    """
    if row == size:
        found.append(tuple(columns))
        return

    for col in range(size):
        if (row, col) in warped:
            continue
        if col in taken_cols or (col - row) in taken_down or (col + row) in taken_up:
            continue
        columns.append(col)
        taken_cols.add(col)
        taken_down.add(col - row)
        taken_up.add(col + row)
        _place(size, warped, row + 1, columns, taken_cols, taken_down, taken_up, found)
        # Undo all four, in the same order they were done. A partial undo is
        # the bug that makes a count too low and is invisible in small racks.
        columns.pop()
        taken_cols.discard(col)
        taken_down.discard(col - row)
        taken_up.discard(col + row)


def arrangements(size: int, warped: set[tuple[int, int]]) -> list[tuple[int, ...]]:
    """Every legal sensor placement.

    Args:
        size: The rack is size x size.
        warped: Slats that cannot hold a sensor.

    Returns:
        A list of tuples, one column index per row. Empty when the rack cannot
        be set up at all.

    Raises:
        ValueError: If size is negative, or a warped slat is off the rack.
    """
    if size < 0:
        raise ValueError("a rack cannot have negative size")
    for row, col in warped:
        if not (0 <= row < size and 0 <= col < size):
            raise ValueError(f"warped slat {(row, col)} is not on the rack")

    found: list[tuple[int, ...]] = []
    _place(size, warped, 0, [], set(), set(), set(), found)
    return found


def count(size: int, warped: set[tuple[int, int]]) -> int:
    """How many legal placements the rack has."""
    return len(arrangements(size, warped))


def first(size: int, warped: set[tuple[int, int]]) -> tuple[int, ...] | None:
    """The smallest legal placement in reading order, or None."""
    found = arrangements(size, warped)
    return min(found) if found else None


def render(size: int, warped: set[tuple[int, int]], placement: tuple[int, ...]) -> str:
    """Draw one arrangement: S a sensor, x a warped slat, . a free slat."""
    lines = []
    for row in range(size):
        cells = []
        for col in range(size):
            if placement[row] == col:
                cells.append("S")
            elif (row, col) in warped:
                cells.append("x")
            else:
                cells.append(".")
        lines.append(" ".join(cells))
    return "\n".join(lines)


# ---- Self-check ----
if __name__ == "__main__":
    print(f"rack {SIZE}x{SIZE}, warped {sorted(WARPED)}")
    total = count(SIZE, WARPED)
    best = first(SIZE, WARPED)
    print(f"    arrangements: {total}")
    print(f"    first:        {best}")
    print()
    print(render(SIZE, WARPED, best))
    print()

    print("the same rack with no warped slats")
    print(f"    arrangements: {count(SIZE, set())}")
    print()

    print("small racks")
    for n in range(0, 6):
        print(f"    {n}x{n}: {count(n, set())}")

    # Warped slats reduce the count - that is the whole point of them being
    # given per rack rather than assumed away.
    assert count(SIZE, WARPED) < count(SIZE, set())

    # The classic counts for an unwarped square rack. These are the numbers the
    # write-up should predict before running anything.
    assert count(0, set()) == 1      # one way to place nothing
    assert count(1, set()) == 1
    assert count(2, set()) == 0      # two rows always interfere
    assert count(3, set()) == 0
    assert count(4, set()) == 2
    assert count(5, set()) == 10
    assert count(6, set()) == 4

    # A sensor never lands on a warped slat.
    for placement in arrangements(SIZE, WARPED):
        for row, col in enumerate(placement):
            assert (row, col) not in WARPED

    # No two sensors share a column or a diagonal.
    for placement in arrangements(SIZE, WARPED):
        cols = list(placement)
        assert len(set(cols)) == len(cols)
        assert len({c - r for r, c in enumerate(cols)}) == len(cols)
        assert len({c + r for r, c in enumerate(cols)}) == len(cols)

    # A rack warped along a whole row cannot be set up at all.
    assert count(4, {(2, c) for c in range(4)}) == 0
    assert first(4, {(2, c) for c in range(4)}) is None

    # Malformed input is refused rather than half-searched.
    for bad_size, bad_warped in ((-1, set()), (3, {(5, 5)})):
        try:
            arrangements(bad_size, bad_warped)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad_size}, {bad_warped}")

    print()
    print("All checks passed.")
```

The four undos sit directly under the recursive call in the same order as the
four marks above it. That symmetry is deliberate: the failure mode here is
undoing three of the four, and the only reliable defence is to write them where
a reader can see one is missing.

## Run it

Download the solution beside this page and run it:

```bash
python challenge-02-drying-rack-sensors.py
```

No third-party packages, no arguments, no input. It prints the warped rack's
count, one rendered arrangement, the unwarped counts and then
`All checks passed.`

## Common bugs to catch

- **A partial undo.** Symptom: counts too low, and correct on a 4×4 so you
  believe it. Undo the column, both diagonals and the placement.
- **Diagonals keyed on the wrong sum.** Symptom: `4x4` gives something other
  than 2. Down-right is `col - row`; down-left is `col + row`. Swapping them
  quietly forbids the wrong squares.
- **Checking the row constraint.** Symptom: correct, slower, and a memo that
  cannot explain why the check never fires.
- **Treating a warped slat as an occupied square.** Symptom: far too few
  arrangements. It blocks one square, not a column and two diagonals.
- **Returning at the first arrangement.** Symptom: every count is 1 or 0. This
  problem asks how many.
- **Assuming more rows means more arrangements.** Symptom: a sanity check that
  rejects the right answer. `6x6` has fewer than `5x5`.

## Acceptance checklist

- [ ] Unwarped counts: `0→1`, `1→1`, `2→0`, `3→0`, `4→2`, `5→10`, `6→4`.
- [ ] The warped rack has strictly fewer arrangements than the same rack clean.
- [ ] No sensor ever lands on a warped slat.
- [ ] No two sensors share a column, a `col - row` or a `col + row`.
- [ ] A rack warped along a whole row returns 0 and `first` returns `None`.
- [ ] A warped slat off the rack raises `ValueError`.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Report the count for every warped-slat *count* from 0 to 6, choosing the slats
  at random with a fixed seed, and describe the shape of the curve. It is not
  monotone in the way people expect.
- Allow **two** sensors per row and say precisely which of your three sets stops
  being usable, and why.
- Find a set of four warped slats on a 6×6 rack that leaves exactly one
  arrangement. Being able to search *for a rack* rather than on one is a
  different skill and a good use of the counter you just wrote.
