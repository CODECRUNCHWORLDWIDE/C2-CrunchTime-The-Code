# Week 11 — Homework

Six problems, all original, each with a runnable worked answer folded away under
it. Allow about five hours. Do each with the lectures closed; open the worked
answer only after your own version runs, or after fifteen minutes stuck on one
step.

The six cover the shapes the week teaches that the exercises did not: a 1D count
with a two-step lookahead, a grid optimised rather than counted, a 1D pass that
has to carry two states at once, and three two-string tables.

| # | Problem | Sub-shape | Est. time |
|---|---------|-----------|----------:|
| 1 | [The Ledger Ribbon](#problem-1--the-ledger-ribbon) | 1D count with a two-character lookahead | 45 min |
| 2 | [The Kiln Flue Draw](#problem-2--the-kiln-flue-draw) | The counting grid with `min` where it had `+` | 40 min |
| 3 | [The Gauge Drift Run](#problem-3--the-gauge-drift-run) | One pass carrying two states, because negatives swap them | 50 min |
| 4 | [The Stencil Match Count](#problem-4--the-stencil-match-count) | Two-string counting table | 50 min |
| 5 | [The Two-Clerk Day Book](#problem-5--the-two-clerk-day-book) | Two-string reachability, where greedy is wrong | 55 min |
| 6 | [The Paired Manifest Strike](#problem-6--the-paired-manifest-strike) | Two-string table, then one line of arithmetic | 45 min |

Every worked answer runs on its own with no arguments and no packages, and ends
by printing `All checks passed.` To run one, open its reveal, copy the code into
a file of your own, and run that file:

```bash
python problem-01-ledger-ribbon.py
```

---

## Problem 1 — The Ledger Ribbon

**The brief.** An old adding machine prints a ribbon of digits with **no
separators** between entries. Each entry is one or two digits and names a till
code from 1 to 26. No entry may start with a zero, because the machine never
printed a leading zero — so a `0` on the ribbon can only ever be the second digit
of `10` or `20`.

Count the readings that account for every digit.

**The data.** Ribbons including `1226`, `1010`, `2101`, `111111`, `27`, `06`,
`100` and `2626262626`.

**Constraints.** A reading has to account for **every** digit — no leftovers. An
unreadable ribbon has zero readings, which is a real answer.

**Answer.** Build the count left to right. The number of readings of the first
`n` digits depends on exactly two things: the count for `n - 1` digits, when the
last digit stands alone as a valid entry, and the count for `n - 2`, when the
last two digits together do. Add whichever apply.

Only those two ever matter, so the whole table is two integers rather than a
list.

`1226` reads **five** ways. `100` reads **none** — `10-0` fails because 0 is not
an entry, and `1-00` fails for the same reason twice.

**Signatures.** `is_entry(digits)`, `reading_count(ribbon)`,
`reading_table(ribbon)`, `first_dead_prefix(ribbon)`.

**Watch for.** Treating `06` as 6 — the leading zero is what makes it invalid,
and the whole zero rule follows from it. Six ones give 13 readings, which is a
Fibonacci number and a good check. But `2626262626` gives **32**, not a Fibonacci
number, because `62` is over 26 and only every other pair is an entry — worth
checking by hand, precisely because it looks like it should behave the same way.

The empty ribbon has **one** reading, the empty one. That is not a special case
to add; it is what makes the recurrence start cleanly.

<details>
<summary>Worked answer — <code>problem-01-ledger-ribbon-solution.py</code></summary>

```python
"""problem-01-ledger-ribbon-solution.py - reading an adding machine's ribbon.

An old adding machine prints a ribbon of digits with no separators between
entries. Each entry is one or two digits and names a till code from 1 to 26.
No entry may start with a zero, because the machine never printed a leading
zero - so a 0 on the ribbon can only ever be the second digit of 10 or 20.

Given a ribbon, count the readings that account for every digit.

The count is built left to right. The number of readings of the first n digits
depends on two things and nothing else: the readings of the first n-1 digits,
when the last digit stands alone as a valid entry, and the readings of the
first n-2, when the last two digits together make a valid entry. That is the
whole recurrence, and it is why one pass and two carried numbers are enough.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
# Ribbons the shop found in the back of the machine.
RIBBONS: tuple[str, ...] = (
    "1226",
    "1010",
    "2101",
    "111111",
    "27",
    "06",
    "100",
    "2626262626",
)


# ---- Your task ----
def is_entry(digits: str) -> bool:
    """Say whether `digits` is one entry the machine could have printed.

    Args:
        digits: One or two characters from the ribbon.

    Returns:
        True when the digits name a till code from 1 to 26 without a leading
        zero. "0" and "06" are both False; "6" and "06" differ because the
        machine never printed a leading zero.
    """
    if not digits or digits[0] == "0":
        return False
    return 1 <= int(digits) <= 26


def reading_count(ribbon: str) -> int:
    """Count the ways `ribbon` can be read as a run of whole entries.

    Args:
        ribbon: The printed digits, with no separators.

    Returns:
        How many readings account for every digit. Zero when no reading does -
        which is a real answer, not an error. An empty ribbon has exactly one
        reading, the empty one, which is what makes the recurrence start
        cleanly.

    Raises:
        ValueError: If the ribbon holds anything but digits.
    """
    if not ribbon.isdigit() and ribbon != "":
        raise ValueError(f"ribbon {ribbon!r} is not all digits")

    # `two_back` is the count for the ribbon two digits shorter, `one_back` for
    # one digit shorter. Only those two ever matter, so the whole table is two
    # integers rather than a list.
    two_back, one_back = 1, 1
    for index in range(1, len(ribbon) + 1):
        count = 0
        if is_entry(ribbon[index - 1]):
            count += one_back
        if index >= 2 and is_entry(ribbon[index - 2 : index]):
            count += two_back
        two_back, one_back = one_back, count
    return one_back


def reading_table(ribbon: str) -> list[int]:
    """Return the count for every prefix of `ribbon`, shortest first.

    Args:
        ribbon: The printed digits.

    Returns:
        A list of length len(ribbon) + 1. Entry k is the number of readings of
        the first k digits, so entry 0 is 1 and the last entry is the answer.
        Useful for seeing where a ribbon dies: the first 0 in this list is the
        prefix that can no longer be read at all.
    """
    counts = [1] + [0] * len(ribbon)
    for index in range(1, len(ribbon) + 1):
        if is_entry(ribbon[index - 1]):
            counts[index] += counts[index - 1]
        if index >= 2 and is_entry(ribbon[index - 2 : index]):
            counts[index] += counts[index - 2]
    return counts


def first_dead_prefix(ribbon: str) -> int | None:
    """Return the length of the shortest unreadable prefix, or None.

    Args:
        ribbon: The printed digits.

    Returns:
        The length of the shortest prefix with no reading at all, or None when
        every prefix can be read. This is what tells an operator where the
        ribbon went wrong rather than merely that it did.
    """
    for length, count in enumerate(reading_table(ribbon)):
        if count == 0:
            return length
    return None


# ---- Self-check ----
if __name__ == "__main__":
    print("RIBBON READINGS")
    for ribbon in RIBBONS:
        count = reading_count(ribbon)
        dead = first_dead_prefix(ribbon)
        note = "" if dead is None else f"   dead at prefix {dead}"
        print(f"    {ribbon:<12} {count:>4} readings{note}")
    print()

    print("PREFIX TABLE for 1226")
    for length, count in enumerate(reading_table("1226")):
        shown = "1226"[:length] or "(empty)"
        print(f"    {shown:<8} {count}")
    print()

    # 1226 reads as 1-2-2-6, 12-2-6, 1-22-6 and 12-26. Not 1-2-26, which is the
    # same as 1-2-26 already counted, and not 122-6, because 122 is over 26.
    assert reading_count("1226") == 5

    # A zero can only ever be the second digit of 10 or 20.
    assert reading_count("1010") == 1      # 10-10, and nothing else
    assert reading_count("100") == 0       # 10-0 fails; 1-00 fails
    assert reading_count("06") == 0        # no entry starts with a zero
    assert reading_count("2101") == 1      # 21-01 fails, so only 2-10-1

    # 27 cannot be one entry, so it is only 2-7.
    assert reading_count("27") == 1

    # All ones is the counting sequence this whole family is built on: the
    # count for n ones is the (n+1)th Fibonacci number.
    assert [reading_count("1" * n) for n in range(1, 8)] == [1, 2, 3, 5, 8, 13, 21]

    # Only every other pair is an entry: "26" is, "62" is not. So the count
    # doubles once per "26" and stands still in between - 2 to the power 5,
    # not a Fibonacci number. Alternating digits are worth checking by hand
    # exactly because they look like they should behave the same as "111111".
    assert reading_count("2626262626") == 32

    # The empty ribbon has one reading: the empty one. That is what makes the
    # recurrence start without a special case.
    assert reading_count("") == 1

    # The table's last entry is the answer, always.
    for ribbon in RIBBONS:
        assert reading_table(ribbon)[-1] == reading_count(ribbon)

    # A dead prefix is reported by length, so an operator knows where to look.
    assert first_dead_prefix("100") == 3
    assert first_dead_prefix("06") == 1
    assert first_dead_prefix("1226") is None

    # Anything that is not digits is refused rather than guessed at.
    for bad in ("12a6", "1 2"):
        try:
            reading_count(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad!r}")

    print("All checks passed.")
```

</details>
---

## Problem 2 — The Kiln Flue Draw

**The brief.** A bottle kiln is packed as a grid of shelves, each costing a
known number of fuel units. The flue draws from the top-left shelf to the
bottom-right one, and heat only moves **down or right**. Find the cheapest draw —
the total fuel of the shelves the heat passes through, both ends included.

**The data.**

```text
 1   3   1   8
 1   5   1   2
 4   2   1   9
 7   6   3   1
```

**Constraints.** Greedy fails on the **first step**. Down from the corner costs 1
and right costs 3, so a greedy fireman goes down — and the cheapest draw goes
right, along the top row to the cheap third column.

**Answer.** This is [Exercise 4](../exercises/exercise-04-terrace-route-table.md)
with one thing changed. There the answer was how many routes exist and the two
routes arriving at a shelf were combined with `+`; here it is the best one, so
they are combined with `min`. The row-by-row fill, the special first row and
column, the single pass — all identical.

Naming that one line is the whole write-up.

Cheapest draw on this kiln: **11 fuel units**, over seven shelves. The file also
ships `route_count`, which is the same fill with `+` instead of `min` and gives
**20** — so you can run both and see that the shape of a table and what you put
in it are separate decisions.

**Signatures.** `check_kiln(kiln)`, `draw_table(kiln)`, `cheapest_draw(kiln)`,
`draw_route(kiln)`, `route_count(kiln)`.

**Watch for.** Reading a neighbour that has not been filled yet. Forgetting that
the first row and first column each have only one way in. A route always passes
through `height + width - 1` shelves whatever it costs, which is a check that
does not depend on the numbers at all.

<details>
<summary>Worked answer — <code>problem-02-kiln-flue-draw-solution.py</code></summary>

```python
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
```

</details>
---

## Problem 3 — The Gauge Drift Run

**The brief.** A tide gauge is checked every day and the check records a **drift
factor** — the number the day's readings must be multiplied by to correct them. A
factor of 1 means the gauge was right. A **negative** factor means the float was
stuck upside down and the readings came out inverted.

Find the run of consecutive days whose factors multiply to the **largest**
number.

**The data.** `2, 3, -2, 4, -1, 2, 2, -3, 1, 2` — a fortnight, with three
inverted days.

**Constraints.** The factors are whole numbers, so the arithmetic stays exact. A
run of one day is allowed, so the answer is never worse than the best single
factor.

**Answer.** The trap is the negatives, and it is a good one: a running product
that is **badly negative** is one negative day away from being the best product
in the record. So tracking the best run so far is not enough.

Carry **both** the best and the worst run ending at each day. On a negative day
they swap — and both candidates must be computed from the *old* pair before
either is written back, which is one line and the most common place to get this
wrong.

**Signatures.** `worst_drift(factors)`, `worst_drift_run(factors)`,
`daily_best(factors)`.

**Watch for.** Tracking only the best: `(2, -3, -4, 1)` then comes out as 2 when
24 is right. A zero cuts the record in two — nothing multiplies across it and
survives — and when every run through it is worse, zero itself is the answer.
`worst_drift_run` is a brute force over every run, shipped so the one-pass
version has something to be checked against on every prefix rather than only on
the whole record.

<details>
<summary>Worked answer — <code>problem-03-gauge-drift-run-solution.py</code></summary>

```python
"""problem-03-gauge-drift-run-solution.py - the worst drift a gauge ever ran up.

A tide gauge is checked every day and the check writes down a drift factor: the
number the day's readings have to be multiplied by to correct them. A factor of
1 means the gauge was right. Above 1 it read low, below 1 it read high, and a
NEGATIVE factor means the float was stuck upside down and the day's readings
came out inverted.

The calibration office wants the worst stretch: the run of consecutive days
whose factors multiply to the largest number, because that is the stretch where
the uncorrected record is most wrong.

Factors here are whole numbers, so the arithmetic stays exact.

The trap is the negatives. A running product that is badly negative is one more
negative day away from being the best product in the record - so tracking the
best run so far is not enough. Both the best AND the worst have to be carried,
and on a negative day they swap.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
# A fortnight of drift factors. Day 5 is the stuck float.
DRIFT: tuple[int, ...] = (2, 3, -2, 4, -1, 2, 2, -3, 1, 2)


# ---- Your task ----
def worst_drift(factors: tuple[int, ...]) -> int:
    """Return the largest product of any run of consecutive days.

    Args:
        factors: The daily drift factors, in order. Must not be empty.

    Returns:
        The largest product achievable by multiplying one or more consecutive
        factors together. A run of one day is allowed, so the answer is never
        worse than the best single factor.

    Raises:
        ValueError: If `factors` is empty.
    """
    if not factors:
        raise ValueError("a drift record needs at least one day")

    best = worst = answer = factors[0]
    for factor in factors[1:]:
        # A negative factor turns the best run into the worst and the worst
        # into the best, so both candidates have to be computed from the OLD
        # pair before either is written back.
        candidates = (factor, best * factor, worst * factor)
        best, worst = max(candidates), min(candidates)
        answer = max(answer, best)
    return answer


def worst_drift_run(factors: tuple[int, ...]) -> tuple[int, int, int]:
    """Return the largest product and the days it runs over.

    Args:
        factors: The daily drift factors, in order. Must not be empty.

    Returns:
        A triple: the product, the first day of the run and the last, both
        counted from 1 as the office numbers them. Ties go to the earliest run,
        then to the shortest, so the answer is one run rather than a family.

    Raises:
        ValueError: If `factors` is empty.
    """
    if not factors:
        raise ValueError("a drift record needs at least one day")

    # Kept honest by brute force over every run. The one-pass version above is
    # the answer to give; this is the one to check it against, and on a record
    # of a fortnight it costs nothing.
    best_product = factors[0]
    best_span = (1, 1)
    for start in range(len(factors)):
        running = 1
        for end in range(start, len(factors)):
            running *= factors[end]
            if running > best_product:
                best_product = running
                best_span = (start + 1, end + 1)
    return best_product, best_span[0], best_span[1]


def daily_best(factors: tuple[int, ...]) -> list[tuple[int, int]]:
    """Return the best and worst run ENDING on each day.

    Args:
        factors: The daily drift factors, in order. Must not be empty.

    Returns:
        One (best, worst) pair per day. Printing this is what makes the swap on
        a negative day visible: the two columns change places.

    Raises:
        ValueError: If `factors` is empty.
    """
    if not factors:
        raise ValueError("a drift record needs at least one day")
    rows = [(factors[0], factors[0])]
    best = worst = factors[0]
    for factor in factors[1:]:
        candidates = (factor, best * factor, worst * factor)
        best, worst = max(candidates), min(candidates)
        rows.append((best, worst))
    return rows


# ---- Self-check ----
if __name__ == "__main__":
    print("DRIFT RECORD")
    print("    day   factor   best run ending here   worst run ending here")
    for day, ((best, worst), factor) in enumerate(zip(daily_best(DRIFT), DRIFT), start=1):
        print(f"    {day:>3}   {factor:>6}   {best:>20}   {worst:>21}")
    print()

    product, first, last = worst_drift_run(DRIFT)
    print(f"    worst drift : {product}")
    print(f"    over days   : {first} to {last}")
    print()

    # The one-pass answer and the brute-force answer must agree. That is the
    # whole claim of the one-pass version.
    assert worst_drift(DRIFT) == worst_drift_run(DRIFT)[0]

    # A single day is a valid run, so a record of one day answers itself.
    assert worst_drift((7,)) == 7
    assert worst_drift((-7,)) == -7

    # One negative day in the middle: the answer is the better of the two
    # sides, not the whole record.
    assert worst_drift((2, 3, -1, 4)) == 6

    # TWO negative days: now the whole record is the answer, because the two
    # negatives cancel. This is the case a best-only tracker gets wrong.
    assert worst_drift((2, -3, -4, 1)) == 24

    # A zero cuts the record in two - nothing multiplies across it and lives.
    assert worst_drift((2, 3, 0, 5, 6)) == 30
    # ...and when every run through it is worse, zero itself is the answer.
    assert worst_drift((-2, 0, -3)) == 0

    # All negatives, odd count: the answer drops one end.
    assert worst_drift((-2, -3, -4)) == 12

    # The one-pass and brute-force answers agree on every prefix of the record,
    # not just the whole of it. Prefixes are where a swapped best and worst
    # first shows up.
    for length in range(1, len(DRIFT) + 1):
        prefix = DRIFT[:length]
        assert worst_drift(prefix) == worst_drift_run(prefix)[0], prefix

    # An empty record is refused rather than answered with 1.
    for function in (worst_drift, worst_drift_run, daily_best):
        try:
            function(())
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError from {function.__name__}")

    print("All checks passed.")
```

</details>
---

## Problem 4 — The Stencil Match Count

**The brief.** A depot stencils long runs of characters onto crate sides. An
inspector looks for a short mark inside a run, and the mark's characters must
appear **in order but not necessarily next to each other** — the die skips.

Count how many distinct ways the mark can be picked out of the run. Two ways are
distinct when they use different positions, even if they read the same.

**The data.** Run `RABBABRAB`, mark `RAB`.

**Constraints.** Order matters and adjacency does not. `BA` is not in a run where
every `A` precedes every `B`.

**Answer.** A two-dimensional table where every entry has the same shape of
answer. To account for the first `m` characters of the mark using the first `r`
of the run, either the run's character is **not used** — which is the entry one
column left — or it **is used and matches**, which is the entry one row up and
one column left. Add them.

The empty mark is found exactly once, by taking nothing, which is what makes the
first row all ones and lets the recurrence start without a special case.

`RAB` sits inside `RABBABRAB` **eight** ways.

**Signatures.** `match_count(run, mark)`, `match_table(run, mark)`,
`first_match(run, mark)`.

**Watch for.** Filling the table in an order that reads entries not yet written.
Forgetting the "not used" branch, which is taken on *every* cell including the
matching ones. `AAA` contains `AA` three ways, not one — repeats multiply, and
that is the case to check by hand first.

<details>
<summary>Worked answer — <code>problem-04-stencil-match-count-solution.py</code></summary>

```python
"""problem-04-stencil-match-count-solution.py - how many ways a mark hides in a run.

A depot stencils long runs of characters onto crate sides. An inspector is
looking for a short mark inside a run, and the rule is that the mark's
characters must appear IN ORDER but need not be next to each other - the die
skips, so the mark can be spread across the run with other characters between.

Count how many distinct ways the mark can be picked out of the run. Two ways
are distinct when they use a different set of positions, even if they read the
same.

The table is two-dimensional and every entry has the same shape of answer: to
account for the first `m` characters of the mark using the first `r` of the
run, either the run's character is not used at all - which is the entry one
column left - or it is used and matches, which is the entry one row up and one
column left. Add them.

The row order matters. Filling the run outer and the mark inner is fine; doing
it the other way round without care reads entries that have not been written
yet, and the count comes out low with nothing to show why.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
RUN = "RABBABRAB"
MARK = "RAB"


# ---- Your task ----
def match_count(run: str, mark: str) -> int:
    """Count the ways `mark` can be picked out of `run` in order.

    Args:
        run: The stencilled run of characters.
        mark: The mark the inspector is looking for.

    Returns:
        How many distinct sets of positions in `run` spell `mark` in order.
        An empty mark is found exactly once - by taking nothing - which is what
        makes the table's first column all ones and the recurrence start
        without a special case.
    """
    # One row per mark length, one column per run length. Only the previous
    # row is ever read, so two rows would do; the whole table is kept because
    # printing it is half the exercise.
    rows, cols = len(mark) + 1, len(run) + 1
    table = [[0] * cols for _ in range(rows)]
    for col in range(cols):
        table[0][col] = 1        # the empty mark: found once, by taking nothing

    for row in range(1, rows):
        for col in range(1, cols):
            # Not using this run character: whatever the count was without it.
            table[row][col] = table[row][col - 1]
            if run[col - 1] == mark[row - 1]:
                # Using it: the count for one fewer mark character, one fewer
                # run character.
                table[row][col] += table[row - 1][col - 1]
    return table[-1][-1]


def match_table(run: str, mark: str) -> list[list[int]]:
    """Return the whole count table, for reading rather than for the answer.

    Args:
        run: The stencilled run.
        mark: The mark.

    Returns:
        A grid with len(mark) + 1 rows and len(run) + 1 columns. Entry
        [m][r] is the number of ways to pick the first m characters of the mark
        out of the first r of the run.
    """
    rows, cols = len(mark) + 1, len(run) + 1
    table = [[0] * cols for _ in range(rows)]
    for col in range(cols):
        table[0][col] = 1
    for row in range(1, rows):
        for col in range(1, cols):
            table[row][col] = table[row][col - 1]
            if run[col - 1] == mark[row - 1]:
                table[row][col] += table[row - 1][col - 1]
    return table


def first_match(run: str, mark: str) -> list[int] | None:
    """Return the earliest set of positions spelling `mark`, or None.

    Args:
        run: The stencilled run.
        mark: The mark.

    Returns:
        The positions, counted from 0, of the leftmost way to pick the mark
        out of the run - or None when the mark is not there at all. A count of
        zero and a None here always agree, and the checks assert that.
    """
    positions: list[int] = []
    cursor = 0
    for wanted in mark:
        while cursor < len(run) and run[cursor] != wanted:
            cursor += 1
        if cursor == len(run):
            return None
        positions.append(cursor)
        cursor += 1
    return positions


# ---- Self-check ----
if __name__ == "__main__":
    print(f"RUN   {RUN}")
    print(f"MARK  {MARK}")
    print()

    print("COUNT TABLE - rows are mark prefixes, columns are run prefixes")
    table = match_table(RUN, MARK)
    print("            " + "".join(f"{ch:>4}" for ch in "-" + RUN))
    for index, row in enumerate(table):
        label = ("(none)" if index == 0 else MARK[:index])
        print(f"    {label:<8}" + "".join(f"{count:>4}" for count in row))
    print()

    print(f"    ways to find {MARK} in {RUN}: {match_count(RUN, MARK)}")
    print(f"    earliest positions          : {first_match(RUN, MARK)}")
    print()

    # Worked by hand: R A B can be picked out of R A B B A B R A B in several
    # ways, and the table's bottom-right corner is the count.
    assert match_count(RUN, MARK) == match_table(RUN, MARK)[-1][-1]

    # The empty mark is found once, by taking nothing.
    assert match_count(RUN, "") == 1
    assert match_count("", "") == 1

    # A mark longer than the run cannot be found.
    assert match_count("AB", "ABC") == 0
    assert match_count("", "A") == 0

    # An exact run finds itself exactly once.
    assert match_count("RAB", "RAB") == 1

    # Repeats multiply. "AA" sits inside "AAA" three ways: positions 01, 02, 12.
    assert match_count("AAA", "AA") == 3
    assert match_count("AAAA", "AA") == 6

    # A run of one repeated character finds a mark of the same character
    # exactly as many ways as there are ways to choose those positions.
    assert match_count("AAAAA", "AAA") == 10

    # Order matters: "BA" is not in a run that only ever has A before B.
    assert match_count("AB", "BA") == 0

    # A count of zero and no first match always agree, in both directions.
    for run, mark in (("RABBABRAB", "RAB"), ("AB", "BA"), ("AB", "ABC"), ("", "A")):
        assert (match_count(run, mark) == 0) == (first_match(run, mark) is None)

    # The first match really does spell the mark, in order.
    positions = first_match(RUN, MARK)
    assert positions is not None
    assert "".join(RUN[position] for position in positions) == MARK
    assert positions == sorted(positions)

    print("All checks passed.")
```

</details>
---

## Problem 5 — The Two-Clerk Day Book

**The brief.** Two clerks share one day book. Each writes their own entries into
it as the day goes on, so the finished book holds both clerks' entries
interleaved — but **each clerk's entries appear in the order that clerk wrote
them**, because neither goes back.

Given both clerks' own records and the finished book, say whether the book could
have been produced this way.

**The data.** Clerk one `ABAB`, clerk two `AABB`, day book `AABABABB`. Plus a
second, smaller book built to catch a greedy reader: clerk one `AA`, clerk two
`AB`, book `AABA`.

**Constraints.** Neither clerk's order may change. The lengths have to add up,
which is worth checking first because it is free.

**Answer.** The obvious approach — walk the book and hand each entry to whichever
clerk has it next — is **wrong**, and wrong in a way that looks right on most
data. When both clerks are due to write the same character, choosing one commits
you.

On the trap book, the greedy reader takes both of clerk one's `A`s and then has
nothing that can write the `B`. It answers **False**; the table answers **True**.
The file ships both so you can run them side by side.

The table is the answer: entry `[a][b]` says whether the first `a` entries of
clerk one and the first `b` of clerk two could have made the first `a + b`
entries of the book. A cell is reachable when the cell above it is and clerk
one's next entry matches, or the cell to its left is and clerk two's does.

**Signatures.** `interleaves(first, second, book)`,
`interleave_table(first, second, book)`,
`greedy_interleaves(first, second, book)`, `split_book(first, second, book)`.

**Watch for.** Reaching for the greedy version because the book is short. Two
empty records make an empty book and nothing else. `split_book` walking the
finished table backwards is what turns "yes it interleaves" into "here is who
wrote each line", which is the part a clerk can act on.

<details>
<summary>Worked answer — <code>problem-05-two-clerk-daybook-solution.py</code></summary>

```python
"""problem-05-two-clerk-daybook-solution.py - did two clerks write this day book?

Two clerks share one day book. Each writes their own entries into it as the day
goes on, so the finished book holds both clerks' entries interleaved - but each
clerk's entries appear in the book in the order that clerk wrote them, because
neither clerk ever goes back.

Given the two clerks' own records and the finished day book, say whether the
book could have been produced this way.

The obvious approach - walk the book and give each entry to whichever clerk has
it next - is wrong, and it is wrong in a way that looks right on most data.
When both clerks are due to write the same character, choosing one commits you,
and the choice can be the wrong one. This file ships that greedy version on
purpose so the two can be run side by side.

The table is the answer. Entry [a][b] says whether the first a entries of clerk
one and the first b of clerk two could have made the first a+b entries of the
book. A cell is reachable when the cell above it is and clerk one's next entry
matches, or the cell to its left is and clerk two's does.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
# Each entry is one letter: the initial of the ledger it was posted to.
CLERK_ONE = "ABAB"
CLERK_TWO = "AABB"
DAY_BOOK = "AABABABB"

# The book that catches a greedy reader. Clerk one opens with two As and clerk
# two with one, and the book needs clerk one to hand over the second A. A
# reader that takes from clerk one whenever it can takes both, and then has
# nothing left that can write the B.
TRAP_ONE = "AA"
TRAP_TWO = "AB"
TRAP_BOOK = "AABA"


# ---- Your task ----
def interleaves(first: str, second: str, book: str) -> bool:
    """Say whether `book` is an interleaving of `first` and `second`.

    Args:
        first: One clerk's entries, in the order they wrote them.
        second: The other clerk's entries, in order.
        book: The finished day book.

    Returns:
        True when the book can be split into the two clerks' records without
        reordering either. False otherwise - including when the lengths do not
        add up, which is checked first because it is free.
    """
    if len(first) + len(second) != len(book):
        return False

    # reachable[b] is "the first `taken_from_first` of `first` and the first b
    # of `second` account for the book so far". One row at a time is enough,
    # because a row only ever reads itself and the row above.
    reachable = [False] * (len(second) + 1)
    reachable[0] = True
    for index in range(1, len(second) + 1):
        reachable[index] = reachable[index - 1] and second[index - 1] == book[index - 1]

    for taken in range(1, len(first) + 1):
        # Column 0: everything so far came from `first` alone.
        reachable[0] = reachable[0] and first[taken - 1] == book[taken - 1]
        for index in range(1, len(second) + 1):
            from_first = reachable[index] and first[taken - 1] == book[taken + index - 1]
            from_second = reachable[index - 1] and second[index - 1] == book[taken + index - 1]
            reachable[index] = from_first or from_second
    return reachable[-1]


def interleave_table(first: str, second: str, book: str) -> list[list[bool]]:
    """Return the whole reachability table, for reading rather than for speed.

    Args:
        first: One clerk's entries.
        second: The other clerk's entries.
        book: The finished day book.

    Returns:
        A grid with len(first) + 1 rows and len(second) + 1 columns. Entry
        [a][b] is True when the first a entries of `first` and the first b of
        `second` account for the first a + b entries of the book.

    Raises:
        ValueError: If the two records cannot possibly fill the book, because
            a table would then mean nothing.
    """
    if len(first) + len(second) != len(book):
        raise ValueError("the two records do not add up to the length of the book")
    rows, cols = len(first) + 1, len(second) + 1
    table = [[False] * cols for _ in range(rows)]
    table[0][0] = True
    for row in range(rows):
        for col in range(cols):
            if row == 0 and col == 0:
                continue
            here = row + col - 1
            if row and table[row - 1][col] and first[row - 1] == book[here]:
                table[row][col] = True
            if col and table[row][col - 1] and second[col - 1] == book[here]:
                table[row][col] = True
    return table


def greedy_interleaves(first: str, second: str, book: str) -> bool:
    """The obvious wrong answer, kept for comparison.

    Walks the book once and hands each entry to whichever clerk has it next,
    preferring the first clerk on a tie. It is fast, it is simple, and it is
    wrong whenever a tie can be resolved only one way.

    Args:
        first: One clerk's entries.
        second: The other clerk's entries.
        book: The finished day book.

    Returns:
        Its answer, which agrees with `interleaves` on most inputs and not on
        all of them.
    """
    if len(first) + len(second) != len(book):
        return False
    one = two = 0
    for entry in book:
        if one < len(first) and first[one] == entry:
            one += 1
        elif two < len(second) and second[two] == entry:
            two += 1
        else:
            return False
    return True


def split_book(first: str, second: str, book: str) -> str | None:
    """Return which clerk wrote each entry, or None when the book is impossible.

    Args:
        first: One clerk's entries.
        second: The other clerk's entries.
        book: The finished day book.

    Returns:
        A string of "1" and "2" the same length as the book, naming the clerk
        for each entry - or None when no split exists. Walks the finished table
        backwards from the bottom-right corner, so it costs nothing extra.
    """
    if len(first) + len(second) != len(book):
        return None
    table = interleave_table(first, second, book)
    row, col = len(first), len(second)
    if not table[row][col]:
        return None
    marks: list[str] = []
    while row or col:
        here = row + col - 1
        if row and table[row - 1][col] and first[row - 1] == book[here]:
            marks.append("1")
            row -= 1
        else:
            marks.append("2")
            col -= 1
    marks.reverse()
    return "".join(marks)


# ---- Self-check ----
if __name__ == "__main__":
    print("THE DAY BOOK")
    print(f"    clerk one : {CLERK_ONE}")
    print(f"    clerk two : {CLERK_TWO}")
    print(f"    day book  : {DAY_BOOK}")
    print(f"    interleaves: {interleaves(CLERK_ONE, CLERK_TWO, DAY_BOOK)}")
    split = split_book(CLERK_ONE, CLERK_TWO, DAY_BOOK)
    print(f"    who wrote  : {split}")
    print()

    print("REACHABILITY TABLE - rows are clerk one, columns are clerk two")
    print("            " + "".join(f"{ch:>3}" for ch in "-" + CLERK_TWO))
    for index, row in enumerate(interleave_table(CLERK_ONE, CLERK_TWO, DAY_BOOK)):
        label = "(none)" if index == 0 else CLERK_ONE[:index]
        print(f"    {label:<8}" + "".join(("  y" if cell else "  .") for cell in row))
    print()

    print("THE BOOK THAT CATCHES A GREEDY READER")
    print(f"    clerk one : {TRAP_ONE}")
    print(f"    clerk two : {TRAP_TWO}")
    print(f"    day book  : {TRAP_BOOK}")
    print(f"    table says : {interleaves(TRAP_ONE, TRAP_TWO, TRAP_BOOK)}")
    print(f"    greedy says: {greedy_interleaves(TRAP_ONE, TRAP_TWO, TRAP_BOOK)}")
    print()

    # The shipped day book really is an interleaving.
    assert interleaves(CLERK_ONE, CLERK_TWO, DAY_BOOK) is True

    # The trap: the table gets it right and the greedy reader does not.
    assert interleaves(TRAP_ONE, TRAP_TWO, TRAP_BOOK) is True
    assert greedy_interleaves(TRAP_ONE, TRAP_TWO, TRAP_BOOK) is False

    # Lengths that do not add up are refused before anything else.
    assert interleaves("AB", "CD", "ABC") is False
    assert interleaves("", "", "A") is False

    # Two empty records make an empty book, and nothing else.
    assert interleaves("", "", "") is True

    # One clerk writing nothing means the book is the other clerk's record.
    assert interleaves("ABC", "", "ABC") is True
    assert interleaves("ABC", "", "ACB") is False

    # Order within a clerk is never allowed to change.
    assert interleaves("AB", "CD", "ABDC") is False
    assert interleaves("AB", "CD", "ACBD") is True

    # The split really does reconstruct both records, in order.
    marks = split_book(CLERK_ONE, CLERK_TWO, DAY_BOOK)
    assert marks is not None
    one = "".join(entry for entry, mark in zip(DAY_BOOK, marks) if mark == "1")
    two = "".join(entry for entry, mark in zip(DAY_BOOK, marks) if mark == "2")
    assert one == CLERK_ONE and two == CLERK_TWO

    # An impossible book has no split, and the two agree on that.
    assert split_book("AB", "CD", "ABDC") is None
    assert interleaves("AB", "CD", "ABDC") is False

    # A table cannot be built for records that do not fit the book.
    try:
        interleave_table("AB", "CD", "ABC")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for a mismatched length")

    print("All checks passed.")
```

</details>
---

## Problem 6 — The Paired Manifest Strike

**The brief.** A cargo is listed twice — once by the shipper and once by the
receiving depot. The two disagree, and the clerk strikes lines out of each until
they read the same. Nothing may be added and nothing reordered; only whole lines
struck out.

Report the fewest strikes, counting a strike on either manifest as one.

**The data.**

```text
shipper   SALT  HIDES  TALLOW  OATS  PITCH  ROPE
depot     HIDES  SALT  OATS  TAR  ROPE
```

**Constraints.** `HIDES` is on both manifests and **cannot survive**, because it
comes before `SALT` on one and after it on the other. That is the whole reason
this is not a set intersection, and it is the first thing to check by hand.

**Answer.** The lines that survive are the same on both sides *and in the same
order* on both — the longest run common to the two manifests without needing to
be contiguous. Once that length is known the answer is one line of arithmetic:

```text
strikes = len(shipper) + len(depot) - 2 * len(common run)
```

Deriving that line is the exercise; the table under it is the ordinary two-string
fill — matching lines take the diagonal plus one, mismatching lines take the
better of up and left.

`SALT OATS ROPE` survives, so `6 + 5 - 2 × 3 = 5` strikes.

**Signatures.** `common_run(shipper, depot)`, `run_table(shipper, depot)`,
`strikes_needed(shipper, depot)`, `struck_lines(shipper, depot)`.

**Watch for.** Intersecting the two as sets, which keeps `HIDES` and gives 3.
Counting a strike on both sides as one. Identical manifests need zero strikes;
manifests with nothing in common lose everything on both sides. `struck_lines`
is the useful output — a count alone is not something a clerk can act on.

<details>
<summary>Worked answer — <code>problem-06-paired-manifest-strike-solution.py</code></summary>

```python
"""problem-06-paired-manifest-strike-solution.py - striking two manifests level.

A cargo is listed twice: once by the shipper and once by the receiving depot.
The two manifests disagree, and the clerk's job is to strike lines out of each
until the two read the same. Nothing may be added and nothing may be reordered
- only whole lines struck out.

Report the fewest strikes needed, counting a strike on either manifest as one.

The lines that survive are the same on both sides and in the same order on
both, which makes them the longest run common to the two manifests without
being contiguous. Once that length is known the answer is arithmetic: strike
everything else on both sides.

    strikes = len(shipper) + len(depot) - 2 * len(the common run)

Deriving that line is the exercise. The table underneath it is the ordinary
two-string fill: matching lines take the diagonal plus one, mismatching lines
take the better of up and left.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
SHIPPER: tuple[str, ...] = ("SALT", "HIDES", "TALLOW", "OATS", "PITCH", "ROPE")
DEPOT: tuple[str, ...] = ("HIDES", "SALT", "OATS", "TAR", "ROPE")


# ---- Your task ----
def common_run(shipper: tuple[str, ...], depot: tuple[str, ...]) -> list[str]:
    """Return the longest run of lines common to both manifests, in order.

    Args:
        shipper: The shipper's manifest, in order.
        depot: The depot's manifest, in order.

    Returns:
        The lines that survive on both sides, in the order they appear. Ties
        are broken towards the shipper's earlier lines, so the answer is one
        run rather than a family of them.
    """
    rows, cols = len(shipper) + 1, len(depot) + 1
    table = [[0] * cols for _ in range(rows)]
    for row in range(1, rows):
        for col in range(1, cols):
            if shipper[row - 1] == depot[col - 1]:
                table[row][col] = table[row - 1][col - 1] + 1
            else:
                table[row][col] = max(table[row - 1][col], table[row][col - 1])

    # Walk the finished table backwards to recover the run itself.
    run: list[str] = []
    row, col = len(shipper), len(depot)
    while row and col:
        if shipper[row - 1] == depot[col - 1]:
            run.append(shipper[row - 1])
            row -= 1
            col -= 1
        elif table[row - 1][col] >= table[row][col - 1]:
            row -= 1
        else:
            col -= 1
    run.reverse()
    return run


def run_table(shipper: tuple[str, ...], depot: tuple[str, ...]) -> list[list[int]]:
    """Return the whole length table, for reading rather than for the answer.

    Args:
        shipper: The shipper's manifest.
        depot: The depot's manifest.

    Returns:
        A grid with len(shipper) + 1 rows and len(depot) + 1 columns. Entry
        [s][d] is the length of the longest common run of the first s shipper
        lines and the first d depot lines.
    """
    rows, cols = len(shipper) + 1, len(depot) + 1
    table = [[0] * cols for _ in range(rows)]
    for row in range(1, rows):
        for col in range(1, cols):
            if shipper[row - 1] == depot[col - 1]:
                table[row][col] = table[row - 1][col - 1] + 1
            else:
                table[row][col] = max(table[row - 1][col], table[row][col - 1])
    return table


def strikes_needed(shipper: tuple[str, ...], depot: tuple[str, ...]) -> int:
    """Return the fewest line strikes that make the two manifests agree.

    Args:
        shipper: The shipper's manifest.
        depot: The depot's manifest.

    Returns:
        The number of strikes, counting one per line struck on either side.
        Zero when the manifests already agree.
    """
    return len(shipper) + len(depot) - 2 * len(common_run(shipper, depot))


def struck_lines(
    shipper: tuple[str, ...], depot: tuple[str, ...]
) -> tuple[list[str], list[str]]:
    """Return which lines are struck on each side.

    Args:
        shipper: The shipper's manifest.
        depot: The depot's manifest.

    Returns:
        A pair of lists: the shipper's struck lines and the depot's, each in
        the order they appear on that manifest. This is the part a clerk can
        act on; the count alone is not.
    """
    survivors = common_run(shipper, depot)

    def strike(manifest: tuple[str, ...]) -> list[str]:
        remaining = list(survivors)
        struck: list[str] = []
        for line in manifest:
            if remaining and line == remaining[0]:
                remaining.pop(0)
            else:
                struck.append(line)
        return struck

    return strike(shipper), strike(depot)


# ---- Self-check ----
if __name__ == "__main__":
    print("THE TWO MANIFESTS")
    print(f"    shipper : {list(SHIPPER)}")
    print(f"    depot   : {list(DEPOT)}")
    print()

    print("COMMON RUN LENGTH - rows are shipper lines, columns are depot lines")
    print("            " + "".join(f"{line[:4]:>7}" for line in ("-",) + DEPOT))
    for index, row in enumerate(run_table(SHIPPER, DEPOT)):
        label = "(none)" if index == 0 else SHIPPER[index - 1]
        print(f"    {label:<8}" + "".join(f"{value:>7}" for value in row))
    print()

    run = common_run(SHIPPER, DEPOT)
    shipper_struck, depot_struck = struck_lines(SHIPPER, DEPOT)
    print(f"    survives     : {run}")
    print(f"    strike from shipper: {shipper_struck}")
    print(f"    strike from depot  : {depot_struck}")
    print(f"    strikes needed     : {strikes_needed(SHIPPER, DEPOT)}")
    print()

    # SALT-OATS-ROPE survives on both sides. HIDES appears on both manifests
    # and cannot survive, because it is before SALT on one and after it on the
    # other - which is the whole reason this is not a set intersection.
    assert run == ["SALT", "OATS", "ROPE"]
    assert "HIDES" in SHIPPER and "HIDES" in DEPOT and "HIDES" not in run

    # 6 + 5 - 2 * 3 = 5 strikes.
    assert strikes_needed(SHIPPER, DEPOT) == 5
    assert len(shipper_struck) + len(depot_struck) == strikes_needed(SHIPPER, DEPOT)

    # Striking those lines really does leave two identical manifests.
    survivors_shipper = list(SHIPPER)
    for line in shipper_struck:
        survivors_shipper.remove(line)
    survivors_depot = list(DEPOT)
    for line in depot_struck:
        survivors_depot.remove(line)
    assert survivors_shipper == survivors_depot == run

    # Identical manifests need no strikes at all.
    assert strikes_needed(SHIPPER, SHIPPER) == 0
    assert common_run(SHIPPER, SHIPPER) == list(SHIPPER)

    # Manifests with nothing in common lose everything on both sides.
    assert strikes_needed(("A", "B"), ("C", "D")) == 4
    assert common_run(("A", "B"), ("C", "D")) == []

    # An empty manifest strikes the whole of the other one.
    assert strikes_needed((), SHIPPER) == len(SHIPPER)
    assert strikes_needed((), ()) == 0

    # Order is what makes this hard: the same lines in reverse share only one.
    assert len(common_run(("A", "B", "C"), ("C", "B", "A"))) == 1

    # A repeated line can survive more than once when both sides repeat it.
    assert common_run(("A", "A", "B"), ("A", "A", "C")) == ["A", "A"]
    assert strikes_needed(("A", "A", "B"), ("A", "A", "C")) == 2

    # The table's bottom-right corner is the length of the run, always.
    assert run_table(SHIPPER, DEPOT)[-1][-1] == len(run)

    print("All checks passed.")
```

</details>
---

## Rubric (5 axes, 4 points each)

| Axis | What "great" looks like |
|------|--------------------------|
| Frame the problem | The memo names the state — what one table entry *means*, in a sentence — and the base case, before any recurrence. |
| Reason about options | Four to six bullets before any code, with the greedy or brute-force alternative named and, where it is wrong, said to be wrong and why. |
| Assemble the solution | Idiomatic Python; the fill order stated and justified; type hints throughout. |
| Measure it | A trace on at least two inputs, one degenerate, and — where the file prints a table — the table read back in the write-up. |
| Evaluate the cost | Time, space, best/average/worst, the trade-off and the improvement. Three of these six reduce to a couple of variables; say which and why. |

Twenty points per problem, 120 for the set. Score yourself honestly; the number
is only useful if it is true.

---

## How to submit

Commit your write-ups under `frame-writeups/c2-week-11/homework/`, one file per
problem:

```
frame-writeups/c2-week-11/homework/
├── problem-1-ledger-ribbon.md
├── problem-2-kiln-flue-draw.md
├── problem-3-gauge-drift-run.md
├── problem-4-stencil-match-count.md
├── problem-5-two-clerk-daybook.md
└── problem-6-paired-manifest-strike.md
```

Each file is 100–200 lines: the five FRAME sections plus a five-line memo at the
top. The code is part of the Assemble section, not a separate file.

When the set is done, push and move on to the
[mini-project](../mini-project/README.md).

---

## Time budget

| Problem | Solve | Write-up | Total |
|---------|------:|---------:|------:|
| 1 — Ledger Ribbon | 30 min | 15 min | 45 min |
| 2 — Kiln Flue Draw | 25 min | 15 min | 40 min |
| 3 — Gauge Drift Run | 35 min | 15 min | 50 min |
| 4 — Stencil Match Count | 35 min | 15 min | 50 min |
| 5 — Two-Clerk Day Book | 40 min | 15 min | 55 min |
| 6 — Paired Manifest Strike | 30 min | 15 min | 45 min |

About four and a half hours. Problems 2, 3 and 5 are the three worth the most:
each one is a familiar algorithm with exactly one thing changed, and being able
to say **which thing** is what separates knowing a recipe from knowing a method.
