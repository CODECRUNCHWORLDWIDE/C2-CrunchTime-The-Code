"""exercise-03-clay-weigh-out-solution.py - making up a weight from the counterweights.

A pottery weighs clay on a beam balance. The studio owns a set of
counterweights and has an unlimited supply of each - the same weight may be put
on the pan as many times as needed.

List every way to make up a target weight, and count the work it took.

This is the first page where the walk is PRUNED. Two prunings, and they are
different in kind:

  the sum prune       stop the moment the running total passes the target,
                      because every counterweight is positive and the total
                      can only ever grow from here
  the index prune     let a branch reuse the counterweight it is on, but never
                      go back to an earlier one - which is what stops
                      2 + 3 and 3 + 2 both being reported

The second is not an optimisation. Without it the answers are duplicated, and
the count of "ways" is wrong rather than slow.

The file counts nodes visited with and without the sum prune, so the saving is
a printed number rather than a claim.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
COUNTERWEIGHTS: tuple[int, ...] = (2, 3, 5)
TARGET = 8


# ---- Your task ----
def weigh_outs(weights: tuple[int, ...], target: int) -> tuple[list[list[int]], int]:
    """Return every way to make `target` from `weights`, and the nodes visited.

    Args:
        weights: The counterweights available, each usable any number of times.
            Must all be positive.
        target: The weight to make up. Must not be negative.

    Returns:
        A pair: every combination as a list of weights in non-decreasing order,
        and how many nodes the walk entered. A target of zero has exactly one
        answer, the empty pan.

    Raises:
        ValueError: If any counterweight is not positive, or the target is
            negative. A counterweight of zero or less would make the sum prune
            unsound, which is worth refusing loudly rather than working around.
    """
    if any(weight <= 0 for weight in weights):
        raise ValueError("every counterweight must be positive")
    if target < 0:
        raise ValueError("a target weight cannot be negative")

    found: list[list[int]] = []
    pan: list[int] = []
    nodes = 0

    def walk(index: int, remaining: int) -> None:
        nonlocal nodes
        nodes += 1
        if remaining == 0:
            found.append(list(pan))
            return
        for next_index in range(index, len(weights)):
            weight = weights[next_index]
            if weight > remaining:
                # The sum prune. Sound only because every weight is positive.
                continue
            pan.append(weight)               # choose
            walk(next_index, remaining - weight)   # explore, same index: reuse
            pan.pop()                        # undo

    walk(0, target)
    return found, nodes


def weigh_outs_unpruned(weights: tuple[int, ...], target: int) -> tuple[list[list[int]], int]:
    """The same walk without the sum prune, shipped for the node count.

    Args:
        weights: The counterweights available.
        target: The weight to make up.

    Returns:
        The same combinations - this version is correct, only slower - and the
        nodes it visited. Running the two together is what turns "pruning
        helps" into a number.

    Raises:
        ValueError: On the same inputs as `weigh_outs`.
    """
    if any(weight <= 0 for weight in weights):
        raise ValueError("every counterweight must be positive")
    if target < 0:
        raise ValueError("a target weight cannot be negative")

    found: list[list[int]] = []
    pan: list[int] = []
    nodes = 0

    def walk(index: int, remaining: int) -> None:
        nonlocal nodes
        nodes += 1
        if remaining == 0:
            found.append(list(pan))
            return
        if remaining < 0:
            return                    # discovered after the fact, not before
        for next_index in range(index, len(weights)):
            pan.append(weights[next_index])
            walk(next_index, remaining - weights[next_index])
            pan.pop()

    walk(0, target)
    return found, nodes


def weigh_outs_no_index(weights: tuple[int, ...], target: int) -> list[list[int]]:
    """The walk that starts every level from zero, shipped to be compared.

    Args:
        weights: The counterweights available.
        target: The weight to make up.

    Returns:
        Its answer, which reports 2 + 3 and 3 + 2 as different ways. The count
        is wrong rather than the arithmetic, which is why the index rule is a
        correctness rule and not a speed one.
    """
    found: list[list[int]] = []
    pan: list[int] = []

    def walk(remaining: int) -> None:
        if remaining == 0:
            found.append(list(pan))
            return
        for weight in weights:
            if weight > remaining:
                continue
            pan.append(weight)
            walk(remaining - weight)
            pan.pop()

    walk(target)
    return found


def shortest_weigh_out(weights: tuple[int, ...], target: int) -> list[int] | None:
    """Return a way to make `target` using the fewest counterweights, or None.

    Args:
        weights: The counterweights available.
        target: The weight to make up.

    Returns:
        The shortest combination, ties going to the one the walk found first,
        or None when the target cannot be made at all.

    Raises:
        ValueError: On the same inputs as `weigh_outs`.
    """
    found, _ = weigh_outs(weights, target)
    return min(found, key=len) if found else None


# ---- Self-check ----
if __name__ == "__main__":
    combinations, nodes = weigh_outs(COUNTERWEIGHTS, TARGET)
    _, unpruned_nodes = weigh_outs_unpruned(COUNTERWEIGHTS, TARGET)

    print(f"COUNTERWEIGHTS  {list(COUNTERWEIGHTS)}     TARGET  {TARGET}")
    print()

    print("EVERY WEIGH-OUT")
    for pan in combinations:
        print(f"    {' + '.join(str(weight) for weight in pan)}")
    print()

    print("WHAT THE SUM PRUNE SAVES")
    print(f"    nodes with the prune   : {nodes}")
    print(f"    nodes without it       : {unpruned_nodes}")
    print()

    print("THE WALK THAT DOES NOT KEEP AN INDEX")
    loose = weigh_outs_no_index(COUNTERWEIGHTS, TARGET)
    print(f"    ways it reports : {len(loose)}   (should be {len(combinations)})")
    print(f"    for example     : {loose[:4]}")
    print()

    # 8 from 2, 3 and 5: 2+2+2+2, 2+3+3, 3+5.
    assert combinations == [[2, 2, 2, 2], [2, 3, 3], [3, 5]]

    # Every combination really does add up.
    for pan in combinations:
        assert sum(pan) == TARGET

    # Every combination is non-decreasing, which is what the index rule buys.
    for pan in combinations:
        assert pan == sorted(pan)

    # The prune changes the work and not the answer.
    unpruned, _ = weigh_outs_unpruned(COUNTERWEIGHTS, TARGET)
    assert unpruned == combinations
    assert nodes < unpruned_nodes

    # Dropping the index rule reports orderings, not combinations, so it finds
    # more "ways" than there are. That is a wrong answer, not a slow one.
    assert len(loose) > len(combinations)

    # A target of zero is made by the empty pan, exactly once.
    assert weigh_outs(COUNTERWEIGHTS, 0)[0] == [[]]

    # A target nothing can make has no ways at all.
    assert weigh_outs((5, 10), 3)[0] == []
    assert shortest_weigh_out((5, 10), 3) is None

    # One counterweight that divides the target makes it exactly one way.
    assert weigh_outs((4,), 12)[0] == [[4, 4, 4]]

    # The fewest counterweights for 8 is two: 3 + 5.
    assert shortest_weigh_out(COUNTERWEIGHTS, TARGET) == [3, 5]

    # A zero or negative counterweight would make the sum prune unsound, and a
    # negative target is meaningless. Both are refused.
    for bad_weights, bad_target in (((0, 2), 4), ((-1, 2), 4), ((2, 3), -1)):
        try:
            weigh_outs(bad_weights, bad_target)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad_weights}, {bad_target}")

    print("All checks passed.")
