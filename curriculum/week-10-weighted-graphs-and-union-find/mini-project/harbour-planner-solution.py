"""harbour-planner-solution.py — the harbour utilities planner.

One report for a harbour board, built from two different questions about the
same set of quays.

  The taxi question is "how long from here to there?", and it is answered by
  growing outwards from the ferry slip, always finishing the nearest unfinished
  quay next. That is a shortest-path search with a heap and a settled set.

  The cable question is "what is the cheapest set of trenches that leaves
  nobody out?", and it is answered by walking the priced trenches from
  cheapest to dearest and keeping any trench that joins two quays not already
  joined. That is a minimum spanning tree, and the "already joined?" test is
  a union-find.

The report is printed to stdout in five parts. Nothing is read from the
keyboard, nothing is written to disk, and the whole thing runs on the
standard library.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
Run = tuple[str, str, int]      # (quay, quay, minutes for the water taxi)
Trench = tuple[str, str, int]   # (quay, quay, cost in thousands of pounds)

QUAYS: list[str] = [
    "Ferry Slip",
    "Bait Wharf",
    "Chandlery Steps",
    "Dry Dock",
    "Eel Stage",
    "Fish Quay",
    "Gull Rock",
]

TAXI_RUNS: list[Run] = [
    ("Ferry Slip", "Bait Wharf", 4),
    ("Ferry Slip", "Chandlery Steps", 9),
    ("Bait Wharf", "Chandlery Steps", 3),
    ("Bait Wharf", "Dry Dock", 11),
    ("Chandlery Steps", "Dry Dock", 5),
    ("Dry Dock", "Eel Stage", 6),
    ("Chandlery Steps", "Fish Quay", 14),
    ("Eel Stage", "Fish Quay", 4),
]

CABLE_TRENCHES: list[Trench] = [
    ("Ferry Slip", "Bait Wharf", 7),
    ("Ferry Slip", "Chandlery Steps", 12),
    ("Bait Wharf", "Chandlery Steps", 4),
    ("Bait Wharf", "Dry Dock", 9),
    ("Chandlery Steps", "Dry Dock", 6),
    ("Dry Dock", "Eel Stage", 8),
    ("Eel Stage", "Fish Quay", 5),
    ("Chandlery Steps", "Fish Quay", 11),
    ("Fish Quay", "Gull Rock", 15),
]

# The board's first draft left the island off the cable plan entirely.
FIRST_DRAFT: list[Trench] = [t for t in CABLE_TRENCHES if "Gull Rock" not in t[:2]]


# ---- Part one: the water taxi ----
def build_water(runs: list[Run]) -> dict[str, list[tuple[str, int]]]:
    """Return the taxi runs keyed by quay, both ways round.

    Args:
        runs: Every water-taxi run, as (quay, quay, minutes).

    Returns:
        A dict where water[quay] is a list of (other quay, minutes).

    Raises:
        ValueError: If any run takes negative minutes. A negative run would
            break the settled-set rule this planner depends on, so it is
            refused at the door rather than producing a quiet wrong answer.
    """
    water: dict[str, list[tuple[str, int]]] = {}
    for here, there, minutes in runs:
        if minutes < 0:
            raise ValueError(f"a run cannot take negative minutes: {here} to {there}")
        water.setdefault(here, []).append((there, minutes))
        water.setdefault(there, []).append((here, minutes))
    return water


def run_minutes(runs: list[Run], start: str) -> dict[str, int]:
    """Return the shortest taxi time from start to every quay it can reach.

    Args:
        runs: Every water-taxi run, as (quay, quay, minutes).
        start: The quay the taxi waits at.

    Returns:
        A dict of quay -> minutes. A quay no run reaches is left out.
    """
    water = build_water(runs)
    best: dict[str, int] = {start: 0}
    settled: set[str] = set()
    queue: list[tuple[int, str]] = [(0, start)]

    while queue:
        so_far, quay = heapq.heappop(queue)
        if quay in settled:
            continue
        settled.add(quay)
        for other, minutes in water.get(quay, []):
            total = so_far + minutes
            if total < best.get(other, float("inf")):
                best[other] = total
                heapq.heappush(queue, (total, other))

    return best


def longest_wait(runs: list[Run], quays: list[str], start: str) -> tuple[str, int]:
    """Return the reachable quay that waits longest for a taxi.

    Args:
        runs: Every water-taxi run, as (quay, quay, minutes).
        quays: Every quay on the harbour board's list.
        start: The quay the taxi waits at.

    Returns:
        (quay, minutes), ties broken by quay name A to Z. Quays the taxi
        cannot reach are ignored here and reported separately.
    """
    minutes = run_minutes(runs, start)
    reachable = [quay for quay in quays if quay in minutes]
    latest, name = min((-minutes[quay], quay) for quay in reachable)
    return name, -latest


def stranded(runs: list[Run], quays: list[str], start: str) -> list[str]:
    """Return the quays no taxi run reaches, in name order.

    Args:
        runs: Every water-taxi run, as (quay, quay, minutes).
        quays: Every quay on the harbour board's list.
        start: The quay the taxi waits at.

    Returns:
        A sorted list of quay names, empty when the taxi reaches everything.
    """
    minutes = run_minutes(runs, start)
    return sorted(quay for quay in quays if quay not in minutes)


# ---- Part two: the cable ring ----
class Harbour:
    """Quays grouped into cabled networks, with path compression and rank."""

    def __init__(self, quays: list[str]) -> None:
        """Start every quay in a network of its own.

        Args:
            quays: Every quay on the harbour board's list.
        """
        self.parent: dict[str, str] = {quay: quay for quay in quays}
        self.rank: dict[str, int] = {quay: 0 for quay in quays}
        self.networks: int = len(quays)

    def network_of(self, quay: str) -> str:
        """Return the quay that names this quay's network.

        Args:
            quay: The quay to look up.

        Returns:
            The root quay, flattening the path on the way back.
        """
        root = quay
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[quay] != root:
            self.parent[quay], quay = root, self.parent[quay]
        return root

    def join(self, left: str, right: str) -> bool:
        """Cable two networks together, shallower tree under deeper.

        Args:
            left: One quay.
            right: The other quay.

        Returns:
            True when the trench joined two networks that were apart. False
            when both quays were already cabled together.
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


def cheapest_cable(
    quays: list[str], trenches: list[Trench]
) -> tuple[int, list[Trench], int]:
    """Return the cheapest set of trenches that cables every quay together.

    Args:
        quays: Every quay on the harbour board's list.
        trenches: Every trench the surveyor priced.

    Returns:
        (total cost, trenches in the order accepted, networks left over).
        The third number is 1 when the plan reaches every quay and more when
        it does not, so the caller can report the shortfall rather than being
        handed a plan that quietly leaves somebody dark.
    """
    harbour = Harbour(quays)
    chosen: list[Trench] = []
    total = 0
    for left, right, cost in sorted(trenches, key=lambda t: (t[2], t[0], t[1])):
        if harbour.join(left, right):
            chosen.append((left, right, cost))
            total += cost
            if len(chosen) == len(quays) - 1:
                break
    return total, chosen, harbour.networks


def dark_networks(quays: list[str], trenches: list[Trench]) -> list[list[str]]:
    """Return the separate networks a trench plan leaves behind.

    Args:
        quays: Every quay on the harbour board's list.
        trenches: Every trench the surveyor priced.

    Returns:
        A list of networks, each a sorted list of quay names, ordered by each
        network's first name.
    """
    harbour = Harbour(quays)
    for left, right, _ in trenches:
        harbour.join(left, right)
    grouped: dict[str, list[str]] = {}
    for quay in quays:
        grouped.setdefault(harbour.network_of(quay), []).append(quay)
    return sorted(sorted(group) for group in grouped.values())


# ---- Part three: the report ----
def report(quays: list[str], runs: list[Run], trenches: list[Trench], start: str) -> list[str]:
    """Return the harbour board's report, one line per list entry.

    Args:
        quays: Every quay on the harbour board's list.
        runs: Every water-taxi run, as (quay, quay, minutes).
        trenches: Every trench the surveyor priced.
        start: The quay the taxi waits at.

    Returns:
        The finished report as a list of lines, with no trailing blank line.
    """
    lines = [f"HARBOUR UTILITIES PLAN - taxi from {start}", ""]

    lines.append("1. Water-taxi minutes")
    minutes = run_minutes(runs, start)
    for wait, quay in sorted((m, q) for q, m in minutes.items()):
        lines.append(f"   {wait:4d}  {quay}")

    lines.append("")
    lines.append("2. Worst wait and who is cut off")
    quay, wait = longest_wait(runs, quays, start)
    lines.append(f"   longest wait: {quay} at {wait} minutes")
    cut_off = stranded(runs, quays, start)
    lines.append(f"   no taxi run:  {', '.join(cut_off) if cut_off else 'nobody'}")

    lines.append("")
    lines.append("3. Cheapest cable ring")
    total, chosen, networks = cheapest_cable(quays, trenches)
    for left, right, cost in chosen:
        lines.append(f"   {cost:4d}k  {left} - {right}")
    lines.append(f"   total {total}k over {len(chosen)} trenches")

    lines.append("")
    lines.append("4. Does the cable reach everybody?")
    if networks == 1:
        lines.append("   yes - one network")
    else:
        lines.append(f"   no - {networks} separate networks:")
        for group in dark_networks(quays, trenches):
            lines.append(f"     {', '.join(group)}")

    lines.append("")
    lines.append("5. Data check")
    try:
        run_minutes([*runs, ("Gull Rock", "Ferry Slip", -3)], start)
    except ValueError as problem:
        lines.append(f"   refused: {problem}")
    else:                                    # pragma: no cover - the guard must fire
        lines.append("   a negative run slipped through, which is a bug")
    return lines


# ---- Self-check ----
if __name__ == "__main__":
    for line in report(QUAYS, TAXI_RUNS, CABLE_TRENCHES, "Ferry Slip"):
        print(line)
    print()
    print("FIRST DRAFT, island left off the cable plan")
    for line in report(QUAYS, TAXI_RUNS, FIRST_DRAFT, "Ferry Slip")[-6:]:
        print(line)

    minutes = run_minutes(TAXI_RUNS, "Ferry Slip")
    assert minutes["Chandlery Steps"] == 7      # 4 + 3 beats the direct 9
    assert minutes["Dry Dock"] == 12            # 7 + 5 beats 4 + 11
    assert minutes["Fish Quay"] == 21           # 7 + 14 beats 12 + 6 + 4
    assert "Gull Rock" not in minutes
    assert longest_wait(TAXI_RUNS, QUAYS, "Ferry Slip") == ("Fish Quay", 21)
    assert stranded(TAXI_RUNS, QUAYS, "Ferry Slip") == ["Gull Rock"]

    total, chosen, networks = cheapest_cable(QUAYS, CABLE_TRENCHES)
    assert total == 45
    assert networks == 1
    assert len(chosen) == len(QUAYS) - 1
    assert chosen[0] == ("Bait Wharf", "Chandlery Steps", 4)
    assert chosen[-1] == ("Fish Quay", "Gull Rock", 15)

    draft_total, draft_chosen, draft_networks = cheapest_cable(QUAYS, FIRST_DRAFT)
    assert draft_networks == 2
    assert draft_total == 30
    assert dark_networks(QUAYS, FIRST_DRAFT)[-1] == ["Gull Rock"]

    try:
        run_minutes([("Ferry Slip", "Bait Wharf", -1)], "Ferry Slip")
    except ValueError as problem:
        assert "negative" in str(problem)
    else:                                    # pragma: no cover - the guard must fire
        raise AssertionError("a negative run should have been refused")
    print("All checks passed.")
