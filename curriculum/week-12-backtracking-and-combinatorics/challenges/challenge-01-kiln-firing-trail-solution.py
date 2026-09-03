"""challenge-01-kiln-firing-trail-solution.py - every trail that spells the schedule.

A pottery kiln holds its shelves in a grid. Each shelf carries one glaze code,
a single letter. A firing schedule is a sequence of glaze codes that must be
loaded in order, and the loader may only step between shelves that share an
edge - up, down, left or right, never diagonally - and may not put two pots on
the same shelf, so a trail never revisits a shelf.

The question is not "is there a trail?". A kiln operator already knows there is
one; they want to know HOW MANY there are, because a schedule with exactly one
trail is a schedule that cannot be loaded wrongly, and one with fourteen is a
schedule that will be.

  count_trails    - how many distinct trails spell the schedule
  first_trail     - the smallest trail in reading order, or None
  trail_report    - both, for a handful of schedules

Counting is what makes the pruning matter. A search that stops at the first hit
can be sloppy and still look right; a search that must find them all cannot.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

# ---- Given data ----
# One glaze code per shelf, top row first.
RACK: list[list[str]] = [
    ["A", "B", "C", "E"],
    ["S", "F", "E", "S"],
    ["A", "D", "E", "E"],
]

STEPS: tuple[tuple[int, int], ...] = ((-1, 0), (0, -1), (0, 1), (1, 0))


# ---- Your task ----
def _walk(
    rack: list[list[str]],
    schedule: str,
    row: int,
    col: int,
    at: int,
    used: set[tuple[int, int]],
    trail: list[tuple[int, int]],
    found: list[list[tuple[int, int]]],
) -> None:
    """Extend the trail from one shelf, recording every completion.

    Args:
        rack: The shelf grid.
        schedule: The glaze codes to spell.
        row: Current shelf row.
        col: Current shelf column.
        at: How many codes of the schedule are already spelled.
        used: Shelves already carrying a pot on this trail.
        trail: The shelves visited, in order.
        found: Every completed trail, appended to in place.
    """
    if at == len(schedule):
        found.append(list(trail))
        return

    height, width = len(rack), len(rack[0])
    for drow, dcol in STEPS:
        nrow, ncol = row + drow, col + dcol
        if not (0 <= nrow < height and 0 <= ncol < width):
            continue
        if (nrow, ncol) in used:
            continue
        # The prune that matters: reject on the CODE before recursing, not
        # inside the call. Checking after the call still works and explores a
        # whole level of shelves that could never spell anything.
        if rack[nrow][ncol] != schedule[at]:
            continue
        used.add((nrow, ncol))
        trail.append((nrow, ncol))
        _walk(rack, schedule, nrow, ncol, at + 1, used, trail, found)
        # Undo, always. The set and the list are shared across every branch, so
        # a branch that forgets to unmark poisons its siblings.
        trail.pop()
        used.discard((nrow, ncol))


def all_trails(rack: list[list[str]], schedule: str) -> list[list[tuple[int, int]]]:
    """Every trail through the rack that spells the schedule.

    Args:
        rack: The shelf grid. Must be rectangular and non-empty.
        schedule: The glaze codes to spell, in order.

    Returns:
        A list of trails, each a list of (row, column). Empty when none exists.
        An empty schedule spells nothing and has no trail - not one empty trail.

    Raises:
        ValueError: If the rack is empty or its rows differ in length.
    """
    if not rack or not rack[0]:
        raise ValueError("the rack has no shelves")
    if len({len(row) for row in rack}) != 1:
        raise ValueError("the rack is not rectangular")
    if not schedule:
        return []

    found: list[list[tuple[int, int]]] = []
    for row in range(len(rack)):
        for col in range(len(rack[0])):
            if rack[row][col] != schedule[0]:
                continue
            _walk(rack, schedule, row, col, 1, {(row, col)}, [(row, col)], found)
    return found


def count_trails(rack: list[list[str]], schedule: str) -> int:
    """How many distinct trails spell the schedule."""
    return len(all_trails(rack, schedule))


def first_trail(
    rack: list[list[str]], schedule: str
) -> list[tuple[int, int]] | None:
    """The smallest trail in reading order, or None when there is none.

    "Smallest" compares the trails as sequences of (row, column), so the trail
    starting nearest the top-left wins, and ties are broken by where it goes
    next. Naming the order matters: without it, two correct programs disagree.
    """
    trails = all_trails(rack, schedule)
    return min(trails) if trails else None


def trail_report(rack: list[list[str]], schedules: list[str]) -> None:
    """Print the count and the first trail for each schedule."""
    for schedule in schedules:
        trails = all_trails(rack, schedule)
        best = min(trails) if trails else None
        shown = " ".join(f"({r},{c})" for r, c in best) if best else "-"
        print(f"    {schedule:<6} trails {len(trails):>2}   first {shown}")


# ---- Self-check ----
if __name__ == "__main__":
    print("the rack")
    for row in RACK:
        print("    " + " ".join(row))
    print()
    print("schedules")
    trail_report(RACK, ["ABCE", "SEE", "ASA", "ABCF", "E", "SFDA"])

    # "ABCE" looks like the top row and is not only the top row: after C at
    # (0,2) the loader can drop to the E at (1,2) instead of stepping right.
    # A search that stops at its first hit reports 1 here and is wrong.
    assert count_trails(RACK, "ABCE") == 2
    assert first_trail(RACK, "ABCE") == [(0, 0), (0, 1), (0, 2), (0, 3)]

    # "SEE" starts from two different S shelves.
    assert count_trails(RACK, "SEE") == 2
    assert first_trail(RACK, "SEE") == [(1, 3), (1, 2), (2, 2)]

    # A single code is a trail of one shelf, once per matching shelf. Four
    # shelves carry E: (0,3), (1,2), (2,2) and (2,3).
    assert count_trails(RACK, "E") == 4
    assert first_trail(RACK, "E") == [(0, 3)]

    # "ASA" turns a corner and comes back down the left edge.
    assert count_trails(RACK, "ASA") == 2
    assert first_trail(RACK, "ASA") == [(0, 0), (1, 0), (2, 0)]

    # No trail at all: F sits alone, with no adjacent shelf spelling nothing.
    assert count_trails(RACK, "ABCF") == 0
    assert first_trail(RACK, "ABCF") is None

    # The empty schedule spells nothing, so there is no trail - not one empty
    # trail. Say which it is; both are defensible and only one is the contract.
    assert count_trails(RACK, "") == 0
    assert first_trail(RACK, "") is None

    # A shelf cannot carry two pots, so a schedule needing one twice in a row
    # has no trail even when the codes are adjacent.
    assert count_trails([["A", "A"]], "AAA") == 0

    # Malformed racks are refused rather than half-searched.
    for bad in ([], [[]], [["A", "B"], ["C"]]):
        try:
            all_trails(bad, "A")
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad!r}")

    print()
    print("All checks passed.")
