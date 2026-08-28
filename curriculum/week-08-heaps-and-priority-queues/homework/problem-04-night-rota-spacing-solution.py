"""problem-04-night-rota-spacing-solution.py — a night rota nobody works twice running.

A night shelter needs one volunteer per night. Each volunteer has agreed to a
number of nights, and the house rule is that nobody works two nights in a row.
Build a rota that uses everybody's agreed nights, or say plainly that no rota
exists.

The greedy rule is "whoever has the most nights left goes tonight", which is a
max-heap, plus one held-back slot for last night's volunteer so they cannot be
picked again immediately.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
# Volunteer to the number of nights they agreed to work.
NIGHTS_AGREED: dict[str, int] = {
    "Ama": 4,
    "Beto": 3,
    "Cass": 2,
    "Dev": 1,
}


# ---- Your task ----
def build_rota(nights_agreed: dict[str, int]) -> list[str] | None:
    """Return a rota with nobody on two nights running, or None if impossible.

    Args:
        nights_agreed: Volunteer to nights agreed. A volunteer agreeing to zero
            nights is ignored.

    Returns:
        One name per night, in order. None when no arrangement can avoid a
        volunteer working back to back — which happens exactly when one person
        has agreed to more than half the nights, rounded up.
    """
    available: list[tuple[int, str]] = [
        (-nights, name) for name, nights in nights_agreed.items() if nights > 0
    ]
    heapq.heapify(available)
    rota: list[str] = []
    resting: tuple[int, str] | None = None

    while available or resting:
        if not available:
            return None
        stored, name = heapq.heappop(available)
        rota.append(name)
        if resting is not None:
            heapq.heappush(available, resting)
            resting = None
        left = -stored - 1
        resting = (-left, name) if left > 0 else None
    return rota


def rota_is_legal(rota: list[str]) -> bool:
    """Return True when no name appears on two nights in a row.

    Args:
        rota: One name per night.

    Returns:
        True for a legal rota, including an empty one.
    """
    return all(tonight != tomorrow for tonight, tomorrow in zip(rota, rota[1:]))


def nights_worked(rota: list[str]) -> dict[str, int]:
    """Return how many nights each volunteer ends up working.

    Args:
        rota: One name per night.

    Returns:
        A dict of volunteer to night count, in first-appearance order.
    """
    worked: dict[str, int] = {}
    for name in rota:
        worked[name] = worked.get(name, 0) + 1
    return worked


# ---- Self-check ----
if __name__ == "__main__":
    rota = build_rota(NIGHTS_AGREED)
    print(f"nights to fill: {sum(NIGHTS_AGREED.values())}")
    print(f"rota: {rota}")
    print(f"legal: {rota_is_legal(rota)}")
    print(f"nights worked: {nights_worked(rota)}")

    crowded = {"Ama": 5, "Beto": 1}
    print(f"one person on five of six nights: {build_rota(crowded)}")

    tight = {"Ama": 3, "Beto": 2}
    print(f"three and two: {build_rota(tight)}")
    print(f"a single night: {build_rota({'Dev': 1})}")
    print(f"one person, two nights: {build_rota({'Dev': 2})}")
    print(f"nobody: {build_rota({})}")
    print(f"a zero pledge: {build_rota({'Ama': 0})}")

    assert rota is not None
    assert len(rota) == sum(NIGHTS_AGREED.values())
    assert rota_is_legal(rota)
    assert nights_worked(rota) == {"Ama": 4, "Beto": 3, "Cass": 2, "Dev": 1}
    assert rota[0] == "Ama"
    assert build_rota(crowded) is None
    assert build_rota(tight) == ["Ama", "Beto", "Ama", "Beto", "Ama"]
    assert build_rota({"Dev": 1}) == ["Dev"]
    assert build_rota({"Dev": 2}) is None
    assert build_rota({}) == []
    assert build_rota({"Ama": 0}) == []
    assert rota_is_legal([])
    print("All checks passed.")
