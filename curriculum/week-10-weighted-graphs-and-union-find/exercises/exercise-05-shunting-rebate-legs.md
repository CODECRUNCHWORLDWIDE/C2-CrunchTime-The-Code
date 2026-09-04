# Exercise 5 — The Shunting Rebate Legs

> **Topic:** why the settled set stops being safe the moment a cost can be negative
> **Lecture:** [02 — Bellman-Ford, Floyd-Warshall and the MST](../lecture-notes/02-bellman-ford-floyd-warshall-and-mst.md)
> **Difficulty:** Medium
> **Target time:** 45 minutes
> **Why this one:** [Exercise 2](./exercise-02-sluice-gate-settling.md) showed the settled set being necessary. This one shows it being *wrong*, on data where it produces a plausible answer that is too high — and then shows what happens when the graph pays you to go round in circles.

## The Brief

A freight yard moves a wagon between sidings. Most legs cost shunting minutes. A
few are downhill runs the yard books as a **rebate**: they give minutes back, so
their cost is a negative number.

Negative costs break the rule the settled set is built on. This page shows it
happening rather than describing it.

Four functions: the true cheapest net minutes by repeated relaxing, the sidings
poisoned by a loop that never stops paying, the settled-set version for
comparison, and a printer that puts the two side by side.

## Starter

The worked answer on this page carries the legs and the self-checks.

```text
Ash Sidings -> Bar Road      3        Coal Drop -> Dock Spur     6
Ash Sidings -> Coal Drop     4        Bar Road  -> Engine Shed   8
Coal Drop   -> Bar Road     -2        Dock Spur -> Engine Shed   2
Bar Road    -> Dock Spur     5
```

The rebate is `Coal Drop -> Bar Road` at **-2**. That single negative leg is what
the whole page turns on.

There is also a second leg list with one more rebate — `Dock Spur -> Bar Road` at
-6 — which turns `Bar Road -> Dock Spur -> Bar Road` into a loop paying out one
minute every time round. That loop has no cheapest answer at all, and saying so
is a real result.

## Requirements

1. `best_net_minutes(legs, start)` returns the true cheapest net minutes to each
   siding, by relaxing every leg repeatedly — or `None` when a paying loop exists.
2. `refund_loop_sidings(legs, start)` returns the sidings whose answer is poisoned
   by such a loop.
3. `dijkstra_net_minutes(legs, start)` is the settled-set version, kept **only**
   for comparison.
4. `comparison_rows(legs, start)` prints both and marks where they differ.
5. On the shipped legs the two disagree on exactly two sidings.

## Constraints

- **Relax every leg, `sidings - 1` times.** That bound is not arbitrary: a
  cheapest route visits each siding at most once, so it uses at most
  `sidings - 1` legs, and one full sweep is guaranteed to extend every route by
  at least one leg.
- **One more sweep detects the loop.** If anything still improves after
  `sidings - 1` sweeps, no cheapest answer exists — because the only way to keep
  improving is to go round something that pays.
- **A paying loop poisons more than itself.** Every siding reachable *from* the
  loop has no cheapest answer either, and `refund_loop_sidings` has to report all
  of them rather than just the loop.
- **`None` means no answer exists**, which is different from unreachable. Say
  which is which in the docstring.
- **The Dijkstra version stays in the file** and is never used for a real answer.
  It is the exhibit.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-05-shunting-rebate-legs.py
siding       sweeps  Dijkstra
Ash Sidings       0         0
Bar Road          2         2
Coal Drop         4         4
Dock Spur         7         8   <- Dijkstra is high
Engine Shed       9        10   <- Dijkstra is high

with the Dock Spur -> Bar Road rebate leg added
  best_net_minutes    -> None
  refund_loop_sidings -> ['Bar Road', 'Dock Spur', 'Engine Shed']
All checks passed.
```

**Dock Spur is 7 by sweeping and 8 by Dijkstra. Engine Shed is 9 against 10.**

Here is why. Dijkstra settles Bar Road at 3 — the direct leg from Ash Sidings —
because 3 is the smallest thing on the frontier at that moment. But the real
cheapest route to Bar Road goes via Coal Drop: 4, then the -2 rebate, for a net
**2**. By the time that route is discovered, Bar Road is settled and never
reconsidered, and every siding downstream of it inherits the extra minute.

Note what the failure looks like: not a crash, not an obviously silly number.
Two rows, each one minute high, in a table that otherwise agrees. That is the
shape of this bug in real code.

The second block is the paying loop: `best_net_minutes` returns **`None`**, and
three sidings are named as poisoned — `Bar Road` and `Dock Spur`, which are the
loop, and `Engine Shed`, which is merely downstream of it.

## Steps

1. Read the self-checks. They are the spec.
2. Work out both routes to Bar Road by hand: 3 direct, 2 via Coal Drop.
3. Write the memo: relax everything repeatedly; the settled set is unsafe here
   and why.
4. Write `best_net_minutes` with the `sidings - 1` sweeps.
5. Add the extra sweep and the `None`. Test it on the looping legs.
6. Write `refund_loop_sidings`, and check it reports Engine Shed too — the
   poison spreads downstream.
7. Run the comparison and find the two disagreeing rows yourself before reading
   them above.
8. Write the FRAME pass. The Bar Road trace belongs in it.

## The Solution

```python
"""exercise-05-shunting-rebate-legs-solution.py — when a leg gives minutes back.

A freight yard moves a wagon between sidings. Most legs cost shunting
minutes. A few are downhill runs the yard books as a rebate: they give
minutes back, so their cost is a negative number.

Negative costs break the rule Dijkstra is built on, and this file shows it
happening rather than describing it. Four functions:

  best_net_minutes     — the true cheapest net minutes, by repeated relaxing
  refund_loop_sidings  — the sidings poisoned by a loop that never stops paying
  dijkstra_net_minutes — the settled-set Dijkstra, for comparison only
  comparison_rows      — the two answers side by side

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

import heapq
from collections import deque

# ---- Given data ----
# (from siding, to siding, net shunting minutes; a rebate leg is negative)
Leg = tuple[str, str, int]

LEGS: list[Leg] = [
    ("Ash Sidings", "Bar Road", 3),
    ("Ash Sidings", "Coal Drop", 4),
    ("Coal Drop", "Bar Road", -2),
    ("Bar Road", "Dock Spur", 5),
    ("Coal Drop", "Dock Spur", 6),
    ("Bar Road", "Engine Shed", 8),
    ("Dock Spur", "Engine Shed", 2),
]

# One extra leg turns Bar Road -> Dock Spur -> Bar Road into a loop that pays
# out one minute every time round.
LOOPING_LEGS: list[Leg] = LEGS + [("Dock Spur", "Bar Road", -6)]


# ---- Your task ----
def all_sidings(legs: list[Leg]) -> list[str]:
    """Return every siding named in the legs, in name order.

    Args:
        legs: Every leg, as (from, to, net minutes).

    Returns:
        A sorted list of siding names, with no repeats.
    """
    named: set[str] = set()
    for source, target, _ in legs:
        named.add(source)
        named.add(target)
    return sorted(named)


def best_net_minutes(legs: list[Leg], start: str) -> dict[str, int] | None:
    """Return the cheapest net minutes from start to every reachable siding.

    The whole leg list is swept over and over. One sweep is enough to settle
    any route one leg long, two sweeps settle any route two legs long, and a
    route that never repeats a siding cannot be longer than one leg fewer
    than there are sidings. So that many sweeps is always enough.

    Args:
        legs: Every leg, as (from, to, net minutes).
        start: The siding the wagon begins at.

    Returns:
        A dict of siding -> net minutes. A siding that cannot be reached is
        left out. None when a refund loop is reachable, because then no
        cheapest answer exists at all.
    """
    sidings = all_sidings(legs)
    cost: dict[str, int] = {start: 0}

    for _ in range(max(len(sidings) - 1, 0)):
        changed = False
        for source, target, minutes in legs:
            if source in cost and cost[source] + minutes < cost.get(target, float("inf")):
                cost[target] = cost[source] + minutes
                changed = True
        if not changed:
            break

    for source, target, minutes in legs:      # one sweep too many, on purpose
        if source in cost and cost[source] + minutes < cost.get(target, float("inf")):
            return None
    return cost


def refund_loop_sidings(legs: list[Leg], start: str) -> list[str]:
    """Return every siding whose cost a refund loop drags down without limit.

    Args:
        legs: Every leg, as (from, to, net minutes).
        start: The siding the wagon begins at.

    Returns:
        A sorted list of siding names. Empty when there is no refund loop
        reachable from start.
    """
    sidings = all_sidings(legs)
    cost: dict[str, float] = {start: 0}

    for _ in range(max(len(sidings) - 1, 0)):
        for source, target, minutes in legs:
            if source in cost and cost[source] + minutes < cost.get(target, float("inf")):
                cost[target] = cost[source] + minutes

    onward: dict[str, list[str]] = {siding: [] for siding in sidings}
    poisoned: set[str] = set()
    for source, target, minutes in legs:
        onward[source].append(target)
        if source in cost and cost[source] + minutes < cost.get(target, float("inf")):
            poisoned.add(target)

    queue = deque(poisoned)
    while queue:                              # anything downstream is poisoned too
        siding = queue.popleft()
        for target in onward[siding]:
            if target not in poisoned:
                poisoned.add(target)
                queue.append(target)
    return sorted(poisoned)


# ---- Given: the settled-set Dijkstra from Exercise 2, unchanged ----
def dijkstra_net_minutes(legs: list[Leg], start: str) -> dict[str, int]:
    """Dijkstra, which is correct only while every leg costs nothing to skip.

    Do not fix it. It is here so the two answers can be printed side by side.

    Args:
        legs: Every leg, as (from, to, net minutes).
        start: The siding the wagon begins at.

    Returns:
        A dict of siding -> net minutes. Where a rebate leg improves a
        siding after that siding was settled, the siding's own number is
        quietly corrected but its outgoing legs are never swept again, so
        everything downstream of it stays too high.
    """
    onward: dict[str, list[tuple[str, int]]] = {s: [] for s in all_sidings(legs)}
    for source, target, minutes in legs:
        onward[source].append((target, minutes))

    cost: dict[str, int] = {start: 0}
    settled: set[str] = set()
    queue: list[tuple[int, str]] = [(0, start)]
    while queue:
        so_far, siding = heapq.heappop(queue)
        if siding in settled:
            continue
        settled.add(siding)
        for target, minutes in onward[siding]:
            total = so_far + minutes
            if total < cost.get(target, float("inf")):
                cost[target] = total
                heapq.heappush(queue, (total, target))
    return cost


def comparison_rows(legs: list[Leg], start: str) -> list[str]:
    """Return one printable row per siding, sweeping beside Dijkstra.

    Args:
        legs: Every leg, as (from, to, net minutes).
        start: The siding the wagon begins at.

    Returns:
        Rows in siding-name order. A row where the two disagree is marked.
    """
    truth = best_net_minutes(legs, start)
    if truth is None:
        return ["no cheapest answer exists: a refund loop is reachable"]
    guess = dijkstra_net_minutes(legs, start)
    rows = []
    for siding in all_sidings(legs):
        if siding not in truth:
            continue
        flag = "" if guess[siding] == truth[siding] else "   <- Dijkstra is high"
        rows.append(f"{siding:<13}{truth[siding]:6d}{guess[siding]:10d}{flag}")
    return rows


# ---- Self-check ----
if __name__ == "__main__":
    print("siding       sweeps  Dijkstra")
    for row in comparison_rows(LEGS, "Ash Sidings"):
        print(row)

    print()
    print("with the Dock Spur -> Bar Road rebate leg added")
    print(f"  best_net_minutes    -> {best_net_minutes(LOOPING_LEGS, 'Ash Sidings')}")
    print(f"  refund_loop_sidings -> {refund_loop_sidings(LOOPING_LEGS, 'Ash Sidings')}")

    truth = best_net_minutes(LEGS, "Ash Sidings")
    assert truth == {
        "Ash Sidings": 0,
        "Coal Drop": 4,
        "Bar Road": 2,
        "Dock Spur": 7,
        "Engine Shed": 9,
    }
    guess = dijkstra_net_minutes(LEGS, "Ash Sidings")
    assert guess["Bar Road"] == 2               # the number was fixed after settling
    assert guess["Dock Spur"] == 8              # but nothing downstream was told
    assert guess["Engine Shed"] == 10
    assert sum(1 for siding in truth if truth[siding] != guess[siding]) == 2

    assert refund_loop_sidings(LEGS, "Ash Sidings") == []
    assert best_net_minutes(LOOPING_LEGS, "Ash Sidings") is None
    assert refund_loop_sidings(LOOPING_LEGS, "Ash Sidings") == [
        "Bar Road",
        "Dock Spur",
        "Engine Shed",
    ]
    assert best_net_minutes(LEGS, "Engine Shed") == {"Engine Shed": 0}
    print("All checks passed.")
```

`dijkstra_net_minutes` is shipped knowing it is wrong on this data, and the file
asserts that it is wrong — the two rows are checked, not just printed. An
exhibit nothing asserts stops being an exhibit the first time somebody tidies it.

## Run it

Download the solution beside this page and run it:

```bash
python exercise-05-shunting-rebate-legs.py
```

No third-party packages, no arguments, no input. It prints the two tables with
the differences marked, the paying-loop results, and then `All checks passed.`

## Common bugs to catch

- **Reaching for Dijkstra because the graph looks small.** Symptom: two rows one
  minute high, and a table that looks fine.
- **Sweeping `sidings` times instead of `sidings - 1`.** Symptom: correct answers
  and one wasted sweep — and no way to detect the loop, because the detection
  sweep is now indistinguishable from a working one.
- **Detecting the loop but reporting only its own sidings.** Symptom: Engine Shed
  gets a confident number that cannot be honoured.
- **Returning a large negative number instead of `None`.** Symptom: an answer to
  a question that has none.
- **Confusing "no cheapest answer" with "unreachable".** Symptom: a siding with
  no route treated as poisoned, or the reverse.
- **Stopping early when a sweep changes nothing.** That optimisation is correct
  and worth having — but it must not skip the detection sweep, and getting that
  ordering wrong is easy.

## Acceptance checklist

- [ ] Bar Road is 2 by sweeping; Dijkstra settles it at 3.
- [ ] Dock Spur is 7 against 8; Engine Shed is 9 against 10.
- [ ] Every other siding agrees between the two.
- [ ] With the extra rebate leg, `best_net_minutes` returns `None`.
- [ ] `refund_loop_sidings` reports Bar Road, Dock Spur **and** Engine Shed.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Report the poisoning loop itself — the actual sequence of legs — rather than
  the sidings it affects. It needs a parent map and a walk back, and it is what a
  yard manager would ask for first.
- Remove the -2 rebate and re-run the comparison. The two tables now agree
  everywhere; say precisely what property of the data that restored.
- Bound the loop: allow at most three trips round and find the cheapest answer
  under that bound. It is a different and answerable question, and noticing that
  it *is* answerable is the useful part.
