# Week 0 — Mini-Project: Your Own Cost Table

> Topic: every claim on the cheat sheet · Lecture: [1](../lecture-notes/01-strings-and-immutability.md), [2](../lecture-notes/02-lists-tuples-and-the-dynamic-array.md), [3](../lecture-notes/03-dicts-sets-and-the-hash-table.md) · Difficulty: Beginner · Target time: 1 hour · Why this one: it is the week's only deliverable you will still be using in Week 12.

## The Brief

You have just read a cheat sheet full of complexity claims, and you took every
one of them on trust. This project makes you check them.

You will end up with a table of your own: one row per operation, what the cheat
sheet claims, what you measured, whether the two agree, and — the column that
matters — *why* it is true, said in terms of how the container is laid out in
memory rather than by repeating the complexity back.

Nobody remembers a table they read. People remember a table they measured.

## Starter

`growth_lab.py` sits beside this page and is already written. It counts work —
elements copied, elements shifted, comparisons, probes, characters — and prints
a Markdown table with a growth column and a verdict.

It counts rather than timing on purpose. A stopwatch measures your machine: your
laptop under load gives a different answer at lunchtime than at midnight, and a
different one again from mine. A counter measures the algorithm, and that number
is the same everywhere. It is also why this page can publish an expected output
at all.

Run it before you change anything:

```bash
python growth_lab.py
```

It covers five of the six required rows. The sixth — and the slice — are yours.

## Requirements

1. At least **twelve rows**, spanning all four containers (`str`, `list`,
   `dict`, `set`).
2. Every row carries: the exact expression, the claim from
   [the cheat sheet](../CHEATSHEET.md), your counts at two doubling sizes, the
   growth figure, a verdict, and the **why**.
3. These six rows are required; six more are yours to choose:
   - `L.append(x)` — shown to be amortised, not worst-case, `O(1)`
   - `L.pop(0)` against a ring buffer's front removal, side by side
   - `x in L` against `x in set(L)`, including the cost of building the set
   - `s += ch` in a loop against `"".join(parts)`
   - `s[a:b]` — shown to cost `O(k)` in **space** as well as time
   - `heapq.heapify(L)` — shown to be `O(n)`, not `O(n log n)`
4. The **why** cell explains from the memory layout — contiguous array, hash
   slots, immutable block — never by restating the complexity. `L.pop(0)` is not
   `O(n)` because a table says so; it is `O(n)` because a list is a contiguous
   array and removing the front forces every remaining element to shift left one
   slot.
5. At least one row where your prediction was **wrong**, with the reason written
   out.

## Constraints

- **Count, do not time.** Every measurement is a number of operations. If you
  reach for `time.perf_counter`, you have started measuring your laptop.
- **Two doubling sizes, minimum**, and large enough to see the trend. At
  `n = 100` everything looks constant.
- **Read the growth column, not the raw counts.** A ratio near 2 per doubling is
  linear, near 4 is quadratic, near 1 is constant. Slightly above 2 is
  `n log n`, and at small `n` it is genuinely hard to tell from linear — say so
  honestly rather than over-claiming.
- **No randomness without a fixed sequence.** A table you cannot reproduce is a
  table you cannot defend.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python README.py
MEASURED - the starter's rows

| what was counted | the claim | n=1000 | n=2000 | growth | verdict |
| --- | --- | ---: | ---: | ---: | --- |
| elements copied, n appends | `amortised O(1) each` | 1020 | 2044 | 2.00x | confirmed |
| elements shifted, n front removals from a list lane | `O(n) each` | 499500 | 1999000 | 4.00x | confirmed |
| elements shifted, n front removals from a ring lane | `O(1) each` | 0 | 0 | - | confirmed - no work either way |
| comparisons, 20 misses in a row of n | `O(n) each` | 20000 | 40000 | 2.00x | confirmed |
| probes, 20 misses in a table of n | `O(1) average each` | 40 | 49 | 1.23x | confirmed |
| characters copied, banner built with += | `O(n^2) in total` | 2502500 | 10005000 | 4.00x | confirmed |
| characters copied, banner built with join | `O(n) in total` | 5000 | 10000 | 2.00x | confirmed |

MEASURED - the two the starter leaves to you

| what was counted | the claim | n=1000 | n=2000 | growth | verdict |
| --- | --- | ---: | ---: | ---: | --- |
| characters copied, slicing the middle half of n | `O(k) time AND space` | 500 | 1000 | 2.00x | confirmed |
| swaps, heap built bottom-up (heapify) | `O(n) in total` | 704 | 1358 | 1.93x | confirmed |
| swaps, same heap built by n pushes | `O(n log n) in total` | 1580 | 3606 | 2.28x | confirmed |

WHY, FROM THE MEMORY LAYOUT

| row | why it is true, from the memory layout |
| --- | --- |
| slice | `str` is a fixed block of characters with no view type, so a slice must allocate its own block and copy into it. The space is the same `k` as the time. |
| heapify | Sift-down from the last parent upward. Half the elements are leaves and cannot fall at all; a quarter can fall one level; an eighth two. The sum converges to a constant times `n`. |
| n pushes | Sift-up from the bottom. A new element can climb the full height of the heap, and the heap is `log n` tall for most of the build, so the total carries the log. |

All checks passed.
```

The two heap rows are the ones to look at. Both build the same heap from the
same values. Bottom-up does it in fewer swaps than there are elements; insertion
does it in more, and the gap widens as `n` grows. That is the whole claim, in
two lines of a table.

## Steps

1. Run `growth_lab.py` and read its table. Five required rows are already there.
2. Add the slice row. Count the characters a slice copies — the count *is* the
   length, which is the point.
3. Add the two heap rows. Write both builders out by hand: the claim is about
   how much work the build does, and a call to `heapq` does its work where your
   counter cannot see it.
4. Fill in the **why** column for every row, from the memory layout.
5. Add six rows of your own. Pick operations you are not sure about — a table of
   twelve confirmations teaches less than one contradiction.
6. Write down every prediction you got wrong, and why.

## The Solution

```python
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
```

The file extends the starter rather than repeating it — `from growth_lab import
report, verdict` — because the starter's five rows are already right and copying
them would be two tables to keep in step.

Both heap builders are written out longhand for the reason step 3 gives. The
counting is deliberately plain: a one-element list passed down as a counter,
rather than a class, because the subject is the heap and not the bookkeeping.

The self-checks at the bottom assert the *shape* of each claim rather than the
exact numbers — `heapify_swaps(n) < n`, and the insertion build growing faster
than the bottom-up build. Asserting the literal counts would make the file fail
the day someone changes the input spread, which is not what is being defended.

## Run it

Download the solution beside this page and run it:

```bash
python README.py
```

It needs `growth_lab.py` in the same folder. No third-party packages, no
arguments, no input. It prints the tables and then `All checks passed.`

Or open it in the browser IDE from the Run button on the block above.

## Common bugs to catch

- **Timing instead of counting.** Symptom: the growth column moves between runs,
  and a "confirmed" becomes a "CHECK IT" when something else on your machine
  wakes up. Fix: count operations.
- **Sizes too small.** Symptom: everything looks constant, every verdict is
  wrong. At `n = 100` a quadratic has not had room to separate from a linear.
- **Calling `heapq.heapify` and expecting a count.** Symptom: nothing to report,
  because the work happened inside C. Fix: write the sift-down yourself.
- **Reading the slice row as time only.** Symptom: the space column says `O(1)`.
  A slice allocates the characters it copies; there is no view type for `str`.
- **`AssertionError` with no message on the last line.** The self-checks compare
  counted work; if you changed `_values`, the spread changed with it. Re-derive
  the bound rather than loosening the assert.

## Acceptance checklist

- [ ] Twelve or more rows, spanning all four containers.
- [ ] Every **why** cell explains from the memory layout, not by restating the
      complexity.
- [ ] At least one row where your prediction was wrong, with the reason written.
- [ ] Amortised append is explained as a statement about the total, not about a
      single call.
- [ ] Auxiliary space is distinguished from output space at least once.
- [ ] The file runs start to finish and prints `All checks passed.`
- [ ] Two runs on two different machines give the same table.

## Stretch

Add a row for an operation whose complexity you could **not** confirm by
measurement, and explain why the measurement failed.

Good candidates: a dict's worst-case `O(n)`, which you cannot trigger without
adversarial keys chosen against the hash; and CPython's `+=` refcount
optimisation, which appears and disappears depending on whether a second
reference to the string exists. Understanding why a claim resists measurement is
worth as much as measuring one that does not.

## Up Next

[Week 1 — The FRAME Method and Thinking Aloud](../../week-01-the-frame-method-and-thinking-aloud/README.md). Bring the cost table; Week 2 grades complexity for real.
