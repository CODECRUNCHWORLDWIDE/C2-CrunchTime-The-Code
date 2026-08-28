# Week 4 — Homework

Six problems, one page each. Three of them are code and three of them are
writing, and that split is deliberate: this is the week the course stops being
only about algorithms. The last problem is the **Phase-1 retrospective** — read
it on Monday so you know what you are collecting evidence for all week.

Each page carries the brief, a starter you can paste and run, the answer with an
explanation, and — for the three code problems — a file you can download and
compare against. Read the answer *after* you have written something and run it.
The gap between "this should work" and "why does it print that" is where the
learning happens, and reading first closes it for free.

## The problems

| # | Problem | What it drills | Difficulty | Target time |
|---|---------|----------------|------------|------------:|
| 1 | [The Loopback Self-Test](./problem-01-loopback-self-test.md) | Floyd's on a functional graph, hidden inside a list of integers | Medium | 75 min |
| 2 | [Trim the Duplicate Scan](./problem-02-trim-scan.md) | The **fixed-gap** variant, and what a dummy head buys you | Medium | 45 min |
| 3 | [The Symmetric Die Sequence](./problem-03-symmetric-dies.md) | Lower middle plus in-place reversal, then put the chain back | Medium | 45 min |
| 4 | [Behavioral Story #4](./problem-04-behavioral-story.md) | A STAR answer to the difficult-feedback question | Written | 45 min |
| 5 | [System-Design Ground Zero #4](./problem-05-system-design-warmup.md) | Detecting that something has *stopped* happening | Written | 45 min |
| 6 | [The Phase-1 Retrospective](./problem-06-phase-1-retrospective.md) | An honest account of four weeks and one mock | Written | 60 min |

## Time budget

| Problem | Time |
|--------:|-----:|
| 1 — The Loopback Self-Test | 75 min |
| 2 — Trim the Duplicate Scan | 45 min |
| 3 — The Symmetric Die Sequence | 45 min |
| 4 — Behavioral Story #4 | 45 min |
| 5 — System-Design Ground Zero #4 | 45 min |
| 6 — The Phase-1 Retrospective | 60 min |
| **Total** | **5h 15min** |

The [week schedule](../README.md#weekly-schedule-intensive--36h) budgets six
hours for homework, spread an hour a day. Both numbers are honest: the figures
here are how long each problem takes when it goes well, and the schedule leaves
room for the ones that do not.

## How to work a code problem

1. Read The Brief and the Requirements. Say out loud what the function takes and
   what it gives back before you type anything.
2. Copy the Starter into a file named after the page — `problem-01-loopback-self-test.py`
   and so on. The `-solution.py` file beside each page is the published answer,
   and it is named differently on purpose so the two never land on top of each
   other.
3. Fill in the `TODO` markers one at a time. Run the file after each one.
4. Compare your output with the Expected output block, character for character.
5. Only then read The Solution and the *why it works* paragraphs under it.

## How to work a written problem

Problems 4, 5 and 6 have no program. Their pages say so on their own line, near
the top, and they still carry every section a code page carries — including a
worked example of what a strong answer looks like.

They are not lighter work. Problem 5 in particular has a rule that is easy to
break and impossible to repair afterwards: **write your answer before you go and
read anyone else's.** The value of that page is the gap between the two, and the
gap only exists if you go in the right order.

## Two conventions that run through the week

Both code problems that walk objects — Problems 2 and 3 — compare with `is`,
because labels and codes repeat on purpose. Problem 1 walks integers, so it
compares with `==`. Say which world you are in every time you start, out loud.
That habit is the reason the week's drills are deliberately split between the
two.

## What you hand in

```text
crunchtime-interview-prep-<you>/
├── frame-writeups/
│   └── c2-week-04/
│       ├── hw-01-loopback-self-test.md
│       ├── hw-02-trim-scan.md
│       └── hw-03-symmetric-dies.md
├── behavioral/
│   └── story-04.md
├── system-design/
│   └── notes-week-04.md
└── study-plan/
    └── phase-1-retrospective.md
```

Each of the three code problems also gets its solution file committed beside its
write-up. Commit with `feat(week-04): homework problems`. If you are working in
a cohort, open a pull request.

## Checking your work

Every problem page ends with an acceptance checklist. Work down it before you
call a problem done. If your output differs from the page's Expected output, the
difference *is* the bug — read it rather than guessing.

Three habits worth building while the code problems are this small:

- **Test with something asymmetric.** Problem 1's shuffle check gives the right
  answer on every table that happens to be one big ring. Problem 3's
  restoration bug hides on every input that turns out symmetric. Both hide from
  a careless test and neither hides from a deliberate one.
- **Write down the behaviour you did *not* want.** `trim_scan(chain, 5)` on a
  four-scan chain does nothing. Asserting that it does nothing turns a surprise
  into a decision.
- **Read the squiggle in a traceback.** Python 3.11 and later underline the
  exact sub-expression that failed, which usually tells you which of two
  similar-looking things went wrong.

When all six are committed, take the [quiz](../quiz.md) if you have not already
and ship the [mini-project](../mini-project/README.md) — Mock Interview #1. That
closes Phase 1.
