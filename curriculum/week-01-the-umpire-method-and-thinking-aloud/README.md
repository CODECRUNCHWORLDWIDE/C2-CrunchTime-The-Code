# Week 1 — The UMPIRE Method & Thinking Aloud

> *Most candidates fail technical interviews not because they couldn't solve the problem. They fail because they couldn't explain themselves.* This week we fix that, before we drill a single algorithm.

Welcome to **C2 · CrunchTime — The Code**. Week 1 is unusual: we will not introduce a hard algorithmic pattern. Instead, you will learn the *six-step method* you'll use for every problem in the next 14 weeks (or 51, in mastery), and you will practice it on **arrays / two pointers** — the easiest pattern to learn UMPIRE on because the algorithms are familiar from C1.

By Sunday of Week 1 you will:

- Be able to recite the six UMPIRE steps from memory and explain what each one is for.
- Have solved **at least five array problems** while narrating UMPIRE out loud.
- Have written **five UMPIRE write-ups** in the standard format that will become your portfolio's primary artifact.
- Have made your first commit to the portfolio repo (`crunchtime-interview-prep-<yourhandle>`).
- Be ready to recognize a two-pointer problem within 30 seconds of reading it.

---

## Learning objectives

By the end of this week, you will be able to:

- **Recite** the UMPIRE Method's six steps in order and explain the purpose of each.
- **Apply** UMPIRE to a fresh medium-easy problem in 30 minutes, narrating each step out loud.
- **Restate** an interview prompt in your own words and surface at least three clarifying questions before writing any code.
- **Match** a problem to the two-pointer pattern by recognizing the canonical signals.
- **Plan** a solution in English before writing code, and translate the plan to code in one direction (English → Python) without surprises.
- **Review** your own code by tracing it on a small input and finding bugs before an interviewer would.
- **Evaluate** time and space complexity using big-O notation, distinguishing best, average, and worst case.
- **Write** a portfolio-quality UMPIRE write-up in Markdown that another engineer could read and learn from.

---

## Prerequisites

- **Comfortable Python 3.11+**: functions, lists, dicts, basic OOP, list comprehensions.
- **Git/GitHub**: clone, commit, push.
- **C1 Weeks 1–7** completed (or equivalent skill).
- **45 minutes you can talk to yourself out loud at full volume.** Sounds odd. Is essential. If you live with others, headphones won't do; you need to *vocalize*. Find a closet, a parked car, an empty conference room. Vocalization is not optional in this course.

---

## Topics covered

- Why interviews are different from solo problem-solving
- The UMPIRE Method's six steps: **Understand · Match · Plan · Implement · Review · Evaluate**
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
| Monday | UMPIRE introduced; first UMPIRE drill | 2h | 1.5h | 0h | 0.5h | 1h | 0h | 0.5h | 5.5h |
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
| [lecture-notes/02-the-umpire-method.md](./lecture-notes/02-the-umpire-method.md) | The six steps in painful detail with worked examples |
| [lecture-notes/03-arrays-and-two-pointers.md](./lecture-notes/03-arrays-and-two-pointers.md) | The first pattern; how to recognize and apply it |
| [exercises/README.md](./exercises/README.md) | Index of the five UMPIRE drills |
| [exercises/drill-01-reverse-string.md](./exercises/drill-01-reverse-string.md) | Two-pointer reverse, with full UMPIRE script |
| [exercises/drill-02-valid-palindrome.md](./exercises/drill-02-valid-palindrome.md) | Drill 2 |
| [exercises/drill-03-two-sum-sorted.md](./exercises/drill-03-two-sum-sorted.md) | Drill 3 |
| [exercises/drill-04-remove-duplicates.md](./exercises/drill-04-remove-duplicates.md) | Drill 4 |
| [exercises/drill-05-container-with-most-water.md](./exercises/drill-05-container-with-most-water.md) | Drill 5 |
| [exercises/umpire_template.md](./exercises/umpire_template.md) | The reusable write-up template |
| [exercises/timed_runner.py](./exercises/timed_runner.py) | A tiny pytest harness for grading your solutions |
| [challenges/README.md](./challenges/README.md) | Index of weekly challenges |
| [challenges/challenge-01-three-sum.md](./challenges/challenge-01-three-sum.md) | Three-sum, the canonical "level up" |
| [challenges/challenge-02-trapping-rain-water.md](./challenges/challenge-02-trapping-rain-water.md) | Hard two-pointer / DP-adjacent |
| [quiz.md](./quiz.md) | 10 pattern-recognition questions |
| [homework.md](./homework.md) | Six practice problems (~6 hrs) |
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
