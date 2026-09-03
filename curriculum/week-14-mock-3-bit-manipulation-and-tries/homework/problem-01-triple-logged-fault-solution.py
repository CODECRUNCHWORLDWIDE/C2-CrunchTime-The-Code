"""problem-01-triple-logged-fault-solution.py - when the fold stops working.

A relay tester writes every fault code THREE times - once when the fault is
raised, once when it is confirmed, once when it is cleared. One code in this log
appears only once, because an engineer wrote it in by hand and the tester never
saw it.

Find it, in linear time and constant space.

The XOR fold from Exercise 1 does not work here and it is worth being clear
why: XOR cancels a code in PAIRS, so three copies leave one behind, and folding
the whole log leaves the XOR of every distinct code rather than the odd one out.

What does work is counting per BIT POSITION rather than per code. Every bit of a
tripled code contributes three to that position's total, and three is divisible
by three. So the positions whose totals are NOT divisible by three are exactly
the positions where the lone code has a bit, and reassembling those bits gives
the answer.

That generalises: for codes appearing k times, count per position and take the
total mod k. The XOR fold is the k = 2 case of the same idea, done faster.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

WIDTH = 16

# ---- Given data ----
# Every code three times except 0x0051, which was written once by hand.
FAULT_LOG: tuple[int, ...] = (
    0x00A3, 0x1F04, 0x00A3, 0x2B77, 0x1F04, 0x0051, 0x2B77,
    0x00A3, 0x1F04, 0x2B77,
)


# ---- Your task ----
def lone_fault(codes: tuple[int, ...], repeats: int = 3) -> int:
    """Return the code logged once when every other is logged `repeats` times.

    Args:
        codes: The fault log, in any order. Every code must fit in WIDTH bits.
        repeats: How many times a normal code appears. Must be at least 2.

    Returns:
        The code that appears once.

    Raises:
        ValueError: If `repeats` is below 2, if any code does not fit in WIDTH
            bits, or if the log does not hold exactly one code appearing a
            number of times not divisible by `repeats`.
    """
    if repeats < 2:
        raise ValueError("a normal code must be logged at least twice")
    for code in codes:
        if not 0 <= code < (1 << WIDTH):
            raise ValueError(f"{code} is not a {WIDTH}-bit fault code")

    lone = [code for code in set(codes) if codes.count(code) % repeats]
    if len(lone) != 1:
        raise ValueError(f"expected exactly one odd code, found {len(lone)}")

    answer = 0
    for position in range(WIDTH):
        total = sum(code >> position & 1 for code in codes)
        if total % repeats:
            answer |= 1 << position
    return answer


def position_totals(codes: tuple[int, ...]) -> list[int]:
    """Return how many codes have a bit at each position, lowest first.

    Args:
        codes: The fault log.

    Returns:
        A list of length WIDTH. Printing it beside the totals mod 3 is what
        makes the method visible: the positions that do not divide evenly are
        exactly the lone code's bits, and you can read the answer off the page.
    """
    return [sum(code >> position & 1 for code in codes) for position in range(WIDTH)]


def lone_fault_by_folding(codes: tuple[int, ...]) -> int:
    """The XOR fold, kept to be run and seen failing.

    Args:
        codes: The fault log.

    Returns:
        Whatever the fold produces, which on a tripled log is NOT the lone
        code. It is the XOR of every distinct code, because three copies of a
        code cancel down to one. Shipped so the failure is something you have
        watched rather than been told about.
    """
    folded = 0
    for code in codes:
        folded ^= code
    return folded


# ---- Self-check ----
if __name__ == "__main__":
    print("FAULT LOG")
    print("    " + "  ".join(f"0x{code:04X}" for code in FAULT_LOG))
    print()

    print("BITS PER POSITION, AND THE REMAINDER MOD 3")
    totals = position_totals(FAULT_LOG)
    for position in range(WIDTH - 1, -1, -1):
        mark = "  <- the lone code has a bit here" if totals[position] % 3 else ""
        print(f"    bit {position:>2}: {totals[position]:>2}   mod 3 = {totals[position] % 3}{mark}")
    print()

    answer = lone_fault(FAULT_LOG)
    folded = lone_fault_by_folding(FAULT_LOG)
    print(f"    counting per position: 0x{answer:04X}")
    print(f"    the XOR fold instead : 0x{folded:04X}   (not the answer)")
    print()

    # The hand-written code is 0x0051.
    assert lone_fault(FAULT_LOG) == 0x0051

    # The fold does NOT find it, and that is the point of shipping it.
    assert lone_fault_by_folding(FAULT_LOG) != 0x0051
    # ...specifically, it is the XOR of the distinct codes.
    distinct = 0
    for code in set(FAULT_LOG):
        distinct ^= code
    assert lone_fault_by_folding(FAULT_LOG) == distinct

    # Order does not matter.
    assert lone_fault(tuple(reversed(FAULT_LOG))) == 0x0051

    # The method is not special to three. Two is the XOR fold's case, and the
    # per-position count gets the same answer more slowly.
    assert lone_fault((7, 7, 3), repeats=2) == 3
    assert lone_fault((5, 5, 5, 5, 9), repeats=4) == 9

    # Zero can be the lone code, which a "non-zero means found" test misses.
    assert lone_fault((7, 7, 7, 0)) == 0

    # A log of one code is that code.
    assert lone_fault((0x2B,)) == 0x2B

    # A log where everything divides evenly has no answer, and so does one with
    # two odd codes - which would otherwise return a number that is neither.
    for bad in ((1, 1, 1, 2, 2, 2), (1, 2), ()):
        try:
            lone_fault(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad}")

    # A code too wide for the register is refused rather than silently truncated.
    try:
        lone_fault((1 << WIDTH, 1, 1, 1))
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for an over-wide code")

    # A repeat count below 2 is meaningless.
    try:
        lone_fault(FAULT_LOG, repeats=1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for repeats below 2")

    print("All checks passed.")
