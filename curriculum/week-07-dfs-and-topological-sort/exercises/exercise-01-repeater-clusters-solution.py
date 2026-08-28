"""exercise-01-repeater-clusters-solution.py — the repeater-mast cluster survey.

Recursive depth-first search over a symmetric 0/1 link table. Each fresh DFS
start is one cluster, and because the outer loop climbs from mast 0 upwards,
the mast that starts a cluster is automatically that cluster's leader.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
PAIR_AND_A_LONER: list[list[int]] = [
    [0, 1, 0],
    [1, 0, 0],
    [0, 0, 0],
]

CHAIN_OF_THREE: list[list[int]] = [
    [0, 1, 0, 0],
    [1, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0],
]

FULLY_LINKED_TRIPLE: list[list[int]] = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0],
]

INTERLEAVED: list[list[int]] = [
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0],
]


def chain_of_masts(masts: int) -> list[list[int]]:
    """Build an n x n link table whose masts form one straight relay chain.

    Args:
        masts: How many masts the chain holds.

    Returns:
        A symmetric table with a zero diagonal where mast i hears mast i + 1.
    """
    table = [[0] * masts for _ in range(masts)]
    for mast in range(masts - 1):
        table[mast][mast + 1] = 1
        table[mast + 1][mast] = 1
    return table


# ---- Your task ----
def survey_clusters(links: list[list[int]]) -> list[tuple[int, int]]:
    """Return one (leader, size) pair per cluster, ascending by leader.

    Args:
        links: A symmetric n x n table of 0s and 1s with a zero diagonal.
            `links[i][j] == 1` means masts i and j hear each other directly.

    Returns:
        One (leader, size) pair per cluster, where leader is the smallest mast
        number in that cluster, sorted ascending by leader. An empty table
        gives an empty list.
    """
    total = len(links)
    visited: set[int] = set()
    clusters: list[tuple[int, int]] = []

    def walk(mast: int) -> int:
        """Mark every mast reachable from `mast` and return how many that was."""
        visited.add(mast)
        reached = 1
        row = links[mast]
        for other in range(total):
            if row[other] == 1 and other not in visited:
                reached += walk(other)
        return reached

    for mast in range(total):
        if mast not in visited:
            clusters.append((mast, walk(mast)))
    return clusters


# ---- Self-check ----
if __name__ == "__main__":
    print(f"no masts at all   : {survey_clusters([])}")
    print(f"one lonely mast   : {survey_clusters([[0]])}")
    print(f"pair and a loner  : {survey_clusters(PAIR_AND_A_LONER)}")
    print(f"chain of three    : {survey_clusters(CHAIN_OF_THREE)}")
    print(f"fully-linked trio : {survey_clusters(FULLY_LINKED_TRIPLE)}")
    print(f"interleaved       : {survey_clusters(INTERLEAVED)}")
    print(f"900-mast chain    : {survey_clusters(chain_of_masts(900))}")

    assert survey_clusters([]) == []
    assert survey_clusters([[0]]) == [(0, 1)]
    assert survey_clusters([[0, 0], [0, 0]]) == [(0, 1), (1, 1)]
    assert survey_clusters(PAIR_AND_A_LONER) == [(0, 2), (2, 1)]
    assert survey_clusters(CHAIN_OF_THREE) == [(0, 3), (3, 1)]
    assert survey_clusters(FULLY_LINKED_TRIPLE) == [(0, 3)]
    assert survey_clusters(INTERLEAVED) == [(0, 2), (1, 2), (4, 1)]
    assert survey_clusters(chain_of_masts(900)) == [(0, 900)]
    print("All checks passed.")
