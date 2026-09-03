"""problem-06-paired-ribbon-swap-solution.py - a ribbon crimped in the wrong pairs.

A ribbon cable carries a 16-bit register. It was crimped with each PAIR of
lines swapped: line 0 and line 1 have changed places, and so have 2 and 3, and
so on all the way up. The register arrives with every adjacent pair the wrong
way round.

Put them back.

The whole answer is two masks and two shifts, done at once:

    take the even lines, shift them up one
    take the odd lines, shift them down one
    OR the two together

    0x5555 is 0101...0101, which keeps the even lines
    0xAAAA is 1010...1010, which keeps the odd lines

Doing it as a loop over pairs is correct and is the answer to write first. The
masked version is the answer to be able to explain: it does every pair at once,
in constant time regardless of the register width, and it is the same shape as
the folding reversal in Problem 3 - which is not a coincidence and is worth a
sentence.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

WIDTH = 16
MASK = (1 << WIDTH) - 1
EVEN_LINES = 0x5555      # 0101 0101 0101 0101
ODD_LINES = 0xAAAA       # 1010 1010 1010 1010

# ---- Given data ----
REGISTERS: tuple[int, ...] = (
    0b0000_0000_0000_0001,
    0b0000_0000_0000_0010,
    0b1010_1010_1010_1010,
    0b0101_0101_0101_0101,
    0b1100_1100_1100_1100,
    0b0000_0000_0000_0000,
    0b1111_1111_1111_1111,
)


# ---- Your task ----
def check_register(value: int) -> None:
    """Raise unless `value` fits in WIDTH bits.

    Args:
        value: The register as it arrived.

    Raises:
        ValueError: If the value is negative or too wide.
    """
    if not 0 <= value <= MASK:
        raise ValueError(f"{value} is not a {WIDTH}-bit register")


def uncrimp(value: int) -> int:
    """Return `value` with every adjacent pair of lines swapped back.

    Args:
        value: The register as it arrived through the ribbon.

    Returns:
        The register as it was sent.

    Raises:
        ValueError: If the value does not fit in WIDTH bits.
    """
    check_register(value)
    return (((value & EVEN_LINES) << 1) | ((value & ODD_LINES) >> 1)) & MASK


def uncrimp_by_looping(value: int) -> int:
    """The same swap, one pair at a time. For comparison.

    Args:
        value: The register as it arrived.

    Returns:
        The same answer, in WIDTH / 2 turns rather than in one expression. This
        is the version to write first and the one to check the masked version
        against.

    Raises:
        ValueError: If the value does not fit in WIDTH bits.
    """
    check_register(value)
    answer = 0
    for position in range(0, WIDTH, 2):
        low = value >> position & 1
        high = value >> (position + 1) & 1
        answer |= high << position
        answer |= low << (position + 1)
    return answer


def crossed_pairs(value: int) -> list[int]:
    """Return the pair positions where the two lines differ.

    Args:
        value: The register as it arrived.

    Returns:
        The lowest line number of each pair whose two lines carry different
        values - which are exactly the pairs the miscrimp actually changes.
        A pair carrying 00 or 11 comes through the wrong crimp unharmed, and
        those are the readings that hide the fault.

    Raises:
        ValueError: If the value does not fit in WIDTH bits.
    """
    check_register(value)
    differing = value ^ uncrimp(value)
    return [position for position in range(0, WIDTH, 2) if differing >> position & 3]


def unharmed(value: int) -> bool:
    """Say whether the miscrimp leaves a register unchanged.

    Args:
        value: The register.

    Returns:
        True when every pair carries the same value on both lines, so the swap
        makes no difference. These are the readings an electrician must not
        test with.

    Raises:
        ValueError: If the value does not fit in WIDTH bits.
    """
    return uncrimp(value) == value


# ---- Self-check ----
if __name__ == "__main__":
    print("REGISTERS THROUGH THE MISCRIMPED RIBBON")
    print("    as received        as sent            crossed pairs")
    for value in REGISTERS:
        pairs = crossed_pairs(value)
        shown = ", ".join(str(pair) for pair in pairs) if pairs else "(none)"
        print(f"    {value:0{WIDTH}b}   {uncrimp(value):0{WIDTH}b}   {shown}")
    print()

    print("THE TWO MASKS")
    print(f"    even lines  0x{EVEN_LINES:04X}  {EVEN_LINES:0{WIDTH}b}")
    print(f"    odd lines   0x{ODD_LINES:04X}  {ODD_LINES:0{WIDTH}b}")
    print(f"    together    0x{EVEN_LINES | ODD_LINES:04X}  {EVEN_LINES | ODD_LINES:0{WIDTH}b}")
    print()

    # The lowest line moves up one and back.
    assert uncrimp(0b01) == 0b10
    assert uncrimp(0b10) == 0b01

    # Alternating patterns invert completely, because every pair is crossed.
    assert uncrimp(0b1010_1010_1010_1010) == 0b0101_0101_0101_0101
    assert uncrimp(0b0101_0101_0101_0101) == 0b1010_1010_1010_1010

    # A pattern in pairs is unharmed, because both lines of each pair agree.
    assert uncrimp(0b1100_1100_1100_1100) == 0b1100_1100_1100_1100
    assert unharmed(0b1100_1100_1100_1100)

    # All zeroes and all ones are unharmed too, which is exactly why they are
    # the worst readings to test a ribbon with.
    assert unharmed(0) and unharmed(MASK)
    assert crossed_pairs(0) == [] and crossed_pairs(MASK) == []

    # The two masks are complements and together cover the whole register.
    assert EVEN_LINES & ODD_LINES == 0
    assert EVEN_LINES | ODD_LINES == MASK

    # The masked and looping versions agree on every register in the data...
    for value in REGISTERS:
        assert uncrimp(value) == uncrimp_by_looping(value)

    # ...and across a sweep of the whole range, which is where a mask written
    # the wrong way round would show up.
    for value in range(0, 1 << WIDTH, 97):
        assert uncrimp(value) == uncrimp_by_looping(value)

    # Swapping twice gives back the original, always. This property needs no
    # known-good answer, which makes it the strongest check available.
    for value in range(0, 1 << WIDTH, 89):
        assert uncrimp(uncrimp(value)) == value

    # The swap never changes how many lines are live - it moves them.
    for value in range(0, 1 << WIDTH, 89):
        assert bin(uncrimp(value)).count("1") == bin(value).count("1")

    # Every crossed pair really does differ across its two lines.
    for value in REGISTERS:
        for pair in crossed_pairs(value):
            assert (value >> pair & 1) != (value >> (pair + 1) & 1)

    # Out-of-range registers are refused, negatives included.
    for bad in (1 << WIDTH, -1):
        for function in (uncrimp, uncrimp_by_looping, crossed_pairs):
            try:
                function(bad)
            except ValueError:
                pass
            else:
                raise AssertionError(f"expected ValueError from {function.__name__}")

    print("All checks passed.")
