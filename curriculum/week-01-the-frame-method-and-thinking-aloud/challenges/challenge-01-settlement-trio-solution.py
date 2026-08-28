"""challenge-01-settlement-trio-solution.py — explaining a suspense balance.

Sort the ledger, pin each amount in turn, and converge two pointers over the
tail for the pair that completes the trio. Three duplicate suppressions —
one on the pin, one on each pointer after a match — turn index triples into
distinct amount triples.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""


def settlement_trios(amounts: list[int], suspense: int) -> list[tuple[int, int, int]]:
    """Find every distinct way three parked entries explain the balance.

    Args:
        amounts: The suspense account in ledger order, cents. Credits are
            negative. The caller's list is not modified.
        suspense: The balance the three amounts must sum to. Rarely zero.

    Returns:
        Every distinct (a, b, c) with a <= b <= c, drawn from three distinct
        ledger positions, summing to `suspense`. Sorted within each triple
        and across triples. Empty list when nothing works.
    """
    ledger = sorted(amounts)
    results: list[tuple[int, int, int]] = []

    for pin in range(len(ledger) - 2):
        if pin > 0 and ledger[pin] == ledger[pin - 1]:
            continue

        pair_target = suspense - ledger[pin]
        left, right = pin + 1, len(ledger) - 1
        while left < right:
            total = ledger[left] + ledger[right]
            if total < pair_target:
                left += 1
            elif total > pair_target:
                right -= 1
            else:
                results.append((ledger[pin], ledger[left], ledger[right]))
                left += 1
                right -= 1
                while left < right and ledger[left] == ledger[left - 1]:
                    left += 1
                while left < right and ledger[right] == ledger[right + 1]:
                    right -= 1

    return results


# ---- Self-check ----
if __name__ == "__main__":
    books = [
        ([-5, -1, 0, 1, 4, 6], 0),
        ([-2, -2, 0, 2, 2, 4], 0),
        ([1, 3, 5, 7, 9], 15),
        ([-7, -3, -3, 10, 6], 0),
        ([5, 5, 5, 1, 1, 9], 15),
        ([2, 2, 2, 2], 6),
        ([3, 3], 9),
        ([], 0),
        ([1, 2, 4, 8], 100),
    ]
    for amounts, suspense in books:
        trios = settlement_trios(amounts, suspense)
        print(f"suspense {suspense:>4}  {len(trios)} explanation(s)  {trios}")

    assert settlement_trios([-5, -1, 0, 1, 4, 6], 0) == [(-5, -1, 6), (-5, 1, 4), (-1, 0, 1)]
    assert settlement_trios([-2, -2, 0, 2, 2, 4], 0) == [(-2, -2, 4), (-2, 0, 2)]
    assert settlement_trios([1, 3, 5, 7, 9], 15) == [(1, 5, 9), (3, 5, 7)]
    assert settlement_trios([-7, -3, -3, 10, 6], 0) == [(-7, -3, 10), (-3, -3, 6)]
    assert settlement_trios([5, 5, 5, 1, 1, 9], 15) == [(1, 5, 9), (5, 5, 5)]
    assert settlement_trios([2, 2, 2, 2], 6) == [(2, 2, 2)]
    assert settlement_trios([0, 0, 0, 0], 0) == [(0, 0, 0)]
    assert settlement_trios([3, 3, 3], 9) == [(3, 3, 3)]
    assert settlement_trios([3, 3], 9) == []
    assert settlement_trios([], 0) == []
    assert settlement_trios([1, 2, 4, 8], 100) == []

    ledger_order = [-7, -3, -3, 10, 6]
    settlement_trios(ledger_order, 0)
    assert ledger_order == [-7, -3, -3, 10, 6]  # the caller's ledger is not sorted
    print("All checks passed.")
