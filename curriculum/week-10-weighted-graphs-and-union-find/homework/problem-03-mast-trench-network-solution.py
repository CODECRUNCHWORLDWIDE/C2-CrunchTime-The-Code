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
