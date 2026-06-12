# Mini-Project — Mock #3 Recorded + XOR-Trick & Trie Write-Ups

> The week's deliverable, the **third inflection point** of C2 · CrunchTime — The Code. A recorded Mock #3 under near-real conditions is the centerpiece; two compact pattern write-ups — one XOR-trick, one trie — frame it and prove the week's two patterns are in your hands. The mock is the checkpoint; the write-ups are the content.

**Estimated time:** the mock plus its self-feedback dominate the week (see the [schedule](../README.md#weekly-schedule-intensive--36h)); the two write-ups are ~3 hours, split Wednesday–Saturday.

This mini-project has two halves that share a week but serve different ends. The **Mock #3** half is *experience-heavy* — a 45-minute recording plus a structured self-feedback note that grades the recording honestly and tracks the trend across all three mocks. The **write-up** half is *content-heavy* — two UMPIRE write-ups that demonstrate fluency on the two Week-14 patterns. Ship both.

---

## Why this matters

Three reasons.

1. **Mock #3 is the near-real rehearsal.** Mock #1 (Week 4) was the baseline and was solo-eligible. Mock #2 (Week 9) measured the Phase-2 ramp. Mock #3 removes the last softenings: peer or platform required, uncurated prompt, **no peeking**. It is the closest the course comes to a real onsite before the Phase-2 capstone Mock #4. The data — does your Match memo hold under an unseen prompt with no safety net — is irreplaceable.

2. **The two write-ups close the last recognition gaps in C2.** Bit manipulation and tries-at-speed are the long tail of the syllabus: narrow, high-yield, and exactly the patterns an unprepared candidate has never drilled. One XOR-trick write-up and one trie write-up prove both are installed.

3. **The trend line is the new analytical skill.** With three recordings in hand, the question shifts from "how did this mock go" to "which direction is the line moving." The self-feedback note this week explicitly grades the Mock #1 -> #2 -> #3 deltas on four axes. That meta-skill — measuring your own improvement quantitatively — is what separates a candidate who *practices* from one who *improves*.

---

## What you ship

Two groups: the Mock #3 artifacts and the two pattern write-ups.

```
mocks/
└── mock-03/
    ├── recording-link.md           # link to the video (URL; the file is too big to commit)
    ├── immediate-notes.md          # 5-minute brain dump + the "no peeking" precommitment line
    └── timestamps.md               # pass-1 timestamps from watching the recording

umpire-writeups/c2-week-14/
├── mock-03-self-feedback.md        # the structured self-feedback, 700-900 words, with the trend-line section
└── mini-project/
    ├── README.md                   # short overview + index + reflection
    ├── problem-01-xor-trick.md      # an XOR-trick write-up (Single Number III, LC 260)
    └── problem-02-trie.md           # a trie write-up (Add and Search Word, LC 211)
```

`recording-link.md` is a one-line file:

```markdown
# Mock #3 recording

[Video — 45 min](https://drive.google.com/file/d/.../view) (private link, view-only)

Problem: [problem name + LeetCode link]
Flavor: A (peer) / B (Pramp / interviewing.io)
Date: YYYY-MM-DD
```

Do **not** commit the raw video; host it on Google Drive, Loom, or unlisted YouTube and commit the link.

The two write-ups are chosen so that:

- **Problem 1 (XOR-trick):** Single Number III (LC 260) — the two-single-numbers partition. The discriminator is the partition-by-a-distinguishing-bit move: XOR the array to get `a ^ b`, isolate a set bit with `x & -x`, partition, XOR each half. Naming *why* `a` and `b` land in different groups is the senior move.
- **Problem 2 (trie):** Add and Search Word (LC 211) — a trie with a wildcard branching walk. The Match move is recognizing that the `.` wildcard forces a recursive walk over all children, not a single-path descent.

---

## The 30-second pattern-recognition memo (the signature element)

At the top of each write-up, immediately after the title, place a single bordered block.

### For Problem 1 (XOR-trick — Single Number III)

```markdown
> **30-second pattern-recognition memo (XOR-trick — Single Number III):**
> Two elements appear once, all others twice; constant space. XOR the whole
> array -> a ^ b (duplicates cancel). Since a != b, a ^ b has a set bit where
> they differ; isolate the lowest one with x & -x. Partition the array by that
> bit: a and b land in different groups, every duplicate pair lands in the same
> group. XOR each group to recover one unique number per group. O(n) time,
> O(1) space. Why not a hash map: O(n) space, forbidden.
```

### For Problem 2 (trie — Add and Search Word)

```markdown
> **30-second pattern-recognition memo (Trie + wildcard — Add and Search Word):**
> Prefix-tree with a '.' wildcard that matches any single character. add is a
> plain trie insert. search is a recursive walk: at a normal character, descend
> the one matching child; at '.', recurse into ALL children and OR the results;
> at end-of-word, return is_end. O(L) for a wildcard-free query; up to O(26^L)
> worst case for an all-'.' query, but sparse branching prunes it in practice.
> Why a trie over a set: the set cannot do prefix or wildcard matching.
```

Read each aloud; both should hit 25–30 seconds.

---

## UMPIRE structure for each write-up

Each problem's write-up follows the full UMPIRE format (the same six-section format from Week 1), plus the leading 30-second memo.

### Understand (~150 words)

Restate the problem in your own words. Confirm input/output format, constraints, edge cases. For Single Number III, confirm: exactly two elements are unpaired; all others appear exactly twice; constant extra space is required. For Add and Search Word, confirm: `add` stores a word; `search` may contain `.` matching any single character; an exact match requires reaching a terminal.

### Match (~200 words)

The 30-second memo *plus* a longer paragraph: the tell that selects the pattern, the technique (partition-by-a-bit for Problem 1; wildcard branching walk for Problem 2), one non-pattern alternative and why it is worse (hash map for Problem 1; per-query linear scan for Problem 2), and the complexity claim with derivation.

### Plan (~120 words)

Numbered steps mapping 1:1 to the code. For Problem 1: XOR all, isolate a bit, partition, XOR each group. For Problem 2: define the node; `add` walks/creates and marks `is_end`; `search` recurses, branching on `.`.

### Implement (~350 words including code)

Working, tested code with type hints, docstrings, and PEP 8 style. Both must be correct on the LC sample cases.

### Review (~200 words)

Trace each on a small example by hand. For Single Number III, walk `[1, 2, 1, 3, 2, 5]` showing `a ^ b = 6`, `diff_bit = 2`, partition recovering `3` and `5`. For Add and Search Word, walk a `.`-query showing the branching recursion.

### Evaluate (~200 words)

Time and space with derivation. One variant or alternative. One trade. **Cross-reference to the Mock #3 experience:** did either of these two patterns (or a relative) appear in your Mock #3 prompt? If so, how did you do on it live, and what does that say about whether the pattern is truly installed?

---

## The starter files

Two starter files are provided for the *code* portion of the write-ups. **They are spec stubs, not working solutions.** You implement the bodies.

| File | Pattern | Functions to implement |
|------|---------|------------------------|
| [problem-01-xor-trick-starter.py](./problem-01-xor-trick-starter.py) | XOR-trick | `single_number_iii` |
| [problem-02-trie-starter.py](./problem-02-trie-starter.py) | Trie + wildcard | `WordDictionary.add_word`, `WordDictionary.search` |

Each starter has a self-test block with LC sample cases. Run `python3 problem-01-xor-trick-starter.py` after implementing.

---

## How the deliverable is graded

| Dimension | Weight | What "yes" looks like |
|-----------|-------:|----------------------|
| Mock #3 recorded under near-real conditions | 30% | 45-min recording, peer/platform, uncurated prompt, no-peeking honored (or honestly flagged if not) |
| Mock #3 self-feedback + trend line | 25% | 700-900 words; the Mock #1 -> #2 -> #3 deltas graded on four axes; one testable behavior change for Mock #4 |
| Match (both write-ups) | 20% | Both memos in the canonical shape; both name the technique and reject one alternative |
| Implement (both write-ups) | 15% | All sample cases pass; type hints; docstrings; PEP 8 |
| Evaluate (both write-ups + Mock #3 cross-ref) | 10% | Complexity derivations; the cross-reference to whether the pattern appeared live in Mock #3 |

The Mock #3 half is the heavier weight (55% combined) because the near-real recording plus its trend-line analysis is the irreplaceable artifact this week.

---

## Reflection — the short README at the top of the deliverable

After both write-ups and the Mock #3 self-feedback are complete, draft a 300-word reflection at the top of `umpire-writeups/c2-week-14/mini-project/README.md`. Answer three questions:

1. **Which Week-14 pattern was harder to recognize, bit manipulation or tries?** Most learners find tries easier (the prefix tell is loud) and XOR-cancellation harder to *invent* under pressure. The senior reflection identifies why — typically because the bit tricks must be *memorized* rather than *derived*, unlike a trie which falls out of the prefix structure.
2. **Did your Mock #2 behavior change stick?** Pull the evidence from the Mock #3 recording. If it stuck, name where. If it did not, diagnose why and carry it into Mock #4. (See [Lecture 3 §8](../lecture-notes/03-the-mock-3-protocol.md).)
3. **What is the trend across your three mocks?** One sentence per axis (Match-memo tightness, silent-period shrinkage, recovery audibility, Evaluate completeness). The trend, not the snapshot, is what this checkpoint measures.

---

## Acceptance

The mini-project is shipped when:

- **Mock #3 is recorded** under near-real conditions (peer/platform, uncurated, no peeking) and uploaded; `recording-link.md`, `immediate-notes.md`, and `timestamps.md` are committed.
- **The self-feedback note** (`mock-03-self-feedback.md`, 700-900 words) is committed with the trend-line section and one specific, testable behavior change for Mock #4.
- **Both starter files** are implemented, all self-tests pass.
- **Both UMPIRE write-ups** are committed to `umpire-writeups/c2-week-14/mini-project/`, each with the 30-second memo and a recording >= 10 minutes.
- The reflection README is committed.
- The push log shows daily commits Wednesday–Saturday.

If you exceed 12 hours on the write-up half (excluding the mock), stop and request a 1:1 with the Phase-2 lead; the over-budget likely indicates a Match-step gap on bit manipulation.

---

## A note on pacing

Protect the Friday mock and the Saturday self-feedback at all costs — they are the irreplaceable artifacts. The two write-ups are the cheaper deliverable; if time is tight, write Problem 1 (XOR-trick) fully and abbreviate Problem 2 (trie), because the trie pattern is already in your portfolio from Week 9 while the partition-by-a-bit move is new this week.

If you ship everything under budget, the stretch is to record a **second, lower-stakes mock** earlier in the week (a Thursday warm-up) so that Friday's Mock #3 is your sharpest — alumni who ran a warm-up reported a visible quality lift. But never let the warm-up cannibalize the real Mock #3; the recorded, graded, trend-lined Friday mock is the deliverable.
