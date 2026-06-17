"""Exercise 1 - Network Delay Time (LeetCode 743).

Pattern: Heap-Dijkstra; the canonical weighted-graph warm-up from Lecture 1.
Difficulty: Medium.
Target solve time: 25 minutes with full UMPIRE narration.

Problem statement
-----------------
You are given a network of `n` nodes, labeled from 1 to n. You are also
given `times`, a list of travel times as directed edges
`times[i] = (u_i, v_i, w_i)`, where `u_i` is the source node, `v_i` is the
target node, and `w_i` is the time it takes for a signal to travel from
source to target.

We will send a signal from a given node `k`. Return the minimum time it
takes for all the n nodes to receive the signal. If it is impossible for
all the n nodes to receive the signal, return -1.

Constraints (LeetCode):
- 1 <= k <= n <= 100.
- 1 <= len(times) <= 6000.
- times[i].length == 3.
- 1 <= u_i, v_i <= n.
- u_i != v_i.
- 0 <= w_i <= 100.
- All the pairs (u_i, v_i) are unique.

Examples
--------
>>> network_delay_time([[2,1,1],[2,3,1],[3,4,1]], 4, 2)
2
>>> network_delay_time([[1,2,1]], 2, 1)
1
>>> network_delay_time([[1,2,1]], 2, 2)
-1

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. Given a directed weighted graph, return the time for
        a signal from `k` to reach every other node -- i.e., the maximum
        over all shortest distances from `k`. Return -1 if any node is
        unreachable.
- [ ] M: Single-source shortest paths on a non-negative-weight graph.
        That is Dijkstra, heap-based. Why not BFS: weights are non-uniform.
        Why not Bellman-Ford: weights are non-negative; Dijkstra is faster.
- [ ] P: Build adjacency list. Run heap-Dijkstra from `k`. Return
        max(dist.values()) if every node reached, else -1.
- [ ] I: heapq for the priority queue; defaultdict for the distance map;
        the `if d > dist[node]: continue` lazy-delete guard.
- [ ] R: Trace example 1 by hand: heap pops (0,2) -> push (1,1) and (1,3) ->
        pops (1,1) and (1,3) -> push (2,4) -> pops (2,4). Max = 2.
- [ ] E: O((V + E) log V) time; O(V) space for dist; O(E) worst-case heap.
        Trade vs Bellman-Ford: O(V*E) but handles negatives; not needed.

References
----------
- Lecture 1, sections 3 and 8 (worked example):
  ../lecture-notes/01-dijkstra-and-the-shortest-path-picker.md
- LeetCode 743: https://leetcode.com/problems/network-delay-time/
- Python heapq docs: https://docs.python.org/3/library/heapq.html
"""

from __future__ import annotations

import heapq
from collections import defaultdict
from typing import Dict, List, Tuple


def network_delay_time(times: List[List[int]], n: int, k: int) -> int:
    """Return min time for a signal from `k` to reach all `n` nodes, or -1.

    The harness passes `times` as a list of `[u, v, w]` triples. Build the
    adjacency list, run heap-Dijkstra from `k`, then return the max of the
    distance dictionary (or -1 if any node is unreachable).

    Replace the body with your solution. The signature and docstring above
    are part of the spec.
    """
    # TODO: build adjacency list from `times`
    # Hint:
    #   graph: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
    #   for u, v, w in times:
    #       graph[u].append((v, w))
    graph: Dict[int, List[Tuple[int, int]]] = defaultdict(list)

    # TODO: run heap-Dijkstra from `k`
    # Hint:
    #   dist: Dict[int, float] = defaultdict(lambda: float("inf"))
    #   dist[k] = 0
    #   heap = [(0, k)]
    #   while heap:
    #       d, node = heapq.heappop(heap)
    #       if d > dist[node]:
    #           continue
    #       for neighbor, weight in graph.get(node, []):
    #           nd = d + weight
    #           if nd < dist[neighbor]:
    #               dist[neighbor] = nd
    #               heapq.heappush(heap, (nd, neighbor))
    _ = graph, n, k, heapq  # silence unused-variable lint until you wire it up

    # TODO: check reachability and return max distance, or -1
    # Hint:
    #   if len(dist) < n:
    #       return -1
    #   return max(dist.values())
    return -1


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 exercise-01-network-delay-time.py`.
# Also discovered by `pytest`.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a battery of asserts against the network_delay_time function.

    When the function is unimplemented (returns -1 always), most asserts
    will fail loudly -- that is the signal to implement.
    """
    failures = 0
    cases: List[Tuple[str, List[List[int]], int, int, int]] = [
        (
            "LC 743 example 1",
            [[2, 1, 1], [2, 3, 1], [3, 4, 1]],
            4,
            2,
            2,
        ),
        (
            "single edge reachable",
            [[1, 2, 1]],
            2,
            1,
            1,
        ),
        (
            "source isolated",
            [[1, 2, 1]],
            2,
            2,
            -1,
        ),
        (
            "linear chain",
            [[1, 2, 5], [2, 3, 5], [3, 4, 5]],
            4,
            1,
            15,
        ),
        (
            "two-path race won by indirect",
            [[1, 2, 10], [1, 3, 1], [3, 2, 1]],
            3,
            1,
            2,
        ),
        (
            "self-only graph",
            [],
            1,
            1,
            0,
        ),
        (
            "fully connected (small star)",
            [[1, 2, 3], [1, 3, 2], [1, 4, 7]],
            4,
            1,
            7,
        ),
        (
            "unreachable downstream",
            [[1, 2, 1]],
            3,
            1,
            -1,
        ),
    ]
    for label, times, n, k, expected in cases:
        actual = network_delay_time(times, n, k)
        marker = "OK  " if actual == expected else "FAIL"
        if actual != expected:
            failures += 1
            print(
                f"[{marker}] {label}: network_delay_time({times}, {n}, {k}) -> {actual}, expected {expected}"
            )
        else:
            print(f"[{marker}] {label}: network_delay_time -> {actual}")
    if failures:
        raise AssertionError(f"{failures} assertion(s) failed; implement network_delay_time.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
