# Challenge 2 — Smallest String With Swaps (LeetCode 1202, Optional)

> **Difficulty:** Medium. **Target solve time:** 45 minutes including UMPIRE write-up.

Optional challenge for learners ahead of schedule by Friday. The canonical "DSU + sort within each group" composition — find the swap-equivalence classes via DSU, then sort the characters within each class to produce the lexicographically smallest arrangement.

---

## Problem spec

You are given a string `s`, and an array of pairs of indices in the string `pairs` where `pairs[i] = [a, b]` indicates 2 indices (0-indexed) of the string.

You can swap the characters at any pair of indices in the given `pairs` **any number of times**.

Return the lexicographically smallest string that `s` can be changed to after using the swaps.

**Constraints (LeetCode):**

- `1 <= len(s) <= 10^5`.
- `0 <= len(pairs) <= 10^5`.
- `0 <= pairs[i][0], pairs[i][1] < len(s)`.
- `s` only contains lower case English letters.

---

## Why this is the canonical DSU composition

The key observation: swaps are *transitive*. If you can swap indices `(0, 1)` and `(1, 2)`, then you can also achieve the swap `(0, 2)` indirectly by a sequence of pair-swaps. The set of indices reachable from any given index via the pair-swap relation forms an **equivalence class**. Within each equivalence class, you can arrange the characters in *any* order.

The optimal arrangement is the lexicographically smallest: sort the characters within each class, then place them back into the sorted positions of that class.

DSU is the canonical reach for the equivalence-class step. Sort is the canonical reach for the within-class step.

---

## 30-second pattern-recognition memo

```markdown
> **30-second pattern-recognition memo (DSU + sort):**
> Swaps are transitive. Compute the equivalence classes of indices via DSU
> over the pairs -- O(P alpha(N)) where P = len(pairs), N = len(s). Group
> indices by their root; within each group, collect the characters from s,
> sort them ascending, and place them back into the sorted positions of
> the group. O(N log N) for the sort. Why not BFS/DFS to find components:
> also correct, comparable complexity, but the DSU is cleaner for the
> "iterate pairs and union" formulation. Output: rebuild the string by
> placing the sorted character lists back into the sorted index lists per
> component.
```

Read aloud; should hit 25-30 seconds.

---

## The intended algorithm

```python
from __future__ import annotations

from collections import defaultdict
from typing import Dict, List


class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent: List[int] = list(range(n))
        self.rank: List[int] = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1


def smallest_string_with_swaps(s: str, pairs: List[List[int]]) -> str:
    """Return the lexicographically smallest string reachable via the swap pairs."""
    n = len(s)
    uf = UnionFind(n)
    for a, b in pairs:
        uf.union(a, b)

    # Group indices by their DSU root.
    groups: Dict[int, List[int]] = defaultdict(list)
    for i in range(n):
        groups[uf.find(i)].append(i)

    result: List[str] = list(s)
    for indices in groups.values():
        chars = sorted(result[i] for i in indices)
        # `indices` is already sorted because we iterated `i` in 0..n-1.
        for idx, ch in zip(indices, chars):
            result[idx] = ch

    return "".join(result)
```

Thirty lines including the DSU class. The structure is two-phase: DSU to find equivalence classes, then sort within each class.

---

## The two subtle bugs

**Bug 1 — Sorting the characters but not aligning them with sorted indices.** The `indices` list is already sorted (we built it by iterating `i` in `0..n-1`), so the alignment with the sorted `chars` produces the lexicographically smallest output for that group. If you build `indices` in a different order (e.g., by traversing `groups[root]` after some mutation), you need to sort it explicitly.

**Bug 2 — Forgetting that the swap relation is over the index, not the character.** The DSU is over *indices* of `s`, not over *characters*. Two indices with the same character that are not in a swap-connected component cannot be exchanged. The senior implementation states this in a comment.

---

## UMPIRE write-up template

### Understand

Restate the problem. Walk the LC 1202 example 1:

```
s = "dcab"
pairs = [[0, 3], [1, 2]]

DSU after unions: {0, 3} and {1, 2}.
Group {0, 3}: characters 'd', 'b'. Sorted: ['b', 'd']. Place at sorted indices [0, 3]: result[0] = 'b', result[3] = 'd'.
Group {1, 2}: characters 'c', 'a'. Sorted: ['a', 'c']. Place at sorted indices [1, 2]: result[1] = 'a', result[2] = 'c'.

Final: "bacd".
```

### Match

Open with the 30-second memo. Name the two algorithms (DSU + sort). State the recognition cue — "swaps are transitive."

### Plan

1. Build `UnionFind(len(s))`; union every pair.
2. Group indices by `uf.find(i)` into a `Dict[int, List[int]]`.
3. For each group: collect the characters at those indices, sort, place back.
4. Return `"".join(result)`.

### Implement

The code above. Type hints on every function; docstrings on the public ones.

### Review

Trace example 1 (above). Edge case — `pairs = []`: every index is its own group; no sort changes anything; return `s` unchanged. Edge case — every pair connects everything: one group covering all of `s`; sort the entire string ascending and return.

### Evaluate

- **Time:** `O(N alpha(N) + N log N + P alpha(N))` = `O(N log N + P alpha(N))`. The sort within each group dominates for typical inputs.
- **Space:** `O(N)` for the DSU and the result.
- **Trade vs BFS to find components:** also correct, comparable complexity. DSU is shorter here because we iterate pairs once and call `union` per pair; BFS would need to build an adjacency list first.

---

## Acceptance

The optional challenge is complete when:

- The implementation passes all LC 1202 sample cases.
- A UMPIRE write-up is committed under `umpire-writeups/c2-week-10/challenge-02-smallest-string/`.
- The Match section names DSU and the composition (DSU + sort).

If time runs short, skip this challenge in favor of homework problems 1-3. It is a high-quality recognition rep but not on the critical path for Mock #2.
