"""exercise-02-cable-ferry-lane-solution.py — the cable ferry's waiting lane.

Vehicles join the lane at the back. Emergency vehicles join at the front.
The ferry takes whoever is nearest the ramp, up to a deck limit, and comes
back for the rest.

Both ends of the lane are busy, so the lane is a deque and never a list.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import deque

DECK = 3

ARRIVALS: list[tuple[str, bool]] = [
    ("van-11", False),
    ("car-02", False),
    ("bus-07", False),
    ("ambulance-1", True),
    ("car-19", False),
    ("car-33", False),
    ("fire-4", True),
]


def board(lane: deque[str], vehicle: str, urgent: bool) -> None:
    """Put one vehicle into the lane.

    Args:
        lane: The waiting lane, front of the lane at index 0.
        vehicle: The vehicle's plate.
        urgent: True for an emergency vehicle, which goes to the front.

    Returns:
        None. The lane is changed in place, on purpose.
    """
    if urgent:
        lane.appendleft(vehicle)
    else:
        lane.append(vehicle)


def next_crossing(lane: deque[str], deck: int) -> list[str]:
    """Take the next boatload off the front of the lane.

    Args:
        lane: The waiting lane. The vehicles taken are removed from it.
        deck: How many vehicles fit on the deck.

    Returns:
        Up to `deck` plates, nearest the ramp first. An empty list when the
        lane is already empty — the ferry does not sail empty.
    """
    manifest: list[str] = []
    while lane and len(manifest) < deck:
        manifest.append(lane.popleft())
    return manifest


def run_ferry(arrivals: list[tuple[str, bool]], deck: int) -> list[list[str]]:
    """Board every arrival, then sail until the lane is clear.

    Args:
        arrivals: (plate, urgent) pairs in the order they reached the slip.
        deck: How many vehicles fit on the deck.

    Returns:
        One manifest per crossing, in sailing order. Empty when nobody came.
    """
    lane: deque[str] = deque()
    for vehicle, urgent in arrivals:
        board(lane, vehicle, urgent)

    crossings: list[list[str]] = []
    while lane:
        crossings.append(next_crossing(lane, deck))
    return crossings


# ---- Self-check ----
if __name__ == "__main__":
    sailings = run_ferry(ARRIVALS, DECK)
    for number, manifest in enumerate(sailings, 1):
        print(f"crossing {number}: {', '.join(manifest)}")
    print(f"lane empty after {len(sailings)} crossings")

    assert sailings[0] == ["fire-4", "ambulance-1", "van-11"]
    assert sailings[1] == ["car-02", "bus-07", "car-19"]
    assert sailings[2] == ["car-33"]
    assert len(sailings) == 3
    assert run_ferry([], DECK) == []
    assert next_crossing(deque(), DECK) == []
    assert len(ARRIVALS) == 7  # the arrivals log is untouched
    print("All checks passed.")
