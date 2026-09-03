"""problem-03-gauge-drift-run-solution.py - the worst drift a gauge ever ran up.

A tide gauge is checked every day and the check writes down a drift factor: the
number the day's readings have to be multiplied by to correct them. A factor of
1 means the gauge was right. Above 1 it read low, below 1 it read high, and a
NEGATIVE factor means the float was stuck upside down and the day's readings
came out inverted.

The calibration office wants the worst stretch: the run of consecutive days
whose factors multiply to the largest number, because that is the stretch where
the uncorrected record is most wrong.

Factors here are whole numbers, so the arithmetic stays exact.

The trap is the negatives. A running product that is badly negative is one more
negative day away from being the best product in the record - so tracking the
best run so far is not enough. Both the best AND the worst have to be carried,
and on a negative day they swap.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
# A fortnight of drift factors. Day 5 is the stuck float.
DRIFT: tuple[int, ...] = (2, 3, -2, 4, -1, 2, 2, -3, 1, 2)


# ---- Your task ----
def worst_drift(factors: tuple[int, ...]) -> int:
    """Return the largest product of any run of consecutive days.

    Args:
        factors: The daily drift factors, in order. Must not be empty.

    Returns:
        The largest product achievable by multiplying one or more consecutive
        factors together. A run of one day is allowed, so the answer is never
        worse than the best single factor.

    Raises:
        ValueError: If `factors` is empty.
    """
    if not factors:
        raise ValueError("a drift record needs at least one day")

    best = worst = answer = factors[0]
    for factor in factors[1:]:
        # A negative factor turns the best run into the worst and the worst
        # into the best, so both candidates have to be computed from the OLD
        # pair before either is written back.
        candidates = (factor, best * factor, worst * factor)
        best, worst = max(candidates), min(candidates)
        answer = max(answer, best)
    return answer


def worst_drift_run(factors: tuple[int, ...]) -> tuple[int, int, int]:
    """Return the largest product and the days it runs over.

    Args:
        factors: The daily drift factors, in order. Must not be empty.

    Returns:
        A triple: the product, the first day of the run and the last, both
        counted from 1 as the office numbers them. Ties go to the earliest run,
        then to the shortest, so the answer is one run rather than a family.

    Raises:
        ValueError: If `factors` is empty.
    """
    if not factors:
        raise ValueError("a drift record needs at least one day")

    # Kept honest by brute force over every run. The one-pass version above is
    # the answer to give; this is the one to check it against, and on a record
    # of a fortnight it costs nothing.
    best_product = factors[0]
    best_span = (1, 1)
    for start in range(len(factors)):
        running = 1
        for end in range(start, len(factors)):
            running *= factors[end]
            if running > best_product:
                best_product = running
                best_span = (start + 1, end + 1)
    return best_product, best_span[0], best_span[1]


def daily_best(factors: tuple[int, ...]) -> list[tuple[int, int]]:
    """Return the best and worst run ENDING on each day.

    Args:
        factors: The daily drift factors, in order. Must not be empty.

    Returns:
        One (best, worst) pair per day. Printing this is what makes the swap on
        a negative day visible: the two columns change places.

    Raises:
        ValueError: If `factors` is empty.
    """
    if not factors:
        raise ValueError("a drift record needs at least one day")
    rows = [(factors[0], factors[0])]
    best = worst = factors[0]
    for factor in factors[1:]:
        candidates = (factor, best * factor, worst * factor)
        best, worst = max(candidates), min(candidates)
        rows.append((best, worst))
    return rows


# ---- Self-check ----
if __name__ == "__main__":
    print("DRIFT RECORD")
    print("    day   factor   best run ending here   worst run ending here")
    for day, ((best, worst), factor) in enumerate(zip(daily_best(DRIFT), DRIFT), start=1):
        print(f"    {day:>3}   {factor:>6}   {best:>20}   {worst:>21}")
    print()

    product, first, last = worst_drift_run(DRIFT)
    print(f"    worst drift : {product}")
    print(f"    over days   : {first} to {last}")
    print()

    # The one-pass answer and the brute-force answer must agree. That is the
    # whole claim of the one-pass version.
    assert worst_drift(DRIFT) == worst_drift_run(DRIFT)[0]

    # A single day is a valid run, so a record of one day answers itself.
    assert worst_drift((7,)) == 7
    assert worst_drift((-7,)) == -7

    # One negative day in the middle: the answer is the better of the two
    # sides, not the whole record.
    assert worst_drift((2, 3, -1, 4)) == 6

    # TWO negative days: now the whole record is the answer, because the two
    # negatives cancel. This is the case a best-only tracker gets wrong.
    assert worst_drift((2, -3, -4, 1)) == 24

    # A zero cuts the record in two - nothing multiplies across it and lives.
    assert worst_drift((2, 3, 0, 5, 6)) == 30
    # ...and when every run through it is worse, zero itself is the answer.
    assert worst_drift((-2, 0, -3)) == 0

    # All negatives, odd count: the answer drops one end.
    assert worst_drift((-2, -3, -4)) == 12

    # The one-pass and brute-force answers agree on every prefix of the record,
    # not just the whole of it. Prefixes are where a swapped best and worst
    # first shows up.
    for length in range(1, len(DRIFT) + 1):
        prefix = DRIFT[:length]
        assert worst_drift(prefix) == worst_drift_run(prefix)[0], prefix

    # An empty record is refused rather than answered with 1.
    for function in (worst_drift, worst_drift_run, daily_best):
        try:
            function(())
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError from {function.__name__}")

    print("All checks passed.")
