"""problem-03-sled-team-rotation-solution.py — who runs at the front today.

A six-dog team rotates its lead every day: on day 1 the second dog leads, on
day 2 the third, and so on round the loop.

Three ways to answer that, and only one of them is free. Rotating a list
builds a new list. Rotating a deque moves a pointer. Working out the lead
with one modulo touches nothing at all.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import deque

TEAM: list[str] = ["Nika", "Bram", "Oso", "Pilot", "Skua", "Tuk"]


def rotate_list(team: list[str], steps: int) -> list[str]:
    """Return a NEW running order with the team rotated forward.

    Args:
        team: The running order, lead dog first.
        steps: How many places to move forward. May be bigger than the team
            and may be negative.

    Returns:
        A new list. The team handed in is not changed.
    """
    if not team:
        return []
    cut = steps % len(team)
    return team[cut:] + team[:cut]


def rotate_deque(team: list[str], steps: int) -> list[str]:
    """Return the same running order, rotated with a deque.

    Args:
        team: The running order, lead dog first.
        steps: How many places to move forward.

    Returns:
        A new list. `deque.rotate` counts the other way, so the sign flips.
    """
    ring = deque(team)
    ring.rotate(-steps)
    return list(ring)


def lead_on_day(team: list[str], day: int) -> str | None:
    """Return the dog leading on a given day, without rotating anything.

    Args:
        team: The running order, lead dog first.
        day: Days since the season started. Day 0 is the order as written.

    Returns:
        The lead dog's name, or None when there is no team.
    """
    if not team:
        return None
    return team[day % len(team)]


# ---- Self-check ----
if __name__ == "__main__":
    for day in (0, 1, 2, 13):
        order = rotate_list(TEAM, day)
        print(f"day {day:>2}  lead {lead_on_day(TEAM, day):<6} order: {', '.join(order)}")

    for steps in range(-8, 9):
        assert rotate_list(TEAM, steps) == rotate_deque(TEAM, steps)
        assert rotate_list(TEAM, steps)[0] == lead_on_day(TEAM, steps)

    assert rotate_list(TEAM, 0) == TEAM
    assert rotate_list(TEAM, 6) == TEAM
    assert rotate_list(TEAM, 2)[0] == "Oso"
    assert rotate_list(TEAM, -1)[0] == "Tuk"
    assert lead_on_day(TEAM, 13) == "Bram"
    assert rotate_list([], 3) == []
    assert lead_on_day([], 3) is None
    assert TEAM[0] == "Nika"  # the running order is untouched
    print("All checks passed.")
