"""exercise-04-on-call-grid-solution.py — the first conflict in an on-call rota.

Three rules, three axes, three sets per axis. One row-major pass over the
8 x 14 grid. For every staffed cell we ask the three questions in precedence
order — ward, then night, then unit — and the first yes is the answer.

Time: O(1) — the grid is fixed at 112 cells. For a general R x C grid the same
code is O(R * C), linear in the number of cells.
Space: O(1) — 8 + 14 + 8 sets, each holding at most 40 sets of initials.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from collections import defaultdict

WARDS = 8
NIGHTS = 14


def first_rota_conflict(rota: list[list[str | None]]) -> tuple[int, int, str] | None:
    """Return the first rule-breaking cell in row-major order.

    Args:
        rota: An 8 x 14 grid. Each cell holds a doctor's initials, or None
            when that ward is unstaffed that night.

    Returns:
        (row, col, axis) for the first conflicting cell, where axis is
        'ward', 'night' or 'unit' and ward outranks night outranks unit.
        None when the whole rota is legal.
    """
    ward_seen: list[set[str]] = [set() for _ in range(len(rota))]
    night_seen: list[set[str]] = [set() for _ in range(len(rota[0]) if rota else 0)]
    unit_seen: defaultdict[tuple[int, int], set[str]] = defaultdict(set)

    for row, nights in enumerate(rota):
        for col, who in enumerate(nights):
            if who is None:
                continue
            unit = (row // 2, col // 7)
            if who in ward_seen[row]:
                return (row, col, "ward")
            if who in night_seen[col]:
                return (row, col, "night")
            if who in unit_seen[unit]:
                return (row, col, "unit")
            ward_seen[row].add(who)
            night_seen[col].add(who)
            unit_seen[unit].add(who)
    return None


def blank() -> list[list[str | None]]:
    """Return an empty 8 x 14 rota: every ward unstaffed every night."""
    return [[None] * NIGHTS for _ in range(WARDS)]


# ---- Self-check ----
if __name__ == "__main__":
    def build(cells: list[tuple[int, int, str]]) -> list[list[str | None]]:
        """Return a blank rota with the listed cells filled in."""
        rota = blank()
        for row, col, who in cells:
            rota[row][col] = who
        return rota

    cases: list[tuple[str, list[tuple[int, int, str]], tuple[int, int, str] | None]] = [
        ("empty rota", [], None),
        ("ward", [(0, 3, "AKB"), (0, 9, "AKB")], (0, 9, "ward")),
        ("night", [(2, 5, "MDR"), (6, 5, "MDR")], (6, 5, "night")),
        ("unit", [(4, 1, "JLO"), (5, 6, "JLO")], (5, 6, "unit")),
        ("precedence", [(2, 4, "PVS"), (3, 4, "PVS")], (3, 4, "night")),
        (
            "row-major",
            [(1, 0, "AKB"), (1, 1, "AKB"), (0, 2, "MDR"), (0, 3, "MDR")],
            (0, 3, "ward"),
        ),
        ("legal repeat", [(0, 0, "AKB"), (1, 7, "AKB")], None),
    ]

    for label, cells, expected in cases:
        found = first_rota_conflict(build(cells))
        assert found == expected, (label, found, expected)
        print(f"{label:<13} ->  {found}")

    print("All checks passed.")
