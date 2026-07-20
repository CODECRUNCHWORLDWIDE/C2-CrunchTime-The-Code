# Week 14 — Resources

Every resource is **free** and **publicly accessible** unless marked as a book.

## Required reading (work it into your week)

- **Python docs — "Bitwise operations on integer types"**: <https://docs.python.org/3/reference/expressions.html#binary-bitwise-operations> — the canonical reference for `& | ^ ~ << >>` in Python. Reread if any operator's precedence or behavior on negative ints feels uncertain.
- **Python docs — `int.bit_count()`**: <https://docs.python.org/3/library/stdtypes.html#int.bit_count> — the one-line popcount, available in Python 3.10+. This is the answer you say *first* in an interview for Number of 1 Bits (LC 191).
- **Sean Eron Anderson — "Bit Twiddling Hacks"**: <https://graphics.stanford.edu/~seander/bithacks.html> — the open-web reference for bit idioms. Read the "Counting bits set," "Compute the lowest set bit," and "Reverse the bits" sections this week; they back Lecture 1 §4–§5 and homework problems 2–3.
- **LeetCode — Bit Manipulation tag**: <https://leetcode.com/tag/bit-manipulation/> — skim 20 titles and predict the sub-shape for each in 5 seconds. The Match-step muscle for the curveball pattern.
- **LeetCode — Trie tag**: <https://leetcode.com/tag/trie/> — re-skim five titles to re-activate the Week 9 recognition before the binary-trie exercise.
- **PEP 8 (recurring)**: <https://peps.python.org/pep-0008/>
- **Big-O Cheat Sheet (recurring)**: <https://www.bigocheatsheet.com/>

## Books (the canonical references)

- **"Hacker's Delight" by Henry S. Warren Jr.** — the canonical bit-manipulation book. Every idiom in Lecture 1 is in here with a proof. Not free, but the single best reference if bit manipulation becomes a focus. Chapters 2 ("Basics") and 5 ("Counting Bits") map directly to this week.
- **"Cracking the Coding Interview" by Gayle Laakmann McDowell** — the "Bit Manipulation" chapter is a tight, interview-focused tour of exactly the operators and tricks this week covers. The clearest book treatment for an interview audience.
- **"Competitive Programmer's Handbook" by Antti Laaksonen** (free PDF): <https://cses.fi/book/book.pdf> — the "Bit manipulation" and "Bitmask DP" chapters are the cleanest free treatment of subset-state DP. Read the bitmask-DP chapter as a Phase-4 stretch (recognition-grade, per Lecture 2 §4).

## Free practice platforms and specific problems

- **LeetCode — Single Number** (LC 136): <https://leetcode.com/problems/single-number/> — the canonical XOR fold; Exercise 1 exactly.
- **LeetCode — Single Number II** (LC 137): <https://leetcode.com/problems/single-number-ii/> — the "appears three times except one" variant; homework problem 1.
- **LeetCode — Single Number III** (LC 260): <https://leetcode.com/problems/single-number-iii/> — two singletons, partition on a differing bit; Lecture 1 §9.
- **LeetCode — Number of 1 Bits** (LC 191): <https://leetcode.com/problems/number-of-1-bits/> — popcount; homework problem 2.
- **LeetCode — Counting Bits** (LC 338): <https://leetcode.com/problems/counting-bits/> — the bit-DP recurrence; Exercise 2 exactly.
- **LeetCode — Sum of Two Integers** (LC 371): <https://leetcode.com/problems/sum-of-two-integers/> — add without `+`; the 32-bit masking subtlety; Challenge 2.
- **LeetCode — Maximum XOR of Two Numbers in an Array** (LC 421): <https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/> — the binary trie; Exercise 3 and the topic bridge.
- **LeetCode — Subsets** (LC 78): <https://leetcode.com/problems/subsets/> — bitmask enumeration; Lecture 2 §2 and homework problem 5.
- **LeetCode — Bitwise AND of Numbers Range** (LC 201): <https://leetcode.com/problems/bitwise-and-of-numbers-range/> — common-prefix observation; homework problem 4.
- **LeetCode — Reverse Bits** (LC 190): <https://leetcode.com/problems/reverse-bits/> — bit-layout; homework problem 3.
- **LeetCode — Missing Number** (LC 268): <https://leetcode.com/problems/missing-number/> — XOR fold or Gauss sum; homework problem 6.
- **LeetCode — Implement Trie (Prefix Tree)** (LC 208): <https://leetcode.com/problems/implement-trie-prefix-tree/> — the Week 9 character trie, for the tries review.

## Mock-interview platforms

- **interviewing.io** (free blog + paid mocks): <https://interviewing.io/blog> — the "lessons from thousands of mock interviews" posts are the best free writing on what interviewers actually grade. Read two before Friday. The platform itself matches you with engineers for Flavor B mocks.
- **Pramp** — peer-to-peer mock matching; free. Book 24+ hours ahead. Flavor B alternative.

## On the pattern itself

Bit manipulation is pattern #13 of the fourteen-pattern catalog. Its surface forms map to four sub-shapes plus a "not a bit problem" rejection:

- **XOR fold** — "every element appears twice (or `k` times) except one"; "find the missing / duplicated number with `O(1)` space." Reduce by `^`; pairs cancel. Single Number (LC 136), Missing Number (LC 268), Single Number III (LC 260, with a partition twist).
- **Bitmask-as-set / subset enumeration** — "consider every subset / assignment / combination of `n` items," with `n` small (≤ ~20). Loop `mask` over `range(1 << n)`; bit `i` is membership. Subsets (LC 78).
- **Bit DP** — "build entry `i` from a smaller entry in `O(1)`," or "state is which subset of items I have used." Counting Bits (LC 338); bitmask DP (TSP, assignment) at the recognition level.
- **Binary trie** — "maximize / query an XOR over a set of integers." Insert MSB-first into a `0`/`1` trie; greedy bit walk. Maximum XOR (LC 421). This is the bridge between bit manipulation and the Week 9 trie family.
- **NOT a bit problem** — duplicate detection (`set`), anagram (counting), arithmetic where `+` is allowed (just add). If there is no cancellation, no subset, no smaller-subproblem recurrence, and no XOR query — it is not a bit problem. Recognizing the rejection is half the skill.

If a prompt mentions "appears twice except one," "constant extra space," "count the set bits," "all subsets with small `n`," or "maximize the XOR" — it is almost certainly a bit problem. If it mentions "any duplicate," "anagram," or plain "sum these numbers" — it is not.

## On the bit idioms specifically

The operations you should know cold.

| Operation | Code | Complexity | Mnemonic |
|-----------|------|-----------:|----------|
| Test bit `i` | `(x >> i) & 1` | `O(1)` | shift down, mask off |
| Set bit `i` | `x \| (1 << i)` | `O(1)` | OR forces 1 |
| Clear bit `i` | `x & ~(1 << i)` | `O(1)` | AND inverted mask |
| Toggle bit `i` | `x ^ (1 << i)` | `O(1)` | XOR flips |
| Isolate lowest set bit | `x & -x` | `O(1)` | negation flips above the low bit |
| Clear lowest set bit | `x & (x - 1)` | `O(1)` | Kernighan step |
| Popcount | `x.bit_count()` | `O(1)`* | Python 3.10+ |
| Full mask of width `n` | `(1 << n) - 1` | `O(1)` | the universe / all-ones |

\* `O(1)` for fixed-width ints; `O(bits)` for arbitrary-precision.

### The four XOR identities

```
a ^ a == 0       (self-cancellation — pairs vanish)
a ^ 0 == a       (identity — survivor remains)
a ^ b == b ^ a   (commutativity — order irrelevant)
(a ^ b) ^ c == a ^ (b ^ c)   (associativity — grouping irrelevant)
```

Together: folding a multiset by `^` returns the XOR of exactly the odd-occurrence values. This is the engine of the entire XOR-fold sub-family.

### The binary trie (the bridge)

```python
from typing import Any, Dict, List

HIGH_BIT = 31


def find_maximum_xor(nums: List[int]) -> int:
    """Maximum nums[i] ^ nums[j] via a binary trie. O(n * 32)."""
    root: Dict[int, Any] = {}
    for num in nums:                                  # insert MSB-first
        node = root
        for bit_pos in range(HIGH_BIT, -1, -1):
            node = node.setdefault((num >> bit_pos) & 1, {})
    best = 0
    for num in nums:                                  # greedy opposite-bit walk
        node = root
        current = 0
        for bit_pos in range(HIGH_BIT, -1, -1):
            bit = (num >> bit_pos) & 1
            want = 1 - bit
            if want in node:
                current |= (1 << bit_pos)
                node = node[want]
            else:
                node = node[bit]
        best = max(best, current)
    return best
```

Twenty-five lines. Memorize the two phases: MSB-first insertion, then the opposite-bit greedy walk. It is the same dict-of-dict trie from Week 9, restricted to the alphabet `{0, 1}`.

## Glossary additions

| Term | Definition |
|------|-----------|
| **Bit `i`** | The bit of value `2**i`; bit 0 is the lowest / rightmost |
| **Mask** | An integer used with `&` / `\|` / `^` to select, set, or flip specific bits |
| **Two's complement** | The standard signed-integer representation; negate by flipping all bits and adding one |
| **XOR fold** | Reducing a sequence by `^`; pairs cancel, the odd-occurrence value(s) survive |
| **Popcount / Hamming weight** | The number of set bits in an integer |
| **Brian Kernighan's algorithm** | Popcount via `while x: x &= x - 1; count += 1`; one iteration per set bit |
| **Lowest set bit** | `x & -x` isolates it; `x & (x - 1)` clears it |
| **Bitmask** | An integer read as a subset of `{0, …, n-1}`: bit `i` set means item `i` is in the set |
| **Subset enumeration** | Looping `mask` over `range(1 << n)` to visit every subset |
| **Submask** | A subset of the bits of a mask `m`; iterated via `(sub - 1) & m` |
| **Bit DP** | DP where each entry is built from a strictly smaller one in `O(1)`, or where the state is a subset (bitmask) |
| **Bitmask DP** | DP whose state is a subset encoded as a bitmask (TSP, assignment); recognition-grade at entry level |
| **Binary trie** | A trie over the alphabet `{0, 1}` storing integers MSB-first; the structure behind Maximum XOR |
| **Greedy opposite-bit walk** | Walking a binary trie preferring the opposite bit at each level to maximize a running XOR |
| **Sum-without-carry** | `a ^ b`; per-bit addition mod 2 |
| **Carry** | `(a & b) << 1`; generated where both bits are 1, propagated one position up |

## What you will be glad you read

Three things, all short, all this week:

1. **The Python docs "Bitwise operations" page** — about 10 minutes. The authoritative behavior of every operator, including on negative (unbounded) ints — which is exactly the subtlety behind Sum of Two Integers (LC 371).
2. **The "Bit Twiddling Hacks" sections on counting and isolating bits** — about 15 minutes. Where `x & -x` and `x & (x - 1)` stop being incantations.
3. **Two interviewing.io blog posts on mock interviews** — about 20 minutes. Read them *before* Friday's Mock #3, not after.

If you read nothing else this week, read those three and skim five titles in the LeetCode Bit Manipulation tag — then run Mock #3.

---

*Broken link? Open an issue.*
