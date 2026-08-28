"""exercise-04-cable-pull-solution.py — surveying twenty thousand junction boxes.

A tower's cable trays run between junction boxes. An electrician standing at
the head end wants to know how many trays a pull has to cross to reach the
furthest box, and which box that is. Twenty thousand boxes is enough that the
choice of queue stops being a matter of taste.

The survey also reports how many times a list-backed queue would have shifted
an element along, which is the work `deque` does not do.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import deque
from typing import NamedTuple

# ---- Given data ----
BOX_COUNT = 20_000
HEAD = "J00000"


class Survey(NamedTuple):
    """What a completed survey of the tray network reports."""

    boxes: int
    deepest: int
    furthest: str
    at_deepest: int
    list_shifts: int


def label(number: int) -> str:
    """Return the stencilled label for a junction box.

    Args:
        number: The box's number, counting from zero at the head end.

    Returns:
        The label as it is painted on the box, e.g. `J00042`.
    """
    return f"J{number:05d}"


def tray_manifest(count: int = BOX_COUNT) -> dict[str, list[str]]:
    """Build the as-built tray manifest for a riser of `count` boxes.

    Two trays leave every box, feeding boxes `2n+1` and `2n+2`. On top of
    that the electricians ran a cross tie from every thirteenth box to the
    box seven along, which is what turns the riser from a tree into a graph.

    Args:
        count: How many junction boxes the riser has.

    Returns:
        The manifest: each label mapped to the labels it shares a tray with.
        Trays run both ways, so every tie appears in both entries.
    """
    trays: dict[str, list[str]] = {label(n): [] for n in range(count)}

    def tie(one: int, other: int) -> None:
        trays[label(one)].append(label(other))
        trays[label(other)].append(label(one))

    for number in range(count):
        for onward in (2 * number + 1, 2 * number + 2):
            if onward < count:
                tie(number, onward)
        if number % 13 == 0 and number + 7 < count:
            tie(number, number + 7)
    return trays


# ---- Your task ----
def tray_hops(trays: dict[str, list[str]], head: str) -> dict[str, int]:
    """Return how many trays a pull crosses from `head` to every box it reaches.

    Args:
        trays: The tray manifest.
        head: The label of the box the pull starts at.

    Returns:
        A dict mapping each reachable label to its tray count. `head` maps
        to 0.

    Raises:
        ValueError: If `head` is not a label in the manifest.
    """
    if head not in trays:
        raise ValueError(f"{head!r} is not a box on this riser")
    hops = {head: 0}
    queue = deque([head])
    while queue:
        box = queue.popleft()
        for neighbour in trays[box]:
            if neighbour not in hops:
                hops[neighbour] = hops[box] + 1
                queue.append(neighbour)
    return hops


def list_queue_shifts(trays: dict[str, list[str]], head: str) -> int:
    """Return the element shifts a list-backed queue would perform.

    `list.pop(0)` has to slide every remaining element one place to the left.
    This counts those slides without ever doing them, by adding up the length
    of the queue behind each box as it comes off the front.

    Args:
        trays: The tray manifest.
        head: The label of the box the pull starts at.

    Returns:
        The total number of element shifts. A `deque` performs none of them.

    Raises:
        ValueError: If `head` is not a label in the manifest.
    """
    if head not in trays:
        raise ValueError(f"{head!r} is not a box on this riser")
    seen = {head}
    queue = deque([head])
    shifts = 0
    while queue:
        shifts += len(queue) - 1  # what pop(0) would have had to slide
        box = queue.popleft()
        for neighbour in trays[box]:
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)
    return shifts


def survey(trays: dict[str, list[str]], head: str) -> Survey:
    """Return the full survey of the riser from `head`.

    Args:
        trays: The tray manifest.
        head: The label of the box the pull starts at.

    Returns:
        A `Survey`: how many boxes were reached, the largest tray count, the
        furthest box (lowest label wins a tie), how many boxes share that
        count, and the shifts a list-backed queue would have performed.

    Raises:
        ValueError: If `head` is not a label in the manifest.
    """
    hops = tray_hops(trays, head)
    deepest = max(hops.values())
    at_deepest = sum(1 for count in hops.values() if count == deepest)
    furthest = min(box for box, count in hops.items() if count == deepest)
    return Survey(
        boxes=len(hops),
        deepest=deepest,
        furthest=furthest,
        at_deepest=at_deepest,
        list_shifts=list_queue_shifts(trays, head),
    )


# ---- Self-check ----
if __name__ == "__main__":
    trays = tray_manifest()
    report = survey(trays, HEAD)
    print(f"boxes reached      : {report.boxes}")
    print(f"deepest tray count : {report.deepest}")
    print(f"furthest box       : {report.furthest}")
    print(f"boxes that deep    : {report.at_deepest}")
    print(f"list pop(0) shifts : {report.list_shifts:,}")
    print(f"deque popleft shifts: 0")

    assert report.boxes == BOX_COUNT  # every box is reachable from the head
    assert report.deepest == 14
    assert report.furthest == "J18447"
    assert report.at_deepest == 1257
    assert report.list_shifts == 97_108_042

    hops = tray_hops(trays, HEAD)
    assert hops[HEAD] == 0
    assert hops["J00001"] == 1 and hops["J00002"] == 1
    assert hops["J00007"] == 1  # the cross tie from box 0, not three trays down
    assert hops["J00008"] == 3  # no cross tie helps here: 0 - 1 - 3 - 8

    try:
        tray_hops(trays, "J99999")
    except ValueError as error:
        assert "not a box on this riser" in str(error)
    else:
        raise AssertionError("expected ValueError")

    print("All checks passed.")
