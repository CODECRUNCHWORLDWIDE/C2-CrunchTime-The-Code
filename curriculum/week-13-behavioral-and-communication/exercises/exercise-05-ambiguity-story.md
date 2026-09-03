# Exercise 5 — The Ambiguity Story

> **Category:** Ambiguity / incomplete information (top signals: ownership + impact)
> **Difficulty:** Medium
> **Target time:** 90-second delivery, ~45 minutes to draft + record + tighten
> **Why last:** the ambiguity story's Action beats most resemble the FRAME Frame step — define the problem, make an explicit assumption, validate cheaply, ship. If you internalized the Frame step over twelve weeks of coding, you already have the skeleton of this story.

<!-- deliverable-page: the answer is a written and recorded story, not a program -->

## The Brief

An interviewer asks how you made progress on something where the requirements were
unclear or the information was missing.

This one should feel familiar. The beats of a good answer are the beats of the
Frame step you have been running for twelve weeks: define the real question, make
an explicit assumption, validate it cheaply, then build. What changes is that the
ambiguity came from a person rather than a problem statement.

The story that scores is one where **you** created the clarity. Waiting for
somebody else to specify it is the version that does not.

The deliverable is a written story and a recording of you telling it from memory.

## Starter

> *"Tell me about a time you had to make progress on something where the requirements were unclear or you didn't have all the information."*

Draft your own answer first, in [`star_template.md`](./star_template.md),
with the recorder running. The model answer is further down this page,
under `## The Solution`, and reading it before you have drafted yours will
cost you the exercise — you will remember its story instead of finding
yours.

## Requirements

Draft your own first, in [`star_template.md`](./star_template.md). Pick a story where *you* created the clarity — not where you waited for someone else to.

- [ ] **S — Situation (~10s):** the vague ask. ("A VP wanted 'a dashboard to see how the product is doing' — no spec, no metrics defined.")
- [ ] **T — Task (~10s):** that you owned turning the vague ask into something shippable.
- [ ] **A — Action (~60s):** how you created clarity — defined the real question behind the ask, made an explicit assumption, validated it cheaply (a sketch, a prototype, a quick stakeholder check), then built. The Frame step, applied.
- [ ] **R — Result (~20s):** what shipped, the adoption/impact number, and that you *created clarity others then used*. The lesson about operating without a spec.

## Constraints

- **Ninety seconds, spoken**, with the usual split.
- **You created the clarity.** A story where the spec eventually arrived from
  somewhere else answers a different question.
- **The assumption is explicit and stated out loud.** "I assumed X, and I checked
  it by Y" is the sentence the whole category is fishing for.
- **The validation is cheap.** A sketch, a prototype, a five-minute conversation.
  If your validation took three weeks, that is a different story about planning.
- **Somebody else used the clarity afterwards.** That is the proof it was
  clarity rather than a guess that happened to work.
- **Do not make the requester look foolish.** Vague asks are normal; handling
  them is the job.

## Expected output

Measure this, do not estimate it. Read the model answer below aloud at an
interview pace — about 150 words a minute — with a timer running:

```text
model answer   313 words   ~125s spoken
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

1. Pick the vaguest ask you have ever been given and shipped something for.
2. Write the *real* question behind the ask, in one sentence, as you eventually
   understood it. That sentence is the heart of the story.
3. Draft in [`star_template.md`](./star_template.md), ten minutes.
4. Name the assumption and the cheap check separately. Candidates routinely
   collapse them, and the collapse loses the point.
5. Find what shipped and who used it.
6. Record from memory, listen back at 1.25×, re-record tightened.
7. Read the model answer below only now.

## The Solution

> *Read this only after drafting your own.*

> *Early last year a VP asked our team for "a dashboard so leadership can see how the product is doing." That was the entire spec. Three engineers could have built three completely different things from that sentence, and I owned figuring out what it actually meant before we burned a sprint on the wrong one.*
>
> *I treated the vagueness as the problem to solve first, the same way I'd clarify an under-specified interview question. I didn't go build something and hope; I also didn't wait for the VP to write a spec he clearly wasn't going to write. Instead I made an explicit assumption — that "how the product is doing" meant the three or four numbers he'd actually look at in a Monday review — and I validated it cheaply. I spent an afternoon making a clickable mock in a spreadsheet with fake data showing weekly active users, activation rate, and week-over-week retention, and I walked him through it for fifteen minutes. That conversation was worth a week of guessing: it turned out he didn't care about raw active users at all, he cared about activation and a revenue-per-account number I hadn't thought of, and he wanted it weekly, not real-time — which massively simplified the engineering. I rescoped to those metrics, dropped the real-time requirement, and shipped the real dashboard in about a week instead of the month a real-time build would have taken.*
>
> *Leadership actually used it — it became a standing part of the Monday review, and a couple of other teams asked to fork it. The lesson, which I now apply to every vague ask: don't build to the literal words and don't wait for a spec — make your best assumption explicit, put a cheap throwaway artifact in front of the person, and let their reaction define the real requirements. A fifteen-minute mock review saved a month of building the wrong thing.*

Why this scores: ownership (owned defining the problem, made the call to rescope), impact (1 week vs ~1 month, adopted into the Monday review, forked by other teams), self-awareness (didn't build blind, didn't wait), growth (the "explicit assumption + cheap artifact" lesson), and the explicit parallel to the FRAME Frame step shows transfer. The senior move is creating clarity *cheaply* — the spreadsheet mock — rather than either guessing or stalling.

## How to deliver it

Record yourself telling it from memory — audio or video, phone is fine. Then
listen back at 1.25 to 1.5 times speed, which makes padding and filler
impossible to miss, and record a second tightened take.

Commit both the write-up and a note on the recording:

```
crunchtime-interview-prep-<you>/
└── behavioral/
    └── story-bank/
        ├── story-05-ambiguity.md
        └── recordings/
            └── story-05.md
```

When done, push. You now have five fresh stories. Combine them with your W1/W4 drafts and assemble the full bank in the [mini-project](../mini-project/README.md). The two [challenges](../challenges/README.md) are your dress rehearsals before Mock #3.

## Common bugs to catch

- **Waiting for clarity instead of creating it.** "The requirements were unclear so I asked my manager to clarify and then built what he said" surfaces no ownership. The signal is that *you* drove the clarity.
- **Guessing blind.** The opposite failure — building something on a pure guess with no validation. The senior move is the *cheap* validation (mock, prototype, quick review) before the expensive build.
- **No artifact.** "I thought hard about what they meant" is invisible. The clickable mock, the one-paragraph proposal, the prototype — the artifact is what made the clarity real.
- **No number.** "It worked out" scores nothing. "1 week instead of a month, adopted into the Monday review" scores.
- **Skipping the explicit assumption.** State the assumption you made out loud ("I assumed it meant the Monday-review numbers") — that is the part that mirrors the FRAME Frame step and reads as senior.

## Acceptance checklist

- [ ] A STAR write-up committed to `behavioral/story-bank/story-05-ambiguity.md`.
- [ ] A recorded rehearsal, **at least 80 seconds**, delivered from memory.
- [ ] A listen-back at 1.25–1.5× and a tightened re-record.

## Stretch

- Prepare the follow-up: *"What if your assumption had been wrong?"* The answer is
  about how cheaply you would have found out, not about being right.
- Map this story onto the Frame step explicitly, in writing, beat for beat. It is
  the clearest evidence you have that the method is a habit rather than a
  vocabulary.
- Deliver all five stories back to back, once, in one sitting. It is the first
  honest rehearsal for [Challenge 1](../challenges/challenge-01-full-behavioral-round.md).
