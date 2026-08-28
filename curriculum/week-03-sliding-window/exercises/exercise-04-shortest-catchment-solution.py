"""exercise-04-shortest-catchment-solution.py — the shortest catchment run.

A reservoir logs daily inflow in megalitres. Before a maintenance drawdown the
operator must bank a quota and wants the shortest run of consecutive days that
delivers it.

This is the shrinking shape: grow the window until the quota is met, then trim
from the left while it is still met, recording the window before each trim.
Non-negative readings are what make the trim safe — dropping a day can only
lower the total, never raise it.

The self-checks are the starter's, unchanged. When they all pass the file
prints "All checks passed."
"""


def shortest_catchment(inflow: list[int], quota: int) -> tuple[int, int] | None:
    """Return the shortest run of days whose inflow reaches the quota.

    Args:
        inflow: Daily inflow in megalitres, in date order. Never negative.
        quota: The megalitres that must be banked.

    Returns:
        (start, days) for the shortest qualifying run. Ties go to the run with
        the largest total, then to the earlier start. None when no run of any
        length reaches the quota.
    """
    left = 0
    running = 0
    best: tuple[int, int, int] | None = None

    for right, litres in enumerate(inflow):
        running += litres
        while running >= quota:
            # Shorter wins; then bigger total; then earlier start. Negating the
            # total lets one tuple comparison say all three rules at once.
            candidate = (right - left + 1, -running, left)
            if best is None or candidate < best:
                best = candidate
            running -= inflow[left]
            left += 1

    if best is None:
        return None
    days, _, start = best
    return (start, days)


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[int], int]] = [
        ([4, 6, 1, 7, 8], 10),
        ([3, 1, 4, 1, 5, 9, 2], 11),
        ([0, 0, 12, 0], 12),
        ([2, 3, 4], 9),
        ([1, 1, 1], 10),
        ([], 1),
    ]
    for inflow, quota in cases:
        answer = shortest_catchment(inflow, quota)
        if answer is None:
            print(f"quota {quota:>2}  log {str(inflow):<22} -> None")
        else:
            start, days = answer
            run = inflow[start : start + days]
            print(f"quota {quota:>2}  log {str(inflow):<22} -> days {start}..{start + days - 1} = {run}, total {sum(run)}")
    print()

    assert shortest_catchment([4, 6, 1, 7, 8], 10) == (3, 2)
    assert shortest_catchment([3, 1, 4, 1, 5, 9, 2], 11) == (4, 2)
    assert shortest_catchment([0, 0, 12, 0], 12) == (2, 1)
    assert shortest_catchment([2, 3, 4], 9) == (0, 3)
    assert shortest_catchment([1, 1, 1], 10) is None
    assert shortest_catchment([], 1) is None

    # Every answer really does reach the quota, and nothing shorter does.
    for inflow, quota in cases:
        answer = shortest_catchment(inflow, quota)
        if answer is None:
            assert all(
                sum(inflow[i:j]) < quota
                for i in range(len(inflow))
                for j in range(i + 1, len(inflow) + 1)
            )
            continue
        start, days = answer
        assert sum(inflow[start : start + days]) >= quota
        for i in range(len(inflow)):
            for j in range(i + 1, len(inflow) + 1):
                if sum(inflow[i:j]) >= quota:
                    assert j - i >= days

    print("All checks passed.")
