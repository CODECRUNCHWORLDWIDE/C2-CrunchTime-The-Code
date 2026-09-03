# Week 1 — The FRAME Method & Thinking Aloud

> *Most candidates fail technical interviews not because they couldn't solve the problem. They fail because they couldn't explain themselves.* This week we fix that, before we drill a single algorithm.

Welcome to **C2 · CrunchTime — The Code**. Week 1 is unusual: we will not introduce a hard algorithmic pattern. Instead, you will learn the *five-step method* you'll use for every problem in the next 14 weeks (or 51, in mastery), and you will practice it on **arrays / two pointers** — the easiest pattern to learn FRAME on because the algorithms are familiar from C1.

FRAME is the method every course in this org teaches, so the habit you build this week carries into C3 and beyond.

By Sunday of Week 1 you will:

- Be able to recite the five FRAME steps from memory and explain what each one is for.
- Have solved **at least five array problems** while narrating FRAME out loud.
- Have written **five FRAME write-ups** in the standard format that will become your portfolio's primary artifact.
- Have made your first commit to the portfolio repo (`crunchtime-interview-prep-<yourhandle>`).
- Be ready to recognize a two-pointer problem within 30 seconds of reading it.

---

## Learning objectives

By the end of this week, you will be able to:

- **Recite** the FRAME Method's five steps in order and explain the purpose of each.
- **Apply** FRAME to a fresh medium-easy problem in 30 minutes, narrating each step out loud.
- **Frame** an interview prompt in your own words — inputs, outputs, and at least three clarifying questions — before writing any code.
- **Research the constraints** of a problem: read the size bounds for what they rule out, list the awkward inputs, and say in one sentence what makes the problem hard.
- **Assess options** by naming the two-pointer pattern from its canonical signals, pricing the simple approach first, comparing at least one alternative, and leaving with an English plan.
- **Make the solution** one English sentence at a time, translating the plan to Python without surprises.
- **Examine** your own work: trace the code on a small input to find bugs before an interviewer would, walk the edge cases, and state time and space complexity in big-O.
- **Write** a portfolio-quality FRAME write-up in Markdown that another engineer could read and learn from.

## Standards this week meets

| Bar | What this week is measured against |
| --- | --- |
| University | `CS 9` — Work a problem out loud in front of somebody, so your reasoning is visible while you are still wrong. |
| Industry | Talk a colleague through a problem you have not solved yet — the inputs, the questions you still have, the approach you are pricing and the one you dropped — so the wrong turn is caught while it is still cheap to take back. |
| Beyond the bar | Homework has you record your own narration, play it back, and count your filler words with a program you write, because an ear stops noticing them after the third one and a rate per minute does not — `homework/problem-02-narration-review.md` |

---

## Prerequisites

- **Comfortable Python 3.11+**: functions, lists, dicts, basic OOP, list comprehensions.
- **Git/GitHub**: clone, commit, push.
- **C1 Weeks 1–7** completed (or equivalent skill).
- **45 minutes you can talk to yourself out loud at full volume.** Sounds odd. Is essential. If you live with others, headphones won't do; you need to *vocalize*. Find a closet, a parked car, an empty conference room. Vocalization is not optional in this course.

---

## Topics covered

- Why interviews are different from solo problem-solving
- The FRAME Method's five steps: **Frame · Research constraints · Assess options · Make the solution · Examine**
- What an interviewer is actually scoring (correctness is one of four dimensions, not the only one)
- The three categories of clarifying question every problem deserves
- "Pattern" as a concept: why we name patterns and what they buy you
- Arrays and two pointers — the canonical "first pattern" because it's geometrically obvious
- The portfolio write-up format (and why we use Markdown, not a notebook)
- Mock interview etiquette (intro, time-checks, code-on-shared-screen, follow-up)
- Reading the prompt slowly: the 60-second discipline

---

## Weekly schedule (intensive · 36h)

| Day | Focus | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project | Self-Study | Daily Total |
|-----|-------|---------:|----------:|-----------:|----------:|---------:|-------------:|-----------:|------------:|
| Monday | FRAME introduced; first FRAME drill | 2h | 1.5h | 0h | 0.5h | 1h | 0h | 0.5h | 5.5h |
| Tuesday | Two-pointer pattern; second + third drills | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Wednesday | Behavioral basics + drills 4-5 | 2h | 2h | 1h | 0.5h | 1h | 0h | 0h | 6.5h |
| Thursday | Write-up format; first portfolio commit | 0h | 1.5h | 1h | 0.5h | 1h | 2h | 0.5h | 6.5h |
| Friday | Stretch drills + portfolio polish | 0h | 1h | 1h | 0.5h | 1h | 2h | 0.5h | 6h |
| Saturday | Mini-project deep work | 0h | 0h | 1h | 0h | 1h | 3h | 0h | 5h |
| Sunday | Pattern-recognition quiz + week reflection | 0h | 0h | 0h | 0.5h | 0h | 0h | 0h | 0.5h |
| **Total** | | **6h** | **8h** | **4h** | **3h** | **6h** | **7h** | **2h** | **36h** |

**Mastery (10h/wk):** spread the same content over three calendar weeks. See the [mastery study plan](../study-plans/mastery-1-year.md) for Week 1's block (mastery weeks 1–3).

---

## How to navigate this week

| File | What's inside |
|------|---------------|
| [README.md](./README.md) | This overview |
| [resources.md](./resources.md) | Free readings + practice platforms + glossary |
| [lecture-notes/01-what-interviewers-actually-score.md](./lecture-notes/01-what-interviewers-actually-score.md) | The four dimensions, debunking "just solve the problem" |
| [lecture-notes/02-the-frame-method.md](./lecture-notes/02-the-frame-method.md) | The five steps in painful detail with worked examples |
| [lecture-notes/03-arrays-and-two-pointers.md](./lecture-notes/03-arrays-and-two-pointers.md) | The first pattern; how to recognize and apply it |
| [exercises/README.md](./exercises/README.md) | Index of the five FRAME drills |
| [exercises/exercise-01-reverse-the-siding.md](./exercises/exercise-01-reverse-the-siding.md) | Converging swap over a sub-range, with full FRAME script |
| [exercises/exercise-02-mirror-serial.md](./exercises/exercise-02-mirror-serial.md) | Converging skip-and-compare, keeping original indices straight |
| [exercises/exercise-03-widest-ballast-pair.md](./exercises/exercise-03-widest-ballast-pair.md) | Converging pair search on sorted input |
| [exercises/exercise-04-stuck-gauge.md](./exercises/exercise-04-stuck-gauge.md) | Same-direction read / write compaction |
| [exercises/exercise-05-market-awning.md](./exercises/exercise-05-market-awning.md) | Converging with a tracked maximum and a greedy move |
| [exercises/frame_template.md](./exercises/frame_template.md) | The reusable write-up template |
| [exercises/timed_runner.py](./exercises/timed_runner.py) | A tiny pytest harness for grading your solutions |
| [challenges/README.md](./challenges/README.md) | Index of weekly challenges |
| [challenges/challenge-01-settlement-trio.md](./challenges/challenge-01-settlement-trio.md) | Pin plus converging — the canonical "level up" |
| [challenges/challenge-02-levee-ponding.md](./challenges/challenge-02-levee-ponding.md) | Hard converging two-pointer with a running max on each side |
| [quiz.md](./quiz.md) | 10 pattern-recognition questions |
| [homework.md](./homework/README.md) | Six practice problems (~5 hrs) |
| [mini-project/README.md](./mini-project/README.md) | Set up your portfolio repo |

---

## Stretch goals

- **Subscribe to one (free) interview podcast.** Recommendations in `resources.md`. Listen on commutes.
- **Read PEP 8 if you haven't.** Interview code that doesn't follow PEP 8 reads sloppy. <https://peps.python.org/pep-0008/>
- **Set up `pytest` so you can grade your own solutions.** Most weeks have a `timed_runner.py` that turns your work into a passing/failing test suite.

---

## Up next

[Week 2 — Complexity, Mental Models for Big-O, and Hash Maps](../week-02-complexity-and-hash-maps/) — once your portfolio repo is live on GitHub.

---

*If you find errors in this material, please open an issue or send a PR. Future learners will thank you.*
