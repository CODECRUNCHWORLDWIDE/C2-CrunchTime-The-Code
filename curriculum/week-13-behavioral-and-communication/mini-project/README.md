# Mini-Project — The Behavioral Story Bank

> The week's deliverable: a **behavioral story bank** of twelve-plus refined STAR anecdotes, each cross-referenced to the question categories it covers, anchored by a coverage matrix that proves every one of the eight categories is covered by at least one story, with a recording of each story delivered aloud. This is the behavioral analogue of your UMPIRE write-up library: an asset you build once and draw on for every onsite for the rest of your career. STAR is to behavioral what UMPIRE is to coding, and this bank is the library you'll select from in the room.

**Estimated time:** 8.5 hours, split across Thursday–Sunday.

This mini-project is *assembly-heavy* rather than *content-heavy* — most of the stories already exist (five from the drills, four from your W1/W4 homework, three new). The work is refining them to a consistent bar, cross-referencing them, building the coverage matrix, and recording each one. By Sunday you have a single folder you can re-read the morning of any onsite.

---

## Why this matters

Three reasons.

1. **Phase 4 grades the full loop, not just the coding.** Mock #3 next week is the first simulation that includes a behavioral round; Mock #4 in W15 is the dress rehearsal. The story bank you build now is *used* under timed pressure starting next week. Engineers who freeze in behavioral rounds are almost always engineers who tried to invent the answer in real time — the bank converts the cognitive load from *invention* (slow, freezes people) to *selection* (fast, reliable).

2. **A bank covers what eight scripts cannot.** In a real loop you will have already used your best story in an earlier round, and you cannot tell the same story to two interviewers who compare notes. Twelve stories covering eight categories with redundancy mean you can always reach for a fresh one. The reuse principle — one story answers several categories depending on which beat you emphasize — is what makes twelve stories cover eight categories several times over.

3. **The coverage matrix is the proof of completeness.** It turns "do I have enough stories?" from a vague worry into a checkable invariant: every column has at least one ●, or you have a gap to fill. Walking into an onsite with a complete matrix is the difference between confidence and hope.

---

## What you ship

A single self-contained folder in your portfolio repo.

```
crunchtime-interview-prep-<yourhandle>/
└── behavioral/
    └── story-bank/
        ├── README.md                         ← index of all stories + how to use the bank + reflection
        ├── coverage-matrix.md                ← stories × 8 categories; no empty column
        ├── story-01-debugging.md             ← Drill 1
        ├── story-02-conflict.md              ← Drill 2
        ├── story-03-leadership.md            ← Drill 3
        ├── story-04-failure.md               ← Drill 4
        ├── story-05-ambiguity.md             ← Drill 5
        ├── story-06-<title>.md               ← refined from W1 homework
        ├── story-07-<title>.md               ← refined from W1 homework
        ├── story-08-<title>.md               ← refined from W4 homework
        ├── story-09-<title>.md               ← refined from W4 homework
        ├── story-10-<title>.md               ← new (fills a coverage gap)
        ├── story-11-<title>.md               ← new (fills a coverage gap)
        ├── story-12-<title>.md               ← new (the "why-me / through-line")
        └── recordings/
            ├── story-01.md ... story-12.md   ← link to / notes on each recording
```

Each story uses the [`star_template.md`](../exercises/star_template.md): title, categories covered, the four STAR parts, a quantified result, the signals it surfaces, the follow-up questions you're ready for, and rehearsal notes.

The five drill stories and the four W1/W4 stories give you nine; the mini-project adds three more (Task 1 of the homework) to reach twelve. **The W1 and W4 homework stories feed directly into this bank** — that's why we asked you to jot them down twelve weeks ago. Refine them to the same bar as the drill stories.

---

## The coverage matrix (the centerpiece)

`coverage-matrix.md` is a grid: your twelve stories down the rows, the eight categories across the columns, a ● where a story strongly covers a category and a ○ where it's usable but not your best. The format and an illustrative example are in [Lecture 2 §6](../lecture-notes/02-the-star-method-and-the-story-bank.md).

Two ways to read it, both required:

- **Down each column** — every category must have at least one ●. An empty column is a gap; fill it before you call the bank done. This is the invariant the matrix exists to check.
- **Across each row** — see how flexible each story is. A story covering five or six categories is a workhorse worth polishing first; a story covering one (often the dedicated failure story) is a fine specialist.

Below the grid, add a short "**deployment notes**" section: for each of the eight categories, name your *first-choice* story and your *backup* (for the case where you already used the first choice in an earlier round). This is what you re-read the morning of an onsite.

---

## How to use the bank (put this in the story-bank README)

Write a short usage section so future-you can pick it up cold:

- **The morning of an onsite:** re-read the coverage matrix and the deployment notes, not all twelve stories. You want the *index* fresh, not a last-minute cram.
- **In the room:** hear the prompt → name the category (5 sec) → select the story (not invent) → deliver in 90 seconds STAR → land the number.
- **Across the loop:** track which story you used in which round so you don't repeat. The redundancy in the matrix is what lets you not repeat.

---

## Rubric

The story bank is graded on six dimensions. Total possible: 100 points; passing: 70.

| Dimension | Points | What "full credit" looks like |
|-----------|-------:|-------------------------------|
| Completeness | 20 | Twelve-plus stories, each in the STAR template; recordings linked for each |
| Coverage | 20 | Matrix present; **no empty column** across all eight categories; deployment notes (first-choice + backup) per category |
| STAR structure | 15 | Every story holds the 10/10/60/20 shape; Action is the bulk; no S/T over-spend |
| Quantified results | 15 | Every story's Result leads with a number (or an honest labeled estimate) tied to something that mattered |
| "I vs we" discipline | 10 | "I" for contribution, "we" for outcome, consistently; ownership and collaboration both surfaced |
| Delivery (recordings) | 20 | Each story recorded from memory, ~90 seconds, tightened on a second take; rehearsal notes present |

A passing bank scores at least 70 overall **and** has no empty column in the matrix — the coverage invariant is a hard gate, not a soft point total. A beautiful bank that can't answer a "difficult person" question is not done.

---

## Acceptance checklist

The mini-project is complete when:

- [ ] Twelve-plus stories committed under `behavioral/story-bank/`, each in the STAR template.
- [ ] Each story has a quantified Result and a tagged category list.
- [ ] `coverage-matrix.md` present, with **no empty column** and deployment notes per category.
- [ ] Each story recorded from memory (~90s), with a second tightened take where the first ran long.
- [ ] `README.md` for the bank: index, "how to use," and the reflection.
- [ ] The W1/W4 homework stories refined to the same bar as the drill stories.
- [ ] Everything pushed by Sunday end-of-day.

Push everything by Sunday. Phase 4's first week is closed on the push.

---

## Self-reflection (in the story-bank README)

End the bank's `README.md` with a short reflection — 4–6 sentences — addressing:

1. Which story is your strongest workhorse (covers the most categories), and why?
2. Which category was hardest to find a real story for, and what did you do about it?
3. What was harder this week — finding the stories, structuring them in STAR, or delivering them aloud?
4. The one thing you want to drill before the behavioral round in **Mock #3** next week.

The reflection is the portfolio-grade artifact. It's also the bridge to next week: the category you name as weakest here is the one to rehearse before Mock #3.

---

## After the mini-project

Move on to [Week 14 — Bit Manipulation, Tries + Mock #3](../../week-14-mock-3-bit-manipulation-and-tries/). Mock #3 is the first full loop that includes a behavioral round graded against the rubric, and it draws directly on the bank you just built. STAR is now in your toolkit alongside UMPIRE — the coding method and the behavioral method, both mechanical, both freeing your attention for signal. Mock #4 in W15 is the dress rehearsal for the real thing.
