"""exercise-05-shunting-rebate-legs-solution.py — when a leg gives minutes back.

A freight yard moves a wagon between sidings. Most legs cost shunting
minutes. A few are downhill runs the yard books as a rebate: they give
minutes back, so their cost is a negative number.

Negative costs break the rule Dijkstra is built on, and this file shows it
happening rather than describing it. Four functions:

  best_net_minutes     — the true cheapest net minutes, by repeated relaxing
  refund_loop_sidings  — the sidings poisoned by a loop that never stops paying
  dijkstra_net_minutes — the settled-set Dijkstra, for comparison only
  comparison_rows      — the two answers side by side

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

import heapq
from collections import deque

# ---- Given data ----
# (from siding, to siding, net shunting minutes; a rebate leg is negative)
Leg = tuple[str, str, int]

LEGS: list[Leg] = [
    ("Ash Sidings", "Bar Road", 3),
    ("Ash Sidings", "Coal Drop", 4),
    ("Coal Drop", "Bar Road", -2),
    ("Bar Road", "Dock Spur", 5),
    ("Coal Drop", "Dock Spur", 6),
    ("Bar Road", "Engine Shed", 8),
    ("Dock Spur", "Engine Shed", 2),
]

# One extra leg turns Bar Road -> Dock Spur -> Bar Road into a loop that pays
# out one minute every time round.
LOOPING_LEGS: list[Leg] = LEGS + [("Dock Spur", "Bar Road", -6)]


# ---- Your task ----
def all_sidings(legs: list[Leg]) -> list[str]:
    """Return every siding named in the legs, in name order.

    Args:
        legs: Every leg, as (from, to, net minutes).

    Returns:
        A sorted list of siding names, with no repeats.
    """
    named: set[str] = set()
    for source, target, _ in legs:
        named.add(source)
        named.add(target)
    return sorted(named)


def best_net_minutes(legs: list[Leg], start: str) -> dict[str, int] | None:
    """Return the cheapest net minutes from start to every reachable siding.

    The whole leg list is swept over and over. One sweep is enough to settle
    any route one leg long, two sweeps settle any route two legs long, and a
    route that never repeats a siding cannot be longer than one leg fewer
    than there are sidings. So that many sweeps is always enough.

    Args:
        legs: Every leg, as (from, to, net minutes).
        start: The siding the wagon begins at.

    Returns:
        A dict of siding -> net minutes. A siding that cannot be reached is
        left out. None when a refund loop is reachable, because then no
        cheapest answer exists at all.
    """
    sidings = all_sidings(legs)
    cost: dict[str, int] = {start: 0}

    for _ in range(max(len(sidings) - 1, 0)):
        changed = False
        for source, target, minutes in legs:
            if source in cost and cost[source] + minutes < cost.get(target, float("inf")):
                cost[target] = cost[source] + minutes
                changed = True
        if not changed:
            break

    for source, target, minutes in legs:      # one sweep too many, on purpose
        if source in cost and cost[source] + minutes < cost.get(target, float("inf")):
            return None
    return cost


def refund_loop_sidings(legs: list[Leg], start: str) -> list[str]:
    """Return every siding whose cost a refund loop drags down without limit.

    Args:
        legs: Every leg, as (from, to, net minutes).
        start: The siding the wagon begins at.

    Returns:
        A sorted list of siding names. Empty when there is no refund loop
        reachable from start.
    """
    sidings = all_sidings(legs)
    cost: dict[str, float] = {start: 0}

    for _ in range(max(len(sidings) - 1, 0)):
        for source, target, minutes in legs:
            if source in cost and cost[source] + minutes < cost.get(target, float("inf")):
                cost[target] = cost[source] + minutes

    onward: dict[str, list[str]] = {siding: [] for siding in sidings}
    poisoned: set[str] = set()
    for source, target, minutes in legs:
        onward[source].append(target)
        if source in cost and cost[source] + minutes < cost.get(target, float("inf")):
            poisoned.add(target)

    queue = deque(poisoned)
    while queue:                              # anything downstream is poisoned too
        siding = queue.popleft()
        for target in onward[siding]:
            if target not in poisoned:
                poisoned.add(target)
                queue.append(target)
    return sorted(poisoned)


# ---- Given: the settled-set Dijkstra from Exercise 2, unchanged ----
def dijkstra_net_minutes(legs: list[Leg], start: str) -> dict[str, int]:
    """Dijkstra, which is correct only while every leg costs nothing to skip.

    Do not fix it. It is here so the two answers can be printed side by side.

    Args:
        legs: Every leg, as (from, to, net minutes).
        start: The siding the wagon begins at.

    Returns:
        A dict of siding -> net minutes. Where a rebate leg improves a
        siding after that siding was settled, the siding's own number is
        quietly corrected but its outgoing legs are never swept again, so
        everything downstream of it stays too high.
    """
    onward: dict[str, list[tuple[str, int]]] = {s: [] for s in all_sidings(legs)}
    for source, target, minutes in legs:
        onward[source].append((target, minutes))

    cost: dict[str, int] = {start: 0}
    settled: set[str] = set()
    queue: list[tuple[int, str]] = [(0, start)]
    while queue:
        so_far, siding = heapq.heappop(queue)
        if siding in settled:
            continue
        settled.add(siding)
        for target, minutes in onward[siding]:
            total = so_far + minutes
            if total < cost.get(target, float("inf")):
                cost[target] = total
                heapq.heappush(queue, (total, target))
    return cost


def comparison_rows(legs: list[Leg], start: str) -> list[str]:
    """Return one printable row per siding, sweeping beside Dijkstra.

    Args:
        legs: Every leg, as (from, to, net minutes).
        start: The siding the wagon begins at.

    Returns:
        Rows in siding-name order. A row where the two disagree is marked.
    """
    truth = best_net_minutes(legs, start)
    if truth is None:
        return ["no cheapest answer exists: a refund loop is reachable"]
    guess = dijkstra_net_minutes(legs, start)
    rows = []
    for siding in all_sidings(legs):
        if siding not in truth:
            continue
        flag = "" if guess[siding] == truth[siding] else "   <- Dijkstra is high"
        rows.append(f"{siding:<13}{truth[siding]:6d}{guess[siding]:10d}{flag}")
    return rows


# ---- Self-check ----
if __name__ == "__main__":
    print("siding       sweeps  Dijkstra")
    for row in comparison_rows(LEGS, "Ash Sidings"):
        print(row)

    print()
    print("with the Dock Spur -> Bar Road rebate leg added")
    print(f"  best_net_minutes    -> {best_net_minutes(LOOPING_LEGS, 'Ash Sidings')}")
    print(f"  refund_loop_sidings -> {refund_loop_sidings(LOOPING_LEGS, 'Ash Sidings')}")

    truth = best_net_minutes(LEGS, "Ash Sidings")
    assert truth == {
        "Ash Sidings": 0,
        "Coal Drop": 4,
        "Bar Road": 2,
        "Dock Spur": 7,
        "Engine Shed": 9,
    }
    guess = dijkstra_net_minutes(LEGS, "Ash Sidings")
    assert guess["Bar Road"] == 2               # the number was fixed after settling
    assert guess["Dock Spur"] == 8              # but nothing downstream was told
    assert guess["Engine Shed"] == 10
    assert sum(1 for siding in truth if truth[siding] != guess[siding]) == 2

    assert refund_loop_sidings(LEGS, "Ash Sidings") == []
    assert best_net_minutes(LOOPING_LEGS, "Ash Sidings") is None
    assert refund_loop_sidings(LOOPING_LEGS, "Ash Sidings") == [
        "Bar Road",
        "Dock Spur",
        "Engine Shed",
    ]
    assert best_net_minutes(LEGS, "Engine Shed") == {"Engine Shed": 0}
    print("All checks passed.")
