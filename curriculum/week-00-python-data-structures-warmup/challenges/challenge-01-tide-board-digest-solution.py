"""challenge-01-tide-board-digest-solution.py — summarise the harbour log.

The tide board's log is a list of hand-typed lines. Some of them are not
lines at all. This program reads what it can, throws away what it cannot,
and reports one row per water state with every time that hit the extreme.

Strings go in. A dict does the grouping. A string comes out.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from typing import NamedTuple

STATES = ("HW", "LW")

LOG: list[str] = [
    "0612 HW 3.42 north quay",
    "1104 LW 0.85 north quay",
    "1231 HW 3.60 boat pound",
    "bad line",
    "1755 LW 0.85 boat pound",
    "1840 HW 3.60 north quay",
    "2033 LW 1.20 slipway",
    "0700 XX 2.00 north quay",
    "0930 HW high boat pound",
]


class StateDigest(NamedTuple):
    """One state's summary: how many readings, the extreme, and its times."""

    count: int
    extreme: float
    times: list[str]


def is_clock(text: str) -> bool:
    """Return True when `text` is a four-digit 24-hour time.

    Args:
        text: The first field of a log line.

    Returns:
        True for "0000" through "2359", False for anything else.
    """
    if len(text) != 4 or not text.isdigit():
        return False
    return int(text[:2]) < 24 and int(text[2:]) < 60


def parse_line(line: str) -> tuple[str, str, float, str] | None:
    """Turn one log line into a reading, or reject it.

    Args:
        line: One raw line from the board.

    Returns:
        (clock, state, height, place), or None when the line is unreadable.
    """
    parts = line.split()
    if len(parts) < 4:
        return None
    clock, state, height = parts[0], parts[1], parts[2]
    if not is_clock(clock) or state not in STATES:
        return None
    try:
        metres = float(height)
    except ValueError:
        return None
    return clock, state, metres, " ".join(parts[3:])


def digest(lines: list[str]) -> dict[str, StateDigest]:
    """Summarise the readable lines, one entry per water state.

    Args:
        lines: The raw log, unreadable lines and all.

    Returns:
        A dict from state to its StateDigest, states in the order each was
        first read. The extreme is the highest height for HW and the lowest
        for LW; times holds every clock that reached it, in log order.
    """
    readings: dict[str, list[tuple[str, float]]] = {}
    for line in lines:
        parsed = parse_line(line)
        if parsed is None:
            continue
        clock, state, metres, _place = parsed
        readings.setdefault(state, []).append((clock, metres))

    summary: dict[str, StateDigest] = {}
    for state, seen in readings.items():
        pick = max if state == "HW" else min
        extreme = pick(metres for _clock, metres in seen)
        summary[state] = StateDigest(
            count=len(seen),
            extreme=extreme,
            times=[clock for clock, metres in seen if metres == extreme],
        )
    return summary


def skipped(lines: list[str]) -> int:
    """Count the lines the parser refused.

    Args:
        lines: The raw log.

    Returns:
        How many lines could not be read as a reading.
    """
    return sum(1 for line in lines if parse_line(line) is None)


def report(lines: list[str]) -> str:
    """Render the whole digest as text.

    Args:
        lines: The raw log.

    Returns:
        One line per state, then one line counting the rejects. No trailing
        newline.
    """
    rows = []
    for state, entry in digest(lines).items():
        times = ", ".join(entry.times)
        rows.append(
            f"{state}  {entry.count} readings  "
            f"extreme {entry.extreme:.2f} m at {times}"
        )
    rows.append(f"skipped {skipped(lines)} unreadable lines")
    return "\n".join(rows)


# ---- Self-check ----
if __name__ == "__main__":
    print(report(LOG))

    summary = digest(LOG)
    assert list(summary) == ["HW", "LW"]
    assert summary["HW"].count == 3
    assert summary["HW"].extreme == 3.60
    assert summary["HW"].times == ["1231", "1840"]
    assert summary["LW"].extreme == 0.85
    assert summary["LW"].times == ["1104", "1755"]
    assert skipped(LOG) == 3
    assert parse_line("0612 HW 3.42 north quay") == ("0612", "HW", 3.42, "north quay")
    assert parse_line("2400 HW 3.42 north quay") is None
    assert parse_line("0612 HW 3.42") is None
    assert digest([]) == {}
    assert report([]) == "skipped 0 unreadable lines"
    assert LOG[3] == "bad line"  # the log is untouched
    print("All checks passed.")
