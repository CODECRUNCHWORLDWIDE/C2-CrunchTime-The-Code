# Exercise 4 — The On-Call Grid

> **Topic:** one hash set per constraint axis — running three membership questions at once without letting them contaminate each other
> **Lecture:** [02 — The Hash Map Pattern](../lecture-notes/02-the-hash-map-pattern.md)
> **Difficulty:** Medium
> **Target time:** 60 minutes
> **Why this one:** the first problem where you hold several structures in your head at the same time, and the first whose honest headline complexity is `O(1)`. Being able to say "this is O(1) because the grid is a fixed size, and O(R × C) for a general grid" without being prompted is a real interview discriminator, and most candidates give only one of the two.

## The Brief

Think of a sudoku. A number is illegal if it repeats in its row, or in its
column, or in its little box. Three rules, three places to look, and the number
itself is fine — it is the *repetition inside a region* that is the problem.

A hospital rota is the same shape, with doctors instead of digits.

The rota is a grid: **8 rows** (the wards) by **14 columns** (the nights of a
fortnight). Each cell holds a doctor's initials, or `None` if that ward is
unstaffed that night.

Three rules govern it. A cell **conflicts** if putting that doctor there breaks
any of them:

1. **`"ward"`** — no doctor covers the same ward twice in one fortnight. That is
   two matching entries in one row.
2. **`"night"`** — no doctor covers two wards on the same night. That is two
   matching entries in one column.
3. **`"unit"`** — the wards are paired into four clinical units (rows 0–1, 2–3,
   4–5, 6–7) and the fortnight into two weeks (columns 0–6, 7–13). Each unit
   runs a single weekly handover, so a doctor may take at most one shift per
   unit per week. That is the 2 × 7 block at `(row // 2, col // 7)` — the
   sudoku box, rectangular.

Scan the grid in **row-major order** — row 0 left to right, then row 1, and so
on — and return the **first cell that conflicts**, as `(row, col, axis)`. If a
cell breaks more than one rule at once, report the axis by this precedence:
`"ward"`, then `"night"`, then `"unit"`.

Return `None` if the whole rota is legal. Unstaffed cells never conflict with
anything, including each other.

The tool is three sets, or rather three *families* of sets: one per row, one per
column, one per unit block. Each set answers the same question Exercise 2's set
answered — *have I seen this before* — but each one is asking about a different
region, and keeping them from bleeding into each other is the whole skill on
this page.

## Starter

Create `exercise-04-on-call-grid.py` in your practice repo and paste this in.
Fill in the `TODO`.

```python
"""exercise-04-on-call-grid.py — the first conflict in an on-call rota.

Fill in the TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the function is correct.
"""

from collections import defaultdict

WARDS = 8
NIGHTS = 14


def first_rota_conflict(rota: list[list[str | None]]) -> tuple[int, int, str] | None:
    """Return the first rule-breaking cell in row-major order.

    Args:
        rota: An 8 x 14 grid. Each cell holds a doctor's initials, or None
            when that ward is unstaffed that night.

    Returns:
        (row, col, axis) for the first conflicting cell, where axis is
        'ward', 'night' or 'unit' and ward outranks night outranks unit.
        None when the whole rota is legal.
    """
    # TODO: allocate one set per row, one per column, one per 2x7 unit block,
    # ABOVE both loops. Then walk row-major, skip None, test the three sets in
    # precedence order, and record a surviving doctor in all three.
    ...


def blank() -> list[list[str | None]]:
    """Return an empty 8 x 14 rota: every ward unstaffed every night."""
    return [[None] * NIGHTS for _ in range(WARDS)]


# ---- Self-check ----
if __name__ == "__main__":
    def build(cells: list[tuple[int, int, str]]) -> list[list[str | None]]:
        """Return a blank rota with the listed cells filled in."""
        rota = blank()
        for row, col, who in cells:
            rota[row][col] = who
        return rota

    cases: list[tuple[str, list[tuple[int, int, str]], tuple[int, int, str] | None]] = [
        ("empty rota", [], None),
        ("ward", [(0, 3, "AKB"), (0, 9, "AKB")], (0, 9, "ward")),
        ("night", [(2, 5, "MDR"), (6, 5, "MDR")], (6, 5, "night")),
        ("unit", [(4, 1, "JLO"), (5, 6, "JLO")], (5, 6, "unit")),
        ("precedence", [(2, 4, "PVS"), (3, 4, "PVS")], (3, 4, "night")),
        (
            "row-major",
            [(1, 0, "AKB"), (1, 1, "AKB"), (0, 2, "MDR"), (0, 3, "MDR")],
            (0, 3, "ward"),
        ),
        ("legal repeat", [(0, 0, "AKB"), (1, 7, "AKB")], None),
    ]

    for label, cells, expected in cases:
        found = first_rota_conflict(build(cells))
        assert found == expected, (label, found, expected)
        print(f"{label:<13} ->  {found}")

    print("All checks passed.")
```

Three things before you start.

**Integer division picks the block.** `row // 2` says which pair of wards a row
belongs to; `col // 7` says which week a column belongs to. Two different
divisors, because the block is 2 tall and 7 wide. Together, `(row // 2, col //
7)` names one of the eight blocks, and it is a tuple, so it can be a dict key.

**Row-major.** Finish a row before starting the next one. `for row in ...: for
col in ...` is row-major; swapping the loops is not, and this page has a case
that tells the difference.

**`defaultdict(set)`.** A dict that invents an empty set the first time you
touch a missing key, so `unit_seen[(0, 1)].add("AKB")` works without a "does
this block exist yet" branch.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-02-complexity-and-hash-maps/exercises/exercise-04-on-call-grid.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `first_rota_conflict` returns `(row, col, axis)` for the first conflicting
   cell in **row-major** order, or `None` if the rota is legal.
2. The cell reported is the **second** occurrence — the one that breaks the
   rule, not the one that was already there.
3. When a cell breaks several rules, the axis reported is the highest-priority
   one: `"ward"`, then `"night"`, then `"unit"`.
4. `None` cells are skipped entirely and never conflict, including with each
   other.
5. A doctor may legally appear many times in the rota. Only repetition *inside a
   region* is a conflict.
6. The three structures are allocated once, above both loops.
7. A doctor who passes all three checks is recorded in **all three** structures.
8. The function keeps its type hints and its docstring.

## Constraints

- **The grid is always exactly 8 × 14 — 112 cells.** The size is fixed by the
  hospital's rota, not supplied by the caller, and that is deliberate: it means
  the honest headline complexity is **`O(1)`**. A function whose work is bounded
  by a constant that no input can change is constant time, however many nested
  loops it contains. Give the general framing in the same breath — for an
  `R × C` grid the identical code is `O(R · C)`, linear in the number of cells —
  because that is the number that would matter if the hospital added a ward. A
  candidate who says "it is `O(n^2)` because there are two loops" has read the
  code and not the constraint.

- **Row count is divisible by 2 and column count by 7.** So every cell belongs
  to exactly one whole 2 × 7 unit block and there is never a ragged block at the
  edge. This bound exists so the block arithmetic is one integer division per
  axis with no remainder handling — the exercise is about keeping three
  structures straight, not about tiling a grid.

- **At most 40 doctors appear anywhere in the rota, and initials are 2 to 4
  uppercase ASCII letters.** Every set you build therefore holds at most 40
  entries, which is why the space answer is also `O(1)` rather than `O(n)`.
  Short initials also keep hashing a key genuinely constant, so there is nothing
  hiding inside the `O(1)` per lookup.

- **Any number of cells may be `None`, including all of them.** An unstaffed
  ward is normal, and `None` is an absence rather than a doctor. This bound
  exists because treating `None` as a value is the single most common failure on
  this page: two unstaffed cells in row 0 would "collide" and a blank rota would
  report a conflict.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-04-on-call-grid-solution.py
empty rota    ->  None
ward          ->  (0, 9, 'ward')
night         ->  (6, 5, 'night')
unit          ->  (5, 6, 'unit')
precedence    ->  (3, 4, 'night')
row-major     ->  (0, 3, 'ward')
legal repeat  ->  None
All checks passed.
```

Two rows deserve a second look.

**`precedence`** puts `PVS` at `(2, 4)` and `(3, 4)`. That cell breaks two rules
at once: it repeats in column 4, and rows 2 and 3 share unit block `(1, 0)`.
Both statements are true, and the spec says `"night"` outranks `"unit"`. If you
test the unit set first you report `"unit"` — with arithmetic that is entirely
correct.

**`row-major`** has two ward conflicts. Row 1's sits at column 1 and row 0's at
column 3, so the *lower column number* is not the answer: row-major order
finishes row 0 before it starts row 1. Any column-major scan returns
`(1, 1, 'ward')` and is wrong.

## Steps

1. Create the file, paste the starter, and run it. Every case fails, starting
   with the blank rota.
2. Write the three allocations first, above both loops, and print their lengths.
   Eight row sets, fourteen column sets, and a `defaultdict(set)` that is empty
   until touched.
3. Write the loop with only the `None` skip and a `print` of each staffed cell.
   Run it against the `row-major` case and read the order the cells come out in.
   That order *is* the answer to two of the seven cases.
4. Add the three checks, in precedence order, returning immediately.
5. Add the three inserts, after the checks. Run. All seven should pass.
6. Break it on purpose twice. First, move the unit check above the night check
   and watch `precedence` fail. Then move the three allocations inside the `col`
   loop and watch every case return `None`. Put both back. Those are the two
   bugs this page exists to inoculate you against.
7. Say both cost framings out loud, in one breath: *"the grid is fixed at 112
   cells so this is O(1) time and O(1) space; for a general R by C grid it is
   O(R times C), which is linear in the number of cells."*

## The Solution

```python
"""exercise-04-on-call-grid-solution.py — the first conflict in an on-call rota.

Three rules, three axes, three sets per axis. One row-major pass over the
8 x 14 grid. For every staffed cell we ask the three questions in precedence
order — ward, then night, then unit — and the first yes is the answer.

Time: O(1) — the grid is fixed at 112 cells. For a general R x C grid the same
code is O(R * C), linear in the number of cells.
Space: O(1) — 8 + 14 + 8 sets, each holding at most 40 sets of initials.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from collections import defaultdict

WARDS = 8
NIGHTS = 14


def first_rota_conflict(rota: list[list[str | None]]) -> tuple[int, int, str] | None:
    """Return the first rule-breaking cell in row-major order.

    Args:
        rota: An 8 x 14 grid. Each cell holds a doctor's initials, or None
            when that ward is unstaffed that night.

    Returns:
        (row, col, axis) for the first conflicting cell, where axis is
        'ward', 'night' or 'unit' and ward outranks night outranks unit.
        None when the whole rota is legal.
    """
    ward_seen: list[set[str]] = [set() for _ in range(len(rota))]
    night_seen: list[set[str]] = [set() for _ in range(len(rota[0]) if rota else 0)]
    unit_seen: defaultdict[tuple[int, int], set[str]] = defaultdict(set)

    for row, nights in enumerate(rota):
        for col, who in enumerate(nights):
            if who is None:
                continue
            unit = (row // 2, col // 7)
            if who in ward_seen[row]:
                return (row, col, "ward")
            if who in night_seen[col]:
                return (row, col, "night")
            if who in unit_seen[unit]:
                return (row, col, "unit")
            ward_seen[row].add(who)
            night_seen[col].add(who)
            unit_seen[unit].add(who)
    return None


def blank() -> list[list[str | None]]:
    """Return an empty 8 x 14 rota: every ward unstaffed every night."""
    return [[None] * NIGHTS for _ in range(WARDS)]


# ---- Self-check ----
if __name__ == "__main__":
    def build(cells: list[tuple[int, int, str]]) -> list[list[str | None]]:
        """Return a blank rota with the listed cells filled in."""
        rota = blank()
        for row, col, who in cells:
            rota[row][col] = who
        return rota

    cases: list[tuple[str, list[tuple[int, int, str]], tuple[int, int, str] | None]] = [
        ("empty rota", [], None),
        ("ward", [(0, 3, "AKB"), (0, 9, "AKB")], (0, 9, "ward")),
        ("night", [(2, 5, "MDR"), (6, 5, "MDR")], (6, 5, "night")),
        ("unit", [(4, 1, "JLO"), (5, 6, "JLO")], (5, 6, "unit")),
        ("precedence", [(2, 4, "PVS"), (3, 4, "PVS")], (3, 4, "night")),
        (
            "row-major",
            [(1, 0, "AKB"), (1, 1, "AKB"), (0, 2, "MDR"), (0, 3, "MDR")],
            (0, 3, "ward"),
        ),
        ("legal repeat", [(0, 0, "AKB"), (1, 7, "AKB")], None),
    ]

    for label, cells, expected in cases:
        found = first_rota_conflict(build(cells))
        assert found == expected, (label, found, expected)
        print(f"{label:<13} ->  {found}")

    print("All checks passed.")
```

**Three rules, three namespaces, and keeping them apart is the whole job.**

```python
ward_seen[row]                # one set per row
night_seen[col]               # one set per column
unit_seen[(row // 2, col // 7)]   # one set per 2x7 block
```

The temptation is one big set of initials. It does not work, and it fails in a
way worth understanding: with a single set, a doctor's first perfectly legal
appearance puts their initials in, and their *next* legal appearance — different
ward, different night, different unit — finds them there and reports a conflict.
Worse, you could not say which rule broke, because the set does not remember
which region it was recording. Three questions need three records.

**`(row // 2, col // 7)` is one integer division per axis, with different
divisors.** Blocks are 2 rows tall and 7 columns wide, so the two divisors are 2
and 7. Writing `(row // 2, col // 2)` gives you 2 × 2 blocks — a plausible-
looking key for a completely different grid. The tuple is the key, and a tuple
of two integers is hashable, so a `defaultdict(set)` indexed by it needs no
setup.

**The checks are `if`s in precedence order, not `elif`s over a computed set.**
The first check that fires returns, so the order the checks are written in *is*
the precedence rule. That is why the `precedence` case answers `"night"`: the
ward check does not fire, the night check does, and the unit check is never
reached even though it would also have fired. Encoding a spec rule as statement
order is cheap and completely invisible — which is exactly why it deserves a
comment or a test, and this page has the test.

**All three inserts, or none.** A cell that survives all three checks has to be
recorded in all three sets. Miss one and you get silent false negatives: a later
conflict on the axis you forgot to record simply never fires. Nothing raises, no
test with three cells in it notices, and the function confidently returns `None`
for an illegal rota. Bugs that fail *quietly* are worse than bugs that crash,
and this is the one on this page.

**`if who is None: continue`, before anything else.** `None` is an absence, not
a doctor. Skip it at the top of the body and the rest of the loop never has to
think about it. If you skip this, the second unstaffed cell of row 0 finds
`None` already in `ward_seen[0]` and a completely blank rota reports
`(0, 1, 'ward')`.

**The cell reported is always the later one.** The conflict is the cell that
*breaks* the rule. The first occurrence was legal when it happened — you cannot
know it was a problem until the second one arrives. This falls out of the loop
shape again: you return at the cell you are standing on, and you are standing on
the second one.

**The cost, said properly, in both framings.** *Time `O(1)`*: the grid is 112
cells, each staffed cell does at most three constant-time set lookups and three
inserts, and 112 does not depend on any input. *Generally `O(R · C)`*: the same
code on an `R × C` grid touches every cell once, which is linear in the number
of cells — say "linear in the number of cells", never "`O(n^2)`", because there
is no `n` here that anything is squared in. *Space `O(1)`*: 8 + 14 + 8 sets,
each holding at most 40 sets of initials; generally `O(R + C + blocks)` sets
holding `O(R · C)` entries in the worst case. *Best case*: a conflict at
`(0, 1)` exits after two cells. *Worst case*: a legal rota, which reads all 112.
*Tradeoff*: one set of tagged tuples replaces the three structures at identical
complexity — see the stretch — and it is a readability call, not a performance
one. *Improvement*: none. A legal rota cannot be certified without inspecting
every staffed cell.

## Download and run

Download
[exercise-04-on-call-grid-solution.py](./exercise-04-on-call-grid-solution.py)
and run it:

```bash
python exercise-04-on-call-grid-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-04-on-call-grid.py`.

## Common bugs to catch

- **A blank rota reports a conflict.** You did not skip `None`:

  ```text
  Traceback (most recent call last):
      assert found == expected, (label, found, expected)
             ^^^^^^^^^^^^^^^^^
  AssertionError: ('empty rota', (0, 1, 'ward'), None)
  ```

  The first cell put `None` into `ward_seen[0]`, and the second cell found it
  there. `None` is hashable, so nothing complains — it just quietly becomes the
  world's most popular doctor. Skip it before you touch any set.

- **Every case returns `None`.** You allocated the sets inside a loop:

  ```text
  Traceback (most recent call last):
      assert found == expected, (label, found, expected)
             ^^^^^^^^^^^^^^^^^
  AssertionError: ('ward', None, (0, 9, 'ward'))
  ```

  `ward_seen = [set() for _ in ...]` written inside the `col` loop is fresh and
  empty on every single cell, so nothing is ever remembered. Hoist all three
  allocations above both loops.

- **`precedence` answers `'unit'` instead of `'night'`.** Your checks are in the
  wrong order. The arithmetic is right and the answer is wrong, which is the
  most frustrating kind of failure and the reason a precedence rule belongs in
  your restatement of the problem rather than in your debugging.

- **`row-major` answers `(1, 1, 'ward')`.** You looped columns on the outside.
  Row-major means the row loop is outermost. Trace which cell you visit fourth.

- **`TypeError: unsupported operand type(s) for //: 'tuple' and 'int'`.** You
  wrote `(row, col) // 7`:

  ```text
  Traceback (most recent call last):
      unit = (row, col) // 7
             ~~~~~~~~~~~^^~~
  TypeError: unsupported operand type(s) for //: 'tuple' and 'int'
  ```

  Divide each coordinate, then make the tuple:
  `unit = (row // 2, col // 7)`.

- **`legal repeat` reports a conflict.** You collapsed the three axes into one
  set of bare initials. The same doctor twice in a fortnight is completely
  ordinary; it is only repetition inside one region that is illegal.

- **Silent false negatives from a missing insert.** Adding a survivor to two of
  the three sets raises nothing and fails no small test. If you are not sure you
  did all three, add a temporary assertion that the three set sizes always move
  together, then delete it.

- **Reporting the first occurrence instead of the second.** The `ward` case
  answers `(0, 9, 'ward')`, not `(0, 3, 'ward')`. The conflict is the cell that
  broke the rule.

## Under the hood

<details>
<summary>Under the hood — collapsing three sets into one with a tagged key, and why O(1) is a real answer</summary>

**The one-set version.** Three structures can become one by *tagging* each fact
with the axis it belongs to. A tuple key gives you the namespace for free, with
no string formatting:

```python
def first_rota_conflict(rota: list[list[str | None]]) -> tuple[int, int, str] | None:
    seen: set[tuple[str, object, str]] = set()
    for row, nights in enumerate(rota):
        for col, who in enumerate(nights):
            if who is None:
                continue
            keys = (
                ("ward", row, who),
                ("night", col, who),
                ("unit", (row // 2, col // 7), who),
            )
            for key in keys:
                if key in seen:
                    return (row, col, key[0])
            seen.update(keys)
    return None
```

The `keys` tuple is built in precedence order, so the loop that tests it returns
the highest-priority axis automatically — the ordering requirement disappears
into the data instead of living in a chain of `if`s. That is the argument for it.

The argument against is that one set now holds three different kinds of fact,
and a reader has to decode the tag to know what any entry means. The complexity
is identical: same number of lookups, same constant space. This is a taste
call, and the useful interview move is not picking the "right" one — it is
saying *"I considered the other and here is the tradeoff"*, which is what is
actually being graded.

**Why `O(1)` is not a trick answer.** Big-O describes how work grows as the
input grows. Here the input cannot grow: the rota is 8 × 14 by definition of the
problem, so the work is bounded by a constant, so the function is constant time.
The number of nested loops is irrelevant — a loop that runs at most 112 times is
`O(1)` just as much as a single statement is.

This trips people up because "constant" feels like it should mean "fast". It
does not. A function that does ten billion operations on every call, always,
is also `O(1)`. Big-O is about *growth*, and a thing that does not grow has
growth zero. The right thing to say out loud is both sentences: the honest
headline, and the general shape that would apply if the constraint were lifted.
Interviewers ask this exact question — "what if the hospital adds wards?" — and
having already said `O(R · C)` means you have answered it before it was asked.

**Why not `O(n^2)`?** Because there is no `n`. A grid has two dimensions, and
calling a full scan of it "quadratic" is only true when `R = C`, which here it
is not. `O(R · C)` is the accurate statement, and it is also the more useful
one: it tells you the cost is linear in the *number of cells*, which is the
thing you actually pay for. Say "linear in the number of cells" and you will
never have to think about whether the grid is square.

**Where the space really goes.** Eight row sets, fourteen column sets and eight
block sets is thirty sets, and every staffed cell puts one entry into three of
them. On a full 112-cell rota that is 336 entries, capped by the 40-doctor
constraint at 40 per set. In general the entry count is `O(R · C)` and the set
count is `O(R + C + blocks)` — so a general grid's space is linear in the number
of cells too, and here both collapse to a constant.

</details>

## Acceptance checklist

- [ ] `python exercise-04-on-call-grid.py` prints seven rows then `All checks passed.`
- [ ] The rows match the expected output character for character.
- [ ] The three structures are allocated **above** both loops.
- [ ] `None` is skipped before any set is touched.
- [ ] The three checks appear in precedence order, and each returns immediately.
- [ ] A surviving doctor is added to all three structures.
- [ ] The unit key uses two *different* divisors.
- [ ] You gave **both** complexity framings — the fixed-grid `O(1)` and the
      general `O(R · C)`.
- [ ] You can name the one-set alternative and say why you did or did not use it.
- [ ] Committed to Git with a message like `Add Week 2 exercise 4: on-call grid`.

## Stretch

- **Report every conflict rather than the first.** The rota office would rather
  fix a fortnight in one pass than run the checker eight times.

  ```python
  from collections import defaultdict

  def all_rota_conflicts(rota: list[list[str | None]]) -> list[tuple[int, int, str]]:
      """Return every conflicting cell in row-major order, one entry per cell."""
      seen: set[tuple[str, object, str]] = set()
      conflicts: list[tuple[int, int, str]] = []
      for row, nights in enumerate(rota):
          for col, who in enumerate(nights):
              if who is None:
                  continue
              keys = (
                  ("ward", row, who),
                  ("night", col, who),
                  ("unit", (row // 2, col // 7), who),
              )
              hit = next((key[0] for key in keys if key in seen), None)
              if hit is not None:
                  conflicts.append((row, col, hit))
              seen.update(keys)
      return conflicts

  rota = [[None] * 14 for _ in range(8)]
  rota[0][3] = rota[0][9] = "AKB"
  rota[2][4] = rota[3][4] = "PVS"
  print(all_rota_conflicts(rota))
  ```

  ```text
  [(0, 9, 'ward'), (3, 4, 'night')]
  ```

  Note what had to change: the early return became an append, and the offending
  cell is still recorded in the sets so that a third occurrence is reported too.
  Deciding whether a rejected cell should still count as "seen" is a real
  product question, and you should say which you chose and why.

- **Count each doctor's shifts and find who is overloaded.**

  ```python
  from collections import Counter

  def shift_counts(rota: list[list[str | None]]) -> list[tuple[str, int]]:
      """Return (initials, shifts) sorted by most shifts, ties alphabetical."""
      tally = Counter(who for nights in rota for who in nights if who is not None)
      return sorted(tally.items(), key=lambda pair: (-pair[1], pair[0]))

  rota = [[None] * 14 for _ in range(8)]
  rota[0][0] = rota[1][1] = rota[2][2] = "AKB"
  rota[3][3] = "MDR"
  print(shift_counts(rota))
  ```

  ```text
  [('AKB', 3), ('MDR', 1)]
  ```

  A different hash structure for a different question, over the same grid. Note
  the generator expression flattening two loops into one line, and the tuple sort
  key with the negated count — the same trick as Week 1, in a new place.

- **Make the block shape a parameter and prove the code did not care.**

  ```python
  def first_conflict_general(
      rota: list[list[str | None]], block_rows: int, block_cols: int
  ) -> tuple[int, int, str] | None:
      """The same checker for any grid and any block shape that tiles it."""
      seen: set[tuple[str, object, str]] = set()
      for row, cells in enumerate(rota):
          for col, who in enumerate(cells):
              if who is None:
                  continue
              keys = (
                  ("ward", row, who),
                  ("night", col, who),
                  ("unit", (row // block_rows, col // block_cols), who),
              )
              for key in keys:
                  if key in seen:
                      return (row, col, key[0])
              seen.update(keys)
      return None

  square = [[None] * 4 for _ in range(4)]
  square[0][0] = square[1][1] = "AKB"
  print(first_conflict_general(square, 2, 2))
  print(first_conflict_general(square, 4, 4))
  ```

  ```text
  (1, 1, 'unit')
  (1, 1, 'unit')
  ```

  Now the grid *can* grow, and `O(R · C)` is the only honest answer — which is
  the point. Try `block_rows=1` and watch the unit rule collapse into the ward
  rule, since every row becomes its own block.
Next: [Exercise 5 — The Longest Dock Run](./exercise-05-longest-dock-run.md).
