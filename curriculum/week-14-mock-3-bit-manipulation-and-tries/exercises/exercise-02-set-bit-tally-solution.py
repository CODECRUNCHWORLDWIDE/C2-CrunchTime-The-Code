"""exercise-02-set-bit-tally-solution.py - counting lamps, and reusing the count.

A panel of indicator lamps shows a register in binary. The maintenance log
wants, for every register value from 0 up to a limit, how many lamps are lit.

Counting each value on its own is fine and is the answer to say first. The
answer worth writing up notices that the work has already been done: a value's
lamp count is its own last bit plus the count of the value with that last bit
shifted off - and that value is smaller, so it is already in the table.

    lit[n] == lit[n >> 1] + (n & 1)

Shifting right by one drops the last lamp. Whatever is left is a number below
`n`, already counted. Add back the lamp that was dropped.

That is one table pass and one addition per value, against a bit-by-bit count
per value. The file counts the operations both ways so the difference is a
printed number rather than a claim about constants.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
LIMIT = 16
BIG_LIMIT = 1024


# ---- Your task ----
def lamp_tally(limit: int) -> tuple[list[int], int]:
    """Return the lamp count for every value from 0 to `limit`, and the work.

    Args:
        limit: The highest register value to count. Must not be negative.

    Returns:
        A pair: a list of length limit + 1 where entry n is the number of lamps
        lit for register value n, and how many additions the pass made.

    Raises:
        ValueError: If `limit` is negative.
    """
    if limit < 0:
        raise ValueError("a register limit cannot be negative")
    lit = [0] * (limit + 1)
    additions = 0
    for value in range(1, limit + 1):
        # value >> 1 is strictly smaller, so lit[value >> 1] is already written.
        lit[value] = lit[value >> 1] + (value & 1)
        additions += 1
    return lit, additions


def lamp_tally_one_at_a_time(limit: int) -> tuple[list[int], int]:
    """The same table, counting each value's bits from scratch. For comparison.

    Args:
        limit: The highest register value to count.

    Returns:
        The same list - this version is correct, only wasteful - and how many
        single-bit tests it made.

    Raises:
        ValueError: If `limit` is negative.
    """
    if limit < 0:
        raise ValueError("a register limit cannot be negative")
    lit: list[int] = []
    tests = 0
    for value in range(limit + 1):
        count = 0
        remaining = value
        while remaining:
            count += remaining & 1
            remaining >>= 1
            tests += 1
        lit.append(count)
    return lit, tests


def lamps_lit(value: int) -> int:
    """Return how many lamps one register value lights, by clearing them.

    Uses `value &= value - 1`, which clears the lowest lit lamp and nothing
    else. That makes the loop run once per LIT lamp rather than once per lamp
    position, so a register with two lamps lit costs two turns however wide the
    register is.

    Args:
        value: The register value. Must not be negative.

    Returns:
        The number of lit lamps.

    Raises:
        ValueError: If `value` is negative. A negative integer in Python has no
            finite binary width, so the loop would not terminate.
    """
    if value < 0:
        raise ValueError("a register value cannot be negative")
    count = 0
    while value:
        value &= value - 1
        count += 1
    return count


def fullest_value(limit: int) -> tuple[int, int]:
    """Return the value below `limit` lighting the most lamps, and how many.

    Args:
        limit: The highest register value to consider.

    Returns:
        A pair: the smallest value with the most lamps lit, and that count.

    Raises:
        ValueError: If `limit` is negative.
    """
    lit, _ = lamp_tally(limit)
    best = max(lit)
    return lit.index(best), best


# ---- Self-check ----
if __name__ == "__main__":
    lit, additions = lamp_tally(LIMIT)
    _, tests = lamp_tally_one_at_a_time(LIMIT)

    print(f"LAMPS LIT, 0 TO {LIMIT}")
    for value in range(LIMIT + 1):
        print(f"    {value:>3}  {value:>5b}   {lit[value]}")
    print()

    _, big_additions = lamp_tally(BIG_LIMIT)
    _, big_tests = lamp_tally_one_at_a_time(BIG_LIMIT)
    print("REUSING THE TABLE AGAINST COUNTING EACH VALUE")
    print(f"    to {LIMIT:>5}:  {additions:>6} additions   {tests:>6} bit tests")
    print(f"    to {BIG_LIMIT:>5}:  {big_additions:>6} additions   {big_tests:>6} bit tests")
    print()

    fullest, count = fullest_value(LIMIT)
    print(f"    fullest value below {LIMIT}: {fullest} ({fullest:b}) with {count} lamps")
    print()

    # The table opens 0, 1, 1, 2, 1, 2, 2, 3 - which is the pattern to check by
    # hand before trusting anything else.
    assert lit[:8] == [0, 1, 1, 2, 1, 2, 2, 3]

    # A power of two lights exactly one lamp, whatever its size.
    for power in range(5):
        assert lit[2 ** power] == 1

    # One less than a power of two lights every lamp below it.
    assert lit[15] == 4
    assert lit[7] == 3

    # The table version and the one-at-a-time version agree everywhere.
    slow, _ = lamp_tally_one_at_a_time(LIMIT)
    assert lit == slow

    # ...and `lamps_lit` agrees with both, value by value.
    for value in range(LIMIT + 1):
        assert lamps_lit(value) == lit[value]

    # The table does strictly less work, and the gap widens with the limit.
    assert additions < tests
    assert big_additions < big_tests
    assert big_tests / big_additions > tests / additions

    # A limit of zero is a table of one entry: zero lamps.
    assert lamp_tally(0)[0] == [0]

    # The fullest value below 16 is 15, with four lamps. Ties go to the
    # smallest value, which is why 15 rather than anything above it.
    assert fullest_value(LIMIT) == (15, 4)

    # Negative limits and values are refused rather than looping forever.
    try:
        lamp_tally(-1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for a negative limit")
    try:
        lamps_lit(-1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for a negative value")

    print("All checks passed.")
