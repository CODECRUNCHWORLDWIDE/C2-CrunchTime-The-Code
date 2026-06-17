# Mini-Project — Re-do Week 1's Five Drills With Full Complexity Sections

> The first *retrospective* mini-project of the course. You will go back to your five Week 1 UMPIRE write-ups and **upgrade** them to Week-2 quality — specifically, rewriting every *Evaluate* section to follow the five-piece structure introduced in Lecture 3.

**Estimated time:** 5-7 hours, split across Thursday-Saturday.

The mini-project this week is small in *new* lines of code (you write none) but large in *editorial* polish. The artifact: a Week-1 portfolio that looks like Week-2 quality. That visible "before/after" matters when a hiring manager scrolls through your repo and sees the trajectory.

---

## Why this matters

Two reasons.

1. **The Evaluate skill is the rubric's *engineering judgment* axis.** Last week we skimmed it because UMPIRE itself was new. This week we make it deep. Going back and *upgrading* old work demonstrates the kind of "I learned something; I applied it backwards" engineering thinking that is rare and impressive.

2. **You will see your own progress.** Reading your Week 1 Evaluate sections cold, after a week of complexity drills, will be a small shock. They are terse, often missing the space discussion, never mentioning tradeoffs. That gap *is* what you learned this week. Closing it visibly is what makes a portfolio compounding.

---

## What you ship

Five files, edited (not added):

```
umpire-writeups/c2-week-01/
├── drill-01-reverse-string.md           ← rewrite Evaluate section
├── drill-02-valid-palindrome.md         ← rewrite Evaluate section
├── drill-03-two-sum-sorted.md           ← rewrite Evaluate section
├── drill-04-remove-duplicates.md        ← rewrite Evaluate section
└── drill-05-container-with-most-water.md ← rewrite Evaluate section
                                            (this one is also Homework #3;
                                             cross-link, don't duplicate)
```

Plus one new file:

```
umpire-writeups/c2-week-02/
└── retrospective.md                     ← short summary of what changed and why
```

---

## The five-piece Evaluate structure (from Lecture 3)

Every Evaluate section in your portfolio from this week forward looks like this:

```markdown
## E — Evaluate

**Time complexity.** Each iteration is O(_) on the [data structure];
n iterations total → **O(_) total time**, because [reason].

**Space complexity.** I allocate [data structure / variables] of size at most
[bound] → **O(_) auxiliary space**.

**Best / average / worst.** [Only if they differ meaningfully — most often
relevant for hash-map operations, sort-like algorithms, or early-termination.]

**Tradeoffs.**
- Alternative 1: [approach name] — O(_)/O(_). Wins when [_].
- Alternative 2 (if relevant): [approach name] — O(_)/O(_). Wins when [_].
- I chose [my approach] because [reason — usually one of: faster, smaller
  memory, simpler to reason about, preserves indices, sorted input].

**Improvement.** [Either: "No improvement obvious; we're at the lower bound."
Or: "Could improve to O(_) if [_]; I didn't because [_]."]
```

That structure, when spoken out loud, takes about two minutes. When written in Markdown, takes about half a page. Both are the right amount.

---

## Per-drill rewrite targets

You're not rewriting the whole drill. Just the Evaluate section. But each drill has *specific* tradeoffs you should now name explicitly.

### Drill 1 — Reverse String In Place

The Week-1 Evaluate said something like "O(n) time, O(1) space." That's *correct* but *thin*.

Week-2 upgrade:
- **Time:** O(n/2) = O(n) — n/2 swaps, each O(1).
- **Space:** O(1) — two integer pointers; Python's tuple-swap idiom is internally O(1).
- **Tradeoff:** `s[::-1]` would work in one line but uses **O(n) extra space** (slicing creates a new list). The drill specifies in-place, so the two-pointer version is the right choice on the space axis.
- **Improvement:** None. Reading every element is the lower bound.

### Drill 2 — Valid Palindrome

Week-2 upgrade:
- **Time:** O(n) — each character visited at most twice (once by `left`, once by `right`).
- **Space:** O(1) — two pointers, one comparison.
- **Tradeoff:** A "preprocess and compare" approach (strip non-alphanumeric, lowercase, check `s == s[::-1]`) is O(n)/O(n). The two-pointer version is strictly better on space.
- **Improvement:** None obvious.

### Drill 3 — Two Sum II (Sorted)

This is the most important rewrite this week — the version where the two-pointer-vs-hash-map decision is **explicit**.

Week-2 upgrade:
- **Time:** O(n) — each iteration moves one pointer toward the other.
- **Space:** O(1) — just two pointers and a sum.
- **Tradeoff:** Hash map version (Drill 1 of Week 2, the *unsorted* variant) is **O(n) time, O(n) space**. Two-pointer wins here on the space axis *because* the input is sorted. If the input weren't sorted, sorting first would cost O(n log n) — at which point the hash map's O(n) is strictly better on time.
- **Improvement:** Two-pointer is optimal for sorted input. No further improvement.

### Drill 4 — Remove Duplicates from Sorted Array

Week-2 upgrade:
- **Time:** O(n) — `read` pointer scans n times; `write` advances at most n times.
- **Space:** O(1) — in-place; two integer pointers.
- **Tradeoff:** A hash-set approach (collect uniques, copy back) is O(n)/O(n). The two-pointer version is strictly better on space. The set version is also unnecessary because the array is sorted — sortedness makes "is this a new element?" an O(1) check (compare to previous), not a hash-set lookup.
- **Improvement:** None obvious.

### Drill 5 — Container With Most Water

Week-2 upgrade:
- **Time:** O(n) — each iteration advances one pointer.
- **Space:** O(1) — three integers.
- **Tradeoff:** Brute-force "try every pair" is O(n²)/O(1). At n = 10⁵, O(n²) is 10¹⁰ ops — minutes. The greedy two-pointer choice (move the shorter side) saves us a complexity class.
- **Improvement:** O(n) is the lower bound for any algorithm that must inspect every height.
- **Best / average / worst:** The greedy invariant holds for all inputs, so the algorithm's runtime is *exactly* O(n), no spread.

(Reminder: Homework Problem 3 also covers this drill. Cross-link from the drill file to your homework write-up — don't duplicate.)

---

## The retrospective file

`umpire-writeups/c2-week-02/retrospective.md` — 200-400 words. The shape:

```markdown
# Week 2 retrospective — what changed in Week 1's drills

After Week 2's complexity work, I went back to my five Week 1 drill write-ups
and upgraded the Evaluate sections to the five-piece structure (time / space
/ best-avg-worst / tradeoff / improvement).

## What was missing before

- [list 2-4 things that were thin or absent — e.g., space complexity, tradeoff
  discussion, explicit comparison with alternative approach]

## What's better now

- [list 2-4 things — e.g., "every drill now names the alternative approach and
  why I rejected it"]

## What I'd do differently in Week 3 onward

- [list 1-3 things — e.g., "I'll write the five-piece Evaluate from the
  first draft, not as a retroactive edit"]

## Net effect on the portfolio

[One sentence: e.g., "Five drills, each readable in 5 minutes, each
demonstrating engineering judgment, not just code correctness."]
```

This file is *for you*, but it's also *for readers*. A hiring manager who reads it sees an engineer who reflects on their own output. That signal is rare and valuable.

---

## Acceptance criteria

- [ ] All five drill files edited in `umpire-writeups/c2-week-01/`. Each Evaluate section follows the five-piece structure.
- [ ] Each updated drill has a short comment at the top of the Evaluate section noting *"Rewritten in Week 2 to the five-piece structure."* — make the upgrade visible, don't hide it.
- [ ] `umpire-writeups/c2-week-02/retrospective.md` committed.
- [ ] At least 5 commits this week with meaningful messages (one per drill is fine — "Upgrade Drill 3 Evaluate section to five-piece structure" is a good message).
- [ ] Repository is *still public* and the README still renders cleanly.

---

## Suggested order of operations

### Thursday — Rewrite Drills 1, 2, 3 (2h)

1. Open Drill 1's write-up. Read the existing Evaluate section cold. Note what's thin.
2. Rewrite to the five-piece structure. Commit.
3. Same for Drill 2, Drill 3.

### Friday — Rewrite Drills 4, 5 + retrospective (2h)

4. Drill 4 rewrite. Commit.
5. Drill 5 rewrite — cross-link to Homework Problem 3. Commit.
6. Draft the retrospective. Commit.

### Saturday — Polish + push to peer (3h)

7. Read all five drills end-to-end. Are the Evaluate sections **consistent in shape**? They should be.
8. Polish the retrospective until it's specific (not generic).
9. Send the repo link to one peer. Ask: *"Reading my Week-1 drills now, can you tell I learned complexity in Week 2?"* If they say yes, you nailed it. If no, the upgrade isn't visible enough — make it more explicit.
10. Push.

---

## What "great" looks like (rubric)

| Criterion | Weight | "Great" looks like |
|-----------|------:|--------------------|
| Evaluate sections follow five-piece structure | 50% | Every drill, no exceptions, consistent shape |
| Tradeoff discussion is *specific* | 20% | Names the alternative approach with its complexity, not "there are tradeoffs" |
| Best-case / average-case discussed where relevant | 10% | At least one drill mentions the spread |
| Retrospective is specific, not generic | 10% | Names actual gaps in the old write-ups, not "I learned a lot" |
| Commits are meaningful | 10% | "Upgrade Drill 3 Evaluate" beats "update" |

---

## Why retrospective work matters

Most candidates accumulate work; the best candidates *upgrade* it. A portfolio with `c2-week-01/` looking just like `c2-week-02/` looking just like `c2-week-15/` is a portfolio that doesn't show learning — it shows a *constant* skill level over 15 weeks. That's not impressive. The portfolio you want shows clear, visible *upgrades*: Week 5 drills with sliding-window edge-case discussions that Week 3 drills couldn't have had; Week 10 system-design discussions that Week 5 problems couldn't have predicted.

This week's mini-project is the first instance of that pattern. Expect more.

---

When you're done: push, send the link to one peer for review, then move on to [Week 3](../../week-03/) (coming soon).
