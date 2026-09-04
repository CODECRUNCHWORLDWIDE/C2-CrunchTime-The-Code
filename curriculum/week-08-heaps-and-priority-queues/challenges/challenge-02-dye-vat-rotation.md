# Challenge 2 — The Dye Vat Rotation

> Topic: greedy scheduling with two heaps · Lecture: [2](../lecture-notes/02-heap-of-tuples-and-k-closest.md) · Difficulty: Medium-Hard · Target time: 75 minutes including the FRAME write-up · Why this one: it is the scheduler shape, and the greedy choice is one that most people can feel is right long before they can say why.

## The Brief

A dye house has **one vat** and a day's worth of orders. After a colour runs,
the vat has to be cleaned down before that same colour may run again — and every
pigment needs a different number of slots to clean down. Indigo needs two,
madder one, weld three, cochineal none at all.

Fill the day in as few slots as possible, and write down what actually happens
in each one — including the slots where the vat stands empty because everything
that could run is still cleaning.

The greedy rule is short: **run the colour with the most batches left**. What
takes the write-up is saying *why* that is right rather than merely plausible.
The colour with the most batches is the one that will still be owed at the end
if you neglect it; every slot spent elsewhere is a slot it cannot use.

## Starter

`challenge-02-dye-vat-rotation-solution.py` sits beside this page with the
workshop's orders and the self-checks.

```text
colour       batches   rest slots
indigo             6            2
madder             4            1
weld               3            3
cochineal          1            0
```

Fourteen batches. If they could run back to back the day would be fourteen slots
long. Work out on paper how long it actually has to be before you write any
code — the arithmetic is the Assess-options step, and it is short.

## Requirements

1. `rotation_plan(batches, rest_slots)` returns a list, one entry per slot: the
   colour that ran, or `None` for a slot where the vat stood empty.
2. `slots_needed(batches, rest_slots)` returns the length of that plan.
3. `idle_slots(plan)` returns the 1-based slot numbers where nothing ran.
4. `rest_respected(plan, rest_slots)` verifies a plan rather than trusting it.
5. Nothing owed returns an empty plan; a colour listed with zero batches is not
   scheduled at all.

## Constraints

- **The plan may end with work, never with an idle slot.** Standing the vat after
  the last batch is not part of the day.
- **Two heaps, not one.** A max-heap of colours that may run now, and a min-heap
  of colours still cleaning down, keyed on the slot they become free. Doing this
  with one structure and a scan is possible and is the alternative your write-up
  should name and reject.
- **`heapq` is a min-heap.** Getting "most batches left" out of it means pushing
  the negated count, and the memo should say that plainly rather than leaving a
  bare minus sign in the code.
- **A rest of zero means no rest.** That colour goes straight back into the
  runnable heap in the same slot it finishes.
- **`rest_respected` must be independent of `rotation_plan`.** A verifier that
  shares the planner's assumptions verifies nothing.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python challenge-02-dye-vat-rotation.py
slots needed: 16
rotation:
  slot  1  indigo
  slot  2  madder
  slot  3  weld
  slot  4  indigo
  slot  5  madder
  slot  6  cochineal
  slot  7  indigo
  slot  8  madder
  slot  9  weld
  slot 10  indigo
  slot 11  madder
  slot 12  - vat standing -
  slot 13  indigo
  slot 14  weld
  slot 15  - vat standing -
  slot 16  indigo
idle slots: [12, 15]
batches run: 14
rest respected: True
one colour, rest 2: ['woad', None, None, 'woad', None, None, 'woad']
nothing owed: []
a zero-batch colour: []
no rest at all: ['onion skin', 'onion skin', 'onion skin']
All checks passed.
```

Sixteen slots for fourteen batches, and the two empty ones are slots 12 and 15 —
late in the day, once the small orders are gone and only indigo and weld are
left, both of them mid-clean. That is the shape to notice: idle slots cluster at
the end, because the greedy rule spends the crowded early slots on the colours
that would otherwise be stranded.

## Steps

1. Read the self-checks. They are the spec.
2. Do the arithmetic on paper: how few slots could this possibly take?
3. Write the memo — the two heaps, what each holds, and the greedy rule in one
   sentence.
4. Build the plan slot by slot. Move everything that has finished cleaning back
   into the runnable heap **first**, then choose.
5. Write `rest_respected` from scratch, from the rule, and run it on your own
   plan. If it agrees only because both share a bug, you will find out on the
   hand-built cases.
6. Handle nothing-owed, zero-batch colours, and zero rest; then write FRAME.

## The Solution

```python
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
```

The idle slot is an entry in the plan rather than a gap in it. That is what makes
`rest_respected` a straight walk over the list, and what makes the day's length
fall out of the plan rather than needing to be computed separately.

## Run it

Download the solution beside this page and run it:

```bash
python challenge-02-dye-vat-rotation.py
```

No third-party packages, no arguments, no input. It prints the rotation, the
idle slots, the degenerate cases, and then `All checks passed.`

## Common bugs to catch

- **Choosing before returning the cleaned colours.** Symptom: an idle slot where
  a colour was in fact free. The order of the two steps inside a slot is the
  whole thing.
- **Pushing the count as-is into a `heapq`.** Symptom: the *rarest* colour runs
  first and the plan is much longer than it needs to be.
- **A trailing idle slot.** Symptom: the length is one or two too long. The day
  ends with the last batch.
- **Scheduling a colour listed with zero batches.** Symptom: a colour name in the
  plan that the workshop never ordered.
- **Rest counted from the wrong slot.** Symptom: off by one, and a plan that
  `rest_respected` rejects — which is exactly what that function is for.
- **A verifier written by copying the planner.** Symptom: it passes on your plan
  and on a plan you know is wrong.

## Acceptance checklist

- [ ] The shipped orders produce a 16-slot plan running all 14 batches.
- [ ] Idle slots are exactly `[12, 15]`, and the plan does not end idle.
- [ ] `rest_respected` returns `True` on that plan, written independently.
- [ ] One colour with three batches and a rest of 2 gives seven slots, two idle.
- [ ] Nothing owed, and a zero-batch colour, both give an empty plan.
- [ ] Zero rest everywhere gives a plan with no idle slots at all.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Report the vat's utilisation as a percentage and say which single extra batch
  of which colour would lower it most. That is a question the dye house would
  actually ask.
- Allow two vats and say what breaks. The greedy rule survives; the bookkeeping
  does not, and naming which part is the interesting half of the answer.
- Add a colour mid-day, after slot 5, and re-plan from there without discarding
  what already ran.
