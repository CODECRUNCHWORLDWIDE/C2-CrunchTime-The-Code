"""problem-04-common-prefix-range-solution.py - what a whole range has in common.

A meter runs through every count from `low` to `high` inclusive during a test.
A latching relay board is wired to AND every count together, so what is left at
the end is the bits that were set in EVERY count of the range.

Report that value, without looping through the range - because the range can be
the whole 16-bit space and the board would have to be modelled a million times.

The structural observation is the whole problem, and it is one sentence: the AND
of a range is the common HIGH-BIT PREFIX of its two ends, with every lower bit
zeroed.

Why: take any bit position below the point where `low` and `high` first differ.
Somewhere inside the range that bit flips to 0 - it must, because the range
crosses a boundary at that position - and once a column holds a 0, the AND of
that column is 0. Above the first difference, both ends agree and so does
everything between them.

So the answer is: shift both ends right until they are equal, then shift that
value back left by the same amount.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

WIDTH = 16
MASK = (1 << WIDTH) - 1

# ---- Given data ----
RANGES: tuple[tuple[int, int], ...] = (
    (5, 7),
    (0, 0),
    (12, 12),
    (0, 1),
    (26, 30),
    (600, 700),
    (0, MASK),
    (0b1111_0000_0000_0000, 0b1111_0000_1111_1111),
)


# ---- Your task ----
def check_range(low: int, high: int) -> None:
    """Raise unless `low` and `high` are a valid range of WIDTH-bit counts.

    Args:
        low: The first count.
        high: The last count.

    Raises:
        ValueError: If either end is out of range, or `low` is above `high`.
    """
    for name, value in (("low", low), ("high", high)):
        if not 0 <= value <= MASK:
            raise ValueError(f"{name} {value} is not a {WIDTH}-bit count")
    if low > high:
        raise ValueError(f"low {low} is above high {high}")


def latched(low: int, high: int) -> tuple[int, int]:
    """Return the AND of every count in the range, and the shifts it took.

    Args:
        low: The first count.
        high: The last count.

    Returns:
        A pair: the latched value, and how many positions the two ends had to
        be shifted before they agreed - which is how many low bits are zero in
        the answer.

    Raises:
        ValueError: If the range is not valid.
    """
    check_range(low, high)
    shifts = 0
    while low < high:
        low >>= 1
        high >>= 1
        shifts += 1
    return low << shifts, shifts


def latched_by_looping(low: int, high: int) -> int:
    """The same value, ANDing every count. For checking, not for using.

    Args:
        low: The first count.
        high: The last count.

    Returns:
        The same answer, in time proportional to the size of the range rather
        than to the width of the register. On a range of the whole 16-bit space
        that is 65,536 operations against 16.

    Raises:
        ValueError: If the range is not valid.
    """
    check_range(low, high)
    latch = MASK
    for count in range(low, high + 1):
        latch &= count
    return latch


def common_prefix(low: int, high: int) -> str:
    """Return the shared opening bits of the two ends, as a string.

    Args:
        low: The first count.
        high: The last count.

    Returns:
        The bits the two ends agree on, from the top down, as "0"s and "1"s -
        empty when they differ at the very first bit. Printing this beside the
        answer is what turns the rule from a recipe into something visible.

    Raises:
        ValueError: If the range is not valid.
    """
    check_range(low, high)
    low_bits = f"{low:0{WIDTH}b}"
    high_bits = f"{high:0{WIDTH}b}"
    shared: list[str] = []
    for left, right in zip(low_bits, high_bits):
        if left != right:
            break
        shared.append(left)
    return "".join(shared)


# ---- Self-check ----
if __name__ == "__main__":
    print("RANGES, THEIR SHARED PREFIX, AND WHAT LATCHES")
    for low, high in RANGES:
        value, shifts = latched(low, high)
        prefix = common_prefix(low, high) or "(none)"
        print(f"    {low:>5} to {high:<5}  prefix {prefix:<16}  latched {value:>5}  ({shifts} shifts)")
    print()

    print("THE STRUCTURAL OBSERVATION, ON 5 TO 7")
    for count in range(5, 8):
        print(f"    {count}  {count:0{WIDTH}b}")
    print(f"    =  {latched(5, 7)[0]:0{WIDTH}b}")
    print()

    # 5, 6 and 7 are 101, 110, 111. They agree on the 4 and disagree below it.
    assert latched(5, 7)[0] == 4

    # A range of one count is that count.
    for count in (0, 12, MASK):
        assert latched(count, count)[0] == count
        assert latched(count, count)[1] == 0

    # A range that crosses zero-to-one latches nothing, because the lowest bit
    # flips inside it.
    assert latched(0, 1)[0] == 0

    # The whole register space latches nothing at all.
    assert latched(0, MASK)[0] == 0

    # The high nibble survives when only the low bits move.
    assert latched(0b1111_0000_0000_0000, 0b1111_0000_1111_1111)[0] == 0b1111_0000_0000_0000

    # The closed form and the loop agree on every range in the data.
    for low, high in RANGES:
        assert latched(low, high)[0] == latched_by_looping(low, high), (low, high)

    # ...and on a sweep of small ranges, which is where an off-by-one in the
    # shifting would show up.
    for low in range(0, 64):
        for high in range(low, min(low + 20, 64)):
            assert latched(low, high)[0] == latched_by_looping(low, high), (low, high)

    # The answer's low bits are exactly the ones the shifting cleared.
    for low, high in RANGES:
        value, shifts = latched(low, high)
        assert value & ((1 << shifts) - 1) == 0

    # The answer is never above the lower end, and never below zero.
    for low, high in RANGES:
        assert 0 <= latched(low, high)[0] <= low

    # The shared prefix and the number of shifts describe the same split.
    for low, high in RANGES:
        assert len(common_prefix(low, high)) == WIDTH - latched(low, high)[1]

    # A backwards or out-of-range pair is refused rather than looping forever.
    for bad_low, bad_high in ((7, 5), (-1, 5), (0, 1 << WIDTH)):
        try:
            latched(bad_low, bad_high)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad_low}, {bad_high}")

    print("All checks passed.")
