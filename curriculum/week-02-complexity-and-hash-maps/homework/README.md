# Week 2 — Homework

Six problems, one page each, about five hours in total. Two of them are code and
four are writing, and that split is deliberate: an interview loop is not five
algorithm rounds, and a portfolio that contains only solutions is a portfolio
that answers only one of the questions you will be asked.

Each page carries the brief, a starter you can paste and run, the answer with an
explanation, and — where there is a program — a file you can download to compare
against. Read the answer *after* you have written something. The gap between
"this should work" and "why does it print that" is where the learning happens,
and reading first closes it for free.

## The problems

| # | Problem | What it drills | Difficulty | Target time |
|---|---------|----------------|------------|------------:|
| 1 | [The Locker Handshake](./problem-01-locker-handshake.md) | Two-way mapping — two maps that must agree, and why a `set` cannot answer | Medium | 90 min |
| 2 | [Time the Gap](./problem-02-time-the-gap.md) | Measuring a complexity class instead of believing in it | Easy to write | 45 min |
| 3 | [Re-narrate the Market Awning](./problem-03-renarrate-market-awning.md) | One Week 1 cost section, rewritten to the five-piece structure | Easy | 30 min |
| 4 | [The Tradeoff Story](./problem-04-tradeoff-story.md) | Behavioural story two — two valid approaches, in STAR | Easy | 45 min |
| 5 | [Counting the Top Queries](./problem-05-top-queries-design.md) | System-design warm-up two, written cold then calibrated | Medium | 45 min |
| 6 | [Week 2 Reflection](./problem-06-week-02-reflection.md) | Four honest questions, before you open Week 3 | Easy | 45 min |

**Total: 5 hours.** The week's [schedule](../README.md#weekly-schedule-intensive--36h)
spreads that across six days at about an hour each, which is the right shape —
Problems 4, 5 and 6 all improve when they sit overnight, and none of them
improves when rushed.

Do them in order. Problem 1 finishes the week's pattern coverage; Problem 2
proves the claim the whole week rests on; Problem 3 rehearses the mini-project;
Problems 4 and 5 are the other half of an interview loop; and Problem 6 measures
what actually landed, which only works if it is done last and before Week 3.

## What you hand in

Two programs and four written pieces, in your portfolio repo:

```text
c2-week-02/
    problem-01-locker-handshake.py
    problem-02-time-the-gap.py
frame-writeups/c2-week-02/
    homework-01-locker-handshake.md      (the FRAME write-up for Problem 1)
    measurement-01.md                    (Problem 2's timing table, your machine)
frame-writeups/c2-week-01/
    exercise-05-market-awning.md         (Problem 3 edits the cost section)
behavioral/
    story-02.md                          (Problem 4)
system-design/
    notes-week-02.md                     (Problem 5)
study-plan/
    week-02-reflection.md                (Problem 6)
```

The `-solution.py` files beside Problems 1 and 2 are the published answers. They
are named after their page rather than after your file so the two can never land
on top of each other, and so a download says what it is before it is opened.

Commit as you go rather than at the end — `feat(week-02): homework problem 1` and
so on. Six commits is the right number, and the cadence is part of what the
portfolio shows.

## The four pages with no program, and why

Problems 3, 4, 5 and 6 declare `no-runnable-file` at the top, because what you
hand in is prose about your own work and your own experience. No script can
write your tradeoff story or your reflection, and one that generated a design
answer would replace the reasoning the problem exists to build.

They still carry every section a code page carries — brief, requirements,
constraints, expected output, the answer, common bugs — because a written
deliverable has a specification too, and "300 to 400 words, four headings, one
checkable commitment" is exactly as checkable as an assert. The **Expected
output** block on each of those pages is a worked example of the finished piece,
and it is not hidden.

## Checking your work

Every page ends with an acceptance checklist. Work down it before you call a
problem done.

For the two programs, the check is mechanical: your output matches the page's
Expected output character for character, or the difference is the bug.

For the four written pieces the check is a reading, and each page names the one
that matters — read the cost section aloud with a timer; hand the story to
somebody who was not there; ask a cohort member what you should drill next. Do
those. A written deliverable that nobody has read is a written deliverable that
has not been tested.

Three habits worth building while the pieces are this short:

- **Say the cost sentence out loud before you write the code.** Problem 6's
  most-chosen commitment, and there is a reason it keeps getting chosen: if you
  cannot state the complexity before implementing, you have not finished
  *Assess options*.
- **Write down the inconvenient number.** Problem 2 will probably show you that
  at `n = 250` the quadratic version is competitive. Report it. A candidate who
  volunteers the number that complicates their story is worth more than one who
  reports only the tidy one.
- **Answer reflection questions from the files, not from memory.** Memory edits
  itself towards whatever story you are currently telling.

## Before you move on

When all six are committed, the week's remaining work is the
[quiz](../quiz.md) and the [mini-project](../mini-project/README.md) — which
takes Problem 3's single rewritten cost section and does the other four, with a
program that proves the tradeoff claims rather than asserting them.

Then: **[Week 3 — Sliding Window](../../week-03-sliding-window/)**, which is
built directly on the amortisation argument from
[Exercise 5](../exercises/exercise-05-longest-dock-run.md). If that argument is
not comfortable, spend twenty minutes on it before you start, rather than
discovering the gap on Week 3's first exercise.
