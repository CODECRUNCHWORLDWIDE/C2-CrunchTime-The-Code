"""Exercise 3 - Number of Provinces (LeetCode 547).

Pattern: Union-Find with path compression and union by rank; the
canonical DSU warm-up from Lecture 3.
Difficulty: Medium.
Target solve time: 20 minutes with full UMPIRE narration.

Problem statement
-----------------
There are `n` cities. Some of them are connected, while some are not. If
city `a` is connected directly with city `b`, and city `b` is connected
directly with city `c`, then city `a` is connected indirectly with city
`c`.

A province is a group of directly or indirectly connected cities and no
other cities outside of the group.

You are given an `n x n` matrix `isConnected` where
`isConnected[i][j] = 1` if the i-th city and the j-th city are directly
connected, and `isConnected[i][j] = 0` otherwise.

Return the total number of provinces.

Constraints (LeetCode):
- 1 <= n <= 200.
- n == len(isConnected).
- n == len(isConnected[i]).
- isConnected[i][j] is 1 or 0.
- isConnected[i][i] == 1.
- isConnected[i][j] == isConnected[j][i].

Examples
--------
>>> find_circle_num([[1,1,0],[1,1,0],[0,0,1]])
2
>>> find_circle_num([[1,0,0],[0,1,0],[0,0,1]])
3
>>> find_circle_num([[1,1,1],[1,1,1],[1,1,1]])
1

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. Count connected components of an undirected graph
        given as an adjacency matrix. Each city is a vertex; a 1 in
        the matrix is an edge.
- [ ] M: Components-count, Sub-shape 1 from Lecture 3. DSU is the
        canonical reach. Why not BFS/DFS: also correct, comparable
        complexity, but the DSU is shorter for the "iterate matrix
        upper triangle and union" formulation and is the right rep for
        the rest of the week.
- [ ] P: Build a UnionFind(n). Iterate i < j over the upper triangle;
        when isConnected[i][j] == 1, union(i, j). Return uf.components.
- [ ] I: Class form for UnionFind (parent, rank, components). Path
        compression in find; union by rank in union; return True on
        merge so we can also count components by decrementing.
- [ ] R: Trace example 1 (a 3x3 matrix with cities 0 and 1 connected,
        2 isolated). Initial components = 3. Union(0, 1) decrements to
        2. Iteration finishes. Return 2.
- [ ] E: O(n^2 alpha(n)) time (matrix walk dominates); O(n) space for
        parent and rank arrays. Trade vs BFS/DFS: BFS is O(n^2) which
        ties; DSU is preferable if the unions arrive streaming (this
        problem they do not, but the rep generalizes).

References
----------
- Lecture 3, sections 3 and 4 (canonical DSU and sub-shape 1):
  ../lecture-notes/03-union-find-and-the-dsu-triggers.md
- LeetCode 547: https://leetcode.com/problems/number-of-provinces/
- Wikipedia Disjoint-Set: https://en.wikipedia.org/wiki/Disjoint-set_data_structure
"""

from __future__ import annotations

from typing import List


class UnionFind:
    """DSU with path compression and union by rank.

    See Lecture 3 section 3 for the full derivation. This is the
    minimal-but-correct class you should be able to write from memory in
    under five minutes.
    """

    def __init__(self, n: int) -> None:
        """Initialize a DSU with `n` singletons."""
        # TODO: initialize parent and rank arrays; components counter
        # Hint:
        #   self.parent: List[int] = list(range(n))
        #   self.rank: List[int] = [0] * n
        #   self.components: int = n
        self.parent: List[int] = list(range(n))
        self.rank: List[int] = [0] * n
        self.components: int = n

    def find(self, x: int) -> int:
        """Return the root of `x`'s set; compress the path on the way back."""
        # TODO: recursive path compression
        # Hint:
        #   if self.parent[x] != x:
        #       self.parent[x] = self.find(self.parent[x])
        #   return self.parent[x]
        return x

    def union(self, x: int, y: int) -> bool:
        """Merge `x`'s set with `y`'s. Return True iff a merge happened."""
        # TODO: union by rank; decrement components on a successful merge
        # Hint:
        #   rx, ry = self.find(x), self.find(y)
        #   if rx == ry: return False
        #   if self.rank[rx] < self.rank[ry]: rx, ry = ry, rx
        #   self.parent[ry] = rx
        #   if self.rank[rx] == self.rank[ry]: self.rank[rx] += 1
        #   self.components -= 1
        #   return True
        _ = x, y  # silence unused-variable lint until you wire it up
        return False


def find_circle_num(is_connected: List[List[int]]) -> int:
    """Return the number of provinces in the undirected graph `is_connected`.

    The matrix is symmetric with 1s on the diagonal. Iterate the upper
    triangle and union for each off-diagonal 1. Return uf.components.

    Replace the body with your solution. The signature and docstring above
    are part of the spec.
    """
    # TODO: build UnionFind; walk the upper triangle; return components count
    # Hint:
    #   n = len(is_connected)
    #   uf = UnionFind(n)
    #   for i in range(n):
    #       for j in range(i + 1, n):
    #           if is_connected[i][j] == 1:
    #               uf.union(i, j)
    #   return uf.components
    _ = is_connected  # silence unused-variable lint until you wire it up
    return 0


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 exercise-03-number-of-provinces.py`.
# Also discovered by `pytest`.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a battery of asserts against find_circle_num.

    When the function is unimplemented (returns 0), several asserts will
    fail loudly -- that is the signal to implement.
    """
    failures = 0
    cases: List = [
        (
            "LC 547 example 1",
            [[1, 1, 0], [1, 1, 0], [0, 0, 1]],
            2,
        ),
        (
            "LC 547 example 2",
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            3,
        ),
        (
            "all-connected",
            [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
            1,
        ),
        (
            "two pairs",
            [
                [1, 1, 0, 0],
                [1, 1, 0, 0],
                [0, 0, 1, 1],
                [0, 0, 1, 1],
            ],
            2,
        ),
        (
            "transitive bridge",
            [
                [1, 1, 0, 0],
                [1, 1, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 1],
            ],
            2,
        ),
        (
            "single city",
            [[1]],
            1,
        ),
        (
            "four isolated",
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ],
            4,
        ),
        (
            "chain of five",
            [
                [1, 1, 0, 0, 0],
                [1, 1, 1, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 1, 1, 1],
                [0, 0, 0, 1, 1],
            ],
            1,
        ),
    ]
    for label, matrix, expected in cases:
        actual = find_circle_num(matrix)
        marker = "OK  " if actual == expected else "FAIL"
        if actual != expected:
            failures += 1
            print(f"[{marker}] {label}: find_circle_num(...) -> {actual}, expected {expected}")
        else:
            print(f"[{marker}] {label}: find_circle_num -> {actual}")
    if failures:
        raise AssertionError(f"{failures} assertion(s) failed; implement find_circle_num.")
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
