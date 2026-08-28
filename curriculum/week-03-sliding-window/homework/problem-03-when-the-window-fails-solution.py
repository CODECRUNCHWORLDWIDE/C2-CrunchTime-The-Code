"""problem-03-when-the-window-fails-solution.py — the pattern that does not fit.

A pallet loader logs crate weights in the order they come off the truck. A
pallet takes exactly two crates, and their weights must add up to the pallet
allowance. The two crates may sit anywhere in the log, with any number of
other crates between them.

That "anywhere" is the whole point. A sliding window only ever looks at a
contiguous stretch, so a window that checks neighbouring crates answers a
different question and misses real pairs. This file implements both — the
lookup that is right, and the window that is wrong — and prints the log where
they disagree, so the rejection is something you can run rather than a claim
you have to take on trust.

The self-checks are the starter's, unchanged. When they all pass the file
prints "All checks passed."
"""


def pallet_pair(weights: list[int], allowance: int) -> tuple[int, int] | None:
    """Return the positions of two crates whose weights fill the allowance.

    Args:
        weights: Crate weights in kilograms, in unloading order.
        allowance: The pallet's total capacity in kilograms.

    Returns:
        (i, j) with i < j, choosing the pair that completes earliest — the
        smallest j — and, among pairs sharing that j, the smallest i. None
        when no two crates add up to the allowance. A crate is never paired
        with itself.
    """
    first_seen: dict[int, int] = {}

    for j, weight in enumerate(weights):
        partner = allowance - weight
        if partner in first_seen:
            return (first_seen[partner], j)
        if weight not in first_seen:
            first_seen[weight] = j

    return None


def neighbouring_pair(weights: list[int], allowance: int) -> tuple[int, int] | None:
    """The wrong pattern, kept so you can watch it fail.

    A two-wide sliding window can only ever compare crates that touch, so it
    answers "are there two ADJACENT crates that fill the pallet?" — a
    different question from the one the loader asked.

    Args:
        weights: Crate weights in kilograms, in unloading order.
        allowance: The pallet's total capacity in kilograms.

    Returns:
        The first adjacent pair that fills the allowance, or None.
    """
    for i in range(len(weights) - 1):
        if weights[i] + weights[i + 1] == allowance:
            return (i, i + 1)
    return None


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[int], int]] = [
        ([310, 240, 90, 150, 260], 400),
        ([200, 100, 200], 400),
        ([120, 280, 200, 200], 400),
        ([200, 200, 200], 400),
        ([10, 20], 100),
        ([400], 400),
        ([], 400),
    ]

    print(f"{'log':<28} {'allowance':>9}  {'lookup':>10}  {'window':>10}  agree")
    for weights, allowance in cases:
        right = pallet_pair(weights, allowance)
        wrong = neighbouring_pair(weights, allowance)
        print(f"{str(weights):<28} {allowance:>9}  {str(right):>10}  {str(wrong):>10}  {'yes' if right == wrong else 'NO'}")
    print()

    weights, allowance = cases[0]
    i, j = pallet_pair(weights, allowance)
    print(f"the window misses {weights[i]} at index {i} plus {weights[j]} at index {j},")
    print(f"because {weights[i + 1]} sits between them and a window cannot skip it.")
    print()

    assert pallet_pair([310, 240, 90, 150, 260], 400) == (0, 2)
    assert pallet_pair([200, 100, 200], 400) == (0, 2)
    assert pallet_pair([120, 280, 200, 200], 400) == (0, 1)
    assert pallet_pair([200, 200, 200], 400) == (0, 1)
    assert pallet_pair([10, 20], 100) is None
    assert pallet_pair([400], 400) is None
    assert pallet_pair([], 400) is None

    assert neighbouring_pair([310, 240, 90, 150, 260], 400) is None
    assert neighbouring_pair([200, 100, 200], 400) is None

    # Whatever the lookup returns is a real pair, and nothing completes sooner.
    for weights, allowance in cases:
        found = pallet_pair(weights, allowance)
        pairs = [
            (j, i)
            for j in range(len(weights))
            for i in range(j)
            if weights[i] + weights[j] == allowance
        ]
        if not pairs:
            assert found is None
            continue
        second, first = min(pairs)
        assert found == (first, second)

    print("All checks passed.")
