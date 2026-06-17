# Week 14 — Resources

Every resource is **free** and **publicly accessible**.

## Required reading (work it into your week)

- **Python `int` bitwise operations — Python docs**: <https://docs.python.org/3/library/stdtypes.html#bitwise-operations-on-integer-types> — the authoritative reference for `&`, `|`, `^`, `~`, `<<`, `>>` on Python's arbitrary-precision integers. The single most important detail for interviews: Python ints never overflow, so the integer-sum form of "missing number" is safe in Python (the overflow risk that motivates the XOR form is a fixed-width-language concern; naming it is the interview tell).
- **`int.bit_count()` — Python docs**: <https://docs.python.org/3/library/stdtypes.html#int.bit_count> — added in Python 3.10. Returns the number of set bits (the popcount). The portable fallback is `bin(x).count("1")`. Know both; the interview environment may be on 3.9 or earlier.
- **Bit Twiddling Hacks (Sean Eron Anderson, Stanford)**: <https://graphics.stanford.edu/~seander/bithacks.html> — the canonical catalogue of bit tricks. Read "Counting bits set," "Determine if an integer is a power of 2," and "Compute the lexicographically next bit permutation" once. You will not memorize it; the point is to recognize the shapes when an interview reaches for one.
- **Trie — Wikipedia**: <https://en.wikipedia.org/wiki/Trie> — the canonical written description of the prefix tree. Re-skim the "Operations" section; the Week-9 install covered this, and Week 14 assumes it.
- **XOR (exclusive or) — Wikipedia**: <https://en.wikipedia.org/wiki/Exclusive_or> — the "Properties" section is the canonical statement of the three identities (`x ^ x = 0`, `x ^ 0 = x`, commutativity, associativity) that every XOR trick rests on.
- **PEP 8 (recurring)**: <https://peps.python.org/pep-0008/>
- **Big-O Cheat Sheet (recurring)**: <https://www.bigocheatsheet.com/>

## On the patterns themselves

Both pattern families this week hide behind surface forms. The recognition skill is mapping the surface form to the underlying technique.

### Bit manipulation

- **"... using only constant extra space ..."** plus **"... every element appears twice except one ..."** — XOR-cancellation. XOR the whole array; pairs cancel; the survivor is the answer. Examples: single number (LC 136), single number III (LC 260).
- **"... a number is missing from `0..n` ..."** — XOR-of-indices-and-values, or the Gauss sum. Example: missing number (LC 268).
- **"... given `n <= 20`, consider all subsets ..."** — bitmask-as-set or bitmask-DP. The small `n` and the "all subsets" phrasing are the joint tell. Examples: partition to K equal-sum subsets (LC 698), shortest path visiting all nodes (LC 847).
- **"... count the set bits / toggle / round to a power of two ..."** — plain bit-twiddling. Examples: counting bits (LC 338), number of 1 bits (LC 191), power of two (LC 231).
- **"... maximum XOR of any two numbers ..."** — bitwise trie. The XOR-maximization-over-pairs phrasing is the tell. Example: maximum XOR (LC 421).

### Tries

- **"... starts with / has prefix / autocomplete ..."** — trie. The prefix question is the discriminator from a hash set. Example: implement trie (LC 208).
- **"... search a word where `.` matches any character ..."** — trie with a wildcard branching walk. Example: add and search word (LC 211).
- **"... longest word built one character at a time / replace words by root ..."** — trie traversal. Examples: longest word in dictionary (LC 720), replace words (LC 648).
- **"... maximum XOR / find the number that XORs largest ..."** — *bitwise* trie (a trie over the binary representation, not over characters). Example: maximum XOR (LC 421). This is the bridge between the two pattern families this week.

If a prompt forbids extra space and mentions duplicates or a single odd-count element — XOR. If it has a small universe (`n <= 20`) and asks about subsets — bitmask. If it asks a prefix question — trie. If it asks for maximum XOR over pairs — bitwise trie. If none of these — it is probably not a Week-14 problem.

## Free practice platforms

- **LeetCode — Bit Manipulation tag** (free): <https://leetcode.com/tag/bit-manipulation/>
- **LeetCode — Trie tag** (free): <https://leetcode.com/tag/trie/>
- **LeetCode — Single Number** (LC 136): <https://leetcode.com/problems/single-number/> — the XOR-cancellation warm-up; Exercise 1 exactly.
- **LeetCode — Implement Trie (Prefix Tree)** (LC 208): <https://leetcode.com/problems/implement-trie-prefix-tree/> — the trie-at-speed rep; Exercise 2 exactly.
- **LeetCode — Counting Bits** (LC 338): <https://leetcode.com/problems/counting-bits/> — the 1D DP over bits; Exercise 3 exactly.
- **LeetCode — Maximum XOR of Two Numbers in an Array** (LC 421): <https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/> — the bitwise trie; Challenge 1.
- **LeetCode — Partition to K Equal Sum Subsets** (LC 698): <https://leetcode.com/problems/partition-to-k-equal-sum-subsets/> — the bitmask DP; Challenge 2.
- **LeetCode — Single Number III** (LC 260): <https://leetcode.com/problems/single-number-iii/> — the two-single-numbers partition; homework.
- **LeetCode — Missing Number** (LC 268): <https://leetcode.com/problems/missing-number/> — XOR-of-indices or Gauss sum; homework.
- **LeetCode — Number of 1 Bits** (LC 191): <https://leetcode.com/problems/number-of-1-bits/> — popcount with `x & (x - 1)`; homework.
- **LeetCode — Add and Search Word** (LC 211): <https://leetcode.com/problems/design-add-and-search-words-data-structure/> — trie with wildcard; homework.
- **Pramp** (free peer mocks): <https://www.pramp.com/> — for Mock #3 Flavor B.
- **interviewing.io** (free tier): <https://interviewing.io/> — for Mock #3 Flavor B.

## On the XOR identities

Every XOR trick rests on exactly three facts. Memorize them; they are the whole foundation.

| Identity | Statement | Consequence |
|----------|-----------|-------------|
| Self-cancellation | `x ^ x = 0` | Any value XORed with itself vanishes; duplicates cancel in pairs. |
| Identity element | `x ^ 0 = x` | Zero is the XOR identity; XORing in a zero changes nothing. |
| Commutative + associative | `a ^ b == b ^ a` and `(a ^ b) ^ c == a ^ (b ^ c)` | Order does not matter; you can XOR an entire array in any order and the result is the same. |

From these three, the single-number derivation is one line:

> XOR every element of `[4, 1, 2, 1, 2]`. By commutativity/associativity, reorder to `(1 ^ 1) ^ (2 ^ 2) ^ 4`. By self-cancellation, `(0) ^ (0) ^ 4`. By identity, `4`. The survivor is the unique element.

That derivation, said aloud, is the Match-step for single-number. Memorize the cadence.

## On the bit-twiddling vocabulary

The five moves that cover ~90% of interview bit problems.

| Move | Expression | What it does |
|------|-----------|--------------|
| Test the low bit | `x & 1` | `1` if `x` is odd (low bit set), else `0`. |
| Shift right | `x >> 1` | Drops the low bit; integer-divides by 2. |
| The `k`-th bit mask | `1 << k` | An integer with only the `k`-th bit set. |
| Clear the lowest set bit | `x & (x - 1)` | Turns off the rightmost `1`. Loop until `0` to count set bits. |
| Isolate the lowest set bit | `x & -x` | Keeps only the rightmost `1`; everything else becomes `0`. |

Two derived idioms worth knowing:

1. **Popcount via clear-lowest-bit:** `count = 0; while x: x &= x - 1; count += 1`. Each iteration removes exactly one set bit, so the loop runs `popcount(x)` times — faster than checking all 32 bits when `x` is sparse. (Or just call `x.bit_count()`.)
2. **Power-of-two test:** `x > 0 and x & (x - 1) == 0`. A power of two has exactly one set bit, so clearing it yields zero.

## On bitmasks and bitmask DP

The shape you should be able to walk in your head when `n <= 20` and the prompt mentions subsets.

| Operation | Expression | Cost |
|-----------|-----------|-----:|
| Empty set | `0` | `O(1)` |
| Full set on `n` elements | `(1 << n) - 1` | `O(1)` |
| Is element `i` in the set? | `mask & (1 << i)` | `O(1)` |
| Add element `i` | `mask | (1 << i)` | `O(1)` |
| Remove element `i` | `mask & ~(1 << i)` | `O(1)` |
| Set size (popcount) | `mask.bit_count()` | `O(1)` |
| Iterate all submasks of `mask` | `sub = mask; while sub: ...; sub = (sub - 1) & mask` (then handle `0`) | `O(2^popcount(mask))` |

The canonical bitmask-DP shape:

```python
from __future__ import annotations


def bitmask_dp_skeleton(n: int) -> int:
    """Skeleton: dp[mask] = best/count over having committed exactly `mask`."""
    full = (1 << n) - 1
    dp = [0] * (1 << n)
    dp[0] = 1  # base case: the empty set has one way (problem-dependent)
    for mask in range(1 << n):
        for i in range(n):
            if not (mask & (1 << i)):
                # transition: add element i to the set `mask`
                nxt = mask | (1 << i)
                dp[nxt] += dp[mask]  # combine per the problem's recurrence
    return dp[full]
```

Three observations:

1. **The state space is `2^n`; the per-state work is `O(n)`.** Total `O(2^n * n)`. For `n = 20`, that is `2^20 * 20 ≈ 2.1e7` — fast. For `n = 25`, it is `2^25 * 25 ≈ 8.4e8` — borderline. The constraint `n <= 20` (sometimes `n <= 22`) is the recognition cue that bitmask DP is intended.
2. **Iterate masks in increasing order** when the transition adds an element (so `mask < nxt` always, and `dp[mask]` is finalized before it is read into `dp[nxt]`). Iterate in decreasing order for the "remove an element" direction.
3. **`dp[mask]` semantics is "having committed exactly the set `mask`."** Like all DP, name the state in words first. The recurrence is problem-specific (sum for counting, min/max for optimization), but the state shape — "a subset of a small universe" — is the constant.

## The Mock #3 checklist

Run this checklist Monday. Mock #3 is your third recorded interview; the rig should be muscle memory by now, but verify anyway.

- [ ] **Recording tool tested.** A 30-second test recording, played back. Face visible, screen sharp, voice clear, no distracting background noise.
- [ ] **Peer or platform partner locked in.** Mock #3 is **not** solo-eligible (unlike Mock #1). Flavor A (peer) or Flavor B (Pramp / interviewing.io). If you do not have a mock partner by Week 14, message the cohort *Monday* — do not discover on Friday that no one is available.
- [ ] **Coding environment chosen.** CoderPad sandbox or a shared editor. Not your personal IDE; the friction of an interview shell is part of the test.
- [ ] **45-minute calendar block claimed**, Do-Not-Disturb on, phone face down, door closed.
- [ ] **The "no peeking" commitment made in writing.** Mock #3's distinguishing constraint vs. Mock #1 is *near-real conditions* — no looking up solutions mid-solve, no consulting your own notes, no second attempts. Write the commitment in `mocks/mock-03/immediate-notes.md` before the mock as a precommitment device.
- [ ] **The Mock #2 self-feedback note re-read.** Mock #3 should test whether last mock's one-behavior-change actually stuck. Pull up `umpire-writeups/c2-week-09/mock-02-self-feedback.md` and re-read the "ONE behavior change" line.

## Glossary additions

- **Bit** — a single binary digit, `0` or `1`. The `i`-th bit of an integer `x` has place value `2^i` and is tested with `x & (1 << i)`.
- **Bitwise operators** — `&` (AND), `|` (OR), `^` (XOR), `~` (NOT / complement), `<<` (left shift), `>>` (right shift). They act on the binary representations of integers position by position.
- **XOR (exclusive or)** — the bitwise operator that yields `1` where exactly one operand has a `1`. Its three defining identities (`x ^ x = 0`, `x ^ 0 = x`, commutative + associative) are the foundation of XOR-cancellation tricks.
- **XOR-cancellation** — the technique of XORing a collection so that paired (duplicated) values cancel to zero, leaving the unpaired value(s). The basis of single-number (LC 136) and single-number-III (LC 260).
- **Popcount (population count)** — the number of set (`1`) bits in an integer. `x.bit_count()` (Python 3.10+) or `bin(x).count("1")`.
- **Bitmask** — an integer used to represent a subset of a small universe `{0, ..., n-1}`: bit `i` set means element `i` is in the subset. Supports set operations in `O(1)` via bitwise operators.
- **Submask** — a subset of the bits set in a given mask. The submasks of `mask` are enumerated with `sub = (sub - 1) & mask`.
- **Bitmask DP** — a dynamic program whose state is a bitmask (a subset of a small universe). `O(2^n)` states; `n <= 20` is the constraint signal. The state semantics is "having committed exactly the set `mask`."
- **Trie (prefix tree)** — a rooted tree in which every edge is a single character and every root-to-terminal path spells one stored key. Answers prefix queries in `O(P)` where `P` is the prefix length. Installed in Week 9; drilled at speed in Week 14.
- **Bitwise trie** — a trie built over the binary representation of integers (each edge is a `0` or a `1`), used to answer maximum-XOR-over-pairs queries by a greedy opposite-bit walk. The bridge between bit manipulation and tries.
- **Wildcard search** — a trie search where a special character (`.`) matches any single character, forcing a branching walk over all children at that level. The basis of add-and-search-word (LC 211).
- **Near-real mock conditions** — the Mock #3 standard: 45 minutes, video on, uncurated prompt, no peeking at solutions or notes, no second attempts, hard stop at the clock. One step closer to a real onsite than Mock #1's solo-eligible protocol.

## Cheatsheet — the Week-14 recognition flowchart

A short decision flowchart you should be able to walk in 30 seconds.

```
Does the prompt forbid extra space AND mention duplicates / single odd-count element?
  Yes -> XOR-cancellation. XOR the whole collection; pairs cancel.
         (single number LC 136, single number III LC 260)
  No  -> next question.

Does the prompt ask for the maximum XOR of two numbers?
  Yes -> bitwise trie. Insert binary reps; greedy opposite-bit walk. (LC 421)
  No  -> next question.

Does the prompt have a small universe (n <= 20) AND ask about subsets / visiting-all?
  Yes -> bitmask. Represent subsets as integers.
         Optimizing/counting over subsets -> bitmask DP, O(2^n * n). (LC 698, 847)
  No  -> next question.

Does the prompt ask a prefix question (starts-with / autocomplete / wildcard)?
  Yes -> trie. insert / search / starts_with; wildcard -> branching walk. (LC 208, 211)
  No  -> next question.

Does the prompt ask to count / toggle / isolate bits, or test power-of-two?
  Yes -> plain bit-twiddling. x & 1, x >> 1, x & (x - 1), x & -x, 1 << k.
         (counting bits LC 338, number of 1 bits LC 191, power of two LC 231)
  No  -> probably not a Week-14 problem. Re-Match against earlier weeks.
```

Read aloud; should hit 25–30 seconds. The order matters — the questions narrow from the highest-signal tells (constant space + duplicates) to the lowest (generic bit-twiddling).
