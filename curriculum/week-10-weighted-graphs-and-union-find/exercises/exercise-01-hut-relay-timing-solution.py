"""exercise-01-hut-relay-timing-solution.py — how fast a snow reading crosses a ridge.

A row of mountain huts passes one snow-depth reading along by radio. Each
radio link takes a whole number of seconds, and every link points one way,
because a hut's aerial is aimed at the next hut and not back.

Two questions, two functions:

  relay_seconds  — how many seconds until each hut has heard the reading
  slowest_hut    — which hut hears it last, and when

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
# (sending hut, receiving hut, seconds on that link)
Link = tuple[str, str, int]

HUTS: list[str] = [
    "Ash Col",
    "Bell Tarn",
    "Cairn Gap",
    "Dun Force",
    "Elder Scree",
    "Fell Hause",
]

LINKS: list[Link] = [
    ("Ash Col", "Bell Tarn", 4),
    ("Ash Col", "Cairn Gap", 9),
    ("Bell Tarn", "Cairn Gap", 3),
    ("Bell Tarn", "Dun Force", 8),
    ("Cairn Gap", "Dun Force", 5),
    ("Cairn Gap", "Elder Scree", 12),
    ("Cairn Gap", "Fell Hause", 9),
    ("Dun Force", "Elder Scree", 4),
]


# ---- Your task ----
def build_aerials(links: list[Link]) -> dict[str, list[tuple[str, int]]]:
    """Return the one-way link list keyed by sending hut.

    Args:
        links: Every radio link, as (sender, receiver, seconds).

    Returns:
        A dict where aerials[hut] is a list of (receiver, seconds) pairs.
        Every hut named anywhere in links is a key, even one that only
        receives, so a later lookup never has to guess.
    """
    aerials: dict[str, list[tuple[str, int]]] = {}
    for sender, receiver, seconds in links:
        aerials.setdefault(sender, []).append((receiver, seconds))
        aerials.setdefault(receiver, [])
    return aerials


def relay_seconds(links: list[Link], start: str) -> dict[str, int]:
    """Return the earliest second at which each reachable hut hears the reading.

    Args:
        links: Every radio link, as (sender, receiver, seconds).
        start: The hut that reads the snow gauge and starts the relay.

    Returns:
        A dict of hut -> seconds. A hut that can never hear the reading is
        left out of the dict entirely, so `in` is the reachability test.
    """
    aerials = build_aerials(links)
    heard: dict[str, int] = {start: 0}
    settled: set[str] = set()
    queue: list[tuple[int, str]] = [(0, start)]

    while queue:
        so_far, hut = heapq.heappop(queue)
        if hut in settled:
            continue
        settled.add(hut)
        for receiver, seconds in aerials.get(hut, []):
            total = so_far + seconds
            if total < heard.get(receiver, float("inf")):
                heard[receiver] = total
                heapq.heappush(queue, (total, receiver))

    return heard


def slowest_hut(links: list[Link], huts: list[str], start: str) -> tuple[str, int] | None:
    """Return the hut that hears the reading last, and the second it hears it.

    Args:
        links: Every radio link, as (sender, receiver, seconds).
        huts: Every hut that must hear the reading.
        start: The hut that starts the relay.

    Returns:
        (hut, seconds) for the last hut to hear it, ties broken by name A to
        Z. None when even one hut in `huts` never hears it at all.
    """
    heard = relay_seconds(links, start)
    if any(hut not in heard for hut in huts):
        return None
    latest, name = min((-heard[hut], hut) for hut in huts)
    return name, -latest


def relay_table(links: list[Link], start: str) -> list[str]:
    """Return one printable row per hut that hears the reading.

    Args:
        links: Every radio link, as (sender, receiver, seconds).
        start: The hut that starts the relay.

    Returns:
        Rows sorted by seconds, ties broken by hut name A to Z.
    """
    heard = relay_seconds(links, start)
    ordered = sorted((seconds, hut) for hut, seconds in heard.items())
    return [f"{seconds:4d}s  {hut}" for seconds, hut in ordered]


# ---- Self-check ----
if __name__ == "__main__":
    print("Reading released at Ash Col")
    for row in relay_table(LINKS, "Ash Col"):
        print(row)
    print(f"last to hear: {slowest_hut(LINKS, HUTS, 'Ash Col')}")

    print()
    print("Reading released at Bell Tarn")
    for row in relay_table(LINKS, "Bell Tarn"):
        print(row)
    print(f"last to hear: {slowest_hut(LINKS, HUTS, 'Bell Tarn')}")

    from_ash = relay_seconds(LINKS, "Ash Col")
    assert from_ash["Ash Col"] == 0
    assert from_ash["Cairn Gap"] == 7          # 4 + 3 beats the direct 9
    assert from_ash["Dun Force"] == 12         # 7 + 5 ties 4 + 8; both are 12
    assert from_ash["Elder Scree"] == 16
    assert from_ash["Fell Hause"] == 16
    assert slowest_hut(LINKS, HUTS, "Ash Col") == ("Elder Scree", 16)

    from_bell = relay_seconds(LINKS, "Bell Tarn")
    assert "Ash Col" not in from_bell          # no link points back up the ridge
    assert slowest_hut(LINKS, HUTS, "Bell Tarn") is None
    assert slowest_hut(LINKS, ["Bell Tarn", "Cairn Gap"], "Bell Tarn") == ("Cairn Gap", 3)
    print("All checks passed.")
