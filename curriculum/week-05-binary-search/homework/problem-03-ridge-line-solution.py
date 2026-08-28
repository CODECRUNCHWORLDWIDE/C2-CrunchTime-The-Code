"""problem-03-ridge-line-solution.py - find a ridge on an unsorted transect.

Bisection without a sorted sequence. The rule that halves the search is not
"the target is bigger than the midpoint" but "the ground is still rising
here, so a ridge lies somewhere to the right".

The self-checks at the bottom are the starter's, unchanged. They assert the
RIDGE PROPERTY rather than a fixed index, because a transect may hold
several ridges and any of them is a correct answer. When they all pass the
file prints "All checks passed."
"""

# ---- Given data ----
TRANSECT: list[int] = [12, 30, 25, 41, 55, 48, 9]


# ---- Your task ----
def find_ridge(elevations: list[int]) -> tuple[int, int] | None:
    """Return a station that is strictly higher than both its neighbours.

    Args:
        elevations: Ground heights at evenly spaced stations. Adjacent
            stations never record the same height.

    Returns:
        (index, elevation) for some ridge, or None for an empty transect.
        The ground off either end counts as infinitely low.
    """
    if not elevations:
        return None

    lo, hi = 0, len(elevations) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if elevations[mid] < elevations[mid + 1]:
            lo = mid + 1  # still climbing, so a ridge lies to the right
        else:
            hi = mid  # falling here, so mid or something left of it is a ridge
    return lo, elevations[lo]


def is_ridge(elevations: list[int], index: int) -> bool:
    """Return True when the station at `index` beats both its neighbours."""
    left = elevations[index - 1] if index > 0 else float("-inf")
    right = elevations[index + 1] if index + 1 < len(elevations) else float("-inf")
    return left < elevations[index] > right


# ---- Self-check ----
if __name__ == "__main__":
    for transect in ([12, 30, 25, 41, 55, 48, 9], [8, 5, 3], [3, 5, 8], [7]):
        print(f"{transect} -> {find_ridge(transect)}")

    for transect in (
        TRANSECT,
        [3, 8, 5],
        [8, 5, 3],
        [3, 5, 8],
        [4, 9],
        [9, 4],
        [7],
        [-120, -45, -300],
    ):
        found = find_ridge(transect)
        assert found is not None
        index, elevation = found
        assert transect[index] == elevation
        assert is_ridge(transect, index), (transect, found)
    assert find_ridge([]) is None
    assert TRANSECT[0] == 12  # the transect was never reordered
    print("All checks passed.")
