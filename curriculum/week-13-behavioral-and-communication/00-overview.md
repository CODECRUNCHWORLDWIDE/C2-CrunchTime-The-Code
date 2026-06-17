# Week 13 — Behavioral & Communication

```
┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐
│ S │  │ T │  │ A │  │ R │  │ . │  │ . │
└───┘  └───┘  └───┘  └───┘  └───┘  └───┘
```

> *Weeks 1–12 installed the UMPIRE method and twelve algorithmic pattern families — two pointers, hash maps, sliding window, binary search, BFS, DFS, heaps, tries, weighted graphs, DSU, and the dynamic-programming pipeline across 60+ problems. Week 13 installs the **other half of the onsite**: the behavioral round. It is graded, it is filtered on, and at most companies a strong-no-hire on behavioral sinks an otherwise-clean coding loop. This week installs a disciplined process for it — the same way UMPIRE is a disciplined process for coding. The eight categories of behavioral question; the STAR format that structures every answer; the **story bank** approach (twelve rehearsed anecdotes, each cross-referenced to the question types it covers, so you walk in with coverage instead of improvising); how to recover when you realize three sentences in that you picked the wrong story; and the follow-up email that closes the loop. By Sunday you can hear any behavioral prompt, map it to one of the eight categories in five seconds, pull the right story from a bank you can recite cold, deliver it in STAR in under two minutes, and recover gracefully if you mis-mapped.*

Welcome to Week 13 of **C2 · CrunchTime — The Code** — the penultimate week of the course and the first of two weeks that are **not about code**. Weeks 1–12 made you fluent at the whiteboard. They did nothing for the 45-minute conversation with a hiring manager that decides, just as firmly, whether you get the offer. This week closes that gap.

The behavioral round is the most under-prepared part of the loop, and it is under-prepared for a bad reason: candidates believe it cannot be studied. They believe it is a personality test, or a vibe check, or pure luck. It is none of those. The behavioral round is **a structured assessment with a rubric**, run by an interviewer who is scoring you against named competencies — ownership, conflict, ambiguity, failure, leadership, influence — and writing those scores into the same hiring packet as your coding scores. It can be prepared exactly the way the coding round can: with a method, a bank of material, and reps.

That is the thesis of the week. You already trust the analogy in your bones, because you have lived it for twelve weeks: a candidate who runs UMPIRE on every coding problem outperforms a candidate who tries to "see the answer." Identically, a candidate who maps every behavioral prompt to a category, pulls a rehearsed story, and delivers it in STAR outperforms a candidate who tries to "just be authentic" and improvises a rambling answer that buries the result. Authenticity is not the opposite of preparation. The most authentic-sounding answers in the room are the rehearsed ones — because rehearsal frees you from scrambling for what happened and lets you focus on telling it well.

The mechanics this week are four. **The eight categories** are your Match step: every behavioral prompt is one of eight question types, and naming the type in five seconds tells you which story to pull. **STAR** is your Implement step: Situation, Task, Action, Result — the structure that keeps you from rambling and guarantees you land the result, which is the part interviewers actually score. **The story bank** is your preparation artifact: twelve anecdotes from your real experience, each written once and cross-referenced to the categories it can answer, so that twelve stories cover roughly thirty distinct prompts. **Recovery and the follow-up email** are the senior polish: how to abandon a wrong story mid-answer without flailing, and how to write the post-interview email that reinforces fit without groveling.

By Sunday of Week 13 you will:

- **Recognize** which of the eight behavioral categories a prompt belongs to within five seconds of hearing it, and name the category aloud the way you name a coding pattern.
- **Structure** any answer in STAR — Situation, Task, Action, Result — with the Action carrying ~60% of the airtime and the Result always stated explicitly and, where possible, quantified.
- **Build** a personal story bank of twelve STAR anecdotes drawn from your real work, internships, projects, and coursework, each cross-referenced to the question categories it covers.
- **Map** the twelve stories to the eight categories in a coverage matrix and prove that every category has at least two stories that can answer it — so you are never caught without material.
- **Recover** from a wrong-story start: recognize within two sentences that the anecdote does not fit the prompt, name the pivot, and switch without apology or panic.
- **Write** a follow-up email within 24 hours of the interview that is specific, brief, and reinforces one concrete reason you are a fit — not a generic thank-you template.
- Have drafted **three STAR answers** as exercises — one conflict story, one failure story, one leadership/initiative story — each timed to under two minutes and revised against the rubric.
- Have shipped **two challenges** — a live recovery drill (rehearse abandoning a wrong story mid-answer) and a polished follow-up email written to a real (or realistic) interview.
- Have shipped the quiz, the homework, and the **mini-project**: a complete twelve-story bank in STAR format with a full cross-reference coverage matrix.

---

## Learning objectives

By the end of this week, you will be able to:

- **Classify a behavioral prompt into one of eight categories in five seconds.** The eight: (1) Conflict / disagreement; (2) Failure / mistake; (3) Leadership / initiative; (4) Teamwork / collaboration; (5) Ambiguity / undefined problems; (6) Handling pressure / deadlines / scope; (7) Influence / persuasion without authority; (8) Growth / feedback / "tell me about yourself." Naming the category is the Match step for behavioral.
- **Deliver any answer in STAR.** Situation (one or two sentences of context), Task (your specific responsibility — not the team's), Action (the bulk of the answer, in first-person "I," with concrete decisions), Result (the outcome, quantified where possible, plus what you learned). The most common failure is an Action that drifts into "we" and a Result that never lands.
- **Distinguish Task from Action and "I" from "we."** Interviewers score *your* contribution. The Task is what you were on the hook for; the Action is what you personally did. An answer that says "we shipped it" earns nothing; "I proposed the rollback plan and paired with the on-call to execute it" earns the point.
- **Build a story bank of twelve anecdotes** from real experience. Each story is written once in STAR, given a short handle (e.g. "the migration rollback," "the teammate who went dark"), and tagged with every category it can answer. Twelve well-chosen stories cover roughly thirty distinct prompts.
- **Cross-reference stories to categories in a coverage matrix.** A grid with eight category columns and twelve story rows; a cell is checked if the story can answer that category. The acceptance bar: every category has ≥ 2 stories, and no story is a one-trick (every story answers ≥ 2 categories). Gaps in the matrix are gaps in your preparation; fill them before the interview, not during it.
- **Recover from a mis-mapped story.** When you realize two sentences in that the anecdote does not actually answer the prompt, you have three moves: (a) pivot the framing of the same story to the actual question, (b) name the switch out loud ("actually, a cleaner example of that is...") and start a different story, or (c) finish the current story briefly and explicitly connect it back to the asked competency. Panicking, apologizing repeatedly, or trailing off are the failure modes.
- **Quantify a Result even when the work was not numeric.** "Reduced the on-call pages from roughly twelve a week to two" is strong; "made things better" is not. Where no metric exists, substitute a concrete observable outcome ("the feature shipped on the original date and the design doc became the team's template").
- **Write a follow-up email that moves the needle.** Within 24 hours; three to five sentences; references one specific moment from the conversation; reinforces one concrete reason you fit the role; no groveling, no restating your whole résumé, no pressure about timeline.

---

## Prerequisites

- **Weeks 1–12 complete.** You have a portfolio of UMPIRE write-ups and 60+ problems. The behavioral round and the coding round are scored in the same packet; this week makes the non-coding half as disciplined as the coding half.
- **A real work history to draw on.** Internships, jobs, significant course projects, open-source contributions, hackathons, club leadership, research — all count. You do **not** need years of industry experience; a well-told story from a six-week internship or a capstone project beats a vague story from a longer role. If your history feels thin, Lecture 1 §6 covers how to mine projects and coursework for legitimate STAR material.
- **Willingness to vocalize.** Same rule as Week 1: behavioral answers are *spoken*, and a story that reads fine on the page falls apart when you say it aloud at full volume and discover it runs four minutes. Find the closet, the parked car, the empty room. Record yourself. This is non-negotiable for the same reason it was in Week 1.
- **Honesty about your real experiences.** The story bank is built from things that actually happened to you. Fabricated stories collapse under follow-up questions ("what did the teammate say back?", "what would you do differently?"), which interviewers ask precisely to test authenticity. Every story this week is true. Embellishment is a strategy that loses.

---

## Topics covered

- **The eight categories** — the complete taxonomy of behavioral questions and the signal phrases that identify each
- **STAR format** — Situation, Task, Action, Result; the airtime budget; the "I vs. we" discipline; landing the Result
- **The Task / Action split** — the most-missed STAR distinction; why interviewers score your contribution, not the team's
- **The story bank** — twelve rehearsed anecdotes; the handle system; writing each story once and reusing it across categories
- **The coverage matrix** — cross-referencing stories to categories; the ≥ 2-stories-per-category bar; finding and filling gaps
- **Mining thin experience** — how to source legitimate STAR material from internships, projects, coursework, and side work
- **Quantifying the Result** — turning "it went well" into a concrete, defensible outcome; metric substitutes when no metric exists
- **Recovery mid-answer** — the three pivot moves when you realize you picked the wrong story; the failure modes to avoid
- **"Tell me about yourself"** — the 90-second opener that frames the whole loop; the narrative arc, not the résumé recital
- **Reading the interviewer** — follow-up questions as signals; when they are probing depth vs. when they have what they need
- **The follow-up email** — timing, length, specificity; what to include and what to leave out
- **The two-way street** — the questions *you* ask, and how they are scored as part of the behavioral signal

---

## Weekly schedule (intensive · 36h)

| Day | Focus | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project | Self-Study | Daily Total |
|-----|-------|---------:|----------:|-----------:|----------:|---------:|-------------:|-----------:|------------:|
| Monday | The eight categories; STAR format; exercise 1 (conflict) | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Tuesday | Task/Action split; quantifying results; exercise 2 (failure) | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Wednesday | The story bank + coverage matrix; exercise 3 (leadership) | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Thursday | Mini-project drafting (stories 1–6); recovery ramp | 0h | 1h | 1h | 0.5h | 1h | 1.5h | 1h | 6h |
| Friday | Challenges (recovery drill + follow-up email) | 0h | 0h | 2h | 0.5h | 1h | 1.5h | 1h | 6h |
| Saturday | Mini-project — stories 7–12 + coverage matrix | 0h | 0h | 0h | 0.5h | 1h | 3h | 0h | 4.5h |
| Sunday | Quiz + retro + push | 0h | 0h | 0h | 0.5h | 0h | 4h | 0h | 4.5h |
| **Total** | | **6h** | **7h** | **3h** | **3h** | **6h** | **10h** | **3.5h** | **38.5h** |

(The week budgets ~36 hours; the table sums slightly higher to absorb a generous self-study allowance. Drop 0.5h from Self-Study if 36h is your hard cap.)

**Mastery (10h/wk):** spread the same content over three calendar weeks. The story-bank mini-project lands in calendar Week 39 of the mastery pathway. See the [mastery study plan](../study-plans/mastery-1-year.md).

---

## How to navigate this week

| File | What's inside |
|------|---------------|
| [README.md](./00-overview.md) | This overview |
| [resources.md](./01-resources.md) | Free readings + behavioral references + the eight-category and STAR cheatsheets + glossary additions |
| [lecture-notes/01-the-eight-categories-and-star.md](./02-lecture-notes/01-the-eight-categories-and-star.md) | The eight categories, the signal phrases, STAR end to end, the Task/Action split, the "I vs. we" discipline, mining thin experience |
| [lecture-notes/02-the-story-bank-and-coverage-matrix.md](./02-lecture-notes/02-the-story-bank-and-coverage-matrix.md) | The twelve-story bank, the handle system, the coverage matrix, quantifying the Result, gap-filling |
| [lecture-notes/03-recovery-the-opener-and-the-follow-up.md](./02-lecture-notes/03-recovery-the-opener-and-the-follow-up.md) | Recovering from a wrong story, "tell me about yourself," reading the interviewer, the questions you ask, the follow-up email |
| [exercises/README.md](./03-exercises/00-overview.md) | Index of the three STAR drafting drills and SOLUTIONS |
| [exercises/exercise-01-conflict-star.md](./03-exercises/exercise-01-conflict-star.md) | Draft a conflict/disagreement STAR answer under two minutes |
| [exercises/exercise-02-failure-star.md](./03-exercises/exercise-02-failure-star.md) | Draft a failure/mistake STAR answer that lands the lesson |
| [exercises/exercise-03-leadership-star.md](./03-exercises/exercise-03-leadership-star.md) | Draft a leadership/initiative STAR answer with a quantified result |
| [exercises/SOLUTIONS.md](./03-exercises/SOLUTIONS.md) | Exemplar answers + per-exercise rubric; consult after attempting each drill |
| [challenges/README.md](./04-challenges/00-overview.md) | Index of weekly challenges |
| [challenges/challenge-01-recovery-drill.md](./04-challenges/challenge-01-recovery-drill.md) | Rehearse abandoning a wrong story mid-answer and pivoting cleanly |
| [challenges/challenge-02-follow-up-email.md](./04-challenges/challenge-02-follow-up-email.md) | Write a specific, concise follow-up email to a real or realistic interview |
| [quiz.md](./05-quiz.md) | 10 category-recognition questions |
| [homework.md](./06-homework.md) | Six practice prompts (~5 hrs) — one per under-drilled category, plus the opener |
| [mini-project/README.md](./07-mini-project/00-overview.md) | **A twelve-story bank in STAR + the full coverage matrix** — the week's deliverable |

---

## Stretch goals

- **Run a mock behavioral round with a peer.** Trade five prompts each, blind. Score each other against the STAR rubric in [exercises/SOLUTIONS.md](./03-exercises/SOLUTIONS.md). Hearing your own stories fail in real time is the fastest feedback in the course.
- **Record every story in your bank as audio.** A story that reads tight on the page often runs long when spoken. The only way to know your two-minute story is actually two minutes is to time the spoken version. Re-record any story that exceeds 2:15.
- **Build a second coverage matrix for one specific company.** Many companies publish or are known for specific competencies (some lead with leadership principles; some weight conflict and ambiguity heavily). Map your twelve stories to that company's named competencies and find the gaps before the loop.
- **Draft the "questions I ask the interviewer" list** — five role-specific questions that show you researched the team. These are scored as part of the behavioral signal (Lecture 3 §4). A candidate with no questions reads as disengaged.
- **Write a "failure" story you are genuinely uncomfortable telling**, then rehearse it until the discomfort is gone. The strongest failure stories involve real stakes and a real lesson; the rehearsal converts the discomfort into composure, which is exactly what the question is testing.

---

## What "done" looks like for Week 13

A learner who has shipped Week 13 has, in their portfolio repo:

- Three STAR exercise drafts (conflict, failure, leadership), each timed under two minutes, under `behavioral/c2-week-13/exercises/`.
- Two challenge deliverables — a recovery-drill transcript/reflection and a polished follow-up email — under `behavioral/c2-week-13/challenges/`.
- The quiz answered (score recorded).
- The homework prompts drafted.
- **The mini-project: a twelve-story bank in STAR format plus the cross-reference coverage matrix**, under `behavioral/c2-week-13/story-bank/`, with every category covered by ≥ 2 stories.
- A push log showing daily commits Mon–Sun.

If all of that is present and pushed, Phase 3's behavioral preparation is closed. You are ready for Week 14 — the full mock-loop and offer-negotiation capstone.

---

## A note on the Phase 3 finish

Week 13 is the *behavioral week* — the round most candidates ignore until the night before, and the round that quietly ends more loops than a missed edge case ever does. The single highest-leverage outcome this week is the **story bank**: twelve rehearsed anecdotes you can recite cold. Everything else — STAR structure, recovery, the follow-up email — is technique layered on top of that material. Without the bank, you are improvising under pressure; with it, you are selecting and delivering, which is a far easier task. Build the bank first; polish second.

If you find yourself ahead by Friday, the right stretch is **not** another story. It is running a live mock with a peer and being scored against the rubric, because the gap between a story that reads well and a story that *delivers* well only shows up out loud, under the small pressure of another person watching. Nothing in the written drills matches the moment you hear yourself bury a great result under thirty seconds of unnecessary setup.

If you find yourself *behind* by Wednesday, cut the bank from twelve stories to eight — but make those eight cover all eight categories. A complete eight-story bank beats an incomplete twelve-story bank every time, because coverage is the property that keeps you from being caught flat-footed. You can add the remaining four stories after the week closes; you cannot add coverage during the interview.

---

## Up next

[Week 14 — The Mock Loop & Offer Negotiation](../week-14-mock-loop-and-negotiation/) — once your twelve-story bank is built, your coverage matrix shows every category green, you can recover from a wrong story without flinching, and your follow-up email is drafted and ready to adapt.

---

*If you find errors in this material, please open an issue or send a PR. Future learners will thank you.*
