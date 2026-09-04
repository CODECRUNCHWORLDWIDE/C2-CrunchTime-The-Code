# Challenge 1 — The Hut Roll Call

> Topic: k-way merge with a heap, lazily · Lecture: [3](../lecture-notes/03-two-heap-and-k-way-merge.md) · Difficulty: Medium-Hard · Target time: 70 minutes including the FRAME write-up · Why this one: the merge is a generator, so "how much of the input do we actually read" becomes a design decision instead of an afterthought.

## The Brief

Four mountain huts radio in. Each hut's log is already in minute order. The
rescue coordinator wants them stitched into **one** roll call — and wants to stop
reading the moment every hut has been heard from twice.

That second half is the challenge. Merging four sorted logs is a heap and a
loop. Merging them **lazily**, so the coordinator pays only for the rows they
actually read, means the merge has to be a generator — and then a hut whose log
never ends is no longer a problem, because nothing ever asks it to finish.

## Starter

`challenge-01-hut-roll-call-stitch-solution.py` sits beside this page with the
hut logs and the self-checks.

Ties matter here. When two huts call in the same minute, the **lower** hut is
written first: it is the relay, so its call is already on the air. That is a
domain rule, not a convention, and it belongs in the heap key rather than in a
sort afterwards.

## Requirements

1. `roll_call(logs)` yields merged rows in minute order, **lazily**.
2. `stitch_until_covered(logs, required)` reads only as far as it must for every
   hut to appear `required` times, and reports the minute coverage was reached.
3. `longest_silence(rows)` returns the widest gap between consecutive calls, as
   `(start, end, length)`, or `None` when there are fewer than two rows.
4. A hut that never calls means coverage is never reached — report `None`, not
   the whole log.
5. `required = 0` is satisfied immediately, having read nothing.

## Constraints

- **The merge must be a generator.** Building the whole list and slicing it is
  correct and defeats the point; the write-up has to say what the generator buys
  and when it does not matter.
- **The heap holds one pending call per hut**, never the whole log. That is what
  makes the space `O(k)` rather than `O(n)`, and it is the sentence Examine
  (cost) is looking for.
- **Ties break by altitude, low first.** Put it in the key.
- **A hut with an endless log must not hang the merge.** If your solution can
  only work on finite lists, say so explicitly rather than letting a reader
  assume otherwise.
- Coverage of zero is reached before reading anything at all.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python challenge-01-hut-roll-call-stitch.py
rows read before stopping: 10
coverage reached at minute: 58
  min   4  Larchgate     LG-1
  min   9  Corrie Bothy  CB-1
  min  11  Rimefell      RF-1
  min  17  Windshiel     WS-1
  min  26  Larchgate     LG-2
  min  26  Corrie Bothy  CB-2
  min  40  Windshiel     WS-2
  min  40  Windshiel     WS-3
  min  51  Larchgate     LG-3
  min  58  Rimefell      RF-2
rows in the whole roll call: 15
rows the coordinator skipped: 5
longest silence: (63, 88, 25)
with a silent hut: 11 rows, coverage None
required of zero: ([], None)
no huts at all: ([], None)
silence needs two rows: None
All checks passed.
```

Read the two numbers together: the whole roll call is **15 rows**, and coverage
was reached after **10**. Five rows were never read. On four short logs that
saves nothing; on four radio feeds that never stop, it is the difference between
a program that answers and one that does not.

## Steps

1. Read the self-checks. They are the spec.
2. Write the memo: name the structure, the heap's contents, and the tie-break.
3. Write `roll_call` as a generator and check it against a plain sorted merge of
   the same logs. They must agree exactly.
4. Write `stitch_until_covered` on top of it, counting per hut. Stop the moment
   the last hut reaches the requirement — not at the end of that minute.
5. Handle the silent hut and `required = 0` before the pretty output.
6. Add `longest_silence`, then write the FRAME pass.

## The Solution

```python
"""challenge-01-hut-roll-call-stitch-solution.py — one roll call from four hut logs.

Four mountain huts radio in. Each hut's log is already in minute order. The
rescue coordinator wants them stitched into one roll call, and wants to stop
reading the moment every hut has been heard from twice.

The merge is a generator over a heap that holds one pending call per hut, so
the coordinator pays only for the rows actually read, and a hut whose log is
endless never has to be finished.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

import heapq
from collections.abc import Iterable, Iterator

# ---- Given data ----
# Metres above sea level. When two huts share a minute the lower one is
# written first: it is the relay, so its call is the one already on the air.
ALTITUDE_M: dict[str, int] = {
    "Larchgate": 980,
    "Corrie Bothy": 1240,
    "Windshiel": 1475,
    "Rimefell": 1710,
}

# Each hut's log is (minute since the watch opened, callsign), already ascending.
HUT_LOGS: dict[str, list[tuple[int, str]]] = {
    "Larchgate": [(4, "LG-1"), (26, "LG-2"), (51, "LG-3"), (88, "LG-4")],
    "Corrie Bothy": [(9, "CB-1"), (26, "CB-2"), (63, "CB-3")],
    "Windshiel": [(17, "WS-1"), (40, "WS-2"), (40, "WS-3"), (95, "WS-4")],
    "Rimefell": [(11, "RF-1"), (58, "RF-2"), (58, "RF-3"), (102, "RF-4")],
}

REQUIRED_CALLS = 2


# ---- Your task ----
def roll_call(
    logs: dict[str, Iterable[tuple[int, str]]]
) -> Iterator[tuple[int, str, str]]:
    """Yield every call from every hut, in minute order, one at a time.

    Nothing is collected. Each hut contributes at most one pending call to the
    heap, so a caller that stops early has never touched the rest of any log.

    Args:
        logs: Hut name to an iterable of (minute, callsign), already ascending
            by minute. A hut may be silent, and its iterable may be endless.

    Yields:
        (minute, hut, callsign), earliest minute first. Calls sharing a minute
        come out lowest hut first, and a single hut's own calls keep the order
        its log put them in.
    """
    pending: list[tuple[int, int, str, int, str]] = []
    readers: dict[str, Iterator[tuple[int, str]]] = {}
    for hut, log in logs.items():
        reader = iter(log)
        first = next(reader, None)
        if first is None:
            continue
        readers[hut] = reader
        minute, callsign = first
        heapq.heappush(pending, (minute, ALTITUDE_M[hut], hut, 0, callsign))

    while pending:
        minute, altitude, hut, position, callsign = heapq.heappop(pending)
        yield minute, hut, callsign
        following = next(readers[hut], None)
        if following is not None:
            next_minute, next_callsign = following
            heapq.heappush(
                pending, (next_minute, altitude, hut, position + 1, next_callsign)
            )


def stitch_until_covered(
    logs: dict[str, Iterable[tuple[int, str]]], required: int
) -> tuple[list[tuple[int, str, str]], int | None]:
    """Stitch the roll call only as far as the coverage rule needs.

    Args:
        logs: Hut name to an iterable of (minute, callsign), already ascending.
        required: How many calls each hut must contribute before the
            coordinator stops. A `required` of 0 or less is already satisfied,
            so nothing is read.

    Returns:
        (rows, minute). `rows` is the prefix of the roll call up to and
        including the call that completed coverage. `minute` is that call's
        minute. When coverage is never reached — a silent hut, or a hut that
        calls too few times — every row is returned and `minute` is None.
    """
    huts = set(logs)
    if required <= 0:
        return [], None
    heard: dict[str, int] = {}
    rows: list[tuple[int, str, str]] = []
    for minute, hut, callsign in roll_call(logs):
        rows.append((minute, hut, callsign))
        heard[hut] = heard.get(hut, 0) + 1
        if len(heard) == len(huts) and all(heard[name] >= required for name in huts):
            return rows, minute
    return rows, None


def longest_silence(rows: list[tuple[int, str, str]]) -> tuple[int, int, int] | None:
    """Return the widest gap between two calls that follow each other.

    Args:
        rows: A stitched roll call.

    Returns:
        (minute before the gap, minute after it, gap in minutes), or None when
        there are fewer than two rows. Ties go to the earliest gap.
    """
    if len(rows) < 2:
        return None
    widest = (rows[0][0], rows[1][0], rows[1][0] - rows[0][0])
    for before, after in zip(rows, rows[1:]):
        gap = after[0] - before[0]
        if gap > widest[2]:
            widest = (before[0], after[0], gap)
    return widest


# ---- Self-check ----
if __name__ == "__main__":
    covered, minute = stitch_until_covered(HUT_LOGS, REQUIRED_CALLS)
    print(f"rows read before stopping: {len(covered)}")
    print(f"coverage reached at minute: {minute}")
    for row_minute, hut, callsign in covered:
        print(f"  min {row_minute:3d}  {hut:<13} {callsign}")

    everything = list(roll_call(HUT_LOGS))
    print(f"rows in the whole roll call: {len(everything)}")
    print(f"rows the coordinator skipped: {len(everything) - len(covered)}")
    print(f"longest silence: {longest_silence(everything)}")

    silent = dict(HUT_LOGS)
    silent["Rimefell"] = []
    silent_rows, silent_minute = stitch_until_covered(silent, REQUIRED_CALLS)
    print(f"with a silent hut: {len(silent_rows)} rows, coverage {silent_minute}")

    print(f"required of zero: {stitch_until_covered(HUT_LOGS, 0)}")
    print(f"no huts at all: {stitch_until_covered({}, 2)}")
    print(f"silence needs two rows: {longest_silence(everything[:1])}")

    assert len(covered) == 10
    assert minute == 58
    assert covered[0] == (4, "Larchgate", "LG-1")
    assert covered[4] == (26, "Larchgate", "LG-2")
    assert covered[5] == (26, "Corrie Bothy", "CB-2")
    assert covered[-1] == (58, "Rimefell", "RF-2")
    assert len(everything) == 15
    assert [row[0] for row in everything] == sorted(row[0] for row in everything)
    assert everything[6:8] == [(40, "Windshiel", "WS-2"), (40, "Windshiel", "WS-3")]
    assert longest_silence(everything) == (63, 88, 25)
    assert len(silent_rows) == 11 and silent_minute is None
    assert stitch_until_covered(HUT_LOGS, 0) == ([], None)
    assert stitch_until_covered({}, 2) == ([], None)
    assert longest_silence(everything[:1]) is None
    print("All checks passed.")
```

The heap entry carries the altitude as part of the key rather than sorting
afterwards, because a lazy merge has no "afterwards" — the row is emitted the
moment it is popped.

## Run it

Download the solution beside this page and run it:

```bash
python challenge-01-hut-roll-call-stitch.py
```

No third-party packages, no arguments, no input. It prints the stitched roll
call, the rows skipped, the longest silence, the degenerate cases, and then
`All checks passed.`

## Common bugs to catch

- **Materialising every log first.** Symptom: correct output, and a program that
  cannot handle a feed that does not end.
- **Pushing whole logs onto the heap.** Symptom: `O(n)` space where `O(k)` was
  the claim. One pending call per hut.
- **Sorting after the merge to fix ties.** Symptom: correct on a finite list and
  impossible in a generator.
- **Stopping at the end of the covering minute.** Symptom: one row too many, and
  a coverage minute that is right by luck.
- **Reporting the last minute as coverage when a hut is silent.** Symptom: a
  confident number where `None` is the truth.
- **`longest_silence` on one row.** Symptom: an exception, or a gap of zero. With
  fewer than two rows there is no gap to report.

## Acceptance checklist

- [ ] The full roll call is 15 rows; coverage at 2 calls each is reached after 10.
- [ ] The lazy merge agrees exactly with a plain sorted merge of the same logs.
- [ ] A silent hut yields coverage `None`, having read the finite logs only once.
- [ ] `required = 0` returns immediately with nothing read.
- [ ] Same-minute rows are ordered by altitude, lower first.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Report, per hut, how many of its rows were read before coverage. It tells the
  coordinator which feed is carrying the roll call and which is dragging.
- Add a fifth hut mid-merge, after the generator has started, and say what has to
  change. The honest answer is more interesting than the code.
- Make one log infinite — a generator counting minutes forever — and check the
  merge still terminates under `stitch_until_covered`. If it does not, you built
  the eager version.
