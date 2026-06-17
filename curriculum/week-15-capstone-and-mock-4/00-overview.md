# Week 15 — Capstone + Mock #4

```
┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐
│ U │  │ M │  │ P │  │ I │  │ R │  │ E │
└───┘  └───┘  └───┘  └───┘  └───┘  └───┘
```

> *Fourteen weeks ago you could not name a pattern under pressure. Now you run UMPIRE as a reflex on every prompt — Match in 30 seconds, the recurrence or the template from memory, the trace by hand, the complexity defended out loud. Week 15 is not a new pattern. It is the **closing week of the whole course**: the final mock under full real-interview conditions; the public portfolio anyone can scroll to see UMPIRE applied to 60+ problems; and the recruiter-prep pack that turns a finished portfolio into actual onsite invitations — a resume that survives a 6-second skim, a LinkedIn that a recruiter searches and finds, a target-company list with named teams, and an outreach template that gets replies. By Sunday you have a recorded Mock #4, a portfolio you would send to a hiring manager unedited, and a recruiter-prep pack you can start sending Monday morning. This is the week the work becomes a job search.*

Welcome to Week 15 of **C2 · CrunchTime — The Code** — the final week of the course and the third of the Phase-3 closing arc (Week 13 installed system-design fundamentals; Week 14 ran Mock #3 and the behavioral-story bank; Week 15 lands the capstone). Every week until now installed a pattern and asked you to ship two or three UMPIRE write-ups. This week installs **no new pattern**. It is pure synthesis: take the 60+ write-ups you have accumulated, make them *public and navigable*, run the hardest mock of the course, and assemble the materials that get you in front of a human who can hire you.

The misconception this week corrects: students think the portfolio is "done" because the write-ups exist in a repo. A pile of markdown files in a private repo is not a portfolio — it is raw material. A **portfolio** is curated, indexed, navigable, and public: a recruiter or hiring manager lands on the README, understands in 20 seconds what they are looking at, and can click straight to your best Edit Distance write-up or your cleanest BFS trace. The gap between "60 files exist" and "a hiring manager spent four minutes and decided to forward you to the team" is the work of this week.

By Sunday of Week 15 you will:

- **Run Mock #4** under full real-interview conditions — a peer or platform partner (no solo flavor this time), an uncurated prompt, a hard 45-minute clock, screen-and-face-and-audio recording, and a 90-second "tell me about yourself" open plus a behavioral question close. This is the course's exit mock; it is the closest thing to a real onsite loop you will run before the real thing.
- **Publish the public portfolio** — a single repository, public, with a curated README that indexes UMPIRE applied to 60+ problems across all 14 prior weeks, grouped by pattern, each entry linking to a clean write-up. Anyone with the URL can scroll the whole arc of your preparation.
- **Polish the resume** to a single page that survives the 6-second recruiter skim: a projects section that links the portfolio, a skills line that matches the job descriptions you are targeting, and bullet points in the *action-verb + scope + measurable-impact* shape.
- **Rebuild the LinkedIn profile** so that a recruiter searching "software engineer Python data structures" in your metro finds you: a headline that is not "aspiring developer," an About section in the first person, the portfolio linked in Featured, and the skills section ordered to match your target roles.
- **Build the target-company list** — 25–40 companies, tiered (reach / match / safety), each with a named team or product where possible, the role link, and a "why this one" sentence. The list is the spine of the entire job search; an untargeted blast is the most common reason a strong candidate gets no replies.
- **Write the outreach template** — a short, specific, no-ask-yet message to a recruiter or engineer that references something real about their team and links the portfolio. Plus two variants (cold recruiter; warm referral) and a follow-up.
- Have shipped the quiz (a recruiter-readiness and interview-loop self-audit), the homework (the 50-application sprint plan plus the behavioral-story polish), and the **capstone**: the public portfolio, the recorded Mock #4, and the complete recruiter-prep pack, all cross-linked.

---

## Learning objectives

By the end of this week, you will be able to:

- **Run a full-fidelity mock interview end to end** — open with a 90-second self-introduction, take an uncurated prompt, run all six UMPIRE steps under a hard clock, recover audibly from a wrong first approach, close with a behavioral question, and write a self-feedback note that names one specific behavior change. By Mock #4 the behavior changes from Mocks #1–#3 should be *closed*; this mock measures whether they stuck.
- **Curate a public portfolio** that a hiring manager can navigate in four minutes: a README that states who you are and what the repo is, an index grouped by the 14 patterns, a "start here" set of three or four flagship write-ups, and a consistent file structure so every write-up has the same six UMPIRE sections in the same order.
- **Audit a write-up for public readiness.** A private drill note and a public portfolio entry are different artifacts. The public version has no "I was stuck for 10 minutes" asides, no broken links, a working code block that actually runs, and a one-line summary at the top so a skimmer gets the gist without reading the whole thing.
- **Write a resume bullet in the canonical shape** — *action verb + what you built + measurable scope or impact* — and reject the weak shapes ("responsible for," "helped with," "worked on"). Quantify everything that can be quantified.
- **Optimize a LinkedIn profile for recruiter search.** Recruiters search by keyword and location; the profile is a search-optimization problem. The headline, the About section, the skills list, and the Featured section are the four levers.
- **Tier a target-company list** into reach / match / safety and defend the tiering. A list that is all reach companies produces no interviews; a list that is all safety companies undersells you. The 20/60/20 split is the default.
- **Write a cold outreach message** that gets a reply: short, specific to the recipient, references something real, links the portfolio, and makes no ask in the first message beyond "would you be open to a 15-minute chat."
- **Articulate your own story** — the 90-second "tell me about yourself," the "why are you leaving / why now," and the three-to-five behavioral stories in STAR shape — without notes and without rambling.

---

## Prerequisites

- **Weeks 1–14 complete.** You have shipped UMPIRE write-ups for all 14 patterns, run Mocks #1 (W4), #2 (W9), and #3 (W14), and built the behavioral-story bank (W14). The 60+ write-ups this week curates must already exist; Week 15 does not generate new problem solutions, it organizes the ones you have.
- **A portfolio repo with the write-ups in it.** From Week 1 you have committed write-ups to `umpire-writeups/c2-week-NN/`. If yours is incomplete, the first homework task is a back-fill audit — you cannot curate a portfolio that is missing a third of its entries.
- **A mock partner.** Mock #4 has no solo flavor. By now you should have a recurring mock partner from the cohort or from Pramp / interviewing.io. If you do not, the Monday task is to find one — the [community channel](../../community/) exists for exactly this.
- **A draft resume and a LinkedIn profile that exist.** This week *polishes* them, it does not create them from nothing. If you do not have a resume at all, build a one-page draft Monday morning before the polish pass; the [resources](./01-resources.md) link a free template.
- **Comfortable being recorded and watched.** Three prior mocks have desensitized you to the camera. Mock #4 adds a behavioral open and close, which raises the pressure again; the recording discipline from Lecture 2 of Week 4 still applies.

---

## Topics covered

- **The exit mock (Mock #4)** — full-fidelity protocol, the behavioral open and close, the self-feedback note that measures whether the prior behavior changes stuck
- **The portfolio as a product** — the difference between a pile of files and a navigable, public, curated portfolio a hiring manager reads in four minutes
- **The portfolio README** — the "who I am / what this is / start here / index by pattern" structure
- **Write-up public-readiness audit** — turning a private drill note into a public portfolio entry; the one-line summary, the working code block, the no-asides discipline
- **The resume** — the one-page constraint, the bullet shape (action verb + scope + impact), the projects section that links the portfolio, the skills line matched to job descriptions
- **LinkedIn for recruiter search** — the headline, the first-person About, the Featured link, the skills ordering; the profile as a keyword-and-location search problem
- **The target-company list** — tiering into reach / match / safety; named teams and products; the "why this one" sentence; the 20/60/20 split
- **The outreach template** — the cold-recruiter message, the warm-referral message, the follow-up; short, specific, no-ask-yet
- **The story** — the 90-second self-introduction, the "why now," the three-to-five STAR behavioral stories
- **The application sprint** — the 50-application plan, the weekly cadence, the tracking spreadsheet, the funnel math

---

## Weekly schedule (intensive · 36h)

| Day | Focus | Lectures | Exercises | Challenges | Quiz/Read | Homework | Capstone | Self-Study | Daily Total |
|-----|-------|---------:|----------:|-----------:|----------:|---------:|---------:|-----------:|------------:|
| Monday | Capstone kickoff; portfolio audit; back-fill missing write-ups | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Tuesday | Portfolio curation; README + index by pattern; exercise 1 | 1h | 2h | 0h | 0.5h | 1h | 1h | 0.5h | 6h |
| Wednesday | Resume + LinkedIn polish; exercise 2; recruiter-prep ramp | 2h | 1.5h | 0h | 0.5h | 0.5h | 1h | 0.5h | 6h |
| Thursday | Target list + outreach (challenge 1); Mock #4 setup | 1h | 0h | 2h | 0.5h | 1h | 1h | 0.5h | 6h |
| Friday | **Mock #4** (recorded) + immediate notes | 0h | 0h | 2h | 0.5h | 0.5h | 2h | 0.5h | 5.5h |
| Saturday | Watch Mock #4; self-feedback; portfolio final polish | 0h | 0h | 0h | 0.5h | 0.5h | 4h | 0h | 5h |
| Sunday | Capstone ship + course retro + push; first outreach sent | 0h | 0h | 0h | 0.5h | 0h | 4h | 0h | 4.5h |
| **Total** | | **8h** | **7.5h** | **6h** | **3.5h** | **5h** | **18h** | **3h** | **39h** |

(The week budgets ~36 hours; the table sums slightly higher to absorb the course-closing load. Drop the Self-Study rows if 36h is your hard cap. "Capstone" replaces the usual "Mini-Project" column this week — it is the same slot, scaled up.)

**Mastery (10h/wk):** spread the same content over three calendar weeks. The capstone lands in calendar Week 45 of the mastery pathway, the final calendar week. See the [mastery study plan](../study-plans/mastery-1-year.md).

---

## How to navigate this week

| File | What's inside |
|------|---------------|
| [README.md](./00-overview.md) | This overview |
| [resources.md](./01-resources.md) | Free portfolio / resume / LinkedIn / outreach references + the recruiter-prep cheatsheet + glossary additions |
| [lecture-notes/01-the-public-portfolio.md](./02-lecture-notes/01-the-public-portfolio.md) | The portfolio as a product; the README structure; the index-by-pattern; the write-up public-readiness audit |
| [lecture-notes/02-mock-4-the-exit-interview.md](./02-lecture-notes/02-mock-4-the-exit-interview.md) | The full-fidelity Mock #4 protocol; the behavioral open and close; the self-feedback note that measures whether prior changes stuck |
| [lecture-notes/03-the-recruiter-prep-pack.md](./02-lecture-notes/03-the-recruiter-prep-pack.md) | Resume, LinkedIn, the target-company list, the outreach template; the application sprint and the funnel math |
| [exercises/README.md](./03-exercises/00-overview.md) | Index of the three portfolio-build exercises and SOLUTIONS |
| [exercises/exercise-01-portfolio-readme.md](./03-exercises/exercise-01-portfolio-readme.md) | Build the public portfolio README — the curated index of 60+ UMPIRE write-ups |
| [exercises/exercise-02-resume-rewrite.md](./03-exercises/exercise-02-resume-rewrite.md) | Rewrite five resume bullets into the action-verb + scope + impact shape |
| [exercises/exercise-03-linkedin-audit.md](./03-exercises/exercise-03-linkedin-audit.md) | Audit and rewrite the four LinkedIn levers for recruiter search |
| [exercises/SOLUTIONS.md](./03-exercises/SOLUTIONS.md) | Worked before/after examples for all three exercises; consult after attempting each |
| [challenges/README.md](./04-challenges/00-overview.md) | Index of weekly challenges |
| [challenges/challenge-01-target-list-and-outreach.md](./04-challenges/challenge-01-target-list-and-outreach.md) | Build the 25–40-company tiered target list + the outreach template trio |
| [challenges/challenge-02-mock-4-and-self-feedback.md](./04-challenges/challenge-02-mock-4-and-self-feedback.md) | Run the recorded Mock #4 and ship the self-feedback note |
| [quiz.md](./05-quiz.md) | 10 recruiter-readiness and interview-loop self-audit questions |
| [homework.md](./06-homework.md) | The 50-application sprint plan + behavioral-story polish (~5 hrs) |
| [mini-project/README.md](./07-mini-project/00-overview.md) | **The capstone spec** — public portfolio + recorded Mock #4 + recruiter-prep pack; points to [projects/capstone](../../projects/) as the master guide |

---

## Stretch goals

- **Record a 60-second portfolio walkthrough** (Loom or screen-recording) and pin it to the top of the portfolio README. A hiring manager who clicks "play" before they read is a hiring manager who is already engaged. The recognition cue: a portfolio with a video intro converts skims to reads at a noticeably higher rate.
- **Do a mock recruiter screen** with a peer playing the recruiter. The 30-minute recruiter phone screen (not the technical loop) is where most candidates fumble the "tell me about yourself" and the "what are you looking for" — drill it once before the real one.
- **Write one "deep-dive" portfolio piece** on your single best problem — 800 words, the full UMPIRE plus two alternative approaches and a benchmark. One genuinely deep piece signals more than 60 shallow ones; it is the artifact a senior engineer remembers.
- **Set up a simple application-tracking spreadsheet** with the funnel columns (applied / responded / phone screen / onsite / offer) and start logging Monday. The funnel math (you need ~10 applications per phone screen, ~4 phone screens per onsite, ~3 onsites per offer, very roughly) only becomes legible once you track it.
- **Read three "lessons from N mock interviews" posts** from interviewing.io's blog and extract one behavior change you have not yet made. Phase-3 alumni who did this reported catching a tell that three mocks had not surfaced.

---

## What "done" looks like for Week 15

A learner who has shipped Week 15 has:

- A **public portfolio repository** with a curated README indexing UMPIRE applied to 60+ problems, grouped by pattern, each entry a clean public write-up. Anyone with the URL can scroll the whole arc.
- A **recorded Mock #4** (peer or platform, not solo), with immediate notes, pass-1 timestamps, and a self-feedback note that explicitly checks whether the behavior changes from Mocks #1–#3 stuck.
- A **complete recruiter-prep pack**: a one-page polished resume that links the portfolio; a rebuilt LinkedIn profile; a tiered target-company list of 25–40 companies; and the outreach template trio (cold recruiter, warm referral, follow-up).
- The **quiz** answered (recruiter-readiness score recorded) and the **homework** committed (the 50-application sprint plan + the polished behavioral stories).
- A **course retrospective** — the arc from "could not name a pattern" to "ships UMPIRE on any prompt in 30 seconds" — committed at the top of the portfolio.
- A push log showing daily commits Mon–Sun, and the **first outreach message actually sent** by Sunday night.

If all of that is present and pushed, the course is complete. You are not "studying for interviews" anymore — you are running a job search with a portfolio behind you.

---

## A note on the course close

Week 15 is the *synthesis week* — there is no pattern to install, only the work of turning fourteen weeks of accumulated reps into something a hiring manager can see and act on. The highest-leverage outcome is the **public portfolio**: it is the single artifact that distinguishes a candidate who "studied data structures" from one who can prove, publicly and at a glance, that they run a disciplined problem-solving process on any prompt. The second-highest is **Mock #4** — the measurement that the habits stuck under pressure. The recruiter-prep pack is the conversion layer: it is what turns the portfolio into interviews.

If you find yourself ahead by Friday, the right stretch is **not** another write-up — it is the deep-dive portfolio piece (stretch goal 3) and the mock recruiter screen (stretch goal 2). Both raise your conversion from "applied" to "phone screen," which is the bottleneck almost every candidate hits.

If you find yourself *behind* by Wednesday, cut the LinkedIn polish to the headline-and-Featured-link only (the two highest-leverage levers), defer the resume to a single bullet-shape pass on your top three bullets, and protect the two non-negotiables: the **public portfolio README** and the **recorded Mock #4**. Those two are the capstone; everything else is recoverable next week.

---

## Up next

There is no Week 16. This is the end of **C2 · CrunchTime — The Code**.

What comes next is not another week of curriculum — it is the job search itself, with the portfolio behind you and the recruiter-prep pack in hand. Send the first outreach Sunday night. Keep running mocks with your cohort partner weekly. Re-do one old write-up a week to keep the patterns warm. When the onsite invitations come — and with a public portfolio and four mocks behind you, they will — you will walk in having already run the loop four times under pressure. That is the whole point of the fifteen weeks.

Go get the offer. Then come back and mentor the next cohort.

---

*If you find errors in this material, please open an issue or send a PR. Future learners will thank you.*
