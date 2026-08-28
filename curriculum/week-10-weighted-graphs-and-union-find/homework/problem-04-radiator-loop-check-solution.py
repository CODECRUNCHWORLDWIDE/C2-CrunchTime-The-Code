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
