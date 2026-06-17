# Lecture 2 — Bitmasks, Bitmask DP, and Tries at Speed

> **Duration:** ~2 hours.
> **Outcome:** You can represent a subset of a small universe as an integer and perform the five set operations in `O(1)`, enumerate every submask of a mask, write a bitmask DP and defend its `O(2^n * n)` bound, implement counting-bits as a 1D DP over bits, write a trie's three operations from memory in under five minutes, and build a bitwise trie for maximum-XOR — the bridge between this week's two pattern families.

Lecture 1 installed the XOR identities and the bit-twiddling vocabulary. This lecture takes both into structured territory. First, **bitmasks** — using a single integer to represent a subset of a small universe, and the dynamic programs whose state *is* such a subset. Then a pivot to **tries at speed** — the Week-9 install drilled until the three operations are sub-five-minute reflexes — and the **bitwise trie**, the data structure that solves maximum-XOR and connects bit manipulation to tries.

By the end of this lecture you should be able to read a problem with `n <= 20` and "consider all subsets" and immediately reach for a bitmask; read a prefix question and write the trie in under five minutes; and read "maximum XOR of two numbers" and reach for the bitwise trie.

---

## 1. A bitmask is a subset in one integer

When the universe is small — `{0, 1, ..., n-1}` with `n <= 20` or so — a subset can be encoded as a single integer where bit `i` is set iff element `i` is in the subset. The set `{0, 2, 3}` over a universe of size 5 is `0b01101 = 13`.

The five core operations, all `O(1)`:

| Operation | Expression |
|-----------|-----------|
| Empty set | `0` |
| Full set on `n` elements | `(1 << n) - 1` |
| Is element `i` in the set? | `mask & (1 << i)` (truthy iff in) |
| Add element `i` | `mask | (1 << i)` |
| Remove element `i` | `mask & ~(1 << i)` |
| Set size | `mask.bit_count()` (3.10+) or `bin(mask).count("1")` |

```python
>>> mask = 0
>>> mask |= (1 << 0)   # add element 0
>>> mask |= (1 << 2)   # add element 2
>>> mask |= (1 << 3)   # add element 3
>>> bin(mask)
'0b1101'
>>> bool(mask & (1 << 2))   # is element 2 in?
True
>>> bool(mask & (1 << 1))   # is element 1 in?
False
>>> mask.bit_count()
3
```

**Why `n <= 20`?** There are `2^n` possible subsets. For `n = 20`, that is about a million masks — feasible to enumerate. For `n = 30`, it is a billion — too many. The constraint `n <= 20` (sometimes `22`) in a problem statement is the recognition cue that a bitmask solution is intended. When you see a tight `n` and "subsets" or "visit all," reach for the bitmask.

---

## 2. Enumerating subsets and submasks

Two enumeration patterns recur.

**All subsets of the universe `{0..n-1}`:** iterate `mask` from `0` to `2^n - 1`. Each value of `mask` *is* a distinct subset.

```python
for mask in range(1 << n):
    # mask ranges over every subset of {0..n-1}
    members = [i for i in range(n) if mask & (1 << i)]
```

**All submasks of a given `mask`:** the `sub = (sub - 1) & mask` idiom. Starting from `sub = mask` and repeatedly applying `sub = (sub - 1) & mask` walks every submask in descending order, ending at `0`.

```python
def submasks(mask: int):
    """Yield every submask of `mask`, including `mask` itself and 0."""
    sub = mask
    while sub:
        yield sub
        sub = (sub - 1) & mask
    yield 0   # the empty submask, which the loop exits before yielding
```

The `(sub - 1) & mask` trick works because subtracting 1 borrows through the trailing zeros and flips the lowest set bit, and the `& mask` projects back onto the bits of `mask`. The aggregate cost of enumerating submasks across *all* masks of an `n`-bit universe is `O(3^n)` — each of the `n` bits is, independently, "in mask and sub," "in mask not sub," or "not in mask," giving `3^n` (mask, submask) pairs. The `3^n` aggregate bound is a Phase-3 favorite; recognition-grade here.

---

## 3. Bitmask DP — the state is a subset

A **bitmask DP** is a dynamic program whose state is a bitmask. The canonical shape: `dp[mask]` answers "the best value (or the count) over having committed exactly the set of elements in `mask`." The transition adds one element to the set.

The skeleton:

```python
from __future__ import annotations


def bitmask_dp_skeleton(n: int) -> int:
    """dp[mask] = best/count over having committed exactly `mask`."""
    full = (1 << n) - 1
    dp = [0] * (1 << n)
    dp[0] = 1  # base case (problem-dependent): the empty set has one way

    for mask in range(1 << n):
        for i in range(n):
            if not (mask & (1 << i)):           # element i not yet committed
                nxt = mask | (1 << i)           # commit it
                dp[nxt] += dp[mask]             # combine per the recurrence
    return dp[full]
```

**Complexity.** `2^n` states; for each, an `O(n)` loop over candidate elements to add. Total `O(2^n * n)`. For `n = 20`, that is `2^20 * 20 ≈ 2.1e7` — fast. For `n = 25`, about `8.4e8` — borderline. The `n <= 20` constraint is exactly calibrated to this bound.

**Iteration order.** Iterate masks in *increasing* order when the transition adds an element, so `mask < nxt` always holds and `dp[mask]` is finalized before it feeds `dp[nxt]`. (If a transition removes an element, iterate in decreasing order.)

**The classic application — travelling salesman / Hamiltonian path / "visit all nodes."** The state is `(mask, last)`: `mask` is the set of visited nodes; `last` is the most recently visited node. `dp[mask][last]` is the best cost of a path that visits exactly the nodes in `mask` and ends at `last`. The transition extends to an unvisited node. This is the standard `O(2^n * n^2)` Held-Karp DP; the recognition cue is "find a path/cost visiting all of `n <= 15` nodes." Shortest path visiting all nodes (LC 847) is the canonical LeetCode instance. Recognition-grade this week; implementation is a Phase-3 rep.

**State semantics first.** As with every DP (Week 11's discipline), name the state in words before writing the recurrence: "`dp[mask]` is the number of ways to have committed exactly the elements in `mask`." The recurrence is problem-specific; the state shape — a subset of a small universe — is the constant.

---

## 4. Counting bits (LC 338) — the 1D DP over bits

> *Given an integer `n`, return an array `ans` of length `n + 1` such that for each `i` (`0 <= i <= n`), `ans[i]` is the number of `1`s in the binary representation of `i`.*

**Match.** You could call `bin(i).count("1")` for each `i` — that is `O(n log n)` (the popcount of each number costs `O(log i)`). But there is an `O(n)` DP that reuses prior answers, and recognizing it is the point.

**The recurrence.** The number of set bits in `i` is the number of set bits in `i >> 1` (drop the low bit) plus the low bit itself (`i & 1`):

```
popcount(i) = popcount(i >> 1) + (i & 1)
```

Right-shifting `i` by one drops its lowest bit; whatever set bits remain are exactly the set bits of `i` minus the low bit. Since `i >> 1 < i`, the answer for `i >> 1` is already computed when we reach `i` — a clean 1D DP.

**Implementation.**

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

Six lines. `dp[0] = 0` is the base case (zero has no set bits), already set by the zero-initialization.

**Trace on `n = 5`:**

```
dp[0] = 0
dp[1] = dp[0] + (1 & 1) = 0 + 1 = 1     (1 = 0b1)
dp[2] = dp[1] + (2 & 1) = 1 + 0 = 1     (2 = 0b10)
dp[3] = dp[1] + (3 & 1) = 1 + 1 = 2     (3 = 0b11)
dp[4] = dp[2] + (4 & 1) = 1 + 0 = 1     (4 = 0b100)
dp[5] = dp[2] + (5 & 1) = 1 + 1 = 2     (5 = 0b101)
Answer: [0, 1, 1, 2, 1, 2].
```

**Defense.** "Counting bits is a 1D DP over the bit representation. `dp[i] = dp[i >> 1] + (i & 1)`: drop the low bit and reuse the already-computed answer, then add back the low bit. `O(n)` time, `O(n)` output. Beats the `O(n log n)` popcount-each-number approach by reusing subproblems — the same DP discipline from Week 11, applied to bits."

---

## 5. Trie at speed — the Week-9 install, drilled to reflex

Week 9 installed the trie and graded *recognition*. Week 14 assumes the recognition and grades *speed*: `insert`, `search`, `starts_with` in under five minutes, no hesitation, in either form. The trie is not in the standard library; you build it every time, so fluency is the whole game.

**The `TrieNode` class form.**

```python
from __future__ import annotations

from typing import Dict


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

    def _walk(self, s: str) -> "TrieNode | None":
        """Walk the trie along s; return the terminal node or None."""
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node
```

The `_walk` helper factors out the shared loop between `search` and `starts_with` — `search` additionally checks `is_end`, `starts_with` only checks reachability. That factoring is the speed move; do not write the walk loop twice.

**The dict-of-dict form** (more compact, no class) was covered in Week 9 Lecture 1 §3. Either is interview-acceptable; the class form reads more clearly under narration and is the one to default to.

**Complexity.** `insert`, `search`, `starts_with` are all `O(L)` where `L` is the length of the word or prefix — worst-case, with no probabilistic failure mode (the distinction from a hash set, defended in Week 9).

---

## 6. The bitwise trie — maximum XOR (LC 421)

> *Given an integer array `nums`, return the maximum result of `nums[i] XOR nums[j]` over all pairs.*

This is the **bridge problem** of the week: it is a trie problem (a prefix tree) *and* a bit problem (the prefix is over binary digits, and the objective is XOR-maximization). The data structure is a **bitwise trie** — a trie where every edge is a `0` or a `1`, and each number is stored as a root-to-leaf path of its bits from most-significant to least.

**Why a trie helps.** The brute force checks all `O(n^2)` pairs. The trie reduces it to `O(n * B)` where `B` is the bit width (32, or fewer if the numbers are bounded). The key insight: **XOR is maximized when the high bits differ.** To maximize `x XOR y` for a fixed `x`, at each bit position from the top down, you want `y` to have the *opposite* bit. The trie lets you greedily follow the opposite bit if a number with that bit exists, falling back to the same bit otherwise.

**The algorithm.**

1. Insert every number into the bitwise trie (each as a 32-bit, or `B`-bit, path).
2. For each number `x`, walk the trie from the most-significant bit. At each level, try to go down the branch with the bit *opposite* to `x`'s bit (which would set this bit in the XOR); if that branch exists, take it and record a `1` in the running XOR for this position; otherwise take the same-bit branch and record a `0`.
3. The maximum over all `x` is the answer.

**Implementation.**

```python
from __future__ import annotations

from typing import Dict, List

BITS = 31  # enough for 0 <= nums[i] <= 2^31 - 1; adjust to the constraint


class BitTrieNode:
    """A node in a bitwise trie; children keyed by bit value 0 or 1."""

    def __init__(self) -> None:
        self.children: Dict[int, "BitTrieNode"] = {}


def find_maximum_xor(nums: List[int]) -> int:
    """Maximum value of nums[i] XOR nums[j] over all pairs, via a bitwise trie."""
    root = BitTrieNode()

    # Insert every number as a path of its bits, high to low.
    for num in nums:
        node = root
        for k in range(BITS, -1, -1):
            bit = (num >> k) & 1
            if bit not in node.children:
                node.children[bit] = BitTrieNode()
            node = node.children[bit]

    best = 0
    # For each number, greedily walk toward the opposite bit at each level.
    for num in nums:
        node = root
        current = 0
        for k in range(BITS, -1, -1):
            bit = (num >> k) & 1
            want = 1 - bit                 # the opposite bit maximizes the XOR
            if want in node.children:
                current |= (1 << k)        # this bit of the XOR can be 1
                node = node.children[want]
            else:
                node = node.children[bit]  # forced to the same bit -> XOR bit is 0
        best = max(best, current)

    return best
```

**Trace the intuition on `nums = [3, 10, 5, 25, 2, 8]`:** the maximum XOR is `5 ^ 25 = 28`. Walking `5 = 00101` against the trie, the greedy opposite-bit choices steer toward `25 = 11001`, whose high bits differ from `5`'s, producing the large XOR. (The full level-by-level trace is in [Challenge 1](../04-challenges/challenge-01-maximum-xor.md).)

**Defense.** "Maximum XOR is a bitwise trie. Insert each number as a 32-bit root-to-leaf path. To maximize the XOR with a fixed `x`, greedily follow the opposite bit at each level from the top — XOR is largest when the most-significant bits differ. `O(n * B)` time where `B` is the bit width, versus `O(n^2)` brute force. This is the problem where bit manipulation and tries meet."

---

## 7. Trie with wildcards — add and search word (LC 211)

> *Design a data structure that supports adding new words and finding if a string matches any previously added string, where the search string may contain `.` to match any single character.*

The `add` operation is a plain trie `insert`. The `search` is the escalation: when the walk hits a `.`, it must try **every** child at that level — a branching, recursive walk.

```python
from __future__ import annotations

from typing import Dict


class WordNode:
    def __init__(self) -> None:
        self.children: Dict[str, "WordNode"] = {}
        self.is_end: bool = False


class WordDictionary:
    """Trie supporting add and wildcard ('.') search."""

    def __init__(self) -> None:
        self.root = WordNode()

    def add_word(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, WordNode())
        node.is_end = True

    def search(self, word: str) -> bool:
        return self._search(word, 0, self.root)

    def _search(self, word: str, i: int, node: WordNode) -> bool:
        if i == len(word):
            return node.is_end
        ch = word[i]
        if ch == ".":
            # Wildcard: try every child.
            return any(self._search(word, i + 1, child) for child in node.children.values())
        if ch not in node.children:
            return False
        return self._search(word, i + 1, node.children[ch])
```

The `.` case is the only difference from a plain trie search: instead of following one child, it recurses into all of them and ORs the results. The worst-case cost of an all-`.` query is `O(26^L)` in the alphabet-26 case, but in practice the trie's branching is sparse and the walk prunes quickly.

---

## 8. Closing — the long tail, installed

Three takeaways:

1. **A bitmask is a subset in an integer.** When `n <= 20` and the prompt says "subsets" or "visit all," reach for the bitmask. The five set operations are `O(1)`; bitmask DP is `O(2^n * n)`; the constraint is calibrated to the bound.
2. **Tries this week are about speed, not recognition.** The Week-9 install is assumed; the bar is sub-five-minute `insert` / `search` / `starts_with`. Factor the walk loop once with a helper.
3. **The bitwise trie is the bridge.** Maximum XOR is simultaneously a trie problem and a bit problem; the greedy opposite-bit walk is the senior-grade move that connects both pattern families. It is the most likely Week-14 problem to appear at a real onsite.

Lecture 3 leaves the patterns behind and installs the **Mock #3 protocol** — near-real conditions, the 45-minute structure, and the self-feedback discipline that turns a recording into one specific behavior change for Mock #4.

[Back to the README](../00-overview.md). On to [Lecture 3 — The Mock #3 Protocol](./03-the-mock-3-protocol.md).
