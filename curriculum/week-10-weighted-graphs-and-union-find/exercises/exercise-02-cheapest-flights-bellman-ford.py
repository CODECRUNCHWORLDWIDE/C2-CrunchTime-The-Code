"""Exercise 2 - Cheapest Flights Within K Stops (LeetCode 787).

Pattern: Bellman-Ford bounded by K + 1 passes; the snapshot idiom from
Lecture 2 section 2.
Difficulty: Medium.
Target solve time: 35 minutes with full UMPIRE narration.

Problem statement
-----------------
There are `n` cities connected by some number of flights. You are given
an array `flights` where `flights[i] = [from_i, to_i, price_i]` indicates
that there is a flight from city `from_i` to city `to_i` with cost
`price_i`.

You are also given three integers `src`, `dst`, and `k`. Return the
cheapest price from `src` to `dst` with at most `k` stops. If there is
no such route, return -1.

Constraints (LeetCode):
- 1 <= n <= 100.
- 0 <= flights.length <= (n * (n - 1) / 2).
- flights[i].length == 3.
- 0 <= from_i, to_i < n.
- from_i != to_i.
- 1 <= price_i <= 10^4.
- There will not be any multiple flights between two cities.
- 0 <= src, dst, k < n.
- src != dst.

Examples
--------
>>> find_cheapest_price(4, [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], 0, 3, 1)
700
>>> find_cheapest_price(3, [[0,1,100],[1,2,100],[0,2,500]], 0, 2, 1)
200
>>> find_cheapest_price(3, [[0,1,100],[1,2,100],[0,2,500]], 0, 2, 0)
500

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. Cheapest path from src to dst using at most K
        intermediate stops -- i.e., at most K + 1 edges. Return -1 if no
        valid path exists.
- [ ] M: Single-source shortest path with a hop-count constraint. The
        clean pattern is Bellman-Ford bounded by K + 1 outer passes.
        Why not vanilla Dijkstra: the heap settles a node at its
        overall-cheapest distance, ignoring the hop budget. Why not
        unconstrained Bellman-Ford: V - 1 passes overshoot the K + 1
        bound and would accept paths longer than allowed.
- [ ] P: Initialize dist = [inf] * n; dist[src] = 0. Loop K + 1 times:
        snapshot prev = dist[:]; for each edge (u, v, w), if
        prev[u] + w < dist[v], update dist[v]. Return dist[dst] or -1.
- [ ] I: The snapshot is non-negotiable -- without it, a single pass
        can chain multiple just-updated values within itself and exceed
        the hop budget. Pure-Python list copy is O(n); cheap relative to
        the edge loop.
- [ ] R: Trace example 1 (K = 1). Pass 0: snapshot all inf except 0.
        Relax 0->1 to 100, 1->2 to inf (prev[1] still inf). Pass 1:
        snapshot. Relax 1->2 to 200, 0->1 still 100, 2->3 to inf
        (prev[2] still inf in this pass's snapshot if pass 0 produced
        200 ... wait, walk it again on paper). The correct trace shows
        why the snapshot matters.
- [ ] E: O(K * E) time; O(V) space. Trade vs modified Dijkstra with
        state (node, hops): also correct, faster on graphs where target
        is reachable in few hops, harder to write right under pressure.

References
----------
- Lecture 2, section 2 (Bellman-Ford with a hop-count constraint):
  ../lecture-notes/02-bellman-ford-floyd-warshall-and-mst.md
- LeetCode 787: https://leetcode.com/problems/cheapest-flights-within-k-stops/
- Wikipedia Bellman-Ford: https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm
"""

from __future__ import annotations

from typing import List


def find_cheapest_price(
    n: int, flights: List[List[int]], src: int, dst: int, k: int
) -> int:
    """Cheapest fare from `src` to `dst` using at most `k` intermediate stops.

    The algorithm is Bellman-Ford bounded by K + 1 outer passes. Each pass
    must snapshot the previous-pass distances before relaxing -- otherwise
    a single pass can chain multiple just-updated values within itself
    and exceed the K + 1 edge budget.

    Replace the body with your solution. The signature and docstring above
    are part of the spec.
    """
    # TODO: initialize dist array
    # Hint:
    #   dist: List[float] = [float("inf")] * n
    #   dist[src] = 0.0
    dist: List[float] = [float("inf")] * n
    dist[src] = 0.0

    # TODO: run K + 1 outer passes
    # Hint:
    #   for _ in range(k + 1):
    #       prev = dist[:]
    #       for u, v, w in flights:
    #           if prev[u] + w < dist[v]:
    #               dist[v] = prev[u] + w
    _ = flights, k  # silence unused-variable lint until you wire it up

    # TODO: return dist[dst] as int, or -1 if unreachable
    # Hint:
    #   return int(dist[dst]) if dist[dst] != float("inf") else -1
    return -1


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 exercise-02-cheapest-flights-bellman-ford.py`.
# Also discovered by `pytest`.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a battery of asserts against find_cheapest_price.

    When the function is unimplemented (returns -1), several asserts will
    fail loudly -- that is the signal to implement.
    """
    failures = 0
    cases: List = [
        (
            "LC 787 example 1 (K=1; cheapest via stop)",
            4,
            [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]],
            0,
            3,
            1,
            700,
        ),
        (
            "LC 787 example 2 (K=1; direct vs 1-stop)",
            3,
            [[0, 1, 100], [1, 2, 100], [0, 2, 500]],
            0,
            2,
            1,
            200,
        ),
        (
            "LC 787 example 3 (K=0; only direct)",
            3,
            [[0, 1, 100], [1, 2, 100], [0, 2, 500]],
            0,
            2,
            0,
            500,
        ),
        (
            "no path",
            3,
            [[0, 1, 100]],
            0,
            2,
            5,
            -1,
        ),
        (
            "K too small to reach",
            4,
            [[0, 1, 1], [1, 2, 1], [2, 3, 1]],
            0,
            3,
            1,
            -1,
        ),
        (
            "K exactly sufficient",
            4,
            [[0, 1, 1], [1, 2, 1], [2, 3, 1]],
            0,
            3,
            2,
            3,
        ),
        (
            "direct flight with K=0",
            2,
            [[0, 1, 50]],
            0,
            1,
            0,
            50,
        ),
        (
            "diamond graph",
            4,
            [[0, 1, 1], [0, 2, 10], [1, 3, 10], [2, 3, 1]],
            0,
            3,
            1,
            11,
        ),
    ]
    for case in cases:
        label, n, flights, src, dst, k, expected = case
        actual = find_cheapest_price(n, flights, src, dst, k)
        marker = "OK  " if actual == expected else "FAIL"
        if actual != expected:
            failures += 1
            print(
                f"[{marker}] {label}: find_cheapest_price({n}, {flights}, {src}, {dst}, {k}) -> {actual}, expected {expected}"
            )
        else:
            print(f"[{marker}] {label}: find_cheapest_price -> {actual}")
    if failures:
        raise AssertionError(
            f"{failures} assertion(s) failed; implement find_cheapest_price."
        )
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
