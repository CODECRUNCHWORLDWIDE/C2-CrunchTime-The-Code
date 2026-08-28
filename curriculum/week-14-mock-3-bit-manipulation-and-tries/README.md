# Week 14 — Bit Manipulation, Tries + Mock #3

```
┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐
│ U │  │ M │  │ P │  │ I │  │ R │  │ E │
└───┘  └───┘  └───┘  └───┘  └───┘  └───┘
```

> *Week 13 installed the behavioral skill set — the eight categories, the STAR structure, the twelve-story bank, the discipline of thinking aloud through an ambiguous prompt. Week 14 installs the last pure-algorithm pattern of the catalog — **bit manipulation** (pattern #13 of 14) — and threads it through the program's third recorded mock. The bit family is three sub-shapes: the **XOR fold** (a^a cancels, so the lone survivor is the answer — Single Number, Missing Number, Single Number III by partitioning on a differing bit); **bitmask-as-set** (enumerate every subset of n items by counting 0..2^n−1, the engine behind Subsets and the recognition-grade framing of bitmask DP); and **bit DP** (build a small answer from a smaller one, as in Counting Bits where `dp[i] = dp[i>>1] + (i&1)`). Then we close the loop with a **tries review** — the dict-of-dict and TrieNode templates from Week 9 — because the bridge between this week's two topics is the **binary trie** that solves Maximum XOR (LC 421). Mock #3 is the first full-loop simulation run under near-real conditions: video on, a hard 45-minute clock, no peeking. By Sunday you can recognize a bit problem in 30 seconds, fold an array with XOR, enumerate subsets with a bitmask, build a binary trie for max-XOR, and run a recorded mock that you watch back twice and turn into one specific behavior change versus Mock #1 and Mock #2.*

Welcome to Week 14 of **C2 · CrunchTime — The Code** — the second week of Phase 4, the capstone-and-onsite-prep block (Weeks 13–15). Last week installed the behavioral round. This week installs the final algorithm pattern in the fourteen-pattern catalog and frames the whole week as **Mock Interview #3** — the third of four recorded mocks, and the first one you run as a full loop under near-real conditions.

Bit manipulation has a peculiar place in the interview canon. It is rarely the *centerpiece* of a loop, but it shows up as the curveball — the "warm-up" that is anything but, the follow-up that the interviewer adds when you finish early, the systems-flavored question at an infrastructure or embedded team. Candidates who have never folded an array with XOR tend to reach for a hash map and an `O(n)` space answer when the interviewer wanted the `O(1)`-space XOR trick. Owning the three sub-shapes — XOR fold, bitmask enumeration, bit DP — and the binary-trie bridge to Maximum XOR is what turns the curveball into a clean, confident answer.

The tries review is deliberate. We are not re-teaching the trie from scratch — you built it in Week 9 in both the dict-of-dict and the `TrieNode` class forms. We are *re-activating* it, because the **binary trie** is the single structure that connects bit manipulation to tries: insert each number's 32-bit (or 31-bit) representation MSB-first as a path through a 2-way trie, then for each number greedily walk the trie choosing the opposite bit at every level to maximize the XOR. That is Maximum XOR of Two Numbers in an Array (LC 421), and it is the topic bridge of the week.

By Sunday of Week 14 you will:

- **Recognize** a bit problem in 30 seconds and classify it as **XOR-fold / bitmask-subset-enumeration / bit-DP / binary-trie / not-a-bit-problem**.
- **Fold** an array with XOR to find the lone unpaired element (Single Number, LC 136), the missing element (Missing Number, LC 268), and — by partitioning on a differing bit — the two unique elements (Single Number III, LC 260).
- **Manipulate** individual bits fluently: set / clear / toggle / test a bit with a mask, isolate the lowest set bit with `x & -x`, clear the lowest set bit with `x & (x - 1)`, and count set bits with `x.bit_count()` (Python 3.10+) and the Brian Kernighan loop.
- **Enumerate** every subset of `n` items by counting `0 .. 2**n - 1` and reading each integer as a membership bitmask (Subsets, LC 78), and iterate submasks of a mask.
- **Apply** the bit-DP recurrence `dp[i] = dp[i >> 1] + (i & 1)` to Counting Bits (LC 338), and recognize — honestly — when bitmask DP is the answer at the *recognition* level (Travelling Salesman, assignment problems) without being expected to write it cold.
- **Build** a binary trie of 32-bit integers and use the greedy opposite-bit walk to solve Maximum XOR of Two Numbers in an Array (LC 421) — the bridge between bits and tries.
- **Run** Mock #3 under near-real conditions — video on, a hard 45-minute clock, no peeking — record it, watch it back twice (1.5× then 1.0×), and write a self-feedback note that names **one** specific behavior change versus Mock #1 (W4) and Mock #2 (W9).
- Have solved **three bit exercises** — Single Number (XOR fold), Counting Bits (bit DP), Maximum XOR (binary trie) — each with a FRAME write-up.
- Have shipped **two challenges** — the Mock #3 timed round and the Sum of Two Integers (LC 371) full-FRAME write-up — plus the quiz, the homework, and the **mini-project**: the Mock #3 recording with self-feedback, one XOR-trick write-up, and one binary-trie write-up.

---

## Learning objectives

By the end of this week, you will be able to:

- **Recognize** an XOR-fold problem from the cue "every element appears twice except one" / "find the missing / duplicated number with `O(1)` extra space" — and reject the hash-map answer when the interview tell is constant space.
- **Apply** the four XOR identities — `a ^ a == 0`, `a ^ 0 == a`, commutativity, associativity — to argue that reducing an array by `^` returns exactly the unpaired element, regardless of order.
- **Manipulate** a single bit at position `i`: set with `x | (1 << i)`, clear with `x & ~(1 << i)`, toggle with `x ^ (1 << i)`, test with `(x >> i) & 1`. Isolate the lowest set bit with `x & -x`; clear it with `x & (x - 1)`.
- **Count** set bits three ways: `x.bit_count()` (Python 3.10+), `bin(x).count("1")`, and the Brian Kernighan loop `while x: x &= x - 1; count += 1` — and state which the interviewer wants and why.
- **Enumerate** subsets with a bitmask: loop `mask` over `range(1 << n)`, and for each `mask` read bit `i` as "item `i` is in the subset." Use it to generate the power set (Subsets, LC 78) in `O(n · 2**n)`.
- **Apply** bitmask DP at the recognition level: state = subset, transition picks one more element; name Travelling Salesman and assignment as the canonical cases; be honest that the *implementation* is a Phase-3/4 stretch, not an interview-cold expectation.
- **Apply** the Counting Bits recurrence `dp[i] = dp[i >> 1] + (i & 1)` and explain why right-shifting by one strips the low bit, so `dp[i]` is the popcount of `i // 2` plus the bit you just dropped.
- **Build** a binary trie for Maximum XOR (LC 421): insert each number MSB-first as a 32-bit path; for each query number, walk the trie greedily choosing the *opposite* bit when a child exists to maximize the running XOR. State the `O(n · 32)` bound.
- **Run** Mock #3 as a near-real full loop: 45-minute hard clock, video on, an unseen Medium, no peeking; record screen + face + audio; watch back at 1.5× then 1.0×; produce a self-feedback note with exactly one testable behavior change versus your two prior mocks.

---

## Prerequisites

- **Weeks 1–13 complete.** You can deliver FRAME without notes on any of the twelve prior algorithm patterns, and you have a twelve-story behavioral bank from Week 13.
- **The Week 9 trie template fluent.** You can write the dict-of-dict trie (`root: Dict[str, Any] = {}`, `END = "$"`) *and* the `TrieNode` class form from memory. The binary trie this week is the same structure restricted to a 2-character alphabet (`0` and `1`); if the W9 template is not in your hands, re-read [Week 9 Lecture 1](../week-09-tries-and-advanced-strings/lecture-notes/01-trie-basics-and-autocomplete.md) before Wednesday.
- **Two prior mocks done.** Mock #1 (W4) and Mock #2 (W9) are recorded, watched, and self-critiqued. Mock #3 builds on those — the self-feedback compares the trajectory across all three.
- **Comfortable with binary and two's complement.** You know that a Python `int` is unbounded, that negative integers are conceptually two's complement, and that bit operations (`& | ^ ~ << >>`) act on the binary representation. Lecture 1 reviews this, but a working comfort speeds the week.
- **Comfortable with the difference between *expected* and *worst-case* space.** The XOR fold is `O(1)` *worst-case* space — there is no hash table to grow. Articulating this against the hash-map alternative is the interview tell.

---

## Topics covered

- **Binary representation and two's complement** — how integers are laid out in bits; why Python ints are unbounded and what that means for masking
- **The bitwise operators** — `&` (and), `|` (or), `^` (xor), `~` (not), `<<` / `>>` (shifts); their truth tables and idioms
- **Single-bit operations** — set / clear / toggle / test a bit at position `i` with a mask
- **The low-bit idioms** — `x & -x` isolates the lowest set bit; `x & (x - 1)` clears it (the Brian Kernighan popcount loop)
- **Popcount** — `x.bit_count()` (Python 3.10+), `bin(x).count("1")`, and the Kernighan loop; when each is the right answer
- **The XOR family** — `a ^ a == 0`, `a ^ 0 == a`, commutative + associative; Single Number (LC 136) by XOR fold; Missing Number (LC 268); Single Number III (LC 260) by partitioning on a differing bit
- **Bitmask-as-set** — represent a subset of `n` items as an `n`-bit integer; subset enumeration over `range(1 << n)`; submask iteration; Subsets (LC 78)
- **Bit DP** — Counting Bits (LC 338) with `dp[i] = dp[i >> 1] + (i & 1)`; the recognition-grade framing of bitmask DP (TSP, assignment)
- **Bitwise AND of a range** — Bitwise AND of Numbers Range (LC 201): the common-prefix observation
- **Reverse Bits** (LC 190) and **Number of 1 Bits** (LC 191) — the popcount and bit-reversal micro-patterns
- **Sum of Two Integers** (LC 371) — add without `+`: XOR for sum-without-carry, `(a & b) << 1` for carry, and the 32-bit masking subtlety in Python
- **The binary trie** — the bridge: insert MSB-first 32-bit paths into a 2-way trie; greedy opposite-bit walk for Maximum XOR (LC 421); ties the bit family to the Week 9 trie family
- **Mock #3 protocol** — the near-real full loop: video on, hard 45-minute clock, no peeking; the two-pass watching protocol; the one-behavior-change rule; the six anti-patterns
- **Tries review** — the dict-of-dict and `TrieNode` templates from Week 9, re-activated and pointed at the binary trie

---

## Weekly schedule (intensive · 36h)

| Day | Focus | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project | Self-Study | Daily Total |
|-----|-------|---------:|----------:|-----------:|----------:|---------:|-------------:|-----------:|------------:|
| Monday | Bit fundamentals + XOR family; exercise 1 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Tuesday | Bitmasks + subset enumeration + bit DP; exercise 2 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Wednesday | Binary trie + tries review; exercise 3 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Thursday | Mock #3 protocol; prep + warm-up; Sum of Two Integers challenge | 0h | 0h | 1.5h | 0.5h | 1h | 1.5h | 1h | 5.5h |
| Friday | **Mock #3 (45 min) + immediate notes** | 0h | 0h | 2h | 0.5h | 1h | 1.5h | 0.5h | 5.5h |
| Saturday | Watch recording + self-feedback + write-ups | 0h | 0h | 0h | 0.5h | 1h | 3h | 0h | 4.5h |
| Sunday | Quiz + retro + push | 0h | 0h | 0h | 0.5h | 0h | 4h | 0h | 4.5h |
| **Total** | | **6h** | **6h** | **5.5h** | **3.5h** | **6h** | **10h** | **3h** | **38h** |

(The week budgets ~36 hours; the table sums slightly higher to absorb the Phase-4 ramp. Drop 0.5h from Self-Study if 36h is your hard cap.)

**Mastery (10h/wk):** spread the same content over two calendar weeks (Phase 4 maps to mastery Q4, ~weeks 40–52). Mock #3 lands around calendar Week 44 of the mastery pathway; do not skip it — a recorded mock is the single highest-signal artifact in the portfolio. See the [mastery study plan](../study-plans/mastery-1-year.md).

---

## How to navigate this week

| File | What's inside |
|------|---------------|
| [README.md](./README.md) | This overview |
| [resources.md](./resources.md) | Free readings + bit-manipulation / trie references + glossary additions |
| [lecture-notes/01-bit-manipulation-fundamentals-and-xor.md](./lecture-notes/01-bit-manipulation-fundamentals-and-xor.md) | Binary + two's complement, the operators, single-bit ops, low-bit idioms, popcount, the XOR family, full worked FRAME on Single Number |
| [lecture-notes/02-bitmasks-and-subset-enumeration-and-bit-dp.md](./lecture-notes/02-bitmasks-and-subset-enumeration-and-bit-dp.md) | Bitmask-as-set, subset enumeration (LC 78), submask iteration, bit-DP intro, full worked FRAME on Counting Bits |
| [lecture-notes/03-the-mock-interview-protocol-mock-3-and-tries-review.md](./lecture-notes/03-the-mock-interview-protocol-mock-3-and-tries-review.md) | The Mock #3 near-real protocol, the two-pass watching protocol, the six anti-patterns, and the tries review with the binary-trie bridge to LC 421 |
| [exercises/README.md](./exercises/README.md) | Index of the three bit exercises and SOLUTIONS |
| [exercises/exercise-01-single-number.py](./exercises/exercise-01-single-number.py) | LC 136 — the XOR fold |
| [exercises/exercise-02-counting-bits.py](./exercises/exercise-02-counting-bits.py) | LC 338 — the bit-DP recurrence |
| [exercises/exercise-03-maximum-xor.py](./exercises/exercise-03-maximum-xor.py) | LC 421 — the binary trie (the topic bridge) |
| [exercises/SOLUTIONS.md](./exercises/SOLUTIONS.md) | Worked solutions with FRAME narration; consult after attempting each exercise |
| [challenges/README.md](./challenges/README.md) | Index of the two challenges |
| [challenges/challenge-01-mock-3-timed-round.md](./challenges/challenge-01-mock-3-timed-round.md) | The Mock #3 deliverable — 45-min hard clock, record, two-pass self-feedback, trajectory vs Mock #1 / #2 |
| [challenges/challenge-02-sum-of-two-integers.md](./challenges/challenge-02-sum-of-two-integers.md) | LC 371 — add without `+`, the 32-bit masking subtlety, full FRAME |
| [quiz.md](./quiz.md) | 10 pattern-recognition questions |
| [homework.md](./homework/README.md) | Six practice problems (~5 hrs) — XOR fold, popcount, reverse, range-AND, subsets, missing number |
| [mini-project/README.md](./mini-project/README.md) | **Mock #3 recording + self-feedback + one XOR-trick write-up + one binary-trie write-up** — the week's deliverable |

---

## Stretch goals

- **Read the LeetCode "Bit Manipulation" tag** and skim 20 titles: <https://leetcode.com/tag/bit-manipulation/>. For each, predict in 5 seconds: XOR-fold? bitmask-enumeration? bit-DP? binary-trie? none? Stretches the Research-constraints muscle on the curveball pattern.
- **Read Sean Eron Anderson's "Bit Twiddling Hacks"** end-to-end once: <https://graphics.stanford.edu/~seander/bithacks.html>. You will not memorize all of it; you will recognize the idioms when they appear. The "Counting bits set" and "Compute the lowest set bit" sections are the high-yield reads this week.
- **Re-derive the binary trie from scratch** without re-reading Lecture 3. If you cannot insert a 32-bit path MSB-first and run the greedy opposite-bit walk from memory, you do not yet own the bridge. Re-read and re-derive until you can.
- **Run Mock #3 as a peer mock both directions.** Pair with another C2 learner; interview them for 45 minutes, then swap. Interviewing someone else is the fastest way to internalize the rubric — you will hear the missing Research-constraints memo and the skipped Examine (cost) in *their* solve, then catch it in your own.
- **Read the bitmask-DP chapter of the Competitive Programmer's Handbook** (Antti Laaksonen, free PDF): <https://cses.fi/book/book.pdf>. The "Bit manipulation" and "Bitmask DP" chapters are the cleanest free treatment of subset-state DP. This is a Phase-4 stretch; recognition is the bar, not implementation.

---

## What "done" looks like for Week 14

A learner who has shipped Week 14 has, in their portfolio repo:

- Three FRAME write-ups for the exercises (Single Number, Counting Bits, Maximum XOR), with recordings >= 10 minutes.
- One FRAME write-up for the Sum of Two Integers challenge.
- The Mock #3 recording (link committed, since the file is too big to commit), the immediate notes, the pass-1 timestamps, and the self-feedback write-up with one behavior change versus Mock #1 and Mock #2.
- The quiz answered (score recorded).
- The homework problems committed.
- **Two mini-project write-ups** — one XOR-trick, one binary-trie — each with a 30-second pattern-recognition memo, under `frame-writeups/c2-week-14/mini-project/`, plus the Mock #3 artifacts under `mocks/mock-03/`.
- A push log showing daily commits Mon–Sun.

If all of that is present and pushed, Phase 4's second week is closed. You are ready for Week 15 — the capstone and Mock #4.

---

## A note on the Phase 4 ramp

Phase 4 — Capstone & Onsite Prep — is the final block: Weeks 13–15. Week 13 installed the behavioral skill set. Week 14 (this week) installs the last algorithm pattern and runs Mock #3 as the first full-loop simulation under near-real conditions. Week 15 is the capstone and Mock #4 — the dress rehearsal for the real thing.

Bit manipulation is pattern #13 of the fourteen-pattern catalog, and it is the one most candidates under-rate. It will not be the *centerpiece* of most loops, but it is the curveball that separates the candidate who reaches for `O(1)` space from the one who reaches for a hash map by reflex. The week's real work is not the bit tricks — those are an afternoon — it is **Mock #3**: a full recorded loop under near-real pressure that you watch back without flinching and turn into one specific change. The bit material is the *vehicle*; the mock is the *destination*.

If you find yourself ahead by Thursday, the right stretch is **not** another bit exercise — it is reading "Bit Twiddling Hacks" end-to-end and re-deriving the binary trie from memory, or running Mock #3 a second time with a peer in the opposite direction. The trajectory across Mock #1 → #2 → #3 is the artifact a senior engineer reads to see whether you can self-correct.

If you find yourself *behind* by Wednesday, skip Exercise 2 (Counting Bits) for now and prioritize Exercise 3 (Maximum XOR) — the binary trie is the topic bridge and the highest-yield single artifact of the week, and the bit-DP recurrence can be picked up in 20 minutes once the XOR fold is fluent. Do not skip Mock #3 under any circumstance.

---

## Up next

[Week 15 — Capstone + Mock #4](../week-15-capstone-and-mock-4/) — once your three bit write-ups are pushed, your Mock #3 recording is watched and self-critiqued with one behavior change named, and you can build a binary trie from memory without consulting the lecture.

---

*If you find errors in this material, please open an issue or send a PR. Future learners will thank you.*
