"""challenge-02-tide-gate-solution.py — crossing a drainage network with a lift budget.

A tidal drainage chart. `S` is the boat, `F` is the pump house, `.` is open
channel, `#` is bank, and `G` is a lift gate. A gate opens for you, but the
keeper only has so many lifts left in the day, so passing one spends part of
a budget.

The twist is that a cell is not one place. Arriving at a junction with two
lifts left and arriving with none left are two different situations, and a
search that cannot tell them apart gets the wrong answer. The state is
`(row, column, lifts spent)`.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import deque

# ---- Given data ----
# The short way to the junction at (0, 4) spends a lift on the gate at
# (0, 2). The long way round the bottom spends nothing. Which one is right
# depends entirely on how many lifts are left for the gate at (0, 5).
CHART: tuple[str, ...] = (
    "S.G..GF",
    ".###.##",
    ".....##",
)

# A chart where the pump house is behind a bank with no gate in it at all.
WALLED: tuple[str, ...] = (
    "S.#.F",
    "..#..",
    "..#..",
)

MOVES: tuple[tuple[int, int], ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))


# ---- Your task ----
def read_chart(chart: tuple[str, ...]) -> tuple[int, int, tuple[int, int], tuple[int, int]]:
    """Return the chart's size and the two marked cells.

    Args:
        chart: The rows of the drainage chart.

    Returns:
        Rows, columns, the boat's cell, and the pump house's cell.

    Raises:
        ValueError: If the chart is empty, ragged, or does not carry exactly
            one `S` and exactly one `F`.
    """
    if not chart or not chart[0]:
        raise ValueError("the chart is empty")
    columns = len(chart[0])
    if any(len(row) != columns for row in chart):
        raise ValueError("the chart is ragged")

    found: dict[str, list[tuple[int, int]]] = {"S": [], "F": []}
    for row, line in enumerate(chart):
        for column, cell in enumerate(line):
            if cell in found:
                found[cell].append((row, column))
    for mark, cells in found.items():
        if len(cells) != 1:
            raise ValueError(f"the chart carries {len(cells)} {mark!r} marks, not 1")
    return len(chart), columns, found["S"][0], found["F"][0]


def tide_moves(chart: tuple[str, ...], lifts: int) -> int | None:
    """Return the fewest moves from the boat to the pump house.

    Args:
        chart: The rows of the drainage chart.
        lifts: How many gate lifts the keeper has left. Passing a `G` cell
            spends one. Sitting on a gate cell costs nothing extra; the lift
            is spent on the move that enters it.

    Returns:
        The number of one-cell moves along the shortest run the budget
        allows, or None when no run reaches the pump house within it.

    Raises:
        ValueError: If the chart is unreadable, or if `lifts` is negative.
    """
    if lifts < 0:
        raise ValueError("lifts cannot be negative")
    rows, columns, boat, pump = read_chart(chart)

    start = (boat[0], boat[1], 0)
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        (row, column, spent), moves = queue.popleft()
        if (row, column) == pump:
            return moves
        for down, across in MOVES:
            next_row, next_column = row + down, column + across
            if not (0 <= next_row < rows and 0 <= next_column < columns):
                continue
            cell = chart[next_row][next_column]
            if cell == "#":
                continue
            next_spent = spent + 1 if cell == "G" else spent
            if next_spent > lifts:
                continue
            state = (next_row, next_column, next_spent)
            if state not in seen:
                seen.add(state)
                queue.append((state, moves + 1))
    return None


def moves_ignoring_the_budget(chart: tuple[str, ...], lifts: int) -> int | None:
    """The same search with a plain cell-only visited set. Kept to be wrong.

    This is the version most people write first. It records that a cell has
    been reached without recording how many lifts were left on arrival, so
    the first arrival locks out every later one — including the cheaper
    arrival that is the only one able to finish the journey.

    Args:
        chart: The rows of the drainage chart.
        lifts: How many gate lifts are left.

    Returns:
        Whatever this flawed search happens to produce.
    """
    if lifts < 0:
        raise ValueError("lifts cannot be negative")
    rows, columns, boat, pump = read_chart(chart)

    queue = deque([(boat, 0, 0)])
    seen = {boat}
    while queue:
        (row, column), spent, moves = queue.popleft()
        if (row, column) == pump:
            return moves
        for down, across in MOVES:
            next_row, next_column = row + down, column + across
            if not (0 <= next_row < rows and 0 <= next_column < columns):
                continue
            cell = chart[next_row][next_column]
            if cell == "#":
                continue
            next_spent = spent + 1 if cell == "G" else spent
            if next_spent > lifts or (next_row, next_column) in seen:
                continue
            seen.add((next_row, next_column))
            queue.append(((next_row, next_column), next_spent, moves + 1))
    return None


# ---- Self-check ----
if __name__ == "__main__":
    for budget in (0, 1, 2, 3):
        correct = tide_moves(CHART, budget)
        flawed = moves_ignoring_the_budget(CHART, budget)
        mark = "same" if correct == flawed else "WRONG"
        print(f"lifts {budget}: state search {str(correct):>4}   cell-only {str(flawed):>4}   {mark}")
    print(f"walled off: {tide_moves(WALLED, 9)}")

    # No lifts: both gates are shut, so the pump house is out of reach.
    assert tide_moves(CHART, 0) is None
    # One lift: the long way round the bottom saves it for the second gate.
    assert tide_moves(CHART, 1) == 10
    # Two lifts: straight along the top, through both gates.
    assert tide_moves(CHART, 2) == 6
    # More lifts than gates changes nothing.
    assert tide_moves(CHART, 3) == 6

    # The cell-only search agrees everywhere except the case that matters.
    assert moves_ignoring_the_budget(CHART, 0) is None
    assert moves_ignoring_the_budget(CHART, 1) is None  # wrong: the answer is 10
    assert moves_ignoring_the_budget(CHART, 2) == 6
    assert moves_ignoring_the_budget(CHART, 3) == 6

    # A bank with no gate in it is a bank, however many lifts are left.
    assert tide_moves(WALLED, 9) is None

    try:
        tide_moves(CHART, -1)
    except ValueError as error:
        assert "cannot be negative" in str(error)
    else:
        raise AssertionError("expected ValueError")

    for bad, fragment in (
        ((), "is empty"),
        (("S.F", "S.."), "2 'S' marks"),
        (("S..", "..."), "0 'F' marks"),
        (("S.F", "...."), "is ragged"),
    ):
        try:
            tide_moves(bad, 1)
        except ValueError as error:
            assert fragment in str(error), str(error)
        else:
            raise AssertionError("expected ValueError")

    print("All checks passed.")
