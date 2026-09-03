# Mini-Project — The Orchard Row and the Dye Batch Log

> Topic: 1D optimisation and 2D counting · Lecture: [1](../lecture-notes/01-the-dp-pipeline-and-1d-states.md), [2](../lecture-notes/02-2d-dp-and-the-grid-and-string-shapes.md) · Difficulty: Medium-Hard · Target time: 10 hours across Thursday–Saturday · Why this one: the two families grade separately, and shipping one of each forces you to say the structural difference out loud.

## The Brief

The week's deliverable: two portfolio artifacts covering the two
highest-leverage Week 11 patterns, each fully narrated in FRAME.

**Half one, the orchard row.** Fruit trees stand in a line, each with a known
yield. The picking ladder needs clearance, so **no two adjacent trees** may be
picked in the same pass. Choose the trees. The orchard wants the yield *and* the
trees — someone has to walk out and mark them.

**Half two, the dye batch log.** A dyehouse logs every bath it ran. A recipe is a
short sequence of bath codes. Count how many **distinct ways** the recipe appears
in the log as a subsequence — the baths in order, not necessarily adjacent. Two
ways differ if they use different log positions, even when the codes read the
same.

One optimises and returns a choice. One counts, and the count gets large fast.
They are graded separately because they are structurally different, and the pair
is what makes you articulate the difference.

## Starter

`README-solution.py` sits beside this page with both halves solved and the
self-checks you must satisfy.

```text
orchard row:  7  12  5  9  14  3  11      (kg per tree, from the gate)

bath log:     INDIGOINDIGO
recipe:       IGO
```

Do the orchard row by hand first. The greedy answer — take the biggest, then the
biggest still legal — is wrong on a row this size, and finding out on paper is
much cheaper than finding out in code.

## Requirements

1. `best_yield(trees)` returns the largest legal total.
2. `picked_trees(trees)` returns the **positions** picked, in row order, with
   ties settled by preferring the earlier tree.
3. `recipe_ways(log, recipe)` returns the number of distinct matches.
4. `recipe_table(log, recipe)` returns the full table, because a write-up that
   shows its working needs it and because it is how you check the row form.
5. The row form and the table form must agree on every case — asserted, not
   assumed.
6. Both halves narrated in full FRAME, cross-referenced to each other.

### What you ship

Three files: two problem write-ups plus a short overview.

```
frame-writeups/c2-week-11/mini-project/
├── README.md                                  ← short overview + index + reflection
├── problem-01-house-robber.md                 ← 1D optimization DP on
└── problem-02-unique-paths.md                 ← 2D counting DP on
```

Each write-up is the full FRAME format from Week 1, **plus a leading 30-second pattern-recognition memo at the top**.

The two problems are chosen so that:

- **Problem 1 (1D optimization DP):** the recurrence is the canonical take-or-skip from, narrated as if you were demoing the four-step pipeline. The discriminator is naming the state semantics in words — "maximum loot considering houses `0..i`" — before writing the recurrence.

- **Problem 2 (2D counting DP):** the recurrence is the canonical pull-from-top-and-left from. The Research constraints move is recognizing the two-precursor counting structure and the rolling-row space reduction; the defense is "the recurrence reads only the previous row plus the current row up to `dp[i][j - 1]`, so `O(n)` space is achievable."

The two problems together cover every Week-11 idiom: the four-step pipeline (recursion -> memoize -> tabulate -> rolling), state semantics in words, counting versus optimization recurrences, and 1D versus 2D iteration. After this pair, the recognition for any 1D or 2D DP should reduce to: *what is the state, and what is the recurrence?*

---

### FRAME structure for each write-up

Each problem's write-up follows the full FRAME format — all five sections, with Examine split into its verify and cost halves.

### Frame (~150 words)

Restate the problem in your own words. Confirm: input format, output format, constraints (size of `n`, range of `nums`, edge cases). For the survey station walk, confirm: the constraint is "adjacent houses cannot both be robbed"; the goal is to *maximize* total loot. For the terrace route table, confirm: the grid is `m x n`; movement is *only* down or right; no obstacles in this version.

### Research constraints (~200 words)

The 30-second memo *plus* a longer paragraph explaining:

- The two DP triggers (overlapping subproblems + optimal substructure).
- The state semantics in words.
- The recurrence as a formula.
- One non-DP alternative and why it is wrong (greedy for the survey station walk; combinatorics for the terrace route table).
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

Trace each implementation on a small example by hand. For the survey station walk, walk `nums = [2, 7, 9, 3, 1]` and show `dp = [2, 7, 11, 11, 12]`. For the terrace route table, walk `m = 3, n = 3` and show the table from Lecture 2 §2.

Then articulate one bug you caught (or could have caught) during the implementation. For the survey station walk, the canonical bug is forgetting that `dp[1] = max(nums[0], nums[1])`, not `nums[1]`. For the terrace route table, the canonical bug is initializing the first row and column to `0` instead of `1`.

### Examine · cost (~250 words)

The discriminating section. Articulate:

- Time and space complexity for both implementations with derivation.
- The space reduction: which prior states does the recurrence read, and therefore which can be discarded?
- One algorithmic variant (combinatorics for the terrace route table; matrix exponentiation for Fibonacci-style 1D DPs).
- One trade with the alternative algorithm: when would you prefer it; when would the DP form be better?
- Cross-reference to the other write-up: how the 1D and 2D shapes differ, and what carries between them (the four-step pipeline; the state-semantics-in-words discipline).

---

### How the pair is graded

| Dimension | Weight | What "yes" looks like |
|-----------|-------:|----------------------|
| Research constraints (both write-ups) | 30% | Both memos in the canonical shape; both name the state in words and the recurrence in formula; both reject one non-DP alternative |
| Assess options (both write-ups) | 15% | Both list the four-step pipeline; both name base cases and iteration order |
| Make the solution (correctness) | 20% | All sample cases pass on both implementations of both problems |
| Make the solution (style) | 10% | Type hints everywhere; docstrings; PEP 8 |
| Examine · verify (both write-ups) | 10% | One hand-traced example per problem; one bug articulated |
| Examine · cost (both write-ups + cross-references) | 15% | Complexity derivations; space-reduction defenses; explicit cross-references between the 1D and 2D write-ups |

The cross-reference weight is the new element this mini-project. Sentences like "as in the survey station walk, the state captures a prefix" or "unlike the terrace route table, the 1D recurrence does not require space reduction beyond rolling-pair" demonstrate that you see the two problems as *the same shape with different parameters*, which is the senior Research constraints move.

---

## Constraints

- **`best_yield` keeps two running totals, not a table.** Nothing older than two
  trees is ever needed, so nothing older is kept. Say that in the memo.
- **`picked_trees` cannot use that form**, because it has thrown away the
  choices. Keeping the table is the price of an answer somebody can act on, and
  naming that trade is part of the grade: constant space and a number, or linear
  space and a list of trees.
- **The subsequence count walks the recipe backwards** for each log character.
  Forwards, one log character gets used twice in the same pass and the count
  comes out too high.
- **An empty recipe matches exactly once** — by taking nothing — however long the
  log. Base case, not special case.
- **Two matches differ by their positions**, not by their codes. `AAAA` contains
  `AA` six times, not once.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python README-solution.py
HALF ONE - the orchard row
    yields:  (7, 12, 5, 9, 14, 3, 11)
    best:    37 kg
    pick:    trees [0, 2, 4, 6] = [7, 5, 14, 11]

HALF TWO - the dye batch log
    log:     INDIGOINDIGO
    recipe:  IGO
    ways:    8

    the table, rows = log read so far, cols = recipe matched
                      I    G    O
                 1    0    0    0
        I        1    1    0    0
        N        1    1    0    0
        D        1    1    0    0
        I        1    2    0    0
        G        1    2    2    0
        O        1    2    2    2
        I        1    3    2    2
        N        1    3    2    2
        D        1    3    2    2
        I        1    4    2    2
        G        1    4    6    2
        O        1    4    6    8

All checks passed.
```

The printed table is the half-two write-up's best exhibit. Read the `I` column
down: 1, 1, 1, 2, 2, 2, 3… each `I` in the log adds the ways that existed before
it. Then read the last row across: 1, 4, 6, 8. Nothing about that is obvious from
the number 8 on its own, which is why the table is part of the deliverable.

## Steps

1. Read the self-checks. They are the spec.
2. Write both memos before any code: name which half optimises and which counts.
3. Implement `best_yield` with two running totals. Check `(6, 10, 6)` gives 12 —
   that row is in the tests precisely because greedy gives 10.
4. Implement `picked_trees`. Assert the choice is legal *and* achieves the
   reported best; those two assertions together are worth more than either.
5. Implement `recipe_ways` with a single row, walking the recipe backwards.
6. Implement `recipe_table` and assert the two agree on every case.
7. Write both FRAME passes and cross-reference them.

## The Solution

```python
"""README-solution.py - the Week 11 mini-project, both halves worked.

Two dynamic programming problems that grade separately because they are
structurally different: one OPTIMISES over a line, one COUNTS over a pair of
sequences.

  Half one - the orchard row. Fruit trees stand in a line, each with a known
  yield. The picking ladder needs clearance, so no two ADJACENT trees may be
  picked in the same pass. Choose the trees. The orchard wants the yield AND
  the trees, because someone has to walk out and mark them.

  Half two - the dye batch log. A dyehouse keeps a log of every bath it ran.
  A recipe is a short sequence of bath codes. Count how many distinct ways the
  recipe appears in the log as a subsequence - the baths in order, not
  necessarily adjacent. Two ways differ if they use a different set of log
  positions, even when the codes are identical.

The first returns a choice and its value. The second returns a count that is
often enormous. Saying which of those two you are doing, before writing code,
is what the pair is graded on.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that fence
reads as a new page section to anything splitting the page on headings.

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""

from __future__ import annotations

# ---- Given data ----
# Yield in kilograms for each tree, from the gate outwards.
ORCHARD_ROW: tuple[int, ...] = (7, 12, 5, 9, 14, 3, 11)

# The dyehouse log, and the recipe being looked for.
BATH_LOG = "INDIGOINDIGO"
RECIPE = "IGO"


# ---- Half one: the orchard row ----
def best_yield(trees: tuple[int, ...]) -> int:
    """The largest yield obtainable with no two adjacent trees picked.

    Two running totals rather than a table: at each tree the answer is either
    "pick it and add the best that ended two trees back" or "skip it and keep
    the best that ended one tree back". Nothing older than two trees is ever
    needed, so nothing older is kept.

    Args:
        trees: Yield per tree, in row order.

    Returns:
        The best total. An empty row yields 0.
    """
    took_previous = 0   # best total for a row ending at the previous tree, picked
    skipped_previous = 0  # best total for a row ending at the previous tree, skipped
    for tree in trees:
        take = skipped_previous + tree
        skip = max(took_previous, skipped_previous)
        took_previous, skipped_previous = take, skip
    return max(took_previous, skipped_previous)


def picked_trees(trees: tuple[int, ...]) -> list[int]:
    """Which trees to pick, as positions, for the best yield.

    The two-running-totals form cannot answer this - it has thrown away the
    choices. So this keeps the whole table and walks it backwards, which is the
    trade the write-up has to name: constant space and a number, or linear space
    and an answer somebody can act on.

    Args:
        trees: Yield per tree, in row order.

    Returns:
        Positions in row order. Ties are settled by preferring the EARLIER tree,
        so the answer is one set rather than a family of them.
    """
    if not trees:
        return []

    size = len(trees)
    best = [0] * (size + 1)   # best[i] = best yield using trees[i:]
    for i in range(size - 1, -1, -1):
        best[i] = max(trees[i] + (best[i + 2] if i + 2 <= size else 0), best[i + 1])

    chosen: list[int] = []
    i = 0
    while i < size:
        take = trees[i] + (best[i + 2] if i + 2 <= size else 0)
        # >= prefers taking the earlier tree on a tie, which is the stated
        # tie-break. Using > would silently prefer the later one.
        if take >= best[i + 1]:
            chosen.append(i)
            i += 2
        else:
            i += 1
    return chosen


# ---- Half two: the dye batch log ----
def recipe_ways(log: str, recipe: str) -> int:
    """How many distinct ways the recipe appears in the log as a subsequence.

    ways[j] is the number of ways to match recipe[:j] against the part of the
    log read so far. Walking the recipe BACKWARDS for each log character is what
    keeps a single row honest: going forwards would let one log character be
    used twice in the same pass.

    Args:
        log: The dyehouse log of bath codes.
        recipe: The sequence being looked for.

    Returns:
        The number of distinct position sets. An empty recipe matches exactly
        once - by taking nothing - which is the base case, not a special case.
    """
    ways = [0] * (len(recipe) + 1)
    ways[0] = 1
    for bath in log:
        for j in range(len(recipe), 0, -1):
            if recipe[j - 1] == bath:
                ways[j] += ways[j - 1]
    return ways[len(recipe)]


def recipe_table(log: str, recipe: str) -> list[list[int]]:
    """The full table, for a write-up that wants to show its working.

    Args:
        log: The dyehouse log.
        recipe: The sequence being looked for.

    Returns:
        (len(log) + 1) by (len(recipe) + 1); entry [i][j] is the number of ways
        to match recipe[:j] within log[:i].
    """
    rows, cols = len(log) + 1, len(recipe) + 1
    table = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        table[i][0] = 1  # the empty recipe matches once, by taking nothing
    for i in range(1, rows):
        for j in range(1, cols):
            table[i][j] = table[i - 1][j]
            if log[i - 1] == recipe[j - 1]:
                table[i][j] += table[i - 1][j - 1]
    return table


# ---- Self-check ----
if __name__ == "__main__":
    print("HALF ONE - the orchard row")
    print(f"    yields:  {ORCHARD_ROW}")
    picked = picked_trees(ORCHARD_ROW)
    print(f"    best:    {best_yield(ORCHARD_ROW)} kg")
    print(f"    pick:    trees {picked} = {[ORCHARD_ROW[i] for i in picked]}")
    print()

    print("HALF TWO - the dye batch log")
    print(f"    log:     {BATH_LOG}")
    print(f"    recipe:  {RECIPE}")
    print(f"    ways:    {recipe_ways(BATH_LOG, RECIPE)}")
    print()
    print("    the table, rows = log read so far, cols = recipe matched")
    table = recipe_table(BATH_LOG, RECIPE)
    print("             " + "".join(f"{c:>5}" for c in " " + RECIPE))
    for i, row in enumerate(table):
        head = " " if i == 0 else BATH_LOG[i - 1]
        print(f"        {head}    " + "".join(f"{v:>5}" for v in row))
    print()

    # ---- Half one.
    # The choice must be legal: no two picked trees adjacent.
    for i in range(len(picked) - 1):
        assert picked[i + 1] - picked[i] >= 2

    # And it must actually achieve the reported best.
    assert sum(ORCHARD_ROW[i] for i in picked) == best_yield(ORCHARD_ROW)

    # Known small cases, including the ones that catch a greedy solution.
    assert best_yield(()) == 0
    assert picked_trees(()) == []
    assert best_yield((5,)) == 5
    assert best_yield((5, 9)) == 9
    assert best_yield((9, 5)) == 9
    # Greedy-by-largest picks 10 and then cannot take either 6, giving 10.
    # Taking both 6s gives 12, so greedy is wrong and this row proves it.
    assert best_yield((6, 10, 6)) == 12
    assert picked_trees((6, 10, 6)) == [0, 2]

    # The tie-break: equal either way, take the earlier tree.
    assert picked_trees((4, 4)) == [0]

    # ---- Half two.
    # The row form and the table form must agree, always.
    for log, recipe in ((BATH_LOG, RECIPE), ("AAAA", "AA"), ("ABC", "ABC"),
                        ("ABC", "CBA"), ("", "A"), ("A", ""), ("", "")):
        assert recipe_ways(log, recipe) == recipe_table(log, recipe)[len(log)][len(recipe)]

    # The empty recipe matches once - by taking nothing - however long the log.
    assert recipe_ways("ANYTHING", "") == 1
    assert recipe_ways("", "") == 1

    # A recipe longer than the log cannot match.
    assert recipe_ways("", "A") == 0
    assert recipe_ways("AB", "ABC") == 0

    # Four A's contain "AA" in six ways: every pair of positions.
    assert recipe_ways("AAAA", "AA") == 6

    # Order matters: the codes are all present but never in the right order.
    assert recipe_ways("ABC", "CBA") == 0

    print("All checks passed.")
```

Both halves in one file, so the two shapes can be read side by side. `best_yield`
carries two integers; `recipe_ways` carries one row. Neither keeps more than it
needs — and `picked_trees` keeps the table precisely because it needs more, which
is the trade the write-up has to defend.

## Download and run

Download the solution beside this page and run it:

```bash
python README-solution.py
```

No third-party packages, no arguments, no input. It prints both halves, the full
count table, and then `All checks passed.`

## Common bugs to catch

- **Greedy on the orchard row.** Symptom: 10 where the answer is 12 on
  `(6, 10, 6)`. Taking the largest first is not the same as taking the best set.
- **Reporting a yield the choice does not achieve.** Symptom: the two functions
  disagree and nothing catches it. Assert that the picked trees sum to the
  reported best.
- **An illegal choice.** Symptom: two adjacent positions in the list. Assert the
  gap is at least 2.
- **Walking the recipe forwards.** Symptom: counts far too high, and worse the
  more the codes repeat. One log character is being used twice in a pass.
- **Seeding the empty recipe as 0.** Symptom: every count is 0. It matches once.
- **Assuming the count is small.** Symptom: nothing, until it is not. The count
  grows quickly; say so in Examine (cost) rather than discovering it.

## Acceptance checklist

The mini-project is shipped when:

- Both starter files are implemented with both `_memoized` and `_tabulated` versions, all self-tests pass.
- Both FRAME write-ups are committed to `frame-writeups/c2-week-11/mini-project/`.
- The reflection README is committed.
- Both write-ups have audio recordings of >= 12 minutes.
- The push log shows daily commits Thursday–Saturday.

Total time budget: 10 hours over three days. If you exceed 12 hours, stop and request a 1:1 with the Phase-2 lead before submitting; the over-budget likely indicates a deeper Research-constraints gap.

---

## Stretch

- Report **how many** different tree sets achieve the best yield, not just one.
  It needs a second table and it is a good test of whether the first one is
  understood.
- Return the earliest and the latest position sets that match the recipe, rather
  than the count. The count table already holds enough to do it.
- Make each tree's yield depend on whether its neighbour was picked — an unpicked
  neighbour shades it — and say what breaks. The answer is that the state is no
  longer just "which tree", and naming the new state is the whole skill.

## The 30-second pattern-recognition memo (the signature element)

At the top of each write-up, immediately after the title, place a single bordered block.

### For Problem 1 (1D optimization DP)

```markdown
> **30-second pattern-recognition memo (1D optimization DP — the survey station walk):**
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
> **30-second pattern-recognition memo (2D counting DP — the terrace route table):**
> Grid traversal counting problem. State = "number of unique paths from
> (0,0) to (i,j)." Recurrence: dp[i][j] = dp[i-1][j] + dp[i][j-1] —
> arrive from the top or from the left. Two triggers fire. O(mn) time,
> O(n) space with rolling row. Why not combinatorics: the closed form is
> C(m + n - 2, m - 1), faster than DP but specific to this problem; for
> a variant with obstacles, DP generalizes immediately and
> combinatorics does not.
```

Read each aloud; both should hit 25–30 seconds.

---

## Reflection — the short README at the top of the deliverable

After both problem write-ups are complete, draft a 300-word reflection at the top of `frame-writeups/c2-week-11/mini-project/README.md`. Answer three questions:

1. **Which sub-pattern was easier to recognize, 1D or 2D?** Most learners find 1D easier because the state is "just an index"; 2D requires more thought to design the state. The senior-grade reflection identifies *why* — typically because 2D state designs require you to ask "what two things determine the subproblem?"
2. **What was the hardest base case to get right?** For the survey station walk, the canonical answer is `dp[1] = max(nums[0], nums[1])`. For the terrace route table, the canonical answer is the all-1s first row and first column. Articulating the answer demonstrates that you tested the boundary.
3. **What is the one DP shape you most want to drill before Mock #2?** Most W11 learners say "edit distance" or "longest palindromic subsequence" — both of which are W11 challenge problems. If yours is something else, name it; the retrospective drives next week's practice.

---

## A note on pacing

The mini-project is *not* a place to optimize for speed. Phase 2 grades depth; the 30% Research constraints weight is unrecoverable. Spend 30 minutes on the 30-second memo for each problem (read aloud, rewrite, read aloud again). Spend 45 minutes on the Examine · cost section (the cross-references are the discriminator). The implementations themselves should take 30–45 minutes per problem; they are the cheapest part.

Common over-spends: writing the brute-force recursion for too long (skip after 5 minutes; the memoized form is the spec for correctness), debugging the tabulation iteration order (re-read Lecture 1 §2 if you spend more than 15 minutes here), and obsessing over the rolling-array reduction (the basic tabulation form is sufficient if the rolling form is taking too long).

If you ship both write-ups under 8 hours, the stretch is to add a **third write-up** for one of the W11 challenge problems (edit distance or longest palindromic subsequence). The third is recognition-grade and not required, but Phase-2 alumni who shipped a third W11 write-up reported a noticeable Mock #2 score lift.
