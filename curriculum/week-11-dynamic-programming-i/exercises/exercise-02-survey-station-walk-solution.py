"""exercise-02-survey-station-walk-solution.py — the take-or-skip walk.

Rock pools sit in a line along the Kelbray shore. Surveying a pool scares the
wildlife out of the pools either side of it, so no two neighbouring pools can
both be surveyed. Record as many species as possible; among the plans that
record the most, use the fewest pools.

`best_survey` returns `(species, pools_used)`.

The file carries the same rule twice — once as a memoized recursion and once as
a bottom-up table that keeps only two entries — and checks that they agree.
"""

from __future__ import annotations

import functools

# One stretch of shore, west to east. Each number is the species count found
# in a trial dip at that pool.
KELBRAY_SHORE = (4, 9, 3, 8, 2, 6, 6, 1)


def better(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    """Pick the better of two (species, pools_used) plans.

    More species wins. On a tie, fewer pools wins. On a tie in both, the
    left-hand plan wins, so the choice is never left to chance.
    """
    if right[0] > left[0]:
        return right
    if right[0] == left[0] and right[1] < left[1]:
        return right
    return left


def best_survey_cached(counts: tuple[int, ...]) -> tuple[int, int]:
    """Top-down: the recurrence said out loud, with every answer remembered."""

    @functools.cache
    def best_from(pool: int) -> tuple[int, int]:
        """The best plan using only pools `pool` and eastwards."""
        if pool >= len(counts):
            return (0, 0)
        skip = best_from(pool + 1)
        taken_species, taken_pools = best_from(pool + 2)
        take = (taken_species + counts[pool], taken_pools + 1)
        return better(skip, take)

    return best_from(0)


def best_survey(counts: tuple[int, ...]) -> tuple[int, int]:
    """Return the best survey plan for a line of rock pools.

    Args:
        counts: Species counts, west to east. Every count is zero or more.

    Returns:
        A pair (species, pools_used). The species total is the largest
        obtainable without surveying two neighbouring pools; pools_used is
        the smallest number of pools that reaches that total.

    Raises:
        ValueError: If any count is negative.
    """
    if any(count < 0 for count in counts):
        raise ValueError("a species count cannot be negative")

    # two_back is the best plan for the pools before the previous one,
    # one_back is the best plan for everything up to the previous one.
    two_back = (0, 0)
    one_back = (0, 0)
    for count in counts:
        take = (two_back[0] + count, two_back[1] + 1)
        two_back, one_back = one_back, better(one_back, take)
    return one_back


def survey_table(counts: tuple[int, ...]) -> list[tuple[int, int]]:
    """The full bottom-up table, kept for the walkthrough on the page.

    Entry i is the best plan considering the first i pools only, so entry 0
    is the empty plan and the last entry is the answer.
    """
    table: list[tuple[int, int]] = [(0, 0)] * (len(counts) + 1)
    for i in range(1, len(counts) + 1):
        two_back = table[i - 2] if i >= 2 else (0, 0)
        take = (two_back[0] + counts[i - 1], two_back[1] + 1)
        table[i] = better(table[i - 1], take)
    return table


def _report() -> None:
    """Print the table walk, the checks, and the agreement between the two."""
    print("pools considered  best plan (species, pools)")
    for i, plan in enumerate(survey_table(KELBRAY_SHORE)):
        print(f"{i:>16}  {plan}")

    cases: list[tuple[tuple[int, ...], tuple[int, int]]] = [
        ((), (0, 0)),                       # no shore at all
        ((0,), (0, 0)),                     # a barren pool is not worth a dip
        ((7,), (7, 1)),
        ((7, 7), (7, 1)),                   # neighbours: only one may be taken
        ((4, 0, 0, 4), (8, 2)),             # the tie-break earns its keep here
        ((0, 0, 0), (0, 0)),
        ((6, 1, 5, 1, 6), (17, 3)),
        (KELBRAY_SHORE, (24, 4)),
    ]
    print()
    for counts, expected in cases:
        rolled = best_survey(counts)
        recursed = best_survey_cached(counts)
        tabled = survey_table(counts)[-1]
        assert rolled == expected, f"{counts} -> {rolled}, expected {expected}"
        assert recursed == expected, f"cached disagrees on {counts}"
        assert tabled == expected, f"table disagrees on {counts}"
        print(f"best_survey({counts}) == {expected}")

    try:
        best_survey((3, -1))
    except ValueError as problem:
        print(f"\nbest_survey((3, -1)) raises ValueError: {problem}")

    print("All checks passed.")


if __name__ == "__main__":
    _report()
