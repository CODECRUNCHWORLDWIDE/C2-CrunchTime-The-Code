"""problem-01-tasting-panel-solution.py - every panel of a fixed size.

A pottery co-operative picks a tasting panel from its members. The panel must
hold exactly `size` people, and who is on it matters while the order does not -
a panel of Ada, Bram and Cato is the same panel however it is written down.

List every panel, and count the walk.

This is Exercise 1's subset walk with a size fixed, which changes two things.
The recording moves from every node to the nodes where the trail is full. And a
new prune becomes possible: once there are not enough members left to fill the
panel, the branch is dead however it continues, so it can be abandoned before
it is walked.

That prune is worth a printed number rather than a claim, so the file counts
nodes with and without it.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

from math import comb

# ---- Given data ----
MEMBERS: tuple[str, ...] = ("Ada", "Bram", "Cato", "Devi", "Enid", "Fen")
PANEL_SIZE = 3


# ---- Your task ----
def panels(members: tuple[str, ...], size: int) -> tuple[list[list[str]], int]:
    """Return every panel of exactly `size` members, and the nodes visited.

    Args:
        members: The co-operative's members, in roster order.
        size: How many people the panel holds.

    Returns:
        A pair: every panel, each in roster order, and how many nodes the walk
        entered. A size of zero has one panel, the empty one; a size larger
        than the roster has none.

    Raises:
        ValueError: If `size` is negative.
    """
    if size < 0:
        raise ValueError("a panel cannot have a negative size")

    found: list[list[str]] = []
    trail: list[str] = []
    nodes = 0

    def walk(index: int) -> None:
        nonlocal nodes
        nodes += 1
        if len(trail) == size:
            found.append(list(trail))
            return
        # The prune: if every remaining member joined, would the panel still be
        # short? Then this branch cannot produce a panel and is not walked.
        for next_index in range(index, len(members)):
            if len(members) - next_index < size - len(trail):
                break
            trail.append(members[next_index])
            walk(next_index + 1)
            trail.pop()

    walk(0)
    return found, nodes


def panels_unpruned(members: tuple[str, ...], size: int) -> tuple[list[list[str]], int]:
    """The same walk without the short-branch prune, shipped for the node count.

    Args:
        members: The co-operative's members.
        size: How many people the panel holds.

    Returns:
        The same panels - this version is correct, only wasteful - and the
        nodes it visited.

    Raises:
        ValueError: If `size` is negative.
    """
    if size < 0:
        raise ValueError("a panel cannot have a negative size")

    found: list[list[str]] = []
    trail: list[str] = []
    nodes = 0

    def walk(index: int) -> None:
        nonlocal nodes
        nodes += 1
        if len(trail) == size:
            found.append(list(trail))
            return
        for next_index in range(index, len(members)):
            trail.append(members[next_index])
            walk(next_index + 1)
            trail.pop()

    walk(0)
    return found, nodes


def panels_with(members: tuple[str, ...], size: int, member: str) -> list[list[str]]:
    """Return the panels that include a given member.

    Args:
        members: The co-operative's members.
        size: How many people the panel holds.
        member: The member who must be on the panel.

    Returns:
        The matching panels. Empty when the member is not on the roster.
    """
    found, _ = panels(members, size)
    return [panel for panel in found if member in panel]


def panel_count(members: tuple[str, ...], size: int) -> int:
    """Return how many panels exist, without enumerating them.

    Args:
        members: The co-operative's members.
        size: How many people the panel holds.

    Returns:
        The binomial coefficient. Kept beside the enumeration so the two can
        check each other.
    """
    if size < 0 or size > len(members):
        return 0
    return comb(len(members), size)


# ---- Self-check ----
if __name__ == "__main__":
    found, nodes = panels(MEMBERS, PANEL_SIZE)
    _, unpruned_nodes = panels_unpruned(MEMBERS, PANEL_SIZE)

    print(f"MEMBERS  {list(MEMBERS)}     PANEL SIZE  {PANEL_SIZE}")
    print()

    print("EVERY PANEL")
    for panel in found:
        print("    " + ", ".join(panel))
    print()

    print("WHAT THE SHORT-BRANCH PRUNE SAVES")
    print(f"    nodes with the prune : {nodes}")
    print(f"    nodes without it     : {unpruned_nodes}")
    print()

    print("PANELS BY SIZE")
    for size in range(len(MEMBERS) + 1):
        print(f"    {size}: {len(panels(MEMBERS, size)[0])}")
    print()

    # Six members choose three is twenty panels.
    assert len(found) == panel_count(MEMBERS, PANEL_SIZE) == 20

    # Every panel is the right size, in roster order, and appears once.
    order = {member: index for index, member in enumerate(MEMBERS)}
    for panel in found:
        assert len(panel) == PANEL_SIZE
        assert [order[member] for member in panel] == sorted(order[member] for member in panel)
    assert len({tuple(panel) for panel in found}) == len(found)

    # The prune changes the work and not the answer.
    unpruned, _ = panels_unpruned(MEMBERS, PANEL_SIZE)
    assert unpruned == found
    assert nodes < unpruned_nodes

    # Each member sits on the same number of panels: 20 * 3 / 6 = 10.
    for member in MEMBERS:
        assert len(panels_with(MEMBERS, PANEL_SIZE, member)) == 10

    # A member who is not on the roster is on no panel.
    assert panels_with(MEMBERS, PANEL_SIZE, "Gwil") == []

    # A panel of nobody is one panel, the empty one.
    assert panels(MEMBERS, 0)[0] == [[]]

    # A panel bigger than the roster cannot be formed at all.
    assert panels(MEMBERS, 7)[0] == []
    assert panel_count(MEMBERS, 7) == 0

    # The sizes across the whole roster are the binomial row, and they sum to
    # the number of subsets - which is Exercise 1's answer, arrived at from the
    # other direction.
    sizes = [len(panels(MEMBERS, size)[0]) for size in range(len(MEMBERS) + 1)]
    assert sizes == [1, 6, 15, 20, 15, 6, 1]
    assert sum(sizes) == 2 ** len(MEMBERS)

    # A negative size is refused rather than quietly returning nothing.
    try:
        panels(MEMBERS, -1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for a negative panel size")

    print("All checks passed.")
