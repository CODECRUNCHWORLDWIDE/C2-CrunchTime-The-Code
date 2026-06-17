# Mini-Project — Six Sliding-Window Write-Ups with 30-Second Pattern-Recognition Memos

> The week's deliverable: a single, compact portfolio artifact that demonstrates **Match-section fluency** across the six most-asked sliding-window problems. The 30-second memo per problem is the discriminating element — interviewers grade Match harder than candidates expect.

**Estimated time:** 7 hours, split across Thursday-Saturday.

This mini-project is *content-heavy* rather than *infrastructure-heavy*. You will produce six UMPIRE write-ups, each anchored by a 30-second pattern-recognition memo at the very top. The Match memos are the artifact's signature element; the rest of each write-up is standard UMPIRE.

---

## Why this matters

Two reasons.

1. **Match is the under-practiced step.** In Weeks 1–2 the *Implement* step got most of the attention because the patterns (two-pointer, hash map) were new. By Week 3 the implementation is increasingly mechanical; the *recognition* — naming the pattern in 30 seconds and stating the invariant — is where the interview points move. This mini-project is the first one in C2 that grades Match as strictly as Implement.

2. **Sliding window has more confusable sub-shapes than any earlier pattern.** Fixed vs variable. Shape A vs shape B vs shape C. Frequency vs sum vs set as state. Six write-ups that each *explicitly disambiguate* the sub-shape force you to articulate the differences out loud. By the sixth, the disambiguation is reflexive.

---

## What you ship

Seven files: six problem write-ups plus a short overview.

```
umpire-writeups/c2-week-03/mini-project/
├── README.md                                ← short overview + index
├── problem-01-fixed-window-max.md           ← fixed-size: max sum of k-subarray
├── problem-02-longest-no-repeat.md          ← variable shape A: longest unique substring
├── problem-03-find-anagrams.md              ← fixed-size + frequency invariant
├── problem-04-min-subarray-sum.md           ← variable shape B: shortest with sum ≥ target
├── problem-05-longest-at-most-k-distinct.md ← variable shape A: at-most-K-distinct template
└── problem-06-min-window-substring.md       ← variable shape B + need/formed invariant
```

Each write-up is the full UMPIRE format from Week 1, **plus a leading 30-second pattern-recognition memo at the top**.

Drills 1, 2, 4, 5 from this week overlap with problems 1, 2, 4, 5 of the mini-project on the *underlying problem*. You may **adapt** your drill write-ups for those problems — but the mini-project write-ups must add the 30-second memo, sharpen the Match section, and explicitly compare the sub-shape against at least one *other* sub-shape from the family. (Reusing a drill write-up verbatim is not acceptable; mini-project write-ups are graded against a stricter rubric.)

Problems 3 and 6 are *new* relative to the drills.

---

## The 30-second pattern-recognition memo (the signature element)

At the top of every write-up, immediately after the title, place a single bordered block in this exact shape:

```markdown
> **30-second pattern-recognition memo:**
> This is a sliding-window problem because [contiguity signal from the prompt].
> The window is [fixed-size with k = ... / variable-size].
> The shape is [fixed / A "longest" / B "shortest" / C "count"], because [signal].
> The invariant is: [property maintained at every iteration].
> The auxiliary state is: [sum / Counter / set / Counter + need-formed].
> Why not [alternative]: [one sentence].
```

Five lines, optionally six (the negative-space sentence). Read aloud, it takes 25-30 seconds. That is the cadence at which a senior interviewer wants to hear Match.

Example for the *longest substring without repeating characters* problem:

> **30-second pattern-recognition memo:**
> This is a sliding-window problem because the prompt asks for the longest contiguous substring with a property.
> The window is variable-size; the length is the answer.
> The shape is A "longest," because we shrink while the invariant is broken.
> The invariant is: every character inside `s[left..right]` is unique.
> The auxiliary state is: a dict mapping each character to its most recent index in the window.
> Why not hash map alone: hash maps without the window structure can't track "distinct *within a contiguous slice*" in O(n).

Six write-ups, six memos. By the sixth, the cadence is automatic.

---

## Per-problem rubric

Each write-up's grade comes from four axes:

| Axis | Weight | "Great" looks like |
|------|------:|--------------------|
| 30-second memo at the top | 30% | Five lines, all five elements named, hits cadence on read-aloud |
| Match section (expanded body) | 25% | Explicit comparison against at least one other sub-shape; explicit rejection of one wrong pattern (e.g., "not two-pointer because...") |
| Implement + Review | 20% | Clean code; trace on at least two examples; one common bug called out and avoided |
| Evaluate (five-piece from W2) | 15% | Time / space / best-avg-worst / tradeoff / improvement, with the amortized-O(n) defense sentence |
| Cross-references | 10% | Each write-up links to the relevant lecture section and at least one *other* mini-project write-up |

A grade of "great" on all six write-ups is the bar.

---

## The six problems

### Problem 1 — Maximum Sum of K-Length Subarray

**Spec.** Given an integer array `nums` and an integer `k`, return the maximum sum of any contiguous subarray of length `k`. Return 0 if `k > len(nums)`.

**Why included.** The simplest fixed-size sliding window. Your memo should make the fixed-size signal obvious in one sentence.

**Stretch in your write-up:** compare against Drill 1 (window *averages*). Same loop structure, different combine step (max vs each-value-pushed-to-list). Note the structural reuse.

### Problem 2 — Longest Substring Without Repeating Characters

**Spec.** Given a string `s`, return the length of the longest substring without repeating characters.

**Why included.** The canonical variable-size shape A. If you can deliver this memo cleanly, you can deliver the family.

**Stretch in your write-up:** explicitly walk *why* this is shape A, not shape B. (Hint: longest vs shortest.)

### Problem 3 — Find All Anagrams in a String

**Spec.** Given two strings `s` and `p`, return a list of starting indices in `s` where a permutation of `p` begins as a substring.

**Why included.** Fixed-size + frequency invariant. Drill 3 returned a boolean; this returns *all* indices. The window mechanics are identical; the *combine* step differs.

**Stretch in your write-up:** compare with Drill 3's `check_inclusion`. Same window, same invariant, different return type. State the relationship explicitly.

### Problem 4 — Minimum Size Subarray Sum

**Spec.** Given positive integers `nums` and integer `target`, return the minimum length of a contiguous subarray with sum at least `target`. Return 0 if impossible.

**Why included.** The canonical variable-size shape B. Your memo must explicitly name "shape B, shrink while property holds, record inside the shrink."

**Stretch in your write-up:** explicitly explain the positivity requirement and what would change if negatives were allowed.

### Problem 5 — Longest Substring with At Most K Distinct Characters

**Spec.** Given a string `s` and integer `k`, return the length of the longest substring containing at most `k` distinct characters.

**Why included.** The general at-most-K-distinct template. Drill 5 (fruit baskets) specialized it to K=2; this is the general case.

**Stretch in your write-up:** show how `K=2` recovers Drill 5 verbatim. The template's value is its parameterizability.

### Problem 6 — Minimum Window Substring

**Spec.** Given strings `s` and `t`, return the minimum-length contiguous substring of `s` that contains every character of `t` (counting multiplicities). Return `""` if none.

**Why included.** This is *the* hard sliding-window problem of the standard interview canon. The mini-project's culminating write-up. Your memo must name the `need/formed` integer invariant in one sentence.

**Stretch in your write-up:** explicitly compare against Problem 3 (find anagrams). Same family — frequency invariant — but Problem 3 has a fixed window size, while Problem 6 has a variable-size shape B. Show the lineage.

---

## Acceptance criteria

- [ ] All six write-ups committed in `umpire-writeups/c2-week-03/mini-project/`.
- [ ] Each write-up has the **30-second memo at the top** in the exact block format above.
- [ ] Each write-up has all six UMPIRE sections (Understand, Match, Plan, Implement, Review, Evaluate).
- [ ] Each Evaluate section follows the **five-piece structure** from Week 2.
- [ ] Each Evaluate section includes the **amortized-O(n) defense sentence** for the variable-size shape, or the equivalent O(n) defense for the fixed-size case.
- [ ] The mini-project `README.md` is the index file linking to all six.
- [ ] At least six commits this week with meaningful messages (one per write-up is fine — *"Add mini-project problem 4: min size subarray sum"* is a good message).
- [ ] Repository is **still public** and the README still renders cleanly.

---

## Suggested order of operations

### Thursday — Problems 1, 2, 3 (2.5h)

1. Open the Drill 1 write-up. Read your existing Match section cold. Note what's thin.
2. Write the 30-second memo block for Problem 1. Read it aloud; time yourself.
3. Adapt the rest of Drill 1's write-up into Problem 1's. Commit.
4. Repeat for Problem 2 (adapt Drill 2). Commit.
5. Problem 3 (Find All Anagrams) is new. Implement, write up, commit.

### Friday — Problems 4, 5, 6 (3h)

6. Problem 4: adapt Drill 4. Commit.
7. Problem 5: adapt the at-most-K-distinct template from Lecture 2 §5. (Drill 5 specialized to K=2; this is the general K version.) Commit.
8. Problem 6: this is the hard one. Implement from scratch using the `need/formed` template. Trace on at least three test cases. Commit.

### Saturday — Polish + memo audit (1.5h)

9. Read all six write-ups end to end. **Are the six 30-second memos consistent in shape?** They should be — same six-line block, same cadence on read-aloud.
10. Read each memo aloud, with a stopwatch. Each should land in 25–30 seconds. If any is over 40 seconds, tighten it.
11. Write the mini-project `README.md` index. Cross-link each problem to its corresponding drill (if any), to the relevant lecture section, and to at least one other problem in this mini-project (for the "compare with X" stretch).
12. Send the repo link to one peer. Ask: *"Read my six Match memos out loud back to me. Do they all sound like the same person on the same week?"* If the answer is yes, you've shipped a coherent artifact. If no, you have inconsistency to clean.

---

## The mini-project README index

Suggested shape:

```markdown
# Week 3 — Sliding Window Mini-Project

Six sliding-window write-ups, each anchored by a 30-second pattern-recognition memo.

| # | Problem | Sub-shape | Auxiliary state |
|---|---------|-----------|-----------------|
| 1 | [Max sum of k-subarray](problem-01-fixed-window-max.md) | Fixed-size | Running sum |
| 2 | [Longest no-repeat substring](problem-02-longest-no-repeat.md) | Variable A (longest) | `dict` of last-seen indices |
| 3 | [Find all anagrams](problem-03-find-anagrams.md) | Fixed-size + frequency | Counter pair |
| 4 | [Min size subarray sum](problem-04-min-subarray-sum.md) | Variable B (shortest) | Running sum |
| 5 | [Longest at-most-K distinct](problem-05-longest-at-most-k-distinct.md) | Variable A (longest) | Counter |
| 6 | [Minimum window substring](problem-06-min-window-substring.md) | Variable B + frequency | Counter + need/formed |

## What this project demonstrates

- Match-section fluency: every problem's pattern is named in the first 30 seconds.
- Sub-shape discrimination: fixed vs variable; longest vs shortest vs count; sum vs frequency vs set as state.
- Negative-space pattern rejection: at least one wrong pattern explicitly rejected per write-up.
```

That index, with your six links, is the second-most-important artifact of the week (after the six memos themselves).

---

## What "great" looks like (rubric)

| Criterion | Weight | "Great" looks like |
|-----------|------:|--------------------|
| Six 30-second memos consistent in shape | 35% | Same six-line block at the top of every write-up; same cadence on read-aloud |
| Sub-shapes correctly named | 20% | Every memo correctly identifies fixed/variable A/B/C |
| Match sections compare against alternatives | 15% | Each names at least one "why not X" rejection |
| Evaluate sections include amortized-O(n) defense | 15% | Every variable-size write-up has the sentence from Lecture 1 §6 |
| Cross-references present | 10% | Each problem links to a drill (if any), a lecture section, and one other mini-project problem |
| Commits are meaningful | 5% | "Add mini-project problem 4" beats "update" |

---

## Why six, not five?

Five would be enough to cover the sub-shapes. The sixth (Minimum Window Substring) is the **discriminator**. Most candidates can write the first five with care; the sixth is what proves the pattern is in muscle memory rather than memorized as a checklist. If you can deliver the sixth memo *cleanly* — including the `need/formed` invariant in one sentence — you have demonstrated something the average candidate can't.

---

When you're done: push, send the link to one peer for review, then move on to [Week 4 — Fast-and-Slow Pointers](../../week-04-fast-and-slow-pointers/) (coming soon).
