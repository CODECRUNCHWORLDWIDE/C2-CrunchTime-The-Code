"""exercise-02-conveyor-reachability-solution.py — where a parcel can end up.

Iterative depth-first search with an explicit stack. The pending work lives in
a plain list on the heap, so the depot's longest belt run — sixty thousand
chutes in the self-check below — costs memory and nothing else. The recursive
spelling of the same walk dies at about a thousand chutes with RecursionError.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
FAN_OUT: list[list[int]] = [
    [1, 2],
    [3],
    [3, 4],
    [],
    [],
]

RESORT_LOOP: list[list[int]] = [
    [1],
    [2],
    [0],
]

DEAD_ENDS: list[list[int]] = [
    [1],
    [],
    [1],
]


def straight_run(chutes: int) -> list[list[int]]:
    """Build a depot that is one straight belt run, chute 0 down to the last.

    Args:
        chutes: How many chutes the run holds.

    Returns:
        A belt table where chute i drops to chute i + 1 and the last is a
        dead end.
    """
    belts: list[list[int]] = [[index + 1] for index in range(chutes - 1)]
    belts.append([])
    return belts


# ---- Your task ----
def reachable_chutes(belts: list[list[int]], start: int) -> list[int]:
    """Return every chute a parcel released at `start` can end up at.

    Args:
        belts: `belts[i]` lists the chutes a parcel drops to directly from
            chute i. One-way: a belt from i to j says nothing about j to i.
        start: The chute the parcel is released into.

    Returns:
        The reachable chute numbers, sorted ascending. `start` is in the list
        only when some belt path leads back to it. An empty depot gives an
        empty list.

    Raises:
        ValueError: If `start` is not a chute in this depot.
    """
    if not belts:
        return []
    if not 0 <= start < len(belts):
        raise ValueError(
            f"no such chute: {start} (this depot has chutes 0 to {len(belts) - 1})"
        )

    reached: set[int] = set()
    stack: list[int] = list(belts[start])
    while stack:
        chute = stack.pop()
        if chute in reached:
            continue
        reached.add(chute)
        stack.extend(belts[chute])
    return sorted(reached)


# ---- Self-check ----
if __name__ == "__main__":
    print(f"empty depot         : {reachable_chutes([], 0)}")
    print(f"fan-out from 0      : {reachable_chutes(FAN_OUT, 0)}")
    print(f"fan-out from 2      : {reachable_chutes(FAN_OUT, 2)}")
    print(f"dead end at chute 1 : {reachable_chutes(DEAD_ENDS, 1)}")
    print(f"re-sort loop from 0 : {reachable_chutes(RESORT_LOOP, 0)}")
    try:
        reachable_chutes(FAN_OUT, 9)
    except ValueError as refusal:
        print(f"chute 9 refused     : {refusal}")

    long_depot = straight_run(60_000)
    far = reachable_chutes(long_depot, 0)
    print(f"60000-chute run     : {len(far)} chutes, first {far[0]}, last {far[-1]}")

    assert reachable_chutes([], 0) == []
    assert reachable_chutes(FAN_OUT, 0) == [1, 2, 3, 4]
    assert reachable_chutes(FAN_OUT, 2) == [3, 4]
    assert reachable_chutes(FAN_OUT, 3) == []
    assert reachable_chutes(DEAD_ENDS, 1) == []
    assert reachable_chutes(DEAD_ENDS, 2) == [1]
    assert reachable_chutes(RESORT_LOOP, 0) == [0, 1, 2]
    assert reachable_chutes(RESORT_LOOP, 1) == [0, 1, 2]
    assert far == list(range(1, 60_000))
    assert reachable_chutes(long_depot, 59_999) == []
    for bad_start in (-1, 5):
        try:
            reachable_chutes(FAN_OUT, bad_start)
        except ValueError as refusal:
            assert str(refusal).startswith(f"no such chute: {bad_start}")
        else:
            raise AssertionError(f"chute {bad_start} should have been refused")
    print("All checks passed.")
