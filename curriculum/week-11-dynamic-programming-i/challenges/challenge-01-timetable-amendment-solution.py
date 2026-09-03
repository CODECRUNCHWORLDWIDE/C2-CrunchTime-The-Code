"""challenge-01-timetable-amendment-solution.py - the cheapest amendment slip.

A branch line publishes a timetable as a sequence of station codes. When the
timetable changes, the operator does not reprint it; they issue an amendment
slip listing the edits a guard must make by hand:

    INSERT a station     costs 3   (a new stop has to be advertised)
    REMOVE a station     costs 2   (a stop is struck through)
    REPLACE a station    costs 4   (struck through and rewritten)
    KEEP a station       costs 0

The costs are not equal, and that is the whole problem. Two amendments with the
same NUMBER of edits can cost different amounts, so counting edits gives the
wrong answer. A guard wants the cheapest slip, and they want to read it - so the
answer is the list of edits, not a number.

  amendment_cost   - the cheapest total
  amendment_slip   - the edits themselves, in reading order
  slip_report      - both, for a few timetables

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

INSERT_COST = 3
REMOVE_COST = 2
REPLACE_COST = 4

# ---- Given data ----
OLD_LINE: tuple[str, ...] = ("BRY", "CRB", "DNM", "ELV", "FNW")
NEW_LINE: tuple[str, ...] = ("BRY", "DNM", "GRV", "ELV", "FNW")


# ---- Your task ----
def _table(old: tuple[str, ...], new: tuple[str, ...]) -> list[list[int]]:
    """Cheapest cost to turn old[:row] into new[:col], for every row and col.

    The table is (len(old) + 1) by (len(new) + 1). Row 0 is "the old timetable
    is empty", so every entry is the cost of inserting that many stations;
    column 0 is the mirror.

    Args:
        old: The published timetable.
        new: The timetable it must become.

    Returns:
        The full cost table. Returning the table rather than one number is what
        lets the slip be reconstructed afterwards.
    """
    rows, cols = len(old) + 1, len(new) + 1
    cost = [[0] * cols for _ in range(rows)]

    for row in range(1, rows):
        cost[row][0] = cost[row - 1][0] + REMOVE_COST
    for col in range(1, cols):
        cost[0][col] = cost[0][col - 1] + INSERT_COST

    for row in range(1, rows):
        for col in range(1, cols):
            if old[row - 1] == new[col - 1]:
                # A station that stays is free, and taking it is never worse
                # than paying to replace it with itself.
                cost[row][col] = cost[row - 1][col - 1]
                continue
            cost[row][col] = min(
                cost[row - 1][col - 1] + REPLACE_COST,
                cost[row - 1][col] + REMOVE_COST,
                cost[row][col - 1] + INSERT_COST,
            )
    return cost


def amendment_cost(old: tuple[str, ...], new: tuple[str, ...]) -> int:
    """The cheapest total cost of amending `old` into `new`."""
    return _table(old, new)[len(old)][len(new)]


def amendment_slip(old: tuple[str, ...], new: tuple[str, ...]) -> list[str]:
    """The cheapest amendment, as instructions a guard can follow.

    Walks the cost table backwards from the far corner. At each step it asks
    which neighbour the cost actually came from - that is why the table is
    needed and a single running total would not do.

    Args:
        old: The published timetable.
        new: The timetable it must become.

    Returns:
        The edits in reading order, one line each. KEEP lines are included:
        a guard reading the slip needs to see the stations they are not
        touching, or they lose their place.
    """
    cost = _table(old, new)
    row, col = len(old), len(new)
    steps: list[str] = []

    while row > 0 or col > 0:
        if row > 0 and col > 0 and old[row - 1] == new[col - 1] \
                and cost[row][col] == cost[row - 1][col - 1]:
            steps.append(f"KEEP    {old[row - 1]}")
            row, col = row - 1, col - 1
        elif row > 0 and col > 0 and cost[row][col] == cost[row - 1][col - 1] + REPLACE_COST:
            steps.append(f"REPLACE {old[row - 1]} -> {new[col - 1]}")
            row, col = row - 1, col - 1
        elif row > 0 and cost[row][col] == cost[row - 1][col] + REMOVE_COST:
            steps.append(f"REMOVE  {old[row - 1]}")
            row -= 1
        else:
            steps.append(f"INSERT  {new[col - 1]}")
            col -= 1

    # Built from the far corner backwards, so the slip is reversed at the end.
    steps.reverse()
    return steps


def slip_report(pairs: list[tuple[tuple[str, ...], tuple[str, ...]]]) -> None:
    """Print the cost and the slip for each pair of timetables."""
    for old, new in pairs:
        print(f"    {' '.join(old) or '(empty)'}  ->  {' '.join(new) or '(empty)'}")
        print(f"        cost {amendment_cost(old, new)}")
        for step in amendment_slip(old, new):
            print(f"        {step}")
        print()


# ---- Self-check ----
if __name__ == "__main__":
    print("amendment slips")
    slip_report([
        (OLD_LINE, NEW_LINE),
        (("BRY", "CRB"), ("BRY", "CRB")),
        (("BRY", "CRB"), ()),
        ((), ("BRY", "CRB")),
    ])

    # The shipped pair: CRB is struck through, GRV is added. Two edits, and the
    # costs differ, so 2 + 3 = 5.
    assert amendment_cost(OLD_LINE, NEW_LINE) == 5
    slip = amendment_slip(OLD_LINE, NEW_LINE)
    assert slip.count("REMOVE  CRB") == 1
    assert slip.count("INSERT  GRV") == 1
    # Every station appears on the slip exactly once as KEEP, or is edited.
    assert len(slip) == 6

    # Identical timetables need no amendment at all.
    assert amendment_cost(OLD_LINE, OLD_LINE) == 0
    assert all(step.startswith("KEEP") for step in amendment_slip(OLD_LINE, OLD_LINE))

    # Empty on either side is the pure insert or pure remove cost.
    assert amendment_cost((), ("BRY", "CRB")) == 2 * INSERT_COST
    assert amendment_cost(("BRY", "CRB"), ()) == 2 * REMOVE_COST
    assert amendment_cost((), ()) == 0
    assert amendment_slip((), ()) == []

    # The costs being unequal is the whole point: replacing one station costs 4,
    # but removing it and inserting the other costs 2 + 3 = 5, so REPLACE wins.
    assert amendment_cost(("AAA",), ("BBB",)) == REPLACE_COST
    assert amendment_slip(("AAA",), ("BBB",)) == ["REPLACE AAA -> BBB"]

    # Make replacing dearer than the pair and the cheapest slip changes shape.
    # This is why a solution that hardcodes "one edit" is wrong.
    assert REMOVE_COST + INSERT_COST == 5 > REPLACE_COST

    # A slip always reconstructs the new timetable when a guard follows it.
    for old, new in ((OLD_LINE, NEW_LINE), (("A", "B", "C"), ("B", "C", "D")),
                     ((), ("X",)), (("X",), ())):
        rebuilt: list[str] = []
        for step in amendment_slip(old, new):
            head = step.split()[0]
            if head == "KEEP":
                rebuilt.append(step.split()[1])
            elif head == "INSERT":
                rebuilt.append(step.split()[1])
            elif head == "REPLACE":
                rebuilt.append(step.split()[-1])
            # REMOVE contributes nothing
        assert tuple(rebuilt) == new, (old, new, rebuilt)

    print("All checks passed.")
