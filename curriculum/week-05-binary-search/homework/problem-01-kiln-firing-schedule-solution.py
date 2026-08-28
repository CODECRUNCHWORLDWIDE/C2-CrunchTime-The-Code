"""problem-01-kiln-firing-schedule-solution.py - the cheapest kiln to rent.

Binary search on the answer, over an answer space that is not the integers:
kilns are sold in whole 5-litre steps, so the search runs over the STEP
COUNT and multiplies by 5 at the end. That way no midpoint is ever an
illegal volume and no rounding is needed inside the loop.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
RAIL: list[int] = [9, 14, 6, 21, 3, 11]
STEP = 5  # kilns are sold in whole 5-litre increments


# ---- Your task ----
def firings_needed(pieces: list[int], volume: int) -> int:
    """Return how many firings a kiln of this volume needs to clear the rail.

    Args:
        pieces: Piece volumes in litres, in loading order.
        volume: The kiln's volume, at least as large as the biggest piece.

    Returns:
        The number of firings the front-loading packer closes.
    """
    firings = 0
    load = 0
    for piece in pieces:
        if load + piece > volume:
            firings += 1  # the door closes, and this piece starts the next one
            load = 0
        load += piece
    return firings + 1 if load else firings


def min_kiln_volume(pieces: list[int], firings: int) -> tuple[int, int] | None:
    """Return the smallest legal kiln volume that clears the rail in time.

    Args:
        pieces: Piece volumes in litres, in loading order.
        firings: How many firings the studio has booked.

    Returns:
        (volume, firings_used), (0, 0) for an empty rail, or None when no
        kiln at all can clear the rail within the budget.
    """
    if not pieces:
        return 0, 0
    if firings < 1:
        return None  # a non-empty rail always needs at least one firing

    lo = -(-max(pieces) // STEP)  # steps: the smallest kiln one piece fits in
    hi = -(-sum(pieces) // STEP)  # steps: the smallest kiln the whole rail fits in
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if firings_needed(pieces, mid * STEP) <= firings:
            hi = mid
        else:
            lo = mid + 1
    return lo * STEP, firings_needed(pieces, lo * STEP)


# ---- Self-check ----
if __name__ == "__main__":
    for booked in (1, 2, 3, 5, 0):
        print(f"{booked} firings booked -> {min_kiln_volume(RAIL, booked)}")

    assert min_kiln_volume(RAIL, 3) == (30, 3)
    assert min_kiln_volume(RAIL, 2) == (35, 2)
    assert min_kiln_volume(RAIL, 4) == (25, 4)
    assert min_kiln_volume(RAIL, 5) == (25, 4)
    assert min_kiln_volume(RAIL, 6) == (25, 4)
    assert min_kiln_volume(RAIL, 1) == (65, 1)
    assert min_kiln_volume(RAIL, 0) is None
    assert min_kiln_volume([5, 5, 5], 1) == (15, 1)
    assert min_kiln_volume([4], 2) == (5, 1)
    assert min_kiln_volume([20], 1) == (20, 1)
    assert min_kiln_volume([], 0) == (0, 0)
    assert min_kiln_volume([], 3) == (0, 0)
    assert min_kiln_volume([9], 0) is None
    assert RAIL[0] == 9  # the rail was never reordered
    print("All checks passed.")
