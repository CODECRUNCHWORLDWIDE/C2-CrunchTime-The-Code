"""exercise-01-reverse-the-siding-solution.py — the yard controller's flip order.

Reverse a run of freight cars on a siding, in place, by swapping pairs.
Refuse a nonsense order whole. Report how many swaps were performed.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""


def reverse_siding(cars: list[str], start: int, end: int) -> int:
    """Reverse cars[start..end] inclusive, in place, by swapping.

    Args:
        cars: The siding, nose-to-tail. Reversed in place when the order is
            valid, and left completely untouched when it is not.
        start: First position of the run to flip.
        end: Last position of the run to flip, inclusive.

    Returns:
        The number of swaps performed. Zero when the order is refused.
    """
    if start < 0 or end >= len(cars) or start >= end:
        return 0

    left, right = start, end
    swaps = 0
    while left < right:
        cars[left], cars[right] = cars[right], cars[left]
        left += 1
        right -= 1
        swaps += 1
    return swaps


# ---- Self-check ----
if __name__ == "__main__":
    orders = [
        (["HOP", "TNK", "BOX", "GON", "FLT"], 1, 3),
        (["HOP", "TNK", "BOX", "GON", "FLT"], 0, 4),
        (["HOP", "TNK", "BOX", "GON"], 0, 3),
        (["HOP"], 0, 0),
        ([], 0, 0),
        (["HOP", "TNK", "BOX"], 2, 1),
        (["HOP", "TNK", "BOX"], 1, 7),
        (["HOP", "TNK", "BOX"], -1, 2),
    ]
    for cars, start, end in orders:
        before = list(cars)
        swaps = reverse_siding(cars, start, end)
        verdict = "refused" if swaps == 0 and cars == before else "flipped "
        print(f"{verdict} start={start:>2} end={end:>2}  swaps={swaps}  {before} -> {cars}")

    siding = ["HOP", "TNK", "BOX", "GON", "FLT"]
    assert reverse_siding(siding, 1, 3) == 1
    assert siding == ["HOP", "GON", "BOX", "TNK", "FLT"]
    assert reverse_siding(["HOP", "TNK", "BOX", "GON", "FLT"], 0, 4) == 2
    assert reverse_siding(["HOP", "TNK", "BOX", "GON"], 0, 3) == 2
    assert reverse_siding(["HOP"], 0, 0) == 0
    assert reverse_siding([], 0, 0) == 0
    assert reverse_siding(["HOP", "TNK", "BOX"], 2, 1) == 0
    assert reverse_siding(["HOP", "TNK", "BOX"], 1, 7) == 0
    assert reverse_siding(["HOP", "TNK", "BOX"], -1, 2) == 0

    untouched = ["HOP", "TNK", "BOX"]
    reverse_siding(untouched, 1, 7)
    assert untouched == ["HOP", "TNK", "BOX"]  # a refused order moves nothing
    print("All checks passed.")
