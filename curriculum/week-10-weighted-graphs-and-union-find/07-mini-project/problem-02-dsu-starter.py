"""Mini-Project Problem 2 starter - DSU (Redundant Connection, LC 684).

This is the starter for the mini-project's second write-up. Copy this
file into your portfolio repository and fill in the function bodies. The
write-up itself lives in `umpire-writeups/c2-week-10/mini-project/`.

Pattern: Union-Find with path compression and union by rank; the cycle-
detection sub-shape from Lecture 3 section 4.
Target solve time: 30 minutes including the full UMPIRE write-up.

Spec
----
In LC 684's framing, you start with a tree on `n` nodes (labeled 1..n)
with `n - 1` edges, then one extra edge is added (creating exactly one
cycle). Given the resulting edge list (length `n`), return the edge that,
when removed, restores the tree property. If multiple candidate edges
would work, return the one that appears last in the input.

Constraints (LeetCode):
- n == len(edges).
- 3 <= n <= 1000.
- edges[i].length == 2.
- 1 <= ai < bi <= n.
- ai != bi.
- No duplicate edges in the input.

The "last edge" rule is the discriminating detail. Process edges in
order; the FIRST edge whose `union(u, v)` returns False is the one that
would have closed the unique cycle if added -- and by LC 684's spec,
this is the answer.

UMPIRE checklist (do this before writing code)
----------------------------------------------
- [ ] U: Restate. There is exactly one redundant edge; return it. The
        spec detail: if multiple, the answer is the LAST in the input
        order. Walking the input top-to-bottom, the FIRST cycle-closing
        union is the answer.
- [ ] M: DSU cycle-detection. Path compression + union by rank ->
        amortized O(alpha(n)) per operation. Reject BFS-based cycle-
        detection (correct but harder to write under pressure).
- [ ] P: Build UnionFind(n + 1) (LC 684 is 1-indexed). Iterate edges
        in order. The first edge whose union returns False is the
        redundant one; return it.
- [ ] I: Class form for UnionFind. find with recursive path compression;
        union with rank balancing; return True/False from union.
- [ ] R: Trace example 1: edges = [[1,2],[1,3],[2,3]]. Initial: each
        node its own root. union(1, 2) -> True; union(1, 3) -> True;
        union(2, 3) -> False (find(2) == find(3) == root of 1). Return
        [2, 3].
- [ ] E: O(n alpha(n)) time; O(n) space. The alpha(n) <= 4 in practice.
        Trade vs BFS-based cycle-detection (O(V + E) per query but
        more code; DSU is also natively incremental).

References
----------
- Lecture 3, sections 3 and 4 (sub-shape 2):
  ../lecture-notes/03-union-find-and-the-dsu-triggers.md
- Exercise 3 (warm-up): ../exercises/exercise-03-number-of-provinces.py
- LeetCode 684: https://leetcode.com/problems/redundant-connection/
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
        """Initialize a DSU with `n` singletons (indices 0..n-1)."""
        # TODO: parent = list(range(n)); rank = [0] * n
        self.parent: List[int] = list(range(n))
        self.rank: List[int] = [0] * n

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
        # TODO: union by rank; return False if already in the same set
        # Hint:
        #   rx, ry = self.find(x), self.find(y)
        #   if rx == ry: return False
        #   if self.rank[rx] < self.rank[ry]: rx, ry = ry, rx
        #   self.parent[ry] = rx
        #   if self.rank[rx] == self.rank[ry]: self.rank[rx] += 1
        #   return True
        _ = x, y  # silence unused-variable lint until you wire it up
        return False


def find_redundant_connection(edges: List[List[int]]) -> List[int]:
    """Return the redundant edge in a near-tree undirected graph.

    Walk the edges in input order; the first edge whose `union(u, v)`
    returns False is the cycle-closer and (by LC 684 spec) the answer.

    Fill in the body. The signature and docstring are part of the spec.
    """
    # TODO: build UnionFind sized for 1-indexed labels (n + 1 entries)
    # Hint:
    #   n = len(edges)
    #   uf = UnionFind(n + 1)
    #   for u, v in edges:
    #       if not uf.union(u, v):
    #           return [u, v]
    #   return []
    _ = edges  # silence unused-variable lint until you wire it up
    return []


# ---------------------------------------------------------------------------
# Self-test block. Runs on `python3 problem-02-dsu-starter.py`.
# Also discovered by `pytest`.
# ---------------------------------------------------------------------------


def _run_self_tests() -> None:
    """Run a battery of asserts; many will fail until you implement."""
    failures = 0
    cases: List = [
        (
            "LC 684 example 1",
            [[1, 2], [1, 3], [2, 3]],
            [2, 3],
        ),
        (
            "LC 684 example 2",
            [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]],
            [1, 4],
        ),
        (
            "triangle on three nodes",
            [[1, 2], [2, 3], [1, 3]],
            [1, 3],
        ),
        (
            "five-cycle",
            [[1, 2], [2, 3], [3, 4], [4, 5], [5, 1]],
            [5, 1],
        ),
        (
            "star with extra edge",
            [[1, 2], [1, 3], [1, 4], [2, 3]],
            [2, 3],
        ),
    ]
    for label, edges, expected in cases:
        actual = find_redundant_connection(edges)
        marker = "OK  " if actual == expected else "FAIL"
        if actual != expected:
            failures += 1
            print(f"[{marker}] {label}: -> {actual}, expected {expected}")
        else:
            print(f"[{marker}] {label}: -> {actual}")
    if failures:
        raise AssertionError(
            f"{failures} assertion(s) failed; implement find_redundant_connection."
        )
    print("All cases passed.")


if __name__ == "__main__":
    _run_self_tests()
