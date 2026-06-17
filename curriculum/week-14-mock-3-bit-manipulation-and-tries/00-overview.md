# Week 14 — Mock #3 + Patterns: Bit Manipulation & Tries

```
┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐
│ U │  │ M │  │ P │  │ I │  │ R │  │ E │
└───┘  └───┘  └───┘  └───┘  └───┘  └───┘
```

> *Week 13 closed the algorithmic syllabus. Week 14 is the **mop-up week plus the third checkpoint**. Two pattern families remain — **bit manipulation** (XOR tricks, bitmask state, bitmask DP) and **tries** (prefix matching applied at mock-interview speed, building on the Week 9 install). Both are narrow, high-yield, and exactly the kind of "did you study the long tail" signal that separates a strong onsite from an average one. The other half of the week is **Mock #3**, run under near-real conditions — 45 minutes, video on, no peeking, an uncurated prompt from a peer or platform — your third recorded interview and the most important data point so far. By Sunday you can read a problem and say, in 30 seconds, "this is XOR-cancellation," or "this is bitmask-DP over a set of size ≤ 20," or "this is a trie because the prompt asks a prefix question," and you have a recorded Mock #3 plus a self-feedback note that produces one specific behavior change for Mock #4.*

Welcome to Week 14 of **C2 · CrunchTime — The Code** — the tenth week of Phase 2 and the third mock checkpoint of the course. The prior weeks installed the heavy machinery: graphs, dynamic programming, backtracking. This week installs the **two remaining patterns** — bit manipulation and tries-at-speed — and then puts you back in the chair for **Mock #3**. The split is deliberate: these two patterns are the last "new" content in C2, they are small enough to install in three lectures, and they are exactly the kind of problem a candidate has *not* drilled enough by Week 14 — which makes them the perfect raw material for an uncurated mock.

This is the third mock, not the first. Mock #1 (Week 4) established the baseline. Mock #2 (Week 9) measured the Phase-2 ramp. Mock #3 is the **near-real** rehearsal: by now the recording rig is muscle memory, the UMPIRE narration is a reflex, and the remaining variable is *performance under an uncurated prompt you have not seen*. The bit-manipulation and trie content this week is **not** what Mock #3 will test — the mock prompt is uncurated, drawn from the full Phase-1-and-Phase-2 surface. The two patterns are this week's *content*; the mock is this week's *checkpoint*. Do both.

The recognition signals for the two patterns are tight. For **bit manipulation**: the prompt mentions "without using extra space," or "appears once / twice / an odd number of times," or "subset of a small set," or constraints with `n <= 20` and "consider all subsets" — these scream XOR or bitmask. For **tries**: the prompt asks a *prefix* question — "starts with," "longest word with prefix," "maximum XOR of two numbers" (a bitwise trie), "search a word with wildcards" — these scream trie. Half of both pattern families do not say the pattern name in the prompt; the recognition is the work.

By Sunday of Week 14 you will:

- **Recognize a bit-manipulation problem in 30 seconds** by the tells: "constant extra space" plus "duplicates," "the single non-repeating element," "subset of a small universe," or "toggle / set / clear a flag." Name XOR-cancellation, bitmask-as-set, or bitmask-DP.
- **Own the XOR identities cold:** `x ^ x = 0`, `x ^ 0 = x`, XOR is commutative and associative. From those three facts derive single-number (LC 136), the missing number (LC 268), and the two-single-numbers partition (LC 260).
- **Own the bit-twiddling vocabulary:** `x & 1` (low bit), `x >> 1` (shift), `x & (x - 1)` (clear lowest set bit), `x & -x` (isolate lowest set bit), `1 << k` (the `k`-th bit mask), `bin(x).count("1")` and `x.bit_count()` (popcount, 3.10+).
- **Use a bitmask as a set** for universes of size ≤ 20: membership is `mask & (1 << i)`, insertion is `mask | (1 << i)`, iteration over subsets is the `sub = (sub - 1) & mask` trick.
- **Write a bitmask DP** where the state is a subset of a small universe. The canonical shape: `dp[mask] = best way to have visited exactly the set `mask``. Defend the `O(2^n * n)` bound and why `n <= 20` is the constraint signal.
- **Write a trie at speed** in both the dict-of-dict and `TrieNode` forms, plus the **bitwise trie** variant for maximum-XOR problems — the Week-14 escalation of the Week-9 install.
- Have solved **three coding exercises** — single number (XOR warm-up), implement-trie-with-prefix (the speed rep), and counting bits (the bitmask-DP warm-up).
- Have shipped **one challenge** (maximum XOR of two numbers, the bitwise-trie deep dive) plus an optional stretch (partition to K equal-sum subsets, the bitmask-DP deep dive).
- Have run **Mock #3** under near-real conditions and shipped the recording, the immediate notes, the pass-1 timestamps, and the self-feedback note.
- Have shipped the quiz, the homework, and the **mini-project**: the recorded Mock #3 plus an XOR-trick write-up and a trie write-up.

---

## Learning objectives

By the end of this week, you will be able to:

- **Match a bit-manipulation problem in 30 seconds.** The signal hierarchy: does the prompt forbid extra space and mention duplicates (XOR-cancellation); does it ask for the single odd-count element (XOR over the whole array); does it ask about subsets of a universe of size `n <= 20` (bitmask-as-set or bitmask-DP); does it ask to toggle / count / isolate bits (bit-twiddling)? The four answers fully classify the bit shape.
- **Derive single-number from the XOR identities.** XOR every element; pairs cancel (`x ^ x = 0`); the survivor is the unique element. State the three identities and the derivation out loud. `O(n)` time, `O(1)` space.
- **Solve the missing-number problem two ways:** the Gauss sum (`n(n+1)/2 - sum(nums)`) and the XOR of indices-and-values. Defend why the XOR form avoids the integer-overflow risk that the sum form carries in fixed-width languages (a non-issue in Python, but the interview tell is naming it).
- **Partition for the two-single-numbers problem (LC 260).** XOR the whole array to get `a ^ b`; isolate any set bit with `x & -x`; partition the array by that bit; XOR each partition independently to recover `a` and `b`. The partition-by-a-distinguishing-bit move is the discriminator.
- **Use a bitmask as a set.** Represent a subset of `{0, ..., n-1}` as an integer. Membership `mask & (1 << i)`, add `mask | (1 << i)`, remove `mask & ~(1 << i)`, full set `(1 << n) - 1`, popcount `mask.bit_count()`. Enumerate every subset of a mask with `sub = (sub - 1) & mask`.
- **Write a bitmask DP.** State is a subset; transition adds one element to the set. `dp[mask]` answers "the best/count over having committed exactly the elements in `mask`." `O(2^n)` states times `O(n)` per transition is `O(2^n * n)`; the `n <= 20` constraint is the recognition cue.
- **Implement counting-bits (LC 338) as a 1D DP over bits:** `dp[i] = dp[i >> 1] + (i & 1)`. The number of set bits in `i` is the count in `i >> 1` plus the low bit. The `O(n)` DP beats the `O(n log n)` popcount-each-number approach.
- **Write a trie at speed.** `insert`, `search`, `starts_with` in under five minutes, in both the dict-of-dict and `TrieNode` forms. The Week-14 standard is *speed* — the Week-9 install was *recognition*; this week the recognition is assumed and the clock is the test.
- **Write a bitwise trie for maximum XOR (LC 421).** Insert each number's 32-bit (or 30-bit) representation as a root-to-leaf path; for each number, greedily walk the trie choosing the opposite bit at each level to maximize the running XOR. `O(n * 32)` time. The bitwise trie is the bridge between the two patterns this week.
- **Run Mock #3 under near-real conditions.** 45 minutes, video on, uncurated prompt, no peeking at solutions, hard stop at the clock. Record screen + face + audio. Ship the four artifacts (recording link, immediate notes, timestamps, self-feedback) with one specific, testable behavior change for Mock #4.

---

## Prerequisites

- **Weeks 1–13 complete.** You have shipped UMPIRE write-ups for the trie pair (W9), the graph pair (W10), the DP pair (W11), and the backtracking pair (W12). You have run Mock #1 (W4) and Mock #2 (W9) and have two self-feedback notes in your portfolio.
- **The Week-9 trie install is live.** This week assumes you can already write `insert` / `search` / `starts_with`. If the Week-9 trie module feels uncertain, re-walk [Week 9 Lecture 1](../week-09-tries-and-advanced-strings/02-lecture-notes/01-trie-basics-and-autocomplete.md) before starting — this week drills *speed*, not first-contact.
- **Comfortable with Python integer semantics.** Python integers are arbitrary-precision; there is no 32-bit overflow. The bit operators `&`, `|`, `^`, `~`, `<<`, `>>` work on the two's-complement representation, with the caveat that `~x == -x - 1` and negative numbers have a conceptually infinite sign-extension of leading 1s. For interview bit problems you almost always work with non-negative integers and a fixed bit width (e.g., 32), which sidesteps the sign subtleties.
- **`x.bit_count()` (Python 3.10+)** returns the popcount; `bin(x).count("1")` is the portable fallback. Know both; the interview environment may be on an older Python.
- **The mock-interview protocol from Week 4.** Re-skim [Week 4 Lecture 2](../week-04-fast-slow-pointers-and-mock-1/02-lecture-notes/02-the-mock-interview-protocol.md) for the 45-minute structure, the two-pass watching protocol, and the one-behavior-change rule. Mock #3 reuses all of it; the bar is higher.

---

## Topics covered

- **The three XOR identities** — `x ^ x = 0`, `x ^ 0 = x`, commutative + associative; the foundation of every XOR trick
- **XOR-cancellation** — single number (LC 136), missing number (LC 268), and the find-the-difference family
- **The two-single-numbers partition** — XOR the array, isolate a distinguishing bit with `x & -x`, partition, XOR each half (LC 260)
- **Bit-twiddling vocabulary** — `x & 1`, `x >> 1`, `x & (x - 1)`, `x & -x`, `1 << k`, popcount; the five moves that cover 90% of bit problems
- **Bitmask as a set** — represent / test / add / remove / iterate subsets of a universe of size ≤ 20 with a single integer
- **Subset enumeration** — the `sub = (sub - 1) & mask` idiom to walk every submask of a mask in `O(2^popcount)`
- **Bitmask DP** — state is a subset; transition adds an element; `O(2^n * n)`; the `n <= 20` constraint signal
- **Counting bits (LC 338)** — the 1D DP over bits, `dp[i] = dp[i >> 1] + (i & 1)`
- **Trie at speed** — `insert` / `search` / `starts_with` in under five minutes; both forms; the Week-9 recognition assumed
- **The bitwise trie** — maximum XOR of two numbers (LC 421); the bridge between bit manipulation and tries
- **Trie with wildcards** — add-and-search-word (LC 211); the dot-wildcard branching walk
- **The Mock #3 protocol** — near-real conditions, the 45-minute structure, the two-pass watching protocol, the self-feedback note
- **The recognition flowchart** — from the constraint signals (extra space forbidden? small `n`? prefix question? odd count?) to the right pattern

---

## Weekly schedule (intensive · 36h)

| Day | Focus | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project | Self-Study | Daily Total |
|-----|-------|---------:|----------:|-----------:|----------:|---------:|-------------:|-----------:|------------:|
| Monday | XOR identities + tricks; exercise 1; set up the Mock #3 rig | 2h | 2h | 0h | 0.5h | 1h | 0.5h | 0h | 6h |
| Tuesday | Bitmask-as-set + bitmask DP; exercise 3 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Wednesday | Trie at speed + bitwise trie; exercise 2; challenge ramp | 2h | 1h | 1h | 0.5h | 1h | 0h | 0.5h | 6h |
| Thursday | Challenge (Maximum XOR) + Mock #3 final prep | 0h | 0h | 2h | 0.5h | 1h | 1.5h | 1h | 6h |
| Friday | **Mock #3** (45 min) + immediate notes | 0h | 0h | 0h | 0.5h | 0.5h | 3.5h | 0h | 4.5h |
| Saturday | Watch the recording + self-feedback write-up + XOR/trie write-ups | 0h | 0h | 0h | 0.5h | 0h | 4h | 0h | 4.5h |
| Sunday | Quiz + retro + push | 0h | 0h | 0h | 0.5h | 0h | 4h | 0h | 4.5h |
| **Total** | | **6h** | **5h** | **3h** | **3.5h** | **4.5h** | **13.5h** | **2h** | **37.5h** |

(The week budgets ~36 hours; the table sums slightly higher to absorb the mock-watching load. Mock #3 plus its self-feedback is the heaviest single deliverable of the week — protect the Saturday block.)

**Mastery (10h/wk):** spread the same content over three calendar weeks. The mini-project lands in calendar Week 42 of the mastery pathway. See the [mastery study plan](../study-plans/mastery-1-year.md).

---

## How to navigate this week

| File | What's inside |
|------|---------------|
| [README.md](./00-overview.md) | This overview |
| [resources.md](./01-resources.md) | Free readings + bit-manipulation references + trie references + the bit-trick cheatsheet + the Mock #3 checklist + glossary additions |
| [lecture-notes/01-bit-manipulation-and-xor-tricks.md](./02-lecture-notes/01-bit-manipulation-and-xor-tricks.md) | The three XOR identities, the bit-twiddling vocabulary, single number, missing number, two single numbers |
| [lecture-notes/02-bitmasks-bitmask-dp-and-tries-at-speed.md](./02-lecture-notes/02-bitmasks-bitmask-dp-and-tries-at-speed.md) | Bitmask-as-set, subset enumeration, bitmask DP, counting bits, trie at speed, the bitwise trie |
| [lecture-notes/03-the-mock-3-protocol.md](./02-lecture-notes/03-the-mock-3-protocol.md) | Mock #3 under near-real conditions; the 45-minute structure; the two-pass watching protocol; the self-feedback note |
| [exercises/README.md](./03-exercises/00-overview.md) | Index of the three exercises and SOLUTIONS |
| [exercises/exercise-01-single-number.py](./03-exercises/exercise-01-single-number.py) | LC 136 — the XOR-cancellation warm-up |
| [exercises/exercise-02-implement-trie.py](./03-exercises/exercise-02-implement-trie.py) | LC 208 — the trie-at-speed rep (insert / search / starts_with) |
| [exercises/exercise-03-counting-bits.py](./03-exercises/exercise-03-counting-bits.py) | LC 338 — the 1D DP over bits |
| [exercises/SOLUTIONS.md](./03-exercises/SOLUTIONS.md) | Worked solutions with UMPIRE narration; consult after attempting each exercise |
| [challenges/README.md](./04-challenges/00-overview.md) | Index of weekly challenges |
| [challenges/challenge-01-maximum-xor.md](./04-challenges/challenge-01-maximum-xor.md) | LC 421 deep-dive — the bitwise trie and the greedy opposite-bit walk |
| [challenges/challenge-02-partition-to-k-equal-sum-subsets.md](./04-challenges/challenge-02-partition-to-k-equal-sum-subsets.md) | LC 698 — the bitmask-DP deep dive |
| [quiz.md](./05-quiz.md) | 10 pattern-recognition questions |
| [homework.md](./06-homework.md) | Six practice problems (~4.5 hrs) — three bit, three trie/bitmask |
| [mini-project/README.md](./07-mini-project/00-overview.md) | **Mock #3 recorded + an XOR-trick write-up + a trie write-up** — the week's deliverable |

---

## Stretch goals

- **Read the LeetCode "Bit Manipulation" tag** and skim 30 titles. For each, predict in 5 seconds: XOR-cancellation? bitmask-as-set? bitmask-DP? plain bit-twiddling? not a bit problem at all? Stretches the Match-step muscle harder than any exercise this week.
- **Implement the `sub = (sub - 1) & mask` submask-enumeration loop** and prove to yourself it visits every submask exactly once, in descending order, in `O(2^popcount(mask))` total across all masks (the famous `3^n` aggregate bound). The proof is two lines; the bound is a Phase-3 favorite.
- **Read Sean Anderson's "Bit Twiddling Hacks"** (Stanford graphics lab) end-to-end once. You will not memorize it; the point is to see the *space* of bit tricks so that when an interview reaches for one, you recognize the shape. Bookmark the "Counting bits set" and "Round up to power of 2" sections.
- **Implement maximum XOR with a 0/1 bitwise trie** without re-reading Challenge 1, then re-derive why the greedy opposite-bit walk is optimal (the most-significant differing bit dominates the XOR value). Phase-3 onsite favorite.
- **Read about the "Gray code" sequence (LC 89)** — a bit-manipulation ordering where successive integers differ in exactly one bit. The construction `i ^ (i >> 1)` is a one-liner; the recognition is the work. Phase-3 stretch.

---

## What "done" looks like for Week 14

A learner who has shipped Week 14 has, in their portfolio repo:

- Three UMPIRE write-ups for the exercises, with recordings >= 10 minutes.
- One UMPIRE write-up for the Maximum XOR challenge.
- The quiz answered (score recorded).
- The homework problems committed.
- **Mock #3 shipped:** the recording link, the immediate notes, the pass-1 timestamps, and the self-feedback note under `mocks/mock-03/` and `umpire-writeups/c2-week-14/`, with one specific, testable behavior change for Mock #4.
- **Two mini-project write-ups** (one XOR-trick, one trie), each with a 30-second pattern-recognition memo at the top, under `umpire-writeups/c2-week-14/mini-project/`.
- A push log showing daily commits Mon–Sun.

If all of that is present and pushed, Phase 2's tenth week is closed. You are ready for Week 15 — the Phase-2 capstone and **Mock #4**, the final recorded interview against which the whole course is measured.

---

## A note on the Phase 2 ramp

Week 14 is the *long-tail-plus-checkpoint* week. The two patterns are deliberately narrow: bit manipulation and tries-at-speed are not where most interviews are won, but they are where a *small number* of interviews are lost — the candidate who has never seen XOR-cancellation flails on single-number, and the candidate who has never written a bitwise trie cannot touch maximum-XOR. Installing both this week closes the last recognition gaps in the C2 syllabus.

The higher-leverage half of the week is **Mock #3**. By now you have two recorded mocks behind you; the marginal value of a third is the *trend line* — are your Match memos getting tighter, are your silent periods shrinking, is your recovery getting more audible? The self-feedback note this week should explicitly compare Mock #3 to Mock #2 on those axes. The one-behavior-change rule still holds: pick one thing, make it testable, carry it into Mock #4.

If you find yourself ahead by Thursday, the right stretch is **not** another exercise — it is a *second* mock (a "practice run" with a peer the day before the real Mock #3) so that the awkwardness is out of the way and Friday's recording is your sharpest. Alumni who ran a Thursday warm-up mock reported a visible Mock #3 quality lift.

If you find yourself *behind* by Wednesday, protect the Friday mock and the Saturday self-feedback at all costs — they are the irreplaceable artifacts. Drop Exercise 3 (counting bits) and Challenge 2 (partition to K subsets) first; the bitmask-DP content is the most droppable this week because it is recognition-grade for Phase 2 and re-installed in Phase 3.

---

## Up next

[Week 15 — Phase 2 Capstone and Mock #4](../week-15-phase-2-capstone-and-mock-4/) — once your three exercise write-ups are pushed, Mock #3 is recorded with a self-feedback note, and your XOR-trick and trie write-ups are shipped. Week 15 is the final mock and the Phase-2 retrospective; you arrive there with three recorded mocks behind you and the full C2 pattern surface installed.

---

*If you find errors in this material, please open an issue or send a PR. Future learners will thank you.*
