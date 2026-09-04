# Week 12 — Mini-Project: The Batch Split and the Glaze Square

> Topic: combinatorial enumeration and constraint satisfaction · Lecture: [1](../lecture-notes/01-the-backtracking-template-and-the-three-warmups.md), [2](../lecture-notes/02-pruning-and-deduplication-and-string-partitioning.md), [3](../lecture-notes/03-grid-backtracking-and-constraint-satisfaction.md) · Difficulty: Medium-Hard · Target time: one week · Why this one: two problems that look nothing alike and are the same shape underneath.

## The Brief

The week's deliverable. Two backtracking write-ups covering the two halves of
the lecture material: **combinatorial enumeration with pruning**, and
**constraint satisfaction**.

The pair is chosen because the two prune differently and *terminate* differently,
and saying which of the two you are doing — out loud, before any code — is the
week's actual lesson.

**Half one, the batch split.** A kiln fires a run of pots at rising then falling
temperatures. A *batch* is a stretch of that run whose temperatures read the same
forwards and backwards, because the kiln ramps up and back down symmetrically.
Cut the whole run into batches. Enumerate **every** legal cut, then report the one
using fewest batches.

**Half two, the glaze square.** A 4×4 rack is divided into four 2×2 quadrants.
Every row, every column and every quadrant must hold each of the four glaze codes
exactly once. Some cells are already loaded. Fill the rest — and stop at the first
filling, because a filled rack is a filled rack.

One counts. One stops. Everything else about them is the same three steps: choose,
explore, undo.

## Starter

The worked answer on this page has both halves solved and the self-checks you
must satisfy. Read the checks; then look away.

The given data:

```text
firing run:  940  1010  940  780  780  1180

glaze rack   A . . D
             . . A .
             . C . .
             B . . C
```

Work the firing run by hand first. `940 1010 940` is symmetric, `780 780` is
symmetric, `1180` is a single pot — and there is more than one way to cut it.
Finding the second cut on paper takes two minutes and saves an hour.

## Requirements

1. `all_splits(run)` returns every way to cut the run into symmetric batches;
   `fewest_batches(run)` returns the one with the fewest, ties settled by reading
   order.
2. `solve_glaze(rack)` returns a **solved copy** and leaves the input untouched,
   or returns `None` when no filling exists.
3. `solve_glaze` raises `ValueError` on a rack that is not 4×4, or that holds a
   symbol which is neither a glaze code nor `.`.
4. `render(...)` draws a rack so a human can check it by eye.
5. Both halves are narrated in full FRAME, committed under
   `frame-writeups/c2-week-12/mini-project/`.

### How to do the write-up

For each problem, produce one Markdown file under `frame-writeups/c2-week-12/mini-project/`:

1. **`problem-01-palindrome-partitioning.md`** — FRAME narration for Problem 1.
2. **`problem-02-sudoku-solver.md`** — FRAME narration for Problem 2.

Each write-up has the canonical five sections:

- **Frame:** restate the problem in your words; identify the inputs and outputs; note any tricky edge cases (e.g., a length-1 string is a valid palindrome partition of itself).
- **Research constraints:** the 30-second pattern-recognition memo at the top; name the limits and edge cases, the state design, the pruning, the recording rule.
- **Assess options:** numbered steps; pseudocode is optional but encouraged.
- **Make the solution:** the working code, with type hints everywhere.
- **Examine:** a worked trace on one example, verifying the output by hand (verify); then time and space with derivation and one variant mentioned with its trade-off (cost).

The recording is the single most useful artifact in the mini-project. A 10–15 minute video walkthrough — you reading your write-up aloud, talking through the state design, the pruning, the leaf-copy discipline — is the closest simulation of an interview that a portfolio can provide.

---

## Constraints

- **Half one enumerates; half two satisfies.** Half one records a completion and
  keeps going. Half two returns `True` up the stack and stops. Writing either one
  in the other's shape is the most common structural mistake this week.
- **Test the candidate before recursing**, in both halves. Testing inside the call
  is correct and explores a whole level of dead branches.
- **Compare the batch in place.** Slicing and reversing allocates a new tuple per
  candidate, and there are a great many candidates.
- **The empty run has exactly one split** — the empty one. That is the base case,
  not a special case, and writing it as a special case is how the count comes out
  wrong by one.
- **`solve_glaze` must not modify its argument.** A solver that mutates the
  caller's rack cannot be called twice, and the second call is where you find out.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python README.py
HALF ONE - the batch split
    run: (940, 1010, 940, 780, 780, 1180)
    splits: 4
    fewest: [(940, 1010, 940), (780, 780), (1180,)]

HALF TWO - the glaze square
    given
        A . . D
        . . A .
        . C . .
        B . . C
    solved
        A B C D
        C D A B
        D C B A
        B A D C

All checks passed.
```

The firing run has **four** legal cuts, not one. `940 1010 940 | 780 780 | 1180`
is the fewest at three batches, but cutting every pot separately is just as legal
— a single temperature is trivially symmetric. If your enumeration returns one
split, it is stopping at the first success, and you have written half two's shape
by mistake.

## Steps

1. Read both harnesses in the solution file. They are the spec.
2. Write both memos before any code. Name which half enumerates and which stops.
3. Implement `_is_symmetric` in place, then `all_splits`. Check the run gives 4.
4. Add `fewest_batches` and state the tie-break.
5. Implement `_legal` for the glaze rack as a plain scan of row, column and
   quadrant. Correct first.
6. Implement `_fill`, returning `True` up the stack. Check the solved rack by eye
   with `render` before trusting the assertions.
7. Add the guards, then write both FRAME passes.

## The Solution

```python
"""README-solution.py - the Week 12 mini-project, both halves worked.

Two backtracking problems that look nothing alike and are the same shape
underneath: choose, explore, undo.

  Half one - the batch split. A kiln fires a run of pots at rising then falling
  temperatures. A BATCH is a stretch of that run whose temperatures read the
  same forwards and backwards, because the kiln ramps up and back down
  symmetrically. Split the whole run into batches. Enumerate every split, then
  report the one with fewest batches.

  Half two - the glaze square. A 4x4 rack is divided into four 2x2 quadrants.
  Every row, every column and every quadrant must hold each of the four glaze
  codes exactly once. Some cells are already loaded. Fill the rest.

The first enumerates and counts; the second satisfies and stops. Saying which
of those two you are doing, out loud, before writing code, is the week's actual
lesson - they prune differently and they terminate differently.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that fence
reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

# ---- Given data ----
FIRING_RUN: tuple[int, ...] = (940, 1010, 940, 780, 780, 1180)

GLAZE_CODES = "ABCD"
GLAZE_RACK: list[list[str]] = [
    ["A", ".", ".", "D"],
    [".", ".", "A", "."],
    [".", "C", ".", "."],
    ["B", ".", ".", "C"],
]


# ---- Half one: the batch split ----
def _is_symmetric(run: tuple[int, ...], lo: int, hi: int) -> bool:
    """Does run[lo:hi] read the same both ways?

    Compared in place rather than by slicing and reversing. The slice would
    allocate a new tuple at every candidate, and there are a great many
    candidates.

    Args:
        run: The whole firing run.
        lo: Start of the stretch, inclusive.
        hi: End of the stretch, exclusive.

    Returns:
        True when the stretch is symmetric. A stretch of one always is.
    """
    left, right = lo, hi - 1
    while left < right:
        if run[left] != run[right]:
            return False
        left += 1
        right -= 1
    return True


def _split(
    run: tuple[int, ...],
    start: int,
    current: list[tuple[int, ...]],
    found: list[list[tuple[int, ...]]],
) -> None:
    """Enumerate every split of run[start:] into symmetric batches."""
    if start == len(run):
        found.append(list(current))
        return
    for end in range(start + 1, len(run) + 1):
        # Test BEFORE recursing. Testing inside the call explores a whole level
        # of splits whose first batch was never legal.
        if not _is_symmetric(run, start, end):
            continue
        current.append(run[start:end])
        _split(run, end, current, found)
        current.pop()


def all_splits(run: tuple[int, ...]) -> list[list[tuple[int, ...]]]:
    """Every way to cut the run into symmetric batches.

    Args:
        run: The firing temperatures, in order.

    Returns:
        A list of splits, each a list of batches. An empty run has exactly one
        split - the empty one - which is the base case, not a special case.
    """
    found: list[list[tuple[int, ...]]] = []
    _split(run, 0, [], found)
    return found


def fewest_batches(run: tuple[int, ...]) -> list[tuple[int, ...]]:
    """The split using the fewest batches; ties settled by reading order."""
    return min(all_splits(run), key=lambda split: (len(split), split))


# ---- Half two: the glaze square ----
def _quadrant(row: int, col: int) -> tuple[int, int]:
    """Which 2x2 quadrant a cell belongs to."""
    return row // 2, col // 2


def _legal(rack: list[list[str]], row: int, col: int, code: str) -> bool:
    """May `code` go in this cell?

    Args:
        rack: The rack as it currently stands, "." for empty.
        row: Cell row.
        col: Cell column.
        code: The glaze code being tried.

    Returns:
        True when the code appears nowhere in that row, column or quadrant.
    """
    for i in range(4):
        if rack[row][i] == code or rack[i][col] == code:
            return False
    qrow, qcol = _quadrant(row, col)
    for r in range(qrow * 2, qrow * 2 + 2):
        for c in range(qcol * 2, qcol * 2 + 2):
            if rack[r][c] == code:
                return False
    return True


def _fill(rack: list[list[str]], cells: list[tuple[int, int]], at: int) -> bool:
    """Fill the empty cells from `at` onwards; True when the rack is solved."""
    if at == len(cells):
        return True
    row, col = cells[at]
    for code in GLAZE_CODES:
        if not _legal(rack, row, col, code):
            continue
        rack[row][col] = code
        if _fill(rack, cells, at + 1):
            # Stop at the first solution. This half SATISFIES; it does not
            # enumerate, and returning True all the way up is what makes it
            # stop rather than exploring the rest of a solved rack.
            return True
        rack[row][col] = "."
    return False


def solve_glaze(rack: list[list[str]]) -> list[list[str]] | None:
    """Fill every empty cell, or report that the rack cannot be filled.

    Args:
        rack: A 4x4 grid of glaze codes and "." for empty. Not modified.

    Returns:
        A solved copy, or None when no filling exists.

    Raises:
        ValueError: If the rack is not 4x4, or holds a symbol that is neither a
            glaze code nor ".".
    """
    if len(rack) != 4 or any(len(row) != 4 for row in rack):
        raise ValueError("the rack must be 4x4")
    for row in rack:
        for cell in row:
            if cell != "." and cell not in GLAZE_CODES:
                raise ValueError(f"{cell!r} is not a glaze code")

    work = [list(row) for row in rack]
    empty = [(r, c) for r in range(4) for c in range(4) if work[r][c] == "."]
    return work if _fill(work, empty, 0) else None


def render(rack: list[list[str]]) -> str:
    """Draw a rack, one row per line."""
    return "\n".join(" ".join(row) for row in rack)


# ---- Self-check ----
if __name__ == "__main__":
    print("HALF ONE - the batch split")
    print(f"    run: {FIRING_RUN}")
    splits = all_splits(FIRING_RUN)
    print(f"    splits: {len(splits)}")
    print(f"    fewest: {fewest_batches(FIRING_RUN)}")
    print()

    print("HALF TWO - the glaze square")
    print("    given")
    for line in render(GLAZE_RACK).splitlines():
        print("        " + line)
    solved = solve_glaze(GLAZE_RACK)
    print("    solved")
    for line in render(solved).splitlines():
        print("        " + line)
    print()

    # ---- Half one.
    # Every batch of every split must be symmetric, and the batches must
    # reassemble into the original run. Those two facts are the definition.
    for split in splits:
        assert tuple(x for batch in split for x in batch) == FIRING_RUN
        for batch in split:
            assert _is_symmetric(batch, 0, len(batch))

    # A run of distinct temperatures can only be cut into single pots.
    assert all_splits((1, 2, 3)) == [[(1,), (2,), (3,)]]

    # A run that is symmetric whole can also be cut every other way that works,
    # so the count is more than one and the fewest is the whole run.
    assert fewest_batches((5, 5, 5)) == [(5, 5, 5)]
    assert len(all_splits((5, 5, 5))) == 4

    # The empty run has exactly one split: no batches at all.
    assert all_splits(()) == [[]]

    # ---- Half two.
    assert solved is not None
    # The given cells are untouched, and the input was not modified.
    for r in range(4):
        for c in range(4):
            if GLAZE_RACK[r][c] != ".":
                assert solved[r][c] == GLAZE_RACK[r][c]
    assert GLAZE_RACK[0][1] == "."

    # Rows, columns and quadrants each hold all four codes exactly once.
    for i in range(4):
        assert sorted(solved[i]) == list(GLAZE_CODES)
        assert sorted(solved[r][i] for r in range(4)) == list(GLAZE_CODES)
    for qr in (0, 2):
        for qc in (0, 2):
            block = [solved[r][c] for r in (qr, qr + 1) for c in (qc, qc + 1)]
            assert sorted(block) == list(GLAZE_CODES)

    # An unsolvable rack reports None rather than a half-filled grid.
    impossible = [["A", "A", ".", "."], [".", ".", ".", "."],
                  [".", ".", ".", "."], [".", ".", ".", "."]]
    assert solve_glaze(impossible) is None

    # Malformed racks are refused.
    for bad in ([["A"]], [["Z", ".", ".", "."], *[[".", ".", ".", "."]] * 3]):
        try:
            solve_glaze(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad!r}")

    print("All checks passed.")
```

The two halves sit in one file on purpose. Read the two recursive functions side
by side: `_split` appends and returns nothing, `_fill` returns a bool and stops.
That difference is the whole week.

## Run it

Download the solution beside this page and run it:

```bash
python README.py
```

No third-party packages, no arguments, no input. It prints both halves and then
`All checks passed.`

## Common bugs to catch

- **Enumerating when you meant to stop.** Symptom: the glaze solver explores every
  filling of an already-solved rack. Return `True` up the stack.
- **Stopping when you meant to enumerate.** Symptom: the firing run reports one
  split. Record and keep going.
- **Forgetting the undo in half two.** Symptom: a rack that fills with codes
  contradicting each other, because a failed branch left its guess behind.
- **Mutating the caller's rack.** Symptom: correct once, wrong the second time it
  is called. Copy before you fill.
- **Slicing to test symmetry.** Symptom: correct, and slower the longer the run.
  Compare in place.
- **Treating the empty run as zero splits.** Symptom: every count one short.

## Acceptance checklist

The week's mini-project is complete when:

- Both `mini-project/c2-week-12/problem-01-palindrome-partitioning.py` and `mini-project/c2-week-12/problem-02-sudoku-solver.py` are committed with passing self-tests.
- Both `frame-writeups/c2-week-12/mini-project/problem-01-palindrome-partitioning.md` and `frame-writeups/c2-week-12/mini-project/problem-02-sudoku-solver.md` are committed.
- A recording of at least one of the two write-ups is committed or linked (10–15 minutes).
- The Week 12 retrospective notes the most-useful and the most-challenging part of the mini-project.

The retrospective is the artifact you re-read in Week 16 (before Mock #3) and in Week 20 (before the Phase 2 capstone). It is the canonical evidence that the week's pattern recognition stuck.

---

*If you find errors in this mini-project, please open an issue or send a PR. Future learners will thank you.*

## Stretch

- Report how the split count grows for runs of 1 to 12 identical temperatures. The
  sequence is one you will recognise, and saying why is a good Examine (cost)
  paragraph.
- Make the glaze solver report **how many** fillings a rack has rather than one.
  The change is two lines and it converts half two into half one — say which two.
- Take a solved glaze rack, blank cells one at a time, and find the most you can
  blank while the filling stays unique. That is how a puzzle setter works, and it
  uses the counter from the previous stretch.

## How this connects to the rest of the curriculum

Palindrome partitioning is the canonical **string-partition backtracking**. The state design (`(start_index, path)`) and the constraint-propagation prune (palindrome check) generalize to:

- the stripped manifest line, every split — same state, dictionary lookup as the prune.
- the grid reference split — same state, value-and-length validation as the prune.
- the signal mast spacing — DP version of the same shape.

Sudoku is the canonical **constraint-satisfaction backtracking**. The state design (pruning sets per dimension) generalizes to:

- the drying rack sensors — three pruning sets per row, both diagonals.
- the kiln firing trail — visited set as the pruning set.
- Solving any Latin-square or graph-coloring problem — pruning set per constraint dimension.

The two together — combinatorial enumeration plus constraint satisfaction — cover the two halves of the backtracking universe. By Sunday of Week 12 you have the template and the two largest applications in your write-up portfolio.

---
