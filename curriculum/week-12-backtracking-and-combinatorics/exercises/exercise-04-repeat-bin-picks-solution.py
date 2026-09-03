"""exercise-04-repeat-bin-picks-solution.py - picking from a bin with repeats in it.

A clay store keeps a bin of body samples. Some samples in the bin are
identical - two bags of the same stoneware are the same stoneware, and a test
using one is the same test as a test using the other.

List every DISTINCT set of samples that could be taken from the bin.

Exercise 1 walked a shelf of distinct glazes and every subset came out once. A
bin with repeats in it breaks that: the walk finds one set per POSITION, and
two positions holding the same sample produce the same set twice.

The fix is two lines and both are needed:

    sort the bin        so identical samples sit next to each other
    skip a repeat       at the same level of the walk only

The second half of that second line is the part people get wrong. Skipping a
repeat everywhere removes sets that genuinely use the sample twice; skipping it
only when it is a SIBLING of a choice already made at this level removes
exactly the duplicates and nothing else.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
# Two bags of stoneware, two of porcelain, one of raku.
BIN: tuple[str, ...] = ("stoneware", "porcelain", "stoneware", "raku", "porcelain")


# ---- Your task ----
def distinct_picks(samples: tuple[str, ...]) -> list[list[str]]:
    """Return every distinct set of samples that could be taken from the bin.

    Args:
        samples: The bin, which may hold the same sample more than once.

    Returns:
        Every distinct subset, each sorted, with the empty set first. Two picks
        are the same when they hold the same samples the same number of times,
        however the bin was ordered.
    """
    bin_order = sorted(samples)
    found: list[list[str]] = []
    trail: list[str] = []

    def walk(index: int) -> None:
        found.append(list(trail))
        for next_index in range(index, len(bin_order)):
            # Skip a repeat only when it is a sibling of a choice already made
            # at THIS level. `next_index > index` is what makes it "at this
            # level"; without it, a pick using the sample twice disappears too.
            if next_index > index and bin_order[next_index] == bin_order[next_index - 1]:
                continue
            trail.append(bin_order[next_index])
            walk(next_index + 1)
            trail.pop()

    walk(0)
    return found


def picks_with_duplicates(samples: tuple[str, ...]) -> list[list[str]]:
    """The same walk without the skip, shipped to be compared.

    Args:
        samples: The bin.

    Returns:
        One pick per set of positions rather than per set of samples, so
        identical picks appear more than once. Its length is 2 to the power of
        the bin size, whatever the bin holds.
    """
    bin_order = sorted(samples)
    found: list[list[str]] = []
    trail: list[str] = []

    def walk(index: int) -> None:
        found.append(list(trail))
        for next_index in range(index, len(bin_order)):
            trail.append(bin_order[next_index])
            walk(next_index + 1)
            trail.pop()

    walk(0)
    return found


def picks_over_skipped(samples: tuple[str, ...]) -> list[list[str]]:
    """The walk that skips a repeat everywhere, shipped to be compared.

    Args:
        samples: The bin.

    Returns:
        Its answer, which is missing every pick that uses a repeated sample
        more than once - so a bin of two stoneware bags never produces the pick
        holding both - and which pads the count back out with duplicates. On
        the shipped bin it returns exactly as many picks as the correct walk
        does, and they are not the same picks. This is the plausible wrong fix
        and it fails silently, which is why it is worth running once.
    """
    bin_order = sorted(samples)
    found: list[list[str]] = []
    trail: list[str] = []
    seen_at_all: set[str] = set()

    def walk(index: int) -> None:
        found.append(list(trail))
        for next_index in range(index, len(bin_order)):
            sample = bin_order[next_index]
            if sample in seen_at_all:
                continue
            seen_at_all.add(sample)
            trail.append(sample)
            walk(next_index + 1)
            trail.pop()
            seen_at_all.discard(sample)

    walk(0)
    return found


def pick_count(samples: tuple[str, ...]) -> int:
    """Return how many distinct picks exist, without enumerating them.

    For each distinct sample the bin holds `k` of, a pick may take 0 to `k` of
    them, so the answer is the product of `k + 1` over the distinct samples.

    Args:
        samples: The bin.

    Returns:
        The number of distinct picks. Kept beside the enumeration so the two
        can check each other - which is the only cheap test of a walk whose
        whole job is not to repeat itself.
    """
    counts: dict[str, int] = {}
    for sample in samples:
        counts[sample] = counts.get(sample, 0) + 1
    total = 1
    for count in counts.values():
        total *= count + 1
    return total


# ---- Self-check ----
if __name__ == "__main__":
    print(f"BIN  {list(BIN)}")
    print()

    picks = distinct_picks(BIN)
    print("EVERY DISTINCT PICK")
    for pick in picks:
        shown = ", ".join(pick) if pick else "(none)"
        print(f"    {len(pick)}  {shown}")
    print()

    loose = picks_with_duplicates(BIN)
    over = picks_over_skipped(BIN)
    print("THE THREE WALKS")
    print(f"    distinct picks        : {len(picks)}   (the answer)")
    print(f"    no skip at all        : {len(loose)}   (one per set of positions)")
    print(f"    skipping repeats always: {len(over)}   (same count, wrong picks)")
    print(f"      ...of which distinct  : {len({tuple(pick) for pick in over})}")
    print()

    # Two stoneware, two porcelain, one raku: 3 * 3 * 2 = 18 distinct picks.
    assert len(picks) == pick_count(BIN) == 18

    # Every pick appears exactly once. That is the whole claim.
    assert len({tuple(pick) for pick in picks}) == len(picks)

    # The empty pick comes first.
    assert picks[0] == []

    # Picks that use a repeated sample twice must be present. This is what the
    # over-skipping version loses.
    assert ["stoneware", "stoneware"] in picks
    assert ["porcelain", "porcelain"] in picks

    # The unskipped walk finds 2 ** 5 = 32 picks, with repeats among them.
    assert len(loose) == 32
    assert len({tuple(pick) for pick in loose}) == len(picks)

    # The over-skipping walk is the nastiest of the three, because on this bin
    # it finds exactly as many picks as the right answer does - 18 - and they
    # are not the same 18. It never picks both stoneware bags, and it makes up
    # the numbers with duplicates of picks it has already found. A test that
    # only counted would pass it.
    assert len(over) == len(picks)
    assert ["stoneware", "stoneware"] not in over
    assert len({tuple(pick) for pick in over}) < len(picks)

    # A bin with no repeats behaves exactly like Exercise 1.
    assert len(distinct_picks(("a", "b", "c"))) == pick_count(("a", "b", "c")) == 8

    # A bin that is all one sample gives one pick per possible count, 0 to k.
    assert distinct_picks(("x", "x", "x")) == [[], ["x"], ["x", "x"], ["x", "x", "x"]]

    # An empty bin still has one pick: the empty one.
    assert distinct_picks(()) == [[]]

    # The order the bin arrives in makes no difference to the answer.
    shuffled = ("raku", "porcelain", "stoneware", "porcelain", "stoneware")
    assert distinct_picks(shuffled) == picks

    print("All checks passed.")
