# Mini-Project — 1D DP + 2D DP, Fully FRAME-Narrated

> The week's deliverable: two compact portfolio artifacts that demonstrate fluency across the two highest-leverage Week-11 patterns — a 1D optimization DP (house robber) and a 2D counting DP (unique paths) — with full FRAME narration end-to-end. The pair is the discriminating element — Mock #2 grades the *1D-DP family* and the *2D-DP family* separately, and shipping one of each forces you to articulate the structural difference out loud.

**Estimated time:** 10 hours, split across Thursday–Saturday.

This mini-project is *narration-heavy* rather than *content-heavy*. You will produce two FRAME write-ups, each fully delivered in all five sections, each anchored by a 30-second pattern-recognition memo at the top. The two write-ups must be navigable as a pair — cross-references between them are part of the rubric.

---

## Why this matters

Three reasons.

1. **Phase 2 is graded on Research constraints.** Phase 1 spent four weeks installing the FRAME habit; Make the solution was the primary work. Phase 2 patterns are heavier and the Research constraints step matters more — recognition cost is no longer "30 seconds to name the pattern" but "60 seconds to name the DP shape (1D vs. 2D), name the state semantics in words, name the recurrence, and reject one wrong alternative." This mini-project is the sixth in C2 to grade two parallel write-ups as a *pair* (W6 BFS pair, W7 DFS pair, W8 heap pair, W9 string pair, W10 graph-and-DSU pair, W11 1D-and-2D pair).

2. **1D and 2D DP are the two structural shapes of every interview DP question.** Half of all FAANG DP problems are 1D (one state parameter); the other half are 2D (two state parameters). The pair forces you to articulate the differences: when does one index suffice (when the subproblem depends only on a prefix); when do you need two indices (when the subproblem depends on two prefixes or two endpoints); how does the iteration order shift between the two; when does space reduction apply.

3. **The full FRAME narration is the rubric.** Drills are graded on Research constraints + Make the solution; the mini-project adds Frame, Assess options, Examine, *and* cross-references. By Sunday you should be able to produce a full FRAME narration on a DP problem in 20–25 minutes, recorded, without rehearsal.

---

## What you ship

Three files: two problem write-ups plus a short overview.

```
frame-writeups/c2-week-11/mini-project/
├── README.md                                  ← short overview + index + reflection
├── problem-01-house-robber.md                 ← 1D optimization DP on LC 198
└── problem-02-unique-paths.md                 ← 2D counting DP on LC 62
```

Each write-up is the full FRAME format from Week 1, **plus a leading 30-second pattern-recognition memo at the top**.

The two problems are chosen so that:

- **Problem 1 (1D optimization DP):** the recurrence is the canonical take-or-skip from LC 198, narrated as if you were demoing the four-step pipeline. The discriminator is naming the state semantics in words — "maximum loot considering houses `0..i`" — before writing the recurrence.

- **Problem 2 (2D counting DP):** the recurrence is the canonical pull-from-top-and-left from LC 62. The Research constraints move is recognizing the two-precursor counting structure and the rolling-row space reduction; the defense is "the recurrence reads only the previous row plus the current row up to `dp[i][j - 1]`, so `O(n)` space is achievable."

The two problems together cover every Week-11 idiom: the four-step pipeline (recursion -> memoize -> tabulate -> rolling), state semantics in words, counting versus optimization recurrences, and 1D versus 2D iteration. After this pair, the recognition for any 1D or 2D DP should reduce to: *what is the state, and what is the recurrence?*

---

## The 30-second pattern-recognition memo (the signature element)

At the top of each write-up, immediately after the title, place a single bordered block.

### For Problem 1 (1D optimization DP)

```markdown
> **30-second pattern-recognition memo (1D optimization DP — House Robber):**
> Single-array optimization problem. State = "maximum loot considering
> houses 0..i." Recurrence: dp[i] = max(dp[i-1], dp[i-2] + nums[i]) —
> skip house i or rob house i. Two triggers: overlapping subproblems (the
> recursion `rob(i) = max(rob(i-1), rob(i-2) + nums[i])` revisits each i)
> and optimal substructure (the optimum composes from sub-optima).
> O(n) time, O(1) space with rolling pair. Why not greedy: the local
> optimum (largest single house) does not extend globally.
```

### For Problem 2 (2D counting DP)

```markdown
> **30-second pattern-recognition memo (2D counting DP — Unique Paths):**
> Grid traversal counting problem. State = "number of unique paths from
> (0,0) to (i,j)." Recurrence: dp[i][j] = dp[i-1][j] + dp[i][j-1] —
> arrive from the top or from the left. Two triggers fire. O(mn) time,
> O(n) space with rolling row. Why not combinatorics: the closed form is
> C(m + n - 2, m - 1), faster than DP but specific to this problem; for
> a variant with obstacles (LC 63), DP generalizes immediately and
> combinatorics does not.
```

Read each aloud; both should hit 25–30 seconds.

---

## FRAME structure for each write-up

Each problem's write-up follows the full FRAME format — all five sections, with Examine split into its verify and cost halves.

### Frame (~150 words)

Restate the problem in your own words. Confirm: input format, output format, constraints (size of `n`, range of `nums`, edge cases). For House Robber, confirm: the constraint is "adjacent houses cannot both be robbed"; the goal is to *maximize* total loot. For Unique Paths, confirm: the grid is `m x n`; movement is *only* down or right; no obstacles in this version.

### Research constraints (~200 words)

The 30-second memo *plus* a longer paragraph explaining:

- The two DP triggers (overlapping subproblems + optimal substructure).
- The state semantics in words.
- The recurrence as a formula.
- One non-DP alternative and why it is wrong (greedy for House Robber; combinatorics for Unique Paths).
- The complexity claim with derivation.

The Research constraints section is the single most-graded part of the write-up. Spend the time.

### Assess options (~120 words)

Numbered steps for the implementation. Should map 1:1 to the lines of code you will write. Both implementations follow the four-step pipeline:

1. Write the brute-force recursion as a comment (do not run it; it is exponential).
2. Convert to memoization with `@functools.lru_cache(maxsize=None)`.
3. Convert to bottom-up tabulation.
4. Reduce space (rolling pair for 1D; rolling row for 2D).

Include the base cases explicitly. Include the iteration order.

### Make the solution (~400 words including code)

Both problems get **two implementations**:

- The memoized form (`@functools.lru_cache`) — to demonstrate fluency with the top-down style.
- The tabulated form with space reduction — to demonstrate fluency with the bottom-up style.

Both must be correct on the LC sample cases. Both must have type hints, docstrings, and PEP 8 style.

### Examine · verify (~200 words)

Trace each implementation on a small example by hand. For House Robber, walk `nums = [2, 7, 9, 3, 1]` and show `dp = [2, 7, 11, 11, 12]`. For Unique Paths, walk `m = 3, n = 3` and show the table from Lecture 2 §2.

Then articulate one bug you caught (or could have caught) during the implementation. For House Robber, the canonical bug is forgetting that `dp[1] = max(nums[0], nums[1])`, not `nums[1]`. For Unique Paths, the canonical bug is initializing the first row and column to `0` instead of `1`.

### Examine · cost (~250 words)

The discriminating section. Articulate:

- Time and space complexity for both implementations with derivation.
- The space reduction: which prior states does the recurrence read, and therefore which can be discarded?
- One algorithmic variant (combinatorics for Unique Paths; matrix exponentiation for Fibonacci-style 1D DPs).
- One trade with the alternative algorithm: when would you prefer it; when would the DP form be better?
- Cross-reference to the other write-up: how the 1D and 2D shapes differ, and what carries between them (the four-step pipeline; the state-semantics-in-words discipline).

---

## The starter files

Two starter files are provided. **They are spec stubs, not working solutions.** You implement the bodies.

| File | Pattern | Functions to implement |
|------|---------|------------------------|
| [problem-01-house-robber-starter.py](./problem-01-house-robber-starter.py) | 1D DP | `rob_memoized`, `rob_tabulated` |
| [problem-02-unique-paths-starter.py](./problem-02-unique-paths-starter.py) | 2D DP | `unique_paths_memoized`, `unique_paths_tabulated` |

Each starter has a self-test block with LC sample cases. Run `python3 problem-01-house-robber-starter.py` after implementing.

---

## How the pair is graded

| Dimension | Weight | What "yes" looks like |
|-----------|-------:|----------------------|
| Research constraints (both write-ups) | 30% | Both memos in the canonical shape; both name the state in words and the recurrence in formula; both reject one non-DP alternative |
| Assess options (both write-ups) | 15% | Both list the four-step pipeline; both name base cases and iteration order |
| Make the solution (correctness) | 20% | All sample cases pass on both implementations of both problems |
| Make the solution (style) | 10% | Type hints everywhere; docstrings; PEP 8 |
| Examine · verify (both write-ups) | 10% | One hand-traced example per problem; one bug articulated |
| Examine · cost (both write-ups + cross-references) | 15% | Complexity derivations; space-reduction defenses; explicit cross-references between the 1D and 2D write-ups |

The cross-reference weight is the new element this mini-project. Sentences like "as in House Robber, the state captures a prefix" or "unlike Unique Paths, the 1D recurrence does not require space reduction beyond rolling-pair" demonstrate that you see the two problems as *the same shape with different parameters*, which is the senior Research constraints move.

---

## Reflection — the short README at the top of the deliverable

After both problem write-ups are complete, draft a 300-word reflection at the top of `frame-writeups/c2-week-11/mini-project/README.md`. Answer three questions:

1. **Which sub-pattern was easier to recognize, 1D or 2D?** Most learners find 1D easier because the state is "just an index"; 2D requires more thought to design the state. The senior-grade reflection identifies *why* — typically because 2D state designs require you to ask "what two things determine the subproblem?"
2. **What was the hardest base case to get right?** For House Robber, the canonical answer is `dp[1] = max(nums[0], nums[1])`. For Unique Paths, the canonical answer is the all-1s first row and first column. Articulating the answer demonstrates that you tested the boundary.
3. **What is the one DP shape you most want to drill before Mock #2?** Most W11 learners say "edit distance" or "longest palindromic subsequence" — both of which are W11 challenge problems. If yours is something else, name it; the retrospective drives next week's practice.

---

## Acceptance

The mini-project is shipped when:

- Both starter files are implemented with both `_memoized` and `_tabulated` versions, all self-tests pass.
- Both FRAME write-ups are committed to `frame-writeups/c2-week-11/mini-project/`.
- The reflection README is committed.
- Both write-ups have audio recordings of >= 12 minutes.
- The push log shows daily commits Thursday–Saturday.

Total time budget: 10 hours over three days. If you exceed 12 hours, stop and request a 1:1 with the Phase-2 lead before submitting; the over-budget likely indicates a deeper Research-constraints gap.

---

## A note on pacing

The mini-project is *not* a place to optimize for speed. Phase 2 grades depth; the 30% Research constraints weight is unrecoverable. Spend 30 minutes on the 30-second memo for each problem (read aloud, rewrite, read aloud again). Spend 45 minutes on the Examine · cost section (the cross-references are the discriminator). The implementations themselves should take 30–45 minutes per problem; they are the cheapest part.

Common over-spends: writing the brute-force recursion for too long (skip after 5 minutes; the memoized form is the spec for correctness), debugging the tabulation iteration order (re-read Lecture 1 §2 if you spend more than 15 minutes here), and obsessing over the rolling-array reduction (the basic tabulation form is sufficient if the rolling form is taking too long).

If you ship both write-ups under 8 hours, the stretch is to add a **third write-up** for one of the W11 challenge problems (edit distance or longest palindromic subsequence). The third is recognition-grade and not required, but Phase-2 alumni who shipped a third W11 write-up reported a noticeable Mock #2 score lift.
