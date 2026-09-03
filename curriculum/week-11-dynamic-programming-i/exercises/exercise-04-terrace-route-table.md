# Exercise 4 — The Terrace Route Table

> Topic: counting paths on a grid, three ways · Lecture: [2](../lecture-notes/02-2d-dp-and-the-grid-and-string-shapes.md) · Difficulty: Beginner-Medium · Target time: 35 minutes · Why this one: it is the exercise where memoisation stops being a slogan and becomes a number you can read.

## The Brief

A hillside vineyard is laid out as a grid of terrace plots. A picker starts at
the north-west plot, ends at the south-east one, and may step only **south or
east** — never back up the slope. Some plots are washed out and cannot be
entered at all.

Return the whole **table** of counts, not just the final number: entry
`[row][col]` is how many distinct routes reach that plot. A washed-out plot
holds `0`.

Returning the table rather than the total is deliberate. The total tells you the
answer; the table shows you the recurrence, and you can check it by eye against
the slope printed beside it.

## Starter

`exercise-04-terrace-route-table-solution.py` sits beside this page with the
slope and the self-checks.

```text
.......
..#....
.....#.
...#...
.......
#......
```

Six terraces of seven plots, four washed out. Count the routes to the plot at
row 1, column 3 by hand before you start — it is small enough to do on paper and
it will tell you immediately whether you have the recurrence the right way round.

## Requirements

1. `route_table(rows)` returns the full grid of counts as a list of lists.
2. `route_count(rows)` returns the count for the south-east plot.
3. Three implementations, all agreeing: plain recursion, the same recursion
   under `functools.cache`, and a bottom-up table.
4. The file **reports the work each one does** — recursive calls for the first
   two, cells filled for the third.
5. `check_slope(rows)` raises `ValueError` for an empty slope, a ragged one, or
   a plot mark that is neither `.` nor `#`, and names the offending row.

## Constraints

- **South and east only.** No diagonal step, and no stepping back.
- **A washed-out plot holds 0**, and it is not a special case in the
  recurrence — it is the recurrence with the plot's own contribution removed.
- **The start plot may itself be washed out.** Then every count is 0, including
  the start, and no exception is raised: an impossible slope is a legitimate
  answer.
- The three implementations must produce **identical** tables. If they do not,
  the disagreement is the exercise.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-04-terrace-route-table-solution.py
slope     route counts
.......     1    1    1    1    1    1    1
..#....     1    2    0    1    2    3    4
.....#.     1    3    3    4    6    0    4
...#...     1    4    7    0    6    6   10
.......     1    5   12   12   18   24   34
#......     0    5   17   29   47   71  105

routes to the south-east plot = 105

on a clear 9 by 9 slope there are 12870 routes
naive recursion  calls  = 71499
cached recursion calls  = 97
bottom-up table  cells  = 81

route_count(('..', '..'))   = 2
route_count(('.#', '#.'))   = 0
route_table(('#.', '..'))   = [[0, 0], [0, 0]]
route_count(('.' * 10,) * 10) = 48620
empty     slope raises ValueError: a slope needs at least one plot
ragged    slope raises ValueError: row 1 is 2 plots wide, expected 1
bad mark  slope raises ValueError: unknown plot mark 'x'; use '.' or '#'
All checks passed.
```

The three call counts are the point of the whole exercise:

```
naive recursion  calls  = 71499
cached recursion calls  = 97
bottom-up table  cells  = 81
```

Same answer, same recurrence, three orders of magnitude apart. The naive version
recomputes the same plots over and over; the cache computes each plot once; the
table computes each plot once and does not pay for the call. Quote those three
numbers in your write-up — they are more convincing than the phrase
"exponential to polynomial".

## Steps

1. Read the self-checks. They are the spec.
2. Write `check_slope` first. Every later function assumes a rectangle of legal
   marks, and validating once at the edge is cheaper than guarding everywhere.
3. Write the naive recursion. Get the six-by-seven slope right before anything
   else.
4. Add `functools.cache` — one decorator — and print the call count. That
   contrast is the exercise.
5. Write the bottom-up table. Fill row by row and check it against the printed
   grid by eye.
6. Assert all three agree, then write the FRAME pass.

## The Solution

```python
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
```

The counting decorator is deliberately crude: it wraps the function and bumps an
attribute. A cleverer instrument would measure the instrument. The point is the
ratio between three numbers, and the ratio survives a crude counter.

## Download and run

Download the solution beside this page and run it:

```bash
python exercise-04-terrace-route-table-solution.py
```

No third-party packages, no arguments, no input. It prints the slope with its
route table, the three work counts, the small cases, and then
`All checks passed.`

Or open it in the browser IDE from the Run button on the block above and wash
out a different plot.

## Common bugs to catch

- **Adding the washed-out plot's own count.** Symptom: routes appear to pass
  through a plot that cannot be entered. A washed-out plot contributes 0 to its
  neighbours *and* holds 0 itself.
- **Seeding the first row and column before checking them.** Symptom: a route
  count that walks straight through a washed-out plot on the top edge. The edges
  are the recurrence too, not a separate rule.
- **Caching on a mutable argument.** Symptom: `TypeError: unhashable type`. The
  slope is a tuple of strings for exactly this reason.
- **Counting calls after the cache decorator.** Symptom: the naive and cached
  counts come out identical. Order the decorators so the counter sees every
  call, not just the misses.
- **Treating a washed-out start as an error.** Symptom: `ValueError` where the
  answer is a table of zeros.

## Acceptance checklist

- [ ] All three implementations return identical tables.
- [ ] The south-east plot on the shipped slope reports 105 routes.
- [ ] A clear 9×9 slope reports 12870.
- [ ] The three work counts are printed and quoted in the write-up.
- [ ] `('.#', '#.')` reports 0 routes, and `('#.', '..')` a table of zeros.
- [ ] Empty, ragged and bad-mark slopes each raise `ValueError` naming the row.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Return the number of routes **and** one of them. Reconstructing a path from a
  count table is a different skill and it is what the follow-up question asks.
- Allow a third step direction — south-east diagonally — and say what changes in
  the recurrence and what changes in the counts.
- Make the slope 30×30 and run the naive version. Do not wait for it; work out
  from the call count on 9×9 what you would be waiting for, and put that number
  in your Examine (cost) section.
