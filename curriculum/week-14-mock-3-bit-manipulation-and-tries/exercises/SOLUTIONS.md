# Week 14 — Worked Solutions

Three worked solutions, each with UMPIRE narration. **Attempt every exercise on your own first.** If you read this file before drafting your own, you forfeit the recognition rep — and recognition is what a mock week grades hardest.

The solutions below are written in the same voice you should be using in your portfolio write-ups. Read them as templates, not as the answer.

---

## Solution 1 — Single Number (LC 136)

### 30-second pattern-recognition memo

> *XOR fold. Every element appears twice except one, and the constraint demands constant extra space — so I reduce the array by `^`. Pairs cancel because `a ^ a == 0`; the survivor remains because `a ^ 0 == a`; order is irrelevant because XOR is commutative and associative. Time `O(n)`, space `O(1)`. The hash-map answer is `O(n)` space, which the constant-space hint rules out.*

### Understand

A non-empty array where every value is paired except one survivor; return the survivor. The two binding constraints are linear time and constant space. Hand-walk `[4, 1, 2, 1, 2]`: the 1s pair, the 2s pair, the 4 is alone → `4`.

### Match

XOR fold (see the memo). Reject the `Counter` answer (`O(n)` space) and sort-then-scan (`O(n log n)` time, mutates the input).

### Plan

1. Seed an accumulator `result = 0` (the XOR identity).
2. XOR every element into `result`.
3. Return `result` — all paired values have cancelled to 0; the survivor remains.

### Implement

```python
from typing import List


def single_number(nums: List[int]) -> int:
    """Return the one element that appears once; all others appear twice."""
    result = 0
    for value in nums:
        result ^= value
    return result
```

The `functools.reduce(xor, nums, 0)` one-liner is worth naming as "the same fold expressed functionally," but write the explicit loop on the whiteboard.

### Review

Trace `[4, 1, 2, 1, 2]`: `0^4=4, 4^1=5, 5^2=7, 7^1=6, 6^2=4` → `4` ✓. Single-element `[1]`: `0^1=1` ✓. Negatives work unchanged — XOR acts on the bit pattern.

### Evaluate

- **Time:** `O(n)` — one pass, one XOR per element.
- **Space:** `O(1)` — a single accumulator. This is exactly the constraint the problem demanded.
- **Trade vs hash map:** the `Counter` solution is `O(n)` time but `O(n)` space; the XOR fold is strictly better on space and is the intended answer.

---

## Solution 2 — Counting Bits (LC 338)

### 30-second pattern-recognition memo

> *Bit DP. I build `dp[i]` from a strictly smaller, already-computed subproblem in `O(1)`. The recurrence is `dp[i] = dp[i >> 1] + (i & 1)`: right-shifting drops the low bit (so `i >> 1` is `i // 2`, whose popcount I already have), and `i & 1` adds the dropped bit back. One forward pass, `O(n)` time, `O(n)` output. The naive per-element popcount is `O(n log n)`; this is the `O(n)` answer the follow-up wants.*

### Understand

For each `i` in `0..n`, store the number of set bits at index `i`. The naive `[i.bit_count() for i in range(n + 1)]` is `O(n log n)`; the follow-up asks for `O(n)`, which means each entry must be `O(1)` given the entries already computed — the DP tell. Hand-walk `n = 5` → `[0, 1, 1, 2, 1, 2]`; note `dp[4] = dp[2]` and `dp[5] = dp[2] + 1`.

### Match

Bit DP (see the memo). The recurrence is `dp[i] = dp[i >> 1] + (i & 1)`. The equivalent `dp[i] = dp[i & (i - 1)] + 1` (clear the lowest set bit, add one) is worth naming as a second valid recurrence.

### Plan

1. Allocate `dp = [0] * (n + 1)`; `dp[0] = 0` holds by initialization.
2. For `i` from `1` to `n`: `dp[i] = dp[i >> 1] + (i & 1)`. The dependency `i >> 1 < i` is always satisfied.
3. Return `dp`.

### Implement

```python
from typing import List


def count_bits(n: int) -> List[int]:
    """Return [popcount(0), ..., popcount(n)] in O(n) time via dp[i] = dp[i >> 1] + (i & 1)."""
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp
```

### Review

Trace `n = 5`:

```
i=1: dp[0] + (1&1) = 0 + 1 = 1
i=2: dp[1] + (2&1) = 1 + 0 = 1
i=3: dp[1] + (3&1) = 1 + 1 = 2
i=4: dp[2] + (4&1) = 1 + 0 = 1
i=5: dp[2] + (5&1) = 1 + 1 = 2
-> [0, 1, 1, 2, 1, 2]   ✓
```

Edge case `n = 0`: the loop does not run; `dp = [0]` ✓.

### Evaluate

- **Time:** `O(n)` — one pass, `O(1)` per index; `dp[i >> 1]` is always a previously-filled cell.
- **Space:** `O(n)` for the required output; no auxiliary state.
- **Trade vs naive popcount:** the comprehension is correct but `O(n log n)`; the recurrence is the `O(n)` answer. Naming both is the move.

---

## Solution 3 — Maximum XOR of Two Numbers in an Array (LC 421)

### 30-second pattern-recognition memo

> *Binary trie — the bridge between bits and tries. I insert every number MSB-first as a 32-bit path into a 2-character (`0`/`1`) trie. Then for each number I greedily walk the trie, preferring the child for the OPPOSITE bit at every level (because `bit ^ opposite == 1` contributes a `1` to that position of the XOR), falling back to the same-bit child if the opposite is absent. Time `O(n · 32)`, space `O(n · 32)`. The `O(n**2)` brute force over all pairs is too slow for `n` up to `2 * 10**5`.*

### Understand

Maximize `nums[i] ^ nums[j]` over all pairs. Brute force is `O(n**2)` — for `n = 2 * 10**5`, that is `4 * 10**10`, too slow. The structural insight: to maximize an XOR, you want the highest bits of the result to be `1`, and high bits dominate magnitude — so commit to high bits first. Hand-walk the LC 421 example `[3, 10, 5, 25, 2, 8]`: the max is `5 ^ 25 = 28`.

### Match

Binary trie (see the memo). Insert MSB-first so the greedy top-down walk can commit high bits before low ones. The alternative is the `O(n**2)` brute force; reject it on the constraints.

### Plan

1. Build the trie: for each `num`, descend bits `31..0`, creating children with `setdefault`.
2. For each `num`, walk the trie from the MSB: compute `want = 1 - bit`; if `want in node`, that position contributes a `1` to the running XOR (`current |= 1 << bit_pos`) and descend into `want`; otherwise descend into `bit` (forced same bit, contributes `0`).
3. Track the running max.

### Implement

```python
from typing import Any, Dict, List

HIGH_BIT = 31  # non-negative 32-bit integers occupy bits 31..0


def find_maximum_xor(nums: List[int]) -> int:
    """Maximum nums[i] ^ nums[j] via a binary trie. Time O(n * 32), space O(n * 32)."""
    root: Dict[int, Any] = {}

    for num in nums:                                  # insert MSB-first
        node = root
        for bit_pos in range(HIGH_BIT, -1, -1):
            bit = (num >> bit_pos) & 1
            node = node.setdefault(bit, {})

    best = 0
    for num in nums:                                  # greedy opposite-bit walk
        node = root
        current = 0
        for bit_pos in range(HIGH_BIT, -1, -1):
            bit = (num >> bit_pos) & 1
            want = 1 - bit
            if want in node:                          # differing bit available
                current |= (1 << bit_pos)
                node = node[want]
            else:                                     # forced to match
                node = node[bit]
        best = max(best, current)
    return best
```

### Review

The two discriminating bugs:

- **Inserting LSB-first instead of MSB-first.** If you descend `range(0, 32)` instead of `range(31, -1, -1)`, the greedy walk commits low bits first and silently returns the wrong answer. The trie still builds; the walk just maximizes the wrong end.
- **Forgetting the same-bit fallback.** If `want not in node` you *must* descend into `bit` — the number you are pairing against shares that bit. Dropping the `else` branch crashes (the node has no `want` child) or, worse, follows a path that does not exist in the trie.

Trace the shape on `[3, 10, 5, 25, 2, 8]`: walking `5 = 0b…00101` against a trie containing `25 = 0b…11001`, the greedy walk reaches for the opposite of each of `5`'s high bits and finds `25`'s bits there, building `0b11100 = 28`. Single-element `[0]`: the only pairing is `0 ^ 0 = 0` ✓.

### Evaluate

- **Time:** `O(n · 32)` — `n` insertions of 32 bits each, then `n` walks of 32 steps each. With a constant bit width this is `O(n)`.
- **Space:** `O(n · 32)` for the trie (at most 32 nodes per inserted number; prefix sharing makes it less in practice).
- **Trade vs brute force:** `O(n**2)` is correct but times out for large `n`; the trie is the intended answer. **Compare to the XOR-fold exercise** — Single Number uses XOR's *algebra* (cancellation); Maximum XOR uses XOR's *structure* (high bits dominate), which is why it needs a data structure (the trie) rather than a one-line fold. Naming that contrast is the senior signal: same operator, two completely different problem shapes.

---

## How to use these solutions

Read them only after your own attempts. The point of UMPIRE is the *recognition rep* — looking at a problem and saying "XOR fold" or "binary trie" and stating the time bound before writing a line. If you read this file first, you skip the rep, and Mock #3 will catch you.

For the mini-project, model the XOR-trick write-up on Solution 1 and the binary-trie write-up on Solution 3. The Match section is the discriminating part — name the sub-shape, state the bound, reject the alternative. The Implement section is second-most-discriminating — the code should match the structure here, not merely produce the right output.

Once all three exercises are committed and recorded, move to [Challenge 1 — the Mock #3 timed round](../challenges/challenge-01-mock-3-timed-round.md).
