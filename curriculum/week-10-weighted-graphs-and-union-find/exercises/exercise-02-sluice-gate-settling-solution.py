"""exercise-02-sluice-gate-settling-solution.py — the settled set, and what it is for.

An irrigation district opens its head gate and water runs downhill through a
web of channels. Each channel takes a whole number of minutes. Two functions
answer two questions:

  settling_order  — the order the gates get their final answer, and when
  arrival_minutes — the same answer as a plain dict of gate -> minutes

A third function, arrival_minutes_no_settled, is the same algorithm with the
settled set taken out. It is shipped on purpose: running the two side by side
is the whole point of the exercise. One gate, and only one, comes out wrong.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
# (upstream gate, downstream gate, minutes for water to travel)
Channel = tuple[str, str, int]

CHANNELS: list[Channel] = [
    ("Head Gate", "Bywash", 1),
    ("Head Gate", "Cut Sluice", 4),
    ("Bywash", "Cut Sluice", 1),
    ("Cut Sluice", "Tail Weir", 1),
    ("Cut Sluice", "Fold Drain", 6),
    ("Tail Weir", "Fold Drain", 5),
]


# ---- Your task ----
def build_channels(channels: list[Channel]) -> dict[str, list[tuple[str, int]]]:
    """Return the downhill channels keyed by the gate they leave from.

    Args:
        channels: Every channel, as (upstream, downstream, minutes).

    Returns:
        A dict where downhill[gate] is a list of (downstream gate, minutes).
        Every gate named anywhere is a key, including the ones nothing
        leaves from.
    """
    downhill: dict[str, list[tuple[str, int]]] = {}
    for upstream, downstream, minutes in channels:
        downhill.setdefault(upstream, []).append((downstream, minutes))
        downhill.setdefault(downstream, [])
    return downhill


def settling_order(channels: list[Channel], head: str) -> list[tuple[str, int]]:
    """Return the gates in the order their arrival time is settled.

    A gate is settled the first time it comes off the queue. That is the
    moment its answer is final and can never improve again.

    Args:
        channels: Every channel, as (upstream, downstream, minutes).
        head: The gate the water is released from.

    Returns:
        A list of (gate, minutes) in settling order. Water that never
        reaches a gate leaves that gate out of the list entirely.
    """
    downhill = build_channels(channels)
    best: dict[str, int] = {head: 0}
    settled: set[str] = set()
    order: list[tuple[str, int]] = []
    queue: list[tuple[int, str]] = [(0, head)]

    while queue:
        so_far, gate = heapq.heappop(queue)
        if gate in settled:
            continue
        settled.add(gate)
        order.append((gate, so_far))
        for downstream, minutes in downhill.get(gate, []):
            total = so_far + minutes
            if total < best.get(downstream, float("inf")):
                best[downstream] = total
                heapq.heappush(queue, (total, downstream))

    return order


def arrival_minutes(channels: list[Channel], head: str) -> dict[str, int]:
    """Return the minute the water reaches each gate it can reach.

    Args:
        channels: Every channel, as (upstream, downstream, minutes).
        head: The gate the water is released from.

    Returns:
        A dict of gate -> minutes, built from the settling order so the two
        functions can never disagree.
    """
    return dict(settling_order(channels, head))


# ---- Given: the same algorithm with the settled set removed ----
def arrival_minutes_no_settled(channels: list[Channel], head: str) -> dict[str, int]:
    """The broken version. Do not fix it; run it and read the difference.

    Every pop writes its own number straight into the answer, with nothing
    checking whether that gate was already settled. A stale copy of a gate
    that is still sitting in the queue will pop later, carrying a larger
    number, and overwrite the correct one.

    Args:
        channels: Every channel, as (upstream, downstream, minutes).
        head: The gate the water is released from.

    Returns:
        A dict of gate -> minutes that is wrong for at least one gate.
    """
    downhill = build_channels(channels)
    best: dict[str, int] = {head: 0}
    answer: dict[str, int] = {}
    queue: list[tuple[int, str]] = [(0, head)]

    while queue:
        so_far, gate = heapq.heappop(queue)
        answer[gate] = so_far          # <- no settled set, so this can be undone
        for downstream, minutes in downhill.get(gate, []):
            total = so_far + minutes
            if total < best.get(downstream, float("inf")):
                best[downstream] = total
                heapq.heappush(queue, (total, downstream))

    return answer


def compare_tables(channels: list[Channel], head: str) -> list[str]:
    """Return one printable row per gate, correct beside broken.

    Args:
        channels: Every channel, as (upstream, downstream, minutes).
        head: The gate the water is released from.

    Returns:
        Rows sorted by the correct arrival time, then by gate name. A row
        whose two numbers disagree is marked "<- wrong".
    """
    right = arrival_minutes(channels, head)
    wrong = arrival_minutes_no_settled(channels, head)
    rows = []
    for minutes, gate in sorted((m, g) for g, m in right.items()):
        flag = "" if wrong[gate] == minutes else "   <- wrong"
        rows.append(f"{gate:<11}{minutes:4d}{wrong[gate]:7d}{flag}")
    return rows


# ---- Self-check ----
if __name__ == "__main__":
    print("Settling order from Head Gate")
    for place, (gate, minutes) in enumerate(settling_order(CHANNELS, "Head Gate"), 1):
        print(f"  {place}. {gate} at {minutes} min")

    print()
    print("gate        with   without")
    for row in compare_tables(CHANNELS, "Head Gate"):
        print(row)

    right = arrival_minutes(CHANNELS, "Head Gate")
    assert right == {
        "Head Gate": 0,
        "Bywash": 1,
        "Cut Sluice": 2,
        "Tail Weir": 3,
        "Fold Drain": 8,
    }
    assert [gate for gate, _ in settling_order(CHANNELS, "Head Gate")] == [
        "Head Gate",
        "Bywash",
        "Cut Sluice",
        "Tail Weir",
        "Fold Drain",
    ]

    wrong = arrival_minutes_no_settled(CHANNELS, "Head Gate")
    assert wrong["Cut Sluice"] == 4            # the stale 4 popped last and won
    assert wrong["Fold Drain"] == 8            # every other gate is still right
    assert sum(1 for gate in right if right[gate] != wrong[gate]) == 1

    from_bywash = arrival_minutes(CHANNELS, "Bywash")
    assert "Head Gate" not in from_bywash      # water does not run uphill
    assert from_bywash["Fold Drain"] == 7
    print("All checks passed.")
