# Exercise 1 — The Debugging Story

> **Category:** Biggest accomplishment / Ambiguity (a debugging story leans on impact + ownership)
> **Difficulty:** Easy (the warm-up)
> **Target time:** 90-second delivery, ~45 minutes to draft + record + tighten
> **Why first:** a debugging story is the easiest to make concrete — the technical detail comes naturally, the "I" is obvious, and the result is usually a clean number (the bug fixed, the latency restored, the incident closed). If you can STAR a debugging story, you can STAR anything.

<!-- deliverable-page: the answer is a written and recorded story, not a program -->

## The Brief

An interviewer asks how you debugged something hard. Ninety seconds later they
have decided whether you are somebody who reasons from evidence or somebody who
changes things until the symptom goes away.

The debugging story is first because it is the easiest to make concrete. The
technical detail comes naturally, the "I" is obvious, and the result is usually a
clean number — the latency restored, the incident closed, the regression caught.
Everything that makes the harder categories hard is absent here, which makes this
the right place to learn the shape.

The deliverable is a written story and a recording of you telling it from memory.

## Starter

> *"Tell me about a time you debugged a really hard problem. What was the bug, how did you find it, and how did you fix it?"*

Draft your own answer first, in [`star_template.md`](./star_template.md),
with the recorder running. The model answer is further down this page,
under `## The Solution`, and reading it before you have drafted yours will
cost you the exercise — you will remember its story instead of finding
yours.

## Requirements

Draft your own answer first, in [`star_template.md`](./star_template.md), hitting each part. Recorder running.

- [ ] **S — Situation (~10s):** the system, the symptom, why it mattered. ("Our checkout p99 spiked from 300ms to 4s, and conversion was dropping.") Resist explaining the whole architecture.
- [ ] **T — Task (~10s):** *your* job. ("I owned the investigation and the fix.") Not "the team was looking into it."
- [ ] **A — Action (~60s):** the investigation, narrated as decisions. What you measured first, what you ruled out, the hypothesis, the confirming evidence, the fix, how you verified it. This is where the ownership and the rigor show.
- [ ] **R — Result (~20s):** the number (latency restored, incident closed, regression prevented) plus the lesson (the monitoring you added so it never recurs silently).

## Constraints

- **Ninety seconds, spoken.** Not a written essay read aloud. If your recording is
  under 75 seconds you skipped the Action; if it is over 120 you are narrating
  dead ends.
- **The Action is roughly two thirds of the time.** Situation and Task are ten
  seconds each. That ratio is not a style preference — the Action is the only
  part that shows how you think.
- **"I", not "we".** Every sentence about a decision has a subject, and it is
  you. "We found the connection pool" hides who did the work.
- **The Result carries a number.** "It got faster" scores nothing. If the number
  is genuinely unavailable, say what you measured instead and why.
- **One dead end, at most.** Ruling something out shows judgement; narrating four
  of them shows you cannot select.
- **It has to be true.** Every part of this week assumes a real story, because a
  follow-up question will find the seam in an invented one.

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

1. Read the prompt and set a timer for ten minutes. Draft in
   [`star_template.md`](./star_template.md) without stopping to polish.
2. Mark your draft up: bracket the Situation, Task, Action and Result and check
   the Action is the longest by some distance.
3. Underline every "we". Replace each one with "I" or delete the sentence.
4. Find your number. If you have none, the story is probably the wrong one.
5. Record it from memory, once. Do not read.
6. Listen back at 1.25×. Everything that makes you wince is a cut.
7. Re-record the tightened version. That second take is the deliverable.
8. Read the model answer below **only now**, and compare structure rather than
   content.

## The Solution

> *Read this only after drafting your own.*

> *About a year ago, our checkout service started intermittently timing out — p99 latency on the order-submit endpoint jumped from around 300 milliseconds to over four seconds, but only during peak evening traffic, and only sometimes. Conversion was visibly dropping during those windows, so it was a real revenue problem, and I owned the investigation.*
>
> *I started with the data instead of the code. I pulled the latency histogram and saw the slow requests clustered, not spread out — which told me it wasn't a slow query on every request, it was contention. My first hypothesis was the database connection pool. I added timing around the pool checkout and confirmed it: under load, requests were blocking up to three seconds waiting for a free connection. The pool was capped at twenty, which had been fine a year earlier. The obvious fix was to raise the cap, but I didn't — I checked the database's own connection limit first and found we were already near it, so blindly raising the app pool would just move the contention to the database and risk taking it down. Instead I traced which queries were holding connections longest and found one analytics query, added by another team, that ran inside the request path and held a connection for two-plus seconds. I moved that query to an async job off the request path and left the pool size alone.*
>
> *p99 went back to about 280 milliseconds and stayed there through the next peak. I also added a connection-pool-saturation alert that pages before we hit the cap, because the real failure was that we'd been blind to the saturation for weeks. Since then, the first thing I check on any latency spike is contention versus per-request cost — the histogram shape tells you which, and it saved me hours that night.*

Why this scores: ownership ("I owned," "I didn't" raise the cap), impact (300ms→4s→280ms, a revenue problem), self-awareness and rigor (checked the DB limit before raising the pool — the senior move), growth (the alert, the histogram-first habit). It is ninety seconds and every sentence is a decision.

## How to deliver it

Record yourself telling it from memory — audio or video, phone is fine. Then
listen back at 1.25 to 1.5 times speed, which makes padding and filler
impossible to miss, and record a second tightened take.

Commit both the write-up and a note on the recording:

```
crunchtime-interview-prep-<you>/
└── behavioral/
    └── story-bank/
        ├── story-01-debugging.md            # the STAR write-up
        └── recordings/
            └── story-01.md                  # link to / notes on the recording
```

When done, push and move on to [Exercise 2 — The Conflict Story](./exercise-02-conflict-story.md).

## Common bugs to catch

- **Burying the result.** Ending on "...and then it was fixed" with no number. The latency restored *is* the result — lead with it.
- **"We" instead of "I."** "We figured out it was the connection pool" hides who did the work. You investigated; say "I."
- **No quantified impact.** "It got a lot faster" scores nothing. "p99 from 4s to 280ms" scores.
- **Rambling Situation.** Explaining the entire service architecture before getting to the symptom. Ten seconds: system, symptom, stakes.
- **Listing every dead end.** You can mention you ruled out a hypothesis ("I ruled out a slow query"), but do not narrate four dead ends — pick the one that shows judgment.

## Acceptance checklist

- [ ] A STAR write-up committed to `behavioral/story-bank/story-01-debugging.md` in your portfolio repo.
- [ ] A recorded rehearsal (audio or video) of you delivering it from memory, **at least 75 seconds** long. If you finished in 30 seconds, you skipped the Action — re-do it.
- [ ] You read the recording back at 1.25–1.5× and re-recorded a tightened second take.

## Stretch

- Deliver it again in **forty-five seconds**. What survives the cut is the story's
  actual spine, and knowing that spine is what lets you adapt on the spot.
- Prepare for the follow-up: *"What would you do differently?"* The strong answer
  names a monitoring or process gap, not a technical regret.
- Retell the same incident as a **failure** story instead. Most real incidents
  can be framed either way, and noticing that is what makes
  [Exercise 4](./exercise-04-failure-story.md) easier.
