"""problem-05-two-clerk-daybook-solution.py - did two clerks write this day book?

Two clerks share one day book. Each writes their own entries into it as the day
goes on, so the finished book holds both clerks' entries interleaved - but each
clerk's entries appear in the book in the order that clerk wrote them, because
neither clerk ever goes back.

Given the two clerks' own records and the finished day book, say whether the
book could have been produced this way.

The obvious approach - walk the book and give each entry to whichever clerk has
it next - is wrong, and it is wrong in a way that looks right on most data.
When both clerks are due to write the same character, choosing one commits you,
and the choice can be the wrong one. This file ships that greedy version on
purpose so the two can be run side by side.

The table is the answer. Entry [a][b] says whether the first a entries of clerk
one and the first b of clerk two could have made the first a+b entries of the
book. A cell is reachable when the cell above it is and clerk one's next entry
matches, or the cell to its left is and clerk two's does.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
# Each entry is one letter: the initial of the ledger it was posted to.
CLERK_ONE = "ABAB"
CLERK_TWO = "AABB"
DAY_BOOK = "AABABABB"

# The book that catches a greedy reader. Clerk one opens with two As and clerk
# two with one, and the book needs clerk one to hand over the second A. A
# reader that takes from clerk one whenever it can takes both, and then has
# nothing left that can write the B.
TRAP_ONE = "AA"
TRAP_TWO = "AB"
TRAP_BOOK = "AABA"


# ---- Your task ----
def interleaves(first: str, second: str, book: str) -> bool:
    """Say whether `book` is an interleaving of `first` and `second`.

    Args:
        first: One clerk's entries, in the order they wrote them.
        second: The other clerk's entries, in order.
        book: The finished day book.

    Returns:
        True when the book can be split into the two clerks' records without
        reordering either. False otherwise - including when the lengths do not
        add up, which is checked first because it is free.
    """
    if len(first) + len(second) != len(book):
        return False

    # reachable[b] is "the first `taken_from_first` of `first` and the first b
    # of `second` account for the book so far". One row at a time is enough,
    # because a row only ever reads itself and the row above.
    reachable = [False] * (len(second) + 1)
    reachable[0] = True
    for index in range(1, len(second) + 1):
        reachable[index] = reachable[index - 1] and second[index - 1] == book[index - 1]

    for taken in range(1, len(first) + 1):
        # Column 0: everything so far came from `first` alone.
        reachable[0] = reachable[0] and first[taken - 1] == book[taken - 1]
        for index in range(1, len(second) + 1):
            from_first = reachable[index] and first[taken - 1] == book[taken + index - 1]
            from_second = reachable[index - 1] and second[index - 1] == book[taken + index - 1]
            reachable[index] = from_first or from_second
    return reachable[-1]


def interleave_table(first: str, second: str, book: str) -> list[list[bool]]:
    """Return the whole reachability table, for reading rather than for speed.

    Args:
        first: One clerk's entries.
        second: The other clerk's entries.
        book: The finished day book.

    Returns:
        A grid with len(first) + 1 rows and len(second) + 1 columns. Entry
        [a][b] is True when the first a entries of `first` and the first b of
        `second` account for the first a + b entries of the book.

    Raises:
        ValueError: If the two records cannot possibly fill the book, because
            a table would then mean nothing.
    """
    if len(first) + len(second) != len(book):
        raise ValueError("the two records do not add up to the length of the book")
    rows, cols = len(first) + 1, len(second) + 1
    table = [[False] * cols for _ in range(rows)]
    table[0][0] = True
    for row in range(rows):
        for col in range(cols):
            if row == 0 and col == 0:
                continue
            here = row + col - 1
            if row and table[row - 1][col] and first[row - 1] == book[here]:
                table[row][col] = True
            if col and table[row][col - 1] and second[col - 1] == book[here]:
                table[row][col] = True
    return table


def greedy_interleaves(first: str, second: str, book: str) -> bool:
    """The obvious wrong answer, kept for comparison.

    Walks the book once and hands each entry to whichever clerk has it next,
    preferring the first clerk on a tie. It is fast, it is simple, and it is
    wrong whenever a tie can be resolved only one way.

    Args:
        first: One clerk's entries.
        second: The other clerk's entries.
        book: The finished day book.

    Returns:
        Its answer, which agrees with `interleaves` on most inputs and not on
        all of them.
    """
    if len(first) + len(second) != len(book):
        return False
    one = two = 0
    for entry in book:
        if one < len(first) and first[one] == entry:
            one += 1
        elif two < len(second) and second[two] == entry:
            two += 1
        else:
            return False
    return True


def split_book(first: str, second: str, book: str) -> str | None:
    """Return which clerk wrote each entry, or None when the book is impossible.

    Args:
        first: One clerk's entries.
        second: The other clerk's entries.
        book: The finished day book.

    Returns:
        A string of "1" and "2" the same length as the book, naming the clerk
        for each entry - or None when no split exists. Walks the finished table
        backwards from the bottom-right corner, so it costs nothing extra.
    """
    if len(first) + len(second) != len(book):
        return None
    table = interleave_table(first, second, book)
    row, col = len(first), len(second)
    if not table[row][col]:
        return None
    marks: list[str] = []
    while row or col:
        here = row + col - 1
        if row and table[row - 1][col] and first[row - 1] == book[here]:
            marks.append("1")
            row -= 1
        else:
            marks.append("2")
            col -= 1
    marks.reverse()
    return "".join(marks)


# ---- Self-check ----
if __name__ == "__main__":
    print("THE DAY BOOK")
    print(f"    clerk one : {CLERK_ONE}")
    print(f"    clerk two : {CLERK_TWO}")
    print(f"    day book  : {DAY_BOOK}")
    print(f"    interleaves: {interleaves(CLERK_ONE, CLERK_TWO, DAY_BOOK)}")
    split = split_book(CLERK_ONE, CLERK_TWO, DAY_BOOK)
    print(f"    who wrote  : {split}")
    print()

    print("REACHABILITY TABLE - rows are clerk one, columns are clerk two")
    print("            " + "".join(f"{ch:>3}" for ch in "-" + CLERK_TWO))
    for index, row in enumerate(interleave_table(CLERK_ONE, CLERK_TWO, DAY_BOOK)):
        label = "(none)" if index == 0 else CLERK_ONE[:index]
        print(f"    {label:<8}" + "".join(("  y" if cell else "  .") for cell in row))
    print()

    print("THE BOOK THAT CATCHES A GREEDY READER")
    print(f"    clerk one : {TRAP_ONE}")
    print(f"    clerk two : {TRAP_TWO}")
    print(f"    day book  : {TRAP_BOOK}")
    print(f"    table says : {interleaves(TRAP_ONE, TRAP_TWO, TRAP_BOOK)}")
    print(f"    greedy says: {greedy_interleaves(TRAP_ONE, TRAP_TWO, TRAP_BOOK)}")
    print()

    # The shipped day book really is an interleaving.
    assert interleaves(CLERK_ONE, CLERK_TWO, DAY_BOOK) is True

    # The trap: the table gets it right and the greedy reader does not.
    assert interleaves(TRAP_ONE, TRAP_TWO, TRAP_BOOK) is True
    assert greedy_interleaves(TRAP_ONE, TRAP_TWO, TRAP_BOOK) is False

    # Lengths that do not add up are refused before anything else.
    assert interleaves("AB", "CD", "ABC") is False
    assert interleaves("", "", "A") is False

    # Two empty records make an empty book, and nothing else.
    assert interleaves("", "", "") is True

    # One clerk writing nothing means the book is the other clerk's record.
    assert interleaves("ABC", "", "ABC") is True
    assert interleaves("ABC", "", "ACB") is False

    # Order within a clerk is never allowed to change.
    assert interleaves("AB", "CD", "ABDC") is False
    assert interleaves("AB", "CD", "ACBD") is True

    # The split really does reconstruct both records, in order.
    marks = split_book(CLERK_ONE, CLERK_TWO, DAY_BOOK)
    assert marks is not None
    one = "".join(entry for entry, mark in zip(DAY_BOOK, marks) if mark == "1")
    two = "".join(entry for entry, mark in zip(DAY_BOOK, marks) if mark == "2")
    assert one == CLERK_ONE and two == CLERK_TWO

    # An impossible book has no split, and the two agree on that.
    assert split_book("AB", "CD", "ABDC") is None
    assert interleaves("AB", "CD", "ABDC") is False

    # A table cannot be built for records that do not fit the book.
    try:
        interleave_table("AB", "CD", "ABC")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for a mismatched length")

    print("All checks passed.")
