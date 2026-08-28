"""exercise-02-hoist-route-solution.py — how many moves the gantry hoist needs.

A warehouse floor drawn as rows of text. A dot is a clear bay the hoist can
sit over; a hash is racking it cannot cross. The hoist moves one bay at a
time, north, south, east or west. This counts the fewest moves from one bay
to another, and says so plainly when there is no way through.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import deque

# ---- Given data ----
# The main floor. The racking spirals inward, so the bay in the middle is a
# long way from the door even though it looks close.
FLOOR: tuple[str, ...] = (
    "..........",
    ".########.",
    ".#......#.",
    ".#.####.#.",
    ".#.#..#.#.",
    ".#.#.##.#.",
    ".#.#....#.",
    ".#.######.",
    ".#........",
    "..........",
)

# A floor with one bay walled off on every side.
SEALED: tuple[str, ...] = (
    ".....",
    ".###.",
    ".#.#.",
    ".###.",
    ".....",
)

MOVES: tuple[tuple[int, int], ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))


# ---- Your task ----
def check_floor(floor: tuple[str, ...]) -> tuple[int, int]:
    """Return the floor's size, refusing a floor that is not a rectangle.

    Args:
        floor: The rows of the floor plan.

    Returns:
        A pair: how many rows and how many columns.

    Raises:
        ValueError: If the floor has no rows, no columns, or rows of
            different lengths.
    """
    if not floor or not floor[0]:
        raise ValueError("the floor plan is empty")
    width = len(floor[0])
    if any(len(row) != width for row in floor):
        raise ValueError("the floor plan is ragged")
    return len(floor), width


def hoist_moves(
    floor: tuple[str, ...], start: tuple[int, int], target: tuple[int, int]
) -> int | None:
    """Return the fewest moves from `start` to `target`, or None if boxed in.

    Args:
        floor: The rows of the floor plan. A dot is clear, a hash is racking.
        start: The (row, column) the hoist parks on now.
        target: The (row, column) it has to reach.

    Returns:
        The number of moves, counting each one-bay step as one move. Zero
        when `start` and `target` are the same bay. None when no run of clear
        bays joins them.

    Raises:
        ValueError: If the plan is empty or ragged, if either bay is off the
            floor, or if either bay is racking.
    """
    rows, columns = check_floor(floor)
    for name, (row, column) in (("start", start), ("target", target)):
        if not (0 <= row < rows and 0 <= column < columns):
            raise ValueError(f"{name} {(row, column)} is off the floor")
        if floor[row][column] != ".":
            raise ValueError(f"{name} {(row, column)} is racking, not a bay")

    queue = deque([(start, 0)])
    reached = {start}
    while queue:
        (row, column), moves = queue.popleft()
        if (row, column) == target:
            return moves
        for down, across in MOVES:
            step = (row + down, column + across)
            if (
                0 <= step[0] < rows
                and 0 <= step[1] < columns
                and floor[step[0]][step[1]] == "."
                and step not in reached
            ):
                reached.add(step)
                queue.append((step, moves + 1))
    return None


# ---- Self-check ----
if __name__ == "__main__":
    door = (0, 0)
    middle = (4, 4)
    print(f"door to middle : {hoist_moves(FLOOR, door, middle)} moves")
    print(f"middle to door : {hoist_moves(FLOOR, middle, door)} moves")
    print(f"door to door   : {hoist_moves(FLOOR, door, door)} moves")
    print(f"into the pocket: {hoist_moves(SEALED, (0, 0), (2, 2))}")

    assert hoist_moves(FLOOR, door, middle) == 32
    assert hoist_moves(FLOOR, middle, door) == 32  # a route is a route either way
    assert hoist_moves(FLOOR, door, door) == 0
    assert hoist_moves(FLOOR, door, (0, 9)) == 9  # straight along the top
    assert hoist_moves(SEALED, (0, 0), (2, 2)) is None

    for bad_start, bad_target, fragment in (
        ((0, 0), (99, 0), "off the floor"),
        ((1, 1), (0, 0), "is racking"),
    ):
        try:
            hoist_moves(FLOOR, bad_start, bad_target)
        except ValueError as error:
            assert fragment in str(error)
        else:
            raise AssertionError("expected ValueError")

    for bad_floor, fragment in ((), "is empty"), (("..", "..."), "is ragged"):
        try:
            hoist_moves(bad_floor, (0, 0), (0, 1))
        except ValueError as error:
            assert fragment in str(error)
        else:
            raise AssertionError("expected ValueError")

    print("All checks passed.")
