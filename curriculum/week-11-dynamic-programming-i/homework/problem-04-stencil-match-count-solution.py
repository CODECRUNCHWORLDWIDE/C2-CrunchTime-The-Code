"""problem-04-stencil-match-count-solution.py - how many ways a mark hides in a run.

A depot stencils long runs of characters onto crate sides. An inspector is
looking for a short mark inside a run, and the rule is that the mark's
characters must appear IN ORDER but need not be next to each other - the die
skips, so the mark can be spread across the run with other characters between.

Count how many distinct ways the mark can be picked out of the run. Two ways
are distinct when they use a different set of positions, even if they read the
same.

The table is two-dimensional and every entry has the same shape of answer: to
account for the first `m` characters of the mark using the first `r` of the
run, either the run's character is not used at all - which is the entry one
column left - or it is used and matches, which is the entry one row up and one
column left. Add them.

The row order matters. Filling the run outer and the mark inner is fine; doing
it the other way round without care reads entries that have not been written
yet, and the count comes out low with nothing to show why.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
RUN = "RABBABRAB"
MARK = "RAB"


# ---- Your task ----
def match_count(run: str, mark: str) -> int:
    """Count the ways `mark` can be picked out of `run` in order.

    Args:
        run: The stencilled run of characters.
        mark: The mark the inspector is looking for.

    Returns:
        How many distinct sets of positions in `run` spell `mark` in order.
        An empty mark is found exactly once - by taking nothing - which is what
        makes the table's first column all ones and the recurrence start
        without a special case.
    """
    # One row per mark length, one column per run length. Only the previous
    # row is ever read, so two rows would do; the whole table is kept because
    # printing it is half the exercise.
    rows, cols = len(mark) + 1, len(run) + 1
    table = [[0] * cols for _ in range(rows)]
    for col in range(cols):
        table[0][col] = 1        # the empty mark: found once, by taking nothing

    for row in range(1, rows):
        for col in range(1, cols):
            # Not using this run character: whatever the count was without it.
            table[row][col] = table[row][col - 1]
            if run[col - 1] == mark[row - 1]:
                # Using it: the count for one fewer mark character, one fewer
                # run character.
                table[row][col] += table[row - 1][col - 1]
    return table[-1][-1]


def match_table(run: str, mark: str) -> list[list[int]]:
    """Return the whole count table, for reading rather than for the answer.

    Args:
        run: The stencilled run.
        mark: The mark.

    Returns:
        A grid with len(mark) + 1 rows and len(run) + 1 columns. Entry
        [m][r] is the number of ways to pick the first m characters of the mark
        out of the first r of the run.
    """
    rows, cols = len(mark) + 1, len(run) + 1
    table = [[0] * cols for _ in range(rows)]
    for col in range(cols):
        table[0][col] = 1
    for row in range(1, rows):
        for col in range(1, cols):
            table[row][col] = table[row][col - 1]
            if run[col - 1] == mark[row - 1]:
                table[row][col] += table[row - 1][col - 1]
    return table


def first_match(run: str, mark: str) -> list[int] | None:
    """Return the earliest set of positions spelling `mark`, or None.

    Args:
        run: The stencilled run.
        mark: The mark.

    Returns:
        The positions, counted from 0, of the leftmost way to pick the mark
        out of the run - or None when the mark is not there at all. A count of
        zero and a None here always agree, and the checks assert that.
    """
    positions: list[int] = []
    cursor = 0
    for wanted in mark:
        while cursor < len(run) and run[cursor] != wanted:
            cursor += 1
        if cursor == len(run):
            return None
        positions.append(cursor)
        cursor += 1
    return positions


# ---- Self-check ----
if __name__ == "__main__":
    print(f"RUN   {RUN}")
    print(f"MARK  {MARK}")
    print()

    print("COUNT TABLE - rows are mark prefixes, columns are run prefixes")
    table = match_table(RUN, MARK)
    print("            " + "".join(f"{ch:>4}" for ch in "-" + RUN))
    for index, row in enumerate(table):
        label = ("(none)" if index == 0 else MARK[:index])
        print(f"    {label:<8}" + "".join(f"{count:>4}" for count in row))
    print()

    print(f"    ways to find {MARK} in {RUN}: {match_count(RUN, MARK)}")
    print(f"    earliest positions          : {first_match(RUN, MARK)}")
    print()

    # Worked by hand: R A B can be picked out of R A B B A B R A B in several
    # ways, and the table's bottom-right corner is the count.
    assert match_count(RUN, MARK) == match_table(RUN, MARK)[-1][-1]

    # The empty mark is found once, by taking nothing.
    assert match_count(RUN, "") == 1
    assert match_count("", "") == 1

    # A mark longer than the run cannot be found.
    assert match_count("AB", "ABC") == 0
    assert match_count("", "A") == 0

    # An exact run finds itself exactly once.
    assert match_count("RAB", "RAB") == 1

    # Repeats multiply. "AA" sits inside "AAA" three ways: positions 01, 02, 12.
    assert match_count("AAA", "AA") == 3
    assert match_count("AAAA", "AA") == 6

    # A run of one repeated character finds a mark of the same character
    # exactly as many ways as there are ways to choose those positions.
    assert match_count("AAAAA", "AAA") == 10

    # Order matters: "BA" is not in a run that only ever has A before B.
    assert match_count("AB", "BA") == 0

    # A count of zero and no first match always agree, in both directions.
    for run, mark in (("RABBABRAB", "RAB"), ("AB", "BA"), ("AB", "ABC"), ("", "A")):
        assert (match_count(run, mark) == 0) == (first_match(run, mark) is None)

    # The first match really does spell the mark, in order.
    positions = first_match(RUN, MARK)
    assert positions is not None
    assert "".join(RUN[position] for position in positions) == MARK
    assert positions == sorted(positions)

    print("All checks passed.")
