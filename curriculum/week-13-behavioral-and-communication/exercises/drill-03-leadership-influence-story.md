# Drill 3 — The Leadership / Influence Story

> **Category:** Leadership / influence-without-authority (top signals: ownership + collaboration)
> **Difficulty:** Medium
> **Target time:** 90-second delivery, ~45 minutes to draft + record + tighten
> **Why now:** the leadership category is where engineers most often confuse "I was assigned to lead" with "I led." Being given authority is not influence. The strong story shows you *moved people and an outcome through people who did not report to you* — and that is a specific skill the worked example makes concrete.

## The prompt

> *"Tell me about a time you led an effort or influenced a decision without having the formal authority to make people do it."*

## STAR checklist for this drill

Draft your own first, in [`star_template.md`](./star_template.md). Pick a story where the people you moved did *not* report to you.

- [ ] **S — Situation (~10s):** the problem nobody owned, or the change you believed in. ("Our flaky CI was wasting everyone's time but no one owned fixing it.")
- [ ] **T — Task (~10s):** that you decided to drive it, without a mandate. ("I wasn't asked to fix it, but I took it on.")
- [ ] **A — Action (~60s):** how you built the case and brought people along — data to make the problem undeniable, a proposal, getting key people bought in, removing the friction so others would adopt. Influence, not orders.
- [ ] **R — Result (~20s):** the outcome (quantified — time saved across the team) and that *others adopted it*, which is the proof of influence.

## Worked example

> *Read this only after drafting your own.*

> *On a team of about a dozen engineers, our CI pipeline had gotten flaky — maybe one in four builds failed for reasons that had nothing to do with the change, so people would just re-run until it passed. Nobody owned it; it was everyone's annoyance and no one's job. I wasn't asked to fix it, but it was costing us real time, so I took it on.*
>
> *I knew I couldn't just tell people to change their workflow — I had no authority and everyone had their own deadlines. So I started by making the problem undeniable: I scraped two weeks of CI logs and showed that flaky failures were burning roughly forty engineer-hours a week across the team in re-runs and context-switches. That number got attention in a way that my complaining hadn't. Then instead of proposing a big rewrite, I quarantined the flaky tests behind a separate non-blocking job so the main pipeline went green reliably, and I fixed the three worst offenders myself as proof it was tractable. I brought the data and the quarantine proposal to our weekly sync, got the tech lead and two senior engineers bought in by framing it as "here's the time we get back," and I set up a rotation where each week one person fixed one quarantined test — small enough that nobody could say no.*
>
> *Within two months the flaky-failure rate dropped from about twenty-five percent to under five, and we got back most of that forty hours a week. The part I'm proudest of is that the rotation kept running after I stopped pushing it — people had adopted it as theirs. The lesson: you don't get influence by being right, you get it by making the cost legible and making the first step small enough that saying yes is easy.*

Why this scores: ownership (took on unowned work, fixed the first three myself), collaboration (got buy-in, built a rotation others ran), impact (40 hrs/wk, 25%→<5% flaky rate), self-awareness (knew I couldn't just give orders), growth (the "make the cost legible, make the first step small" lesson). The proof of *influence* is that the rotation outlived your pushing — that is the senior signal in this category.

## Acceptance criteria

- A STAR write-up committed to `behavioral/story-bank/story-03-leadership.md`.
- A recorded rehearsal, **at least 80 seconds**, delivered from memory.
- A listen-back at 1.25–1.5× and a tightened re-record.

## Common mistakes

- **"I was the tech lead so I led."** Formal authority is not influence. If the story works only because people had to listen to you, it's not a leadership-without-authority story.
- **No adoption.** If you drove something and it died when you stopped, you surfaced effort but not influence. The proof is that it *stuck* without you.
- **All vision, no first step.** "I convinced everyone we should care about quality." How? Influence stories need the concrete mechanism — the data, the small first step, the buy-in conversation.
- **"We" hiding the drive.** You scraped the logs, you proposed the quarantine, you fixed the first three. Keep the "I" on the moves that show you drove it.
- **No number.** "It got better" is not influence. "40 hrs/wk recovered, flaky rate 25%→<5%" is.

## What to commit to your portfolio repo

```
crunchtime-interview-prep-<you>/
└── behavioral/
    └── story-bank/
        ├── story-03-leadership.md
        └── recordings/
            └── story-03.md
```

When done, push and move on to [Drill 4 — The Failure Story](./drill-04-failure-story.md).
