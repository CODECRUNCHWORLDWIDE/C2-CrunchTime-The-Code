"""problem-02-splice-drum-tape-solution.py — joining fibre drums with the least tape.

A cable crew has to join several drums of fibre into one continuous run. Each
join costs tape equal to the combined length of the two pieces being joined, so
the order of the joins changes the bill. Always joining the two shortest pieces
first is the cheapest order, and a min-heap makes "the two shortest" a pair of
pops.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
# Drum lengths in metres.
DRUM_METRES: list[int] = [12, 9, 30, 21, 5, 16]


# ---- Your task ----
def splice_costs(drums: list[int]) -> tuple[int, list[int]]:
    """Return the cheapest total tape and the cost of each join, in order.

    Args:
        drums: Drum lengths in metres. This list is not modified.

    Returns:
        (total tape in metres, one cost per join). One drum needs no join, so
        it costs nothing; no drums at all costs nothing too.
    """
    if len(drums) < 2:
        return 0, []
    pieces = list(drums)
    heapq.heapify(pieces)
    costs = []
    while len(pieces) > 1:
        shortest = heapq.heappop(pieces)
        second = heapq.heappop(pieces)
        joined = shortest + second
        costs.append(joined)
        heapq.heappush(pieces, joined)
    return sum(costs), costs


def worst_order_cost(drums: list[int]) -> int:
    """Return what the same drums cost when the two LONGEST are joined first.

    This is the same simulation with the comparison flipped, and it exists to
    be compared against — the difference is the whole point of the greedy rule.

    Args:
        drums: Drum lengths in metres. This list is not modified.

    Returns:
        The total tape in metres for the worst join order.
    """
    if len(drums) < 2:
        return 0
    pieces = [-length for length in drums]
    heapq.heapify(pieces)
    total = 0
    while len(pieces) > 1:
        longest = -heapq.heappop(pieces)
        second = -heapq.heappop(pieces)
        joined = longest + second
        total += joined
        heapq.heappush(pieces, -joined)
    return total


def run_length(drums: list[int]) -> int:
    """Return the length of the finished run, which the join order cannot change.

    Args:
        drums: Drum lengths in metres.

    Returns:
        The sum of the drum lengths.
    """
    return sum(drums)


# ---- Self-check ----
if __name__ == "__main__":
    total, costs = splice_costs(DRUM_METRES)
    print(f"drums: {DRUM_METRES}")
    print(f"finished run: {run_length(DRUM_METRES)} m")
    print("joins, cheapest order:")
    for number, cost in enumerate(costs, 1):
        print(f"  join {number}: {cost} m of tape")
    print(f"total tape, cheapest order: {total} m")
    print(f"total tape, worst order   : {worst_order_cost(DRUM_METRES)} m")
    print(f"difference: {worst_order_cost(DRUM_METRES) - total} m")

    print(f"one drum: {splice_costs([40])}")
    print(f"no drums: {splice_costs([])}")
    print(f"two drums: {splice_costs([7, 3])}")

    assert costs == [14, 26, 37, 56, 93]
    assert total == 226
    assert run_length(DRUM_METRES) == 93
    assert costs[-1] == run_length(DRUM_METRES)
    assert worst_order_cost(DRUM_METRES) > total
    assert splice_costs([40]) == (0, [])
    assert splice_costs([]) == (0, [])
    assert splice_costs([7, 3]) == (10, [10])
    assert DRUM_METRES == [12, 9, 30, 21, 5, 16]  # original list untouched
    print("All checks passed.")
