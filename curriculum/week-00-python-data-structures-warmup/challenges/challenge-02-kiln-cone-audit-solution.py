"""challenge-02-kiln-cone-audit-solution.py — audit the pottery's kilns.

Every firing is logged as (kiln, cone, hours). The studio wants two things
out of that log: a league table of kiln hours, and the kilns that are doing
the same job as each other.

A dict adds the hours up. A frozenset is what lets one kiln's set of cones
become the key that finds its twins.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

FIRINGS: list[tuple[str, str, int]] = [
    ("bisque-1", "04", 9),
    ("glaze-a", "6", 11),
    ("bisque-2", "04", 8),
    ("glaze-b", "6", 12),
    ("bisque-1", "06", 7),
    ("glaze-a", "10", 6),
    ("test-kiln", "6", 4),
    ("bisque-2", "06", 9),
    ("glaze-b", "10", 5),
    ("test-kiln", "10", 3),
    ("bisque-1", "04", 5),
]


def hours_by_kiln(firings: list[tuple[str, str, int]]) -> dict[str, int]:
    """Add up the hours each kiln ran.

    Args:
        firings: (kiln, cone, hours) records in log order.

    Returns:
        A dict from kiln to total hours, kilns in first-seen order.
    """
    totals: dict[str, int] = {}
    for kiln, _cone, hours in firings:
        totals[kiln] = totals.get(kiln, 0) + hours
    return totals


def cones_by_kiln(firings: list[tuple[str, str, int]]) -> dict[str, frozenset[str]]:
    """Collect the distinct cone codes each kiln has fired.

    Args:
        firings: (kiln, cone, hours) records in log order.

    Returns:
        A dict from kiln to a frozenset of its cone codes. Frozen because
        these sets are used as dict keys in `twin_kilns`.
    """
    gathered: dict[str, set[str]] = {}
    for kiln, cone, _hours in firings:
        gathered.setdefault(kiln, set()).add(cone)
    return {kiln: frozenset(cones) for kiln, cones in gathered.items()}


def ranked(firings: list[tuple[str, str, int]]) -> list[tuple[str, int]]:
    """Rank the kilns by hours run, most first.

    Args:
        firings: (kiln, cone, hours) records in log order.

    Returns:
        (kiln, hours) pairs, most hours first, ties broken by kiln name
        A to Z as text.
    """
    totals = hours_by_kiln(firings)
    return sorted(totals.items(), key=lambda pair: (-pair[1], pair[0]))


def twin_kilns(firings: list[tuple[str, str, int]]) -> list[list[str]]:
    """Find the kilns whose cone sets match exactly.

    Args:
        firings: (kiln, cone, hours) records in log order.

    Returns:
        One list per group of two or more kilns sharing an identical cone
        set. Names inside a group are sorted A to Z; groups are ordered by
        size, largest first, ties broken by the group's first name.
    """
    groups: dict[frozenset[str], list[str]] = {}
    for kiln, cones in cones_by_kiln(firings).items():
        groups.setdefault(cones, []).append(kiln)

    found = [sorted(names) for names in groups.values() if len(names) > 1]
    return sorted(found, key=lambda names: (-len(names), names[0]))


def audit(firings: list[tuple[str, str, int]]) -> str:
    """Render the whole audit as text.

    Args:
        firings: (kiln, cone, hours) records in log order.

    Returns:
        The league table, then the matching cone sets. No trailing newline.
    """
    cones = cones_by_kiln(firings)
    rows = [
        f"{kiln:<10} {hours:3d}h  cones {', '.join(sorted(cones[kiln]))}"
        for kiln, hours in ranked(firings)
    ]
    rows.append("matching cone sets:")
    for group in twin_kilns(firings):
        rows.append(f"  {', '.join(group)}")
    return "\n".join(rows)


# ---- Self-check ----
if __name__ == "__main__":
    print(audit(FIRINGS))

    totals = hours_by_kiln(FIRINGS)
    assert totals == {
        "bisque-1": 21,
        "glaze-a": 17,
        "bisque-2": 17,
        "glaze-b": 17,
        "test-kiln": 7,
    }
    assert list(totals) == ["bisque-1", "glaze-a", "bisque-2", "glaze-b", "test-kiln"]
    assert ranked(FIRINGS)[:2] == [("bisque-1", 21), ("bisque-2", 17)]
    assert [kiln for kiln, _hours in ranked(FIRINGS)][-1] == "test-kiln"
    assert cones_by_kiln(FIRINGS)["bisque-1"] == frozenset({"04", "06"})
    assert twin_kilns(FIRINGS) == [
        ["glaze-a", "glaze-b", "test-kiln"],
        ["bisque-1", "bisque-2"],
    ]
    assert twin_kilns([]) == []
    assert ranked([]) == []
    assert FIRINGS[0] == ("bisque-1", "04", 9)  # the log is untouched
    print("All checks passed.")
