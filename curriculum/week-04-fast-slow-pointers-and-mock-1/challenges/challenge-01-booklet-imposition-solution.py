"""challenge-01-booklet-imposition-solution.py — collate a booklet outside-in.

Three small jobs, done in a row, none of which needs a spare copy of the
chain:

1. Find the earlier of the two middle pages and cut the chain there, so the
   front half is never shorter than the back half.
2. Turn the back half around, one page at a time.
3. Zip the two halves together, taking from the turned-around back half
   first, and let whatever is left of the front half stay attached.

The booklets are built in this file, so it runs on its own with no imports.

The self-checks at the bottom print one line per booklet, then
"All checks passed."
"""

from __future__ import annotations


class Page:
    """One page of a booklet, in chain order. Only `next_page` may change."""

    def __init__(self, number: int, next_page: "Page | None" = None) -> None:
        self.number = number
        self.next_page = next_page


def build_chain(numbers: list[int]) -> Page | None:
    """Wire a booklet from a list of printed page numbers.

    Args:
        numbers: The number printed on each page, in chain order. Numbers
            may repeat and need not be sequential.

    Returns:
        The first page, or None for an empty booklet.
    """
    if not numbers:
        return None
    pages = [Page(number) for number in numbers]
    for earlier, later in zip(pages, pages[1:]):
        earlier.next_page = later
    return pages[0]


def chain_numbers(first: Page | None) -> list[int]:
    """Walk a booklet into a list of page numbers, refusing to hang.

    Args:
        first: The first page of the chain, or None.

    Returns:
        The printed numbers in feed order.

    Raises:
        AssertionError: If the chain loops, which means the rewiring is
            wrong and a plain walk would never stop.
    """
    numbers: list[int] = []
    while first is not None:
        numbers.append(first.number)
        first = first.next_page
        assert len(numbers) < 100_000, "the imposition created a loop"
    return numbers


def _lower_middle(first: Page) -> Page:
    """Return the last page of the front half — the earlier of two middles."""
    slow = first
    fast = first
    while fast.next_page is not None and fast.next_page.next_page is not None:
        slow = slow.next_page
        fast = fast.next_page.next_page
    return slow


def _reverse(first: Page | None) -> Page | None:
    """Turn a chain around in place and return its new first page."""
    previous = None
    current = first
    while current is not None:
        following = current.next_page
        current.next_page = previous
        previous = current
        current = following
    return previous


def _interleave(front: Page, back: Page | None) -> Page:
    """Zip two chains together, one page each, starting with `back`.

    Args:
        front: The front half. Never empty, and never shorter than `back`.
        back: The reversed back half, or None when the booklet has one page.

    Returns:
        The head of the zipped chain.
    """
    if back is None:
        return front

    head = back
    while back is not None:
        back_next = back.next_page
        front_next = front.next_page
        back.next_page = front
        if back_next is None:
            break  # The front half's leftover page is already attached.
        front.next_page = back_next
        back = back_next
        front = front_next
    return head


def impose(first_page: Page | None) -> Page | None:
    """Rewire a booklet into outside-in feed order and return the new head.

    Args:
        first_page: The first page of the chain, or None for no booklet.

    Returns:
        The new first page, which is the booklet's original last page.
    """
    if first_page is None:
        return None
    middle = _lower_middle(first_page)
    back = middle.next_page
    middle.next_page = None
    return _interleave(first_page, _reverse(back))


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        ([], []),
        ([7], [7]),
        ([1, 2], [2, 1]),
        ([1, 2, 3], [3, 1, 2]),
        ([1, 2, 3, 4], [4, 1, 3, 2]),
        ([1, 2, 3, 4, 5], [5, 1, 4, 2, 3]),
        ([1, 2, 3, 4, 5, 6], [6, 1, 5, 2, 4, 3]),
        ([1, 2, 3, 4, 5, 6, 7], [7, 1, 6, 2, 5, 3, 4]),
        ([11, 4, 4, 90], [90, 11, 4, 4]),
        ([-3, 12, -3], [-3, -3, 12]),
    ]

    for numbers, expected in CASES:
        fed = chain_numbers(impose(build_chain(numbers)))
        assert fed == expected, f"{numbers}: got {fed}, wanted {expected}"
        print(f"{str(numbers):<24} feeds as {fed}")

    kept = [5, 5, 9, 2, 2, 2, 8]
    assert sorted(chain_numbers(impose(build_chain(kept)))) == sorted(kept)

    long_run = chain_numbers(impose(build_chain(list(range(4000)))))
    assert len(long_run) == 4000
    assert long_run[0] == 3999
    assert long_run[1] == 0
    assert long_run[-1] == 1999
    print(f"{'4000 pages':<24} feeds as [3999, 0, 3998, 1, ..., 2000, 1999]")

    print("All checks passed.")
