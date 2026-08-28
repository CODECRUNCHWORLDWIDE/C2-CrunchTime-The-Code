"""problem-02-relay-handoff-solution.py - the fairest relay split.

Binary search on the answer, minimise-the-maximum flavour. The predicate
counts the FEWEST blocks a cap allows and tests `blocks <= riders`, not
`== riders`: a split into fewer blocks can always be cut finer as long as
there are legs left to cut.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
ROUTE: list[int] = [8, 3, 9, 4, 6, 2]


# ---- Your task ----
def blocks_needed(legs: list[int], cap: int) -> int:
    """Return the fewest contiguous blocks whose sums all stay within `cap`.

    Args:
        legs: Leg distances in kilometres, in route order.
        cap: The distance no single rider may exceed. At least max(legs).

    Returns:
        The number of blocks the greedy left-to-right sweep closes.
    """
    blocks = 1
    carried = 0
    for leg in legs:
        if carried + leg > cap:
            blocks += 1
            carried = 0
        carried += leg
    return blocks


def fairest_relay_split(legs: list[int], riders: int) -> int | None:
    """Return the smallest possible distance for the hardest-worked rider.

    Args:
        legs: Leg distances in kilometres, in route order.
        riders: How many riders the route is split among, exactly.

    Returns:
        The minimum achievable largest block sum, 0 for an empty route with
        zero riders, or None when the split cannot be made at all.
    """
    if not legs:
        return 0 if riders == 0 else None
    if riders < 1 or riders > len(legs):
        return None

    lo, hi = max(legs), sum(legs)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if blocks_needed(legs, mid) <= riders:
            hi = mid
        else:
            lo = mid + 1
    return lo


# ---- Self-check ----
if __name__ == "__main__":
    for team in (1, 2, 3, 5, 7):
        print(f"{team} riders -> {fairest_relay_split(ROUTE, team)}")

    assert fairest_relay_split(ROUTE, 3) == 12
    assert fairest_relay_split(ROUTE, 2) == 20
    assert fairest_relay_split(ROUTE, 4) == 11
    assert fairest_relay_split(ROUTE, 5) == 9
    assert fairest_relay_split(ROUTE, 6) == 9
    assert fairest_relay_split(ROUTE, 1) == 32
    assert fairest_relay_split(ROUTE, 7) is None
    assert fairest_relay_split(ROUTE, 0) is None
    assert fairest_relay_split([0, 0, 0], 2) == 0
    assert fairest_relay_split([5, 0, 5], 2) == 5
    assert fairest_relay_split([], 0) == 0
    assert fairest_relay_split([], 1) is None
    assert ROUTE[0] == 8  # the route was never reordered
    print("All checks passed.")
