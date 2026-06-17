"""
Week 4 - pytest grader for the four UMPIRE fast/slow-pointer drills.

Place your solutions in this folder (or any folder on PYTHONPATH) with these
exact function and class names:

    drill_01_solution.ListNode
    drill_01_solution.has_cycle(head)

    drill_02_solution.ListNode
    drill_02_solution.detect_cycle(head)

    drill_03_solution.ListNode
    drill_03_solution.middle_node(head)

    drill_04_solution.digit_square_sum(n)
    drill_04_solution.is_happy(n)

Then run:

    pytest exercises/timed_runner.py -v

Acceptance criterion for the week: all tests pass on a fresh checkout.

If you implemented with different names, edit the import / call sites below.
The point is the test logic, not the import shape.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

# Make this folder importable so drill_NN_solution.py modules are found.
sys.path.insert(0, str(Path(__file__).parent))


def _load(module_name: str):
    """Import a drill module lazily so missing solutions skip rather than fail collection."""
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        pytest.skip(f"{module_name} not found - write your solution first.")


# -----------------------------------------------------------------------------
# Helpers for building linked lists with optional cycles
# -----------------------------------------------------------------------------


def _build_list(node_cls, values):
    """Build a singly-linked list of node_cls from a list of values.

    Returns (head, nodes) where nodes is the index-aligned list of node objects
    so tests can refer to specific nodes by their position.
    """
    if not values:
        return None, []
    nodes = [node_cls(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    return nodes[0], nodes


def _build_list_with_cycle(node_cls, values, pos):
    """Build a linked list and connect the tail's .next to nodes[pos]. pos = -1 means no cycle."""
    head, nodes = _build_list(node_cls, values)
    if pos != -1 and nodes:
        nodes[-1].next = nodes[pos]
    return head, nodes


def _list_to_values(head, max_len=10_000):
    """Walk a NON-CYCLIC linked list and return its values. Safety: hard-stop at max_len."""
    out = []
    node = head
    count = 0
    while node is not None and count < max_len:
        out.append(node.val)
        node = node.next
        count += 1
    return out


# ----- Drill 1 - Linked list cycle detection ---------------------------------


@pytest.mark.parametrize(
    "values, pos, expected",
    [
        ([3, 2, 0, -4], 1, True),       # cycle starting at index 1
        ([1, 2], 0, True),               # cycle starting at index 0 (head)
        ([1], -1, False),                # single node, no cycle
        ([], -1, False),                 # empty list
        ([1, 2, 3, 4, 5], -1, False),    # standard terminating list
        ([1, 2, 3, 4, 5], 4, True),      # tail points to itself
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0, True),
        ([42], 0, True),                 # single node self-loop
    ],
)
def test_drill_01_has_cycle(values, pos, expected):
    mod = _load("drill_01_solution")
    head, _ = _build_list_with_cycle(mod.ListNode, values, pos)
    assert mod.has_cycle(head) is expected


# ----- Drill 2 - Cycle entrance ---------------------------------------------


@pytest.mark.parametrize(
    "values, pos",
    [
        ([3, 2, 0, -4], 1),
        ([1, 2], 0),
        ([1], -1),
        ([], -1),
        ([1, 2, 3, 4, 5], -1),
        ([1, 2, 3, 4, 5], 4),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5),
        ([42], 0),
    ],
)
def test_drill_02_detect_cycle(values, pos):
    mod = _load("drill_02_solution")
    head, nodes = _build_list_with_cycle(mod.ListNode, values, pos)
    got = mod.detect_cycle(head)
    if pos == -1:
        assert got is None, f"expected None for no-cycle case, got node with val {getattr(got, 'val', None)}"
    else:
        assert got is nodes[pos], (
            f"expected entrance node at index {pos} (val={nodes[pos].val}), "
            f"got node with val {getattr(got, 'val', None)}"
        )


# ----- Drill 3 - Middle of linked list --------------------------------------


@pytest.mark.parametrize(
    "values, expected_val",
    [
        ([1, 2, 3, 4, 5], 3),            # odd: single middle
        ([1, 2, 3, 4, 5, 6], 4),         # even: upper middle
        ([1], 1),                        # single node
        ([1, 2], 2),                     # two nodes, upper middle is second
        ([1, 2, 3], 2),                  # three nodes, middle is second
        ([1, 2, 3, 4], 3),               # four nodes, upper middle is third
        ([10, 20, 30, 40, 50, 60, 70], 40),
        ([10, 20, 30, 40, 50, 60, 70, 80], 50),
    ],
)
def test_drill_03_middle_node(values, expected_val):
    mod = _load("drill_03_solution")
    head, _ = _build_list(mod.ListNode, values)
    mid = mod.middle_node(head)
    assert mid is not None, "middle_node returned None on a non-empty list"
    assert mid.val == expected_val, f"got middle val {mid.val}, expected {expected_val}"


def test_drill_03_middle_node_empty():
    mod = _load("drill_03_solution")
    assert mod.middle_node(None) is None


# ----- Drill 4 - Happy number ------------------------------------------------


@pytest.mark.parametrize(
    "n, expected",
    [
        (1, 1),
        (2, 4),
        (7, 49),
        (10, 1),
        (19, 1 + 81),       # 1^2 + 9^2 = 82
        (100, 1),
        (123, 14),          # 1 + 4 + 9 = 14
        (999, 243),         # 81 * 3
    ],
)
def test_drill_04_digit_square_sum(n, expected):
    mod = _load("drill_04_solution")
    assert mod.digit_square_sum(n) == expected


@pytest.mark.parametrize(
    "n, expected",
    [
        (1, True),
        (7, True),
        (10, True),
        (13, True),
        (19, True),
        (23, True),
        (2, False),
        (3, False),
        (4, False),
        (11, False),
        (20, False),
        (1234567, False),
    ],
)
def test_drill_04_is_happy(n, expected):
    mod = _load("drill_04_solution")
    assert mod.is_happy(n) is expected


# -----------------------------------------------------------------------------
# Run with:
#     pytest exercises/timed_runner.py -v
#
# Or, to run only one drill:
#     pytest exercises/timed_runner.py::test_drill_02_detect_cycle -v
#
# Add `--durations=10` to see which tests take longest - useful when checking
# you haven't accidentally written an O(n) extra-space solution (with a set)
# where O(1) is required by the spec. The runner doesn't enforce the space
# bound mechanically - that's on your code review of your own solution and
# your interviewer's eye in Mock #1.
# -----------------------------------------------------------------------------
