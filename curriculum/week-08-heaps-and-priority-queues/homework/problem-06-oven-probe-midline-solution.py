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
