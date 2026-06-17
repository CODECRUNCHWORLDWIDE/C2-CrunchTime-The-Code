# Week 12 — Homework

Six practice problems plus the rubric. Allow ~5 hours total. Do the problems on your own with the lectures *closed*; consult the lecture or the resources only after a 15-minute stuck-period on a single problem.

The problems are chosen to drill the six Week-12 sub-patterns: combinations (k-of-n), Cartesian product (phone keypad), constraint-aware enumeration (generate parentheses), deduplication (subsets II), string-piece backtracking with constraints (restore IP addresses), and combination sum with deduplication (combination sum II). By Sunday, the recognition step on each should be reflexive.

| # | Problem | Pattern | Source | Est. time |
|---|---------|---------|--------|----------:|
| 1 | Combinations | Backtracking — k-of-n with length prune | LeetCode 77 | 40 min |
| 2 | Letter Combinations of a Phone Number | Backtracking — Cartesian product | LeetCode 17 | 40 min |
| 3 | Generate Parentheses | Backtracking — constraint-aware enumeration | LeetCode 22 | 50 min |
| 4 | Subsets II | Backtracking — deduplication by sort + index-skip | LeetCode 90 | 40 min |
| 5 | Restore IP Addresses | Backtracking — string pieces with constraints | LeetCode 93 | 60 min |
| 6 | Combination Sum II | Backtracking — sum-based prune + deduplication | LeetCode 40 | 50 min |

Problems 1, 2, and 4 are the high-yield warm-ups; problem 3 is the constraint-aware-enumeration rep; problem 5 is the string-piece rep; problem 6 combines the prune and the dedup.

---

## Problem 1 — Combinations (LC 77)

**Spec.** Given two integers `n` and `k`, return all possible combinations of `k` numbers chosen from the range `[1, n]`.

**Constraints.** `1 <= n <= 20`; `1 <= k <= n`.

**Pattern.** Backtracking — k-of-n combinatorial enumeration with length prune (Lecture 1 §4).

**Hint.** State: `(start_index, path)`. Record at leaves where `len(path) == k`. The prune: `last = n - (k - len(path)) + 1`; iterating beyond `last` cannot reach length `k`.

**Acceptance.** Function signature `combine(n: int, k: int) -> List[List[int]]`. Time: `O(C(n, k) * k)`. Space: `O(k)` recursion plus output.

**Variant.** Bit-enumeration: iterate masks of `n` bits with exactly `k` set bits. Same asymptotic; the backtracking form is more interview-fluent.

---

## Problem 2 — Letter Combinations of a Phone Number (LC 17)

**Spec.** Given a string of digits 2-9, return all possible letter combinations under the phone-keypad mapping (2 -> "abc", 3 -> "def", ..., 9 -> "wxyz").

**Constraints.** `0 <= len(digits) <= 4`; digits only contain '2'-'9'.

**Pattern.** Backtracking — Cartesian product (Lecture 3 §5).

**Hint.** State: `(digit_index, path)`. At each level, iterate every letter in the current digit's group; choose, recurse, unchoose. No pruning needed (every letter is valid). Record at leaves where `digit_index == len(digits)`. Edge case: empty input returns `[]`, not `[""]`.

**Acceptance.** Function signature `letter_combinations(digits: str) -> List[str]`. Time: `O(4^n * n)` where `n = len(digits)` and 4 is the largest digit-group size (digits 7 and 9). Space: `O(n)` recursion plus output.

**Variant.** Iterative with `itertools.product`. Equivalent; the backtracking form is the template.

---

## Problem 3 — Generate Parentheses (LC 22)

**Spec.** Given `n` pairs of parentheses, return all combinations of well-formed parentheses.

**Constraints.** `1 <= n <= 8`.

**Pattern.** Backtracking — constraint-aware enumeration.

**Hint.** State: `(open_used, close_used, path)`. Two constraints: never use more than `n` of either; never use more `close` than `open`. At each level, two candidate choices: add an open paren if `open_used < n`; add a close paren if `close_used < open_used`. Record at leaves where `open_used == n and close_used == n`.

**Acceptance.** Function signature `generate_parenthesis(n: int) -> List[str]`. Time: the count of well-formed strings is the `n`-th Catalan number `C_n = (1 / (n + 1)) * C(2n, n)`; each string is length `2n`. Space: `O(n)` recursion plus output.

**Variant.** DP (count only — not enumeration) using Catalan recurrence. The DP form counts but does not generate; this is the canonical "enumeration is backtracking, counting is DP" pair.

---

## Problem 4 — Subsets II (LC 90)

**Spec.** Given an integer array `nums` that may contain duplicates, return all possible subsets (the power set). The solution set must not contain duplicate subsets.

**Constraints.** `1 <= len(nums) <= 10`; `-10 <= nums[i] <= 10`.

**Pattern.** Backtracking — deduplication by sort + index-skip (Lecture 2 §2).

**Hint.** Sort `nums` first. State: `(start_index, path)`. The dedup: `if i > start and nums[i] == nums[i - 1]: continue`. The discriminator is `i > start`, **not** `i > 0`; the condition skips duplicates at the same level but allows the same value at different depths.

**Acceptance.** Function signature `subsets_with_dup(nums: List[int]) -> List[List[int]]`. Time: `O(2^n * n)` worst case (when no duplicates). Space: `O(n)` recursion plus output.

**Variant.** Counting form: count subsets II in `O(n)` using the recurrence on the multiplicity of each distinct value. Mention the trade.

---

## Problem 5 — Restore IP Addresses (LC 93)

**Spec.** A valid IP address consists of exactly four integers (each between 0 and 255, no leading zeros except '0' itself) separated by single dots. Given a string `s` containing only digits, return all possible valid IP addresses that can be formed by inserting three dots into `s`.

**Constraints.** `1 <= len(s) <= 20`; `s` consists of digits only.

**Pattern.** Backtracking — string pieces with validation constraints.

**Hint.** State: `(start_index, segments)`. At each level, try lengths 1, 2, and 3 for the next segment; validate (no leading zero except "0", value <= 255); choose, recurse, unchoose. Record at leaves where `len(segments) == 4 and start == len(s)`. Prune the subtree early if any segment is invalid.

**Acceptance.** Function signature `restore_ip_addresses(s: str) -> List[str]`. Time: `O(1)` — the recursion has at most 4 levels and each level has at most 3 choices, so the total node count is constant (81 leaves maximum). Space: `O(1)`.

**Variant.** Iterative with three nested loops over the three dot positions. Same asymptotic; the backtracking form is more general.

---

## Problem 6 — Combination Sum II (LC 40)

**Spec.** Given an integer array `candidates` and a target integer `target`, return all unique combinations of `candidates` summing to `target`. Each number in `candidates` may be used **only once** in each combination. The solution set must not contain duplicate combinations.

**Constraints.** `1 <= len(candidates) <= 100`; `1 <= candidates[i] <= 50`; `1 <= target <= 30`.

**Pattern.** Backtracking — sum-based prune + deduplication.

**Hint.** Sort `candidates` first. State: `(start_index, remaining_target, path)`. No-reuse rule: recurse with `start = i + 1` (not `i`). The dedup: `if i > start and candidates[i] == candidates[i - 1]: continue`. The combination of the two — no-reuse for individual elements, no-dup for combinations — is the discriminator from LC 39.

**Acceptance.** Function signature `combination_sum2(candidates: List[int], target: int) -> List[List[int]]`. Time: bounded by the output size (the number of unique combinations) times the average path length. Space: `O(target / min_candidate)` recursion.

**Variant.** Without the dedup, the output contains duplicates for inputs like `[1, 1, 2], target = 3`. The dedup-by-skip is the senior signal; the alternative (post-process the output to remove duplicates) is `O(output_size * path_length)` extra time and is the junior signal.

---

## Rubric

For each problem, your write-up is graded on five dimensions:

| Dimension | Weight | What "yes" looks like |
|-----------|-------:|----------------------|
| Match (Pattern Recognition) | 25% | 30-second memo at the top; pattern named (subsets / permutations / combinations / Cartesian / string-pieces / dedup); alternative rejected (DP, greedy, bit-enumeration) with reason |
| Plan | 15% | Numbered steps; state design (`(start, path)` or `(used, path)` etc.); pruning condition |
| Implement (Correctness) | 25% | All LC sample cases pass; the deep-copy at the leaf (`path[:]`); the choose-recurse-unchoose template intact |
| Implement (Style) | 10% | Type hints everywhere; docstring on every function; PEP 8; idiomatic Python |
| Evaluate (Defense) | 25% | Time + space bounds with derivation; one variant mentioned; trade against a non-backtracking alternative stated |

The Match weight is the highest for a reason. Phase 2 grades recognition heavily; you can have a working implementation and still lose the rep if you cannot defend "this is backtracking, not DP" with one sentence.

---

## Suggested order

1. **Problem 1** first — Combinations is the highest-clarity warm-up. The length prune is the smallest non-trivial pruning rep.
2. **Problem 2** second — Letter Combinations is the Cartesian-product rep. The "no pruning needed" form contrasts with later problems.
3. **Problem 4** third — Subsets II installs the sort + index-skip dedup that recurs in problems 6 and beyond.
4. **Problem 3** fourth — Generate Parentheses is the constraint-aware-enumeration rep. The two-counter state design is the work.
5. **Problem 6** fifth — Combination Sum II combines the prune (from Exercise 3) and the dedup (from Problem 4). The combination is the senior-signal move.
6. **Problem 5** last — Restore IP Addresses is the string-piece rep with multi-constraint validation. The constant-time bound is the elegant surprise.

If time runs out, prioritize Problems 1, 2, and 4. They are the three patterns most likely to appear on Mock #2.

---

## Acceptance

The week's homework is complete when:

- All six problems have a committed implementation under `homework/c2-week-12/`.
- All six problems have a UMPIRE write-up under `umpire-writeups/c2-week-12/homework/`.
- The quiz is taken and scored.
- The score is in the retrospective: which sub-pattern needs the most reps before Mock #2.

The retrospective is the single most useful artifact this week. The pattern most candidates need more reps on after W12 is "the dedup discipline" — the recurrence is easy to write, but the discriminator between `i > start` (correct) and `i > 0` (subtly wrong) separates the senior signal from the junior one. Drill the verbal Match-step ("we sort, then skip duplicates at the same level") aloud until it is reflexive.
