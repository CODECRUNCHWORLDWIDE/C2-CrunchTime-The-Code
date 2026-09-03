"""problem-05-tare-weight-picks-solution.py - both rules at once.

A works store keeps a bag of tare weights. Some weights in the bag are
identical - two 3lb weights are two separate lumps of iron, and either can go
on the pan, but a pan holding one 3lb weight is the same pan as one holding the
other.

Pick weights from the bag summing to a target, using each LUMP at most once,
and list the distinct pans.

This is Exercise 3 and Exercise 4 in one problem, and the two rules pull in
opposite directions:

  from Exercise 3   the sum prune, and a walk that moves forwards only
  from Exercise 4   sort the bag, and skip a repeat at the same level

but with one thing changed from Exercise 3: the recursion moves to `index + 1`
rather than staying on `index`, because a lump can be used once. Getting that
one character wrong is a different bug from getting the dedup wrong, and both
produce plausible-looking answers.

The file ships three walks so the two failures can be told apart by running
them rather than by reasoning about them.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
# Two 3lb weights, two 1lb, and singles besides.
BAG: tuple[int, ...] = (10, 1, 2, 7, 6, 1, 5, 3, 3)
TARGET = 8


# ---- Your task ----
def tare_pans(bag: tuple[int, ...], target: int) -> list[list[int]]:
    """Return every distinct pan of weights summing to `target`.

    Args:
        bag: The weights in the store, which may hold the same weight more than
            once. Every weight must be positive.
        target: The weight to make up. Must not be negative.

    Returns:
        Every distinct pan, each sorted, in walk order. Two pans are the same
        when they hold the same weights the same number of times.

    Raises:
        ValueError: If any weight is not positive, or the target is negative.
    """
    if any(weight <= 0 for weight in bag):
        raise ValueError("every tare weight must be positive")
    if target < 0:
        raise ValueError("a target weight cannot be negative")

    weights = sorted(bag)
    found: list[list[int]] = []
    pan: list[int] = []

    def walk(index: int, remaining: int) -> None:
        if remaining == 0:
            found.append(list(pan))
            return
        for next_index in range(index, len(weights)):
            weight = weights[next_index]
            if weight > remaining:
                # The bag is sorted, so nothing further along fits either.
                break
            if next_index > index and weight == weights[next_index - 1]:
                # A repeat at this level would produce a pan already found.
                continue
            pan.append(weight)
            walk(next_index + 1, remaining - weight)   # + 1: one lump, once
            pan.pop()

    walk(0, target)
    return found


def tare_pans_reusing(bag: tuple[int, ...], target: int) -> list[list[int]]:
    """The walk that recurses on the same index, shipped to be compared.

    Args:
        bag: The weights in the store.
        target: The weight to make up.

    Returns:
        Its answer, which uses a single lump more than once - so a bag holding
        one 2lb weight produces a pan of four 2lb weights. One character
        different from the right walk.
    """
    weights = sorted(bag)
    found: list[list[int]] = []
    pan: list[int] = []

    def walk(index: int, remaining: int) -> None:
        if remaining == 0:
            found.append(list(pan))
            return
        for next_index in range(index, len(weights)):
            weight = weights[next_index]
            if weight > remaining:
                break
            if next_index > index and weight == weights[next_index - 1]:
                continue
            pan.append(weight)
            walk(next_index, remaining - weight)       # the bug
            pan.pop()

    walk(0, target)
    return found


def tare_pans_undeduped(bag: tuple[int, ...], target: int) -> list[list[int]]:
    """The walk without the repeat skip, shipped to be compared.

    Args:
        bag: The weights in the store.
        target: The weight to make up.

    Returns:
        Its answer, which reports the same pan once per set of lumps rather
        than once per set of weights - so a pan using a 3lb weight appears
        twice when the bag holds two of them.
    """
    weights = sorted(bag)
    found: list[list[int]] = []
    pan: list[int] = []

    def walk(index: int, remaining: int) -> None:
        if remaining == 0:
            found.append(list(pan))
            return
        for next_index in range(index, len(weights)):
            weight = weights[next_index]
            if weight > remaining:
                break
            pan.append(weight)
            walk(next_index + 1, remaining - weight)
            pan.pop()

    walk(0, target)
    return found


def fewest_lumps(bag: tuple[int, ...], target: int) -> list[int] | None:
    """Return a pan making `target` from the fewest lumps, or None.

    Args:
        bag: The weights in the store.
        target: The weight to make up.

    Returns:
        The shortest pan, ties going to the one found first, or None when the
        target cannot be made at all. Fewest lumps is what a storeman actually
        wants, because every lump is one thing to lift.

    Raises:
        ValueError: On the same inputs as `tare_pans`.
    """
    pans = tare_pans(bag, target)
    return min(pans, key=len) if pans else None


# ---- Self-check ----
if __name__ == "__main__":
    pans = tare_pans(BAG, TARGET)
    reusing = tare_pans_reusing(BAG, TARGET)
    undeduped = tare_pans_undeduped(BAG, TARGET)

    print(f"BAG  {sorted(BAG)}     TARGET  {TARGET}")
    print()

    print("EVERY DISTINCT PAN")
    for pan in pans:
        print(f"    {' + '.join(str(weight) for weight in pan)}")
    print()

    print("THE THREE WALKS")
    print(f"    distinct pans, each lump once : {len(pans)}   (the answer)")
    print(f"    recursing on the same index   : {len(reusing)}   (reuses a lump)")
    print(f"    without the repeat skip       : {len(undeduped)}   (same pan twice)")
    print()

    print(f"    fewest lumps for {TARGET}: {fewest_lumps(BAG, TARGET)}")
    print()

    # Every pan sums to the target and is sorted.
    for pan in pans:
        assert sum(pan) == TARGET
        assert pan == sorted(pan)

    # Every pan appears exactly once. That is the dedup rule working.
    assert len({tuple(pan) for pan in pans}) == len(pans)

    # No pan uses more lumps of a weight than the bag holds. That is the
    # "each lump once" rule working, and it is a different claim.
    for pan in pans:
        for weight in set(pan):
            assert pan.count(weight) <= BAG.count(weight)

    # The two failures are different and both are visible.
    # Reusing a lump invents pans the store cannot make: 2+2+2+2 off one 2.
    assert [2, 2, 2, 2] in reusing
    assert [2, 2, 2, 2] not in pans
    # Skipping the dedup repeats pans it has already found.
    assert len(undeduped) > len(pans)
    assert len({tuple(pan) for pan in undeduped}) == len(pans)

    # The fewest lumps for 8 is two.
    shortest = fewest_lumps(BAG, TARGET)
    assert shortest is not None and len(shortest) == 2 and sum(shortest) == TARGET

    # A target of zero is made by the empty pan, exactly once.
    assert tare_pans(BAG, 0) == [[]]

    # A target nothing can reach has no pans and no shortest.
    assert tare_pans((5, 10), 3) == []
    assert fewest_lumps((5, 10), 3) is None

    # A bag of identical weights gives one pan per reachable multiple.
    assert tare_pans((4, 4, 4), 8) == [[4, 4]]
    assert tare_pans((4, 4, 4), 12) == [[4, 4, 4]]
    assert tare_pans((4, 4, 4), 16) == []      # only three lumps in the bag

    # A zero or negative weight would make the sum prune unsound; a negative
    # target is meaningless. Both are refused.
    for bad_bag, bad_target in (((0, 2), 4), ((-1, 2), 4), ((2, 3), -1)):
        try:
            tare_pans(bad_bag, bad_target)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad_bag}, {bad_target}")

    print("All checks passed.")
