"""problem-05-grant-round-picks-solution.py — which projects a small fund should back.

A community fund holds a reserve. Every project has an unlock — the reserve the
fund must already hold before the trustees will sign it off — and a payout that
goes back into the reserve when the project finishes. The fund may back only a
few projects in a round, and each one it backs may unlock the next.

Two heaps: a min-heap of projects by unlock, so the cheapest to unlock is
always next in line, and a max-heap of the projects already unlocked, so the
biggest payout is always on top.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
# (project, reserve needed to unlock it, payout it returns)
PROJECTS: list[tuple[str, int, int]] = [
    ("Roof repair", 0, 30),
    ("Kiln rebuild", 40, 90),
    ("Tool shed", 25, 20),
    ("Van service", 10, 45),
    ("Server rack", 120, 200),
]

START_RESERVE = 15
ROUND_SIZE = 3


# ---- Your task ----
def grant_round(
    projects: list[tuple[str, int, int]], reserve: int, picks: int
) -> tuple[int, list[str]]:
    """Return the reserve at the end of the round and the projects backed.

    Args:
        projects: (name, unlock, payout) rows, in any order.
        reserve: What the fund holds when the round opens.
        picks: How many projects the round may back at most.

    Returns:
        (closing reserve, project names in the order they were backed). The
        round stops early when nothing is unlocked, so it can back fewer than
        `picks` projects.
    """
    waiting = [(unlock, payout, name) for name, unlock, payout in projects]
    heapq.heapify(waiting)
    unlocked: list[tuple[int, str]] = []
    backed: list[str] = []

    for _ in range(picks):
        while waiting and waiting[0][0] <= reserve:
            _, payout, name = heapq.heappop(waiting)
            heapq.heappush(unlocked, (-payout, name))
        if not unlocked:
            break
        stored, name = heapq.heappop(unlocked)
        reserve += -stored
        backed.append(name)
    return reserve, backed


def locked_out(
    projects: list[tuple[str, int, int]], reserve: int, picks: int
) -> list[str]:
    """Return the projects the round never reached, cheapest unlock first.

    Args:
        projects: (name, unlock, payout) rows.
        reserve: What the fund holds when the round opens.
        picks: How many projects the round may back at most.

    Returns:
        Names, ordered by unlock then by name.
    """
    _, backed = grant_round(projects, reserve, picks)
    left = [row for row in projects if row[0] not in set(backed)]
    return [name for name, _, _ in sorted(left, key=lambda row: (row[1], row[0]))]


def best_single(projects: list[tuple[str, int, int]], reserve: int) -> str | None:
    """Return the one project worth backing if the round could back only one.

    Args:
        projects: (name, unlock, payout) rows.
        reserve: What the fund holds when the round opens.

    Returns:
        The name of the unlocked project with the biggest payout, or None when
        nothing is unlocked. Ties go to the name that sorts earlier.
    """
    _, backed = grant_round(projects, reserve, 1)
    return backed[0] if backed else None


# ---- Self-check ----
if __name__ == "__main__":
    closing, backed = grant_round(PROJECTS, START_RESERVE, ROUND_SIZE)
    print(f"opening reserve: {START_RESERVE}")
    print(f"projects backed: {backed}")
    print(f"closing reserve: {closing}")
    print(f"never reached  : {locked_out(PROJECTS, START_RESERVE, ROUND_SIZE)}")
    print(f"best single pick: {best_single(PROJECTS, START_RESERVE)}")

    print(f"nothing unlocked: {grant_round(PROJECTS, 0, 3)}")
    print(f"no picks allowed: {grant_round(PROJECTS, START_RESERVE, 0)}")
    print(f"no projects: {grant_round([], 50, 3)}")
    print(f"more picks than projects: {grant_round(PROJECTS, START_RESERVE, 99)}")
    print(f"best single on a bare fund: {best_single(PROJECTS, 0)}")

    assert backed == ["Van service", "Kiln rebuild", "Server rack"]
    assert closing == 350
    assert locked_out(PROJECTS, START_RESERVE, ROUND_SIZE) == ["Roof repair", "Tool shed"]
    assert best_single(PROJECTS, START_RESERVE) == "Van service"
    assert grant_round(PROJECTS, 0, 3) == (
        165,
        ["Roof repair", "Van service", "Kiln rebuild"],
    )
    assert grant_round(PROJECTS, START_RESERVE, 0) == (15, [])
    assert grant_round([], 50, 3) == (50, [])
    assert grant_round(PROJECTS, START_RESERVE, 99)[0] == 400
    assert best_single(PROJECTS, 0) == "Roof repair"
    print("All checks passed.")
