"""exercise-03-mooring-chain-groups-solution.py — union-find on a boatyard's moorings.

A boatyard has twelve numbered berths. Over a morning the crew shackle pairs
of berths together with chain. Shackle 3 to 7, and anything already chained
to 3 is now chained to 7 as well — the chain does not care how it got there.

Three things to report:

  chain_counts  — how many separate chains exist after each shackle
  chain_roster  — the finished chains, as sorted lists of berth numbers
  parent_trail  — the parent array before and after one find, so you can see
                  path compression flatten it

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
BERTH_COUNT = 12

# (berth, berth) pairs, in the order the crew shackled them
SHACKLES: list[tuple[int, int]] = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),   # closes a loop; nothing new is joined
    (5, 6),
    (7, 8),
    (6, 7),
    (9, 10),
    (10, 9),  # the same shackle, done twice
    (4, 5),
]


# ---- Your task ----
class Moorings:
    """Berths grouped into chains, with path compression and union by rank.

    Every berth starts alone. `join` shackles two berths together. `chain_of`
    reports which chain a berth belongs to, named after its root berth.
    """

    def __init__(self, berth_count: int) -> None:
        """Start every berth in a chain of its own.

        Args:
            berth_count: How many berths the yard has, numbered from 0.
        """
        self.parent: list[int] = list(range(berth_count))
        self.rank: list[int] = [0] * berth_count
        self.chains: int = berth_count

    def chain_of(self, berth: int) -> int:
        """Return the root berth of this berth's chain, flattening on the way.

        Args:
            berth: The berth to look up.

        Returns:
            The root berth. Two berths are on the same chain exactly when
            this returns the same number for both.
        """
        root = berth
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[berth] != root:      # path compression, second pass
            self.parent[berth], berth = root, self.parent[berth]
        return root

    def join(self, left: int, right: int) -> bool:
        """Shackle two berths together, smaller tree under larger.

        Args:
            left: One berth.
            right: The other berth.

        Returns:
            True when this shackle joined two chains that were apart.
            False when the two berths were already on one chain, which means
            the shackle closed a loop and changed nothing.
        """
        left_root, right_root = self.chain_of(left), self.chain_of(right)
        if left_root == right_root:
            return False
        if self.rank[left_root] < self.rank[right_root]:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        if self.rank[left_root] == self.rank[right_root]:
            self.rank[left_root] += 1
        self.chains -= 1
        return True


def chain_counts(berth_count: int, shackles: list[tuple[int, int]]) -> list[int]:
    """Return how many separate chains remain after each shackle.

    Args:
        berth_count: How many berths the yard has, numbered from 0.
        shackles: The pairs of berths, in the order they were shackled.

    Returns:
        One number per shackle. A shackle that closed a loop repeats the
        previous number, which is how a loop shows up in the report.
    """
    moorings = Moorings(berth_count)
    counts = []
    for left, right in shackles:
        moorings.join(left, right)
        counts.append(moorings.chains)
    return counts


def chain_roster(berth_count: int, shackles: list[tuple[int, int]]) -> list[list[int]]:
    """Return the finished chains, each as a sorted list of berth numbers.

    Args:
        berth_count: How many berths the yard has, numbered from 0.
        shackles: The pairs of berths, in the order they were shackled.

    Returns:
        A list of chains, sorted by each chain's smallest berth. A berth that
        was never shackled to anything is a chain of one and is included.
    """
    moorings = Moorings(berth_count)
    for left, right in shackles:
        moorings.join(left, right)
    grouped: dict[int, list[int]] = {}
    for berth in range(berth_count):
        grouped.setdefault(moorings.chain_of(berth), []).append(berth)
    return sorted(grouped.values())


def parent_trail(berth_count: int, shackles: list[tuple[int, int]], berth: int) -> tuple[list[int], list[int]]:
    """Return the parent array either side of one `chain_of` call.

    Args:
        berth_count: How many berths the yard has, numbered from 0.
        shackles: The pairs of berths, in the order they were shackled.
        berth: The berth to look up once, after all the shackling.

    Returns:
        (before, after) copies of the parent array. Any position that changed
        was shortened by path compression.
    """
    moorings = Moorings(berth_count)

    def plain_root(start: int) -> int:
        """Walk to the root without flattening anything on the way."""
        while moorings.parent[start] != start:
            start = moorings.parent[start]
        return start

    for left, right in shackles:
        left_root, right_root = plain_root(left), plain_root(right)
        if left_root != right_root:            # no rank either, so the tree stays deep
            moorings.parent[left_root] = right_root
            moorings.chains -= 1
    before = list(moorings.parent)
    moorings.chain_of(berth)
    return before, list(moorings.parent)


# ---- Self-check ----
if __name__ == "__main__":
    print("chains left after each shackle")
    for (left, right), left_over in zip(SHACKLES, chain_counts(BERTH_COUNT, SHACKLES)):
        print(f"  shackle {left:2d}-{right:<2d} -> {left_over} chains")

    print()
    print("finished chains")
    for chain in chain_roster(BERTH_COUNT, SHACKLES):
        print(f"  {chain}")

    before, after = parent_trail(BERTH_COUNT, SHACKLES, 0)
    print()
    print(f"parents before chain_of(0): {before}")
    print(f"parents after  chain_of(0): {after}")

    assert chain_counts(BERTH_COUNT, SHACKLES) == [11, 10, 9, 9, 8, 7, 6, 5, 5, 4]
    assert chain_roster(BERTH_COUNT, SHACKLES) == [
        [0, 1, 2, 3],
        [4, 5, 6, 7, 8],
        [9, 10],
        [11],
    ]

    moorings = Moorings(4)
    assert moorings.join(0, 1) is True
    assert moorings.join(1, 0) is False        # already one chain
    assert moorings.chains == 3
    assert moorings.chain_of(0) == moorings.chain_of(1)
    assert moorings.chain_of(2) != moorings.chain_of(3)
    assert before != after                     # the find really did flatten something
    print("All checks passed.")
