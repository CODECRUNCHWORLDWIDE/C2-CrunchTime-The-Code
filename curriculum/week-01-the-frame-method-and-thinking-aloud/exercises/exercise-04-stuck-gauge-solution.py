"""exercise-04-stuck-gauge-solution.py — collapsing a stuck river gauge.

A read pointer visits every sample; a write pointer marks where the next
kept sample goes and only advances when a sample survives. Only adjacent
repeats collapse, because the river really does come back to a level it
held before.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""


def collapse_stuck_readings(levels: list[int]) -> int:
    """Collapse runs of equal adjacent samples in place, preserving order.

    Args:
        levels: The record, millimetres above datum. Rewritten in place so
            that levels[:kept] holds the collapsed series. Entries at or
            after `kept` are scratch and are deliberately left alone.

    Returns:
        The number of samples dropped, which is len(levels) - kept.
    """
    if not levels:
        return 0

    write = 1
    for read in range(1, len(levels)):
        if levels[read] != levels[write - 1]:
            levels[write] = levels[read]
            write += 1
    return len(levels) - write


# ---- Self-check ----
if __name__ == "__main__":
    records = [
        [412, 412, 412, 415, 415, 409],
        [300, 300, 305, 300],
        [777, 777, 777, 777],
        [500, 501, 502],
        [-2, -2, 0, 0, -2],
        [640],
        [],
    ]
    for levels in records:
        before = list(levels)
        dropped = collapse_stuck_readings(levels)
        kept = len(levels) - dropped
        print(f"dropped {dropped}  kept {levels[:kept]}  whole list {levels}  was {before}")

    record = [412, 412, 412, 415, 415, 409]
    assert collapse_stuck_readings(record) == 3
    assert record[:3] == [412, 415, 409]
    assert record == [412, 415, 409, 415, 415, 409]  # tail untouched on purpose

    wobble = [300, 300, 305, 300]
    assert collapse_stuck_readings(wobble) == 1
    assert wobble[:3] == [300, 305, 300]

    stuck = [777, 777, 777, 777]
    assert collapse_stuck_readings(stuck) == 3
    assert stuck == [777, 777, 777, 777]  # non-zero return, identical list

    assert collapse_stuck_readings([500, 501, 502]) == 0
    assert collapse_stuck_readings([-2, -2, 0, 0, -2]) == 2
    assert collapse_stuck_readings([640]) == 0
    assert collapse_stuck_readings([]) == 0
    print("All checks passed.")
