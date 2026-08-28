"""problem-01-dawn-chorus-shortlist-solution.py — the most-heard birds of the dawn watch.

A recorder logs one line per detection through a spring morning. The survey
wants the five most-heard species, most first, and alphabetical between species
that were heard the same number of times.

The two halves of that rule pull in opposite directions — count downwards, name
upwards — and a string cannot be negated. `heapq.nsmallest` with a tuple key is
the tool that handles both directions in one bounded pass.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

import heapq
from collections import Counter

# ---- Given data ----
DETECTIONS: list[str] = [
    "blackcap", "wren", "robin", "wren", "song thrush", "robin", "wren",
    "chiffchaff", "blackcap", "wren", "robin", "dunnock", "song thrush",
    "wren", "blackcap", "robin", "chiffchaff", "wren", "goldcrest", "robin",
    "song thrush", "wren", "blackcap", "dunnock", "robin", "wren", "nuthatch",
    "blackcap", "robin", "song thrush", "wren", "chiffchaff", "robin",
]

SHORTLIST_SIZE = 5


# ---- Your task ----
def shortlist(detections: list[str], size: int) -> list[tuple[str, int]]:
    """Return the most-heard species, most first.

    Args:
        detections: One species name per detection, in any order.
        size: How many species to list. 0 lists none.

    Returns:
        (species, count) pairs, highest count first, ties alphabetical. When
        fewer distinct species were heard than `size`, every species is
        returned.
    """
    if size <= 0:
        return []
    counts = Counter(detections)
    return heapq.nsmallest(size, counts.items(), key=lambda pair: (-pair[1], pair[0]))


def heard_once(detections: list[str]) -> list[str]:
    """Return the species heard exactly one time, alphabetically.

    Args:
        detections: One species name per detection.

    Returns:
        Species names, A to Z. Empty when every species was heard twice or more.
    """
    counts = Counter(detections)
    return sorted(name for name, count in counts.items() if count == 1)


def share_of_dawn(detections: list[str], species: str) -> float:
    """Return what fraction of the morning's detections one species accounts for.

    Args:
        detections: One species name per detection.
        species: The species to measure.

    Returns:
        A fraction between 0.0 and 1.0, rounded to three places. A species that
        was never heard gives 0.0, and so does an empty log.
    """
    if not detections:
        return 0.0
    return round(detections.count(species) / len(detections), 3)


# ---- Self-check ----
if __name__ == "__main__":
    top = shortlist(DETECTIONS, SHORTLIST_SIZE)
    print(f"detections logged: {len(DETECTIONS)}")
    print(f"distinct species : {len(set(DETECTIONS))}")
    print("shortlist:")
    for rank, (species, count) in enumerate(top, 1):
        print(f"  {rank}. {count:2d}  {species}")

    print(f"heard once: {heard_once(DETECTIONS)}")
    print(f"wren's share: {share_of_dawn(DETECTIONS, 'wren')}")
    print(f"raven's share: {share_of_dawn(DETECTIONS, 'raven')}")
    print(f"asking for more than exist: {len(shortlist(DETECTIONS, 99))}")
    print(f"asking for none: {shortlist(DETECTIONS, 0)}")
    print(f"an empty log: {shortlist([], 3)}")

    assert top[0] == ("wren", 9)
    assert top[1] == ("robin", 8)
    assert top[2] == ("blackcap", 5)
    assert top[3] == ("song thrush", 4)
    assert top[4] == ("chiffchaff", 3)
    assert heard_once(DETECTIONS) == ["goldcrest", "nuthatch"]
    assert share_of_dawn(DETECTIONS, "raven") == 0.0
    assert len(shortlist(DETECTIONS, 99)) == len(set(DETECTIONS))
    assert shortlist(DETECTIONS, 0) == []
    assert shortlist([], 3) == []
    print("All checks passed.")
