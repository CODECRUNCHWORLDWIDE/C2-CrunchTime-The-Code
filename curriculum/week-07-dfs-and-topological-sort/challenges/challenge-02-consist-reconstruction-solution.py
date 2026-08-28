"""challenge-02-consist-reconstruction-solution.py — rebuild a train from sightings.

A freight train's wagons sit in one fixed front-to-back order. No single yard
saw the whole train, so each yard filed a sighting: the wagons it did see,
front to back, with gaps where wagons it never saw would have been.

Every sighting says the same small thing over and over: this wagon is in front
of the next one. Collect those neighbouring pairs, run Kahn's algorithm over
them, and the train comes back — or the sightings contradict each other and
nothing can.

The verdict is the second half of the answer. "unique" means the sightings pin
the train down. "ambiguous" means more than one train fits, and the order
handed back is only one of them. "impossible" means no train fits at all.

`_constraints_every_pair` is here to be measured, not used: it is the common
wrong move of writing a constraint between every pair of wagons in a sighting
instead of only the neighbouring ones. It gets the same answer for far more
work, and the self-checks print both counts so the gap is visible.
"""

from __future__ import annotations

import heapq


def reconstruct_consist(sightings: list[list[str]]) -> tuple[list[str], str]:
    """Rebuild the train's wagon order from the yards' sightings.

    Args:
        sightings: One list per yard, holding the wagon marks that yard saw,
            written front to back. A yard may have seen one wagon, or none.

    Returns:
        (order, verdict). verdict is "unique" when exactly one train fits the
        sightings, "ambiguous" when more than one does, and "impossible" when
        none does. On "impossible" the order is []. On "ambiguous" the order
        is one train that really does fit: at every step the alphabetically
        smallest wagon that could come next.

    Raises:
        ValueError: a sighting holds a wagon mark that is not a non-empty
            string.
    """
    wagons: set[str] = set()
    for index, sighting in enumerate(sightings):
        for mark in sighting:
            if not isinstance(mark, str) or not mark:
                raise ValueError(
                    f"sighting {index} holds {mark!r}, which is not a wagon mark"
                )
            wagons.add(mark)
        if len(set(sighting)) != len(sighting):
            # One wagon cannot stand in two places in one train.
            return [], "impossible"

    # Only neighbouring pairs. A > B and B > C already say A > C.
    constraints: set[tuple[str, str]] = set()
    for sighting in sightings:
        for front, back in zip(sighting, sighting[1:]):
            constraints.add((front, back))

    behind: dict[str, list[str]] = {wagon: [] for wagon in wagons}
    ahead_count: dict[str, int] = {wagon: 0 for wagon in wagons}
    for front, back in constraints:
        behind[front].append(back)
        ahead_count[back] += 1

    ready = [wagon for wagon in wagons if ahead_count[wagon] == 0]
    heapq.heapify(ready)
    order: list[str] = []
    forced = True
    while ready:
        if len(ready) > 1:
            # More than one wagon could legally come next, so the train the
            # sightings describe is not the only one that fits.
            forced = False
        wagon = heapq.heappop(ready)
        order.append(wagon)
        for follower in behind[wagon]:
            ahead_count[follower] -= 1
            if ahead_count[follower] == 0:
                heapq.heappush(ready, follower)

    if len(order) != len(wagons):
        # Whatever is left is stuck behind itself: the sightings loop.
        return [], "impossible"
    return order, "unique" if forced else "ambiguous"


def _constraints_every_pair(sightings: list[list[str]]) -> set[tuple[str, str]]:
    """Build the constraint set the wasteful way, for measuring only.

    Args:
        sightings: The yards' sightings.

    Returns:
        A constraint for every pair of wagons in every sighting, not only the
        neighbouring ones.
    """
    constraints: set[tuple[str, str]] = set()
    for sighting in sightings:
        for i, front in enumerate(sighting):
            for back in sighting[i + 1 :]:
                constraints.add((front, back))
    return constraints


def _constraints_neighbours(sightings: list[list[str]]) -> set[tuple[str, str]]:
    """Build the constraint set the way the answer does, for measuring only.

    Args:
        sightings: The yards' sightings.

    Returns:
        One constraint per neighbouring pair in each sighting.
    """
    constraints: set[tuple[str, str]] = set()
    for sighting in sightings:
        for front, back in zip(sighting, sighting[1:]):
            constraints.add((front, back))
    return constraints


def _order_from_constraints(
    wagons: set[str], constraints: set[tuple[str, str]]
) -> list[str]:
    """Run the same Kahn walk over a constraint set someone else built.

    Args:
        wagons: Every wagon that must appear in the order.
        constraints: (front, back) pairs, each meaning front is ahead of back.

    Returns:
        The alphabetically smallest legal order, or [] when none exists.
    """
    behind: dict[str, list[str]] = {wagon: [] for wagon in wagons}
    ahead_count: dict[str, int] = {wagon: 0 for wagon in wagons}
    for front, back in constraints:
        behind[front].append(back)
        ahead_count[back] += 1
    ready = [wagon for wagon in wagons if ahead_count[wagon] == 0]
    heapq.heapify(ready)
    order: list[str] = []
    while ready:
        wagon = heapq.heappop(ready)
        order.append(wagon)
        for follower in behind[wagon]:
            ahead_count[follower] -= 1
            if ahead_count[follower] == 0:
                heapq.heappush(ready, follower)
    return order if len(order) == len(wagons) else []


if __name__ == "__main__":
    cases: list[tuple[str, list[list[str]]]] = [
        ("nothing filed", []),
        ("two blank sightings", [[], []]),
        ("one wagon each", [["HOP-11"], ["TNK-04"]]),
        (
            "overlapping yards",
            [
                ["HOP-11", "BOX-27", "CAB-09"],
                ["HOP-11", "TNK-04", "BOX-27"],
                ["BOX-27", "GON-52", "CAB-09"],
            ],
        ),
        ("never seen together", [["FLT-03", "CAB-09"], ["REF-08", "CAB-09"]]),
        ("yards disagree", [["TNK-04", "BOX-27"], ["BOX-27", "TNK-04"]]),
        ("wagon listed twice", [["HOP-11", "TNK-04", "HOP-11"]]),
    ]
    print(f"{'sightings':<21}{'verdict':<12}order")
    for name, sightings in cases:
        order, verdict = reconstruct_consist(sightings)
        print(f"{name:<21}{verdict:<12}{order}")

    assert reconstruct_consist([]) == ([], "unique")
    assert reconstruct_consist([[], []]) == ([], "unique")
    assert reconstruct_consist([["HOP-11"], ["TNK-04"]]) == (
        ["HOP-11", "TNK-04"],
        "ambiguous",
    )
    assert reconstruct_consist(
        [
            ["HOP-11", "BOX-27", "CAB-09"],
            ["HOP-11", "TNK-04", "BOX-27"],
            ["BOX-27", "GON-52", "CAB-09"],
        ]
    ) == (["HOP-11", "TNK-04", "BOX-27", "GON-52", "CAB-09"], "unique")
    assert reconstruct_consist([["FLT-03", "CAB-09"], ["REF-08", "CAB-09"]]) == (
        ["FLT-03", "REF-08", "CAB-09"],
        "ambiguous",
    )
    assert reconstruct_consist([["TNK-04", "BOX-27"], ["BOX-27", "TNK-04"]]) == (
        [],
        "impossible",
    )
    assert reconstruct_consist([["HOP-11", "TNK-04", "HOP-11"]]) == ([], "impossible")

    # One yard that saw the whole train. Both ways of reading it agree; only
    # one of them stays linear in the wagons it was given.
    long_train = [[f"WAG-{number:04d}" for number in range(200)]]
    wagons = {mark for sighting in long_train for mark in sighting}
    neighbours = _constraints_neighbours(long_train)
    every_pair = _constraints_every_pair(long_train)
    assert _order_from_constraints(wagons, neighbours) == long_train[0]
    assert _order_from_constraints(wagons, every_pair) == long_train[0]
    print(f"200-wagon sighting : {len(neighbours)} neighbouring constraints")
    print(f"                     {len(every_pair)} if you write every pair")
    assert len(neighbours) == 199
    assert len(every_pair) == 19_900

    try:
        reconstruct_consist([["HOP-11", ""]])
    except ValueError as error:
        print(f"blank wagon mark   : {error}")
    else:  # pragma: no cover - the call above always raises
        raise AssertionError("a blank wagon mark must be refused")

    print("All checks passed.")
