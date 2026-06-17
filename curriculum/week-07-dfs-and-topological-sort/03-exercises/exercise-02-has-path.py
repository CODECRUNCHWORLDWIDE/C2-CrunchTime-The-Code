"""Exercise 2 - Has Path (LeetCode 1971: Find If Path Exists in Graph).

Pattern: Iterative DFS with explicit stack; path existence.
Difficulty: Medium.
Target solve time: 25 minutes with full UMPIRE narration.

Problem statement
-----------------
There is a bi-directional graph with `n` vertices, where each vertex is
labeled from `0` to `n - 1` (inclusive). The edges in the graph are
represented as a 2-D integer array `edges`, where each `edges[i] = [u_i, v_i]`
denotes a bi-directional edge between vertex `u_i` and vertex `v_i`.

Every vertex pair is connected by at most one edge, and no vertex has an edge
to itself.

You want to determine if there is a valid path that exists from vertex
`source` to vertex `destination`.

Given `edges` and the integers `n`, `source`, and `destination`, return
`True` if there is a valid path from `source` to `destination`, or `False`
otherwise.

Constraints (LeetCode):
- 1 <= n <= 2 * 10^5
- 0 <= edges.length <= 2 * 10^5
- edges[i].length == 2
- 0 <= u_i, v_i <= n - 1
- u_i != v_i

Why iterative
-------------
With `n` up to 2 * 10^5, the recursion depth could exceed Python's default
limit of 1000 for adversarial chain-shaped inputs. The iterative form with an
explicit stack is the production-grade answer; it is also what the rubric
this week is grading.

Examples
--------
>>> valid_path(3, [[0, 1], [1, 2], [2, 0]], 0, 2)
True
>>> valid_path(6, [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]], 0, 5)
False

UMPIRE checklist
----------------
- [ ] U: Restate. Bi-directional means undirected. Confirm self-loops are
        forbidden and there are no duplicate edges. Confirm n can be up to
        2 * 10^5 -> recursion-limit risk -> iterative DFS.
- [ ] M: Path existence on an undirected graph -> iterative DFS with explicit
        stack. Sub-shape: build adjacency list from edge list. Visited is a
        set of node integers. Why iterative: n is large; recursive DFS would
        risk RecursionError on a chain-shaped input. Why not BFS: same
        asymptotic; DFS is shorter to write and equally correct for path
        existence. Why not union-find: works equally well; DFS shows the
        iterative-stack technique the week is grading.
- [ ] P: Build adjacency list. Initialize stack = [source], visited = set().
        Loop: pop node; if node == destination, return True; if node in
        visited, continue; add to visited; push unvisited neighbors. After
        loop, return False.
- [ ] I: Iterative DFS body with the pop-time visited check.
- [ ] R: Trace on both examples. Edge case: source == destination -> True
        immediately. Edge case: disconnected graph (example 2) -> False.
- [ ] E: O(V + E) time and space. State the iterative defense sentence:
        recursion-limit risk avoided; same asymptotic as recursive DFS;
        constant factor on space slightly smaller.

References
----------
- Lecture 2 (iterative DFS): ../lecture-notes/02-iterative-dfs.md
- LeetCode 1971: https://leetcode.com/problems/find-if-path-exists-in-graph/
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List


def valid_path(n: int, edges: List[List[int]], source: int, destination: int) -> bool:
    """Return True if there is a path from `source` to `destination`.

    Replace the body with your iterative DFS solution.
    """
    # TODO: implement iterative DFS with an explicit stack.
    # 1. Build the adjacency list. Hint:
    #        adj: Dict[int, List[int]] = defaultdict(list)
    #        for u, v in edges:
    #            adj[u].append(v); adj[v].append(u)
    # 2. Handle the trivial case: source == destination -> return True.
    # 3. Initialize stack = [source]; visited: set[int] = set().
    # 4. Loop: pop node; pop-time visited check; mark visited; if node ==
    #    destination return True; push unvisited neighbors.
    # 5. After loop, return False.
    _ = (n, edges, source, destination)
    return False


def _build_adjacency(n: int, edges: List[List[int]]) -> Dict[int, List[int]]:
    """Helper: build an undirected adjacency list from an edge list.

    Exposed at module scope so the solution body can call it cleanly.
    Not strictly required; you may inline the build if you prefer.
    """
    adj: Dict[int, List[int]] = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    # Ensure isolated nodes appear as keys (for clean iteration in tests).
    for i in range(n):
        if i not in adj:
            adj[i] = []
    return adj


# ---------------------------------------------------------------------------
# Self-test block.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a small battery of asserts against the public function."""
    cases: list[tuple[int, list[list[int]], int, int, bool]] = [
        # Standard connected triangle.
        (3, [[0, 1], [1, 2], [2, 0]], 0, 2, True),
        # Two components; source and destination in different components.
        (6, [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]], 0, 5, False),
        # source == destination, trivial path.
        (1, [], 0, 0, True),
        (5, [[0, 1], [1, 2], [2, 3], [3, 4]], 0, 4, True),
        (5, [[0, 1], [1, 2], [2, 3], [3, 4]], 0, 0, True),
        # No edges, source != destination.
        (5, [], 0, 4, False),
        # Star graph: 0 connected to 1, 2, 3, 4.
        (5, [[0, 1], [0, 2], [0, 3], [0, 4]], 2, 4, True),
        # Long chain that exceeds the default recursion limit if you used
        # recursive DFS: 2000 nodes in a single path.
        (
            2000,
            [[i, i + 1] for i in range(1999)],
            0,
            1999,
            True,
        ),
    ]
    failures = 0
    for i, (n, edges, source, destination, expected) in enumerate(cases, start=1):
        actual = valid_path(n, edges, source, destination)
        marker = "OK " if actual == expected else "FAIL"
        if actual != expected:
            failures += 1
            print(f"[{marker}] case {i}: expected {expected}, got {actual}")
        else:
            print(f"[{marker}] case {i}: {actual}")
    # Smoke-test the adjacency-list helper.
    adj = _build_adjacency(3, [[0, 1], [1, 2]])
    assert sorted(adj[1]) == [0, 2], "Helper _build_adjacency is wrong."
    if failures:
        raise AssertionError(f"{failures} case(s) failed; implement valid_path.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
