"""exercise-05-paving-reach-solution.py - the smallest nightly paving reach.

Binary search on the ANSWER. Nothing in the input is sorted and nothing is
being looked up; what gets bisected is the interval of reaches the crew
could rent, using "does this reach finish in time?" as the comparator.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
SECTIONS: list[int] = [30, 12, 21, 5, 18]


# ---- Your task ----
def nights_needed(sections: list[int], reach: int) -> int:
    """Return how many nights a train of this reach takes on these sections.

    Args:
        sections: Section lengths in metres.
        reach: The nightly reach in metres, at least 1.

    Returns:
        The sum of ceil(section / reach) over every section.
    """
    return sum((length + reach - 1) // reach for length in sections)


def min_nightly_reach(sections: list[int], nights: int) -> int | None:
    """Return the cheapest nightly reach that clears the road in time.

    Args:
        sections: Section lengths in metres, in any order.
        nights: How many nights the crew has before the road reopens.

    Returns:
        The smallest whole-metre reach that finishes within `nights`, 0 when
        there is nothing to pave, or None when no reach is fast enough.
    """
    if not sections:
        return 0
    if len(sections) > nights:
        return None  # one section per night means this can never be met

    lo, hi = 1, max(sections)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nights_needed(sections, mid) <= nights:
            hi = mid  # mid works, so the answer is mid or smaller
        else:
            lo = mid + 1  # mid is too slow, so the answer is bigger
    return lo


# ---- Self-check ----
if __name__ == "__main__":
    for budget in (6, 5, 4):
        answer = min_nightly_reach(SECTIONS, budget)
        if answer is None:
            print(f"{budget} nights -> no reach finishes in time")
        else:
            print(f"{budget} nights -> reach {answer}m, which uses {nights_needed(SECTIONS, answer)} nights")

    assert min_nightly_reach(SECTIONS, 6) == 21
    assert min_nightly_reach(SECTIONS, 5) == 30
    assert min_nightly_reach(SECTIONS, 4) is None
    assert min_nightly_reach([4, 4], 3) == 4
    assert min_nightly_reach([7], 3) == 3
    assert min_nightly_reach([9, 9, 9], 3) == 9
    assert min_nightly_reach([1_000_000_000], 1_000_000_000) == 1
    assert min_nightly_reach([], 0) == 0
    assert min_nightly_reach([12], 0) is None
    assert SECTIONS[0] == 30  # the section list was never rearranged
    print("All checks passed.")
