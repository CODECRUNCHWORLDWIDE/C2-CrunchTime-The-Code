# Drill 4 — The Failure Story

> **Category:** Failure / mistake (top signals: ownership + growth)
> **Difficulty:** Hard (the most-mishandled category)
> **Target time:** 90-second delivery, ~50 minutes to draft + record + tighten
> **Why now:** the failure story is the single category most candidates get wrong, because the instinct is to protect yourself — pick a fake failure, blame someone else, or claim you'd have succeeded with more time. All three undo the signal. The interviewer asks this *specifically* to see whether you can own a real mistake. Owned well, a failure story is one of your strongest assets.

## The prompt

> *"Tell me about a time you failed. What happened, and what did you take away from it?"*

## STAR checklist for this drill

Draft your own first, in [`star_template.md`](./star_template.md). Pick a *real* failure with real consequences — not a humblebrag.

- [ ] **S — Situation (~10s):** the high-stakes context. ("I owned a database migration that I was confident about.")
- [ ] **T — Task (~10s):** what you were responsible for. ("I planned and ran the cutover.")
- [ ] **A — Action (~60s):** what you did, **including the mistake**, owned without flinching. What you decided, where your judgment was wrong, what the consequence was, and — critically — how *you* responded once it went wrong.
- [ ] **R — Result (~20s):** the honest outcome (the damage, and that you contained it) plus the concrete process you changed so it can't recur. The growth *is* the point of this story.

## Worked example

> *Read this only after drafting your own.*

> *About two years ago I owned a schema migration on our main user table — adding a column and backfilling it. I'd done migrations before and I was confident, so I planned to run the backfill in a single transaction over the weekend when traffic was low.*
>
> *That was my mistake. The table had grown to about eighty million rows, and the single-transaction backfill held a lock far longer than I'd estimated — long enough that it blocked writes and started timing out user-facing requests on a Saturday evening. We took roughly twenty minutes of partial write outage before I killed the migration. I want to be clear that this was my call and my error: I'd tested the migration on a staging table with a fraction of the production row count, so I never saw the lock duration that mattered, and I hadn't built a kill switch, so my "rollback" was a panicked manual abort. Once it was down, I focused on containment — I aborted the transaction, confirmed no data corruption from the partial backfill, and posted a clear incident update so support knew what was happening rather than guessing. Then I re-did the migration properly the next week: batched backfill in chunks of ten thousand rows with a pause between batches, a feature flag to halt it instantly, and a load test against a production-sized table first.*
>
> *The honest result is that I caused a twenty-minute partial outage that I should have prevented. What I changed has stuck with me on every migration since: I never test a data migration against anything smaller than production scale, and I never run one without a kill switch. I've since run a dozen migrations on bigger tables with zero incidents, specifically because of what that Saturday taught me. I'd rather tell you about a real one I learned from than a comfortable one I didn't.*

Why this scores: ownership (repeated, unflinching — "my call and my error," "I should have prevented"), growth (two concrete habits, proven by the dozen clean migrations since), self-awareness (named exactly why the staging test lied), impact (the outage quantified honestly, the containment). The closing line ("a real one I learned from") signals that the candidate understands what the question is for. A candidate who owns a real failure scores *higher* than one who claims never to have failed.

## Acceptance criteria

- A STAR write-up committed to `behavioral/story-bank/story-04-failure.md`.
- A recorded rehearsal, **at least 80 seconds**, delivered from memory.
- A listen-back at 1.25–1.5× and a tightened re-record.
- A pre-drafted answer to the follow-up "what would you have done with more time?" — answered concretely (the kill switch, the production-scale test), *not* as "I'd have succeeded."

## Common mistakes

- **The fake failure.** "I'm too much of a perfectionist." Interviewers have heard it; it reads as evasive and forfeits the whole answer. Pick a real one.
- **The blame-shift.** "The failure was really QA's fault for not catching it." This is the fastest way to fail the question. Own your part.
- **No growth.** A failure with no lesson is just a failure. The concrete process you changed is the signal — make it specific ("batched, kill switch, production-scale test"), not vague ("I learned to be more careful").
- **Retroactive success.** Using "what I'd do differently" to claim you'd actually have nailed it undoes the ownership. The failure was real; let it be real.
- **Hiding the consequence.** "It almost caused a problem but I caught it" is a near-miss, not a failure. The question wants a real consequence you owned.

## What to commit to your portfolio repo

```
crunchtime-interview-prep-<you>/
└── behavioral/
    └── story-bank/
        ├── story-04-failure.md
        └── recordings/
            └── story-04.md
```

When done, push and move on to [Drill 5 — The Ambiguity Story](./drill-05-ambiguity-story.md).
