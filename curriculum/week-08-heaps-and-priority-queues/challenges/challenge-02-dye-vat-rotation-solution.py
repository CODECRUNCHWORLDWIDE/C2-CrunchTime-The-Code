"""challenge-02-dye-vat-rotation-solution.py — the dye house rotation plan.

One vat, several colours, and a rule: after a colour runs, the vat has to be
cleaned down before that same colour may run again, and every pigment needs a
different number of slots to clean down. Fill the day with as few slots as
possible, and write down what actually happens in each one.

Two heaps do the work. A max-heap holds the colours that could run now, so the
one with the most batches left is always on top. A min-heap holds the colours
that are still cleaning down, so the one that becomes free soonest is always on
top. Every slot moves whatever has finished cleaning from the second into the
first.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
# How many batches of each colour the workshop owes.
BATCHES: dict[str, int] = {
    "indigo": 6,
    "madder": 4,
    "weld": 3,
    "cochineal": 1,
}

# How many slots the vat must stand between two runs of the same colour.
REST_SLOTS: dict[str, int] = {
    "indigo": 2,
    "madder": 1,
    "weld": 3,
    "cochineal": 0,
}


# ---- Your task ----
def rotation_plan(
    batches: dict[str, int], rest_slots: dict[str, int]
) -> list[str | None]:
    """Return what the vat does in every slot, first slot first.

    Args:
        batches: Colour to the number of batches still owed. A colour with
            zero batches is ignored.
        rest_slots: Colour to how many slots the vat must stand after that
            colour before it may run again. Zero means it may run next slot.

    Returns:
        One entry per slot: the colour that ran, or None for a slot in which
        every unfinished colour was still cleaning down. The list ends on the
        slot that ran the last batch, so it never ends with None.
    """
    ready: list[tuple[int, str]] = [
        (-owed, colour) for colour, owed in batches.items() if owed > 0
    ]
    heapq.heapify(ready)
    cleaning: list[tuple[int, int, str]] = []
    plan: list[str | None] = []
    slot = 0

    while ready or cleaning:
        slot += 1
        while cleaning and cleaning[0][0] <= slot:
            _, owed, colour = heapq.heappop(cleaning)
            heapq.heappush(ready, (-owed, colour))
        if not ready:
            plan.append(None)
            continue
        stored, colour = heapq.heappop(ready)
        plan.append(colour)
        left = -stored - 1
        if left > 0:
            heapq.heappush(cleaning, (slot + rest_slots[colour] + 1, left, colour))
    return plan


def slots_needed(batches: dict[str, int], rest_slots: dict[str, int]) -> int:
    """Return how many slots the whole rotation takes, idle slots included.

    Args:
        batches: Colour to the number of batches still owed.
        rest_slots: Colour to its clean-down length in slots.

    Returns:
        The length of the plan.
    """
    return len(rotation_plan(batches, rest_slots))


def idle_slots(plan: list[str | None]) -> list[int]:
    """Return the slot numbers in which the vat stood empty.

    Args:
        plan: A plan from rotation_plan.

    Returns:
        Slot numbers, counting from 1.
    """
    return [slot for slot, colour in enumerate(plan, 1) if colour is None]


def rest_respected(plan: list[str | None], rest_slots: dict[str, int]) -> bool:
    """Return True when no colour runs again before its clean-down is over.

    Args:
        plan: A plan from rotation_plan.
        rest_slots: Colour to its clean-down length in slots.

    Returns:
        True when every pair of consecutive runs of the same colour is far
        enough apart, False otherwise.
    """
    last_run: dict[str, int] = {}
    for slot, colour in enumerate(plan, 1):
        if colour is None:
            continue
        if colour in last_run and slot - last_run[colour] <= rest_slots[colour]:
            return False
        last_run[colour] = slot
    return True


# ---- Self-check ----
if __name__ == "__main__":
    plan = rotation_plan(BATCHES, REST_SLOTS)
    print(f"slots needed: {len(plan)}")
    print("rotation:")
    for slot, colour in enumerate(plan, 1):
        print(f"  slot {slot:2d}  {colour if colour else '- vat standing -'}")

    print(f"idle slots: {idle_slots(plan)}")
    print(f"batches run: {sum(1 for colour in plan if colour)}")
    print(f"rest respected: {rest_respected(plan, REST_SLOTS)}")

    lone = rotation_plan({"woad": 3}, {"woad": 2})
    print(f"one colour, rest 2: {lone}")
    print(f"nothing owed: {rotation_plan({}, {})}")
    print(f"a zero-batch colour: {rotation_plan({'oak gall': 0}, {'oak gall': 4})}")
    print(f"no rest at all: {rotation_plan({'onion skin': 3}, {'onion skin': 0})}")

    assert len(plan) == 16
    assert plan[0] == "indigo"
    assert plan[7] == "madder"  # slot 8: madder and weld both owe 2; m before w
    assert idle_slots(plan) == [12, 15]
    assert plan[-1] == "indigo"
    assert sum(1 for colour in plan if colour) == sum(BATCHES.values())
    assert rest_respected(plan, REST_SLOTS)
    assert slots_needed(BATCHES, REST_SLOTS) == 16
    assert lone == ["woad", None, None, "woad", None, None, "woad"]
    assert rotation_plan({}, {}) == []
    assert rotation_plan({"oak gall": 0}, {"oak gall": 4}) == []
    assert rotation_plan({"onion skin": 3}, {"onion skin": 0}) == [
        "onion skin",
        "onion skin",
        "onion skin",
    ]
    print("All checks passed.")
