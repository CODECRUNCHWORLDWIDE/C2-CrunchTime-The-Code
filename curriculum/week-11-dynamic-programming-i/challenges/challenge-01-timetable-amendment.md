# Challenge 1 — The Timetable Amendment Slip

> Topic: two-sequence DP with a reconstructed answer · Lecture: [2](../lecture-notes/02-2d-dp-and-the-grid-and-string-shapes.md) · Difficulty: Medium-Hard · Target time: 75 minutes including the FRAME write-up · Why this one: the costs are unequal and the answer is a list, so neither counting edits nor keeping a running total will do.

## The Brief

A branch line publishes its timetable as a sequence of station codes. When the
timetable changes the operator does not reprint it — they issue an **amendment
slip** listing the edits a guard makes by hand:

```text
INSERT  a station    costs 3     a new stop has to be advertised
REMOVE  a station    costs 2     a stop is struck through
REPLACE a station    costs 4     struck through and rewritten
KEEP    a station    costs 0
```

The costs are **not equal**, and that is the problem. Two amendments with the
same *number* of edits can cost different amounts, so counting edits gives the
wrong answer. And a guard needs to read the slip, so the answer is the list of
edits — not a number.

## Starter

The worked answer on this page carries the timetables and the self-checks.

```text
old:  BRY  CRB  DNM  ELV  FNW
new:  BRY  DNM  GRV  ELV  FNW
```

Work it by eye first. Two edits are obvious. Now check the arithmetic: is
striking one station and adding another cheaper than replacing it? With these
costs, sometimes.

## Requirements

1. `amendment_cost(old, new)` returns the cheapest total.
2. `amendment_slip(old, new)` returns the edits **in reading order**, one line
   each, including `KEEP` lines — a guard needs the untouched stations shown or
   they lose their place.
3. The reconstruction walks a **cost table**. A single running total cannot say
   which neighbour a cost came from.
4. `slip_report(...)` prints both for several pairs.
5. Empty timetables work on either side, and two empty ones cost 0.

## Constraints

- **Costs are constants at the top of the file**, and changing them must change
  the slip. A solution that hardcodes "one edit" for a substitution is reading
  the example rather than the contract.
- **A station that stays is free**, and taking it is never worse than paying to
  replace it with itself. Say why in your memo; it is the line that collapses
  four cases to three.
- **The slip must reconstruct the new timetable** when followed. That is the
  strongest test you can write, and it is worth writing before the pretty
  output.
- Row 0 and column 0 are the recurrence, not special cases: they are the cost of
  amending from nothing, and to nothing.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python challenge-01-timetable-amendment.py
amendment slips
    BRY CRB DNM ELV FNW  ->  BRY DNM GRV ELV FNW
        cost 5
        KEEP    BRY
        REMOVE  CRB
        KEEP    DNM
        INSERT  GRV
        KEEP    ELV
        KEEP    FNW

    BRY CRB  ->  BRY CRB
        cost 0
        KEEP    BRY
        KEEP    CRB

    BRY CRB  ->  (empty)
        cost 4
        REMOVE  BRY
        REMOVE  CRB

    (empty)  ->  BRY CRB
        cost 6
        INSERT  BRY
        INSERT  CRB

All checks passed.
```

The shipped pair costs **5**: strike `CRB` for 2, insert `GRV` for 3. Note it did
*not* choose to replace — replacing would cost 4 for one edit, but the two
stations sit in different places, so a replace does not apply. Reading the slip
tells you why in a way the number never could.

## Steps

1. Read the self-checks. They are the spec.
2. Write the memo: name the table's axes and what an entry means, in one
   sentence each.
3. Fill the first row and column, and say out loud what they mean before filling
   the interior.
4. Get `amendment_cost` right on the shipped pair and on both empty cases.
5. Write the backward walk. Test it by reconstructing the new timetable from the
   slip — that assertion catches more than eyeballing ever will.
6. Change `REPLACE_COST` to 6 and check the slip changes shape. Then change it
   back.
7. Write the FRAME pass.

## The Solution

```python
"""challenge-01-timetable-amendment-solution.py - the cheapest amendment slip.

A branch line publishes a timetable as a sequence of station codes. When the
timetable changes, the operator does not reprint it; they issue an amendment
slip listing the edits a guard must make by hand:

    INSERT a station     costs 3   (a new stop has to be advertised)
    REMOVE a station     costs 2   (a stop is struck through)
    REPLACE a station    costs 4   (struck through and rewritten)
    KEEP a station       costs 0

The costs are not equal, and that is the whole problem. Two amendments with the
same NUMBER of edits can cost different amounts, so counting edits gives the
wrong answer. A guard wants the cheapest slip, and they want to read it - so the
answer is the list of edits, not a number.

  amendment_cost   - the cheapest total
  amendment_slip   - the edits themselves, in reading order
  slip_report      - both, for a few timetables

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

INSERT_COST = 3
REMOVE_COST = 2
REPLACE_COST = 4

# ---- Given data ----
OLD_LINE: tuple[str, ...] = ("BRY", "CRB", "DNM", "ELV", "FNW")
NEW_LINE: tuple[str, ...] = ("BRY", "DNM", "GRV", "ELV", "FNW")


# ---- Your task ----
def _table(old: tuple[str, ...], new: tuple[str, ...]) -> list[list[int]]:
    """Cheapest cost to turn old[:row] into new[:col], for every row and col.

    The table is (len(old) + 1) by (len(new) + 1). Row 0 is "the old timetable
    is empty", so every entry is the cost of inserting that many stations;
    column 0 is the mirror.

    Args:
        old: The published timetable.
        new: The timetable it must become.

    Returns:
        The full cost table. Returning the table rather than one number is what
        lets the slip be reconstructed afterwards.
    """
    rows, cols = len(old) + 1, len(new) + 1
    cost = [[0] * cols for _ in range(rows)]

    for row in range(1, rows):
        cost[row][0] = cost[row - 1][0] + REMOVE_COST
    for col in range(1, cols):
        cost[0][col] = cost[0][col - 1] + INSERT_COST

    for row in range(1, rows):
        for col in range(1, cols):
            if old[row - 1] == new[col - 1]:
                # A station that stays is free, and taking it is never worse
                # than paying to replace it with itself.
                cost[row][col] = cost[row - 1][col - 1]
                continue
            cost[row][col] = min(
                cost[row - 1][col - 1] + REPLACE_COST,
                cost[row - 1][col] + REMOVE_COST,
                cost[row][col - 1] + INSERT_COST,
            )
    return cost


def amendment_cost(old: tuple[str, ...], new: tuple[str, ...]) -> int:
    """The cheapest total cost of amending `old` into `new`."""
    return _table(old, new)[len(old)][len(new)]


def amendment_slip(old: tuple[str, ...], new: tuple[str, ...]) -> list[str]:
    """The cheapest amendment, as instructions a guard can follow.

    Walks the cost table backwards from the far corner. At each step it asks
    which neighbour the cost actually came from - that is why the table is
    needed and a single running total would not do.

    Args:
        old: The published timetable.
        new: The timetable it must become.

    Returns:
        The edits in reading order, one line each. KEEP lines are included:
        a guard reading the slip needs to see the stations they are not
        touching, or they lose their place.
    """
    cost = _table(old, new)
    row, col = len(old), len(new)
    steps: list[str] = []

    while row > 0 or col > 0:
        if row > 0 and col > 0 and old[row - 1] == new[col - 1] \
                and cost[row][col] == cost[row - 1][col - 1]:
            steps.append(f"KEEP    {old[row - 1]}")
            row, col = row - 1, col - 1
        elif row > 0 and col > 0 and cost[row][col] == cost[row - 1][col - 1] + REPLACE_COST:
            steps.append(f"REPLACE {old[row - 1]} -> {new[col - 1]}")
            row, col = row - 1, col - 1
        elif row > 0 and cost[row][col] == cost[row - 1][col] + REMOVE_COST:
            steps.append(f"REMOVE  {old[row - 1]}")
            row -= 1
        else:
            steps.append(f"INSERT  {new[col - 1]}")
            col -= 1

    # Built from the far corner backwards, so the slip is reversed at the end.
    steps.reverse()
    return steps


def slip_report(pairs: list[tuple[tuple[str, ...], tuple[str, ...]]]) -> None:
    """Print the cost and the slip for each pair of timetables."""
    for old, new in pairs:
        print(f"    {' '.join(old) or '(empty)'}  ->  {' '.join(new) or '(empty)'}")
        print(f"        cost {amendment_cost(old, new)}")
        for step in amendment_slip(old, new):
            print(f"        {step}")
        print()


# ---- Self-check ----
if __name__ == "__main__":
    print("amendment slips")
    slip_report([
        (OLD_LINE, NEW_LINE),
        (("BRY", "CRB"), ("BRY", "CRB")),
        (("BRY", "CRB"), ()),
        ((), ("BRY", "CRB")),
    ])

    # The shipped pair: CRB is struck through, GRV is added. Two edits, and the
    # costs differ, so 2 + 3 = 5.
    assert amendment_cost(OLD_LINE, NEW_LINE) == 5
    slip = amendment_slip(OLD_LINE, NEW_LINE)
    assert slip.count("REMOVE  CRB") == 1
    assert slip.count("INSERT  GRV") == 1
    # Every station appears on the slip exactly once as KEEP, or is edited.
    assert len(slip) == 6

    # Identical timetables need no amendment at all.
    assert amendment_cost(OLD_LINE, OLD_LINE) == 0
    assert all(step.startswith("KEEP") for step in amendment_slip(OLD_LINE, OLD_LINE))

    # Empty on either side is the pure insert or pure remove cost.
    assert amendment_cost((), ("BRY", "CRB")) == 2 * INSERT_COST
    assert amendment_cost(("BRY", "CRB"), ()) == 2 * REMOVE_COST
    assert amendment_cost((), ()) == 0
    assert amendment_slip((), ()) == []

    # The costs being unequal is the whole point: replacing one station costs 4,
    # but removing it and inserting the other costs 2 + 3 = 5, so REPLACE wins.
    assert amendment_cost(("AAA",), ("BBB",)) == REPLACE_COST
    assert amendment_slip(("AAA",), ("BBB",)) == ["REPLACE AAA -> BBB"]

    # Make replacing dearer than the pair and the cheapest slip changes shape.
    # This is why a solution that hardcodes "one edit" is wrong.
    assert REMOVE_COST + INSERT_COST == 5 > REPLACE_COST

    # A slip always reconstructs the new timetable when a guard follows it.
    for old, new in ((OLD_LINE, NEW_LINE), (("A", "B", "C"), ("B", "C", "D")),
                     ((), ("X",)), (("X",), ())):
        rebuilt: list[str] = []
        for step in amendment_slip(old, new):
            head = step.split()[0]
            if head == "KEEP":
                rebuilt.append(step.split()[1])
            elif head == "INSERT":
                rebuilt.append(step.split()[1])
            elif head == "REPLACE":
                rebuilt.append(step.split()[-1])
            # REMOVE contributes nothing
        assert tuple(rebuilt) == new, (old, new, rebuilt)

    print("All checks passed.")
```

The backward walk asks each step which neighbour the cost actually came from,
which is why the table has to survive past the cost calculation. A version that
keeps only the running minimum is shorter, correct for the number, and cannot
produce the slip at all — that trade is worth a paragraph in Examine (cost).

## Run it

Download the solution beside this page and run it:

```bash
python challenge-01-timetable-amendment.py
```

No third-party packages, no arguments, no input. It prints four slips and then
`All checks passed.`

## Common bugs to catch

- **Counting edits instead of costing them.** Symptom: the answer is right
  whenever the costs happen to be equal and wrong otherwise. The shipped costs
  are unequal on purpose.
- **Keeping a running total instead of the table.** Symptom: the cost is right
  and the slip is impossible to produce.
- **Walking the table forwards.** Symptom: a slip in reverse order, or one that
  reconstructs the old timetable. Build backwards, then reverse.
- **Omitting `KEEP` lines.** Symptom: a technically minimal slip that a guard
  cannot follow, because nothing says where the edits go.
- **Comparing floats or using `<=` where the tie matters.** Symptom: the slip
  changes when the costs are edited even though the total does not.
- **Special-casing the empty timetable.** Symptom: an exception on `()`, where
  the answer is 0 and an empty slip.

## Acceptance checklist

- [ ] The shipped pair costs 5, with one `REMOVE` and one `INSERT`.
- [ ] Identical timetables cost 0 and produce only `KEEP` lines.
- [ ] `() → (BRY, CRB)` costs `2 × INSERT`, and the mirror costs `2 × REMOVE`.
- [ ] Following any slip reconstructs the new timetable exactly.
- [ ] Raising `REPLACE_COST` above `REMOVE + INSERT` changes the slip.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Add a `SWAP` edit — two adjacent stations exchanged, cost 3 — and say what it
  does to the recurrence. It is one more case and it is not free.
- Return **every** cheapest slip rather than one, and say how many there are for
  the shipped pair. Ties are more common than people expect.
- Make the cost of inserting depend on the station — some stops are dearer to
  advertise — and check the table still works. It should; saying why is the
  point.
