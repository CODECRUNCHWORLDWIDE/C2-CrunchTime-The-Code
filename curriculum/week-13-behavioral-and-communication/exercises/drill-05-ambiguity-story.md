# Drill 5 — The Ambiguity Story

> **Category:** Ambiguity / incomplete information (top signals: ownership + impact)
> **Difficulty:** Medium
> **Target time:** 90-second delivery, ~45 minutes to draft + record + tighten
> **Why last:** the ambiguity story's Action beats most resemble the UMPIRE Understand step — define the problem, make an explicit assumption, validate cheaply, ship. If you internalized the Understand step over twelve weeks of coding, you already have the skeleton of this story.

## The prompt

> *"Tell me about a time you had to make progress on something where the requirements were unclear or you didn't have all the information."*

## STAR checklist for this drill

Draft your own first, in [`star_template.md`](./star_template.md). Pick a story where *you* created the clarity — not where you waited for someone else to.

- [ ] **S — Situation (~10s):** the vague ask. ("A VP wanted 'a dashboard to see how the product is doing' — no spec, no metrics defined.")
- [ ] **T — Task (~10s):** that you owned turning the vague ask into something shippable.
- [ ] **A — Action (~60s):** how you created clarity — defined the real question behind the ask, made an explicit assumption, validated it cheaply (a sketch, a prototype, a quick stakeholder check), then built. The Understand step, applied.
- [ ] **R — Result (~20s):** what shipped, the adoption/impact number, and that you *created clarity others then used*. The lesson about operating without a spec.

## Worked example

> *Read this only after drafting your own.*

> *Early last year a VP asked our team for "a dashboard so leadership can see how the product is doing." That was the entire spec. Three engineers could have built three completely different things from that sentence, and I owned figuring out what it actually meant before we burned a sprint on the wrong one.*
>
> *I treated the vagueness as the problem to solve first, the same way I'd clarify an under-specified interview question. I didn't go build something and hope; I also didn't wait for the VP to write a spec he clearly wasn't going to write. Instead I made an explicit assumption — that "how the product is doing" meant the three or four numbers he'd actually look at in a Monday review — and I validated it cheaply. I spent an afternoon making a clickable mock in a spreadsheet with fake data showing weekly active users, activation rate, and week-over-week retention, and I walked him through it for fifteen minutes. That conversation was worth a week of guessing: it turned out he didn't care about raw active users at all, he cared about activation and a revenue-per-account number I hadn't thought of, and he wanted it weekly, not real-time — which massively simplified the engineering. I rescoped to those metrics, dropped the real-time requirement, and shipped the real dashboard in about a week instead of the month a real-time build would have taken.*
>
> *Leadership actually used it — it became a standing part of the Monday review, and a couple of other teams asked to fork it. The lesson, which I now apply to every vague ask: don't build to the literal words and don't wait for a spec — make your best assumption explicit, put a cheap throwaway artifact in front of the person, and let their reaction define the real requirements. A fifteen-minute mock review saved a month of building the wrong thing.*

Why this scores: ownership (owned defining the problem, made the call to rescope), impact (1 week vs ~1 month, adopted into the Monday review, forked by other teams), self-awareness (didn't build blind, didn't wait), growth (the "explicit assumption + cheap artifact" lesson), and the explicit parallel to the UMPIRE Understand step shows transfer. The senior move is creating clarity *cheaply* — the spreadsheet mock — rather than either guessing or stalling.

## Acceptance criteria

- A STAR write-up committed to `behavioral/story-bank/story-05-ambiguity.md`.
- A recorded rehearsal, **at least 80 seconds**, delivered from memory.
- A listen-back at 1.25–1.5× and a tightened re-record.

## Common mistakes

- **Waiting for clarity instead of creating it.** "The requirements were unclear so I asked my manager to clarify and then built what he said" surfaces no ownership. The signal is that *you* drove the clarity.
- **Guessing blind.** The opposite failure — building something on a pure guess with no validation. The senior move is the *cheap* validation (mock, prototype, quick review) before the expensive build.
- **No artifact.** "I thought hard about what they meant" is invisible. The clickable mock, the one-paragraph proposal, the prototype — the artifact is what made the clarity real.
- **No number.** "It worked out" scores nothing. "1 week instead of a month, adopted into the Monday review" scores.
- **Skipping the explicit assumption.** State the assumption you made out loud ("I assumed it meant the Monday-review numbers") — that is the part that mirrors the UMPIRE Understand step and reads as senior.

## What to commit to your portfolio repo

```
crunchtime-interview-prep-<you>/
└── behavioral/
    └── story-bank/
        ├── story-05-ambiguity.md
        └── recordings/
            └── story-05.md
```

When done, push. You now have five fresh stories. Combine them with your W1/W4 drafts and assemble the full bank in the [mini-project](../mini-project/README.md). The two [challenges](../challenges/README.md) are your dress rehearsals before Mock #3.
