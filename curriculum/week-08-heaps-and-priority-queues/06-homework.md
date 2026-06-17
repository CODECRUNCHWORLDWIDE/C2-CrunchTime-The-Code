# Week 8 — Homework

Five practice problems plus the rubric. Allow ~5 hours total. Do the problems on your own with the lectures *closed*; consult the lecture or the resources only after a 15-minute stuck-period on a single problem.

The problems are chosen to drill the five Week-8 sub-patterns: top-k, k-closest, two-heap, k-way merge, scheduler. By Sunday, the recognition step on each should be reflexive.

| # | Problem | Pattern | Source | Est. time |
|---|---------|---------|--------|----------:|
| 1 | Top K Frequent Elements | Heap-of-tuples; top-k by count | LeetCode 347 | 35 min |
| 2 | Last Stone Weight | Max-heap simulation | LeetCode 1046 | 25 min |
| 3 | Kth Smallest Element in a Sorted Matrix | k-way merge over rows | LeetCode 378 | 50 min |
| 4 | Reorganize String | Greedy max-heap with cooldown of size 1 | LeetCode 767 | 45 min |
| 5 | IPO | Two heaps (capital + profit) | LeetCode 502 | 60 min |

The first three are the high-yield drills; problems 4 and 5 are the composition problems that combine two heap primitives.

---

## Problem 1 — Top K Frequent Elements (LC 347)

**Spec.** Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. The answer order is unspecified.

**Constraints.** `1 <= len(nums) <= 10⁵`; `k` is in the valid range `[1, distinct(nums)]`.

**Pattern.** Heap-of-tuples; size-k min-heap by count.

**Hint.** `counts = collections.Counter(nums)`; iterate `(value, count)` pairs; size-k min-heap by count; return the values.

**Acceptance.** Function signature `top_k_frequent(nums: List[int], k: int) -> List[int]`. Time: `O(n log k)`. Space: `O(n + k)`.

**Variant to mention in the write-up.** `heapq.nlargest(k, counts.keys(), key=counts.get)` — the one-liner. Same `O(n log k)`. Mention as the production answer.

---

## Problem 2 — Last Stone Weight (LC 1046)

**Spec.** You are given an array of stone weights. On each turn, take the two heaviest stones; if their weights are equal, both are destroyed; otherwise, the heavier stone is replaced by a stone of weight `(heavy - light)`. Continue until at most one stone remains. Return the weight of the last stone (or `0` if no stones remain).

**Constraints.** `1 <= len(stones) <= 30`; `1 <= stones[i] <= 1000`.

**Pattern.** Max-heap simulation. The "take the two heaviest" cue is the heap signal.

**Hint.** Negate weights for max-heap. Pop two, push the difference (if non-zero). Loop until size ≤ 1.

**Acceptance.** Function signature `last_stone_weight(stones: List[int]) -> int`. Time: `O(n log n)` — n stones, each insert/pop is `O(log n)`. Space: `O(n)`.

**Variant.** What if there were a million stones? Same algorithm; the constant matters more. The senior framing: "size of the heap is bounded by the initial count; each round shrinks it by 1 or 2."

---

## Problem 3 — Kth Smallest Element in a Sorted Matrix (LC 378)

**Spec.** Given an `n × n` matrix where each row and each column is sorted in ascending order, return the k-th smallest element. (Note: the k-th in *sorted order* with duplicates; not the k-th distinct.)

**Constraints.** `1 <= n <= 300`; `1 <= k <= n²`.

**Pattern.** k-way merge over the rows. Each row is an already-sorted source; we merge until we have emitted `k` elements; the `k`-th is the answer.

**Hint.** Start a heap with the first element of each row: `(matrix[r][0], r, 0)`. Pop `k` times; each pop refills with `(matrix[r][c+1], r, c+1)` if `c+1 < n`. The `k`-th pop is the answer.

**Acceptance.** Function signature `kth_smallest(matrix: List[List[int]], k: int) -> int`. Time: `O(k log n)` — at most `n` items in the heap; `k` pops. Space: `O(n)`.

**Variant to mention.** Binary search on the value range — `O(n log(max - min))`. Faster when `k` is close to `n²`; named in the write-up as the alternative.

---

## Problem 4 — Reorganize String (LC 767)

**Spec.** Given a string `s`, rearrange the characters so that no two adjacent characters are the same. Return the rearranged string, or `""` if impossible.

**Constraints.** `1 <= len(s) <= 500`. `s` contains only lowercase letters.

**Pattern.** Greedy max-heap with cooldown of size 1. At each step, place the most-frequent remaining character; "cool" it (cannot use again until at least one other character is placed).

**Hint.** Count frequencies; if any character's count exceeds `(len(s) + 1) // 2`, return `""` (impossible). Otherwise: max-heap by count; on each step pop the top; emit; if the previous-step character still has remaining count, push it back.

**Acceptance.** Function signature `reorganize_string(s: str) -> str`. Time: `O(L log m)` where `L = len(s)` and `m = 26` (distinct letters). Space: `O(m)`.

**Variant.** This is the cooldown-size-1 case of Task Scheduler (Challenge 2). Mention the structural parallel in the write-up.

---

## Problem 5 — IPO (LC 502)

**Spec.** You have `k` distinct projects to choose from. Each project has a `capital[i]` (the capital required to start it) and a `profits[i]` (the profit it earns when finished). You start with initial capital `w`. Each completed project's profit is added to your capital; the new capital can start additional projects. Maximize your final capital after selecting at most `k` projects.

**Constraints.** `1 <= k <= 10⁵`; `0 <= w <= 10⁹`; `1 <= len(profits) == len(capital) <= 10⁵`.

**Pattern.** Two heaps. A **min-heap by capital** of "not-yet-affordable" projects; a **max-heap by profit** of "affordable" projects. At each step: move all newly-affordable projects from the capital-heap to the profit-heap; pop the most-profitable; add to `w`.

**Hint.** Sort projects by capital, then move into the affordable heap as `w` grows. The affordable heap is the active selection pool.

**Acceptance.** Function signature `find_maximized_capital(k: int, w: int, profits: List[int], capital: List[int]) -> int`. Time: `O((n + k) log n)`. Space: `O(n)`.

**Variant.** A *single*-heap version exists: sort the projects array and use one pointer plus one heap. Mention both; the two-heap version reads cleaner.

---

## Rubric (5 axes, 4 points each)

| Axis | What "great" looks like |
|------|--------------------------|
| Match-step recognition | The 30-second memo names the sub-pattern (top-k / k-closest / two-heap / k-way merge / scheduler) and the invariant (size bound / balance / tiebreaker / negation). |
| Plan | A 4-6 bullet algorithm before any code is written. |
| Implement | Idiomatic Python; `heapq` operations only (no manual sift code); type hints on every function. |
| Review | Trace on at least one example; one common bug called out and avoided. |
| Evaluate | The 5-piece — time / space / best-avg-worst / tradeoff / improvement — with the `O(n log k)` defense sentence and at least one rejected alternative. |

20 points total per problem; 100 points for the full homework set. Self-score honestly.

---

## How to submit

Commit your solutions under `umpire-writeups/c2-week-08/homework/`, one file per problem:

```
umpire-writeups/c2-week-08/homework/
├── problem-1-top-k-frequent.md      ← UMPIRE write-up + solution
├── problem-2-last-stone-weight.md
├── problem-3-kth-smallest-matrix.md
├── problem-4-reorganize-string.md
└── problem-5-ipo.md
```

Each file should be 100-200 lines: U + M + P + I + R + E plus a 5-line top memo. The solution code is part of the I section, not a separate file.

When done, push and move on to the [mini-project](./07-mini-project/00-overview.md).

---

## Time budget

| Problem | Solve | Write-up | Total |
|---------|------:|---------:|------:|
| 1 — Top K Frequent | 25 min | 10 min | 35 min |
| 2 — Last Stone Weight | 15 min | 10 min | 25 min |
| 3 — Kth Smallest Matrix | 40 min | 10 min | 50 min |
| 4 — Reorganize String | 30 min | 15 min | 45 min |
| 5 — IPO | 45 min | 15 min | 60 min |
| **Total** | **2h 35min** | **1h 0min** | **3h 35min** |

The remaining ~1.5h of the 5-hour homework budget is for the recording, the rebuild after stuck-periods, and the cross-references at the end of each write-up. Stay disciplined on the time budget; if a problem runs 30 minutes over, read the LeetCode editorial and move on.
