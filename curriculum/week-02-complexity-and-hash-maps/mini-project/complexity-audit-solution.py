"""complexity-audit-solution.py — evidence for five rewritten cost sections.

The Week 2 mini-project asks you to go back to your five Week 1 write-ups and
rewrite every cost section to the five-piece structure. Four of those five
sections have to name an alternative approach, and for three of them the
honest sentence is not "the alternative is slower" but "the alternative is
wrong".

A sentence like that is cheap to write and expensive to be wrong about. This
file is the evidence: for each of the five drills it runs the shipped approach
and the rejected alternative on the same inputs, and reports where they part
company. Paste the disagreeing input into your write-up. A claim with an input
attached is worth five without one.

Every function here is a Week 1 contract, restated. Nothing in this file is new
algorithm work; the new work is the audit at the bottom.
"""

from collections import Counter


# ---- Drill 1 — Reverse the Siding ----
def reverse_siding(cars: list[str], start: int, end: int) -> int:
    """Shipped: swap in place. O(n) time, O(1) space, and it counts the swaps."""
    if not (0 <= start < end < len(cars)):
        return 0
    swaps = 0
    left, right = start, end
    while left < right:
        cars[left], cars[right] = cars[right], cars[left]
        swaps += 1
        left += 1
        right -= 1
    return swaps


def reverse_siding_sliced(cars: list[str], start: int, end: int) -> int:
    """Alternative: slice-assign. O(m) auxiliary space, and it cannot count."""
    if not (0 <= start < end < len(cars)):
        return 0
    cars[start : end + 1] = cars[start : end + 1][::-1]
    return 0  # there is no swap count to return; nothing was swapped


# ---- Drill 2 — The Mirror Serial ----
def first_mirror_break(serial: str) -> int | None:
    """Shipped: two pointers over the printed serial. O(n) time, O(1) space."""
    left, right = 0, len(serial) - 1
    while left < right:
        while left < right and not serial[left].isalnum():
            left += 1
        while left < right and not serial[right].isalnum():
            right -= 1
        if serial[left].lower() != serial[right].lower():
            return left
        left += 1
        right -= 1
    return None


def first_mirror_break_filtered(serial: str) -> int | None:
    """Alternative: filter first, then compare. Renumbers the positions."""
    significant = [character.lower() for character in serial if character.isalnum()]
    left, right = 0, len(significant) - 1
    while left < right:
        if significant[left] != significant[right]:
            return left  # an index into the filtered string, not the printed one
        left += 1
        right -= 1
    return None


# ---- Drill 3 — The Widest Ballast Pair ----
def widest_ballast_pair(weights: list[int], correction: int) -> tuple[int, int] | None:
    """Shipped: converging pointers on a sorted row. O(n) time, O(1) space."""
    left, right = 0, len(weights) - 1
    while left < right:
        total = weights[left] + weights[right]
        if total == correction:
            return (left, right)
        if total < correction:
            left += 1
        else:
            right -= 1
    return None


def widest_ballast_pair_hashed(
    weights: list[int], correction: int
) -> tuple[int, int] | None:
    """Alternative: this week's complement map. Finds the earliest pair, not the widest."""
    earliest_at: dict[int, int] = {}
    for position, weight in enumerate(weights):
        complement = correction - weight
        if complement in earliest_at:
            return (earliest_at[complement], position)
        if weight not in earliest_at:
            earliest_at[weight] = position
    return None


# ---- Drill 4 — The Stuck Gauge ----
def collapse_stuck_readings(levels: list[int]) -> int:
    """Shipped: read and write pointers, in place. Collapses adjacent runs only."""
    if not levels:
        return 0
    write = 1
    for read in range(1, len(levels)):
        if levels[read] != levels[write - 1]:
            levels[write] = levels[read]
            write += 1
    return len(levels) - write


def collapse_stuck_readings_seen(levels: list[int]) -> int:
    """Alternative: a set of values already seen. Drops every repeat, not every run."""
    if not levels:
        return 0
    seen: set[int] = set()
    write = 0
    for read in range(len(levels)):
        if levels[read] not in seen:
            seen.add(levels[read])
            levels[write] = levels[read]
            write += 1
    return len(levels) - write


# ---- Drill 5 — The Market Awning ----
def max_curtain_area(pole_heights: list[int]) -> int:
    """Shipped: converging pointers, move the shorter side. O(n) time, O(1) space."""
    left, right = 0, len(pole_heights) - 1
    best = 0
    while left < right:
        height = min(pole_heights[left], pole_heights[right])
        best = max(best, height * (right - left - 1))
        if pole_heights[left] <= pole_heights[right]:
            left += 1
        else:
            right -= 1
    return best


def max_curtain_area_brute(pole_heights: list[int]) -> int:
    """Alternative: every pair. O(n^2) time, O(1) space. Same answer, worse cost."""
    best = 0
    for left in range(len(pole_heights)):
        for right in range(left + 1, len(pole_heights)):
            height = min(pole_heights[left], pole_heights[right])
            best = max(best, height * (right - left - 1))
    return best


# ---- The audit ----
def audit_reverse_siding() -> list[str]:
    """Drill 1: does the slice version answer the question that was asked?"""
    disagreements: list[str] = []
    for cars, start, end in [
        (["HOP", "TNK", "BOX", "GON", "FLT"], 1, 3),
        (["HOP", "TNK", "BOX", "GON", "FLT"], 0, 4),
        (["HOP", "TNK", "BOX", "GON"], 0, 3),
        (["HOP"], 0, 0),
        (["HOP", "TNK", "BOX"], 2, 1),
    ]:
        mine, theirs = list(cars), list(cars)
        shipped = reverse_siding(mine, start, end)
        other = reverse_siding_sliced(theirs, start, end)
        if mine != theirs or shipped != other:
            disagreements.append(
                f"cars={cars} start={start} end={end}: "
                f"shipped returned {shipped}, slice returned {other}"
            )
    return disagreements


def audit_mirror_serial() -> list[str]:
    """Drill 2: does filtering first still point at the right printed position?"""
    disagreements: list[str] = []
    for serial in ["RT7-e77-E7tr", "RT7-e77-E8tr", "8a-b-c8", "--G9", "Bb", "-K-", "--  --", ""]:
        shipped = first_mirror_break(serial)
        other = first_mirror_break_filtered(serial)
        if shipped != other:
            disagreements.append(
                f"serial={serial!r}: shipped {shipped}, filtered {other}"
            )
    return disagreements


def audit_ballast_pair() -> list[str]:
    """Drill 3: does the complement map pick the pair this contract asks for?"""
    disagreements: list[str] = []
    for weights, correction in [
        ([120, 340, 500, 660, 880], 1000),
        ([-400, -100, 0, 100, 300], 0),
        ([100, 100, 100, 100], 200),
        ([200, 200, 800, 800], 1000),
        ([150, 150], 300),
    ]:
        shipped = widest_ballast_pair(weights, correction)
        other = widest_ballast_pair_hashed(weights, correction)
        if shipped != other:
            disagreements.append(
                f"weights={weights} correction={correction}: "
                f"shipped {shipped}, hash map {other}"
            )
    return disagreements


def audit_stuck_gauge() -> list[str]:
    """Drill 4: does a seen-set collapse runs, or does it deduplicate?"""
    disagreements: list[str] = []
    for levels in [
        [412, 412, 412, 415, 415, 409],
        [300, 300, 305, 300],
        [777, 777, 777, 777],
        [500, 501, 502],
        [-2, -2, 0, 0, -2],
    ]:
        mine, theirs = list(levels), list(levels)
        dropped_mine = collapse_stuck_readings(mine)
        dropped_theirs = collapse_stuck_readings_seen(theirs)
        kept_mine = mine[: len(levels) - dropped_mine]
        kept_theirs = theirs[: len(levels) - dropped_theirs]
        if kept_mine != kept_theirs:
            disagreements.append(
                f"levels={levels}: shipped kept {kept_mine}, seen-set kept {kept_theirs}"
            )
    return disagreements


def audit_market_awning() -> list[str]:
    """Drill 5: does the greedy scan ever disagree with checking every pair?"""
    disagreements: list[str] = []
    rows = [
        [2, 6, 3, 8, 1, 7, 4],
        [2, 7, 5, 5, 7, 2],
        [5, 5],
        [0, 9, 9, 0],
        [4],
        [],
    ]
    # Plus every row of four poles with heights 0..3, so the claim is checked
    # against 256 rows rather than against six hand-picked ones.
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    rows.append([a, b, c, d])
    for poles in rows:
        shipped = max_curtain_area(poles)
        other = max_curtain_area_brute(poles)
        if shipped != other:
            disagreements.append(f"poles={poles}: shipped {shipped}, brute force {other}")
    return disagreements


AUDITS = [
    ("1 Reverse the Siding", "slice-assign reversal", audit_reverse_siding),
    ("2 The Mirror Serial", "filter, then compare", audit_mirror_serial),
    ("3 Widest Ballast Pair", "complement hash map", audit_ballast_pair),
    ("4 The Stuck Gauge", "set of values seen", audit_stuck_gauge),
    ("5 The Market Awning", "every pair, brute force", audit_market_awning),
]


if __name__ == "__main__":
    print("Drill                   Rejected alternative      Verdict")
    print("-" * 72)
    wrong = 0
    for drill, alternative, audit in AUDITS:
        disagreements = audit()
        if disagreements:
            wrong += 1
            verdict = f"WRONG on {len(disagreements)} input(s)"
        else:
            verdict = "agrees; only slower"
        print(f"{drill:<23} {alternative:<25} {verdict}")

    print()
    print("Where they disagree, and on what:")
    for drill, _, audit in AUDITS:
        for line in audit():
            print(f"  {drill[0]}. {line}")

    print()
    print(f"{wrong} of {len(AUDITS)} alternatives are wrong rather than merely slower.")

    # The mini-project's acceptance checklist asks for at least three.
    assert wrong >= 3, "at least three alternatives should be wrong, not just slower"
    # Counter is imported to make the point that it buys nothing here: the
    # gauge question is about adjacency, and a tally has no idea what is next
    # to what.
    assert Counter([300, 300, 305, 300])[300] == 3
    print("All checks passed.")
