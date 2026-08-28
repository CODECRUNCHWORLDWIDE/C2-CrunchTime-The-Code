"""exercise-04-wear-level-rotation-solution.py — the shape of a write walk.

There is no chain of objects here. There is a formula, and a formula that
gives every slot exactly one successor is a chain all the same: the "nodes"
are slot numbers and the "next pointer" is the arithmetic.

Three phases. Phase 1 meets the two pointers somewhere inside the rotation.
Phase 2 turns that meeting point into the rotation's first slot and counts
the tail on the way. Phase 3 walks once around to measure the rotation.

The self-checks at the bottom print one line per walk, then
"All checks passed."
"""

from __future__ import annotations


def next_slot(s: int, slots: int) -> int:
    """Return the controller's successor slot for slot `s`.

    Args:
        s: The slot just written to.
        slots: How many erase blocks the part has.

    Returns:
        The slot the next write lands on: (s * s + 1) % slots.
    """
    return (s * s + 1) % slots


def rotation_shape(seed: int, slots: int) -> tuple[int, int]:
    """Return the tail length and the rotation length of the write walk.

    Args:
        seed: The slot the controller starts at.
        slots: How many erase blocks the part has.

    Returns:
        A pair of (tail length, rotation length). The tail is how many slots
        are written once at the start of the device's life and then never
        revisited; the rotation is how many slots repeat forever after that.
        The tail is 0 when `seed` is already inside the rotation.
    """
    slow = seed
    fast = seed
    while True:  # No guard: a finite walk with one successor per slot cannot end.
        slow = next_slot(slow, slots)
        fast = next_slot(next_slot(fast, slots), slots)
        if slow == fast:
            break

    finder = seed
    tail = 0
    while finder != slow:
        finder = next_slot(finder, slots)
        slow = next_slot(slow, slots)
        tail += 1

    walker = next_slot(finder, slots)
    rotation = 1
    while walker != finder:
        walker = next_slot(walker, slots)
        rotation += 1

    return tail, rotation


# ---- Self-check ----
if __name__ == "__main__":
    SUCCESSORS = [(0, 12, 1), (5, 12, 2), (11, 12, 2), (7, 1000, 50), (999, 1000, 2)]
    for s, slots, expected in SUCCESSORS:
        found = next_slot(s, slots)
        assert found == expected, f"next_slot({s}, {slots}): got {found}"

    CASES = [
        ("seed 0, 12 slots", 0, 12, (2, 2)),
        ("seed 5, 12 slots", 5, 12, (0, 2)),
        ("seed 4, 12 slots", 4, 12, (1, 2)),
        ("seed 3, 12 slots", 3, 12, (2, 2)),
        ("seed 0, 3 slots", 0, 3, (2, 1)),
        ("seed 0, 2 slots", 0, 2, (0, 2)),
        ("seed 7, 1000 slots", 7, 1000, (5, 6)),
        ("seed 12345, 2^20 slots", 12_345, 1_048_576, (12, 2)),
    ]

    for label, seed, slots, expected in CASES:
        found = rotation_shape(seed, slots)
        assert found == expected, f"{label}: got {found}, wanted {expected}"
        tail, rotation = found
        print(f"{label:<24} tail {tail:>2}, rotation {rotation}")

    print("All checks passed.")
