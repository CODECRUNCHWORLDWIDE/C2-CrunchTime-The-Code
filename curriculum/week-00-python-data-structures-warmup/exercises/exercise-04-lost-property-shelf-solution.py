"""exercise-04-lost-property-shelf-solution.py — the depot's lost-property shelf.

Every item handed in is logged as (route, item). Four questions get asked
about that log, and every one of them is a dict away.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

FINDS: list[tuple[str, str]] = [
    ("R12", "umbrella"),
    ("R7", "water bottle"),
    ("R12", "hat"),
    ("R3", "umbrella"),
    ("R7", "glove"),
    ("R7", "umbrella"),
    ("R12", "scarf"),
    ("R3", "phone"),
]


def items_by_route(finds: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group the log by route, keeping the order things were handed in.

    Args:
        finds: (route, item) pairs in the order they reached the shelf.

    Returns:
        A dict from route to its items. Routes appear in the order each was
        first seen, and each route's items in the order they arrived.
    """
    shelf: dict[str, list[str]] = {}
    for route, item in finds:
        shelf.setdefault(route, []).append(item)
    return shelf


def count_by_route(finds: list[tuple[str, str]]) -> dict[str, int]:
    """Count how many items each route lost.

    Args:
        finds: (route, item) pairs in the order they reached the shelf.

    Returns:
        A dict from route to its item count, in first-seen order.
    """
    counts: dict[str, int] = {}
    for route, _item in finds:
        counts[route] = counts.get(route, 0) + 1
    return counts


def busiest_route(finds: list[tuple[str, str]]) -> str | None:
    """Return the route that lost the most, ties broken by route label.

    Args:
        finds: (route, item) pairs in the order they reached the shelf.

    Returns:
        The winning route label, or None when the log is empty.
    """
    counts = count_by_route(finds)
    if not counts:
        return None
    return min(counts.items(), key=lambda pair: (-pair[1], pair[0]))[0]


def first_route_for(finds: list[tuple[str, str]], item: str) -> str | None:
    """Return the route where this kind of item first turned up.

    Args:
        finds: (route, item) pairs in the order they reached the shelf.
        item: The item description to look for.

    Returns:
        The route label of the earliest matching entry, or None if this kind
        of item has never been handed in.
    """
    first: dict[str, str] = {}
    for route, found in finds:
        first.setdefault(found, route)
    return first.get(item)


# ---- Self-check ----
if __name__ == "__main__":
    shelf = items_by_route(FINDS)
    counts = count_by_route(FINDS)
    for route, items in shelf.items():
        print(f"{route:<4} {counts[route]}  {', '.join(items)}")

    print(f"busiest: {busiest_route(FINDS)}")
    print(f"first umbrella: {first_route_for(FINDS, 'umbrella')}")
    print(f"first kite: {first_route_for(FINDS, 'kite')}")

    assert list(shelf) == ["R12", "R7", "R3"]
    assert shelf["R7"] == ["water bottle", "glove", "umbrella"]
    assert counts == {"R12": 3, "R7": 3, "R3": 2}
    assert busiest_route(FINDS) == "R12"  # ties go to the earlier label as text
    assert busiest_route([]) is None
    assert first_route_for(FINDS, "umbrella") == "R12"
    assert first_route_for(FINDS, "kite") is None
    assert len(FINDS) == 8  # the log is untouched
    print("All checks passed.")
