"""problem-02-bakery-order-slips-solution.py — tidy the counter's order slips.

Slips are written by hand on a pad: a quantity, an x, what was ordered, a
slash, and who it is for. The spacing is whatever the pen felt like.

`split()` with no argument is the whole trick: it collapses runs of spaces
and strips the ends. `split(" ")` does neither, and would leave you holding
a list full of empty strings.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

SLIPS: list[str] = [
    "2 x sourdough / kelly",
    "  1  x   rye    loaf / MO ",
    "3 x sourdough / Ade",
    "x sourdough / kelly",
    "two x baguette / Kelly",
    "5 x seeded roll / bo",
]


def fields(slip: str) -> tuple[int, str, str] | None:
    """Pull the three parts out of one slip.

    Args:
        slip: One raw line from the order pad.

    Returns:
        (quantity, item, customer), or None when the slip cannot be read.
        The item is lower-cased and single-spaced; the customer is
        title-cased.
    """
    if slip.count("/") != 1:
        return None
    left, right = slip.split("/")
    parts = left.split()
    if len(parts) < 3 or parts[1] != "x":
        return None
    if not parts[0].isdigit():
        return None
    customer = " ".join(right.split()).title()
    if not customer:
        return None
    return int(parts[0]), " ".join(parts[2:]).lower(), customer


def tidy(slip: str) -> str:
    """Render one slip the way the kitchen board wants it.

    Args:
        slip: One raw line from the order pad.

    Returns:
        "Customer: 2 x item", or "unreadable: <the slip, trimmed>".
    """
    parsed = fields(slip)
    if parsed is None:
        return f"unreadable: {slip.strip()}"
    quantity, item, customer = parsed
    return f"{customer}: {quantity} x {item}"


def basket(slips: list[str]) -> dict[str, int]:
    """Add up how much of each item was ordered.

    Args:
        slips: The whole pad, unreadable slips and all.

    Returns:
        A dict from item to total quantity, items in first-ordered order.
    """
    totals: dict[str, int] = {}
    for slip in slips:
        parsed = fields(slip)
        if parsed is None:
            continue
        quantity, item, _customer = parsed
        totals[item] = totals.get(item, 0) + quantity
    return totals


# ---- Self-check ----
if __name__ == "__main__":
    for slip in SLIPS:
        print(tidy(slip))
    loaves = basket(SLIPS)
    print("basket: " + ", ".join(f"{item} {count}" for item, count in loaves.items()))

    assert fields("  1  x   rye    loaf / MO ") == (1, "rye loaf", "Mo")
    assert fields("x sourdough / kelly") is None
    assert fields("two x baguette / Kelly") is None
    assert fields("2 x sourdough") is None
    assert tidy("2 x sourdough / kelly") == "Kelly: 2 x sourdough"
    assert loaves == {"sourdough": 5, "rye loaf": 1, "seeded roll": 5}
    assert list(loaves) == ["sourdough", "rye loaf", "seeded roll"]
    assert basket([]) == {}
    assert SLIPS[1] == "  1  x   rye    loaf / MO "  # the pad is untouched
    print("All checks passed.")
