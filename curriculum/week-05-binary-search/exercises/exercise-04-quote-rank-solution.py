"""exercise-04-quote-rank-solution.py - the freight broker's k-th quote.

Binary search on VALUES, not on indices. There is no list of quotes to
bisect - there can be ten billion of them - but "how many quotes cost at
most v?" is non-decreasing in v, and that is all bisection needs.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
HANDLING: list[int] = [2, 5, 9]
LINEHAUL: list[int] = [1, 4, 4]


# ---- Your task ----
def count_at_most(handling: list[int], linehaul: list[int], ceiling: int) -> int:
    """Return how many pairwise quotes cost at most `ceiling`.

    Args:
        handling: Handling fees, sorted ascending.
        linehaul: Linehaul fees, sorted ascending.
        ceiling: The price to count up to, inclusive.

    Returns:
        The number of (handling, linehaul) pairs whose sum is <= ceiling,
        counted with multiplicity.
    """
    j = len(linehaul) - 1
    total = 0
    for fee in handling:
        while j >= 0 and fee + linehaul[j] > ceiling:
            j -= 1  # j only ever falls, which is what keeps this O(n + m)
        total += j + 1
    return total


def quote_rank(handling: list[int], linehaul: list[int], k: int) -> tuple[int, int] | None:
    """Return the k-th cheapest quote and how many quotes are cheaper still.

    Args:
        handling: Handling fees, sorted ascending.
        linehaul: Linehaul fees, sorted ascending.
        k: The 1-based rank the shipper asked for.

    Returns:
        (quote, strictly_cheaper_count), or None when the rate card cannot
        produce k quotes at all.
    """
    if not handling or not linehaul or k < 1:
        return None
    if k > len(handling) * len(linehaul):
        return None

    lo = handling[0] + linehaul[0]
    hi = handling[-1] + linehaul[-1]
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if count_at_most(handling, linehaul, mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo, count_at_most(handling, linehaul, lo - 1)


# ---- Self-check ----
if __name__ == "__main__":
    for rank in (1, 2, 4, 5, 9, 10):
        print(f"k={rank:2d} -> {quote_rank(HANDLING, LINEHAUL, rank)}")

    assert quote_rank(HANDLING, LINEHAUL, 1) == (3, 0)
    assert quote_rank(HANDLING, LINEHAUL, 2) == (6, 1)
    assert quote_rank(HANDLING, LINEHAUL, 4) == (6, 1)
    assert quote_rank(HANDLING, LINEHAUL, 5) == (9, 4)
    assert quote_rank(HANDLING, LINEHAUL, 9) == (13, 7)
    assert quote_rank(HANDLING, LINEHAUL, 10) is None
    assert quote_rank([], [1, 4, 4], 1) is None
    assert quote_rank([7], [7], 1) == (14, 0)
    assert count_at_most(HANDLING, LINEHAUL, 6) == 4
    assert HANDLING == [2, 5, 9]  # the rate card was never rearranged
    print("All checks passed.")
