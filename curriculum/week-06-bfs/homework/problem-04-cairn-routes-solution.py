"""problem-04-cairn-routes-solution.py — every shortest way across the fell.

A mountain rescue team keeps a map of cairns and the paths between them.
Before a search they want two things about the quickest way from one cairn to
another: how many different quickest ways there are, and which cairns lie on
at least one of them. The second list is where they post spotters.

One BFS from each end answers both. A cairn is on a quickest route exactly
when its distance from one end plus its distance from the other adds up to
the length of the whole route.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import deque

# ---- Given data ----
# Nine cairns on the open fell, laid out three by three, plus two on the far
# side of a river with no crossing.
PATHS: dict[str, list[str]] = {
    "ALDER": ["BIRCH", "DAMSON"],
    "BIRCH": ["ALDER", "CEDAR", "ELDER"],
    "CEDAR": ["BIRCH", "FIRTH"],
    "DAMSON": ["ALDER", "ELDER", "GORSE"],
    "ELDER": ["BIRCH", "DAMSON", "FIRTH", "HOLLY"],
    "FIRTH": ["CEDAR", "ELDER", "IVY"],
    "GORSE": ["DAMSON", "HOLLY"],
    "HOLLY": ["ELDER", "GORSE", "IVY"],
    "IVY": ["FIRTH", "HOLLY"],
    "JUNIPER": ["KELD"],
    "KELD": ["JUNIPER"],
}


# ---- Your task ----
def steps_from(paths: dict[str, list[str]], start: str) -> dict[str, int]:
    """Return the path count from `start` to every cairn it can reach.

    Args:
        paths: The map. Each cairn maps to the cairns a path joins it to.
        start: The cairn to measure from.

    Returns:
        A dict mapping each reachable cairn to its path count. `start` maps
        to 0. Cairns on the far side of the river are simply absent.
    """
    steps = {start: 0}
    queue = deque([start])
    while queue:
        cairn = queue.popleft()
        for neighbour in paths.get(cairn, ()):
            if neighbour not in steps:
                steps[neighbour] = steps[cairn] + 1
                queue.append(neighbour)
    return steps


def route_spread(
    paths: dict[str, list[str]], start: str, finish: str
) -> tuple[int, list[str]] | None:
    """Return how many quickest routes there are, and which cairns they use.

    Args:
        paths: The map.
        start: The cairn the team sets off from.
        finish: The cairn they are heading for.

    Returns:
        A pair: the number of different quickest routes, and every cairn
        lying on at least one of them, sorted A to Z. When `start` and
        `finish` are the same cairn there is one route of no steps and it
        uses that cairn alone. None when no path joins the two.

    Raises:
        KeyError: If either cairn is missing from the map.
    """
    for role, cairn in (("start", start), ("finish", finish)):
        if cairn not in paths:
            raise KeyError(f"{role} cairn {cairn!r} is not on the map")

    from_start = steps_from(paths, start)
    if finish not in from_start:
        return None
    from_finish = steps_from(paths, finish)
    length = from_start[finish]

    routes = {start: 1}
    queue = deque([start])
    seen = {start}
    while queue:
        cairn = queue.popleft()
        for neighbour in paths[cairn]:
            if from_start[neighbour] != from_start[cairn] + 1:
                continue
            routes[neighbour] = routes.get(neighbour, 0) + routes[cairn]
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)

    on_route = sorted(
        cairn
        for cairn, out in from_start.items()
        if out + from_finish.get(cairn, length + 1) == length
    )
    return routes[finish], on_route


# ---- Self-check ----
if __name__ == "__main__":
    for start, finish in (("ALDER", "IVY"), ("ALDER", "FIRTH"), ("ALDER", "ALDER")):
        spread = route_spread(PATHS, start, finish)
        print(f"{start} to {finish}: {spread[0]} quickest routes over {len(spread[1])} cairns")
        print(f"  spotters at: {', '.join(spread[1])}")
    print(f"ALDER to KELD: {route_spread(PATHS, 'ALDER', 'KELD')}")

    # Corner to opposite corner on a three-by-three lattice: four steps, and
    # every one of the six orders of two easts and two souths is quickest.
    assert route_spread(PATHS, "ALDER", "IVY") == (
        6,
        [
            "ALDER",
            "BIRCH",
            "CEDAR",
            "DAMSON",
            "ELDER",
            "FIRTH",
            "GORSE",
            "HOLLY",
            "IVY",
        ],
    )

    # Three steps to FIRTH, three ways to order them, and the three cairns
    # in the far corner are not on any of them.
    count, spotters = route_spread(PATHS, "ALDER", "FIRTH")
    assert count == 3
    assert spotters == ["ALDER", "BIRCH", "CEDAR", "DAMSON", "ELDER", "FIRTH"]
    assert "GORSE" not in spotters and "HOLLY" not in spotters

    # Standing still is one route over one cairn.
    assert route_spread(PATHS, "ALDER", "ALDER") == (1, ["ALDER"])
    # Neighbours: one route, two cairns.
    assert route_spread(PATHS, "ALDER", "BIRCH") == (1, ["ALDER", "BIRCH"])
    # The river has no crossing.
    assert route_spread(PATHS, "ALDER", "KELD") is None

    try:
        route_spread(PATHS, "ALDER", "LARCH")
    except KeyError as error:
        assert "is not on the map" in str(error)
    else:
        raise AssertionError("expected KeyError")

    print("All checks passed.")
