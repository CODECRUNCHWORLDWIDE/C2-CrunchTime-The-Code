# Mini-Project — Five Binary-Search Write-Ups (Including Two "Search on Answer" Variants)

> The week's deliverable: a single, compact portfolio artifact that demonstrates **boundary-defense fluency** across the five canonical binary-search shapes, plus a 30-second pattern-recognition memo per problem. The parametric-cadence memos on Problems 4 and 5 are the discriminating element — interviewers grade Match harder than candidates expect, and parametric recognition is the senior-level marker.

**Estimated time:** 10 hours, split across Thursday-Saturday.

This mini-project is *content-heavy* rather than *infrastructure-heavy*. You will produce five UMPIRE write-ups, each anchored by a 30-second pattern-recognition memo at the top. The Match memos are the artifact's signature element; the rest of each write-up is standard UMPIRE.

---

## Why this matters

Three reasons.

1. **Phase 2 is graded on Match.** Phase 1 spent four weeks installing the UMPIRE habit; the Implement step was the primary work. Phase 2 patterns are heavier and the Match step matters more — the recognition cost is no longer "30 seconds to name the pattern" but "60 seconds to name the variant, defend the boundary, and (for parametric) prove monotonicity." This mini-project is the first one in C2 that grades the four-element parametric cadence as strictly as Implement.

2. **Binary search has more confusable variants than any earlier pattern.** Classic (variant 1), lower bound (variant 2), upper bound (variant 3), rotated, binary search on values, parametric on the answer — six recognized shapes, each with its own template. Five write-ups force you to articulate the differences out loud. By the fifth, the disambiguation is reflexive.

3. **The "search on answer" variants are interview-distinguishing.** Most candidates pass the classic binary-search test. Few recognize parametric search on a prompt that does not mention "binary search" or "log n." If you ship Week 5 with parametric in your hands, you are statistically distinguishable from the median candidate at the same level. This mini-project demands two such write-ups.

---

## What you ship

Six files: five problem write-ups plus a short overview.

```
umpire-writeups/c2-week-05/mini-project/
├── README.md                                       ← short overview + index
├── problem-01-classic-binary-search.md             ← variant 1: classic find-target
├── problem-02-find-min-in-rotated.md               ← variant 1 + which-half-sorted: find pivot value
├── problem-03-search-insert-position.md            ← variant 2: lower bound on a sorted array
├── problem-04-koko-bananas.md                      ← parametric: minimum rate (search on answer)
└── problem-05-magnetic-force-aggressive-cows.md    ← parametric: maximize-the-minimum (search on answer)
```

Each write-up is the full UMPIRE format from Week 1, **plus a leading 30-second pattern-recognition memo at the top** — and for problems 4 and 5, the four-element parametric cadence (reframe, interval, predicate, return).

Drill 1 from this week overlaps with Problem 1 of the mini-project on the *underlying problem*. You may **adapt** your drill write-up for Problem 1 — but the mini-project write-up must add the 30-second memo, sharpen the Match section, and explicitly compare the variant against at least one *other* variant from the family. (Reusing a drill write-up verbatim is not acceptable; mini-project write-ups are graded against a stricter rubric.)

Problems 2, 3, 4, 5 are *new* relative to the drills. (Problem 4 reuses Drill 5's underlying problem but the mini-project version must add additional Match content — see Problem 4 below.)

---

## The 30-second pattern-recognition memo (the signature element)

At the top of every write-up, immediately after the title, place a single bordered block.

### For classic binary-search problems (Problems 1-3)

```markdown
> **30-second pattern-recognition memo:**
> This is a binary-search problem because [sorted-structure / target / log-n signal].
> The variant is [classic find-any / lower bound / upper bound / rotated / search on values].
> The boundary convention is [closed `[lo, hi]` with `<=` / half-open `[lo, hi)` with `<`].
> The shrink rules are: [one line each for the less-than and greater-than branches].
> The post-loop assertion is: [what `lo` represents when the loop exits].
> Why not [alternative]: [one sentence].
```

Six lines. Read aloud, ~25 seconds.

### For parametric problems (Problems 4-5)

```markdown
> **30-second pattern-recognition memo (parametric):**
> Reframe: find the [smallest / largest] `k` in [interval] such that [predicate].
> Interval: `lo = ...` because [one-line justification]; `hi = ...` because [one-line justification].
> Predicate: `feasible(k)` returns True iff [property]. Monotone in `k` because [one-line reason].
> Return: post-loop `lo` is the answer because [post-loop invariant].
> Why not [alternative]: [one sentence].
```

Six lines. Read aloud, ~30 seconds.

Example for Problem 1 (Classic Binary Search):

> **30-second pattern-recognition memo:**
> This is a binary-search problem because the array is sorted ascending and we need to locate a target in `O(log n)`.
> The variant is **variant 1, classic find-any**.
> The boundary convention is closed `[lo, hi]` with `while lo <= hi`.
> The shrink rules are: `arr[mid] < target → lo = mid + 1`; `arr[mid] > target → hi = mid - 1`. Both exclude `mid`.
> The post-loop assertion is: target was not found; the loop exited via `lo > hi`.
> Why not linear scan: `O(n)` is rejectable when the array is already sorted.

Example for Problem 4 (Koko Bananas):

> **30-second pattern-recognition memo (parametric):**
> Reframe: find the smallest rate `k` in `[1, max(piles)]` such that Koko finishes within `h` hours.
> Interval: `lo = 1` because Koko must eat at least 1 banana/hour to finish; `hi = max(piles)` because at this rate every pile takes exactly one hour and total hours = n ≤ h is guaranteed.
> Predicate: `feasible(k)` returns True iff `sum(ceil(pile/k) for pile in piles) <= h`. Monotone because a larger `k` never increases per-pile hours, so total hours is non-increasing in `k`.
> Return: post-loop `lo` is the smallest rate satisfying the predicate — the minimum eating speed.
> Why not brute force: trying `k = 1, 2, ..., max(piles)` linearly is `O(n · max(piles))`; binary-searching `k` is `O(n log max(piles))`, exponentially better.

Five write-ups, five memos. By the fifth, the cadence is automatic.

---

## Per-problem rubric

Each write-up's grade comes from four axes:

| Axis | Weight | "Great" looks like |
|------|------:|--------------------|
| 30-second memo at the top | 30% | Six lines, all required elements named, hits cadence on read-aloud (≤30s) |
| Match section (expanded body) | 25% | Explicit comparison against at least one other variant; explicit rejection of one wrong pattern (e.g., "not parametric because the predicate is not monotone" or "not classic because the array is unsorted") |
| Implement + Review | 20% | Clean code; trace on at least two examples; one common bug called out and avoided |
| Evaluate (five-piece from W2) | 15% | Time / space / best-avg-worst / tradeoff / improvement, with the `O(log n)` or `O(n log M)` defense sentence |
| Cross-references | 10% | Each write-up links to the relevant lecture section and at least one *other* mini-project write-up |

A grade of "great" on all five write-ups is the bar.

---

## The five problems

### Problem 1 — Classic Binary Search (LeetCode 704)

**Spec.** Given a sorted (ascending) array of distinct integers and a target, return the index of the target or `-1` if absent.

**Why included.** The textbook variant. Your memo must make the **closed-interval convention** explicit in one sentence.

**Stretch in your write-up:** compare against Drill 2's lower-bound (find-first) variant. Same family, different boundary convention; the comparison forces you to articulate why you chose closed for "find any" and half-open for "find first." This is the **boundary-defense** skill the rubric grades.

### Problem 2 — Find Minimum in Rotated Sorted Array (LeetCode 153)

**Spec.** Given a rotated sorted array of distinct integers, return the minimum element. Solve in `O(log n)`.

**Why included.** A natural follow-up to Drill 3 (search rotated). The trick: at each midpoint, decide whether the minimum lies in `[lo, mid]` or in `(mid, hi]` by comparing `arr[mid]` with `arr[hi]`. If `arr[mid] > arr[hi]`, the minimum is in the right half; else it is at or before `mid`.

**Stretch in your write-up:** compare against Drill 3. Drill 3 *finds a target* in a rotated array (variant 1 with "which half sorted?"); this one *finds the pivot value* using a different predicate (`arr[mid] > arr[hi]`). The shapes are related but distinct — name the relationship.

### Problem 3 — Search Insert Position (LeetCode 35)

**Spec.** Given a sorted array of distinct integers and a target, return the index where the target would be inserted to keep the array sorted (or its current index if present). This is the canonical "lower bound" problem.

**Why included.** The cleanest exercise of the half-open convention. Your memo must explicitly call out that this is variant 2 (lower bound) and that the return value is `lo` from the post-loop.

**Stretch in your write-up:** explicitly compare against `bisect.bisect_left`. Why do interviewers ask candidates to *write* the loop instead of using the library? Answer: because the writing exercises boundary discipline. Mention this in your Evaluate section as the interview-meta point.

### Problem 4 — Koko Eating Bananas (LeetCode 875) — PARAMETRIC

**Spec.** (Same as Drill 5.) Find the minimum integer eating rate `k` such that Koko finishes all piles within `h` hours.

**Why included.** The canonical parametric problem. Your write-up must add at least three things over Drill 5's write-up:

1. **A monotonicity proof** longer than one sentence — work it out for a specific example showing `feasible(3) → False, feasible(4) → True, feasible(5) → True`.
2. **A failure-mode example** — what happens with the wrong `hi` bound? Walk through what the algorithm does if you mistakenly use `hi = sum(piles)` (works but slower) or `hi = max(piles) // h` (wrong; misses the answer).
3. **A compare-to-Problem-5 paragraph** — Koko is "minimize the threshold"; Problem 5 (Aggressive Cows) is "maximize the threshold." Same template, mirrored predicate. Name the structural parallel.

### Problem 5 — Magnetic Force / Aggressive Cows (LeetCode 1552) — PARAMETRIC

**Spec.** You are given an integer array `position` and an integer `m`. `m` balls (cows) must be placed in baskets at positions `position[i]`, with **at most one ball per basket**. The *magnetic force* between two balls at positions `x` and `y` is `|x - y|`. Find the placement that **maximizes the minimum** magnetic force over all pairs. Return that maximum minimum force.

**Why included.** The canonical *maximize-the-minimum* parametric problem — the structural mirror of Koko. The predicate is `can_place(d) = (we can place m balls with all pairwise distances >= d)`, monotone in *the opposite direction* from Koko's: as `d` increases, eventually `can_place(d) = False`. So we search for the **largest** `d` with `can_place(d) = True` — the upper-bound mirror of the parametric template.

**The technique.** Sort `position`. Predicate `can_place(d)`: greedy from the leftmost basket; place a ball there; place the next ball in the leftmost basket at distance `>= d` from the previous; continue. Return `count >= m`. This is `O(n)` per call. Search interval: `[1, position[-1] - position[0]]`. Use the **upper-bound** template (round-up mid, `lo = mid` on True, `hi = mid - 1` on False).

**Why this matters.** Maximize-the-minimum is the second of the four parametric shapes (Pattern C from Lecture 2 §8). Most candidates can do Pattern A (Koko's minimize-the-maximum / minimize-the-threshold) after some practice; Pattern C catches them out because the boundary direction is flipped. After this problem, you have practiced both directions and the four-element cadence is robust.

**Acceptance:**

- The 30-second parametric memo at the top.
- Explicit statement of which template (lower-bound or upper-bound) you use, and why the predicate's monotonicity-direction forces that choice.
- A worked example: `position = [1, 2, 4, 8, 9]`, `m = 3` → answer 3. Trace `can_place(3)` to confirm it returns True (place at 1, 4, 8 or 1, 4, 9), and `can_place(4)` returns False.

---

## File-level template

Each problem write-up follows this skeleton. Save as `problem-NN-<slug>.md`.

```markdown
# Problem NN — <name> (<LC reference>)

> **30-second pattern-recognition memo [optional: (parametric)]:**
> [six lines as above]

## Problem

[Spec + 2-3 examples.]

## Why this variant

[1 paragraph: what makes this variant distinct from the others in the family.]

## UMPIRE write-up

### Understand
### Match
[Expanded body — comparison against at least one other variant.]
### Plan
### Implement
[Code with brief inline narration.]
### Review
[Trace on 2 examples + 1 common bug avoided.]
### Evaluate
[5-piece from W2; with the time-defense sentence cleanly delivered.]

## Cross-references

- Lecture: [link]
- Drill: [link, if applicable]
- Related mini-project problem: [link to another problem in this folder]

## What I would do differently next time

[Optional but recommended: 1-2 sentences.]
```

---

## Acceptance criteria

- [ ] All five write-ups present in `umpire-writeups/c2-week-05/mini-project/`.
- [ ] Each write-up has a leading 30-second memo following the schema above.
- [ ] **Problems 4 and 5 use the parametric memo schema** (four-element cadence), not the classic schema.
- [ ] Problem 5 explicitly states which boundary template (lower-bound or upper-bound) and why.
- [ ] Each write-up has a trace on at least two examples in the Review section.
- [ ] Each write-up cross-references at least one other write-up in this folder.
- [ ] All five `.py` solution files are present and pass their respective test cases.

---

## Suggested order of operations

### Thursday — drafting (1.5h)

1. Open the mini-project folder. Create six empty files (the five problem write-ups + the README).
2. For each problem, write only the **30-second memo** at the top. Do not write the rest yet. Read each memo aloud; sharpen until it hits 25-30 seconds.
3. Commit "Mini-project memos drafted."

### Friday — Problems 1, 2, 3 (3h)

4. Write up Problems 1, 2, 3. These are classic variants and should be fast after the drills.
5. For each, trace at least two examples in Review.
6. Commit each as you finish.

### Saturday — Problems 4, 5 (3h)

7. Problem 4: adapt Drill 5's write-up but add the three things demanded above (monotonicity proof, failure-mode example, compare-to-Problem-5 paragraph).
8. Problem 5: this is *new* — derive the algorithm from scratch using Lecture 2's three-step recipe. Allow 90 minutes for the first attempt.
9. Re-read all five memos aloud one last time. Sharpen anything that runs over 30 seconds.

### Sunday — polish + push (0.5h)

10. Add cross-references (each write-up links to ≥1 other).
11. Score yourself against the per-problem rubric. If anything is "vague" or "missing the boundary defense," sharpen it.
12. Push.

---

## What "great" looks like (final rubric)

A learner who has shipped this mini-project *well* has:

- All five memos under 30 seconds when read aloud.
- **Both parametric memos** explicitly state the monotonicity claim in one sentence.
- Problem 5's boundary template choice (lower-bound vs upper-bound) is explicitly justified by the monotonicity direction.
- At least one "why not [alternative]" rejection per write-up.
- Cross-references that form a small navigable web (Problem 4 ↔ Problem 5, Problem 1 ↔ Problem 3, etc.).

A learner who has shipped this mini-project *poorly* has:

- Memos that run 60+ seconds — too verbose, missing the cadence.
- Parametric memos without an explicit monotonicity claim.
- Problem 5 written as if it were Pattern A (Koko-style); failing to recognize the maximize-the-minimum mirror.
- No cross-references; each write-up reads as a stand-alone with no awareness of the others.

If you catch yourself producing the "poorly" shape, the fix is to re-read Lecture 2 §8 (the four parametric patterns) and re-do Problem 5 from scratch.

---

## Why five problems specifically

Two reasons.

1. **Three classic + two parametric is the diet of a real binary-search interview.** A Phase-2 onsite typically asks one classic and one parametric variant. Five problems gives you 5x at-bats on the memo cadence and 2x at-bats on the parametric four-element form — enough for the muscle memory to install, not so many that the artifact bloats.

2. **The syllabus mandates exactly this composition.** From the Week 5 line in `SYLLABUS.md`: *"Mini-project: Solve 5 binary-search problems including 2 'search on answer' variants."* The composition is the contract.

If you finish before Sunday with energy to spare, add a Problem 6 from the LeetCode Binary Search tag at your discretion. The acceptance criterion is *five* — anything beyond is bonus.

---

When done: push everything, then move on to [Week 6 — Graphs Part 1: BFS](../../week-06/).

Phase 2's first week is closed. Your portfolio now contains five canonical binary-search write-ups; that section will be referenced again in Mock #2 (Week 9) and in the capstone (Week 15).
