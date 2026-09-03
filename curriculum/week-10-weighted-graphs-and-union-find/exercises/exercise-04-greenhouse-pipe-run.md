# Exercise 4 — The Greenhouse Pipe Run

> **Topic:** the minimum spanning tree, with union-find deciding what to accept
> **Lecture:** [02 — Bellman-Ford, Floyd-Warshall and the MST](../lecture-notes/02-bellman-ford-floyd-warshall-and-mst.md)
> **Difficulty:** Medium
> **Target time:** 40 minutes
> **Why this one:** it is the page where [Exercise 3](./exercise-03-mooring-chain-groups.md) stops being a curiosity and becomes a component. The whole algorithm is "sort, then accept if it joins two things that are not joined yet" — and the second half of that sentence is a union-find query.

## The Brief

A walled garden is putting a hot-water pipe into every glasshouse. The surveyor
has priced each trench that could be dug, in metres of pipe. Any house fed by the
boiler **through any chain of trenches** is warm, so the job is to pick the
cheapest set of trenches that leaves nothing out.

Report the total metres and the trenches to dig, in the order you accept them.

## Starter

`exercise-04-greenhouse-pipe-run-solution.py` sits beside this page with the
prices and the self-checks.

```text
Cold Frame - Fig House      7m       Melon Pit  - Vine Range    12m
Cold Frame - Melon Pit      9m       Palm Court - Vine Range     6m
Fig House  - Melon Pit      4m       Palm Court - Wardian Case  14m
Fig House  - Palm Court    11m       Vine Range - Wardian Case   5m
Melon Pit  - Palm Court     6m
```

Six houses, nine priced trenches, and the answer digs five of them. Five, not
six — a network joining six things needs one fewer trench than it has houses, and
knowing that number before you start is what tells you when to stop.

There is also an **alpine house** outside the wall with no trench priced to it.
It is in the file to make the failure case real.

## Requirements

1. `Plots` is the union-find over the houses.
2. `cheapest_pipe_run(houses, trenches)` returns the total metres and the accepted
   trenches in order — or `None` when no set of trenches reaches every house.
3. `network_count(houses, trenches)` returns how many separate warm networks the
   trenches leave.
4. Accepting a trench between two houses already joined is skipped, not counted.
5. The alpine house makes `cheapest_pipe_run` return `None` and `network_count`
   return 2.

## Constraints

- **Cheapest first.** Sort the trenches by metres and walk them in order. That
  ordering is the greedy, and the greedy is correct here — the write-up should
  say why in one sentence rather than asserting it.
- **Accept only a trench joining two houses not already joined.** That check is
  exactly `find(a) != find(b)`, and it is why this exercise follows Exercise 3.
- **Stop after `houses - 1` trenches**, or when the trenches run out. Both endings
  matter: the first is success, the second may not be.
- **Unreachable is `None`, not a partial network.** A pipe run that warms five of
  six houses is not a cheaper answer; it is a different and wrong one.
- **`network_count` is independent of `cheapest_pipe_run`.** It answers the "why
  did it fail" question, and a version that just calls the other one cannot.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-04-greenhouse-pipe-run-solution.py
trenches to dig, in order
    4m  Fig House - Melon Pit   (running 4m)
    5m  Vine Range - Wardian Case   (running 9m)
    6m  Melon Pit - Palm Court   (running 15m)
    6m  Palm Court - Vine Range   (running 21m)
    7m  Cold Frame - Fig House   (running 28m)
total: 28m for 5 trenches across 6 houses

with the alpine house added and no trench priced to it
  cheapest_pipe_run -> None
  network_count     -> 2
All checks passed.
```

Read the dig order against the price list. The 4-metre and 5-metre trenches go in
first, then the two 6-metre ones, and then the **7-metre** Cold Frame to Fig
House — while the 9-metre Cold Frame to Melon Pit is skipped entirely. Not
because it is expensive, but because by the time it comes up, Cold Frame and
Melon Pit are already joined through Fig House.

That skip is the union-find query earning its place. **28 metres across five
trenches.**

Below it, the alpine house: `None` and two networks. The second number is what
tells the surveyor *why* — there is a house nothing reaches, not a pricing
problem.

## Steps

1. Read the self-checks. They are the spec.
2. Work out how many trenches the answer must have before doing anything else.
   Six houses, five trenches.
3. Write the memo: sort by price, accept when the two houses are in different
   networks, stop at five.
4. Reuse the union-find from Exercise 3. Do not rewrite it.
5. Walk the sorted list and record the running total as you accept.
6. Add the alpine house and get `None` out of it. Then write `network_count`
   separately.
7. Write the FRAME pass, with the skipped 9-metre trench as the worked example.

## The Solution

```python
"""exercise-04-greenhouse-pipe-run-solution.py — the cheapest pipe run that feeds every house.

A walled garden is putting a hot-water pipe into every glasshouse. The
surveyor has priced each trench that could be dug, in metres of pipe. Any
house fed by the boiler through any chain of trenches is warm, so the job is
to pick the cheapest set of trenches that leaves nothing out.

Two functions:

  cheapest_pipe_run — the total metres and the trenches to dig, in dig order
  network_count     — how many separate warm networks the trenches leave

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
# (one house, the other house, metres of pipe in that trench)
Trench = tuple[str, str, int]

HOUSES: list[str] = [
    "Cold Frame",
    "Fig House",
    "Melon Pit",
    "Palm Court",
    "Vine Range",
    "Wardian Case",
]

TRENCHES: list[Trench] = [
    ("Cold Frame", "Fig House", 7),
    ("Cold Frame", "Melon Pit", 9),
    ("Fig House", "Melon Pit", 4),
    ("Fig House", "Palm Court", 11),
    ("Melon Pit", "Palm Court", 6),
    ("Melon Pit", "Vine Range", 12),
    ("Palm Court", "Vine Range", 6),
    ("Palm Court", "Wardian Case", 14),
    ("Vine Range", "Wardian Case", 5),
]

# The alpine house sits outside the wall and nobody priced a trench to it.
STRANDED_HOUSES: list[str] = HOUSES + ["Alpine House"]


# ---- Your task ----
class Plots:
    """Houses grouped into warm networks, with path compression and rank."""

    def __init__(self, houses: list[str]) -> None:
        """Start every house in a network of its own.

        Args:
            houses: Every house that has to end up warm.
        """
        self.parent: dict[str, str] = {house: house for house in houses}
        self.rank: dict[str, int] = {house: 0 for house in houses}
        self.networks: int = len(houses)

    def network_of(self, house: str) -> str:
        """Return the name the house's network goes by, flattening on the way.

        Args:
            house: The house to look up.

        Returns:
            The root house. Two houses share a network exactly when this
            returns the same name for both.
        """
        root = house
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[house] != root:
            self.parent[house], house = root, self.parent[house]
        return root

    def join(self, left: str, right: str) -> bool:
        """Merge two networks, shallower tree under deeper.

        Args:
            left: One house.
            right: The other house.

        Returns:
            True when the two were in different networks and are now one.
            False when they were already warm together, so digging this
            trench would buy nothing.
        """
        left_root, right_root = self.network_of(left), self.network_of(right)
        if left_root == right_root:
            return False
        if self.rank[left_root] < self.rank[right_root]:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        if self.rank[left_root] == self.rank[right_root]:
            self.rank[left_root] += 1
        self.networks -= 1
        return True


def cheapest_pipe_run(
    houses: list[str], trenches: list[Trench]
) -> tuple[int, list[Trench]] | None:
    """Return the cheapest set of trenches that warms every house.

    Args:
        houses: Every house that has to end up warm.
        trenches: Every trench the surveyor priced.

    Returns:
        (total metres, trenches in the order they are accepted). Trenches of
        equal cost are considered in name order, so the answer is the same
        every run. None when no set of the priced trenches can warm them all.
    """
    plots = Plots(houses)
    chosen: list[Trench] = []
    total = 0
    for left, right, metres in sorted(trenches, key=lambda t: (t[2], t[0], t[1])):
        if plots.join(left, right):
            chosen.append((left, right, metres))
            total += metres
            if len(chosen) == len(houses) - 1:
                break
    if plots.networks != 1:
        return None
    return total, chosen


def network_count(houses: list[str], trenches: list[Trench]) -> int:
    """Return how many separate warm networks the priced trenches allow.

    Args:
        houses: Every house that has to end up warm.
        trenches: Every trench the surveyor priced.

    Returns:
        1 when everything can be joined up, more when the garden falls into
        separate pieces. This is the number cheapest_pipe_run checks before
        it agrees to return an answer.
    """
    plots = Plots(houses)
    for left, right, _ in trenches:
        plots.join(left, right)
    return plots.networks


# ---- Self-check ----
if __name__ == "__main__":
    run = cheapest_pipe_run(HOUSES, TRENCHES)
    assert run is not None
    total, chosen = run
    print("trenches to dig, in order")
    running = 0
    for left, right, metres in chosen:
        running += metres
        print(f"  {metres:3d}m  {left} - {right}   (running {running}m)")
    print(f"total: {total}m for {len(chosen)} trenches across {len(HOUSES)} houses")

    print()
    print("with the alpine house added and no trench priced to it")
    print(f"  cheapest_pipe_run -> {cheapest_pipe_run(STRANDED_HOUSES, TRENCHES)}")
    print(f"  network_count     -> {network_count(STRANDED_HOUSES, TRENCHES)}")

    assert total == 28
    assert chosen == [
        ("Fig House", "Melon Pit", 4),
        ("Vine Range", "Wardian Case", 5),
        ("Melon Pit", "Palm Court", 6),
        ("Palm Court", "Vine Range", 6),
        ("Cold Frame", "Fig House", 7),
    ]
    assert len(chosen) == len(HOUSES) - 1
    assert network_count(HOUSES, TRENCHES) == 1
    assert cheapest_pipe_run(STRANDED_HOUSES, TRENCHES) is None
    assert network_count(STRANDED_HOUSES, TRENCHES) == 2
    assert cheapest_pipe_run(["Fig House"], []) == (0, [])
    print("All checks passed.")
```

The running total is recorded as trenches are accepted rather than summed at the
end. It costs nothing and it makes the output a trace of the decision rather than
a report of the conclusion — which is what you want when the answer surprises
you.

## Download and run

Download the solution beside this page and run it:

```bash
python exercise-04-greenhouse-pipe-run-solution.py
```

No third-party packages, no arguments, no input. It prints the dig order with a
running total, the alpine-house failure, and then `All checks passed.`

## Common bugs to catch

- **Accepting a trench between two already-joined houses.** Symptom: six trenches
  for six houses, a ring in the network, and money spent on pipe that warms
  nothing new.
- **Sorting by house name.** Symptom: a valid network at the wrong price.
- **Stopping at `houses` trenches rather than `houses - 1`.** Symptom: one trench
  too many, or a loop that never ends when the trenches run out first.
- **Returning a partial network.** Symptom: an answer that warms five houses and
  reports a total, which reads as success.
- **`network_count` implemented by calling `cheapest_pipe_run`.** Symptom: it
  cannot explain a failure, which is the only thing it is for.
- **Rewriting union-find inline.** Symptom: a second copy that drifts from the
  first, and probably no path compression in it.

## Acceptance checklist

- [ ] Five trenches, 28 metres, across six houses.
- [ ] The 9-metre Cold Frame to Melon Pit trench is skipped.
- [ ] Trenches are accepted in ascending price order.
- [ ] With the alpine house, `cheapest_pipe_run` returns `None`.
- [ ] With the alpine house, `network_count` returns 2.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Report the **most expensive trench in the answer**. That is the one to
  re-survey, because it is the single price that most affects the total.
- Price one new trench to the alpine house and re-run. Work out beforehand what
  price would change the rest of the answer rather than just adding to it.
- Solve it the other way — start from one house and grow the network outwards,
  always taking the cheapest trench leaving it. It gets the same answer by a
  different route, and saying why both are correct is worth a paragraph.
