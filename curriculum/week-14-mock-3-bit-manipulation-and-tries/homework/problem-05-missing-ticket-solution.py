"""problem-05-missing-ticket-solution.py - the one ticket that never came back.

A cloakroom issues tickets numbered 0 to n. At the end of the night every
ticket but one has been handed back. Find the missing number.

Two answers, and the second is better than the first for a reason worth saying
out loud rather than guessing at.

    the sum          add 0 to n with the closed form, subtract what came back.
                     One line, and it builds a number as large as the whole
                     range - which on a fixed-width register can overflow, in a
                     language that has fixed-width registers.

    the fold         XOR every returned ticket AND every number from 0 to n
                     together. Each number that came back cancels itself
                     against its own position in the range, and what survives
                     is the one that had nothing to cancel against.

Python's integers do not overflow, so here both are safe and the sum is simpler.
The fold is the answer that stays safe when the register is 32 bits wide, and
being able to say WHICH constraint makes the difference is the thing being
drilled. "Use XOR because it is clever" is not the answer.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
# Tickets 0 to 9 were issued. These came back.
RETURNED: tuple[int, ...] = (3, 0, 1, 9, 2, 5, 8, 7, 6)


# ---- Your task ----
def check_returns(returned: tuple[int, ...]) -> int:
    """Raise unless `returned` is a valid set of returns, and give the range.

    Args:
        returned: The tickets handed back, in any order.

    Returns:
        The highest ticket issued - which is len(returned), because exactly one
        of 0 to n is missing and n of them came back.

    Raises:
        ValueError: If a ticket is outside 0 to n, or if the same ticket came
            back twice. Both would make the answer meaningless, and neither is
            detected by the arithmetic itself.
    """
    highest = len(returned)
    for ticket in returned:
        if not 0 <= ticket <= highest:
            raise ValueError(f"ticket {ticket} was never issued")
    if len(set(returned)) != len(returned):
        raise ValueError("the same ticket came back twice")
    return highest


def missing_by_folding(returned: tuple[int, ...]) -> int:
    """Return the missing ticket, by XOR.

    Args:
        returned: The tickets handed back, in any order.

    Returns:
        The one number from 0 to n that did not come back.

    Raises:
        ValueError: If the returns are not valid.
    """
    highest = check_returns(returned)
    folded = 0
    for number in range(highest + 1):
        folded ^= number
    for ticket in returned:
        folded ^= ticket
    return folded


def missing_by_summing(returned: tuple[int, ...]) -> int:
    """Return the missing ticket, by arithmetic. Kept to be compared.

    Args:
        returned: The tickets handed back, in any order.

    Returns:
        The same answer. The sum of 0 to n is n * (n + 1) // 2, and what is
        left after subtracting the returns is the missing ticket.

    Raises:
        ValueError: If the returns are not valid.
    """
    highest = check_returns(returned)
    return highest * (highest + 1) // 2 - sum(returned)


def fold_trail(returned: tuple[int, ...]) -> list[int]:
    """Return the running fold, range first then returns, for reading.

    Args:
        returned: The tickets handed back.

    Returns:
        The value after each XOR. The first half folds the whole range down to
        something, and the second half cancels it away ticket by ticket until
        only the missing one is left.

    Raises:
        ValueError: If the returns are not valid.
    """
    highest = check_returns(returned)
    trail: list[int] = []
    folded = 0
    for number in range(highest + 1):
        folded ^= number
        trail.append(folded)
    for ticket in returned:
        folded ^= ticket
        trail.append(folded)
    return trail


# ---- Self-check ----
if __name__ == "__main__":
    highest = check_returns(RETURNED)
    print(f"TICKETS 0 TO {highest} WERE ISSUED")
    print(f"    came back : {sorted(RETURNED)}")
    print(f"    missing   : {missing_by_folding(RETURNED)}")
    print()

    print("THE RUNNING FOLD")
    trail = fold_trail(RETURNED)
    print("    folding the range 0 to " + str(highest) + ":")
    print("      " + "  ".join(str(value) for value in trail[: highest + 1]))
    print("    then cancelling the returns:")
    print("      " + "  ".join(str(value) for value in trail[highest + 1 :]))
    print()

    # Ticket 4 never came back.
    assert missing_by_folding(RETURNED) == 4

    # The two methods agree here...
    assert missing_by_folding(RETURNED) == missing_by_summing(RETURNED)

    # ...and on every possible single omission from a range of 0 to 30, which
    # is the check that matters: an off-by-one in the range bound shows up on
    # exactly one of these and on none of a handful of hand-picked cases.
    for size in range(1, 31):
        for missing in range(size + 1):
            returns = tuple(number for number in range(size + 1) if number != missing)
            assert missing_by_folding(returns) == missing, (size, missing)
            assert missing_by_summing(returns) == missing, (size, missing)

    # Order does not matter to either method.
    assert missing_by_folding(tuple(reversed(RETURNED))) == 4

    # The smallest case: one ticket issued, none returned. The missing one is 0.
    assert missing_by_folding(()) == 0
    assert missing_by_summing(()) == 0

    # The missing ticket can be either end of the range, which is where a loop
    # bounded at `len(returned)` rather than `len(returned) + 1` goes wrong.
    assert missing_by_folding((1, 2, 3)) == 0
    assert missing_by_folding((0, 1, 2)) == 3

    # A ticket that was never issued, or one returned twice, is refused. The
    # arithmetic would otherwise produce a confident number that means nothing.
    for bad in ((0, 1, 99), (0, 1, 1), (0, -1, 2)):
        for function in (missing_by_folding, missing_by_summing):
            try:
                function(bad)
            except ValueError:
                pass
            else:
                raise AssertionError(f"expected ValueError from {function.__name__} for {bad}")

    print("All checks passed.")
