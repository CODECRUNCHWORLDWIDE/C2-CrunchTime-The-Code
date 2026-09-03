# Week 3 — Sliding Window

```
┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐
│ F │  │ R │  │ A │  │ M │  │ E │
└───┘  └───┘  └───┘  └───┘  └───┘
```

> *Last week we taught you to reach for a hash map when the array is unsorted. This week we teach you to recognize when "something over every contiguous slice" is actually a single linear scan.* By Sunday you can spot a sliding-window problem in 30 seconds, decide fixed-size versus variable-size in the next 30, and write the canonical two-index loop without notes.

Welcome to Week 3 of **C2 · CrunchTime — The Code**. The pattern this week — sliding window — is one of the highest-yield pattern matches in the entire course. It collapses an apparent `O(n·k)` or `O(n²)` brute force into an honest `O(n)`, and it does it with two indices that never converge, never swap, and never sort. Different from two-pointer. Different from hash map. New muscle.

By Sunday of Week 3 you will:

- **Spot** a sliding-window problem within 30 seconds of reading the prompt, using the canonical signals from Lecture 1.
- **Distinguish** fixed-size from variable-size windows and pick the right loop shape on first try.
- **Write** the canonical *expand then shrink* loop for variable-size windows without referring to notes.
- **Maintain** a window invariant (sum, count, frequency, distinctness) in `O(1)` per step — the entire reason sliding window is `O(n)`.
- Have solved **five sliding-window drills**, one hard challenge (The Shortest Kit Span), the quiz, and the homework, all FRAME-narrated.
- Have shipped a **mini-project** of six sliding-window write-ups with a 30-second pattern-recognition memo for each.

---

## Learning objectives

By the end of this week, you will be able to:

- **Name** a sliding-window problem in 30 seconds by recognizing the canonical signals: "contiguous subarray / substring," "longest / shortest / count of windows satisfying a property," "fixed window size `k`," or "longest run with at most / exactly / no more than X distinct."
- **Distinguish** fixed-size from variable-size windows on first read, and explain *why* the choice matters for the loop shape.
- **State** the window invariant for any problem you tackle — the property that holds at every iteration — and use it to justify correctness.
- **Code** both loop shapes:
  - **Fixed:** initialize the first window, then slide one position at a time (add right, remove left).
  - **Variable:** outer loop on `right`, inner `while` shrinks from `left` until the invariant is restored.
- **Defend** the `O(n)` claim by amortized argument: each element enters the window at most once and leaves at most once.
- **Reach** for the right auxiliary structure inside the window: a running sum (numeric), a `Counter` / `defaultdict(int)` (character / value frequency), a `set` (distinctness), a deque (window max/min — preview of Week 9).
- **Reject** the pattern when it doesn't fit: negative numbers in a "sum at most k" problem, non-contiguous subsequences, problems that need a hash-map prefix-sum reformulation instead.
- **Write** a FRAME write-up whose Research constraints section delivers the 30-second pattern-recognition memo cleanly.

---

## Prerequisites

- **Week 1 and Week 2 complete.** You can run FRAME on a two-pointer or hash-map problem without notes. You can state time and space complexity in the standard five-piece Examine (cost) shape.
- **Comfortable with Python `collections.Counter` and `defaultdict`.** We use them daily this week — the window's auxiliary state is almost always a counter.
- **Portfolio repo current** with Week 1 and Week 2 contents committed (mini-projects done). You will add a `c2-week-03/` subfolder to `frame-writeups/`.
- **45 minutes of out-loud time per drill.** Same standard as Weeks 1 and 2 — vocalization is not optional in this course.

---

## Topics covered

- Why "contiguous subarray / substring" is the single most reliable sliding-window signal
- Fixed-size windows: the classic average-of-every-k-window shape
- Variable-size windows: the expand-then-shrink shape that produces "longest / shortest" answers
- The window invariant as a first-class concept — the property that the loop maintains
- The amortized `O(n)` argument — each element enters and leaves the window at most once
- Why two-pointer converging is *not* sliding window, even though both use two indices
- The auxiliary state inside the window: running sum, `Counter`, `set`, deque
- When the pattern fails: negative numbers, non-contiguous subsequences, "exactly k" vs "at most k" framings
- Reading the *contract* before writing the loop: tie-breaks, span versus length, and the difference between "no answer" and "an answer of zero"
- The 30-second pattern-recognition memo — a Week 3 deliverable

---

## Weekly schedule (intensive · 36h)

| Day | Focus | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project | Self-Study | Daily Total |
|-----|-------|---------:|----------:|-----------:|----------:|---------:|-------------:|-----------:|------------:|
| Monday | Pattern intro; fixed vs variable; drills 1-2 | 2h | 1.5h | 0h | 0.5h | 1h | 0h | 0.5h | 5.5h |
| Tuesday | Shrink-and-grow mechanics; drills 3-4 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Wednesday | Invariant discipline; exercise 5 | 2h | 2h | 1h | 0.5h | 1h | 0h | 0h | 6.5h |
| Thursday | Challenge + mini-project starts | 0h | 1.5h | 1h | 0.5h | 1h | 2h | 0.5h | 6.5h |
| Friday | Stretch + mini-project continues | 0h | 1h | 1h | 0.5h | 1h | 2h | 0.5h | 6h |
| Saturday | Mini-project deep work | 0h | 0h | 1h | 0h | 1h | 3h | 0h | 5h |
| Sunday | Pattern-recognition quiz + reflection | 0h | 0h | 0h | 0.5h | 0h | 0h | 0h | 0.5h |
| **Total** | | **6h** | **8h** | **4h** | **3h** | **6h** | **7h** | **2h** | **36h** |

**Mastery (10h/wk):** spread the same content over three calendar weeks. See the [mastery study plan](../study-plans/mastery-1-year.md) for Week 3's block.

---

## How to navigate this week

| File | What's inside |
|------|---------------|
| [README.md](./README.md) | This overview |
| [resources.md](./resources.md) | Free readings + pattern references + glossary additions |
| [lecture-notes/01-the-sliding-window-pattern.md](./lecture-notes/01-the-sliding-window-pattern.md) | Fixed vs variable windows; invariants; the canonical recognition signals |
| [lecture-notes/02-the-shrinking-and-growing-mechanics.md](./lecture-notes/02-the-shrinking-and-growing-mechanics.md) | When to expand, when to shrink; the two-pointer-but-not-converging shape; worked examples |
| [exercises/README.md](./exercises/README.md) | Index of the five sliding-window drills |
| [exercises/exercise-01-staffing-block.md](./exercises/exercise-01-staffing-block.md) | The fixed-window warm-up — busiest block of k intervals |
| [exercises/exercise-02-longest-clean-run.md](./exercises/exercise-02-longest-clean-run.md) | Variable window with a distinctness invariant, returning a span |
| [exercises/exercise-03-rota-window.md](./exercises/exercise-03-rota-window.md) | Fixed window with a frequency-table invariant |
| [exercises/exercise-04-shortest-catchment.md](./exercises/exercise-04-shortest-catchment.md) | Variable window — shortest, not longest |
| [exercises/exercise-05-cold-chain-load.md](./exercises/exercise-05-cold-chain-load.md) | Longest window with at-most-K distinct, `k` as a parameter |
| [challenges/README.md](./challenges/README.md) | Index of weekly challenges |
| [challenges/challenge-01-shortest-kit-span.md](./challenges/challenge-01-shortest-kit-span.md) | The hardest sliding-window shape — frequency invariant with a matched count |
| [quiz.md](./quiz.md) | 10 pattern-recognition questions |
| [homework.md](./homework/README.md) | Six practice problems (~5 hrs) |
| [mini-project/README.md](./mini-project/README.md) | Six sliding-window write-ups + 30-second memo per problem |

---

## Stretch goals

- **Skim ten sliding-window problem titles from any practice set.** Pattern recognition compounds with exposure. Do not solve them — read the titles, predict fixed or variable, then read the constraints to check yourself. Ten predictions is about four minutes and it is the cheapest recognition rep there is.
- **Re-read Week 2's Lecture 2 (the hash-map pattern).** The window's auxiliary state is almost always a `Counter`. The two patterns compose more than they compete.
- **Watch one Python `collections.deque` walkthrough.** We don't formally need it until Week 9 (top-K), but the "window maximum in O(1)" idiom is a sliding-window staple and previewing it now pays.

---

## Up next

[Week 4 — Fast-and-Slow Pointers + Mock 1](../week-04-fast-slow-pointers-and-mock-1/) — once your Week 3 mini-project is pushed, your six 30-second memos are tight, and your quiz score is 8 or better.

---

*If you find errors in this material, please open an issue or send a PR. Future learners will thank you.*
