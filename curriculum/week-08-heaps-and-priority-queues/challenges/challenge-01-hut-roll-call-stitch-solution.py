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
