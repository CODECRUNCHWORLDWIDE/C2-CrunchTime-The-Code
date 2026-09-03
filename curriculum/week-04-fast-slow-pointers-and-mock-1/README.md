# Week 4 — Fast/Slow Pointers + Mock Interview #1

```
┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐
│ F │  │ R │  │ A │  │ M │  │ E │
└───┘  └───┘  └───┘  └───┘  └───┘
```

> *Week 3 taught you to recognize a contiguous slice. Week 4 teaches you to recognize a cycle — and to put yourself in front of a recorder for the first time, alone or with a peer, and watch yourself solve a problem cold.* By Sunday you can write Floyd's tortoise-and-hare without notes, derive the cycle-start trick out loud, and have shipped Mock #1 as a recording plus a self-feedback write-up.

Welcome to Week 4 of **C2 · CrunchTime — The Code** — the final week of Phase 1. This week is *two things wearing one hat*. The first is a small, tight pattern (fast/slow pointers) that uses two indices moving at *different speeds* through the same structure — usually a linked list, sometimes a sequence of integers acting as a functional graph. The second is the program's first inflection point: the **mock interview**. Reading about FRAME is one thing. Doing it under a clock, with a camera on your face, against a real (or simulated) interviewer, and then *watching the recording* — that's another thing entirely. This week we do both.

By Sunday of Week 4 you will:

- **Spot** a fast/slow-pointer problem in 30 seconds: loop detection in a chain, midpoint, nth-from-the-end, functional-graph cycles on an iterated integer function, symmetry check on a chain.
- **Write** Floyd's tortoise-and-hare cycle detection without notes, and *derive* the cycle-start algorithm out loud (the `2k = k + nC` lemma).
- **Use** the same template on three structurally different problems — a chain of objects, an integer sequence, midpoint finding — and explain why "fast = 2·slow" is the right speed ratio.
- Have solved **four fast/slow-pointer drills**, one challenge (Booklet Imposition), the quiz, and the homework, all FRAME-narrated.
- Have **recorded, watched, and self-critiqued your first mock interview** — the Week 4 mini-project. Peer or solo. 45 minutes on the clock. Then 30 minutes of self-review against a rubric.

---

## Learning objectives

By the end of this week, you will be able to:

- **Name** a fast/slow-pointer problem in 30 seconds by recognizing the canonical signals: a structure you can only step forward through, "cycle" or "loop" or "repeats forever," "the middle," "counted back from the end," and any rule of the form "the next value is a function of this one."
- **Distinguish** fast/slow from the other two-index patterns (converging two-pointer, sliding window) by *speed* — fast/slow advances at different rates, the others advance in lockstep or independently in one direction.
- **Code** Floyd's tortoise and hare for loop *detection* on a chain, then extend it to find the **loop entrance** by restarting a third pointer at the head.
- **Find the midpoint** of a chain in a single pass with the speed-2 hare — and pick the right convention (lower vs upper middle) from the problem prompt, since the loop guard differs between them.
- **Translate** an iterated integer function into a functional-graph cycle problem and measure the walk's shape with constant space.
- **Run** a 45-minute mock interview with a peer or solo (Excalidraw, recorder on), and produce a **self-feedback write-up** that grades yourself honestly against the FRAME rubric.
- **Watch** your own recording at 1.0× and 1.5× and extract three specific behavior changes for Mock #2 (Week 9).
- **Defend** the `O(n)` time and `O(1)` space claims out loud — Floyd's is the canonical "no auxiliary data structure" cycle algorithm, and the constant-space defense is the interview tell.

## Standards this week meets

| Bar | What this week is measured against |
| --- | --- |
| University | `CS 1332` — Linked structures, and the pointer techniques that walk them without a second pass. |
| Industry | Diagnose a chain of handoffs that has started repeating itself: prove the loop is there with two walkers and no extra memory, name the step where it enters, and leave the wiring exactly as you found it on every path out of the function. |
| Beyond the bar | The week's deliverable is not code at all — a forty-five-minute recording of the learner solving an unseen problem on a hard clock, then watched back against a rubric until it yields one named behaviour change for the next mock — `mini-project/README.md` |

---

## Prerequisites

- **Weeks 1, 2, and 3 complete.** You can deliver FRAME without notes on two-pointer, hash-map, and sliding-window problems. You can give the 30-second pattern-recognition memo for a sliding-window problem in under 30 seconds.
- **Comfortable building a chain of objects in Python from a list of values.** Three of this week's four drills hand you a small class with one "next" field — a chute, a rota slot, a stream segment — and the fourth has no objects at all. The builders live in [`exercises/timed_runner.py`](./exercises/timed_runner.py); read that file once before Monday's drills so the shape is familiar.
- **A way to record video + audio of yourself solving a problem.** OBS Studio (free), QuickTime (macOS, free), Loom (free tier), or the screen-recorder built into Zoom/Meet/Teams. Camera on. Voice clear.
- **45 minutes of uninterrupted time on one day this week.** This is for Mock #1. Block it on the calendar Monday. Don't move it.

---

## Topics covered

- The fast/slow-pointer pattern: two indices, different speeds, same structure
- Floyd's tortoise and hare: cycle *detection* in `O(n)` time, `O(1)` space
- The `2k = k + nC` cycle-entrance lemma — the small piece of math that makes "find the start of the loop" trivial
- Measuring a loop once you have found it — the counting walk, and why it must take its first step before comparing
- Single-pass midpoint of a chain — the most common fast/slow micro-pattern, and the guard shift that picks lower versus upper middle
- Iterated integer functions as functional graphs — same pattern, no objects and no pointers in sight
- Symmetry checking on a chain — fast/slow to find the midpoint, reverse the back half, compare, then put it back
- When fast/slow *doesn't* apply: arrays where indices are random access (use two-pointer or sliding window instead)
- **Mock Interview #1:** the protocol, the recording, the self-feedback rubric
- How to *watch* a recording of yourself — what to look for, what to ignore, how to extract behavior changes without spiraling

---

## Weekly schedule (intensive · 36h)

| Day | Focus | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project (Mock) | Self-Study | Daily Total |
|-----|-------|---------:|----------:|-----------:|----------:|---------:|--------------------:|-----------:|------------:|
| Monday | Pattern intro; Floyd's; drills 1-2 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Tuesday | Cycle entrance + midpoint; drills 3-4 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Wednesday | Challenge (Booklet Imposition) | 0h | 1h | 2h | 0.5h | 1h | 0h | 1h | 5.5h |
| Thursday | Mock protocol; prep + warm-up | 1h | 0h | 0h | 0.5h | 1h | 1.5h | 1h | 5h |
| Friday | **Mock #1 (45 min) + immediate notes** | 0h | 0h | 0h | 0.5h | 1h | 2.5h | 1h | 5h |
| Saturday | Watch recording + self-feedback write-up | 0h | 0h | 0h | 0h | 1h | 3h | 0h | 4h |
| Sunday | Quiz + reflection + Phase-1 retrospective | 0h | 0h | 0h | 0.5h | 0h | 4h | 0h | 4.5h |
| **Total** | | **5h** | **5h** | **2h** | **2.5h** | **6h** | **11h** | **4h** | **36h** |

**Mastery (10h/wk):** spread the same content over three calendar weeks. The mock interview happens in calendar Week 12 of the mastery pathway; do not skip it. See the [mastery study plan](../study-plans/mastery-1-year.md) for Week 4's block.

---

## How to navigate this week

| File | What's inside |
|------|---------------|
| [README.md](./README.md) | This overview |
| [resources.md](./resources.md) | Free readings + Floyd's references + mock-interview platforms + glossary additions |
| [lecture-notes/01-floyds-tortoise-and-hare.md](./lecture-notes/01-floyds-tortoise-and-hare.md) | The pattern, the algorithm, the cycle-entrance lemma, the midpoint micro-pattern |
| [lecture-notes/02-the-mock-interview-protocol.md](./lecture-notes/02-the-mock-interview-protocol.md) | How to set up the mock, run it, record it, watch it, and write self-feedback |
| [exercises/README.md](./exercises/README.md) | Index of the four fast/slow drills |
| [exercises/exercise-01-conveyor-loop.md](./exercises/exercise-01-conveyor-loop.md) | Detect a miswired loop in a parcel sorter, then measure it — Floyd's plus a counting walk |
| [exercises/exercise-02-escalation-loop.md](./exercises/exercise-02-escalation-loop.md) | Find the *entrance* of an on-call escalation loop, and how far in front of it you started — the lemma in action |
| [exercises/exercise-03-midroll-break.md](./exercises/exercise-03-midroll-break.md) | Single-pass midpoint with the speed-2 hare, lower-middle convention |
| [exercises/exercise-04-wear-level-rotation.md](./exercises/exercise-04-wear-level-rotation.md) | Functional-graph cycle detection — same pattern, integers instead of objects |
| [exercises/timed_runner.py](./exercises/timed_runner.py) | Pytest harness for the four drills |
| [challenges/README.md](./challenges/README.md) | Index of weekly challenges |
| [challenges/challenge-01-booklet-imposition.md](./challenges/challenge-01-booklet-imposition.md) | Rewire a page chain into a saddle-stitch feed order, outside-in — three sub-patterns in one |
| [quiz.md](./quiz.md) | 10 pattern-recognition questions |
| [homework.md](./homework/README.md) | Six practice problems (~5 hrs) including the Phase-1 retrospective |
| [mini-project/README.md](./mini-project/README.md) | **Mock Interview #1** — record, watch, self-feedback. The week's deliverable. |

---

## Stretch goals

- **Skim ten problem titles from any linked-list index and classify them from the title alone.** Titles only — no statements. For each, predict whether it is fast/slow, a simple traversal, or a reverse-and-merge composition. Classification from a title is the cheapest pattern-recognition rep there is.
- **Re-read Week 1's two-pointer lecture, section on "same-direction two-pointer."** Fast/slow is *almost* a same-direction two-pointer — but the *speed* difference is the discriminator. Make sure you can articulate why.
- **Set up your mock-interview rig now.** Test the recorder, test the screen share, test the audio. If you discover on Friday at 14:55 that your microphone is broken, the mock is gone. Test on Monday.
- **Run a 10-minute "pre-mock" on yourself Tuesday or Wednesday** — pick any easy problem, set a 10-minute timer, narrate FRAME start to finish. The goal: get the "talking to a camera" awkwardness out of the way *before* Friday's real mock.

---

## What "done" looks like for Week 4

A learner who has shipped Week 4 has, in their portfolio repo:

- Four FRAME write-ups for the drills, all with recordings ≥10 minutes.
- One FRAME write-up for the Booklet Imposition challenge.
- The quiz answered (score recorded).
- The homework problems committed.
- **A 45-minute mock-interview recording** (audio + video + screen) uploaded somewhere accessible (private YouTube unlisted, Google Drive, Loom — your choice).
- **A self-feedback write-up** (`mini-project/mock-01-self-feedback.md`) following the rubric in `mini-project/README.md`.
- A Phase-1 retrospective at `study-plan/phase-1-retrospective.md`.

If all of that is present and pushed, Phase 1 is closed. You are ready for Phase 2 (Week 5 — Binary Search Beyond Sorted Arrays).

---

## Up next

[Week 5 — Binary Search Beyond Sorted Arrays](../week-05-binary-search/) — once your Mock #1 recording is uploaded, your self-feedback write-up is honest (not flattering), and your Phase-1 retrospective is committed.

---

*If you find errors in this material, please open an issue or send a PR. Future learners will thank you.*
