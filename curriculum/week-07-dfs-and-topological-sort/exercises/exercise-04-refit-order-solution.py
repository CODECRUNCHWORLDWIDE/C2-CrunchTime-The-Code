"""exercise-04-refit-order-solution.py — a legal running order for a dry-dock refit.

Kahn's algorithm. Count how many jobs each job is waiting on, start with the
jobs waiting on nothing, and every time a job finishes, take one off the count
of the jobs it was holding up. The ready pile is a heap because the tie rule is
"alphabetically smallest ready job", so the answer is one specific order rather
than any legal one.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

import heapq

# ---- Given data ----
REFIT_JOBS: list[str] = [
    "anode-swap",
    "bilge-clean",
    "blast",
    "dock-in",
    "float-out",
    "hull-survey",
    "paint",
    "prop-shaft",
    "sea-trial",
    "weld",
]

# The maintenance system emits ("dock-in", "hull-survey") from two different
# forms, so the same dependency arrives twice. Counting it twice would leave
# hull-survey waiting forever.
REFIT_RULES: list[tuple[str, str]] = [
    ("dock-in", "hull-survey"),
    ("hull-survey", "blast"),
    ("blast", "weld"),
    ("weld", "paint"),
    ("paint", "float-out"),
    ("float-out", "sea-trial"),
    ("dock-in", "bilge-clean"),
    ("bilge-clean", "paint"),
    ("hull-survey", "prop-shaft"),
    ("prop-shaft", "float-out"),
    ("prop-shaft", "anode-swap"),
    ("dock-in", "hull-survey"),
]

VALVE_JOBS: list[str] = ["fit-valve", "handover", "pressure-test", "sign-off"]

VALVE_RULES: list[tuple[str, str]] = [
    ("fit-valve", "pressure-test"),
    ("pressure-test", "sign-off"),
    ("sign-off", "fit-valve"),
    ("sign-off", "handover"),
]


# ---- Your task ----
def plan_refit(
    jobs: list[str], must_follow: list[tuple[str, str]]
) -> tuple[list[str], list[str]]:
    """Return a legal running order for the refit, and the jobs that never ran.

    Args:
        jobs: Every job in the refit. Names are unique.
        must_follow: Pairs (a, b) meaning job a must finish before job b
            starts. The same pair may arrive more than once; it still counts
            once.

    Returns:
        A pair (order, blocked). `order` takes the alphabetically smallest
        ready job at every step. `blocked` is the sorted list of jobs that
        never became ready — the jobs inside a loop, plus everything
        downstream of one.

    Raises:
        ValueError: If a pair names a job that is not in `jobs`.
    """
    known = set(jobs)
    holds_up: dict[str, set[str]] = {job: set() for job in jobs}
    waiting_on: dict[str, int] = {job: 0 for job in jobs}

    for before, after in must_follow:
        for name in (before, after):
            if name not in known:
                raise ValueError(f"must_follow names a job that is not in jobs: {name!r}")
        if after in holds_up[before]:
            continue  # the same dependency, said twice
        holds_up[before].add(after)
        waiting_on[after] += 1

    ready = [job for job in jobs if waiting_on[job] == 0]
    heapq.heapify(ready)
    order: list[str] = []
    while ready:
        job = heapq.heappop(ready)
        order.append(job)
        for held in sorted(holds_up[job]):
            waiting_on[held] -= 1
            if waiting_on[held] == 0:
                heapq.heappush(ready, held)

    blocked = sorted(known - set(order))
    return order, blocked


# ---- Self-check ----
if __name__ == "__main__":
    refit_order, refit_blocked = plan_refit(REFIT_JOBS, REFIT_RULES)
    print(f"refit order   : {refit_order}")
    print(f"refit blocked : {refit_blocked}")

    valve_order, valve_blocked = plan_refit(VALVE_JOBS, VALVE_RULES)
    print(f"valve order   : {valve_order}")
    print(f"valve blocked : {valve_blocked}")

    print(f"nothing to do : {plan_refit([], [])}")
    print(f"no rules      : {plan_refit(['zinc-check', 'scrub'], [])}")
    try:
        plan_refit(REFIT_JOBS, [("dock-in", "grind")])
    except ValueError as refusal:
        print(f"unknown job   : {refusal}")

    assert refit_order == [
        "dock-in",
        "bilge-clean",
        "hull-survey",
        "blast",
        "prop-shaft",
        "anode-swap",
        "weld",
        "paint",
        "float-out",
        "sea-trial",
    ]
    assert refit_blocked == []
    assert valve_order == []
    assert valve_blocked == ["fit-valve", "handover", "pressure-test", "sign-off"]
    assert plan_refit([], []) == ([], [])
    assert plan_refit(["zinc-check", "scrub"], []) == (["scrub", "zinc-check"], [])
    assert plan_refit(["weld"], [("weld", "weld")]) == ([], ["weld"])
    try:
        plan_refit(REFIT_JOBS, [("dock-in", "grind")])
    except ValueError as refusal:
        assert "'grind'" in str(refusal)
    else:
        raise AssertionError("an unknown job should have been refused")
    print("All checks passed.")
