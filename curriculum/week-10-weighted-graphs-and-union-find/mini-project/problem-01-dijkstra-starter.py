"""problem-01-dijkstra-starter.py - the water-taxi timings, to fill in.

A harbour board wants to know how long the water taxi takes from the ferry slip
to every other quay, and which quay is worst served.

Grow outwards from the start, always finishing the nearest unfinished quay next.
Once a quay is finished its time is final - that is the invariant a heap buys
you, and it holds only because no run takes negative minutes.

Fill in the three function bodies. Do not change the signatures or the harness:
the harness is the spec.

Run it and it will tell you which cases still fail. When they all pass it prints
"All checks passed."
"""

import heapq

Run = tuple[str, str, int]      # (quay, quay, minutes for the water taxi)

QUAYS: list[str] = [
    "Ferry Slip",
    "Bait Wharf",
    "Chandlery Steps",
    "Dry Dock",
    "Gull Rock",
]

RUNS: list[Run] = [
    ("Ferry Slip", "Bait Wharf", 4),
    ("Bait Wharf", "Chandlery Steps", 3),
    ("Ferry Slip", "Chandlery Steps", 9),
    ("Chandlery Steps", "Dry Dock", 2),
]
# Gull Rock is in QUAYS and in no run: the taxi does not go there.


def build_water(runs: list[Run]) -> dict[str, list[tuple[str, int]]]:
    """Turn the run list into an adjacency map.

    Runs are two-way: the taxi takes the same time in either direction.

    Args:
        runs: Every scheduled run, as (quay, quay, minutes).

    Returns:
        quay -> list of (neighbouring quay, minutes).
    """
    # TODO: both directions, and a quay with no runs must still be safe to look
    # up - reach for a default rather than a KeyError.
    raise NotImplementedError


def run_minutes(runs: list[Run], start: str) -> dict[str, int]:
    """Shortest taxi time from `start` to every quay it can reach.

    Args:
        runs: Every scheduled run.
        start: The quay the taxi waits at.

    Returns:
        quay -> minutes, containing ONLY the quays that can be reached. A quay
        the taxi cannot reach is absent, not infinite - the caller decides what
        unreachable means, and a sentinel number invites arithmetic on it.
    """
    # TODO: heap of (minutes, quay). Pop the smallest, skip it if already
    # settled, otherwise settle it and push its neighbours.
    raise NotImplementedError


def longest_wait(runs: list[Run], quays: list[str], start: str) -> tuple[str, int]:
    """The reachable quay that takes longest to get to.

    Args:
        runs: Every scheduled run.
        quays: Every quay the harbour has.
        start: The quay the taxi waits at.

    Returns:
        (quay, minutes). Ties are settled alphabetically so the report is
        stable. `start` itself counts, at 0 minutes, when nothing else is
        reachable.
    """
    # TODO: read run_minutes and take the maximum, breaking ties by name.
    raise NotImplementedError


# ---- Harness. This is the spec - do not edit. ----
if __name__ == "__main__":
    failed = 0

    def check(label: str, got, want) -> None:
        global failed
        ok = got == want
        failed += not ok
        print(f"    {'ok ' if ok else 'FAIL'} {label:<34} got {got!r}")
        if not ok:
            print(f"         want {want!r}")

    water = build_water(RUNS)
    check("Ferry Slip neighbours", sorted(water["Ferry Slip"]),
          [("Bait Wharf", 4), ("Chandlery Steps", 9)])
    check("Gull Rock neighbours", list(water.get("Gull Rock", [])), [])

    times = run_minutes(RUNS, "Ferry Slip")
    check("start is zero", times["Ferry Slip"], 0)
    check("direct run", times["Bait Wharf"], 4)
    # 4 + 3 = 7 beats the single 9-minute run: the two-leg route wins.
    check("two legs beat one", times["Chandlery Steps"], 7)
    check("three legs", times["Dry Dock"], 9)
    check("unreachable is absent", "Gull Rock" in times, False)

    check("worst served", longest_wait(RUNS, QUAYS, "Ferry Slip"), ("Dry Dock", 9))
    check("nothing reachable", longest_wait([], QUAYS, "Ferry Slip"), ("Ferry Slip", 0))

    print()
    print("All checks passed." if failed == 0 else f"{failed} check(s) still failing.")
