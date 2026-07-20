# Week 5 — Homework

Six problems. ~5 hours total. Each commits to your portfolio repo. Two of them are parametric (binary search on the answer) — the highest-yield interview skill of the week.

---

## Problem 1 — Capacity to Ship Packages in D Days (LeetCode 1011) (60 min)

The canonical "minimize the capacity / threshold" parametric problem. Same structural family as Koko Bananas (Drill 5).

**Problem.** Given an array `weights[i]` of package weights (in load order) and an integer `D`, find the smallest ship capacity `c` such that all packages can be shipped within `D` days, where on each day the ship loads a contiguous prefix of remaining packages up to capacity `c`.

**The insight.** Reframe: find the smallest `c` in `[max(weights), sum(weights)]` such that `days_needed(c) <= D`. Predicate is monotone (larger capacity never increases day count).

**Acceptance:**

- A file `umpire-writeups/c2-week-05/hw-01-ship-capacity-in-D-days.md` with the UMPIRE write-up.
- Match section delivers the **four-element parametric cadence** (reframe, interval, predicate, return) and states the monotonicity claim explicitly.
- Evaluate section justifies **O(n log S) time, O(1) space** where `S = sum(weights)`.
- Recording ≥ 15 minutes.
- Tests passing on: `weights=[1,2,3,4,5,6,7,8,9,10], D=5 → 15`, `D=15 → 11`, `D=10 → 10`, `weights=[3,2,2,4,1,4], D=3 → 6`, `weights=[1,2,3,1,1], D=4 → 3`.

This problem and Koko are *structurally identical*. Your Match section should call out the parallel explicitly — "same family as Drill 5, predicate replaces 'hours' with 'days,' interval becomes `[max(weights), sum(weights)]` instead of `[1, max(piles)]`."

---

## Problem 2 — Split Array Largest Sum (LeetCode 410) (60 min)

A parametric problem in the *minimize-the-maximum* family — the harder cousin of Problem 1.

**Problem.** Given an array `nums` of non-negative integers and an integer `k`, partition `nums` into `k` non-empty contiguous subarrays. Minimize the largest sum among the `k` subarrays. Return that minimum.

**The insight.** Reframe: find the smallest `cap` in `[max(nums), sum(nums)]` such that we can partition into at most `k` groups, each with sum `<= cap`. Predicate is monotone.

**Acceptance:**

- File `umpire-writeups/c2-week-05/hw-02-split-array-largest-sum.md`.
- Match section names the **"minimize the maximum"** family and compares against Problem 1 ("same predicate shape, different framing: ship-capacity says 'within D days,' this says 'into k groups' — combinatorially identical").
- Working code with tests: `nums=[7,2,5,10,8], k=2 → 18`, `nums=[1,2,3,4,5], k=2 → 9`, `nums=[1,4,4], k=3 → 4`.

This is the most-asked parametric problem in real interviews. After Problem 1 and 2, the "minimize the maximum" pattern should be reflexive.

---

## Problem 3 — Find Peak Element (LeetCode 162) (40 min)

A "binary search on a non-sorted array via a monotone-flip predicate" — the structural cousin to the Median challenge but much easier.

**Problem.** Given an integer array `nums` where adjacent elements are distinct, return the index of *any* peak — an element strictly greater than its neighbors. Treat `nums[-1] = nums[n] = -inf`. Solve in `O(log n)`.

**The insight.** Even though the array is not sorted, the "go uphill" rule produces a monotone bisection: at any midpoint `m`, if `nums[m] < nums[m+1]`, a peak must lie to the right (because we can keep climbing); else a peak lies at `m` or to the left. The predicate `is_ascending_at(m) = (nums[m] < nums[m+1])` is *eventually False* once you pass the peak, so binary-search for the first index where it becomes False.

**Acceptance:**

- File `umpire-writeups/c2-week-05/hw-03-find-peak-element.md`.
- Match section names the **"binary search on a non-sorted array via a monotone predicate"** insight.
- Evaluate section justifies **O(log n) time, O(1) space** — and explicitly addresses how binary search applies to a non-sorted array.
- Tests: `nums=[1,2,3,1] → 2`, `nums=[1,2,1,3,5,6,4] → 1 or 5 (either valid)`, `nums=[1] → 0`, `nums=[1,2] → 1`.

This problem warms up the technique for the Median challenge if you have not yet attempted it. If Median felt hard, do this first; the partial-monotonicity idea transfers.

---

## Problem 4 — Search in Rotated Sorted Array II (LeetCode 81) (45 min)

The duplicate-allowed variant of Drill 3. The duplicates break the strict invariant; you handle them with a small additional case.

**Problem.** Same as Drill 3 (search a rotated sorted array for a target), but the array may contain duplicates. Return True if target is present, False otherwise.

**The insight.** When `arr[lo] == arr[mid]` (and `arr[mid] == arr[hi]`), you cannot decide which half is sorted in `O(1)`. Solution: shrink one end by one (`lo += 1`) and retry. This is `O(n)` worst case (e.g., array of all duplicates), but typical inputs remain `O(log n)`.

**Acceptance:**

- File `umpire-writeups/c2-week-05/hw-04-search-rotated-with-duplicates.md`.
- Match section explicitly addresses the **worst-case complexity degrades to O(n)** because of the deduplication step, with one-line justification.
- Tests: `arr=[2,5,6,0,0,1,2], target=0 → True`, `target=3 → False`, `arr=[1,0,1,1,1], target=0 → True`, `arr=[1], target=1 → True`.

The interview-tell move on this problem is **proactively stating** that the duplicate-allowed variant has worse worst-case complexity than the distinct-element variant. Most candidates do not realize this and produce a "log n" defense that is wrong.

---

## Problem 5 — Behavioral story #5 (45 min)

The story bank continues.

**Acceptance:**

- A file `behavioral/story-05.md` in your portfolio repo.
- Topic: **"Tell me about a time you had to make a decision with incomplete information."**
- Format: STAR (Situation, Task, Action, Result).
- 200-400 words.
- Read it aloud at least twice.
- Bonus credit: the story should connect to the *meta-skill* of binary search — making the *best possible decision at each midpoint* given limited information. The connection is: every binary-search iteration is a "decision with incomplete information" (you only see one element, but you reason about half the array). Behavioral interviewers love when the candidate finds a structural connection to the technical skills.

---

## Problem 6 — System-design ground zero #5 (45 min)

Fifth 300-word warm-up.

**Acceptance:**

- A file `system-design/notes-week-05.md` containing a 300-word answer to: **"How would you design an autocomplete service that returns the top-10 completions for any prefix typed by a user, at 100K QPS?"**
- Do not look up the canonical answer first. Write what you'd say in an interview today.
- After writing, search "autocomplete trie" and "autocomplete service architecture" and read one free article on each. Note three things you'd add — *especially* if it mentions tries, prefix indexes, or caching.

The connection to this week: tries are an `O(prefix_length)` lookup structure, but the "top-k" requires either pre-computed ranks or a binary-search-on-the-answer over a sorted score list per prefix. The interview tell on this prompt is mentioning both the structural choice (trie vs sorted-list with binary search) and the tradeoff.

---

## Time budget

| Problem | Time |
|--------:|----:|
| 1 — Ship Capacity in D Days | 60 min |
| 2 — Split Array Largest Sum | 60 min |
| 3 — Find Peak Element | 40 min |
| 4 — Rotated Sorted Array II | 45 min |
| 5 — Behavioral story #5 | 45 min |
| 6 — System-design warm-up #5 | 45 min |
| **Total** | **4h 55min** |

---

By the end of Week 5 your portfolio repo's commit history should show ~60-80 commits total (the cumulative count through Week 4 + ~10-15 commits this week, including the mini-project's five write-ups and the Median challenge write-up). The cadence is the artifact; keep the streak.

Up next: [Week 6 — Graphs Part 1: BFS](../week-06/).
