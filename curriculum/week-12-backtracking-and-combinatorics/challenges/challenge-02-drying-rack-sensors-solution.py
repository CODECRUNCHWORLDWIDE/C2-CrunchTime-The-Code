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
