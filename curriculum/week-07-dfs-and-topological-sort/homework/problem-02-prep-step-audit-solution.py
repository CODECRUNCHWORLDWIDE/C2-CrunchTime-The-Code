"""problem-02-prep-step-audit-solution.py -- can the prep list be scheduled at all?

A pastry kitchen writes down its prep steps and the rules between them. A rule
(a, b) means step a has to be finished before step b can start. This page asks
the cheapest question in the family: is there a legal order at all, yes or no?
No order is produced.

Two routes answer it, both O(V + E) -- one look at every step and one look at
every rule, and then it is done:

  * the three-colour walk, which can stop the instant it meets a step that is
    already on the path it is standing on, and
  * Kahn's counting, which reads every step to build its waiting-on table
    before it can start, and so always pays for the whole list.

This file ships the colour walk and keeps the counting version beside it so the
two can be run against the same inputs and compared.

Run it with no arguments. The self-checks at the bottom print
"All checks passed." when every case agrees.
"""

from __future__ import annotations

from collections import deque

WHITE, GREY, BLACK = 0, 1, 2

# ---- Given data ----
BISCUIT_STEPS = [
    "chill dough",
    "roll dough",
    "cut shapes",
    "proof",
    "bake",
    "glaze",
    "box",
]
BISCUIT_RULES = [
    ("chill dough", "roll dough"),
    ("roll dough", "cut shapes"),
    ("cut shapes", "proof"),
    ("proof", "bake"),
    ("bake", "glaze"),
    ("glaze", "box"),
]

# Two branches that meet again. "combine" is reached down both, and the second
# arrival lands on a step that is already finished -- not a circle.
DIAMOND_STEPS = ["measure", "mix wet", "mix dry", "combine"]
DIAMOND_RULES = [
    ("measure", "mix wet"),
    ("measure", "mix dry"),
    ("mix wet", "combine"),
    ("mix dry", "combine"),
]

# The rules chase each other: temper before dip, dip before set, set before
# temper.
CIRCLE_STEPS = ["temper chocolate", "dip", "set", "wrap"]
CIRCLE_RULES = [
    ("temper chocolate", "dip"),
    ("dip", "set"),
    ("set", "temper chocolate"),
    ("set", "wrap"),
]

# A long list whose circle sits in the first two steps. The colour walk finds it
# without reading the rest; the counting version reads all of it first.
BUSY_STEPS = ["swap pans", "clear rack"] + [f"tray {slot:03d}" for slot in range(500)]
BUSY_RULES = [("swap pans", "clear rack"), ("clear rack", "swap pans")] + [
    (f"tray {slot:03d}", f"tray {slot + 1:03d}") for slot in range(499)
]


def _rules_by_step(
    steps: list[str], must_precede: list[tuple[str, str]]
) -> dict[str, list[str]]:
    """Turn the rule list into "once this step is done, these become possible".

    Args:
        steps: Every prep step on the list.
        must_precede: Pairs (a, b) meaning a has to be done before b starts.

    Returns:
        A dict from each step to the steps it unblocks.

    Raises:
        ValueError: A rule names a step that is not on the list.
    """
    after: dict[str, list[str]] = {step: [] for step in steps}
    for earlier, later in must_precede:
        for name in (earlier, later):
            if name not in after:
                raise ValueError(
                    f"rule names prep step {name!r}, which is not on the list"
                )
        after[earlier].append(later)
    return after


def _audit_by_colour(after: dict[str, list[str]]) -> tuple[bool, int]:
    """The three-colour walk.

    White is a step not looked at yet, grey is a step on the path we are
    standing on right now, black is a step whose whole branch is finished. A
    rule that points at a grey step is the circle. A rule that points at a black
    step is a branch we already cleared, and is fine.

    Args:
        after: The unblocks-map from _rules_by_step.

    Returns:
        (schedulable, steps_entered). The second number is how many prep steps
        the walk actually stepped into before it could answer.
    """
    colour: dict[str, int] = {step: WHITE for step in after}
    entered = 0

    def walk(step: str) -> bool:
        nonlocal entered
        entered += 1
        colour[step] = GREY
        for later in after[step]:
            if colour[later] == GREY:
                return False
            if colour[later] == WHITE and not walk(later):
                return False
        colour[step] = BLACK
        return True

    for step in after:
        if colour[step] == WHITE and not walk(step):
            return (False, entered)
    return (True, entered)


def _audit_by_counting(after: dict[str, list[str]]) -> tuple[bool, int]:
    """Kahn's counting.

    Every step gets a tally of how many rules are still holding it back. Steps
    on zero are ready; doing one lowers the tally of everything it unblocks. If
    the ready pile runs dry before every step has been done, the leftovers are
    holding each other back in a circle.

    Args:
        after: The unblocks-map from _rules_by_step.

    Returns:
        (schedulable, steps_read). The second number is how many prep steps had
        to be read to build the waiting-on table, which is all of them.
    """
    waiting_on: dict[str, int] = {}
    steps_read = 0
    for step in after:
        waiting_on[step] = 0
        steps_read += 1
    for laters in after.values():
        for later in laters:
            waiting_on[later] += 1

    ready: deque[str] = deque(step for step in after if waiting_on[step] == 0)
    done = 0
    while ready:
        step = ready.popleft()
        done += 1
        for later in after[step]:
            waiting_on[later] -= 1
            if waiting_on[later] == 0:
                ready.append(later)
    return (done == len(after), steps_read)


def can_schedule(steps: list[str], must_precede: list[tuple[str, str]]) -> bool:
    """Say whether every prep step can be done in some legal order.

    Args:
        steps: Every prep step on the list.
        must_precede: Pairs (a, b) meaning a has to be done before b starts.

    Returns:
        True when a legal order exists, False when the rules chase each other in
        a circle. An empty list with no rules is True -- nothing to do is
        trivially doable.

    Raises:
        ValueError: A rule names a step that is not on the list.
    """
    return _audit_by_colour(_rules_by_step(steps, must_precede))[0]


def can_schedule_by_counting(
    steps: list[str], must_precede: list[tuple[str, str]]
) -> bool:
    """The same answer, reached by Kahn's counting instead. Kept for comparison.

    Args:
        steps: Every prep step on the list.
        must_precede: Pairs (a, b) meaning a has to be done before b starts.

    Returns:
        The same bool can_schedule returns, on every input.

    Raises:
        ValueError: A rule names a step that is not on the list.
    """
    return _audit_by_counting(_rules_by_step(steps, must_precede))[0]


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[str, list[str], list[tuple[str, str]]]] = [
        ("biscuit line", BISCUIT_STEPS, BISCUIT_RULES),
        ("two branches that meet", DIAMOND_STEPS, DIAMOND_RULES),
        ("rules in a circle", CIRCLE_STEPS, CIRCLE_RULES),
        ("nothing on the list", [], []),
    ]
    for label, steps, rules in cases:
        print(f"{label:24s} -> {can_schedule(steps, rules)}")

    colour_answer, entered = _audit_by_colour(_rules_by_step(BUSY_STEPS, BUSY_RULES))
    counting_answer, steps_read = _audit_by_counting(
        _rules_by_step(BUSY_STEPS, BUSY_RULES)
    )
    print(f"a {len(BUSY_STEPS)}-step list whose circle is in the first two steps")
    print(f"  colour walk   : {colour_answer}, after entering {entered} steps")
    print(f"  Kahn counting : {counting_answer}, after reading {steps_read} steps")

    assert can_schedule(BISCUIT_STEPS, BISCUIT_RULES) is True
    assert can_schedule(DIAMOND_STEPS, DIAMOND_RULES) is True
    assert can_schedule(CIRCLE_STEPS, CIRCLE_RULES) is False
    assert can_schedule([], []) is True
    assert can_schedule(["proof"], []) is True
    assert can_schedule(["proof"], [("proof", "proof")]) is False
    assert can_schedule(BUSY_STEPS, BUSY_RULES) is False

    for _, steps, rules in cases:
        assert can_schedule(steps, rules) == can_schedule_by_counting(steps, rules)
    assert can_schedule_by_counting(BUSY_STEPS, BUSY_RULES) is False

    try:
        can_schedule(BISCUIT_STEPS, [("bake", "wash up")])
    except ValueError as err:
        assert "wash up" in str(err)
    else:
        raise AssertionError("a rule naming an unlisted step should raise ValueError")

    print("All checks passed.")
