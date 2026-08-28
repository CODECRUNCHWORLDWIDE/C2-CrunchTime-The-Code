"""growth_lab.py — the Week 0 cost table, counted rather than timed.

A stopwatch tells you about your laptop. A counter tells you about the data
structure. Everything in here counts the work itself: elements copied,
elements shifted, comparisons made, probes taken, characters copied.

Because nothing is timed, this table is the same on every machine, and the
growth column is the whole point. Double the size of the job and watch what
the count does. Roughly doubling means linear. Roughly quadrupling means
quadratic. Staying put means constant.

Run it, and keep the table:

    python growth_lab.py > COST-TABLE.md

Then write the "why" column yourself, from the memory layout.
"""

SIZES = (1_000, 2_000)
STRIP = "BLOOM"
MISSES = 20


# ---------------------------------------------------------------- lists ----
class CountingRow:
    """A list built by hand, so the copying is visible.

    A real Python list is a row of slots with spare room at the end. When
    the spare room runs out, a bigger row is allocated and every item is
    copied across. That copy is the only expensive thing `append` ever does,
    and this class counts it.
    """

    def __init__(self) -> None:
        self.slots: list[object] = []
        self.length = 0
        self.copies = 0
        self.comparisons = 0

    def append(self, item: object) -> None:
        """Add one item to the end, growing the row when it is full."""
        if self.length == len(self.slots):
            wanted = 4 if not self.slots else len(self.slots) * 2
            self.copies += self.length  # every item already here moves
            self.slots = self.slots + [None] * (wanted - len(self.slots))
        self.slots[self.length] = item
        self.length += 1

    def __contains__(self, item: object) -> bool:
        """Walk the row from the front, counting every comparison."""
        for index in range(self.length):
            self.comparisons += 1
            if self.slots[index] == item:
                return True
        return False


class ListLane:
    """A queue kept in a plain list, served from the front."""

    def __init__(self) -> None:
        self.items: list[object] = []
        self.shifts = 0

    def join(self, item: object) -> None:
        """Add one item to the back."""
        self.items.append(item)

    def take_front(self) -> object:
        """Remove the front item. Everything behind it slides up one slot."""
        self.shifts += len(self.items) - 1
        return self.items.pop(0)


class RingLane:
    """A queue that never slides anything, because it moves a marker instead."""

    def __init__(self) -> None:
        self.items: list[object] = []
        self.head = 0
        self.shifts = 0

    def join(self, item: object) -> None:
        """Add one item to the back."""
        self.items.append(item)

    def take_front(self) -> object:
        """Remove the front item by stepping the marker one place along."""
        item = self.items[self.head]
        self.head += 1
        return item


# ------------------------------------------------------------ hash table ----
class CountingTable:
    """A set of integers in an open hash table, counting every probe.

    The probe rule is CPython's: start at the low bits of the hash, and on a
    collision jump using the rest of the hash rather than to the next slot
    along. That scattering is why a table of neighbouring numbers does not
    turn into one long queue.
    """

    def __init__(self) -> None:
        self.slots: list[int | None] = [None] * 8
        self.used = 0
        self.probes = 0

    def add(self, key: int) -> None:
        """Store one key, growing the table before it gets crowded."""
        if (self.used + 1) * 3 > len(self.slots) * 2:
            self._grow()
        mask = len(self.slots) - 1
        perturb = hash(key)
        spot = perturb & mask
        while self.slots[spot] is not None:
            if self.slots[spot] == key:
                return
            perturb >>= 5
            spot = (spot * 5 + 1 + perturb) & mask
        self.slots[spot] = key
        self.used += 1

    def __contains__(self, key: int) -> bool:
        """Look one key up, counting each slot inspected."""
        mask = len(self.slots) - 1
        perturb = hash(key)
        spot = perturb & mask
        while True:
            self.probes += 1
            if self.slots[spot] is None:
                return False
            if self.slots[spot] == key:
                return True
            perturb >>= 5
            spot = (spot * 5 + 1 + perturb) & mask

    def _grow(self) -> None:
        """Double the slot array and re-place every key in it."""
        old = self.slots
        self.slots = [None] * (len(old) * 2)
        self.used = 0
        for key in old:
            if key is not None:
                self.add(key)


# ------------------------------------------------------------ the counts ----
def append_copies(size: int) -> int:
    """Elements copied while appending `size` items to a growing row."""
    row = CountingRow()
    for number in range(size):
        row.append(number)
    return row.copies


def list_lane_shifts(size: int) -> int:
    """Elements shifted while serving `size` items from a list lane."""
    lane = ListLane()
    for number in range(size):
        lane.join(number)
    for _ in range(size):
        lane.take_front()
    return lane.shifts


def ring_lane_shifts(size: int) -> int:
    """Elements shifted while serving `size` items from a ring lane."""
    lane = RingLane()
    for number in range(size):
        lane.join(number)
    for _ in range(size):
        lane.take_front()
    return lane.shifts


def scan_comparisons(size: int) -> int:
    """Comparisons made by MISSES failed searches through a row of `size`."""
    row = CountingRow()
    for number in range(size):
        row.append(number)
    for offset in range(MISSES):
        _ = (9_000_000 + offset * 7_919) in row
    return row.comparisons


def probe_steps(size: int) -> int:
    """Probes taken by MISSES failed lookups in a table holding `size` keys."""
    table = CountingTable()
    for number in range(size):
        table.add(number)
    for offset in range(MISSES):
        _ = (9_000_000 + offset * 7_919) in table
    return table.probes


def concat_chars(size: int) -> int:
    """Characters copied building a banner of `size` strips with `+=`."""
    copied = 0
    banner = ""
    for _ in range(size):
        copied += len(banner) + len(STRIP)
        banner += STRIP
    return copied


def join_chars(size: int) -> int:
    """Characters copied building a banner of `size` strips with `join`."""
    parts = [STRIP] * size
    return sum(len(part) for part in parts)


# ----------------------------------------------------------- the report ----
ROWS: list[tuple[str, str, object, float | None]] = [
    ("elements copied, n appends", "amortised O(1) each", append_copies, 2.0),
    ("elements shifted, n front removals from a list lane", "O(n) each", list_lane_shifts, 4.0),
    ("elements shifted, n front removals from a ring lane", "O(1) each", ring_lane_shifts, None),
    (f"comparisons, {MISSES} misses in a row of n", "O(n) each", scan_comparisons, 2.0),
    (f"probes, {MISSES} misses in a table of n", "O(1) average each", probe_steps, 1.0),
    ("characters copied, banner built with +=", "O(n^2) in total", concat_chars, 4.0),
    ("characters copied, banner built with join", "O(n) in total", join_chars, 2.0),
]

TOLERANCE = 0.35


def verdict(small: int, large: int, expected: float | None) -> tuple[str, str]:
    """Turn two counts into a growth figure and a plain-words verdict.

    Args:
        small: The count at the smaller size.
        large: The count at the larger size.
        expected: The growth the claim predicts, or None when the claim is
            that there is no work at all.

    Returns:
        (growth, verdict) as two strings ready to print.
    """
    if expected is None:
        return ("-", "confirmed - no work either way" if large == 0 else "CHECK IT")
    if small == 0:
        return ("-", "CHECK IT")
    growth = large / small
    settled = "confirmed" if abs(growth - expected) <= TOLERANCE else "CHECK IT"
    return (f"{growth:.2f}x", settled)


def report(sizes: tuple[int, int]) -> str:
    """Render the whole cost table as Markdown.

    Args:
        sizes: The smaller and the larger job size.

    Returns:
        A Markdown table. No trailing newline.
    """
    small_size, large_size = sizes
    lines = [
        f"| what was counted | the claim | n={small_size} | n={large_size} | growth | verdict |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for label, claim, measure, expected in ROWS:
        small = measure(small_size)
        large = measure(large_size)
        growth, settled = verdict(small, large, expected)
        lines.append(f"| {label} | `{claim}` | {small} | {large} | {growth} | {settled} |")
    return "\n".join(lines)


# ---- Self-check ----
if __name__ == "__main__":
    print(report(SIZES))
    print()

    assert append_copies(1_000) == 1_020  # 4 + 8 + 16 + ... + 512
    assert list_lane_shifts(1_000) == 1_000 * 999 // 2
    assert ring_lane_shifts(1_000) == 0
    assert scan_comparisons(1_000) == MISSES * 1_000
    assert concat_chars(1_000) == len(STRIP) * 1_000 * 1_001 // 2
    assert join_chars(1_000) == len(STRIP) * 1_000
    assert probe_steps(1_000) < MISSES * 10  # a small constant per lookup
    assert verdict(10, 20, 2.0) == ("2.00x", "confirmed")
    assert verdict(10, 40, 2.0)[1] == "CHECK IT"
    assert verdict(0, 0, None)[1].startswith("confirmed")
    print("All checks passed.")
