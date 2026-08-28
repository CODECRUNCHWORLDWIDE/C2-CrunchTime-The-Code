"""exercise-02-crest-watch-shortlist-solution.py — the six highest crests in a season.

A river basin's gauges report a stage reading every few minutes all season.
The flood desk wants the six highest crests of the whole season and nothing
else. This file keeps a bounded min-heap of six entries and walks the feed
once, so the other 39,994 readings are never stored.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

import heapq
from math import log2

# ---- Given data ----
GAUGE_NAMES: tuple[str, ...] = (
    "Bent Weir",
    "Cattle Ford",
    "Drovers Bridge",
    "Elder Reach",
    "Fishlock",
    "Gorse Cut",
    "Harrow Sill",
    "Ironmill",
)

READING_COUNT = 40_000
SHORTLIST_SIZE = 6


def gauge_feed(count: int):
    """Yield (gauge, stage_cm) readings one at a time, like a live feed.

    The feed is a generator on purpose. It hands out one reading, forgets it,
    and moves on — there is no list behind it to index into and no way to
    rewind. Every reading it produces is decided by arithmetic, so two runs of
    this file see exactly the same season.

    Args:
        count: How many readings the season contains.

    Yields:
        (gauge name, stage in centimetres) pairs.
    """
    state = 20_250_827
    for _ in range(count):
        state = (state * 1_103_515_245 + 12_345) % 2_147_483_648
        stage = 20 + (state >> 8) % 400 + (state >> 20) % 400
        yield GAUGE_NAMES[state % len(GAUGE_NAMES)], stage


# ---- Your task ----
def top_crests(
    feed, size: int, stats: dict[str, int] | None = None
) -> list[tuple[str, int]]:
    """Return the `size` highest readings from a one-pass feed.

    Args:
        feed: An iterable of (gauge, stage) readings. Walked exactly once.
        size: How many crests to keep. 0 means keep none.
        stats: Optional dict. When given, "peak_heap" is set to the largest
            the heap ever grew and "readings" to how many arrived.

    Returns:
        (gauge, stage) pairs, highest stage first. Where two readings tie on
        stage, the one that arrived earlier comes first.
    """
    shortlist: list[tuple[int, int, str]] = []
    peak = 0
    arrival = 0
    for arrival, (gauge, stage) in enumerate(feed, 1):
        if size <= 0:
            continue
        entry = (stage, -arrival, gauge)
        if len(shortlist) < size:
            heapq.heappush(shortlist, entry)
        elif entry > shortlist[0]:
            heapq.heapreplace(shortlist, entry)
        peak = max(peak, len(shortlist))
    if stats is not None:
        stats["peak_heap"] = peak
        stats["readings"] = arrival
    return [
        (gauge, stage)
        for stage, _, gauge in sorted(shortlist, key=lambda e: (-e[0], -e[1]))
    ]


def sorted_crests(readings: list[tuple[str, int]], size: int) -> list[tuple[str, int]]:
    """Return the same answer by sorting everything. Correct, and wasteful.

    Args:
        readings: Every reading of the season, already collected into a list.
        size: How many crests to keep.

    Returns:
        The same pairs top_crests returns, in the same order.
    """
    ranked = sorted(enumerate(readings, 1), key=lambda pair: (-pair[1][1], pair[0]))
    return [reading for _, reading in ranked[:size]]


def work_estimate(readings: int, size: int) -> tuple[int, int]:
    """Return roughly how many comparisons each approach costs.

    Args:
        readings: How many readings arrive.
        size: How many crests are wanted.

    Returns:
        (heap comparisons, full-sort comparisons), both rounded to whole
        numbers. These are the textbook n·log2(k) and n·log2(n) counts, not a
        measurement — they are here to be read, not benchmarked.
    """
    heap_cost = round(readings * log2(max(size, 2)))
    sort_cost = round(readings * log2(max(readings, 2)))
    return heap_cost, sort_cost


# ---- Self-check ----
if __name__ == "__main__":
    stats: dict[str, int] = {}
    shortlist = top_crests(gauge_feed(READING_COUNT), SHORTLIST_SIZE, stats)

    print(f"readings seen : {stats['readings']}")
    print(f"peak heap size: {stats['peak_heap']}")
    print("season shortlist:")
    for rank, (gauge, stage) in enumerate(shortlist, 1):
        print(f"  {rank}. {stage:3d} cm  {gauge}")

    heap_cost, sort_cost = work_estimate(READING_COUNT, SHORTLIST_SIZE)
    print(f"heap comparisons (n log2 k) : {heap_cost}")
    print(f"sort comparisons (n log2 n) : {sort_cost}")
    print(f"the sort does about {sort_cost / heap_cost:.1f} times the work")

    every_reading = list(gauge_feed(READING_COUNT))
    print(f"sorting holds {len(every_reading)} readings; the heap held {stats['peak_heap']}")

    tiny = [("Fishlock", 61), ("Bent Weir", 61), ("Ironmill", 12)]
    print(f"two readings tie at 61: {top_crests(tiny, 2)}")
    print(f"asking for more than exist: {top_crests(tiny, 9)}")
    print(f"asking for none: {top_crests(tiny, 0)}")

    assert stats["peak_heap"] == SHORTLIST_SIZE
    assert stats["readings"] == READING_COUNT
    assert len(shortlist) == SHORTLIST_SIZE
    assert shortlist == sorted_crests(every_reading, SHORTLIST_SIZE)
    assert [stage for _, stage in shortlist] == sorted(
        (stage for _, stage in shortlist), reverse=True
    )
    assert shortlist[3] == ("Bent Weir", 813) and shortlist[4] == ("Gorse Cut", 813)
    assert top_crests(tiny, 2) == [("Fishlock", 61), ("Bent Weir", 61)]
    assert len(top_crests(tiny, 9)) == 3
    assert top_crests(tiny, 0) == []
    print("All checks passed.")
