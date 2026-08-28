"""exercise-05-market-awning-solution.py — the largest wind curtain on the row.

Two pointers start at the ends of the pole row, measure the curtain they
could hang, keep the best, then discard the shorter pole. Discarding the
shorter pole is safe because every remaining pair that still uses it is
narrower and no taller.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""


def max_curtain_area(pole_heights: list[int]) -> int:
    """Find the largest wind curtain that can hang between two poles.

    Args:
        pole_heights: Surveyed pole heights in whole metres, west to east.
            A height of 0 is a snapped stub that still occupies its slot.

    Returns:
        The largest achievable area in square metres, which is
        min(height[i], height[j]) * (j - i - 1) maximised over i < j, or 0
        when no choice of two poles yields any fabric.
    """
    left, right = 0, len(pole_heights) - 1
    best = 0
    while left < right:
        height = min(pole_heights[left], pole_heights[right])
        area = height * (right - left - 1)
        if area > best:
            best = area
        if pole_heights[left] < pole_heights[right]:
            left += 1
        else:
            right -= 1
    return best


# ---- Self-check ----
if __name__ == "__main__":
    rows = [
        [2, 6, 3, 8, 1, 7, 4],
        [2, 7, 5, 5, 7, 2],
        [5, 5],
        [0, 9, 9, 0],
        [4],
        [],
    ]
    for poles in rows:
        print(f"best area {max_curtain_area(poles):>3} sq m   poles {poles}")

    assert max_curtain_area([2, 6, 3, 8, 1, 7, 4]) == 18
    assert max_curtain_area([2, 7, 5, 5, 7, 2]) == 14
    assert max_curtain_area([5, 5]) == 0
    assert max_curtain_area([0, 9, 9, 0]) == 0
    assert max_curtain_area([4]) == 0
    assert max_curtain_area([]) == 0
    print("All checks passed.")
