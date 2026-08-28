"""problem-02-kerb-step-route-solution.py — the route whose worst kerb is smallest.

A market square is paved in blocks, each surveyed to a height in millimetres.
A wheelchair crosses from the north-west corner to the south-east corner,
moving one block at a time, north, south, east or west. Stepping between two
blocks means climbing the difference in their heights.

Nobody cares about the total climb. What matters is the single worst step on
the route, because that is the one that stops the chair. So the cost of a
route is the largest step on it, and the job is to make that as small as
possible.

  gentlest_route   — the smallest possible worst step
  route_within     — is there a route whose every step is at most this?

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

import heapq
from collections import deque

# ---- Given data ----
# Paving-block heights in millimetres, north row first, west column first
SQUARE: list[list[int]] = [
    [12, 14, 15, 62],
    [20, 15, 16, 64],
    [21, 40, 22, 66],
    [23, 42, 20, 21],
]

STEPS: tuple[tuple[int, int], ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))


# ---- Your task ----
def gentlest_route(square: list[list[int]]) -> int:
    """Return the smallest possible worst step from north-west to south-east.

    This is Dijkstra with one change. Normal Dijkstra adds the cost of a step
    to the cost so far. Here the cost of a route is the largest step on it,
    so instead of adding, the relaxation takes whichever is bigger: the worst
    step so far, or the step about to be taken.

    Args:
        square: Block heights, as rows of millimetres. Every row is the same
            length and there is at least one block.

    Returns:
        The largest step on the gentlest route, in millimetres. Zero when the
        square is a single block, because no step is ever taken.
    """
    rows, columns = len(square), len(square[0])
    worst: dict[tuple[int, int], int] = {(0, 0): 0}
    settled: set[tuple[int, int]] = set()
    queue: list[tuple[int, int, int]] = [(0, 0, 0)]

    while queue:
        so_far, row, column = heapq.heappop(queue)
        if (row, column) in settled:
            continue
        settled.add((row, column))
        if (row, column) == (rows - 1, columns - 1):
            return so_far
        for down, across in STEPS:
            next_row, next_column = row + down, column + across
            if not (0 <= next_row < rows and 0 <= next_column < columns):
                continue
            step = abs(square[next_row][next_column] - square[row][column])
            worst_here = max(so_far, step)     # the max, not the sum
            if worst_here < worst.get((next_row, next_column), float("inf")):
                worst[(next_row, next_column)] = worst_here
                heapq.heappush(queue, (worst_here, next_row, next_column))

    raise ValueError("the square is not fully connected, which cannot happen on a grid")


def route_within(square: list[list[int]], limit: int) -> bool:
    """Return whether a route exists where no single step exceeds the limit.

    This is the plain-BFS way to answer the same question, one limit at a
    time. It is the check a binary search over the limit would call.

    Args:
        square: Block heights, as rows of millimetres.
        limit: The largest step the chair will take, in millimetres.

    Returns:
        True when the south-east corner is reachable without ever stepping
        more than `limit`.
    """
    rows, columns = len(square), len(square[0])
    seen = {(0, 0)}
    queue = deque([(0, 0)])
    while queue:
        row, column = queue.popleft()
        if (row, column) == (rows - 1, columns - 1):
            return True
        for down, across in STEPS:
            next_row, next_column = row + down, column + across
            if not (0 <= next_row < rows and 0 <= next_column < columns):
                continue
            if (next_row, next_column) in seen:
                continue
            if abs(square[next_row][next_column] - square[row][column]) <= limit:
                seen.add((next_row, next_column))
                queue.append((next_row, next_column))
    return False


# ---- Self-check ----
if __name__ == "__main__":
    answer = gentlest_route(SQUARE)
    print("block heights in mm")
    for row in SQUARE:
        print("  " + " ".join(f"{height:3d}" for height in row))
    print(f"gentlest route: worst step {answer} mm")

    print()
    print("limit  route?")
    for limit in range(max(answer - 2, 0), answer + 3):
        print(f"{limit:5d}  {route_within(SQUARE, limit)}")

    assert answer == 6
    assert route_within(SQUARE, answer) is True
    assert route_within(SQUARE, answer - 1) is False
    assert gentlest_route([[7]]) == 0
    assert gentlest_route([[0, 100]]) == 100   # one row, one forced step
    assert gentlest_route([[5, 5], [5, 5]]) == 0
    print("All checks passed.")
