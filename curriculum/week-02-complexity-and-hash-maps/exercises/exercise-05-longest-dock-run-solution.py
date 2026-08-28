"""exercise-05-longest-dock-run-solution.py — the longest run of docks.

Put every reported ID in a set, then walk forward only from the IDs that start
a run. An ID starts a run when its predecessor is missing. Runs are disjoint,
so the walks together take at most one step per dock, and the whole thing is
O(n) with no sort anywhere.

Time: O(n) expected — n set inserts, one outer pass over the distinct IDs, and
at most n inner steps in total.
Space: O(n) — one set entry per distinct dock, never O(2_000_000_000).

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""


def longest_dock_run(reported: list[int]) -> tuple[int, int] | None:
    """Return the start and length of the longest run of consecutive docks.

    Args:
        reported: Dock IDs that phoned home overnight, unsorted, possibly
            with repeats.

    Returns:
        (first_id, length) for the longest run of consecutive IDs all
        present, ties broken toward the smaller first_id. None if nothing
        reported.
    """
    docks = set(reported)
    if not docks:
        return None

    best: tuple[int, int] | None = None
    for dock in docks:
        if dock - 1 in docks:
            continue  # not the root of its run; some other root will walk it
        length = 1
        while dock + length in docks:
            length += 1
        if best is None or length > best[1] or (length == best[1] and dock < best[0]):
            best = (dock, length)
    return best


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[int], tuple[int, int] | None]] = [
        ([4021, 88, 4019, 4020, 87, 700], (4019, 3)),
        ([12, 13, 40, 41], (12, 2)),
        ([50, 50, 51, 50], (50, 2)),
        ([9], (9, 1)),
        ([], None),
        ([5, 3, 1], (1, 1)),
        ([1000, 999, 998, 997, 996, 2, 1], (996, 5)),
        ([1, 2, 3, 4, 5, 6, 7, 8], (1, 8)),
    ]

    for reported, expected in cases:
        found = longest_dock_run(reported)
        assert found == expected, (reported, found, expected)
        counted = f"{len(reported)} reported"
        if found is None:
            print(f"{counted:<12} ->  nothing reported")
        else:
            start, length = found
            docks = f"{length} dock" + ("" if length == 1 else "s")
            print(f"{counted:<12} ->  {docks} from {start}")

    print("All checks passed.")
