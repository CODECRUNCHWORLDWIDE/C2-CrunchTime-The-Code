# Week 10 — Homework

Six problems, all original, each with a runnable worked answer folded away under
it. Allow about five and a half hours. Do each with the lectures closed; open the
worked answer only after your own version runs, or after fifteen minutes stuck on
one step.

The six cover the week's whole range: union-find as a grouping tool and as a
diagnosis, a spanning tree, a search where the cost is a maximum rather than a
sum, all-pairs distances, and a search where the cost multiplies.

| # | Problem | Sub-shape | Est. time |
|---|---------|-----------|----------:|
| 1 | [The Claim Slip Merge](#problem-1--the-claim-slip-merge) | Union-find over a shared attribute | 50 min |
| 2 | [The Kerb Step Route](#problem-2--the-kerb-step-route) | Minimising the worst step, not the total | 60 min |
| 3 | [The Mast Trench Network](#problem-3--the-mast-trench-network) | Minimum spanning tree with a non-obvious cost | 55 min |
| 4 | [The Radiator Loop Check](#problem-4--the-radiator-loop-check) | Union-find as a diagnosis, naming both faults | 50 min |
| 5 | [The Market Stall Reach](#problem-5--the-market-stall-reach) | All pairs at once, rather than one search per start | 50 min |
| 6 | [The Relay Reliability](#problem-6--the-relay-reliability) | The same search where cost multiplies and bigger is better | 55 min |

Every worked answer runs on its own with no arguments and no packages, and ends
by printing `All checks passed.` To run one, open its reveal, copy the code into
a file of your own, and run that file:

```bash
python problem-01-claim-slip-merge.py
```

---

## Problem 1 — The Claim Slip Merge

**The brief.** A station lost-property office writes a claim slip every time
somebody rings about a missing bag. Each slip has a name and one or more phone
numbers. The same person rings back from a different phone, and now there are two
slips.

Two slips belong to the same person when they **share at least one phone number**,
and that spreads: slip A shares a number with slip B, slip B shares a different
number with slip C, so all three are one person.

**Constraints.** **The name is not the key.** Two different people can share a
name, and the shipped data has exactly that case in it. Merging on the name is
the wrong answer that passes a careless test.

**Answer.** Union-find over the **phone numbers**, not the slips. Keep a map from
each number to the first slip that mentioned it; for every later slip, union it
with that slip. Numbers do the joining because the numbers are what is shared.

Then group the slips by root and read the name off any member of the group — they
all agree, because they are one person by construction.

**Signatures.** `Slips` with the union-find, `merged_claims(slips)`,
`phone_owner(records, phone)`.

**Watch for.** Grouping by name — the shipped data punishes it. Building the
union over slips directly without the number-to-slip map, which misses the
transitive case. A number nobody claimed returns `None`, not an empty string.

<details>
<summary>Worked answer — <code>problem-01-claim-slip-merge-solution.py</code></summary>

```python
"""problem-01-claim-slip-merge-solution.py — merging lost-property slips by phone number.

A station lost-property office writes a claim slip every time someone rings
about a missing bag. Each slip has a name and one or more phone numbers. The
same person rings back from a different phone, and now there are two slips.

Two slips belong to the same person when they share at least one phone
number, and that spreads: slip A shares a number with slip B, slip B shares a
different number with slip C, so all three are one person. The name is not
the key — two different people can share a name, and this file's data has
exactly that.

  merged_claims — one record per person, phones sorted, records sorted

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
# [name, phone, phone, ...] as written on each slip
Slip = list[str]

SLIPS: list[Slip] = [
    ["Rosa Lindqvist", "0117 496 0021", "0117 496 0088"],
    ["Rosa Lindqvist", "0117 496 0088", "07700 900142"],
    ["Rosa Lindqvist", "0117 496 5555"],
    ["Deniz Aksoy", "07700 900333"],
    ["Deniz Aksoy", "07700 900333", "0117 496 0777"],
    ["Marek Solc", "0117 496 9000"],
]


# ---- Your task ----
class Slips:
    """Slip numbers grouped into people, with path compression and rank."""

    def __init__(self, slip_count: int) -> None:
        """Start every slip as a person of its own.

        Args:
            slip_count: How many slips the office wrote.
        """
        self.parent: list[int] = list(range(slip_count))
        self.rank: list[int] = [0] * slip_count

    def person_of(self, slip: int) -> int:
        """Return the slip number that names this slip's person.

        Args:
            slip: The slip to look up.

        Returns:
            The root slip number, flattening the path on the way back.
        """
        root = slip
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[slip] != root:
            self.parent[slip], slip = root, self.parent[slip]
        return root

    def join(self, left: int, right: int) -> bool:
        """Merge two slips into one person, shallower tree under deeper.

        Args:
            left: One slip number.
            right: The other slip number.

        Returns:
            True when two separate people turned out to be one. False when
            they were already merged.
        """
        left_root, right_root = self.person_of(left), self.person_of(right)
        if left_root == right_root:
            return False
        if self.rank[left_root] < self.rank[right_root]:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        if self.rank[left_root] == self.rank[right_root]:
            self.rank[left_root] += 1
        return True


def merged_claims(slips: list[Slip]) -> list[list[str]]:
    """Return one record per person, built from the slips that share a phone.

    Args:
        slips: Every slip, each [name, phone, phone, ...].

    Returns:
        A list of [name, phone, phone, ...] records. Phones inside a record
        are sorted and appear once. Records are sorted by name, then by the
        phone list, so two people with the same name still come out in a
        fixed order and a slip with no phone at all still sorts.
    """
    owners = Slips(len(slips))
    seen_on: dict[str, int] = {}
    for index, slip in enumerate(slips):
        for phone in slip[1:]:
            if phone in seen_on:
                owners.join(seen_on[phone], index)
            else:
                seen_on[phone] = index

    gathered: dict[int, set[str]] = {}
    for index, slip in enumerate(slips):
        gathered.setdefault(owners.person_of(index), set()).update(slip[1:])

    records = [[slips[root][0], *sorted(phones)] for root, phones in gathered.items()]
    return sorted(records, key=lambda record: (record[0], record[1:]))


def phone_owner(records: list[list[str]], phone: str) -> str | None:
    """Return the name on the record holding this phone number.

    Args:
        records: The output of merged_claims.
        phone: The number to look up.

    Returns:
        The name, or None when no record holds that number.
    """
    for record in records:
        if phone in record[1:]:
            return record[0]
    return None


# ---- Self-check ----
if __name__ == "__main__":
    records = merged_claims(SLIPS)
    print(f"{len(SLIPS)} slips merged into {len(records)} people")
    for record in records:
        print(f"  {record[0]}")
        for phone in record[1:]:
            print(f"      {phone}")

    print()
    print(f"who owns 07700 900142? {phone_owner(records, '07700 900142')}")
    print(f"who owns 0117 496 5555? {phone_owner(records, '0117 496 5555')}")
    print(f"who owns 0117 496 0001? {phone_owner(records, '0117 496 0001')}")

    assert records == [
        ["Deniz Aksoy", "0117 496 0777", "07700 900333"],
        ["Marek Solc", "0117 496 9000"],
        ["Rosa Lindqvist", "0117 496 0021", "0117 496 0088", "07700 900142"],
        ["Rosa Lindqvist", "0117 496 5555"],
    ]
    assert len(records) == 4                   # two of them are called Rosa Lindqvist
    assert phone_owner(records, "0117 496 0001") is None
    assert merged_claims([]) == []
    assert merged_claims([["Pat Ng"]]) == [["Pat Ng"]]
    print("All checks passed.")
```

</details>
---

## Problem 2 — The Kerb Step Route

**The brief.** A market square is paved in blocks, each surveyed to a height in
millimetres. A wheelchair crosses from the north-west corner to the south-east
corner, one block at a time, north, south, east or west. Stepping between two
blocks means climbing the difference in their heights.

**Nobody cares about the total climb.** What matters is the **single worst step**
on the route, because that is the one that stops the chair. Make it as small as
possible.

**Constraints.** The cost of a route is a **maximum**, not a sum. That one change
breaks every instinct built up on shortest-path problems, and it is the whole
reason this problem is here.

**Answer.** Two answers, and the write-up should name both.

The first is a **search where the accumulated cost is a maximum**: the frontier is
ordered by the worst step so far, and extending a route costs
`max(worst_so_far, this_step)` rather than `worst_so_far + this_step`. Everything
else about the search is unchanged, which is the point worth making.

The second is a **decision procedure plus a search over the answer**: ask "is
there a route where no step exceeds `limit`?" — which is a plain reachability
question — and binary-search `limit`. `route_within` is that decision procedure,
and having it in the file lets you check the first answer against the second.

On the shipped square the answer is **6**: no route at limit 5, a route at limit 6.

**Signatures.** `gentlest_route(square)`, `route_within(square, limit)`.

**Watch for.** Summing the steps, which answers a different and easier question.
Comparing heights rather than the difference between them. A one-block square is
zero, not an error.

<details>
<summary>Worked answer — <code>problem-02-kerb-step-route-solution.py</code></summary>

```python
"""problem-02-kerb-step-route-solution.py — the route whose worst kerb is smallest.

A market square is paved in blocks, each surveyed to a height in millimetres.
A wheelchair crosses from the north-west corner to the south-east corner,
moving one block at a time, north, south, east or west. Stepping between two
blocks means climbing the difference in their heights.

Nobody cares about the total climb. What matters is the single worst step on
the route, because that is the one that stops the chair. So the cost of a
route is the largest step on it, and the job is to make that as small as
possible.

  gentlest_route   — the smallest possible worst step
  route_within     — is there a route whose every step is at most this?

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

import heapq
from collections import deque

# ---- Given data ----
# Paving-block heights in millimetres, north row first, west column first
SQUARE: list[list[int]] = [
    [12, 14, 15, 62],
    [20, 15, 16, 64],
    [21, 40, 22, 66],
    [23, 42, 20, 21],
]

STEPS: tuple[tuple[int, int], ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))


# ---- Your task ----
def gentlest_route(square: list[list[int]]) -> int:
    """Return the smallest possible worst step from north-west to south-east.

    This is Dijkstra with one change. Normal Dijkstra adds the cost of a step
    to the cost so far. Here the cost of a route is the largest step on it,
    so instead of adding, the relaxation takes whichever is bigger: the worst
    step so far, or the step about to be taken.

    Args:
        square: Block heights, as rows of millimetres. Every row is the same
            length and there is at least one block.

    Returns:
        The largest step on the gentlest route, in millimetres. Zero when the
        square is a single block, because no step is ever taken.
    """
    rows, columns = len(square), len(square[0])
    worst: dict[tuple[int, int], int] = {(0, 0): 0}
    settled: set[tuple[int, int]] = set()
    queue: list[tuple[int, int, int]] = [(0, 0, 0)]

    while queue:
        so_far, row, column = heapq.heappop(queue)
        if (row, column) in settled:
            continue
        settled.add((row, column))
        if (row, column) == (rows - 1, columns - 1):
            return so_far
        for down, across in STEPS:
            next_row, next_column = row + down, column + across
            if not (0 <= next_row < rows and 0 <= next_column < columns):
                continue
            step = abs(square[next_row][next_column] - square[row][column])
            worst_here = max(so_far, step)     # the max, not the sum
            if worst_here < worst.get((next_row, next_column), float("inf")):
                worst[(next_row, next_column)] = worst_here
                heapq.heappush(queue, (worst_here, next_row, next_column))

    raise ValueError("the square is not fully connected, which cannot happen on a grid")


def route_within(square: list[list[int]], limit: int) -> bool:
    """Return whether a route exists where no single step exceeds the limit.

    This is the plain-BFS way to answer the same question, one limit at a
    time. It is the check a binary search over the limit would call.

    Args:
        square: Block heights, as rows of millimetres.
        limit: The largest step the chair will take, in millimetres.

    Returns:
        True when the south-east corner is reachable without ever stepping
        more than `limit`.
    """
    rows, columns = len(square), len(square[0])
    seen = {(0, 0)}
    queue = deque([(0, 0)])
    while queue:
        row, column = queue.popleft()
        if (row, column) == (rows - 1, columns - 1):
            return True
        for down, across in STEPS:
            next_row, next_column = row + down, column + across
            if not (0 <= next_row < rows and 0 <= next_column < columns):
                continue
            if (next_row, next_column) in seen:
                continue
            if abs(square[next_row][next_column] - square[row][column]) <= limit:
                seen.add((next_row, next_column))
                queue.append((next_row, next_column))
    return False


# ---- Self-check ----
if __name__ == "__main__":
    answer = gentlest_route(SQUARE)
    print("block heights in mm")
    for row in SQUARE:
        print("  " + " ".join(f"{height:3d}" for height in row))
    print(f"gentlest route: worst step {answer} mm")

    print()
    print("limit  route?")
    for limit in range(max(answer - 2, 0), answer + 3):
        print(f"{limit:5d}  {route_within(SQUARE, limit)}")

    assert answer == 6
    assert route_within(SQUARE, answer) is True
    assert route_within(SQUARE, answer - 1) is False
    assert gentlest_route([[7]]) == 0
    assert gentlest_route([[0, 100]]) == 100   # one row, one forced step
    assert gentlest_route([[5, 5], [5, 5]]) == 0
    print("All checks passed.")
```

</details>
---

## Problem 3 — The Mast Trench Network

**The brief.** Six weather masts stand on a moor. Every mast has to end up wired
to every other, directly or through its neighbours. A trenching machine digs
between two masts, and the price is set by the machine's boom: **it swings once,
so a trench costs whichever is larger — the east-west gap or the north-south
gap.** Not the two added together, and not the straight-line distance.

**Constraints.** Every pair could be trenched, so the surveyor is choosing five
trenches from fifteen candidates. The cost function is the trap: it is a maximum
of two differences, and every wrong answer here comes from using the sum instead.

**Answer.** Build all fifteen candidate trenches with the boom cost, sort them
cheapest first, and accept a trench only when its two masts are **not already
joined** — union-find answering that question in near-constant time. Stop after
five, which for six masts is one fewer than the mast count.

Total on this moor: **13 metres across five trenches**, and the longest single
trench — the one that sizes the boom you have to hire — is Beacon Ridge to Ewe
Crag at 4 metres.

The data includes one pair, Alder Hill to Drum Rig, where the boom cost is 6 and
the sum of the two gaps is 11. That row is in the output on purpose: it is the
evidence that the cost rule matters.

**Signatures.** `boom_cost(first, second)`, `cheapest_network(masts)`,
`longest_trench(chosen)`.

**Watch for.** Adding the two gaps. Accepting a trench between masts already
joined, which builds a ring and costs money for nothing. Forgetting that the
answer is `n - 1` trenches, not `n`.

<details>
<summary>Worked answer — <code>problem-03-mast-trench-network-solution.py</code></summary>

```python
"""problem-03-mast-trench-network-solution.py — trenching a weather-mast network.

Six weather masts stand on a moor. Every mast has to end up wired to every
other, directly or through its neighbours. A trenching machine digs between
two masts, and the price is set by the machine's boom: it swings once, so a
trench costs whichever is larger, the east-west gap or the north-south gap.
Not the two added together, and not the straight-line distance.

Every pair of masts could be trenched, so the surveyor is choosing from
fifteen possible trenches and needs the cheapest five that join them all up.

  cheapest_network — total cost and the trenches, in the order accepted
  longest_trench   — the single widest trench, which sets the boom to hire

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from itertools import combinations

# ---- Given data ----
# (mast name, metres east of the gate, metres north of the gate)
Mast = tuple[str, int, int]

MASTS: list[Mast] = [
    ("Alder Hill", 0, 0),
    ("Beacon Ridge", 3, 1),
    ("Cross Fell", 1, 4),
    ("Drum Rig", 6, 5),
    ("Ewe Crag", 7, 0),
    ("Fold Head", 2, 2),
]


# ---- Your task ----
class Moor:
    """Masts grouped into wired networks, with path compression and rank."""

    def __init__(self, mast_count: int) -> None:
        """Start every mast in a network of its own.

        Args:
            mast_count: How many masts stand on the moor.
        """
        self.parent: list[int] = list(range(mast_count))
        self.rank: list[int] = [0] * mast_count
        self.networks: int = mast_count

    def network_of(self, mast: int) -> int:
        """Return the mast that names this mast's network.

        Args:
            mast: The mast's position in the list.

        Returns:
            The root mast, flattening the path on the way back.
        """
        root = mast
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[mast] != root:
            self.parent[mast], mast = root, self.parent[mast]
        return root

    def join(self, left: int, right: int) -> bool:
        """Wire two networks together, shallower tree under deeper.

        Args:
            left: One mast's position in the list.
            right: The other mast's position in the list.

        Returns:
            True when the trench joined two networks that were apart. False
            when both masts were already on one network, so the trench would
            be wasted.
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


def boom_cost(first: Mast, second: Mast) -> int:
    """Return the price of trenching between two masts.

    Args:
        first: One mast, as (name, east, north).
        second: The other mast.

    Returns:
        The larger of the east-west gap and the north-south gap, in metres.
    """
    return max(abs(first[1] - second[1]), abs(first[2] - second[2]))


def cheapest_network(masts: list[Mast]) -> tuple[int, list[tuple[str, str, int]]]:
    """Return the cheapest set of trenches that wires every mast together.

    Args:
        masts: Every mast, as (name, east, north).

    Returns:
        (total metres, trenches in the order accepted). Trenches of equal
        price are considered in list order, so the answer is the same every
        run. A single mast needs no trench and costs nothing.
    """
    moor = Moor(len(masts))
    priced = sorted(
        (boom_cost(masts[left], masts[right]), left, right)
        for left, right in combinations(range(len(masts)), 2)
    )
    chosen: list[tuple[str, str, int]] = []
    total = 0
    for price, left, right in priced:
        if moor.join(left, right):
            chosen.append((masts[left][0], masts[right][0], price))
            total += price
            if len(chosen) == len(masts) - 1:
                break
    return total, chosen


def longest_trench(chosen: list[tuple[str, str, int]]) -> tuple[str, str, int] | None:
    """Return the single widest trench in a chosen network.

    Args:
        chosen: The trenches cheapest_network picked.

    Returns:
        The trench with the largest price, ties broken by mast names. None
        when there are no trenches at all.
    """
    if not chosen:
        return None
    return max(chosen, key=lambda trench: (trench[2], trench[0], trench[1]))


# ---- Self-check ----
if __name__ == "__main__":
    total, chosen = cheapest_network(MASTS)
    print("trenches to dig, in order")
    for left, right, price in chosen:
        print(f"  {price:2d}m  {left} - {right}")
    print(f"total: {total}m across {len(chosen)} trenches")
    print(f"boom to hire: {longest_trench(chosen)}")

    print()
    print("what the boom rule changes")
    alder, drum = MASTS[0], MASTS[3]
    print(f"  {alder[0]} to {drum[0]}: boom {boom_cost(alder, drum)}m, "
          f"east-west plus north-south {abs(alder[1] - drum[1]) + abs(alder[2] - drum[2])}m")

    assert total == 13
    assert chosen == [
        ("Beacon Ridge", "Fold Head", 1),
        ("Alder Hill", "Fold Head", 2),
        ("Cross Fell", "Fold Head", 2),
        ("Beacon Ridge", "Drum Rig", 4),
        ("Beacon Ridge", "Ewe Crag", 4),
    ]
    assert len(chosen) == len(MASTS) - 1
    assert longest_trench(chosen) == ("Beacon Ridge", "Ewe Crag", 4)
    assert boom_cost(("a", 0, 0), ("b", 3, 4)) == 4      # not 5, and not 7
    assert cheapest_network([("Lone Pike", 9, 9)]) == (0, [])
    assert longest_trench([]) is None
    print("All checks passed.")
```

</details>
---

## Problem 4 — The Radiator Loop Check

**The brief.** A plumber surveys the heating in an old building. Radiators are
numbered from zero and each pipe run joins two of them. Good pipework is a tree:
every radiator fed, and no ring letting water go round without ever reaching the
far end.

**Two faults are possible and they are independent**, so a plain true-or-false
answer loses information. Name both:

```text
"tree"            every radiator fed, no ring
"loop"            there is a ring, but everything is still fed
"split"           no ring, but some radiators are unreachable
"loop and split"  both
```

**Constraints.** Reporting one bit where there are two facts is the wrong answer
the problem is built to reject. A survey can be a ring *and* have an orphaned
wing, and the plumber needs to know which of the two they are dealing with — the
fixes are different.

**Answer.** Union-find, one pass over the runs. A run whose two radiators are
**already joined** closes a ring — that run is a loop-closer. After the pass,
count the distinct roots: more than one means the system is split.

Both facts come out of the same walk, which is why they cost nothing extra to
report separately.

`loop_closing_runs` returns the runs you could cut — the ones that closed a ring —
which is the actionable half of the answer.

**Signatures.** `Pipework` with the union-find,
`survey_pipework(radiator_count, runs)`,
`loop_closing_runs(radiator_count, runs)`.

**Watch for.** Returning a boolean. Counting roots before the pass rather than
after. A building with zero pipe runs and one radiator is a tree; with zero runs
and three radiators it is split.

<details>
<summary>Worked answer — <code>problem-04-radiator-loop-check-solution.py</code></summary>

```python
"""problem-04-radiator-loop-check-solution.py — is the pipework a tree, and if not, why not.

A plumber surveys the heating in an old building. Radiators are numbered from
zero, and each pipe run joins two of them. Good pipework is a tree: every
radiator fed, and no ring that lets water go round and round without ever
reaching the far end of the building.

Two faults are possible and they are independent, so a plain True or False
loses information. This survey names both:

  "tree"           every radiator fed, no ring
  "loop"           there is a ring, but everything is still fed
  "split"          no ring, but some radiators are on a separate system
  "loop and split" both faults at once

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
# (name of the survey, radiator count, pipe runs between radiators)
Survey = tuple[str, int, list[tuple[int, int]]]

SURVEYS: list[Survey] = [
    ("Coach House", 5, [(0, 1), (0, 2), (2, 3), (3, 4)]),
    ("Long Gallery", 5, [(0, 1), (1, 2), (2, 0), (3, 4), (0, 3)]),
    ("Stable Block", 6, [(0, 1), (1, 2), (3, 4)]),
    ("Bothy", 4, [(0, 1), (1, 2), (2, 0), (2, 1)]),
    ("Gatehouse", 1, []),
    ("Boiler Room", 3, [(0, 1), (1, 2), (0, 2)]),
]


# ---- Your task ----
class Pipework:
    """Radiators grouped by what water can reach, with compression and rank."""

    def __init__(self, radiator_count: int) -> None:
        """Start every radiator on a system of its own.

        Args:
            radiator_count: How many radiators the building has, from 0.
        """
        self.parent: list[int] = list(range(radiator_count))
        self.rank: list[int] = [0] * radiator_count
        self.systems: int = radiator_count

    def system_of(self, radiator: int) -> int:
        """Return the radiator that names this radiator's system.

        Args:
            radiator: The radiator to look up.

        Returns:
            The root radiator, flattening the path on the way back.
        """
        root = radiator
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[radiator] != root:
            self.parent[radiator], radiator = root, self.parent[radiator]
        return root

    def join(self, left: int, right: int) -> bool:
        """Connect two systems, shallower tree under deeper.

        Args:
            left: One radiator.
            right: The other radiator.

        Returns:
            True when the pipe run joined two separate systems. False when
            both ends were already on one system, which means this pipe run
            closed a ring.
        """
        left_root, right_root = self.system_of(left), self.system_of(right)
        if left_root == right_root:
            return False
        if self.rank[left_root] < self.rank[right_root]:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        if self.rank[left_root] == self.rank[right_root]:
            self.rank[left_root] += 1
        self.systems -= 1
        return True


def survey_pipework(radiator_count: int, runs: list[tuple[int, int]]) -> str:
    """Return the verdict on a building's pipework.

    Args:
        radiator_count: How many radiators the building has, from 0.
        runs: Every pipe run, as a pair of radiator numbers.

    Returns:
        One of "tree", "loop", "split" or "loop and split".

    Raises:
        ValueError: If radiator_count is not at least one.
    """
    if radiator_count < 1:
        raise ValueError("a building has at least one radiator")
    pipework = Pipework(radiator_count)
    has_loop = False
    for left, right in runs:
        if not pipework.join(left, right):
            has_loop = True
    is_split = pipework.systems > 1
    if has_loop and is_split:
        return "loop and split"
    if has_loop:
        return "loop"
    if is_split:
        return "split"
    return "tree"


def loop_closing_runs(radiator_count: int, runs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Return the pipe runs that closed a ring, in survey order.

    Args:
        radiator_count: How many radiators the building has, from 0.
        runs: Every pipe run, as a pair of radiator numbers.

    Returns:
        The runs whose two ends were already joined. Cutting these leaves the
        same radiators fed, which is what makes them the ones to cut.
    """
    pipework = Pipework(radiator_count)
    return [(left, right) for left, right in runs if not pipework.join(left, right)]


# ---- Self-check ----
if __name__ == "__main__":
    print(f"{'building':<14}{'runs':>5}  verdict")
    for name, radiators, runs in SURVEYS:
        verdict = survey_pipework(radiators, runs)
        print(f"{name:<14}{len(runs):>5}  {verdict}")

    print()
    for name, radiators, runs in SURVEYS:
        closing = loop_closing_runs(radiators, runs)
        if closing:
            print(f"{name}: cut {closing}")

    assert survey_pipework(5, SURVEYS[0][2]) == "tree"
    assert survey_pipework(5, SURVEYS[1][2]) == "loop"
    assert survey_pipework(6, SURVEYS[2][2]) == "split"
    assert survey_pipework(4, SURVEYS[3][2]) == "loop and split"
    assert survey_pipework(1, []) == "tree"
    assert survey_pipework(3, SURVEYS[5][2]) == "loop"

    # A tree on n radiators has exactly n - 1 runs, but the run count on its
    # own proves nothing. The Boiler Room has three runs on three radiators
    # and is a ring; the Stable Block has three runs on six and is split.
    assert len(SURVEYS[5][2]) == 3 and survey_pipework(3, SURVEYS[5][2]) == "loop"
    assert len(SURVEYS[2][2]) == 3 and survey_pipework(6, SURVEYS[2][2]) == "split"
    assert loop_closing_runs(5, SURVEYS[1][2]) == [(2, 0)]
    assert loop_closing_runs(4, SURVEYS[3][2]) == [(2, 0), (2, 1)]
    assert loop_closing_runs(5, SURVEYS[0][2]) == []

    try:
        survey_pipework(0, [])
    except ValueError as problem:
        assert str(problem) == "a building has at least one radiator"
    else:                                    # pragma: no cover - the guard must fire
        raise AssertionError("an empty building should have been refused")
    print("All checks passed.")
```

</details>
---

## Problem 5 — The Market Stall Reach

**The brief.** A covered market has numbered stalls joined by aisles. Pushing a
loaded barrow along an aisle takes a known number of seconds, and an aisle is
walkable both ways at the same cost.

The market wants the **quietest pitch**: the stall from which the fewest other
stalls are within a barrow-push budget.

**Constraints.** The question is about **every pair** of stalls, not about one
starting point. That is what decides the algorithm, and saying so is the
recognition step.

**Answer.** All-pairs distances in one go: start from the direct aisle times, then
for every possible intermediate stall, check whether going via it is quicker than
what you have. Three nested loops, and the intermediate stall must be the
**outermost** of the three — that ordering is the whole correctness argument and
it is the thing to get right before writing anything else.

Then count, per stall, how many others are within the budget, and take the
smallest count.

With a budget of 10 seconds the quietest pitch is **stall 6, reaching one other
stall**.

Running one search per stall gives the same answer. On a market this size it
costs about the same; the write-up should say at what size that stops being true
and why.

**Signatures.** `push_times(stall_count, aisles)`,
`neighbours_within(times, stall, budget)`,
`quietest(stall_count, aisles, budget)`.

**Watch for.** Putting the intermediate stall in an inner loop — the answer is
then wrong in a way that looks plausible on small inputs. Counting the stall
itself among its neighbours. Unreachable pairs must stay at infinity rather than
becoming a large number that later arithmetic treats as real.

<details>
<summary>Worked answer — <code>problem-05-market-stall-reach-solution.py</code></summary>

```python
"""problem-05-market-stall-reach-solution.py — every pair of stalls at once.

A covered market has numbered stalls joined by aisles. Pushing a loaded
barrow along an aisle takes a known number of seconds, and an aisle is
walkable both ways at the same cost.

The market wants the quietest pitch: the stall from which the fewest other
stalls are within a barrow-push budget. That question is about every pair of
stalls, not about one starting point, so it is answered once for the whole
market rather than one search per stall.

  push_times   — the seconds between every pair of stalls
  quietest     — the stall with the fewest neighbours inside the budget

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
STALL_COUNT = 7

# (stall, stall, seconds to push a barrow along that aisle, both ways)
AISLES: list[tuple[int, int, int]] = [
    (0, 1, 10),
    (1, 2, 10),
    (2, 3, 10),
    (3, 4, 10),
    (4, 5, 10),
    (1, 4, 5),
    (5, 6, 10),
    (0, 6, 20),
    (2, 6, 45),
]

BUDGET = 10


# ---- Your task ----
def push_times(stall_count: int, aisles: list[tuple[int, int, int]]) -> list[list[float]]:
    """Return the shortest push time between every pair of stalls.

    The table starts with the aisles themselves and is then improved once per
    stall. After the round for stall `middle`, every entry is the best time
    that uses only stalls up to `middle` in the middle of the route. After the
    last round, every stall has been allowed in the middle, so the table is
    finished.

    Args:
        stall_count: How many stalls the market has, numbered from 0.
        aisles: Every aisle, as (stall, stall, seconds).

    Returns:
        A square table where times[a][b] is the seconds from a to b, 0 on the
        diagonal, and float("inf") where no route exists.
    """
    times: list[list[float]] = [
        [0.0 if here == there else float("inf") for there in range(stall_count)]
        for here in range(stall_count)
    ]
    for here, there, seconds in aisles:
        times[here][there] = min(times[here][there], float(seconds))
        times[there][here] = times[here][there]

    for middle in range(stall_count):
        for here in range(stall_count):
            through = times[here][middle]
            if through == float("inf"):
                continue                     # nothing to gain by going via middle
            for there in range(stall_count):
                if through + times[middle][there] < times[here][there]:
                    times[here][there] = through + times[middle][there]
    return times


def neighbours_within(times: list[list[float]], stall: int, budget: int) -> int:
    """Return how many other stalls sit inside the budget from this one.

    Args:
        times: The table push_times returned.
        stall: The stall to count from.
        budget: The barrow-push budget in seconds.

    Returns:
        The count of other stalls whose push time is at most the budget. The
        stall itself is never counted.
    """
    return sum(
        1
        for there, seconds in enumerate(times[stall])
        if there != stall and seconds <= budget
    )


def quietest(stall_count: int, aisles: list[tuple[int, int, int]], budget: int) -> tuple[int, int]:
    """Return the stall with the fewest neighbours inside the budget.

    Args:
        stall_count: How many stalls the market has, numbered from 0.
        aisles: Every aisle, as (stall, stall, seconds).
        budget: The barrow-push budget in seconds.

    Returns:
        (stall, count). Where two stalls tie on count the higher-numbered one
        wins, because the far end of the market is the quieter pitch.
    """
    times = push_times(stall_count, aisles)
    best_stall, best_count = 0, neighbours_within(times, 0, budget)
    for stall in range(1, stall_count):
        count = neighbours_within(times, stall, budget)
        if count <= best_count:              # <=, so a later stall wins a tie
            best_stall, best_count = stall, count
    return best_stall, best_count


# ---- Self-check ----
if __name__ == "__main__":
    times = push_times(STALL_COUNT, AISLES)
    print("push times in seconds")
    print("      " + "".join(f"{there:6d}" for there in range(STALL_COUNT)))
    for here in range(STALL_COUNT):
        cells = "".join(
            "   inf" if seconds == float("inf") else f"{int(seconds):6d}"
            for seconds in times[here]
        )
        print(f"{here:4d}  {cells}")

    print()
    print(f"stalls within {BUDGET}s")
    for stall in range(STALL_COUNT):
        print(f"  stall {stall}: {neighbours_within(times, stall, BUDGET)}")
    print(f"quietest pitch: {quietest(STALL_COUNT, AISLES, BUDGET)}")

    assert times[0][0] == 0
    assert times[0][4] == 15                 # 0-1-4 beats 0-1-2-3-4
    assert times[2][5] == 25                 # 2-1-4-5
    assert times[2][6] == 35                 # 2-1-4-5-6 beats the direct 45
    assert times[3][6] == 30
    assert all(times[a][b] == times[b][a] for a in range(STALL_COUNT) for b in range(STALL_COUNT))
    # Stalls 0 and 6 both have one neighbour inside 10s; the far end wins.
    assert neighbours_within(times, 0, BUDGET) == 1
    assert quietest(STALL_COUNT, AISLES, BUDGET) == (6, 1)
    assert quietest(STALL_COUNT, AISLES, 30) == (6, 5)
    assert quietest(STALL_COUNT, AISLES, 1000) == (6, 6)

    lonely = push_times(2, [])
    assert lonely[0][1] == float("inf")
    assert quietest(2, [], 5) == (1, 0)
    print("All checks passed.")
```

</details>
---

## Problem 6 — The Relay Reliability

**The brief.** A harbour passes messages between boats by short-range radio. Each
hop works some fraction of the time — a hop of 0.9 gets through nine times in ten.
A relay through several boats works only if **every** hop works, so the chance of
the whole relay is the hops **multiplied**, never added.

Find the most reliable relay from one boat to another.

**Constraints.** Multiplying makes a route worse the longer it gets, and the job
is to make the number **as large as possible** rather than as small as possible.
Both of those invert the usual search, and inverting exactly one of them is the
most common wrong answer.

**Answer.** The same search shape as a shortest path, with two changes and no
others: combine costs by multiplying instead of adding, and take the **best**
frontier entry as the largest rather than the smallest. Reliabilities are between
0 and 1, so multiplying can only shrink a route — which is what makes the greedy
argument hold, exactly as non-negative edge weights do in the additive case.

That sentence is what the write-up is really for. It is also why the same trick
does not survive a hop with reliability above 1, and saying so shows you
understand the argument rather than the recipe.

From Anvil: Cutter at 0.9 in one hop, Dredger at 0.4 in two, Ebb at 0.36 in
three, and Fluke unreachable.

**Signatures.** `build_radio(hops)`, `best_relay(hops, start, end)`,
`relay_rows(hops, boats, start)`.

**Watch for.** Adding the reliabilities, which can exceed 1 and means nothing.
Taking the smallest frontier entry, which finds the *worst* relay confidently.
Starting the source at 0 rather than 1 — the multiplicative identity is 1, and
starting at 0 makes every relay impossible. An unreachable boat returns `None`.

<details>
<summary>Worked answer — <code>problem-06-relay-reliability-solution.py</code></summary>

```python
"""problem-06-relay-reliability-solution.py — the relay most likely to get through.

A harbour passes messages between boats by short-range radio. Each radio hop
works some fraction of the time: a hop with reliability 0.9 gets the message
through nine times in ten. A relay through several boats only works if every
hop on it works, so the chance of the whole relay is the hops multiplied
together, never added.

Multiplying makes a route worse the longer it gets, and the job is to make
that number as large as possible rather than as small as possible. The search
is otherwise the same shape as a shortest-path search.

  best_relay   — the likeliest route, its chance, and how many hops it takes

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
# (boat, boat, chance one hop between them gets through)
Hop = tuple[str, str, float]

HOPS: list[Hop] = [
    ("Anvil", "Bosun", 0.5),
    ("Anvil", "Cutter", 0.9),
    ("Cutter", "Bosun", 0.5),
    ("Bosun", "Dredger", 0.8),
    ("Cutter", "Dredger", 0.4),
    ("Dredger", "Ebb", 0.9),
]

BOATS: list[str] = ["Anvil", "Bosun", "Cutter", "Dredger", "Ebb", "Fluke"]


# ---- Your task ----
def build_radio(hops: list[Hop]) -> dict[str, list[tuple[str, float]]]:
    """Return the hops keyed by boat, both ways round.

    Args:
        hops: Every radio hop, as (boat, boat, chance).

    Returns:
        A dict where radio[boat] is a list of (other boat, chance). Radio
        works both ways, so each hop appears under both boats.
    """
    radio: dict[str, list[tuple[str, float]]] = {}
    for here, there, chance in hops:
        radio.setdefault(here, []).append((there, chance))
        radio.setdefault(there, []).append((here, chance))
    return radio


def best_relay(hops: list[Hop], start: str, end: str) -> tuple[float, int] | None:
    """Return the best chance of getting a message from start to end.

    The queue holds the negative of the chance, because Python's heap always
    hands back the smallest item and the largest chance is wanted first.
    Negating turns "largest chance" into "smallest number", which is what the
    heap is good at.

    Args:
        hops: Every radio hop, as (boat, boat, chance).
        start: The boat sending the message.
        end: The boat that has to receive it.

    Returns:
        (chance rounded to six decimal places, number of hops). Where two
        relays have the same chance the one with fewer hops wins. None when
        no relay of working hops connects the two boats.
    """
    radio = build_radio(hops)
    best: dict[str, tuple[float, int]] = {start: (1.0, 0)}
    settled: set[str] = set()
    queue: list[tuple[float, int, str]] = [(-1.0, 0, start)]

    while queue:
        negative_chance, hop_count, boat = heapq.heappop(queue)
        if boat in settled:
            continue
        settled.add(boat)
        if boat == end:
            return round(-negative_chance, 6), hop_count
        for other, chance in radio.get(boat, []):
            onward = -negative_chance * chance
            known_chance, known_hops = best.get(other, (-1.0, 0))
            if onward > known_chance or (
                onward == known_chance and hop_count + 1 < known_hops
            ):
                best[other] = (onward, hop_count + 1)
                heapq.heappush(queue, (-onward, hop_count + 1, other))

    return None


def relay_rows(hops: list[Hop], boats: list[str], start: str) -> list[str]:
    """Return one printable row per boat, best chance and hop count.

    Args:
        hops: Every radio hop, as (boat, boat, chance).
        boats: Every boat in the harbour, including any with no radio hop.
        start: The boat sending the message.

    Returns:
        Rows in boat-name order. A boat no relay reaches says "no relay".
    """
    rows = []
    for boat in sorted(boats):
        relay = best_relay(hops, start, boat)
        if relay is None:
            rows.append(f"  {boat:<9} no relay")
        else:
            chance, hop_count = relay
            plural = "hop" if hop_count == 1 else "hops"
            rows.append(f"  {boat:<9} {chance:8.6f}  {hop_count} {plural}")
    return rows


# ---- Self-check ----
if __name__ == "__main__":
    print("best relay from Anvil")
    for row in relay_rows(HOPS, BOATS, "Anvil"):
        print(row)

    assert best_relay(HOPS, "Anvil", "Anvil") == (1.0, 0)
    assert best_relay(HOPS, "Anvil", "Cutter") == (0.9, 1)
    # 0.5 direct beats 0.9 * 0.5 = 0.45 through Cutter.
    assert best_relay(HOPS, "Anvil", "Bosun") == (0.5, 1)
    # 0.5 * 0.8 = 0.4 beats 0.9 * 0.4 = 0.36.
    assert best_relay(HOPS, "Anvil", "Dredger") == (0.4, 2)
    assert best_relay(HOPS, "Anvil", "Ebb") == (0.36, 3)
    assert best_relay(HOPS, "Anvil", "Fluke") is None
    assert best_relay(HOPS, "Ebb", "Anvil") == (0.36, 3)

    dead = [("Anvil", "Bosun", 0.0)]
    assert best_relay(dead, "Anvil", "Bosun") == (0.0, 1)
    print("All checks passed.")
```

</details>
---

## Rubric (5 axes, 4 points each)

| Axis | What "great" looks like |
|------|--------------------------|
| Frame the problem | The memo names the structure and — for problems 2 and 6 — exactly which part of the usual search changed and which part did not. |
| Reason about options | Four to six bullets before any code, with the alternative named and costed. |
| Assemble the solution | Idiomatic Python; union-find with both path compression and union by size, and a sentence on why each is there; type hints throughout. |
| Measure it | A trace on at least two inputs, one of them degenerate or unreachable. |
| Evaluate the cost | Time, space, best/average/worst, the trade-off and the improvement — in the problem's own numbers. |

Twenty points per problem, 120 for the set. Score yourself honestly; the number
is only useful if it is true.

---

## How to submit

Commit your write-ups under `frame-writeups/c2-week-10/homework/`, one file per
problem:

```
frame-writeups/c2-week-10/homework/
├── problem-1-claim-slip-merge.md
├── problem-2-kerb-step-route.md
├── problem-3-mast-trench-network.md
├── problem-4-radiator-loop-check.md
├── problem-5-market-stall-reach.md
└── problem-6-relay-reliability.md
```

Each file is 100–200 lines: the five FRAME sections plus a five-line memo at the
top. The code is part of the Assemble section, not a separate file.

When the set is done, push and move on to the
[mini-project](../mini-project/README.md).

---

## Time budget

| Problem | Solve | Write-up | Total |
|---------|------:|---------:|------:|
| 1 — Claim Slip Merge | 35 min | 15 min | 50 min |
| 2 — Kerb Step Route | 45 min | 15 min | 60 min |
| 3 — Mast Trench Network | 40 min | 15 min | 55 min |
| 4 — Radiator Loop Check | 35 min | 15 min | 50 min |
| 5 — Market Stall Reach | 35 min | 15 min | 50 min |
| 6 — Relay Reliability | 40 min | 15 min | 55 min |

About five and a half hours. Problems 2 and 6 are the two that pay off most in a
real round, because both are the same search with one thing changed — and being
able to say which thing is the difference between knowing an algorithm and
knowing what it is made of.
