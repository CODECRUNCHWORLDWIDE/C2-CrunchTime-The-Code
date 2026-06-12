# Mini-Project — Set Up Your Interview-Prep Portfolio Repo

> The single repo you will commit to for the next 15 weeks (or 51) and ultimately point recruiters at.

**Estimated time:** 5–7 hours, split across Thursday-Saturday.

This is the *only* mini-project of the course that produces infrastructure rather than content. Every subsequent week's mini-project *adds to* this repo. By Week 15 it is the artifact you point hiring managers at.

---

## What you ship

A public GitHub repository named `crunchtime-interview-prep-<yourhandle>`. Final structure target (you'll build it up week by week):

```
crunchtime-interview-prep-<you>/
├── README.md                       ← portfolio cover (most important file)
├── LICENSE                         ← CC-BY-4.0 or MIT (your work; not C2 itself)
├── .gitignore                      ← Python, macOS, IDE
├── progress.md                     ← your live dashboard (streak, patterns, mocks)
├── umpire-writeups/
│   └── c2-week-01/                 ← drills + wild problem, written up
├── mocks/
│   └── README.md                   ← schema for each mock entry
├── system-design/
│   └── notes-week-01.md            ← URL shortener warm-up (from homework)
├── behavioral/
│   └── story-01.md                 ← debugging story (from homework)
├── recruiter-prep/
│   └── README.md                   ← placeholder; populated Week 15
├── study-plan/
│   ├── week-01-reflection.md
│   └── pre-onsite-template.md      ← we provide; you customize Week 15
└── badges/
    └── README.md                   ← placeholder; badges added as earned
```

This week you set up the skeleton and populate just the Week 1 contents. The structure is what matters.

---

## Acceptance criteria

- [ ] Public GitHub repo `crunchtime-interview-prep-<yourhandle>` exists.
- [ ] Repository is **public**. (Private repos help no one — including future you.)
- [ ] All eight top-level files / directories listed above are present.
- [ ] `README.md` answers, in order:
  1. **Who am I?** One paragraph. Don't pretend; you're a learner.
  2. **What is this repo?** Two sentences.
  3. **What's in it?** Link to each subdirectory with a one-line description.
  4. **What's my progress?** Link to `progress.md`.
  5. **License.** Note your license (CC-BY or MIT) and that the C2 curriculum it follows is GPL-3.0.
- [ ] `progress.md` follows the [intensive study plan template](../../study-plans/intensive-15-week.md#tracking-your-progress) (or the mastery equivalent).
- [ ] All Week 1 drill solutions are committed (`drill-01-solution.py` through `drill-05-solution.py`) under `umpire-writeups/c2-week-01/`.
- [ ] All Week 1 UMPIRE write-ups are committed (`drill-01-reverse-string.md` through `drill-05-container-with-most-water.md`).
- [ ] At least one "wild problem" UMPIRE write-up (from homework #3) is committed.
- [ ] The `system-design/` and `behavioral/` folders contain Week 1's contributions (from homework #4 and #5).
- [ ] `study-plan/week-01-reflection.md` (homework #6) is committed.
- [ ] At least 10 commits with **meaningful messages** (not just "wip" or "update"). "Add Drill 3 UMPIRE write-up" is good; "stuff" is not.
- [ ] Repository is **starred by at least one peer or instructor.** This step is social. Reach out to someone in the Code Crunch community.

---

## Suggested order of operations

### Thursday — Skeleton (2h)

1. Create the repo on GitHub.
2. Clone locally. Initialize the directory structure.
3. Write `.gitignore` and `LICENSE`.
4. Write a stub `README.md` (~150 lines). Push.
5. Write `progress.md`. Push.

### Friday — Week 1 content (2h)

6. Move your five drill solutions + write-ups into `umpire-writeups/c2-week-01/`. Push each as its own commit.
7. Move your behavioral story #1 into `behavioral/story-01.md`. Push.
8. Move your system-design warm-up into `system-design/notes-week-01.md`. Push.

### Saturday — Polish + reflection (3h)

9. Polish `README.md` until it would impress a stranger.
10. Write `study-plan/week-01-reflection.md`. Push.
11. Audit the repo: does the URL render cleanly on GitHub? Does the README cover answer all five questions? Does `progress.md` make sense to a peer?
12. Send the link to one person in the Code Crunch community. Ask for two things they'd improve. **Apply at least one** before Sunday end.

---

## The README cover — make this great

This is the file recruiters and hiring managers see first. Aim for the following structure (and use real, specific writing — not boilerplate):

```markdown
# CrunchTime Interview Prep · <Your Name>

I'm <Your Name>, a <one-line description, e.g. "self-taught engineer
preparing for senior backend roles in Spring 2027">. This repo is my
public interview-prep work — built openly so that (a) I'm accountable to
my own progress, and (b) future learners can fork my approach.

## What's in here

- [`progress.md`](progress.md) — my live dashboard. Streak, patterns
  completed, mocks recorded.
- [`umpire-writeups/`](umpire-writeups/) — every problem I solve gets a
  full UMPIRE write-up. Currently <N> problems.
- [`mocks/`](mocks/) — recorded mock interviews with self-feedback.
- [`system-design/`](system-design/) — my system-design notes and one
  capstone write-up.
- [`behavioral/`](behavioral/) — my STAR-format story bank.
- [`recruiter-prep/`](recruiter-prep/) — resume, target companies,
  outreach templates.
- [`study-plan/`](study-plan/) — weekly reflections and my pre-onsite
  4-week plan.
- [`badges/`](badges/) — open-source milestone badges I've earned.

## Methodology

This work follows [C2 · CrunchTime — The Code](https://github.com/CODECRUNCHWORLDWIDE/C2-CrunchTime-The-Code),
a free open-source interview-prep curriculum built around the UMPIRE Method
(Understand · Match · Plan · Implement · Review · Evaluate).

## License

My work in this repo: CC-BY-4.0. The C2 curriculum it follows: GPL-3.0.
You may fork this structure for your own prep. If you do, please open an
issue on the C2 repo to be added to the showcase.
```

That cover, with your name and real specifics, is what a recruiter sees. Make it good.

---

## What "great" looks like (rubric)

| Criterion | Weight | "Great" looks like |
|-----------|------:|--------------------|
| Repo set up | 30% | All directories present, public, license, gitignore |
| Week 1 content committed | 30% | All drills, write-ups, homework artifacts present |
| README cover | 20% | Clean, specific, no boilerplate, would impress a stranger |
| `progress.md` dashboard | 10% | Working, updated, accurate |
| Commit hygiene | 10% | ≥10 commits, meaningful messages |

---

## Why this matters

The portfolio repo is **the thing you point at when applying.** It demonstrates, in chronological commit history, that you sustained a practice for months. That single piece of evidence outweighs almost anything else on a junior or career-switcher resume.

By Week 15 it will be the most valuable artifact you've ever produced as a learner.

---

When you're done: push, send the link to one peer for review, then move on to [Week 2](../../week-02-complexity-and-hash-maps/) (coming soon — currently a placeholder; the C2 curriculum builds out week by week).
