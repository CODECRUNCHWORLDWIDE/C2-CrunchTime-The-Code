# Exercise 1 — The Debugging Story

> **Category:** Biggest accomplishment / Ambiguity (a debugging story leans on impact + ownership)
> **Difficulty:** Easy (the warm-up)
> **Target time:** 90-second delivery, ~45 minutes to draft + record + tighten
> **Why first:** a debugging story is the easiest to make concrete — the technical detail comes naturally, the "I" is obvious, and the result is usually a clean number (the bug fixed, the latency restored, the incident closed). If you can STAR a debugging story, you can STAR anything.

## The prompt

> *"Tell me about a time you debugged a really hard problem. What was the bug, how did you find it, and how did you fix it?"*

## STAR checklist for this drill

Draft your own answer first, in [`star_template.md`](./star_template.md), hitting each part. Recorder running.

- [ ] **S — Situation (~10s):** the system, the symptom, why it mattered. ("Our checkout p99 spiked from 300ms to 4s, and conversion was dropping.") Resist explaining the whole architecture.
- [ ] **T — Task (~10s):** *your* job. ("I owned the investigation and the fix.") Not "the team was looking into it."
- [ ] **A — Action (~60s):** the investigation, narrated as decisions. What you measured first, what you ruled out, the hypothesis, the confirming evidence, the fix, how you verified it. This is where the ownership and the rigor show.
- [ ] **R — Result (~20s):** the number (latency restored, incident closed, regression prevented) plus the lesson (the monitoring you added so it never recurs silently).

## Worked example

> *Read this only after drafting your own.*

> *About a year ago, our checkout service started intermittently timing out — p99 latency on the order-submit endpoint jumped from around 300 milliseconds to over four seconds, but only during peak evening traffic, and only sometimes. Conversion was visibly dropping during those windows, so it was a real revenue problem, and I owned the investigation.*
>
> *I started with the data instead of the code. I pulled the latency histogram and saw the slow requests clustered, not spread out — which told me it wasn't a slow query on every request, it was contention. My first hypothesis was the database connection pool. I added timing around the pool checkout and confirmed it: under load, requests were blocking up to three seconds waiting for a free connection. The pool was capped at twenty, which had been fine a year earlier. The obvious fix was to raise the cap, but I didn't — I checked the database's own connection limit first and found we were already near it, so blindly raising the app pool would just move the contention to the database and risk taking it down. Instead I traced which queries were holding connections longest and found one analytics query, added by another team, that ran inside the request path and held a connection for two-plus seconds. I moved that query to an async job off the request path and left the pool size alone.*
>
> *p99 went back to about 280 milliseconds and stayed there through the next peak. I also added a connection-pool-saturation alert that pages before we hit the cap, because the real failure was that we'd been blind to the saturation for weeks. Since then, the first thing I check on any latency spike is contention versus per-request cost — the histogram shape tells you which, and it saved me hours that night.*

Why this scores: ownership ("I owned," "I didn't" raise the cap), impact (300ms→4s→280ms, a revenue problem), self-awareness and rigor (checked the DB limit before raising the pool — the senior move), growth (the alert, the histogram-first habit). It is ninety seconds and every sentence is a decision.

## Acceptance criteria

- A STAR write-up committed to `behavioral/story-bank/story-01-debugging.md` in your portfolio repo.
- A recorded rehearsal (audio or video) of you delivering it from memory, **at least 75 seconds** long. If you finished in 30 seconds, you skipped the Action — re-do it.
- You read the recording back at 1.25–1.5× and re-recorded a tightened second take.

## Common mistakes

- **Burying the result.** Ending on "...and then it was fixed" with no number. The latency restored *is* the result — lead with it.
- **"We" instead of "I."** "We figured out it was the connection pool" hides who did the work. You investigated; say "I."
- **No quantified impact.** "It got a lot faster" scores nothing. "p99 from 4s to 280ms" scores.
- **Rambling Situation.** Explaining the entire service architecture before getting to the symptom. Ten seconds: system, symptom, stakes.
- **Listing every dead end.** You can mention you ruled out a hypothesis ("I ruled out a slow query"), but do not narrate four dead ends — pick the one that shows judgment.

## What to commit to your portfolio repo

```
crunchtime-interview-prep-<you>/
└── behavioral/
    └── story-bank/
        ├── story-01-debugging.md            # the STAR write-up
        └── recordings/
            └── story-01.md                  # link to / notes on the recording
```

When done, push and move on to [Exercise 2 — The Conflict Story](./exercise-02-conflict-story.md).
