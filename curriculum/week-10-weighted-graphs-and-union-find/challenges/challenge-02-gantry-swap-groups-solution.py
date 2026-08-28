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
