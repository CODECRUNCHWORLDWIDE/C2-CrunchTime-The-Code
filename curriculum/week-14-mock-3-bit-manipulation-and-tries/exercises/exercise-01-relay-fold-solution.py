"""exercise-01-relay-fold-solution.py - the one relay that tripped alone.

A signal box logs a relay code every time a relay trips. Relays trip in pairs -
one going in, one going out - so a healthy log holds every code twice. This log
holds one code once.

Find it, in one pass and in constant space.

XOR is the whole answer, and it works because of three properties worth naming
out loud rather than taking on trust:

    a ^ a == 0        a code cancels itself
    a ^ 0 == a        zero leaves a code alone
    order does not matter, because XOR is associative and commutative

Fold the whole log with XOR and every paired code cancels itself out, whatever
order the pairs arrived in. What survives is the code that had no partner.

A counter dictionary answers the same question and is the answer to name and
reject: it is linear space where this is constant, and the whole reason this
problem is asked is that constant space is possible.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
# Relay codes as logged, in the order they tripped.
TRIP_LOG: tuple[int, ...] = (0x2B, 0x14, 0x2B, 0x77, 0x14, 0x09, 0x77)


# ---- Your task ----
def lone_relay(codes: tuple[int, ...]) -> int:
    """Return the code that appears once when every other appears twice.

    Args:
        codes: The trip log, in any order.

    Returns:
        The unpaired code.

    Raises:
        ValueError: If the log does not hold exactly one unpaired code. The
            fold alone cannot tell that apart - a log with three unpaired codes
            also folds to something non-zero - so the count is checked as well,
            and that check is part of the contract rather than an extra.
    """
    folded = 0
    for code in codes:
        folded ^= code

    lone = [code for code in set(codes) if codes.count(code) % 2 == 1]
    if len(lone) != 1:
        raise ValueError(f"expected exactly one unpaired code, found {len(lone)}")
    return folded


def fold_trail(codes: tuple[int, ...]) -> list[int]:
    """Return the running fold after each code, for reading.

    Args:
        codes: The trip log.

    Returns:
        One value per code: the XOR of everything up to and including it.
        Printing this is what makes the cancellation visible - the running
        value returns to a previous number the moment a pair completes.
    """
    trail: list[int] = []
    folded = 0
    for code in codes:
        folded ^= code
        trail.append(folded)
    return trail


def lone_relay_by_counting(codes: tuple[int, ...]) -> int:
    """The counter version, kept to be compared rather than used.

    Args:
        codes: The trip log.

    Returns:
        The same answer for linear space. This is the alternative to name and
        reject in the write-up, and it is worth writing once so the rejection
        is informed.

    Raises:
        ValueError: On the same logs as `lone_relay`.
    """
    counts: dict[int, int] = {}
    for code in codes:
        counts[code] = counts.get(code, 0) + 1
    lone = [code for code, count in counts.items() if count % 2 == 1]
    if len(lone) != 1:
        raise ValueError(f"expected exactly one unpaired code, found {len(lone)}")
    return lone[0]


# ---- Self-check ----
if __name__ == "__main__":
    print("TRIP LOG AND THE RUNNING FOLD")
    for code, folded in zip(TRIP_LOG, fold_trail(TRIP_LOG)):
        print(f"    0x{code:02X}   running fold 0x{folded:02X}")
    print()

    print(f"    the lone relay: 0x{lone_relay(TRIP_LOG):02X}")
    print()

    # 0x09 is the code with no partner.
    assert lone_relay(TRIP_LOG) == 0x09

    # The two versions agree, and the write-up should say why one is preferred.
    assert lone_relay(TRIP_LOG) == lone_relay_by_counting(TRIP_LOG)

    # Order genuinely does not matter, which is what "commutative" buys.
    assert lone_relay(tuple(reversed(TRIP_LOG))) == 0x09
    assert lone_relay((0x09, 0x2B, 0x2B, 0x14, 0x14, 0x77, 0x77)) == 0x09

    # A log of one code is that code.
    assert lone_relay((5,)) == 5

    # Zero can be the lone code, which is the case a "fold to non-zero" test
    # would get wrong.
    assert lone_relay((7, 7, 0)) == 0

    # The running fold returns to a previous value when a pair completes: after
    # 0x2B, 0x14, 0x2B the fold is back to 0x14 alone.
    assert fold_trail((0x2B, 0x14, 0x2B))[-1] == 0x14

    # A log where every code is paired folds to zero and has no answer. So does
    # one with three unpaired codes, which folds to something non-zero and
    # would fool a solution that only checked the fold.
    for bad in ((1, 1, 2, 2), (1, 2, 3), ()):
        for function in (lone_relay, lone_relay_by_counting):
            try:
                function(bad)
            except ValueError:
                pass
            else:
                raise AssertionError(f"expected ValueError from {function.__name__} for {bad}")

    print("All checks passed.")
