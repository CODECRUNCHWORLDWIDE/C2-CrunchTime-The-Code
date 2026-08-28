"""problem-01-hose-clusters-solution.py -- counting a greenhouse's irrigation clusters.

Valves are numbered 0..valve_count-1 and hoses join pairs of them. Water that
reaches one valve in a group reaches every valve in that group, so "how many
separate watering circuits are there, and how big is the biggest one" is the
connected-components question -- asked from an edge list rather than a grid.

The maintenance log is a real log. The same hose can be written down twice, and
a hose can run from a valve back to itself. Neither changes the answer, because
the visited set absorbs both.

Run it with no arguments. The self-checks at the bottom print
"All checks passed." when every case agrees.
"""

from __future__ import annotations

# ---- Given data ----
VALVE_COUNT = 9

# (valve, valve) pairs, straight off the clipboard. Hose (3, 4) was written down
# twice, and valve 6 has a hose looped back to itself so the line can be bled.
MAINTENANCE_LOG: list[tuple[int, int]] = [
    (0, 1),
    (1, 2),
    (3, 4),
    (4, 5),
    (3, 4),
    (6, 6),
    (7, 8),
]


def survey_hoses(valve_count: int, hoses: list[tuple[int, int]]) -> tuple[int, int]:
    """Count the watering clusters and measure the biggest one.

    Args:
        valve_count: How many valves the bench has. They are numbered
            0 to valve_count - 1.
        hoses: The maintenance log. Each pair joins two valves. A repeated pair
            and a valve-to-itself pair are both allowed, and neither changes
            the answer.

    Returns:
        (cluster_count, largest_cluster_size). A valve joined to nothing is a
        cluster of one. A bench with no valves gives (0, 0).

    Raises:
        ValueError: A hose names a valve outside 0..valve_count - 1.
    """
    joined: list[list[int]] = [[] for _ in range(valve_count)]
    for left, right in hoses:
        for valve in (left, right):
            if not 0 <= valve < valve_count:
                raise ValueError(
                    f"hose names valve {valve}, which is outside 0..{valve_count - 1}"
                )
        joined[left].append(right)
        joined[right].append(left)

    seen: set[int] = set()

    def walk(valve: int) -> int:
        """Mark every valve reachable from this one, and count them."""
        seen.add(valve)
        size = 1
        for neighbour in joined[valve]:
            if neighbour not in seen:
                size += walk(neighbour)
        return size

    cluster_count = 0
    largest = 0
    for valve in range(valve_count):
        if valve not in seen:
            cluster_count += 1
            largest = max(largest, walk(valve))
    return (cluster_count, largest)


# ---- Self-check ----
if __name__ == "__main__":
    clusters, largest = survey_hoses(VALVE_COUNT, MAINTENANCE_LOG)
    print(f"bench: {VALVE_COUNT} valves, {len(MAINTENANCE_LOG)} hoses logged")
    print(f"  clusters        : {clusters}")
    print(f"  largest cluster : {largest}")

    print("the log is messy on purpose")
    print("  hose (3, 4) is written down twice")
    print("  hose (6, 6) loops valve 6 back to itself")
    print(
        f"  valves minus logged hoses would say "
        f"{VALVE_COUNT - len(MAINTENANCE_LOG)} clusters, which is wrong"
    )

    chain = [(step, step + 1) for step in range(899)]
    deep = survey_hoses(900, chain)
    print("a 900-valve chain, the longest run the constraints allow")
    print(f"  clusters        : {deep[0]}")
    print(f"  largest cluster : {deep[1]}")

    assert survey_hoses(VALVE_COUNT, MAINTENANCE_LOG) == (4, 3)
    assert survey_hoses(0, []) == (0, 0)
    assert survey_hoses(1, []) == (1, 1)
    assert survey_hoses(4, []) == (4, 1)
    assert survey_hoses(5, [(0, 1), (1, 2), (2, 3), (3, 4)]) == (1, 5)
    assert survey_hoses(3, [(0, 1), (0, 1), (0, 1)]) == (2, 2)
    assert survey_hoses(3, [(1, 1)]) == (3, 1)
    assert survey_hoses(2, [(1, 0)]) == (1, 2)
    assert deep == (1, 900)

    try:
        survey_hoses(4, [(0, 9)])
    except ValueError as err:
        assert "9" in str(err)
    else:
        raise AssertionError("a valve outside the bench should raise ValueError")

    print("All checks passed.")
