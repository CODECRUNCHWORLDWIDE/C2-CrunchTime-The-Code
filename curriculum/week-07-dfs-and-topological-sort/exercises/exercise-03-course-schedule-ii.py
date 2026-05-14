"""Exercise 3 - Course Schedule II (LeetCode 210).

Pattern: Topological sort -- Kahn's algorithm (BFS-shaped) or DFS post-order.
Difficulty: Medium.
Target solve time: 30 minutes with full UMPIRE narration.

Problem statement
-----------------
There are a total of `num_courses` courses you have to take, labeled from
`0` to `num_courses - 1`. You are given an array `prerequisites` where
`prerequisites[i] = [a_i, b_i]` indicates that you *must* take course `b_i`
first if you want to take course `a_i`.

Return the ordering of courses you should take to finish all courses. If
there are many valid answers, return *any* of them. If it is impossible to
finish all courses (i.e., the prerequisite graph has a cycle), return an
empty array.

Constraints (LeetCode):
- 1 <= num_courses <= 2000
- 0 <= prerequisites.length <= num_courses * (num_courses - 1)
- prerequisites[i].length == 2
- 0 <= a_i, b_i < num_courses
- a_i != b_i
- All pairs `[a_i, b_i]` are distinct.

The graph model
---------------
`[a, b]` means "b is a prerequisite of a" -> directed edge `b -> a`. The
in-degree of `a` is the number of prerequisites of `a`.

Examples
--------
>>> find_order(2, [[1, 0]])
[0, 1]
>>> find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) in ([0, 1, 2, 3], [0, 2, 1, 3])
True
>>> find_order(1, [])
[0]
>>> find_order(2, [[0, 1], [1, 0]])
[]

UMPIRE checklist
----------------
- [ ] U: Restate. `[a, b]` means "b before a". Confirm cycle -> return [].
        Confirm "any valid order" is acceptable (we do not need a specific
        ordering).
- [ ] M: Topological sort on a directed graph. Two algorithms:
        - Kahn's (BFS-shaped): in-degree array; queue of zero-in-degree
          nodes; iterative.
        - DFS post-order with three-color invariant: recursive; reverse
          post-order.
        Choose Kahn (default at Phase 2): iterative, no recursion-limit
        risk; n is small here (<= 2000) so either works.
- [ ] P: Four bullets.
        1. Build adjacency list and in-degree array.
        2. Seed queue with every node of in-degree zero.
        3. Loop: pop, append, decrement neighbor in-degrees, queue any that
           drop to zero.
        4. If len(output) < num_courses -> cycle -> return [].
- [ ] I: Write Kahn's algorithm. Use `collections.deque`.
- [ ] R: Trace on the four examples above. Edge: cycle on a single edge ->
        []. Edge: num_courses == 1, no prerequisites -> [0].
- [ ] E: O(V + E) time and space. State the defense sentence: Kahn is
        iterative, no recursion-limit risk, cycle detection by exhaustion
        (len(output) != V).

References
----------
- Lecture 3, sections 4 and 6: ../lecture-notes/03-topological-sort.md
- LeetCode 210: https://leetcode.com/problems/course-schedule-ii/
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Dict, List


def find_order(num_courses: int, prerequisites: List[List[int]]) -> List[int]:
    """Return any valid topological order of the courses, or [] on cycle.

    Replace the body with your Kahn's-algorithm solution.
    """
    # TODO: implement Kahn's algorithm.
    # 1. Build adjacency list `adj: Dict[int, List[int]]` and `in_degree`.
    #    Hint: for [a, b] in prerequisites, adj[b].append(a); in_degree[a]+=1
    # 2. Initialize a deque containing every course whose in_degree is zero.
    # 3. While the deque is non-empty: pop, append to `order`, decrement
    #    in_degrees of out-neighbors; queue any that drop to zero.
    # 4. If len(order) == num_courses, return order; else return [].
    _ = (num_courses, prerequisites)
    return []


def _build_graph(num_courses: int, prerequisites: List[List[int]]) -> tuple[Dict[int, List[int]], List[int]]:
    """Helper: build the adjacency list and in-degree array.

    Returned as a (adj, in_degree) pair. Adjacency keys cover all courses
    0..num_courses-1 (isolated nodes have empty lists).
    """
    adj: Dict[int, List[int]] = defaultdict(list)
    in_degree: List[int] = [0] * num_courses
    for a, b in prerequisites:
        adj[b].append(a)
        in_degree[a] += 1
    for c in range(num_courses):
        if c not in adj:
            adj[c] = []
    return adj, in_degree


def _is_valid_topological_order(num_courses: int, prerequisites: List[List[int]], order: List[int]) -> bool:
    """Verify that `order` is a valid topological order for the given graph.

    A correct answer to this problem is "any valid order"; the verifier checks
    the validity rather than insisting on a specific permutation.
    """
    if len(order) != num_courses:
        return False
    position: Dict[int, int] = {c: i for i, c in enumerate(order)}
    if len(position) != num_courses:
        return False  # duplicates or missing courses
    for a, b in prerequisites:
        if position[b] > position[a]:
            return False  # prerequisite comes after the dependent
    return True


# ---------------------------------------------------------------------------
# Self-test block.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a small battery of asserts against the public function."""
    # Each case: (num_courses, prerequisites, expected_emptiness)
    # We verify validity, not a specific permutation.
    cases: list[tuple[int, list[list[int]], bool]] = [
        (2, [[1, 0]], False),
        (4, [[1, 0], [2, 0], [3, 1], [3, 2]], False),
        (1, [], False),
        (2, [[0, 1], [1, 0]], True),
        (3, [[0, 1], [1, 2], [2, 0]], True),  # 3-cycle
        (6, [[1, 0], [2, 0], [3, 1], [4, 2], [5, 3], [5, 4]], False),
        # Disconnected DAG: two separate chains.
        (5, [[1, 0], [3, 2]], False),
        # Empty prerequisites with multiple courses: many valid orders.
        (5, [], False),
    ]
    failures = 0
    for i, (n, prereqs, expected_empty) in enumerate(cases, start=1):
        order = find_order(n, prereqs)
        if expected_empty:
            ok = order == []
            detail = f"expected [], got {order}"
        else:
            ok = _is_valid_topological_order(n, prereqs, order)
            detail = f"got {order}; not a valid topological order"
        marker = "OK " if ok else "FAIL"
        if not ok:
            failures += 1
            print(f"[{marker}] case {i}: {detail}")
        else:
            print(f"[{marker}] case {i}: {order}")
    # Smoke-test the helpers.
    adj, in_deg = _build_graph(3, [[1, 0], [2, 1]])
    assert adj[0] == [1] and adj[1] == [2] and adj[2] == [], "Helper _build_graph wrong adj"
    assert in_deg == [0, 1, 1], "Helper _build_graph wrong in_degree"
    assert _is_valid_topological_order(3, [[1, 0], [2, 1]], [0, 1, 2]) is True
    assert _is_valid_topological_order(3, [[1, 0], [2, 1]], [2, 1, 0]) is False
    if failures:
        raise AssertionError(f"{failures} case(s) failed; implement find_order.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
