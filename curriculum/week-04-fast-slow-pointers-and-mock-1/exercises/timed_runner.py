"""Week 4 test harness — fast/slow pointers.

Point this at your own solutions and it grades them.

Usage
-----
1. Put your five drill solutions, and both challenges, in one module. The
   default is a file called ``solutions.py`` sitting next to this one, but you
   can point at any module::

       C2_WEEK04_SOLUTIONS=my_package.week04 pytest timed_runner.py

2. Run it::

       pytest timed_runner.py -v

Every function you have not written yet is reported as skipped, so you can run
the harness after Exercise 1 and watch the skips turn into passes across the week.

The seven functions it grades are ``loop_size``, ``find_escalation_loop``,
``mid_roll_point``, ``next_slot`` and ``rotation_shape``, ``hop_landing``,
``impose``, and ``find_weld``.

The node classes and the builders live *here*, not in your solutions module.
Your functions receive objects built by this file and should read the attribute
names the drill specifies (``forwards_to``, ``escalates_to``, ``next_segment``,
``repeats_to``, ``next_page``, ``feeds_to``). Do not redefine the classes in
your own module and do not convert the chains into lists — most of these
problems are graded on O(1) auxiliary space, which no test can check for you.
That part is on your honour and on your Examine (cost) section.

Two conventions run through the week and they are deliberately opposed.
Exercises 1, 2, 3 and 5 and both challenges walk objects, so identity (``is``)
is the comparison; labels repeat on purpose and several cases below exist only
to punish ``==``. Exercise 4 walks integers, so equality (``==``) is the
comparison, and the large cases exist only to punish ``is``.

Every case below is author-generated. The ones printed in the drill files are
here, plus adversarial ones that are not. Passing this harness is the floor, not
the ceiling: write your own cases too, especially large ones.
"""

from __future__ import annotations

import importlib
import os

import pytest

MODULE_NAME = os.environ.get("C2_WEEK04_SOLUTIONS", "solutions")

CYCLE_GUARD = 10_000_000


def load(function_name: str):
    """Return the learner's function, or skip the test if it is not there yet."""
    try:
        module = importlib.import_module(MODULE_NAME)
    except ModuleNotFoundError:  # pragma: no cover - environment dependent
        pytest.skip(
            f"No module named {MODULE_NAME!r}. Create it, or set "
            f"C2_WEEK04_SOLUTIONS to the module holding your solutions."
        )
    function = getattr(module, function_name, None)
    if function is None:
        pytest.skip(f"{MODULE_NAME}.{function_name} is not defined yet.")
    return function


# ---------------------------------------------------------------------------
# Structures and builders
# ---------------------------------------------------------------------------


class Chute:
    """Exercise 1. A parcel-sorter chute with exactly one outgoing edge."""

    def __init__(self, chute_id: str, forwards_to: "Chute | None" = None) -> None:
        self.chute_id = chute_id
        self.forwards_to = forwards_to


class Rota:
    """Exercise 2. An on-call slot that escalates to exactly one other slot."""

    def __init__(self, slot: str, escalates_to: "Rota | None" = None) -> None:
        self.slot = slot
        self.escalates_to = escalates_to


class Segment:
    """Exercise 3. One block of a live stream, followed forward only."""

    def __init__(self, segment_id: str, next_segment: "Segment | None" = None) -> None:
        self.segment_id = segment_id
        self.next_segment = next_segment


class Mast:
    """Exercise 5. One relay mast, repeating onward to exactly one other."""

    def __init__(self, call_sign: str, repeats_to: "Mast | None" = None) -> None:
        self.call_sign = call_sign
        self.repeats_to = repeats_to


class Page:
    """Challenge 1. One page of a booklet, in chain order."""

    def __init__(self, number: int, next_page: "Page | None" = None) -> None:
        self.number = number
        self.next_page = next_page


class Pan:
    """Challenge 2. One pan on a conveyor, feeding exactly one other."""

    def __init__(self, tag: str, feeds_to: "Pan | None" = None) -> None:
        self.tag = tag
        self.feeds_to = feeds_to


def _wire(cls, link_attr, labels, loop_to):
    """Build a chain of `cls` from `labels`, optionally looping the tail back.

    `loop_to` is an index into `labels`, or None for a chain that terminates.
    Returns (first_node, nodes) so tests can assert on identity, not on labels.
    """
    if not labels:
        return None, []
    nodes = [cls(label) for label in labels]
    for earlier, later in zip(nodes, nodes[1:]):
        setattr(earlier, link_attr, later)
    if loop_to is not None:
        setattr(nodes[-1], link_attr, nodes[loop_to])
    return nodes[0], nodes


def build_sorter(ids, loop_to=None):
    """Exercise 1's builder. Returns the entry chute (or None for no sorter)."""
    return _wire(Chute, "forwards_to", ids, loop_to)[0]


def build_rota(labels, loop_to=None):
    """Exercise 2's builder. Returns the starting slot (or None for no rota)."""
    return _wire(Rota, "escalates_to", labels, loop_to)[0]


def build_stream(ids):
    """Exercise 3's builder. Returns the first segment (or None for empty)."""
    return _wire(Segment, "next_segment", ids, None)[0]


def build_network(call_signs, loop_to=None):
    """Exercise 5's builder. Returns (first mast, masts) for identity checks."""
    return _wire(Mast, "repeats_to", call_signs, loop_to)


def build_chain(numbers):
    """Challenge 1's builder. Returns the first page (or None for empty)."""
    return _wire(Page, "next_page", numbers, None)[0]


def build_lines(lead_a, lead_b, shared):
    """Challenge 2's builder. Two feed lines onto one shared discharge run.

    Returns (head of A, head of B, the shared pans). `shared` empty means the
    two lines never meet.
    """
    pans_a = [Pan(tag) for tag in lead_a]
    pans_b = [Pan(tag) for tag in lead_b]
    pans_shared = [Pan(tag) for tag in shared]

    for run in (pans_a, pans_b, pans_shared):
        for earlier, later in zip(run, run[1:]):
            earlier.feeds_to = later
    if pans_shared:
        if pans_a:
            pans_a[-1].feeds_to = pans_shared[0]
        if pans_b:
            pans_b[-1].feeds_to = pans_shared[0]

    head_a = (pans_a or pans_shared or [None])[0]
    head_b = (pans_b or pans_shared or [None])[0]
    return head_a, head_b, pans_shared


def last_pan(first):
    """Walk a feed line to its end, refusing to hang on a leftover knot."""
    last, seen = first, 0
    while last.feeds_to is not None:
        last = last.feeds_to
        seen += 1
        assert seen < CYCLE_GUARD, "the diagnostic left the plant rewired"
    return last


def chain_numbers(first):
    """Walk a page chain into a list of numbers, refusing to hang on a cycle."""
    out = []
    while first is not None:
        out.append(first.number)
        first = first.next_page
        assert len(out) < CYCLE_GUARD, "the imposition created a cycle"
    return out


# ---------------------------------------------------------------------------
# Exercise 1 — The Conveyor Loop
# ---------------------------------------------------------------------------

LOOP_SIZE_CASES = [
    # ids, loop_to, expected loop size
    (["IN", "S1", "S2", "S3"], 1, 3),        # tail of 1, loop of 3
    (["IN"], 0, 1),                          # a chute wired to itself
    (["A", "B"], 0, 2),
    (["IN", "S1", "OUT"], None, 0),          # correctly wired
    ([], None, 0),                           # no sorter at all
    (["A", "B", "C", "D", "E"], 4, 1),       # long tail, minimal loop
    (["A", "B", "C", "D", "E"], 2, 3),
    (["A", "B", "C", "D", "E"], 0, 5),       # the whole sorter is the loop
    # Duplicate stencils. The first has no loop and the second does; a
    # solution keeping a set of ids gets both of these backwards.
    (["S-12", "S-12"], None, 0),
    (["S-12", "S-12"], 0, 2),
    (["R4", "R4", "R4", "R4", "R4"], 3, 2),
    # Large enough that a visited set would be the wrong instinct.
    ([f"C{i}" for i in range(200_000)], 199_999, 1),
    ([f"C{i}" for i in range(200_000)], 0, 200_000),
    ([f"C{i}" for i in range(200_000)], None, 0),
]


@pytest.mark.parametrize("ids, loop_to, expected", LOOP_SIZE_CASES)
def test_loop_size(ids, loop_to, expected):
    loop_size = load("loop_size")
    assert loop_size(build_sorter(ids, loop_to)) == expected


# ---------------------------------------------------------------------------
# Exercise 2 — The Escalation Loop
# ---------------------------------------------------------------------------

ESCALATION_CASES = [
    # labels, loop_to, expected entrance index, expected hops
    (["L1", "L2", "L3", "L4"], 1, 1, 1),
    # The meeting point here is L5, which is not the entrance. Returning the
    # phase-1 collision gives (4, 4) instead of (2, 2).
    (["L1", "L2", "L3", "L4", "L5", "L6"], 2, 2, 2),
    (["A"], 0, 0, 0),                        # self-escalating slot
    (["A", "B", "C", "D"], 0, 0, 0),         # start is already the entrance
    (["A", "B", "C", "D", "E", "F", "G"], 6, 6, 6),
    # Every slot carries the same label. Identity is the only thing that means
    # anything, and the expected entrance is checked by identity below.
    (["weekend-primary"] * 4, 1, 1, 1),
    ([f"S{i}" for i in range(1000)], 500, 500, 500),
]


@pytest.mark.parametrize("labels, loop_to, entrance_index, hops", ESCALATION_CASES)
def test_find_escalation_loop(labels, loop_to, entrance_index, hops):
    find_escalation_loop = load("find_escalation_loop")
    first, nodes = _wire(Rota, "escalates_to", labels, loop_to)
    result = find_escalation_loop(first)
    assert result is not None, "this rota does loop"
    entrance, reported_hops = result
    assert entrance is nodes[entrance_index], "wrong slot: compare by identity"
    assert reported_hops == hops


TERMINATING_ROTA_CASES = [
    ["L1", "L2", "L3"],
    ["A"],
    [],
    ["dup", "dup", "dup"],
    [f"S{i}" for i in range(1000)],
]


@pytest.mark.parametrize("labels", TERMINATING_ROTA_CASES)
def test_find_escalation_loop_terminating(labels):
    """A correct rota returns None outright, not a pair containing None."""
    find_escalation_loop = load("find_escalation_loop")
    assert find_escalation_loop(build_rota(labels, None)) is None


# ---------------------------------------------------------------------------
# Exercise 3 — The Mid-Roll Break
# ---------------------------------------------------------------------------

MID_ROLL_CASES = [
    # ids, expected index of the lower middle
    (["s1", "s2", "s3", "s4", "s5"], 2),
    (["s1", "s2", "s3", "s4", "s5", "s6"], 2),   # lower, not upper
    (["s1", "s2", "s3", "s4"], 1),               # upper-middle bug shows here
    (["s1", "s2", "s3"], 1),
    (["s1", "s2"], 0),
    (["s1"], 0),
    (["s1", "s2", "s3", "s4", "s5", "s6", "s7"], 3),
    (["AD", "AD", "AD", "AD"], 1),               # repeated marker segments
    ([f"b{i}" for i in range(1000)], 499),
    ([f"b{i}" for i in range(1001)], 500),
]


@pytest.mark.parametrize("ids, expected_index", MID_ROLL_CASES)
def test_mid_roll_point(ids, expected_index):
    mid_roll_point = load("mid_roll_point")
    first, nodes = _wire(Segment, "next_segment", ids, None)
    result = mid_roll_point(first)
    assert result is not None, "this stream is not empty"
    segment, before = result
    assert segment is nodes[expected_index], "wrong segment: compare by identity"
    assert before == expected_index


def test_mid_roll_point_empty_stream():
    """None, not (None, 0) — a caller unpacking the result must fail loudly."""
    mid_roll_point = load("mid_roll_point")
    assert mid_roll_point(build_stream([])) is None


# ---------------------------------------------------------------------------
# Exercise 4 — The Wear-Level Rotation
# ---------------------------------------------------------------------------

NEXT_SLOT_CASES = [
    (0, 12, 1),
    (5, 12, 2),
    (11, 12, 2),        # 121 + 1 = 122, and 122 % 12 = 2
    (7, 1000, 50),
    (999, 1000, 2),     # 998001 + 1 = 998002, and 998002 % 1000 = 2
    (0, 2, 1),
    (1, 2, 0),
    (1000, 1_048_576, 1_000_001),
]


@pytest.mark.parametrize("s, slots, expected", NEXT_SLOT_CASES)
def test_next_slot(s, slots, expected):
    next_slot = load("next_slot")
    assert next_slot(s, slots) == expected


ROTATION_SHAPE_CASES = [
    # seed, slots, (tail, rotation)
    (0, 12, (2, 2)),        # 0 -> 1 -> 2 -> 5 -> 2 ...
    (5, 12, (0, 2)),        # seed already inside the rotation
    (4, 12, (1, 2)),
    (3, 12, (2, 2)),
    (1, 12, (1, 2)),
    (11, 12, (1, 2)),
    (0, 3, (2, 1)),         # fixed point: rotation of length one
    (0, 7, (3, 1)),         # another fixed point, longer tail
    (0, 2, (0, 2)),         # the whole slot space rotates, no tail
    (0, 10, (0, 6)),
    # Above CPython's cached-integer range. `is` silently stops matching here.
    (7, 1000, (5, 6)),
    (3, 1000, (5, 6)),
    (0, 1000, (4, 6)),
    (0, 100, (1, 6)),
    (0, 1_048_576, (13, 2)),
    (12_345, 1_048_576, (12, 2)),
]


@pytest.mark.parametrize("seed, slots, expected", ROTATION_SHAPE_CASES)
def test_rotation_shape(seed, slots, expected):
    rotation_shape = load("rotation_shape")
    assert rotation_shape(seed, slots) == expected


# ---------------------------------------------------------------------------
# Exercise 5 — The Relay Hop Budget
# ---------------------------------------------------------------------------

HUGE = 10 ** 18

HOP_LANDING_LOOPING = [
    # call signs, loop_to, budget, expected mast index
    (["R1", "R2", "R3", "R4"], 1, 0, 0),
    (["R1", "R2", "R3", "R4"], 1, 1, 1),
    (["R1", "R2", "R3", "R4"], 1, 2, 2),
    (["R1", "R2", "R3", "R4"], 1, 3, 3),
    (["R1", "R2", "R3", "R4"], 1, 4, 1),
    # Far past anything a per-hop walk could reach. 10**18 - 1 divides by 3.
    (["R1", "R2", "R3", "R4"], 1, HUGE, 1),
    (["R1", "R2", "R3", "R4"], 1, HUGE + 1, 2),
    (["R1", "R2", "R3", "R4"], 1, HUGE + 2, 3),
    (["SOLO"], 0, HUGE, 0),              # fixed point: ring of one
    (["A", "B"], 0, 7, 1),               # no lead-in, ring of two
    (["A", "B"], 0, HUGE, 0),
    # Repeated call signs. Identity is the only thing that means anything.
    (["KX-7", "KX-7"], 0, 5, 1),
    (["KX-7", "KX-7"], 0, HUGE, 0),
    # Long enough that a per-hop walk of the BUDGET never finishes, while a
    # walk of the network is instant.
    ([f"M{i}" for i in range(1000)], 500, HUGE, 500),
]


@pytest.mark.parametrize("signs, loop_to, budget, expected_index", HOP_LANDING_LOOPING)
def test_hop_landing_looping(signs, loop_to, budget, expected_index):
    hop_landing = load("hop_landing")
    first, masts = _wire(Mast, "repeats_to", signs, loop_to)
    assert hop_landing(first, budget) is masts[expected_index]


HOP_LANDING_ENDING = [
    # call signs, budget, expected index or None once the packet is delivered
    (["G1", "G2", "G3"], 0, 0),
    (["G1", "G2", "G3"], 2, 2),
    (["G1", "G2", "G3"], 3, None),
    (["G1", "G2", "G3"], HUGE, None),
    (["G1"], 0, 0),
    (["G1"], 1, None),
    ([f"M{i}" for i in range(1000)], 999, 999),
    ([f"M{i}" for i in range(1000)], 1000, None),
]


@pytest.mark.parametrize("signs, budget, expected_index", HOP_LANDING_ENDING)
def test_hop_landing_terminating(signs, budget, expected_index):
    """A run that reaches the ground station hands the packet on and stops."""
    hop_landing = load("hop_landing")
    first, masts = _wire(Mast, "repeats_to", signs, None)
    landed = hop_landing(first, budget)
    if expected_index is None:
        assert landed is None
    else:
        assert landed is masts[expected_index]


def test_hop_landing_no_network():
    hop_landing = load("hop_landing")
    assert hop_landing(None, 0) is None
    assert hop_landing(None, HUGE) is None


@pytest.mark.parametrize("budget", [-1, -10, -HUGE])
def test_hop_landing_rejects_a_negative_budget(budget):
    hop_landing = load("hop_landing")
    first, _ = _wire(Mast, "repeats_to", ["G1", "G2"], None)
    with pytest.raises(ValueError):
        hop_landing(first, budget)


# ---------------------------------------------------------------------------
# Challenge 1 — Booklet Imposition
# ---------------------------------------------------------------------------

IMPOSE_CASES = [
    ([], []),
    ([7], [7]),
    ([1, 2], [2, 1]),
    ([1, 2, 3], [3, 1, 2]),
    ([1, 2, 3, 4], [4, 1, 3, 2]),
    ([1, 2, 3, 4, 5], [5, 1, 4, 2, 3]),
    ([1, 2, 3, 4, 5, 6], [6, 1, 5, 2, 4, 3]),
    ([1, 2, 3, 4, 5, 6, 7], [7, 1, 6, 2, 5, 3, 4]),
    ([11, 4, 4, 90], [90, 11, 4, 4]),
    ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),
    ([-3, 12, -3], [-3, -3, 12]),
]


@pytest.mark.parametrize("numbers, expected", IMPOSE_CASES)
def test_impose(numbers, expected):
    impose = load("impose")
    assert chain_numbers(impose(build_chain(numbers))) == expected


def test_impose_does_not_rewrite_numbers():
    """Rewiring only. The multiset of page numbers must be unchanged."""
    impose = load("impose")
    numbers = [5, 5, 9, 2, 2, 2, 8]
    head = impose(build_chain(numbers))
    assert sorted(chain_numbers(head)) == sorted(numbers)


def test_impose_is_iterative():
    """4000 pages: a recursive reversal raises RecursionError here.

    The halves are 0..1999 and 2000..3999, equal in length, so nothing is
    appended at the end and the last page fed is the front half's last: 1999.
    """
    impose = load("impose")
    result = chain_numbers(impose(build_chain(list(range(4000)))))
    assert len(result) == 4000
    assert result[0] == 3999
    assert result[1] == 0
    assert result[-1] == 1999


# ---------------------------------------------------------------------------
# Challenge 2 — The Feed-Line Weld
# ---------------------------------------------------------------------------

WELD_CASES = [
    # lead A tags, lead B tags, shared tags, (A's lead-in, B's lead-in)
    (["a1", "a2"], ["b1", "b2", "b3"], ["w1", "w2"], (2, 3)),
    ([], ["b1", "b2"], ["w1"], (0, 2)),
    (["a1"], [], ["w1", "w2", "w3"], (1, 0)),
    ([], [], ["w1", "w2", "w3", "w4"], (0, 0)),       # both start at the weld
    (["a1"], ["b1"], ["w1"], (1, 1)),
    # Every pan carries the same tag. Identity is the only thing that means
    # anything, and a solution comparing tags reports a lead-in of 0.
    (["P", "P", "P"], ["P"], ["P"], (3, 1)),
    (["P"] * 500, ["P"] * 250, ["P"] * 100, (500, 250)),
    ([f"a{i}" for i in range(1000)], [f"b{i}" for i in range(1)], ["w"], (1000, 1)),
]


@pytest.mark.parametrize("lead_a, lead_b, shared, expected", WELD_CASES)
def test_find_weld(lead_a, lead_b, shared, expected):
    find_weld = load("find_weld")
    head_a, head_b, pans_shared = build_lines(lead_a, lead_b, shared)
    result = find_weld(head_a, head_b)
    assert result is not None, "these lines do meet"
    weld, found_a, found_b = result
    assert weld is pans_shared[0], "wrong pan: compare by identity, not by tag"
    assert (found_a, found_b) == expected
    # The plant must come back exactly as it was handed over.
    assert last_pan(head_a) is pans_shared[-1]
    assert last_pan(head_b) is pans_shared[-1]


SEPARATE_LINES = [
    (["a1", "a2"], ["b1", "b2", "b3"]),
    (["a1"], ["b1"]),
    (["P"] * 100, ["P"] * 100),
    ([f"a{i}" for i in range(1000)], [f"b{i}" for i in range(1000)]),
]


@pytest.mark.parametrize("lead_a, lead_b", SEPARATE_LINES)
def test_find_weld_separate_lines(lead_a, lead_b):
    """No weld returns None outright - and still leaves the plant untied."""
    find_weld = load("find_weld")
    head_a, head_b, _ = build_lines(lead_a, lead_b, [])
    assert find_weld(head_a, head_b) is None
    assert last_pan(head_a).tag == lead_a[-1]
    assert last_pan(head_b).tag == lead_b[-1]


def test_find_weld_missing_line():
    find_weld = load("find_weld")
    head_a, head_b, _ = build_lines(["a1"], ["b1"], ["w1"])
    assert find_weld(None, head_b) is None
    assert find_weld(head_a, None) is None
    assert find_weld(None, None) is None
