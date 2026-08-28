"""exercise-03-stage-twins-solution.py — grouping acts by their load-out.

Every act gets one canonical key: its load-out sorted into a tuple. Two acts
are stage twins exactly when their keys are equal, so grouping the acts becomes
bucketing their indices under that key.

Time: O(n * k log k) — one sort per act, k items in the largest load-out.
Space: O(n * k) — the keys and the buckets.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from collections import defaultdict


def stage_twins(loadouts: list[list[str]]) -> list[list[int]]:
    """Group the submission indices of acts with identical load-outs.

    Args:
        loadouts: One list of backline item codes per act, in submission
            order. An act that brings two of an item lists it twice.

    Returns:
        Groups of at least two indices, each group ascending, the groups
        themselves ordered by their smallest index. Acts with a unique
        load-out are absent.
    """
    groups: defaultdict[tuple[str, ...], list[int]] = defaultdict(list)
    for index, items in enumerate(loadouts):
        groups[tuple(sorted(items))].append(index)
    return [indices for indices in groups.values() if len(indices) >= 2]


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[list[str]], list[list[int]]]] = [
        (
            [
                ["gtr", "kit", "bass"],
                ["bass", "gtr", "kit"],
                ["kit", "kit"],
                ["gtr", "gtr", "kit"],
                ["kit", "kit"],
            ],
            [[0, 1], [2, 4]],
        ),
        ([["gtr", "gtr"], ["gtr"]], []),
        ([["kit"], ["kit"], ["kit"]], [[0, 1, 2]]),
        ([[], []], [[0, 1]]),
        ([], []),
        ([["snare", "hat"], ["hat", "snare"], ["gtr"], ["hat", "hat"]], [[0, 1]]),
    ]

    for loadouts, expected in cases:
        found = stage_twins(loadouts)
        assert found == expected, (loadouts, found, expected)
        print(f"{len(loadouts)} acts  ->  {found}")

    print("All checks passed.")
