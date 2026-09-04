# Challenge 1 — The Kiln Firing Trail

> Topic: grid backtracking with a visited set · Lecture: [3](../lecture-notes/03-grid-backtracking-and-constraint-satisfaction.md) · Difficulty: Medium · Target time: 60 minutes including the FRAME write-up · Why this one: counting every trail, rather than stopping at the first, is what forces the pruning to be correct instead of merely lucky.

## The Brief

A pottery kiln holds its shelves in a grid, and each shelf carries one glaze
code — a single letter. A firing schedule is a sequence of those codes, loaded in
order. The loader may step only between shelves that share an edge — up, down,
left, right, never diagonally — and cannot put two pots on the same shelf, so a
trail never revisits a shelf.

The question is **not** "is there a trail?" The operator already assumes there is
one. What they need to know is **how many** there are, because a schedule with
exactly one trail cannot be loaded wrongly, and a schedule with fourteen will be.

That change of question is the whole challenge. A search that stops at its first
hit can be sloppy about pruning and still look correct. A search that has to find
them all cannot.

## Starter

The worked answer on this page carries the rack and the self-checks you must
satisfy.

```text
A B C E
S F E S
A D E E
```

Try `ABCE` by eye before you write anything. It looks like the top row. It is not
only the top row — and finding the second one by hand is the fastest way to
understand what the counting is for.

## Requirements

1. `all_trails(rack, schedule)` returns every trail, each a list of
   `(row, column)` in visiting order.
2. `count_trails(...)` returns how many there are.
3. `first_trail(...)` returns the **smallest trail in reading order**, or `None`.
   Smallest compares the trails as sequences of coordinates, so the one starting
   nearest the top-left wins and ties are settled by where it goes next.
4. A malformed rack — empty, or rows of differing length — raises `ValueError`
   rather than being half-searched.
5. `trail_report(...)` prints the count and the first trail per schedule.

## Constraints

- **Four neighbours, never eight.** Diagonal steps are not loading moves.
- **A shelf carries one pot.** The visited set is per trail, not global, and it
  must be undone on the way back out.
- **The empty schedule has no trail**, not one empty trail. Both readings are
  defensible; the contract picks one and your code must match it.
- **"Smallest" must be defined** before you can return it. An unstated ordering
  is two correct programs disagreeing.
- Prune on the glaze code **before** recursing, not inside the call. Both are
  correct; only one avoids exploring a whole level of shelves that could never
  spell anything.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python challenge-01-kiln-firing-trail.py
the rack
    A B C E
    S F E S
    A D E E

schedules
    ABCE   trails  2   first (0,0) (0,1) (0,2) (0,3)
    SEE    trails  2   first (1,3) (1,2) (2,2)
    ASA    trails  2   first (0,0) (1,0) (2,0)
    ABCF   trails  0   first -
    E      trails  4   first (0,3)
    SFDA   trails  1   first (1,0) (1,1) (2,1) (2,0)

All checks passed.
```

`ABCE` reporting **2** is the row that matters. After `C` at `(0,2)` the loader
can step right to the `E` at `(0,3)` or drop to the `E` at `(1,2)`. Both spell
the schedule. A first-hit search reports 1 and is wrong, and nothing about its
output looks wrong.

## Steps

1. Read the self-checks. They are the spec.
2. Write the memo: name the structure (grid backtracking), the state (position,
   how much is spelled, what is visited) and the undo.
3. Write `_walk` first, with the mark and the undo adjacent in the code so the
   pairing is visible.
4. Get `ABCE` to report 2 before going further. If it reports 1, your search is
   returning early; if it reports 3, your undo is leaking.
5. Add the ordering for `first_trail` and say in one sentence what it compares.
6. Add the `ValueError` guards, then write the FRAME pass.

## The Solution

```python
"""challenge-01-kiln-firing-trail-solution.py - every trail that spells the schedule.

A pottery kiln holds its shelves in a grid. Each shelf carries one glaze code,
a single letter. A firing schedule is a sequence of glaze codes that must be
loaded in order, and the loader may only step between shelves that share an
edge - up, down, left or right, never diagonally - and may not put two pots on
the same shelf, so a trail never revisits a shelf.

The question is not "is there a trail?". A kiln operator already knows there is
one; they want to know HOW MANY there are, because a schedule with exactly one
trail is a schedule that cannot be loaded wrongly, and one with fourteen is a
schedule that will be.

  count_trails    - how many distinct trails spell the schedule
  first_trail     - the smallest trail in reading order, or None
  trail_report    - both, for a handful of schedules

Counting is what makes the pruning matter. A search that stops at the first hit
can be sloppy and still look right; a search that must find them all cannot.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

# ---- Given data ----
# One glaze code per shelf, top row first.
RACK: list[list[str]] = [
    ["A", "B", "C", "E"],
    ["S", "F", "E", "S"],
    ["A", "D", "E", "E"],
]

STEPS: tuple[tuple[int, int], ...] = ((-1, 0), (0, -1), (0, 1), (1, 0))


# ---- Your task ----
def _walk(
    rack: list[list[str]],
    schedule: str,
    row: int,
    col: int,
    at: int,
    used: set[tuple[int, int]],
    trail: list[tuple[int, int]],
    found: list[list[tuple[int, int]]],
) -> None:
    """Extend the trail from one shelf, recording every completion.

    Args:
        rack: The shelf grid.
        schedule: The glaze codes to spell.
        row: Current shelf row.
        col: Current shelf column.
        at: How many codes of the schedule are already spelled.
        used: Shelves already carrying a pot on this trail.
        trail: The shelves visited, in order.
        found: Every completed trail, appended to in place.
    """
    if at == len(schedule):
        found.append(list(trail))
        return

    height, width = len(rack), len(rack[0])
    for drow, dcol in STEPS:
        nrow, ncol = row + drow, col + dcol
        if not (0 <= nrow < height and 0 <= ncol < width):
            continue
        if (nrow, ncol) in used:
            continue
        # The prune that matters: reject on the CODE before recursing, not
        # inside the call. Checking after the call still works and explores a
        # whole level of shelves that could never spell anything.
        if rack[nrow][ncol] != schedule[at]:
            continue
        used.add((nrow, ncol))
        trail.append((nrow, ncol))
        _walk(rack, schedule, nrow, ncol, at + 1, used, trail, found)
        # Undo, always. The set and the list are shared across every branch, so
        # a branch that forgets to unmark poisons its siblings.
        trail.pop()
        used.discard((nrow, ncol))


def all_trails(rack: list[list[str]], schedule: str) -> list[list[tuple[int, int]]]:
    """Every trail through the rack that spells the schedule.

    Args:
        rack: The shelf grid. Must be rectangular and non-empty.
        schedule: The glaze codes to spell, in order.

    Returns:
        A list of trails, each a list of (row, column). Empty when none exists.
        An empty schedule spells nothing and has no trail - not one empty trail.

    Raises:
        ValueError: If the rack is empty or its rows differ in length.
    """
    if not rack or not rack[0]:
        raise ValueError("the rack has no shelves")
    if len({len(row) for row in rack}) != 1:
        raise ValueError("the rack is not rectangular")
    if not schedule:
        return []

    found: list[list[tuple[int, int]]] = []
    for row in range(len(rack)):
        for col in range(len(rack[0])):
            if rack[row][col] != schedule[0]:
                continue
            _walk(rack, schedule, row, col, 1, {(row, col)}, [(row, col)], found)
    return found


def count_trails(rack: list[list[str]], schedule: str) -> int:
    """How many distinct trails spell the schedule."""
    return len(all_trails(rack, schedule))


def first_trail(
    rack: list[list[str]], schedule: str
) -> list[tuple[int, int]] | None:
    """The smallest trail in reading order, or None when there is none.

    "Smallest" compares the trails as sequences of (row, column), so the trail
    starting nearest the top-left wins, and ties are broken by where it goes
    next. Naming the order matters: without it, two correct programs disagree.
    """
    trails = all_trails(rack, schedule)
    return min(trails) if trails else None


def trail_report(rack: list[list[str]], schedules: list[str]) -> None:
    """Print the count and the first trail for each schedule."""
    for schedule in schedules:
        trails = all_trails(rack, schedule)
        best = min(trails) if trails else None
        shown = " ".join(f"({r},{c})" for r, c in best) if best else "-"
        print(f"    {schedule:<6} trails {len(trails):>2}   first {shown}")


# ---- Self-check ----
if __name__ == "__main__":
    print("the rack")
    for row in RACK:
        print("    " + " ".join(row))
    print()
    print("schedules")
    trail_report(RACK, ["ABCE", "SEE", "ASA", "ABCF", "E", "SFDA"])

    # "ABCE" looks like the top row and is not only the top row: after C at
    # (0,2) the loader can drop to the E at (1,2) instead of stepping right.
    # A search that stops at its first hit reports 1 here and is wrong.
    assert count_trails(RACK, "ABCE") == 2
    assert first_trail(RACK, "ABCE") == [(0, 0), (0, 1), (0, 2), (0, 3)]

    # "SEE" starts from two different S shelves.
    assert count_trails(RACK, "SEE") == 2
    assert first_trail(RACK, "SEE") == [(1, 3), (1, 2), (2, 2)]

    # A single code is a trail of one shelf, once per matching shelf. Four
    # shelves carry E: (0,3), (1,2), (2,2) and (2,3).
    assert count_trails(RACK, "E") == 4
    assert first_trail(RACK, "E") == [(0, 3)]

    # "ASA" turns a corner and comes back down the left edge.
    assert count_trails(RACK, "ASA") == 2
    assert first_trail(RACK, "ASA") == [(0, 0), (1, 0), (2, 0)]

    # No trail at all: F sits alone, with no adjacent shelf spelling nothing.
    assert count_trails(RACK, "ABCF") == 0
    assert first_trail(RACK, "ABCF") is None

    # The empty schedule spells nothing, so there is no trail - not one empty
    # trail. Say which it is; both are defensible and only one is the contract.
    assert count_trails(RACK, "") == 0
    assert first_trail(RACK, "") is None

    # A shelf cannot carry two pots, so a schedule needing one twice in a row
    # has no trail even when the codes are adjacent.
    assert count_trails([["A", "A"]], "AAA") == 0

    # Malformed racks are refused rather than half-searched.
    for bad in ([], [[]], [["A", "B"], ["C"]]):
        try:
            all_trails(bad, "A")
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad!r}")

    print()
    print("All checks passed.")
```

The mark and the undo sit either side of the recursive call, four lines apart,
on purpose. The single most common backtracking bug is an undo that is skipped on
one branch, and the way to not write it is to never let the two drift apart.

## Run it

Download the solution beside this page and run it:

```bash
python challenge-01-kiln-firing-trail.py
```

No third-party packages, no arguments, no input. It prints the rack, the report,
and then `All checks passed.`

Or open it in the browser IDE from the Run button on the block above and add a
schedule of your own.

## Common bugs to catch

- **Returning on the first completion.** Symptom: every count is 1 or 0, and
  `ABCE` reports 1. A counting search records and *keeps going*.
- **Forgetting to unmark.** Symptom: counts too low, and lower the longer the
  schedule. The shelf stays occupied for every sibling branch.
- **Unmarking in the wrong place.** Symptom: counts too high, often wildly.
  Unmark after the call returns, not before it.
- **Checking the code inside the recursive call.** Symptom: correct answers,
  visibly slower, and a call stack full of frames that die immediately.
- **Diagonal steps.** Symptom: extra trails that no loader could walk. Four
  offsets, not eight.
- **Treating the empty schedule as one empty trail.** Symptom: `count_trails`
  returns 1 for `""`. Read the contract.

## Acceptance checklist

- [ ] `ABCE` reports 2 trails, first `(0,0) (0,1) (0,2) (0,3)`.
- [ ] `E` reports 4 — one per shelf carrying that code.
- [ ] `ABCF` reports 0 and `first_trail` returns `None`.
- [ ] `""` reports 0 trails.
- [ ] A rack with ragged rows raises `ValueError`.
- [ ] The write-up names the ordering `first_trail` uses.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Report the count **per starting shelf** rather than in total. The change is
  small and it turns the answer into something an operator could act on.
- Add a rule that the trail may not turn more than twice, and say where the prune
  goes. Constraints that depend on the path so far are the interesting ones.
- Count trails on a 12×12 rack of random codes and watch the number climb. Then
  say honestly what the worst case of this search is, and why the prune does not
  change it.
