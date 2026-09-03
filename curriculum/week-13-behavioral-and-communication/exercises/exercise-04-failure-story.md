# Exercise 4 — The Failure Story

> **Category:** Failure / mistake (top signals: ownership + growth)
> **Difficulty:** Hard (the most-mishandled category)
> **Target time:** 90-second delivery, ~50 minutes to draft + record + tighten
> **Why now:** the failure story is the single category most candidates get wrong, because the instinct is to protect yourself — pick a fake failure, blame someone else, or claim you'd have succeeded with more time. All three undo the signal. The interviewer asks this *specifically* to see whether you can own a real mistake. Owned well, a failure story is one of your strongest assets.

<!-- deliverable-page: the answer is a written and recorded story, not a program -->

## The Brief

An interviewer asks about a time you failed. This is the single most-mishandled
question in the whole loop, because the instinct is to protect yourself: pick a
failure that is secretly a success, spread the blame, or claim it would have gone
fine with more time. All three destroy the signal, and all three are obvious from
the outside.

The question is asked *specifically* to see whether you can own a real mistake.
Owned properly, a failure story is one of the strongest assets you have — it is
the only category where the interviewer learns something they cannot get from
your résumé.

The deliverable is a written story and a recording of you telling it from memory.

## Starter

> *"Tell me about a time you failed. What happened, and what did you take away from it?"*

Draft your own answer first, in [`star_template.md`](./star_template.md),
with the recorder running. The model answer is further down this page,
under `## The Solution`, and reading it before you have drafted yours will
cost you the exercise — you will remember its story instead of finding
yours.

## Requirements

Draft your own first, in [`star_template.md`](./star_template.md). Pick a *real* failure with real consequences — not a humblebrag.

- [ ] **S — Situation (~10s):** the high-stakes context. ("I owned a database migration that I was confident about.")
- [ ] **T — Task (~10s):** what you were responsible for. ("I planned and ran the cutover.")
- [ ] **A — Action (~60s):** what you did, **including the mistake**, owned without flinching. What you decided, where your judgment was wrong, what the consequence was, and — critically — how *you* responded once it went wrong.
- [ ] **R — Result (~20s):** the honest outcome (the damage, and that you contained it) plus the concrete process you changed so it can't recur. The growth *is* the point of this story.

## Constraints

- **A real failure with real consequences.** "I worked too hard on it" is not a
  failure and everyone in the room knows it.
- **You made the mistake.** Not the team, not the process, not the person who
  gave you bad information. If your story needs somebody else to be at fault, it
  is the wrong story.
- **Say the consequence plainly.** Data lost, a customer affected, a launch
  missed. Softening it is the tell.
- **No "with more time I would have succeeded".** It undoes the ownership in one
  sentence.
- **Roughly a third of the Action is what you did after.** Containing it, telling
  people, fixing it. That part is what a hiring manager is actually buying.
- **The growth is concrete.** A process you changed, a check that now exists —
  not "I learned to be more careful".

## Expected output

Measure this, do not estimate it. Read the model answer below aloud at an
interview pace — about 150 words a minute — with a timer running:

```text
model answer   312 words   ~125s spoken
target         75-120s, and 90s is the number to aim at
situation      ~10s
task           ~10s
action         ~60s
result         ~20s
```

Notice the model comes in at about 125 seconds — *over* the target,
not under it. That is deliberate, and it is the shape of a good first draft:
every sentence in it is doing work and it is still too long. Getting from
there to ninety seconds is what the second take is for, and it is done by
compressing sentences, never by dropping one of the four beats.

A draft that comes in far *under* the target has a different problem, and a
worse one: the Action is missing.

## Steps

1. Pick the failure you least want to tell. It is almost always the right one.
2. Write the consequence in one sentence before anything else. If you cannot write
   it without hedging, work on that sentence until you can.
3. Draft in [`star_template.md`](./star_template.md), ten minutes.
4. Split the Action in two: what you did wrong, and what you did once you knew.
   Check the second half is substantial.
5. Name the concrete thing that changed afterwards.
6. Draft the follow-up answer to *"what would you have done with more time?"* —
   concretely, in terms of a test or a safeguard, never as "I would have
   succeeded".
7. Record from memory. Listen back for flinching. Re-record tightened.
8. Read the model answer below only now.

## The Solution

> *Read this only after drafting your own.*

> *About two years ago I owned a schema migration on our main user table — adding a column and backfilling it. I'd done migrations before and I was confident, so I planned to run the backfill in a single transaction over the weekend when traffic was low.*
>
> *That was my mistake. The table had grown to about eighty million rows, and the single-transaction backfill held a lock far longer than I'd estimated — long enough that it blocked writes and started timing out user-facing requests on a Saturday evening. We took roughly twenty minutes of partial write outage before I killed the migration. I want to be clear that this was my call and my error: I'd tested the migration on a staging table with a fraction of the production row count, so I never saw the lock duration that mattered, and I hadn't built a kill switch, so my "rollback" was a panicked manual abort. Once it was down, I focused on containment — I aborted the transaction, confirmed no data corruption from the partial backfill, and posted a clear incident update so support knew what was happening rather than guessing. Then I re-did the migration properly the next week: batched backfill in chunks of ten thousand rows with a pause between batches, a feature flag to halt it instantly, and a load test against a production-sized table first.*
>
> *The honest result is that I caused a twenty-minute partial outage that I should have prevented. What I changed has stuck with me on every migration since: I never test a data migration against anything smaller than production scale, and I never run one without a kill switch. I've since run a dozen migrations on bigger tables with zero incidents, specifically because of what that Saturday taught me. I'd rather tell you about a real one I learned from than a comfortable one I didn't.*

Why this scores: ownership (repeated, unflinching — "my call and my error," "I should have prevented"), growth (two concrete habits, proven by the dozen clean migrations since), self-awareness (named exactly why the staging test lied), impact (the outage quantified honestly, the containment). The closing line ("a real one I learned from") signals that the candidate understands what the question is for. A candidate who owns a real failure scores *higher* than one who claims never to have failed.

## How to deliver it

Record yourself telling it from memory — audio or video, phone is fine. Then
listen back at 1.25 to 1.5 times speed, which makes padding and filler
impossible to miss, and record a second tightened take.

Commit both the write-up and a note on the recording:

```
crunchtime-interview-prep-<you>/
└── behavioral/
    └── story-bank/
        ├── story-04-failure.md
        └── recordings/
            └── story-04.md
```

When done, push and move on to [Exercise 5 — The Ambiguity Story](./exercise-05-ambiguity-story.md).

## Common bugs to catch

- **The fake failure.** "I'm too much of a perfectionist." Interviewers have heard it; it reads as evasive and forfeits the whole answer. Pick a real one.
- **The blame-shift.** "The failure was really QA's fault for not catching it." This is the fastest way to fail the question. Own your part.
- **No growth.** A failure with no lesson is just a failure. The concrete process you changed is the signal — make it specific ("batched, kill switch, production-scale test"), not vague ("I learned to be more careful").
- **Retroactive success.** Using "what I'd do differently" to claim you'd actually have nailed it undoes the ownership. The failure was real; let it be real.
- **Hiding the consequence.** "It almost caused a problem but I caught it" is a near-miss, not a failure. The question wants a real consequence you owned.

## Acceptance checklist

- [ ] A STAR write-up committed to `behavioral/story-bank/story-04-failure.md`.
- [ ] A recorded rehearsal, **at least 80 seconds**, delivered from memory.
- [ ] A listen-back at 1.25–1.5× and a tightened re-record.
- [ ] A pre-drafted answer to the follow-up "what would you have done with more time?" — answered concretely (the kill switch, the production-scale test), *not* as "I'd have succeeded."

## Stretch

- Prepare the harder follow-up: *"Whose fault was it, really?"* The answer is
  yours, said once, without elaborating. Practise not filling the silence.
- Draft a **second** failure story. Some loops ask for two, and the second is
  always worse if it is produced on the spot.
- Take the debugging story from [Exercise 1](./exercise-01-debugging-story.md)
  and find the version of that incident where you were the cause. Most incidents
  have one, and the exercise is in being willing to look.
