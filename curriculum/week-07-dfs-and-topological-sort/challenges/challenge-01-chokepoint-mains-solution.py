"""challenge-01-chokepoint-mains-solution.py — the mains a city cannot lose.

A chokepoint is a water main whose failure would cut some pumping station off
from a station it can reach today. One depth-first walk over the network finds
every one of them: one look at every station and one look at every main, and
then it is done.

The walk is iterative on purpose. Fifty thousand stations laid in a line is
fifty times CPython's default recursion limit, so a recursive version dies
before it answers.

Beside the real answer sits `_chokepoints_the_slow_way`, which pulls out one
main at a time and counts how many pieces the network falls into. It is far
too slow for a real network and it is obviously correct, which is exactly what
a reference implementation is for. The self-checks run both over seeded random
networks and demand that they agree.
"""

from __future__ import annotations

import random
from collections.abc import Iterator

UNSEEN = -1


def survey_chokepoints(
    stations: int, mains: list[tuple[int, int]]
) -> tuple[list[tuple[int, int]], int]:
    """Find every chokepoint main, and the pieces left if they all failed.

    Args:
        stations: How many pumping stations the network has. They are
            numbered 0 to stations - 1.
        mains: The maintenance log, one (a, b) pair per pipe. The same pair
            may be listed twice, because two pipes really were laid side by
            side, and either station may be written first.

    Returns:
        (chokepoints, pieces). chokepoints holds every main whose failure
        would cut some station off from a station it can currently reach,
        each written (a, b) with a < b, the whole list sorted ascending.
        pieces is how many separate networks would be left if every
        chokepoint failed at once.

    Raises:
        ValueError: a main names a station this network does not have.
    """
    for a, b in mains:
        for station in (a, b):
            if not 0 <= station < stations:
                if stations == 0:
                    raise ValueError(
                        f"main {(a, b)} names station {station}, "
                        "but the network has no stations"
                    )
                raise ValueError(
                    f"main {(a, b)} names station {station}, "
                    f"but the network's stations are 0..{stations - 1}"
                )
    if stations == 0:
        return [], 0

    # Every pipe gets a number. Both ends of pipe 7 remember that they are
    # pipe 7, which is how a pair listed twice stays two pipes.
    pipes_at: list[list[tuple[int, int]]] = [[] for _ in range(stations)]
    for pipe, (a, b) in enumerate(mains):
        pipes_at[a].append((b, pipe))
        pipes_at[b].append((a, pipe))

    reached_at = [UNSEEN] * stations  # when the walk first stood here
    lowest = [0] * stations  # the earliest time this station's side can reach
    clock = 0
    pieces_today = 0
    chokepoints: list[tuple[int, int]] = []

    for start in range(stations):
        if reached_at[start] != UNSEEN:
            continue
        pieces_today += 1
        reached_at[start] = lowest[start] = clock
        clock += 1
        # Each stack entry is: the station, the pipe we walked in by, and an
        # iterator over the pipes at that station we have not tried yet.
        walk: list[tuple[int, int, Iterator[tuple[int, int]]]] = [
            (start, -1, iter(pipes_at[start]))
        ]
        while walk:
            station, came_in_by, untried = walk[-1]
            went_deeper = False
            for nxt, pipe in untried:
                if pipe == came_in_by:
                    continue  # the one pipe we arrived on, not a way back
                if reached_at[nxt] == UNSEEN:
                    reached_at[nxt] = lowest[nxt] = clock
                    clock += 1
                    walk.append((nxt, pipe, iter(pipes_at[nxt])))
                    went_deeper = True
                    break
                if reached_at[nxt] < lowest[station]:
                    lowest[station] = reached_at[nxt]
            if went_deeper:
                continue
            walk.pop()
            if walk:
                behind = walk[-1][0]
                if lowest[station] < lowest[behind]:
                    lowest[behind] = lowest[station]
                if lowest[station] > reached_at[behind]:
                    ends = (behind, station) if behind < station else (station, behind)
                    chokepoints.append(ends)

    chokepoints.sort()
    # Pulling one chokepoint out splits exactly one piece in two, so the
    # network today plus one piece per chokepoint is the whole answer.
    return chokepoints, pieces_today + len(chokepoints)


def _piece_count(stations: int, mains: list[tuple[int, int]]) -> int:
    """Count the separate pieces of a network, the plain way.

    Args:
        stations: How many pumping stations the network has.
        mains: The pipes that are still standing.

    Returns:
        How many groups of stations there are, where two stations are in the
        same group when water can get from one to the other.
    """
    linked: list[list[int]] = [[] for _ in range(stations)]
    for a, b in mains:
        linked[a].append(b)
        linked[b].append(a)
    seen = [False] * stations
    pieces = 0
    for start in range(stations):
        if seen[start]:
            continue
        pieces += 1
        seen[start] = True
        stack = [start]
        while stack:
            station = stack.pop()
            for nxt in linked[station]:
                if not seen[nxt]:
                    seen[nxt] = True
                    stack.append(nxt)
    return pieces


def _chokepoints_the_slow_way(
    stations: int, mains: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    """Find chokepoints by shutting off one main at a time and looking.

    This is the definition typed out. It re-walks the whole network once per
    main, so it is hopeless on a real one — and unarguable on a small one,
    which is why the self-checks measure the fast answer against it.

    Args:
        stations: How many pumping stations the network has.
        mains: The maintenance log.

    Returns:
        The chokepoints, each (a, b) with a < b, sorted ascending.
    """
    whole = _piece_count(stations, mains)
    found: list[tuple[int, int]] = []
    for index, (a, b) in enumerate(mains):
        without = mains[:index] + mains[index + 1 :]
        if _piece_count(stations, without) > whole:
            found.append((a, b) if a < b else (b, a))
    return sorted(found)


def _random_network(rng: random.Random) -> tuple[int, list[tuple[int, int]]]:
    """Build one small network to test with, duplicates and all.

    Args:
        rng: The seeded source of randomness, so every run is the same run.

    Returns:
        (stations, mains) — between one and seven stations, up to ten pipes,
        no pipe from a station to itself.
    """
    stations = rng.randint(1, 7)
    mains: list[tuple[int, int]] = []
    for _ in range(rng.randint(0, 10)):
        a = rng.randrange(stations)
        b = rng.randrange(stations)
        if a != b:
            mains.append((a, b))
    return stations, mains


if __name__ == "__main__":
    cases: list[tuple[str, int, list[tuple[int, int]]]] = [
        ("empty city", 0, []),
        ("single station", 1, []),
        ("no mains at all", 3, []),
        ("short chain", 4, [(0, 1), (1, 2), (2, 3)]),
        ("one ring", 4, [(0, 1), (1, 2), (2, 3), (3, 0)]),
        ("twin mains", 2, [(0, 1), (1, 0)]),
        ("barbell", 6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (2, 3)]),
        ("already split", 5, [(0, 1), (2, 3), (3, 4), (4, 2)]),
    ]
    print(f"{'network':<16}{'chokepoints':<26}pieces")
    for name, stations, mains in cases:
        chokepoints, pieces = survey_chokepoints(stations, mains)
        print(f"{name:<16}{str(chokepoints):<26}{pieces}")

    assert survey_chokepoints(0, []) == ([], 0)
    assert survey_chokepoints(1, []) == ([], 1)
    assert survey_chokepoints(3, []) == ([], 3)
    assert survey_chokepoints(4, [(0, 1), (1, 2), (2, 3)]) == (
        [(0, 1), (1, 2), (2, 3)],
        4,
    )
    assert survey_chokepoints(4, [(0, 1), (1, 2), (2, 3), (3, 0)]) == ([], 1)
    assert survey_chokepoints(2, [(0, 1), (1, 0)]) == ([], 1)
    assert survey_chokepoints(
        6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (2, 3)]
    ) == ([(2, 3)], 2)
    assert survey_chokepoints(5, [(0, 1), (2, 3), (3, 4), (4, 2)]) == ([(0, 1)], 3)

    rng = random.Random(20260826)
    trials = 300
    for _ in range(trials):
        stations, mains = _random_network(rng)
        fast, pieces = survey_chokepoints(stations, mains)
        slow = _chokepoints_the_slow_way(stations, mains)
        assert fast == slow, (stations, mains, fast, slow)
        standing = [
            (a, b) for a, b in mains if (min(a, b), max(a, b)) not in set(slow)
        ]
        assert pieces == _piece_count(stations, standing), (stations, mains)
    print(f"random cross-check : {trials} networks, fast answer matches the slow one")

    long_chain = [(i, i + 1) for i in range(49_999)]
    chokepoints, pieces = survey_chokepoints(50_000, long_chain)
    assert len(chokepoints) == 49_999
    assert pieces == 50_000
    print(f"50000-station chain: {len(chokepoints)} chokepoints, {pieces} pieces")

    try:
        survey_chokepoints(4, [(0, 1), (0, 7)])
    except ValueError as error:
        print(f"out-of-range main  : {error}")
    else:  # pragma: no cover - the call above always raises
        raise AssertionError("a main outside the station numbers must be refused")

    print("All checks passed.")
