"""Week 1 test harness — arrays and two pointers.

Point this at your own solutions and it grades them.

Usage
-----
1. Put your five drill solutions in one module. The default is a file called
   ``solutions.py`` sitting next to this one, but you can point at any module::

       C2_WEEK01_SOLUTIONS=my_package.week01 pytest timed_runner.py

2. Run it::

       pytest timed_runner.py -v

Every function you have not written yet is reported as skipped, so you can run
the harness after Exercise 1 and watch the skips turn into passes across the week.

The cases below are the ones printed in the exercise files plus a handful of
adversarial ones that are not. Passing this harness is the floor, not the
ceiling: write your own cases too, especially large ones. Several exercises are
graded on O(1) auxiliary space, which no test can check for you — that part is
on your honour and on your Examine section.
"""

from __future__ import annotations

import importlib
import os

import pytest

MODULE_NAME = os.environ.get("C2_WEEK01_SOLUTIONS", "solutions")


def load(function_name: str):
    """Return the learner's function, or skip the test if it is not there yet."""
    try:
        module = importlib.import_module(MODULE_NAME)
    except ModuleNotFoundError:  # pragma: no cover - environment dependent
        pytest.skip(
            f"No module named {MODULE_NAME!r}. Create it, or set "
            f"C2_WEEK01_SOLUTIONS to the module holding your solutions."
        )
    function = getattr(module, function_name, None)
    if function is None:
        pytest.skip(f"{MODULE_NAME}.{function_name} is not defined yet.")
    return function


# ---------------------------------------------------------------------------
# Exercise 1 — Reverse the Siding
# ---------------------------------------------------------------------------

REVERSE_SIDING_CASES = [
    # cars, start, end, expected swaps, expected list afterwards
    (["HOP", "TNK", "BOX", "GON", "FLT"], 1, 3, 1,
     ["HOP", "GON", "BOX", "TNK", "FLT"]),
    (["HOP", "TNK", "BOX", "GON", "FLT"], 0, 4, 2,
     ["FLT", "GON", "BOX", "TNK", "HOP"]),
    (["HOP", "TNK", "BOX", "GON"], 0, 3, 2,
     ["GON", "BOX", "TNK", "HOP"]),
    (["HOP", "TNK", "BOX", "GON", "FLT", "TNK"], 2, 5, 2,
     ["HOP", "TNK", "TNK", "FLT", "GON", "BOX"]),
    (["HOP"], 0, 0, 0, ["HOP"]),
    ([], 0, 0, 0, []),
    ([], 0, -1, 0, []),
    (["HOP", "TNK", "BOX"], 2, 1, 0, ["HOP", "TNK", "BOX"]),
    (["HOP", "TNK", "BOX"], 1, 7, 0, ["HOP", "TNK", "BOX"]),
    (["HOP", "TNK", "BOX"], -1, 2, 0, ["HOP", "TNK", "BOX"]),
    (["HOP", "TNK", "BOX"], 0, 3, 0, ["HOP", "TNK", "BOX"]),
    (["HOP", "TNK", "BOX"], 1, 1, 0, ["HOP", "TNK", "BOX"]),
]


@pytest.mark.parametrize("cars, start, end, swaps, after", REVERSE_SIDING_CASES)
def test_reverse_siding(cars, start, end, swaps, after):
    reverse_siding = load("reverse_siding")
    siding = list(cars)
    assert reverse_siding(siding, start, end) == swaps
    assert siding == after


# ---------------------------------------------------------------------------
# Exercise 2 — The Mirror Serial
# ---------------------------------------------------------------------------

MIRROR_SERIAL_CASES = [
    ("RT7-e77-E7tr", None),
    ("RT7-e77-E8tr", 2),
    ("8a-b-c8", 1),
    ("--G9", 2),
    ("Bb", None),
    ("-K-", None),
    ("--  --", None),
    ("", None),
    ("K", None),
    ("7", None),
    ("ab", 0),
    ("a-b", 0),
    ("Never odd or even", None),
    # One character drifted, mid-serial. The break is at printed index 7,
    # not at significant-sequence index 6 — the separators shift the count.
    ("Never odg or even", 7),
]


@pytest.mark.parametrize("serial, expected", MIRROR_SERIAL_CASES)
def test_first_mirror_break(serial, expected):
    first_mirror_break = load("first_mirror_break")
    assert first_mirror_break(serial) == expected


# ---------------------------------------------------------------------------
# Exercise 3 — The Widest Ballast Pair
# ---------------------------------------------------------------------------

WIDEST_BALLAST_PAIR_CASES = [
    ([120, 340, 500, 660, 880], 1000, (0, 4)),
    ([-400, -100, 0, 100, 300], 0, (1, 3)),
    ([100, 100, 100, 100], 200, (0, 3)),
    ([200, 200, 800, 800], 1000, (0, 3)),
    ([150, 150], 300, (0, 1)),
    ([150], 300, None),
    ([], 0, None),
    ([10, 20, 30], 100, None),
    ([1, 2, 3, 4, 5], 9, (3, 4)),
    ([-50, -20, -20, 70], -40, (1, 2)),
    ([0, 0], 0, (0, 1)),
    ([5], 10, None),
]


@pytest.mark.parametrize("weights, correction, expected", WIDEST_BALLAST_PAIR_CASES)
def test_widest_ballast_pair(weights, correction, expected):
    widest_ballast_pair = load("widest_ballast_pair")
    assert widest_ballast_pair(list(weights), correction) == expected


# ---------------------------------------------------------------------------
# Exercise 4 — The Stuck Gauge
# ---------------------------------------------------------------------------

COLLAPSE_STUCK_READINGS_CASES = [
    # levels, expected dropped count, expected kept prefix
    ([412, 412, 412, 415, 415, 409], 3, [412, 415, 409]),
    ([300, 300, 305, 300], 1, [300, 305, 300]),
    ([777, 777, 777, 777], 3, [777]),
    ([500, 501, 502], 0, [500, 501, 502]),
    ([-2, -2, 0, 0, -2], 2, [-2, 0, -2]),
    ([640], 0, [640]),
    ([], 0, []),
    ([0, 0, 0, 1, 0], 2, [0, 1, 0]),
    ([9, 9], 1, [9]),
    ([1, 2, 1, 2, 1], 0, [1, 2, 1, 2, 1]),
]


@pytest.mark.parametrize("levels, dropped, kept", COLLAPSE_STUCK_READINGS_CASES)
def test_collapse_stuck_readings(levels, dropped, kept):
    collapse_stuck_readings = load("collapse_stuck_readings")
    record = list(levels)
    assert collapse_stuck_readings(record) == dropped
    assert len(record) == len(levels), "do not truncate the record"
    assert record[: len(kept)] == kept


# ---------------------------------------------------------------------------
# Exercise 5 — The Market Awning
# ---------------------------------------------------------------------------

MAX_CURTAIN_AREA_CASES = [
    ([2, 6, 3, 8, 1, 7, 4], 18),
    ([2, 7, 5, 5, 7, 2], 14),
    ([5, 5], 0),
    ([0, 9, 9, 0], 0),
    ([4], 0),
    ([], 0),
    ([3, 1, 4], 3),
    ([0, 0, 0, 0], 0),
    ([6, 0, 0, 0, 6], 18),
    # Best pair is (1, 4): min(2, 5) * (4 - 1 - 1) = 2 * 2 = 4.
    # A j - i width formula gives 6 here, which is how that bug announces itself.
    ([1, 2, 3, 4, 5], 4),
]


@pytest.mark.parametrize("pole_heights, expected", MAX_CURTAIN_AREA_CASES)
def test_max_curtain_area(pole_heights, expected):
    max_curtain_area = load("max_curtain_area")
    assert max_curtain_area(list(pole_heights)) == expected


# ---------------------------------------------------------------------------
# Challenge 1 — The Settlement Trio
# ---------------------------------------------------------------------------

SETTLEMENT_TRIOS_CASES = [
    ([-5, -1, 0, 1, 4, 6], 0, [(-5, -1, 6), (-5, 1, 4), (-1, 0, 1)]),
    ([-2, -2, 0, 2, 2, 4], 0, [(-2, -2, 4), (-2, 0, 2)]),
    ([1, 3, 5, 7, 9], 15, [(1, 5, 9), (3, 5, 7)]),
    ([-7, -3, -3, 10, 6], 0, [(-7, -3, 10), (-3, -3, 6)]),
    ([5, 5, 5, 1, 1, 9], 15, [(1, 5, 9), (5, 5, 5)]),
    ([2, 2, 2, 2], 6, [(2, 2, 2)]),
    ([0, 0, 0, 0], 0, [(0, 0, 0)]),
    ([3, 3, 3], 9, [(3, 3, 3)]),
    ([3, 3], 9, []),
    ([], 0, []),
    ([1, 2, 4, 8], 100, []),
]


@pytest.mark.parametrize("amounts, suspense, expected", SETTLEMENT_TRIOS_CASES)
def test_settlement_trios(amounts, suspense, expected):
    settlement_trios = load("settlement_trios")
    assert settlement_trios(list(amounts), suspense) == expected


# ---------------------------------------------------------------------------
# Challenge 2 — Ponding on the Levee Road
# ---------------------------------------------------------------------------

PONDED_VOLUME_CASES = [
    ([4, 1, 3, 0, 2, 5], 100, 10),
    ([4, 1, 3, 0, 2, 5], 2, 7),
    ([4, 1, 3, 0, 2, 5], 0, 0),
    ([1, 5, 2, 6, 3], 100, 3),
    ([8, 0, 5, 0, 8], 3, 9),
    ([9, 6, 4, 1], 100, 0),
    ([3, 3, 3], 100, 0),
    ([2, 0, 2], 5, 2),
    ([3, 0, 0, 3], 100, 6),
    ([7, 2], 100, 0),
    ([7], 100, 0),
    ([], 100, 0),
]


@pytest.mark.parametrize("crown, shoulder, expected", PONDED_VOLUME_CASES)
def test_ponded_volume(crown, shoulder, expected):
    ponded_volume = load("ponded_volume")
    assert ponded_volume(list(crown), shoulder) == expected
