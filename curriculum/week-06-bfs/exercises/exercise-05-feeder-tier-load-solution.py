"""exercise-05-feeder-tier-load-solution.py — load on a distribution feeder, tier by tier.

A substation feeds transformers; those transformers feed more transformers.
The planners want one row per tier: how much current that whole tier draws,
and which single transformer on it draws the most. That is a level-by-level
walk with a sum and a maximum taken while the level is still in one piece.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import deque
from typing import NamedTuple

# ---- Given data ----
# Who feeds whom. GRANGE appears twice on purpose: the as-built has it
# spurred off two different transformers.
FEEDER: dict[str, list[str]] = {
    "SUBSTATION": ["ASHLEY", "BRINDLE", "COLTON"],
    "ASHLEY": ["DEEPING", "ELVASTON"],
    "BRINDLE": ["FRAMPTON", "GRANGE"],
    "COLTON": ["GRANGE", "HALLOW"],
    "DEEPING": [],
    "ELVASTON": ["IRTON"],
    "FRAMPTON": [],
    "GRANGE": ["JUNIPER"],
    "HALLOW": [],
    "IRTON": [],
    "JUNIPER": [],
}

# Amps drawn at each transformer. IRTON is not listed: it was commissioned
# last week and nobody has metered it yet.
LOADS: dict[str, int] = {
    "SUBSTATION": 0,
    "ASHLEY": 120,
    "BRINDLE": 95,
    "COLTON": 140,
    "DEEPING": 60,
    "ELVASTON": 75,
    "FRAMPTON": 210,
    "GRANGE": 45,
    "HALLOW": 210,
    "JUNIPER": 30,
}


class Tier(NamedTuple):
    """One row of the tier report."""

    depth: int
    total: int
    heaviest: str


# ---- Your task ----
def tier_report(
    feeder: dict[str, list[str]], loads: dict[str, int], head: str
) -> list[Tier]:
    """Return one row per tier of the feeder, working outward from `head`.

    Args:
        feeder: Each transformer mapped to the transformers it feeds.
        loads: Each transformer mapped to the amps it draws. A transformer
            with no entry counts as 0 amps, because an unmetered site is not
            a site drawing an unknown amount — it is a site with no reading.
        head: The substation the report starts from, at tier 0.

    Returns:
        A list of `Tier` rows, tier 0 first. `total` is the tier's combined
        amps; `heaviest` is the single largest draw on that tier, with the
        earlier name A to Z winning a tie.

    Raises:
        ValueError: If `head` is not a key in `feeder`.
    """
    if head not in feeder:
        raise ValueError(f"{head!r} is not on this feeder")

    queue = deque([head])
    seen = {head}
    report: list[Tier] = []
    depth = 0
    while queue:
        names: list[str] = []
        for _ in range(len(queue)):  # this tier only — the queue grows below
            name = queue.popleft()
            names.append(name)
            for fed in feeder.get(name, ()):
                if fed not in seen:
                    seen.add(fed)
                    queue.append(fed)
        report.append(
            Tier(
                depth=depth,
                total=sum(loads.get(name, 0) for name in names),
                heaviest=min(names, key=lambda name: (-loads.get(name, 0), name)),
            )
        )
        depth += 1
    return report


# ---- Self-check ----
if __name__ == "__main__":
    report = tier_report(FEEDER, LOADS, "SUBSTATION")
    for row in report:
        print(f"tier {row.depth}: {row.total:>4} A   heaviest {row.heaviest}")

    assert [row.depth for row in report] == [0, 1, 2, 3]
    assert [row.total for row in report] == [0, 355, 600, 30]
    assert [row.heaviest for row in report] == [
        "SUBSTATION",
        "COLTON",
        "FRAMPTON",
        "JUNIPER",
    ]

    # FRAMPTON and HALLOW both draw 210 A on tier 2. The earlier name wins.
    assert LOADS["FRAMPTON"] == LOADS["HALLOW"] == 210
    assert report[2].heaviest == "FRAMPTON"

    # GRANGE is spurred off two transformers but belongs to one tier: the
    # first one that reaches it. Counting it twice would inflate tier 2.
    assert 60 + 75 + 210 + 45 + 210 == report[2].total  # GRANGE counted once

    # IRTON has no meter reading, so it adds nothing and never wins a tier.
    assert "IRTON" not in LOADS
    assert report[3].total == 30 and report[3].heaviest == "JUNIPER"

    # A leaf is a one-tier report all by itself.
    assert tier_report(FEEDER, LOADS, "DEEPING") == [Tier(0, 60, "DEEPING")]

    for feeder, head in ((FEEDER, "MARSTON"), ({}, "SUBSTATION")):
        try:
            tier_report(feeder, LOADS, head)
        except ValueError as error:
            assert "is not on this feeder" in str(error)
        else:
            raise AssertionError("expected ValueError")

    print("All checks passed.")
