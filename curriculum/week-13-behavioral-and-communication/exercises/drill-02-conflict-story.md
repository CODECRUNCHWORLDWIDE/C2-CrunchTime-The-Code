# Drill 2 — The Conflict Story

> **Category:** Conflict (top signals: collaboration + self-awareness)
> **Difficulty:** Medium
> **Target time:** 90-second delivery, ~45 minutes to draft + record + tighten
> **Why now:** the conflict story is one of the two most-mishandled categories (failure is the other). The trap is telling a story where you were right and the other person was wrong — which surfaces zero collaboration and reads as arrogant. We drill it mid-week with a worked example because the framing is the hard part.

## The prompt

> *"Tell me about a time you disagreed with a coworker. What was the disagreement, and how did you resolve it?"*

## STAR checklist for this drill

Draft your own answer first, in [`star_template.md`](./star_template.md). The framing is the whole exercise here — pick a real disagreement where you genuinely understood the other side.

- [ ] **S — Situation (~10s):** the decision under disagreement and why it mattered. ("We had to pick a datastore for a new service and a senior teammate and I disagreed.")
- [ ] **T — Task (~10s):** your stake. ("I'd be on-call for this service, so I cared a lot about the operational story.")
- [ ] **A — Action (~60s):** how you *engaged* the disagreement. The senior move: you sought to understand their reasoning first, found the shared goal, and resolved it on evidence — not by pulling rank or going silent.
- [ ] **R — Result (~20s):** the outcome (which choice, and that it worked) **and** that the relationship survived. The lesson about how you handle disagreement.

## Worked example

> *Read this only after drafting your own.*

> *A while back my team was standing up a new notifications service, and a senior engineer I respected wanted to use a document store for the message data. I disagreed — I thought we needed a relational store, because the access patterns clearly involved joins across users, channels, and delivery status, and I'd be one of the people on-call for this thing.*
>
> *My first instinct was to argue my case harder, but I caught that and did something better: I asked him to walk me through why the document store fit. It turned out his real concern wasn't the data model at all — he'd been burned by a painful schema migration on a relational database the previous year and was optimizing to avoid that pain. That reframed the disagreement entirely. We didn't actually disagree about the access patterns; we disagreed about migration risk. So I proposed we time-box a half-day spike: I'd model the schema and write a sample migration using our migration tooling, and we'd look at it together. The migration turned out to be straightforward with the tooling we'd adopted since his bad experience, and seeing that, he was comfortable with relational. I also adopted his concern as a real constraint — I documented a migration runbook up front so the next schema change wouldn't be scary.*
>
> *We shipped on relational, the joins stayed simple, and the service has been low-maintenance on-call since. More importantly, that engineer and I worked together well afterward — he later told me he appreciated that I dug into his reasoning instead of just out-arguing him. The lesson I took: when someone smart disagrees with me, the disagreement is usually about a constraint I can't see yet. Finding that constraint resolves most arguments faster than winning them.*

Why this scores: collaboration (sought to understand, found the shared goal, relationship survived), self-awareness (caught my own instinct to argue), ownership (I proposed the spike, I wrote the runbook), impact (low-maintenance on-call, shipped on the right store), growth (the "disagreement is about a hidden constraint" lesson). Note that the candidate "won" the technical decision but the story is *not* about winning — it is about how the disagreement was handled.

## Acceptance criteria

- A STAR write-up committed to `behavioral/story-bank/story-02-conflict.md`.
- A recorded rehearsal, **at least 80 seconds**, delivered from memory.
- A listen-back at 1.25–1.5× and a tightened re-record.

## Common mistakes

- **The "I was right" story.** If your story is just "I knew better and proved it," you surface no collaboration. Pick or reframe a story where you genuinely understood the other side.
- **Trashing the coworker.** The interviewer is grading *you*, not the coworker. Empathy for the other side is the signal; contempt is a red flag.
- **No resolution.** A disagreement with no resolution ("we just agreed to disagree and I did it my way") surfaces no collaboration. Show how it actually resolved.
- **"We" hiding the move.** "We talked it out" is vague. *You* asked him to walk through his reasoning; *you* proposed the spike. Keep the "I" on your moves.
- **Forgetting the relationship outcome.** A conflict story isn't done until you've said the relationship survived (or improved). That's half the signal.

## What to commit to your portfolio repo

```
crunchtime-interview-prep-<you>/
└── behavioral/
    └── story-bank/
        ├── story-02-conflict.md
        └── recordings/
            └── story-02.md
```

When done, push and move on to [Drill 3 — The Leadership / Influence Story](./drill-03-leadership-influence-story.md).
