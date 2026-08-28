"""challenge-01-shortest-kit-span-solution.py — the shortest kit span.

A parts conveyor feeds an assembly cell. A kit is defined by a bill of
materials, and repeats in the bill are real requirements. The operator stops
the belt over a contiguous stretch and pulls the whole bill out of it. Surplus
and irrelevant parts inside the stretch are allowed; they only make it longer.

The state that makes this fast is a single integer. `matched` counts how many
distinct part codes from the bill are currently satisfied in the window, so
"does this stretch cover the bill?" is one equality test rather than a walk
over the bill's whole table. Two comparison operators carry the whole trick:
increment only on exact equality, decrement only on a strict shortfall.

The self-checks are the starter's, unchanged. When they all pass the file
prints "All checks passed."
"""

from collections import Counter


def shortest_kit_span(conveyor: list[str], bill: list[str]) -> tuple[int, int] | None:
    """Return the shortest stretch of conveyor containing the whole bill.

    Args:
        conveyor: Part codes in the order they arrive at the cell.
        bill: The bill of materials. Repeats mean "this many of that part".

    Returns:
        (start, length) for the shortest covering stretch. Ties go to the
        larger start. An empty bill returns (0, 0); a bill no stretch can
        cover returns None.
    """
    if not bill:
        return (0, 0)
    if len(bill) > len(conveyor):
        return None

    wanted = Counter(bill)
    distinct_wanted = len(wanted)

    on_belt: dict[str, int] = {}
    left = 0
    matched = 0
    best: tuple[int, int] | None = None

    for right, part in enumerate(conveyor):
        on_belt[part] = on_belt.get(part, 0) + 1
        if part in wanted and on_belt[part] == wanted[part]:
            matched += 1

        while matched == distinct_wanted:
            # Shorter wins; then the later start. Negating the start lets one
            # tuple comparison say both rules at once.
            candidate = (right - left + 1, -left)
            if best is None or candidate < best:
                best = candidate

            dropped = conveyor[left]
            on_belt[dropped] -= 1
            if dropped in wanted and on_belt[dropped] < wanted[dropped]:
                matched -= 1
            left += 1

    if best is None:
        return None
    length, negated_start = best
    return (-negated_start, length)


def covers(stretch: list[str], bill: list[str]) -> bool:
    """Return True when `stretch` holds every part in `bill`, counting repeats.

    Args:
        stretch: The parts inside a candidate window.
        bill: The bill of materials.

    Returns:
        True when the stretch's counts meet or beat the bill's, for every code
        the bill names.
    """
    have = Counter(stretch)
    return all(have[code] >= needed for code, needed in Counter(bill).items())


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[str], list[str]]] = [
        (["bolt", "clip", "washer", "nut", "bolt", "washer", "nut", "clip"], ["bolt", "nut", "washer"]),
        (["nut", "bolt", "nut", "nut", "bolt"], ["nut", "nut"]),
        (["bolt", "bolt", "nut"], ["bolt", "nut"]),
        (["washer", "clip", "bolt"], ["bolt", "washer"]),
        (["bolt", "bolt", "bolt"], ["bolt", "nut"]),
        (["nut", "bolt"], ["nut", "nut"]),
        (["bolt"], []),
        ([], ["bolt"]),
    ]
    for conveyor, bill in cases:
        answer = shortest_kit_span(conveyor, bill)
        shown = f"bill {str(bill):<26} belt {str(conveyor):<74}"
        if answer is None:
            print(f"{shown} -> None")
        else:
            start, length = answer
            print(f"{shown} -> ({start}, {length}) = {conveyor[start : start + length]}")
    print()

    assert shortest_kit_span(["bolt", "clip", "washer", "nut", "bolt", "washer", "nut", "clip"], ["bolt", "nut", "washer"]) == (4, 3)
    assert shortest_kit_span(["nut", "bolt", "nut", "nut", "bolt"], ["nut", "nut"]) == (2, 2)
    assert shortest_kit_span(["bolt", "bolt", "nut"], ["bolt", "nut"]) == (1, 2)
    assert shortest_kit_span(["washer", "clip", "bolt"], ["bolt", "washer"]) == (0, 3)
    assert shortest_kit_span(["bolt", "bolt", "bolt"], ["bolt", "nut"]) is None
    assert shortest_kit_span(["nut", "bolt"], ["nut", "nut"]) is None
    assert shortest_kit_span(["bolt"], []) == (0, 0)
    assert shortest_kit_span([], ["bolt"]) is None

    # Brute force agrees, on the examples and on a generated adversarial log.
    scarce = ["bolt"] * 40 + ["nut"] + ["bolt"] * 40
    for conveyor, bill in cases + [(scarce, ["bolt", "nut"]), (scarce, ["nut", "nut"])]:
        spans = [
            (j - i, -i)
            for i in range(len(conveyor))
            for j in range(i + 1, len(conveyor) + 1)
            if covers(conveyor[i:j], bill)
        ]
        if not bill:
            expected: tuple[int, int] | None = (0, 0)
        elif not spans:
            expected = None
        else:
            length, negated_start = min(spans)
            expected = (-negated_start, length)
        assert shortest_kit_span(conveyor, bill) == expected

    print("All checks passed.")
