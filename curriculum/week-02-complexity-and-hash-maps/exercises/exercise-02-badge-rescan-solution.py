"""exercise-02-badge-rescan-solution.py — the first repeated badge tap.

One pass over the tap log, carrying a set of the badges seen so far. At every
tap we ask one question: have I seen this badge already? The first time the
answer is yes, that tap's index is the answer.

Time: O(n) worst case, O(1) best case when the second tap repeats the first.
Space: O(n) — one entry per distinct badge, never O(10_000_000).

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""


def first_repeated_scan(badge_ids: list[int]) -> int | None:
    """Return the index of the first tap whose badge was already tapped.

    Args:
        badge_ids: Badge numbers in the order they were tapped.

    Returns:
        The smallest index i such that badge_ids[i] appears in badge_ids[:i],
        or None if every badge in the log is distinct.
    """
    seen: set[int] = set()
    for index, badge in enumerate(badge_ids):
        if badge in seen:
            return index
        seen.add(badge)
    return None


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[int], int | None]] = [
        ([4820, 1173, 4820, 9002], 2),
        ([4820, 1173, 9002], None),
        ([], None),
        ([7715], None),
        ([3301, 3301, 3301], 1),
        ([5, 9, 12, 9, 5], 3),
    ]

    for log, expected in cases:
        found = first_repeated_scan(log)
        assert found == expected, (log, found, expected)
        verdict = "clean" if found is None else f"review from tap {found}"
        counted = f"{len(log)} tap" + ("" if len(log) == 1 else "s")
        print(f"{counted:<7} ->  {verdict:<20}  {log}")

    print("All checks passed.")
