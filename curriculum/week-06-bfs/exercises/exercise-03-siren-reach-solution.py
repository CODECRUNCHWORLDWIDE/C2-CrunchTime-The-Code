"""exercise-03-siren-reach-solution.py — how far the flood sirens carry.

A town drawn as rows of text. `S` is a siren mast, `.` is open ground the
sound crosses, `#` is a building that blocks it. The sound spreads one square
per second in the four compass directions. This works out, for every open
square, how many seconds until it hears something — from whichever mast is
nearest, all of them sounding at once.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import deque

# ---- Given data ----
# Two masts, a terrace of buildings across the middle, and a yard behind the
# terrace that neither mast can reach.
TOWN: tuple[str, ...] = (
    "S........",
    ".........",
    "..#####..",
    "..#...#..",
    "..#.#.#..",
    "..#.#.#..",
    "..#####..",
    ".........",
    "........S",
)

BLOCKED = -1
SPREAD: tuple[tuple[int, int], ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))


# ---- Your task ----
def siren_reach(town: tuple[str, ...]) -> tuple[list[list[int]], int]:
    """Return the seconds-to-hear map, and how many squares never hear a thing.

    Args:
        town: The rows of the town plan. `S` is a mast, `.` is open ground,
            `#` is a building.

    Returns:
        A pair. The first item is a grid the same shape as `town`: a mast
        square holds 0, an open square holds the seconds until the nearest
        mast reaches it, and a building holds -1. An open square no mast can
        reach also holds -1, because "never" is not a number of seconds. The
        second item counts those unreached open squares.

        An empty town returns an empty grid and a count of zero.
    """
    if not town or not town[0]:
        return [], 0

    rows, columns = len(town), len(town[0])
    seconds = [[BLOCKED] * columns for _ in range(rows)]

    queue: deque[tuple[int, int]] = deque()
    open_squares = 0
    for row in range(rows):
        for column in range(columns):
            square = town[row][column]
            if square == "S":
                seconds[row][column] = 0
                queue.append((row, column))
            elif square == ".":
                open_squares += 1

    heard = 0
    while queue:
        row, column = queue.popleft()
        for down, across in SPREAD:
            next_row, next_column = row + down, column + across
            if (
                0 <= next_row < rows
                and 0 <= next_column < columns
                and town[next_row][next_column] == "."
                and seconds[next_row][next_column] == BLOCKED
            ):
                seconds[next_row][next_column] = seconds[row][column] + 1
                heard += 1
                queue.append((next_row, next_column))

    return seconds, open_squares - heard


def draw(seconds: list[list[int]]) -> str:
    """Return the seconds map as text, with a dash where nothing is heard.

    Args:
        seconds: The grid `siren_reach` returned.

    Returns:
        One line per row, each entry padded to two characters.
    """
    return "\n".join(
        " ".join(f"{cell:>2}" if cell != BLOCKED else " -" for cell in row)
        for row in seconds
    )


# ---- Self-check ----
if __name__ == "__main__":
    seconds, deaf = siren_reach(TOWN)
    print(draw(seconds))
    print(f"squares that never hear a siren: {deaf}")

    assert seconds[0][0] == 0 and seconds[8][8] == 0  # the masts themselves
    assert seconds[0][8] == 8  # eight squares along the top row
    assert seconds[2][2] == BLOCKED  # a corner of the terrace
    assert seconds[3][3] == BLOCKED  # open ground inside the terrace, unreached
    assert seconds[4][4] == BLOCKED  # the shed in the middle of the courtyard
    assert deaf == 7

    # Two masts beat one: the middle of the map is reached from the nearer.
    assert seconds[1][1] == 2
    assert seconds[7][7] == 2

    # No masts at all: every open square is unreached, and the count says so.
    quiet, quiet_deaf = siren_reach(("...", ".#.", "..."))
    assert quiet == [[BLOCKED] * 3, [BLOCKED, BLOCKED, BLOCKED], [BLOCKED] * 3]
    assert quiet_deaf == 8

    # One mast and nothing else.
    lone, lone_deaf = siren_reach(("S",))
    assert lone == [[0]] and lone_deaf == 0

    # An empty town.
    assert siren_reach(()) == ([], 0)
    assert siren_reach(("",)) == ([], 0)

    print("All checks passed.")
