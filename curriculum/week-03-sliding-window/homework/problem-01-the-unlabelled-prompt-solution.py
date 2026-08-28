"""problem-01-the-unlabelled-prompt-solution.py — the busiest half hour.

The customer asked one sentence: "which half hour was busiest on the ramp, and
how full were we on average during it?" Everything else — what a half hour is,
what to return, what happens on a tie, what happens on a short log, how the
average is rounded — was never said. The page lists the five questions and the
answers this file was written against.

The algorithm is a fixed-size window with a running total. The teaching is in
the contract, not the loop: the tie-break here is the opposite of the one in
Exercise 1, on purpose.

The self-checks are the starter's, unchanged. When they all pass the file
prints "All checks passed."
"""


def busiest_half_hour(boarded: list[int], slots: int = 6) -> tuple[int, int, float] | None:
    """Return the busiest window of consecutive five-minute slots.

    Args:
        boarded: Cars that boarded in each five-minute slot, in time order.
        slots: How many slots make a window. Six five-minute slots is the
            half hour the customer meant.

    Returns:
        (start_slot, cars, average) for the busiest window: its first slot,
        its total, and its cars-per-slot average rounded to one decimal
        place. Ties go to the earliest start. None when the log holds fewer
        than `slots` slots.
    """
    if slots > len(boarded):
        return None

    window_total = sum(boarded[:slots])
    best_total = window_total
    best_start = 0

    for right in range(slots, len(boarded)):
        window_total += boarded[right] - boarded[right - slots]
        # Strict >, because the customer wanted the earliest busiest window.
        if window_total > best_total:
            best_total = window_total
            best_start = right - slots + 1

    return (best_start, best_total, round(best_total / slots, 1))


# ---- Self-check ----
if __name__ == "__main__":
    ramp = [3, 0, 5, 2, 8, 1, 0, 9, 4, 2, 1, 6]
    windows = [sum(ramp[i : i + 6]) for i in range(len(ramp) - 5)]
    print(f"ramp log {ramp}")
    print(f"  half-hour totals by start slot : {windows}")
    print(f"  busiest half hour              : {busiest_half_hour(ramp)}")
    print()

    print(f"flat log, so the tie goes early : {busiest_half_hour([2, 2, 2, 2, 2, 2, 2])}")
    print(f"a quiet night is still an answer: {busiest_half_hour([0, 0, 0, 0, 0, 0])}")
    print(f"one-slot windows                : {busiest_half_hour([4, 9, 9, 1], slots=1)}")
    print(f"log shorter than one window     : {busiest_half_hour([1, 2, 3])}")
    print()

    assert busiest_half_hour(ramp) == (2, 25, 4.2)
    assert busiest_half_hour([2, 2, 2, 2, 2, 2, 2]) == (0, 12, 2.0)
    assert busiest_half_hour([0, 0, 0, 0, 0, 0]) == (0, 0, 0.0)
    assert busiest_half_hour([4, 9, 9, 1], slots=1) == (1, 9, 9.0)
    assert busiest_half_hour([1, 2, 3]) is None
    assert busiest_half_hour([]) is None

    # The window total really is the largest, and it really is the earliest.
    start, cars, average = busiest_half_hour(ramp)
    assert cars == max(windows)
    assert start == windows.index(max(windows))
    assert average == round(cars / 6, 1)

    print("All checks passed.")
