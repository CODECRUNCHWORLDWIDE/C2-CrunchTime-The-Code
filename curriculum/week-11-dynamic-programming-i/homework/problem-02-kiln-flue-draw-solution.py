"""problem-02-kiln-flue-draw-solution.py - the cheapest draw through a kiln.

A bottle kiln is packed as a grid of shelves. Each shelf holds ware that costs
a known number of fuel units to bring to temperature. The flue draws from the
top-left shelf to the bottom-right one, and heat only ever moves DOWN or RIGHT
- never back up the stack, never sideways against the draw.

The fireman wants the cheapest draw: the total fuel of the shelves the heat
passes through, including both ends.

This is the counting grid from Exercise 4 with one thing changed. There the
answer was how many routes exist; here it is the best one, so the two routes
arriving at a shelf are combined with min instead of with plus. Everything else
- the row-by-row fill, the first row and column being special, the single pass
- is identical. Saying which line changed is the whole write-up.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
# Fuel units per shelf. Rows run down the stack; columns run across it.
KILN: tuple[tuple[int, ...], ...] = (
    (1, 3, 1, 8),
    (1, 5, 1, 2),
    (4, 2, 1, 9),
    (7, 6, 3, 1),
)


# ---- Your task ----
def check_kiln(kiln: tuple[tuple[int, ...], ...]) -> None:
    """Raise unless `kiln` is a rectangle of at least one shelf.

    Args:
        kiln: The shelf costs, row by row.

    Raises:
        ValueError: If the kiln is empty, has an empty row, or is ragged.
    """
    if not kiln or not kiln[0]:
        raise ValueError("a kiln needs at least one shelf")
    width = len(kiln[0])
    if any(len(row) != width for row in kiln):
        raise ValueError("every row of the kiln must be the same width")


def draw_table(kiln: tuple[tuple[int, ...], ...]) -> list[list[int]]:
    """Return the cheapest fuel total to reach every shelf.

    Args:
        kiln: The shelf costs, row by row.

    Returns:
        A grid the same shape as `kiln`, where entry [row][col] is the cheapest
        total fuel for a draw from the top-left shelf to that one. The bottom
        right entry is the answer to the whole problem.

    Raises:
        ValueError: If the kiln is not a rectangle of at least one shelf.
    """
    check_kiln(kiln)
    height, width = len(kiln), len(kiln[0])
    table = [[0] * width for _ in range(height)]

    for row in range(height):
        for col in range(width):
            if row == 0 and col == 0:
                table[row][col] = kiln[row][col]
            elif row == 0:
                # The top row can only be reached from the left.
                table[row][col] = table[row][col - 1] + kiln[row][col]
            elif col == 0:
                # The left column can only be reached from above.
                table[row][col] = table[row - 1][col] + kiln[row][col]
            else:
                # The one line that differs from the counting version: min,
                # where that used a sum.
                table[row][col] = min(table[row - 1][col], table[row][col - 1]) + kiln[row][col]
    return table


def cheapest_draw(kiln: tuple[tuple[int, ...], ...]) -> int:
    """Return the fuel cost of the cheapest draw through the kiln.

    Args:
        kiln: The shelf costs, row by row.

    Returns:
        The total fuel of the cheapest route from top-left to bottom-right.

    Raises:
        ValueError: If the kiln is not a rectangle of at least one shelf.
    """
    return draw_table(kiln)[-1][-1]


def draw_route(kiln: tuple[tuple[int, ...], ...]) -> list[tuple[int, int]]:
    """Return the shelves the cheapest draw passes through, in order.

    Walks the finished table backwards from the bottom-right shelf, at each
    step going to whichever neighbour the table says the cheapest route came
    from. Ties go to the shelf above, so the route is one route rather than a
    family of them.

    Args:
        kiln: The shelf costs, row by row.

    Returns:
        The (row, column) pairs of the route, top-left first.

    Raises:
        ValueError: If the kiln is not a rectangle of at least one shelf.
    """
    table = draw_table(kiln)
    row, col = len(kiln) - 1, len(kiln[0]) - 1
    route = [(row, col)]
    while (row, col) != (0, 0):
        if row == 0:
            col -= 1
        elif col == 0:
            row -= 1
        elif table[row - 1][col] <= table[row][col - 1]:
            row -= 1
        else:
            col -= 1
        route.append((row, col))
    route.reverse()
    return route


def route_count(kiln: tuple[tuple[int, ...], ...]) -> int:
    """Return how many routes exist at all, ignoring cost.

    Kept beside the cheapest-draw table on purpose: it is the same fill with
    plus where the other has min, and running both is the clearest way to see
    that the shape of a table and what you put in it are separate decisions.

    Args:
        kiln: The shelf costs, row by row. Only the shape is used.

    Returns:
        The number of down-and-right routes from top-left to bottom-right.

    Raises:
        ValueError: If the kiln is not a rectangle of at least one shelf.
    """
    check_kiln(kiln)
    height, width = len(kiln), len(kiln[0])
    table = [[0] * width for _ in range(height)]
    for row in range(height):
        for col in range(width):
            if row == 0 or col == 0:
                table[row][col] = 1
            else:
                table[row][col] = table[row - 1][col] + table[row][col - 1]
    return table[-1][-1]


# ---- Self-check ----
if __name__ == "__main__":
    print("THE KILN")
    for row in KILN:
        print("    " + "  ".join(f"{cost:2d}" for cost in row))
    print()

    print("CHEAPEST TOTAL TO EACH SHELF")
    for row in draw_table(KILN):
        print("    " + "  ".join(f"{total:2d}" for total in row))
    print()

    route = draw_route(KILN)
    print(f"    cheapest draw : {cheapest_draw(KILN)} fuel units")
    print(f"    shelves passed: {len(route)}")
    print(f"    route         : {route}")
    print(f"    routes at all : {route_count(KILN)}")
    print()

    # Greedy fails here on the very first step. Down from the corner costs 1
    # and right costs 3, so greedy goes down - and the cheapest draw goes
    # right, along the top row to the cheap third column: 1,3,1,1,1,3,1 for 11.
    assert cheapest_draw(KILN) == 11

    # A route always passes through height + width - 1 shelves, whatever it
    # costs. That is a useful check because it does not depend on the costs.
    assert len(draw_route(KILN)) == len(KILN) + len(KILN[0]) - 1

    # The route the table describes really does cost what the table says.
    assert sum(KILN[row][col] for row, col in draw_route(KILN)) == cheapest_draw(KILN)

    # The route only ever steps down or right, never back.
    for (row, col), (next_row, next_col) in zip(draw_route(KILN), draw_route(KILN)[1:]):
        assert (next_row - row, next_col - col) in ((1, 0), (0, 1))

    # One shelf is its own draw.
    assert cheapest_draw(((5,),)) == 5
    assert draw_route(((5,),)) == [(0, 0)]

    # A single row or column has exactly one route, so the cheapest is the sum.
    assert cheapest_draw(((1, 2, 3),)) == 6
    assert cheapest_draw(((1,), (2,), (3,))) == 6
    assert route_count(((1, 2, 3),)) == 1

    # The same fill with plus instead of min counts routes rather than costing
    # them. On a 4x4 grid that is 20.
    assert route_count(KILN) == 20

    # A row of zeroes costs nothing, which is a real answer and not a bug.
    assert cheapest_draw(((0, 0), (0, 0))) == 0

    # Anything that is not a rectangle of shelves is refused.
    for bad in ((), ((),), ((1, 2), (3,))):
        try:
            cheapest_draw(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad!r}")

    print("All checks passed.")
