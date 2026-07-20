# Week 13 — Behavioral & Communication

```
┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐
│ U │  │ M │  │ P │  │ I │  │ R │  │ E │
└───┘  └───┘  └───┘  └───┘  └───┘  └───┘
```

> *Week 12 installed backtracking — the choose-explore-unchoose template that enumerates every solution to a combinatorial decision problem, the last of the pure algorithm weeks of Phase 2. Week 13 installs the **behavioral** skill set: the eight categories of "tell me about a time…," the STAR structure that turns a war story into a scored answer, a **story bank** of twelve-plus refined anecdotes that covers every category, the discipline of thinking aloud under pressure, and the moves for handling ambiguous, hostile, and curveball questions without flinching. This is the **first week of Phase 4 — Capstone & Onsite Prep.** STAR is to the behavioral round what UMPIRE is to the coding round: a mechanical method that frees your attention from "what do I say next" so you can spend it on signal. By Sunday you can hear any behavioral prompt, name which of the eight categories it tests in five seconds, reach for the right story from your bank, and deliver it in ninety seconds with a quantified result and a clear "I" — and you can recover gracefully when the interviewer pushes back, goes quiet, or asks something you are not allowed to answer.*

Welcome to Week 13 of **C2 · CrunchTime — The Code** — the first week of Phase 4, the capstone-and-onsite-prep block (Weeks 13–15). For twelve weeks you have trained the coding round: the UMPIRE method, twelve algorithm patterns, two recorded mocks. A real onsite is not five coding rounds. It is three or four coding rounds **plus** a behavioral round — sometimes two — plus a hiring-manager conversation that is behavioral in everything but name. Candidates who can invert a binary tree and freeze on "tell me about a time you disagreed with your manager" do not get the offer. This week closes that gap.

The misconception this week corrects: most engineers believe the behavioral round is "soft" — unstructured, unscorable, a vibe check you either pass or fail on personality. It is not. Behavioral interviewers grade against a rubric, the same way a coding interviewer grades against correctness and complexity. The rubric measures **signals**: ownership, quantified impact, self-awareness, collaboration, and growth. A rambling, modest, "we did a great job as a team" answer scores low on every axis — not because the candidate is a bad engineer, but because the answer surfaced no signal. STAR is the structure that surfaces signal on purpose.

The mechanical method is four letters: **Situation, Task, Action, Result.** The trap — the behavioral equivalent of forgetting the leaf-copy in backtracking — is over-spending on Situation and Task (the setup) and under-spending on Action and Result (where the signal lives). A senior candidate spends ten seconds on S and T, sixty on A, twenty on R, and lands the whole answer in ninety seconds with a number attached. We will drill that budget until it is reflexive.

By Sunday of Week 13 you will:

- **Recognize** which of the eight behavioral categories a prompt tests in five seconds, and which story from your bank you will deploy to answer it.
- **Draft and refine** a story bank of **twelve-plus** STAR anecdotes, each cross-referenced to the categories it covers, such that every one of the eight categories is covered by at least one story (most by two).
- **Deliver** any story from the bank in a ninety-second STAR structure: ten seconds Situation, ten seconds Task, sixty seconds Action (first-person, specific, technical), twenty seconds Result (quantified, with a follow-on of what you learned).
- **Hold the "I" discipline** — describe what *you* did, not what the team did, without sounding like you are taking credit for others' work. The senior move is "I" for your contribution and "we" for the outcome.
- **Quantify every result** — latency cut, dollars saved, incidents avoided, percent improved, time-to-ship reduced, people unblocked. A result without a number is a result the interviewer cannot score.
- **Think aloud under pressure** — narrate your reasoning when an interviewer goes quiet or pushes back, the same way the UMPIRE method makes you narrate a coding solve.
- **Recover** from a mid-answer wrong turn, a hostile follow-up, an ambiguous prompt, and an illegal/inappropriate question — gracefully, without freezing and without escalating.
- Have drafted **five new stories** this week (Drills 1–5) on top of the early stories you started in the Week 1 and Week 4 homework, refining the combined set to the twelve-plus that the mini-project ships.
- Have shipped **two challenges** — a full forty-five-minute mock behavioral round (six to eight questions, recorded, two-pass self-feedback) and a hostile-and-curveball round (weakness, why-leaving, illegal-question deflection, "sell me this pen").
- Have shipped the quiz, the homework, and the **mini-project**: the behavioral story bank itself — twelve-plus STAR anecdotes, a coverage matrix, and recordings — committed to your portfolio under `behavioral/story-bank/`.

---

## Learning objectives

By the end of this week, you will be able to:

- **Recognize the eight categories.** Conflict; Failure / mistake; Leadership / influence-without-authority; Ambiguity / incomplete-information; Teamwork / collaboration; Dealing with a difficult person; Biggest accomplishment / proudest work; "Why this company / role" and "Tell me about yourself." Given any prompt, name the category in five seconds — most prompts map cleanly, a few are deliberate hybrids, and naming the hybrid is itself a signal.
- **Score an answer against the rubric.** The five signals interviewers grade: **ownership** (you drove it, you did not watch it happen), **impact** (a quantified result, not "it went well"), **self-awareness** (you can name what you would do differently), **collaboration** (you worked with and through other people), **growth** (the experience changed how you operate). Hear an answer and name which signals it surfaced and which it missed.
- **Structure any answer in STAR.** Situation (the context, briefly), Task (your specific responsibility or the problem you owned), Action (what *you* did, step by step, the bulk of the answer), Result (the quantified outcome plus what you learned). Hold the 10/10/60/20-second budget.
- **Build a story bank.** Twelve-plus stories drawn from real projects, each written up once in full STAR, each tagged with the categories it covers, arranged in a coverage matrix so you can see at a glance that every category has a story behind it. Reuse is the point — one well-refined "migration" story answers Conflict, Leadership, *and* Ambiguity prompts depending on which beat you emphasize.
- **Think aloud under pressure.** Treat silence as a prompt, not a verdict. Narrate the structure ("Let me give you the situation first, then what I did…"). When pushed, restate the question, take a breath, and answer the question that was asked — not the one you wish had been asked.
- **Reframe the round as non-adversarial.** The interviewer is not trying to trick you; they are trying to find a reason to hire you. Hostile-sounding follow-ups are usually probes for depth, not attacks. Answering them as collaboration rather than combat is the senior signal.
- **Handle the hard questions.** The weakness question (name a real one plus the system you built to manage it), the why-leaving question (forward-looking, never bitter), the failure-with-a-twist ("what if you'd had more time"), the illegal/inappropriate question (deflect to the job, do not litigate), and the curveball ("sell me this pen," "how many golf balls fit in a bus") — each has a move, and we drill the moves.
- **Write the follow-up email.** A short, specific, same-day note that references one concrete thing from the conversation. The lowest-effort, highest-leverage move in the entire loop, and the one most candidates skip.

---

## Prerequisites

- **Weeks 1–12 complete.** You have shipped UMPIRE write-ups for every pattern through backtracking, two recorded mocks (Mock #1 in W4, Mock #2 in W8), and you can narrate a coding solve aloud. The narration habit transfers directly — thinking aloud in a behavioral round is the same muscle as thinking aloud in a coding round.
- **The early behavioral stories you started in the W1 and W4 homework.** Week 1's homework asked you to jot two rough "tell me about a time" anecdotes; Week 4's mock-prep asked for two more. Those four rough drafts are the seed of this week's story bank. Have them in front of you — even as bullet points — before Monday.
- **45 minutes of vocalization space.** A room where you can talk aloud for forty-five minutes without an audience, and a way to record audio or video (your phone is fine). You cannot refine a spoken answer you have only ever written. Every drill this week ends with "record it and listen back." If you do not have private space, a parked car works; many of our learners drafted their first story banks in one.

---

## Topics covered

- **The eight behavioral categories** — Conflict, Failure, Leadership/influence, Ambiguity, Teamwork, Difficult-person, Biggest-accomplishment, Why-this-role/tell-me-about-yourself; the category-recognition skill
- **The behavioral scoring rubric** — the five signals (ownership, impact, self-awareness, collaboration, growth) and what a high-signal versus low-signal answer sounds like on each
- **The STAR method in depth** — Situation/Task/Action/Result; the over-spend-on-S/T trap; the 10/10/60/20 budget; the ninety-second target
- **The "I" vs "we" discipline** — "I" for your contribution, "we" for the outcome; taking credit without grabbing it
- **Quantifying results** — turning "it went well" into "p99 latency dropped from 1.2s to 280ms, and on-call pages for that service fell to near zero"
- **The story bank** — twelve-plus stories, the coverage matrix, the reuse principle (one story answers multiple categories)
- **Thinking aloud under pressure** — narrating structure, treating silence as a prompt, the restate-and-breathe move
- **The non-adversarial reframe** — the interviewer wants to hire you; hostile follow-ups are depth probes
- **Handling ambiguous questions** — clarify the scope, state your assumption, then answer; the same Understand-step discipline as UMPIRE
- **Handling hostile / curveball / illegal questions** — the weakness move, the why-leaving move, the failure-with-a-twist, the illegal-question deflect, the estimation curveball
- **The recovery move** — what to do when you realize mid-answer you picked the wrong story or buried the result
- **The follow-up email** — the same-day, specific, low-effort, high-leverage close

---

## Weekly schedule (intensive · 36h)

| Day | Focus | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project | Self-Study | Daily Total |
|-----|-------|---------:|----------:|-----------:|----------:|---------:|-------------:|-----------:|------------:|
| Monday | Lecture 1 (eight categories + rubric); Drill 1 (debugging story) | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Tuesday | Lecture 2 (STAR + story bank); Drill 2 (conflict story) | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Wednesday | Lecture 3 (pressure + hostile); Drills 3–4 (leadership, failure) | 2h | 2h | 0h | 0.5h | 0.5h | 0h | 0.5h | 5.5h |
| Thursday | Drill 5 (ambiguity); story-bank drafting; challenge ramp | 0h | 1h | 1h | 0.5h | 1h | 1.5h | 1h | 6h |
| Friday | Challenge 1 (full 45-min mock behavioral round) | 0h | 0h | 2h | 0.5h | 1h | 1.5h | 0.5h | 5.5h |
| Saturday | Challenge 2 (hostile/curveball round); story-bank build | 0h | 0h | 1.5h | 0h | 1h | 2h | 0h | 4.5h |
| Sunday | Coverage matrix + record the bank + retro + push | 0h | 0h | 0h | 0.5h | 0.5h | 3.5h | 0h | 4.5h |
| **Total** | | **6h** | **7h** | **5h** | **3h** | **6h** | **8.5h** | **3h** | **38h** |

(The week budgets ~36 hours; the table sums slightly higher to absorb the Phase-4 ramp. Drop 0.5h from Self-Study on Monday and Tuesday if 36h is your hard cap. Unlike algorithm weeks, the highest-leverage hours here are the recorded-and-played-back ones — protect those first.)

**Mastery (10h/wk):** spread the same content over two calendar weeks (Phase 4 maps to mastery Q4, ~weeks 40–52). The story bank lands around calendar Week 40 of the mastery pathway; refine two or three stories per sitting rather than all twelve in one weekend. See the [mastery study plan](../study-plans/mastery-1-year.md).

---

## How to navigate this week

| File | What's inside |
|------|---------------|
| [README.md](./README.md) | This overview |
| [resources.md](./resources.md) | Behavioral & communication references — Tech Interview Handbook, Amazon Leadership Principles, Never Split the Difference, Crucial Conversations, Staff Engineer, The Manager's Path — plus the STAR cheatsheet and a glossary |
| [lecture-notes/01-the-eight-categories-and-the-rubric.md](./lecture-notes/01-the-eight-categories-and-the-rubric.md) | The eight categories, the five-signal rubric, what high- vs low-signal answers sound like |
| [lecture-notes/02-the-star-method-and-the-story-bank.md](./lecture-notes/02-the-star-method-and-the-story-bank.md) | STAR in depth, the S/T over-spend trap, the "I vs we" discipline, quantifying results, the story bank and coverage matrix |
| [lecture-notes/03-communication-under-pressure-and-hostile-questions.md](./lecture-notes/03-communication-under-pressure-and-hostile-questions.md) | Thinking aloud, the non-adversarial reframe, ambiguous questions, hostile/curveball/illegal questions, the recovery move, the follow-up email |
| [exercises/README.md](./exercises/README.md) | Index of the five STAR drafting drills and the portfolio tree they produce |
| [exercises/drill-01-debugging-story.md](./exercises/drill-01-debugging-story.md) | "Tell me about a time you debugged a hard problem" — full worked STAR example |
| [exercises/drill-02-conflict-story.md](./exercises/drill-02-conflict-story.md) | "Tell me about a disagreement with a coworker" — full worked STAR example |
| [exercises/drill-03-leadership-influence-story.md](./exercises/drill-03-leadership-influence-story.md) | "Tell me about a time you led without authority" — full worked STAR example |
| [exercises/drill-04-failure-story.md](./exercises/drill-04-failure-story.md) | "Tell me about a time you failed" — full worked STAR example |
| [exercises/drill-05-ambiguity-story.md](./exercises/drill-05-ambiguity-story.md) | "Tell me about a time you worked with unclear requirements" — full worked STAR example |
| [exercises/star_template.md](./exercises/star_template.md) | The reusable STAR write-up template (the behavioral analogue of `umpire_template.md`) |
| [challenges/README.md](./challenges/README.md) | Index of the two mock rounds |
| [challenges/challenge-01-full-behavioral-round.md](./challenges/challenge-01-full-behavioral-round.md) | A full 45-minute mock behavioral round — 6–8 questions, timing, rubric, two-pass self-feedback |
| [challenges/challenge-02-hostile-and-curveball-round.md](./challenges/challenge-02-hostile-and-curveball-round.md) | Hostile, ambiguous, curveball, and illegal questions — worked responses and the recovery framework |
| [quiz.md](./quiz.md) | 10 category-recognition prompts — name the category, the story you'd deploy, and the top signal |
| [homework.md](./homework.md) | Six tasks (~5–6 hrs) — refine to 12 stories, record a round, build the matrix, draft the pitch and the email, reflect |
| [mini-project/README.md](./mini-project/README.md) | **The story bank** — 12+ STAR anecdotes, coverage matrix, recordings — the week's deliverable |

---

## Stretch goals

- **Read the full Amazon Leadership Principles list** and map each of your story-bank anecdotes to one or two principles. Amazon's behavioral loop ("bar raiser") grades explicitly against these sixteen principles; even at non-Amazon companies, "Ownership," "Dive Deep," "Earn Trust," and "Deliver Results" are the universal axes. Annotating your stories against them sharpens the signal you lead with.
- **Record a "tell me about yourself" pitch and cut it to 90 seconds.** Most candidates ramble for three minutes. The senior version is ninety seconds: who you are now, the through-line of your last two roles, and why this conversation. Record, time, cut, re-record until it lands under ninety.
- **Run a peer mock both directions.** Pair with another C2 learner; you interview them for forty-five minutes, then swap. Interviewing someone else is the fastest way to internalize the rubric — you will hear the missing "I," the buried result, and the unquantified outcome in *their* answers, then catch them in your own.
- **Read one of Chris Voss's tactical-empathy chapters in "Never Split the Difference"** and try a calibrated question ("How am I supposed to…?") as a response to a hardball compensation or scope question. The negotiation framing is the same as the behavioral one: lower the temperature, keep the other person talking.
- **Build a "story-to-principle" lookup card.** One index card: eight categories down the left, your twelve story titles across the top, a check in each cell the story covers. This is the physical artifact of the coverage matrix; carry it the morning of an onsite.

---

## What "done" looks like for Week 13

A learner who has shipped Week 13 has, in their portfolio repo:

- Five new STAR write-ups (the five drills), each refined and recorded, under `behavioral/story-bank/`.
- The combined story bank of **twelve-plus** stories, each in the STAR template, each tagged with the categories it covers.
- A **coverage matrix** (`behavioral/story-bank/coverage-matrix.md`) showing every one of the eight categories is covered by at least one story.
- Two challenge recordings: the full 45-minute mock behavioral round and the hostile/curveball round, each with two-pass self-feedback notes.
- A 90-second "tell me about yourself" pitch (text + recording) and a follow-up-email template.
- The quiz answered (score recorded) and a retro naming the one category you are weakest on going into Mock #3.
- A push log showing daily commits Mon–Sun.

If all of that is present and pushed, Phase 4's first week is closed. Your coding game is already sharp; now your behavioral game matches it.

---

## A note on the Phase 4 ramp

Phase 4 — Capstone & Onsite Prep — is the final block: Weeks 13–15. Week 13 (this week) installs the behavioral skill set. Week 14 is **Mock #3** (with a bit-manipulation-and-tries algorithm refresher woven in); Mock #3 is the first full-loop simulation that includes a behavioral round, so the story bank you build this week is *used* next week under timed pressure. Week 15 is the capstone and **Mock #4** — the dress rehearsal for the real thing.

The mistake to avoid this week is treating behavioral prep as something you can "wing." You cannot. The story bank is exactly like the UMPIRE write-up library: an asset you build once and draw on forever. Engineers who freeze in behavioral rounds are almost always engineers who tried to invent the answer in real time. Engineers who shine are reaching into a bank of twelve rehearsed stories and selecting the right one — the cognitive load is *selection*, not *invention*, and selection is fast. STAR is to behavioral what UMPIRE is to coding: the method that frees your attention from "what do I say" so you can spend it on signal.

If you find yourself ahead by Friday, the right stretch is **not** drafting a thirteenth story — it is recording your best three stories a second time and cutting thirty seconds out of each. Concision is the skill that separates a good behavioral round from a great one.

If you find yourself behind by Wednesday, prioritize the five drills and the coverage matrix over a polished mini-project README. A rough story that covers a missing category beats a beautiful story for a category you already had.

---

## Up next

[Week 14 — Bit Manipulation, Tries + Mock #3](../week-14-mock-3-bit-manipulation-and-tries/) — once your twelve-plus stories are written, your coverage matrix shows no empty category, and you can deliver any story from the bank in ninety seconds without notes. Mock #3 next week is the first full loop that grades the behavioral round; Mock #4 in W15 is the dress rehearsal.

---

*If you find errors in this material, please open an issue or send a PR. Future learners will thank you.*
