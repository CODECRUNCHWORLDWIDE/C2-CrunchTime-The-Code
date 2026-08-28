# Mini-Project — The Capstone Portfolio

> The course's final deliverable, and the most important file of the week: a single public GitHub repository — **`crunchtime-interview-prep-<yourhandle>`** — that has grown from the Week 1 mini-project into a recruiter-grade artifact demonstrating FRAME across 60+ problems, four recorded mocks, a system-design write-up, a behavioral story bank, a recruiter-prep pack, a personalized study plan, and three honestly-earned badges. This is the thing you point a recruiter at when they say "show me how you think."

**Estimated time:** ~7 hours this week, but most of the *content* already exists — every prior week's mini-project, exercises, and homework fed this repo. Week 15 is assembly and polish, not creation. Treat Saturday–Sunday as the assembly weekend.

This is not a new project. It is the *closing* of the project you have been building since Week 1, when you pushed five array write-ups. Fifteen weeks later you have fifty-plus; this week brings the total over sixty, audits the lot for quality, bolts on the final artifacts, and polishes the README cover until a recruiter can read the repo in ninety seconds.

---

## Why this matters

Three reasons.

1. **The portfolio is the proof, and proof beats claims.** Anyone can say "I'm good at algorithms." A repo with 60+ FRAME write-ups, four recorded mocks you watched without flinching, and a commit history spanning fifteen weeks *proves* it. A recruiter who lands on this repo gives it about ninety seconds before deciding whether to keep scrolling. In those ninety seconds the README cover, the progress dashboard, and the commit history have to say "this person has been deliberate about interview prep for fifteen weeks and can back every claim." This week is where you make those ninety seconds land.

2. **The mock trajectory is the highest-signal artifact you own.** Mocks #1 (W4) → #2 (W9) → #3 (W14) → #4 (W15) are the record of whether you can *self-correct* — and self-correction is the single trait a senior engineer reads to judge whether you will grow on the job. Four recorded mocks with honest self-feedback, ending in the Mock #1→#4 trajectory note, is worth more than another ten write-ups. It is the part of the portfolio that cannot be faked.

3. **The repo is a reusable, living artifact.** When a friend starts interviewing in six months, you fork the structure to them. When you interview again in two years, you pick up where you left off instead of starting over. A portfolio that keeps getting occasional commits reads as an engineer who stays sharp; one whose commits trail off reads as abandoned. This is the artifact you maintain (homework Part 5), not the one you archive.

---

## What you ship

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

## The README-cover spec (what the recruiter sees first)

The repo README is the single highest-leverage file in the capstone. It is what loads first, and it must sell the repo before the recruiter decides whether to scroll. Build it in this order — the order matters, because a recruiter reads top-down and stops the moment they lose interest:

1. **The one-line pitch (above the fold).** One sentence: who you are and what the repo proves. *"Fifteen weeks of deliberate interview prep — FRAME for 60+ problems, four recorded mocks, and a system-design write-up. Here's how I think."* Not "my LeetCode solutions." A pitch, not a description.

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

## The 60+ write-up quality bar

Every write-up must clear the six-point bar from [Exercise 1](../exercises/exercise-01-portfolio-audit.md). A write-up that fails any one of these is not "done" — it is a liability, because a recruiter who opens one weak write-up assumes the rest are weak too:

1. **Research-constraints memo present** — a 30-second pattern-recognition memo at the top: the pattern, the cue, the sub-shape, and one rejected alternative.
2. **All five FRAME sections present** — Frame · Research constraints · Assess options · Make the solution · Examine; none half-finished.
3. **Code is correct and tested** — it runs, it passes the examples, and there is at least one edge-case trace in Examine (verify).
4. **Complexity is *derived*, not just stated** — the Examine (cost) section shows *why* the bound holds, not only the big-O.
5. **Type hints + PEP 8** — every function typed; idiomatic Python ([PEP 8](https://peps.python.org/pep-0008/)).
6. **It reads cleanly** — a stranger can follow it without you narrating.

The audit (Exercise 1) is where you find and fix the write-ups that fail — the half-finished Examine, the missing Research-constraints memo, the untested code. The bar is non-negotiable: **60+ write-ups, every one audited.**

---

## Acceptance criteria

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

## Rubric

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

## How every prior week fed this repo

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

## After the capstone — you go interview

When this repo is public, pushed, and clears the rubric, **C2 is complete.** Stop and take the measure of it: a public repository with 60+ problem write-ups, four recorded mocks you watched without flinching, a system-design write-up, a twelve-story behavioral bank, a recruiter pack, and a written plan for the next four weeks and beyond. That is not a completion certificate. That is a *portfolio* — and it is the thing you point a hiring manager at when they ask "show me how you think."

Then do the thing the portfolio is for. Open your [personalized go-forward study plan](../homework/README.md), send the first batch of applications this week using the [recruiter-prep pack](../exercises/exercise-03-recruiter-prep-pack.md) you built, and — when an offer comes — go to [C13 · Hack the Interview](../../../C13-HACK-THE-INTERVIEW/) for negotiation and to [C3 · Crunch Labs Portfolio](../../../C3-CRUNCH-LABS-PORTFOLIO/) to build a project portfolio alongside this one.

You have done the work. The next mock is a real one, for a real job. Go get the offer.

---

*If you find errors in this material, please open an issue or send a PR. Future learners will thank you.*
