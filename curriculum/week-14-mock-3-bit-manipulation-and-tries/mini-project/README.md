# Mini-Project — Mock #3 Recorded, Plus an XOR-Trick and a Binary-Trie Write-Up

> The week's deliverable: the Mock #3 recording with a two-pass self-feedback note, plus two compact portfolio artifacts that demonstrate fluency across the highest-leverage Week-14 patterns — one XOR-trick write-up and one binary-trie write-up, each fully UMPIRE-narrated. The three pieces together are the proof that you can run a full mock under pressure *and* defend the two bit sub-shapes that matter most. The binary-trie write-up is the bridge artifact — it ties this week's bit work back to the Week 9 trie family.

**Estimated time:** 10 hours, split across Thursday–Saturday (Mock #3 on Friday).

This mini-project is *mock-centered*. The Mock #3 recording is the keystone; the two write-ups are the supporting evidence that the bit material is in your hands. All three are anchored by a 30-second pattern-recognition memo where applicable.

---

## Why this matters

Three reasons.

1. **Mock #3 is the first full-loop simulation.** A real onsite is three or four coding rounds plus a behavioral round (Week 13). Mock #3 is the first recorded mock run under *near-real conditions* — video on, hard 45-minute clock, no peeking — and the first chance to bolt the behavioral round onto the coding round (Lecture 3 §8). The recording, watched honestly, is the single highest-signal artifact in the portfolio.

2. **The trajectory across Mock #1 → #2 → #3 is what a senior reads.** Anyone can solve a problem once. The trait that predicts whether a candidate grows on the job is *self-correction* — naming a behavior change after each mock and actually making it. The self-feedback note's trajectory section is where you prove it.

3. **Bit manipulation is the last pattern, and the binary trie is the bridge.** The XOR-trick write-up locks in the algebra (cancellation); the binary-trie write-up locks in the structure (high bits dominate) and connects bit manipulation to the Week 9 trie family. Shipping one of each forces you to articulate that two completely different problem shapes use the same operator.

---

## What you ship

A Mock #3 artifact set plus two problem write-ups.

```
mocks/mock-03/
├── recording-link.md          ← link to the video (file too big to commit)
├── immediate-notes.md         ← 5-minute brain dump right after the clock stops
└── timestamps.md              ← pass-1 timestamps

umpire-writeups/c2-week-14/
├── mock-03-self-feedback.md   ← the two-pass self-feedback + trajectory section
└── mini-project/
    ├── README.md                              ← short overview + index + reflection
    ├── problem-01-xor-trick-single-number.md  ← XOR fold (Single Number, LC 136)
    └── problem-02-binary-trie-maximum-xor.md  ← binary trie (Maximum XOR, LC 421)
```

Each write-up is the full UMPIRE format from Week 1, **plus a leading 30-second pattern-recognition memo at the top**.

The two problems are chosen so that:

- **Problem 1 (XOR trick):** Single Number (LC 136), narrated as a demonstration of XOR's *algebra* — pairs cancel via `a ^ a == 0`, the survivor remains via `a ^ 0 == a`, order is irrelevant by commutativity and associativity. The discriminator is the constant-space defense: "the hash-map answer is `O(n)` space; the XOR fold is `O(1)`."
- **Problem 2 (binary trie):** Maximum XOR (LC 421), narrated as a demonstration of XOR's *structure* — high bits dominate magnitude, so insert MSB-first and greedily walk for the opposite bit. The discriminator is "the `O(n**2)` brute force is too slow; the binary trie is `O(n · 32)`," and the cross-reference to the Week 9 trie ("same dict-of-dict structure, alphabet `{0, 1}`").

Together they cover the bit family's two faces: algebraic cancellation and structural greedy search.

---

## The 30-second pattern-recognition memo templates

At the top of each write-up, immediately after the title, place a single bordered block.

### For Problem 1 (XOR trick)

```markdown
> **30-second pattern-recognition memo (XOR fold):**
> This is an XOR fold because [every element appears twice except one /
> I need to find the missing element with O(1) extra space].
> Why XOR: pairs cancel (a ^ a == 0), the survivor remains (a ^ 0 == a),
> order is irrelevant (commutative + associative).
> Time O(n), space O(1).
> Why not a hash map: [Counter is O(n) space; the constant-space constraint
> rules it out].
```

### For Problem 2 (binary trie)

```markdown
> **30-second pattern-recognition memo (binary trie):**
> This is a binary-trie problem because [I must maximize / query an XOR over
> a set of integers].
> Structure: a trie over the alphabet {0, 1}; insert each number MSB-first as
> a 32-bit path.
> Greedy walk: at each bit prefer the OPPOSITE bit's child (bit ^ opp == 1
> contributes to the XOR), falling back to the same bit if absent.
> Why MSB-first: high bits dominate the XOR magnitude; commit them first.
> Time O(n * 32), space O(n * 32). Why not brute force: O(n^2) is too slow.
> Bridge: this is the Week 9 dict-of-dict trie restricted to {0, 1}.
```

Read each aloud; both should hit 25–30 seconds.

---

## UMPIRE structure for each write-up

The full six-section format. The Match section opens with the 30-second memo above.

### Understand

Restate the problem in your own words. Walk one example by hand. Note the constraints. Specifically:

- Problem 1 — state the binding constraints (linear time, constant space) and why they rule out the hash-map answer.
- Problem 2 — state why the `O(n**2)` brute force is too slow for the constraints, and the structural insight that high bits dominate the XOR.

### Match

Open with the 30-second memo. Then in 2–3 sentences name the sub-shape (XOR fold / binary trie), the discriminating cue, and the rejected alternative (hash map for Problem 1; brute force for Problem 2).

### Plan

Numbered steps; 4–6 lines. State the data structure (none / the binary trie) first, the loop shape second, the termination third.

- Problem 1: seed an accumulator at 0; XOR every element; return it.
- Problem 2: build the trie MSB-first; for each number, greedy opposite-bit walk; track the max.

### Implement

The code. Type hints on every function. Docstrings on every public function. Comments only where the line is non-obvious — the binary trie's `want = 1 - bit` and the same-bit fallback deserve a comment; the XOR accumulator does not.

### Review

Trace each implementation by hand on at least two inputs: one positive case and one edge case (single element for both; for Problem 2 the edge is `[0]` → `0`).

### Evaluate

Time and space bounds **with derivation** — the derivation is mandatory, not the bound alone.

- Problem 1: `O(n)` time / `O(1)` space, derived from "one pass, one accumulator."
- Problem 2: `O(n · 32)` time / `O(n · 32)` space, derived from "n insertions of 32 bits, then n walks of 32 steps."

Mention at least one variant in each Evaluate. Problem 1: Single Number III (LC 260), which folds to `a ^ b` and partitions on a differing bit. Problem 2: the `O(n**2)` brute force, and a note that the trie generalizes to "max XOR with a constraint" variants (LC 1707).

---

## Cross-references between the two write-ups

The pair must be navigable. At minimum:

- The Problem 1 write-up cites Problem 2 in its Evaluate: "Compare to the binary-trie write-up — Single Number uses XOR's *algebra* (cancellation in a fold), while Maximum XOR uses XOR's *structure* (high bits dominate, so it needs a data structure). Same operator, two problem shapes."
- The Problem 2 write-up cites Problem 1 in its Match, and cites the Week 9 trie: "Unlike the XOR-fold problem, this cannot be solved by a one-line fold — the structure (high bits dominate) requires the binary trie, which is the Week 9 dict-of-dict trie restricted to the alphabet `{0, 1}`."

The cross-references earn senior signal — they show you navigate the *taxonomy* of the bit family, not just the individual templates.

---

## Rubric

The Mock #3 artifact and each write-up are graded. Total possible: 100; passing: **70 on each component**.

### Mock #3 rubric (the keystone)

| Dimension | Points | What "full credit" looks like |
|-----------|-------:|-------------------------------|
| Conditions held | 20 | Video on, hard 45-min clock, no peeking — verifiable from the recording |
| Two-pass review done | 20 | Pass-1 timestamps + pass-2 prescriptions both present |
| Self-feedback complete | 25 | All sections present; Match / thinking-aloud / recovery / Evaluate each graded |
| Trajectory section | 20 | Honest comparison across Mock #1 → #2 → #3; prior behavior changes assessed |
| One behavior change for Mock #4 | 15 | Specific and testable; not "be more confident" |

### Problem 1 (XOR trick) rubric

| Dimension | Points | What "full credit" looks like |
|-----------|-------:|-------------------------------|
| 30-second memo at the top | 10 | All lines present; the constant-space discriminator vs hash map stated |
| Understand | 10 | One example walked; the constraints that rule out the hash map stated |
| Match | 20 | XOR fold named; the four identities cited; hash map rejected with reason |
| Plan | 10 | Accumulator-and-fold sketched |
| Implement | 25 | Test cases pass; type hints; PEP 8; idiomatic Python |
| Review | 10 | Positive trace + single-element edge case |
| Evaluate | 15 | `O(n)`/`O(1)` derived; trade vs hash map; the Single Number III variant named |

### Problem 2 (binary trie) rubric

| Dimension | Points | What "full credit" looks like |
|-----------|-------:|-------------------------------|
| 30-second memo at the top | 10 | All lines present; the MSB-first / opposite-bit rule stated |
| Understand | 10 | One example walked; why brute force is too slow stated |
| Match | 20 | Binary trie named; greedy opposite-bit walk explained; brute force rejected |
| Plan | 10 | Insert MSB-first + greedy walk outlined |
| Implement | 25 | Test cases pass; MSB-first insertion correct; same-bit fallback present; type hints |
| Review | 10 | Positive trace + `[0]` edge case |
| Evaluate | 15 | `O(n · 32)` derived; brute-force trade; the Week 9 trie cross-reference present |

---

## Acceptance

The mini-project is complete when:

- The Mock #3 recording link, immediate notes, and pass-1 timestamps are committed under `mocks/mock-03/`.
- The Mock #3 self-feedback (with the trajectory section and one behavior change for Mock #4) is committed under `umpire-writeups/c2-week-14/`.
- Both problem write-ups are committed under `umpire-writeups/c2-week-14/mini-project/`, each with the 30-second memo at the top.
- The cross-references in both directions are present.
- Both implementations pass the test cases in the Week-14 exercise starters.

Push everything by Sunday end-of-day. Phase 4's second week is closed on the push.

---

## Self-reflection (in the mini-project README)

End `umpire-writeups/c2-week-14/mini-project/README.md` with a short reflection — 4–6 sentences — addressing:

1. Which sub-shape felt more natural — the XOR fold's algebra or the binary trie's structure? Why?
2. What was the hardest part of the binary trie to articulate aloud — the MSB-first insertion, or the opposite-bit greedy walk?
3. Looking at the trajectory across Mock #1 → #2 → #3: what is the one habit that has genuinely improved, and the one that is still your weakest going into Mock #4?

The reflection is the portfolio-grade artifact. Future you — the one walking into the real onsite — will thank present you for writing it.

---

## After the mini-project

Move on to [Week 15 — Capstone + Mock #4](../../week-15-capstone-and-mock-4/). The fourteen-pattern catalog is complete; Week 15 is the dress rehearsal — the capstone project and the final recorded mock, run as the full loop you simulated here for the first time.
