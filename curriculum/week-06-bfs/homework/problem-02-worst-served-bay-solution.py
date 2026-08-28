"""problem-02-worst-served-bay-solution.py — the bay the forklifts hate.

A distribution shed. `D` marks a loading dock, `.` marks a storage bay, `#`
marks a stanchion the forklifts drive around. A forklift crosses one square
at a time, north, south, east or west.

The shift planner wants the one bay that is worst off: the bay whose nearest
dock is furthest away. A bay no dock can reach at all is worse than any
distance, so it wins outright.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import deque
from typing import NamedTuple

# ---- Given data ----
# Two docks on the left wall. The right-hand aisle is long, and the corner
# room behind the stanchions has no way in at all.
SHED: tuple[str, ...] = (
    "D.........",
    "..........",
    "...#####..",
    "...#...#..",
    "...#...#..",
    "...#####..",
    "..........",
    "..........",
    "D.........",
    "..........",
)

DRIVE: tuple[tuple[int, int], ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))
UNREACHED = -1


class Bay(NamedTuple):
    """The worst-served bay in the shed."""

    row: int
    column: int
    squares: int


# ---- Your task ----
def worst_served_bay(shed: tuple[str, ...]) -> Bay | None:
    """Return the storage bay whose nearest dock is furthest away.

    Args:
        shed: The rows of the shed plan. `D` is a dock, `.` is a storage
            bay, `#` is a stanchion.

    Returns:
        A `Bay` holding its row, its column, and how many squares the
        forklift drives to the nearest dock. A bay no dock can reach is
        reported with `squares` of -1 and beats every reachable bay, because
        "no route" is a worse problem than a long one. The lowest row wins a
        tie, and then the lowest column, so the answer does not depend on
        the order the search happened to run in.

        None when the shed has no storage bays at all — with or without
        docks, there is then nothing to be worst.
    """
    if not shed or not shed[0]:
        return None

    rows, columns = len(shed), len(shed[0])
    squares = [[UNREACHED] * columns for _ in range(rows)]
    queue: deque[tuple[int, int]] = deque()
    for row in range(rows):
        for column in range(columns):
            if shed[row][column] == "D":
                squares[row][column] = 0
                queue.append((row, column))

    while queue:
        row, column = queue.popleft()
        for down, across in DRIVE:
            next_row, next_column = row + down, column + across
            if (
                0 <= next_row < rows
                and 0 <= next_column < columns
                and shed[next_row][next_column] == "."
                and squares[next_row][next_column] == UNREACHED
            ):
                squares[next_row][next_column] = squares[row][column] + 1
                queue.append((next_row, next_column))

    worst: Bay | None = None
    for row in range(rows):
        for column in range(columns):
            if shed[row][column] != ".":
                continue
            here = Bay(row, column, squares[row][column])
            if worst is None or _worse(here, worst):
                worst = here
    return worst


def _worse(candidate: Bay, best: Bay) -> bool:
    """Return True when `candidate` is a worse-served bay than `best`.

    Args:
        candidate: The bay being considered.
        best: The worst bay found so far.

    Returns:
        True if the candidate should replace it. Unreachable beats every
        distance; otherwise the larger distance wins, and neither row nor
        column is consulted, because the outer scan already visits bays in
        row-then-column order and only a strict improvement replaces.
    """
    if best.squares == UNREACHED:
        return False
    if candidate.squares == UNREACHED:
        return True
    return candidate.squares > best.squares


# ---- Self-check ----
if __name__ == "__main__":
    worst = worst_served_bay(SHED)
    print(f"worst bay: row {worst.row}, column {worst.column}")
    print(f"drive    : {worst.squares} squares" if worst.squares != UNREACHED else "drive    : no route")

    # The walled room is unreachable, so it wins however short the drive to
    # the rest of the shed is. Row 3, column 4 is its top-left corner.
    assert worst == Bay(3, 4, UNREACHED)

    # Take the stanchions away and the answer becomes a real distance: the
    # far corner of the middle of the right-hand wall, equidistant-ish from
    # both docks.
    open_shed = tuple(row.replace("#", ".") for row in SHED)
    open_worst = worst_served_bay(open_shed)
    assert open_worst == Bay(4, 9, 13)

    # One dock in a corner: the opposite corner is worst, and the drive is
    # the two side lengths added together.
    assert worst_served_bay(("D...", "....", "....")) == Bay(2, 3, 5)

    # No docks: every bay is unreachable and the lowest row and column wins.
    assert worst_served_bay(("...", "...")) == Bay(0, 0, UNREACHED)

    # No bays: nothing to report.
    assert worst_served_bay(("D#", "#D")) is None
    assert worst_served_bay(()) is None
    assert worst_served_bay(("",)) is None

    print("All checks passed.")
