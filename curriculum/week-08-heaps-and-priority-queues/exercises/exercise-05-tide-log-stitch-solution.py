"""exercise-05-tide-log-stitch-solution.py — one estuary ledger from four station logs.

Four tide stations each keep their own log, already in time order. The harbour
office wants a single ledger in time order. The heap holds at most one entry
per station — four rows, never fourteen — so the merge costs one pass and a
handful of comparisons per row rather than a full sort of everything.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

import heapq

# ---- Given data ----
# Precedence when two stations report the same minute: seaward first, then up
# the estuary. This is the harbour office's rule; it is not alphabetical.
STATION_ORDER: tuple[str, ...] = (
    "Skerry Point",
    "Cormorant Bar",
    "Long Slip",
    "Herring Steps",
)

# Each log is already ascending by minute. Minute 0 is the start of the watch.
LOGS: dict[str, list[tuple[int, int]]] = {
    "Skerry Point": [(0, 412), (15, 455), (30, 486), (45, 501), (60, 498)],
    "Cormorant Bar": [(0, 388), (20, 441), (30, 470), (55, 494)],
    "Long Slip": [(10, 366), (30, 449), (45, 472), (75, 480), (90, 461)],
    "Herring Steps": [],
}


# ---- Your task ----
def seed_heap(logs: dict[str, list[tuple[int, int]]]) -> list[tuple]:
    """Return a heap holding the first unread row of every non-empty log.

    Args:
        logs: Station name to a list of (minute, height) rows, each ascending.

    Returns:
        A heapified list of (minute, precedence rank, station, position,
        height) entries. A station with an empty log contributes nothing.
    """
    heap = []
    for rank, station in enumerate(STATION_ORDER):
        rows = logs.get(station, [])
        if rows:
            minute, height = rows[0]
            heap.append((minute, rank, station, 0, height))
    heapq.heapify(heap)
    return heap


def stitch(
    logs: dict[str, list[tuple[int, int]]], stats: dict[str, int] | None = None
) -> list[tuple[int, str, int]]:
    """Return every row from every log, in one time-ordered ledger.

    Args:
        logs: Station name to a list of (minute, height) rows, each ascending.
        stats: Optional dict. When given, "peak_heap" is set to the largest
            the heap ever grew.

    Returns:
        (minute, station, height) rows. Rows sharing a minute come out in
        STATION_ORDER.
    """
    heap = seed_heap(logs)
    peak = len(heap)
    ledger = []
    while heap:
        minute, rank, station, position, height = heapq.heappop(heap)
        ledger.append((minute, station, height))
        rows = logs[station]
        if position + 1 < len(rows):
            next_minute, next_height = rows[position + 1]
            heapq.heappush(heap, (next_minute, rank, station, position + 1, next_height))
        peak = max(peak, len(heap))
    if stats is not None:
        stats["peak_heap"] = peak
    return ledger


def first_rows(
    logs: dict[str, list[tuple[int, int]]], count: int
) -> list[tuple[int, str, int]]:
    """Return only the earliest `count` rows of the stitched ledger.

    The rows after them are never popped, so a caller who wants the first
    handful does not pay for the rest.

    Args:
        logs: Station name to a list of (minute, height) rows, each ascending.
        count: How many rows to take. 0 returns nothing.

    Returns:
        The first `count` (minute, station, height) rows, or all of them when
        the logs hold fewer than `count`.
    """
    heap = seed_heap(logs)
    taken = []
    while heap and len(taken) < count:
        minute, rank, station, position, height = heapq.heappop(heap)
        taken.append((minute, station, height))
        rows = logs[station]
        if position + 1 < len(rows):
            next_minute, next_height = rows[position + 1]
            heapq.heappush(heap, (next_minute, rank, station, position + 1, next_height))
    return taken


def highest_at_minute(ledger: list[tuple[int, str, int]], minute: int) -> str | None:
    """Return the station reporting the greatest height at one minute.

    Args:
        ledger: A stitched ledger.
        minute: The minute to look at.

    Returns:
        The station name, or None when no station reported that minute. Ties
        go to whichever of them comes first in STATION_ORDER, which is the
        order the ledger already holds them in.
    """
    best = None
    for row_minute, station, height in ledger:
        if row_minute == minute and (best is None or height > best[0]):
            best = (height, station)
    return None if best is None else best[1]


# ---- Self-check ----
if __name__ == "__main__":
    stats: dict[str, int] = {}
    ledger = stitch(LOGS, stats)

    print(f"rows stitched : {len(ledger)}")
    print(f"peak heap size: {stats['peak_heap']}")
    print("ledger:")
    for minute, station, height in ledger:
        print(f"  min {minute:3d}  {station:<14} {height} cm")

    print(f"first four rows: {first_rows(LOGS, 4)}")
    print(f"first zero rows: {first_rows(LOGS, 0)}")
    print(f"highest at minute 30: {highest_at_minute(ledger, 30)}")
    print(f"highest at minute 31: {highest_at_minute(ledger, 31)}")
    print(f"stitching empty logs: {stitch({'Herring Steps': []})}")

    assert len(ledger) == 14
    assert stats["peak_heap"] == 3
    assert ledger[0] == (0, "Skerry Point", 412)
    assert ledger[1] == (0, "Cormorant Bar", 388)
    assert ledger[5:8] == [
        (30, "Skerry Point", 486),
        (30, "Cormorant Bar", 470),
        (30, "Long Slip", 449),
    ]
    assert [minute for minute, _, _ in ledger] == sorted(m for m, _, _ in ledger)
    assert first_rows(LOGS, 4) == ledger[:4]
    assert first_rows(LOGS, 0) == []
    assert first_rows(LOGS, 99) == ledger
    assert highest_at_minute(ledger, 30) == "Skerry Point"
    assert highest_at_minute(ledger, 31) is None
    assert stitch({"Herring Steps": []}) == []
    print("All checks passed.")
