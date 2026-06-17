# Week 14 — Homework

Six practice problems plus the rubric. Allow ~4.5 hours total. Do the problems on your own with the lectures *closed*; consult the lecture or the resources only after a 15-minute stuck-period on a single problem.

The problems are chosen to drill the six Week-14 sub-patterns: XOR-cancellation with a twist (triples), XOR-partition, plain bit-twiddling, trie with a wildcard, bitmask DP, and the bitwise trie. By Sunday, the recognition step on each should be reflexive.

**Note on pacing this week:** the homework is lighter than usual (4.5 hours, not 5+) because Mock #3 and its self-feedback are the heavy deliverable. If time is tight, prioritize Problems 1, 2, and 4 (the three most-likely-at-an-onsite shapes) and treat the rest as recognition-only reps.

| # | Problem | Pattern | Source | Est. time |
|---|---------|---------|--------|----------:|
| 1 | Single Number III | XOR-partition (two singletons) | LeetCode 260 | 35 min |
| 2 | Add and Search Word | Trie with '.' wildcard | LeetCode 211 | 50 min |
| 3 | Number of 1 Bits | Plain bit-twiddling (popcount) | LeetCode 191 | 25 min |
| 4 | Single Number II | XOR limit / bit-count mod 3 | LeetCode 137 | 45 min |
| 5 | Sum of Two Integers | Add without `+`, full-adder bits | LeetCode 371 | 40 min |
| 6 | Maximum XOR of Two Numbers | Bitwise trie | LeetCode 421 | 55 min |

Problems 1, 4, and 6 are the high-yield bit drills; problem 2 is the trie-with-wildcard rep; problem 3 is the popcount rep; problem 5 is the full-adder rep that stretches the bit vocabulary.

---

## Problem 1 — Single Number III (LC 260)

**Spec.** Given an array in which exactly two elements appear once and all others appear twice, return the two singletons (any order). Linear time, constant space.

**Constraints.** `2 <= len(nums) <= 3 * 10^4`; `-2^31 <= nums[i] <= 2^31 - 1`.

**Pattern.** XOR-cancellation plus partition-by-a-bit (Lecture 1 §6).

**Hint.** XOR all → `a ^ b`. Isolate one differing bit with `diff = (a ^ b) & -(a ^ b)`. Partition by that bit; XOR each group; recover `a` and `b = (a ^ b) ^ a`.

**Acceptance.** Function signature `single_number_iii(nums: List[int]) -> List[int]`. Time: `O(n)`. Space: `O(1)`. (This is also Mini-Project Problem 1 — drill it here, write it up there.)

**Variant.** A `Counter`-based solution is `O(n)` time but `O(n)` space and forfeits the rep; the constant-space constraint demands the bit approach.

---

## Problem 2 — Add and Search Word (LC 211)

**Spec.** Design a `WordDictionary` with `add_word(word)` and `search(word)`, where `search` may contain `.` matching any single character.

**Constraints.** `1 <= word.length <= 25`; lowercase letters in `add_word`; letters and `.` in `search`; up to `10^4` calls.

**Pattern.** Trie with a wildcard branching walk (Lecture 2 §7).

**Hint.** `add_word` is a plain trie insert. `search` recurses: a normal character descends one child; a `.` recurses into *all* children and ORs the results; end-of-word checks `is_end`.

**Acceptance.** Class `WordDictionary` with `add_word` and `search`. Time: `O(L)` per query without wildcards; up to `O(26^d * L)` with `d` dots. Space: `O(total characters added)`. (This is also Mini-Project Problem 2.)

**Variant.** Bucketing words by length plus a regex match is an alternative but loses the prefix-sharing efficiency; the trie is the right structure.

---

## Problem 3 — Number of 1 Bits (LC 191)

**Spec.** Write a function that takes an unsigned integer and returns the number of `1` bits it has (the Hamming weight / popcount).

**Constraints.** The input is a 32-bit integer.

**Pattern.** Plain bit-twiddling (Lecture 1 §7).

**Hint.** The clear-lowest-bit loop: `count = 0; while x: x &= x - 1; count += 1`. Each iteration removes exactly one set bit, so the loop runs `popcount(x)` times. (Or `x.bit_count()` / `bin(x).count("1")` — but the loop is the one to *explain*.)

**Acceptance.** Function signature `hamming_weight(n: int) -> int`. Time: `O(popcount)` with the Kernighan loop (or `O(1)` fixed-32 with the built-in). Space: `O(1)`.

**Variant.** The naive "check all 32 bits" loop is `O(32)`; the clear-lowest-bit loop is `O(popcount)`, faster on sparse inputs. Name the trade.

---

## Problem 4 — Single Number II (LC 137)

**Spec.** Given an array where every element appears three times except for one which appears once, find the single one. Linear time, constant space.

**Constraints.** `1 <= len(nums) <= 3 * 10^4`; `-2^31 <= nums[i] <= 2^31 - 1`.

**Pattern.** The XOR *limit case* — plain XOR-cancellation works for pairs, not triples (Lecture 1 §3-4, the limits of XOR).

**Hint.** Two approaches. (a) Count, for each of the 32 bit positions, how many numbers have that bit set; take the count modulo 3; the surviving bits form the answer. (b) The two-accumulator state machine: `ones, twos = 0, 0`; for each `num`, `ones = (ones ^ num) & ~twos; twos = (twos ^ num) & ~ones`. The state machine tracks "seen once" and "seen twice" bitwise, resetting at three.

**Acceptance.** Function signature `single_number_ii(nums: List[int]) -> int`. Time: `O(n)` (or `O(32n)` for the bit-count form). Space: `O(1)`.

**Variant.** The bit-count-mod-3 form is easier to derive under pressure; the two-accumulator form is the slick `O(1)`-space-no-32-loop version. Discuss the trade. **The key recognition:** plain `result ^= num` (the LC 136 trick) does *not* work here, because XOR cancels pairs, and triples leave one copy uncancelled plus the singleton — two survivors, not one. Mistaking this for LC 136 is the canonical bug.

---

## Problem 5 — Sum of Two Integers (LC 371)

**Spec.** Given two integers `a` and `b`, return their sum without using the `+` or `-` operators.

**Constraints.** `-1000 <= a, b <= 1000`.

**Pattern.** Full-adder bit arithmetic.

**Hint.** The XOR `a ^ b` is the sum without carries; `(a & b) << 1` is the carry. Loop: while there is a carry, recompute `a, b = a ^ b, (a & b) << 1` until `b` (the carry) is zero. In Python, the arbitrary-precision integers complicate negative handling — mask with `& 0xFFFFFFFF` to simulate 32-bit wraparound and convert back at the end. (This problem is notoriously fiddly in Python *precisely because* there is no fixed width; naming that is the interview tell.)

**Acceptance.** Function signature `get_sum(a: int, b: int) -> int`. Time: `O(1)` (bounded by the bit width). Space: `O(1)`.

**Variant.** The Python-specific 32-bit masking is the discriminator; in a fixed-width language (C, Java) the loop is cleaner because overflow wraps naturally. Name the language dependence.

---

## Problem 6 — Maximum XOR of Two Numbers (LC 421)

**Spec.** Given an integer array, return the maximum `nums[i] XOR nums[j]` over all pairs.

**Constraints.** `1 <= len(nums) <= 2 * 10^5`; `0 <= nums[i] <= 2^31 - 1`.

**Pattern.** Bitwise trie with a greedy opposite-bit walk (Lecture 2 §6; Challenge 1).

**Hint.** Insert each number's 31 bits (most-significant first) into a 0/1 trie. For each number, walk the trie greedily choosing the *opposite* bit at each level when it exists — XOR is maximized when the high bits differ. `O(n * B)`.

**Acceptance.** Function signature `find_maximum_xor(nums: List[int]) -> int`. Time: `O(n * B)`, `B = 31`. Space: `O(n * B)`. (This is also Challenge 1 — drill the recognition here, ship the full write-up there.)

**Variant.** A hash-set bit-by-bit approach builds the answer one bit at a time using a set of prefixes — same `O(n * B)` time, `O(n)` space. The trie form is more transparent and generalizes to "find the partner."

---

## Rubric

For each problem, your write-up is graded on five dimensions:

| Dimension | Weight | What "yes" looks like |
|-----------|-------:|----------------------|
| Match (Pattern Recognition) | 25% | 30-second memo at the top; pattern named in one of the Week-14 shapes; alternative rejected with reason |
| Plan | 15% | Numbered steps; the key move named (XOR-then-partition, greedy opposite-bit, wildcard branching, etc.) |
| Implement (Correctness) | 25% | All LC sample cases pass; the bit-width / off-by-one details correct |
| Implement (Style) | 10% | Type hints everywhere; docstrings; PEP 8; idiomatic Python |
| Evaluate (Defense) | 25% | Time + space bounds with derivation; one variant mentioned; trade against an alternative stated |

The Match weight is the highest for a reason. Phase 2 grades recognition heavily; the discriminating recognitions this week are "triples break plain XOR" (Problem 4) and "this is a *bitwise* trie, not a character trie" (Problem 6).

---

## Suggested order

1. **Problem 1** first — Single Number III cements the partition-by-a-bit move, the most reusable bit trick.
2. **Problem 3** second — Number of 1 Bits is a quick popcount rep; warms up the bit vocabulary.
3. **Problem 4** third — Single Number II is the high-value recognition: where plain XOR-cancellation *fails*. The mod-3 / state-machine insight is the work.
4. **Problem 2** fourth — Add and Search Word is the trie-with-wildcard rep; the branching recursion is the new piece.
5. **Problem 6** fifth — Maximum XOR is the bitwise trie; the most onsite-likely problem of the week.
6. **Problem 5** last — Sum of Two Integers is the fiddly full-adder rep; save it for when the others are fluent.

If time runs out, prioritize Problems 1, 2, and 4 — the three patterns most likely to appear on Mock #4 and at a real onsite.

---

## Acceptance

The week's homework is complete when:

- All six problems have a committed implementation under `homework/c2-week-14/`.
- All six problems have a UMPIRE write-up under `umpire-writeups/c2-week-14/homework/`.
- The quiz is taken and scored.
- The score is in the retrospective: which sub-pattern needs the most reps before Mock #4.

The retrospective is the single most useful artifact this week. The pattern most candidates need more reps on after W14 is the *recognition limit* — knowing when plain XOR-cancellation applies (pairs) and when it does not (triples → bit-count mod 3; partition → distinguishing bit). The bit *vocabulary* is easy to memorize; the discipline of saying out loud "this is XOR-cancellation because the duplicates come in pairs and space is constant" — and rejecting it when the duplicates come in threes — is what separates the senior signal from the junior one. Drill the verbal Match-step in writing, then drill it aloud, then carry it into Mock #4.
