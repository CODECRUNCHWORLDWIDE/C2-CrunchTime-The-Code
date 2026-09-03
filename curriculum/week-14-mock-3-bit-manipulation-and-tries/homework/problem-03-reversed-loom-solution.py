"""problem-03-reversed-loom-solution.py - a cable loom wired back to front.

A sensor board is wired to a display through a ribbon loom, and the loom was
made up back to front: the sensor's lowest line reaches the display's highest
lamp, and so on all the way down. Every reading arrives with its bits reversed.

Reverse them back.

Two ways, and both are worth writing:

    the walk         take the bits off the bottom of the reading and push them
                     onto the bottom of the answer, WIDTH times. The answer
                     grows upwards while the reading shrinks downwards, which
                     is what performs the reversal.

    the fold         swap halves, then quarters, then eighths, down to single
                     bits. Four masked steps for a 16-bit register instead of
                     sixteen, and it is the one worth being able to explain
                     rather than the one worth writing first.

The walk is the answer to give at a panel. The fold is the answer to mention.

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
READINGS: tuple[int, ...] = (
    0b0000_0000_0000_0001,
    0b1000_0000_0000_0000,
    0b0000_0000_1111_1111,
    0b1010_1010_1010_1010,
    0b1100_0000_0000_0011,
    0b0000_0000_0000_0000,
    0b1111_1111_1111_1111,
)


# ---- Your task ----
def check_reading(value: int) -> None:
    """Raise unless `value` fits in WIDTH bits.

    Args:
        value: The reading as it arrived.

    Raises:
        ValueError: If the value is negative or too wide.
    """
    if not 0 <= value <= MASK:
        raise ValueError(f"{value} is not a {WIDTH}-bit reading")


def unloom(value: int) -> int:
    """Return `value` with its bits reversed, by walking them.

    Args:
        value: The reading as it arrived through the loom.

    Returns:
        The reading as the sensor sent it.

    Raises:
        ValueError: If the value does not fit in WIDTH bits.
    """
    check_reading(value)
    answer = 0
    for _ in range(WIDTH):
        # Push the answer up to make room, then take the reading's lowest bit.
        answer = (answer << 1) | (value & 1)
        value >>= 1
    return answer


def unloom_by_folding(value: int) -> int:
    """Return `value` with its bits reversed, by swapping halves repeatedly.

    Swaps the two halves of the register, then the halves of each half, and so
    on down to single bits. Four steps for 16 bits, and the same four lines
    would be five for 32.

    Args:
        value: The reading as it arrived.

    Returns:
        The reading as the sensor sent it.

    Raises:
        ValueError: If the value does not fit in WIDTH bits.
    """
    check_reading(value)
    # Swap 8-bit halves, then 4-bit, then 2-bit, then single bits.
    value = ((value & 0x00FF) << 8) | ((value & 0xFF00) >> 8)
    value = ((value & 0x0F0F) << 4) | ((value & 0xF0F0) >> 4)
    value = ((value & 0x3333) << 2) | ((value & 0xCCCC) >> 2)
    value = ((value & 0x5555) << 1) | ((value & 0xAAAA) >> 1)
    return value & MASK


def unloom_steps(value: int) -> list[str]:
    """Return the folding version's register after each swap, for reading.

    Args:
        value: The reading as it arrived.

    Returns:
        Five binary strings: the reading, then the register after each of the
        four swaps. Printing them is what makes the method make sense - the
        halves visibly change places, then the quarters, and so on.

    Raises:
        ValueError: If the value does not fit in WIDTH bits.
    """
    check_reading(value)
    steps = [f"{value:0{WIDTH}b}"]
    for keep, shift in ((0x00FF, 8), (0x0F0F, 4), (0x3333, 2), (0x5555, 1)):
        drop = (~keep) & MASK
        value = ((value & keep) << shift) | ((value & drop) >> shift)
        steps.append(f"{value:0{WIDTH}b}")
    return steps


def symmetric(value: int) -> bool:
    """Say whether a reading is unchanged by the loom.

    Args:
        value: The reading.

    Returns:
        True when the reading reads the same both ways, so the miswired loom
        makes no difference to it. Those readings are exactly the ones that
        would hide the fault, which is why the electrician wants them named.

    Raises:
        ValueError: If the value does not fit in WIDTH bits.
    """
    return unloom(value) == value


# ---- Self-check ----
if __name__ == "__main__":
    print("READINGS THROUGH THE LOOM")
    print("    as received        as sent            same?")
    for value in READINGS:
        print(f"    {value:0{WIDTH}b}   {unloom(value):0{WIDTH}b}   {symmetric(value)}")
    print()

    print("THE FOLDING VERSION, STEP BY STEP")
    print("    starting from 1100000000000011")
    for step in unloom_steps(0b1100_0000_0000_0011):
        print(f"    {step}")
    print()

    # The lowest bit becomes the highest and back again.
    assert unloom(0b0000_0000_0000_0001) == 0b1000_0000_0000_0000
    assert unloom(0b1000_0000_0000_0000) == 0b0000_0000_0000_0001

    # A byte of ones moves from the bottom to the top.
    assert unloom(0b0000_0000_1111_1111) == 0b1111_1111_0000_0000

    # An alternating pattern shifts by one, which is a good hand check.
    assert unloom(0b1010_1010_1010_1010) == 0b0101_0101_0101_0101

    # The two methods agree on every reading in the data...
    for value in READINGS:
        assert unloom(value) == unloom_by_folding(value)

    # ...and on a wide sweep of the whole register range, which is the check
    # that matters: bit tricks are exactly the code that passes six hand-picked
    # examples and fails a seventh.
    for value in range(0, 1 << WIDTH, 97):
        assert unloom(value) == unloom_by_folding(value)

    # Reversing twice gives back the original, always. That is the strongest
    # property this function has and it needs no known-good answer to check.
    for value in range(0, 1 << WIDTH, 89):
        assert unloom(unloom(value)) == value

    # All zeroes and all ones are unchanged, and so is any palindrome.
    assert unloom(0) == 0
    assert unloom(MASK) == MASK
    assert symmetric(0) and symmetric(MASK)
    assert symmetric(0b1100_0000_0000_0011)
    assert not symmetric(0b0000_0000_0000_0001)

    # The folding version really does swap halves first: after one step the
    # two bytes have changed places and nothing else has moved.
    steps = unloom_steps(0b1111_1111_0000_0000)
    assert steps[1] == "0000000011111111"

    # Out-of-range readings are refused, negatives included.
    for bad in (1 << WIDTH, -1):
        for function in (unloom, unloom_by_folding, unloom_steps):
            try:
                function(bad)
            except ValueError:
                pass
            else:
                raise AssertionError(f"expected ValueError from {function.__name__}")

    print("All checks passed.")
