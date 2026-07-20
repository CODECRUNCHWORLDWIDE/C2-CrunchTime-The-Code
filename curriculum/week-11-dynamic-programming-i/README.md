# Week 11 — Dynamic Programming I

```
┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐
│ U │  │ M │  │ P │  │ I │  │ R │  │ E │
└───┘  └───┘  └───┘  └───┘  └───┘  └───┘
```

> *Week 10 installed the weighted-graph family — Dijkstra, Bellman-Ford, Floyd-Warshall, MST, DSU. Week 11 installs the **dynamic-programming pipeline**: the disciplined route from a brute-force recursion, through a `functools.lru_cache` memoization, to a hand-rolled bottom-up tabulation, and finally to a state-space reduction with a rolling array. 1D DP first — Fibonacci, climbing stairs, house robber, decode ways, word break. Then 2D DP — unique paths, longest common subsequence, edit distance, longest palindromic subsequence. The Match-step skill: what signal in the prompt screams DP (overlapping subproblems plus optimal substructure), and the four mechanical steps to convert any top-down recursion into a bottom-up table. By Sunday you can read a problem and say, in 30 seconds, "this is 1D-DP with state `i`," or "this is 2D-DP with state `(i, j)` and the recurrence is `dp[i][j] = ...`," and you can ship the table with a rolling-array space reduction if asked.*

Welcome to Week 11 of **C2 · CrunchTime — The Code** — the seventh week of Phase 2. Last week installed the weighted-graph family plus DSU. This week installs **dynamic programming**, beginning with the 1D and 2D foundations. The trie was the W9 specialization; the graph algorithms were the W10 specialization; DP is the W11–W12 specialization, and unlike the prior two, it is **less about a data structure** and **more about a disciplined process** — the four-step pipeline that turns any recursive decision tree into a bottom-up table.

DP is the single highest-variance interview topic. Strong candidates solve a medium DP in 15 minutes; weak candidates flail for 45 minutes and never reach a working solution. The discriminator is **not raw intelligence** — it is whether the candidate has internalized the pipeline. A candidate who writes brute-force recursion first, decorates it with `@lru_cache`, then mechanically converts to a bottom-up table will outperform a candidate who tries to "see the answer" in their head. This week installs that pipeline as a reflex.

The recognition signals are two: **overlapping subproblems** (the same recursive call appears many times in the call tree) and **optimal substructure** (the optimum of the full problem is composed of optima of subproblems). If both hold, the problem is DP. If only optimal substructure holds, it is greedy. If neither holds, it is brute-force search with pruning. The triage is the Match step.

By Sunday of Week 11 you will:

- **Recognize** a DP problem in 30 seconds by checking two boxes: overlapping subproblems (the recursion revisits the same state) and optimal substructure (the answer composes from sub-answers).
- **Write** a brute-force recursion first, **then** decorate with `functools.lru_cache(maxsize=None)`, **then** convert to a bottom-up table — in that order, every time. The pipeline is the rubric.
- **Convert** any top-down recursion to bottom-up in four mechanical steps: (1) identify the state; (2) identify the base cases; (3) identify the transition; (4) decide the iteration order so each `dp[state]` is computed before it is needed.
- **Write** a 1D DP from memory for Fibonacci, climbing stairs, house robber, decode ways, and word break. Defend the recurrence in one sentence per problem.
- **Write** a 2D DP from memory for unique paths, longest common subsequence (LCS), and edit distance. Defend the `dp[i][j]` state semantics and the transition out loud.
- **Articulate the subsequence/substring distinction.** Subsequence DP allows skipping characters; the recurrence pulls from `dp[i-1][j]` and `dp[i][j-1]`. Substring DP requires contiguity; the recurrence either continues the current substring or resets to zero. This distinction is the most-missed Phase-2 detail.
- **Reduce 2D DP space to `O(min(m, n))`** with a rolling array when only the previous row is needed. Defend the reduction by pointing at the recurrence and showing that `dp[i][j]` depends only on `dp[i-1][...]` and `dp[i][j-1]`.
- Have solved **three DP exercises** — climbing stairs (1D warm-up), longest common subsequence (2D canonical), and word break (1D plus a string-set check).
- Have shipped **one challenge** (edit distance with full UMPIRE narration) plus an optional stretch (longest palindromic subsequence with the substring/subsequence distinction defended).
- Have shipped the quiz, the homework, and the **mini-project**: one 1D DP write-up (house robber) plus one 2D DP write-up (unique paths), each with the four-step pipeline narrated end to end.

---

## Learning objectives

By the end of this week, you will be able to:

- **Match a DP problem in 30 seconds.** The signal hierarchy: does the brute-force recursion revisit the same arguments (overlapping subproblems); does the optimum of the whole problem compose from optima of subproblems (optimal substructure); is the state 1D (a single index) or 2D (a pair of indices); is the recurrence min/max (optimization) or count (combinatorial)? The four answers fully classify the DP shape.
- **Implement the four-step pipeline** as a reflex. Step 1: write brute-force recursion with the state as parameters. Step 2: add `@functools.lru_cache(maxsize=None)` and verify correctness on samples. Step 3: write a bottom-up table with the same state and the same transition. Step 4: if the recurrence only looks at the previous row (or the previous two values for 1D), reduce space with a rolling array.
- **Defend the choice of memoization versus tabulation** out loud. Memoization is easier to write under pressure; tabulation is faster (no function-call overhead) and supports rolling-array space reduction. Interview-grade answer: "I will start with memoization to verify correctness, then convert to tabulation if asked to optimize."
- **Implement Fibonacci** three ways: naive recursion (`O(2^n)`), memoized (`O(n)` time, `O(n)` space), tabulated (`O(n)` time, `O(1)` space with two rolling variables).
- **Implement climbing stairs** as a 1D DP: `dp[i] = dp[i-1] + dp[i-2]`. State = "number of ways to reach step `i`."
- **Implement house robber** as a 1D DP: `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`. State = "max loot considering houses `0..i`." Defend the choice between robbing house `i` (take `nums[i] + dp[i-2]`) and skipping it (take `dp[i-1]`).
- **Implement decode ways** as a 1D DP with a transition that conditionally adds `dp[i-1]` (if `s[i-1]` is a valid single-digit code) and conditionally adds `dp[i-2]` (if `s[i-2..i-1]` is a valid two-digit code). The branching transition is the discriminator.
- **Implement word break** as a 1D DP: `dp[i] = True` if some `j < i` has `dp[j] == True` and `s[j:i]` in the word set. State = "is `s[:i]` segmentable." Defend the `O(n^2)` time bound.
- **Implement unique paths** as a 2D DP: `dp[i][j] = dp[i-1][j] + dp[i][j-1]`. State = "number of paths from `(0,0)` to `(i,j)`." Reduce space to `O(n)` with a rolling row.
- **Implement longest common subsequence** as a 2D DP: `dp[i][j] = dp[i-1][j-1] + 1` if `s1[i-1] == s2[j-1]` else `max(dp[i-1][j], dp[i][j-1])`. State = "length of the LCS of `s1[:i]` and `s2[:j]`." The if/else transition is the discriminator vs. edit distance.
- **Implement edit distance** as a 2D DP: `dp[i][j] = dp[i-1][j-1]` if `s1[i-1] == s2[j-1]` else `1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`. The three-way min (delete, insert, replace) is the discriminator.
- **Implement longest palindromic subsequence** as a 2D DP with a non-standard iteration order: by substring length. `dp[i][j] = dp[i+1][j-1] + 2` if `s[i] == s[j]` else `max(dp[i+1][j], dp[i][j-1])`. The discriminator is iteration order: the table must be filled diagonally (by length), not row-major.

---

## Prerequisites

- **Weeks 1–10 complete.** You have shipped UMPIRE write-ups for the heap pair (W8), the trie pair (W9), and the graph pair (W10). You can write a recursion with a memoization decorator from memory.
- **Comfortable with `functools.lru_cache`.** The decorator caches the return value of a function keyed on its arguments. Set `maxsize=None` for unbounded cache. The decorated function must take hashable arguments (no lists; convert lists to tuples or pass indices).
- **Comfortable with recursion.** Specifically, the "branching recursion" pattern from W5: a function that calls itself two or more times with smaller inputs. If the recursion module from W3 still feels uncertain, re-walk it before starting this week.
- **Comfortable with 2D arrays.** `dp = [[0] * n for _ in range(m)]` is the canonical initializer. Reading `dp[i][j]` and writing `dp[i][j] = ...` should be reflexive. The off-by-one between "string of length `n`" and "indices `0..n-1`" and "table dimension `n + 1`" is the most common Phase-2 bug.
- **Comfortable with the difference between expected and worst-case complexity.** DP is `O(states * transition_cost)` always — not expected, not amortized. There is no probabilistic or amortized analysis hidden in standard DP, which makes the bound easier to defend than W10's `heapq` or DSU bounds.

---

## Topics covered

- **The DP pipeline** — the four mechanical steps from brute-force recursion to bottom-up table to rolling array
- **The two DP triggers** — overlapping subproblems plus optimal substructure; absence of either rules out DP
- **`functools.lru_cache` as a memoization decorator** — the one-line top-down DP; `maxsize=None` for unbounded
- **1D DP — Fibonacci** — the canonical warm-up; three forms: naive, memoized, tabulated with rolling pair
- **1D DP — climbing stairs** — Fibonacci in disguise; the state is "number of ways"
- **1D DP — house robber** — the take-or-skip recurrence; the simplest combinatorial-choice 1D
- **1D DP — decode ways** — the conditional-transition 1D; the discriminator is the validity check on each branch
- **1D DP — word break** — the segmentation 1D; the discriminator is the string-set lookup
- **2D DP — unique paths** — the canonical 2D warm-up; the recurrence pulls from the top and left
- **2D DP — longest common subsequence (LCS)** — the canonical subsequence DP; the if/else transition is the template for many subsequence variants
- **2D DP — edit distance** — the three-way min DP; the canonical "transform string A into string B" reach
- **2D DP — longest palindromic subsequence (LPS)** — the diagonal-fill DP; the discriminator is iteration order, not the recurrence
- **Subsequence vs. substring DP** — the contiguity distinction; LCS vs. longest common substring; the most-missed Phase-2 detail
- **State-space reduction** — rolling array for 2D DP that only depends on the previous row; rolling pair for 1D DP that only depends on the previous two values
- **The DP recognition flowchart** — from the constraint signals (counting? optimization? string-pair? grid?) to the right state form

---

## Weekly schedule (intensive · 36h)

| Day | Focus | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project | Self-Study | Daily Total |
|-----|-------|---------:|----------:|-----------:|----------:|---------:|-------------:|-----------:|------------:|
| Monday | The DP pipeline; Fibonacci three ways; exercise 1 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Tuesday | 1D DP suite; exercise 2 prep | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Wednesday | 2D DP suite; LCS and edit distance; exercise 3 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Thursday | Mini-project drafting; challenge ramp | 0h | 1h | 1h | 0.5h | 1h | 1.5h | 1h | 6h |
| Friday | Challenge (Edit Distance) | 0h | 0h | 2h | 0.5h | 1h | 1.5h | 1h | 6h |
| Saturday | Mini-project — 1D + 2D write-ups | 0h | 0h | 0h | 0.5h | 1h | 3h | 0h | 4.5h |
| Sunday | Quiz + retro + push | 0h | 0h | 0h | 0.5h | 0h | 4h | 0h | 4.5h |
| **Total** | | **6h** | **7h** | **3h** | **3h** | **6h** | **10h** | **3.5h** | **38.5h** |

(The week budgets ~36 hours; the table sums slightly higher to absorb the Phase-2 ramp. Drop 0.5h from Self-Study if 36h is your hard cap.)

**Mastery (10h/wk):** spread the same content over three calendar weeks. The mini-project lands in calendar Week 33 of the mastery pathway. See the [mastery study plan](../study-plans/mastery-1-year.md).

---

## How to navigate this week

| File | What's inside |
|------|---------------|
| [README.md](./README.md) | This overview |
| [resources.md](./resources.md) | Free readings + DP references + the four-step pipeline cheatsheet + glossary additions |
| [lecture-notes/01-the-dp-pipeline-and-1d-states.md](./lecture-notes/01-the-dp-pipeline-and-1d-states.md) | The two triggers, the four-step pipeline, the 1D suite (Fibonacci, climbing stairs, house robber, decode ways, word break) |
| [lecture-notes/02-2d-dp-and-the-grid-and-string-shapes.md](./lecture-notes/02-2d-dp-and-the-grid-and-string-shapes.md) | Unique paths, LCS, edit distance; the subsequence-vs-substring distinction |
| [lecture-notes/03-state-space-reduction-and-recognition.md](./lecture-notes/03-state-space-reduction-and-recognition.md) | Rolling-array reductions, longest palindromic subsequence and diagonal iteration, the recognition flowchart |
| [exercises/README.md](./exercises/README.md) | Index of the three DP exercises and SOLUTIONS |
| [exercises/exercise-01-climbing-stairs.py](./exercises/exercise-01-climbing-stairs.py) | LC 70 — the canonical 1D DP warm-up |
| [exercises/exercise-02-longest-common-subsequence.py](./exercises/exercise-02-longest-common-subsequence.py) | LC 1143 — the canonical 2D subsequence DP |
| [exercises/exercise-03-word-break.py](./exercises/exercise-03-word-break.py) | LC 139 — 1D DP with a string-set check |
| [exercises/SOLUTIONS.md](./exercises/SOLUTIONS.md) | Worked solutions with UMPIRE narration; consult after attempting each exercise |
| [challenges/README.md](./challenges/README.md) | Index of weekly challenges |
| [challenges/challenge-01-edit-distance.md](./challenges/challenge-01-edit-distance.md) | LC 72 deep-dive — the three-way-min recurrence and the rolling-array reduction |
| [challenges/challenge-02-longest-palindromic-subsequence.md](./challenges/challenge-02-longest-palindromic-subsequence.md) | LC 516 — the diagonal-fill DP and the subsequence/substring rejection |
| [quiz.md](./quiz.md) | 10 pattern-recognition questions |
| [homework.md](./homework.md) | Six practice problems (~5 hrs) — three 1D, three 2D |
| [mini-project/README.md](./mini-project/README.md) | **One 1D DP write-up (house robber) + one 2D DP write-up (unique paths)** — the week's deliverable |

---

## Stretch goals

- **Read the LeetCode "Dynamic Programming" tag** and skim 30 titles. For each, predict in 5 seconds: 1D or 2D? counting or optimization? string-pair or grid or array? Stretches the Match-step muscle harder than any exercise this week.
- **Re-derive the four-step pipeline** without re-reading Lecture 1. State the four steps aloud; if you cannot, you do not yet own the pipeline. Re-read and re-derive until you can.
- **Read the Wikipedia "Dynamic programming" article** end-to-end (about 20 minutes). The "Overlapping sub-problems" and "Optimal substructure" sections are the canonical written defenses of the two triggers; the "Examples of dynamic programming" section has six worked problems including the matrix-chain multiplication that Phase 3 revisits.
- **Implement Fibonacci with matrix exponentiation** for `O(log n)` time. The recurrence `[F(n+1), F(n)] = [[1,1],[1,0]] * [F(n), F(n-1)]` plus fast exponentiation gives the bound. Phase-3 stretch; the recognition cue is "compute the `n`-th Fibonacci number where `n` is `10^18`."
- **Read about the longest increasing subsequence in `O(n log n)`** via patience sorting. The standard LIS DP is `O(n^2)`; the patience-sorting variant uses `bisect` and is the canonical "DP can be optimized below the naive bound" example. Phase-3; this lecture covers LIS only as a Phase-3 stretch.

---

## What "done" looks like for Week 11

A learner who has shipped Week 11 has, in their portfolio repo:

- Three UMPIRE write-ups for the exercises, with recordings >= 10 minutes.
- One UMPIRE write-up for the Edit Distance challenge.
- The quiz answered (score recorded).
- The homework problems committed.
- **Two mini-project write-ups** (one 1D DP, one 2D DP), each with a 30-second pattern-recognition memo at the top, under `umpire-writeups/c2-week-11/mini-project/`.
- A push log showing daily commits Mon–Sun.

If all of that is present and pushed, Phase 2's seventh week is closed. You are ready for Week 12 — dynamic programming II (knapsack, longest increasing subsequence, and the Phase-2 capstone retrospective).

---

## A note on the Phase 2 ramp

Week 11 is the *pipeline-week* — the first of two DP weeks. The four-step pipeline is the highest-leverage Match-step skill for the remainder of Phase 2; almost every Phase-3 onsite asks at least one DP problem, and the recognition of "this is DP" plus the disciplined conversion from recursion to table is the senior signal. Implementation fluency on the 1D suite (climbing stairs, house robber, decode ways) and the 2D pair (LCS, edit distance) is the second-most-important outcome; longest palindromic subsequence and the diagonal-fill iteration are recognition-grade this week (know the shape, know the iteration order, implement under pressure but do not optimize for speed).

If you find yourself ahead by Friday, the right stretch is **not** another exercise — it is re-implementing climbing stairs from scratch *three different ways* (naive recursion, memoized, tabulated with rolling pair) and timing each on `n = 35`. The asymptotic difference is the most visceral demonstration of why DP matters; nothing in the lecture matches the moment a `2^35`-operation recursion runs for 20 seconds and the same problem with `@lru_cache` runs in 50 microseconds.

If you find yourself *behind* by Wednesday, skip Exercise 3 (Word Break) for now and prioritize Exercise 1 (Climbing Stairs — 1D) and Exercise 2 (LCS — 2D) — those are the two patterns that show up most often in Mock #2, and Word Break can be picked up in 30 minutes once the 1D template is fluent.

---

## Up next

[Week 12 — Dynamic Programming II](../week-12-dp-knapsack-lis-and-capstone/) — once your three DP write-ups are pushed, your four-step pipeline is articulate, and you can convert any top-down recursion to bottom-up from memory without consulting the lecture.

---

*If you find errors in this material, please open an issue or send a PR. Future learners will thank you.*
