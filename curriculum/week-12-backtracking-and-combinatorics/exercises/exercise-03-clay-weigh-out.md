# Exercise 3 — The Clay Weigh-Out

> **Topic:** two prunes that look alike and are not — one saves work, one fixes the answer
> **Lecture:** [02 — Pruning, Deduplication and String Partitioning](../lecture-notes/02-pruning-and-deduplication-and-string-partitioning.md)
> **Difficulty:** Medium
> **Target time:** 40 minutes
> **Why this one:** it is the first page where the walk is cut short, and it cuts twice for two entirely different reasons. Telling those two reasons apart is the thing being drilled — one is an optimisation you could skip, and the other is the difference between right and wrong.

## The Brief

A pottery weighs clay on a beam balance. The studio owns a set of
counterweights and has an **unlimited supply of each** — the same weight may go
on the pan as many times as needed.

List every way to make up a target weight.

## Starter

`exercise-03-clay-weigh-out-solution.py` sits beside this page with the weights
and the self-checks.

```text
counterweights   2   3   5
target           8
```

Three ways exist. Find them on paper first; it takes a minute and it is what
tells you whether your answer later is short or complete.

## Requirements

1. `weigh_outs(weights, target)` returns every combination **and** the number of
   nodes the walk entered.
2. `weigh_outs_unpruned(weights, target)` is the same walk without the sum
   prune — correct, slower, shipped for the node count.
3. `weigh_outs_no_index(weights, target)` is the walk that starts every level
   from zero — shipped because its answer is *wrong*, not slow.
4. `shortest_weigh_out(weights, target)` returns a combination using the fewest
   counterweights, or `None`.
5. A target of zero has exactly one answer: the empty pan.

## Constraints

- **The sum prune is an optimisation.** Stop the moment the running total would
  pass the target. It is sound only because every counterweight is positive —
  the total can only grow from here — and that sentence is what makes it a prune
  rather than a guess.
- **The index rule is a correctness rule.** A branch may reuse the counterweight
  it is on but must never go back to an earlier one. Without it, `2 + 3` and
  `3 + 2` are both reported and the count of ways is simply wrong.
- **Zero and negative counterweights are refused.** Not because they are awkward,
  but because they make the sum prune unsound — the total could stop growing, and
  the whole argument for stopping early collapses. Refuse them loudly rather than
  working around them.
- **Report the node counts**, so the saving is a number.
- **Recurse on the same index after choosing**, which is what "unlimited supply"
  means in code.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-03-clay-weigh-out-solution.py
COUNTERWEIGHTS  [2, 3, 5]     TARGET  8

EVERY WEIGH-OUT
    2 + 2 + 2 + 2
    2 + 3 + 3
    3 + 5

WHAT THE SUM PRUNE SAVES
    nodes with the prune   : 13
    nodes without it       : 23

THE WALK THAT DOES NOT KEEP AN INDEX
    ways it reports : 6   (should be 3)
    for example     : [[2, 2, 2, 2], [2, 3, 3], [3, 2, 3], [3, 3, 2]]

All checks passed.
```

Two blocks to read, and they say different kinds of thing.

**The prune saves work**: 13 nodes against 23, on a target of 8. Same answer,
about half the walk. That is an optimisation, and on a larger target it is the
difference between finishing and not.

**Dropping the index rule changes the answer**: six "ways" reported where three
exist, because `2 + 3 + 3`, `3 + 2 + 3` and `3 + 3 + 2` are counted separately.
That is not a slower answer. It is a wrong one, and the two failures are worth
keeping straight in the write-up.

## Steps

1. Read the self-checks. They are the spec.
2. Find the three answers on paper.
3. Write the memo: choose-explore-undo, the sum prune and why it is sound, the
   index rule and why it is not optional.
4. Write the walk **without** either prune first. Confirm it gets six ways, and
   see that the extra three are reorderings.
5. Add the index rule. Now three ways.
6. Add the sum prune and the node counter together. Compare against the
   unpruned count.
7. Add `shortest_weigh_out` and the input checks, then write the FRAME pass.

## The Solution

```python
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
```

Both wrong versions are shipped, and the file asserts what each one gets wrong —
that the unpruned walk agrees on the answer and disagrees on the work, and that
the index-free walk disagrees on the answer. Two exhibits, two different claims.

## Download and run

Download the solution beside this page and run it:

```bash
python exercise-03-clay-weigh-out-solution.py
```

No third-party packages, no arguments, no input. It prints the combinations, the
two node counts, the index-free walk's inflated answer, and then
`All checks passed.`

## Common bugs to catch

- **Recursing on `index + 1` after choosing.** Symptom: each counterweight used
  at most once, so `2+2+2+2` disappears. A quiet, plausible undercount.
- **Starting every level at zero.** Symptom: six ways where three exist.
- **Checking the total after adding rather than before.** Symptom: correct
  answers, more nodes, and a prune that is not really pruning.
- **Allowing a counterweight of zero.** Symptom: the walk never terminates,
  because the remaining weight stops falling.
- **Treating a target of zero as an error.** Symptom: a missing base case, and a
  walk that has nowhere to stop.
- **Comparing the two versions' node counts without checking they agree on the
  answer.** Symptom: a fast wrong version declared an improvement.

## Acceptance checklist

- [ ] Three ways to make 8: `2+2+2+2`, `2+3+3`, `3+5`.
- [ ] Every combination sums to the target and is non-decreasing.
- [ ] The pruned and unpruned walks agree on the answer and differ on the nodes.
- [ ] The index-free walk reports more ways than exist.
- [ ] A target of zero gives `[[]]`; an impossible target gives `[]` and `None`.
- [ ] A zero or negative counterweight raises `ValueError`.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Add a limit on how many counterweights may go on the pan, and prune on that
  too. It is a second optimisation prune, and saying which of the three prunes
  are optional is a good test of whether the distinction landed.
- Count only the number of ways, without building the lists. It is much faster
  and it is a different algorithm — a table rather than a walk, which is
  [Week 11](../../week-11-dynamic-programming-i/) coming back.
- Report the target that has the most ways, for a given set of counterweights and
  a bound. It is one run per target and the answer is not the largest target.
