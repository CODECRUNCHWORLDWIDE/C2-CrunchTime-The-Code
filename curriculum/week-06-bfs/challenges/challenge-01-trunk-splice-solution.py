"""challenge-01-trunk-splice-solution.py — where to cut a trunk cable in half.

A telephone trunk network of street cabinets. A fault has to be traced from
the west end to the east end, and the crew wants to start at the cabinet in
the middle of the shortest route: whichever cabinet sits exactly half the
hops from the west end and the rest of the way to the east end.

Two searches do it. One from each end. A cabinet is on some shortest route
exactly when its two distances add up to the length of the whole route.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import deque
from typing import NamedTuple

# ---- Given data ----
# Cabinets and the trunks between them. Trunks carry both ways.
TRUNKS: dict[str, list[str]] = {
    "ABBOT": ["BEDE", "CULVER"],
    "BEDE": ["ABBOT", "DRAYTON", "ELMET"],
    "CULVER": ["ABBOT", "ELMET", "FENWICK"],
    "DRAYTON": ["BEDE", "GARROW"],
    "ELMET": ["BEDE", "CULVER", "GARROW", "HORNBY"],
    "FENWICK": ["CULVER", "HORNBY"],
    "GARROW": ["DRAYTON", "ELMET", "IVEGATE"],
    "HORNBY": ["ELMET", "FENWICK", "IVEGATE"],
    "IVEGATE": ["GARROW", "HORNBY"],
    "KEELBY": ["LOWTHER"],
    "LOWTHER": ["KEELBY"],
}


class Splice(NamedTuple):
    """Where to cut, and how long the route is."""

    hops: int
    midpoint: str


# ---- Your task ----
def hops_from(trunks: dict[str, list[str]], start: str) -> dict[str, int]:
    """Return the trunk count from `start` to every cabinet it can reach.

    Args:
        trunks: The trunk map. Each cabinet maps to the cabinets it is
            joined to.
        start: The cabinet to measure from.

    Returns:
        A dict mapping each reachable cabinet to its trunk count. `start`
        maps to 0. Cabinets on another island of the network are absent.
    """
    hops = {start: 0}
    queue = deque([start])
    while queue:
        cabinet = queue.popleft()
        for neighbour in trunks.get(cabinet, ()):
            if neighbour not in hops:
                hops[neighbour] = hops[cabinet] + 1
                queue.append(neighbour)
    return hops


def trunk_splice(trunks: dict[str, list[str]], west: str, east: str) -> Splice | None:
    """Return the shortest route's length and the cabinet at its midpoint.

    The midpoint is the cabinet sitting `hops // 2` trunks from `west` and
    the remaining `hops - hops // 2` from `east`, on some shortest route. If
    more than one cabinet qualifies, the earlier name A to Z is chosen, so
    two crews reading the same map pick the same cabinet.

    Args:
        trunks: The trunk map.
        west: The cabinet at the west end of the trace.
        east: The cabinet at the east end.

    Returns:
        A `Splice`, or None when no run of trunks joins the two ends. When
        `west` and `east` are the same cabinet the route is 0 hops long and
        that cabinet is its own midpoint.

    Raises:
        ValueError: If either cabinet is missing from the trunk map.
    """
    for name, cabinet in (("west", west), ("east", east)):
        if cabinet not in trunks:
            raise ValueError(f"{name} end {cabinet!r} is not on the trunk map")

    from_west = hops_from(trunks, west)
    if east not in from_west:
        return None
    from_east = hops_from(trunks, east)
    hops = from_west[east]
    half = hops // 2

    midpoint = min(
        cabinet
        for cabinet, west_hops in from_west.items()
        if west_hops == half and from_east.get(cabinet) == hops - half
    )
    return Splice(hops=hops, midpoint=midpoint)


def on_a_shortest_route(
    trunks: dict[str, list[str]], west: str, east: str
) -> list[str]:
    """Return every cabinet lying on at least one shortest route, sorted.

    Args:
        trunks: The trunk map.
        west: The cabinet at the west end.
        east: The cabinet at the east end.

    Returns:
        The cabinets whose two distances add up to the route length, A to Z.
        An empty list when the two ends are not joined.

    Raises:
        ValueError: If either cabinet is missing from the trunk map.
    """
    for name, cabinet in (("west", west), ("east", east)):
        if cabinet not in trunks:
            raise ValueError(f"{name} end {cabinet!r} is not on the trunk map")

    from_west = hops_from(trunks, west)
    if east not in from_west:
        return []
    from_east = hops_from(trunks, east)
    hops = from_west[east]
    return sorted(
        cabinet
        for cabinet, west_hops in from_west.items()
        if west_hops + from_east.get(cabinet, hops + 1) == hops
    )


# ---- Self-check ----
if __name__ == "__main__":
    splice = trunk_splice(TRUNKS, "ABBOT", "IVEGATE")
    print(f"ABBOT to IVEGATE : {splice.hops} hops, splice at {splice.midpoint}")
    print(f"on a shortest route: {', '.join(on_a_shortest_route(TRUNKS, 'ABBOT', 'IVEGATE'))}")
    print(f"ABBOT to KEELBY  : {trunk_splice(TRUNKS, 'ABBOT', 'KEELBY')}")
    print(f"ABBOT to ABBOT   : {trunk_splice(TRUNKS, 'ABBOT', 'ABBOT')}")

    assert splice == Splice(hops=4, midpoint="DRAYTON")
    assert on_a_shortest_route(TRUNKS, "ABBOT", "IVEGATE") == [
        "ABBOT",
        "BEDE",
        "CULVER",
        "DRAYTON",
        "ELMET",
        "FENWICK",
        "GARROW",
        "HORNBY",
        "IVEGATE",
    ]

    # An even route has a true middle, so turning the trace around finds the
    # same cabinet. DRAYTON and ELMET are both two hops from either end;
    # DRAYTON wins because D comes before E.
    assert trunk_splice(TRUNKS, "IVEGATE", "ABBOT") == Splice(4, "DRAYTON")

    # An odd route does not. 3 // 2 == 1, so the midpoint sits one hop from
    # the west end and two from the east — and that depends on which end is
    # called west.
    assert trunk_splice(TRUNKS, "ABBOT", "GARROW") == Splice(3, "BEDE")
    assert trunk_splice(TRUNKS, "GARROW", "ABBOT") == Splice(3, "DRAYTON")

    # No route at all: the second island is not joined to the first.
    assert trunk_splice(TRUNKS, "ABBOT", "KEELBY") is None
    assert on_a_shortest_route(TRUNKS, "ABBOT", "KEELBY") == []

    # A cabinet is its own midpoint over a route of no hops.
    assert trunk_splice(TRUNKS, "ABBOT", "ABBOT") == Splice(0, "ABBOT")
    assert trunk_splice(TRUNKS, "KEELBY", "LOWTHER") == Splice(1, "KEELBY")

    try:
        trunk_splice(TRUNKS, "ABBOT", "MERRION")
    except ValueError as error:
        assert "is not on the trunk map" in str(error)
    else:
        raise AssertionError("expected ValueError")

    print("All checks passed.")
