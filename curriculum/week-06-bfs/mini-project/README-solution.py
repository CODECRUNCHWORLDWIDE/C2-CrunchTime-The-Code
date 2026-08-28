"""README-solution.py — the Muster Report for a flood-response drill.

One program, three questions, one algorithm underneath all of them.

  1. The call-out. The control room keys the radio once. Which relays hear
     it, on which hop, and which ones never hear it at all?
  2. The route. How many street moves from the depot to the muster point,
     around the flooded streets?
  3. The sirens. For every open square, how long until the nearest mast
     reaches it, which square waits longest, and how many hear nothing?

Question 1 is breadth-first search over a mesh of named relays, taken one
hop at a time. Question 2 is breadth-first search over a grid of squares
from one start. Question 3 is breadth-first search over the same grid from
every mast at once. The queue, the seen-set and the loop body are the same
in all three; only the seed and the neighbour rule change.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import deque
from typing import NamedTuple

# ---- Given data ----
# The town. `D` is the depot, `M` is the muster point, `S` is a siren mast,
# `.` is a passable street, `#` is flooded or built on.
TOWN: tuple[str, ...] = (
    "D....#....S",
    ".###.#.##..",
    ".#...#..#..",
    ".#.#####.#.",
    "...#.....#.",
    "##.#.###.#.",
    "S..#.#...#.",
    ".###.#.###.",
    ".....#....M",
)

# Which relays can hear which. Terrain makes this one-way in places.
MESH: dict[str, list[str]] = {
    "CONTROL": ["NORTHGATE", "STAITHE"],
    "NORTHGATE": ["BRIDGEFOOT", "STAITHE"],
    "STAITHE": ["QUAYSIDE"],
    "BRIDGEFOOT": ["CONTROL", "MILLRACE"],
    "QUAYSIDE": ["MILLRACE"],
    "MILLRACE": [],
    "OUTMARSH": ["TIDEWELL"],
    "TIDEWELL": ["OUTMARSH"],
}

CONTROL = "CONTROL"
STREET_MOVES: tuple[tuple[int, int], ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))
PASSABLE = frozenset(".DMS")
NEVER = -1


class Coverage(NamedTuple):
    """What the siren sweep found."""

    slowest: tuple[int, int]
    seconds: int
    silent: int


# ---- Part 1: the call-out ----
def call_out(mesh: dict[str, list[str]], control: str) -> tuple[list[list[str]], list[str]]:
    """Return the hop-by-hop roster of a radio call-out, and who misses it.

    Args:
        mesh: Each relay mapped to the relays that can hear it.
        control: The call-sign that transmits first.

    Returns:
        A pair. The hops, with hop 0 holding `control` alone and each hop's
        call-signs sorted A to Z; and every call-sign the mesh mentions that
        never hears the call, also sorted.

    Raises:
        ValueError: If `control` is not a call-sign the mesh mentions.
    """
    everyone = set(mesh)
    for listeners in mesh.values():
        everyone.update(listeners)
    if control not in everyone:
        raise ValueError(f"{control!r} is not on this mesh")

    queue = deque([control])
    heard = {control}
    hops: list[list[str]] = []
    while queue:
        this_hop: list[str] = []
        for _ in range(len(queue)):  # today's hop, frozen before it grows
            sign = queue.popleft()
            this_hop.append(sign)
            for listener in mesh.get(sign, ()):
                if listener not in heard:
                    heard.add(listener)
                    queue.append(listener)
        hops.append(sorted(this_hop))
    return hops, sorted(everyone - heard)


# ---- Part 2: the route ----
def find_mark(town: tuple[str, ...], mark: str) -> tuple[int, int]:
    """Return the single square carrying `mark`.

    Args:
        town: The rows of the town plan.
        mark: The character to find.

    Returns:
        The (row, column) of that square.

    Raises:
        ValueError: If the plan carries anything other than exactly one.
    """
    found = [
        (row, column)
        for row, line in enumerate(town)
        for column, square in enumerate(line)
        if square == mark
    ]
    if len(found) != 1:
        raise ValueError(f"the plan carries {len(found)} {mark!r} marks, not 1")
    return found[0]


def street_moves(town: tuple[str, ...], start: tuple[int, int], finish: tuple[int, int]) -> int | None:
    """Return the fewest street moves from `start` to `finish`.

    Args:
        town: The rows of the town plan.
        start: The square to set off from.
        finish: The square to reach.

    Returns:
        The number of one-square moves, 0 when the two are the same square,
        or None when no run of passable squares joins them.
    """
    rows, columns = len(town), len(town[0])
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        (row, column), moves = queue.popleft()
        if (row, column) == finish:
            return moves
        for down, across in STREET_MOVES:
            step = (row + down, column + across)
            if (
                0 <= step[0] < rows
                and 0 <= step[1] < columns
                and town[step[0]][step[1]] in PASSABLE
                and step not in seen
            ):
                seen.add(step)
                queue.append((step, moves + 1))
    return None


# ---- Part 3: the sirens ----
def siren_sweep(town: tuple[str, ...]) -> tuple[list[list[int]], Coverage]:
    """Return the seconds-to-hear map and a summary of the worst of it.

    Args:
        town: The rows of the town plan. Every `S` sounds at once.

    Returns:
        A pair. The map, holding the seconds until the nearest mast reaches
        each passable square and -1 everywhere else; and a `Coverage` giving
        the passable square that waits longest (lowest row then lowest
        column wins a tie), how long it waits, and how many passable squares
        hear nothing at all.
    """
    rows, columns = len(town), len(town[0])
    seconds = [[NEVER] * columns for _ in range(rows)]
    queue: deque[tuple[int, int]] = deque()
    for row in range(rows):
        for column in range(columns):
            if town[row][column] == "S":
                seconds[row][column] = 0
                queue.append((row, column))

    while queue:
        row, column = queue.popleft()
        for down, across in STREET_MOVES:
            step_row, step_column = row + down, column + across
            if (
                0 <= step_row < rows
                and 0 <= step_column < columns
                and town[step_row][step_column] in PASSABLE
                and seconds[step_row][step_column] == NEVER
            ):
                seconds[step_row][step_column] = seconds[row][column] + 1
                queue.append((step_row, step_column))

    slowest, worst, silent = (0, 0), NEVER, 0
    for row in range(rows):
        for column in range(columns):
            if town[row][column] not in PASSABLE:
                continue
            wait = seconds[row][column]
            if wait == NEVER:
                silent += 1
            if wait > worst:
                slowest, worst = (row, column), wait
    return seconds, Coverage(slowest=slowest, seconds=worst, silent=silent)


# ---- The report ----
def muster_report(town: tuple[str, ...], mesh: dict[str, list[str]]) -> list[str]:
    """Return the finished report, one line at a time.

    Args:
        town: The rows of the town plan.
        mesh: The relay mesh.

    Returns:
        The lines of the report, ready to print or write to a file.
    """
    lines = ["MUSTER REPORT", "=" * 13, "", "1. Radio call-out"]

    hops, stranded = call_out(mesh, CONTROL)
    for number, roster in enumerate(hops):
        lines.append(f"   hop {number}: {', '.join(roster)}")
    lines.append(f"   never hears it: {', '.join(stranded) or 'nobody'}")

    depot, muster = find_mark(town, "D"), find_mark(town, "M")
    moves = street_moves(town, depot, muster)
    lines += ["", "2. Depot to muster point"]
    lines.append(f"   depot at {depot}, muster point at {muster}")
    lines.append(f"   shortest run: {moves} moves" if moves is not None else "   no way through")

    _, coverage = siren_sweep(town)
    lines += ["", "3. Siren coverage"]
    lines.append(f"   slowest square: {coverage.slowest} at {coverage.seconds} seconds")
    lines.append(f"   squares that hear nothing: {coverage.silent}")
    return lines


# ---- Self-check ----
if __name__ == "__main__":
    print("\n".join(muster_report(TOWN, MESH)))

    hops, stranded = call_out(MESH, CONTROL)
    assert hops == [
        ["CONTROL"],
        ["NORTHGATE", "STAITHE"],
        ["BRIDGEFOOT", "QUAYSIDE"],
        ["MILLRACE"],
    ]
    assert stranded == ["OUTMARSH", "TIDEWELL"]

    depot, muster = find_mark(TOWN, "D"), find_mark(TOWN, "M")
    assert depot == (0, 0) and muster == (8, 10)
    assert street_moves(TOWN, depot, muster) == 34
    assert street_moves(TOWN, depot, depot) == 0

    seconds, coverage = siren_sweep(TOWN)
    assert seconds[0][10] == 0 and seconds[6][0] == 0  # the two masts
    assert coverage.silent == 0  # every passable square hears something
    assert coverage.seconds == 16
    assert coverage.slowest == (6, 8)

    # Take the masts away and nothing is heard anywhere.
    quiet = tuple(row.replace("S", ".") for row in TOWN)
    _, quiet_coverage = siren_sweep(quiet)
    assert quiet_coverage.seconds == NEVER
    assert quiet_coverage.silent == sum(
        1 for row in quiet for square in row if square in PASSABLE
    )

    for mark in ("D", "M"):
        try:
            find_mark(("...", "..."), mark)
        except ValueError as error:
            assert "marks, not 1" in str(error)
        else:
            raise AssertionError("expected ValueError")

    try:
        call_out(MESH, "SEAWALL")
    except ValueError as error:
        assert "is not on this mesh" in str(error)
    else:
        raise AssertionError("expected ValueError")

    print("")
    print("All checks passed.")
