# Week 5 — Binary Search Beyond Sorted Arrays

```
┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐
│ F │  │ R │  │ A │  │ M │  │ E │
└───┘  └───┘  └───┘  └───┘  └───┘
```

> *Phase 1 trained you on contiguous slices, cycles, and lockstep traversal. Phase 2 opens with the pattern most candidates think they know but rarely write cleanly: **binary search**. The "search a sorted array" version is the warm-up. The real lesson is "binary search on the answer" — parametric search — the idiom that turns a monotone predicate into a logarithmic optimization.* By Sunday you can write the canonical `lo <= hi` loop without notes, defend your boundary convention out loud, and convert "find the smallest `k` such that …" into a binary search in 30 seconds.

Welcome to Week 5 of **C2 · CrunchTime — The Code** — the first week of Phase 2. Phase 1 was four patterns over four weeks: two-pointer, hash map, sliding window, fast/slow. Phase 2 is five patterns over five weeks: binary search (this week), BFS, DFS, backtracking, top-K. Each pattern is heavier than its Phase 1 counterpart, and each builds on the FRAME discipline you spent four weeks installing.

Binary search has a reputation. Candidates think it is trivial — "split in half, recurse" — and then write a loop that crashes on every other input. The boundary cases (`lo <= hi` vs `lo < hi`, `mid = (lo + hi) // 2` vs `mid = lo + (hi - lo + 1) // 2`, when to write `hi = mid` vs `hi = mid - 1`) are the part of binary search that interviewers grade. The pattern itself is two lines; the discipline of *picking the right template and defending the boundary* is what separates "I know binary search" from "I can write binary search cleanly under pressure."

By Sunday of Week 5 you will:

- **Spot** a binary-search problem in 30 seconds — and the harder skill, recognize a "search on the answer" problem when the array is not sorted at all.
- **Write** the canonical `lo <= hi` loop from memory, defend the boundary convention out loud, and pick the right template for "find any," "find first," "find last," and "find smallest `k` such that …".
- **Convert** an optimization problem ("minimize the maximum X subject to …") into a binary search on a monotone predicate, in under 60 seconds of Research constraints.
- Have solved **five binary-search drills**, including two that search a value space rather than an index space (The Quote Rank and The Paving Reach).
- Have shipped one challenge (The Merged Book Boundary — a rank query across two sorted sequences, solved by bisecting a *partition* rather than a value), the quiz, and the homework.
- Have started the Phase 2 mini-project: **five binary-search problem write-ups including two "search on answer" variants** — the artifact that opens your Phase 2 portfolio section.

---

## Learning objectives

By the end of this week, you will be able to:

- **Name** a binary-search problem in 30 seconds by recognizing the canonical signals: "sorted array," "find target," "first / last position of," "smallest `k` such that," "minimize the maximum," "maximize the minimum," "logarithmic time required."
- **Distinguish** "binary search on values" (classic) from "binary search on the answer space" (parametric). The first searches an *array*; the second searches an *interval of possible answers*, using a monotone predicate `feasible(k)` as the comparator.
- **Code** the canonical `lo <= hi` template without notes, with the correct loop guard, the correct `mid` formula (overflow-safe), and the correct shrink rules for each of the four variants.
- **Defend** the boundary convention out loud. "I picked `lo <= hi` because the search space is *closed* on both sides — every index in `[lo, hi]` is a valid candidate. The alternative `lo < hi` is the *half-open* version; both work but they shrink the space differently and I picked the closed form to keep the post-loop invariant simple."
- **Find first / last** occurrence of a value in a sorted array with duplicates, in `O(log n)` time, using the canonical lower-bound / upper-bound templates.
- **Search a rotated sorted array** in `O(log n)` time using the "which half is sorted?" decision at each step.
- **Convert** an optimization problem into a binary search on the answer: pick the search interval `[lo, hi]`, write the monotone `feasible(k)` predicate, run binary search, return the boundary value. This is the highest-yield interview skill of the week.
- **Defend** `O(log n)` time and `O(1)` space out loud — and recognize when the predicate's cost makes the total `O(n log M)` instead of `O(log n)`.

---

## Prerequisites

- **Weeks 1–4 complete.** You can deliver FRAME without notes on a fast/slow problem; you delivered Mock #1 and watched the recording; you have a Phase-1 retrospective committed.
- **Comfortable with array indexing in Python.** Off-by-one errors in indexing are the dominant source of binary-search bugs; if Python slicing still surprises you, re-do Week 1's two-pointer drills before starting here.
- **Comfortable with the term "monotone."** A function `f: int → bool` is monotone if `f(k) = True ⇒ f(k+1) = True` (non-decreasing) or vice versa. Binary search on the answer requires a monotone predicate; recognizing monotonicity is the Research-constraints skill.
- **A working pytest setup.** Drills are graded by [`timed_runner.py`](exercises/timed_runner.py).

---

## Topics covered

- The canonical binary-search template: `lo <= hi`, `mid = lo + (hi - lo) // 2`, the four shrink rules
- Off-by-one diagnostics: when to write `hi = mid` vs `hi = mid - 1`, when to write `lo = mid + 1` vs `lo = mid`
- The `lo <= hi` (closed interval) vs `lo < hi` (half-open) templates — pick one and defend it
- **Lower bound and upper bound:** find first / last occurrence of a value in a sorted array with duplicates
- **Rotated sorted array:** the "which half is sorted?" decision tree, classic and with duplicates
- **Binary search on the answer:** the parametric idiom — pick `[lo, hi]`, write `feasible(k)`, run the search, return the boundary
- **Ranking a value space you cannot materialize:** binary search on values, with a `count_at_most(v)` predicate
- **Minimising a threshold under a budget:** the canonical parametric shape, and its mirror, maximising a minimum
- **Bisecting a partition across two sorted sequences:** the hardest composition of the week (the week's challenge)
- When binary search *does not* apply — random unsorted arrays without a monotone structure, problems whose "answer space" is exponential without a polynomial-time `feasible`

---

## Weekly schedule (intensive · 36h)

| Day | Focus | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project | Self-Study | Daily Total |
|-----|-------|---------:|----------:|-----------:|----------:|---------:|-------------:|-----------:|------------:|
| Monday | Template + boundaries; drills 1-2 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Tuesday | Rotated arrays + lower/upper bound; exercise 3 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Wednesday | Binary search on the answer; drills 4-5 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Thursday | Mini-project drafting; challenge ramp | 0h | 1h | 1h | 0.5h | 1h | 1.5h | 1h | 6h |
| Friday | Challenge (The Merged Book Boundary) | 0h | 0h | 2h | 0.5h | 1h | 1.5h | 1h | 6h |
| Saturday | Mini-project — five write-ups | 0h | 0h | 0h | 0.5h | 1h | 3h | 0h | 4.5h |
| Sunday | Quiz + retro + push | 0h | 0h | 0h | 0.5h | 0h | 4h | 0h | 4.5h |
| **Total** | | **6h** | **7h** | **3h** | **3h** | **6h** | **10h** | **3.5h** | **38.5h** |

(The week budgets ~36 hours of curriculum work; the table sums slightly higher to absorb the Phase-2 ramp. Drop 0.5h from Self-Study if 36h is your hard cap.)

**Mastery (10h/wk):** spread the same content over three calendar weeks. The mini-project lands in calendar Week 16 of the mastery pathway. See the [mastery study plan](../study-plans/mastery-1-year.md).

---

## How to navigate this week

| File | What's inside |
|------|---------------|
| [README.md](./README.md) | This overview |
| [resources.md](./resources.md) | Free readings + binary-search references + monotonicity glossary additions |
| [lecture-notes/01-the-binary-search-template.md](./lecture-notes/01-the-binary-search-template.md) | The canonical loop, the four shrink rules, lower/upper bound, rotated arrays, off-by-one diagnostics |
| [lecture-notes/02-binary-search-on-the-answer.md](./lecture-notes/02-binary-search-on-the-answer.md) | Parametric search — pick `[lo, hi]`, write `feasible(k)`, run the search, return the boundary |
| [exercises/README.md](./exercises/README.md) | Index of the five binary-search drills |
| [exercises/exercise-01-ladder-seat.md](./exercises/exercise-01-ladder-seat.md) | The classic search, on a **descending** ladder — the template with the reflexes removed |
| [exercises/exercise-02-scan-window.md](./exercises/exercise-02-scan-window.md) | Lower bound applied twice to a run of duplicates, returning a half-open slice |
| [exercises/exercise-03-ring-buffer-probe.md](./exercises/exercise-03-ring-buffer-probe.md) | A rotated ring-buffer dump — locate the wrap point, then convert a slot to an age |
| [exercises/exercise-04-quote-rank.md](./exercises/exercise-04-quote-rank.md) | Binary search on values with a `count_at_most(v)` predicate over ten billion pair sums |
| [exercises/exercise-05-paving-reach.md](./exercises/exercise-05-paving-reach.md) | Binary search on the answer — the canonical parametric problem |
| [exercises/timed_runner.py](./exercises/timed_runner.py) | Pytest harness for the five drills |
| [challenges/README.md](./challenges/README.md) | Index of weekly challenges |
| [challenges/challenge-01-order-book-boundary.md](./challenges/challenge-01-order-book-boundary.md) | The Merged Book Boundary — bisecting a partition across two sorted reports |
| [quiz.md](./quiz.md) | 10 pattern-recognition questions |
| [homework.md](./homework/README.md) | Six practice problems (~5 hrs) including two parametric variants |
| [mini-project/README.md](./mini-project/README.md) | **Five binary-search write-ups including two "search on answer" variants** — the week's deliverable |

---

## Stretch goals

- **Skim fifteen problem titles** from any public binary-search problem set and predict, from the title alone: classic? lower/upper bound? rotated? parametric? Do not solve them. The recognition is the muscle, and titles are enough to train it.
- **Re-derive the lower-bound template from scratch** without re-reading Lecture 1. If you cannot, you do not yet own the template. Re-read and re-derive until you can.
- **Find one production-engineering binary-search story.** Examples: file-system block lookup, a relational index B-tree, autocomplete prefix search, a rate limiter searching for a sustainable throughput. The "where does binary search live in real systems?" question lifts you out of the practice-problem frame — and it is where the best answers to "tell me about a time you optimized something" come from.
- **Write one parametric problem of your own.** Pick a system you use, find a monotone threshold inside it, and pose it with a contract, justified constraints, and three examples. Authoring is the strongest evidence you own a pattern.
- **Predict your weakest drill before you start.** Then check at the end of the week. Calibration of your own self-assessment is a meta-skill worth grading separately.

---

## What "done" looks like for Week 5

A learner who has shipped Week 5 has, in their portfolio repo:

- Five FRAME write-ups for the drills, all with recordings ≥10 minutes.
- One FRAME write-up for the Merged Book Boundary challenge.
- The quiz answered (score recorded).
- The homework problems committed.
- **Five mini-project write-ups** (three classic, two parametric), each with a 30-second pattern-recognition memo at the top, under `frame-writeups/c2-week-05/mini-project/`.
- A push log showing daily commits Mon-Sun.

If all of that is present and pushed, Phase 2's first week is closed. You are ready for Week 6 — BFS.

---

## A note on the Phase 2 ramp

Phase 2 patterns are heavier than Phase 1. The drills are longer, the challenges are harder, and the mini-projects ship more material. If by Thursday you find yourself behind, the right move is **not** to skip a drill — it is to compress the homework's design / behavioral problems to their minimum and protect the pattern work. The patterns are the spine of the course; the system-design warm-ups exist to keep that muscle warm, not to be optimized at the expense of pattern fluency.

If you find yourself behind by Friday, drop the *stretch* on the challenge (no follow-up problem) and ship the mini-project's five core write-ups. The mini-project is the artifact for Phase 2's portfolio; everything else can be backfilled in Week 9's pre-mock review.

---

## Up next

[Week 6 — Graphs Part 1: BFS](../week-06-bfs/) — once your five binary-search write-ups are pushed, your boundary defenses are clean, and you can write the canonical loop from memory without a single off-by-one error.

---

*If you find errors in this material, please open an issue or send a PR. Future learners will thank you.*
