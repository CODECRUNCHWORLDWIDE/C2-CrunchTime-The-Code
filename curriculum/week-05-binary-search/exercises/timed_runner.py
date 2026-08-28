"""Week 5 test harness — binary search and binary search on the answer.

Point this at your own solutions and it grades them.

Usage
-----
1. Put your five drill solutions (and the challenge, if you have done it) in one
   module. The default is a file called ``solutions.py`` sitting next to this
   one, but you can point at any module::

       C2_WEEK05_SOLUTIONS=my_package.week05 pytest timed_runner.py

2. Run it::

       pytest timed_runner.py -v

Every function you have not written yet is reported as skipped, so you can run
the harness after Exercise 1 and watch the skips turn into passes across the week.

The cases below are the ones printed in the drill files plus a number of
adversarial ones that are not: values sitting between two real entries, targets
past both ends, sequences that are entirely one repeated value, and every
empty-input branch each contract defines.

Two things no test can check for you, both of which the write-up grades:

* **Space.** Several drills are specified at ``O(1)`` auxiliary space. A
  solution that rebuilds the un-rotated list, or materialises the pair sums,
  passes every assertion here and fails the drill.
* **Depth.** Nothing below distinguishes ``O(log n)`` from ``O(n)`` — the inputs
  are far too small. If you want that signal, generate a two-million-entry
  sequence yourself and time both.

Passing this harness is the floor, not the ceiling. Write your own cases too.
"""

from __future__ import annotations

import importlib
import os

import pytest

MODULE_NAME = os.environ.get("C2_WEEK05_SOLUTIONS", "solutions")


def load(function_name: str):
    """Return the learner's function, or skip the test if it is not there yet."""
    try:
        module = importlib.import_module(MODULE_NAME)
    except ModuleNotFoundError:  # pragma: no cover - environment dependent
        pytest.skip(
            f"No module named {MODULE_NAME!r}. Create it, or set "
            f"C2_WEEK05_SOLUTIONS to the module holding your solutions."
        )
    function = getattr(module, function_name, None)
    if function is None:
        pytest.skip(f"{MODULE_NAME}.{function_name} is not defined yet.")
    return function


# ---------------------------------------------------------------------------
# Exercise 1 — The Ladder Seat
#
# ratings is sorted strictly DESCENDING. Return the seat index, or None.
# The descending order is the point: ascending shrink rules walk the wrong way.
# ---------------------------------------------------------------------------

LADDER = [2410, 2205, 2199, 1870, 1602, 1044]

LADDER_SEAT_CASES = [
    (LADDER, 1870, 3),
    (LADDER, 2410, 0),          # top seat
    (LADDER, 1044, 5),          # bottom seat
    (LADDER, 2205, 1),
    (LADDER, 2199, 2),
    (LADDER, 1602, 4),
    (LADDER, 2200, None),       # between two real ratings
    (LADDER, 3000, None),       # above the whole ladder
    (LADDER, 500, None),        # below the whole ladder
    ([1200, 800], 1200, 0),
    ([1200, 800], 800, 1),
    ([1200, 800], 1000, None),  # two seats, miss in the middle
    ([900, 12, -85], -85, 2),   # negative rating is legal
    ([900, 12, -85], 900, 0),
    ([900, 12, -85], 0, None),
    ([1500], 1500, 0),
    ([1500], 1499, None),
    ([], 1500, None),           # empty ladder: never index
]


@pytest.mark.parametrize("ratings, rating, expected", LADDER_SEAT_CASES)
def test_find_ladder_seat(ratings, rating, expected):
    find_ladder_seat = load("find_ladder_seat")
    assert find_ladder_seat(list(ratings), rating) == expected


# ---------------------------------------------------------------------------
# Exercise 2 — The Scan Window
#
# Half-open slice bounds. On a miss, the empty slice at the insertion point.
# Never (-1, -1). The returned pair must always be a valid slice.
# ---------------------------------------------------------------------------

SCAN_LOG = [61, 61, 61, 64, 64, 70]

SCAN_WINDOW_CASES = [
    (SCAN_LOG, 64, (3, 5)),
    (SCAN_LOG, 61, (0, 3)),           # run starts at index 0
    (SCAN_LOG, 70, (5, 6)),           # end == len(minutes) is legal
    (SCAN_LOG, 62, (3, 3)),           # miss, insertion point mid-log
    (SCAN_LOG, 65, (5, 5)),           # miss, between the 64s and the 70
    (SCAN_LOG, 0, (0, 0)),            # before everything
    (SCAN_LOG, 99, (6, 6)),           # after everything; do not index there
    ([300, 300, 300, 300], 300, (0, 4)),   # every row matches
    ([300, 300, 300, 300], 299, (0, 0)),
    ([300, 300, 300, 300], 301, (4, 4)),
    ([1, 2, 3, 4, 5], 3, (2, 3)),     # no duplicates at all
    ([7], 7, (0, 1)),
    ([7], 6, (0, 0)),
    ([7], 8, (1, 1)),
    ([], 5, (0, 0)),                  # empty log needs no special case
]


@pytest.mark.parametrize("minutes, minute, expected", SCAN_WINDOW_CASES)
def test_scan_window(minutes, minute, expected):
    scan_window = load("scan_window")
    result = scan_window(list(minutes), minute)
    assert result == expected
    start, end = result
    assert minutes[start:end] == [minute] * (end - start), (
        "the returned bounds must slice out exactly the matching run"
    )


# ---------------------------------------------------------------------------
# Exercise 3 — The Ring Buffer Probe
#
# slots is a rotation of a strictly increasing id sequence. Return the row's
# AGE POSITION in write order, not its physical slot.
# ---------------------------------------------------------------------------

# Write order 12, 19, 33, 47, 58, 61, 64, 70 — wrapped so the oldest is slot 4.
DUMP = [58, 61, 64, 70, 12, 19, 33, 47]

ROWS_OLDER_THAN_CASES = [
    (DUMP, 12, 0),        # oldest row, sitting in slot 4
    (DUMP, 19, 1),
    (DUMP, 33, 2),
    (DUMP, 47, 3),
    (DUMP, 58, 4),        # slot 0 — answering 0 here means you never converted
    (DUMP, 61, 5),
    (DUMP, 64, 6),
    (DUMP, 70, 7),        # newest row, sitting in slot 3
    (DUMP, 50, None),     # inside the id range, still absent
    (DUMP, 11, None),     # below every id
    (DUMP, 71, None),     # above every id
    ([12, 19, 33, 47], 33, 2),    # not rotated at all
    ([12, 19, 33, 47], 12, 0),
    ([12, 19, 33, 47], 47, 3),
    ([12, 19, 33, 47], 20, None),
    ([91, 7], 1, None),
    ([91, 7], 91, 1),     # written second, so age 1, even though it is slot 0
    ([91, 7], 7, 0),
    ([5], 5, 0),
    ([5], 9, None),
    ([], 5, None),        # empty dump: guard before indexing
]


@pytest.mark.parametrize("slots, reading_id, expected", ROWS_OLDER_THAN_CASES)
def test_rows_older_than(slots, reading_id, expected):
    rows_older_than = load("rows_older_than")
    assert rows_older_than(list(slots), reading_id) == expected


# ---------------------------------------------------------------------------
# Exercise 4 — The Quote Rank
#
# Return (kth cheapest quote, count of STRICTLY cheaper quotes), 1-based k.
# The second element is not k - 1 whenever k lands inside a tie.
# ---------------------------------------------------------------------------

# handling [2, 5, 9] x linehaul [1, 4, 4] -> 3, 6, 6, 6, 9, 9, 10, 13, 13
HANDLING = [2, 5, 9]
LINEHAUL = [1, 4, 4]

QUOTE_RANK_CASES = [
    (HANDLING, LINEHAUL, 1, (3, 0)),
    (HANDLING, LINEHAUL, 2, (6, 1)),    # k - 1 happens to be right here...
    (HANDLING, LINEHAUL, 3, (6, 1)),    # ...and wrong here: k - 1 would give 2
    (HANDLING, LINEHAUL, 4, (6, 1)),    # ...and here: k - 1 would give 3
    (HANDLING, LINEHAUL, 5, (9, 4)),
    (HANDLING, LINEHAUL, 6, (9, 4)),
    (HANDLING, LINEHAUL, 7, (10, 6)),   # the one quote with no tie at all
    (HANDLING, LINEHAUL, 8, (13, 7)),
    (HANDLING, LINEHAUL, 9, (13, 7)),   # the last rank
    (HANDLING, LINEHAUL, 10, None),     # k beyond the pair count
    (HANDLING, LINEHAUL, 100, None),
    ([1, 2], [10, 20], 1, (11, 0)),     # 11, 12, 21, 22 — no ties anywhere
    ([1, 2], [10, 20], 2, (12, 1)),
    ([1, 2], [10, 20], 3, (21, 2)),
    ([1, 2], [10, 20], 4, (22, 3)),
    ([0, 0], [0, 0], 1, (0, 0)),        # every quote identical
    ([0, 0], [0, 0], 4, (0, 0)),
    ([0, 0], [0, 0], 5, None),
    ([7], [7], 1, (14, 0)),             # one quote; the interval never opens
    ([7], [7], 2, None),
    ([], [1, 4, 4], 1, None),           # empty handling list
    ([2, 5, 9], [], 1, None),           # empty linehaul list
    ([], [], 1, None),
]


@pytest.mark.parametrize("handling, linehaul, k, expected", QUOTE_RANK_CASES)
def test_quote_rank(handling, linehaul, k, expected):
    quote_rank = load("quote_rank")
    assert quote_rank(list(handling), list(linehaul), k) == expected


def test_quote_rank_matches_brute_force():
    """Cross-check against the O(nm log nm) reference on generated rate cards."""
    import random

    quote_rank = load("quote_rank")
    rng = random.Random(20250506)
    for _ in range(400):
        n, m = rng.randrange(0, 6), rng.randrange(0, 6)
        handling = sorted(rng.randrange(0, 12) for _ in range(n))
        linehaul = sorted(rng.randrange(0, 12) for _ in range(m))
        quotes = sorted(h + t for h in handling for t in linehaul)
        for k in range(1, len(quotes) + 3):
            if k <= len(quotes):
                quote = quotes[k - 1]
                expected = (quote, sum(1 for q in quotes if q < quote))
            else:
                expected = None
            assert quote_rank(handling, linehaul, k) == expected, (
                handling,
                linehaul,
                k,
            )


# ---------------------------------------------------------------------------
# Exercise 5 — The Paving Reach
#
# One section per night. Return the smallest whole-metre reach, 0 on an empty
# road, None when the budget cannot be met at any reach.
# ---------------------------------------------------------------------------

ROAD = [30, 12, 21, 5, 18]

PAVING_REACH_CASES = [
    (ROAD, 6, 21),
    (ROAD, 7, 18),
    (ROAD, 10, 11),
    (ROAD, 5, 30),          # nights == sections, so the answer is max(sections)
    (ROAD, 4, None),        # fewer nights than sections: unsatisfiable
    (ROAD, 0, None),
    ([4, 4], 3, 4),         # ceil(sum / nights) = 3 and 3 does not work
    ([4, 4], 2, 4),
    ([4, 4], 4, 2),
    ([7], 1, 7),
    ([7], 3, 3),
    ([7], 7, 1),
    ([9, 9, 9], 3, 9),
    ([9, 9, 9], 6, 5),
    ([1, 1, 1], 2, None),
    ([1_000_000_000], 1_000_000_000, 1),   # predicate true at the very bottom
    ([], 0, 0),             # empty road: no train needed, and max([]) would raise
    ([], 5, 0),
    ([12], 0, None),        # the unsatisfiable check fires on the count
]


@pytest.mark.parametrize("sections, nights, expected", PAVING_REACH_CASES)
def test_min_nightly_reach(sections, nights, expected):
    min_nightly_reach = load("min_nightly_reach")
    assert min_nightly_reach(list(sections), nights) == expected


# ---------------------------------------------------------------------------
# Challenge 1 — The Merged Book Boundary
#
# (kth, (k+1)th) of the combined multiset, 1-based k. Second element is None at
# the last rank; the whole result is None when k is out of range.
# ---------------------------------------------------------------------------

VENUE_A = [3, 8, 8, 15]
VENUE_B = [1, 4, 9]        # combined: 1, 3, 4, 8, 8, 9, 15

BOOK_BOUNDARY_CASES = [
    (VENUE_A, VENUE_B, 1, (1, 3)),      # pair comes from two different venues
    (VENUE_A, VENUE_B, 2, (3, 4)),
    (VENUE_A, VENUE_B, 3, (4, 8)),
    (VENUE_A, VENUE_B, 4, (8, 8)),      # tie straddles the split
    (VENUE_A, VENUE_B, 5, (8, 9)),
    (VENUE_A, VENUE_B, 6, (9, 15)),
    (VENUE_A, VENUE_B, 7, (15, None)),  # last rank: no successor
    (VENUE_A, VENUE_B, 8, None),        # above range
    (VENUE_A, VENUE_B, 0, None),        # below range; k is 1-based
    (VENUE_A, VENUE_B, -3, None),
    ([], [42], 1, (42, None)),          # one venue empty
    ([42], [], 1, (42, None)),          # the mirror, exercising the swap
    ([], [], 1, None),
    ([1, 2, 3], [10, 20, 30], 1, (1, 2)),
    ([1, 2, 3], [10, 20, 30], 3, (3, 10)),    # disjoint: split at an endpoint
    ([1, 2, 3], [10, 20, 30], 4, (10, 20)),   # the other endpoint
    ([1, 2, 3], [10, 20, 30], 5, (20, 30)),
    ([1, 2, 3], [10, 20, 30], 6, (30, None)),
    ([10, 20, 30], [1, 2, 3], 3, (3, 10)),    # argument order must not matter
    ([5, 5, 5], [5, 5], 3, (5, 5)),           # every comparison an equality
    ([-9, -4, 0], [-7, 2], 2, (-7, -4)),      # signed: -9, -7, -4, 0, 2
    ([-9, -4, 0], [-7, 2], 5, (2, None)),
]


@pytest.mark.parametrize("venue_a, venue_b, k, expected", BOOK_BOUNDARY_CASES)
def test_book_boundary(venue_a, venue_b, k, expected):
    book_boundary = load("book_boundary")
    assert book_boundary(list(venue_a), list(venue_b), k) == expected


def test_book_boundary_matches_brute_force():
    """Cross-check against the O((m+n) log(m+n)) reference on generated books.

    This is the test that finds sentinel bugs. Write the generator before you
    write the solution, not after.
    """
    import random

    book_boundary = load("book_boundary")
    rng = random.Random(20250505)
    for _ in range(500):
        m, n = rng.randrange(0, 9), rng.randrange(0, 9)
        a = sorted(rng.randrange(-20, 21) for _ in range(m))
        b = sorted(rng.randrange(-20, 21) for _ in range(n))
        merged = sorted(a + b)
        for k in range(0, len(merged) + 2):
            if 1 <= k <= len(merged):
                nxt = merged[k] if k < len(merged) else None
                expected = (merged[k - 1], nxt)
            else:
                expected = None
            assert book_boundary(a, b, k) == expected, (a, b, k)
