# Problem 2 — Worst-Served Bay

> **Topic:** multi-source again, but the answer is the *worst* square rather than the map
> **Lecture:** [02 — Grid BFS and Graph BFS](../lecture-notes/02-grid-bfs-and-graph-bfs.md)
> **Difficulty:** Medium
> **Target time:** 45 minutes
> **Why this one:** Exercise 3 built the map. Here the map is scaffolding and the answer is one square out of it, which means the whole difficulty moves into the comparison — and the comparison has a rule most people get wrong the first time, because "unreachable" has to beat every distance rather than lose to it.

## The Brief

A distribution shed, drawn as rows of text:

```
D  a loading dock
.  a storage bay
#  a stanchion holding the roof up
```

A forklift crosses one square at a time, north, south, east or west. Every
dock is equally good; the forklift goes to whichever is nearest.

The shift planner wants **one** bay: the one that is worst off. That is the
bay whose nearest dock is furthest away.

Two rules make the answer definite.

**Unreachable beats far.** A bay the forklift cannot get to at all is a worse
problem than a bay forty squares from a dock — you cannot fix "no route" by
walking faster. So a bay with no route wins outright, and it is reported with
a distance of `-1`. If several bays have no route, the tie-break below picks
between them.

**Lowest row, then lowest column, wins a tie.** Two bays exactly equally
badly served are indistinguishable to the planner, so the spec picks one, and
picks it in a way that does not depend on the order the search happened to
run in. Two people running this get the same bay.

`None` comes back when the shed has no storage bays at all — with or without
docks, there is then nothing to be worst. A shed with bays but no docks is
**not** that case: every bay is unreachable, and the first one wins.

## Starter

Create `problem-02-worst-served-bay.py` in your practice repo and paste this
in. Fill in every `TODO`.

```python
"""problem-02-worst-served-bay.py — the bay the forklifts hate.

A distribution shed. `D` marks a loading dock, `.` marks a storage bay, `#`
marks a stanchion the forklifts drive around. A forklift crosses one square
at a time, north, south, east or west.

The shift planner wants the one bay that is worst off: the bay whose nearest
dock is furthest away. A bay no dock can reach at all is worse than any
distance, so it wins outright.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from collections import deque
from typing import NamedTuple

# ---- Given data ----
# Two docks on the left wall. The right-hand aisle is long, and the corner
# room behind the stanchions has no way in at all.
SHED: tuple[str, ...] = (
    "D.........",
    "..........",
    "...#####..",
    "...#...#..",
    "...#...#..",
    "...#####..",
    "..........",
    "..........",
    "D.........",
    "..........",
)

DRIVE: tuple[tuple[int, int], ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))
UNREACHED = -1


class Bay(NamedTuple):
    """The worst-served bay in the shed."""

    row: int
    column: int
    squares: int


# ---- Your task ----
def worst_served_bay(shed: tuple[str, ...]) -> Bay | None:
    """Return the storage bay whose nearest dock is furthest away.

    Args:
        shed: The rows of the shed plan. `D` is a dock, `.` is a storage
            bay, `#` is a stanchion.

    Returns:
        A `Bay` holding its row, its column, and how many squares the
        forklift drives to the nearest dock. A bay no dock can reach is
        reported with `squares` of -1 and beats every reachable bay, because
        "no route" is a worse problem than a long one. The lowest row wins a
        tie, and then the lowest column, so the answer does not depend on
        the order the search happened to run in.

        None when the shed has no storage bays at all — with or without
        docks, there is then nothing to be worst.
    """
    # TODO: an empty plan returns None
    # TODO: build a grid of UNREACHED; seed the queue with EVERY dock at 0
    # TODO: the usual multi-source walk over '.' squares
    # TODO: scan the bays in row-then-column order, keeping the worst so far
    ...


def _worse(candidate: Bay, best: Bay) -> bool:
    """Return True when `candidate` is a worse-served bay than `best`.

    Args:
        candidate: The bay being considered.
        best: The worst bay found so far.

    Returns:
        True if the candidate should replace it. Unreachable beats every
        distance; otherwise the larger distance wins, and neither row nor
        column is consulted, because the outer scan already visits bays in
        row-then-column order and only a strict improvement replaces.
    """
    # TODO: three lines — best already unreachable, candidate unreachable,
    #       then the plain comparison
    ...


# ---- Self-check ----
if __name__ == "__main__":
    worst = worst_served_bay(SHED)
    print(f"worst bay: row {worst.row}, column {worst.column}")
    print(f"drive    : {worst.squares} squares" if worst.squares != UNREACHED else "drive    : no route")

    # The walled room is unreachable, so it wins however short the drive to
    # the rest of the shed is. Row 3, column 4 is its top-left corner.
    assert worst == Bay(3, 4, UNREACHED)

    # Take the stanchions away and the answer becomes a real distance: the
    # far corner of the middle of the right-hand wall, equidistant-ish from
    # both docks.
    open_shed = tuple(row.replace("#", ".") for row in SHED)
    open_worst = worst_served_bay(open_shed)
    assert open_worst == Bay(4, 9, 13)

    # One dock in a corner: the opposite corner is worst, and the drive is
    # the two side lengths added together.
    assert worst_served_bay(("D...", "....", "....")) == Bay(2, 3, 5)

    # No docks: every bay is unreachable and the lowest row and column wins.
    assert worst_served_bay(("...", "...")) == Bay(0, 0, UNREACHED)

    # No bays: nothing to report.
    assert worst_served_bay(("D#", "#D")) is None
    assert worst_served_bay(()) is None
    assert worst_served_bay(("",)) is None

    print("All checks passed.")
```

One idea before you start.

**The tie-break is not in the comparison — it is in the scan order.** The
outer scan visits bays top to bottom, left to right, and `_worse` replaces
only on a *strict* improvement. So the first bay to reach any given badness
keeps the title, and the first bay in scan order is the lowest row and then
the lowest column. That is why `_worse` never mentions rows or columns, and
why you must not use `>=`.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/courses/ide#src=C2-CrunchTime-The-Code/curriculum/week-06-bfs/homework/problem-02-worst-served-bay.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `worst_served_bay` returns a `Bay` or `None`.
2. Only `.` squares are candidates. Docks and stanchions never win.
3. `Bay.squares` is the number of squares driven to the nearest dock, or
   `-1` when no dock can reach the bay.
4. An unreachable bay beats every reachable one.
5. Ties are broken by lowest row, then lowest column.
6. A shed with no `.` squares returns `None`, as do `()` and `("",)`.
7. A shed with bays and no docks returns the first bay with `-1`.
8. Both functions keep their type hints and their docstrings.

## Constraints

- **Seed with every dock, not one search per dock.** With `D` docks in an
  `R × C` shed, one search each is `O(D × R × C)`; all of them together is
  `O(R × C)`. This is Exercise 3's line, and the point of meeting it again is
  that it should now be automatic.

- **Do not use a large number to stand in for "unreachable".** A `10**9`
  would let one comparison handle both cases, and it would also survive being
  printed, added or averaged, which is how the wrong number reaches a report.
  `-1` cannot be mistaken for a drive distance.

- **Compare with `>`, never `>=`.** `>=` makes the *last* bay of a tied group
  win, which is the bottom-right one, which is the opposite of the spec. This
  is a one-character bug that passes every test written against a shed with
  no ties in it.

- **Keep `_worse` free of coordinates.** The scan order already encodes the
  tie-break. Putting rows and columns into the comparison as well means the
  rule is written in two places, and the day somebody changes the scan order
  they will only find one of them.

- **Scan the bays in row-then-column order.** Two nested `range` loops, rows
  outermost. Iterating a set or a dict of distances instead gives you an
  order Python is free to change, and the tie-break silently stops being
  stable.

- **`None` for "no bays", not a `Bay` with odd values.** There is no bay to
  report, so there is no `Bay`. A sentinel like `Bay(-1, -1, -1)` would have
  to be checked for at every call site, which is what `None` already does
  better.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
@@OUTPUT@@
```

Row 3, column 4. That is the top-left square of the walled room in the middle
of the shed — four stanchion walls with no doorway, so no forklift will ever
park there. There are nine such squares, and the one reported is the first in
scan order.

The second printed line says `no route` rather than `-1 squares`, because a
report that says "the drive is minus one squares" is a report nobody trusts.
Formatting is where a sentinel earns or loses its keep.

Take the stanchions out and the answer becomes `Bay(4, 9, 13)` — a real
distance, on the right-hand wall, roughly equidistant from both docks. That
assert is in the self-check on purpose: it exercises the *other* branch of
the comparison, and without it a version that only ever handles unreachable
bays would pass.

## Steps

1. Create the file, paste the starter, and run it. It fails at the first use.
2. Write the seeding scan and print the queue's length. Two entries.
3. Write the walk. It is Exercise 3's walk exactly — if you have that file,
   the only change is which characters count as passable.
4. Print the finished distance grid before you write the comparison. Look at
   the middle: nine `-1`s in a block, surrounded by real numbers.
5. Write `_worse`, then the scan. Three lines and two loops.
6. Run the open-shed assert. If it fails, your comparison is only handling
   the unreachable case — a common shape of bug when the interesting example
   is written first.
7. Change `>` to `>=` on purpose and watch the answer move to the last tied
   bay. Change it back.
8. When `All checks passed.` prints, add a doorway to the walled room and
   confirm the answer moves to a real distance somewhere else.

## The Solution

```python
@@CODE@@
```

**The walk is Exercise 3's, and the work is all in the comparison.**

Seeding every dock, spreading outward, writing each bay once — none of that
is new. What is new is that the map is thrown away. It exists only so that
the scan underneath it has something to compare.

**`_worse` is three lines and each one is a decision.**

```python
if best.squares == UNREACHED:
    return False
if candidate.squares == UNREACHED:
    return True
return candidate.squares > best.squares
```

Line one: nothing beats an unreachable bay, so once we hold one we are done
comparing. Line two: an unreachable candidate beats any reachable holder.
Line three: two reachable bays compare by distance, plainly.

Written as one expression it would need `-1` to sort above every positive
number, which no ordinary comparison does. Three lines, in this order, say
the rule exactly and are readable at a glance. That is worth more than
brevity here.

**The strict `>` is the tie-break, and it is load-bearing.** The scan visits
bays in row-then-column order, so the first bay to hit a given badness is
already the lowest row and then the lowest column. `>` means a later bay
equal to it does not replace it. Change it to `>=` and the *last* tied bay
wins instead — the bottom-right of the walled room rather than the top-left.
No exception, no warning, just a different square.

**`worst is None` seeds the scan without a sentinel.** The first bay
encountered becomes the holder unconditionally, whatever its distance. That
avoids inventing a starting `Bay` that has to be worse than every real one —
which for the unreachable case would be impossible anyway, since `-1` is
already the top of the ordering.

**The `None` return falls out of `worst` never being assigned.** A shed with
no `.` squares runs both loops, finds nothing to consider, and returns the
`None` it started with. No counter, no flag.

**Why the docks are not candidates.** A dock is where the forklift is going,
not somewhere it stores anything. The `if shed[row][column] != "."` guard in
the scan says that, and it is the same guard that keeps stanchions out. One
test, two exclusions, because both are "not a bay".

## Download and run

Download
[problem-02-worst-served-bay-solution.py](./problem-02-worst-served-bay-solution.py)
and run it:

```bash
python problem-02-worst-served-bay-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `problem-02-worst-served-bay.py`.

## Common bugs to catch

- **The answer is a real distance when it should be `-1`.** No exception:

  ```text
  worst bay: row 4, column 9
  drive    : 13 squares
  ```

  Your comparison treats `-1` as a small number, so every reachable bay beats
  every unreachable one. The two `UNREACHED` checks have to come before the
  plain comparison, not after.

- **The answer is row 5, column 6.** Also no exception. That is the
  bottom-right of the walled room, so your comparison uses `>=` and the last
  tied bay wins. Use `>`.

- **`AttributeError: 'NoneType' object has no attribute 'squares'`.**

  ```text
  Traceback (most recent call last):
      print(f"worst bay: row {worst.row}, column {worst.column}")
                                  ^^^^^^^^^
  AttributeError: 'NoneType' object has no attribute 'row'
  ```

  `worst_served_bay` returned `None` on a shed that has bays. Usually the
  scan is skipping every square because the `!= "."` test is inverted.

- **The open-shed assert fails but the main one passes.** You wrote the
  comparison for the unreachable case only. This is why the self-check
  carries a shed with no stanchions in it.

- **`IndexError: list index out of range`.**

  ```text
  Traceback (most recent call last):
      squares[next_row][next_column] == UNREACHED
      ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  IndexError: list index out of range
  ```

  Missing upper bounds check on the distance grid. Note this one *does* raise
  where the equivalent on the plan string wraps — lists raise on a
  too-large index, and strings do too, but a negative index on either wraps
  silently.

- **A shed with no docks returns a bay with a huge number.** You seeded the
  distance grid with `0` rather than `UNREACHED`, so untouched squares look
  like docks. The starting value must be one that cannot be a real answer.

- **`worst_served_bay(("D#", "#D"))` returns a `Bay`.** Your scan considers
  docks or stanchions as candidates. Only `.` squares are bays.

## Under the hood

<details>
<summary>Under the hood — sentinels, and why the ordering has a top element</summary>

**Cost.** One seeding scan, one walk, one comparison scan: three passes over
`R × C` squares, so `O(R × C)` time and the same memory for the distance
grid. Nothing depends on how many docks there are, which is the multi-source
property from Exercise 3 turning up again.

**What "unreachable beats far" really is.** The distances form an ordering
with a top element bolted on: `0 < 1 < 2 < … < unreachable`. That is a
perfectly ordinary structure — in mathematics it is the natural numbers with
an added infinity — and it is why a single numeric comparison cannot express
it. `-1` is a *label* for that top element, not a number playing the role.

Two other ways to write the same thing, both used in real code:

- `float("inf")` genuinely does compare above every number, so one `>` works.
  The cost is that the value is a float, so it infects arithmetic — an
  average over a column containing one `inf` is `inf`, silently.
- `None` for unreachable, with the comparison written as a `key` returning
  `(is_unreachable, distance)`. Clean, and it moves the rule into a tuple
  key the way Exercise 5 does.

`-1` was picked here because it prints readably, stays an `int`, and cannot
be confused with a distance. Every choice trades something; being able to say
what you traded is the point.

**Why the scan order carries the tie-break.** Encoding a tie-break in
iteration order is compact and fragile. It works because the scan is two
explicit `range` loops whose order is guaranteed by the language. It would
stop working the moment somebody iterated a set, a dict, or a parallel
result. If that ever seems likely, move the rule into the comparison as
`(candidate.squares, -candidate.row, -candidate.column) > ...` and accept the
extra noise. The version here is the right trade for a function this small,
and the docstring says so, which is what makes it a decision rather than an
accident.

**A related question that is genuinely harder.** "Where should we put one new
dock to make the worst-served bay as good as possible?" — the minimax
placement — cannot be answered by one walk. The straightforward approach runs
the whole search once per candidate square, which is `O((R × C)²)`. That is
fine for a shed and hopeless for a city, and the fast versions are a research
topic rather than an interview answer. Knowing that boundary is worth more
than knowing the fast version.

</details>

## Acceptance checklist

- [ ] `python problem-02-worst-served-bay.py` prints two lines then
      `All checks passed.`
- [ ] The output matches the expected block character for character.
- [ ] Both docks are in the queue before the walk starts.
- [ ] `_worse` handles `UNREACHED` before it compares distances.
- [ ] The comparison is `>`, not `>=`, and you have watched `>=` move the
      answer.
- [ ] The bay scan uses two `range` loops, rows outermost.
- [ ] A shed with no bays returns `None`.
- [ ] Both functions have type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 6 homework 2: worst-served bay`.

## Stretch

- **Report the whole tail, not just the worst.** The five worst bays tell a
  planner more than one does.

  ```python
  def worst_bays(shed: tuple[str, ...], how_many: int = 5) -> list[Bay]:
      """Return the worst-served bays, worst first."""
      bays = []
      squares, _ = _distance_grid(shed)   # split the walk out of the function
      for row, line in enumerate(shed):
          for column, square in enumerate(line):
              if square == ".":
                  bays.append(Bay(row, column, squares[row][column]))
      return sorted(
          bays,
          key=lambda bay: (bay.squares != UNREACHED, -bay.squares, bay.row, bay.column),
      )[:how_many]
  ```

  ```text
  [Bay(row=3, column=4, squares=-1), Bay(row=3, column=5, squares=-1),
   Bay(row=3, column=6, squares=-1), Bay(row=4, column=4, squares=-1),
   Bay(row=4, column=5, squares=-1)]
  ```

  Note the key's first field: `False` sorts before `True`, so unreachable
  bays come first. That is the same ordering as `_worse`, said in the tuple
  language of Exercise 5 — and doing it both ways is worth the time, because
  interviewers ask you to justify one over the other.

- **Count how many bays are unreachable at all.** The number that decides
  whether the planner needs a doorway or a better rota.

  ```python
  def stranded_bays(shed: tuple[str, ...]) -> int:
      """Return how many storage bays no dock can reach."""
      ...
  ```

  ```text
  stranded bays: 9
  ```

  Nine — the whole walled room. One number, and it changes the conversation
  from "which bay is worst" to "there is a room nobody can get into".

- **Ask what a doorway is worth.** Knock one stanchion out at a time and see
  which single change helps most.

  ```text
  best stanchion to remove: (2, 4) — rescues 9 bays
  ```

  Any of the room's wall squares does it, and the first in scan order is
  reported. Running the whole search once per stanchion is `O((R × C)²)` and
  entirely reasonable at this size — recognising when a slow answer is the
  right answer is a real skill, and it is the same finding as Exercise 3's
  last stretch.

Next: [Problem 3 — Shim Dial](./problem-03-shim-dial.md).
