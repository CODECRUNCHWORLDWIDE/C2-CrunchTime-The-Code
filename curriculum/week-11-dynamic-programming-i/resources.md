# Week 11 — Resources

Every resource is **free** and **publicly accessible**.

## Required reading (work it into your week)

- **`functools` — Python docs**: <https://docs.python.org/3/library/functools.html> — re-read the `lru_cache` and `cache` sections. The single most important DP-relevant detail: `@functools.lru_cache(maxsize=None)` caches return values keyed on the (hashable) argument tuple, turning any pure recursive function into a memoized top-down DP for free. As of Python 3.9, `@functools.cache` is the alias for `@functools.lru_cache(maxsize=None)`.
- **CPython `Lib/functools.py` source**: <https://github.com/python/cpython/blob/main/Lib/functools.py> — `_lru_cache_wrapper` is the readable reference. The cache uses a doubly-linked list plus a dict for `O(1)` insertion, lookup, and eviction; the comments at the top of `_lru_cache_wrapper` explain the design.
- **Dynamic programming — Wikipedia**: <https://en.wikipedia.org/wiki/Dynamic_programming> — the "Overlapping sub-problems" and "Optimal substructure" sections are the canonical written defenses of the two DP triggers. The "Examples of dynamic programming" section walks Fibonacci, the egg-dropping puzzle, and matrix-chain multiplication; the third is a Phase-3 stretch.
- **Memoization — Wikipedia**: <https://en.wikipedia.org/wiki/Memoization> — short article; the "Etymology" section is worth two minutes (memoization, not memorization; coined by Donald Michie, 1968).
- **Bellman's equation — Wikipedia**: <https://en.wikipedia.org/wiki/Bellman_equation> — Richard Bellman invented dynamic programming in the 1950s. The article is heavy on the operations-research framing; skim the "Bellman's principle of optimality" section, which is the math statement of "optimal substructure."
- **PEP 8 (recurring)**: <https://peps.python.org/pep-0008/>
- **Big-O Cheat Sheet (recurring)**: <https://www.bigocheatsheet.com/>

## On the pattern itself

Dynamic programming appears in interview prompts under many surface forms. The recognition skill is mapping the surface form to the underlying state.

- **"Count the number of ways to ..."** — counting DP. State is the thing being counted; recurrence sums contributions from preceding states. Examples: the ferry ramp manifests, the terrace route table, the ledger ribbon.
- **"Find the minimum / maximum ..."** — optimization DP. State is the index or pair of indices; recurrence is a min or max over choices. Examples: the survey station walk, the timetable amendment, the kiln flue draw.
- **"Is it possible to ..."** — boolean DP. State is a partial configuration; recurrence is an OR over preceding boolean states. Examples: the stripped manifest line, the batch split.
- **"Find the longest / shortest ... that satisfies ..."** — optimization DP, often 2D. State is `(i, j)` where `i` and `j` are positions in two sequences (or two ends of one sequence). Examples: the paired manifest strike, the reversible rake.
- **"Compute the cost to transform ..."** — distance / edit DP. State is `(i, j)`; recurrence is a min over three choices (delete, insert, replace). Example: the timetable amendment.

If a prompt says "count" and the brute-force enumeration has overlapping branches — DP. If it says "min" or "max" and the optimum composes from sub-optima — DP. If it says "is it possible" and the partial answers can be cached — DP. If neither overlapping subproblems nor optimal substructure is present — not DP.

## Free practice platforms

- **HackerRank — DP domain**: <https://www.hackerrank.com/domains/algorithms?filters%5Bsubdomains%5D%5B%5D=dynamic-programming>
- **CSES Problem Set — Dynamic Programming section**: <https://cses.fi/problemset/> — the canonical curated set; the first 19 problems are the DP foundations and are exactly the right Phase-2 reps.

## On the four-step pipeline

The shape you should be able to walk in your head on every DP problem.

| Step | What you do | What you produce | Cost |
|------|-------------|------------------|------|
| 1. Recursion | Write a pure recursive function with the state as parameters | Brute-force solution, exponential time | 5 minutes |
| 2. Memoize | Add `@functools.lru_cache(maxsize=None)` | Top-down DP, polynomial time | 30 seconds |
| 3. Tabulate | Convert to a bottom-up loop over a `dp` array | Bottom-up DP, same complexity, no recursion overhead | 5–10 minutes |
| 4. Reduce | If the recurrence only needs the previous row, use a rolling array | Bottom-up DP with optimal space | 2–3 minutes |

Three observations:

1. **Skip step 2 only if you are confident.** Under interview pressure, the memoized form is the fastest correct DP you can produce. Convert to tabulation only if the interviewer asks for the space optimization or if recursion depth is a real concern (Python's default recursion limit is 1000; `sys.setrecursionlimit(10**6)` is a one-liner if you need it).
2. **Tabulation requires an explicit iteration order.** The iteration order must guarantee that every `dp[state]` is computed before it is read. For 1D, this is "left to right." For 2D, this is row-major (most cases) or by-substring-length (longest palindromic subsequence). Getting the order wrong is the most common tabulation bug.
3. **Step 4 is recognition-grade for most interviews.** If the interviewer asks "can you reduce the space?", you should be able to point at the recurrence, identify which prior states are used, and reduce to a rolling array on the spot. For 2D DPs that depend only on `dp[i-1][...]` and the current row, the reduction is `O(min(m, n))` space.

### The canonical four-step pipeline on Fibonacci

```python
from __future__ import annotations

import functools

# Step 1 — brute-force recursion. O(2^n) time, O(n) stack.
def fib_naive(n: int) -> int:
    """Compute the n-th Fibonacci number by naive recursion."""
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)

# Step 2 — memoize. O(n) time, O(n) space.
@functools.lru_cache(maxsize=None)
def fib_memo(n: int) -> int:
    """Compute the n-th Fibonacci number with top-down memoization."""
    if n < 2:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)

# Step 3 — tabulate. O(n) time, O(n) space.
def fib_table(n: int) -> int:
    """Compute the n-th Fibonacci number with bottom-up tabulation."""
    if n < 2:
        return n
    dp: list[int] = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

# Step 4 — reduce. O(n) time, O(1) space.
def fib_rolling(n: int) -> int:
    """Compute the n-th Fibonacci number with rolling-pair space reduction."""
    if n < 2:
        return n
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr
```

Memorize the four-step cadence; the body of each step is short, but the *progression* is what interviewers grade.

## On the 1D suite

A short table of the five 1D DPs you should be able to write from memory.

| Problem | State | Recurrence | Complexity |
|---------|-------|------------|-----------:|
| Fibonacci | `dp[i] = i-th Fibonacci number` | `dp[i] = dp[i-1] + dp[i-2]` | `O(n)` time, `O(1)` space |
| Climbing stairs | `dp[i] = ways to reach step i` | `dp[i] = dp[i-1] + dp[i-2]` | `O(n)` time, `O(1)` space |
| House robber | `dp[i] = max loot from houses 0..i` | `dp[i] = max(dp[i-1], dp[i-2] + nums[i])` | `O(n)` time, `O(1)` space |
| Decode ways | `dp[i] = ways to decode s[:i]` | `dp[i] = (dp[i-1] if s[i-1] valid) + (dp[i-2] if s[i-2..i] valid)` | `O(n)` time, `O(1)` space |
| Word break | `dp[i] = True iff s[:i] segmentable` | `dp[i] = any(dp[j] and s[j:i] in words for j in range(i))` | `O(n^2 * L)` time, `O(n)` space |

Three observations:

1. **Fibonacci and climbing stairs are the same DP.** The state semantics differ ("i-th Fibonacci" vs. "ways to reach step i"), but the recurrence is identical. This is the first reminder that DP is **state semantics first, recurrence second**.
2. **House robber is the simplest combinatorial-choice 1D.** The "take or skip" choice generalizes to coin change, knapsack, partition equal subset sum, and many Phase-3 DPs. Master it cold; the structure recurs.
3. **Decode ways has a conditional transition.** The recurrence adds `dp[i-1]` *only if* the single-digit code is valid (1–9) and adds `dp[i-2]` *only if* the two-digit code is valid (10–26). Forgetting one of the validity checks is the canonical bug; the canonical edge case is `s = "06"` (invalid because leading zero).

## On the 2D suite

A short table of the four 2D DPs you should be able to write from memory.

| Problem | State | Recurrence | Complexity |
|---------|-------|------------|-----------:|
| Unique paths | `dp[i][j] = paths from (0,0) to (i,j)` | `dp[i][j] = dp[i-1][j] + dp[i][j-1]` | `O(mn)` time, `O(n)` rolling space |
| Longest common subsequence | `dp[i][j] = LCS of s1[:i] and s2[:j]` | match: `dp[i-1][j-1] + 1`; else: `max(dp[i-1][j], dp[i][j-1])` | `O(mn)` time, `O(n)` rolling space |
| Edit distance | `dp[i][j] = edits to convert s1[:i] to s2[:j]` | match: `dp[i-1][j-1]`; else: `1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])` | `O(mn)` time, `O(n)` rolling space |
| Longest palindromic subsequence | `dp[i][j] = LPS of s[i..j]` | match: `dp[i+1][j-1] + 2`; else: `max(dp[i+1][j], dp[i][j-1])` | `O(n^2)` time, `O(n^2)` space (diagonal fill) |

Three observations:

1. **LCS and edit distance share the table shape, differ in the transition.** LCS picks the max over two; edit distance picks the min over three (delete, insert, replace). Recognizing this similarity is the senior-grade Research constraints move.
2. **LCS measures subsequence (skipping allowed); longest common substring measures substring (contiguous).** The substring variant uses a different recurrence: match extends `dp[i-1][j-1] + 1`; no-match resets to 0. The reset is the discriminator. This week is **subsequence only**; the substring variant is briefly noted in Lecture 2 §5.
3. **Longest palindromic subsequence requires diagonal iteration.** The recurrence reads `dp[i+1][j-1]` — the cell *below and to the left* — so the standard row-major iteration is wrong. Iterate by *substring length* (1, 2, 3, ..., n) so that shorter substrings are filled before longer ones. The iteration order is the discriminator, not the recurrence.

### The canonical 2D DP — longest common subsequence

```python
from __future__ import annotations

from typing import List

def longest_common_subsequence(s1: str, s2: str) -> int:
    """Length of the longest common subsequence of s1 and s2."""
    m, n = len(s1), len(s2)
    dp: List[List[int]] = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]
```

Sixteen lines. Memorize the shape. The `s1[i - 1] == s2[j - 1]` index offset (`i - 1`, not `i`) is the canonical off-by-one source; you index the *string* with `i - 1` because `dp[0][...]` and `dp[...][0]` are the empty-prefix base cases.

## Glossary additions

- **Dynamic programming (DP)** — a technique for solving problems by combining the solutions to overlapping subproblems. Two requirements: overlapping subproblems and optimal substructure.
- **Overlapping subproblems** — the property that the recursive call tree of a brute-force solution revisits the same arguments many times. Caching the result of each unique call collapses exponential time to polynomial.
- **Optimal substructure** — the property that the optimum of the full problem composes from optima of subproblems. The Bellman principle.
- **Memoization** — top-down DP. Write the recursion; cache the result keyed on the arguments. Python's `@functools.lru_cache(maxsize=None)` or `@functools.cache` (3.9+) is the one-liner.
- **Tabulation** — bottom-up DP. Iterate the state space in an order that guarantees every read of `dp[state]` happens after the corresponding write.
- **State** — the parameters that fully determine a subproblem. For 1D DP, the state is one index. For 2D DP, the state is a pair. The state-space size times the per-state work is the DP's time complexity.
- **Transition** — the recurrence that defines `dp[state]` in terms of `dp[smaller_state]`. The cost of evaluating one transition is the per-state work; for most DPs this is `O(1)`.
- **Base case** — the value of `dp[state]` for the smallest state(s), defined directly rather than via the recurrence. For 1D this is typically `dp[0]` and sometimes `dp[1]`; for 2D it is typically the first row and the first column.
- **Iteration order** — the order in which the bottom-up loop visits states. Must guarantee that every `dp[state]` is written before it is read. For 1D this is usually left to right; for 2D it is usually row-major; for longest palindromic subsequence it is by-substring-length.
- **Rolling array** — a space optimization where, if the recurrence only depends on the previous row (or the previous two rows), the table is collapsed to one or two rows. Reduces space from `O(mn)` to `O(min(m, n))`.
- **Subsequence** — a sequence that can be derived from another by deleting some elements without changing the order of the remaining elements. *Skipping is allowed.* "abc" is a subsequence of "axbycz".
- **Substring** — a contiguous sequence of characters within a string. *Skipping is not allowed.* "axb" is a substring of "axbycz"; "abc" is not.
- **Decision tree** — the tree of choices implicit in a brute-force recursion. Each node is a state; each edge is a choice. The size of the decision tree is the brute-force complexity; the size of the *unique state space* is the DP complexity.

## Cheatsheet — the DP recognition flowchart

A short decision flowchart you should be able to walk in 30 seconds.

```
Does the brute-force recursion revisit the same arguments many times?
  No  -> not DP. Consider greedy / brute-force with pruning / divide-and-conquer.
  Yes -> next question.

Does the optimum of the full problem compose from optima of subproblems?
  No  -> not DP. Consider backtracking with branch-and-bound.
  Yes -> DP. Identify the state next.

How many parameters does the state need?
  One  -> 1D DP. dp is a list. Examples: Fibonacci, climbing stairs, house robber.
  Two  -> 2D DP. dp is a 2D list. Examples: unique paths, LCS, edit distance.
  More -> the state design needs work. Most interview DP is 1D or 2D.

What does the recurrence look like?
  Sum / Count        -> counting DP. dp[i] = dp[i-1] + dp[i-2] or similar.
  Min / Max          -> optimization DP. dp[i] = min(...) or max(...).
  Boolean / Possible -> reachability DP. dp[i] = any(...) over preceding states.

What is the iteration order?
  1D, left to right  -> almost always correct.
  2D, row-major      -> correct for most 2D DPs (unique paths, LCS, edit distance).
  2D, by length      -> required for substring / palindromic subsequence DPs.

Can the space be reduced?
  Only previous row needed -> rolling array, O(min(m, n)) space.
  Only previous two values -> rolling pair, O(1) space.
  Otherwise                -> O(states) space is the bound.
```

Read aloud; should hit 25–30 seconds. The order matters — the questions narrow the DP shape in the same order they would surface in an interview prompt.
