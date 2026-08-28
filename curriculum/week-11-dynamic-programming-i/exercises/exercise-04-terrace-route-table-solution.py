"""exercise-04-terrace-route-table-solution.py — routes across a terraced slope.

A hillside vineyard is laid out as a grid of terrace plots. A picker starts at
the north-west plot, ends at the south-east one, and may only step south or
east. Some plots are washed out and cannot be entered at all.

`route_table` returns the whole grid of counts: entry [row][col] is the number
of distinct routes from the start to that plot. A washed-out plot holds 0.

The file shows the same count three ways — plain recursion, the same recursion
with `functools.cache`, and a bottom-up table — and prints the call counts that
separate them.
"""

from __future__ import annotations

import functools

OPEN = "."
WASHED_OUT = "#"

# The Kelbray slope: six terraces of seven plots, four of them washed out.
SLOPE = (
    ".......",
    "..#....",
    ".....#.",
    "...#...",
    ".......",
    "#......",
)


def count_calls(func):
    """Wrap `func` so `func.calls` counts how many times its body ran."""

    @functools.wraps(func)
    def wrapper(*args):
        wrapper.calls += 1
        return func(*args)

    wrapper.calls = 0
    return wrapper


def check_slope(rows: tuple[str, ...]) -> None:
    """Reject a slope that is not a rectangle of open and washed-out plots.

    Raises:
        ValueError: If the slope is empty, ragged, or holds an unknown mark.
    """
    if not rows or not rows[0]:
        raise ValueError("a slope needs at least one plot")
    width = len(rows[0])
    for index, row in enumerate(rows):
        if len(row) != width:
            raise ValueError(f"row {index} is {len(row)} plots wide, expected {width}")
        for mark in row:
            if mark not in (OPEN, WASHED_OUT):
                raise ValueError(f"unknown plot mark {mark!r}; use '.' or '#'")


def naive_route_count(rows: tuple[str, ...]) -> int:
    """Count routes to the south-east plot, remembering nothing."""

    @count_calls
    def routes_to(row: int, col: int) -> int:
        if row < 0 or col < 0 or rows[row][col] == WASHED_OUT:
            return 0
        if row == 0 and col == 0:
            return 1
        return routes_to(row - 1, col) + routes_to(row, col - 1)

    total = routes_to(len(rows) - 1, len(rows[0]) - 1)
    naive_route_count.calls = routes_to.calls
    return total


def cached_route_count(rows: tuple[str, ...]) -> int:
    """The same recursion, with every plot's answer written down once."""

    @functools.cache
    @count_calls
    def routes_to(row: int, col: int) -> int:
        if row < 0 or col < 0 or rows[row][col] == WASHED_OUT:
            return 0
        if row == 0 and col == 0:
            return 1
        return routes_to(row - 1, col) + routes_to(row, col - 1)

    total = routes_to(len(rows) - 1, len(rows[0]) - 1)
    cached_route_count.calls = routes_to.__wrapped__.calls
    return total


def route_table(rows: tuple[str, ...]) -> list[list[int]]:
    """Return the route count for every plot on the slope.

    Args:
        rows: The slope, north row first. Each row is a string of '.' for an
            open plot and '#' for a washed-out one. All rows are the same
            length.

    Returns:
        A list of lists the same shape as `rows`. Entry [row][col] is the
        number of distinct south-or-east routes from the north-west plot to
        that plot. Washed-out plots hold 0, and so does every plot when the
        start itself is washed out.

    Raises:
        ValueError: If the slope is empty, ragged, or holds an unknown mark.
    """
    check_slope(rows)
    height, width = len(rows), len(rows[0])
    table = [[0] * width for _ in range(height)]

    for row in range(height):
        for col in range(width):
            if rows[row][col] == WASHED_OUT:
                continue  # stays 0: no route ends on a plot you cannot enter
            if row == 0 and col == 0:
                table[row][col] = 1
                continue
            from_north = table[row - 1][col] if row > 0 else 0
            from_west = table[row][col - 1] if col > 0 else 0
            table[row][col] = from_north + from_west
    return table


def route_count(rows: tuple[str, ...]) -> int:
    """The number of routes all the way to the south-east plot."""
    return route_table(rows)[-1][-1]


def _report() -> None:
    """Print the table, the call counts, and the checks."""
    table = route_table(SLOPE)
    print("slope     route counts")
    for row, counts in zip(SLOPE, table):
        cells = " ".join(f"{value:>4}" for value in counts)
        print(f"{row}  {cells}")

    print()
    print(f"routes to the south-east plot = {route_count(SLOPE)}")

    # The blow-up is easiest to see on a slope with nothing washed out.
    clear = ("." * 9,) * 9
    naive = naive_route_count(clear)
    cached = cached_route_count(clear)
    print()
    print(f"on a clear 9 by 9 slope there are {route_count(clear)} routes")
    print(f"naive recursion  calls  = {naive_route_count.calls}")
    print(f"cached recursion calls  = {cached_route_count.calls}")
    print(f"bottom-up table  cells  = {9 * 9}")
    assert naive == cached == route_count(clear)
    assert naive_route_count(SLOPE) == cached_route_count(SLOPE) == route_count(SLOPE)

    print()
    assert route_table((".",)) == [[1]]
    assert route_table(("#",)) == [[0]]
    assert route_count(("..", "..")) == 2
    assert route_count((".#", "..")) == 1
    assert route_count(("..", "#.")) == 1
    assert route_count((".#", "#.")) == 0          # walled off completely
    assert route_table(("#.", "..")) == [[0, 0], [0, 0]]  # start washed out
    assert route_count(("." * 8,)) == 1            # one terrace, one route
    assert route_count(("." * 1,) * 8) == 1        # one column, one route
    print("route_count(('..', '..'))   =", route_count(("..", "..")))
    print("route_count(('.#', '#.'))   =", route_count((".#", "#.")))
    print("route_table(('#.', '..'))   =", route_table(("#.", "..")))
    print("route_count(('.' * 10,) * 10) =", route_count(("." * 10,) * 10))

    for bad, why in [((), "empty"), ((".", ".."), "ragged"), (("x",), "bad mark")]:
        try:
            route_table(bad)
        except ValueError as problem:
            print(f"{why:<9} slope raises ValueError: {problem}")

    print("All checks passed.")


if __name__ == "__main__":
    _report()
