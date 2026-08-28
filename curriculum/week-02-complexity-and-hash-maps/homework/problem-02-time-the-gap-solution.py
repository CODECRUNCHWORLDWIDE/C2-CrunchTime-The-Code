"""problem-02-time-the-gap-solution.py — watching a complexity class change.

Two solutions to Exercise 1's refund-pair problem, side by side on the same
input: the nested scan that compares every pair, and the one-pass hash map.
Both are instrumented, so they report how many charge-to-charge comparisons
each one actually performed.

The counts go to stdout, because they are the same on every machine and are
the thing the argument rests on. The wall-clock seconds go to stderr, because
they are different on every machine and would make this file's output
unreproducible. That split is worth keeping: it is why
`python problem-02-time-the-gap-solution.py > counts.txt` saves the table and
leaves the timings on your screen.

Time: the nested scan is O(n^2), the hash map is O(n).
Space: the nested scan is O(1), the hash map is O(n).
"""

import random
import sys
import time


def unsolvable_charges(n: int, seed: int = 20260221) -> tuple[list[int], int]:
    """Return n charges that no pair can ever complete, plus that total.

    Every charge is even and the refund total is odd, so no two charges can
    sum to it. Neither implementation can exit early, so the comparison
    measures the full scan instead of measuring luck.

    Args:
        n: How many charges to generate.
        seed: Fixed so every run of this file produces the same input.

    Returns:
        (charges, refund_total).
    """
    rng = random.Random(seed)
    charges = [2 * rng.randint(-25_000, 25_000) for _ in range(n)]
    return charges, 1


def find_refund_pair_nested(
    charges: list[int], refund_total: int
) -> tuple[tuple[int, int] | None, int]:
    """The nested scan. O(n^2) time, O(1) space.

    Args:
        charges: Charge amounts in cents.
        refund_total: The disputed refund total.

    Returns:
        (pair or None, number of charge-to-charge comparisons performed).
    """
    comparisons = 0
    for later in range(len(charges)):
        for earlier in range(later):
            comparisons += 1
            if charges[earlier] + charges[later] == refund_total:
                return ((earlier, later), comparisons)
    return (None, comparisons)


def find_refund_pair_hashed(
    charges: list[int], refund_total: int
) -> tuple[tuple[int, int] | None, int]:
    """The one-pass hash map. O(n) time, O(n) space.

    Args:
        charges: Charge amounts in cents.
        refund_total: The disputed refund total.

    Returns:
        (pair or None, number of map lookups performed).
    """
    lookups = 0
    earliest_at: dict[int, int] = {}
    for position, amount in enumerate(charges):
        lookups += 1
        complement = refund_total - amount
        if complement in earliest_at:
            return ((earliest_at[complement], position), lookups)
        if amount not in earliest_at:
            earliest_at[amount] = position
    return (None, lookups)


def median_seconds(runner, charges: list[int], refund_total: int, runs: int = 3) -> float:
    """Return the median wall-clock time of `runs` calls, in seconds.

    The median, not the first run: the first run pays for warm-up and
    allocation that the comparison does not care about.
    """
    timings = []
    for _ in range(runs):
        started = time.perf_counter()
        runner(charges, refund_total)
        timings.append(time.perf_counter() - started)
    return sorted(timings)[len(timings) // 2]


# ---- Self-check ----
if __name__ == "__main__":
    sizes = [250, 1_000, 4_000]

    print("n            nested comparisons   hashed lookups     ratio")
    previous: tuple[int, int] | None = None
    for n in sizes:
        charges, refund_total = unsolvable_charges(n)

        nested_pair, nested_ops = find_refund_pair_nested(charges, refund_total)
        hashed_pair, hashed_ops = find_refund_pair_hashed(charges, refund_total)

        assert nested_pair is None, "the generator promised no pair completes"
        assert hashed_pair is None, "both implementations must agree"
        assert nested_ops == n * (n - 1) // 2
        assert hashed_ops == n

        print(f"{n:8d} {nested_ops:20d} {hashed_ops:16d} {nested_ops / hashed_ops:9.1f}")

        print(
            f"n={n}: nested {median_seconds(find_refund_pair_nested, charges, refund_total):.4f}s, "
            f"hashed {median_seconds(find_refund_pair_hashed, charges, refund_total):.4f}s",
            file=sys.stderr,
        )

        if previous is not None:
            grew_by = n / previous[0]
            nested_grew = nested_ops / previous[1]
            print(
                f"         n x{grew_by:.0f}  ->  nested work x{nested_grew:.1f}, "
                f"hashed work x{grew_by:.0f}"
            )
        previous = (n, nested_ops)

    print()
    print("Quadruple n and the linear column quadruples; the quadratic one grows")
    print("about sixteenfold. That is the whole difference between O(n) and O(n^2),")
    print("and it is a fact about the algorithms, not about this machine.")
    print("All checks passed.")
