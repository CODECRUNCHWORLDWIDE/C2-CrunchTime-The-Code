"""challenge-01-order-book-boundary-solution.py - the rank boundary of two books.

Binary search on a SPLIT, not on a value. Choose how many deltas from the
shorter report land left of the split; the count from the other report
follows, because the left side must hold exactly k deltas.

The self-checks at the bottom are the starter's, unchanged. The last one
cross-checks the search against a plain merge on generated books, which is
where sentinel bugs surface. When they all pass the file prints
"All checks passed."
"""

import random
from math import inf

# ---- Given data ----
VENUE_A: list[int] = [3, 8, 8, 15]
VENUE_B: list[int] = [1, 4, 9]


# ---- Your task ----
def book_boundary(venue_a: list[int], venue_b: list[int], k: int) -> tuple[int, int | None] | None:
    """Return the k-th and (k+1)-th smallest deltas of the combined multiset.

    Args:
        venue_a: One venue's deltas, sorted ascending, duplicates allowed.
        venue_b: The other venue's deltas, sorted ascending.
        k: The 1-based rank the risk desk asked for.

    Returns:
        (kth, next_kth), with next_kth None at the last rank, or None when k
        falls outside 1..len(venue_a) + len(venue_b).
    """
    short, long = (venue_a, venue_b) if len(venue_a) <= len(venue_b) else (venue_b, venue_a)
    m, n = len(short), len(long)
    if k < 1 or k > m + n:
        return None

    lo, hi = max(0, k - n), min(k, m)
    while lo <= hi:
        taken = lo + (hi - lo) // 2  # deltas taken from the shorter report
        rest = k - taken  # deltas taken from the longer one
        left_short = short[taken - 1] if taken > 0 else -inf
        right_short = short[taken] if taken < m else inf
        left_long = long[rest - 1] if rest > 0 else -inf
        right_long = long[rest] if rest < n else inf

        if left_short > right_long:
            hi = taken - 1  # took too many from the shorter report
        elif left_long > right_short:
            lo = taken + 1  # took too few
        else:
            kth = max(left_short, left_long)
            nxt = min(right_short, right_long)
            return kth, (None if nxt == inf else nxt)
    return None  # unreachable: the clamped interval always holds the crossing


# ---- Self-check ----
if __name__ == "__main__":
    print(f"combined order: {sorted(VENUE_A + VENUE_B)}")
    for rank in (1, 4, 7, 8):
        print(f"k={rank} -> {book_boundary(VENUE_A, VENUE_B, rank)}")

    assert book_boundary(VENUE_A, VENUE_B, 1) == (1, 3)
    assert book_boundary(VENUE_A, VENUE_B, 2) == (3, 4)
    assert book_boundary(VENUE_A, VENUE_B, 4) == (8, 8)
    assert book_boundary(VENUE_A, VENUE_B, 7) == (15, None)
    assert book_boundary(VENUE_A, VENUE_B, 8) is None
    assert book_boundary(VENUE_A, VENUE_B, 0) is None
    assert book_boundary([], [42], 1) == (42, None)
    assert book_boundary([42], [], 1) == (42, None)
    assert book_boundary([], [], 1) is None
    assert book_boundary([1, 2, 3], [10, 20, 30], 3) == (3, 10)
    assert book_boundary([1, 2, 3], [10, 20, 30], 4) == (10, 20)
    assert book_boundary([10, 20, 30], [1, 2, 3], 3) == (3, 10)
    assert book_boundary([5, 5, 5], [5, 5], 3) == (5, 5)
    assert book_boundary([-9, -4, 0], [-7, 2], 2) == (-7, -4)

    rng = random.Random(20250505)
    pairs = 0
    for _ in range(500):
        a = sorted(rng.randrange(-20, 21) for _ in range(rng.randrange(0, 9)))
        b = sorted(rng.randrange(-20, 21) for _ in range(rng.randrange(0, 9)))
        merged = sorted(a + b)
        for rank in range(0, len(merged) + 2):
            if 1 <= rank <= len(merged):
                after = merged[rank] if rank < len(merged) else None
                wanted = (merged[rank - 1], after)
            else:
                wanted = None
            assert book_boundary(a, b, rank) == wanted, (a, b, rank)
        pairs += 1
    print(f"cross-checked {pairs} generated book pairs against a plain merge")
    print("All checks passed.")
