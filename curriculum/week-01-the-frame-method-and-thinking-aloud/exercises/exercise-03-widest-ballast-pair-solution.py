"""exercise-03-widest-ballast-pair-solution.py — the two containers to shift.

A sorted row of container weights, one correction figure, and a rule that
picks the pair standing furthest apart on the deck. Converging pointers
examine pairs in strictly decreasing order of span, so the first match they
find is already the widest.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""


def widest_ballast_pair(weights: list[int], correction: int) -> tuple[int, int] | None:
    """Find the furthest-apart pair of containers summing to the correction.

    Args:
        weights: Deck positions in non-decreasing weight order, kilograms.
        correction: The figure the two shifted containers must sum to.

    Returns:
        The pair of 0-indexed deck positions (i, j) with i < j, maximising
        j - i, or None when no pair sums to the correction figure.
    """
    left, right = 0, len(weights) - 1
    while left < right:
        total = weights[left] + weights[right]
        if total == correction:
            return (left, right)
        if total < correction:
            left += 1
        else:
            right -= 1
    return None


# ---- Self-check ----
if __name__ == "__main__":
    manifests = [
        ([120, 340, 500, 660, 880], 1000),
        ([-400, -100, 0, 100, 300], 0),
        ([100, 100, 100, 100], 200),
        ([200, 200, 800, 800], 1000),
        ([150, 150], 300),
        ([150], 300),
        ([], 0),
        ([10, 20, 30], 100),
    ]
    for weights, correction in manifests:
        pair = widest_ballast_pair(weights, correction)
        if pair is None:
            print(f"correction {correction:>5}  no pair            {weights}")
        else:
            i, j = pair
            print(f"correction {correction:>5}  pair {pair} span {j - i}  {weights}")

    assert widest_ballast_pair([120, 340, 500, 660, 880], 1000) == (0, 4)
    assert widest_ballast_pair([-400, -100, 0, 100, 300], 0) == (1, 3)
    assert widest_ballast_pair([100, 100, 100, 100], 200) == (0, 3)
    assert widest_ballast_pair([200, 200, 800, 800], 1000) == (0, 3)
    assert widest_ballast_pair([150, 150], 300) == (0, 1)
    assert widest_ballast_pair([150], 300) is None
    assert widest_ballast_pair([], 0) is None
    assert widest_ballast_pair([10, 20, 30], 100) is None
    print("All checks passed.")
