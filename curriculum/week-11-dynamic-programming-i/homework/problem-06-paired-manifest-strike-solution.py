"""problem-06-paired-manifest-strike-solution.py - striking two manifests level.

A cargo is listed twice: once by the shipper and once by the receiving depot.
The two manifests disagree, and the clerk's job is to strike lines out of each
until the two read the same. Nothing may be added and nothing may be reordered
- only whole lines struck out.

Report the fewest strikes needed, counting a strike on either manifest as one.

The lines that survive are the same on both sides and in the same order on
both, which makes them the longest run common to the two manifests without
being contiguous. Once that length is known the answer is arithmetic: strike
everything else on both sides.

    strikes = len(shipper) + len(depot) - 2 * len(the common run)

Deriving that line is the exercise. The table underneath it is the ordinary
two-string fill: matching lines take the diagonal plus one, mismatching lines
take the better of up and left.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
SHIPPER: tuple[str, ...] = ("SALT", "HIDES", "TALLOW", "OATS", "PITCH", "ROPE")
DEPOT: tuple[str, ...] = ("HIDES", "SALT", "OATS", "TAR", "ROPE")


# ---- Your task ----
def common_run(shipper: tuple[str, ...], depot: tuple[str, ...]) -> list[str]:
    """Return the longest run of lines common to both manifests, in order.

    Args:
        shipper: The shipper's manifest, in order.
        depot: The depot's manifest, in order.

    Returns:
        The lines that survive on both sides, in the order they appear. Ties
        are broken towards the shipper's earlier lines, so the answer is one
        run rather than a family of them.
    """
    rows, cols = len(shipper) + 1, len(depot) + 1
    table = [[0] * cols for _ in range(rows)]
    for row in range(1, rows):
        for col in range(1, cols):
            if shipper[row - 1] == depot[col - 1]:
                table[row][col] = table[row - 1][col - 1] + 1
            else:
                table[row][col] = max(table[row - 1][col], table[row][col - 1])

    # Walk the finished table backwards to recover the run itself.
    run: list[str] = []
    row, col = len(shipper), len(depot)
    while row and col:
        if shipper[row - 1] == depot[col - 1]:
            run.append(shipper[row - 1])
            row -= 1
            col -= 1
        elif table[row - 1][col] >= table[row][col - 1]:
            row -= 1
        else:
            col -= 1
    run.reverse()
    return run


def run_table(shipper: tuple[str, ...], depot: tuple[str, ...]) -> list[list[int]]:
    """Return the whole length table, for reading rather than for the answer.

    Args:
        shipper: The shipper's manifest.
        depot: The depot's manifest.

    Returns:
        A grid with len(shipper) + 1 rows and len(depot) + 1 columns. Entry
        [s][d] is the length of the longest common run of the first s shipper
        lines and the first d depot lines.
    """
    rows, cols = len(shipper) + 1, len(depot) + 1
    table = [[0] * cols for _ in range(rows)]
    for row in range(1, rows):
        for col in range(1, cols):
            if shipper[row - 1] == depot[col - 1]:
                table[row][col] = table[row - 1][col - 1] + 1
            else:
                table[row][col] = max(table[row - 1][col], table[row][col - 1])
    return table


def strikes_needed(shipper: tuple[str, ...], depot: tuple[str, ...]) -> int:
    """Return the fewest line strikes that make the two manifests agree.

    Args:
        shipper: The shipper's manifest.
        depot: The depot's manifest.

    Returns:
        The number of strikes, counting one per line struck on either side.
        Zero when the manifests already agree.
    """
    return len(shipper) + len(depot) - 2 * len(common_run(shipper, depot))


def struck_lines(
    shipper: tuple[str, ...], depot: tuple[str, ...]
) -> tuple[list[str], list[str]]:
    """Return which lines are struck on each side.

    Args:
        shipper: The shipper's manifest.
        depot: The depot's manifest.

    Returns:
        A pair of lists: the shipper's struck lines and the depot's, each in
        the order they appear on that manifest. This is the part a clerk can
        act on; the count alone is not.
    """
    survivors = common_run(shipper, depot)

    def strike(manifest: tuple[str, ...]) -> list[str]:
        remaining = list(survivors)
        struck: list[str] = []
        for line in manifest:
            if remaining and line == remaining[0]:
                remaining.pop(0)
            else:
                struck.append(line)
        return struck

    return strike(shipper), strike(depot)


# ---- Self-check ----
if __name__ == "__main__":
    print("THE TWO MANIFESTS")
    print(f"    shipper : {list(SHIPPER)}")
    print(f"    depot   : {list(DEPOT)}")
    print()

    print("COMMON RUN LENGTH - rows are shipper lines, columns are depot lines")
    print("            " + "".join(f"{line[:4]:>7}" for line in ("-",) + DEPOT))
    for index, row in enumerate(run_table(SHIPPER, DEPOT)):
        label = "(none)" if index == 0 else SHIPPER[index - 1]
        print(f"    {label:<8}" + "".join(f"{value:>7}" for value in row))
    print()

    run = common_run(SHIPPER, DEPOT)
    shipper_struck, depot_struck = struck_lines(SHIPPER, DEPOT)
    print(f"    survives     : {run}")
    print(f"    strike from shipper: {shipper_struck}")
    print(f"    strike from depot  : {depot_struck}")
    print(f"    strikes needed     : {strikes_needed(SHIPPER, DEPOT)}")
    print()

    # SALT-OATS-ROPE survives on both sides. HIDES appears on both manifests
    # and cannot survive, because it is before SALT on one and after it on the
    # other - which is the whole reason this is not a set intersection.
    assert run == ["SALT", "OATS", "ROPE"]
    assert "HIDES" in SHIPPER and "HIDES" in DEPOT and "HIDES" not in run

    # 6 + 5 - 2 * 3 = 5 strikes.
    assert strikes_needed(SHIPPER, DEPOT) == 5
    assert len(shipper_struck) + len(depot_struck) == strikes_needed(SHIPPER, DEPOT)

    # Striking those lines really does leave two identical manifests.
    survivors_shipper = list(SHIPPER)
    for line in shipper_struck:
        survivors_shipper.remove(line)
    survivors_depot = list(DEPOT)
    for line in depot_struck:
        survivors_depot.remove(line)
    assert survivors_shipper == survivors_depot == run

    # Identical manifests need no strikes at all.
    assert strikes_needed(SHIPPER, SHIPPER) == 0
    assert common_run(SHIPPER, SHIPPER) == list(SHIPPER)

    # Manifests with nothing in common lose everything on both sides.
    assert strikes_needed(("A", "B"), ("C", "D")) == 4
    assert common_run(("A", "B"), ("C", "D")) == []

    # An empty manifest strikes the whole of the other one.
    assert strikes_needed((), SHIPPER) == len(SHIPPER)
    assert strikes_needed((), ()) == 0

    # Order is what makes this hard: the same lines in reverse share only one.
    assert len(common_run(("A", "B", "C"), ("C", "B", "A"))) == 1

    # A repeated line can survive more than once when both sides repeat it.
    assert common_run(("A", "A", "B"), ("A", "A", "C")) == ["A", "A"]
    assert strikes_needed(("A", "A", "B"), ("A", "A", "C")) == 2

    # The table's bottom-right corner is the length of the run, always.
    assert run_table(SHIPPER, DEPOT)[-1][-1] == len(run)

    print("All checks passed.")
