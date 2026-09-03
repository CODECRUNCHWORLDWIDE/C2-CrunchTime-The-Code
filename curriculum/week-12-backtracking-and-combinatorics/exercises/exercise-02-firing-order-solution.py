"""exercise-02-firing-order-solution.py - every order the kiln could fire in.

A kiln fires a set of pots one at a time. Every pot is fired exactly once, and
the studio wants to see every possible order.

Subsets walked forwards through a list and never looked back, which is why an
index was enough to keep them straight. An ORDER can put any unfired pot next,
including one earlier in the list, so an index cannot do the bookkeeping. What
replaces it is a record of what has already been used.

The template is unchanged - choose, explore, undo - but the undo now has two
halves, because choosing did two things: it appended to the trail AND marked
the pot as used. Undoing one and not the other is the bug on this page, and it
does not crash. It silently drops orders.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that
fence reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

from math import factorial

# ---- Given data ----
POTS: tuple[str, ...] = ("jug", "bowl", "vase")
BIGGER_KILN: tuple[str, ...] = ("jug", "bowl", "vase", "dish", "cup")


# ---- Your task ----
def firing_orders(pots: tuple[str, ...]) -> list[list[str]]:
    """Return every order the pots could be fired in.

    Args:
        pots: The pots to fire. Assumed distinct.

    Returns:
        Every ordering, as a list of lists. There are len(pots) factorial of
        them, which is the number to say out loud before writing any code:
        five pots is 120 orders and ten pots is over three million, so this is
        a walk that is only ever run on small sets.
    """
    found: list[list[str]] = []
    trail: list[str] = []
    used: set[str] = set()

    def walk() -> None:
        if len(trail) == len(pots):
            found.append(list(trail))
            return
        for pot in pots:
            if pot in used:
                continue
            trail.append(pot)          # choose - two things happen here
            used.add(pot)
            walk()                     # explore
            trail.pop()                # undo - so two things happen here too
            used.discard(pot)

    walk()
    return found


def firing_orders_half_undone(pots: tuple[str, ...]) -> list[list[str]]:
    """The same walk that forgets to unmark the pot, shipped to be compared.

    Args:
        pots: The pots to fire.

    Returns:
        Its answer, which is a single order rather than all of them. The trail
        is undone and the used set is not, so once a pot has been fired in any
        branch it is never available again anywhere.
    """
    found: list[list[str]] = []
    trail: list[str] = []
    used: set[str] = set()

    def walk() -> None:
        if len(trail) == len(pots):
            found.append(list(trail))
            return
        for pot in pots:
            if pot in used:
                continue
            trail.append(pot)
            used.add(pot)
            walk()
            trail.pop()
            # the discard belongs here

    walk()
    return found


def orders_starting_with(pots: tuple[str, ...], first: str) -> list[list[str]]:
    """Return the orders that fire `first` first.

    Args:
        pots: The pots to fire.
        first: The pot that must go in first.

    Returns:
        The matching orders. Empty when `first` is not one of the pots, which
        is a real answer rather than an error.
    """
    return [order for order in firing_orders(pots) if order and order[0] == first]


def order_count(pots: tuple[str, ...]) -> int:
    """Return how many orders exist, without enumerating them.

    Args:
        pots: The pots to fire.

    Returns:
        len(pots) factorial. Kept beside the enumeration so the two can check
        each other, and so the growth is printable rather than described.
    """
    return factorial(len(pots))


# ---- Self-check ----
if __name__ == "__main__":
    print(f"POTS  {list(POTS)}")
    print()

    print("EVERY FIRING ORDER")
    for order in firing_orders(POTS):
        print("    " + " -> ".join(order))
    print()

    print("HOW FAST THIS GROWS")
    for size in range(1, 9):
        print(f"    {size} pots: {factorial(size):>6} orders")
    print()

    print("THE SAME WALK THAT FORGETS TO UNMARK")
    half = firing_orders_half_undone(POTS)
    print(f"    orders found: {len(half)}   (should be {order_count(POTS)})")
    print(f"    what it found: {half}")
    print()

    orders = firing_orders(POTS)

    # Three pots make six orders, and the closed form agrees.
    assert len(orders) == order_count(POTS) == 6

    # Every order uses every pot exactly once.
    for order in orders:
        assert sorted(order) == sorted(POTS)

    # Every order appears exactly once.
    assert len({tuple(order) for order in orders}) == len(orders)

    # Each pot leads the same number of orders: 6 / 3 = 2 apiece.
    for pot in POTS:
        assert len(orders_starting_with(POTS, pot)) == 2

    # A pot that is not on the list leads nothing.
    assert orders_starting_with(POTS, "teapot") == []

    # One pot has one order; no pots has one order, the empty one.
    assert firing_orders(("jug",)) == [["jug"]]
    assert firing_orders(()) == [[]]

    # Five pots is 120 orders. The enumeration and the closed form still agree,
    # which is the check worth keeping as the set grows.
    assert len(firing_orders(BIGGER_KILN)) == order_count(BIGGER_KILN) == 120

    # Forgetting the unmark does not crash and does not warn. It finds exactly
    # one order, because after the first full descent every pot is used
    # forever. That is the exhibit.
    assert len(half) == 1
    assert half[0] == list(POTS)

    print("All checks passed.")
