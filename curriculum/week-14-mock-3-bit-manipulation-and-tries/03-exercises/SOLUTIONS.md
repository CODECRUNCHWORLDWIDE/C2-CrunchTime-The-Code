# Week 14 — Worked Solutions

Three worked solutions, each with UMPIRE narration. **Attempt every exercise on your own first.** If you read this file before drafting your own, you forfeit the recognition rep — and recognition is what Phase 2 is grading.

The solutions below are written in the same voice you should be using in your portfolio write-ups. Read them as templates, not as the answer.

---

## Solution 1 — Single Number (LC 136)

### Understand

We have an array where every value appears exactly twice except one, which appears once. Return the lone value, in `O(n)` time and `O(1)` space.

Hand-walk on `nums = [4, 1, 2, 1, 2]`: the values `1` and `2` each appear twice; `4` appears once. Answer: `4`.

### Match

Bit manipulation — XOR-cancellation. The 30-second memo:

> *Constant-space duplicate problem. The tells: "constant extra space" (rules out a hash map) plus "every element appears twice except one." XOR every element into an accumulator. By commutativity/associativity I can reorder so each duplicated pair sits together; each pair self-cancels (x ^ x = 0); the lone element survives (x ^ 0 = x). O(n) time, O(1) space. Why not a hash map / Counter: O(n) space, and the constraint forbids it. Why not a sort: O(n log n) and it mutates the input.*

### Plan

1. Initialize `result = 0` (the XOR identity).
2. XOR every element of `nums` into `result`.
3. Return `result`.

### Implement

```python
from __future__ import annotations

from typing import List


def single_number(nums: List[int]) -> int:
    """Return the element that appears exactly once; all others appear twice."""
    result = 0
    for num in nums:
        result ^= num
    return result
```

The one-liner `from functools import reduce; from operator import xor; return reduce(xor, nums, 0)` is equivalent and idiomatic, but the explicit loop is clearer to narrate.

### Review

Trace `nums = [4, 1, 2, 1, 2]` in array order:

```
result = 0
^ 4 -> 4
^ 1 -> 5
^ 2 -> 7
^ 1 -> 6
^ 2 -> 4
Return 4.
```

Or grouped, to show the cancellation: `4 ^ (1 ^ 1) ^ (2 ^ 2) = 4 ^ 0 ^ 0 = 4`. The identities guarantee both orders produce the same result.

### Evaluate

- **Time:** `O(n)`. Single pass.
- **Space:** `O(1)`. One accumulator.
- **Trade-off:** vs. a hash map / `Counter` — same `O(n)` time but `O(n)` space, which the constraint forbids. vs. sorting and scanning for the unpaired element — `O(n log n)` and mutates the input. The constant-space constraint is exactly the tell that selects XOR over both.

---

## Solution 2 — Implement Trie (LC 208)

### Understand

Build a prefix-tree data structure supporting `insert`, exact `search`, and prefix `starts_with`. The distinction: `search("app")` is `True` only if `"app"` was inserted as a complete word; `starts_with("app")` is `True` if any inserted word *begins* with `"app"`.

Hand-walk: insert `"apple"`. Then `search("apple")` is `True`; `search("app")` is `False` (the path `a -> p -> p` exists, but the node at the second `p` is not marked as a terminal); `starts_with("app")` is `True` (the path exists). After `insert("app")`, `search("app")` becomes `True` (the node is now a terminal).

### Match

Trie at speed. The 30-second memo:

> *Prefix-query data structure. Each node is a dict of child characters plus an is_end flag. insert walks/creates the path and marks the terminal. search walks and checks is_end. starts_with walks and checks reachability. Factor the shared walk into one helper. Why a trie over a hash set: a set answers exact-match in O(L) but cannot answer prefix queries in less than O(n * L); the trie answers starts_with in O(P). All three ops are O(L) worst-case with no probabilistic failure mode. This week the recognition is assumed; the bar is speed — under five minutes for the three operations.*

### Plan

1. `TrieNode` holds `children: dict[str, TrieNode]` and `is_end: bool`.
2. `insert(word)`: walk from the root, creating a child node for each missing character; mark the final node `is_end = True`.
3. `_walk(s)`: follow children character by character; return the terminal node, or `None` on a miss.
4. `search(word)`: `_walk(word)` is not `None` **and** the node's `is_end` is `True`.
5. `starts_with(prefix)`: `_walk(prefix)` is not `None`.

### Implement

```python
from __future__ import annotations

from typing import Dict, Optional


class TrieNode:
    """A single trie node: a map of child characters plus an end-of-word flag."""

    def __init__(self) -> None:
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end: bool = False


class Trie:
    """Prefix tree supporting insert, exact search, and prefix search."""

    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        return self._walk(prefix) is not None

    def _walk(self, s: str) -> Optional["TrieNode"]:
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node
```

The `_walk` helper is the speed move — `search` and `starts_with` share the loop, differing only in the final check. Writing the walk twice is the canonical time-waster on this problem.

### Review

After `insert("apple")`:

```
search("apple"): _walk reaches the 'e' node, is_end = True -> True.
search("app"):   _walk reaches the second 'p' node, is_end = False -> False.
starts_with("app"): _walk reaches the second 'p' node (not None) -> True.
starts_with("apx"): _walk fails at 'x' (no child) -> None -> False.
```

After `insert("app")`: the second `p` node now has `is_end = True`, so `search("app")` returns `True`.

### Evaluate

- **Time:** `insert`, `search`, `starts_with` are all `O(L)` where `L` is the length of the word or prefix — worst-case, with no probabilistic failure mode (the hash-set distinction from Week 9).
- **Space:** `O(total characters inserted)` in the worst case of no shared prefixes; better when keys overlap, since common prefixes share nodes.
- **Trade-off:** vs. a `Set[str]` — the set is simpler and competitive for exact-match-only workloads, but cannot answer prefix queries efficiently. The moment the problem asks "starts with" / autocomplete / longest-word-with-prefix, the trie is the right structure.

---

## Solution 3 — Counting Bits (LC 338)

### Understand

For every `i` in `0..n`, return the number of set bits in `i`. The output is a list of length `n + 1`. The follow-up: `O(n)` time, no built-in popcount.

Hand-walk on `n = 5`: `0=0b0` (0 bits), `1=0b1` (1), `2=0b10` (1), `3=0b11` (2), `4=0b100` (1), `5=0b101` (2). Answer: `[0, 1, 1, 2, 1, 2]`.

### Match

Bit manipulation meets DP — a 1D DP over the bit representation. The 30-second memo:

> *Count set bits for every i up to n. The naive approach calls popcount per number — O(n log n). The DP reuses subproblems: popcount(i) = popcount(i >> 1) + (i & 1). Right-shifting i drops its lowest bit; the remaining set bits are exactly popcount(i >> 1), already computed because i >> 1 < i; add back the low bit. State = "number of set bits in i." Recurrence: dp[i] = dp[i >> 1] + (i & 1). O(n) time, O(n) output. The same Week-11 DP discipline, applied to bits.*

### Plan

1. Allocate `dp = [0] * (n + 1)`; `dp[0] = 0` by zero-initialization (the base case — zero has no set bits).
2. Loop `i` from `1` to `n`: `dp[i] = dp[i >> 1] + (i & 1)`.
3. Return `dp`.

### Implement

```python
from __future__ import annotations

from typing import List


def count_bits(n: int) -> List[int]:
    """ans[i] = number of set bits in i, for i in 0..n. O(n) time."""
    dp: List[int] = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp
```

Six lines. No call to `bin().count` or `int.bit_count`; the DP is the point.

### Review

Trace `n = 5`:

```
dp[0] = 0
dp[1] = dp[1 >> 1] + (1 & 1) = dp[0] + 1 = 1
dp[2] = dp[2 >> 1] + (2 & 1) = dp[1] + 0 = 1
dp[3] = dp[3 >> 1] + (3 & 1) = dp[1] + 1 = 2
dp[4] = dp[4 >> 1] + (4 & 1) = dp[2] + 0 = 1
dp[5] = dp[5 >> 1] + (5 & 1) = dp[2] + 1 = 2
Return [0, 1, 1, 2, 1, 2].
```

Matches the hand-enumeration. Note the recurrence reads `dp[i >> 1]`, which is always a *smaller* index, so it is finalized before `dp[i]` needs it — the iteration order (left to right) is automatically correct.

### Evaluate

- **Time:** `O(n)`. Each `dp[i]` is `O(1)` work (a shift, an AND, an add).
- **Space:** `O(n)` for the output array. No auxiliary structure beyond it.
- **Trade-off:** vs. popcount-each-number (`bin(i).count("1")` for each `i`) — that is `O(n log n)` because each popcount is `O(log i)`. The DP reuses the answer for `i >> 1`, dropping the log factor. An alternative DP recurrence `dp[i] = dp[i & (i - 1)] + 1` (clear the lowest set bit, add one) is equally `O(n)` and equally valid; the `dp[i >> 1] + (i & 1)` form is the more common shape.

---

## Closing — common bugs and how to avoid them

Across all three exercises:

1. **Forgetting the XOR identity initializer.** Single number must start the accumulator at `0`, not at `nums[0]` — starting at `0` is cleaner and avoids an empty-array special case. (`0 ^ nums[0] == nums[0]`, so both work, but `0` is the principled choice.)
2. **Writing the trie walk loop twice.** `search` and `starts_with` share the walk; factor it into `_walk`. Duplicating the loop is the canonical time-waster on LC 208 and the reason an unprepared candidate misses the under-five-minute bar.
3. **The trie `is_end` distinction.** `search` requires `is_end`; `starts_with` does not. Conflating them makes `search("app")` wrongly return `True` after inserting only `"apple"`. This is the single most common LC 208 bug.
4. **Calling built-in popcount on counting-bits.** The follow-up forbids `bin().count` and `int.bit_count`; the lesson is the DP. Reaching for the built-in passes the test but forfeits the rep.
5. **Off-by-one on the counting-bits output length.** The output is length `n + 1` (indices `0` through `n`), not `n`. Allocating `[0] * n` drops the final entry.

After this set of three, the two Week-14 patterns should be reflexive: XOR-cancellation for the constant-space-plus-duplicates tell, the trie template at speed, and the bit-DP for the count-set-bits shape. The week's mini-project (Mock #3 plus the XOR-trick and trie write-ups) is the proof.

Move on to the [quiz](../05-quiz.md), then the [homework](../06-homework.md), then the [mini-project](../07-mini-project/00-overview.md).
