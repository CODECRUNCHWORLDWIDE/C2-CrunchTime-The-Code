# Challenge 1 — The Reefer Transfer Budget

> Topic: shortest path under a hop constraint · Lecture: [1](../lecture-notes/01-dijkstra-and-the-shortest-path-picker.md) · Difficulty: Medium-Hard · Target time: 75 minutes including the FRAME write-up · Why this one: it is the cleanest problem in the course for defending an algorithm *choice*, which is the senior signal on weighted graphs.

## The Brief

A refrigerated container — a reefer — moves between depots on booked legs, and
each leg has a price. Every time the container is lifted off one truck and onto
another it warms slightly, so the shipper caps how many **transfer depots** the
run may pass through. A run with no transfer depot goes straight from start to
end.

The interesting part is that the cheapest run overall is usually **over budget**,
and the cheapest run inside budget is usually **not on the cheapest route at
all**. Raising the budget by one transfer can drop the price by hundreds; raising
it again can change nothing. A shipper wants to see that trade, not just the
final number.

This is the deep-dive partner to [Exercise 2](../exercises/exercise-02-sluice-gate-settling.md).
The work here is to implement **both** standard approaches and defend the trade
between them.

## Starter

The worked answer on this page carries the booked legs as given data and the
self-checks you must satisfy — read those first, then look away and implement.

The depot network is fixed:

```text
Aveley    -> Brayton      80        Aveley  -> Elvington   100
Brayton   -> Corbridge    80        Elvington -> Dunmore   200
Corbridge -> Dunmore      80        Aveley  -> Fenwick     150
Aveley    -> Dunmore     500        Fenwick -> Dunmore     150
                                    Fenwick -> Garvock      90
```

Aveley to Dunmore is the row that carries the lesson: £500 direct, £300 through
one transfer, £240 through two.

## Requirements

1. `cheapest_run(legs, start, end, transfer_budget)` returns `(price, route)`
   for the cheapest run inside the budget, or `None` when no such run exists.
   `route` lists every depot including both ends.
2. Ties are settled in this order: **lowest price, then fewest transfers, then
   the route that sorts first alphabetically.** State the tie-break in your memo;
   an unstated tie-break is a bug waiting for a second correct answer.
3. `budget_table(...)` prints one row per budget, so the trade is visible rather
   than asserted.
4. `transfer_budget` below zero raises `ValueError`. A negative budget is not a
   run with no transfers; it is a caller mistake.
5. Implement it **twice** — the layered relaxation and the heap-with-state — and
   defend the choice in your Examine (cost) section. Implementing one and naming
   the other is not the exercise.

### The two algorithms

**A — layered relaxation.** Walk outward one leg at a time, `transfer_budget + 1`
times. Each pass builds a *new* layer from the previous one, so a run can never
chain several legs inside a single pass and quietly exceed the budget. Building
the next layer from a frozen previous layer is what makes this correct; doing it
in place is the bug below. Deterministically `O(B · E)`.

**B — heap with state.** Dijkstra where the heap holds `(price, node, legs_used)`
rather than `(price, node)`. Often faster when the destination is reachable in
few legs, because it can stop as soon as the destination is popped. The state
augmentation is the whole trick.

## Constraints

- **A run of `k` legs passes through `k - 1` transfer depots.** The search
  therefore never looks at runs longer than `transfer_budget + 1` legs. Confusing
  transfers with legs is the most common misreading of this problem — say the
  bound out loud in your memo.
- **Prices are positive**, so no negative-cycle handling is needed and a heap is
  legitimate. Say why that matters; with negative legs, approach B is simply
  wrong.
- **The route is part of the answer**, not just the price. A solution that
  returns a number and reconstructs the route afterwards has to keep predecessor
  state that the tie-break can see.
- `start == end` is a legal run of price zero and no transfers.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python challenge-01-reefer-transfer-budget.py
Aveley -> Dunmore
  budget 0 transfers:  500 via Aveley -> Dunmore
  budget 1 transfers:  300 via Aveley -> Elvington -> Dunmore
  budget 2 transfers:  240 via Aveley -> Brayton -> Corbridge -> Dunmore
  budget 3 transfers:  240 via Aveley -> Brayton -> Corbridge -> Dunmore

Aveley -> Garvock
  budget 0 transfers: no run
  budget 1 transfers:  240 via Aveley -> Fenwick -> Garvock
  budget 2 transfers:  240 via Aveley -> Fenwick -> Garvock
All checks passed.
```

Read the Aveley → Dunmore block downward. Each extra transfer buys a cheaper run
until it does not: budget 2 and budget 3 give the same £240, because there is no
four-leg run worth taking. That plateau is the shape a shipper actually wants to
see, and it is why `budget_table` prints rather than returns.

Aveley → Garvock shows the other half: at budget 0 there is **no run at all**,
and `None` is the honest answer rather than a very large number.

## Steps

1. Read the self-checks at the foot of the solution file. They are the spec.
2. Write the memo before any code: name the constraint, name both algorithms,
   name the tie-break.
3. Implement A. Build each layer from the previous one — a fresh dict per pass —
   and watch the Aveley → Dunmore row at budget 1 give £300 rather than £240.
4. Implement B in a second function. Key the visited set on `(depot, legs_used)`,
   not on `depot`.
5. Check both agree on every row of the table, then time them on a wider budget
   and write down which won and why.
6. Write the FRAME pass. Examine (cost) is where the marks are here.

## The Solution

```python
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
```

The layered form is the one shipped. The snapshot that approach A needs is not a
`dist[:]` copy here — it is structural: `nxt` is a brand-new dict built only from
`layer`, so there is no live state to chain through. Writing it that way makes
the bug impossible rather than merely avoided, which is worth a sentence in your
write-up.

## Run it

Download the solution beside this page and run it:

```bash
python challenge-01-reefer-transfer-budget.py
```

No third-party packages, no arguments, no input. It prints both budget tables and
then `All checks passed.`

Or open it in the browser IDE from the Run button on the block above, and add a
leg to see which budgets change.

## Common bugs to catch

- **Relaxing in place.** Symptom: Aveley → Dunmore at budget 1 returns £240, the
  three-leg answer, because one pass chained `Aveley → Brayton → Corbridge →
  Dunmore` through values updated inside that same pass. Build the next layer
  from a frozen previous one.
- **Marking a depot visited instead of `(depot, legs_used)`.** Symptom: approach
  B returns a run that is cheapest overall but over budget. Vanilla Dijkstra
  settles a node once, at its overall-cheapest distance; that invariant is simply
  false once a budget exists.
- **Counting transfers as legs.** Symptom: every answer is one transfer out. A
  direct run has one leg and zero transfers.
- **Returning a large sentinel instead of `None`.** Symptom: Aveley → Garvock at
  budget 0 reports an enormous price that later arithmetic happily adds to.
- **An unstated tie-break.** Symptom: two runs at the same price, and the answer
  changes when the legs are reordered in the input. The contract fixes the order;
  implement it.

## Acceptance checklist

- [ ] Both algorithms implemented, both agreeing on every row of both tables.
- [ ] The memo names the constraint, both algorithms, and the tie-break.
- [ ] `transfer_budget = -1` raises `ValueError`.
- [ ] `start == end` returns price 0.
- [ ] Aveley → Garvock at budget 0 returns `None`.
- [ ] Examine (cost) compares `O(B · E)` against the heap form and says which you
      would ship, and on what evidence.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Add a leg that makes a **four**-transfer run worthwhile, and show the plateau
  moving. If you cannot make one matter, say why the network resists it.
- Make one leg free (`0`) and check both algorithms still agree. Zero-weight
  edges are legal here and are a common source of heap bugs.
- Return the **two** cheapest runs inside the budget rather than one. The change
  to approach B is small and the change to approach A is not — that asymmetry is
  worth a paragraph.
