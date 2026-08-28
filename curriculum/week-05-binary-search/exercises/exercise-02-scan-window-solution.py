"""exercise-02-scan-window-solution.py - the parcel-hub scan window.

One lower-bound helper, called twice, returns the half-open slice bounds of
every scan in a single minute. A miss comes back as an empty slice sitting at
the insertion point, so the caller never has to special-case it.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
SHIFT_LOG: list[int] = [61, 61, 61, 64, 64, 70]


# ---- Your task ----
def lower_bound(minutes: list[int], minute: int) -> int:
    """Return the first index whose scan minute is >= `minute`.

    Args:
        minutes: Scan minutes, non-decreasing, duplicates expected.
        minute: The minute to place.

    Returns:
        The index at which `minute` would be written to keep the log ordered.
        That is len(minutes) when every scan is earlier.
    """
    lo, hi = 0, len(minutes)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if minutes[mid] < minute:
            lo = mid + 1  # mid tested False, so exclude it
        else:
            hi = mid  # hi is exclusive, so mid is still a candidate
    return lo


def scan_window(minutes: list[int], minute: int) -> tuple[int, int]:
    """Return (start, end) with minutes[start:end] the run for `minute`.

    Args:
        minutes: Scan minutes, non-decreasing.
        minute: The minute the auditor asked for.

    Returns:
        Half-open slice bounds. On a miss both bounds are the insertion
        point, which makes the slice empty and still valid.
    """
    return lower_bound(minutes, minute), lower_bound(minutes, minute + 1)


# ---- Self-check ----
if __name__ == "__main__":
    for wanted in (64, 61, 70, 62, 99):
        start, end = scan_window(SHIFT_LOG, wanted)
        print(f"minute {wanted:3d} -> ({start}, {end})  count {end - start}  {SHIFT_LOG[start:end]}")

    assert scan_window(SHIFT_LOG, 64) == (3, 5)
    assert scan_window(SHIFT_LOG, 61) == (0, 3)
    assert scan_window(SHIFT_LOG, 70) == (5, 6)
    assert scan_window(SHIFT_LOG, 62) == (3, 3)
    assert scan_window(SHIFT_LOG, 0) == (0, 0)
    assert scan_window(SHIFT_LOG, 99) == (6, 6)
    assert scan_window([300, 300, 300, 300], 300) == (0, 4)
    assert scan_window([], 5) == (0, 0)
    assert SHIFT_LOG[0] == 61  # the log was never rearranged
    print("All checks passed.")
