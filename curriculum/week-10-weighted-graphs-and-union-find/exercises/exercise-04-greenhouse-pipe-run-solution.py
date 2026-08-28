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
