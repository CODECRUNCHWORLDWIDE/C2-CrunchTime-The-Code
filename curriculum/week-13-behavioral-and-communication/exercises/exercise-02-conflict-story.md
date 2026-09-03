# Exercise 2 — The Conflict Story

> **Category:** Conflict (top signals: collaboration + self-awareness)
> **Difficulty:** Medium
> **Target time:** 90-second delivery, ~45 minutes to draft + record + tighten
> **Why now:** the conflict story is one of the two most-mishandled categories (failure is the other). The trap is telling a story where you were right and the other person was wrong — which surfaces zero collaboration and reads as arrogant. We drill it mid-week with a worked example because the framing is the hard part.

<!-- deliverable-page: the answer is a written and recorded story, not a program -->

## The Brief

An interviewer asks about a disagreement with a coworker. The trap is enormous and
almost everybody walks into it: telling a story in which you were right and the
other person was wrong.

That story surfaces zero collaboration. It reads as somebody who wins arguments,
which is not what the question is testing. What scores is a disagreement you
*engaged* — where you understood the other position well enough to state it
fairly, found the goal you both shared, and resolved it on evidence rather than
by rank or by silence.

The framing is the whole exercise, which is why this one comes mid-week with a
worked model attached.

The deliverable is a written story and a recording of you telling it from memory.

## Starter

> *"Tell me about a time you disagreed with a coworker. What was the disagreement, and how did you resolve it?"*

Draft your own answer first, in [`star_template.md`](./star_template.md),
with the recorder running. The model answer is further down this page,
under `## The Solution`, and reading it before you have drafted yours will
cost you the exercise — you will remember its story instead of finding
yours.

## Requirements

Draft your own answer first, in [`star_template.md`](./star_template.md). The framing is the whole exercise here — pick a real disagreement where you genuinely understood the other side.

- [ ] **S — Situation (~10s):** the decision under disagreement and why it mattered. ("We had to pick a datastore for a new service and a senior teammate and I disagreed.")
- [ ] **T — Task (~10s):** your stake. ("I'd be on-call for this service, so I cared a lot about the operational story.")
- [ ] **A — Action (~60s):** how you *engaged* the disagreement. The senior move: you sought to understand their reasoning first, found the shared goal, and resolved it on evidence — not by pulling rank or going silent.
- [ ] **R — Result (~20s):** the outcome (which choice, and that it worked) **and** that the relationship survived. The lesson about how you handle disagreement.

## Constraints

- **Ninety seconds, spoken**, with the same ten / ten / sixty / twenty split.
- **State the other position fairly, in their words.** If you cannot make their
  case sound reasonable, you did not understand it, and the interviewer will hear
  that.
- **The resolution is evidence or a shared goal.** Not "they eventually agreed",
  not "I escalated", not "I let it go".
- **The relationship survives, and you say so.** A conflict story that ends with
  the outcome and not the working relationship has answered half the question.
- **You may lose.** A story where their idea was better and you say so is a
  strong answer, provided you say what changed your mind.
- **No villains.** The moment a coworker becomes the antagonist, the story is
  about them and the interviewer learns nothing about you.

## Expected output

Measure this, do not estimate it. Read the model answer below aloud at an
interview pace — about 150 words a minute — with a timer running:

```text
model answer   291 words   ~116s spoken
target         75-120s, and 90s is the number to aim at
situation      ~10s
task           ~10s
action         ~60s
result         ~20s
```

Notice the model comes in at about 116 seconds — *over* the target,
not under it. That is deliberate, and it is the shape of a good first draft:
every sentence in it is doing work and it is still too long. Getting from
there to ninety seconds is what the second take is for, and it is done by
compressing sentences, never by dropping one of the four beats.

A draft that comes in far *under* the target has a different problem, and a
worse one: the Action is missing.

## Steps

1. Pick the disagreement first, and check it against one test: can you state the
   other person's reasoning in a sentence that they would accept? If not, pick a
   different one.
2. Draft in [`star_template.md`](./star_template.md), ten minutes, no polishing.
3. Write the other position **before** your own. It forces the framing.
4. Name the shared goal explicitly in the Action. It is the sentence that turns a
   disagreement into a collaboration.
5. Record from memory. Listen back at 1.25× specifically for tone — this is the
   story where you can sound defensive without noticing.
6. Re-record tightened. That take is the deliverable.
7. Read the model answer below only now.

## The Solution

> *Read this only after drafting your own.*

> *A while back my team was standing up a new notifications service, and a senior engineer I respected wanted to use a document store for the message data. I disagreed — I thought we needed a relational store, because the access patterns clearly involved joins across users, channels, and delivery status, and I'd be one of the people on-call for this thing.*
>
> *My first instinct was to argue my case harder, but I caught that and did something better: I asked him to walk me through why the document store fit. It turned out his real concern wasn't the data model at all — he'd been burned by a painful schema migration on a relational database the previous year and was optimizing to avoid that pain. That reframed the disagreement entirely. We didn't actually disagree about the access patterns; we disagreed about migration risk. So I proposed we time-box a half-day spike: I'd model the schema and write a sample migration using our migration tooling, and we'd look at it together. The migration turned out to be straightforward with the tooling we'd adopted since his bad experience, and seeing that, he was comfortable with relational. I also adopted his concern as a real constraint — I documented a migration runbook up front so the next schema change wouldn't be scary.*
>
> *We shipped on relational, the joins stayed simple, and the service has been low-maintenance on-call since. More importantly, that engineer and I worked together well afterward — he later told me he appreciated that I dug into his reasoning instead of just out-arguing him. The lesson I took: when someone smart disagrees with me, the disagreement is usually about a constraint I can't see yet. Finding that constraint resolves most arguments faster than winning them.*

Why this scores: collaboration (sought to understand, found the shared goal, relationship survived), self-awareness (caught my own instinct to argue), ownership (I proposed the spike, I wrote the runbook), impact (low-maintenance on-call, shipped on the right store), growth (the "disagreement is about a hidden constraint" lesson). Note that the candidate "won" the technical decision but the story is *not* about winning — it is about how the disagreement was handled.

## How to deliver it

Record yourself telling it from memory — audio or video, phone is fine. Then
listen back at 1.25 to 1.5 times speed, which makes padding and filler
impossible to miss, and record a second tightened take.

Commit both the write-up and a note on the recording:

```
crunchtime-interview-prep-<you>/
└── behavioral/
    └── story-bank/
        ├── story-02-conflict.md
        └── recordings/
            └── story-02.md
```

When done, push and move on to [Exercise 3 — The Leadership / Influence Story](./exercise-03-leadership-influence-story.md).

## Common bugs to catch

- **The "I was right" story.** If your story is just "I knew better and proved it," you surface no collaboration. Pick or reframe a story where you genuinely understood the other side.
- **Trashing the coworker.** The interviewer is grading *you*, not the coworker. Empathy for the other side is the signal; contempt is a red flag.
- **No resolution.** A disagreement with no resolution ("we just agreed to disagree and I did it my way") surfaces no collaboration. Show how it actually resolved.
- **"We" hiding the move.** "We talked it out" is vague. *You* asked him to walk through his reasoning; *you* proposed the spike. Keep the "I" on your moves.
- **Forgetting the relationship outcome.** A conflict story isn't done until you've said the relationship survived (or improved). That's half the signal.

## Acceptance checklist

- [ ] A STAR write-up committed to `behavioral/story-bank/story-02-conflict.md`.
- [ ] A recorded rehearsal, **at least 80 seconds**, delivered from memory.
- [ ] A listen-back at 1.25–1.5× and a tightened re-record.

## Stretch

- Prepare the follow-up: *"What if they had refused to look at the data?"* The
  honest answer involves escalation, and saying how you would escalate without
  making it personal is a senior signal.
- Draft a second conflict story where **you were wrong**. Some interviewers ask
  for it directly, and it is much harder to produce cold.
- Deliver it once from the other person's point of view, out loud, to yourself.
  It is a rehearsal technique, and it usually exposes a place where your version
  is unfair.
