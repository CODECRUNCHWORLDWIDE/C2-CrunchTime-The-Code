# Exercise 1 — The Glaze Sample Set

> **Topic:** the backtracking template, with the recording step in the place that surprises people
> **Lecture:** [01 — The Backtracking Template](../lecture-notes/01-the-backtracking-template-and-the-three-warmups.md)
> **Difficulty:** Easy
> **Target time:** 30 minutes
> **Why this one:** it is the smallest problem where choose-explore-undo is the whole answer, so the three lines have nothing to hide behind. It also ships the version with the undo left out, which does not crash and finds the right *number* of answers — the single most useful thing to have seen before the rest of the week.

## The Brief

A pottery keeps a shelf of glaze samples. Before a firing the studio picks some
subset of them to test together — possibly all of them, possibly none.

List every subset, and count them.

The surprise is where the recording goes. In most walks you record at a leaf,
when something is finished. Here a subset is complete **the moment you stop
adding to it**, so every node of the walk is an answer and the recording happens
at all of them.

## Starter

`exercise-01-glaze-sample-set-solution.py` sits beside this page with the shelf
and the self-checks.

```text
ash   celadon   tenmoku   shino
```

Four glazes. Say how many subsets there are before you write anything — the
number is the first line of the memo and it is what tells you this walk can
never be made fast.

## Requirements

1. `sample_sets(glazes)` returns every subset, in walk order, with the empty set
   first.
2. `sample_sets_no_undo(glazes)` is the same walk with the `pop` removed —
   shipped on purpose, to be run and compared.
3. `sets_of_size(glazes, size)` filters to a given size.
4. `set_count(glazes)` returns `2 ** len(glazes)` without enumerating.
5. An empty shelf still has one subset: the empty one.

## Constraints

- **Record at every node**, not at the leaves. There is no "finished" test to
  write on this page, and looking for one is the first wrong turn.
- **Three lines, in order: choose, explore, undo.** Name them in the memo. Every
  page this week is these three lines with something added.
- **Walk forwards only.** The loop starts at the current index, never at zero.
  That is what keeps each subset in shelf order and what stops the same subset
  arriving twice by a different route.
- **`set_count` must not call the enumeration.** It is there to check it, and a
  check that calls the thing it checks is not one.
- **Say `2 ** n` out loud before coding.** Four glazes is 16 and twenty glazes is
  over a million; the growth is the constraint, not an aside.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-01-glaze-sample-set-solution.py
GLAZES  ['ash', 'celadon', 'tenmoku', 'shino']

EVERY SAMPLE SET, IN WALK ORDER
    0  (none)
    1  ash
    2  ash, celadon
    3  ash, celadon, tenmoku
    4  ash, celadon, tenmoku, shino
    3  ash, celadon, shino
    2  ash, tenmoku
    3  ash, tenmoku, shino
    2  ash, shino
    1  celadon
    2  celadon, tenmoku
    3  celadon, tenmoku, shino
    2  celadon, shino
    1  tenmoku
    2  tenmoku, shino
    1  shino

SETS BY SIZE
    0 glazes: 1
    1 glazes: 4
    2 glazes: 6
    3 glazes: 4
    4 glazes: 1

THE SAME WALK WITHOUT THE UNDO
    subsets found : 16   (the right number)
    last three    : [['ash', 'celadon', 'tenmoku', 'shino', 'shino', 'tenmoku', 'shino', 'shino', 'celadon', 'tenmoku', 'shino', 'shino', 'tenmoku'], ['ash', 'celadon', 'tenmoku', 'shino', 'shino', 'tenmoku', 'shino', 'shino', 'celadon', 'tenmoku', 'shino', 'shino', 'tenmoku', 'shino'], ['ash', 'celadon', 'tenmoku', 'shino', 'shino', 'tenmoku', 'shino', 'shino', 'celadon', 'tenmoku', 'shino', 'shino', 'tenmoku', 'shino', 'shino']]

All checks passed.
```

The last block is the exhibit. The walk with the undo removed finds **sixteen**
subsets — exactly the right number — and they are not the right subsets. The
trail is never emptied, so the later ones accumulate every glaze the walk has
ever touched, and the last one holds fifteen entries off a shelf of four.

A test that only counted the answers would pass it. That is the shape of this
bug, and it is worth having seen once before Challenge 1, where the same
omission on a grid produces a plausible number of routes rather than an obvious
mess.

## Steps

1. Read the self-checks. They are the spec.
2. Write the memo: `2 ** n` subsets, record at every node, three lines.
3. Write the walk. Get the empty set out of it first — if `sample_sets(())`
   does not return `[[]]`, the recording is in the wrong place.
4. Delete the `pop` and run it again. Look at the last three subsets.
5. Put the `pop` back and check the sizes come out as 1, 4, 6, 4, 1.
6. Add `sets_of_size` and `set_count`, then write the FRAME pass.

## The Solution

```python
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
```

`sample_sets_no_undo` is shipped knowing it is wrong, and the file asserts that
it is wrong rather than merely printing it. An exhibit nothing asserts stops
being an exhibit the first time somebody tidies the file.

## Download and run

Download the solution beside this page and run it:

```bash
python exercise-01-glaze-sample-set-solution.py
```

No third-party packages, no arguments, no input. It prints every subset, the
counts by size, the broken walk's output, and then `All checks passed.`

## Common bugs to catch

- **No undo.** Symptom: the right number of subsets and the wrong contents. It
  does not crash and a count-only test passes it.
- **Recording only at the leaves.** Symptom: one subset — the whole shelf —
  because nothing else is ever considered finished.
- **Appending `trail` instead of `list(trail)`.** Symptom: sixteen references to
  one list, all showing the same thing at the end. A different bug from the
  missing undo, with an almost identical symptom.
- **Starting the loop at zero.** Symptom: subsets in every order rather than
  every subset, and far more of them.
- **`set_count` calling `sample_sets`.** Symptom: a check that can never fail.
- **Treating the empty shelf as a special case.** Symptom: extra code for
  something the walk already handles correctly.

## Acceptance checklist

- [ ] Four glazes give 16 subsets, and `set_count` agrees.
- [ ] The empty set is first.
- [ ] Every subset appears exactly once, in shelf order.
- [ ] Sizes come out as 1, 4, 6, 4, 1.
- [ ] An empty shelf returns `[[]]`.
- [ ] The no-undo walk finds 16 subsets and different ones.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Return the subsets as a generator instead of a list, and say what that buys.
  On four glazes, nothing; on twenty, it is the difference between running and
  not.
- Produce the same subsets with a bit mask over `range(2 ** n)` instead of a
  walk. It is shorter, it is not a template, and saying which you would write in
  an interview — and why — is the point.
- Add a rule that two named glazes cannot be tested together, and prune. That is
  the first real prune of the week and it makes Exercise 3 much easier.
