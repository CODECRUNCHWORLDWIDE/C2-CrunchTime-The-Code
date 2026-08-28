"""exercise-02-longest-clean-run-solution.py — the longest clean run.

A stamping press marks each part with the ID of the die that made it. Between
recalibrations a die may not be used twice, so a clean run is a stretch of
consecutive parts in which no die ID repeats.

One pass, two indices that only ever move forward, and a dict remembering
where each die was last seen. The answer is a half-open span, so the caller
can slice the log with it directly.

The self-checks are the starter's, unchanged. When they all pass the file
prints "All checks passed."
"""


def longest_clean_run(stamps: list[int]) -> tuple[int, int]:
    """Return the longest stretch of parts with no repeated die ID.

    Args:
        stamps: Die IDs, one per part, in production order.

    Returns:
        A half-open span (start, end) with stamps[start:end] the longest clean
        run. Ties go to the smaller start. An empty log returns (0, 0).
    """
    last_index: dict[int, int] = {}
    left = 0
    best = (0, 0)

    for right, die in enumerate(stamps):
        seen_at = last_index.get(die)
        if seen_at is not None and seen_at >= left:
            left = seen_at + 1
        last_index[die] = right
        if right - left + 1 > best[1] - best[0]:
            best = (left, right + 1)

    return best


# ---- Self-check ----
if __name__ == "__main__":
    logs: list[list[int]] = [
        [7, 3, 9, 3, 4, 1, 9],
        [1, 2, 2, 1],
        [2, 1, 2, 3],
        [5, 5, 5, 5],
        [4],
        [],
    ]
    for log in logs:
        start, end = longest_clean_run(log)
        print(f"{str(log):<22} -> span ({start}, {end}) = {log[start:end]}")
    print()

    assert longest_clean_run([7, 3, 9, 3, 4, 1, 9]) == (2, 6)
    assert longest_clean_run([1, 2, 2, 1]) == (0, 2)
    assert longest_clean_run([2, 1, 2, 3]) == (1, 4)
    assert longest_clean_run([5, 5, 5, 5]) == (0, 1)
    assert longest_clean_run([4]) == (0, 1)
    assert longest_clean_run([]) == (0, 0)

    # Whatever span comes back really is clean, and really is maximal.
    for log in logs:
        start, end = longest_clean_run(log)
        run = log[start:end]
        assert len(set(run)) == len(run), f"{run} repeats a die"
        for begin in range(len(log)):
            for stop in range(begin + 1, len(log) + 1):
                candidate = log[begin:stop]
                if len(set(candidate)) == len(candidate):
                    assert len(candidate) <= end - start

    print("All checks passed.")
