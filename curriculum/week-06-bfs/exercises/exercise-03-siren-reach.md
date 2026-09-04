# Exercise 3 — Siren Reach

> **Topic:** starting the search from every source at once, and reading a whole map of answers out of one walk
> **Lecture:** [02 — Grid BFS and Graph BFS](../lecture-notes/02-grid-bfs-and-graph-bfs.md)
> **Difficulty:** Medium
> **Target time:** 40 minutes
> **Why this one:** "how far is each thing from the nearest one of these" is one of the most common shapes a real question arrives in, and the obvious answer — search once from every source and take the smallest — is slower than it needs to be by a factor of however many sources there are. The fix is one line, in the seed. This page is where that line stops being surprising.

## The Brief

A town has flood sirens on masts. When the warning goes out, every mast
sounds at the same moment. Sound spreads down the streets one square per
second and does not go through buildings.

The plan is rows of text:

```
S  a siren mast — open ground, and a mast stands on it
.  open ground the sound crosses
#  a building the sound stops at
```

You are asked for two things.

**A map**, the same shape as the plan, saying how many seconds each square
waits before it hears anything. A mast square is `0` — it is right there. A
building is `-1`, because a building does not wait, it just does not hear.
And an open square that no mast can reach is `-1` too, because "never" is not
a number of seconds and pretending it is a very large number is how a bug
gets into a report.

**A count** of those unreachable open squares. It is the number the council
cares about, and burying it inside the map as one more `-1` would make it
invisible — you cannot tell a `-1` that means "building" from a `-1` that
means "nobody hears this" by looking.

An empty plan gives back an empty map and a count of zero. No masts at all
gives back a map of nothing but `-1`, and a count equal to every open square
on it. Both of those are ordinary answers, not errors.

Here is the idea the whole page rests on. You could work this out one mast at
a time: search from the first mast, write down every distance, search from
the second, and keep the smaller of the two numbers for each square. That is
correct, and with fifty masts it does fifty times the work.

Instead, put **all** the masts in the queue before you start. The search then
spreads out from all of them together, like several stones dropped in a pond
at once. The first time a square is reached, it is reached by whichever mast
was nearest — because the search always deals with the nearest squares first,
and it does not care which mast they came from. One walk. Every answer.

## Starter

Create `exercise-03-siren-reach.py` in your practice repo and paste this in.
Fill in every `TODO`.

```python
"""exercise-03-siren-reach.py — how far the flood sirens carry.

A town drawn as rows of text. `S` is a siren mast, `.` is open ground the
sound crosses, `#` is a building that blocks it. The sound spreads one square
per second in the four compass directions. Work out, for every open square,
how many seconds until it hears something — from whichever mast is nearest,
all of them sounding at once.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
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
    # TODO: an empty plan returns ([], 0) before anything else happens
    # TODO: build a grid of BLOCKED, one row per row, one column per column
    # TODO: one scan of the plan: every 'S' gets 0 and goes in the queue,
    #       every '.' adds one to the open-square tally
    # TODO: the usual loop — pop, look at the four neighbours, and take an
    #       open neighbour that is still BLOCKED at one second more
    # TODO: the count is the open squares minus the ones you reached
    ...


def draw(seconds: list[list[int]]) -> str:
    """Return the seconds map as text, with a dash where nothing is heard.

    Args:
        seconds: The grid `siren_reach` returned.

    Returns:
        One line per row, each entry padded to two characters.
    """
    # TODO: join each row with a space; a BLOCKED entry prints as " -"
    ...


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
```

Two things to have straight before you start.

**The seed is a list, not a single item.** Exercise 1 and Exercise 2 both put
one thing in the queue to begin with. Here you put several. Nothing else in
the loop changes — not one line. That is the whole lesson, and it is smaller
than it sounds until you try to write it the other way.

**The map doubles as the reached set.** You do not need a separate `set` on
this page. A square is "already reached" exactly when its entry is no longer
`-1`. One structure, two jobs, and no chance of the two disagreeing.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-06-bfs/exercises/exercise-03-siren-reach.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `siren_reach` returns a tuple: the map first, the count second.
2. The map has exactly as many rows as the plan, and each row has exactly as
   many entries as that row has characters.
3. Every `S` square holds `0`.
4. Every `#` square holds `-1`.
5. An open square holds the number of seconds until the **nearest** mast
   reaches it, counting one square of travel as one second.
6. An open square no mast can reach holds `-1`, and is counted in the second
   return value.
7. `siren_reach(())` and `siren_reach(("",))` both return `([], 0)`.
8. `draw` renders the map with each entry padded to two characters, joined by
   single spaces, one line per row, and a `-1` shown as `-`.
9. Both functions keep their type hints and their docstrings.

## Constraints

- **Seed the queue with every mast before the loop starts.** Not one search
  per mast. With `M` masts on an `R × C` plan, one search per mast is
  `O(M × R × C)`; seeding them all together is `O(R × C)` no matter how many
  masts there are. On this nine-by-nine plan with two masts you would not
  notice. On a city of ten thousand squares with two hundred masts it is two
  hundred times the work for the same answer.

- **Build the map with a loop, not with `[[-1] * columns] * rows`.**
  Multiplying a list of lists copies the *reference*, so all the rows end up
  being the same row and writing to one writes to all of them. `[[-1] *
  columns for _ in range(rows)]` builds a genuinely separate list per row.
  This is not a BFS bug; it is a Python bug that BFS problems catch.

- **Use the map itself as the reached set.** A square whose entry is still
  `-1` has not been reached; anything else has. Keeping a separate `set` as
  well would be a second copy of the same fact, and two copies of a fact go
  out of step eventually.

- **Count the open squares on the way in, not the unreached ones on the way
  out.** Tally every `.` during the seeding scan, tally every square you
  reach during the walk, and subtract at the end. Scanning the finished map
  for `-1` entries would need you to look at the plan again for each one, to
  tell an unreached square from a building.

- **Do not write into the plan.** The plan is a tuple of strings so you
  cannot, and that is deliberate. Mark progress in the map you were asked to
  produce.

- **Bounds first, then the plan lookup, then the map lookup.** Same order as
  Exercise 2, same reason: Python's negative indexing means a missed bounds
  check wraps round the plan instead of raising, and answers a question about
  a town that does not exist.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
 0  1  2  3  4  5  6  7  8
 1  2  3  4  5  6  7  8  7
 2  3  -  -  -  -  -  7  6
 3  4  -  -  -  -  -  6  5
 4  5  -  -  -  -  -  5  4
 5  6  -  -  -  -  -  4  3
 6  7  -  -  -  -  -  3  2
 7  8  7  6  5  4  3  2  1
 8  7  6  5  4  3  2  1  0
squares that never hear a siren: 7
All checks passed.
```

Read the top-right corner and the bottom-left. Both are `8`. The top-right is
eight squares from the mast at `(0, 0)`, straight along the top; the
bottom-left is eight squares from the mast at `(8, 8)`, straight along the
bottom. Neither is reached by the mast nearer the other end, and neither had
to be worked out separately.

Now look at the diagonal band running down the middle-right of the map —
`7, 6, 5, 4, 3, 2` down the column at index 8. That is where the two spreads
meet. Above the meeting line the numbers come from the top-left mast; below
it they come from the bottom-right one. Nothing in the code decides where
that line falls. It falls out of whichever spread arrived first.

The seven dashes in the middle are the courtyard inside the terrace. Sound
that would have to pass through a wall does not arrive, and `-1` is what the
map says about it.

## Steps

1. Create the file, paste the starter, and run it. It fails on the first
   line that uses the result.
2. Write the empty-plan guard and the map builder. Check in a REPL that
   writing to `grid[0][0]` changes exactly one entry. If it changes a whole
   column, you multiplied a list of lists.
3. Write the seeding scan on its own and print the queue. Two entries:
   `(0, 0)` and `(8, 8)`. Print the open-square tally too — sixty-two on this
   plan.
4. Write the loop. It is the same loop as Exercise 2 with the target check
   taken out, because there is no target: you are not looking for anything,
   you are filling everything in.
5. Run it and compare against the expected output. If your map is right but
   your count is wrong, the count is the easier bug — print the two tallies
   you are subtracting.
6. Write `draw` last. It is presentation, and it is worth writing last so
   that a broken `draw` never makes you doubt a correct search.
7. Change `TOWN` so the courtyard has a doorway — put a `.` where a `#` is on
   the terrace wall — and run again. Seven dashes become seven numbers, and
   the count drops to zero. That is a good way to convince yourself the `-1`
   really does mean "no route" and not "special square".

## The Solution

```python
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
```

**One line separates this page from Exercise 2.**

```python
if square == "S":
    seconds[row][column] = 0
    queue.append((row, column))
```

That is inside the scan, so it happens once per mast. By the time the walk
starts, the queue already holds every mast, all of them at zero seconds. The
loop underneath is unchanged — it does not know or care how many things it
started with.

Why that is correct, in one sentence: **the queue always deals with the
nearest unfinished squares first, so the first spread to arrive at a square
is the nearest mast's, whichever mast that is.** With one mast the queue
holds 0, then all the 1s, then all the 2s. With five masts it holds five 0s,
then all the 1s, then all the 2s. The order is the same. Only the width of
each band changed.

**The map is the reached set, and that is why there is no `set` here.**

```python
and seconds[next_row][next_column] == BLOCKED
```

`-1` means two things at once — "no answer yet" and, when the walk is over,
"no answer ever". They are the same condition at different moments, which is
exactly why one value can carry both. A square is written once and never
again, because the moment it is written it stops passing this test.

**The count is a subtraction, done in two halves.** `open_squares` is tallied
during the scan; `heard` is tallied inside the walk, once per square written.
The answer is the difference. Trying to work it out at the end instead would
mean walking the finished map and asking, for each `-1`, whether the plan has
a building there — the same information, gathered twice, with a chance of
disagreeing.

**Why `-1` and not a big number.** A very large number would let the map be
searched for a maximum without a special case, which is genuinely convenient.
It also survives being added up, averaged, or plotted, and the answer it
gives is nonsense with a straight face. `-1` cannot be mistaken for a real
number of seconds, so a bug that ignores it shows up as an obviously silly
result rather than a slightly wrong one. When the difference between a loud
wrong answer and a quiet wrong answer is available, take loud.

**`draw` pads to two characters on purpose.** With a single-character format
the columns stop lining up the moment a distance reaches ten, and a map you
cannot read by eye is a map you cannot check by eye. The whole point of
printing it is to be able to see the meeting line.

## Run it

Copy the worked answer on this page into `exercise-03-siren-reach.py` and run it:

```bash
python exercise-03-siren-reach.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-03-siren-reach.py`.

## Common bugs to catch

- **Every row of the map is identical.** No exception, and it looks like the
  search is broken:

  ```text
  >>> grid = [[0] * 2] * 2
  >>> grid[0][0] = 9
  >>> grid
  [[9, 0], [9, 0]]
  ```

  `* 2` on a list of lists makes two references to one list, not two lists.
  Build with a comprehension: `[[BLOCKED] * columns for _ in range(rows)]`.

- **The distances are right near one mast and wrong near the other.** You
  searched from one mast, finished, then searched from the next and
  overwrote. Look at your queue at the moment the loop begins: it should
  already hold both masts.

- **The count is 62 instead of 7.** You counted every open square rather than
  the unreached ones — the subtraction is missing, or `heard` is never
  incremented. Print both tallies before subtracting.

- **The count is 0 and the map is right.** You tallied `heard` at the wrong
  moment: increment it where you write a square's seconds, not where you pop
  one, or the masts get counted and nothing else does.

- **`IndexError: string index out of range`.**

  ```text
  Traceback (most recent call last):
      town[next_row][next_column] == "."
      ~~~~~~~~~~~~~~^^^^^^^^^^^^^
  IndexError: string index out of range
  ```

  A missing upper bounds check, walking off the right or bottom edge. The
  missing *lower* check does not raise at all — it wraps to the far side and
  gives you a plausible, wrong map. Both tests, always, before the lookup.

- **`AttributeError: 'list' object has no attribute 'popleft'`.**

  ```text
  Traceback (most recent call last):
      queue.popleft()
      ^^^^^^^^^^^^^
  AttributeError: 'list' object has no attribute 'popleft'
  ```

  The queue is a list. `from collections import deque` and seed with
  `deque()`.

- **The map holds `0` where a building is.** You built the grid full of zeros
  instead of `-1`, so an untouched square is indistinguishable from a mast.
  The starting value has to be one that cannot be a real answer.

## Under the hood

<details>
<summary>Under the hood — why many sources cost the same as one, and what this is really computing</summary>

**The complexity, and why the number of masts does not appear in it.**

Every square is written at most once, because writing it is what stops it
passing the `== BLOCKED` test. So the walk performs at most `R × C` writes
and at most `R × C` pops, each pop looking at four neighbours. Time is
`O(R × C)`. The seeding scan is another `O(R × C)`. Total: `O(R × C)`.

The number of masts, `M`, is nowhere in that. It cannot be, because the masts
are squares too — putting `M` of them in the queue up front is `M` appends,
and `M` is at most `R × C`. Compare against one search per mast, which is
`O(M × R × C)`. For a city plan of 200 × 200 with 300 masts, that is forty
thousand units of work against twelve million. Same answer.

**What this really is.** Add an imaginary square that is joined to every
mast, and run an ordinary single-source search from it. Every mast is one
step from the imaginary square, so every mast sits at distance 1 and every
real answer is one too big — subtract one and you have this page's map.
Seeding the queue with all the masts at zero is that construction with the
imaginary square optimised away.

That reframing is worth carrying. Whenever a problem says "from any of
these", you can either invent a source joined to all of them, or seed the
queue with all of them. They are the same algorithm, and the second is less
typing.

**Where the same shape turns up.** "Distance to the nearest of a set" is one
of the most reused questions there is: nearest fire station, nearest
charging point, nearest clean pixel in an image mask, nearest reachable node
in a failure model. It is also the engine behind a *distance transform* in
image processing, where the sources are the black pixels and the map is what
you threshold to fatten or thin a shape. Same walk, different noun.

**The one thing multi-source does not do.** It cannot tell you *which* mast
reached a square, only how far the nearest one was. If you need that, carry
the mast's identity along on the queue beside the coordinates and write it
into a second map at the same moment you write the seconds. The cost does not
change; the memory doubles.

</details>

## Acceptance checklist

- [ ] `python exercise-03-siren-reach.py` prints the nine-row map, the count
      line, then `All checks passed.`
- [ ] The output matches the expected block character for character.
- [ ] The queue holds both masts before the `while` loop runs once.
- [ ] The map is built with a comprehension, and writing one entry changes
      one entry.
- [ ] There is no separate `visited` set anywhere in the file.
- [ ] `siren_reach(())` returns `([], 0)` without touching the queue.
- [ ] A plan with no masts returns an all-`-1` map and a count of every open
      square.
- [ ] Both functions have type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 6 exercise 3: siren reach`.

## Stretch

- **Report the worst-served square as well as the count.** One pass over the
  finished map.

  ```python
  def worst_square(town: tuple[str, ...], seconds: list[list[int]]) -> tuple[int, int, int]:
      """Return the open square that waits longest, and how long it waits."""
      worst = (0, 0, -1)
      for row, line in enumerate(town):
          for column, square in enumerate(line):
              if square == "." and seconds[row][column] > worst[2]:
                  worst = (row, column, seconds[row][column])
      return worst
  ```

  ```text
  (0, 8, 8)
  ```

  Row 0, column 8, eight seconds — the top-right corner. Note this ignores
  the unreachable squares by design, because `-1` never beats a real number.
  Deciding whether that is the behaviour you want is the interesting half of
  the exercise.

- **Say which mast reached each square.** Carry the mast along on the queue.

  ```python
  queue = deque((mast, mast) for mast in masts)   # (square, the mast it came from)
  ...
  queue.append((step, source))
  ```

  ```text
  (0, 4) heard from (0, 0)
  (8, 4) heard from (8, 8)
  (8, 0) heard from (0, 0)
  ```

  The middle of the top row belongs to the top mast and the middle of the
  bottom row to the bottom one, as you would guess. The bottom-left corner is
  the interesting one: it is eight squares from either mast, and the top mast
  got there first only because the terrace makes the other route longer. Same
  walk, one extra field.

- **Ask the opposite question: which mast, added, helps the most?** Try every
  open square as a third mast and keep the one that shrinks the count most.

  ```python
  def best_new_mast(town: tuple[str, ...]) -> tuple[tuple[int, int], int]:
      """Return the open square worth putting a mast on, and the squares it saves."""
      _, before = siren_reach(town)
      best, saved = (0, 0), 0
      for row, line in enumerate(town):
          for column, square in enumerate(line):
              if square != ".":
                  continue
              trial = list(town)
              trial[row] = line[:column] + "S" + line[column + 1 :]
              _, after = siren_reach(tuple(trial))
              if before - after > saved:
                  best, saved = (row, column), before - after
      return best, saved
  ```

  ```text
  ((3, 3), 7)
  ```

  A mast inside the courtyard rescues all seven squares, which is obvious
  once you see it and not before. Running the whole search once per candidate
  is `O((R × C)²)` and perfectly fine at this size — knowing when a slow
  answer is the right answer is its own skill.

When your map is right, move on to
[Exercise 4 — Cable Pull](./exercise-04-cable-pull.md).
