# Mini-Project — The Muster Report

> Topic: one algorithm, three questions, three seeds · Lecture: [1](../lecture-notes/01-the-bfs-template.md), [2](../lecture-notes/02-grid-bfs-and-graph-bfs.md) · Difficulty: Medium · Target time: 8 hours across Thursday to Saturday · Why this one: the exercises drilled each BFS shape alone. Here all three sit in one program, and the only differences between them are the seed and the neighbour rule — which is the week's whole argument, made in code rather than in prose.

## The Brief

A coastal town runs a flood-response drill. The control room wants one report
answering three questions:

1. **The call-out.** The control room keys the radio once. Which relays hear it,
   on which hop, and which ones never hear it at all?
2. **The route.** How many street moves from the depot to the muster point,
   going around the flooded streets?
3. **The sirens.** For every open square, how long until the nearest mast reaches
   it, which square waits longest, and how many squares hear nothing?

All three are breadth-first search. Question 1 walks a mesh of named relays one
hop at a time. Question 2 walks a grid of squares from one start. Question 3
walks the same grid from **every mast at once**. The queue, the seen-set and the
loop body are identical in all three; only the seed and the neighbour rule
change.

That sentence is the deliverable. The program is how you earn the right to say
it.

## Starter

`README-solution.py` sits beside this page with the town, the mesh and the
self-checks.

```text
D....#....S      D  the depot          .  passable street
.###.#.##..      M  the muster point   #  flooded or built on
.#...#..#..      S  a siren mast
.#.#####.#.
...#.....#.
##.#.###.#.
S..#.#...#.
.###.#.###.
.....#....M
```

The relay mesh is **directed**, and deliberately so — terrain makes some links
one-way:

```text
CONTROL   → NORTHGATE, STAITHE
NORTHGATE → BRIDGEFOOT, STAITHE
STAITHE   → QUAYSIDE
BRIDGEFOOT→ CONTROL, MILLRACE
QUAYSIDE  → MILLRACE
MILLRACE  → (nothing)
OUTMARSH  → TIDEWELL
TIDEWELL  → OUTMARSH
```

Outmarsh and Tidewell hear each other and nobody else. They are not a bug in the
data; they are the disconnected component, and a report that does not name them
is a report that quietly loses two relays.

## Requirements

1. `call_out(mesh, control)` returns the relays grouped by hop, and the list of
   relays never reached.
2. `find_mark(town, mark)` locates a single marked square and raises
   `ValueError` when the mark is missing or appears twice.
3. `street_moves(town, start, finish)` returns the fewest moves, or `None` when
   the muster point cannot be reached.
4. `siren_sweep(town)` returns a distance map from all masts at once, plus a
   `Coverage` naming the slowest square, its wait, and how many squares hear
   nothing.
5. `muster_report(town, mesh)` assembles the printed report from the three.

### What you ship

Three files under `frame-writeups/c2-week-06/mini-project/`:

```
frame-writeups/c2-week-06/mini-project/
├── README.md                        ← overview, index, and the reflection
├── problem-01-siren-sweep.md        ← grid BFS, multi-source, a distance map
└── problem-02-radio-call-out.md     ← node BFS, single-source, hop levels
```

The two are chosen to sit on opposite corners of the week:

- **Problem 1 (grid, multi-source).** The seed is every mast; the answer is a
  per-square distance map. It forces the multi-source idiom to be written out
  explicitly rather than gestured at.
- **Problem 2 (mesh, single-source).** The seed is one relay; the graph is a
  dictionary, not a rectangle; the answer is a level grouping. It forces a real
  neighbour rule and a real unreachable case.

Between them they cover every idiom of the week: single-source, multi-source,
grid shape, node shape, per-node distance, level tracking, and unreachable
handling. After this pair, recognising a BFS problem should reduce to asking
which of those four corners it sits in.

### The recognition memo

Five lines at the top of each write-up, readable in thirty seconds:

1. **The shape.** Grid or node graph, and how you knew inside ten seconds.
2. **The seed.** One source or many, and what goes into the queue before the
   loop starts.
3. **The neighbour rule**, in one line — including what makes a neighbour
   illegal.
4. **What the answer is.** A count, a level grouping, or a full distance map.
5. **The cost**, in terms of the town's own numbers, not in abstract n.

### Cross-references

The two write-ups are graded as a pair and must be navigable as one:

- The grid write-up says why seeding every mast at once is still one BFS and not
  several, and points at the mesh write-up for the single-source case.
- The mesh write-up says why the hop grouping is the same information the grid's
  distance map holds, in a different shape.
- Both name the same rejected alternative — depth-first search — and say why it
  is wrong here specifically, not in general.

### Rubric

| Axis | What "great" looks like |
|------|--------------------------|
| Frame the problem | The memo names the shape, the seed and the answer in five lines. |
| Reason about options | Four to six bullets before any code, with depth-first search named and rejected for a stated reason. |
| Assemble the solution | `deque`, not a list, for the queue; marked seen on enqueue; type hints throughout. |
| Measure it | A trace on at least two examples, including one unreachable case. |
| Evaluate the cost | Time, space, best/average/worst, the trade-off and the improvement — different paragraphs for the two write-ups, not the same one twice. |

Twenty points per write-up, forty for the pair.

## Constraints

- **Mark squares seen when they are enqueued, not when they are dequeued.**
  Marking on dequeue lets the same square enter the queue several times; on this
  town it still terminates and the count is still right, which is what makes it
  a bug you can ship.
- **A `deque`, not a list.** `list.pop(0)` is `O(n)` and turns the whole sweep
  quadratic without ever looking wrong.
- **Multi-source is one search, not many.** Every mast goes into the queue before
  the loop starts, all at distance zero. Running one BFS per mast and taking the
  minimum gives the same answer for `masts` times the work.
- **Unreachable is a real answer.** `None` for the route, `-1` in the distance
  map, and a named list of relays that never hear the call.
- **The mesh is directed.** A link is not a two-way street unless the mesh says
  it twice.
- **The report is assembled from the three functions**, not recomputed inside
  the printer.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python README.py
MUSTER REPORT
=============

1. Radio call-out
   hop 0: CONTROL
   hop 1: NORTHGATE, STAITHE
   hop 2: BRIDGEFOOT, QUAYSIDE
   hop 3: MILLRACE
   never hears it: OUTMARSH, TIDEWELL

2. Depot to muster point
   depot at (0, 0), muster point at (8, 10)
   shortest run: 34 moves

3. Siren coverage
   slowest square: (6, 8) at 16 seconds
   squares that hear nothing: 0

All checks passed.
```

Three numbers are worth pausing on. The route is **34 moves** across a town
whose corners are 17 apart in a straight line — the flooding roughly doubles it.
The slowest square waits **16 seconds** for a siren while the masts sit at two
corners. And **two relays never hear the call at all**, which is the kind of
finding a drill exists to produce.

## Steps

1. Read the self-checks. They are the spec.
2. Write both memos before any code. If you cannot write them, you do not yet
   know which shape you are building.
3. Do the mesh first — it is the smaller graph and the easier one to trace by
   hand. Get the hop grouping and the never-reached list both right.
4. Do the route next. Trace the first three levels on paper against the map
   before trusting the number.
5. Do the sweep last, and seed **every** mast before the loop. Check one square
   by hand against the map.
6. Assemble the report, then write both FRAME passes and the cross-references.

## The Solution

```python
"""README-solution.py — the Muster Report for a flood-response drill.

One program, three questions, one algorithm underneath all of them.

  1. The call-out. The control room keys the radio once. Which relays hear
     it, on which hop, and which ones never hear it at all?
  2. The route. How many street moves from the depot to the muster point,
     around the flooded streets?
  3. The sirens. For every open square, how long until the nearest mast
     reaches it, which square waits longest, and how many hear nothing?

Question 1 is breadth-first search over a mesh of named relays, taken one
hop at a time. Question 2 is breadth-first search over a grid of squares
from one start. Question 3 is breadth-first search over the same grid from
every mast at once. The queue, the seen-set and the loop body are the same
in all three; only the seed and the neighbour rule change.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import deque
from typing import NamedTuple

# ---- Given data ----
# The town. `D` is the depot, `M` is the muster point, `S` is a siren mast,
# `.` is a passable street, `#` is flooded or built on.
TOWN: tuple[str, ...] = (
    "D....#....S",
    ".###.#.##..",
    ".#...#..#..",
    ".#.#####.#.",
    "...#.....#.",
    "##.#.###.#.",
    "S..#.#...#.",
    ".###.#.###.",
    ".....#....M",
)

# Which relays can hear which. Terrain makes this one-way in places.
MESH: dict[str, list[str]] = {
    "CONTROL": ["NORTHGATE", "STAITHE"],
    "NORTHGATE": ["BRIDGEFOOT", "STAITHE"],
    "STAITHE": ["QUAYSIDE"],
    "BRIDGEFOOT": ["CONTROL", "MILLRACE"],
    "QUAYSIDE": ["MILLRACE"],
    "MILLRACE": [],
    "OUTMARSH": ["TIDEWELL"],
    "TIDEWELL": ["OUTMARSH"],
}

CONTROL = "CONTROL"
STREET_MOVES: tuple[tuple[int, int], ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))
PASSABLE = frozenset(".DMS")
NEVER = -1


class Coverage(NamedTuple):
    """What the siren sweep found."""

    slowest: tuple[int, int]
    seconds: int
    silent: int


# ---- Part 1: the call-out ----
def call_out(mesh: dict[str, list[str]], control: str) -> tuple[list[list[str]], list[str]]:
    """Return the hop-by-hop roster of a radio call-out, and who misses it.

    Args:
        mesh: Each relay mapped to the relays that can hear it.
        control: The call-sign that transmits first.

    Returns:
        A pair. The hops, with hop 0 holding `control` alone and each hop's
        call-signs sorted A to Z; and every call-sign the mesh mentions that
        never hears the call, also sorted.

    Raises:
        ValueError: If `control` is not a call-sign the mesh mentions.
    """
    everyone = set(mesh)
    for listeners in mesh.values():
        everyone.update(listeners)
    if control not in everyone:
        raise ValueError(f"{control!r} is not on this mesh")

    queue = deque([control])
    heard = {control}
    hops: list[list[str]] = []
    while queue:
        this_hop: list[str] = []
        for _ in range(len(queue)):  # today's hop, frozen before it grows
            sign = queue.popleft()
            this_hop.append(sign)
            for listener in mesh.get(sign, ()):
                if listener not in heard:
                    heard.add(listener)
                    queue.append(listener)
        hops.append(sorted(this_hop))
    return hops, sorted(everyone - heard)


# ---- Part 2: the route ----
def find_mark(town: tuple[str, ...], mark: str) -> tuple[int, int]:
    """Return the single square carrying `mark`.

    Args:
        town: The rows of the town plan.
        mark: The character to find.

    Returns:
        The (row, column) of that square.

    Raises:
        ValueError: If the plan carries anything other than exactly one.
    """
    found = [
        (row, column)
        for row, line in enumerate(town)
        for column, square in enumerate(line)
        if square == mark
    ]
    if len(found) != 1:
        raise ValueError(f"the plan carries {len(found)} {mark!r} marks, not 1")
    return found[0]


def street_moves(town: tuple[str, ...], start: tuple[int, int], finish: tuple[int, int]) -> int | None:
    """Return the fewest street moves from `start` to `finish`.

    Args:
        town: The rows of the town plan.
        start: The square to set off from.
        finish: The square to reach.

    Returns:
        The number of one-square moves, 0 when the two are the same square,
        or None when no run of passable squares joins them.
    """
    rows, columns = len(town), len(town[0])
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        (row, column), moves = queue.popleft()
        if (row, column) == finish:
            return moves
        for down, across in STREET_MOVES:
            step = (row + down, column + across)
            if (
                0 <= step[0] < rows
                and 0 <= step[1] < columns
                and town[step[0]][step[1]] in PASSABLE
                and step not in seen
            ):
                seen.add(step)
                queue.append((step, moves + 1))
    return None


# ---- Part 3: the sirens ----
def siren_sweep(town: tuple[str, ...]) -> tuple[list[list[int]], Coverage]:
    """Return the seconds-to-hear map and a summary of the worst of it.

    Args:
        town: The rows of the town plan. Every `S` sounds at once.

    Returns:
        A pair. The map, holding the seconds until the nearest mast reaches
        each passable square and -1 everywhere else; and a `Coverage` giving
        the passable square that waits longest (lowest row then lowest
        column wins a tie), how long it waits, and how many passable squares
        hear nothing at all.
    """
    rows, columns = len(town), len(town[0])
    seconds = [[NEVER] * columns for _ in range(rows)]
    queue: deque[tuple[int, int]] = deque()
    for row in range(rows):
        for column in range(columns):
            if town[row][column] == "S":
                seconds[row][column] = 0
                queue.append((row, column))

    while queue:
        row, column = queue.popleft()
        for down, across in STREET_MOVES:
            step_row, step_column = row + down, column + across
            if (
                0 <= step_row < rows
                and 0 <= step_column < columns
                and town[step_row][step_column] in PASSABLE
                and seconds[step_row][step_column] == NEVER
            ):
                seconds[step_row][step_column] = seconds[row][column] + 1
                queue.append((step_row, step_column))

    slowest, worst, silent = (0, 0), NEVER, 0
    for row in range(rows):
        for column in range(columns):
            if town[row][column] not in PASSABLE:
                continue
            wait = seconds[row][column]
            if wait == NEVER:
                silent += 1
            if wait > worst:
                slowest, worst = (row, column), wait
    return seconds, Coverage(slowest=slowest, seconds=worst, silent=silent)


# ---- The report ----
def muster_report(town: tuple[str, ...], mesh: dict[str, list[str]]) -> list[str]:
    """Return the finished report, one line at a time.

    Args:
        town: The rows of the town plan.
        mesh: The relay mesh.

    Returns:
        The lines of the report, ready to print or write to a file.
    """
    lines = ["MUSTER REPORT", "=" * 13, "", "1. Radio call-out"]

    hops, stranded = call_out(mesh, CONTROL)
    for number, roster in enumerate(hops):
        lines.append(f"   hop {number}: {', '.join(roster)}")
    lines.append(f"   never hears it: {', '.join(stranded) or 'nobody'}")

    depot, muster = find_mark(town, "D"), find_mark(town, "M")
    moves = street_moves(town, depot, muster)
    lines += ["", "2. Depot to muster point"]
    lines.append(f"   depot at {depot}, muster point at {muster}")
    lines.append(f"   shortest run: {moves} moves" if moves is not None else "   no way through")

    _, coverage = siren_sweep(town)
    lines += ["", "3. Siren coverage"]
    lines.append(f"   slowest square: {coverage.slowest} at {coverage.seconds} seconds")
    lines.append(f"   squares that hear nothing: {coverage.silent}")
    return lines


# ---- Self-check ----
if __name__ == "__main__":
    print("\n".join(muster_report(TOWN, MESH)))

    hops, stranded = call_out(MESH, CONTROL)
    assert hops == [
        ["CONTROL"],
        ["NORTHGATE", "STAITHE"],
        ["BRIDGEFOOT", "QUAYSIDE"],
        ["MILLRACE"],
    ]
    assert stranded == ["OUTMARSH", "TIDEWELL"]

    depot, muster = find_mark(TOWN, "D"), find_mark(TOWN, "M")
    assert depot == (0, 0) and muster == (8, 10)
    assert street_moves(TOWN, depot, muster) == 34
    assert street_moves(TOWN, depot, depot) == 0

    seconds, coverage = siren_sweep(TOWN)
    assert seconds[0][10] == 0 and seconds[6][0] == 0  # the two masts
    assert coverage.silent == 0  # every passable square hears something
    assert coverage.seconds == 16
    assert coverage.slowest == (6, 8)

    # Take the masts away and nothing is heard anywhere.
    quiet = tuple(row.replace("S", ".") for row in TOWN)
    _, quiet_coverage = siren_sweep(quiet)
    assert quiet_coverage.seconds == NEVER
    assert quiet_coverage.silent == sum(
        1 for row in quiet for square in row if square in PASSABLE
    )

    for mark in ("D", "M"):
        try:
            find_mark(("...", "..."), mark)
        except ValueError as error:
            assert "marks, not 1" in str(error)
        else:
            raise AssertionError("expected ValueError")

    try:
        call_out(MESH, "SEAWALL")
    except ValueError as error:
        assert "is not on this mesh" in str(error)
    else:
        raise AssertionError("expected ValueError")

    print("")
    print("All checks passed.")
```

The three searches are deliberately not factored into one generic function. They
could be, and the week's argument is that they are the same algorithm — but
writing them out separately is what lets you see that the queue, the seen-set and
the loop body really are identical, which reading a parameterised version would
hide.

## Run it

Download the solution beside this page and run it:

```bash
python README.py
```

No third-party packages, no arguments, no input. It prints the three-part muster
report and then `All checks passed.`

## Common bugs to catch

- **Marking seen on dequeue.** Symptom: correct answers and a queue that grows
  far past the square count. The bug that survives testing.
- **A list as the queue.** Symptom: correct answers, quadratic time, and nothing
  in the output to tell you.
- **One BFS per mast.** Symptom: the right distance map for several times the
  work — and a write-up that has missed the point of the week.
- **Treating the mesh as undirected.** Symptom: Outmarsh and Tidewell suddenly
  hear the call, which the data plainly says they do not.
- **Walking onto `#`.** Symptom: a route shorter than the map allows. The
  passable set is `.DMS`, and the depot, muster point and masts are all streets.
- **Raising on an unreachable muster point.** Symptom: an exception where `None`
  is the honest answer.
- **Recomputing inside the printer.** Symptom: a report that disagrees with the
  functions it claims to be reporting.

## Acceptance checklist

- [ ] The call-out reaches six relays across four hops; Outmarsh and Tidewell are
      named as never hearing it.
- [ ] The depot-to-muster route is 34 moves.
- [ ] The slowest square is at 16 seconds, and no square hears nothing.
- [ ] `find_mark` raises `ValueError` for a missing or duplicated mark.
- [ ] An unreachable muster point returns `None` rather than raising.
- [ ] The file runs start to finish and prints `All checks passed.`
- [ ] Both write-ups exist, both have memos, and they cross-reference each other.

## Stretch

- Report which single flooded square, if cleared, would shorten the route most.
  It is one BFS per candidate and the answer is not always the obvious square.
- Add a second control room and re-run the call-out as a multi-source search on
  the mesh. The grid and the mesh then use the same idiom, which is worth a
  paragraph.
- Weight the streets — some are slower than others — and say plainly what breaks.
  Breadth-first search stops being correct at that point, and naming why is worth
  more than the code that replaces it.

## Self-reflection

Close the mini-project README with four short paragraphs:

1. **Which of the three searches you got wrong first**, and what the symptom was.
2. **The one line** that differs between the grid search and the mesh search,
   written out.
3. **The pair comparison.** How multi-source and single-source differ in what
   goes into the queue before the loop, in one paragraph.
4. **What you would do differently.** One concrete thing.

## After the mini-project

Week 7 is depth-first search, and it will be introduced by contrast with this
week. If you cannot say, from memory, why breadth-first search finds shortest
paths and depth-first search does not, re-read your own Problem 1 memo before
Monday.
