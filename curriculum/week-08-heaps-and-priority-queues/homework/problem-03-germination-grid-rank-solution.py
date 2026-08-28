"""problem-03-germination-grid-rank-solution.py — the seventh-lowest germination count.

A seed lab runs four trays of four slots. Every tray's counts rise from left to
right, and every slot's counts rise from tray to tray. The lab wants the k-th
lowest count in the whole grid and, because two slots can tie, the slot it came
from.

Each tray is an already-sorted source, so a heap holding one pending count per
tray merges them and stops after k pops instead of sorting all sixteen.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
# Rows are trays; each row rises left to right, each column rises top to bottom.
GRID: list[list[int]] = [
    [2, 6, 11, 17],
    [5, 6, 14, 21],
    [9, 13, 15, 26],
    [12, 19, 23, 30],
]

WANTED_RANK = 7


# ---- Your task ----
def nth_lowest(grid: list[list[int]], rank: int) -> tuple[int, int, int]:
    """Return the rank-th lowest count in the grid, with the slot it came from.

    Args:
        grid: Trays of counts. Each tray is ascending. Trays may differ in
            length, and a tray may be empty.
        rank: Which count to return, counting from 1. Equal counts each take a
            place of their own, so a grid of sixteen slots has sixteen ranks.

    Returns:
        (count, tray index, slot index). Where two slots hold the same count,
        the lower tray comes first, and within a tray the lower slot.

    Raises:
        ValueError: When `rank` is below 1 or above the number of slots.
    """
    slots = sum(len(tray) for tray in grid)
    if rank < 1 or rank > slots:
        raise ValueError(f"rank {rank} is outside 1..{slots}")

    pending = [(tray[0], index, 0) for index, tray in enumerate(grid) if tray]
    heapq.heapify(pending)
    for _ in range(rank - 1):
        count, tray_index, slot_index = heapq.heappop(pending)
        if slot_index + 1 < len(grid[tray_index]):
            heapq.heappush(
                pending,
                (grid[tray_index][slot_index + 1], tray_index, slot_index + 1),
            )
    return pending[0]


def merged_counts(grid: list[list[int]]) -> list[int]:
    """Return every count in the grid, lowest first.

    Args:
        grid: Trays of counts, each tray ascending.

    Returns:
        All counts in one ascending list, duplicates kept.
    """
    return [nth_lowest(grid, rank)[0] for rank in range(1, sum(map(len, grid)) + 1)]


def slot_of_rank(grid: list[list[int]], rank: int) -> str:
    """Return a readable label for the slot at a rank.

    Args:
        grid: Trays of counts, each tray ascending.
        rank: Which count to name, counting from 1.

    Returns:
        A string like "tray 4 slot 1", counting both from 1.
    """
    _, tray_index, slot_index = nth_lowest(grid, rank)
    return f"tray {tray_index + 1} slot {slot_index + 1}"


# ---- Self-check ----
if __name__ == "__main__":
    count, tray_index, slot_index = nth_lowest(GRID, WANTED_RANK)
    print(f"grid slots: {sum(len(tray) for tray in GRID)}")
    print(f"rank {WANTED_RANK}: count {count} from {slot_of_rank(GRID, WANTED_RANK)}")
    print(f"lowest : {nth_lowest(GRID, 1)}")
    print(f"highest: {nth_lowest(GRID, 16)}")
    print("first eight ranks:")
    for rank in range(1, 9):
        value, tray, slot = nth_lowest(GRID, rank)
        print(f"  rank {rank}: {value:2d}  tray {tray + 1} slot {slot + 1}")

    print(f"merged: {merged_counts(GRID)}")
    print(f"ragged trays: {nth_lowest([[3], [], [1, 8]], 2)}")
    try:
        nth_lowest(GRID, 0)
    except ValueError as error:
        print(f"rank 0: ValueError: {error}")
    try:
        nth_lowest(GRID, 17)
    except ValueError as error:
        print(f"rank 17: ValueError: {error}")

    assert (count, tray_index, slot_index) == (12, 3, 0)
    assert nth_lowest(GRID, 1) == (2, 0, 0)
    assert nth_lowest(GRID, 3) == (6, 0, 1)
    assert nth_lowest(GRID, 4) == (6, 1, 1)  # the tie goes to the lower tray
    assert nth_lowest(GRID, 16) == (30, 3, 3)
    assert merged_counts(GRID) == sorted(value for tray in GRID for value in tray)
    assert nth_lowest([[3], [], [1, 8]], 2) == (3, 0, 0)
    print("All checks passed.")
