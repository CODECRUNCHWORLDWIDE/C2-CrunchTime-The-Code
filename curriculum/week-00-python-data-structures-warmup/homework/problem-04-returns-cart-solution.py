"""problem-04-returns-cart-solution.py — the library's returns cart.

Every book on the cart carries a title, a shelf mark and how many days late
it came back. The desk wants two orderings out of the same cart, and both
of them have a tie in them.

One tuple key says a whole ordering rule, in the order you would say it out
loud. That is the entire lesson here.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

from typing import NamedTuple


class Returned(NamedTuple):
    """One book on the cart."""

    title: str
    shelf: str
    days_late: int


CART: list[Returned] = [
    Returned("Tide Tables", "REF", 4),
    Returned("Bread Science", "641", 11),
    Returned("Knot Work", "623", 4),
    Returned("Salt Marsh Birds", "598", 11),
    Returned("Kiln Repair", "738", 0),
    Returned("Ferry Timetables", "REF", 2),
]


def by_lateness(cart: list[Returned]) -> list[Returned]:
    """Return a NEW cart ordered latest first.

    Args:
        cart: The books to order. This list is not changed.

    Returns:
        A new list, most days late first, ties broken by title A to Z.
    """
    return sorted(cart, key=lambda book: (-book.days_late, book.title))


def by_shelf(cart: list[Returned]) -> list[Returned]:
    """Return a NEW cart in the order a trolley walks the shelves.

    Args:
        cart: The books to order. This list is not changed.

    Returns:
        A new list, shelf marks A to Z as text, ties broken by title.
    """
    return sorted(cart, key=lambda book: (book.shelf, book.title))


def worst_offender(cart: list[Returned]) -> Returned | None:
    """Return the single latest book.

    Args:
        cart: The books to search.

    Returns:
        The whole record, ties broken by title A to Z, or None on an empty
        cart.
    """
    if not cart:
        return None
    return min(cart, key=lambda book: (-book.days_late, book.title))


def total_days_late(cart: list[Returned]) -> int:
    """Add up the days late across the whole cart.

    Args:
        cart: The books to add up.

    Returns:
        The sum of every book's days late.
    """
    return sum(book.days_late for book in cart)


# ---- Self-check ----
if __name__ == "__main__":
    for book in by_lateness(CART):
        print(f"{book.days_late:>3}d  {book.shelf:<4} {book.title}")
    print("shelf walk: " + ", ".join(book.shelf for book in by_shelf(CART)))
    print(f"worst: {worst_offender(CART).title}")
    print(f"total days late: {total_days_late(CART)}")

    assert [b.title for b in by_lateness(CART)][:2] == ["Bread Science", "Salt Marsh Birds"]
    assert [b.title for b in by_lateness(CART)][2] == "Knot Work"  # not Tide Tables
    assert [b.shelf for b in by_shelf(CART)] == ["598", "623", "641", "738", "REF", "REF"]
    assert by_shelf(CART)[-2].title == "Ferry Timetables"
    assert worst_offender(CART).title == "Bread Science"
    assert worst_offender([]) is None
    assert total_days_late(CART) == 32
    assert CART[0].title == "Tide Tables"  # the cart is untouched
    print("All checks passed.")
