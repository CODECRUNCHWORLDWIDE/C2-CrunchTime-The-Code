"""problem-02-courier-zone-count-solution.py — counting exactly-K segments.

A courier's shift is a list of delivery-zone codes, one per stop. Regional
accounting bills the route segments that touch exactly k distinct zones, and a
segment is any contiguous run of one or more stops.

No single window counts "exactly k" directly, because a window that is
currently at k distinct zones may later be at k + 1 and the segments it
already contributed cannot be taken back. The way through is an identity:

    exactly(k) = at_most(k) - at_most(k - 1)

`at_most` is a counting window. Once its invariant holds at `right`, every
segment that ends at `right` and starts anywhere in [left, right] also holds
it, so the step adds `right - left + 1` in one go rather than enumerating.

The self-checks are the starter's, unchanged. When they all pass the file
prints "All checks passed."
"""


def at_most(stops: list[str], limit: int) -> int:
    """Return how many segments touch at most `limit` distinct zones.

    Args:
        stops: Zone codes, one per stop, in visit order.
        limit: The largest number of distinct zones a segment may touch.

    Returns:
        The number of contiguous runs of one or more stops within the limit.
        Zero when the limit is zero or negative, because no run of one or more
        stops touches zero zones.
    """
    if limit <= 0:
        return 0

    counts: dict[str, int] = {}
    left = 0
    total = 0

    for right, zone in enumerate(stops):
        counts[zone] = counts.get(zone, 0) + 1

        while len(counts) > limit:
            leaving = stops[left]
            counts[leaving] -= 1
            if counts[leaving] == 0:
                del counts[leaving]
            left += 1

        # Every segment ending here and starting at or after `left` qualifies.
        total += right - left + 1

    return total


def segments_with_exactly_k_zones(stops: list[str], k: int) -> int:
    """Return how many route segments touch exactly k distinct zones.

    Args:
        stops: Zone codes, one per stop, in visit order.
        k: The exact number of distinct zones a billable segment touches.

    Returns:
        The count of qualifying segments. Zero when k is zero or the shift is
        empty.
    """
    if k == 0 or not stops:
        return 0
    return at_most(stops, k) - at_most(stops, k - 1)


def count_by_enumeration(stops: list[str], k: int) -> int:
    """Count the same thing the slow, obvious way. Used only to check.

    Args:
        stops: Zone codes, one per stop, in visit order.
        k: The exact number of distinct zones a billable segment touches.

    Returns:
        The same number, reached by looking at every segment in turn.
    """
    if k == 0:
        return 0
    return sum(
        1
        for i in range(len(stops))
        for j in range(i + 1, len(stops) + 1)
        if len(set(stops[i:j])) == k
    )


# ---- Self-check ----
if __name__ == "__main__":
    shift = ["N", "N", "E", "S", "E"]
    print(f"shift {shift}, k=2")
    print(f"  at_most(2)            : {at_most(shift, 2)}")
    print(f"  at_most(1)            : {at_most(shift, 1)}")
    print(f"  exactly 2 zones       : {segments_with_exactly_k_zones(shift, 2)}")
    print(f"  same, by enumeration  : {count_by_enumeration(shift, 2)}")
    print()

    cases: list[tuple[list[str], int]] = [
        (["N", "N", "E", "S", "E"], 2),
        (["N", "E", "N"], 1),
        (["W", "X", "Y", "Z"], 4),
        (["W", "W", "W"], 1),
        (["W", "X"], 3),
        (["W"], 0),
        ([], 1),
    ]
    for stops, k in cases:
        print(f"k={k}  stops {str(stops):<26} -> {segments_with_exactly_k_zones(stops, k)}")
    print()

    assert segments_with_exactly_k_zones(["N", "N", "E", "S", "E"], 2) == 5
    assert segments_with_exactly_k_zones(["N", "E", "N"], 1) == 3
    assert segments_with_exactly_k_zones(["W", "X", "Y", "Z"], 4) == 1
    assert segments_with_exactly_k_zones(["W", "W", "W"], 1) == 6
    assert segments_with_exactly_k_zones(["W", "X"], 3) == 0
    assert segments_with_exactly_k_zones(["W"], 0) == 0
    assert segments_with_exactly_k_zones([], 1) == 0

    assert at_most(["N", "N", "E", "S", "E"], 2) == 11
    assert at_most(["N", "N", "E", "S", "E"], 1) == 6
    assert at_most(["N", "E", "N"], 0) == 0

    # The identity and the enumeration must agree on every case, at every k.
    for stops, _ in cases:
        for k in range(0, 6):
            assert segments_with_exactly_k_zones(stops, k) == count_by_enumeration(stops, k)

    print("All checks passed.")
