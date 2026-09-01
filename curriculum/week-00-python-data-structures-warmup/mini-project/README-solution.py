"""README-solution.py — a finished cost table, measured rather than believed.

This is the reference deliverable for the Week 0 mini-project: the cheat sheet's
claims, checked, with the reason each one is true written from the memory layout
rather than restated from the table.

It extends the starter (growth_lab.py) instead of repeating it. The starter
already counts appends, front removals from a list lane and a ring lane, scans
against probes, and += against join. Two claims from the brief's required list
are missing there, and they are the two that catch people out:

  * a slice costs its length in SPACE as well as time, and
  * heapify is linear, not n log n, even though it looks like n insertions.

Everything is COUNTED, never timed. A stopwatch measures the machine; a counter
measures the algorithm, and only the second one is the same on your laptop as it
is on mine. That is also why this file's output is identical every run, which is
what lets the page publish it as expected output.

The section labels below are printed in plain capitals rather than as Markdown
headings on purpose: this output is published inside a fenced block on the page,
and a "##" line inside that fence reads as a new page section to anything that
splits the page on headings.

The self-checks at the bottom assert the shape of every claim. When they pass the
file prints "All checks passed."
"""

from growth_lab import SIZES, TOLERANCE, report, verdict

# ------------------------------------------------------------- the slice ----


def slice_chars_copied(size: int) -> int:
    """Count the characters a half-open slice has to copy.

    A slice is a new string. Python has no view type for `str`, so `s[a:b]`
    allocates `b - a` characters and copies them in — which is why the cost is
    `O(k)` in space as well as in time. Nothing here is measured by timing; the
    count IS the length, and that is the whole point.

    Args:
        size: The length of the string being sliced.

    Returns:
        The number of characters copied by taking the middle half of it.
    """
    text = "x" * size
    start, stop = size // 4, size // 4 * 3
    piece = text[start:stop]
    return len(piece)


# -------------------------------------------------------------- the heap ----
#
# Both builders below are written out rather than calling heapq, because the
# claim under test is about how much work the build does, and a library call
# does its work where a counter cannot see it.


def _sift_down(heap: list[int], start: int, count: list[int]) -> None:
    """Push one element down to its place, counting every swap."""
    size = len(heap)
    root = start
    while True:
        child = 2 * root + 1
        if child >= size:
            return
        if child + 1 < size and heap[child + 1] < heap[child]:
            child += 1
        if heap[root] <= heap[child]:
            return
        heap[root], heap[child] = heap[child], heap[root]
        count[0] += 1
        root = child


def _sift_up(heap: list[int], start: int, count: list[int]) -> None:
    """Pull one element up to its place, counting every swap."""
    child = start
    while child > 0:
        parent = (child - 1) // 2
        if heap[parent] <= heap[child]:
            return
        heap[parent], heap[child] = heap[child], heap[parent]
        count[0] += 1
        child = parent


def _values(size: int) -> list[int]:
    """A fixed, reproducible spread of values — no randomness, no seed to forget."""
    return [(i * 7919) % size for i in range(size)]


def heapify_swaps(size: int) -> int:
    """Swaps performed building a heap bottom-up, the way heapify does it.

    Sift-down from the last parent to the root. The elements near the bottom —
    which is most of them — can only fall a short distance, so the total is
    bounded by a constant times `n`, not by `n log n`.

    Args:
        size: How many values to heapify.

    Returns:
        Total swaps performed.
    """
    heap = _values(size)
    count = [0]
    for start in range(len(heap) // 2 - 1, -1, -1):
        _sift_down(heap, start, count)
    return count[0]


def push_swaps(size: int) -> int:
    """Swaps performed building the same heap by n separate insertions.

    Each insertion sifts UP from the bottom, and an element inserted into a heap
    of height h can climb the whole height. This is the `n log n` build, and it
    is what intuition reaches for when it hears "build a heap".

    Args:
        size: How many values to insert one at a time.

    Returns:
        Total swaps performed.
    """
    heap: list[int] = []
    count = [0]
    for value in _values(size):
        heap.append(value)
        _sift_up(heap, len(heap) - 1, count)
    return count[0]


# ------------------------------------------------------------ the report ----

EXTRA_ROWS: list[tuple[str, str, object, float | None]] = [
    ("characters copied, slicing the middle half of n", "O(k) time AND space", slice_chars_copied, 2.0),
    ("swaps, heap built bottom-up (heapify)", "O(n) in total", heapify_swaps, 2.0),
    ("swaps, same heap built by n pushes", "O(n log n) in total", push_swaps, 2.0),
]


def extra_report(sizes: tuple[int, int]) -> str:
    """Render the two required rows the starter does not cover.

    Args:
        sizes: The smaller and the larger job size.

    Returns:
        A Markdown table. No trailing newline.
    """
    small_size, large_size = sizes
    lines = [
        f"| what was counted | the claim | n={small_size} | n={large_size} | growth | verdict |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for label, claim, measure, expected in EXTRA_ROWS:
        small = measure(small_size)
        large = measure(large_size)
        growth, settled = verdict(small, large, expected)
        lines.append(f"| {label} | `{claim}` | {small} | {large} | {growth} | {settled} |")
    return "\n".join(lines)


WHY = """\
| row | why it is true, from the memory layout |
| --- | --- |
| slice | `str` is a fixed block of characters with no view type, so a slice must allocate its own block and copy into it. The space is the same `k` as the time. |
| heapify | Sift-down from the last parent upward. Half the elements are leaves and cannot fall at all; a quarter can fall one level; an eighth two. The sum converges to a constant times `n`. |
| n pushes | Sift-up from the bottom. A new element can climb the full height of the heap, and the heap is `log n` tall for most of the build, so the total carries the log. |
"""


# ---- Self-check ----
if __name__ == "__main__":
    print("MEASURED - the starter's rows\n")
    print(report(SIZES))
    print()
    print("MEASURED - the two the starter leaves to you\n")
    print(extra_report(SIZES))
    print()
    print("WHY, FROM THE MEMORY LAYOUT\n")
    print(WHY)

    small, large = SIZES

    # A slice copies exactly its own length. Not a claim about speed: a count.
    assert slice_chars_copied(small) == small // 4 * 3 - small // 4
    assert slice_chars_copied(large) == large // 4 * 3 - large // 4

    # Doubling the input doubles the characters copied — linear, as claimed.
    assert abs(slice_chars_copied(large) / slice_chars_copied(small) - 2.0) <= TOLERANCE

    # The heap claims. Bottom-up stays under one swap per element; insertion
    # does not, and the gap widens with n — which is the whole lesson.
    assert heapify_swaps(small) < small
    assert heapify_swaps(large) < large
    assert push_swaps(small) > heapify_swaps(small)
    assert push_swaps(large) / push_swaps(small) > heapify_swaps(large) / heapify_swaps(small)

    print("All checks passed.")
