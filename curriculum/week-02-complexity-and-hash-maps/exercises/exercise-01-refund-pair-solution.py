"""exercise-01-refund-pair-solution.py — the earliest-completing refund pair.

One pass over the charge history, carrying a map from amount to the earliest
position that amount was seen at. At every charge we ask one question: have I
already seen the amount that would complete this one?

Time: O(n) — one pass, each dict operation O(1) average.
Space: O(n) — the map holds at most one entry per distinct amount.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""


def find_refund_pair(charges: list[int], refund_total: int) -> tuple[int, int] | None:
    """Return the earliest-completing pair of positions summing to the total.

    Args:
        charges: Charge amounts in cents, in the order they were made.
        refund_total: The disputed refund total, in cents.

    Returns:
        (i, j) with i < j and charges[i] + charges[j] == refund_total,
        choosing the pair whose later position j is smallest. None if no
        pair sums to the total.
    """
    earliest_at: dict[int, int] = {}
    for position, amount in enumerate(charges):
        complement = refund_total - amount
        if complement in earliest_at:
            return (earliest_at[complement], position)
        if amount not in earliest_at:
            earliest_at[amount] = position
    return None


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[int], int, tuple[int, int] | None]] = [
        ([400, 150, 250, 300], 550, (0, 1)),
        ([100, 450, 450, 100], 550, (0, 1)),
        ([700, 700], 1400, (0, 1)),
        ([700], 1400, None),
        ([], 0, None),
        ([-200, 500, 200], 0, (0, 2)),
        ([100, 200, 300], 1000, None),
    ]

    for charges, total, expected in cases:
        found = find_refund_pair(charges, total)
        assert found == expected, (charges, total, found, expected)
        shown = "none" if found is None else f"{found[0]},{found[1]}"
        print(f"total {total:5d}  ->  {shown:>6}   from {charges}")

    print("All checks passed.")
