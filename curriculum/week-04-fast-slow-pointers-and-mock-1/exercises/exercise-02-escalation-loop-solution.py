"""exercise-02-escalation-loop-solution.py — where does the paging loop start?

Phase 1 is Exercise 1's tortoise and hare: it lands both pointers on the
same slot somewhere inside the loop. Phase 2 restarts a third pointer at
the beginning and walks it alongside the slow one, one slot each, until
they collide. The collision is the loop's entrance, and the number of
steps it took is the hop count the platform team asked for.

The rotas are built in this file, so it runs on its own with no imports.

The self-checks at the bottom print one line per rota, then
"All checks passed."
"""

from __future__ import annotations


class Rota:
    """One on-call slot. It escalates to exactly one other slot, or to none."""

    def __init__(self, slot: str, escalates_to: "Rota | None" = None) -> None:
        self.slot = slot
        self.escalates_to = escalates_to


def build_rota(labels: list[str], loop_to: int | None = None) -> list[Rota]:
    """Wire a rota from a list of labels and hand back every slot.

    Args:
        labels: One label per slot, in escalation order. Labels may repeat.
        loop_to: Index the last slot escalates back to, or None for a rota
            that reaches the top and stops.

    Returns:
        The slots, in order. Empty when `labels` is empty. The caller reads
        `slots[0]` for the starting slot and uses the rest to check answers
        by identity rather than by label.
    """
    slots = [Rota(label) for label in labels]
    for earlier, later in zip(slots, slots[1:]):
        earlier.escalates_to = later
    if slots and loop_to is not None:
        slots[-1].escalates_to = slots[loop_to]
    return slots


def find_escalation_loop(start: Rota | None) -> tuple[Rota, int] | None:
    """Return the loop's entrance and how many hops sit in front of it.

    Args:
        start: The slot a page begins at, or None for no rota at all.

    Returns:
        A pair of (entrance slot, hops from `start` to it), or None when the
        rota terminates and the page reaches a director.
    """
    slow = start
    fast = start
    while fast is not None and fast.escalates_to is not None:
        slow = slow.escalates_to
        fast = fast.escalates_to.escalates_to
        if slow is fast:
            break
    else:
        return None

    finder = start
    hops = 0
    while finder is not slow:
        finder = finder.escalates_to
        slow = slow.escalates_to
        hops += 1
    return finder, hops


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        ("L1 -> L2 -> L3 -> L4 -> L2", ["L1", "L2", "L3", "L4"], 1, 1, 1),
        (
            "L1 -> ... -> L6 -> L3",
            ["L1", "L2", "L3", "L4", "L5", "L6"],
            2,
            2,
            2,
        ),
        ("A -> A", ["A"], 0, 0, 0),
        ("A -> B -> C -> D -> A", ["A", "B", "C", "D"], 0, 0, 0),
        ("four slots, one label", ["weekend-primary"] * 4, 1, 1, 1),
    ]

    for wiring, labels, loop_to, entrance_index, hops in CASES:
        slots = build_rota(labels, loop_to)
        result = find_escalation_loop(slots[0])
        assert result is not None, f"{wiring}: this rota does loop"
        entrance, reported = result
        assert entrance is slots[entrance_index], f"{wiring}: wrong slot"
        assert reported == hops, f"{wiring}: got {reported} hops, wanted {hops}"
        print(f"{wiring:<28} entrance {entrance.slot}, {reported} hop(s) in front")

    TERMINATING = [
        ("L1 -> L2 -> L3 -> None", ["L1", "L2", "L3"]),
        ("A -> None", ["A"]),
        ("(no rota at all)", []),
        ("dup -> dup -> dup -> None", ["dup", "dup", "dup"]),
    ]

    for wiring, labels in TERMINATING:
        slots = build_rota(labels, None)
        start = slots[0] if slots else None
        assert find_escalation_loop(start) is None, f"{wiring}: no loop here"
        print(f"{wiring:<28} no loop")

    print("All checks passed.")
