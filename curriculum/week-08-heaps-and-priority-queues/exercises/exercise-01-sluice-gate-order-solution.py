"""exercise-01-sluice-gate-order-solution.py — the drainage board's opening order.

A polder's sluice gates are opened lowest water head first. This file builds
the queue with `heapq`, reads the front of it without disturbing it, drains it
in service order, and answers a prefix question — "which gates come before the
head reaches 25 cm?" — without draining the rest.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
# (gate name, water head in centimetres, turns of the handwheel to open it)
GATES: list[tuple[str, int, int]] = [
    ("Molenkade", 41, 6),
    ("Zwarte Sloot", 17, 3),
    ("Kruisweg", 41, 2),
    ("Oude Dijk", 8, 9),
    ("Vaartbrug", 23, 4),
    ("Noordkil", 17, 3),
    ("Boezemsluis", 62, 1),
]


# ---- Your task ----
def build_queue(gates: list[tuple[str, int, int]]) -> list[tuple[int, int, str]]:
    """Return a NEW heapified list of (head, turns, name) entries.

    Args:
        gates: (name, head, turns) rows. This list is not modified.

    Returns:
        A list rearranged so that entry 0 is the smallest by
        (head, turns, name). The rest of the list is heap order, not
        sorted order.
    """
    queue = [(head, turns, name) for name, head, turns in gates]
    heapq.heapify(queue)
    return queue


def peek_next(queue: list[tuple[int, int, str]]) -> str | None:
    """Return the name of the gate at the front of the queue, without removing it.

    Args:
        queue: A heapified queue from build_queue.

    Returns:
        The gate's name, or None when the queue is empty.
    """
    if not queue:
        return None
    return queue[0][2]


def drain_order(gates: list[tuple[str, int, int]]) -> list[str]:
    """Return every gate's name in the order the crew opens them.

    Args:
        gates: (name, head, turns) rows. This list is not modified.

    Returns:
        Names, lowest head first; ties by fewer turns, then by name A to Z.
    """
    queue = build_queue(gates)
    order = []
    while queue:
        _, _, name = heapq.heappop(queue)
        order.append(name)
    return order


def gates_below(gates: list[tuple[str, int, int]], limit_cm: int) -> list[str]:
    """Return the names of the gates whose head is under limit_cm, in service order.

    Stops as soon as the front of the queue reaches the limit, so the gates
    behind it are never removed.

    Args:
        gates: (name, head, turns) rows. This list is not modified.
        limit_cm: The head, in centimetres, at which the crew stops.

    Returns:
        Names in service order. Empty when the shallowest gate is already at
        or above the limit.
    """
    queue = build_queue(gates)
    picked = []
    while queue and queue[0][0] < limit_cm:
        _, _, name = heapq.heappop(queue)
        picked.append(name)
    return picked


# ---- Self-check ----
if __name__ == "__main__":
    queue = build_queue(GATES)
    print("heap layout:")
    for head, turns, name in queue:
        print(f"  {head:3d} cm  {turns} turns  {name}")

    print(f"front of the queue: {peek_next(queue)}")
    print(f"queue length after peeking: {len(queue)}")

    print("service order:")
    for position, name in enumerate(drain_order(GATES), 1):
        print(f"  {position}. {name}")

    print(f"under 25 cm: {gates_below(GATES, 25)}")
    print(f"under 5 cm: {gates_below(GATES, 5)}")
    print(f"front of an empty queue: {peek_next([])}")

    assert queue[0] == (8, 9, "Oude Dijk")
    assert len(queue) == 7
    assert peek_next(queue) == "Oude Dijk"
    assert drain_order(GATES)[:3] == ["Oude Dijk", "Noordkil", "Zwarte Sloot"]
    assert drain_order(GATES)[-1] == "Boezemsluis"
    assert drain_order(GATES).index("Kruisweg") < drain_order(GATES).index("Molenkade")
    assert gates_below(GATES, 25) == ["Oude Dijk", "Noordkil", "Zwarte Sloot", "Vaartbrug"]
    assert gates_below(GATES, 5) == []
    assert peek_next([]) is None
    assert GATES[0] == ("Molenkade", 41, 6)  # original rows untouched
    print("All checks passed.")
