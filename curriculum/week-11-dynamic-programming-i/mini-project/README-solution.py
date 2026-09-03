"""README-solution.py - the Week 11 mini-project, both halves worked.

Two dynamic programming problems that grade separately because they are
structurally different: one OPTIMISES over a line, one COUNTS over a pair of
sequences.

  Half one - the orchard row. Fruit trees stand in a line, each with a known
  yield. The picking ladder needs clearance, so no two ADJACENT trees may be
  picked in the same pass. Choose the trees. The orchard wants the yield AND
  the trees, because someone has to walk out and mark them.

  Half two - the dye batch log. A dyehouse keeps a log of every bath it ran.
  A recipe is a short sequence of bath codes. Count how many distinct ways the
  recipe appears in the log as a subsequence - the baths in order, not
  necessarily adjacent. Two ways differ if they use a different set of log
  positions, even when the codes are identical.

The first returns a choice and its value. The second returns a count that is
often enormous. Saying which of those two you are doing, before writing code,
is what the pair is graded on.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that fence
reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
# Yield in kilograms for each tree, from the gate outwards.
ORCHARD_ROW: tuple[int, ...] = (7, 12, 5, 9, 14, 3, 11)

# The dyehouse log, and the recipe being looked for.
BATH_LOG = "INDIGOINDIGO"
RECIPE = "IGO"


# ---- Half one: the orchard row ----
def best_yield(trees: tuple[int, ...]) -> int:
    """The largest yield obtainable with no two adjacent trees picked.

    Two running totals rather than a table: at each tree the answer is either
    "pick it and add the best that ended two trees back" or "skip it and keep
    the best that ended one tree back". Nothing older than two trees is ever
    needed, so nothing older is kept.

    Args:
        trees: Yield per tree, in row order.

    Returns:
        The best total. An empty row yields 0.
    """
    took_previous = 0   # best total for a row ending at the previous tree, picked
    skipped_previous = 0  # best total for a row ending at the previous tree, skipped
    for tree in trees:
        take = skipped_previous + tree
        skip = max(took_previous, skipped_previous)
        took_previous, skipped_previous = take, skip
    return max(took_previous, skipped_previous)


def picked_trees(trees: tuple[int, ...]) -> list[int]:
    """Which trees to pick, as positions, for the best yield.

    The two-running-totals form cannot answer this - it has thrown away the
    choices. So this keeps the whole table and walks it backwards, which is the
    trade the write-up has to name: constant space and a number, or linear space
    and an answer somebody can act on.

    Args:
        trees: Yield per tree, in row order.

    Returns:
        Positions in row order. Ties are settled by preferring the EARLIER tree,
        so the answer is one set rather than a family of them.
    """
    if not trees:
        return []

    size = len(trees)
    best = [0] * (size + 1)   # best[i] = best yield using trees[i:]
    for i in range(size - 1, -1, -1):
        best[i] = max(trees[i] + (best[i + 2] if i + 2 <= size else 0), best[i + 1])

    chosen: list[int] = []
    i = 0
    while i < size:
        take = trees[i] + (best[i + 2] if i + 2 <= size else 0)
        # >= prefers taking the earlier tree on a tie, which is the stated
        # tie-break. Using > would silently prefer the later one.
        if take >= best[i + 1]:
            chosen.append(i)
            i += 2
        else:
            i += 1
    return chosen


# ---- Half two: the dye batch log ----
def recipe_ways(log: str, recipe: str) -> int:
    """How many distinct ways the recipe appears in the log as a subsequence.

    ways[j] is the number of ways to match recipe[:j] against the part of the
    log read so far. Walking the recipe BACKWARDS for each log character is what
    keeps a single row honest: going forwards would let one log character be
    used twice in the same pass.

    Args:
        log: The dyehouse log of bath codes.
        recipe: The sequence being looked for.

    Returns:
        The number of distinct position sets. An empty recipe matches exactly
        once - by taking nothing - which is the base case, not a special case.
    """
    ways = [0] * (len(recipe) + 1)
    ways[0] = 1
    for bath in log:
        for j in range(len(recipe), 0, -1):
            if recipe[j - 1] == bath:
                ways[j] += ways[j - 1]
    return ways[len(recipe)]


def recipe_table(log: str, recipe: str) -> list[list[int]]:
    """The full table, for a write-up that wants to show its working.

    Args:
        log: The dyehouse log.
        recipe: The sequence being looked for.

    Returns:
        (len(log) + 1) by (len(recipe) + 1); entry [i][j] is the number of ways
        to match recipe[:j] within log[:i].
    """
    rows, cols = len(log) + 1, len(recipe) + 1
    table = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        table[i][0] = 1  # the empty recipe matches once, by taking nothing
    for i in range(1, rows):
        for j in range(1, cols):
            table[i][j] = table[i - 1][j]
            if log[i - 1] == recipe[j - 1]:
                table[i][j] += table[i - 1][j - 1]
    return table


# ---- Self-check ----
if __name__ == "__main__":
    print("HALF ONE - the orchard row")
    print(f"    yields:  {ORCHARD_ROW}")
    picked = picked_trees(ORCHARD_ROW)
    print(f"    best:    {best_yield(ORCHARD_ROW)} kg")
    print(f"    pick:    trees {picked} = {[ORCHARD_ROW[i] for i in picked]}")
    print()

    print("HALF TWO - the dye batch log")
    print(f"    log:     {BATH_LOG}")
    print(f"    recipe:  {RECIPE}")
    print(f"    ways:    {recipe_ways(BATH_LOG, RECIPE)}")
    print()
    print("    the table, rows = log read so far, cols = recipe matched")
    table = recipe_table(BATH_LOG, RECIPE)
    print("             " + "".join(f"{c:>5}" for c in " " + RECIPE))
    for i, row in enumerate(table):
        head = " " if i == 0 else BATH_LOG[i - 1]
        print(f"        {head}    " + "".join(f"{v:>5}" for v in row))
    print()

    # ---- Half one.
    # The choice must be legal: no two picked trees adjacent.
    for i in range(len(picked) - 1):
        assert picked[i + 1] - picked[i] >= 2

    # And it must actually achieve the reported best.
    assert sum(ORCHARD_ROW[i] for i in picked) == best_yield(ORCHARD_ROW)

    # Known small cases, including the ones that catch a greedy solution.
    assert best_yield(()) == 0
    assert picked_trees(()) == []
    assert best_yield((5,)) == 5
    assert best_yield((5, 9)) == 9
    assert best_yield((9, 5)) == 9
    # Greedy-by-largest picks 10 and then cannot take either 6, giving 10.
    # Taking both 6s gives 12, so greedy is wrong and this row proves it.
    assert best_yield((6, 10, 6)) == 12
    assert picked_trees((6, 10, 6)) == [0, 2]

    # The tie-break: equal either way, take the earlier tree.
    assert picked_trees((4, 4)) == [0]

    # ---- Half two.
    # The row form and the table form must agree, always.
    for log, recipe in ((BATH_LOG, RECIPE), ("AAAA", "AA"), ("ABC", "ABC"),
                        ("ABC", "CBA"), ("", "A"), ("A", ""), ("", "")):
        assert recipe_ways(log, recipe) == recipe_table(log, recipe)[len(log)][len(recipe)]

    # The empty recipe matches once - by taking nothing - however long the log.
    assert recipe_ways("ANYTHING", "") == 1
    assert recipe_ways("", "") == 1

    # A recipe longer than the log cannot match.
    assert recipe_ways("", "A") == 0
    assert recipe_ways("AB", "ABC") == 0

    # Four A's contain "AA" in six ways: every pair of positions.
    assert recipe_ways("AAAA", "AA") == 6

    # Order matters: the codes are all present but never in the right order.
    assert recipe_ways("ABC", "CBA") == 0

    print("All checks passed.")
