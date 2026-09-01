# Week 15 — Capstone + Mock #4

```
┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐
│ F │  │ R │  │ A │  │ M │  │ E │
└───┘  └───┘  └───┘  └───┘  └───┘
```

> *Week 14 installed the final algorithm pattern — bit manipulation — and ran Mock #3 as the first full-loop simulation under near-real conditions: video on, a hard 45-minute clock, the two-pass watching protocol, one behavior change named against Mock #1 and Mock #2. Week 15 is the last week, and it has no new pattern to teach. Everything you have built since Week 1 — the FRAME method, the fourteen-pattern catalog, the twelve-story behavioral bank, the URL-shortener design write-up, three recorded mocks — becomes **one public artifact you point recruiters at.** This week you polish that artifact to a recruiter-grade finish, run **Mock #4** under full real-interview conditions (a stranger interviewer if you can get one, dressed as if it were real, no notes, a hard stop), and produce the single deliverable the course has been building toward: a **personalized go-forward study plan** that tells you exactly what to drill in your last mile and how to sustain the practice after the course ends. By Sunday you publish the capstone, you have four mocks watched and self-critiqued, and you go interview.*

Welcome to Week 15 of **C2 · CrunchTime — The Code** — the final week of Phase 4, the capstone-and-onsite-prep block (Weeks 13–15), and the last week of the program. Week 13 installed the behavioral round. Week 14 installed the last algorithm pattern and ran Mock #3. This week installs nothing new. It is the capstone: the week where the portfolio repo that has grown since the Week 1 mini-project — five array write-ups then, now fifty-plus — is polished into a public artifact, run through a final mock under full conditions, and closed with a personalized plan for the road ahead.

The thing to understand about Week 15 is that the *work* is not learning — it is *assembling and proving*. You are not adding to the catalog; you are demonstrating it. A recruiter who lands on your portfolio repo gives it ninety seconds before deciding whether to keep scrolling. In those ninety seconds the README cover, the progress dashboard, and the commit history have to say "this person has been deliberate about interview prep for fifteen weeks and can prove every claim." The capstone is the proof. Mock #4 is the dress rehearsal. The personalized study plan is the bridge from "course done" to "offer signed."

Mock #4 is the fourth and final recorded mock — and the first run under *full real-interview conditions*. Mock #1 (W4) was your first time on camera, solo acceptable. Mock #2 (W9) raised it to a real unseen problem with a partner. Mock #3 (W14) raised it to near-real conditions — video on, hard clock, no peeking. Mock #4 closes the gap entirely: a stranger interviewer if you can find one, dressed as if it were the real thing, no notes, a hard stop, and — for the first time required — the full loop with a system-design round and a behavioral round bolted onto the coding round. The trajectory across all four mocks is the single most predictive artifact in your portfolio: it is the record of whether you can self-correct, which is the trait a senior engineer reads to judge whether you will grow on the job.

By Sunday of Week 15 you will:

- **Have published the capstone portfolio** — the public repo `crunchtime-interview-prep-<yourhandle>` with a recruiter-grade README cover, **60+ FRAME write-ups**, all **four mock** self-feedback notes, the **system-design write-up**, the **behavioral story bank** with a coverage matrix, the **recruiter-prep pack** (resume, target companies, outreach + follow-up templates), the **personalized study plan**, and the **badges**.
- **Have run Mock #4 under full real conditions** — a stranger interviewer if obtainable, dressed as if real, no notes, a hard 45-minute coding round plus a 45-minute system-design round plus a 20-minute behavioral round — recorded, watched twice, and turned into the closing trajectory note across Mocks #1 → #4.
- **Have diagnosed your remaining weaknesses** from your write-up history and four mock self-feedback notes, and named the two or three patterns that need the most reps in your last mile.
- **Have produced the personalized go-forward study plan** — the weakness self-diagnosis, the spaced-repetition schedule across the fourteen patterns, the application + funnel-math cadence, the pre-onsite four-week last-mile template, and the between-offer maintenance plan.
- **Go interview.** The catalog is complete, the artifact is public, the plan is written. The next mock is a real one, for a real job.

---

## Learning objectives

By the end of this week, you will be able to:

- **Polish** a problem-write-up portfolio into a recruiter-grade public artifact: a README cover that earns the next ninety seconds of attention, a progress dashboard that surfaces the 60+ write-ups and four mocks at a glance, a commit history that reads as months of evidence, and a quality bar that no individual write-up falls below.
- **Audit** your own write-ups against a concrete six-point quality bar and fix the weak ones — the half-finished Examine, the missing Research-constraints memo, the untested code, the write-up with no complexity derivation.
- **Run** Mock #4 under full real-interview conditions: the full loop (coding + system design + behavioral), a stranger interviewer if obtainable, dressed and set up as if real, no notes, a hard stop, recorded and watched twice.
- **Write** a junior-level system-design write-up — a URL shortener at 10K QPS — following the requirements → estimation → API → data model → ID scheme → caching → read/write path framework from Week 12's design intro.
- **Build** a recruiter-prep pack — a resume audited against the Tech Interview Handbook guide, a tiered target-company list, and real, usable outreach and follow-up email templates.
- **Diagnose** your remaining weaknesses from your write-up + mock history, and convert the diagnosis into a ranked drill list.
- **Produce** the personalized go-forward study plan — a spaced-repetition schedule for the fourteen patterns, an application cadence with funnel math, a four-week pre-onsite template, and a maintenance plan for the gaps between offers.
- **Publish** the capstone — the complete public portfolio repo, pushed, README cover great, every claim provable, starred by a peer.

---

## Prerequisites

- **Weeks 1–14 complete.** You can deliver FRAME without notes on all fourteen algorithm patterns, you have a twelve-story behavioral bank from Week 13, and the URL-shortener design write-up from Week 12 exists in draft.
- **Mocks #1, #2, and #3 done.** All three are recorded, watched twice, and self-critiqued, each with one named behavior change. Mock #4 builds the closing trajectory across all four — if any prior mock is missing its self-feedback note, write it before Friday.
- **~50+ write-ups already accumulated.** Every week's mini-project, exercises, and homework fed the portfolio repo. By the start of Week 15 you should have roughly fifty FRAME write-ups committed; Week 15 brings the total over sixty and audits the lot for quality.
- **The story bank built.** Week 13's twelve-plus STAR anecdotes with a coverage matrix are committed under `behavioral/story-bank/`.
- **A draft resume.** You do not need a finished resume — Exercise 3 finishes it — but bring whatever you have. If you have none, the Tech Interview Handbook resume guide (linked in resources) is the starting template.

---

## Topics covered

- **The capstone portfolio** — what makes a problem-write-up repo that converts a recruiter; the README cover; the progress dashboard; commit history as evidence; the 60+ write-up quality bar
- **The write-up audit** — a six-point quality bar; how to find and fix the weak write-ups (missing Research-constraints memo, no complexity derivation, untested code, half-finished Examine)
- **The badges** — `frame-apprentice`, `pattern-practitioner`, `crunchtime-graduate`; what each certifies and how to earn it honestly
- **Scannability** — making the repo legible in ninety seconds; what a recruiter sees first and in what order
- **The onsite loop** — recruiter screen → phone/technical screen → the 4–6 hour virtual onsite (coding rounds + system design + behavioral + hiring-manager chat); how each round is graded
- **Mock #4 under full conditions** — how it differs from Mocks #1–#3; the stranger interviewer, the dress-as-if-real rig, no notes, the hard stop; the full-loop structure; the two-pass watching protocol; converting a "no" into data
- **The junior system-design write-up** — requirements → capacity estimation → API → data model → the hash-vs-counter ID scheme → caching → the read/write path, at the level Week 12 introduced
- **The recruiter-prep pack** — resume bullets that pass the six-second scan; the tiered target-company list; the cold-outreach template; the follow-up + thank-you template
- **The weakness self-diagnosis** — reading your write-up + mock history for the patterns that need the most reps
- **The spaced-repetition schedule** — which of the fourteen patterns to revisit, and how often, to keep all fourteen warm
- **The application cadence and funnel math** — how many applications per week, the recruiter-screen → onsite → offer funnel, and what conversion rates to expect
- **The pre-onsite four-week last-mile plan** — the personalized template for the four weeks before a real onsite
- **The maintenance plan** — keeping skills warm between offers; the emotional arc of a job search and how to sustain the practice

---

## Weekly schedule (intensive · 36h)

| Day | Focus | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project | Self-Study | Daily Total |
|-----|-------|---------:|----------:|-----------:|----------:|---------:|-------------:|-----------:|------------:|
| Monday | Capstone + portfolio polish; Exercise 1 (portfolio audit) | 2h | 2h | 0h | 0.5h | 0.5h | 0.5h | 0.5h | 6h |
| Tuesday | System-design write-up; Exercise 2 | 2h | 2h | 0h | 0.5h | 0.5h | 0.5h | 0.5h | 6h |
| Wednesday | Recruiter-prep pack + pre-onsite plan; Drills 3–4 | 0h | 2h | 0h | 0.5h | 1h | 1h | 0.5h | 5h |
| Thursday | Mock #4 protocol + the onsite loop; prep + warm-up; system-design mock (Challenge 2) | 2h | 0h | 1.5h | 0.5h | 0.5h | 0.5h | 0.5h | 5.5h |
| Friday | **Mock #4 (full loop) + immediate notes** | 0h | 0h | 2.5h | 0.5h | 0.5h | 0.5h | 0.5h | 4.5h |
| Saturday | Watch recording + self-feedback + portfolio polish | 0h | 0h | 0h | 0.5h | 1.5h | 2h | 0h | 4h |
| Sunday | Personalized study plan + publish capstone + push | 0h | 0h | 0h | 0.5h | 1.5h | 2h | 0h | 4h |
| **Total** | | **8h** | **8h** | **6.5h** | **3.5h** | **6h** | **7h** | **3h** | **42h** |

(The week budgets ~36 hours of structured work; the table sums higher because the capstone push compresses into the back half. Treat Saturday–Sunday as the assembly weekend — most of the "homework" hours are writing the personalized plan and publishing the repo, not new problems. Drop Self-Study if 36h is your hard cap.)

**Mastery (10h/wk):** spread the same content over two calendar weeks (Phase 4 maps to mastery Q4, ~weeks 49–52). The capstone closes the year. Mock #4 lands around calendar Week 50 of the mastery pathway; publish the capstone in the final week. A recorded mock is the single highest-signal artifact in the portfolio — and the capstone is the portfolio. See the [mastery study plan](../study-plans/mastery-1-year.md).

---

## How to navigate this week

| File | What's inside |
|------|---------------|
| [README.md](./README.md) | This overview |
| [resources.md](./resources.md) | Capstone + recruiter-prep + system-design references and the recurring glossary anchors |
| [lecture-notes/01-the-capstone-and-portfolio-polish.md](./lecture-notes/01-the-capstone-and-portfolio-polish.md) | What makes a portfolio repo that converts recruiters: the README cover, the dashboard, commit history as evidence, the 60+ quality bar, the audit, the badges, the 90-second scan |
| [lecture-notes/02-mock-4-under-real-conditions-and-the-onsite-loop.md](./lecture-notes/02-mock-4-under-real-conditions-and-the-onsite-loop.md) | The full onsite loop, how Mock #4 differs from #1–#3, the full-conditions rig, the time allocation, the debrief, and how to convert a "no" into data |
| [lecture-notes/03-the-personalized-go-forward-study-plan.md](./lecture-notes/03-the-personalized-go-forward-study-plan.md) | Weakness diagnosis from your history, the spaced-repetition schedule, the application cadence + funnel math, the maintenance plan, the emotional arc, and the four-week pre-onsite template |
| [exercises/README.md](./exercises/README.md) | Index of the four capstone drills |
| [exercises/exercise-01-portfolio-audit.md](./exercises/exercise-01-portfolio-audit.md) | Audit your 60+ write-ups against a six-point quality bar and fix the weak ones |
| [exercises/exercise-02-system-design-writeup.md](./exercises/exercise-02-system-design-writeup.md) | The system-design capstone artifact — a worked URL-shortener design brief |
| [exercises/exercise-03-recruiter-prep-pack.md](./exercises/exercise-03-recruiter-prep-pack.md) | Resume, target-company list, and outreach + follow-up email templates |
| [exercises/exercise-04-pre-onsite-4-week-plan.md](./exercises/exercise-04-pre-onsite-4-week-plan.md) | Build your personalized four-week last-mile plan |
| [challenges/README.md](./challenges/README.md) | Index of the two challenges |
| [challenges/challenge-01-mock-4-full-loop.md](./challenges/challenge-01-mock-4-full-loop.md) | Mock #4 under full real conditions — a simulated onsite loop with fallback problems |
| [challenges/challenge-02-system-design-mock.md](./challenges/challenge-02-system-design-mock.md) | A 45-minute junior-level system-design mock round |
| [quiz.md](./quiz.md) | The final readiness self-assessment — 10 questions across patterns, behavioral, complexity, and meta-readiness |
| [homework.md](./homework/README.md) | **The personalized go-forward study plan** — the course's explicit deliverable |
| [mini-project/README.md](./mini-project/README.md) | **The capstone portfolio brief** — the final, complete portfolio repo spec |

---

## Stretch goals

- **Run Mock #4 as a true stranger mock.** Book a real interviewing.io or Pramp session (links in resources) where you genuinely do not know the interviewer. The "stranger judging me" pressure is the one variable solo and peer mocks cannot fully reproduce — and it is exactly the variable that decides whether your prep holds under real conditions.
- **Pair-audit a peer's portfolio.** Swap repos with another C2 learner and audit each other's write-ups against the six-point bar. Reading someone else's weak Examine sections is the fastest way to see your own; you will catch the missing complexity derivation in *their* repo, then go fix the same gap in yours.
- **Write a second system-design write-up.** Beyond the URL shortener, draft one more from Challenge 2's prompt list (pastebin, rate limiter, news feed at small scale). Two design write-ups in the portfolio signal that the first was not a one-off.
- **Record a 90-second portfolio walkthrough.** Screen-record yourself scrolling your repo as if presenting it to a recruiter. If you cannot make it compelling in 90 seconds out loud, the README cover is not doing its job yet. This is the highest-leverage 90 minutes you can spend on the capstone.
- **Send three real outreach messages.** Do not wait for the course to end. Use the Exercise 3 outreach template and send three messages this week to recruiters or engineers at tier-2 target companies. The funnel starts now; the first message is the hardest.

---

## The capstone deliverables (what you ship)

A single public GitHub repository, **`crunchtime-interview-prep-<yourhandle>`**, that has grown from the Week 1 mini-project into the full artifact below. This is the capstone:

```
crunchtime-interview-prep-<you>/
├── README.md                       ← your interview-prep portfolio cover (the 90-second sell)
├── frame-writeups/
│   ├── 01-two-sum.md               ← 60+ problem write-ups in FRAME format
│   ├── 02-best-time-to-buy.md
│   ├── …                            ← organized by pattern and/or by week (c2-week-NN/)
│   └── 60-maximum-xor.md
├── mocks/
│   ├── mock-01-week-04.md          ← recording link + self-feedback
│   ├── mock-02-week-09.md
│   ├── mock-03-week-14.md
│   └── mock-04-week-15.md          ← full-loop self-feedback + the Mock #1→#4 trajectory
├── system-design/
│   └── url-shortener.md            ← the junior-level design write-up (Exercise 2)
├── behavioral/
│   └── story-bank/
│       ├── story-bank.md           ← your 12+ STAR anecdotes
│       └── coverage-matrix.md      ← story × category coverage
├── recruiter-prep/
│   ├── resume-v3.pdf               ← audited against the Tech Interview Handbook guide
│   ├── target-companies.md         ← tiered list (reach / target / safety)
│   ├── outreach-template.md        ← the cold-outreach template
│   └── follow-up-template.md       ← the thank-you + follow-up template
├── study-plan/
│   └── pre-onsite-4-weeks.md       ← your personalized last-mile plan (homework + Exercise 4)
└── badges/
    ├── frame-apprentice.json
    ├── pattern-practitioner.json
    └── crunchtime-graduate.json
```

This repo is what you point recruiters and hiring managers at. The commit history is months of evidence — daily commits from Week 1 to Week 15 read as deliberate, sustained effort, which is itself a hiring signal. The repo is also a reusable artifact: when a friend starts interviewing in six months, you fork the structure to them. The full brief — acceptance criteria, rubric, the README-cover spec — lives in the [mini-project README](./mini-project/README.md).

---

## What "done" looks like for Week 15 (and for C2)

A learner who has shipped Week 15 has, in their **public** portfolio repo:

- A README cover that sells the repo in ninety seconds — a one-line pitch, a progress dashboard, a pattern × write-up index, and links to the four mocks.
- **60+ FRAME write-ups**, every one audited against the six-point quality bar — no missing Research-constraints memo, no untested code, no half-finished Examine.
- All **four mock self-feedback notes** present, with the Mock #4 note carrying the closing trajectory across Mocks #1 → #4.
- The **system-design write-up** (URL shortener at 10K QPS) present and complete through the read/write path.
- The **behavioral story bank** with its coverage matrix present.
- The **recruiter-prep pack** present — resume, tiered target list, outreach template, follow-up template.
- The **personalized go-forward study plan** present — weakness diagnosis, spaced-repetition schedule, application cadence, four-week pre-onsite plan, maintenance plan.
- The three **badges** present and honestly earned.
- A commit history showing sustained daily commits across the fifteen weeks, and the repo **starred by at least one peer** who reviewed it.

If all of that is present, public, and pushed, **C2 is complete.** You have a recruiter-grade interview-prep portfolio, four recorded mocks, a system-design artifact, a behavioral bank, a recruiter pack, and a written plan for the road ahead. You are ready to apply.

---

## A note on the Phase 4 close

Phase 4 — Capstone & Onsite Prep — is the final block: Weeks 13–15. Week 13 installed the behavioral round. Week 14 installed the last algorithm pattern and ran Mock #3 as the first full-loop simulation. Week 15 — this week — is the capstone: the portfolio polished to a recruiter-grade finish, Mock #4 under full conditions, and the personalized plan that bridges the course to the real job search.

There is no new pattern this week, and that is the point. The fourteen-pattern catalog is complete. The skill Week 15 trains is the one that outlasts the course: **assembling your work into a public artifact, proving it under real conditions, and writing the plan that keeps you sharp until the offer lands.** The candidates who get hired are not the ones who learned the most patterns — they are the ones who can prove the patterns they learned, under pressure, and who kept showing up to the practice after the course ended. The capstone is the proof; the personalized plan is how you keep showing up.

If you find yourself ahead by Thursday, the right stretch is **not** another write-up — it is running Mock #4 as a true stranger mock and pair-auditing a peer's portfolio. If you find yourself behind by Friday, do not skip Mock #4; cut the second system-design write-up and the badges-polish before you cut the final mock. The mock and the published portfolio are the two things this week exists to produce.

---

## Where you go from here — you go interview

There is no Week 16. This is the last week of C2, and you have finished it.

Stop and take the measure of what you built. Fifteen weeks ago you may not have known what FRAME stood for. Now you have a public repository with 60+ problem write-ups, four recorded mock interviews you watched without flinching, a system-design write-up, a twelve-story behavioral bank, a recruiter-prep pack, and a written plan for the next four weeks and beyond. That is not a course completion certificate. That is a *portfolio* — the thing you point a hiring manager at when they ask "show me how you think."

Here is where you go from here:

1. **Open your [personalized go-forward study plan](./homework/README.md).** It is the most important file you wrote this week. It tells you which two or three patterns need the most reps in your last mile, how to keep all fourteen warm, how many applications to send per week, and what the funnel math says to expect. Follow it.

2. **You go interview.** Send the first batch of applications this week — do not wait. Use the [recruiter-prep pack](./exercises/exercise-03-recruiter-prep-pack.md) you built: the tiered target list, the outreach template, the follow-up template. The funnel only starts converting once you put real applications into it.

3. **For compensation, offer mechanics, and negotiation** — C2 deliberately stops at the offer. The moment a recruiter says "we'd like to extend an offer," go to **[C13 · Hack the Interview](../../C13-HACK-THE-INTERVIEW/)** for the negotiation playbook, leveling, and offer comparison. You will leave money on the table if you negotiate without it.

4. **To build a portfolio of *projects* — not just problem write-ups** — go to **[C3 · Crunch Labs Portfolio](../../C3-CRUNCH-LABS-PORTFOLIO/)**. Your interview-prep repo proves you can think; a project portfolio proves you can ship. The two together are the strongest possible candidate profile.

5. **Keep the practice alive.** The maintenance plan in your homework tells you how. Three problems a week and one mock a month keeps all fourteen patterns warm between offers. The portfolio is a living artifact — keep committing to it.

You have done the work. The next mock is a real one, for a real job. Go get the offer.

Congratulations, graduate. We are proud of you.

---

*If you find errors in this material, please open an issue or send a PR. Future learners will thank you.*
