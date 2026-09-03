# Challenge 2 — Tide Gate

> **Topic:** when a cell is not a state, and what has to go in the visited set instead
> **Lecture:** [02 — Grid BFS and Graph BFS](../lecture-notes/02-grid-bfs-and-graph-bfs.md)
> **Difficulty:** Hard
> **Target time:** 90 minutes
> **Why this one:** every grid problem so far has had one fact per square — reached or not. Add a budget and that stops being true: arriving at a junction with two lifts left and arriving with none are different situations, and a search that cannot tell them apart returns a wrong answer with no error and no warning. This page ships the wrong version alongside the right one so you can watch it disagree.

## The Brief

A tidal drainage network, drawn as rows of text:

```
S  the boat, where the trip starts
F  the pump house, where it ends
.  open channel
#  bank
G  a lift gate
```

The boat moves one square at a time, north, south, east or west. A gate can
be passed, but the keeper has to lift it, and there are only so many lifts
left in the day. Passing one **spends a lift**. The budget is a number you
are given.

Return the fewest moves from the boat to the pump house, or `None` when the
budget does not stretch to it.

Here is the whole difficulty, and it is worth reading twice.

On the chart in the starter there are two ways to the junction at `(0, 4)`.
The short way runs straight along the top through the gate at `(0, 2)`: four
moves, one lift. The long way goes down, along the bottom and back up: eight
moves, no lifts. Past the junction there is a second gate at `(0, 5)`, and
the pump house is behind it.

With two lifts, the short way wins: six moves.

With **one** lift, the short way is a trap. It gets you to the junction
quickest and leaves you with nothing to open the second gate. The right
answer is the long way — ten moves — and a search that recorded "I have
reached `(0, 4)`" without recording "…with one lift already spent" will never
find it. It marked the junction the first time it arrived, so the slower,
cheaper arrival is thrown away, and the function returns `None` on a chart
where a route plainly exists.

The fix is one word in the definition of a state. A state is not a square. A
state is **a square together with how many lifts have been spent getting to
it**. Two arrivals at the same square with different budgets are two
different states, and the search has to keep both.

The rest of the contract:

- `tide_moves(chart, lifts)` returns an `int` or `None`.
- A negative budget raises `ValueError`; so does an empty chart, a ragged
  chart, or a chart that does not carry exactly one `S` and exactly one `F`.
- A budget larger than the number of gates is not an error and changes
  nothing.
- The file also ships `moves_ignoring_the_budget`, which is the wrong search,
  kept on purpose so the self-check can show the two disagreeing.

## Starter

Create `challenge-02-tide-gate.py` in your practice repo and paste this in.
Fill in every `TODO`.

```python
"""challenge-02-tide-gate.py — crossing a drainage network with a lift budget.

A tidal drainage chart. `S` is the boat, `F` is the pump house, `.` is open
channel, `#` is bank, and `G` is a lift gate. A gate opens for you, but the
keeper only has so many lifts left in the day, so passing one spends part of
a budget.

The twist is that a cell is not one place. Arriving at a junction with two
lifts left and arriving with none left are two different situations, and a
search that cannot tell them apart gets the wrong answer. The state is
`(row, column, lifts spent)`.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
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
    # TODO: refuse an empty chart, then a ragged one
    # TODO: one scan collecting every 'S' and every 'F'
    # TODO: refuse anything but exactly one of each, saying how many there were
    ...


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
    # TODO: refuse a negative budget, then read the chart
    # TODO: the state is (row, column, spent) — seed with (boat, 0) at 0 moves
    # TODO: `seen` holds STATES, not cells
    # TODO: entering a 'G' costs a lift; skip the step if that busts the budget
    ...


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
    # TODO: copy your tide_moves and change `seen` to hold cells only
    ...


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
```

One idea, and it is the only new one this week.

**A state is whatever you have to know to decide what happens next.** On the
earlier grid pages that was the square, and nothing else — so the square was
the state, and the visited set held squares. Here, standing on a square with
two lifts left and standing on the same square with none are two different
situations with different futures. So the state is the pair, and the visited
set holds pairs.

Ask yourself the question in that form on every problem: *if I told you only
this, could you work out what my options are?* If the answer is no, you have
not got the whole state yet.

## Requirements

1. `read_chart` returns `(rows, columns, boat, pump)` and raises `ValueError`
   for an empty chart, a ragged chart, or one without exactly one `S` and one
   `F`. The message says how many marks it found.
2. `tide_moves` returns the fewest moves, or `None`.
3. Entering a `G` square spends exactly one lift. Leaving one spends nothing.
4. A step that would spend more lifts than the budget is not taken.
5. `tide_moves(chart, -1)` raises `ValueError` containing
   `cannot be negative`.
6. The visited set holds `(row, column, spent)` triples.
7. `moves_ignoring_the_budget` is the same search with a cell-only visited
   set, and disagrees with `tide_moves` on `CHART` at a budget of one.
8. Every function keeps its type hints and its docstring.

## Constraints

- **The visited set holds states, not squares.** This is the page. A
  cell-only set is smaller and faster and wrong, and it is wrong in the worst
  way available: it returns a plausible answer on most inputs and a wrong one
  on the input that matters.

- **Spend the lift on the move that *enters* the gate.** Not on leaving it,
  not on both. Pick one and write it in the docstring, because a reader
  cannot tell from the code which convention you chose and the two give
  different answers on a chart that starts on a gate.

- **Check the budget before adding the state, not after.** `next_spent >
  lifts` means the step is illegal, so it never becomes a state at all.
  Queueing it and filtering later means the visited set fills with states
  that could never be used.

- **Every move still costs one.** A gate costs a lift, not extra moves. That
  is what keeps this a breadth-first problem: the queue's order is only
  meaningful while every step is the same size. If passing a gate cost two
  moves this algorithm would return a wrong answer, and the fix would be a
  different algorithm entirely — worth saying out loud in an interview
  because it shows you know why the queue works.

- **Do not try to be clever about which route is better.** There is no rule
  like "always prefer the route with lifts left" — the ten-move answer at a
  budget of one *is* the route that saved its lift, and the six-move answer
  at a budget of two *is* the route that spent one early. The search finds
  both because it keeps both. Pruning by a heuristic here is how the bug gets
  reintroduced after you have fixed it.

- **Keep the wrong version in the file.** It is four lines different and it
  is the page's evidence. Delete it and the only thing proving the state
  matters is a paragraph of prose.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
lifts 0: state search None   cell-only None   same
lifts 1: state search   10   cell-only None   WRONG
lifts 2: state search    6   cell-only    6   same
lifts 3: state search    6   cell-only    6   same
walled off: None
All checks passed.
```

Line two is the whole challenge in one row. Both searches are given one lift.
The correct one finds a ten-move route. The cell-only one says there is no
route at all.

Trace what the wrong search did. It set off, reached `(0, 1)`, opened the
gate at `(0, 2)` because it could, and arrived at the junction `(0, 4)` after
four moves with its only lift gone. It wrote `(0, 4)` into the visited set.
Later the long way round the bottom arrived at the same junction after eight
moves with the lift still in hand — and was thrown away, because `(0, 4)` was
already visited. The second gate stayed shut and the queue emptied.

Lines one, three and four agree, which is the uncomfortable part. Three
inputs out of four give the same answer either way. A test suite built from
those three would pass.

## Steps

1. Create the file, paste the starter, and run it. It fails at the first use.
2. Write `read_chart` and get all five `ValueError` self-checks passing
   before anything else. They are the easy marks and they stop a malformed
   chart from confusing you later.
3. Now write the **wrong** version first, deliberately: cell-only visited,
   budget tracked but not remembered. Run the four budgets and look at the
   table. You will get `None` where the answer is ten.
4. Sit with that for a minute. Draw the chart on paper, mark the junction,
   and walk both routes with a finger. The point of doing it in this order is
   that the fix is obvious afterwards and mysterious before.
5. Copy it, change the visited set to hold triples, and run again. One line
   flips from WRONG to a number.
6. Check the budget arithmetic on the boundary: `tide_moves(CHART, 2)` must
   be 6, and `tide_moves(CHART, 1)` must be 10, and if you get 6 for both you
   are not spending the lift.
7. Add a third gate somewhere and predict the four answers before running.
   Predicting and being right is the test that you understand it; running and
   then explaining is not.
8. When `All checks passed.` prints, work out how many states the search can
   hold at most on this chart. Rows times columns times budget-plus-one. That
   number is the memory, and it is why a large budget is expensive.

## The Solution

```python
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
```

**One line is the difference between the two searches.**

```python
start = (boat[0], boat[1], 0)
...
state = (next_row, next_column, next_spent)
if state not in seen:
```

against the flawed version's

```python
if next_spent > lifts or (next_row, next_column) in seen:
```

Everything else in the two functions is the same. The right one asks "have I
been here *in this situation*"; the wrong one asks "have I been here". On a
chart with no gates those two questions have the same answer, which is why
the bug survives so much testing.

**Why the state is exactly `(row, column, spent)` and not more.** The test is
whether the triple determines the future. Given a square and a number of
lifts already spent, everything you can do next is fixed: the four
neighbours, whether each is bank, whether each is a gate, and whether you can
afford it. Nothing about *how* you got there matters — not the route, not the
order, not the time. So the triple is the whole state, and adding anything
else to it would only make the search slower by splitting identical
situations apart.

That is the general rule, and it is worth memorising: **the state is the
smallest thing that determines what happens next.** Too little and the search
is wrong. Too much and it is slow. This problem needs a budget; a problem
with a key that opens red doors needs the set of keys held; a problem with a
direction of travel needs the direction.

**Why the answer is still the fewest moves.** Every step, gate or not, costs
one move. So the queue still hands out states in non-decreasing order of
moves, and the first time a state reaches the pump house's square, no shorter
route exists. The budget changes which states are legal; it does not change
the order they come out in. Break that — charge two moves for a gate — and
the queue's order stops meaning anything and the answer stops being right.

**The pump-house test is on the square, not the state.**

```python
if (row, column) == pump:
    return moves
```

You have arrived when you are there, whatever you spent getting there. There
is deliberately no "…and with lifts to spare" clause; the budget's only job
is to say which moves were legal on the way.

**`read_chart` counts both marks in one pass and reports the count.** Saying
`the chart carries 2 'S' marks, not 1` tells the reader what to look for.
Saying `bad chart` sends them to read the whole file. The extra information
costs one f-string.

**`moves_ignoring_the_budget` earns its place.** It is not dead code — the
self-check calls it four times and asserts it is wrong exactly once. A test
that pins down *how* the wrong version fails is more useful than a comment
saying it would, because a comment cannot notice when somebody accidentally
fixes it.

## Download and run

Download
[challenge-02-tide-gate-solution.py](./challenge-02-tide-gate-solution.py)
and run it:

```bash
python challenge-02-tide-gate-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `challenge-02-tide-gate.py`.

## Common bugs to catch

- **`tide_moves(CHART, 1)` returns `None`.** No exception, and three of the
  four budgets still agree:

  ```text
  lifts 1: state search None   cell-only None   same
  ```

  Your visited set holds cells. This is the bug the page exists for. The
  tell is that a case with *fewer* resources fails while the case with more
  succeeds — real routes do not stop existing because you have less budget,
  they only get longer.

- **`tide_moves(CHART, 1)` returns `6`.** The opposite mistake: you are
  tracking the budget in the state but never actually spending it, or you
  spend it only on the second gate. Print the state as it comes off the queue
  and watch `spent` — it should reach 1 on the top route and stay 0 on the
  bottom one.

- **`tide_moves(CHART, 0)` returns a number.** The `next_spent > lifts` check
  is missing or is `>=`. With `>=` a budget of one refuses the first gate and
  everything is off by one.

- **The search never finishes on a large chart.** Your visited set holds
  states but you forgot to bound `spent`. If a gate could be re-entered and
  re-charged without limit the state space would be infinite — the
  `next_spent > lifts` test is what keeps it finite, so it is doing two jobs
  and one of them is termination.

- **`TypeError: unhashable type: 'list'`.**

  ```text
  Traceback (most recent call last):
      seen.add([0, 1])
      ~~~~~~~~^^^^^^^^
  TypeError: unhashable type: 'list'
  ```

  You built the state as a list. States go in a set, so they have to be
  tuples.

- **`IndexError: string index out of range`.**

  ```text
  Traceback (most recent call last):
      cell = chart[next_row][next_column]
             ~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  IndexError: string index out of range
  ```

  The bounds check is missing on the high side. On the low side it does not
  raise — it wraps to the far edge of the chart. Both, before the lookup.

- **The two `ValueError`s for mark counts fire on the wrong chart.** You
  checked `S` and `F` separately with two `if len(...) != 1` blocks and got
  the messages the wrong way round. The dict loop in the solution makes that
  impossible because the mark's own name goes into the message.

## Under the hood

<details>
<summary>Under the hood — how big a state space gets, and how to spot the state you are missing</summary>

**Cost.** The state space is rows times columns times budget-plus-one. On the
starter chart that is 3 x 7 x 3 = 63 states at a budget of two — small enough
to list on paper. Each state is visited at most once and looks at four
neighbours, so the search is `O(R x C x (B + 1))` in time and the same in
memory, where `B` is the budget.

The important shape there is that the budget is a **multiplier**, not an
addition. Double the budget and you double the work. That is fine for a
handful of lifts and ruinous for a budget in the thousands — at which point
the budget is not really a budget, it is a number, and the problem wants a
different technique.

**Why the budget test is also what makes it stop.** Take out
`next_spent > lifts` and the state space becomes infinite: a boat can cross a
gate, come back, cross again, and rack up `spent` for ever. Nothing repeats,
so the visited set never fires, and the search runs until memory gives out.
The check is doing two jobs — enforcing the rule, and bounding the search —
and only one of them is obvious from its name.

**How to spot a missing state, before it costs you an afternoon.** Ask the
question in this form: *if I put the boat down on this square and told you
nothing else, could you play the rest of the game?* On Exercise 2 the answer
is yes, so the square is the state. Here it is no — you would not know
whether the gate ahead is affordable — so something is missing, and the thing
missing is the budget.

The same question sorts out the whole family:

| The problem also involves | Then the state is |
|---|---|
| A number of uses of something | cell plus uses spent |
| Keys that open coloured doors | cell plus the set of keys held |
| A direction you are travelling in | cell plus heading |
| A number of turns already made | cell plus turn count |
| Whose move it is | position plus side to move |

Every one of those is the same algorithm with a wider tuple in the visited
set, and every one of them is silently wrong with a narrower one.

**Why a set of keys still works as a state.** It has to be hashable and
small. A `frozenset` of keys is hashable; a bitmask integer is hashable and
faster. With `k` key colours the state space is multiplied by `2**k`, which
is fine up to about twenty colours and hopeless after that. Knowing where
that wall is matters more than knowing the technique.

**What breaks the whole approach.** Unit cost. The queue's order only means
"fewest moves" while every move costs the same. Charge two moves for a gate
and the queue starts handing out a five-move state before a four-move one,
and the first arrival stops being the best arrival. The repair is a priority
queue instead of a plain one — a different algorithm with a different name,
and a later course. The tell that you need it is a problem where the steps
have different sizes. Say that out loud when you meet one; it is exactly the
distinction interviewers are listening for.

</details>

## Acceptance checklist

- [ ] `python challenge-02-tide-gate.py` prints five lines then
      `All checks passed.`
- [ ] The output matches the expected block character for character.
- [ ] Exactly one row of the table says WRONG, and it is the one-lift row.
- [ ] The visited set in `tide_moves` holds three-part tuples.
- [ ] The budget test rejects a step before it becomes a state.
- [ ] `tide_moves(CHART, 1)` is `10` and `tide_moves(CHART, 2)` is `6`.
- [ ] `tide_moves(CHART, -1)` raises `ValueError`.
- [ ] A chart with two `S` marks raises, and the message says `2`.
- [ ] Every function has type hints and a docstring.
- [ ] You can say, without notes, what the state is and why.
- [ ] Committed to Git with a message like `Add Week 6 challenge 2: tide gate`.

## Stretch

- **Return the route, not just the count.** Remember the state you came from,
  then walk back and drop the budget out of each step.

  ```python
  def tide_route(chart: tuple[str, ...], lifts: int) -> list[tuple[int, int]] | None:
      """Return the squares the boat crosses, start first, or None."""
      rows, columns, boat, pump = read_chart(chart)
      start = (boat[0], boat[1], 0)
      came: dict[tuple[int, int, int], tuple[int, int, int] | None] = {start: None}
      queue = deque([start])
      while queue:
          state = queue.popleft()
          row, column, spent = state
          if (row, column) == pump:
              route = []
              while state is not None:
                  route.append((state[0], state[1]))
                  state = came[state]
              return route[::-1]
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
              nxt = (next_row, next_column, next_spent)
              if nxt not in came:
                  came[nxt] = state
                  queue.append(nxt)
      return None
  ```

  ```text
  route with 1 lift : [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (1, 4), (0, 4), (0, 5), (0, 6)]
  route with 2 lifts: [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6)]
  ```

  Two genuinely different routes over the same chart. Note that `came` is
  keyed by *state*, not by square — keying it by square would lose the
  cheaper arrival exactly the way the flawed search does.

- **Ask the keeper the other question: what is the smallest budget that works
  at all?** Try each budget upward and stop at the first that succeeds.

  ```python
  def fewest_lifts(chart: tuple[str, ...]) -> int | None:
      """Return the smallest budget that reaches the pump house, or None."""
      gates = sum(row.count("G") for row in chart)
      for budget in range(gates + 1):
          if tide_moves(chart, budget) is not None:
              return budget
      return None
  ```

  ```text
  fewest lifts: 1
  ```

  The loop stops at the number of gates on the chart, and it has to: without
  that bound there is no largest budget to give up at. Worth noticing that a
  budget above the gate count can never help, which is why the bound is
  correct and not merely convenient.

- **Print the whole trade-off curve.** Moves against budget is the table the
  keeper actually wants.

  ```python
  for budget in range(5):
      print(f"budget {budget}: {tide_moves(CHART, budget)}")
  ```

  ```text
  budget 0: None
  budget 1: 10
  budget 2: 6
  budget 3: 6
  budget 4: 6
  ```

  Two lifts buy four moves; a third buys nothing. Curves like that are how an
  engineer decides what to pay for, and this one came out of running the same
  function five times.

When your state search is right, the week's homework is next:
[Week 6 homework](../homework/README.md).
