# Challenge 2 — The Gantry Swap Groups

> Topic: disjoint set union · Lecture: [3](../lecture-notes/03-union-find-and-the-dsu-triggers.md) · Difficulty: Medium · Target time: 60 minutes including the FRAME write-up · Why this one: it is the problem where union-find stops being a connectivity trick and becomes a way of deciding what is *permitted*.

## The Brief

A quarry loads dressed stone onto a rail of numbered slots. Some pairs of slots
share a travelling gantry, so the blocks in those two slots can be swapped as
often as you like. Share a gantry with a slot that shares a gantry with a third,
and all three contents can be shuffled freely between them.

The loader wants the heaviest stone nearest the locomotive, which is slot 0. It
cannot move a block into a slot no gantry reaches — so the answer is not "sort
the rail". It is: **sort inside each reachable group, and leave the groups where
they are.**

That distinction is the whole problem. A learner who reaches for a sort produces
an arrangement the gantries cannot physically build.

## Starter

The worked answer on this page carries the blocks, the gantry pairs, and the
self-checks you must satisfy.

```text
slot   0        1         2       3         4       5       6       7
block  Ashlar   Bullnose  Coping  Dogtooth  Edging  Fillet  Gablet  Header
tonnes 4        9         4       7         2       9       1       6

gantries: (0,3) (3,5) (0,2) (1,4) (6,1) (2,2)
```

`(2, 2)` is deliberate: a gantry that reaches one slot moves nothing, and joining
a slot to itself must not change the group count.

## Requirements

1. A `Rail` class implementing disjoint set union with **both** optimisations:
   path compression in `group_of`, union by rank in `join`.
2. `join(left, right)` returns whether a merge actually happened, and the live
   `groups` count stays correct as merges occur.
3. `gantry_groups(...)` returns the slots each group covers.
4. `best_loading(...)` returns the arrangement as block labels in slot order:
   within each group, the heaviest block goes to that group's lowest-numbered
   slot.
5. The output shows which slots **moved**, because the claim being made is about
   what the gantries can physically do.

## Constraints

- **A block may only move within its group.** The arrangement must be reachable
  by repeated swaps along gantry pairs, and your write-up must say why sorting
  within a group is always reachable — any permutation of a connected group is,
  and that is the fact the whole solution rests on.
- **Ties in weight are settled by label**, so the answer is one arrangement and
  not a family of them. Bullnose and Fillet are both 9t; the contract decides
  which lands where.
- **Self-joins are legal input** and must not decrement the group count.
- Both optimisations are required. Either alone is correct but slower; the
  write-up must say what each one buys.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python challenge-02-gantry-swap-groups.py
gantry groups
  [0, 2, 3, 5]
  [1, 4, 6]
  [7]

loading, heaviest nearest the locomotive
  slot 0: Ashlar    -> Fillet     9t   moved
  slot 1: Bullnose  -> Bullnose   9t
  slot 2: Coping    -> Dogtooth   7t   moved
  slot 3: Dogtooth  -> Ashlar     4t   moved
  slot 4: Edging    -> Edging     2t
  slot 5: Fillet    -> Coping     4t   moved
  slot 6: Gablet    -> Gablet     1t
  slot 7: Header    -> Header     6t

arrangement: ['Fillet', 'Bullnose', 'Dogtooth', 'Ashlar', 'Edging', 'Coping', 'Gablet', 'Header']
groups: 3
All checks passed.
```

Slot 1 is the row to look at. Bullnose is 9 tonnes and it does **not** move,
because its group is `{1, 4, 6}` and it is already the heaviest in it sitting at
the group's lowest slot. A rail-wide sort would have moved it, and would have
been wrong.

Slot 0 taking Fillet is the mirror: Fillet is in group `{0, 2, 3, 5}`, so it is
allowed to travel to slot 0 even though it starts five slots away.

## Steps

1. Read the self-checks. They are the spec.
2. Write the memo: name the structure, and name what makes this union-find rather
   than a graph traversal — you never need the path, only the membership.
3. Implement `Rail` with both optimisations. Test `(2, 2)` early.
4. Build the groups, then sort inside each one and write the arrangement back.
5. Prove to yourself that the arrangement is reachable: pick one moved block and
   name the gantry sequence that carries it.
6. Write the FRAME pass, with the cost of union-find stated honestly — near
   constant per operation, not constant.

## The Solution

```python
"""challenge-02-gantry-swap-groups-solution.py — sort inside what the gantries can reach.

A quarry loads dressed stone onto a rail of numbered slots. Some pairs of
slots share a travelling gantry, so the blocks in those two slots can be
swapped as often as you like. Share a gantry with a slot that shares a gantry
with a third, and all three contents can be shuffled freely between them.

The loader wants the heaviest stone nearest the locomotive, which is slot 0.
It cannot move a block into a slot no gantry reaches, so the answer is: sort
inside each reachable group, and leave the groups where they are.

  gantry_groups   — the slots each gantry group covers
  best_loading    — the arrangement, as block labels in slot order

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
# (block label, tonnes) for the block sitting in each slot, slot 0 first
Block = tuple[str, int]

BLOCKS: list[Block] = [
    ("Ashlar", 4),
    ("Bullnose", 9),
    ("Coping", 4),
    ("Dogtooth", 7),
    ("Edging", 2),
    ("Fillet", 9),
    ("Gablet", 1),
    ("Header", 6),
]

# (slot, slot) pairs that share a travelling gantry
GANTRIES: list[tuple[int, int]] = [
    (0, 3),
    (3, 5),
    (0, 2),
    (1, 4),
    (6, 1),
    (2, 2),   # a gantry that reaches one slot moves nothing
]


# ---- Your task ----
class Rail:
    """Slots grouped by what a gantry can reach, with compression and rank."""

    def __init__(self, slot_count: int) -> None:
        """Start every slot in a group of its own.

        Args:
            slot_count: How many slots the rail has, numbered from 0.
        """
        self.parent: list[int] = list(range(slot_count))
        self.rank: list[int] = [0] * slot_count
        self.groups: int = slot_count

    def group_of(self, slot: int) -> int:
        """Return the slot that names this slot's group, flattening on the way.

        Args:
            slot: The slot to look up.

        Returns:
            The root slot. Two slots are in one group exactly when this
            returns the same number for both.
        """
        root = slot
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[slot] != root:
            self.parent[slot], slot = root, self.parent[slot]
        return root

    def join(self, left: int, right: int) -> bool:
        """Merge two groups, shallower tree under deeper.

        Args:
            left: One slot.
            right: The other slot.

        Returns:
            True when the two groups were apart and are now one. False when
            they were already the same group, which includes a gantry whose
            two slots are the same slot.
        """
        left_root, right_root = self.group_of(left), self.group_of(right)
        if left_root == right_root:
            return False
        if self.rank[left_root] < self.rank[right_root]:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        if self.rank[left_root] == self.rank[right_root]:
            self.rank[left_root] += 1
        self.groups -= 1
        return True


def gantry_groups(slot_count: int, gantries: list[tuple[int, int]]) -> list[list[int]]:
    """Return the slots each gantry group covers.

    Args:
        slot_count: How many slots the rail has, numbered from 0.
        gantries: Every gantry, as a pair of slots it reaches.

    Returns:
        A list of groups, each a sorted list of slot numbers, ordered by the
        group's lowest slot. A slot no gantry reaches is a group of one.
    """
    rail = Rail(slot_count)
    for left, right in gantries:
        rail.join(left, right)
    grouped: dict[int, list[int]] = {}
    for slot in range(slot_count):
        grouped.setdefault(rail.group_of(slot), []).append(slot)
    return sorted(grouped.values())


def best_loading(blocks: list[Block], gantries: list[tuple[int, int]]) -> tuple[list[str], int]:
    """Return the heaviest-first arrangement the gantries allow.

    Args:
        blocks: The block in each slot, as (label, tonnes), slot 0 first.
        gantries: Every gantry, as a pair of slots it reaches.

    Returns:
        (labels in slot order, number of gantry groups). Inside a group the
        blocks go heaviest first; two blocks of the same weight go in label
        order A to Z, so the answer is the same on every run.

    Raises:
        IndexError: If a gantry names a slot the rail does not have.
    """
    groups = gantry_groups(len(blocks), gantries)
    arrangement = [""] * len(blocks)
    for slots in groups:
        picked = sorted((blocks[slot] for slot in slots), key=lambda b: (-b[1], b[0]))
        for slot, (label, _) in zip(slots, picked):
            arrangement[slot] = label
    return arrangement, len(groups)


def loading_rows(blocks: list[Block], gantries: list[tuple[int, int]]) -> list[str]:
    """Return one printable row per slot, before beside after.

    Args:
        blocks: The block in each slot, as (label, tonnes), slot 0 first.
        gantries: Every gantry, as a pair of slots it reaches.

    Returns:
        Rows in slot order. A slot whose block changed is marked "moved".
    """
    arrangement, _ = best_loading(blocks, gantries)
    tonnes = dict(blocks)
    rows = []
    for slot, (was, _) in enumerate(blocks):
        now = arrangement[slot]
        flag = "" if now == was else "   moved"
        rows.append(f"  slot {slot}: {was:<9} -> {now:<9} {tonnes[now]:2d}t{flag}")
    return rows


# ---- Self-check ----
if __name__ == "__main__":
    print("gantry groups")
    for group in gantry_groups(len(BLOCKS), GANTRIES):
        print(f"  {group}")

    print()
    print("loading, heaviest nearest the locomotive")
    for row in loading_rows(BLOCKS, GANTRIES):
        print(row)

    arrangement, groups = best_loading(BLOCKS, GANTRIES)
    print()
    print(f"arrangement: {arrangement}")
    print(f"groups: {groups}")

    assert gantry_groups(len(BLOCKS), GANTRIES) == [[0, 2, 3, 5], [1, 4, 6], [7]]
    assert groups == 3
    # Ashlar and Coping both weigh 4t, so the label decides which slot each takes.
    assert arrangement == [
        "Fillet",
        "Bullnose",
        "Dogtooth",
        "Ashlar",
        "Edging",
        "Coping",
        "Gablet",
        "Header",
    ]

    untouched, alone = best_loading(BLOCKS, [])
    assert untouched == [label for label, _ in BLOCKS]
    assert alone == len(BLOCKS)
    assert best_loading([("Solo", 3)], [(0, 0)]) == (["Solo"], 1)
    print("All checks passed.")
```

`group_of` compresses on the way back up rather than in a second pass, which is
why the loop reassigns `self.parent[slot]` and `slot` together. Read that line
slowly; it is the shortest correct path compression and the most commonly
mangled one.

## Run it

Download the solution beside this page and run it:

```bash
python challenge-02-gantry-swap-groups.py
```

No third-party packages, no arguments, no input. It prints the slot-by-slot
arrangement, the group count, and then `All checks passed.`

## Common bugs to catch

- **Sorting the whole rail.** Symptom: a tidy descending arrangement that the
  gantries cannot build. The heaviest block is not allowed to reach slot 0 unless
  a gantry path exists.
- **Recursion in `group_of`.** Symptom: fine on eight slots, `RecursionError` on
  a long chain. Iterate.
- **Compressing without rank, or ranking without compression.** Symptom: correct
  answers, degraded trees. The write-up must say what each buys — rank keeps the
  tree shallow, compression flattens what is already walked.
- **Decrementing the group count on a self-join.** Symptom: `groups` reports 2
  where the answer is 3. `join` must report whether it actually merged.
- **An unstated tie-break on equal weights.** Symptom: two 9-tonne blocks and an
  arrangement that flips depending on sort stability.

## Acceptance checklist

- [ ] Path compression and union by rank both implemented.
- [ ] `join(2, 2)` returns False and leaves `groups` unchanged.
- [ ] Group count is 3 for the given data.
- [ ] Slot 1 does not move; slot 0 receives Fillet.
- [ ] The write-up names one moved block and the gantry sequence that carries it.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Add a gantry joining 4 and 5 and predict the new arrangement **before**
  running it. Two groups become one; say which blocks move and check.
- Replace union by rank with union by size and say what changes. Both bound the
  tree height; one of them tells you something you might want to report.
- Answer "how many slots are in the same group as slot 6?" without building the
  group lists. If your structure cannot, say what you would add and what it costs
  on every `join`.
