"""problem-06-relay-reliability-solution.py — the relay most likely to get through.

A harbour passes messages between boats by short-range radio. Each radio hop
works some fraction of the time: a hop with reliability 0.9 gets the message
through nine times in ten. A relay through several boats only works if every
hop on it works, so the chance of the whole relay is the hops multiplied
together, never added.

Multiplying makes a route worse the longer it gets, and the job is to make
that number as large as possible rather than as small as possible. The search
is otherwise the same shape as a shortest-path search.

  best_relay   — the likeliest route, its chance, and how many hops it takes

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
# (boat, boat, chance one hop between them gets through)
Hop = tuple[str, str, float]

HOPS: list[Hop] = [
    ("Anvil", "Bosun", 0.5),
    ("Anvil", "Cutter", 0.9),
    ("Cutter", "Bosun", 0.5),
    ("Bosun", "Dredger", 0.8),
    ("Cutter", "Dredger", 0.4),
    ("Dredger", "Ebb", 0.9),
]

BOATS: list[str] = ["Anvil", "Bosun", "Cutter", "Dredger", "Ebb", "Fluke"]


# ---- Your task ----
def build_radio(hops: list[Hop]) -> dict[str, list[tuple[str, float]]]:
    """Return the hops keyed by boat, both ways round.

    Args:
        hops: Every radio hop, as (boat, boat, chance).

    Returns:
        A dict where radio[boat] is a list of (other boat, chance). Radio
        works both ways, so each hop appears under both boats.
    """
    radio: dict[str, list[tuple[str, float]]] = {}
    for here, there, chance in hops:
        radio.setdefault(here, []).append((there, chance))
        radio.setdefault(there, []).append((here, chance))
    return radio


def best_relay(hops: list[Hop], start: str, end: str) -> tuple[float, int] | None:
    """Return the best chance of getting a message from start to end.

    The queue holds the negative of the chance, because Python's heap always
    hands back the smallest item and the largest chance is wanted first.
    Negating turns "largest chance" into "smallest number", which is what the
    heap is good at.

    Args:
        hops: Every radio hop, as (boat, boat, chance).
        start: The boat sending the message.
        end: The boat that has to receive it.

    Returns:
        (chance rounded to six decimal places, number of hops). Where two
        relays have the same chance the one with fewer hops wins. None when
        no relay of working hops connects the two boats.
    """
    radio = build_radio(hops)
    best: dict[str, tuple[float, int]] = {start: (1.0, 0)}
    settled: set[str] = set()
    queue: list[tuple[float, int, str]] = [(-1.0, 0, start)]

    while queue:
        negative_chance, hop_count, boat = heapq.heappop(queue)
        if boat in settled:
            continue
        settled.add(boat)
        if boat == end:
            return round(-negative_chance, 6), hop_count
        for other, chance in radio.get(boat, []):
            onward = -negative_chance * chance
            known_chance, known_hops = best.get(other, (-1.0, 0))
            if onward > known_chance or (
                onward == known_chance and hop_count + 1 < known_hops
            ):
                best[other] = (onward, hop_count + 1)
                heapq.heappush(queue, (-onward, hop_count + 1, other))

    return None


def relay_rows(hops: list[Hop], boats: list[str], start: str) -> list[str]:
    """Return one printable row per boat, best chance and hop count.

    Args:
        hops: Every radio hop, as (boat, boat, chance).
        boats: Every boat in the harbour, including any with no radio hop.
        start: The boat sending the message.

    Returns:
        Rows in boat-name order. A boat no relay reaches says "no relay".
    """
    rows = []
    for boat in sorted(boats):
        relay = best_relay(hops, start, boat)
        if relay is None:
            rows.append(f"  {boat:<9} no relay")
        else:
            chance, hop_count = relay
            plural = "hop" if hop_count == 1 else "hops"
            rows.append(f"  {boat:<9} {chance:8.6f}  {hop_count} {plural}")
    return rows


# ---- Self-check ----
if __name__ == "__main__":
    print("best relay from Anvil")
    for row in relay_rows(HOPS, BOATS, "Anvil"):
        print(row)

    assert best_relay(HOPS, "Anvil", "Anvil") == (1.0, 0)
    assert best_relay(HOPS, "Anvil", "Cutter") == (0.9, 1)
    # 0.5 direct beats 0.9 * 0.5 = 0.45 through Cutter.
    assert best_relay(HOPS, "Anvil", "Bosun") == (0.5, 1)
    # 0.5 * 0.8 = 0.4 beats 0.9 * 0.4 = 0.36.
    assert best_relay(HOPS, "Anvil", "Dredger") == (0.4, 2)
    assert best_relay(HOPS, "Anvil", "Ebb") == (0.36, 3)
    assert best_relay(HOPS, "Anvil", "Fluke") is None
    assert best_relay(HOPS, "Ebb", "Anvil") == (0.36, 3)

    dead = [("Anvil", "Bosun", 0.0)]
    assert best_relay(dead, "Anvil", "Bosun") == (0.0, 1)
    print("All checks passed.")
