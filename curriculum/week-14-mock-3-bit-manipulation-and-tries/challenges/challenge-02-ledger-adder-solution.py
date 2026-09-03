"""challenge-02-ledger-adder-solution.py - adding without an adder.

An old signal box totals its movement counts on a relay board. The board can
AND, OR, XOR and shift. It has no adder, because nobody built one - so addition
has to be assembled from the operations it does have.

XOR is addition that forgets to carry. AND finds exactly the columns that
should have carried. Shift the carries one place left and do it again. When
there is nothing left to carry, the XOR is the answer.

The engineer maintaining the board wants two things: the total, and how many
carry rounds it took, because a total that needs many rounds is a total the
board computes slowly and is worth knowing about.

  ledger_add    - the sum, and the number of carry rounds
  add_report    - a few pairs, with their rounds

Python's integers are unbounded and negative ones behave as though they have
infinitely many leading 1 bits, so the carry loop on a negative operand never
terminates. The board is 16-bit, so this masks to 16 bits and interprets the
result as signed - which is what the relays actually do, and is the part of the
problem that is really about how machines hold numbers.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

WIDTH = 16
MASK = (1 << WIDTH) - 1
SIGN_BIT = 1 << (WIDTH - 1)


def _to_signed(value: int) -> int:
    """Read a 16-bit pattern the way the board reads it: two's complement."""
    value &= MASK
    return value - (1 << WIDTH) if value & SIGN_BIT else value


def ledger_add(left: int, right: int) -> tuple[int, int]:
    """Add two counts using only bitwise operations.

    Args:
        left: One count, as the board holds it.
        right: The other count.

    Returns:
        (total, carry_rounds). The total is the 16-bit signed result, and
        carry_rounds is how many times the board had to fold carries back in.
        It is 0 only when the second count is zero and the loop never runs;
        adding anything at all costs at least one round, even when the two
        numbers share no bit positions and that round finds nothing to carry.

    Raises:
        ValueError: If either operand does not fit in 16 signed bits.
    """
    for name, value in (("left", left), ("right", right)):
        if not -SIGN_BIT <= value < SIGN_BIT:
            raise ValueError(f"{name}={value} does not fit in {WIDTH} signed bits")

    total = left & MASK
    carry = right & MASK
    rounds = 0
    while carry:
        # XOR is the sum of every column that does not carry; AND marks the
        # columns that do. Masking after the shift is what stops the carry
        # walking off the top of a board that only has 16 relays.
        total, carry = (total ^ carry) & MASK, ((total & carry) << 1) & MASK
        rounds += 1
    return _to_signed(total), rounds


def add_report(pairs: list[tuple[int, int]]) -> None:
    """Print the total and the carry rounds for each pair."""
    for left, right in pairs:
        total, rounds = ledger_add(left, right)
        check = "ok " if total == _to_signed(left + right) else "WRAP"
        print(f"    {left:>7} + {right:>7} = {total:>7}   rounds {rounds:>2}   {check}")


# ---- Self-check ----
if __name__ == "__main__":
    print("ledger additions")
    add_report([
        (0, 0),
        (5, 3),
        (255, 1),
        (1023, 1),
        (-1, 1),
        (-8, 3),
        (12345, -12345),
        (32767, 1),      # the top of the board: this one wraps, and says so
    ])

    # The arithmetic must match ordinary addition wherever the board can hold
    # the answer. That is the whole claim, so it is tested across a range
    # rather than on a handful of favourites.
    for left in range(-40, 41):
        for right in range(-40, 41):
            total, _ = ledger_add(left, right)
            assert total == left + right, (left, right, total)

    # Zero carries nothing.
    assert ledger_add(0, 0) == (0, 0)

    # Numbers sharing no bit positions still cost one round - the loop is
    # entered because the second count is non-zero, and that round finds
    # nothing to carry. 8 is 1000 and 5 is 0101, so the XOR alone is the answer.
    assert ledger_add(8, 5) == (13, 1)
    # Only a zero second count skips the loop entirely.
    assert ledger_add(13, 0) == (13, 0)

    # A long carry chain: 255 is eight 1 bits, and adding 1 folds through all
    # of them. The round count is the interesting output here, not the total.
    total, rounds = ledger_add(255, 1)
    assert total == 256
    assert rounds == 9

    # Negatives work because the board reads two's complement.
    assert ledger_add(-1, 1)[0] == 0
    assert ledger_add(-8, 3)[0] == -5
    assert ledger_add(12345, -12345)[0] == 0

    # The top of the board wraps rather than growing, which is what the relays
    # do. A solution that returns 32768 here is not modelling the hardware.
    assert ledger_add(32767, 1)[0] == -32768

    # Anything that does not fit is refused rather than silently truncated.
    for bad in (32768, -32769, 70000):
        try:
            ledger_add(bad, 0)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad}")

    print()
    print("All checks passed.")
