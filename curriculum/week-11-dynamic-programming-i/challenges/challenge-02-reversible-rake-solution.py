"""challenge-02-reversible-rake-solution.py - the longest rake that reads both ways.

A shunting yard makes up a rake of wagons from a standing line. Each wagon has a
one-letter type code. A rake is REVERSIBLE when its type codes read the same from
either end, because the locomotive can then run round and push it back without
the load being redistributed.

Wagons may be detached from anywhere in the line, but the ones that remain keep
their order - nothing is shunted past anything else. So the longest reversible
rake is the longest subsequence of the line that reads the same both ways.

The yard does not want a length. It wants the WAGONS, and it wants to know which
ones to detach, because that is the work.

  longest_rake     - the wagon codes of the longest reversible rake
  detach_list      - the positions to detach, in the order a shunter walks them
  rake_report      - both, for a few lines

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
# One type code per wagon, from the buffer stop outwards.
STANDING_LINE = "OXBVANBXO"


# ---- Your task ----
def _table(line: str) -> list[list[int]]:
    """Longest reversible rake within line[lo..hi], for every lo and hi.

    Filled by increasing span length, because the answer for a span depends on
    strictly shorter spans and on nothing else. Filling row by row instead
    reads entries that have not been written yet - which is the bug that makes
    this table look almost right.

    Args:
        line: The standing line of type codes.

    Returns:
        A square table; entry [lo][hi] is the best length within that span.
    """
    size = len(line)
    best = [[0] * size for _ in range(size)]
    for lo in range(size):
        best[lo][lo] = 1  # one wagon reads the same either way

    for span in range(2, size + 1):
        for lo in range(size - span + 1):
            hi = lo + span - 1
            if line[lo] == line[hi]:
                # The two ends pair off. For a span of two that inner span is
                # empty, which is 0 - hence the guard rather than best[lo+1][hi-1].
                inner = best[lo + 1][hi - 1] if span > 2 else 0
                best[lo][hi] = inner + 2
            else:
                best[lo][hi] = max(best[lo + 1][hi], best[lo][hi - 1])
    return best


def longest_rake(line: str) -> str:
    """The type codes of the longest reversible rake.

    Args:
        line: The standing line of type codes.

    Returns:
        The rake's codes in order. Ties are settled by taking the leftmost
        wagon available at each step, so the answer is one rake rather than a
        family of them.
    """
    if not line:
        return ""

    best = _table(line)
    lo, hi = 0, len(line) - 1
    front: list[str] = []
    back: list[str] = []

    while lo <= hi:
        if lo == hi:
            front.append(line[lo])
            break
        if line[lo] == line[hi]:
            front.append(line[lo])
            back.append(line[hi])
            lo, hi = lo + 1, hi - 1
        elif best[lo + 1][hi] > best[lo][hi - 1]:
            # Strictly greater, so an equal pair falls through to the branch
            # below and the BACK wagon is dropped. That keeps the leftmost
            # wagon available, which is the tie-break the docstring promises -
            # and a tie-break you state but do not implement is worse than none.
            lo += 1
        else:
            hi -= 1

    back.reverse()
    return "".join(front + back)


def detach_list(line: str) -> list[int]:
    """Positions to detach, left to right, to leave the longest rake.

    Args:
        line: The standing line of type codes.

    Returns:
        Zero-based positions in the ORIGINAL line. Left to right is how a
        shunter walks the line, so it is the order the list is given in.
    """
    keep = longest_rake(line)
    detach: list[int] = []
    at = 0
    for position, code in enumerate(line):
        if at < len(keep) and code == keep[at]:
            at += 1
        else:
            detach.append(position)
    return detach


def rake_report(lines: list[str]) -> None:
    """Print the rake and the detach list for each standing line."""
    for line in lines:
        rake = longest_rake(line)
        detach = detach_list(line)
        shown = line or "(empty)"
        print(f"    {shown:<12} rake {rake or '(none)':<10} detach {detach}")


# ---- Self-check ----
if __name__ == "__main__":
    print("standing lines")
    rake_report([STANDING_LINE, "BOX", "AA", "AB", "ABCBA", "", "XYZ"])

    rake = longest_rake(STANDING_LINE)
    print()
    print(f"    line {STANDING_LINE} -> rake {rake} ({len(rake)} wagons)")

    # The rake must read the same both ways. That is the definition, so it is
    # the first thing asserted, for every case.
    for line in (STANDING_LINE, "BOX", "AA", "AB", "ABCBA", "", "XYZ", "AABAA"):
        got = longest_rake(line)
        assert got == got[::-1], (line, got)

    # It must be a subsequence of the line: same order, nothing shunted past.
    for line in (STANDING_LINE, "ABCBA", "XYZ", "AABAA"):
        got = longest_rake(line)
        at = 0
        for code in line:
            if at < len(got) and code == got[at]:
                at += 1
        assert at == len(got), (line, got)

    # And the detach list must be exactly the wagons not in the rake.
    for line in (STANDING_LINE, "ABCBA", "XYZ", "AABAA", "AA", ""):
        assert len(detach_list(line)) == len(line) - len(longest_rake(line))

    # Known answers.
    assert longest_rake("ABCBA") == "ABCBA"      # already reversible
    assert detach_list("ABCBA") == []
    assert longest_rake("AA") == "AA"
    assert longest_rake("") == ""
    assert detach_list("") == []

    # A line with no repeats leaves a single wagon, and the tie-break says which.
    assert longest_rake("XYZ") == "X"   # leftmost, per the tie-break
    assert detach_list("XYZ") == [1, 2]

    # The shipped line: OXBVANBXO. Three pairs nest - O..O, X..X, B..B - around
    # one wagon from the middle, so the best rake is 7 of the 9 wagons.
    assert len(longest_rake(STANDING_LINE)) == 7
    assert len(detach_list(STANDING_LINE)) == 2

    print()
    print("All checks passed.")
