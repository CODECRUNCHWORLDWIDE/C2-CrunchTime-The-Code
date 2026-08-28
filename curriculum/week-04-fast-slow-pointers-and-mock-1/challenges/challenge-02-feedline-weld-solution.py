"""challenge-02-feedline-weld-solution.py — where do two feed lines join?

There is no loop anywhere in this problem, which is exactly why it is hard.
The move is to *make* one: tie the end of line A onto the head of line B and
the shared run becomes a ring. Now the week's cycle machinery applies
unchanged — Floyd's tortoise and hare finds a pan inside the ring, and the
entrance walk turns that into the ring's first pan, which is the weld.

Then untie the knot, because a diagnostic that leaves the plant rewired is
not a diagnostic.

The feed lines are built in this file, so it runs on its own with no imports.

The self-checks at the bottom print one line per plant, then
"All checks passed."
"""

from __future__ import annotations


class Pan:
    """One pan on a conveyor. It feeds exactly one other pan, or none."""

    def __init__(self, tag: str, feeds_to: "Pan | None" = None) -> None:
        self.tag = tag
        self.feeds_to = feeds_to


def build_lines(
    lead_a: list[str], lead_b: list[str], shared: list[str]
) -> tuple[Pan | None, Pan | None, list[Pan]]:
    """Wire two feed lines that join onto one shared discharge run.

    Args:
        lead_a: Tags for the pans only line A passes over, in order.
        lead_b: Tags for the pans only line B passes over, in order.
        shared: Tags for the pans both lines pass over. Empty means the two
            lines never meet.

    Returns:
        A triple of (first pan of A, first pan of B, the shared pans). Either
        head is None when that line has no pans at all.
    """
    pans_a = [Pan(tag) for tag in lead_a]
    pans_b = [Pan(tag) for tag in lead_b]
    pans_shared = [Pan(tag) for tag in shared]

    for run in (pans_a, pans_b, pans_shared):
        for earlier, later in zip(run, run[1:]):
            earlier.feeds_to = later
    if pans_shared:
        if pans_a:
            pans_a[-1].feeds_to = pans_shared[0]
        if pans_b:
            pans_b[-1].feeds_to = pans_shared[0]

    head_a = (pans_a or pans_shared or [None])[0]
    head_b = (pans_b or pans_shared or [None])[0]
    return head_a, head_b, pans_shared


def _last_pan(first: Pan) -> Pan:
    """Return the pan at the end of a run that is known to terminate."""
    last = first
    while last.feeds_to is not None:
        last = last.feeds_to
    return last


def _ring_entrance(first: Pan) -> tuple[Pan, int] | None:
    """Return the first pan of the ring reachable from `first`, and its lead.

    Args:
        first: Where to start walking.

    Returns:
        A pair of (first pan of the ring, pans in front of it), or None when
        the run has no ring and simply ends.
    """
    slow = first
    fast = first
    while fast is not None and fast.feeds_to is not None:
        slow = slow.feeds_to
        fast = fast.feeds_to.feeds_to
        if slow is fast:
            break
    else:
        return None

    finder = first
    lead = 0
    while finder is not slow:
        finder = finder.feeds_to
        slow = slow.feeds_to
        lead += 1
    return finder, lead


def find_weld(line_a: Pan | None, line_b: Pan | None) -> tuple[Pan, int, int] | None:
    """Return the weld the two feed lines share, and each line's lead-in.

    Args:
        line_a: The first pan of one feed line, or None for no line.
        line_b: The first pan of the other feed line, or None for no line.

    Returns:
        A triple of (weld pan, pans in front of it on line A, pans in front
        of it on line B), or None when the two lines never meet. Both lines
        are left wired exactly as they were found.
    """
    if line_a is None or line_b is None:
        return None

    tail_a = _last_pan(line_a)
    tail_a.feeds_to = line_b  # Tie the knot: the shared run becomes a ring.
    found = _ring_entrance(line_a)
    tail_a.feeds_to = None  # Untie it before doing anything else.

    if found is None:
        return None
    weld, lead_a = found

    lead_b = 0
    pan = line_b
    while pan is not weld:
        pan = pan.feeds_to
        lead_b += 1
    return weld, lead_a, lead_b


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        ("A:2 B:3 shared:2", ["a1", "a2"], ["b1", "b2", "b3"], ["w1", "w2"], (2, 3)),
        ("A:0 B:2 shared:1", [], ["b1", "b2"], ["w1"], (0, 2)),
        ("A:1 B:0 shared:3", ["a1"], [], ["w1", "w2", "w3"], (1, 0)),
        ("same head, shared:4", [], [], ["w1", "w2", "w3", "w4"], (0, 0)),
        ("A:3 B:1 shared:1", ["P", "P", "P"], ["P"], ["P"], (3, 1)),
    ]

    for label, lead_a, lead_b, shared, expected in CASES:
        head_a, head_b, pans_shared = build_lines(lead_a, lead_b, shared)
        result = find_weld(head_a, head_b)
        assert result is not None, f"{label}: these lines do meet"
        weld, found_a, found_b = result
        assert weld is pans_shared[0], f"{label}: wrong pan, compare by identity"
        assert (found_a, found_b) == expected, f"{label}: got {(found_a, found_b)}"
        assert _last_pan(head_a) is pans_shared[-1], f"{label}: line A was left tied"
        print(f"{label:<20} weld {weld.tag}, lead-ins {found_a} and {found_b}")

    SEPARATE = [
        ("two runs, no weld", ["a1", "a2"], ["b1", "b2", "b3"]),
        ("one pan each", ["a1"], ["b1"]),
    ]

    for label, lead_a, lead_b in SEPARATE:
        head_a, head_b, _ = build_lines(lead_a, lead_b, [])
        assert find_weld(head_a, head_b) is None, f"{label}: no weld here"
        assert _last_pan(head_a).tag == lead_a[-1], f"{label}: line A was left tied"
        print(f"{label:<20} no weld")

    assert find_weld(None, build_lines([], ["b1"], [])[1]) is None
    print(f"{'no line A at all':<20} no weld")

    print("All checks passed.")
