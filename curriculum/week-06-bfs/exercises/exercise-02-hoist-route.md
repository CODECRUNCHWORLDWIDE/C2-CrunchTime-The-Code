# Exercise 2 — Hoist Route

> **Topic:** shortest route across a grid with obstacles, carrying the distance on the queue
> **Lecture:** [02 — Grid BFS and Graph BFS](../lecture-notes/02-grid-bfs-and-graph-bfs.md)
> **Difficulty:** Medium
> **Target time:** 40 minutes
> **Why this one:** the grid is the shape most interview graph problems arrive in, and it arrives without an edge list — you have to *see* that a square's neighbours are the four squares next to it. This page also teaches the bounds check properly, because Python's negative indexing means a missing bounds check does not crash: it wraps round to the far side of the floor and quietly answers a different question.

## The Brief

A warehouse has a gantry hoist that slides over the floor on rails. The floor
is drawn as rows of text, one character per bay:

```
.  a clear bay — the hoist can sit over it
#  racking — the hoist cannot cross it
```

The hoist moves one bay at a time: north, south, east or west. No diagonals,
because the two rails move one at a time.

Count the **moves**, not the bays. Standing still is 0 moves. Going next door
is 1 move. Five bays in a row is 4 moves. Counting bays instead of moves is
the classic off-by-one on this kind of problem, and the page's data is chosen
so that the two numbers are never accidentally the same.

The floor you are given is a spiral. From the corner by the door the middle
looks close — four bays down and four across — but the racking coils round,
so the hoist has to go all the way out, all the way round, and all the way
back in. Read the plan and you can see it; that is the point of a plan.

Three answers your function has to give:

- **A number** when a route exists.
- **`None`** when there is none. Not `-1`, not `0`, not an exception. `None`
  is Python's word for "there is no answer", and a caller writing
  `if moves is None:` reads exactly like the sentence it means. Returning
  `-1` would work too, right up to the day somebody adds it to a total.
- **`ValueError`** when the question itself is broken: an empty plan, a
  ragged plan whose rows are different lengths, a bay off the edge of the
  floor, or a start or target sitting on racking. Those are not "no route" —
  they are "that is not a floor" or "that is not a bay", and telling them
  apart matters when the plan comes out of a file somebody edited.

## Starter

Create `exercise-02-hoist-route.py` in your practice repo and paste this in.
Fill in every `TODO`.

```python
"""exercise-02-hoist-route.py — how many moves the gantry hoist needs.

A warehouse floor drawn as rows of text. A dot is a clear bay the hoist can
sit over; a hash is racking it cannot cross. The hoist moves one bay at a
time, north, south, east or west. Count the fewest moves from one bay to
another, and say so plainly when there is no way through.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
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
    # TODO: refuse an empty plan, then refuse a ragged one
    ...


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
    # TODO: check the floor, then check both bays are on it and are clear
    # TODO: deque of ((row, column), moves) seeded with (start, 0)
    # TODO: a `reached` set holding start
    # TODO: pop; if this is the target, return the moves stored with it
    # TODO: for each of the four MOVES: in bounds? clear? not reached yet?
    #       then mark it reached and append it with moves + 1
    # TODO: fall out of the loop -> return None
    ...


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
```

Three ideas you need before you start.

**The grid is a graph, and nobody wrote it down.** In Exercise 1 the network
came as a dictionary. Here it does not. A bay's neighbours are the four bays
touching it, and you work them out with arithmetic every time you need them.
Nothing is stored. That is called an **implicit graph**, and most grid
problems are one.

**Coordinates are `(row, column)`, and row counts downward.** `(0, 0)` is the
top-left. Going "down the page" means `row + 1`. If you slip into thinking of
them as `(x, y)` you will swap the axes somewhere, and on a square floor the
mistake is invisible until it is not.

**Negative indexes do not raise in Python.** `"abcdef"[-1]` is `"f"`. So on a
grid, a missing bounds check does not crash — the hoist steps off the left
edge and reappears on the right, and your program answers a question about a
different floor. Check `0 <= row < rows` *before* you look the bay up, every
single time.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-06-bfs/exercises/exercise-02-hoist-route.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `check_floor` returns `(rows, columns)` and raises `ValueError` on a plan
   with no rows, no columns, or rows of unequal length.
2. `hoist_moves` returns the number of **moves**, which is one less than the
   number of bays the hoist sits over on the way.
3. `hoist_moves(FLOOR, (0, 0), (0, 0))` returns `0`.
4. `hoist_moves(SEALED, (0, 0), (2, 2))` returns `None`.
5. A start or target off the floor raises `ValueError` whose message contains
   `off the floor` and names which of the two was wrong.
6. A start or target on racking raises `ValueError` whose message contains
   `is racking`.
7. The hoist moves in four directions only. Diagonals are not moves.
8. Both functions keep their type hints and their docstrings.

## Constraints

- **Check bounds before you index, not after.** `floor[-1][3]` is a real bay
  on the bottom row and Python will hand it to you without a word. Put the
  two range tests first in the `and` chain so they run before the lookup
  does — Python stops at the first false test, so a bay off the floor never
  reaches the character lookup at all.

- **Store the move count on the queue, beside the bay.** Push
  `((row, column), moves)` and read both back out. The alternative — a
  separate dictionary of distances — also works, and Exercise 3 uses it
  because there the map *is* the answer. Here the answer is one number about
  one bay, so carrying it along is simpler and there is no second structure
  to keep in step.

- **Mark a bay reached at the moment you queue it.** Same rule as Exercise 1,
  and on a grid it bites harder: a bay in the middle of an open floor has
  four neighbours, so marking late can put four copies of it in the queue
  before any of them is dealt with.

- **Check for the target when you take a bay *off* the queue, not when you
  put it on.** Both work on this page, and checking on the way in is even a
  little faster. But taking it off is the version that keeps working when the
  problem grows a rule — a cost, a budget, a state — because then "reached"
  and "settled" stop being the same thing. Challenge 2 is that problem. Learn
  the shape that survives.

- **Keep the four directions in one named tuple at the top.** `MOVES` is
  given to you already. Four `if` blocks that each hand-write an offset are
  four places for a typo, and the day the hoist gets diagonals you would edit
  four blocks instead of one line.

- **Do not mutate `floor` to mark visits.** It is a tuple of strings, so you
  cannot anyway — and that is on purpose. Overwriting the plan to record
  where you have been is a real technique, it saves the reached set, and it
  destroys the caller's data. Use a set until somebody asks you not to.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
door to middle : 32 moves
middle to door : 32 moves
door to door   : 0 moves
into the pocket: None
All checks passed.
```

Thirty-two moves. Trace it on the plan with a finger: out along the top row
to the far corner, down the right-hand edge, back along row 8, up the column
at index 2, along row 2, down the column at index 7, along row 6, and finally
up to the middle. Eight straight runs. The straight-line distance from
`(0, 0)` to `(4, 4)` is eight moves, so the racking costs you four times the
journey.

The last line is `None`, printed as the word `None`, because that is what
`print` does with it. If yours prints `-1` you have chosen a different
contract from the one the requirements ask for.

## Steps

1. Create the file, paste the starter, and run it. It fails immediately.
   Good.
2. Write `check_floor` first and test it on its own with `()`, `("",)`,
   `("..", "...")` and `FLOOR`. Three raises and one `(10, 10)`.
3. Write the two guards in `hoist_moves` — off the floor, then on racking —
   before you write any searching. Run the two `ValueError` self-checks and
   get them passing while the search still returns nothing.
4. Now the search, but **without** the reached set on purpose. Run it. It
   hangs, or eats memory until you stop it. That is a cycle: two bays keep
   putting each other back in the queue forever. Stop it with Ctrl-C and read
   the traceback for where it was.
5. Add the reached set, in the right place. It finishes.
6. Check `32`, not `33`. If you get `33` you counted bays; the fix is that
   the start goes on the queue with `0`, not `1`.
7. Delete the two bounds tests on purpose and run again. You get a number,
   and it is smaller — the hoist wrapped round the edge. Put them back and
   remember what a missing bounds check *looks* like, because it does not
   look like an error.
8. When `All checks passed.` prints, draw your own floor plan as a tuple of
   strings and check a route you can count by hand.

## The Solution

```python
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
```

**The queue carries a pair, and the pair is the point.**

```python
queue = deque([(start, 0)])
```

Every entry is a bay and the number of moves it took to get there. When a bay
comes off the front, its number came with it, so there is nothing to look up
and nothing to keep in step. Push a neighbour with `moves + 1` and the
arithmetic is done.

This works because of the queue's order, not in spite of it. Bays leave the
queue in non-decreasing order of moves — 0, then all the 1s, then all the 2s
— so the first time the target comes off the front, no shorter route to it
exists. If a shorter one did, it would have come off earlier.

**The guards run before the search, and they run on both bays.**

```python
for name, (row, column) in (("start", start), ("target", target)):
```

Looping over the pair `("start", start), ("target", target)` writes the check
once and applies it twice, and the name goes into the message, so the error
says *which* bay was wrong. Two copy-pasted blocks would do the same job
until somebody fixed a bug in one of them.

The order inside matters too: off-the-floor is tested first, because the
racking test indexes into the plan and would raise the wrong exception — or
worse, silently read the far side of the floor — on a bay that is not there.

**The bounds check and the lookup are one `and` chain, in that order.**

```python
if (
    0 <= step[0] < rows
    and 0 <= step[1] < columns
    and floor[step[0]][step[1]] == "."
    and step not in reached
):
```

Python evaluates `and` left to right and stops at the first false part. So
`floor[step[0]][step[1]]` never runs for a bay off the floor. Reorder those
four lines and you get the wrap-around bug — no exception, no warning, just a
smaller number than the truth. The `not in reached` test goes last because it
is the only one that touches a set, and there is no point hashing a tuple you
have already ruled out.

**`None` and `-1` are not the same answer.** `None` cannot be added to, cannot
be compared with `<` by accident, and reads as the sentence "there is no
route". `-1` is a number that behaves like a number: put it in a `sum` and it
quietly shortens your total. The one cost of `None` is that callers must
write `if moves is None`, and that is a cost worth paying.

**Falling out of the `while` *is* the no-route answer.** The queue empties
when there is nothing new left to reach. No flag, no counter, no special
case: `return None` after the loop is reached exactly when the target was
never dequeued. That is why the sealed pocket needs no code of its own.

**Why 32 and not 8.** Nothing in the algorithm knows what a spiral is. It
reaches every bay it can, in order of distance, and stops when it meets the
target. The racking is not an obstacle the code steps around; it is simply a
set of bays that fail the `== "."` test and are never queued. That is the
whole trick with grids — the shape of the answer comes out of the data, and
the code stays four lines long.

## Download and run

Download
[exercise-02-hoist-route-solution.py](./exercise-02-hoist-route-solution.py)
and run it:

```bash
python exercise-02-hoist-route-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-02-hoist-route.py`.

## Common bugs to catch

- **The answer comes back `33`.** No exception. You seeded the queue with
  `(start, 1)`, counting bays instead of moves:

  ```text
  door to middle : 33 moves
  ```

  The hoist sits over 33 bays on the way, and makes 32 moves between them.
  Standing still is the test: `hoist_moves(FLOOR, door, door)` must be `0`,
  and with the wrong seed it is `1`.

- **The answer is smaller than it should be, with no error.** You dropped a
  bounds check. `floor[-1][4]` is a bay on the bottom row, so the hoist steps
  off the top of the plan and lands at the bottom:

  ```text
  door to middle : 12 moves
  ```

  Nothing raises, because negative indexing is a feature. This is the most
  expensive bug on the page precisely because it looks like a working
  program. Both range tests, before the lookup, always.

- **`IndexError: string index out of range`.** You checked the low end but
  not the high end:

  ```text
  Traceback (most recent call last):
      floor[step[0]][step[1]] == "."
      ~~~~~~~~~~~~~~^^^^^^^^^
  IndexError: string index out of range
  ```

  Walking off the *right* edge does raise, because `"abcdefghij"[10]` has no
  wrap-around to hide behind. So the low-side bug is silent and the high-side
  bug is loud — which is why people fix the loud one and ship the quiet one.

- **The program never finishes.** You left out the reached set. Two
  neighbouring bays put each other back in the queue forever, and the queue
  grows until memory runs out. Interrupt it and look at the queue's length in
  the traceback; a number in the millions on a hundred-bay floor is the tell.

- **`TypeError: unhashable type: 'list'`.** You stored the bay as
  `[row, column]`:

  ```text
  Traceback (most recent call last):
      seen.add([0, 1])
      ~~~~~~~~^^^^^^^^
  TypeError: unhashable type: 'list'
  ```

  A set needs things that cannot change after they go in. Use a tuple:
  `(row, column)`. This is the reason grid coordinates are tuples everywhere
  in this week's code.

- **`AttributeError: 'list' object has no attribute 'popleft'`.** The queue
  is a list:

  ```text
  Traceback (most recent call last):
      queue.popleft()
      ^^^^^^^^^^^^^
  AttributeError: 'list' object has no attribute 'popleft'
  ```

  On a hundred-bay floor the list version would give the right answer at a
  speed nobody could measure. Exercise 4 is where that stops being true.

- **The sealed pocket returns `0`.** You returned `moves` from inside the
  neighbour loop rather than after the pop, so the first bay examined looked
  like a match. Check the target on the way *out* of the queue.

## Under the hood

<details>
<summary>Under the hood — the cost of a grid search, and the two ways to carry the distance</summary>

**Cost.** Call the floor `R` rows by `C` columns. Every bay joins the queue
at most once, because the reached set says so, so there are at most `R × C`
pops. Each pop looks at four neighbours, and four is a constant. Total time
`O(R × C)` — you touch each bay a fixed number of times. Memory is the same
order: the reached set can hold every bay, and on a wide open floor the queue
can hold a whole diagonal band of them at once.

That "at most once" is doing real work in the argument. Take the reached set
away and the bound is gone entirely — the search does not slow down, it never
stops.

**Where the constant hides.** Four neighbours per bay is `O(1)`, but a
tuple gets built, hashed and thrown away for every one of them. On a
thousand-by-thousand floor that is four million hashes. If you ever need to
make a grid search genuinely fast, that is where the time is, and the fix is
to hold the reached marks in a list of bytearrays indexed by row and column
rather than a set of tuples. It is uglier and about three times quicker. Do
not reach for it until something is actually slow.

**Distance on the queue, or distance in a dict?** Both are correct and you
should be able to say why you picked one.

```python
queue = deque([(start, 0)])            # this page
```

```python
distance = {start: 0}                  # the other way
queue = deque([start])
...
distance[step] = distance[bay] + 1
```

The dict version gives you the distance to *every* bay for free, which is
exactly what Exercise 3 wants and this page does not. It also merges two jobs
into one structure: `distance` doubles as the reached set, since a bay is in
it if and only if it has been queued. The pair version keeps the answer local
and is easier to read when there is only one target. Pick by what the answer
looks like, not by taste.

**Why no diagonals is a real decision.** Allow diagonals and every move still
costs 1, so the search is unchanged — you just add four more offsets to
`MOVES`. But the *meaning* changes: a diagonal move covers more floor than a
straight one, so "fewest moves" and "shortest distance travelled" stop being
the same question. Breadth-first search answers the first. If somebody asks
for the second, every move no longer costs the same, and you need a different
algorithm.

</details>

## Acceptance checklist

- [ ] `python exercise-02-hoist-route.py` prints four lines then
      `All checks passed.`
- [ ] The output matches the expected block character for character.
- [ ] `hoist_moves(FLOOR, (0, 0), (0, 0))` is `0`, not `1`.
- [ ] Both range tests come before the character lookup in the same `and`
      chain.
- [ ] The reached set is added to at the moment of queueing.
- [ ] The target check happens after the pop, not before the push.
- [ ] The sealed pocket returns `None`, and the word `None` is what prints.
- [ ] `ValueError` messages name which bay was wrong and why.
- [ ] Both functions have type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 6 exercise 2: hoist route`.

## Stretch

- **Return the route, not just its length.** Remember which bay you came
  from, then walk backwards from the target.

  ```python
  def hoist_route(
      floor: tuple[str, ...], start: tuple[int, int], target: tuple[int, int]
  ) -> list[tuple[int, int]] | None:
      """Return the bays the hoist sits over, start first, or None."""
      check_floor(floor)
      rows, columns = check_floor(floor)
      came_from: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
      queue = deque([start])
      while queue:
          bay = queue.popleft()
          if bay == target:
              route = []
              while bay is not None:
                  route.append(bay)
                  bay = came_from[bay]
              return route[::-1]
          for down, across in MOVES:
              step = (bay[0] + down, bay[1] + across)
              if (
                  0 <= step[0] < rows
                  and 0 <= step[1] < columns
                  and floor[step[0]][step[1]] == "."
                  and step not in came_from
              ):
                  came_from[step] = bay
                  queue.append(step)
      return None
  ```

  ```text
  33 bays, 32 moves
  first five: [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
  ```

  `came_from` replaces the reached set outright — a bay is in it exactly when
  it has been queued — which is the same merge the *Under the hood* block
  describes for the distance dict.

- **Give the hoist diagonals and see the spiral collapse.**

  ```python
  EIGHT = MOVES + ((-1, -1), (-1, 1), (1, -1), (1, 1))
  ```

  ```text
  four ways : 32 moves
  eight ways: 20 moves
  ```

  The algorithm did not change at all. Only the tuple did. That is what it
  means for the neighbour rule to be the one thing a grid problem varies.

- **Find the furthest bay from the door.** One search answers it for every
  bay at once, which is the shape Exercise 3 builds on.

  ```python
  def furthest_bay(floor: tuple[str, ...], start: tuple[int, int]) -> tuple[tuple[int, int], int]:
      """Return the reachable bay needing the most moves, and that count."""
      rows, columns = check_floor(floor)
      distance = {start: 0}
      queue = deque([start])
      while queue:
          bay = queue.popleft()
          for down, across in MOVES:
              step = (bay[0] + down, bay[1] + across)
              if (
                  0 <= step[0] < rows
                  and 0 <= step[1] < columns
                  and floor[step[0]][step[1]] == "."
                  and step not in distance
              ):
                  distance[step] = distance[bay] + 1
                  queue.append(step)
      return max(distance.items(), key=lambda pair: (pair[1], pair[0]))
  ```

  ```text
  ((4, 5), 33)
  ```

  Not the middle — the bay next to it. The spiral's dead end is one move
  further in than its centre.

When your route is right, move on to
[Exercise 3 — Siren Reach](./exercise-03-siren-reach.md).
