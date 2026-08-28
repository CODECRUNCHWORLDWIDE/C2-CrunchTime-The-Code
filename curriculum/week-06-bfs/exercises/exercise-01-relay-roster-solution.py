"""exercise-01-relay-roster-solution.py — who hears the flood warning, and when.

A mesh of radio relays. The base station transmits once; every relay that
hears it repeats the message; every relay that hears a repeat repeats it
again. This walks the mesh outward one hop at a time and reports the roster
of call-signs at each hop, plus the relays nobody ever reaches.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import deque

# ---- Given data ----
# Who each relay can be heard BY. Terrain makes this one-way in places:
# NOVA can hear BASE, but BASE sits in a dip and cannot hear NOVA.
LINKS: dict[str, list[str]] = {
    "BASE": ["KILO", "MIKE"],
    "KILO": ["NOVA", "OSCAR"],
    "MIKE": ["OSCAR", "PAPA"],
    "NOVA": ["BASE"],
    "OSCAR": ["QUEBEC"],
    "PAPA": [],
    "QUEBEC": [],
    "ROMEO": ["SIERRA"],
    "SIERRA": ["ROMEO"],
}


# ---- Your task ----
def every_sign(links: dict[str, list[str]]) -> set[str]:
    """Return every call-sign the mesh mentions, as a transmitter or a listener.

    Args:
        links: The mesh. Each key is a relay; its value is the relays that
            can hear it.

    Returns:
        A set holding every call-sign that appears anywhere in the mesh.
    """
    signs = set(links)
    for heard_by in links.values():
        signs.update(heard_by)
    return signs


def broadcast_roster(
    links: dict[str, list[str]], base: str
) -> tuple[list[list[str]], list[str]]:
    """Return the hop-by-hop roster of a broadcast, and the relays it misses.

    Args:
        links: The mesh. Each key is a relay; its value is the relays that
            can hear it.
        base: The call-sign that transmits first.

    Returns:
        A pair. The first item is a list of hops: hop 0 holds only `base`,
        hop 1 holds every relay that hears `base` directly, and so on. Each
        hop's call-signs are sorted A to Z. The second item is every
        call-sign the broadcast never reaches, also sorted A to Z.

    Raises:
        ValueError: If `base` is not a call-sign the mesh mentions. An empty
            mesh mentions nothing, so every base raises.
    """
    signs = every_sign(links)
    if base not in signs:
        raise ValueError(f"{base!r} is not on this mesh")

    queue = deque([base])
    reached = {base}
    hops: list[list[str]] = []
    while queue:
        this_hop: list[str] = []
        for _ in range(len(queue)):  # the snapshot: today's hop, not tomorrow's
            sign = queue.popleft()
            this_hop.append(sign)
            for listener in links.get(sign, ()):
                if listener not in reached:
                    reached.add(listener)
                    queue.append(listener)
        hops.append(sorted(this_hop))

    return hops, sorted(signs - reached)


# ---- Self-check ----
if __name__ == "__main__":
    hops, stranded = broadcast_roster(LINKS, "BASE")
    for number, roster in enumerate(hops):
        print(f"hop {number}: {', '.join(roster)}")
    print(f"stranded: {', '.join(stranded)}")

    assert hops == [
        ["BASE"],
        ["KILO", "MIKE"],
        ["NOVA", "OSCAR", "PAPA"],
        ["QUEBEC"],
    ]
    assert stranded == ["ROMEO", "SIERRA"]

    # A relay that hears nobody is still a hop of its own, alone.
    lonely, lonely_stranded = broadcast_roster(LINKS, "PAPA")
    assert lonely == [["PAPA"]]
    assert len(lonely_stranded) == 8

    # Starting inside the stranded island reaches only the island.
    island, island_stranded = broadcast_roster(LINKS, "ROMEO")
    assert island == [["ROMEO"], ["SIERRA"]]
    assert island_stranded == ["BASE", "KILO", "MIKE", "NOVA", "OSCAR", "PAPA", "QUEBEC"]

    # An empty mesh mentions nobody, so every base is off-mesh.
    for mesh, sign in (({}, "BASE"), (LINKS, "TANGO")):
        try:
            broadcast_roster(mesh, sign)
        except ValueError as error:
            assert "is not on this mesh" in str(error)
        else:
            raise AssertionError("expected ValueError")

    print("All checks passed.")
