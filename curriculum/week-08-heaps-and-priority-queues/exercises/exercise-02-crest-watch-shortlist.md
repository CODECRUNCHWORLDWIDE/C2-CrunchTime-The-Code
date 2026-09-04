# Exercise 2 — The Crest Watch Shortlist

> **Topic:** the bounded top-k heap — holding six things while forty thousand go past
> **Lecture:** [01 — `heapq` and the Top-k Template](../lecture-notes/01-heapq-and-top-k.md)
> **Difficulty:** Beginner-Medium
> **Target time:** 30 minutes
> **Why this one:** it is the first page where the heap's *size* is the answer rather than an implementation detail. Sorting gets the same six crests; it also holds forty thousand readings to do it, and this page is where that stops being an abstract complaint.

## The Brief

Eight river gauges report a stage reading every few minutes, all season — forty
thousand readings by the end of it. The flood desk wants **the six highest
crests of the season** and nothing else.

The obvious answer is to collect everything, sort it, and take the first six.
That is correct. It also holds the whole season in memory to answer a question
about six numbers.

The heap answer keeps exactly six entries. Every reading is compared against the
smallest of the six; if it does not beat that, it is dropped and never stored.
The smallest of the six is the **bar** — that framing is the one to carry into
the write-up, because it is what makes the min-heap choice feel inevitable
rather than backwards.

## Starter

`exercise-02-crest-watch-shortlist-solution.py` sits beside this page with the
gauge feed and the self-checks.

The feed is a **generator**, not a list. That is deliberate: it means you cannot
quietly call `sorted()` on it without materialising it first, and materialising
it first is the thing being avoided.

```text
gauges   : 8 named stations
readings : 40,000 across the season
shortlist: the top 6, highest first
```

## Requirements

1. `top_crests(feed, size)` walks the feed once and returns the `size` highest
   readings, highest first, as `(gauge, stage)` pairs.
2. The heap never holds more than `size` entries. That is the claim; the file
   tracks the peak so it can be asserted rather than believed.
3. `sorted_crests(readings, size)` is the sort-everything version, used only to
   check the heap version agrees with it.
4. `work_estimate(readings, size)` returns the two comparison counts,
   `n log₂ k` and `n log₂ n`, so the difference can be printed rather than
   asserted from memory.
5. Asking for zero crests returns an empty list; asking for more than exist
   returns everything there is.

## Constraints

- **A min-heap, for the largest values.** This is the inversion worth writing
  down: the heap holds the six largest *so far*, and the cheapest thing to check
  is whether a new reading beats the worst of them — which is what a min-heap
  puts on top.
- **Push then pop, not check then push.** `heappushpop` does both in one sift and
  keeps the size fixed for free.
- **Ties keep both.** Two gauges cresting at the same stage are two crests, not
  one, and the shortlist reflects that.
- **The feed is walked once.** No second pass, no storing it.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-02-crest-watch-shortlist.py
readings seen : 40000
peak heap size: 6
season shortlist:
  1. 818 cm  Gorse Cut
  2. 816 cm  Gorse Cut
  3. 815 cm  Ironmill
  4. 813 cm  Bent Weir
  5. 813 cm  Gorse Cut
  6. 811 cm  Drovers Bridge
heap comparisons (n log2 k) : 103399
sort comparisons (n log2 n) : 611508
the sort does about 5.9 times the work
sorting holds 40000 readings; the heap held 6
two readings tie at 61: [('Fishlock', 61), ('Bent Weir', 61)]
asking for more than exist: [('Fishlock', 61), ('Bent Weir', 61), ('Ironmill', 12)]
asking for none: []
All checks passed.
```

The two numbers to read together are the comparison counts. The sort does about
**5.9×** the work of the heap here — and, more to the point, it holds 40,000
readings where the heap held 6. On a season this size the time barely matters;
the memory is the argument.

## Steps

1. Read the self-checks. They are the spec.
2. Write the memo: min-heap of size k, the top of it is the bar, and why that is
   the right way round.
3. Walk the feed, filling the heap until it holds `size` entries, then
   `heappushpop` for the rest.
4. Return them highest first — the heap is not sorted, so this is a real step.
5. Check against `sorted_crests` on the same data. They must agree exactly.
6. Handle `size = 0` and `size` larger than the feed, then write the FRAME pass.

## The Solution

```python
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
```

`work_estimate` is in the file rather than in a comment because a claimed ratio
is easy to get wrong and a printed one is not.

## Run it

Download the solution beside this page and run it:

```bash
python exercise-02-crest-watch-shortlist.py
```

No third-party packages, no arguments, no input. It prints the shortlist, the
peak heap size, the work comparison, the edge cases, and then
`All checks passed.`

## Common bugs to catch

- **A max-heap by negation.** Symptom: it works, and it holds everything. The
  bar you want to check against is the *smallest* of the kept crests.
- **Checking `if reading > heap[0]` before the heap is full.** Symptom: a
  shortlist with fewer than six entries on a feed that had plenty.
- **Returning the heap as-is.** Symptom: six correct crests in the wrong order. A
  heap is not a sorted list.
- **Dropping ties.** Symptom: five crests reported where six exist, on a season
  with two gauges at the same stage.
- **Materialising the generator to sort it.** Symptom: correct output and the
  memory profile you were avoiding.

## Acceptance checklist

- [ ] The shortlist matches `sorted_crests` exactly on the shipped feed.
- [ ] The peak heap size is 6, asserted, not assumed.
- [ ] 40,000 readings are seen and the count is reported.
- [ ] Two readings tied at the same stage both appear.
- [ ] `size = 0` returns `[]`; `size` above the feed length returns all of it.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Report the top crest **per gauge** rather than overall. It is a different
  structure, and noticing that it is not a top-k problem is the exercise.
- Make the feed a hundred times longer and watch the peak heap size stay at six.
  Print the memory difference rather than describing it.
- Add a fifth column: the minute each crest was recorded, and break ties by
  earliest. Say where in the tuple that has to go and why.
