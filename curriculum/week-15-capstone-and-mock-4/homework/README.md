# Week 15 — Homework: The Personalized Go-Forward Study Plan

This is the course's explicit final deliverable — the single most useful document you will write all week. It is not a set of practice problems. It is *your plan*: built from your own fifty-plus write-ups and four mock self-feedback notes, aimed at your own weaknesses, set to a cadence you can actually hold. A generic study plan is worthless. A plan you wrote from your own evidence is the thing future-you follows into a real onsite.

The homework is a guided build in six parts. By Sunday you ship two files to the capstone repo — `study-plan/go-forward-plan.md` (the full plan, Parts 1–6) and `study-plan/pre-onsite-4-weeks.md` (the last-mile template, Part 4, also Exercise 4). Allow ~5–6 hours, most of it on Saturday and Sunday. The grounding for every part is [Lecture 3](.././lecture-notes/03-the-personalized-go-forward-study-plan.md); this homework is where you turn that lecture into your own document.

| # | Part | What it produces | Est. time |
|---|------|------------------|----------:|
| 1 | Weakness self-diagnosis | The ranked list of 2–3 hot patterns + 1 weak behavior | 1h |
| 2 | Spaced-repetition schedule | The three-tier table + your weekly rhythm | 1h |
| 3 | Application cadence + funnel math | Your weekly cadence and the funnel you expect | 0.75h |
| 4 | Pre-onsite 4-week plan | `study-plan/pre-onsite-4-weeks.md` (also Exercise 4) | 1h |
| 5 | Maintenance plan | The between-offer upkeep floor | 0.5h |
| 6 | Final reflection on C2 | The closing reflection on the whole journey | 0.75h |

---

## Part 1 — Weakness self-diagnosis

You cannot make a plan until you know what to drill. Pull from the two sources you already have: your **write-up history** (the 60+ FRAME write-ups) and your **four mock self-feedback notes**.

### Source 1 — the write-up history

For each of the fourteen patterns, fill the table. Count quality write-ups, mark whether the pattern felt fluent (be honest — "I solved it eventually after looking something up" is *not* fluent), and note the specific struggle.

| Pattern | # quality write-ups | Felt fluent? | Notes (the specific struggle) |
|---------|--------------------:|:------------:|-------------------------------|
| Arrays & two pointers | | | |
| Hash maps | | | |
| Sliding window | | | |
| Fast/slow pointers | | | |
| Binary search | | | |
| BFS | | | |
| DFS / topological sort | | | |
| Backtracking | | | |
| Heaps / top-K | | | |
| Intervals / greedy | | | |
| DP 1D | | | |
| DP 2D | | | |
| Bit manipulation | | | |
| Behavioral / STAR | (story count) | | |

The rows you mark **"No"** under *Felt fluent?* are your primary drill targets. Rank them worst-first.

### Source 2 — the four mock self-feedback notes

Each mock named one behavior change. Pull all four and judge whether the weakness is gone, improved, or still present.

| Mock | Behavior change named | Made it? | Status now |
|------|-----------------------|:--------:|-----------|
| #1 (../W4) | | | |
| #2 (../W9) | | | |
| #3 (../W14) | | | |
| #4 (../W15) | | | |

A behavior weakness **still present after four mocks** is your highest-priority meta-target — it is exactly what a real interviewer will see.

### The diagnosis output

Write the ranked list. This drives everything below.

```
Hot patterns (drill hardest):   1) ____  2) ____  3) ____
Warm patterns (keep up):        ____, ____, ____
Weak behavior (top meta-target): ____
```

**Acceptance.** Both source tables filled honestly, and a three-line ranked output. If every pattern says "Yes" and every mock behavior says "Gone," you have either finished a genuinely strong course or not been honest — re-watch Mock #4 with the trajectory note open before you accept that result.

---

## Part 2 — The spaced-repetition schedule for the fourteen patterns

Skills decay unless refreshed, and the trap is treating all fourteen patterns equally. Sort them into three tiers from your Part 1 diagnosis, then build a concrete weekly rhythm.

| Tier | Which patterns (from Part 1) | Review cadence | Reps per touch |
|------|------------------------------|----------------|----------------|
| **Hot (../weak)** | your 2–3 "not fluent" patterns | every 3–4 days | 2 problems each |
| **Warm (mostly fluent)** | your "mostly" patterns | weekly | 1 problem each |
| **Cold (../reflexive)** | your reflexive patterns | every 2–3 weeks | 1 problem, recognition-only |

Now write *your* weekly rhythm — assign specific patterns to specific days. A template to personalize:

```
Mon:  <hot pattern 1> (2 problems)
Tue:  <hot pattern 2> (2 problems)
Wed:  <hot pattern 3> (2 problems)
Thu:  <warm pattern> + <warm pattern> (1 each)
Fri:  <warm pattern> + <warm pattern> (1 each)
Sat:  one cold-tier problem (rotate through the reflexive patterns)
Sun:  one mock OR rest
```

That is ~10 problems a week — weighted toward the weak, touching every pattern within a three-week window so none goes fully cold. **The schedule is living:** re-run the Part 1 diagnosis every two weeks; as a hot pattern becomes fluent, promote it to warm and pull the next weak one up.

Problem sources, free: the [NeetCode roadmap](https://neetcode.io/) groups problems by pattern (maps directly onto the tiers); [LeetCode](https://leetcode.com/) tag pages give an endless supply per pattern; the Blind 75 / NeetCode 150 lists are the minimum-viable cold-tier rotation when time is short.

**Acceptance.** The three-tier table filled with your patterns, plus a written weekly rhythm naming specific patterns per day and a named problem source per hot pattern.

---

## Part 3 — The application cadence and the funnel math

A study plan with no applications is a hobby. The other half of the plan is putting real applications into the funnel — and knowing the funnel math so rejections do not derail you.

### The funnel you should expect

These are illustrative base rates for a competently-prepared early-career candidate; track your own and overwrite them as data comes in:

```
100 applications / outreach
  ↓  ~15–25% get a recruiter screen
 ~20 recruiter screens
  ↓  ~50% advance to a technical screen
 ~10 technical screens
  ↓  ~40–50% advance to an onsite
 ~4–5 onsites
  ↓  ~20–35% convert to an offer
 ~1–2 offers
```

**One offer can require ~50–100 applications.** That is the base rate, not a sign you are doing it wrong. A candidate who applies to five companies and gets no offer has learned nothing — the sample is too small.

### Your cadence

Set a sustainable weekly cadence and hold it. Fill in numbers you can actually sustain:

| Activity | Your cadence | Source |
|----------|--------------|--------|
| New applications / outreach | ___ per week (target 8–12) | the tiered list from [Exercise 3](.././exercises/exercise-03-recruiter-prep-pack.md) |
| Follow-ups on prior outreach | ___ per week (../3–5) | the follow-up template from Exercise 3 |
| Pattern drilling | ___ problems/week (../~10) | Part 2 schedule |
| Mock interviews | one every ___ weeks (../1–2) | Pramp / interviewing.io / a peer |

The key discipline: **apply continuously, do not batch-and-wait.** Batching empties the funnel — by the time the rejections return you must rebuild momentum from zero. Hold the 8–12/week cadence so something is always in every stage.

**Acceptance.** Your funnel numbers (start with the base rates, then replace with your own as you go) and a filled cadence table with numbers you will actually hold.

---

## Part 4 — The pre-onsite four-week last-mile plan

When a real onsite is booked — usually 1–4 weeks out — your general plan compresses into a focused sprint. This is Exercise 4; if you have not built it, build it now. It tapers breadth → depth → mocks → rest:

| Week out | Theme | Daily volume | Your personalized focus |
|----------|-------|--------------|--------------------------|
| **4** | Breadth + re-diagnose | 2 problems/day, all 14 patterns | _(re-run the diagnosis; confirm nothing is cold)_ |
| **3** | Depth on hot patterns + company research | 3 problems/day on weak patterns | _(your hot list; the company's eng blog)_ |
| **2** | Full mocks + tailor the story bank | 1 full mock + 2 problems/day | _(which 3 stories to tailor for this company)_ |
| **1** | Taper + logistics + rest | 1–2 easy problems/day | _(setup test, schedule, questions per interviewer)_ |

The week-1 taper is non-negotiable: cramming the night before makes you tired and anxious — worse, not better. Athletes taper before a race; so do you. If the onsite is sooner than four weeks, compress proportionally (a one-week notice collapses to two days breadth, two days depth, one day full mock, then taper).

**Acceptance.** `study-plan/pre-onsite-4-weeks.md` exists, all four weeks filled with *your* hot patterns and weak behavior (not the generic template), Week 1 is a genuine taper, and each hot pattern names a specific problem source. (Exercise 4 has the full worked example.)

---

## Part 5 — The maintenance plan (between-offer upkeep)

Even after you stop active interviewing — between offers, or after accepting one while keeping options open — skills decay. The maintenance plan is the low-effort floor that keeps you from starting over:

- **Three problems a week**, rotating the cold tier so every pattern gets touched within ~5 weeks. (~30 minutes a day, three days a week.)
- **One mock a month**, to keep narration, timing, and the full-loop rhythm from going cold.
- **Keep the portfolio living** — add a write-up when you solve something interesting. A repo with commits trailing off looks abandoned; one with occasional fresh commits looks like an engineer who keeps sharp.

That floor is the difference between picking back up in a day versus rebuilding fluency over a month when the next search starts.

**Acceptance.** A three-line maintenance floor written into your plan, plus a one-line "wins log" commitment (note every screen passed, clean mock, recruiter reply — it keeps progress visible on the hard days) and a named rest day each week.

---

## Part 6 — Final reflection on the C2 journey

This is the last thing you write before you go interview. Write 8–12 sentences addressing:

1. **Then vs. now.** Fifteen weeks ago, what could you *not* do that you can do reflexively today? Be concrete — name a pattern or a behavior.
2. **The mock trajectory.** Across Mocks #1 → #4, what is the one behavior change that is now reflexive, and the one weakness that is still present? (This should match your Mock #4 trajectory note.)
3. **The hardest week.** Which of the fifteen weeks was hardest, and what did you learn from pushing through it?
4. **The one drill that mattered most.** Of everything in C2 — the FRAME method, the 30-second Research-constraints memo, the two-pass mock watching, the STAR story bank — which single practice changed how you interview the most? Why?
5. **The road ahead.** In one sentence: what does the next four weeks look like, and what is the first concrete action you take this week (which application do you send first)?

The reflection is the portfolio-grade artifact — it is what turns this homework from "I made a schedule" into "I know exactly who I am as a candidate and what I do next." Future you, on the hard days of the search, will thank present you for writing it.

**Acceptance.** A reflection of 8–12 sentences committed at the top of `study-plan/go-forward-plan.md`.

---

## Time budget

| Block | Hours | When |
|-------|------:|------|
| Part 1 — weakness diagnosis | 1.0 | Saturday |
| Part 2 — spaced-repetition schedule | 1.0 | Saturday |
| Part 3 — application cadence + funnel math | 0.75 | Saturday |
| Part 4 — pre-onsite 4-week plan (Exercise 4) | 1.0 | Sunday |
| Part 5 — maintenance plan | 0.5 | Sunday |
| Part 6 — final reflection | 0.75 | Sunday |
| **Total** | **~5** | **the assembly weekend** |

---

## Acceptance — the homework is complete when:

- [ ] **Part 1** — both source tables (write-ups, mocks) filled honestly; a three-line ranked output of 2–3 hot patterns + 1 weak behavior.
- [ ] **Part 2** — the three-tier spaced-repetition table filled with your patterns; a written weekly rhythm with a named problem source per hot pattern.
- [ ] **Part 3** — your funnel numbers and a filled cadence table (applications, follow-ups, drilling, mocks) with numbers you will hold.
- [ ] **Part 4** — `study-plan/pre-onsite-4-weeks.md` committed, all four weeks personalized, Week 1 a genuine taper.
- [ ] **Part 5** — a three-line maintenance floor, a wins-log commitment, and a named weekly rest day.
- [ ] **Part 6** — the 8–12 sentence final reflection committed at the top of `study-plan/go-forward-plan.md`.
- [ ] Both files (`go-forward-plan.md` + `pre-onsite-4-weeks.md`) are pushed to the capstone repo.
- [ ] The quiz is taken and scored, and its outcome (apply now / finish capstone / drill more) is reflected in the plan's cadence.

The single most useful artifact this week is the **weakness diagnosis with its ranked output** — it is the difference between drilling everything equally (and improving nothing) and drilling the two or three things that are actually holding you back. Build the plan from your own evidence, set the cadence, and then do the thing the plan is for: **you go interview.**

When the plan is written and the capstone is published, return to the README's [**Where you go from here — you go interview**](.././README.md#where-you-go-from-here--you-go-interview) section. That is the last thing C2 asks of you: open the plan, send the first application, and go.
