"""challenge-01-reefer-transfer-budget-solution.py — cheapest run inside a transfer budget.

A refrigerated container moves between depots on booked legs. Each leg has a
price. Every time the container is lifted off one truck and onto another it
warms slightly, so the shipper caps how many *transfer depots* the run may
pass through. A run with no transfer depot goes straight from start to end.

The cheapest run overall is often over budget, and the cheapest run inside
budget is often not on the cheapest route at all. That is the whole problem.

  cheapest_run  — (price, route) inside the budget, or None
  budget_table  — one row per budget, so the trade is visible

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
# (from depot, to depot, price of that leg in pounds)
Leg = tuple[str, str, int]

LEGS: list[Leg] = [
    ("Aveley", "Brayton", 80),
    ("Brayton", "Corbridge", 80),
    ("Corbridge", "Dunmore", 80),
    ("Aveley", "Dunmore", 500),
    ("Aveley", "Elvington", 100),
    ("Elvington", "Dunmore", 200),
    ("Aveley", "Fenwick", 150),
    ("Fenwick", "Dunmore", 150),
    ("Fenwick", "Garvock", 90),
]


# ---- Your task ----
def cheapest_run(
    legs: list[Leg], start: str, end: str, transfer_budget: int
) -> tuple[int, list[str]] | None:
    """Return the cheapest run from start to end inside the transfer budget.

    A run that uses `k` legs passes through `k - 1` transfer depots, so the
    search never needs to look at runs longer than `transfer_budget + 1`
    legs.

    Args:
        legs: Every booked leg, as (from, to, price).
        start: The depot the container is loaded at.
        end: The depot it has to reach.
        transfer_budget: How many transfer depots the run may pass through.

    Returns:
        (price, route) where route lists every depot including both ends.
        Ties are settled in this order: lowest price, then fewest transfers,
        then the route that comes first alphabetically. None when no run
        inside the budget exists.

    Raises:
        ValueError: If transfer_budget is negative.
    """
    if transfer_budget < 0:
        raise ValueError("transfer_budget cannot be negative")

    # layer[depot] = (price so far, route so far), for runs of exactly `step` legs
    layer: dict[str, tuple[int, list[str]]] = {start: (0, [start])}
    best: tuple[int, int, list[str]] | None = None
    if start == end:
        best = (0, 0, [start])

    for step in range(1, transfer_budget + 2):
        nxt: dict[str, tuple[int, list[str]]] = {}
        for source, target, price in legs:
            if source not in layer:
                continue
            so_far, route = layer[source]
            candidate = (so_far + price, route + [target])
            if target not in nxt or candidate < nxt[target]:
                nxt[target] = candidate
        layer = nxt
        if not layer:
            break
        if end in layer:
            price, route = layer[end]
            candidate = (price, step, route)
            if best is None or candidate < best:
                best = candidate

    if best is None:
        return None
    return best[0], best[2]


def budget_table(legs: list[Leg], start: str, end: str, budgets: range) -> list[str]:
    """Return one printable row per transfer budget.

    Args:
        legs: Every booked leg, as (from, to, price).
        start: The depot the container is loaded at.
        end: The depot it has to reach.
        budgets: The budgets to report on, smallest first.

    Returns:
        Rows reading "budget N transfers: ...", one per budget.
    """
    rows = []
    for budget in budgets:
        run = cheapest_run(legs, start, end, budget)
        if run is None:
            rows.append(f"  budget {budget} transfers: no run")
        else:
            price, route = run
            rows.append(f"  budget {budget} transfers: {price:4d} via " + " -> ".join(route))
    return rows


# ---- Self-check ----
if __name__ == "__main__":
    print("Aveley -> Dunmore")
    for row in budget_table(LEGS, "Aveley", "Dunmore", range(0, 4)):
        print(row)

    print()
    print("Aveley -> Garvock")
    for row in budget_table(LEGS, "Aveley", "Garvock", range(0, 3)):
        print(row)

    assert cheapest_run(LEGS, "Aveley", "Dunmore", 0) == (500, ["Aveley", "Dunmore"])
    # Two runs cost 300 with one transfer; Elvington beats Fenwick on the name.
    assert cheapest_run(LEGS, "Aveley", "Dunmore", 1) == (
        300,
        ["Aveley", "Elvington", "Dunmore"],
    )
    assert cheapest_run(LEGS, "Aveley", "Dunmore", 2) == (
        240,
        ["Aveley", "Brayton", "Corbridge", "Dunmore"],
    )
    assert cheapest_run(LEGS, "Aveley", "Dunmore", 9) == cheapest_run(
        LEGS, "Aveley", "Dunmore", 2
    )

    assert cheapest_run(LEGS, "Aveley", "Garvock", 0) is None
    assert cheapest_run(LEGS, "Aveley", "Garvock", 1) == (
        240,
        ["Aveley", "Fenwick", "Garvock"],
    )
    assert cheapest_run(LEGS, "Aveley", "Aveley", 0) == (0, ["Aveley"])
    assert cheapest_run(LEGS, "Dunmore", "Aveley", 5) is None

    try:
        cheapest_run(LEGS, "Aveley", "Dunmore", -1)
    except ValueError as problem:
        assert str(problem) == "transfer_budget cannot be negative"
    else:                                    # pragma: no cover - the guard must fire
        raise AssertionError("a negative budget should have been refused")
    print("All checks passed.")
