# Mini-Project — The Capstone Portfolio

> Topic: closing the repo you have been building since Week 1 · Lecture: [1](../lecture-notes/01-the-capstone-and-portfolio-polish.md), [3](../lecture-notes/03-the-personalized-go-forward-study-plan.md) · Difficulty: assembly and polish, not creation · Target time: about 7 hours, Saturday and Sunday · Why this one: it is the thing you point at when somebody says "show me how you think", and ninety seconds of a recruiter's attention is what it gets.

<!-- deliverable-page: the answer is a public portfolio repository, not a program -->

## The Brief

This is not a new project. It is the **closing** of the project you started in
Week 1, when you pushed five write-ups on arrays. Fifteen weeks later there are
fifty-plus. This week brings the total past sixty, audits the lot to one bar,
bolts on the last artifacts, and polishes the cover until a stranger can read the
repo in ninety seconds.

One public repository — `crunchtime-interview-prep-<yourhandle>` — holding FRAME
across sixty-plus problems, four recorded mocks, a system-design write-up, a
behavioural story bank, a recruiter-prep pack, a personalised study plan, and
three honestly-earned badges.

Most of the content already exists. Every prior week's mini-project, exercises
and homework fed this repo. Week 15 is assembly.

Three reasons.

1. **The portfolio is the proof, and proof beats claims.** Anyone can say "I'm good at algorithms." A repo with 60+ FRAME write-ups, four recorded mocks you watched without flinching, and a commit history spanning fifteen weeks *proves* it. A recruiter who lands on this repo gives it about ninety seconds before deciding whether to keep scrolling. In those ninety seconds the README cover, the progress dashboard, and the commit history have to say "this person has been deliberate about interview prep for fifteen weeks and can back every claim." This week is where you make those ninety seconds land.

2. **The mock trajectory is the highest-signal artifact you own.** Mocks #1 (W4) → #2 (W9) → #3 (W14) → #4 (W15) are the record of whether you can *self-correct* — and self-correction is the single trait a senior engineer reads to judge whether you will grow on the job. Four recorded mocks with honest self-feedback, ending in the Mock #1→#4 trajectory note, is worth more than another ten write-ups. It is the part of the portfolio that cannot be faked.

3. **The repo is a reusable, living artifact.** When a friend starts interviewing in six months, you fork the structure to them. When you interview again in two years, you pick up where you left off instead of starting over. A portfolio that keeps getting occasional commits reads as an engineer who stays sharp; one whose commits trail off reads as abandoned. This is the artifact you maintain (homework Part 5), not the one you archive.

---

## Starter

Everything from the other three exercises this week lands here, so do them first:

```text
Exercise 1   the audit          every existing write-up brought to the six-point bar
Exercise 2   the design artifact system-design/url-shortener.md
Exercise 3   the prep pack      job-search/
Exercise 4   the plan           study-plan/pre-onsite-4-weeks.md
Challenge 1  Mock #4            mocks/mock-04/ and the trajectory note
Challenge 2  the design mock    the recording and self-grade
```

The repo structure is below under Requirements. Every directory in it should
already be partly populated; this week completes and audits it.

This repo is not assembled in Week 15 — it is *closed* in Week 15. The trail:

- **W1–W2** — five array write-ups, then re-done with complexity sections. The first commits.
- **W3–W12** — every week's mini-project, exercises, and homework added write-ups (sliding window, fast/slow, binary search, BFS, DFS, backtracking, heaps, intervals/greedy, DP 1D, DP 2D). The pattern-paired mini-projects (W6–W9) added the parallel write-ups.
- **W4 / W9 / W14** — Mocks #1, #2, #3 recorded with self-feedback, each added to `mocks/`.
- **W12** — the URL-shortener design write-up drafted (`system-design/`).
- **W13** — the 12-story STAR bank and coverage matrix (`behavioral/story-bank/`).
- **W14** — the last write-ups (XOR fold, binary trie) bring the total toward sixty.
- **W15** — the audit, Mock #4, the system-design polish, the recruiter pack, the study plan, the badges, and the README cover. The close.

If a directory is thin, that is the gap Week 15 fills. The audit (Exercise 1) is where you discover what is missing.

---

## Requirements

A single **public** GitHub repository, **`crunchtime-interview-prep-<yourhandle>`**, with this structure. Every directory below should already be partly populated from prior weeks; Week 15 completes and audits it.

```
crunchtime-interview-prep-<you>/
├── README.md                       ← the portfolio cover (the 90-second sell) — polished this week
├── frame-writeups/
│   ├── 01-two-sum.md               ← 60+ problem write-ups in FRAME format
│   ├── 02-best-time-to-buy.md
│   ├── …                            ← organized by pattern and/or by week (c2-week-NN/)
│   └── 60-maximum-xor.md
├── mocks/
│   ├── mock-01-week-04.md          ← recording link + two-pass self-feedback
│   ├── mock-02-week-09.md
│   ├── mock-03-week-14.md
│   └── mock-04-week-15.md          ← full-loop self-feedback + the Mock #1→#4 trajectory note
├── system-design/
│   └── url-shortener.md            ← the junior-level design write-up (Exercise 2)
├── behavioral/
│   └── story-bank/
│       ├── story-bank.md           ← your 12+ STAR anecdotes (from Week 13)
│       └── coverage-matrix.md      ← story × category coverage, no empty column
├── recruiter-prep/
│   ├── resume-v3.pdf               ← audited against the Tech Interview Handbook guide
│   ├── target-companies.md         ← tiered list (reach / target / safety)
│   ├── outreach-template.md        ← the cold-outreach template
│   └── follow-up-template.md       ← the thank-you + follow-up template
├── study-plan/
│   ├── go-forward-plan.md          ← the full personalized plan (homework Parts 1–6)
│   └── pre-onsite-4-weeks.md       ← your personalized last-mile plan (Exercise 4 + homework Part 4)
└── badges/
    ├── frame-apprentice.json
    ├── pattern-practitioner.json
    └── crunchtime-graduate.json
```

This matches the capstone tree in the [SYLLABUS](../../../README.md#what-you-ship-capstone-deliverables) and the README's [capstone deliverables](../README.md#the-capstone-deliverables-what-you-ship) section.

---

### The README cover

The repo README is the single highest-leverage file in the capstone. It is what loads first, and it must sell the repo before the recruiter decides whether to scroll. Build it in this order — the order matters, because a recruiter reads top-down and stops the moment they lose interest:

1. **The one-line pitch (above the fold).** One sentence: who you are and what the repo proves. *"Fifteen weeks of deliberate interview preparation — FRAME for 60+ problems, four recorded mocks, and a system-design write-up. Here's how I think."* Not "my practice solutions." A pitch, not a description.

2. **The progress dashboard.** A small table or badge row that surfaces the headline numbers at a glance: write-up count, patterns covered, mocks recorded, system-design write-ups. Example:

   | | |
   |---|---|
   | **Write-ups** | 62 (FRAME format) |
   | **Patterns** | 14 / 14 covered |
   | **Recorded mocks** | 4 (W4, W9, W14, W15) |
   | **System-design** | 1 (URL shortener, 10K QPS) |
   | **Behavioral** | 12-story STAR bank |

3. **The pattern × write-up index.** A table mapping each of the fourteen patterns to its write-ups, so a recruiter (or you, prepping for a specific company) can jump straight to "all the graph problems." This is the navigation spine of the repo.

4. **The mocks section, prominent.** Link the four mock self-feedback notes high on the page — they are your strongest signal. Lead with the Mock #1→#4 trajectory line: *"Mock #1 I coded silently for ten minutes; by Mock #4 I narrate continuously and recover from a wrong direction out loud."*

5. **A "how this repo is organized" note** and a one-line "fork this for your own prep" invitation. The reusable-artifact framing is itself a signal of how you think.

The test: screen-record yourself scrolling the README aloud as if presenting to a recruiter. If you cannot make it compelling in ninety seconds, the cover is not done. (This is a stretch goal in the [README](../README.md#stretch-goals) — and the highest-leverage ninety minutes you can spend on the capstone.)

---

### The quality bar for every write-up

Every write-up must clear the six-point bar from [Exercise 1](../exercises/exercise-01-portfolio-audit.md). A write-up that fails any one of these is not "done" — it is a liability, because a recruiter who opens one weak write-up assumes the rest are weak too:

1. **Research-constraints memo present** — a 30-second pattern-recognition memo at the top: the pattern, the cue, the sub-shape, and one rejected alternative.
2. **All five FRAME sections present** — Frame · Research constraints · Assess options · Make the solution · Examine; none half-finished.
3. **Code is correct and tested** — it runs, it passes the examples, and there is at least one edge-case trace in Examine (verify).
4. **Complexity is *derived*, not just stated** — the Examine (cost) section shows *why* the bound holds, not only the big-O.
5. **Type hints + PEP 8** — every function typed; idiomatic Python ([PEP 8](https://peps.python.org/pep-0008/)).
6. **It reads cleanly** — a stranger can follow it without you narrating.

The audit (Exercise 1) is where you find and fix the write-ups that fail — the half-finished Examine, the missing Research-constraints memo, the untested code. The bar is non-negotiable: **60+ write-ups, every one audited.**

---

### Rubric

Graded across eight dimensions; total 100, passing bar **≥ 70**. A capstone that scores below 70 on any single dimension is not shippable — fix that dimension before you call C2 done.

| Dimension | Weight | What full credit looks like |
|-----------|------:|------------------------------|
| **README cover / scannability** | 15 | One-line pitch, dashboard, pattern index, prominent mocks; readable in 90 seconds |
| **Write-up volume + audit** | 20 | 60+ write-ups, every one clears the six-point bar; the audit log shows weak ones were fixed |
| **Mock trajectory** | 20 | All four mocks present with honest two-pass self-feedback; the Mock #1→#4 trajectory is articulated and credible |
| **System-design write-up** | 10 | URL shortener complete through requirements → estimation → API → data model → ID scheme → caching → read/write path |
| **Behavioral story bank** | 10 | 12+ STAR stories; coverage matrix with no empty column |
| **Recruiter-prep pack** | 10 | Audited resume, tiered target list, usable outreach + follow-up templates |
| **Personalized study plan** | 10 | Weakness diagnosis, spaced-repetition tiers, application cadence, 4-week pre-onsite plan, maintenance plan |
| **Commit history + polish** | 5 | Sustained daily commits across 15 weeks; badges present and honest; peer star |

The two heaviest dimensions — **write-up volume + audit (20)** and **mock trajectory (20)** — are deliberately the ones that cannot be faked: you either did sixty audited write-ups and four honest mocks, or you didn't. They are 40% of the grade because they are 80% of the signal.

---

## Constraints

- **Public.** A private portfolio is a private diary. If something in it cannot be
  public, remove that thing rather than the repo.
- **Sixty-plus write-ups, every one audited.** The bar is not negotiable, because
  the recruiter opens a random one. One weak write-up discounts the other
  fifty-nine.
- **The dashboard count is the passing count**, not the file count. This is the
  single easiest claim in the repo to disprove.
- **Ninety seconds is the budget.** The cover is written for a reader who will
  stop the moment they lose interest, and the order of the sections is what
  decides whether they do.
- **The mocks go high on the page.** They are the strongest signal you own and the
  one part that cannot be faked. Burying them below the write-up index is the most
  common self-inflicted wound on this page.
- **Badges are earned or absent.** A badge for something you did not do is worse
  than no badge, and it is the sort of thing that gets checked.
- **Assembly, not creation.** If you find yourself writing new content this
  weekend beyond the last ten write-ups, you are doing a different project.

## Expected output

What a finished capstone measures:

```text
write-ups             60+, every one clearing all six bars
patterns covered      14 / 14
recorded mocks        4  (W4, W9, W14, W15) with self-feedback for each
trajectory note       1, Mock #1 to #4
system-design         1 written artifact + 1 recorded design mock
behavioural           12+ story bank, coverage matrix with no empty column
job-search            resume, tier list, outreach + follow-up + thank-you
study-plan            weakness diagnosis + 4-week pre-onsite plan
badges                3, all earned
commit history        ~15 weeks, continuous

README cover          readable aloud, compellingly, in 90 seconds
```

The test for the cover is not a checklist. Screen-record yourself scrolling it
and reading it aloud as if presenting to a recruiter. If you cannot make it
compelling in ninety seconds, the cover is not done — and that ninety minutes is
the highest-leverage time in the whole weekend.

## Steps

1. Finish the four exercises and both challenges first. They are the contents.
2. Run the audit (Exercise 1) to completion. Do not start the cover until the
   count is true.
3. Write the last ten-plus write-ups to clear sixty, choosing patterns from the
   thin columns of your own index rather than from what you enjoy.
4. Assemble the directory structure. Every folder populated, nothing left as a
   placeholder.
5. Build the pattern index — it is the navigation spine and it is what makes the
   repo usable by somebody else.
6. Write the README cover in the order given above: pitch, dashboard, index,
   mocks, organisation note.
7. Check every badge against what you actually did. Remove any that does not
   hold.
8. Screen-record the ninety-second read-through. Fix whatever made you wince.
9. Push. The programme closes on the push.

## The Solution

The worked answer here is the **cover**, because it is the artifact everything
else is judged through and the one people write last and worst.

Here is a complete one, at the length it should actually be:

```markdown
# crunchtime-interview-prep

Fifteen weeks of deliberate interview preparation: FRAME write-ups for 62
problems, four recorded mock interviews with honest self-feedback, and a
junior-level system-design artifact. This repo is how I think, written down.

| | |
|---|---|
| **Write-ups** | 62, all in FRAME format, all audited |
| **Patterns** | 14 / 14 covered |
| **Recorded mocks** | 4 — weeks 4, 9, 14, 15 |
| **System design** | 1 written (URL shortener, 10K QPS) + 1 timed mock |
| **Behavioural** | 12-story bank, 8 / 8 categories covered |

## The mocks

The four recordings are the part of this repo I would read first. They are the
record of whether I can correct myself, which is the only thing fifteen weeks of
practice can really prove.

- [Mock #1 — week 4](mocks/mock-01/self-feedback.md) — I coded silently for ten
  minutes and did not notice.
- [Mock #2 — week 9](mocks/mock-02/self-feedback.md) — narrating, still losing
  the thread under time pressure.
- [Mock #3 — week 14](mocks/mock-03/self-feedback.md) — near-real conditions;
  first round where I recovered from a wrong direction out loud.
- [Mock #4 — week 15](mocks/mock-04/self-feedback.md) — full loop, three rounds
  back to back. [The trajectory across all four](mocks/trajectory.md).

## Write-ups by pattern

| Pattern | Write-ups |
|---|---|
| Arrays and hashing | [01](frame-writeups/01-refund-pair.md), [02](frame-writeups/02-badge-rescan.md), [04](frame-writeups/04-stage-twins.md) … |
| Two pointers | … |
| … | … |

## How this repo is organised

`frame-writeups/` is one file per problem, each with a 30-second recognition memo
at the top and all five FRAME sections below it. `mocks/` holds the recordings
and the self-feedback. `system-design/`, `behavioral/`, `study-plan/` and
`job-search/` hold the rest.

Fork it if you are prepping. The structure is the useful part.
```

Four things make that cover work, and all four are easy to get wrong.

**The pitch is a claim, not a description.** "Fifteen weeks of deliberate
interview preparation… this repo is how I think" says what the repo proves. "My
my practice solutions" says what is in the folder, and nobody scrolls past it.

**The dashboard is above the index.** Numbers first, navigation second. A reader
deciding whether to keep scrolling wants the size of the thing before its
contents.

**The mocks are third, not last.** They are the strongest signal in the repo and
the only one that cannot be faked, and the standard mistake is to put them at the
bottom because they feel like process rather than product.

**The mock links carry one honest sentence each.** "I coded silently for ten
minutes and did not notice" is worth more than any claim you could make about
yourself, because it demonstrates the thing it describes. A reader who sees a
candidate write that about their own recording stops needing to be convinced
about self-awareness.

## How to deliver it

One public GitHub repository, named `crunchtime-interview-prep-<yourhandle>`.

Push everything by Sunday end of day. The programme closes on the push — not on
the last write-up, not on Mock #4, on the push.

After that, the repo is maintained rather than archived. A portfolio that keeps
getting occasional commits reads as an engineer who stays sharp; one whose commits
stop reads as abandoned, and the difference is visible on the contributions graph
from across the room.

## Common bugs to catch

- **A private repo.** Symptom: a portfolio nobody can open.
- **A file count on the dashboard.** Symptom: a number a reader disproves by
  opening one weak write-up.
- **The mocks at the bottom.** Symptom: your strongest evidence below the fold.
- **A description instead of a pitch.** Symptom: "my solutions to interview
  problems", and a reader who stops at line one.
- **No pattern index.** Symptom: sixty write-ups nobody can navigate, including
  you, the week before an onsite.
- **Badges that are not earned.** Symptom: a claim that fails the first check, and
  every other claim in the repo devalued with it.
- **Writing new content instead of assembling.** Symptom: Sunday evening, a
  half-finished new write-up, and no cover.
- **Skipping the ninety-second read-through.** Symptom: a cover that reads fine
  silently and falls apart out loud. Every weak sentence is audible.

## Acceptance checklist

The capstone is complete when **all** of the following are true and the repo is public and pushed:

- [ ] The repo is **public** on GitHub at `crunchtime-interview-prep-<yourhandle>`.
- [ ] The **README cover** follows the spec above: one-line pitch, progress dashboard, pattern × write-up index, prominent mocks section, organization note.
- [ ] **60+ FRAME write-ups** are present, organized by pattern and/or week, and **every one** has been audited against the six-point bar (Exercise 1) — no missing Research-constraints memo, no untested code, no half-finished Examine, no underived complexity.
- [ ] **All four mock self-feedback notes** are present (`mock-01`…`mock-04`), each with a recording link and two-pass notes; the Mock #4 note carries the **Mock #1 → #4 trajectory**.
- [ ] The **system-design write-up** (`system-design/url-shortener.md`) is present and complete through the read/write path (Exercise 2).
- [ ] The **behavioral story bank** with its **coverage matrix** (no empty column) is present under `behavioral/story-bank/`.
- [ ] The **recruiter-prep pack** is present: resume, tiered `target-companies.md`, `outreach-template.md`, `follow-up-template.md` (Exercise 3).
- [ ] The **personalized study plan** is present: `study-plan/go-forward-plan.md` (homework Parts 1–6) and `study-plan/pre-onsite-4-weeks.md` (Exercise 4).
- [ ] The three **badges** are present and **honestly earned** (`frame-apprentice`, `pattern-practitioner`, `crunchtime-graduate`).
- [ ] The **commit history** shows sustained, roughly-daily commits across the fifteen weeks — months of evidence, not one bulk dump.
- [ ] The repo is **starred by at least one peer** who actually reviewed it (the pair-audit stretch goal is the natural way to earn this).

---

## Stretch

- Record the ninety-second walkthrough properly and link it from the cover. Very
  few candidates do this, and it lets a recruiter hear you before they meet you.
- Write the "what I would do differently over fifteen weeks" note and commit it.
  It is the same self-correction signal as the mock trajectory, applied to the
  whole programme.
- Set a calendar reminder for three months out to re-audit and add two write-ups.
  The difference between a living portfolio and an archive is about two hours a
  quarter.
- Fork the structure to somebody who is starting. Explaining why the repo is laid
  out this way is the fastest way to find out which parts of it you actually
  believe in.

## After the capstone — you go interview

When this repo is public, pushed, and clears the rubric, **C2 is complete.** Stop and take the measure of it: a public repository with 60+ problem write-ups, four recorded mocks you watched without flinching, a system-design write-up, a twelve-story behavioral bank, a recruiter pack, and a written plan for the next four weeks and beyond. That is not a completion certificate. That is a *portfolio* — and it is the thing you point a hiring manager at when they ask "show me how you think."

Then do the thing the portfolio is for. Open your [personalized go-forward study plan](../homework/README.md), send the first batch of applications this week using the [recruiter-prep pack](../exercises/exercise-03-recruiter-prep-pack.md) you built, and — when an offer comes — go to [C13 · Hack the Interview](../../../../C13-HACK-THE-INTERVIEW/) for negotiation and to [C3 · Crunch Labs Portfolio](../../../../C3-CRUNCH-LABS-PORTFOLIO/) to build a project portfolio alongside this one.

You have done the work. The next mock is a real one, for a real job. Go get the offer.

---

*If you find errors in this material, please open an issue or send a PR. Future learners will thank you.*
