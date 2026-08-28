"""problem-05-hive-inspection-log-solution.py — what the beekeepers found.

Every hive visit is logged as (hive, finding). Four questions come out of
that log at the end of the month, and each one is a different shape of dict.

The one to watch is the ranking. `Counter.most_common` breaks ties by
whichever finding was written down first, and the apiary's report wants ties
broken alphabetically. Those are not the same order, and this log proves it.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from collections import Counter, defaultdict

INSPECTIONS: list[tuple[str, str]] = [
    ("hive-02", "varroa"),
    ("hive-01", "queen seen"),
    ("hive-01", "brood healthy"),
    ("hive-03", "varroa"),
    ("hive-02", "queen seen"),
    ("hive-03", "low stores"),
    ("hive-01", "varroa"),
    ("hive-04", "queen seen"),
    ("hive-02", "low stores"),
]


def findings_by_hive(log: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group the log by hive, keeping the order things were noticed.

    Args:
        log: (hive, finding) pairs in visit order.

    Returns:
        A plain dict from hive to its findings, hives in first-seen order.
    """
    grouped: defaultdict[str, list[str]] = defaultdict(list)
    for hive, finding in log:
        grouped[hive].append(finding)
    return dict(grouped)


def finding_tally(log: list[tuple[str, str]]) -> Counter[str]:
    """Count how often each finding was written down.

    Args:
        log: (hive, finding) pairs in visit order.

    Returns:
        A Counter from finding to how many visits noted it.
    """
    return Counter(finding for _hive, finding in log)


def top_findings(log: list[tuple[str, str]], wanted: int) -> list[tuple[str, int]]:
    """Rank the findings, most common first, ties broken alphabetically.

    Args:
        log: (hive, finding) pairs in visit order.
        wanted: How many rows the report has room for.

    Returns:
        Up to `wanted` (finding, count) pairs. Not `most_common(wanted)` —
        that breaks ties by insertion order, which is not the rule here.
    """
    tally = finding_tally(log)
    ordered = sorted(tally.items(), key=lambda pair: (-pair[1], pair[0]))
    return ordered[:wanted]


def hives_with(log: list[tuple[str, str]], finding: str) -> list[str]:
    """Return every hive where one particular thing was found.

    Args:
        log: (hive, finding) pairs in visit order.
        finding: The finding to look for, matched exactly.

    Returns:
        The matching hive names, each once, sorted A to Z.
    """
    return sorted({hive for hive, noted in log if noted == finding})


# ---- Self-check ----
if __name__ == "__main__":
    grouped = findings_by_hive(INSPECTIONS)
    for hive in sorted(grouped):
        print(f"{hive}: {', '.join(grouped[hive])}")
    for finding, count in top_findings(INSPECTIONS, 3):
        print(f"  {count} x {finding}")
    print(f"varroa in: {', '.join(hives_with(INSPECTIONS, 'varroa'))}")

    tally = finding_tally(INSPECTIONS)
    assert tally["varroa"] == 3
    assert tally["queen seen"] == 3
    assert tally["kite"] == 0  # a Counter answers 0, it does not raise
    assert tally.most_common(2)[0][0] == "varroa"  # insertion order wins here
    assert top_findings(INSPECTIONS, 2)[0][0] == "queen seen"  # A to Z wins here
    assert top_findings(INSPECTIONS, 3) == [
        ("queen seen", 3),
        ("varroa", 3),
        ("low stores", 2),
    ]
    assert grouped["hive-01"] == ["queen seen", "brood healthy", "varroa"]
    assert list(grouped) == ["hive-02", "hive-01", "hive-03", "hive-04"]
    assert hives_with(INSPECTIONS, "varroa") == ["hive-01", "hive-02", "hive-03"]
    assert hives_with(INSPECTIONS, "wax moth") == []
    assert top_findings([], 3) == []
    assert len(INSPECTIONS) == 9  # the log is untouched
    print("All checks passed.")
