# Exercise 2 — The Firing Order

> **Topic:** when an index is not enough bookkeeping, and the undo grows a second half
> **Lecture:** [01 — The Backtracking Template](../lecture-notes/01-the-backtracking-template-and-the-three-warmups.md)
> **Difficulty:** Easy-Medium
> **Target time:** 30 minutes
> **Why this one:** subsets walked forwards and never looked back, so an index kept them straight. An order can put any unfired pot next, so it cannot. Watching what replaces the index — and what that does to the undo — is the whole page.

## The Brief

A kiln fires a set of pots one at a time. Every pot is fired exactly once, and
the studio wants to see **every possible order**.

[Exercise 1](./exercise-01-glaze-sample-set.md) only ever moved forwards through
the shelf, which is why the index was enough. Here the next pot can be any pot
not yet fired, including one earlier in the list — so the walk needs a record of
what has already been used.

## Starter

The worked answer on this page carries the pots and the self-checks.

```text
jug   bowl   vase
```

Three pots. Work out how many orders before writing anything, and then work out
how many for eight — the file prints the row so you can check yourself, and the
shape of that row is the constraint.

## Requirements

1. `firing_orders(pots)` returns every ordering.
2. `firing_orders_half_undone(pots)` is the same walk that undoes the trail and
   **not** the used set — shipped on purpose, to be run and compared.
3. `orders_starting_with(pots, first)` filters to orders that begin with a given
   pot.
4. `order_count(pots)` returns `len(pots)` factorial without enumerating.
5. No pots gives one order — the empty one.

## Constraints

- **Choosing does two things**, so undoing must do two things. Append to the
  trail and mark the pot used; then pop the trail and unmark the pot. Doing one
  and not the other is the bug this page is built around.
- **Record at the leaves this time**, not at every node. An order is only an
  order when every pot is in it — which is the opposite of Exercise 1, and worth
  saying out loud in the memo rather than absorbing silently.
- **The loop runs over all the pots**, every time, and skips the used ones. It
  does not start from an index.
- **`order_count` must not call the enumeration.**
- **Say the growth out loud.** Five pots is 120 orders, eight is 40,320, ten is
  over three million. This is a walk that is only ever run on small sets, and
  knowing where the wall is matters more than the code.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python exercise-02-firing-order.py
POTS  ['jug', 'bowl', 'vase']

EVERY FIRING ORDER
    jug -> bowl -> vase
    jug -> vase -> bowl
    bowl -> jug -> vase
    bowl -> vase -> jug
    vase -> jug -> bowl
    vase -> bowl -> jug

HOW FAST THIS GROWS
    1 pots:      1 orders
    2 pots:      2 orders
    3 pots:      6 orders
    4 pots:     24 orders
    5 pots:    120 orders
    6 pots:    720 orders
    7 pots:   5040 orders
    8 pots:  40320 orders

THE SAME WALK THAT FORGETS TO UNMARK
    orders found: 1   (should be 6)
    what it found: [['jug', 'bowl', 'vase']]

All checks passed.
```

The last block is the exhibit, and it is a sharper failure than Exercise 1's.
The walk that pops the trail but never unmarks the pot finds **exactly one
order** — `jug -> bowl -> vase` — because after the first full descent every pot
is marked used forever and no other branch can start.

It does not crash. It does not warn. It just quietly answers a question nobody
asked, and if you were expecting a long list you would notice, while if you were
counting something aggregate you would not.

## Steps

1. Read the self-checks. They are the spec.
2. Write the memo: a used set replaces the index, record at the leaves, and the
   undo has two halves.
3. Write the walk. Get three pots to give six orders.
4. Delete the `discard` and run it again. One order. Look at which one, and work
   out why it is that one.
5. Put it back, then check that each pot leads exactly two of the six orders.
6. Run it on five pots and confirm 120 against the closed form.
7. Write the FRAME pass, with the growth row in the cost section.

## The Solution

```python
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
```

The used set is a `set` rather than a list of booleans because the pots are named
rather than numbered. On numbered items a list indexed by position is faster and
says the same thing; noting which you would use and why is a reasonable sentence
for the write-up.

## Run it

Download the solution beside this page and run it:

```bash
python exercise-02-firing-order.py
```

No third-party packages, no arguments, no input. It prints every order, the
growth row, the half-undone walk's single answer, and then `All checks passed.`

## Common bugs to catch

- **Undoing the trail and not the used set.** Symptom: one order, silently. The
  page's headline bug.
- **Undoing the used set and not the trail.** Symptom: orders that grow past the
  number of pots, and a leaf test that never fires.
- **Recording at every node** as in Exercise 1. Symptom: every partial order in
  the output, including the empty one. The two pages differ here on purpose.
- **Keeping the index as well as the used set.** Symptom: subsets in order rather
  than orderings — a much smaller answer that looks reasonable.
- **Appending `trail` rather than a copy.** Symptom: six references to one list,
  all empty at the end.
- **Running it on ten pots to "check it scales".** Symptom: three and a half
  million lists. Say the number instead.

## Acceptance checklist

- [ ] Three pots give six orders, and `order_count` agrees.
- [ ] Every order uses every pot exactly once, and appears exactly once.
- [ ] Each pot leads exactly two of the six.
- [ ] One pot gives one order; no pots gives `[[]]`.
- [ ] Five pots give 120.
- [ ] The half-undone walk finds exactly one order.
- [ ] The file runs start to finish and prints `All checks passed.`

## Stretch

- Return orders in lexicographic order by pot name, and say what has to change.
  It is one word, and knowing which is a good sign you understood the loop.
- Generate the next order from a given one, without generating the others. It is
  a genuinely different algorithm and it is what a library function does.
- Add a rule that one named pot must be fired before another, and prune. Compare
  the count against the unpruned run — half, and saying why it is exactly half is
  the interesting part.
