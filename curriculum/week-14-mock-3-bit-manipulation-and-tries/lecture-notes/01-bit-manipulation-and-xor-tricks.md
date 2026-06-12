# Lecture 1 — Bit Manipulation and XOR Tricks

> **Duration:** ~2 hours.
> **Outcome:** You can recognize a bit-manipulation problem in 30 seconds by its tells (constant extra space plus duplicates, the single odd-count element, toggle/count/isolate bits), recite the three XOR identities, derive single-number / missing-number / two-single-numbers from them, and wield the five-move bit-twiddling vocabulary without hesitation.

The course is nearly complete. Weeks 1 through 13 installed the heavy patterns — pointers, hashing, search, graphs, dynamic programming, backtracking. This week installs the **long tail**: two narrow but high-yield pattern families that the previous weeks left out. This lecture covers the first — **bit manipulation** — and Lecture 2 covers bitmasks, bitmask DP, and tries-at-speed. Lecture 3 is the Mock #3 protocol.

Bit manipulation is not where most interviews are won. But it is where a *small number* of interviews are lost: a candidate who has never seen XOR-cancellation will flail on single-number — a problem that is trivial once you know the trick and nearly impossible to invent on the spot if you do not. The entire pattern is **memorization-of-a-small-vocabulary plus recognition**. Three XOR identities, five bit-twiddling moves, and the recognition of which problems they unlock. That is the whole lecture.

By the end of this lecture you should be able to read a bit problem and, within 30 seconds, say two things out loud: "**this is bit manipulation because [constant space + duplicates / single odd-count element / subset of a small set / toggle a flag]**," and "**the move is [XOR the array / isolate a bit with `x & -x` / clear the low bit with `x & (x - 1)`]**."

---

## 1. The tells — recognizing a bit-manipulation problem

Bit problems hide behind surface forms, but the tells are tight. Scan for these:

1. **"Using only constant extra space"** combined with **"every element appears twice except one"** (or "appears an odd number of times"). This is the loudest tell in the entire pattern family. The `O(1)`-space constraint rules out a hash map; the duplicate structure invites XOR-cancellation. Single number (LC 136) is the canonical example.
2. **"A number is missing from the range `0..n`."** The complete-range structure invites XOR-of-indices-and-values or the Gauss sum. Missing number (LC 268).
3. **"Consider all subsets"** with a small constraint (`n <= 20`). The exponential subset count is feasible only because `n` is tiny; the subset is a bitmask. (Lecture 2.)
4. **"Count the set bits / toggle / round to a power of two / is it a power of two."** Plain bit-twiddling. Counting bits (LC 338), number of 1 bits (LC 191), power of two (LC 231).
5. **"Maximum XOR of any two numbers."** A bitwise trie. (Lecture 2 §6; Challenge 1.)

If none of these fire, the problem is probably not bit manipulation — and the most common Phase-2 error is *over-applying* bit tricks to a problem that is cleaner with a hash map or a sort. The negative-space recognition ("this is *not* a bit problem") is graded in the quiz.

---

## 2. The number-as-bits mental model

An integer is a sequence of bits, each with a place value that is a power of two. `13` in binary is `1101`:

```
  bit index:   3   2   1   0
  place value: 8   4   2   1
  13 =         1   1   0   1   =  8 + 4 + 0 + 1
```

The `i`-th bit of `x` has place value `2^i` and is tested with `x & (1 << i)`. In Python:

```python
>>> bin(13)
'0b1101'
>>> 13 & (1 << 0)   # bit 0 set?
1
>>> 13 & (1 << 1)   # bit 1 set?
0
>>> 13 >> 2         # drop the low two bits
3
>>> 13 | (1 << 1)   # set bit 1
15
```

**Python integers are arbitrary-precision.** There is no 32-bit or 64-bit overflow. The bitwise operators work as if on an infinitely long two's-complement representation, which means negative numbers have a conceptually infinite run of leading `1`s and `~x == -x - 1`. For interview problems you almost always work with **non-negative integers and a fixed bit width** (usually 32), which sidesteps the sign subtleties entirely. When a problem does involve negatives or a fixed width, mask with `& 0xFFFFFFFF` to simulate 32-bit wraparound — but that is rare in the Week-14 surface.

---

## 3. The three XOR identities

Every XOR trick rests on exactly three facts. Memorize them; they are the whole foundation.

1. **Self-cancellation:** `x ^ x = 0`. Any value XORed with itself vanishes.
2. **Identity element:** `x ^ 0 = x`. Zero is the XOR identity.
3. **Commutative and associative:** `a ^ b == b ^ a` and `(a ^ b) ^ c == a ^ (b ^ c)`. Order does not matter; you may XOR an entire array in any order and get the same result.

The XOR truth table, for reference:

```
  a   b   a ^ b
  0   0     0
  0   1     1
  1   0     1
  1   1     0
```

XOR yields `1` exactly where the two bits differ. "Exclusive or": one or the other, but not both.

The consequence of the three identities, stated as a single sentence you will repeat in every XOR Match: **"XOR an entire collection; because XOR is commutative and associative I can reorder freely, paired values self-cancel to zero, and zero is the identity, so the survivors are exactly the unpaired values."** That sentence *is* the XOR pattern. The specific problem only changes what counts as "paired."

---

## 4. Single number (LC 136) — the XOR-cancellation warm-up

> *Given a non-empty array of integers `nums`, every element appears twice except for one. Find that single one. You must implement a solution with linear runtime complexity and use only constant extra space.*

**Match.** The tells fire immediately: "constant extra space" (rules out a hash map / set) plus "every element appears twice except one" (the duplicate structure). XOR-cancellation. The 30-second memo:

> *Constant-space duplicate problem. XOR every element. By commutativity/associativity I reorder so each duplicated pair sits together; each pair self-cancels (`x ^ x = 0`); the lone element survives (`x ^ 0 = x`). O(n) time, O(1) space. Why not a hash map: that is O(n) space and the constraint forbids it. Why not a sort: O(n log n) and mutates the input.*

**The derivation.** On `nums = [4, 1, 2, 1, 2]`:

```
4 ^ 1 ^ 2 ^ 1 ^ 2
= 4 ^ (1 ^ 1) ^ (2 ^ 2)     (reorder by commutativity/associativity)
= 4 ^ 0 ^ 0                  (self-cancellation)
= 4                          (identity)
```

The survivor is `4`. The reordering step is conceptual — the code XORs in array order, and the identities guarantee the array order produces the same result as the grouped order.

**Implementation.**

```python
from __future__ import annotations

from functools import reduce
from operator import xor
from typing import List


def single_number(nums: List[int]) -> int:
    """Return the element that appears exactly once; all others appear twice."""
    result = 0
    for num in nums:
        result ^= num
    return result
```

Six lines. The one-liner `return reduce(xor, nums, 0)` is equivalent and idiomatic; the explicit loop is clearer to narrate in an interview. The `result = 0` initialization is the identity element — XORing the first number into `0` yields the number itself.

**Defense.** "Single number is XOR-cancellation. Initialize an accumulator to `0` (the XOR identity), XOR every element in, and the paired elements cancel, leaving the unique one. `O(n)` time, `O(1)` space. The constant-space constraint is the tell that rules out the hash-map solution."

---

## 5. Missing number (LC 268) — two solutions, one tell

> *Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.*

There are `n + 1` slots (`0` through `n`) and `n` numbers, so exactly one is missing. Two solutions; both are interview-acceptable, and naming the trade between them is the senior move.

**Solution A — the Gauss sum.** The sum of `0..n` is `n(n+1)/2`. Subtract the actual array sum; the difference is the missing number.

```python
from __future__ import annotations

from typing import List


def missing_number_sum(nums: List[int]) -> int:
    """Missing number via the Gauss sum of 0..n minus the array sum."""
    n = len(nums)
    expected = n * (n + 1) // 2
    return expected - sum(nums)
```

**Solution B — XOR of indices and values.** XOR all the indices `0..n` together with all the values. Every value that *is* present cancels against its matching index; the missing number's index has no value to cancel it, so it survives.

```python
from __future__ import annotations

from typing import List


def missing_number_xor(nums: List[int]) -> int:
    """Missing number via XOR of all indices 0..n and all values."""
    result = len(nums)  # start with index n (the highest index, absent from range(len))
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result
```

**The trade.** Both are `O(n)` time, `O(1)` space. The Gauss-sum form is shorter and more obvious. The XOR form's selling point is that it **never overflows** — in a fixed-width language, `n(n+1)/2` for large `n` can exceed the integer range, while XOR stays within the word. In Python the overflow point is moot (arbitrary-precision ints), so the Gauss sum is perfectly safe — but the interview tell is *naming* the overflow consideration, which signals you have thought about the fixed-width case. Deliver: "the sum form is cleaner; the XOR form is the overflow-safe variant if we were in a fixed-width language."

---

## 6. Two single numbers (LC 260) — the partition-by-a-bit move

> *Given an integer array `nums` in which exactly two elements appear only once and all the other elements appear exactly twice, find the two elements that appear only once.*

This is the escalation of single-number, and it introduces the **partition-by-a-distinguishing-bit** move — the most reusable bit trick in the lecture.

**Match.** XOR the whole array. The duplicates cancel, leaving `a ^ b`, where `a` and `b` are the two unique numbers. But `a ^ b` is not directly `a` or `b` — it is their XOR. The problem: how to *separate* them?

**The key insight.** Since `a != b`, their XOR `a ^ b` has at least one set bit — a bit position where `a` and `b` differ. Pick any such bit. That bit partitions the entire array into two groups: numbers with that bit set, and numbers with that bit clear. Crucially, `a` and `b` fall into *different* groups (they differ at exactly that bit). Every duplicated pair falls into the *same* group (both copies have the same bits). So XORing each group independently recovers one unique number per group.

**Isolating a distinguishing bit.** `x & -x` isolates the lowest set bit of `x`. (`-x` in two's complement is `~x + 1`, which flips all bits above the lowest set bit and leaves the lowest set bit; the AND keeps only that bit.) So `diff & -diff` gives a mask with exactly one bit — a bit where `a` and `b` differ.

**Implementation.**

```python
from __future__ import annotations

from typing import List


def single_number_iii(nums: List[int]) -> List[int]:
    """Return the two elements that each appear once; all others appear twice."""
    # Step 1: XOR everything -> a ^ b (duplicates cancel).
    xor_all = 0
    for num in nums:
        xor_all ^= num

    # Step 2: isolate one bit where a and b differ.
    diff_bit = xor_all & -xor_all

    # Step 3: partition by that bit; XOR each group independently.
    a = 0
    for num in nums:
        if num & diff_bit:
            a ^= num
    b = xor_all ^ a  # the other unique number
    return [a, b]
```

Sixteen lines. Step 3's final line uses a shortcut: rather than XOR the second group separately, `b = xor_all ^ a` recovers `b` because `xor_all == a ^ b`, so `xor_all ^ a == b`.

**Trace on `nums = [1, 2, 1, 3, 2, 5]`:**

```
Step 1: 1^2^1^3^2^5 = 3^5 = 6 (binary 110). So a^b = 6.
Step 2: diff_bit = 6 & -6 = 2 (binary 010). a and b differ at bit 1.
Step 3: numbers with bit 1 set: 2, 3, 2 -> XOR = 3. So a = 3.
        b = 6 ^ 3 = 5.
Answer: [3, 5].
```

**Defense.** "Two single numbers is XOR-cancellation plus a partition. XOR everything to get `a ^ b`. Since `a != b`, that XOR has a set bit where they differ; isolate it with `x & -x`. Partition the array by that bit — `a` and `b` land in different groups, every duplicate pair lands in the same group — and XOR each group to recover one unique number per group. `O(n)` time, `O(1)` space."

---

## 7. The five-move bit-twiddling vocabulary

Beyond XOR, five moves cover ~90% of bit problems. Memorize all five.

| Move | Expression | What it does | Where it shows up |
|------|-----------|--------------|-------------------|
| Test the low bit | `x & 1` | `1` if `x` is odd | parity checks, counting-bits |
| Shift right | `x >> 1` | integer-divide by 2; drop low bit | counting-bits, base conversion |
| The `k`-th bit mask | `1 << k` | integer with only bit `k` set | bitmask set operations |
| Clear lowest set bit | `x & (x - 1)` | turn off the rightmost `1` | popcount, power-of-two test |
| Isolate lowest set bit | `x & -x` | keep only the rightmost `1` | partition-by-a-bit, Fenwick trees |

**Two derived idioms.**

1. **Popcount via clear-lowest-bit (Kernighan's algorithm):**

   ```python
   def popcount(x: int) -> int:
       """Number of set bits, via repeated clear-lowest-bit."""
       count = 0
       while x:
           x &= x - 1   # clear the lowest set bit
           count += 1
       return count
   ```

   Each iteration removes exactly one set bit, so the loop runs `popcount(x)` times — better than checking all 32 bits when `x` is sparse. (In practice, just call `x.bit_count()` on Python 3.10+; the manual form is the one to *explain* in an interview.)

2. **Power-of-two test:**

   ```python
   def is_power_of_two(x: int) -> bool:
       """True iff x is a positive power of two."""
       return x > 0 and x & (x - 1) == 0
   ```

   A power of two has exactly one set bit; clearing it yields zero. The `x > 0` guard handles `x = 0` (zero is not a power of two but `0 & -1 == 0` would falsely pass).

---

## 8. Worked example — number of 1 bits by hand on `x = 11`

The trace is the standard lecture-closing exercise for the clear-lowest-bit idiom. `11` is `1011` in binary; it has three set bits.

```
x = 11  (1011)
  iter 1: x &= x - 1  ->  1011 & 1010 = 1010 (10)   count = 1
  iter 2: x &= x - 1  ->  1010 & 1001 = 1000 (8)    count = 2
  iter 3: x &= x - 1  ->  1000 & 0111 = 0000 (0)    count = 3
  x == 0, loop ends.   popcount = 3.
```

Each step removes exactly the lowest remaining `1`. The loop runs three times for three set bits — not the full four bit-positions. That is why Kernighan's algorithm beats the naive "check all 32 bits" approach on sparse inputs.

---

## 9. Closing — bit manipulation as vocabulary plus recognition

Three takeaways:

1. **The pattern is small.** Three XOR identities, five bit-twiddling moves, one partition-by-a-bit technique. Memorize the vocabulary and the recognition becomes the only remaining work. Unlike DP — where the *process* is the skill — bit manipulation is *vocabulary* first.
2. **The tells are tight.** "Constant space + duplicates" is the loudest tell in the course. When you see it, reach for XOR before anything else.
3. **Over-application is the failure mode.** The most common Phase-2 error is forcing a bit trick onto a problem that a hash map solves more cleanly. The negative-space recognition — "this looks bit-flavored but a `Counter` is simpler" — is the senior move, and it is graded in the quiz.

Lecture 2 takes the vocabulary into two-dimensional territory: bitmasks (a subset of a small universe in one integer), bitmask DP, and the counting-bits 1D DP. Then it pivots to tries-at-speed and the bitwise trie — the bridge that connects this week's two pattern families.

[Back to the README](../README.md). On to [Lecture 2 — Bitmasks, Bitmask DP, and Tries at Speed](./02-bitmasks-bitmask-dp-and-tries-at-speed.md).
