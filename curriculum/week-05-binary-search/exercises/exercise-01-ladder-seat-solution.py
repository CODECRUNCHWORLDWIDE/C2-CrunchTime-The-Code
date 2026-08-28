"""exercise-01-ladder-seat-solution.py - the chess ladder seat lookup.

One binary search over a strictly DESCENDING list of ratings. The descending
order is the whole twist: the two shrink rules swap sides compared with the
ascending template in the lecture.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
LADDER: list[int] = [2410, 2205, 2199, 1870, 1602, 1044]


# ---- Your task ----
def find_ladder_seat(ratings: list[int], rating: int) -> int | None:
    """Return the seat index holding `rating`, or None when no seat does.

    Args:
        ratings: Seat ratings, sorted strictly descending. Never modified.
        rating: The rating to look up.

    Returns:
        The index i with ratings[i] == rating, or None on a miss.
    """
    lo, hi = 0, len(ratings) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if ratings[mid] == rating:
            return mid
        if ratings[mid] > rating:
            lo = mid + 1  # midpoint is stronger, so the target sits lower down
        else:
            hi = mid - 1  # midpoint is weaker, so the target sits higher up
    return None


# ---- Self-check ----
if __name__ == "__main__":
    for wanted in (1870, 2200, 2410, 1044):
        print(f"rating {wanted:5d} -> seat {find_ladder_seat(LADDER, wanted)}")

    assert find_ladder_seat(LADDER, 1870) == 3
    assert find_ladder_seat(LADDER, 2200) is None
    assert find_ladder_seat(LADDER, 2410) == 0
    assert find_ladder_seat(LADDER, 1044) == 5
    assert find_ladder_seat([900, 12, -85], -85) == 2
    assert find_ladder_seat([1500], 1500) == 0
    assert find_ladder_seat([1500], 1499) is None
    assert find_ladder_seat([], 1500) is None
    assert LADDER[0] == 2410  # the ladder was never rearranged
    print("All checks passed.")
