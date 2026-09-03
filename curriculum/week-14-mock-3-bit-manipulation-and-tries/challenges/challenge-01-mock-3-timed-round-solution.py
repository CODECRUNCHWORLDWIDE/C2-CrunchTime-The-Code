"""challenge-01-mock-3-timed-round-solution.py - the fallback problem, worked.

Mock #3 is a timed round, not a problem. This file is the FALLBACK the page
offers for solo mode: something genuinely unseen to work under the clock, and
the reference answer to read only afterwards.

The fault register pair. A machine writes a 16-bit fault register every cycle.
Maintenance wants the two cycles whose registers disagree in the MOST bit
positions, because that pair brackets the widest change in machine state and is
where the fault is worth looking for.

Note what is being maximised: the NUMBER of differing bits, not the value of
the difference. Those are different questions and they have different answers -
0b1000 and 0b0000 differ by 8 in value and by one bit; 0b0111 and 0b0000 differ
by 7 in value and by three bits. A candidate who maximises the XOR value has
answered a different question, and under a clock they will not notice.

  bit_spread     - the widest disagreement, and the pair that produces it
  spread_report  - the pair, with the registers drawn in binary

The obvious answer is every pair, which is fine at this size and is the one to
say out loud first. The write-up is expected to name what it would cost at a
million cycles and what it would reach for then.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

WIDTH = 16

# ---- Given data ----
# One fault register per cycle, in cycle order.
# Chosen so that the two questions have DIFFERENT answers: cycles 0 and 3
# produce the largest XOR value and disagree in only two bits, while cycles 0
# and 2 disagree in thirteen. A candidate maximising the wrong one gets a
# plausible pair and the wrong answer.
REGISTERS: tuple[int, ...] = (
    0b1000_0000_0000_0000,
    0b0000_0000_0000_0001,
    0b0000_1111_1111_1111,
    0b0001_0000_0000_0000,
)


def differing_bits(left: int, right: int) -> int:
    """How many bit positions the two registers disagree in.

    XOR marks every disagreeing position with a 1, so the answer is how many
    1 bits the XOR has. int.bit_count does that in one call; the loop it
    replaces is the thing worth being able to write from memory.

    Args:
        left: One register.
        right: The other.

    Returns:
        A count between 0 and WIDTH.
    """
    return (left ^ right).bit_count()


def bit_spread(registers: tuple[int, ...]) -> tuple[int, tuple[int, int]] | None:
    """The pair of cycles disagreeing in the most bit positions.

    Args:
        registers: One register per cycle, in cycle order.

    Returns:
        (bits, (earlier cycle, later cycle)), or None when there are fewer than
        two cycles to compare. Ties are settled by the earlier first cycle, then
        the earlier second - so the answer is one pair rather than a family.

    Raises:
        ValueError: If a register does not fit in WIDTH bits.
    """
    for index, value in enumerate(registers):
        if not 0 <= value < (1 << WIDTH):
            raise ValueError(f"cycle {index} holds {value}, which is not a {WIDTH}-bit register")

    if len(registers) < 2:
        return None

    best_bits = -1
    best_pair = (0, 0)
    for i in range(len(registers)):
        for j in range(i + 1, len(registers)):
            bits = differing_bits(registers[i], registers[j])
            # Strictly greater, so the first pair found at a given width wins.
            # Cycles are visited in order, so that is the earliest pair.
            if bits > best_bits:
                best_bits, best_pair = bits, (i, j)
    return best_bits, best_pair


def spread_report(registers: tuple[int, ...]) -> None:
    """Print every register, then the widest-disagreeing pair."""
    for index, value in enumerate(registers):
        print(f"    cycle {index}  {value:0{WIDTH}b}")
    found = bit_spread(registers)
    if found is None:
        print("    not enough cycles to compare")
        return
    bits, (i, j) = found
    print()
    print(f"    widest: cycles {i} and {j}, disagreeing in {bits} of {WIDTH} bits")
    print(f"            {registers[i]:0{WIDTH}b}")
    print(f"            {registers[j]:0{WIDTH}b}")
    print(f"        xor {registers[i] ^ registers[j]:0{WIDTH}b}")


# ---- Self-check ----
if __name__ == "__main__":
    print("fault registers")
    spread_report(REGISTERS)

    bits, pair = bit_spread(REGISTERS)

    # The reported count must be the count for the reported pair, and no pair
    # may beat it. Those two assertions together are the definition.
    assert differing_bits(REGISTERS[pair[0]], REGISTERS[pair[1]]) == bits
    for i in range(len(REGISTERS)):
        for j in range(i + 1, len(REGISTERS)):
            assert differing_bits(REGISTERS[i], REGISTERS[j]) <= bits

    # The trap this problem is built around: maximising the XOR VALUE picks a
    # different pair from maximising the number of differing BITS.
    spread = [(differing_bits(REGISTERS[i], REGISTERS[j]), REGISTERS[i] ^ REGISTERS[j], (i, j))
              for i in range(len(REGISTERS)) for j in range(i + 1, len(REGISTERS))]
    by_bits = max(spread, key=lambda row: (row[0], -row[2][0], -row[2][1]))
    by_value = max(spread, key=lambda row: row[1])
    assert by_bits[2] != by_value[2], "the data must distinguish the two questions"

    # Small and degenerate cases.
    assert bit_spread(()) is None
    assert bit_spread((5,)) is None
    assert bit_spread((0, 0)) == (0, (0, 1))
    assert bit_spread((0, 0xFFFF)) == (16, (0, 1))

    # The tie-break: two pairs at the same width, earliest wins.
    assert bit_spread((0b0001, 0b0010, 0b0100))[1] == (0, 1)

    # Registers are checked rather than silently truncated.
    for bad in ((1 << WIDTH,), (-1,)):
        try:
            bit_spread(bad + (0,))
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad!r}")

    print()
    print("All checks passed.")
