"""problem-04-duplicated-manifest-solution.py - rotated search with duplicates.

The same rotated buffer as the drill, with the distinctness guarantee taken
away. When the three probe points all read the same stamp, no O(1) test can
say which half holds the wrap, so the loop gives up ONE slot and retries -
and that is why the worst case is a linear scan, not a logarithmic one.

The self-checks at the bottom are the starter's, unchanged. They assert the
property `slots[result] == stamp` rather than a fixed slot, because a stamp
may sit in several slots and any of them is a correct answer. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
# Write order 8, 8, 8, 19, 33, 47, 47, 51, wrapped so the oldest row sits in
# slot 3.
MANIFEST: list[int] = [47, 47, 51, 8, 8, 8, 19, 33]


# ---- Your task ----
def find_stamp_slot(slots: list[int], stamp: int) -> int | None:
    """Return the physical slot of a row carrying `stamp`, or None.

    Args:
        slots: A rotation of a non-decreasing list of dock minutes.
            Duplicates are the normal shape of this data.
        stamp: The dock minute the supervisor is looking for.

    Returns:
        Any index i with slots[i] == stamp, or None when no row carries it.
    """
    lo, hi = 0, len(slots) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if slots[mid] == stamp:
            return mid
        if slots[lo] == slots[mid] == slots[hi]:
            lo += 1  # the probes learned nothing; pay one slot and retry
        elif slots[lo] <= slots[mid]:
            # the left half is genuinely sorted
            if slots[lo] <= stamp < slots[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            # the right half is genuinely sorted
            if slots[mid] < stamp <= slots[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return None


# ---- Self-check ----
if __name__ == "__main__":
    for wanted in (19, 51, 8, 20):
        print(f"stamp {wanted:3d} -> slot {find_stamp_slot(MANIFEST, wanted)}")

    for wanted in (19, 51, 33, 8, 47):
        slot = find_stamp_slot(MANIFEST, wanted)
        assert slot is not None and MANIFEST[slot] == wanted, (wanted, slot)
    assert find_stamp_slot(MANIFEST, 20) is None

    adversarial = [2, 2, 2, 0, 2]
    assert find_stamp_slot(adversarial, 0) == 3
    assert adversarial[find_stamp_slot(adversarial, 2)] == 2
    flat = [5, 5, 5, 5, 5]
    assert find_stamp_slot(flat, 9) is None
    assert flat[find_stamp_slot(flat, 5)] == 5
    assert find_stamp_slot([9], 9) == 0
    assert find_stamp_slot([9], 1) is None
    assert find_stamp_slot([], 7) is None
    assert MANIFEST[0] == 47  # the dump was never rebuilt
    print("All checks passed.")
