# Challenge 1 — The Cold Store Aisle Sweep

> Topic: hanging a whole word list on one tree and walking the grid once · Lecture: [2](../lecture-notes/02-word-break-and-aho-corasick.md) · Difficulty: Hard · Target time: 70 minutes including the FRAME write-up · Why this one: it is the composition the week exists for — a grid walk and a prefix tree, where the tree's job is to stop the walk early. The saving is printed rather than claimed.

## The Brief

A cold store is a grid of bins, each stamped with one letter. A picker starts at
**any** bin and steps up, down, left or right, never entering the same bin twice
on one walk. The letters they pass spell a route code.

Given the pick list, report **how many different starting bins** each code can be
walked from. Codes that cannot be walked at all are left out of the report.

The obvious approach is one grid search per code. The approach worth writing up
hangs the **whole pick list on one prefix tree** and walks the grid once — because
the moment the letters under the picker's feet stop matching any code's opening
run, the walk can stop, and it stops for every code at once.

## Starter

`challenge-01-cold-store-aisle-sweep-solution.py` sits beside this page with the
store and the self-checks.

```text
S A L T          pick list
T L A S            SALT  SALTS  MAST  TAIL  LIT  TIL
A I M E            PEST  TALL   SEA   SLAT  MEAL
L T S P
```

Four of those eleven codes cannot be walked at all. Work out which before you
write anything — it takes two minutes with a finger on the grid, and it is the
answer you will be checking against.

The file reports the step counts for both approaches, so the saving is a number
on the page rather than an assertion in a paragraph.

## Requirements

1. `build_pick_tree(codes)` returns a prefix tree over the whole pick list.
2. `sweep(bins, codes)` returns the count of starting bins per walkable code,
   **and** the number of steps taken.
3. `naive_sweep(bins, codes)` does the same job one code at a time, also
   returning its step count.
4. Codes that cannot be walked are absent from the report, not present with zero.
5. Both sweeps agree exactly on the counts.

## Constraints

- **One walk, not one per code.** That is the challenge. Doing it per code is
  correct and is the alternative to name and reject in the write-up.
- **No bin twice on one walk**, and the mark has to be undone when the walk backs
  out. A visited set that is never unmarked turns this into a much smaller and
  wrong problem.
- **Prune on the tree.** When the current node has no child for the next letter,
  stop. That single check is the entire reason the one-tree version is faster.
- **Count starting bins, not walks.** A code reachable from one bin by two
  different routes counts once.
- **The two sweeps must agree.** `naive_sweep` is in the file to be disagreed
  with, and a challenge where the fast version is only checked against itself
  proves nothing.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python challenge-01-cold-store-aisle-sweep.py
S A L T
T L A S
A I M E
L T S P

SALT   2 starting bins
SALTS  2 starting bins
LIT    1 starting bin
MAST   1 starting bin
PEST   1 starting bin
TAIL   1 starting bin
TIL    1 starting bin

not walkable  MEAL, SEA, SLAT, TALL
one-tree steps     39
code-by-code       62

All checks passed.
```

Two numbers at the end: **39 steps** for the one-tree sweep against **62** for
the code-by-code version, on a four-by-four store and eleven codes. The ratio
grows with the pick list — the one-tree walk barely notices a longer list,
because the extra codes mostly share their opening letters with codes already
there.

`SALT` and `SALTS` both start from two bins, which is worth checking by hand: the
grid has two `S` bins from which the walk works.

## Steps

1. Read the self-checks. They are the spec.
2. Find the four unwalkable codes by hand, on paper.
3. Write the memo: one tree over the pick list, one walk per starting bin, prune
   where the tree runs out.
4. Build the tree. Store the whole code at its end node so a hit does not have to
   rebuild the string from the path.
5. Write the walk. Mark on entry, unmark on exit, and get that pair right before
   anything else.
6. Add the pruning check and the step counter together.
7. Write `naive_sweep` and assert the two agree.
8. Write the FRAME pass, with the two step counts in the cost section.

## The Solution

```python
"""challenge-01-cold-store-aisle-sweep-solution.py — one walk, every code.

A cold store is a grid of bins, each stamped with one letter. A picker starts
at any bin and steps up, down, left or right, never entering the same bin
twice on one walk. The letters they pass spell a route code.

Given the pick list, report how many different starting bins each code can be
walked from. Codes that cannot be walked at all are left out of the report.

The trick is to hang the whole pick list on one prefix tree and walk the grid
once, instead of walking the grid once per code. The file prints both step
counts so the saving is visible rather than claimed.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

END = "*"

CodeTree = dict

BINS: list[str] = [
    "SALT",
    "TLAS",
    "AIME",
    "LTSP",
]

PICK_LIST: list[str] = [
    "SALT",
    "SALTS",
    "MAST",
    "TAIL",
    "LIT",
    "TIL",
    "PEST",
    "TALL",
    "SEA",
    "SLAT",
    "MEAL",
]


def build_pick_tree(codes: list[str]) -> CodeTree:
    """Return a prefix tree of the pick list, with each code at its own leaf.

    Args:
        codes: The route codes to look for. Each must be at least two letters.

    Returns:
        The root node. A node that ends a code carries END, and END holds the
        code itself, so a walk that reaches it already knows what it spelled.

    Raises:
        ValueError: If any code is shorter than two letters.
    """
    root: CodeTree = {}
    for code in codes:
        if len(code) < 2:
            raise ValueError(f"route code {code!r} is too short to be a walk")
        node = root
        for letter in code:
            node = node.setdefault(letter, {})
        node[END] = code
    return root


def sweep(bins: list[str], codes: list[str]) -> tuple[dict[str, int], int]:
    """Return the starting-bin count for every walkable code, plus the work done.

    Args:
        bins: The store, one string per row. Every row is the same length.
        codes: The pick list.

    Returns:
        A pair. First, a dict from code to the number of distinct bins a walk
        spelling it can start from; codes that cannot be walked are absent.
        Second, how many bin-entry steps the sweep took.
    """
    root = build_pick_tree(codes)
    rows = len(bins)
    columns = len(bins[0]) if rows else 0
    starts: dict[str, set[tuple[int, int]]] = {}
    steps = 0

    def walk(row: int, column: int, node: CodeTree, origin: tuple[int, int]) -> None:
        nonlocal steps
        letter = bins[row][column]
        child = node.get(letter)
        if child is None:
            return
        steps += 1
        standing = bins[row]
        bins[row] = standing[:column] + " " + standing[column + 1 :]
        if END in child:
            starts.setdefault(child[END], set()).add(origin)
        for next_row, next_column in (
            (row - 1, column),
            (row + 1, column),
            (row, column - 1),
            (row, column + 1),
        ):
            if 0 <= next_row < rows and 0 <= next_column < columns:
                walk(next_row, next_column, child, origin)
        bins[row] = standing

    for row in range(rows):
        for column in range(columns):
            walk(row, column, root, (row, column))

    return {code: len(cells) for code, cells in starts.items()}, steps


def naive_sweep(bins: list[str], codes: list[str]) -> tuple[dict[str, int], int]:
    """Return the same report, walking the grid once per code.

    Args:
        bins: The store, one string per row.
        codes: The pick list.

    Returns:
        A pair: the same dict `sweep` returns, and the bin-entry step count.
    """
    rows = len(bins)
    columns = len(bins[0]) if rows else 0
    report: dict[str, int] = {}
    steps = 0

    def walk(row: int, column: int, code: str, position: int) -> bool:
        nonlocal steps
        if bins[row][column] != code[position]:
            return False
        steps += 1
        if position == len(code) - 1:
            return True
        standing = bins[row]
        bins[row] = standing[:column] + " " + standing[column + 1 :]
        for next_row, next_column in (
            (row - 1, column),
            (row + 1, column),
            (row, column - 1),
            (row, column + 1),
        ):
            if 0 <= next_row < rows and 0 <= next_column < columns:
                if walk(next_row, next_column, code, position + 1):
                    bins[row] = standing
                    return True
        bins[row] = standing
        return False

    for code in codes:
        if len(code) < 2:
            raise ValueError(f"route code {code!r} is too short to be a walk")
        found = 0
        for row in range(rows):
            for column in range(columns):
                if walk(row, column, code, 0):
                    found += 1
        if found:
            report[code] = found

    return report, steps


# ---- Self-check ----
if __name__ == "__main__":
    for row in BINS:
        print(" ".join(row))
    print()

    report, tree_steps = sweep(BINS, PICK_LIST)
    for code, count in sorted(report.items(), key=lambda pair: (-pair[1], pair[0])):
        bin_word = "bin" if count == 1 else "bins"
        print(f"{code:<6} {count} starting {bin_word}")

    missing = sorted(code for code in PICK_LIST if code not in report)
    print()
    print(f"not walkable  {', '.join(missing)}")

    plain_report, plain_steps = naive_sweep(BINS, PICK_LIST)
    print(f"one-tree steps {tree_steps:>6}")
    print(f"code-by-code   {plain_steps:>6}")

    assert report == {
        "SALT": 2,
        "SALTS": 2,
        "MAST": 1,
        "TAIL": 1,
        "LIT": 1,
        "TIL": 1,
        "PEST": 1,
    }
    assert plain_report == report
    assert tree_steps < plain_steps
    assert BINS == ["SALT", "TLAS", "AIME", "LTSP"]  # the store was put back

    try:
        sweep(BINS, ["S"])
    except ValueError as problem:
        assert str(problem) == "route code 'S' is too short to be a walk"
    else:
        raise AssertionError("a one-letter code should have been rejected")

    print()
    print("All checks passed.")
```

Storing the finished code at its end node rather than reconstructing it from the
path is a small thing that matters at scale: the path is rebuilt at every hit,
and hits are the common case in a store full of matching letters.

## Run it

Download the solution beside this page and run it:

```bash
python challenge-01-cold-store-aisle-sweep.py
```

No third-party packages, no arguments, no input. It prints the store, the counts
per code, the unwalkable codes, both step counts, and then `All checks passed.`

## Common bugs to catch

- **Never unmarking a bin.** Symptom: far fewer codes found than exist, and no
  error. The walk has to undo its mark on the way back out.
- **One search per code.** Symptom: correct answers and no challenge — the step
  count gives it away.
- **No pruning.** Symptom: the one-tree version is *slower* than the naive one,
  because it walks the whole grid from every bin without ever stopping early.
- **Counting walks instead of starting bins.** Symptom: counts higher than the
  number of bins in the store.
- **Reporting unwalkable codes with a count of zero.** Symptom: eleven rows where
  seven are meant.
- **Rebuilding the code from the path at every hit.** Symptom: correct, and
  quadratic in the code length for no reason.
- **Marking the starting bin after the first step.** Symptom: a walk that revisits
  its own start, which finds codes the store cannot spell.

## Acceptance checklist

- [ ] `SALT` and `SALTS` each come from two starting bins.
- [ ] `LIT`, `MAST`, `PEST`, `TAIL` and `TIL` each come from one.
- [ ] `MEAL`, `SEA`, `SLAT` and `TALL` are reported as not walkable.
- [ ] Both sweeps agree exactly on every count.
- [ ] The one-tree sweep takes 39 steps against the naive 62.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Report, for each walkable code, *which* bins it starts from rather than how
  many. It is the version a picker could act on.
- Double the pick list with codes sharing the same opening letters and re-run
  both step counts. The naive count roughly doubles; the one-tree count barely
  moves, and that gap is the write-up's strongest sentence.
- Prune the tree as you go: once a code has been found from every bin it can
  start at, it can be removed from the tree entirely. It is a real optimisation
  and it is fiddly to get right without breaking the shared prefixes.
