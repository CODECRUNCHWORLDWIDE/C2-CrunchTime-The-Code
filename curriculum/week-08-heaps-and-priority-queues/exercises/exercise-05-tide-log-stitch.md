# Exercise 5 — The Estuary Ledger

> **Topic:** the k-way merge — one heap entry per source, not one per row
> **Lecture:** [03 — Two Heaps and the k-Way Merge](../lecture-notes/03-two-heap-and-k-way-merge.md)
> **Difficulty:** Medium
> **Target time:** 35 minutes
> **Why this one:** it is the merge in its plainest form, so the one thing worth arguing about is the heap's *size*. Get that right here and [Challenge 1](../challenges/challenge-01-hut-roll-call-stitch.md) is the same idea with a generator on top.

## The Brief

Four tide stations each keep their own log, already in time order. The harbour
office wants **one ledger** in time order.

Concatenating and sorting works. So does the merge — and the merge holds four
rows at a time rather than fourteen, because each log is already sorted and the
only question at each step is *which log has the earliest unread row*.

That is the whole idea: the heap holds **one pending row per station**, never the
whole log. Space is `O(k)` where k is the number of stations, not `O(n)` where n
is the number of readings. On four short logs it saves nothing. On four logs that
each run to a million rows it is the difference between a program that fits in
memory and one that does not.

## Starter

`exercise-05-tide-log-stitch-solution.py` sits beside this page with the four
station logs and the self-checks.

```text
station          rows
Skerry Point        5
Cormorant Bar       4
Long Slip           5
Herring Steps       0
```

Herring Steps reported nothing all watch. An empty log is not an error and it is
not a row — it simply never enters the heap, and a merge that seeds blindly will
crash on it before it reads anything.

When two stations report the same minute, precedence runs **seaward first, then
up the estuary**: Skerry Point, Cormorant Bar, Long Slip, Herring Steps. That is
the harbour office's rule and it is not alphabetical, so it has to be encoded
rather than assumed.

## Requirements

1. `seed_heap(logs)` puts the first row of each **non-empty** log into the heap.
2. `stitch(logs)` returns the full ledger as `(minute, station, stage)` rows in
   time order, and reports the peak heap size.
3. `first_rows(logs, count)` returns only the first `count` rows, doing only the
   work those rows need.
4. `highest_at_minute(ledger, minute)` returns the station reading highest at a
   given minute, or `None` if nothing was recorded then.
5. All-empty logs stitch to an empty ledger without special-casing.

## Constraints

- **One row per station in the heap at a time.** This is the claim the whole
  exercise rests on, so the file tracks the peak and asserts it.
- **Ties break by station precedence,** encoded as an index in the heap key. Not
  by name, and not by whatever order the dictionary happens to iterate in.
- **The station's own log position travels in the heap entry.** That is how the
  next row is found without searching for it.
- **An empty log never enters the heap.** Seeding it is the bug; skipping it is
  the rule.
- `first_rows` must genuinely stop early. Stitching everything and slicing is
  correct and misses the point.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-05-tide-log-stitch.py
rows stitched : 14
peak heap size: 3
ledger:
  min   0  Skerry Point   412 cm
  min   0  Cormorant Bar  388 cm
  min  10  Long Slip      366 cm
  min  15  Skerry Point   455 cm
  min  20  Cormorant Bar  441 cm
  min  30  Skerry Point   486 cm
  min  30  Cormorant Bar  470 cm
  min  30  Long Slip      449 cm
  min  45  Skerry Point   501 cm
  min  45  Long Slip      472 cm
  min  55  Cormorant Bar  494 cm
  min  60  Skerry Point   498 cm
  min  75  Long Slip      480 cm
  min  90  Long Slip      461 cm
first four rows: [(0, 'Skerry Point', 412), (0, 'Cormorant Bar', 388), (10, 'Long Slip', 366), (15, 'Skerry Point', 455)]
first zero rows: []
highest at minute 30: Skerry Point
highest at minute 31: None
stitching empty logs: []
All checks passed.
```

The peak heap size is **3**, not 4 — Herring Steps never contributed a row, so
the heap never held four. Fourteen rows merged, three entries held. That number
is the exercise; everything else on the page is scaffolding around it.

## Steps

1. Read the self-checks. They are the spec.
2. Write the memo: heap of one row per source, keyed on `(minute, precedence)`.
3. Seed the heap, skipping empty logs. Print it once and look at the entries.
4. Loop: pop the earliest, write it down, push that station's next row if it has
   one.
5. Track the peak heap size as you go, and assert it rather than claiming it.
6. Add `first_rows` and `highest_at_minute`, then write the FRAME pass.

## The Solution

```python
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
```

`highest_at_minute` returning `None` for minute 31 rather than the nearest row is
deliberate: the ledger records what was reported, and interpolating between rows
is a different question the harbour office did not ask.

## Run it

Download the solution beside this page and run it:

```bash
python exercise-05-tide-log-stitch.py
```

No third-party packages, no arguments, no input. It prints the row count, the
peak heap size, the full ledger, the first four rows, the minute lookups, the
empty case, and then `All checks passed.`

## Common bugs to catch

- **Pushing every row of every log at the start.** Symptom: correct output,
  `O(n)` space, and no exercise. The peak-size assertion catches it.
- **Seeding an empty log.** Symptom: `IndexError` before a single row is merged.
- **Breaking ties alphabetically.** Symptom: Cormorant Bar ahead of Skerry Point
  at minute 0, which is the wrong estuary order.
- **Forgetting to push the next row after a pop.** Symptom: a ledger with exactly
  one row per station.
- **`first_rows` slicing a full stitch.** Symptom: correct rows, and all the work
  done anyway.
- **Comparing station names as a fallback key.** Symptom: it works until a station
  is renamed. Encode the precedence.

## Acceptance checklist

- [ ] Fourteen rows stitched, in minute order.
- [ ] Peak heap size is 3, asserted, because one log is empty.
- [ ] Minute 0 gives Skerry Point before Cormorant Bar.
- [ ] `first_rows(logs, 4)` returns four rows; `first_rows(logs, 0)` returns none.
- [ ] `highest_at_minute` is `Skerry Point` at 30 and `None` at 31.
- [ ] All-empty logs stitch to `[]`.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Add a fifth station whose log is longer than the other four put together, and
  confirm the peak heap size still does not exceed the station count.
- Report, per station, how many rows it contributed to the first half of the
  ledger. It says which station is driving the watch.
- Turn `stitch` into a generator and compare it with
  [Challenge 1](../challenges/challenge-01-hut-roll-call-stitch.md). The change is
  small; what it buys is not.
