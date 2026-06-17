"""
Week 6 - pytest grader for the five UMPIRE BFS drills.

Place your solutions in this folder (or any folder on PYTHONPATH) with these
exact function names:

    drill_01_solution.level_order(root)

    drill_02_solution.shortest_path_binary_matrix(grid)

    drill_03_solution.oranges_rotting(grid)

    drill_04_solution.ladder_length(beginWord, endWord, wordList)

    drill_05_solution.right_side_view(root)

For the tree drills (01 and 05), `root` is a TreeNode as defined below.
A helper `build_tree(values)` constructs a tree from a level-order list with
`None` markers for missing children - matching the LeetCode convention.

Then run:

    pytest exercises/timed_runner.py -v

Acceptance criterion for the week: all tests pass on a fresh checkout.

If you implemented with different names, edit the import / call sites below.
The point is the test logic, not the import shape.
"""

from __future__ import annotations

import importlib
import sys
from collections import deque
from pathlib import Path
from typing import Optional

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
# Tree helpers (used by drills 01 and 05)
# -----------------------------------------------------------------------------


class TreeNode:
    """Standard binary-tree node used by the tree-shaped drills."""

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(values):
    """Construct a binary tree from a LeetCode-style level-order list.

    `None` entries mark absent children. Returns the root, or `None` if the
    list is empty.
    """
    if not values:
        return None
    iterator = iter(values)
    root_val = next(iterator)
    if root_val is None:
        return None
    root = TreeNode(root_val)
    queue = deque([root])
    for val in iterator:
        node = queue[0]
        if node is None:
            queue.popleft()
            node = queue[0]
        # try left child
        if not hasattr(node, "_left_set"):
            if val is not None:
                node.left = TreeNode(val)
                queue.append(node.left)
            node._left_set = True
        else:
            if val is not None:
                node.right = TreeNode(val)
                queue.append(node.right)
            queue.popleft()
    return root


# -----------------------------------------------------------------------------
# Drill 1 - Level order traversal
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "values, expected",
    [
        ([3, 9, 20, None, None, 15, 7], [[3], [9, 20], [15, 7]]),
        ([1], [[1]]),
        ([], []),
        ([1, 2, 3, 4, 5, 6, 7], [[1], [2, 3], [4, 5, 6, 7]]),
        ([1, 2, None, 3], [[1], [2], [3]]),
        ([1, None, 2, None, 3], [[1], [2], [3]]),
    ],
)
def test_drill_01_level_order(values, expected):
    mod = _load("drill_01_solution")
    root = build_tree(values)
    assert mod.level_order(root) == expected


# -----------------------------------------------------------------------------
# Drill 2 - Shortest path in a binary matrix (8-directional)
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "grid, expected",
    [
        ([[0, 1], [1, 0]], 2),
        ([[0, 0, 0], [1, 1, 0], [1, 1, 0]], 4),
        ([[1, 0, 0], [1, 1, 0], [1, 1, 0]], -1),
        ([[0, 0, 0], [1, 1, 0], [1, 1, 1]], -1),
        ([[0]], 1),
        ([[1]], -1),
        ([[0, 0], [0, 0]], 2),
        ([[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 0, 1, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0]], 5),
    ],
)
def test_drill_02_shortest_path_binary_matrix(grid, expected):
    mod = _load("drill_02_solution")
    # Copy grid in case the solution mutates it.
    grid_copy = [row[:] for row in grid]
    assert mod.shortest_path_binary_matrix(grid_copy) == expected


# -----------------------------------------------------------------------------
# Drill 3 - Rotting oranges (multi-source grid BFS)
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "grid, expected",
    [
        ([[2, 1, 1], [1, 1, 0], [0, 1, 1]], 4),
        ([[2, 1, 1], [0, 1, 1], [1, 0, 1]], -1),
        ([[0, 2]], 0),
        ([[1]], -1),
        ([[2]], 0),
        ([[0]], 0),
        ([[2, 1, 1], [1, 1, 1], [0, 1, 2]], 2),
        ([[1, 2]], 1),
    ],
)
def test_drill_03_oranges_rotting(grid, expected):
    mod = _load("drill_03_solution")
    grid_copy = [row[:] for row in grid]
    assert mod.oranges_rotting(grid_copy) == expected


# -----------------------------------------------------------------------------
# Drill 4 - Word Ladder (node-BFS on implicit string graph)
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "begin, end, words, expected",
    [
        ("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"], 5),
        ("hit", "cog", ["hot", "dot", "dog", "lot", "log"], 0),
        ("a", "c", ["a", "b", "c"], 2),
        ("hot", "dog", ["hot", "dog"], 0),
        ("hot", "dog", ["hot", "dog", "dot"], 3),
        ("leet", "code", ["lest", "leet", "lose", "code", "lode", "robe", "lost"], 6),
        ("game", "thee", ["frye", "heat", "tree", "thee", "game", "free", "head", "flex", "trek", "fame", "faye"], 0),
    ],
)
def test_drill_04_ladder_length(begin, end, words, expected):
    mod = _load("drill_04_solution")
    assert mod.ladder_length(begin, end, list(words)) == expected


# -----------------------------------------------------------------------------
# Drill 5 - Binary tree right side view
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "values, expected",
    [
        ([1, 2, 3, None, 5, None, 4], [1, 3, 4]),
        ([1, None, 3], [1, 3]),
        ([], []),
        ([1, 2, 3, 4], [1, 3, 4]),
        ([1], [1]),
        ([1, 2, None, 4], [1, 2, 4]),
        ([1, 2, 3, 4, None, None, None, 5], [1, 3, 4, 5]),
    ],
)
def test_drill_05_right_side_view(values, expected):
    mod = _load("drill_05_solution")
    root = build_tree(values)
    assert mod.right_side_view(root) == expected


# -----------------------------------------------------------------------------
# Self-tests for the build_tree helper - these always run so a broken helper is
# caught before it confuses learners debugging their solutions.
# -----------------------------------------------------------------------------


def test_helper_build_tree_empty():
    assert build_tree([]) is None
    assert build_tree([None]) is None


def test_helper_build_tree_single():
    root = build_tree([42])
    assert root is not None
    assert root.val == 42
    assert root.left is None and root.right is None


def test_helper_build_tree_full():
    root = build_tree([1, 2, 3, 4, 5, 6, 7])
    assert root.val == 1
    assert root.left.val == 2 and root.right.val == 3
    assert root.left.left.val == 4 and root.left.right.val == 5
    assert root.right.left.val == 6 and root.right.right.val == 7


def test_helper_build_tree_with_gaps():
    # [1, 2, 3, None, 5, None, 4] - depth 1 node 2 has no left, depth 1 node 3 has no left.
    root = build_tree([1, 2, 3, None, 5, None, 4])
    assert root.val == 1
    assert root.left.val == 2 and root.right.val == 3
    assert root.left.left is None
    assert root.left.right.val == 5
    assert root.right.left is None
    assert root.right.right.val == 4


# -----------------------------------------------------------------------------
# Run with:
#     pytest exercises/timed_runner.py -v
#
# Or, to run only one drill:
#     pytest exercises/timed_runner.py::test_drill_03_oranges_rotting -v
#
# Add `--durations=10` to see which tests take longest - useful when checking
# that your BFS loop hasn't accidentally degenerated into quadratic work
# (the classic bugs: list-as-queue, visited-at-dequeue-time). The runner
# doesn't enforce O(V+E) mechanically - that's on your code review of your
# own solution and your interviewer's eye in Mock #2.
# -----------------------------------------------------------------------------
