"""Mini-Project Problem 1 starter - Dijkstra (Network Delay Time, LC 743).

This is the starter for the mini-project's first write-up. Copy this file
into your portfolio repository and fill in the function body. The write-up
itself lives in `umpire-writeups/c2-week-10/mini-project/`.

Pattern: Heap-Dijkstra; the canonical single-source shortest-paths
algorithm from Lecture 1.
Target solve time: 30 minutes including the full UMPIRE write-up.

Spec
----
You are given a network of `n` nodes labeled 1..n and a list of travel
times as directed edges `times[i] = (u_i, v_i, w_i)`. Send a signal from
node `k` and return the minimum time for all nodes to receive it, or -1
if any node is unreachable.

Constraints (LeetCode):
- 1 <= k <= n <= 100.
- 1 <= len(times) <= 6000.
- 0 <= w_i <= 100.
- All edges are non-negative.

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate the input format, the output, and the reachability
        check that produces -1.
- [ ] M: Heap-Dijkstra. Non-negative weights + single source -> Dijkstra.
        Reject BFS (weights non-uniform). Reject Bellman-Ford (slower
        when weights are non-negative).
- [ ] P: Build adjacency list. Initialize dist as defaultdict(inf) with
        dist[k] = 0. Heap of (d, node). Lazy-delete guard. Relax
        outgoing edges; push improvements.
- [ ] I: heapq for the priority queue; defaultdict for dist; the lazy-
        delete guard `if d > dist[node]: continue`.
- [ ] R: Trace LC 743 example 1. Trace the unreachable case.
- [ ] E: O((V + E) log V) time; O(V) space. Trade vs Bellman-Ford
        (handles negatives, O(V*E)). Trade vs Floyd-Warshall (all-pairs,
        O(V^3) -- overkill for single-source).

References
----------
- Lecture 1, sections 3 and 8:
  ../lecture-notes/01-dijkstra-and-the-shortest-path-picker.md
- Exercise 1 (warm-up): ../exercises/exercise-01-network-delay-time.py
- LeetCode 743: https://leetcode.com/problems/network-delay-time/
"""

from __future__ import annotations

import heapq
from collections import defaultdict
from typing import Dict, List, Tuple


def network_delay_time(times: List[List[int]], n: int, k: int) -> int:
    """Min time for a signal from `k` to reach all `n` nodes, or -1.

    Pattern: heap-Dijkstra. The relaxation loop pops the smallest-distance
    entry from the heap; the lazy-delete guard skips stale entries; each
    edge is relaxed at most once.

    Fill in the body. The signature, docstring, and helper imports are
    part of the spec.
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
    #   heap: List[Tuple[float, int]] = [(0.0, k)]
    #   while heap:
    #       d, node = heapq.heappop(heap)
    #       if d > dist[node]:
    #           continue
    #       for neighbor, weight in graph.get(node, []):
    #           new_dist = d + weight
    #           if new_dist < dist[neighbor]:
    #               dist[neighbor] = new_dist
    #               heapq.heappush(heap, (new_dist, neighbor))
    _ = graph, n, k, heapq  # silence unused-variable lint until you wire it up

    # TODO: return max distance or -1 if not all nodes reached
    # Hint:
    #   if len(dist) < n:
    #       return -1
    #   return int(max(dist.values()))
    return -1


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 problem-01-dijkstra-starter.py`.
# Also discovered by `pytest`.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a battery of asserts; many will fail until you implement."""
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
            "isolated source",
            [[1, 2, 1]],
            2,
            2,
            -1,
        ),
        (
            "two-path race",
            [[1, 2, 10], [1, 3, 1], [3, 2, 1]],
            3,
            1,
            2,
        ),
        (
            "trivial single node",
            [],
            1,
            1,
            0,
        ),
        (
            "linear chain length 5",
            [[1, 2, 1], [2, 3, 2], [3, 4, 3], [4, 5, 4]],
            5,
            1,
            10,
        ),
    ]
    for label, times, n, k, expected in cases:
        actual = network_delay_time(times, n, k)
        marker = "OK  " if actual == expected else "FAIL"
        if actual != expected:
            failures += 1
            print(f"[{marker}] {label}: -> {actual}, expected {expected}")
        else:
            print(f"[{marker}] {label}: -> {actual}")
    if failures:
        raise AssertionError(f"{failures} assertion(s) failed; implement network_delay_time.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
