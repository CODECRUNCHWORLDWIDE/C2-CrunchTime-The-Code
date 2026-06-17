# Week 15 — Exercise Solutions

Unlike the algorithm weeks, these exercises have no single correct answer — a resume bullet, a portfolio README, and a LinkedIn headline each have many right forms. So this file gives **worked examples** and the **rubric** each artifact is graded on, not an answer key. Compare your output to the examples; grade yourself against the rubric; have a peer or mentor sanity-check the verdict.

Read these only after you have built your own artifacts. The point is to calibrate, not to copy.

---

## Exercise 1 — Portfolio README

### Worked example (above the fold)

```markdown
# Maya Okonkwo — Interview-Prep Portfolio

> Backend-leaning software engineer (3 yrs, Python/Go). This repo documents
> 64 algorithm problems solved with the UMPIRE framework (Understand, Match,
> Plan, Implement, Review, Evaluate) across 15 weeks of structured practice,
> plus four recorded mock interviews.

## Start here

- [Edit Distance — 2D DP, three-way min](./umpire-writeups/c2-week-11/challenge-01-edit-distance.md) — my cleanest dynamic-programming write-up
- [Course Schedule — topological sort + cycle detection](./umpire-writeups/c2-week-07/exercise-01-course-schedule.md) — graph modeling
- [Mock #4 self-feedback](./mocks/mock-04/self-feedback.md) — how I run a 45-minute loop and self-correct
```

Why this works: the blockquote states who (backend engineer, Python/Go) and what (64 problems, UMPIRE, 15 weeks, 4 mocks) in three sentences. The count is specific (64, not "many"). The start-here set shows range — DP, graph, and a communication artifact — not three easy wins. Every link is relative and would resolve in the repo.

### Common failure modes

| Failure | Fix |
|---------|-----|
| README is the default GitHub placeholder | Write the who/what/start-here, period |
| Pitch says "many problems" | State the exact count; back-fill to 60+ if short |
| Start-here is three easy problems | Choose for range: one hard DP, one graph, one communication piece |
| Index grouped by week | Regroup by pattern; week is a secondary tag |
| Broken links | Click every link after pushing |

### Rubric

| Dimension | "Yes" looks like |
|-----------|------------------|
| Above the fold | Who, what, and start-here all in the first screenful |
| Specific count | A real number (60+) in the pitch |
| Start-here range | 3–4 links spanning different pattern families |
| Index by pattern | Grouped by the 14 patterns; every row ≥ 2 links; mock row present |
| Links resolve | All clicked and working post-push |
| Tone | Plain, senior, no emoji/buzzword soup |

---

## Exercise 2 — Resume bullets

### Worked examples (before → after)

| Before | After |
|--------|-------|
| "Responsible for the team's CI pipeline." | "Rebuilt the team's CI pipeline in GitHub Actions, cutting average build time from 22 to 6 minutes and eliminating ~40 flaky failures/week." |
| "Helped migrate services to Kubernetes." | "Migrated 8 backend services to Kubernetes with zero-downtime cutover, reducing deploy time from 30 min to under 5." |
| "Worked on the search feature." | "Built the autocomplete search backend (trie + Redis cache) serving 1.2M queries/day at p99 under 40ms." |
| "Familiar with data structures and algorithms." | (deleted — this is a skills-line entry, not an achievement bullet) |
| "Did a coding bootcamp project." | "Shipped a full-stack expense tracker (React + FastAPI + Postgres) used by 200+ beta users; deployed on Fly.io with CI." |

### The portfolio bullet (the sixth)

```
CrunchTime Interview-Prep Portfolio                    github.com/maya/prep
  Solved 64 data-structure and algorithm problems with the UMPIRE framework
  across 15 weeks; every solution documented with complexity analysis, plus
  four recorded mock interviews. Public, navigable, indexed by pattern.
```

### Rubric

| Dimension | "Yes" looks like |
|-----------|------------------|
| Shape | Every bullet: action verb + what you built + scope/impact |
| Banned phrases | Zero instances of "responsible for / helped / worked on / familiar with" |
| Strong verbs | Every bullet opens with an action verb |
| Quantification | At least 3 of 5 carry a number; the rest name a concrete scope |
| Portfolio bullet | Present, strong-shaped, links the portfolio |
| One-page fit | All six fit comfortably on one page |

---

## Exercise 3 — LinkedIn levers

### Worked examples (before → after)

**Headline**

- Before: "Aspiring Software Developer | Bootcamp Grad | Open to Work"
- After: "Software Engineer | Python, Data Structures & Algorithms | Building backend & data tools"

**About (first paragraph)**

- Before (third person, generic): "Maya is a passionate developer who loves coding and is eager to learn and grow in a fast-paced environment."
- After (first person, specific, keyword-rich): "I'm a backend-leaning software engineer who turns ambiguous problems into shipped systems. Over the last three years I've built data pipelines and search backends in Python and Go; most recently I rebuilt a CI pipeline that cut build times 70%. I'm looking for a role where I can own a service end-to-end and go deeper on distributed systems."

**Featured caption**

- After: "Interview-prep portfolio — 64 algorithm problems solved with the UMPIRE framework, indexed by pattern. github.com/maya/prep"

**Skills (top three)**

- Before: "Microsoft Office, Teamwork, Communication, Python"
- After: "Python, Data Structures, Algorithms" (then: Go, PostgreSQL, REST APIs, Kubernetes, ...)

### Rubric

| Dimension | "Yes" looks like |
|-----------|------------------|
| Headline | ≥ 2 target keywords; no "aspiring"; reads as a peer |
| About | First person; 3–4 paragraphs; keywords present; portfolio linked |
| Featured | Portfolio pinned with a one-line caption |
| Skills | Top three match recruiter-filter phrases for target roles |
| Keyword consistency | Same exact phrasings across headline, About, skills, and the target job descriptions |

---

## The meta-lesson

All three exercises are the same skill in different surfaces: **design an artifact for a specific reader with a short attention budget**. The portfolio README's reader is a hiring manager with four minutes; the resume's reader is a recruiter with six seconds; the LinkedIn profile's reader is a search algorithm plus the recruiter who clicks the result. In every case you are not "describing yourself" — you are optimizing a piece of communication for a known reader and a known decision. That is the synthesis the whole week is about: fourteen weeks proved you can do the work; this week makes the work *legible* to the people who decide whether to interview you.
