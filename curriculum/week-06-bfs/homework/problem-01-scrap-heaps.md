# Problem 1 — Scrap Heaps

> **Topic:** finding the separate islands in a grid, and measuring each one
> **Lecture:** [02 — Grid BFS and Graph BFS](../lecture-notes/02-grid-bfs-and-graph-bfs.md)
> **Difficulty:** Medium
> **Target time:** 45 minutes
> **Why this one:** every grid page so far has run one search. This runs many — one per island — and the whole trick is that a single shared `counted` set across all of them is what keeps the total work linear. It is also the first page where the answer is not a distance at all, which is a useful reminder that the queue is a tool, not a purpose.

## The Brief

A drone photographs a salvage yard. The photograph comes back as rows of
text: `#` is scrap metal, `.` is bare ground.

Scrap that touches **edge to edge** is one heap. Scrap that touches only at a
**corner** is two heaps, because the grab cannot lift across a corner — it
would drop the load. So a diagonal touch is not a join, and the yard in the
starter has a deliberate pair of single sheets meeting at a corner so that
you can see the difference in the answer.

The yard manager does not want the number of heaps. He wants the **sizes**,
biggest first, so he can decide which heaps the grab clears today. Equal
sizes keep no particular order, because nothing about two heaps of five
distinguishes one from the other.

An empty photograph, or one with no scrap on it, gives back an empty list.
Not zero, not `None` — an empty list, because "here are the sizes" of nothing
is a list with nothing in it, and a caller writing `sum(sizes)` should get
`0` without a guard.

## Starter

Create `problem-01-scrap-heaps.py` in your practice repo and paste this in.
Fill in every `TODO`.

```python
"""problem-01-scrap-heaps.py — measuring the heaps in a salvage yard.

A drone photograph of a salvage yard, drawn as rows of text. A hash is scrap
metal, a dot is bare ground. Scrap that touches edge to edge is one heap; a
corner touch is not enough, because a grab cannot lift across a corner.

The yard manager does not want the number of heaps. He wants the sizes,
biggest first, so he can plan which ones the grab clears today.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from collections import deque

# ---- Given data ----
# A yard with one long heap, several middling ones, and a single sheet at
# (3, 8) that touches the pair above it only at a corner — so it is a heap
# of its own, not part of theirs.
YARD: tuple[str, ...] = (
    "##....###.",
    "##.....#..",
    "#........#",
    "....##..#.",
    "#...##....",
    "#...##..#.",
    "#.......#.",
    "......###.",
    ".#....#...",
    ".#....#...",
)

TOUCHING: tuple[tuple[int, int], ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))


# ---- Your task ----
def heap_sizes(yard: tuple[str, ...]) -> list[int]:
    """Return the size of every scrap heap, biggest first.

    Args:
        yard: The rows of the photograph. `#` is scrap, `.` is bare ground.

    Returns:
        One number per heap — how many squares of scrap it holds — sorted
        largest to smallest. Equal sizes keep no particular order because
        nothing distinguishes them. An empty yard, or one with no scrap in
        it, gives an empty list.
    """
    # TODO: an empty photograph returns [] before anything else
    # TODO: ONE `counted` set for the whole function, outside both loops
    # TODO: scan every square; skip bare ground and squares already counted
    # TODO: on a fresh scrap square, run a walk that counts its whole heap
    #       and adds every square of it to `counted`
    # TODO: collect the sizes, then return them sorted largest first
    ...


# ---- Self-check ----
if __name__ == "__main__":
    sizes = heap_sizes(YARD)
    print(f"heaps    : {len(sizes)}")
    print(f"sizes    : {sizes}")
    print(f"scrap    : {sum(sizes)} squares")

    assert sum(sizes) == sum(row.count("#") for row in YARD)
    assert sizes == sorted(sizes, reverse=True)
    assert sizes == [7, 6, 5, 4, 3, 2, 1, 1]
    # The sheet at (3, 8) and the sheet at (2, 9) meet at a corner only, so
    # they are the two heaps of size 1 rather than one heap of size 2.
    assert sizes.count(1) == 2

    # A corner touch is not a join. These two heaps stay separate.
    assert heap_sizes(("#.", ".#")) == [1, 1]
    # An edge touch is.
    assert heap_sizes(("##", "..")) == [2]
    # Nothing to count.
    assert heap_sizes(()) == []
    assert heap_sizes(("",)) == []
    assert heap_sizes(("...", "...")) == []
    # One heap filling the whole yard.
    assert heap_sizes(("###", "###")) == [6]

    print("All checks passed.")
```

One idea before you start.

**One `counted` set for the whole yard, not one per heap.** It is tempting to
make a fresh set inside the scan for each heap you find. Do that and the
outer scan will start a *second* walk from every square of a heap it has
already measured, and the work goes from linear to quadratic. The shared set
is what lets the outer scan say "skip, done that" in one lookup.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-06-bfs/homework/problem-01-scrap-heaps.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `heap_sizes` returns a `list[int]`, sorted largest first.
2. The sizes add up to the number of `#` squares in the photograph.
3. Two scrap squares touching only at a corner belong to different heaps.
4. Two scrap squares sharing an edge belong to the same heap.
5. `heap_sizes(())`, `heap_sizes(("",))` and a yard of all bare ground each
   return `[]`.
6. Every scrap square is counted exactly once, across all heaps.
7. `heap_sizes` keeps its type hints and its docstring.

## Constraints

- **One `counted` set, shared by every heap.** With a set per heap the outer
  scan restarts a walk from each square of each heap, so a yard of `n`
  squares in one heap does `n` walks of `n` squares — `O(n²)`. Shared, it is
  `O(rows × columns)` however the scrap is arranged.

- **Mark the starting square before the walk begins.** Not inside the loop's
  first turn. Otherwise the outer scan can reach it again before the walk
  does, and start a second walk over the same heap.

- **Four directions, not eight.** The corner rule is the whole reason the
  page has a `TOUCHING` tuple with four entries in it. Adding the diagonals
  is a one-line change that gives a different, also-reasonable answer to a
  different question — and it is the single most likely way to get this wrong
  by accident.

- **Bounds before the lookup.** Same rule as every grid page: a missing lower
  bound wraps to the far edge rather than raising, so it merges heaps that
  are nowhere near each other and nothing tells you.

- **Sort once, at the end.** Collect the sizes as you find them and sort the
  finished list. Inserting into a sorted list per heap does more work and
  reads worse.

- **The answer is sizes, not a count.** `len(heap_sizes(yard))` gives the
  number of heaps for free. Building the count instead and then trying to
  recover the sizes does not work in the other direction, which is why the
  richer answer is the one the function returns.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
@@OUTPUT@@
```

Eight heaps, twenty-nine squares of scrap. The two heaps of size one are the
corner-touching pair — the sheet at row 3, column 8, and the sheet at row 2,
column 9. If your answer shows seven heaps with a `2` where those two ones
are, you have the diagonals switched on.

The first assert is the one worth keeping in your own tests forever: the
sizes must add up to the number of `#` characters in the photograph. That
single line catches double-counting, missed squares and merged heaps all at
once, and it does not need you to know the right answer in advance.

## Steps

1. Create the file, paste the starter, and run it. It fails at the first use.
2. Write the outer scan on its own, printing every fresh scrap square it
   finds, with **no** walk at all. You should see twenty-nine of them — one
   per scrap square, because nothing is being marked yet.
3. Add the walk and the shared `counted` set. The same print should now fire
   eight times.
4. Count one heap by hand from the photograph and check it against your
   answer. The seven is the bottom-right one; trace it with a finger.
5. Run the sum assert. If it fails high, a square is being counted twice —
   look at where you mark the starting square.
6. Switch `TOUCHING` to eight directions on purpose, run, and look at how the
   answer changes. Then switch it back. Knowing what the wrong version looks
   like is worth two minutes.
7. When `All checks passed.` prints, write your own photograph with a heap
   shaped like a ring and check the hole in the middle is not counted.

## The Solution

```python
@@CODE@@
```

**The outer scan and the inner walk do different jobs.**

The scan's job is to find a square that belongs to a heap nobody has measured
yet. The walk's job is to measure exactly one heap and mark every square of
it. The `counted` set is the only thing the two share, and it is what makes
the scan's `or (row, column) in counted` test enough to skip a whole heap in
one lookup.

Once you see it that way, the total cost is easy to argue: the scan looks at
each square once, and the walks between them look at each scrap square once.
Two passes over the yard, whatever shape the scrap is in.

**`counted.add((row, column))` happens before the queue does anything.**

```python
counted.add((row, column))
queue = deque([(row, column)])
```

Marking the seed square first is the same enqueue-time rule as everywhere
else this week, applied to the one square that has no neighbour to mark it.
Leave it out and the walk itself will re-enqueue the seed from one of its own
neighbours, counting it twice and inflating the heap by one.

**`size` counts pops, not appends.** Every square is popped exactly once, so
counting on the way out is exact. Counting on the way in would also work here
because each square is appended exactly once too — but only because the
marking is right, and tying the count to the marking rather than to a second
place is one fewer thing that can drift.

**Four offsets, and the corner rule lives entirely in that tuple.** There is
no code anywhere that mentions corners. The rule is expressed by which
offsets exist, which is the cleanest way to express it: change the tuple and
the meaning of "one heap" changes with it, and nothing else has to move.

**`sorted(sizes, reverse=True)` at the end, once.** The sizes come out in
whatever order the scan met the heaps in — which is top-left to bottom-right,
and is not what was asked for. One sort, one line, and it is presentation
rather than algorithm.

**Why no distances anywhere.** Every other page this week used the queue to
measure how far. This one uses it only to *reach* — the order things come out
in does not matter at all, and a stack would give the same sizes. That is
worth knowing: when the answer is "which things are connected", breadth-first
and depth-first are interchangeable, and you should pick on other grounds.
Next week's page picks the other one.

## Download and run

Download
[problem-01-scrap-heaps-solution.py](./problem-01-scrap-heaps-solution.py)
and run it:

```bash
python problem-01-scrap-heaps-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `problem-01-scrap-heaps.py`.

## Common bugs to catch

- **The sizes add up to more than the scrap on the photograph.** No
  exception:

  ```text
  scrap    : 34 squares
  ```

  against twenty-nine `#` characters. Squares are being counted twice, which
  means a square gets into the queue twice. Mark at enqueue time, and mark
  the seed square before the loop starts.

- **Seven heaps, with a `2` instead of two `1`s.** You are using eight
  directions. The corner-touching pair merged. Check the `TOUCHING` tuple has
  exactly four entries.

- **The program takes noticeably long on a big yard.** You built a fresh
  `counted` set per heap, so the outer scan restarts a walk from every square
  of every heap. One set, outside both loops.

- **`IndexError: string index out of range`.**

  ```text
  Traceback (most recent call last):
      yard[next_cell[0]][next_cell[1]] == "#"
      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
  IndexError: string index out of range
  ```

  A missing upper bounds check. The missing lower one does not raise — it
  wraps, and merges the left edge of the yard with the right.

- **`TypeError: unhashable type: 'list'`.**

  ```text
  Traceback (most recent call last):
      seen.add([0, 1])
      ~~~~~~~~^^^^^^^^
  TypeError: unhashable type: 'list'
  ```

  Squares in a set have to be tuples.

- **`heap_sizes(("",))` raises instead of returning `[]`.** Your empty guard
  checks `not yard` but not `not yard[0]`. A photograph of one empty row is
  still a photograph of nothing.

- **The list comes back smallest first.** `sorted` ascends by default. Pass
  `reverse=True`, and note that `sorted(sizes)[::-1]` gives the same answer
  while saying it less clearly.

## Under the hood

<details>
<summary>Under the hood — the cost of many searches, and why the traversal order does not matter here</summary>

**Cost, argued properly.** Let the yard be `R` by `C`. The outer scan looks
at `R × C` squares and does one set lookup each. The walks, added together,
pop each scrap square exactly once and examine four neighbours each. So the
whole function is `O(R × C)` — the *same* as one search, even though it runs
one search per heap.

That surprises people, and it is worth being able to say why: the searches do
not overlap. The shared `counted` set partitions the scrap between them, so
their costs add up to one pass rather than multiplying.

Take the shared set away and the argument collapses. A yard that is one solid
heap of `n` squares would run `n` walks, each covering `n` squares —
`O(n²)`, which on a 1000 x 1000 photograph is 10¹² operations against 10⁶.

**Why a stack would do just as well.** Nothing here reads the order squares
come out in. The answer is "how many squares are connected to this one", and
connectivity does not care how you walk. Swap the `deque` for a list and
`popleft` for `pop` and you have a depth-first search that returns identical
sizes.

So why breadth-first? On this page, habit and consistency — it is the week's
tool. In production the choice is about memory: breadth-first holds a frontier
that can be as wide as the heap, depth-first holds a path that can be as long
as the heap, and which is smaller depends on the shape. A recursive
depth-first version is the shortest code of the three and will exceed
Python's recursion limit at around a thousand connected squares, which is
smaller than a real photograph. That is usually the deciding argument.

**The "sizes add up" invariant.** `sum(heap_sizes(yard)) == total scrap` is a
property test: it must hold for every possible yard, and it does not require
you to know the right answer for any particular one. Properties like that are
worth hunting for on every problem, because they catch bugs on inputs you
never thought to write down. Here it catches double-counting, skipped
squares, and heaps merged by a bounds error, all in one line.

**A related question with a very different answer.** "How many *distinct
shapes* of heap are there, up to translation?" sounds like a small extension
and is not: it needs each heap recorded as a normalised set of offsets and
then compared, and the comparison is where all the difficulty moves. Noticing
that a small change in wording moves the difficulty is a skill worth
practising deliberately.

</details>

## Acceptance checklist

- [ ] `python problem-01-scrap-heaps.py` prints three lines then
      `All checks passed.`
- [ ] The output matches the expected block character for character.
- [ ] There is exactly one `counted` set in the function.
- [ ] The seed square is marked before the walk's loop begins.
- [ ] `TOUCHING` has four entries and the corner pair stays as two heaps.
- [ ] The sizes add up to the number of `#` characters.
- [ ] Empty inputs return `[]` rather than raising.
- [ ] The function has type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 6 homework 1: scrap heaps`.

## Stretch

- **Report where each heap is, not just how big.** Keep the top-left square
  of each heap alongside its size.

  ```python
  def heap_report(yard: tuple[str, ...]) -> list[tuple[int, tuple[int, int]]]:
      """Return (size, first square) per heap, biggest first."""
      report = []
      counted: set[tuple[int, int]] = set()
      rows, columns = len(yard), len(yard[0]) if yard else (0, 0)
      for row in range(rows):
          for column in range(columns):
              if yard[row][column] != "#" or (row, column) in counted:
                  continue
              counted.add((row, column))
              queue, size = deque([(row, column)]), 0
              while queue:
                  at_row, at_column = queue.popleft()
                  size += 1
                  for down, across in TOUCHING:
                      cell = (at_row + down, at_column + across)
                      if (
                          0 <= cell[0] < rows
                          and 0 <= cell[1] < columns
                          and yard[cell[0]][cell[1]] == "#"
                          and cell not in counted
                      ):
                          counted.add(cell)
                          queue.append(cell)
              report.append((size, (row, column)))
      return sorted(report, reverse=True)
  ```

  ```text
  [(7, (5, 8)), (6, (3, 4)), (5, (0, 0)), (4, (0, 6)),
   (3, (4, 0)), (2, (8, 1)), (1, (3, 8)), (1, (2, 9))]
  ```

  The scan order means the "first square" is always the topmost, then
  leftmost, square of its heap — a useful stable label that comes free.

- **Switch the corner rule on and see the answer change.** One line.

  ```python
  TOUCHING_EIGHT = TOUCHING + ((-1, -1), (-1, 1), (1, -1), (1, 1))
  ```

  ```text
  four ways : [7, 6, 5, 4, 3, 2, 1, 1]
  eight ways: [7, 6, 5, 4, 3, 2, 2]
  ```

  Eight heaps become seven: the corner-touching pair joins into one heap of
  two and nothing else moves. A single character of the direction tuple is
  the entire difference between "the grab can lift this in one go" and "the
  grab drops it", which is exactly why the rule had to be written into the
  spec rather than assumed.

- **Find the largest heap that fits inside a bounding box you name.** A
  filter over the walk rather than a change to it.

  ```python
  def heaps_within(yard: tuple[str, ...], height: int, width: int) -> list[int]:
      """Return the sizes of heaps whose bounding box fits in height x width."""
      ...
  ```

  ```text
  heaps fitting in 3 x 3: [6, 5, 4, 3, 2, 1, 1]
  ```

  The interesting part is that you have to track the minimum and maximum row
  and column while walking, which means the walk now produces four numbers
  instead of one. Deciding whether that belongs in the walk or in a second
  pass is the design question, and both answers are defensible.

Next: [Problem 2 — Worst-Served Bay](./problem-02-worst-served-bay.md).
