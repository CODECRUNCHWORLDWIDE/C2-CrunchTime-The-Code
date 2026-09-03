"""problem-02-lamp-distance-solution.py - how far apart two panels are.

A works has two indicator panels that are supposed to show the same register.
When they disagree, the electrician wants to know HOW MUCH - not whether, but in
how many lamp positions.

Two questions, and the second falls out of the first in one line:

    lamps_lit(value)      how many lamps one panel has lit
    lamp_distance(a, b)   in how many positions the two panels differ

XOR is what joins them. `a ^ b` lights a bit exactly where the two registers
disagree, so the distance is the lamp count of the XOR - and once that sentence
is written down there is no second algorithm to write.

The counting itself is the Kernighan loop from Exercise 2: `n &= n - 1` clears
the lowest lit lamp, so the loop turns once per LIT lamp rather than once per
lamp position. On a 16-bit register differing in two places, that is two turns
and not sixteen.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

WIDTH = 16

# ---- Given data ----
# Readings taken from the two panels at the same moment.
PANEL_A: tuple[int, ...] = (0b0000_0000_0000_0000, 0b1111_0000_1111_0000,
                            0b1010_1010_1010_1010, 0b0000_0000_1111_1111,
                            0b1111_1111_1111_1111)
PANEL_B: tuple[int, ...] = (0b0000_0000_0000_0001, 0b1111_0000_1111_0000,
                            0b0101_0101_0101_0101, 0b1111_1111_0000_0000,
                            0b0000_0000_0000_0000)


# ---- Your task ----
def check_register(name: str, value: int) -> None:
    """Raise unless `value` fits in WIDTH bits.

    Args:
        name: What the value is, for the message.
        value: The register reading.

    Raises:
        ValueError: If the value is negative or too wide. Negative matters:
            a negative Python integer has no finite binary width, so the
            clearing loop below would never terminate.
    """
    if not 0 <= value < (1 << WIDTH):
        raise ValueError(f"{name} {value} is not a {WIDTH}-bit register")


def lamps_lit(value: int) -> tuple[int, int]:
    """Return how many lamps are lit, and how many turns it took.

    Args:
        value: The register reading.

    Returns:
        A pair: the number of lit lamps, and the number of loop turns - which
        are the same number, and that is the point. The loop runs once per lit
        lamp, never once per position.

    Raises:
        ValueError: If the value does not fit in WIDTH bits.
    """
    check_register("value", value)
    count = turns = 0
    while value:
        value &= value - 1      # clears the lowest lit lamp and nothing else
        count += 1
        turns += 1
    return count, turns


def lamps_lit_by_position(value: int) -> tuple[int, int]:
    """The same count, testing every position. For comparison.

    Args:
        value: The register reading.

    Returns:
        A pair: the count, and the turns - which is always WIDTH, whatever the
        value. Shipped so "once per lit lamp" is a number rather than a claim.

    Raises:
        ValueError: If the value does not fit in WIDTH bits.
    """
    check_register("value", value)
    count = 0
    for position in range(WIDTH):
        count += value >> position & 1
    return count, WIDTH


def lamp_distance(first: int, second: int) -> int:
    """Return in how many positions two registers differ.

    Args:
        first: One panel's reading.
        second: The other panel's reading.

    Returns:
        The number of differing lamp positions. Zero when the panels agree,
        WIDTH when they disagree everywhere.

    Raises:
        ValueError: If either value does not fit in WIDTH bits.
    """
    check_register("first", first)
    check_register("second", second)
    return lamps_lit(first ^ second)[0]


def worst_pair(readings: tuple[int, ...]) -> tuple[int, int, int] | None:
    """Return the two readings that differ most, and by how much.

    Args:
        readings: Register readings.

    Returns:
        A triple: the two positions in the list and the distance between them,
        or None when there are fewer than two readings. Ties go to the earliest
        pair, so the answer is one pair.

    Raises:
        ValueError: If any reading does not fit in WIDTH bits.
    """
    if len(readings) < 2:
        return None
    best = (0, 1, -1)
    for first in range(len(readings)):
        for second in range(first + 1, len(readings)):
            gap = lamp_distance(readings[first], readings[second])
            if gap > best[2]:
                best = (first, second, gap)
    return best


# ---- Self-check ----
if __name__ == "__main__":
    print("PANEL READINGS AND THEIR DISTANCE")
    print("    A                  B                  differ")
    for a, b in zip(PANEL_A, PANEL_B):
        print(f"    {a:0{WIDTH}b}   {b:0{WIDTH}b}   {lamp_distance(a, b):>2}")
    print()

    print("CLEARING THE LOWEST LAMP AGAINST TESTING EVERY POSITION")
    for value in (0b0000_0000_0000_0000, 0b0000_0000_0000_0011,
                  0b1010_1010_1010_1010, 0b1111_1111_1111_1111):
        lit, turns = lamps_lit(value)
        _, position_turns = lamps_lit_by_position(value)
        print(f"    {value:0{WIDTH}b}  {lit:>2} lit   {turns:>2} turns / {position_turns} tested")
    print()

    pair = worst_pair(PANEL_A)
    print(f"    the two panel-A readings that differ most: {pair}")
    print()

    # A register agrees with itself everywhere.
    for value in PANEL_A:
        assert lamp_distance(value, value) == 0

    # All zeroes against all ones differ in every position.
    assert lamp_distance(0, (1 << WIDTH) - 1) == WIDTH

    # Alternating patterns are the maximal disagreement short of that.
    assert lamp_distance(0b1010_1010_1010_1010, 0b0101_0101_0101_0101) == WIDTH

    # The distance is symmetric, which follows from XOR being symmetric.
    for a, b in zip(PANEL_A, PANEL_B):
        assert lamp_distance(a, b) == lamp_distance(b, a)

    # The two counting methods agree on every value in the data.
    for value in PANEL_A + PANEL_B:
        assert lamps_lit(value)[0] == lamps_lit_by_position(value)[0]

    # The clearing loop turns once per lit lamp; the positional test always
    # turns WIDTH times. That is the whole claim, and it is asserted.
    for value in PANEL_A + PANEL_B:
        lit, turns = lamps_lit(value)
        assert turns == lit
        assert lamps_lit_by_position(value)[1] == WIDTH

    # A register of zero costs no turns at all.
    assert lamps_lit(0) == (0, 0)

    # The distance obeys the triangle inequality, which is worth checking
    # because it is what makes "distance" the right word.
    for a in PANEL_A:
        for b in PANEL_B:
            for c in PANEL_A:
                assert lamp_distance(a, c) <= lamp_distance(a, b) + lamp_distance(b, c)

    # Fewer than two readings has no worst pair.
    assert worst_pair(()) is None
    assert worst_pair((5,)) is None

    # Out-of-range registers are refused, negatives included.
    for bad in (1 << WIDTH, -1):
        try:
            lamps_lit(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad}")

    print("All checks passed.")
