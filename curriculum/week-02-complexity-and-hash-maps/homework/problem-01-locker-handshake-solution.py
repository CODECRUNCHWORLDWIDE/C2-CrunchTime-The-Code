"""problem-01-locker-handshake-solution.py — the first broken handshake.

Two maps that have to agree with each other: route code to locker, and locker
to route code. A set cannot answer this problem at all, because the question is
never "have I seen this route" — it is "have I seen this route paired with a
*different* locker", and that needs the payload.

Time: O(n) — one pass, two lookups and two writes per entry, each O(1) average.
Space: O(n) — at most one entry per distinct route and one per distinct locker.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""


def first_handshake_break(
    assignments: list[tuple[str, int]],
) -> tuple[int, str] | None:
    """Return the first entry that breaks the one-to-one correspondence.

    Args:
        assignments: (route_code, locker_id) pairs in the order the parcels
            were processed.

    Returns:
        (index, side) for the first offending entry, where side is 'route'
        when the route was already logged against a different locker and
        'locker' when the locker was already logged against a different
        route. 'route' wins when both are true. None when the whole shift
        is consistent.
    """
    locker_of: dict[str, int] = {}
    route_of: dict[int, str] = {}

    for index, (route, locker) in enumerate(assignments):
        if route in locker_of and locker_of[route] != locker:
            return (index, "route")
        if locker in route_of and route_of[locker] != route:
            return (index, "locker")
        locker_of[route] = locker
        route_of[locker] = route

    return None


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[tuple[str, int]], tuple[int, str] | None]] = [
        ([("QRT", 14), ("BLM", 9), ("QRT", 14)], None),
        ([("QRT", 14), ("QRT", 21)], (1, "route")),
        ([("QRT", 14), ("BLM", 14)], (1, "locker")),
        ([("QRT", 14), ("BLM", 21), ("QRT", 21)], (2, "route")),
        ([("QRT", 14), ("BLM", 9), ("ZED", 9), ("QRT", 30)], (2, "locker")),
        ([("QRT", 14), ("BLM", 9), ("QRT", 14), ("BLM", 9)], None),
        ([("QRT", 14)], None),
        ([], None),
    ]

    for log, expected in cases:
        found = first_handshake_break(log)
        assert found == expected, (log, found, expected)
        verdict = "consistent" if found is None else f"{found[1]} break at {found[0]}"
        pairs = " ".join(f"{route}->{locker}" for route, locker in log) or "(no parcels)"
        print(f"{verdict:<20}  {pairs}")

    print("All checks passed.")
