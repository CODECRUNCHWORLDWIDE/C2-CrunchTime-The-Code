"""exercise-01-ferry-ramp-manifests-solution.py — the ramp loading table.

The Kelbray Sound ferry loads through one stern ramp, in stints of 1, 2 or 3
vehicles. `plan_counts(capacity)` returns the whole prefix table: how many
distinct stint sequences load exactly k vehicles, for every k from 0 to
`capacity`.

The file shows the same count three ways, in the order you should write them:

    1. a plain recursion, which recomputes the same answers over and over,
    2. the same recursion with `functools.cache` bolted on,
    3. a bottom-up table, which is what the contract actually asks for.

Running it prints the table, then the call counts that make the difference
between (1) and (2) visible, then a consistency check at scale.
"""

from __future__ import annotations

import functools

# A stint moves one, two or three vehicles. Three abreast is the widest the
# ramp takes, so the recurrence has three terms and not two.
STINT_SIZES = (1, 2, 3)


def count_calls(func):
    """Wrap `func` so `func.calls` counts how many times its body ran."""

    @functools.wraps(func)
    def wrapper(*args):
        wrapper.calls += 1
        return func(*args)

    wrapper.calls = 0
    return wrapper


@count_calls
def naive_plan_count(remaining: int) -> int:
    """Count loading plans for `remaining` vehicles, remembering nothing.

    Correct, and unusably slow. Every call re-derives answers it has already
    derived, because nothing is written down between calls.
    """
    if remaining == 0:
        return 1
    return sum(
        naive_plan_count(remaining - size)
        for size in STINT_SIZES
        if size <= remaining
    )


@functools.cache
@count_calls
def cached_plan_count(remaining: int) -> int:
    """The same recursion, with every answer written down the first time.

    `functools.cache` sits outside the counter, so `cached_plan_count.calls`
    counts only the calls that actually reached the body — the misses.
    """
    if remaining == 0:
        return 1
    return sum(
        cached_plan_count(remaining - size)
        for size in STINT_SIZES
        if size <= remaining
    )


def plan_counts(capacity: int) -> list[int]:
    """Return the loading-plan count for every deck size from 0 to capacity.

    Args:
        capacity: How many vehicles the deck holds. Never negative.

    Returns:
        A list of length `capacity + 1`. Entry k is the number of distinct
        stint sequences that load exactly k vehicles. Entry 0 is 1, because
        the empty sequence loads nothing and is a plan.

    Raises:
        ValueError: If `capacity` is negative.
    """
    if capacity < 0:
        raise ValueError(f"capacity must not be negative, got {capacity}")

    plans = [0] * (capacity + 1)
    plans[0] = 1
    for deck in range(1, capacity + 1):
        total = 0
        for size in STINT_SIZES:
            if size <= deck:  # guard, or plans[-1] silently reads the last entry
                total += plans[deck - size]
        plans[deck] = total
    return plans


def _report() -> None:
    """Print the table, the call counts, and the scale check."""
    table = plan_counts(8)
    print("deck  plans")
    for deck, count in enumerate(table):
        print(f"{deck:>4}  {count}")

    probe = 18
    naive_plan_count.calls = 0
    cached_plan_count.cache_clear()
    cached_plan_count.__wrapped__.calls = 0

    naive_answer = naive_plan_count(probe)
    cached_answer = cached_plan_count(probe)

    print()
    print(f"plan_counts({probe})[-1]      = {plan_counts(probe)[-1]}")
    print(f"naive recursion  calls  = {naive_plan_count.calls}")
    print(f"cached recursion calls  = {cached_plan_count.__wrapped__.calls}")
    print(f"bottom-up table  reads  = {3 * probe - 3}")

    assert naive_answer == cached_answer == plan_counts(probe)[-1]

    assert plan_counts(0) == [1]
    assert plan_counts(1) == [1, 1]
    assert plan_counts(2) == [1, 1, 2]
    assert plan_counts(3) == [1, 1, 2, 4]
    assert plan_counts(4) == [1, 1, 2, 4, 7]  # a two-term recurrence says 5
    assert plan_counts(5) == [1, 1, 2, 4, 7, 13]

    big = plan_counts(300)
    assert len(big) == 301
    assert all(isinstance(value, int) for value in big)
    assert big[300] == big[299] + big[298] + big[297]
    print(f"plan_counts(300)[-1] has {len(str(big[300]))} digits")

    try:
        plan_counts(-1)
    except ValueError as problem:
        print(f"plan_counts(-1) raises ValueError: {problem}")

    print("All checks passed.")


if __name__ == "__main__":
    _report()
