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
