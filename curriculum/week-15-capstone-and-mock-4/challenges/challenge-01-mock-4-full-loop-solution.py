"""challenge-01-mock-4-full-loop-solution.py - the overnight leak survey.

The worked answer to the fallback coding problem inside Mock #4. Read it after
your clock has stopped, not before.

A water utility surveys a rectangular district overnight. Every street block
carries a pressure sensor and the survey comes back as a grid of readings in
kilopascals relative to nominal, so a reading can be negative. A block is wet
when its reading is strictly below a threshold, and wet blocks touching
horizontally or vertically form one leak zone.

A zone with a block on the outer border of the survey may continue into streets
nobody measured, so the crew cannot bound it and ignores it however large it is.
Every other zone is interior and dispatchable. Report how many interior zones
there are and how many blocks are in the largest.

Two things carry the answer, and both are worth saying out loud in a round:

  * mark a block on enqueue, not on pop - a block with two wet neighbours is
    otherwise queued twice and its zone over-counted;
  * the border flag belongs to the zone, not to the seed - accumulate it across
    the whole walk, then test it once at the end.

The traversal is iterative on purpose. A single zone can snake through most of a
1200x1200 grid, which is hundreds of thousands of blocks deep, and Python's
recursion limit is 1000.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from collections import deque


def survey_leak_zones(pressure: list[list[int]], threshold: int) -> tuple[int, int]:
    """Count interior leak zones and size the largest. O(rows*cols) time and space.

    A zone is a 4-connected group of blocks reading strictly below `threshold`.
    A zone is interior when none of its blocks lies on the grid's outer border.
    `pressure` is never modified.
    """
    if not pressure or not pressure[0]:
        return (0, 0)

    rows, cols = len(pressure), len(pressure[0])
    visited = [[False] * cols for _ in range(rows)]
    interior_zones = 0
    largest = 0

    for seed_r in range(rows):
        for seed_c in range(cols):
            if visited[seed_r][seed_c] or pressure[seed_r][seed_c] >= threshold:
                continue

            # Walk the entire zone first; only then decide whether it counts.
            frontier = deque([(seed_r, seed_c)])
            visited[seed_r][seed_c] = True
            blocks = 0
            reaches_border = False

            while frontier:
                r, c = frontier.popleft()
                blocks += 1
                if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                    reaches_border = True
                for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                    if (
                        0 <= nr < rows
                        and 0 <= nc < cols
                        and not visited[nr][nc]
                        and pressure[nr][nc] < threshold
                    ):
                        visited[nr][nc] = True   # mark on enqueue, not on pop
                        frontier.append((nr, nc))

            if not reaches_border:
                interior_zones += 1
                largest = max(largest, blocks)

    return (interior_zones, largest)


if __name__ == "__main__":
    district = [
        [10, 10, 10, 50, 50, 50],
        [10, 50, 50, 10, 10, 50],
        [50, 50, 50, 10, 50, 50],
        [50, 10, 50, 50, 50, 50],
        [50, 50, 50, 50, 50, 50],
    ]
    snapshot = [row[:] for row in district]
    assert survey_leak_zones(district, 30) == (2, 3)
    assert district == snapshot, "the caller's survey must come back untouched"

    # The zone seeded at (1,1) leaks out to the last column: unbounded.
    assert survey_leak_zones(
        [
            [90, 90, 90, 90, 90],
            [90, 1, 1, 90, 90],
            [90, 90, 1, 90, 90],
            [90, 90, 1, 1, 1],
            [90, 90, 90, 90, 90],
        ],
        10,
    ) == (0, 0)

    # Negative and zero readings are ordinary and both wet.
    assert survey_leak_zones(
        [[80, 80, 80, 80], [80, -5, 0, 80], [80, 80, 80, 80]], 10
    ) == (1, 2)

    # Strictly below: a reading equal to the threshold is dry.
    assert survey_leak_zones([[9, 9, 9], [9, 10, 9], [9, 9, 9]], 10) == (0, 0)

    # No grid narrower than three blocks can hold an interior zone.
    assert survey_leak_zones([[5, 5], [5, 5]], 10) == (0, 0)

    # Three separate one-block zones: count 3, largest 1.
    assert survey_leak_zones(
        [[8, 8, 8, 8, 8, 8, 8], [8, 2, 8, 2, 8, 2, 8], [8, 8, 8, 8, 8, 8, 8]], 5
    ) == (3, 1)

    assert survey_leak_zones([], 0) == (0, 0)
    assert survey_leak_zones([[]], 0) == (0, 0)
    print("All checks passed.")
