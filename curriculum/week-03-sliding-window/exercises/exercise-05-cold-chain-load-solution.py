"""exercise-05-cold-chain-load-solution.py — the longest loadable run.

A depot loads a refrigerated van straight off a conveyor. Each compartment is
set to exactly one temperature class, so a contiguous run of packages is
loadable exactly when it holds at most k distinct classes.

This is the at-most-K-distinct template, and it is the most reusable shape of
the week: a frequency table inside the window, a shrink loop that runs while
the table is too wide, and a record taken once the invariant holds again.
`k` is a parameter, never a hard-coded number.

The self-checks are the starter's, unchanged. When they all pass the file
prints "All checks passed."
"""


def longest_load(classes: list[str], k: int) -> tuple[int, int]:
    """Return the longest run of packages spanning at most k classes.

    Args:
        classes: Temperature class of each package, in conveyor order.
        k: How many compartments the van has, so how many distinct classes a
            single run may contain.

    Returns:
        (start, count) for the longest loadable run. Ties go to the larger
        start. (-1, 0) when the conveyor is empty or the van has no
        compartments.
    """
    if not classes or k == 0:
        return (-1, 0)

    counts: dict[str, int] = {}
    left = 0
    best = (-1, 0)

    for right, package in enumerate(classes):
        counts[package] = counts.get(package, 0) + 1

        while len(counts) > k:
            leaving = classes[left]
            counts[leaving] -= 1
            if counts[leaving] == 0:
                del counts[leaving]
            left += 1

        # The invariant holds again, so this window is a real candidate. The
        # >= is the tie-break: a run of equal length but a later start wins.
        if right - left + 1 >= best[1]:
            best = (left, right - left + 1)

    return best


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[str], int]] = [
        (["chilled", "frozen", "chilled", "ambient", "ambient", "frozen"], 2),
        (["chilled", "frozen", "chilled", "ambient"], 2),
        (["dry", "dry", "cold", "cold", "cold"], 1),
        (["ambient", "frozen"], 5),
        (["ambient"], 0),
        ([], 3),
    ]
    for conveyor, compartments in cases:
        start, count = longest_load(conveyor, compartments)
        run = conveyor[start : start + count] if start >= 0 else []
        print(f"k={compartments}  {str(conveyor):<62} -> ({start}, {count}) {run}")
    print()

    assert longest_load(["chilled", "frozen", "chilled", "ambient", "ambient", "frozen"], 2) == (3, 3)
    assert longest_load(["chilled", "frozen", "chilled", "ambient"], 2) == (0, 3)
    assert longest_load(["dry", "dry", "cold", "cold", "cold"], 1) == (2, 3)
    assert longest_load(["ambient", "frozen"], 5) == (0, 2)
    assert longest_load(["ambient"], 0) == (-1, 0)
    assert longest_load([], 3) == (-1, 0)

    # The run that comes back is loadable, and no longer run is.
    for conveyor, compartments in cases:
        start, count = longest_load(conveyor, compartments)
        if start < 0:
            continue
        assert len(set(conveyor[start : start + count])) <= compartments
        for i in range(len(conveyor)):
            for j in range(i + 1, len(conveyor) + 1):
                if len(set(conveyor[i:j])) <= compartments:
                    assert j - i <= count

    print("All checks passed.")
