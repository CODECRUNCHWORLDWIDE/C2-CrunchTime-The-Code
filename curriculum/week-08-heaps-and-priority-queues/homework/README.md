# Week 8 — Homework

Six problems, all original, each with a runnable worked answer folded under it.
Allow about five hours. Do each problem with the lectures closed; open the
reveal only after your own version runs, or after fifteen minutes stuck on one
step.

The six cover every heap sub-shape the week teaches, so that by Sunday the
recognition step is reflexive: a bounded shortlist, a repeated-merge cost, a
k-way merge over sorted sources, a spacing scheduler, a two-heap unlock loop,
and a two-heap running statistic.

| # | Problem | Sub-shape | Est. time |
|---|---------|-----------|----------:|
| 1 | [The Dawn Chorus Shortlist](#problem-1--the-dawn-chorus-shortlist) | Bounded top-k with a two-direction tiebreak | 35 min |
| 2 | [The Splice Drum Tape](#problem-2--the-splice-drum-tape) | Repeated merge of the two smallest | 30 min |
| 3 | [The Germination Grid Rank](#problem-3--the-germination-grid-rank) | k-way merge, stopping at rank k | 50 min |
| 4 | [The Night Rota](#problem-4--the-night-rota) | Max-heap scheduler with a held-back slot | 50 min |
| 5 | [The Grant Round](#problem-5--the-grant-round) | Two heaps: locked by cost, unlocked by payout | 60 min |
| 6 | [The Oven Probe Midline](#problem-6--the-oven-probe-midline) | Two heaps: the running middle | 45 min |

Every worked answer runs on its own with no arguments and no packages, and ends
by printing `All checks passed.` To run one, copy the code out of the reveal
into a file of your own and run that file:

```bash
python problem-01-dawn-chorus-shortlist.py
```

---

## Problem 1 — The Dawn Chorus Shortlist

**The brief.** A recorder logs one line per bird detection through a spring
morning — 33 detections across eight species. The survey wants the **five
most-heard species**, most first, and **alphabetical** between species heard the
same number of times.

**The data.**

```text
wren 9 · robin 8 · blackcap 5 · song thrush 4 · chiffchaff 3
dunnock 2 · goldcrest 1 · nuthatch 1
```

**Constraints.** The two halves of the sort rule pull in **opposite
directions**: count downwards, name upwards. A string cannot be negated, so the
usual "negate the key" trick only half works — and noticing that before you write
it is the point of the problem.

**Answer.** `heapq.nsmallest(size, counts.items(), key=lambda kv: (-kv[1], kv[0]))`.
The key sorts by negated count, so higher counts come first among the "smallest"
keys, and then by name ascending — which is exactly the rule. `nsmallest` holds
`size` entries rather than sorting all eight species, and the negation lives only
in the key, never in the data.

**Signatures.** `shortlist(detections, size)`, `heard_once(detections)`,
`share_of_dawn(detections, species)`.

**Watch for.** Sorting twice to get the two directions — it works, and it says you
did not see the single-key answer. A species never heard has a share of `0.0`,
not an error. `size = 0` returns an empty list; a size above the species count
returns all eight.

<details>
<summary>Worked answer — <code>problem-01-dawn-chorus-shortlist-solution.py</code></summary>

```python
"""problem-01-dawn-chorus-shortlist-solution.py — the most-heard birds of the dawn watch.

A recorder logs one line per detection through a spring morning. The survey
wants the five most-heard species, most first, and alphabetical between species
that were heard the same number of times.

The two halves of that rule pull in opposite directions — count downwards, name
upwards — and a string cannot be negated. `heapq.nsmallest` with a tuple key is
the tool that handles both directions in one bounded pass.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

import heapq
from collections import Counter

# ---- Given data ----
DETECTIONS: list[str] = [
    "blackcap", "wren", "robin", "wren", "song thrush", "robin", "wren",
    "chiffchaff", "blackcap", "wren", "robin", "dunnock", "song thrush",
    "wren", "blackcap", "robin", "chiffchaff", "wren", "goldcrest", "robin",
    "song thrush", "wren", "blackcap", "dunnock", "robin", "wren", "nuthatch",
    "blackcap", "robin", "song thrush", "wren", "chiffchaff", "robin",
]

SHORTLIST_SIZE = 5


# ---- Your task ----
def shortlist(detections: list[str], size: int) -> list[tuple[str, int]]:
    """Return the most-heard species, most first.

    Args:
        detections: One species name per detection, in any order.
        size: How many species to list. 0 lists none.

    Returns:
        (species, count) pairs, highest count first, ties alphabetical. When
        fewer distinct species were heard than `size`, every species is
        returned.
    """
    if size <= 0:
        return []
    counts = Counter(detections)
    return heapq.nsmallest(size, counts.items(), key=lambda pair: (-pair[1], pair[0]))


def heard_once(detections: list[str]) -> list[str]:
    """Return the species heard exactly one time, alphabetically.

    Args:
        detections: One species name per detection.

    Returns:
        Species names, A to Z. Empty when every species was heard twice or more.
    """
    counts = Counter(detections)
    return sorted(name for name, count in counts.items() if count == 1)


def share_of_dawn(detections: list[str], species: str) -> float:
    """Return what fraction of the morning's detections one species accounts for.

    Args:
        detections: One species name per detection.
        species: The species to measure.

    Returns:
        A fraction between 0.0 and 1.0, rounded to three places. A species that
        was never heard gives 0.0, and so does an empty log.
    """
    if not detections:
        return 0.0
    return round(detections.count(species) / len(detections), 3)


# ---- Self-check ----
if __name__ == "__main__":
    top = shortlist(DETECTIONS, SHORTLIST_SIZE)
    print(f"detections logged: {len(DETECTIONS)}")
    print(f"distinct species : {len(set(DETECTIONS))}")
    print("shortlist:")
    for rank, (species, count) in enumerate(top, 1):
        print(f"  {rank}. {count:2d}  {species}")

    print(f"heard once: {heard_once(DETECTIONS)}")
    print(f"wren's share: {share_of_dawn(DETECTIONS, 'wren')}")
    print(f"raven's share: {share_of_dawn(DETECTIONS, 'raven')}")
    print(f"asking for more than exist: {len(shortlist(DETECTIONS, 99))}")
    print(f"asking for none: {shortlist(DETECTIONS, 0)}")
    print(f"an empty log: {shortlist([], 3)}")

    assert top[0] == ("wren", 9)
    assert top[1] == ("robin", 8)
    assert top[2] == ("blackcap", 5)
    assert top[3] == ("song thrush", 4)
    assert top[4] == ("chiffchaff", 3)
    assert heard_once(DETECTIONS) == ["goldcrest", "nuthatch"]
    assert share_of_dawn(DETECTIONS, "raven") == 0.0
    assert len(shortlist(DETECTIONS, 99)) == len(set(DETECTIONS))
    assert shortlist(DETECTIONS, 0) == []
    assert shortlist([], 3) == []
    print("All checks passed.")
```

</details>
---

## Problem 2 — The Splice Drum Tape

**The brief.** A cable crew joins several drums of fibre into one continuous run.
Each join costs tape equal to the **combined length of the two pieces being
joined**, so the *order* of the joins changes the bill. Report the cheapest total
and the cost of each join along the way.

**The data.** Drums of 12, 9, 30, 21, 5 and 16 metres.

**Constraints.** Every join reduces the count by one, so there are always exactly
`n - 1` joins whatever order you pick. The order is the only lever.

**Answer.** Always join the **two shortest pieces** available. Heapify the drums,
then repeatedly pop two, push their sum, and record that sum as the join's cost.
Why it is optimal is the sentence the write-up needs: a piece's length is paid for
once per join it takes part in, so the pieces that go through the most joins
should be the shortest ones — and joining the two shortest first is what pushes
the long pieces to the end.

Total on this data: **226 m**, against **378 m** for the worst order. The
difference is 152 m of tape on six drums.

**Signatures.** `splice_costs(drums)`, `worst_order_cost(drums)`,
`run_length(drums)`.

**Watch for.** One drum needs no joins and costs nothing — not an error, and not
the drum's own length. No drums at all costs nothing too. `run_length` is just
the sum, and it is there to check the joins conserved the fibre.

<details>
<summary>Worked answer — <code>problem-02-splice-drum-tape-solution.py</code></summary>

```python
"""problem-02-splice-drum-tape-solution.py — joining fibre drums with the least tape.

A cable crew has to join several drums of fibre into one continuous run. Each
join costs tape equal to the combined length of the two pieces being joined, so
the order of the joins changes the bill. Always joining the two shortest pieces
first is the cheapest order, and a min-heap makes "the two shortest" a pair of
pops.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
# Drum lengths in metres.
DRUM_METRES: list[int] = [12, 9, 30, 21, 5, 16]


# ---- Your task ----
def splice_costs(drums: list[int]) -> tuple[int, list[int]]:
    """Return the cheapest total tape and the cost of each join, in order.

    Args:
        drums: Drum lengths in metres. This list is not modified.

    Returns:
        (total tape in metres, one cost per join). One drum needs no join, so
        it costs nothing; no drums at all costs nothing too.
    """
    if len(drums) < 2:
        return 0, []
    pieces = list(drums)
    heapq.heapify(pieces)
    costs = []
    while len(pieces) > 1:
        shortest = heapq.heappop(pieces)
        second = heapq.heappop(pieces)
        joined = shortest + second
        costs.append(joined)
        heapq.heappush(pieces, joined)
    return sum(costs), costs


def worst_order_cost(drums: list[int]) -> int:
    """Return what the same drums cost when the two LONGEST are joined first.

    This is the same simulation with the comparison flipped, and it exists to
    be compared against — the difference is the whole point of the greedy rule.

    Args:
        drums: Drum lengths in metres. This list is not modified.

    Returns:
        The total tape in metres for the worst join order.
    """
    if len(drums) < 2:
        return 0
    pieces = [-length for length in drums]
    heapq.heapify(pieces)
    total = 0
    while len(pieces) > 1:
        longest = -heapq.heappop(pieces)
        second = -heapq.heappop(pieces)
        joined = longest + second
        total += joined
        heapq.heappush(pieces, -joined)
    return total


def run_length(drums: list[int]) -> int:
    """Return the length of the finished run, which the join order cannot change.

    Args:
        drums: Drum lengths in metres.

    Returns:
        The sum of the drum lengths.
    """
    return sum(drums)


# ---- Self-check ----
if __name__ == "__main__":
    total, costs = splice_costs(DRUM_METRES)
    print(f"drums: {DRUM_METRES}")
    print(f"finished run: {run_length(DRUM_METRES)} m")
    print("joins, cheapest order:")
    for number, cost in enumerate(costs, 1):
        print(f"  join {number}: {cost} m of tape")
    print(f"total tape, cheapest order: {total} m")
    print(f"total tape, worst order   : {worst_order_cost(DRUM_METRES)} m")
    print(f"difference: {worst_order_cost(DRUM_METRES) - total} m")

    print(f"one drum: {splice_costs([40])}")
    print(f"no drums: {splice_costs([])}")
    print(f"two drums: {splice_costs([7, 3])}")

    assert costs == [14, 26, 37, 56, 93]
    assert total == 226
    assert run_length(DRUM_METRES) == 93
    assert costs[-1] == run_length(DRUM_METRES)
    assert worst_order_cost(DRUM_METRES) > total
    assert splice_costs([40]) == (0, [])
    assert splice_costs([]) == (0, [])
    assert splice_costs([7, 3]) == (10, [10])
    assert DRUM_METRES == [12, 9, 30, 21, 5, 16]  # original list untouched
    print("All checks passed.")
```

</details>
---

## Problem 3 — The Germination Grid Rank

**The brief.** A seed lab runs four trays of four slots. Every tray's counts rise
**left to right**, and every slot's counts rise **tray to tray**. The lab wants
the **k-th lowest count** in the whole grid and the slot it came from.

**The data.**

```text
tray 1    2   6  11  17
tray 2    5   6  14  21
tray 3    9  13  15  26
tray 4   12  19  23  30
```

**Constraints.** Two slots can tie — there are two 6s here — so the answer is a
count *and* a position, and the tie has to resolve to one of them by a stated
rule rather than by luck.

**Answer.** Each tray is an already-sorted source, so this is a k-way merge that
**stops after k pops**. Seed a heap with the first count of each tray, then pop k
times, pushing the next count from whichever tray the pop came from. Sorting all
sixteen is correct and costs `O(n log n)`; the merge costs `O(k log t)` for t
trays and never looks at the counts past rank k. On a four-by-four grid that
saves nothing; on a thousand trays it is the whole answer.

Rank 7 on this grid is **12, in tray 4 slot 1**.

**Signatures.** `nth_lowest(grid, rank)`, `merged_counts(grid)`,
`slot_of_rank(grid, rank)`.

**Watch for.** A rank outside `1..16` raises `ValueError` rather than returning
something. Ragged trays — rows of different lengths — must not crash the merge.
The row-and-column ordering is *not* a full sort of the grid: tray 2's first
count (5) is lower than tray 1's second (6), which is exactly why a row-by-row
scan gets the wrong answer.

<details>
<summary>Worked answer — <code>problem-03-germination-grid-rank-solution.py</code></summary>

```python
"""problem-03-germination-grid-rank-solution.py — the seventh-lowest germination count.

A seed lab runs four trays of four slots. Every tray's counts rise from left to
right, and every slot's counts rise from tray to tray. The lab wants the k-th
lowest count in the whole grid and, because two slots can tie, the slot it came
from.

Each tray is an already-sorted source, so a heap holding one pending count per
tray merges them and stops after k pops instead of sorting all sixteen.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
# Rows are trays; each row rises left to right, each column rises top to bottom.
GRID: list[list[int]] = [
    [2, 6, 11, 17],
    [5, 6, 14, 21],
    [9, 13, 15, 26],
    [12, 19, 23, 30],
]

WANTED_RANK = 7


# ---- Your task ----
def nth_lowest(grid: list[list[int]], rank: int) -> tuple[int, int, int]:
    """Return the rank-th lowest count in the grid, with the slot it came from.

    Args:
        grid: Trays of counts. Each tray is ascending. Trays may differ in
            length, and a tray may be empty.
        rank: Which count to return, counting from 1. Equal counts each take a
            place of their own, so a grid of sixteen slots has sixteen ranks.

    Returns:
        (count, tray index, slot index). Where two slots hold the same count,
        the lower tray comes first, and within a tray the lower slot.

    Raises:
        ValueError: When `rank` is below 1 or above the number of slots.
    """
    slots = sum(len(tray) for tray in grid)
    if rank < 1 or rank > slots:
        raise ValueError(f"rank {rank} is outside 1..{slots}")

    pending = [(tray[0], index, 0) for index, tray in enumerate(grid) if tray]
    heapq.heapify(pending)
    for _ in range(rank - 1):
        count, tray_index, slot_index = heapq.heappop(pending)
        if slot_index + 1 < len(grid[tray_index]):
            heapq.heappush(
                pending,
                (grid[tray_index][slot_index + 1], tray_index, slot_index + 1),
            )
    return pending[0]


def merged_counts(grid: list[list[int]]) -> list[int]:
    """Return every count in the grid, lowest first.

    Args:
        grid: Trays of counts, each tray ascending.

    Returns:
        All counts in one ascending list, duplicates kept.
    """
    return [nth_lowest(grid, rank)[0] for rank in range(1, sum(map(len, grid)) + 1)]


def slot_of_rank(grid: list[list[int]], rank: int) -> str:
    """Return a readable label for the slot at a rank.

    Args:
        grid: Trays of counts, each tray ascending.
        rank: Which count to name, counting from 1.

    Returns:
        A string like "tray 4 slot 1", counting both from 1.
    """
    _, tray_index, slot_index = nth_lowest(grid, rank)
    return f"tray {tray_index + 1} slot {slot_index + 1}"


# ---- Self-check ----
if __name__ == "__main__":
    count, tray_index, slot_index = nth_lowest(GRID, WANTED_RANK)
    print(f"grid slots: {sum(len(tray) for tray in GRID)}")
    print(f"rank {WANTED_RANK}: count {count} from {slot_of_rank(GRID, WANTED_RANK)}")
    print(f"lowest : {nth_lowest(GRID, 1)}")
    print(f"highest: {nth_lowest(GRID, 16)}")
    print("first eight ranks:")
    for rank in range(1, 9):
        value, tray, slot = nth_lowest(GRID, rank)
        print(f"  rank {rank}: {value:2d}  tray {tray + 1} slot {slot + 1}")

    print(f"merged: {merged_counts(GRID)}")
    print(f"ragged trays: {nth_lowest([[3], [], [1, 8]], 2)}")
    try:
        nth_lowest(GRID, 0)
    except ValueError as error:
        print(f"rank 0: ValueError: {error}")
    try:
        nth_lowest(GRID, 17)
    except ValueError as error:
        print(f"rank 17: ValueError: {error}")

    assert (count, tray_index, slot_index) == (12, 3, 0)
    assert nth_lowest(GRID, 1) == (2, 0, 0)
    assert nth_lowest(GRID, 3) == (6, 0, 1)
    assert nth_lowest(GRID, 4) == (6, 1, 1)  # the tie goes to the lower tray
    assert nth_lowest(GRID, 16) == (30, 3, 3)
    assert merged_counts(GRID) == sorted(value for tray in GRID for value in tray)
    assert nth_lowest([[3], [], [1, 8]], 2) == (3, 0, 0)
    print("All checks passed.")
```

</details>
---

## Problem 4 — The Night Rota

**The brief.** A night shelter needs one volunteer per night. Each volunteer has
agreed to a number of nights, and the house rule is that **nobody works two
nights in a row**. Build a rota that uses everybody's agreed nights, or say
plainly that no rota exists.

**The data.** Ama 4 nights, Beto 3, Cass 2, Dev 1 — ten nights to fill.

**Constraints.** "No rota exists" is a real answer and has to be returned as
`None`, not raised and not fudged. One person on five of six nights cannot be
spaced out, and the function must say so.

**Answer.** Greedy on a max-heap: **whoever has the most nights left works
tonight**, plus one held-back slot for last night's volunteer so they cannot be
picked again immediately. After picking, decrement, then return *last night's*
volunteer to the heap — the hold-back is one night deep, which is exactly the
rule.

The greedy is right because the volunteer with the most nights left is the one
most likely to be stranded at the end; every night given to somebody else is a
night they cannot use.

Rota on this data: `Ama Beto Ama Beto Ama Cass Ama Beto Cass Dev`.

**Signatures.** `build_rota(nights_agreed)`, `rota_is_legal(rota)`,
`nights_worked(rota)`.

**Watch for.** Returning `None` after building a partial rota rather than
detecting the impossibility. `rota_is_legal` must be written independently of
`build_rota` — a verifier that shares the builder's assumptions verifies nothing.
A single night, a zero pledge, and nobody at all are all valid inputs.

<details>
<summary>Worked answer — <code>problem-04-night-rota-spacing-solution.py</code></summary>

```python
"""problem-04-night-rota-spacing-solution.py — a night rota nobody works twice running.

A night shelter needs one volunteer per night. Each volunteer has agreed to a
number of nights, and the house rule is that nobody works two nights in a row.
Build a rota that uses everybody's agreed nights, or say plainly that no rota
exists.

The greedy rule is "whoever has the most nights left goes tonight", which is a
max-heap, plus one held-back slot for last night's volunteer so they cannot be
picked again immediately.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
# Volunteer to the number of nights they agreed to work.
NIGHTS_AGREED: dict[str, int] = {
    "Ama": 4,
    "Beto": 3,
    "Cass": 2,
    "Dev": 1,
}


# ---- Your task ----
def build_rota(nights_agreed: dict[str, int]) -> list[str] | None:
    """Return a rota with nobody on two nights running, or None if impossible.

    Args:
        nights_agreed: Volunteer to nights agreed. A volunteer agreeing to zero
            nights is ignored.

    Returns:
        One name per night, in order. None when no arrangement can avoid a
        volunteer working back to back — which happens exactly when one person
        has agreed to more than half the nights, rounded up.
    """
    available: list[tuple[int, str]] = [
        (-nights, name) for name, nights in nights_agreed.items() if nights > 0
    ]
    heapq.heapify(available)
    rota: list[str] = []
    resting: tuple[int, str] | None = None

    while available or resting:
        if not available:
            return None
        stored, name = heapq.heappop(available)
        rota.append(name)
        if resting is not None:
            heapq.heappush(available, resting)
            resting = None
        left = -stored - 1
        resting = (-left, name) if left > 0 else None
    return rota


def rota_is_legal(rota: list[str]) -> bool:
    """Return True when no name appears on two nights in a row.

    Args:
        rota: One name per night.

    Returns:
        True for a legal rota, including an empty one.
    """
    return all(tonight != tomorrow for tonight, tomorrow in zip(rota, rota[1:]))


def nights_worked(rota: list[str]) -> dict[str, int]:
    """Return how many nights each volunteer ends up working.

    Args:
        rota: One name per night.

    Returns:
        A dict of volunteer to night count, in first-appearance order.
    """
    worked: dict[str, int] = {}
    for name in rota:
        worked[name] = worked.get(name, 0) + 1
    return worked


# ---- Self-check ----
if __name__ == "__main__":
    rota = build_rota(NIGHTS_AGREED)
    print(f"nights to fill: {sum(NIGHTS_AGREED.values())}")
    print(f"rota: {rota}")
    print(f"legal: {rota_is_legal(rota)}")
    print(f"nights worked: {nights_worked(rota)}")

    crowded = {"Ama": 5, "Beto": 1}
    print(f"one person on five of six nights: {build_rota(crowded)}")

    tight = {"Ama": 3, "Beto": 2}
    print(f"three and two: {build_rota(tight)}")
    print(f"a single night: {build_rota({'Dev': 1})}")
    print(f"one person, two nights: {build_rota({'Dev': 2})}")
    print(f"nobody: {build_rota({})}")
    print(f"a zero pledge: {build_rota({'Ama': 0})}")

    assert rota is not None
    assert len(rota) == sum(NIGHTS_AGREED.values())
    assert rota_is_legal(rota)
    assert nights_worked(rota) == {"Ama": 4, "Beto": 3, "Cass": 2, "Dev": 1}
    assert rota[0] == "Ama"
    assert build_rota(crowded) is None
    assert build_rota(tight) == ["Ama", "Beto", "Ama", "Beto", "Ama"]
    assert build_rota({"Dev": 1}) == ["Dev"]
    assert build_rota({"Dev": 2}) is None
    assert build_rota({}) == []
    assert build_rota({"Ama": 0}) == []
    assert rota_is_legal([])
    print("All checks passed.")
```

</details>
---

## Problem 5 — The Grant Round

**The brief.** A community fund holds a reserve. Every project has an **unlock** —
the reserve the fund must already hold before the trustees will sign it off — and
a **payout** that goes back into the reserve when the project finishes. The fund
may back only a few projects in a round, and each one it backs may unlock the
next. Which ones, and what does the reserve close at?

**The data.**

```text
project        unlock   payout
Roof repair         0       30
Kiln rebuild       40       90
Tool shed          25       20
Van service        10       45
Server rack       120      200

opening reserve 15 · three picks allowed
```

**Constraints.** Greedy on payout alone is wrong — the biggest payout may be
locked. Greedy on unlock alone is wrong too — the cheapest unlock may pay almost
nothing. The answer needs both, which is why it is two heaps.

**Answer.** A **min-heap of projects by unlock**, so the cheapest still-locked
project is always next in line, and a **max-heap of the projects already
unlocked**, so the biggest payout is always on top. Each round: move everything
the current reserve now unlocks from the first heap into the second, then take
the biggest payout available. If nothing is unlocked, stop — no further reserve is
coming.

On this data the fund backs **Van service, Kiln rebuild, Server rack** and closes
at **350** from an opening 15. Roof repair pays 30 and is never taken, because
three picks is three picks and the fund can afford to be choosy.

**Signatures.** `grant_round(projects, reserve, picks)`,
`locked_out(projects, reserve, picks)`, `best_single(projects, reserve)`.

**Watch for.** Looping on when the unlocked heap is empty — that is the stopping
condition, and it is not the same as running out of picks. Zero picks returns the
opening reserve untouched. More picks than projects backs all of them and stops.

<details>
<summary>Worked answer — <code>problem-05-grant-round-picks-solution.py</code></summary>

```python
"""problem-05-grant-round-picks-solution.py — which projects a small fund should back.

A community fund holds a reserve. Every project has an unlock — the reserve the
fund must already hold before the trustees will sign it off — and a payout that
goes back into the reserve when the project finishes. The fund may back only a
few projects in a round, and each one it backs may unlock the next.

Two heaps: a min-heap of projects by unlock, so the cheapest to unlock is
always next in line, and a max-heap of the projects already unlocked, so the
biggest payout is always on top.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
# (project, reserve needed to unlock it, payout it returns)
PROJECTS: list[tuple[str, int, int]] = [
    ("Roof repair", 0, 30),
    ("Kiln rebuild", 40, 90),
    ("Tool shed", 25, 20),
    ("Van service", 10, 45),
    ("Server rack", 120, 200),
]

START_RESERVE = 15
ROUND_SIZE = 3


# ---- Your task ----
def grant_round(
    projects: list[tuple[str, int, int]], reserve: int, picks: int
) -> tuple[int, list[str]]:
    """Return the reserve at the end of the round and the projects backed.

    Args:
        projects: (name, unlock, payout) rows, in any order.
        reserve: What the fund holds when the round opens.
        picks: How many projects the round may back at most.

    Returns:
        (closing reserve, project names in the order they were backed). The
        round stops early when nothing is unlocked, so it can back fewer than
        `picks` projects.
    """
    waiting = [(unlock, payout, name) for name, unlock, payout in projects]
    heapq.heapify(waiting)
    unlocked: list[tuple[int, str]] = []
    backed: list[str] = []

    for _ in range(picks):
        while waiting and waiting[0][0] <= reserve:
            _, payout, name = heapq.heappop(waiting)
            heapq.heappush(unlocked, (-payout, name))
        if not unlocked:
            break
        stored, name = heapq.heappop(unlocked)
        reserve += -stored
        backed.append(name)
    return reserve, backed


def locked_out(
    projects: list[tuple[str, int, int]], reserve: int, picks: int
) -> list[str]:
    """Return the projects the round never reached, cheapest unlock first.

    Args:
        projects: (name, unlock, payout) rows.
        reserve: What the fund holds when the round opens.
        picks: How many projects the round may back at most.

    Returns:
        Names, ordered by unlock then by name.
    """
    _, backed = grant_round(projects, reserve, picks)
    left = [row for row in projects if row[0] not in set(backed)]
    return [name for name, _, _ in sorted(left, key=lambda row: (row[1], row[0]))]


def best_single(projects: list[tuple[str, int, int]], reserve: int) -> str | None:
    """Return the one project worth backing if the round could back only one.

    Args:
        projects: (name, unlock, payout) rows.
        reserve: What the fund holds when the round opens.

    Returns:
        The name of the unlocked project with the biggest payout, or None when
        nothing is unlocked. Ties go to the name that sorts earlier.
    """
    _, backed = grant_round(projects, reserve, 1)
    return backed[0] if backed else None


# ---- Self-check ----
if __name__ == "__main__":
    closing, backed = grant_round(PROJECTS, START_RESERVE, ROUND_SIZE)
    print(f"opening reserve: {START_RESERVE}")
    print(f"projects backed: {backed}")
    print(f"closing reserve: {closing}")
    print(f"never reached  : {locked_out(PROJECTS, START_RESERVE, ROUND_SIZE)}")
    print(f"best single pick: {best_single(PROJECTS, START_RESERVE)}")

    print(f"nothing unlocked: {grant_round(PROJECTS, 0, 3)}")
    print(f"no picks allowed: {grant_round(PROJECTS, START_RESERVE, 0)}")
    print(f"no projects: {grant_round([], 50, 3)}")
    print(f"more picks than projects: {grant_round(PROJECTS, START_RESERVE, 99)}")
    print(f"best single on a bare fund: {best_single(PROJECTS, 0)}")

    assert backed == ["Van service", "Kiln rebuild", "Server rack"]
    assert closing == 350
    assert locked_out(PROJECTS, START_RESERVE, ROUND_SIZE) == ["Roof repair", "Tool shed"]
    assert best_single(PROJECTS, START_RESERVE) == "Van service"
    assert grant_round(PROJECTS, 0, 3) == (
        165,
        ["Roof repair", "Van service", "Kiln rebuild"],
    )
    assert grant_round(PROJECTS, START_RESERVE, 0) == (15, [])
    assert grant_round([], 50, 3) == (50, [])
    assert grant_round(PROJECTS, START_RESERVE, 99)[0] == 400
    assert best_single(PROJECTS, 0) == "Roof repair"
    print("All checks passed.")
```

</details>
---

## Problem 6 — The Oven Probe Midline

**The brief.** A bakery's deck oven reports its crown temperature every few
minutes. The baker wants the **midline after every reading** — the middle value of
everything seen so far. With an even number of readings there are two middle
values; this bakery wants the **lower** of the two, plus **how far apart they
are**, because a wide gap means the oven is swinging.

**The data.** 214, 231, 205, 240, 226, 219, 236, 208 degrees.

**Constraints.** The midline is wanted after *every* reading, so re-sorting the
history each time costs `O(n² log n)` over the run — that is the alternative to
name and reject.

**Answer.** Two heaps holding the two halves. The **lower half in a max-heap**, so
its biggest value is on top; the **upper half in a min-heap**, so its smallest is
on top. The two tops are the two middle readings — the midline is the lower one,
the spread is their difference. After every push, rebalance so the halves differ
in size by at most one; that invariant is what the whole structure rests on.

Insert and rebalance are `O(log n)`; reading the midline is `O(1)`.

**Signatures.** `Midline` with `add`, `midline`, `spread`;
`midline_trace(readings)`, `widest_swing(readings)`.

**Watch for.** Pushing straight onto the half you think it belongs in without
comparing against the tops — the halves stop being halves and the answer drifts
without ever crashing. Rebalancing by size alone, ignoring the values, has the
same symptom. Before any reading the midline is `None` and the spread is `0`; four
identical readings have a spread of `0`, which is a real answer and not a
degenerate one.

<details>
<summary>Worked answer — <code>problem-06-oven-probe-midline-solution.py</code></summary>

```python
"""problem-06-oven-probe-midline-solution.py — the running midline of a deck oven.

A bakery's deck oven reports its crown temperature every few minutes. The baker
wants the midline after every reading: the middle value of everything seen so
far. With an even number of readings there are two middle values, and this
bakery wants the lower of the two, plus how far apart they are — a wide gap
means the oven is swinging.

Two heaps hold the two halves. The lower half sits in a max-heap so its biggest
value is on top; the upper half sits in a min-heap so its smallest value is on
top. The two tops are the two middle readings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
# Crown temperature in degrees Celsius, in the order the probe reported them.
READINGS: list[int] = [214, 231, 205, 240, 226, 219, 236, 208]


# ---- Your task ----
class Midline:
    """A running lower-median over readings that arrive one at a time."""

    def __init__(self) -> None:
        """Start with both halves empty."""
        self._lower: list[int] = []  # max-heap, values stored negated
        self._upper: list[int] = []  # min-heap, values stored as they are

    def __len__(self) -> int:
        """Return how many readings have been added."""
        return len(self._lower) + len(self._upper)

    def add(self, reading: int) -> None:
        """Add one reading and restore the two-halves invariant.

        Args:
            reading: The temperature to add.
        """
        if not self._lower or reading <= -self._lower[0]:
            heapq.heappush(self._lower, -reading)
        else:
            heapq.heappush(self._upper, reading)

        if len(self._lower) > len(self._upper) + 1:
            heapq.heappush(self._upper, -heapq.heappop(self._lower))
        elif len(self._upper) > len(self._lower):
            heapq.heappush(self._lower, -heapq.heappop(self._upper))

    def midline(self) -> int | None:
        """Return the lower of the two middle readings.

        Returns:
            The middle reading when the count is odd, the lower of the two
            middles when it is even, or None before anything is added.
        """
        if not self._lower:
            return None
        return -self._lower[0]

    def spread(self) -> int:
        """Return the distance between the two middle readings.

        Returns:
            0 when the count is odd or empty — there is only one middle to
            report. Otherwise the upper middle minus the lower middle, which
            is never negative.
        """
        if not self._upper or len(self._lower) != len(self._upper):
            return 0
        return self._upper[0] - -self._lower[0]


def midline_trace(readings: list[int]) -> list[tuple[int, int, int]]:
    """Return the midline after each reading in turn.

    Args:
        readings: Temperatures in the order the probe reported them.

    Returns:
        (reading count, lower middle, spread) after each reading.
    """
    probe = Midline()
    trace = []
    for reading in readings:
        probe.add(reading)
        trace.append((len(probe), probe.midline(), probe.spread()))
    return trace


def widest_swing(readings: list[int]) -> tuple[int, int] | None:
    """Return the reading count at which the two middles were furthest apart.

    Args:
        readings: Temperatures in the order the probe reported them.

    Returns:
        (reading count, spread), or None when no even count ever occurred.
        Ties go to the earliest count.
    """
    best = None
    for count, _, spread in midline_trace(readings):
        if count % 2 == 0 and (best is None or spread > best[1]):
            best = (count, spread)
    return best


# ---- Self-check ----
if __name__ == "__main__":
    print("midline after each reading:")
    for (count, middle, spread), reading in zip(midline_trace(READINGS), READINGS):
        print(f"  after {count}: newest {reading}C, midline {middle}C, spread {spread}C")

    print(f"widest swing: {widest_swing(READINGS)}")

    probe = Midline()
    print(f"midline before anything: {probe.midline()}")
    print(f"spread before anything: {probe.spread()}")
    probe.add(300)
    print(f"one reading: midline {probe.midline()}, spread {probe.spread()}")

    flat = Midline()
    for value in (200, 200, 200, 200):
        flat.add(value)
    print(f"four identical readings: midline {flat.midline()}, spread {flat.spread()}")

    falling = midline_trace([9, 7, 5, 3, 1])
    print(f"a falling probe: {falling}")

    trace = midline_trace(READINGS)
    assert trace[0] == (1, 214, 0)
    assert trace[1] == (2, 214, 17)
    assert trace[2] == (3, 214, 0)
    assert trace[-1] == (8, 219, 7)
    assert widest_swing(READINGS) == (2, 17)
    assert Midline().midline() is None
    assert Midline().spread() == 0
    assert flat.midline() == 200 and flat.spread() == 0
    assert falling[-1] == (5, 5, 0)
    assert len(trace) == len(READINGS)
    print("All checks passed.")
```

</details>
---

## Rubric (5 axes, 4 points each)

| Axis | What "great" looks like |
|------|--------------------------|
| Frame the problem | The 30-second memo names the sub-shape — bounded top-k, repeated merge, k-way merge, spacing scheduler, two-heap unlock, two-heap statistic — and the invariant that goes with it. |
| Reason about options | Four to six bullets of algorithm before any code is written, including the alternative you rejected. |
| Assemble the solution | Idiomatic Python; `heapq` operations only, no hand-written sift code; type hints on every function. |
| Measure it | A trace on at least one example, and one common bug named and avoided. |
| Evaluate the cost | Time, space, best/average/worst, the trade-off, and the improvement — with the sentence that defends the heap against sorting. |

Twenty points per problem, 120 for the set. Score yourself honestly; the number
is only useful if it is true.

---

## How to submit

Commit your write-ups under `frame-writeups/c2-week-08/homework/`, one file per
problem:

```
frame-writeups/c2-week-08/homework/
├── problem-1-dawn-chorus-shortlist.md
├── problem-2-splice-drum-tape.md
├── problem-3-germination-grid-rank.md
├── problem-4-night-rota-spacing.md
├── problem-5-grant-round-picks.md
└── problem-6-oven-probe-midline.md
```

Each file is 100–200 lines: the five FRAME sections plus a five-line memo at the
top. The code is part of the Assemble section, not a separate file.

When the set is done, push and move on to the
[mini-project](../mini-project/README.md).

---

## Time budget

| Problem | Solve | Write-up | Total |
|---------|------:|---------:|------:|
| 1 — Dawn Chorus Shortlist | 25 min | 10 min | 35 min |
| 2 — Splice Drum Tape | 20 min | 10 min | 30 min |
| 3 — Germination Grid Rank | 40 min | 10 min | 50 min |
| 4 — Night Rota | 35 min | 15 min | 50 min |
| 5 — Grant Round | 45 min | 15 min | 60 min |
| 6 — Oven Probe Midline | 30 min | 15 min | 45 min |

About four and a half hours of work, and the write-ups are the half that Mock #2
actually grades.
