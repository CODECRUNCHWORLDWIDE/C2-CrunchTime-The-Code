"""exercise-01-staffing-block-solution.py — the busiest staffing block.

A 24-hour clinic counts walk-ins in every 15-minute interval. The rota manager
staffs the floor in blocks of k consecutive intervals and wants to know which
block is under the most pressure.

Two versions of the same answer live here. `busiest_block` carries one running
total across the log and fixes it up in constant time at every step.
`busiest_block_rescan` adds the whole block up again at every position. The
rescan is the wrong way, and it is here on purpose: the checks at the bottom
prove the two agree, and the two cost functions put a number on how much extra
work the wrong way does.

The self-checks are the starter's, unchanged. When they all pass the file
prints "All checks passed."
"""


def busiest_block(arrivals: list[int], k: int) -> int | None:
    """Return the start index of the k-interval block with the most arrivals.

    Args:
        arrivals: Walk-in counts, one per 15-minute interval, in time order.
        k: How many consecutive intervals a staffing block covers.

    Returns:
        The start index of the busiest block, ties going to the latest such
        start. None when the block does not fit inside the log.
    """
    if k > len(arrivals):
        return None

    window_total = sum(arrivals[:k])
    best_total = window_total
    best_start = 0

    for right in range(k, len(arrivals)):
        window_total += arrivals[right] - arrivals[right - k]
        start = right - k + 1
        if window_total >= best_total:
            best_total = window_total
            best_start = start

    return best_start


def busiest_block_rescan(arrivals: list[int], k: int) -> int | None:
    """The same answer, computed the expensive way. Kept only for comparison.

    Args:
        arrivals: Walk-in counts, one per 15-minute interval, in time order.
        k: How many consecutive intervals a staffing block covers.

    Returns:
        The same value `busiest_block` returns, reached by adding every block
        up from scratch.
    """
    if k > len(arrivals):
        return None

    best_total = sum(arrivals[:k])
    best_start = 0

    for start in range(1, len(arrivals) - k + 1):
        total = sum(arrivals[start : start + k])
        if total >= best_total:
            best_total = total
            best_start = start

    return best_start


def additions_rescan(n: int, k: int) -> int:
    """How many additions the rescan performs on a log of n intervals.

    Args:
        n: Length of the log.
        k: Block size.

    Returns:
        One addition fewer than k for every block, times the number of blocks.
    """
    if k > n:
        return 0
    return (n - k + 1) * (k - 1)


def additions_sliding(n: int, k: int) -> int:
    """How many additions the sliding window performs on a log of n intervals.

    Args:
        n: Length of the log.
        k: Block size.

    Returns:
        The cost of the first block, plus one add and one subtract per slide.
    """
    if k > n:
        return 0
    return (k - 1) + 2 * (n - k)


# ---- Self-check ----
if __name__ == "__main__":
    log = [4, 1, 7, 2, 5, 3, 3, 6]
    totals = [sum(log[i : i + 3]) for i in range(len(log) - 2)]
    print(f"log {log}, k=3")
    print(f"  block totals : {totals}")
    print(f"  busiest block starts at index {busiest_block(log, 3)}")
    print()

    print(f"four-way tie at 9 in [1, 8, 1, 1, 8, 1], k=2 -> {busiest_block([1, 8, 1, 1, 8, 1], 2)}")
    print(f"all-zero log [0, 0, 0], k=2                  -> {busiest_block([0, 0, 0], 2)}")
    print(f"block longer than the log [5, 5], k=3        -> {busiest_block([5, 5], 3)}")
    print()

    n, k = 2_000, 500
    rescan, sliding = additions_rescan(n, k), additions_sliding(n, k)
    print(f"additions on a {n}-interval log with k={k}")
    print(f"  rescan  : {rescan:>9,}")
    print(f"  sliding : {sliding:>9,}")
    print(f"  the rescan does {rescan // sliding} times the work for the same answer")
    print()

    assert busiest_block([4, 1, 7, 2, 5, 3, 3, 6], 3) == 2
    assert busiest_block([1, 8, 1, 1, 8, 1], 2) == 4
    assert busiest_block([2, 0, 2, 0, 2], 2) == 3
    assert busiest_block([0, 0, 0], 2) == 1
    assert busiest_block([9], 1) == 0
    assert busiest_block([5, 5], 3) is None
    assert busiest_block([], 1) is None

    for case, size in [([4, 1, 7, 2, 5, 3, 3, 6], 3), ([1, 8, 1, 1, 8, 1], 2), ([2, 0, 2, 0, 2], 2), ([0, 0, 0], 2)]:
        assert busiest_block(case, size) == busiest_block_rescan(case, size)

    print("All checks passed.")
