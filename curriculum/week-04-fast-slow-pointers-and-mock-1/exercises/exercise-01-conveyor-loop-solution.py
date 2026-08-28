"""exercise-01-conveyor-loop-solution.py — how many chutes are in the loop?

Two walks. The first sends a slow pointer one chute at a time and a fast
pointer two at a time until they land on the same chute, which proves there
is a loop and puts you inside it. The second walks once around from there,
counting.

The sorters are built in this file, so it runs on its own with no imports.

The self-checks at the bottom print one line per wiring, then
"All checks passed."
"""

from __future__ import annotations


class Chute:
    """One chute in a parcel sorter. Exactly one outgoing edge, or none."""

    def __init__(self, chute_id: str, forwards_to: "Chute | None" = None) -> None:
        self.chute_id = chute_id
        self.forwards_to = forwards_to


def build_sorter(ids: list[str], loop_to: int | None = None) -> Chute | None:
    """Wire a sorter from a list of stencilled ids.

    Args:
        ids: One id per chute, in order. Ids may repeat.
        loop_to: Index the last chute forwards back to, or None for a
            correctly wired sorter that ends in the outbound bin.

    Returns:
        The entry chute, or None when there are no chutes at all.
    """
    if not ids:
        return None
    chutes = [Chute(chute_id) for chute_id in ids]
    for earlier, later in zip(chutes, chutes[1:]):
        earlier.forwards_to = later
    if loop_to is not None:
        chutes[-1].forwards_to = chutes[loop_to]
    return chutes[0]


def loop_size(entry: Chute | None) -> int:
    """Return how many chutes are in the loop reachable from `entry`.

    Args:
        entry: The chute a parcel is dropped into, or None for no sorter.

    Returns:
        The number of chutes in the loop, or 0 when a parcel entering here
        eventually falls out the end.
    """
    slow = entry
    fast = entry
    while fast is not None and fast.forwards_to is not None:
        slow = slow.forwards_to
        fast = fast.forwards_to.forwards_to
        if slow is fast:
            break
    else:
        return 0

    count = 1
    walker = slow.forwards_to
    while walker is not slow:
        walker = walker.forwards_to
        count += 1
    return count


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        ("IN -> S1 -> S2 -> S3 -> S1", ["IN", "S1", "S2", "S3"], 1, 3),
        ("IN -> IN", ["IN"], 0, 1),
        ("A -> B -> A", ["A", "B"], 0, 2),
        ("IN -> S1 -> OUT", ["IN", "S1", "OUT"], None, 0),
        ("(no sorter at all)", [], None, 0),
        ("S-12 -> S-12' -> OUT", ["S-12", "S-12", "OUT"], None, 0),
        ("S-12 -> S-12' -> S-12", ["S-12", "S-12"], 0, 2),
        ("A -> B -> C -> D -> E -> E", ["A", "B", "C", "D", "E"], 4, 1),
    ]

    for wiring, ids, loop_to, expected in CASES:
        found = loop_size(build_sorter(ids, loop_to))
        assert found == expected, f"{wiring}: got {found}, wanted {expected}"
        print(f"{wiring:<28} loop of {found}")

    print("All checks passed.")
