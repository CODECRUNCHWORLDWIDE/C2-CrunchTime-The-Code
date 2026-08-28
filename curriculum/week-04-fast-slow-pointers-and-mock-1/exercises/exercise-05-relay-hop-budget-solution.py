"""exercise-05-relay-hop-budget-solution.py — where is the packet when the
budget runs out?

Walking the budget one hop at a time is the obvious answer and it is far too
slow: the budget is a 64-bit counter. So measure the network's shape first.
A relay run that loops has a straight lead-in of `lead` masts and then a ring
of `ring` masts. Once those two numbers are known, every hop past the lead-in
is arithmetic: hop number `budget` lands at position `lead + (budget - lead)
% ring`, and that position is a short walk from the first mast.

The networks are built in this file, so it runs on its own with no imports.

The self-checks at the bottom print one line per network, then
"All checks passed."
"""

from __future__ import annotations


class Mast:
    """One relay mast. It repeats to exactly one other mast, or to none."""

    def __init__(self, call_sign: str, repeats_to: "Mast | None" = None) -> None:
        self.call_sign = call_sign
        self.repeats_to = repeats_to


def build_network(call_signs: list[str], loop_to: int | None = None) -> list[Mast]:
    """Wire a relay run from a list of call signs and hand back every mast.

    Args:
        call_signs: One call sign per mast, in repeat order. Signs repeat
            across regions, so they are not identifiers.
        loop_to: Index the last mast repeats back to, or None for a run that
            ends at the ground station.

    Returns:
        The masts, in order. Empty when `call_signs` is empty.
    """
    masts = [Mast(call_sign) for call_sign in call_signs]
    for earlier, later in zip(masts, masts[1:]):
        earlier.repeats_to = later
    if masts and loop_to is not None:
        masts[-1].repeats_to = masts[loop_to]
    return masts


def hop_landing(first: Mast | None, budget: int) -> Mast | None:
    """Return the mast holding the packet after exactly `budget` hops.

    Args:
        first: The mast the packet is injected at, or None for no network.
        budget: How many times the packet is repeated onward. Zero means the
            packet has not moved yet.

    Returns:
        The mast holding the packet when the budget runs out, or None when
        the packet reached the ground station before the budget ran out.

    Raises:
        ValueError: If `budget` is negative.
    """
    if budget < 0:
        raise ValueError("a hop budget counts hops made, so it cannot be negative")
    if first is None:
        return None

    slow = first
    fast = first
    while fast is not None and fast.repeats_to is not None:
        slow = slow.repeats_to
        fast = fast.repeats_to.repeats_to
        if slow is fast:
            break
    else:
        # The run ends at the ground station. Walk it, and stop early if the
        # packet leaves the network before the budget is spent.
        here = first
        for _ in range(budget):
            here = here.repeats_to
            if here is None:
                return None
        return here

    finder = first
    lead = 0
    while finder is not slow:
        finder = finder.repeats_to
        slow = slow.repeats_to
        lead += 1

    walker = finder.repeats_to
    ring = 1
    while walker is not finder:
        walker = walker.repeats_to
        ring += 1

    steps = budget if budget < lead else lead + (budget - lead) % ring
    here = first
    for _ in range(steps):
        here = here.repeats_to
    return here


# ---- Self-check ----
if __name__ == "__main__":
    HUGE = 10 ** 18

    LOOPING = [
        ("R1 -> R2 -> R3 -> R4 -> R2", ["R1", "R2", "R3", "R4"], 1, 0, 0),
        ("R1 -> R2 -> R3 -> R4 -> R2", ["R1", "R2", "R3", "R4"], 1, 1, 1),
        ("R1 -> R2 -> R3 -> R4 -> R2", ["R1", "R2", "R3", "R4"], 1, HUGE, 1),
        ("R1 -> R2 -> R3 -> R4 -> R2", ["R1", "R2", "R3", "R4"], 1, HUGE + 1, 2),
        ("SOLO -> SOLO", ["SOLO"], 0, HUGE, 0),
        ("KX-7 -> KX-7' -> KX-7", ["KX-7", "KX-7"], 0, 5, 1),
    ]

    for wiring, signs, loop_to, budget, expected_index in LOOPING:
        masts = build_network(signs, loop_to)
        landed = hop_landing(masts[0], budget)
        assert landed is masts[expected_index], f"{wiring}, budget {budget}"
        print(f"{wiring:<28} budget {budget:>19}  ->  {landed.call_sign}")

    ENDING = [
        ("G1 -> G2 -> G3 -> ground", ["G1", "G2", "G3"], 2, 2),
        ("G1 -> G2 -> G3 -> ground", ["G1", "G2", "G3"], 3, None),
        ("G1 -> ground", ["G1"], 0, 0),
        ("G1 -> ground", ["G1"], 1, None),
    ]

    for wiring, signs, budget, expected_index in ENDING:
        masts = build_network(signs, None)
        landed = hop_landing(masts[0], budget)
        if expected_index is None:
            assert landed is None, f"{wiring}, budget {budget}: packet has left"
            print(f"{wiring:<28} budget {budget:>19}  ->  delivered")
        else:
            assert landed is masts[expected_index], f"{wiring}, budget {budget}"
            print(f"{wiring:<28} budget {budget:>19}  ->  {landed.call_sign}")

    assert hop_landing(None, 4) is None, "no network, nowhere to land"

    try:
        hop_landing(build_network(["G1"])[0], -1)
    except ValueError as caught:
        print(f"{'budget of -1':<28} raises ValueError: {caught}")
    else:  # pragma: no cover - the assert above is the real check
        raise AssertionError("a negative budget must raise")

    print("All checks passed.")
