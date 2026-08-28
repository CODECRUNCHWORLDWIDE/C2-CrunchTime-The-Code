"""challenge-01-balanced-shifts-solution.py — counting balanced shift windows.

A window's sum is the difference of two prefix sums, so "which windows sum to
the target" becomes "which pairs of prefix sums differ by the target" — and
that is a lookup, not a search. One map from prefix value to (how many times
it has occurred, the most recent index it occurred at) answers both halves of
the question in one pass.

Time: O(n) — one pass, one addition, one lookup and one write per hour.
Space: O(n) — the map holds at most n + 1 distinct prefix values.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""


def balanced_shifts(
    net_moves: list[int], target: int
) -> tuple[int, tuple[int, int] | None]:
    """Count balanced windows and name the one to look at first.

    Args:
        net_moves: Net pallet movement for each hour of operation. Negative
            on an hour when more went out than came in.
        target: The sum a window must hit to be balanced.

    Returns:
        (count, earliest) where count is how many contiguous non-empty
        windows sum to target, and earliest is the (i, j) of the balanced
        window with the smallest end j, breaking ties toward the largest
        start i. (0, None) when no window is balanced.
    """
    # The empty prefix has value 0, has occurred once, and lives at index 0.
    seen: dict[int, tuple[int, int]] = {0: (1, 0)}
    running = 0
    count = 0
    earliest: tuple[int, int] | None = None

    for end, moved in enumerate(net_moves):
        running += moved
        needed = running - target
        if needed in seen:
            frequency, most_recent = seen[needed]
            count += frequency
            if earliest is None:
                earliest = (most_recent, end)
        frequency, _ = seen.get(running, (0, 0))
        seen[running] = (frequency + 1, end + 1)

    return (count, earliest)


# ---- Self-check ----
if __name__ == "__main__":
    checks: list[tuple[list[int], int, tuple[int, tuple[int, int] | None]]] = [
        ([3, -1, 4, -3, 1, 2], 3, (5, (0, 0))),
        ([2, 0, 3], 3, (2, (2, 2))),
        ([0, 0, 0], 0, (6, (0, 0))),
        ([1, -1, 1, -1, 1], 1, (6, (0, 0))),
        ([10, -10, 10, -10], 0, (4, (0, 1))),
        ([-2, -3, 5, -5], -5, (3, (0, 1))),
        ([4, -7, 2], -7, (1, (1, 1))),
        ([0], 0, (1, (0, 0))),
        ([7], 7, (1, (0, 0))),
        ([3], 0, (0, None)),
        ([5, 5], 3, (0, None)),
        ([], 0, (0, None)),
    ]

    def brute_force(
        net_moves: list[int], target: int
    ) -> tuple[int, tuple[int, int] | None]:
        """Reference answer straight from the definition. O(n^2), obviously right."""
        windows = [
            (start, end)
            for start in range(len(net_moves))
            for end in range(start, len(net_moves))
            if sum(net_moves[start : end + 1]) == target
        ]
        if not windows:
            return (0, None)
        return (len(windows), min(windows, key=lambda w: (w[1], -w[0])))

    for net_moves, target, expected in checks:
        found = balanced_shifts(list(net_moves), target)
        assert found == expected, (net_moves, target, found, expected)
        assert found == brute_force(net_moves, target), (net_moves, target)
        count, earliest = found
        window = "none" if earliest is None else f"{earliest[0]}..{earliest[1]}"
        print(f"target {target:3d}  ->  {count:2d} balanced, first {window:>6}   {net_moves}")

    print("All checks passed.")
