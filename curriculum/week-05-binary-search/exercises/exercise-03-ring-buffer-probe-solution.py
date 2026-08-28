"""exercise-03-ring-buffer-probe-solution.py - the turnstile ring buffer.

Two composed binary searches. The first finds the wrap point - the slot
holding the oldest row. The second searches the logical view that the wrap
point defines, and the logical index it lands on IS the row's age.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
# Write order 12, 19, 33, 47, 58, 61, 64, 70, wrapped so the oldest row
# sits in slot 4.
DUMP: list[int] = [58, 61, 64, 70, 12, 19, 33, 47]


# ---- Your task ----
def wrap_point(slots: list[int]) -> int:
    """Return the slot index holding the oldest reading id.

    Args:
        slots: A rotation of a strictly increasing list of ids. Not empty.

    Returns:
        The index of the smallest id, which is 0 when the dump never wrapped.
    """
    lo, hi = 0, len(slots) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if slots[mid] > slots[hi]:
            lo = mid + 1  # the wrap is strictly right of mid
        else:
            hi = mid  # mid is still a candidate for the oldest slot
    return lo


def rows_older_than(slots: list[int], reading_id: int) -> int | None:
    """Return the 0-based position of `reading_id` in write order.

    Args:
        slots: The physical dump, slot 0 first.
        reading_id: The id to locate.

    Returns:
        How many rows in the buffer are older than that row, or None when
        the id is not in the buffer at all.
    """
    n = len(slots)
    if n == 0:
        return None

    start = wrap_point(slots)
    lo, hi = 0, n - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        probe = slots[(start + mid) % n]
        if probe == reading_id:
            return mid
        if probe < reading_id:
            lo = mid + 1
        else:
            hi = mid - 1
    return None


# ---- Self-check ----
if __name__ == "__main__":
    print(f"wrap point: slot {wrap_point(DUMP)} holds id {DUMP[wrap_point(DUMP)]}")
    for wanted in (12, 70, 58, 50):
        print(f"id {wanted:3d} -> age {rows_older_than(DUMP, wanted)}")

    assert rows_older_than(DUMP, 12) == 0
    assert rows_older_than(DUMP, 70) == 7
    assert rows_older_than(DUMP, 58) == 4
    assert rows_older_than(DUMP, 50) is None
    assert rows_older_than([12, 19, 33, 47], 33) == 2
    assert rows_older_than([91, 7], 91) == 1
    assert rows_older_than([91, 7], 7) == 0
    assert rows_older_than([5], 5) == 0
    assert rows_older_than([5], 9) is None
    assert rows_older_than([], 5) is None
    assert DUMP[0] == 58  # the dump was never rebuilt
    print("All checks passed.")
