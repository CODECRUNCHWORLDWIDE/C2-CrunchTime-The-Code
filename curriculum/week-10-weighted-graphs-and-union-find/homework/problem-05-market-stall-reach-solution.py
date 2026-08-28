"""problem-05-market-stall-reach-solution.py — every pair of stalls at once.

A covered market has numbered stalls joined by aisles. Pushing a loaded
barrow along an aisle takes a known number of seconds, and an aisle is
walkable both ways at the same cost.

The market wants the quietest pitch: the stall from which the fewest other
stalls are within a barrow-push budget. That question is about every pair of
stalls, not about one starting point, so it is answered once for the whole
market rather than one search per stall.

  push_times   — the seconds between every pair of stalls
  quietest     — the stall with the fewest neighbours inside the budget

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
STALL_COUNT = 7

# (stall, stall, seconds to push a barrow along that aisle, both ways)
AISLES: list[tuple[int, int, int]] = [
    (0, 1, 10),
    (1, 2, 10),
    (2, 3, 10),
    (3, 4, 10),
    (4, 5, 10),
    (1, 4, 5),
    (5, 6, 10),
    (0, 6, 20),
    (2, 6, 45),
]

BUDGET = 10


# ---- Your task ----
def push_times(stall_count: int, aisles: list[tuple[int, int, int]]) -> list[list[float]]:
    """Return the shortest push time between every pair of stalls.

    The table starts with the aisles themselves and is then improved once per
    stall. After the round for stall `middle`, every entry is the best time
    that uses only stalls up to `middle` in the middle of the route. After the
    last round, every stall has been allowed in the middle, so the table is
    finished.

    Args:
        stall_count: How many stalls the market has, numbered from 0.
        aisles: Every aisle, as (stall, stall, seconds).

    Returns:
        A square table where times[a][b] is the seconds from a to b, 0 on the
        diagonal, and float("inf") where no route exists.
    """
    times: list[list[float]] = [
        [0.0 if here == there else float("inf") for there in range(stall_count)]
        for here in range(stall_count)
    ]
    for here, there, seconds in aisles:
        times[here][there] = min(times[here][there], float(seconds))
        times[there][here] = times[here][there]

    for middle in range(stall_count):
        for here in range(stall_count):
            through = times[here][middle]
            if through == float("inf"):
                continue                     # nothing to gain by going via middle
            for there in range(stall_count):
                if through + times[middle][there] < times[here][there]:
                    times[here][there] = through + times[middle][there]
    return times


def neighbours_within(times: list[list[float]], stall: int, budget: int) -> int:
    """Return how many other stalls sit inside the budget from this one.

    Args:
        times: The table push_times returned.
        stall: The stall to count from.
        budget: The barrow-push budget in seconds.

    Returns:
        The count of other stalls whose push time is at most the budget. The
        stall itself is never counted.
    """
    return sum(
        1
        for there, seconds in enumerate(times[stall])
        if there != stall and seconds <= budget
    )


def quietest(stall_count: int, aisles: list[tuple[int, int, int]], budget: int) -> tuple[int, int]:
    """Return the stall with the fewest neighbours inside the budget.

    Args:
        stall_count: How many stalls the market has, numbered from 0.
        aisles: Every aisle, as (stall, stall, seconds).
        budget: The barrow-push budget in seconds.

    Returns:
        (stall, count). Where two stalls tie on count the higher-numbered one
        wins, because the far end of the market is the quieter pitch.
    """
    times = push_times(stall_count, aisles)
    best_stall, best_count = 0, neighbours_within(times, 0, budget)
    for stall in range(1, stall_count):
        count = neighbours_within(times, stall, budget)
        if count <= best_count:              # <=, so a later stall wins a tie
            best_stall, best_count = stall, count
    return best_stall, best_count


# ---- Self-check ----
if __name__ == "__main__":
    times = push_times(STALL_COUNT, AISLES)
    print("push times in seconds")
    print("      " + "".join(f"{there:6d}" for there in range(STALL_COUNT)))
    for here in range(STALL_COUNT):
        cells = "".join(
            "   inf" if seconds == float("inf") else f"{int(seconds):6d}"
            for seconds in times[here]
        )
        print(f"{here:4d}  {cells}")

    print()
    print(f"stalls within {BUDGET}s")
    for stall in range(STALL_COUNT):
        print(f"  stall {stall}: {neighbours_within(times, stall, BUDGET)}")
    print(f"quietest pitch: {quietest(STALL_COUNT, AISLES, BUDGET)}")

    assert times[0][0] == 0
    assert times[0][4] == 15                 # 0-1-4 beats 0-1-2-3-4
    assert times[2][5] == 25                 # 2-1-4-5
    assert times[2][6] == 35                 # 2-1-4-5-6 beats the direct 45
    assert times[3][6] == 30
    assert all(times[a][b] == times[b][a] for a in range(STALL_COUNT) for b in range(STALL_COUNT))
    # Stalls 0 and 6 both have one neighbour inside 10s; the far end wins.
    assert neighbours_within(times, 0, BUDGET) == 1
    assert quietest(STALL_COUNT, AISLES, BUDGET) == (6, 1)
    assert quietest(STALL_COUNT, AISLES, 30) == (6, 5)
    assert quietest(STALL_COUNT, AISLES, 1000) == (6, 6)

    lonely = push_times(2, [])
    assert lonely[0][1] == float("inf")
    assert quietest(2, [], 5) == (1, 0)
    print("All checks passed.")
