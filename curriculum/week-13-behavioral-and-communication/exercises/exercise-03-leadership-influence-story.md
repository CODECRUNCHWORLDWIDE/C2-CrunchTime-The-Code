# Exercise 3 — The Leadership / Influence Story

> **Category:** Leadership / influence-without-authority (top signals: ownership + collaboration)
> **Difficulty:** Medium
> **Target time:** 90-second delivery, ~45 minutes to draft + record + tighten
> **Why now:** the leadership category is where engineers most often confuse "I was assigned to lead" with "I led." Being given authority is not influence. The strong story shows you *moved people and an outcome through people who did not report to you* — and that is a specific skill the worked example makes concrete.

<!-- deliverable-page: the answer is a written and recorded story, not a program -->

## The Brief

An interviewer asks about a time you led something or moved a decision without
having the authority to make anyone do anything.

The category is where engineers most often confuse "I was assigned to lead" with
"I led". Being given a title is not influence. What the question is looking for
is evidence that you moved people and an outcome *through people who did not
report to you* — which is a specific, learnable skill, and one that looks like
nothing at all when it is done well.

The deliverable is a written story and a recording of you telling it from memory.

## Starter

> *"Tell me about a time you led an effort or influenced a decision without having the formal authority to make people do it."*

Draft your own answer first, in [`star_template.md`](./star_template.md),
with the recorder running. The model answer is further down this page,
under `## The Solution`, and reading it before you have drafted yours will
cost you the exercise — you will remember its story instead of finding
yours.

## Requirements

Draft your own first, in [`star_template.md`](./star_template.md). Pick a story where the people you moved did *not* report to you.

- [ ] **S — Situation (~10s):** the problem nobody owned, or the change you believed in. ("Our flaky CI was wasting everyone's time but no one owned fixing it.")
- [ ] **T — Task (~10s):** that you decided to drive it, without a mandate. ("I wasn't asked to fix it, but I took it on.")
- [ ] **A — Action (~60s):** how you built the case and brought people along — data to make the problem undeniable, a proposal, getting key people bought in, removing the friction so others would adopt. Influence, not orders.
- [ ] **R — Result (~20s):** the outcome (quantified — time saved across the team) and that *others adopted it*, which is the proof of influence.

## Constraints

- **Ninety seconds, spoken**, with the usual split.
- **Nobody in the story reports to you.** If they do, it is a management story and
  it answers a different question.
- **You were not asked to do it.** The strongest version starts with a problem
  nobody owned. Say plainly that you took it on without a mandate.
- **The proof of influence is adoption by others.** Not that you built the thing —
  that other people used it after you stopped pushing.
- **The number is time or effort saved across the team**, not for you. Influence
  is measured in other people's work.
- **Show the friction you removed.** People adopt what is easy. The step where you
  made it easy is usually the step candidates leave out.

## Expected output

Measure this, do not estimate it. Read the model answer below aloud at an
interview pace — about 150 words a minute — with a timer running:

```text
model answer   300 words   ~120s spoken
target         75-120s, and 90s is the number to aim at
situation      ~10s
task           ~10s
action         ~60s
result         ~20s
```

Notice the model comes in at about 120 seconds — *over* the target,
not under it. That is deliberate, and it is the shape of a good first draft:
every sentence in it is doing work and it is still too long. Getting from
there to ninety seconds is what the second take is for, and it is done by
compressing sentences, never by dropping one of the four beats.

A draft that comes in far *under* the target has a different problem, and a
worse one: the Action is missing.

## Steps

1. List three things you drove that nobody asked you to. Pick the one where the
   most other people ended up using the result.
2. Draft in [`star_template.md`](./star_template.md), ten minutes.
3. Write down, explicitly, who you needed and why they said yes. That list is the
   Action.
4. Find the adoption number. "Everyone uses it now" is not one.
5. Record from memory, listen back at 1.25×, cut anything that sounds like a
   project plan rather than a decision.
6. Re-record tightened.
7. Read the model answer below only now.

## The Solution

> *Read this only after drafting your own.*

> *On a team of about a dozen engineers, our CI pipeline had gotten flaky — maybe one in four builds failed for reasons that had nothing to do with the change, so people would just re-run until it passed. Nobody owned it; it was everyone's annoyance and no one's job. I wasn't asked to fix it, but it was costing us real time, so I took it on.*
>
> *I knew I couldn't just tell people to change their workflow — I had no authority and everyone had their own deadlines. So I started by making the problem undeniable: I scraped two weeks of CI logs and showed that flaky failures were burning roughly forty engineer-hours a week across the team in re-runs and context-switches. That number got attention in a way that my complaining hadn't. Then instead of proposing a big rewrite, I quarantined the flaky tests behind a separate non-blocking job so the main pipeline went green reliably, and I fixed the three worst offenders myself as proof it was tractable. I brought the data and the quarantine proposal to our weekly sync, got the tech lead and two senior engineers bought in by framing it as "here's the time we get back," and I set up a rotation where each week one person fixed one quarantined test — small enough that nobody could say no.*
>
> *Within two months the flaky-failure rate dropped from about twenty-five percent to under five, and we got back most of that forty hours a week. The part I'm proudest of is that the rotation kept running after I stopped pushing it — people had adopted it as theirs. The lesson: you don't get influence by being right, you get it by making the cost legible and making the first step small enough that saying yes is easy.*

Why this scores: ownership (took on unowned work, fixed the first three myself), collaboration (got buy-in, built a rotation others ran), impact (40 hrs/wk, 25%→<5% flaky rate), self-awareness (knew I couldn't just give orders), growth (the "make the cost legible, make the first step small" lesson). The proof of *influence* is that the rotation outlived your pushing — that is the senior signal in this category.

## How to deliver it

Record yourself telling it from memory — audio or video, phone is fine. Then
listen back at 1.25 to 1.5 times speed, which makes padding and filler
impossible to miss, and record a second tightened take.

Commit both the write-up and a note on the recording:

```
crunchtime-interview-prep-<you>/
└── behavioral/
    └── story-bank/
        ├── story-03-leadership.md
        └── recordings/
            └── story-03.md
```

When done, push and move on to [Exercise 4 — The Failure Story](./exercise-04-failure-story.md).

## Common bugs to catch

- **"I was the tech lead so I led."** Formal authority is not influence. If the story works only because people had to listen to you, it's not a leadership-without-authority story.
- **No adoption.** If you drove something and it died when you stopped, you surfaced effort but not influence. The proof is that it *stuck* without you.
- **All vision, no first step.** "I convinced everyone we should care about quality." How? Influence stories need the concrete mechanism — the data, the small first step, the buy-in conversation.
- **"We" hiding the drive.** You scraped the logs, you proposed the quarantine, you fixed the first three. Keep the "I" on the moves that show you drove it.
- **No number.** "It got better" is not influence. "40 hrs/wk recovered, flaky rate 25%→<5%" is.

## Acceptance checklist

- [ ] A STAR write-up committed to `behavioral/story-bank/story-03-leadership.md`.
- [ ] A recorded rehearsal, **at least 80 seconds**, delivered from memory.
- [ ] A listen-back at 1.25–1.5× and a tightened re-record.

## Stretch

- Prepare the follow-up: *"Who disagreed, and what did you do?"* Every real
  influence story has one, and having the answer ready separates a rehearsed
  story from a real one.
- Write the same story in one sentence — the version you would give if the
  interviewer says "briefly". Practising the compression is the point.
- Identify something at your current work that nobody owns, and draft the case
  for fixing it as if you were about to make it. The story bank gets a new entry
  and so does your week.
