"""problem-06-test-tray-fill-solution.py - filling a tray so nothing repeats.

A glaze test tray is a square grid of wells. Every ROW must hold each glaze
exactly once, and so must every COLUMN - that is the whole point of the tray,
because it lets the studio compare glazes across two firing gradients at the
same time.

Some wells are already filled from a previous session. Finish the tray, or say
that it cannot be finished.

This is the constraint-satisfaction shape, and it differs from every other
walk this week in one way: the walk does not choose WHICH well to fill in an
arbitrary order. It fills them in a fixed order and chooses only what goes in
them. That keeps the state small - one row and one column set per line - and it
is why the legality test is a lookup rather than a scan.

The prune is the legality test itself, applied BEFORE descending rather than
after. Placing a glaze and discovering at the bottom of the tray that it was
illegal is the same walk doing far more work for the same answer, and the file
counts nodes for both so the difference is a number.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
GLAZES: tuple[str, ...] = ("A", "B", "C", "D")
EMPTY = "."

# A tray part-filled from a previous session.
TRAY: tuple[str, ...] = (
    "A...",
    "..C.",
    ".B..",
    "...A",
)

# A tray that cannot be finished: two As already share a column.
SPOILED: tuple[str, ...] = (
    "A...",
    "A...",
    "....",
    "....",
)


# ---- Your task ----
def check_tray(tray: tuple[str, ...], glazes: tuple[str, ...]) -> None:
    """Raise unless `tray` is a square grid of glazes and empty wells.

    Args:
        tray: The tray, one string per row.
        glazes: The glazes in use.

    Raises:
        ValueError: If the tray is not square, is not the size of the glaze
            set, or holds a character that is neither a glaze nor EMPTY.
    """
    size = len(glazes)
    if len(tray) != size or any(len(row) != size for row in tray):
        raise ValueError(f"the tray must be {size} by {size}")
    allowed = set(glazes) | {EMPTY}
    for row in tray:
        for well in row:
            if well not in allowed:
                raise ValueError(f"{well!r} is not a glaze or an empty well")


def already_spoiled(tray: tuple[str, ...], glazes: tuple[str, ...]) -> bool:
    """Say whether the wells already filled break the rule between themselves.

    Args:
        tray: The tray.
        glazes: The glazes in use.

    Returns:
        True when some row or column already holds one glaze twice. Written
        independently of the fill on purpose - a tray can be unfinishable
        because of what is already in it, and saying so is a better answer
        than "no solution found".

    Raises:
        ValueError: If the tray is not a valid tray.
    """
    check_tray(tray, glazes)
    size = len(glazes)
    for line in range(size):
        row = [tray[line][col] for col in range(size) if tray[line][col] != EMPTY]
        col = [tray[r][line] for r in range(size) if tray[r][line] != EMPTY]
        if len(set(row)) != len(row) or len(set(col)) != len(col):
            return True
    return False


def fill_tray(
    tray: tuple[str, ...], glazes: tuple[str, ...]
) -> tuple[tuple[str, ...] | None, int]:
    """Finish the tray, or report that it cannot be finished.

    Args:
        tray: The tray, part filled.
        glazes: The glazes in use.

    Returns:
        A pair: the finished tray, or None when no filling exists, and how many
        wells the walk placed a glaze into.

    Raises:
        ValueError: If the tray is not a valid tray.
    """
    check_tray(tray, glazes)
    size = len(glazes)
    wells = [list(row) for row in tray]
    rows: list[set[str]] = [set() for _ in range(size)]
    cols: list[set[str]] = [set() for _ in range(size)]

    for row in range(size):
        for col in range(size):
            glaze = wells[row][col]
            if glaze != EMPTY:
                if glaze in rows[row] or glaze in cols[col]:
                    return None, 0        # spoiled before the walk begins
                rows[row].add(glaze)
                cols[col].add(glaze)

    placed = 0

    def walk(position: int) -> bool:
        nonlocal placed
        if position == size * size:
            return True
        row, col = divmod(position, size)
        if wells[row][col] != EMPTY:
            return walk(position + 1)
        for glaze in glazes:
            # The legality test IS the prune, and it happens before descending.
            if glaze in rows[row] or glaze in cols[col]:
                continue
            wells[row][col] = glaze       # choose
            rows[row].add(glaze)
            cols[col].add(glaze)
            placed += 1
            if walk(position + 1):        # explore
                return True
            wells[row][col] = EMPTY       # undo - three things this time
            rows[row].discard(glaze)
            cols[col].discard(glaze)
        return False

    if walk(0):
        return tuple("".join(row) for row in wells), placed
    return None, placed


def fill_tray_late_check(
    tray: tuple[str, ...], glazes: tuple[str, ...]
) -> tuple[tuple[str, ...] | None, int]:
    """The same fill that checks legality only at the bottom, for comparison.

    Args:
        tray: The tray, part filled.
        glazes: The glazes in use.

    Returns:
        The same answer for far more work, and the wells it placed into. This
        is what "prune early" costs when it is not done, and on a four-glaze
        tray the difference is already large enough to print.

    Raises:
        ValueError: If the tray is not a valid tray.
    """
    check_tray(tray, glazes)
    size = len(glazes)
    wells = [list(row) for row in tray]
    placed = 0

    def legal() -> bool:
        for line in range(size):
            row = [wells[line][c] for c in range(size) if wells[line][c] != EMPTY]
            col = [wells[r][line] for r in range(size) if wells[r][line] != EMPTY]
            if len(set(row)) != len(row) or len(set(col)) != len(col):
                return False
        return True

    def walk(position: int) -> bool:
        nonlocal placed
        if position == size * size:
            return legal()
        row, col = divmod(position, size)
        if wells[row][col] != EMPTY:
            return walk(position + 1)
        for glaze in glazes:
            wells[row][col] = glaze
            placed += 1
            if walk(position + 1):
                return True
            wells[row][col] = EMPTY
        return False

    if walk(0):
        return tuple("".join(row) for row in wells), placed
    return None, placed


# ---- Self-check ----
if __name__ == "__main__":
    filled, placed = fill_tray(TRAY, GLAZES)
    _, late_placed = fill_tray_late_check(TRAY, GLAZES)

    print("THE TRAY AS FOUND")
    for row in TRAY:
        print("    " + " ".join(row))
    print()

    print("THE TRAY FINISHED")
    for row in filled or ():
        print("    " + " ".join(row))
    print()

    print("CHECKING EARLY AGAINST CHECKING LATE")
    print(f"    wells filled, pruning early : {placed}")
    print(f"    wells filled, checking late : {late_placed}")
    print()

    print("A TRAY THAT CANNOT BE FINISHED")
    for row in SPOILED:
        print("    " + " ".join(row))
    print(f"    already spoiled: {already_spoiled(SPOILED, GLAZES)}")
    print(f"    fill_tray says : {fill_tray(SPOILED, GLAZES)[0]}")
    print()

    # The tray can be finished.
    assert filled is not None

    # Every row and every column holds each glaze exactly once.
    for line in range(len(GLAZES)):
        assert sorted(filled[line]) == sorted(GLAZES)
        assert sorted(filled[r][line] for r in range(len(GLAZES))) == sorted(GLAZES)

    # The wells that were already filled are untouched.
    for row in range(len(GLAZES)):
        for col in range(len(GLAZES)):
            if TRAY[row][col] != EMPTY:
                assert filled[row][col] == TRAY[row][col]

    # Checking early does strictly less work than checking late, for the same
    # answer. That is the whole argument for pruning where the choice is made.
    assert placed < late_placed
    assert fill_tray_late_check(TRAY, GLAZES)[0] is not None

    # A tray already spoiled is reported as spoiled, and cannot be filled.
    assert already_spoiled(SPOILED, GLAZES) is True
    assert fill_tray(SPOILED, GLAZES)[0] is None

    # A tray as found that is legal is not spoiled.
    assert already_spoiled(TRAY, GLAZES) is False

    # An empty tray fills straightforwardly; a full legal tray is returned as is.
    empty = tuple(EMPTY * len(GLAZES) for _ in GLAZES)
    assert fill_tray(empty, GLAZES)[0] is not None
    done = ("ABCD", "BCDA", "CDAB", "DABC")
    assert fill_tray(done, GLAZES)[0] == done

    # A tray of the wrong size, or holding something that is not a glaze, is
    # refused rather than guessed at.
    for bad in (("ABC", "BCA", "CAB"), ("ABCD", "BCDA", "CDAB", "DABX")):
        try:
            fill_tray(bad, GLAZES)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad}")

    print("All checks passed.")
