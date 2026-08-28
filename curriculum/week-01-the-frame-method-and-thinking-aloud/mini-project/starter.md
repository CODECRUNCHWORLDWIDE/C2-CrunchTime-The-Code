# Mini-Project starter — the repository skeleton

Scaffolding for the [mini-project](./README.md). Nothing here is a problem to
solve; it is the material you copy so that you can spend your time on the
writing rather than on typing folder names.

## The files to copy

### `.gitignore`

```text
__pycache__/
*.py[cod]
.venv/
venv/
.env
.DS_Store
.idea/
.vscode/
*.swp
```

Two of those are worth a sentence. `__pycache__/` is where Python caches the
compiled form of your modules; it is generated, machine-specific, and never
belongs in a repository. `.DS_Store` is a folder-view file macOS writes into
every directory you open in Finder — harmless, invisible locally, and
faintly embarrassing when it turns up in a public repository.

### `README.md` — the cover

Replace every angle-bracketed placeholder. Do not ship a sentence you would
not say out loud to a stranger.

```markdown
# CrunchTime Interview Prep · <Your Name>

I'm <Your Name>, a <one line, specific — for example "self-taught engineer
preparing for backend roles in spring 2027">. This repo is my public
interview-prep work, built openly so that I stay accountable to my own
progress and so that other learners can fork the approach.

## What's in here

- [`progress.md`](progress.md) — my live dashboard. Streak, patterns
  completed, mocks recorded.
- [`frame-writeups/`](frame-writeups/) — every problem I solve gets a full
  FRAME write-up. Currently <N> problems.
- [`mocks/`](mocks/) — recorded mock interviews with self-feedback.
- [`system-design/`](system-design/) — my system-design notes.
- [`behavioral/`](behavioral/) — my STAR-format story bank.
- [`recruiter-prep/`](recruiter-prep/) — resume, target companies, outreach
  templates.
- [`study-plan/`](study-plan/) — weekly reflections and my pre-onsite plan.
- [`badges/`](badges/) — milestone badges I've earned.

## Method

This work follows [C2 · CrunchTime — The Code](https://github.com/CODECRUNCHWORLDWIDE/C2-CrunchTime-The-Code),
a free open-source interview-prep curriculum built around the FRAME method:
Frame, Research constraints, Assess options, Make the solution, Examine.

## Licence

My work in this repo: CC-BY-4.0. The C2 curriculum it follows: GPL-3.0.
Fork this structure for your own prep if it is useful — and if you do, open
an issue on the C2 repo to be added to the showcase.
```

Note the method line names five steps and expands them once, correctly. If
you write it any other way, a reader who has done the course will notice.

### `progress.md` — the dashboard

```markdown
# Progress

**Pathway:** intensive (15 weeks) · **Started:** <date> · **Streak:** <N> days

| Week | Pattern | Exercises | Challenges | Mini-project | Mock |
|-----:|---------|:---------:|:----------:|:------------:|:----:|
| 01 | Two pointers | 5/5 | 0/2 | done | — |
| 02 | Hash maps | | | | |

## Patterns I can recognise in under 30 seconds

- Converging two pointers — sorted input, looking for a pair.

## Patterns I still have to think about

- (be honest here; this list is the useful one)

## Mocks recorded

| # | Date | Problem shape | What I'd fix |
|--:|------|---------------|--------------|
```

The two lists in the middle are the part that earns its keep. A table of
ticks tells you what you have done; the "still have to think about" list
tells you what to do next.

### `mocks/README.md` — the schema

```markdown
# Mock interviews

One folder per mock: `mock-NN-<pattern>/`, holding

- `prompt.md` — the problem as it was given to me
- `notes.md` — my FRAME pass, written up afterwards
- `feedback.md` — what my partner said, verbatim, before I argue with it
- `recording.md` — a link to the recording, or a note on where it lives
```

### `badges/README.md` and `recruiter-prep/README.md`

Both are placeholders this week. Give each one a heading and one line saying
when it gets filled in, so that a reader who clicks does not land on an empty
file and wonder whether the repository is abandoned.

## Suggested order of work

1. Repository first, empty, public, cloned.
2. `portfolio_scaffold.py` next, run against a temporary folder.
3. Point it at the clone. Everything appears at once.
4. Replace seeded files with real content, one commit at a time.
5. `README.md` last, when you know what you are describing.

## What "great" looks like

| Criterion | Weight | Great looks like |
|-----------|-------:|------------------|
| Repository set up | 30% | Public, all nineteen paths, licence, gitignore |
| Week 1 content committed | 30% | Five write-ups, five solutions, three homework artifacts |
| README cover | 20% | Specific, no boilerplate, would hold a stranger's attention |
| `progress.md` dashboard | 10% | Accurate, and the two honest lists are filled in |
| Commit hygiene | 10% | Ten or more commits, messages a stranger could read |

Back to the [mini-project brief](./README.md).
