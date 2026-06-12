# Challenge 1 — Maximum XOR of Two Numbers (Deep Dive, LeetCode 421)

> **Difficulty:** Medium-Hard (with the deep-dive treatment). **Target solve time:** 75 minutes including UMPIRE write-up and both implementations.

This is the **bridge problem** of Week 14 — simultaneously a trie problem (a prefix tree) and a bit problem (the prefix is over binary digits, the objective is XOR-maximization). The work this week is to **implement both** the `O(n^2)` brute force (for the correctness baseline and the trade) and the `O(n * B)` bitwise-trie solution, and to defend the greedy opposite-bit walk in the Evaluate section. This is the most likely Week-14 problem to surface at a real onsite, because it tests whether you can *combine* two patterns rather than apply one in isolation.

---

## Problem spec

Given an integer array `nums`, return the maximum result of `nums[i] XOR nums[j]`, where `0 <= i <= j < n`.

**Constraints (LeetCode):**

- `1 <= nums.length <= 2 * 10^5`.
- `0 <= nums[i] <= 2^31 - 1`.

The `n` up to `2 * 10^5` is the tell: an `O(n^2)` brute force is `4 * 10^10` operations — too slow. The intended solution is `O(n * B)` where `B` is the bit width (31 or 32).

---

## Why this is the canonical bitwise-trie problem

Three reasons.

1. **It forces the recognition that a "trie" need not be over characters.** Every trie you wrote in Week 9 and earlier this week was over an alphabet of characters. The bitwise trie is over the alphabet `{0, 1}` — the binary digits of the numbers. Recognizing that the trie technique generalizes from characters to bits is the senior-grade Match move.

2. **The greedy opposite-bit walk is a clean, defensible optimality argument.** XOR is maximized when the high bits differ, because a `1` at bit position `k` contributes `2^k`, which dominates every lower bit combined. So at each level from the most-significant bit down, you greedily steer toward the *opposite* bit if a number with that bit exists. The greedy is provably optimal — the most-significant differing bit dominates — and articulating *why* is the discriminating part of the write-up.

3. **It is the bridge between the week's two pattern families.** Bit manipulation supplies the "XOR is maximized when high bits differ" insight; the trie supplies the data structure that lets you find the best partner for each number in `O(B)`. Neither pattern alone solves it; the combination does.

---

## 30-second pattern-recognition memo

Use this exact shape at the top of your write-up.

```markdown
> **30-second pattern-recognition memo (Maximum XOR / bitwise trie):**
> Maximize nums[i] XOR nums[j] over all pairs. n up to 2e5 rules out the
> O(n^2) brute force. Insert each number into a bitwise trie (a trie over
> its 31 bits, most-significant first). For each number, greedily walk the
> trie choosing the OPPOSITE bit at each level when it exists -- XOR is
> maximized when the most-significant bits differ, and a high bit dominates
> every lower bit. O(n * B) time, O(n * B) space, B = bit width = 31.
> Why not brute force: O(n^2) = 4e10, too slow. The bridge between bit
> manipulation and tries.
```

Read aloud; should hit 25–30 seconds.

---

## The intended algorithms

### Algorithm A — Brute force (O(n^2), the baseline)

```python
from __future__ import annotations

from typing import List


def find_maximum_xor_brute(nums: List[int]) -> int:
    """Maximum XOR over all pairs by checking every pair. O(n^2)."""
    best = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            best = max(best, nums[i] ^ nums[j])
    return best
```

Correct, obvious, and too slow for the constraint — but the right thing to *write first* (the Implement step's brute-force baseline) and the right thing to *trade against* in Evaluate.

### Algorithm B — Bitwise trie (O(n * B))

```python
from __future__ import annotations

from typing import Dict, List

BITS = 31  # 0 <= nums[i] <= 2^31 - 1 fits in 31 bits (bit indices 30..0)


class BitTrieNode:
    """A node in a bitwise trie; children keyed by bit value 0 or 1."""

    def __init__(self) -> None:
        self.children: Dict[int, "BitTrieNode"] = {}


def find_maximum_xor(nums: List[int]) -> int:
    """Maximum XOR over all pairs via a bitwise trie. O(n * BITS) time."""
    root = BitTrieNode()

    # Insert each number as a path of its bits, most-significant first.
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
            want = 1 - bit                 # opposite bit -> this XOR bit becomes 1
            if want in node.children:
                current |= (1 << k)
                node = node.children[want]
            else:
                node = node.children[bit]  # forced same bit -> this XOR bit is 0
        best = max(best, current)

    return best
```

The two passes — insert, then query — are each `O(n * BITS)`. The greedy `want = 1 - bit` is the heart of it: at each level, you *want* the opposite bit (which makes this position of the XOR a `1`), and you take it if the trie offers it.

---

## The level-by-level trace

`nums = [3, 10, 5, 25, 2, 8]`. The maximum XOR is `5 ^ 25 = 28`. In 5-bit binary (high to low, bits 4..0):

```
 3 = 00011
10 = 01010
 5 = 00101
25 = 11001
 2 = 00010
 8 = 01000
```

After inserting all six numbers, query with `num = 5 = 00101`. Walk from bit 4 down, wanting the opposite bit each time:

```
bit 4: 5's bit = 0, want 1. Trie has a '1' child (25, 8, 10 went down it). Take 1. current bit 4 = 1.
bit 3: 5's bit = 0, want 1. Among numbers under '1' at bit 4 (25=11001, ...), 25 has bit 3 = 1. Take 1. current bit 3 = 1.
bit 2: 5's bit = 1, want 0. 25 has bit 2 = 0. Take 0. current bit 2 = 1.
bit 1: 5's bit = 0, want 1. 25 has bit 1 = 0; no '1' child here. Take 0. current bit 1 = 0.
bit 0: 5's bit = 1, want 0. 25 has bit 0 = 1; no '0' child. Take 1. current bit 0 = 0.
```

`current = 11100 = 28`. The walk reconstructed `5 ^ 25 = 28` by greedily steering toward `25`'s differing high bits. The maximum over all six query numbers is `28`.

---

## Trade-off — when to use which

| Dimension | Algorithm A (brute force) | Algorithm B (bitwise trie) |
|-----------|---------------------------|----------------------------|
| Time | O(n^2) | O(n * B), B = 31 |
| Space | O(1) | O(n * B) for the trie |
| Code complexity | Trivial | Moderate (trie + greedy walk) |
| Feasible for n = 2e5? | No (~4e10 ops) | Yes (~6e6 ops) |
| Feasible for n = 100? | Yes | Yes (overkill) |

The discriminating factor: **if `n` is large, you must use Algorithm B**; the brute force is only acceptable when `n` is small (a few hundred) or as the correctness oracle in testing. There is also a hash-set bit-by-bit solution (build the answer one bit at a time, checking via a set of prefixes) that is also `O(n * B)` and uses `O(n)` space — mention it by name; the trie form is more transparent.

---

## Common bugs

1. **Iterating bits low-to-high instead of high-to-low.** The greedy *must* go most-significant first, because a high bit dominates. Walking low-to-high breaks the optimality argument and produces wrong answers.
2. **Off-by-one on the bit width.** `0 <= nums[i] <= 2^31 - 1` needs bit indices `30..0` (31 bits). Using too few bits truncates the high bits of large numbers; using a few extra (e.g., 32) is harmless. When in doubt, use one more bit than the constraint requires.
3. **Forgetting to take the same-bit branch when the opposite is absent.** Every number was inserted with all `BITS + 1` bits, so at every level *some* child exists; if the opposite bit is missing, the same bit must be present. Failing to fall back to it walks off the trie (a `KeyError`).
4. **Maximizing over the wrong set.** The answer is `max` over all query numbers of their best XOR partner — not the XOR of the first number only. The outer `best = max(best, current)` must run for every number.

---

## UMPIRE write-up structure

Your write-up should hit every section. The Evaluate section is the discriminating part.

### Understand

Restate the problem. Confirm: maximize XOR over all pairs; `n` up to `2 * 10^5`; values fit in 31 bits.

### Match

The 30-second memo. Name the pattern (bitwise trie), the greedy (opposite-bit walk), the complexity, and the negative-space rejection (brute force too slow).

### Plan

1. Build a bitwise trie; insert each number as a 31-bit path, most-significant first.
2. For each number, walk the trie greedily choosing the opposite bit when present.
3. Track the maximum reconstructed XOR.

### Implement

Algorithm A (brute force) as the correctness baseline, then Algorithm B (bitwise trie) as the scalable solution. Both must agree on the LC 421 examples.

### Review

Walk the level-by-level trace above for `num = 5` against the inserted set, showing `current` reaching `11100 = 28`. Confirm against the brute-force oracle on the same input.

### Evaluate

- **Time:** `O(n^2)` for A; `O(n * B)` for B with `B = 31`. For `n = 2e5`, B's `~6e6` operations versus A's `~4e10`.
- **Space:** `O(1)` for A; `O(n * B)` for B (the trie).
- **The optimality argument:** XOR is maximized when the most-significant differing bit is `1`, because `2^k` exceeds the sum of all lower bits. The greedy that steers toward the opposite bit at each level from the top is therefore optimal.
- **Trade vs. the hash-set bit-by-bit approach:** same `O(n * B)` time, `O(n)` space; the trie form is more transparent and generalizes to "find the partner," while the hash-set form only computes the maximum value.
- **Cross-reference to the week's two patterns:** this problem is where bit manipulation (Lecture 1) and tries (Lecture 2 §5) meet; name both.

---

## Acceptance

This challenge is shipped when:

- A `find_maximum_xor_brute` (Algorithm A) passes the LC 421 sample cases.
- A `find_maximum_xor` (Algorithm B, bitwise trie) passes the same cases with `O(n * B)` time, verified against the brute force on random inputs.
- A UMPIRE write-up under `umpire-writeups/c2-week-14/challenge-01-maximum-xor/` is committed with the 30-second memo at the top and a recording >= 12 minutes.
- The Evaluate section explicitly states the optimality argument for the greedy opposite-bit walk and the trade between the two algorithms.

---

## Stretch — maximum XOR with a query bound (LC 1707)

If you ship the challenge with time remaining, read **Maximum XOR With an Element From Array (LC 1707)**: the same bitwise trie, but each query restricts the partner to numbers `<= m_i`. The technique: sort the numbers and the queries, and insert into the trie *incrementally* as the query bound grows (offline processing). The bitwise trie plus offline-sorted queries is a Phase-3 onsite favorite and the natural next step once the base bitwise trie is fluent.
