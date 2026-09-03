"""exercise-01-glaze-sample-set-solution.py - every set of glazes the studio could test.

A pottery keeps a shelf of glaze samples. Before a firing the studio picks some
subset of them to test together - possibly all of them, possibly none.

List every subset, and count them.

This is the backtracking template with the recording step in the one place that
surprises people: at EVERY node, not at the leaves. A subset is complete the
moment you stop adding to it, so there is no "finished" test to write - every
partial answer is also a whole answer.

The three lines of the template are here and nowhere else:

    choose    trail.append(glaze)
    explore   walk(index + 1)
    undo      trail.pop()

The undo is what people leave out, and leaving it out does not crash. It
produces subsets with extra glazes in them, and the count comes out right,
which is what makes it hard to spot.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
GLAZES: tuple[str, ...] = ("ash", "celadon", "tenmoku", "shino")


# ---- Your task ----
def sample_sets(glazes: tuple[str, ...]) -> list[list[str]]:
    """Return every subset of `glazes`, in the order the walk finds them.

    Args:
        glazes: The samples on the shelf. Assumed distinct.

    Returns:
        Every subset, each in shelf order, with the empty set first. There are
        2 ** len(glazes) of them, which is the number to state out loud before
        writing any code - it is what tells you this cannot be made fast.
    """
    found: list[list[str]] = []
    trail: list[str] = []

    def walk(index: int) -> None:
        # Recorded at EVERY node, not at the leaves. A subset is complete the
        # moment we stop adding to it.
        found.append(list(trail))
        for next_index in range(index, len(glazes)):
            trail.append(glazes[next_index])       # choose
            walk(next_index + 1)                   # explore
            trail.pop()                            # undo

    walk(0)
    return found


def sample_sets_no_undo(glazes: tuple[str, ...]) -> list[list[str]]:
    """The same walk with the undo left out, shipped to be compared.

    Args:
        glazes: The samples on the shelf.

    Returns:
        Its answer, which has the right NUMBER of subsets and the wrong
        contents. Running this beside `sample_sets` is the point of the
        exercise - the count agreeing is exactly why the bug survives testing.
    """
    found: list[list[str]] = []
    trail: list[str] = []

    def walk(index: int) -> None:
        found.append(list(trail))
        for next_index in range(index, len(glazes)):
            trail.append(glazes[next_index])
            walk(next_index + 1)
            # the pop belongs here

    walk(0)
    return found


def sets_of_size(glazes: tuple[str, ...], size: int) -> list[list[str]]:
    """Return only the subsets holding exactly `size` glazes.

    Args:
        glazes: The samples on the shelf.
        size: How many glazes each set must hold.

    Returns:
        The matching subsets, in shelf order. An empty list when `size` is
        negative or larger than the shelf - both are real answers rather than
        errors, because asking for six glazes off a shelf of four is a question
        with the answer "none".
    """
    return [subset for subset in sample_sets(glazes) if len(subset) == size]


def set_count(glazes: tuple[str, ...]) -> int:
    """Return how many subsets exist, without enumerating them.

    Args:
        glazes: The samples on the shelf.

    Returns:
        2 raised to the number of glazes. Kept beside the enumeration so the
        two can be checked against each other, which is the cheapest possible
        test of a combinatorial walk.
    """
    return 2 ** len(glazes)


# ---- Self-check ----
if __name__ == "__main__":
    print(f"GLAZES  {list(GLAZES)}")
    print()

    print("EVERY SAMPLE SET, IN WALK ORDER")
    for subset in sample_sets(GLAZES):
        shown = ", ".join(subset) if subset else "(none)"
        print(f"    {len(subset)}  {shown}")
    print()

    print("SETS BY SIZE")
    for size in range(len(GLAZES) + 1):
        print(f"    {size} glazes: {len(sets_of_size(GLAZES, size))}")
    print()

    print("THE SAME WALK WITHOUT THE UNDO")
    broken = sample_sets_no_undo(GLAZES)
    print(f"    subsets found : {len(broken)}   (the right number)")
    print(f"    last three    : {broken[-3:]}")
    print()

    subsets = sample_sets(GLAZES)

    # Four glazes make sixteen sets, and the closed form agrees.
    assert len(subsets) == set_count(GLAZES) == 16

    # The empty set comes first, because it is recorded before any choice.
    assert subsets[0] == []

    # Every subset appears exactly once.
    assert len({tuple(subset) for subset in subsets}) == len(subsets)

    # Every subset keeps shelf order, which is what the index-only walk buys.
    order = {glaze: index for index, glaze in enumerate(GLAZES)}
    for subset in subsets:
        assert [order[glaze] for glaze in subset] == sorted(order[glaze] for glaze in subset)

    # Sizes are the binomial row: 1, 4, 6, 4, 1.
    assert [len(sets_of_size(GLAZES, size)) for size in range(5)] == [1, 4, 6, 4, 1]

    # Asking for more glazes than the shelf holds is a question with an answer.
    assert sets_of_size(GLAZES, 9) == []
    assert sets_of_size(GLAZES, -1) == []

    # An empty shelf still has one subset: the empty one.
    assert sample_sets(()) == [[]]

    # The version without the undo finds the right NUMBER of sets and the
    # wrong sets. That is the whole exhibit: a count-only test passes it.
    assert len(broken) == len(subsets)
    assert broken != subsets
    # ...and specifically, it never empties the trail, so late sets are too big.
    assert any(len(subset) > 4 for subset in broken) or broken[-1] != subsets[-1]

    print("All checks passed.")
