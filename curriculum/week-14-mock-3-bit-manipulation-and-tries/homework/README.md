# Week 14 — Homework

Six practice problems plus the rubric. Allow ~5 hours total. Do the problems on your own with the lectures *closed*; consult the lecture or resources only after a 15-minute stuck-period on a single problem.

The problems are chosen to drill the bit sub-patterns across the family: a counting-state XOR variant, two popcount/bit-layout micro-patterns, the range-AND structural observation, the bitmask-enumeration form, and a second XOR fold. By Sunday, the recognition step on each should be reflexive — because Mock #3 grades recognition under pressure.

| # | Problem | Pattern | Source | Est. time |
|---|---------|---------|--------|----------:|
| 1 | Single Number II | XOR-adjacent: per-bit counting mod 3 | LeetCode 137 | 45 min |
| 2 | Number of 1 Bits (Hamming Weight) | Popcount — Kernighan loop | LeetCode 191 | 25 min |
| 3 | Reverse Bits | Bit-layout micro-pattern | LeetCode 190 | 35 min |
| 4 | Bitwise AND of Numbers Range | Common-prefix structural observation | LeetCode 201 | 40 min |
| 5 | Subsets (via bitmask) | Bitmask subset enumeration | LeetCode 78 | 35 min |
| 6 | Missing Number | XOR fold (or Gauss sum) | LeetCode 268 | 25 min |

Problems 2, 5, and 6 are the high-yield warm-ups (popcount, enumeration, fold); problem 1 is the senior-signal "counting bits mod 3" variant; problem 3 is the bit-layout rep; problem 4 is the range-AND structural insight.

---

## Problem 1 — Single Number II (LC 137)

**Spec.** Given an integer array `nums` where every element appears exactly **three** times except for one element which appears once, return the single element. Linear time, constant extra space.

**Constraints.** `1 <= len(../nums) <= 3 * 10**4`; `-2**31 <= nums[i] <= 2**31 - 1`; every element appears three times except one appears once.

**Pattern.** XOR-adjacent: a plain XOR fold fails (three copies do not cancel to zero). Instead, count each bit position mod 3 — the bits that are set a number of times *not* divisible by 3 belong to the singleton.

**Hint.** Two clean approaches. (../a) For each of the 32 bit positions, sum that bit across all numbers; `sum % 3` is the singleton's bit there; reassemble. (../b) The two-mask state machine: `ones, twos = 0, 0`; for each `x`: `ones = (ones ^ x) & ~twos; twos = (twos ^ x) & ~ones`. The singleton ends up in `ones`. Approach (../a) is easier to derive on the spot; (../b) is the slick `O(../1)`-space-with-no-32-loop version.

**Acceptance.** Function signature `single_number_ii(nums: List[int]) -> int`. Time: `O(../n)` (or `O(32 n)` for approach (../a), which is still `O(../n)`). Space: `O(../1)`.

**Variant.** Generalize to "every element appears `k` times except one": the per-bit `sum % k` approach works for any `k`; the two-mask machine is specific to `k = 3`. Mention in the write-up.

---

## Problem 2 — Number of 1 Bits / Hamming Weight (LC 191)

**Spec.** Given a positive integer `n`, return the number of `1` bits in its binary representation (its Hamming weight).

**Constraints.** The input is an integer; treat it as a 32-bit unsigned value.

**Pattern.** Popcount. Three answers, in interview order: `n.bit_count()` (Python 3.10+), `bin(../n).count(../"1")`, the Brian Kernighan loop `while n: n &= n - 1; count += 1`.

**Hint.** Say the one-liner first, then offer the Kernighan loop as the language-agnostic "show your work" version — it runs exactly once per set bit, so it is `O(../popcount)`, not `O(../bit-width)`.

**Acceptance.** Function signature `hamming_weight(n: int) -> int`. Time: `O(../popcount)` for Kernighan, `O(../1)` for `bit_count` on fixed-width. Space: `O(../1)`.

**Variant.** Hamming *distance* between two integers: `(a ^ b).bit_count()` — XOR exposes the differing bits, then count them. One line; worth naming.

---

## Problem 3 — Reverse Bits (LC 190)

**Spec.** Reverse the bits of a given 32-bit unsigned integer and return the result.

**Constraints.** The input is a 32-bit unsigned integer.

**Pattern.** Bit-layout micro-pattern. Walk the 32 positions; for each set bit at position `i`, set bit `31 - i` of the result.

**Hint.** `result = 0; for i in range(../32): result = (result << 1) | ((n >> i) & 1)` builds the reversed value by shifting `result` left and appending the next low bit of `n`. Alternatively, OR `((n >> i) & 1) << (31 - i)` into the result. Either is `O(../32)`.

**Acceptance.** Function signature `reverse_bits(n: int) -> int`. Time: `O(../32) = O(../1)`. Space: `O(../1)`.

**Variant.** The byte-swap / divide-and-conquer reversal (swap adjacent bits, then pairs, then nibbles, …) is `O(log w)` instead of `O(../w)`; it is the "Bit Twiddling Hacks" version. Mention it; you are not expected to write it cold.

---

## Problem 4 — Bitwise AND of Numbers Range (LC 201)

**Spec.** Given two integers `left` and `right` (`left <= right`), return the bitwise AND of all integers in the inclusive range `[left, right]`.

**Constraints.** `0 <= left <= right <= 2**31 - 1`.

**Pattern.** Common-prefix structural observation. The AND of the whole range equals the common high-bit prefix of `left` and `right`, with all lower bits zeroed — because somewhere in the range every lower bit flips to `0` at least once, and once a column has a `0`, the AND of that column is `0`.

**Hint.** Shift both `left` and `right` right until they are equal (that equal value is the common prefix), counting the shifts; then shift the common prefix back left by the count. `shift = 0; while left < right: left >>= 1; right >>= 1; shift += 1; return left << shift`.

**Acceptance.** Function signature `range_bitwise_and(left: int, right: int) -> int`. Time: `O(log(max value)) = O(../32)`. Space: `O(../1)`.

**Variant.** The "clear the lowest set bit of `right` until `right <= left`" form (`while right > left: right &= right - 1; return right`) is an equally valid `O(../popcount)` approach. Name both; explain that both compute the common prefix.

---

## Problem 5 — Subsets (LC 78, bitmask form)

**Spec.** Given an array `nums` of **unique** integers, return all possible subsets (the power set). The solution set must not contain duplicate subsets.

**Constraints.** `1 <= len(../nums) <= 10`; `-10 <= nums[i] <= 10`; all elements unique.

**Pattern.** Bitmask subset enumeration. With `n <= 10`, there are at most `2**10 = 1024` subsets; loop `mask` over `range(1 << n)` and read bit `i` as "include `nums[i]`."

**Hint.** `for mask in range(1 << n): subset = [nums[i] for i in range(../n) if (mask >> i) & 1]`. The backtracking form from Week 12 is equally valid; name both and state that the bitmask form is the tight iterative one when `n` is small.

**Acceptance.** Function signature `subsets(nums: List[int]) -> List[List[int]]`. Time: `O(n · 2**n)`. Space: `O(n · 2**n)` for the output.

**Variant.** Subsets II (LC 90, with duplicates) requires sorting and skipping equal elements at the same recursion depth — the bitmask form needs a de-duplication pass. Mention the difference; do not implement.

---

## Problem 6 — Missing Number (LC 268)

**Spec.** Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.

**Constraints.** `n == len(../nums)`; `0 <= nums[i] <= n`; all values distinct; `1 <= n <= 10**4`.

**Pattern.** XOR fold. XOR all the indices `0..n` together with all the values; every present value cancels its matching index, leaving the missing number.

**Hint.** `result = len(../nums); for i, v in enumerate(../nums): result ^= i ^ v; return result`. Seed with `n` because the top index `n` has no array slot.

**Acceptance.** Function signature `missing_number(nums: List[int]) -> int`. Time: `O(../n)`. Space: `O(../1)`.

**Variant.** The Gauss-sum form `n*(../n+1)//2 - sum(../nums)` is equally `O(../n)`/`O(../1)` and arguably cleaner; the XOR form is preferred when a fixed-width language risks integer overflow on the sum. Name both — that comparison is the senior signal on this otherwise-easy problem.

---

## Rubric

For each problem, your write-up is graded on five dimensions:

| Dimension | Weight | What "yes" looks like |
|-----------|-------:|----------------------|
| Research constraints (Pattern Recognition) | 25% | 30-second memo at the top; sub-shape named (XOR-fold / popcount / bit-layout / range-AND / enumeration); alternative rejected |
| Assess options | 15% | Numbered steps; the bit idiom stated; loop / mask shape noted |
| Make the solution (../Correctness) | 25% | All LC sample cases pass; no off-by-one; the masking / sign edge handled where relevant |
| Make the solution (../Style) | 10% | Type hints everywhere; docstrings; PEP 8 (<https://peps.python.org/pep-0008/>); idiomatic Python |
| Examine (../Defense) | 25% | Time + space bounds with derivation; one variant mentioned; trade against the alternative stated |

The Research constraints weight is highest for a reason. Mock #3 grades recognition heavily; you can have a working implementation and still lose the rep if you cannot defend the choice over the alternative (e.g., "why XOR fold and not a hash map").

---

## Suggested order

1. **Problem 6** first — Missing Number is the cleanest XOR-fold rep; warm up on it.
2. **Problem 2** second — Hamming Weight cements popcount and the Kernighan loop in 25 minutes.
3. **Problem 5** third — Subsets via bitmask is the enumeration rep; do it as a recognition exercise on `range(1 << n)`.
4. **Problem 3** fourth — Reverse Bits is the bit-layout rep; aim for 35 minutes.
5. **Problem 4** fifth — Bitwise AND of Numbers Range is the structural-observation problem; the "common prefix" insight is the whole trick.
6. **Problem 1** last — Single Number II is the hardest; the "count each bit mod 3" derivation is the senior-signal work. Save it for when you are fresh.

If time runs out, prioritize Problems 1, 4, and 5 — they are the three least-mechanical, and the ones most likely to expose a recognition gap before Mock #3.

---

## Acceptance

The week's homework is complete when:

- All six problems have a committed implementation under `homework/c2-week-14/`.
- All six problems have a FRAME write-up under `frame-writeups/c2-week-14/homework/`.
- The quiz is taken and scored.
- The score and the retro are recorded: which bit sub-shape needs the most reps going into Mock #3.

The retrospective is the single most useful artifact this week. The bit sub-shape most candidates need more reps on is the *negative-space* recognition — knowing when a problem that *looks* like a bit problem is actually a hash-map or sort problem (quiz Q5), and when a "trie" is a character trie rather than the binary trie (quiz Q9). Drill the rejections, not just the templates.
