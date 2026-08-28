# Mini-Project — Your Interview-Prep Portfolio Repo

> **Topic:** the one public repository you will commit to for the next fifteen weeks, and a small program that builds and audits its shape
> **Lecture:** [01 — What Interviewers Actually Score](../lecture-notes/01-what-interviewers-actually-score.md)
> **Difficulty:** nothing here is algorithmically hard; keeping the layout honest as it grows for fifteen weeks is the whole project
> **Target time:** 5–7 hours, spread across Thursday to Saturday
> **Why this one:** it is the only mini-project in the course that produces infrastructure rather than content, and every later week adds to it. By Week 15 it is the artifact you point a hiring manager at — a commit history showing that you sustained a practice for months. That single piece of evidence outweighs almost anything else on a junior or career-switcher resume.

<!-- no-runnable-file: what you hand in is a repository on GitHub with your own writing in it, which no test can run. The runnable answer is portfolio-scaffold-solution.py, which ships beside this page, is linked from Download and run, and is shown in full under The Solution. It is named after the project rather than after the page because a file called README.py would be a strange thing to ask anybody to download. -->

## The Brief

You are creating one public GitHub repository, called
`crunchtime-interview-prep-<yourhandle>`, and you will still be committing to
it in Week 15.

The repository has a required shape — a set of folders and files, each one
holding a particular kind of work. Here it is:

```text
crunchtime-interview-prep-<you>/
├── README.md                       ← the portfolio cover; the most important file
├── LICENSE                         ← CC-BY-4.0 or MIT, for your work
├── .gitignore                      ← Python, editor noise
├── progress.md                     ← your live dashboard: streak, patterns, mocks
├── frame-writeups/
│   └── c2-week-01/                 ← this week's five exercises, written up
├── mocks/
│   └── README.md                   ← the schema each mock entry follows
├── system-design/
│   └── notes-week-01.md            ← the URL-shortener warm-up, from homework
├── behavioral/
│   └── story-01.md                 ← the debugging story, from homework
├── recruiter-prep/
│   └── README.md                   ← a placeholder; filled in Week 15
├── study-plan/
│   ├── week-01-reflection.md
│   └── pre-onsite-template.md      ← we provide it; you customise it in Week 15
└── badges/
    └── README.md                   ← a placeholder; badges added as you earn them
```

That is nineteen paths. You could make them by hand this week. The trouble is
Week 6, when you add `frame-writeups/c2-week-06/` and forget `mocks/`
entirely, and nothing tells you — a missing folder is silent in a way a
missing function never is.

So the deliverable has two halves.

**The repository**, with this week's real work committed into it.

**A small program that builds and checks the layout.** One list describing
the required shape, a function that creates whatever is missing, and a
function that reports what is there. Both read the same list, so the checker
can never drift away from the builder. Add a folder to the list and both of
them learn about it at once.

That last sentence is the actual engineering idea on this page, and it has a
name: **a single source of truth.** Two things that must agree should be
generated from one description rather than written out twice and kept in step
by hand. You will meet the principle again every time a project has a config
file and documentation that both describe the same settings.

## Starter

Save this as `portfolio_scaffold.py` inside your new repository and fill in
the `TODO`s. There is more scaffolding than usual here because the shape of
the program is part of the lesson — see
[starter.md](./starter.md) for the repository skeleton and the suggested
order of work.

```python
"""portfolio_scaffold.py — build and audit your interview-prep portfolio.

One list describes the required layout. One function creates what is
missing, another reports what is there, and both read that same list.

Fill in every TODO, then run the file with no arguments. It rehearses in a
temporary folder and prints an audit.
"""

from __future__ import annotations

import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

HANDLE_PLACEHOLDER = "<yourhandle>"


@dataclass(frozen=True)
class Entry:
    """One required path in the portfolio, and what should be in it."""

    path: str
    is_dir: bool
    seed: str = ""


# TODO: write out the nineteen entries from The Brief, in the order they
#       appear there. Folders get is_dir=True; files get a one-line seed so
#       a fresh file is never empty and always says what it is for.
PLAN: list[Entry] = []


def build(root: Path) -> list[str]:
    """Create every missing entry under `root`. Never overwrite."""
    # TODO: make root itself, then walk PLAN. Create a folder when it is not
    #       already a folder; write a file only when nothing is there.
    #       Collect and return the paths you actually created.
    ...


def audit(root: Path) -> list[tuple[str, bool]]:
    """Report whether each planned entry exists, and is the right kind."""
    # TODO: one (path, ok) pair per PLAN entry, in PLAN order. A file
    #       standing where a folder belongs is not ok.
    ...


def main(argv: list[str]) -> int:
    """Build the portfolio, audit it, and print the report."""
    # TODO: with no arguments, build inside tempfile.mkdtemp() and delete it
    #       afterwards. With `--into PATH`, build at PATH for real.
    # TODO: build, audit, print, then build a SECOND time and report that it
    #       created nothing — that is the proof it is safe to re-run.
    ...


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/courses/ide#src=C2-CrunchTime-The-Code/curriculum/week-01-the-frame-method-and-thinking-aloud/mini-project/README.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. A **public** GitHub repository named
   `crunchtime-interview-prep-<yourhandle>` exists. Private repositories
   help nobody, including future you.
2. Every one of the nineteen paths in The Brief is present.
3. `README.md` answers five questions, in this order: who you are, what this
   repository is, what is in it (with a link and one line per folder), where
   your progress lives, and what licence applies.
4. `progress.md` follows the
   [intensive study plan template](../../study-plans/intensive-15-week.md#tracking-your-progress),
   or the mastery equivalent.
5. This week's five exercise write-ups and five solution files are committed
   under `frame-writeups/c2-week-01/`.
6. The homework artifacts are committed where the plan puts them:
   `behavioral/story-01.md`, `system-design/notes-week-01.md`,
   `study-plan/week-01-reflection.md`.
7. `portfolio_scaffold.py` runs with no arguments, builds and audits a
   throwaway copy of the layout, and prints the audit.
8. Running `build` twice creates nothing the second time and overwrites
   nothing.
9. At least ten commits, with messages a stranger could read.
   `Add exercise 3 FRAME write-up` is a message; `stuff` is not.

## Constraints

- **The repository must be public, and it must stay public.** The whole
  argument for this artifact is that somebody else can look at it. A private
  repository is a diary.

- **Your work is yours to licence; the course is not.** Put CC-BY-4.0 or MIT
  on your own writing, and say in the README that the C2 curriculum it
  follows is GPL-3.0. Those are different licences on different things and
  conflating them is the kind of small inaccuracy a careful reader notices.

- **`build` never overwrites an existing file.** This is the constraint that
  makes the program worth having. A scaffolder you can only run once is a
  scaffolder you run once and then abandon; one that is safe on a repository
  full of fourteen weeks of work is one you actually use in Week 14. It is
  also the difference between a helpful tool and a tool that eats your
  homework.

- **The plan is data, not code.** The nineteen paths live in one list. Do not
  spell them out again inside `audit` — the moment the two disagree, the
  checker starts lying with full confidence, and it will do so quietly.

- **No third-party packages.** `pathlib`, `shutil`, `tempfile` and
  `dataclasses` are all in the standard library. A tool that needs a `pip
  install` before it can check your folders is not a tool you will run on a
  borrowed laptop.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13:

```text
$ python portfolio-scaffold-solution.py
Rehearsing in a temporary folder. Nothing is written to your disk.
Repository name: crunchtime-interview-prep-<yourhandle>

Created 19 of 19 planned entries.

Audit after building:
  ok       README.md
  ok       LICENSE
  ok       .gitignore
  ok       progress.md
  ok       frame-writeups/
  ok       frame-writeups/c2-week-01/
  ok       mocks/
  ok       mocks/README.md
  ok       system-design/
  ok       system-design/notes-week-01.md
  ok       behavioral/
  ok       behavioral/story-01.md
  ok       recruiter-prep/
  ok       recruiter-prep/README.md
  ok       study-plan/
  ok       study-plan/week-01-reflection.md
  ok       study-plan/pre-onsite-template.md
  ok       badges/
  ok       badges/README.md

Second run created 0 entries - re-running is safe.
Portfolio skeleton complete.
```

Two lines carry the weight.

`Created 19 of 19 planned entries.` is what a first run looks like — the
folder was empty, so everything was made.

`Second run created 0 entries - re-running is safe.` is the interesting one.
The program built the tree, then immediately tried to build it again. Nothing
was created because everything already existed. That single line is the proof
of the "never overwrite" constraint, and it is printed rather than merely
asserted because you want to see it every time you run the tool on your real
repository, where the stakes are your own writing.

When you point it at a repository that has drifted, the audit is what you
read:

```text
  ok       frame-writeups/c2-week-01/
  MISSING  mocks/README.md
```

## Steps

### Thursday — the skeleton, about two hours

1. Create the repository on GitHub, public, named
   `crunchtime-interview-prep-<yourhandle>`. Clone it.
2. Write `portfolio_scaffold.py` from the starter. Get it running against a
   temporary folder first, where mistakes cost nothing.
3. Run it against your clone: `python portfolio_scaffold.py --into .`
4. Replace the seeded one-line files with real content. Start with
   `.gitignore` and `LICENSE`, which are quick.
5. Write a stub `README.md` and `progress.md`. Commit and push each as its
   own commit.

### Friday — this week's content, about two hours

6. Move your five exercise write-ups and five solution files into
   `frame-writeups/c2-week-01/`. One commit each.
7. Move your behavioural story into `behavioral/story-01.md`.
8. Move your system-design warm-up into `system-design/notes-week-01.md`.
9. Re-run the scaffolder. Everything should report `ok` and nothing should be
   created.

### Saturday — polish and reflection, about three hours

10. Rewrite `README.md` until it would hold a stranger's attention. This is
    the file a recruiter opens first.
11. Write `study-plan/week-01-reflection.md`.
12. Audit by eye as well as by program: does the repository render cleanly on
    GitHub? Does the README cover answer all five questions? Would
    `progress.md` make sense to somebody who is not you?
13. Send the link to one person in the Code Crunch community. Ask for two
    things they would improve, and apply at least one before Sunday.

## The Solution

```python
"""portfolio-scaffold-solution.py — build and audit your interview-prep portfolio.

The mini-project asks for a repository with a particular shape. This program
is that shape, written down once so a machine can build it and check it.

Two things live here, and keeping them apart is the whole design:

  * PLAN — the required layout, as data. One list of entries.
  * build() and audit() — two functions that read PLAN. One creates what is
    missing; the other reports what is there.

Because both read the same list, the checker can never drift away from the
builder. Add a folder to PLAN and both of them learn about it at once.

Run it with no arguments and it does a rehearsal: it builds the tree inside a
temporary folder, audits it, prints the report, then deletes the folder again
so nothing is left behind. That is what the output below shows.

Run it with a path and it builds there for real:

    python portfolio-scaffold-solution.py --into ~/code/crunchtime-interview-prep-yourhandle

It never overwrites a file that already exists, so it is safe to re-run on a
repository you have been working in for weeks. Re-running is the point: it is
how you find out which week-14 folder you forgot to create.
"""

from __future__ import annotations

import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

HANDLE_PLACEHOLDER = "<yourhandle>"


@dataclass(frozen=True)
class Entry:
    """One required path in the portfolio, and what should be in it.

    Attributes:
        path: Where it lives, relative to the repository root.
        is_dir: True for a folder, False for a file.
        seed: First line to write into a new file, so the file is never
            empty and always says what it is for. Ignored for folders.
    """

    path: str
    is_dir: bool
    seed: str = ""


PLAN: list[Entry] = [
    Entry("README.md", False, "# CrunchTime Interview Prep"),
    Entry("LICENSE", False, "Choose CC-BY-4.0 or MIT and paste the full text here."),
    Entry(".gitignore", False, "__pycache__/"),
    Entry("progress.md", False, "# Progress dashboard"),
    Entry("frame-writeups", True),
    Entry("frame-writeups/c2-week-01", True),
    Entry("mocks", True),
    Entry("mocks/README.md", False, "# Mock interviews"),
    Entry("system-design", True),
    Entry("system-design/notes-week-01.md", False, "# System design - week 1 warm-up"),
    Entry("behavioral", True),
    Entry("behavioral/story-01.md", False, "# Story 1 - a hard bug I debugged"),
    Entry("recruiter-prep", True),
    Entry("recruiter-prep/README.md", False, "# Recruiter prep - populated in week 15"),
    Entry("study-plan", True),
    Entry("study-plan/week-01-reflection.md", False, "# Week 1 reflection"),
    Entry("study-plan/pre-onsite-template.md", False, "# Pre-onsite plan - four weeks out"),
    Entry("badges", True),
    Entry("badges/README.md", False, "# Badges earned"),
]


def build(root: Path) -> list[str]:
    """Create every missing entry under `root`. Never overwrite.

    Args:
        root: The repository root. Created if it does not exist.

    Returns:
        The paths that were created, in PLAN order.
    """
    created: list[str] = []
    root.mkdir(parents=True, exist_ok=True)

    for entry in PLAN:
        target = root / entry.path
        if entry.is_dir:
            if not target.is_dir():
                target.mkdir(parents=True)
                created.append(entry.path + "/")
        else:
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(entry.seed + "\n", encoding="utf-8")
                created.append(entry.path)

    return created


def audit(root: Path) -> list[tuple[str, bool]]:
    """Report whether each planned entry exists, and is the right kind.

    Args:
        root: The repository root to inspect.

    Returns:
        One (path, ok) pair per PLAN entry, in PLAN order. `ok` is False
        when the entry is missing, and also when a file is standing where a
        folder belongs or the other way round.
    """
    findings: list[tuple[str, bool]] = []
    for entry in PLAN:
        target = root / entry.path
        ok = target.is_dir() if entry.is_dir else target.is_file()
        findings.append((entry.path, ok))
    return findings


def render(findings: list[tuple[str, bool]]) -> list[str]:
    """Turn audit findings into printable lines, folders marked with a slash."""
    lines: list[str] = []
    for path, ok in findings:
        entry = next(item for item in PLAN if item.path == path)
        shown = path + "/" if entry.is_dir else path
        lines.append(f"  {'ok     ' if ok else 'MISSING'}  {shown}")
    return lines


def main(argv: list[str]) -> int:
    """Build the portfolio, audit it, and print the report.

    Args:
        argv: Command-line arguments after the program name. `--into PATH`
            builds at PATH. With no arguments the program rehearses in a
            temporary folder and cleans up afterwards.

    Returns:
        0 when every planned entry is present afterwards, 1 otherwise.
    """
    rehearsing = "--into" not in argv
    if rehearsing:
        root = Path(tempfile.mkdtemp(prefix="crunchtime-portfolio-"))
        print("Rehearsing in a temporary folder. Nothing is written to your disk.")
    else:
        root = Path(argv[argv.index("--into") + 1]).expanduser()
        print(f"Building in {root}")

    print(f"Repository name: crunchtime-interview-prep-{HANDLE_PLACEHOLDER}")
    print()

    try:
        created = build(root)
        print(f"Created {len(created)} of {len(PLAN)} planned entries.")
        print()

        findings = audit(root)
        print("Audit after building:")
        for line in render(findings):
            print(line)
        print()

        # The second build proves the program is safe to re-run: everything
        # already exists, so nothing is created and nothing is overwritten.
        again = build(root)
        print(f"Second run created {len(again)} entries - re-running is safe.")

        missing = [path for path, ok in findings if not ok]
        if missing:
            print(f"Still missing: {missing}")
            return 1
        print("Portfolio skeleton complete.")
        return 0
    finally:
        if rehearsing:
            shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

**`PLAN` is the whole program, and the two functions are just readers of it.**
That is the point worth taking away. The alternative — a `build` function
full of `mkdir` calls and an `audit` function full of `exists` calls — works
perfectly on the day you write it and starts lying the first time somebody
updates one and not the other. Here there is nowhere for a disagreement to
live.

**`Entry` is a frozen dataclass rather than a tuple.** `entry.is_dir` says
what it means; `entry[1]` does not. Freezing it means nothing can quietly
rewrite the plan halfway through a run. Three lines of declaration buy
readable code at every use site, which is the same trade as the `namedtuple`
in C1's Week 5.

**`build` checks before it writes, and the two branches check different
things.** For a folder it asks `is_dir()`, because a *file* named
`mocks` should be reported as a problem rather than silently accepted. For a
file it asks `exists()` rather than `is_file()`, because if something is
already sitting at that path — even a folder — the safe move is to leave it
alone and let `audit` complain. Refusing to overwrite is more important than
being tidy.

**Building twice is a test, and it is printed rather than asserted.** The
second call returns an empty list because every path already exists. Printing
that count means you see the guarantee every time you run the tool on your
real repository, which is where you actually care about it. An assertion
would prove the same thing and show you nothing.

**The rehearsal mode is what makes the file runnable anywhere.** With no
arguments the program builds inside `tempfile.mkdtemp()` and deletes it in a
`finally` block, so it leaves nothing behind even if something raises
partway. That is why you can run the shipped file on your own machine, right
now, without deciding where your portfolio is going to live first.

**`main` returns an exit code, and that is not decoration.** `0` when the
layout is complete, `1` when something is missing. That makes the tool usable
from a shell script or a Git hook later — `python portfolio_scaffold.py --into . || echo "layout drifted"`
— without any changes. Programs that report success through their exit status
compose; programs that only print do not.

## Download and run

Download
[portfolio-scaffold-solution.py](./portfolio-scaffold-solution.py)
and run it:

```bash
python portfolio-scaffold-solution.py
```

That is the rehearsal: it builds the layout in a temporary folder, audits it,
prints the report, and cleans up. To build your real repository, give it a
path:

```bash
python portfolio-scaffold-solution.py --into ~/code/crunchtime-interview-prep-yourhandle
```

It is the same program you are writing, under a name that will not collide
with your own `portfolio_scaffold.py`.

## Common bugs to catch

- **`TypeError: 'NoneType' object is not iterable` when you print the audit.**
  Your `audit` builds a list and forgets to return it:

  ```text
  Traceback (most recent call last):
      for line in render(findings):
                         ^^^^^^^^
  TypeError: 'NoneType' object is not iterable
  ```

  A function with no `return` hands back `None`. The message names the place
  the `None` was *used*, not the place it was made, which is why you look one
  frame up.

- **`FileNotFoundError` when creating a nested file.** You wrote the file
  before its parent folder existed:

  ```text
  Traceback (most recent call last):
      target.write_text(entry.seed + "\n", encoding="utf-8")
  FileNotFoundError: [Errno 2] No such file or directory: 'mocks/README.md'
  ```

  Two fixes and only one is right. Reordering `PLAN` so folders always come
  before their contents works until somebody adds an entry in the wrong
  place. Calling `target.parent.mkdir(parents=True, exist_ok=True)` first
  works whatever the order. Prefer the fix that cannot be undone by an
  innocent edit.

- **The scaffolder overwrites your README.** You wrote the file without
  checking:

  ```text
  Created 19 of 19 planned entries.
  ```

  on a repository that already had nineteen. Nothing raises, and that count
  is the only warning you get — a first run and a destructive re-run print
  the same line. The guard is `if not target.exists()`, and this is why the
  program prints the second-run count: on a healthy repository it is `0`.

- **`IndexError: list index out of range` from `--into` with nothing after
  it.**

  ```text
  Traceback (most recent call last):
      root = Path(argv[argv.index("--into") + 1]).expanduser()
                  ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  IndexError: list index out of range
  ```

  The shipped version is deliberately minimal about argument handling — one
  flag, read positionally. If you want it to fail politely instead, that is
  the first stretch below.

- **The audit passes and the folder is wrong.** You listed the paths a second
  time inside `audit` instead of reading `PLAN`. Nothing raises, ever. The
  checker simply stops checking the thing you changed, and you find out in
  Week 14.

- **A file standing where a folder belongs.** `audit` using `exists()` for
  everything reports `ok` for a *file* called `mocks`. Use `is_dir()` for
  folders and `is_file()` for files: the question is not "is something
  there", it is "is the right kind of thing there".

- **Committing the temporary folder.** If you run the rehearsal from inside
  your repository, nothing is written there — the temporary folder is
  somewhere else entirely, which is the point. But `__pycache__/` *will*
  appear, which is why it is the seeded line in `.gitignore`.

## Under the hood

<details>
<summary>Under the hood — idempotence, why the plan is data, and what a recruiter actually reads</summary>

**Idempotent is the word for what `build` is.**

An operation is **idempotent** when doing it twice has the same effect as
doing it once. Setting a light switch to "off" is idempotent; flipping it is
not. `build` is idempotent because it only ever creates what is missing, so
running it on a complete repository does nothing at all.

This matters far beyond this page. Every infrastructure tool worth using —
package managers, deployment systems, database migrations — is built around
idempotence, because the alternative is a tool you are afraid to run. Fear of
running your own tooling is how repositories drift.

The property is easy to lose by accident. `target.write_text(...)` with no
guard is not idempotent. `target.mkdir(parents=True)` without `exist_ok=True`
raises the second time. Both are one keyword away from correct, and both fail
in ways you will not notice until the run that matters.

**Why the plan is data and not code.**

Compare:

```python
# The version that drifts
def build(root):
    (root / "mocks").mkdir(exist_ok=True)
    (root / "badges").mkdir(exist_ok=True)

def audit(root):
    return [(root / "mocks").is_dir(), (root / "badges").is_dir()]
```

Two lists of the same facts, in two places. The day somebody adds
`interviews/` to `build` and forgets `audit`, the audit still passes and it
is now wrong. Nothing warns you, because from the computer's point of view
nothing is inconsistent — there are simply two functions that happen to
disagree.

Pulling the shared facts into `PLAN` removes the possibility. This is the
same reasoning behind a single `requirements.txt`, a single schema
definition, a single constants module. Any time you notice yourself writing
the same list twice, the list wants to be data.

**`pathlib` versus string paths.**

`root / entry.path` builds a path with the right separator for the operating
system, so the same program works on Windows and on Linux without a single
`os.sep`. `Path.expanduser()` turns `~/code/...` into a real home directory —
the shell normally does that for you, but only when the argument is unquoted,
so a program that accepts paths has to do it itself.

`Path` objects also carry their own questions: `is_dir()`, `is_file()`,
`exists()`. Compare that with `os.path.isdir(os.path.join(root, path))`, which
says the same thing with more punctuation.

**What a recruiter actually reads.**

Not your code. The README, for about twenty seconds, and the commit graph.
That is the honest reason this project spends so much of its time budget on a
cover page and on commit hygiene.

The cover should answer, in this order: who you are, what this is, what is in
it, where the progress lives, and what licence applies. Concretely, and
without boilerplate — "self-taught engineer preparing for backend roles in
spring 2027" tells a reader something; "passionate about technology" does
not.

And the commit graph tells a story no cover letter can. Fifteen weeks of
regular, meaningfully-titled commits is evidence of a sustained practice. Ten
commits in one evening followed by silence is evidence of something else.
That is why the requirement is at least ten commits with real messages rather
than one commit with everything in it — the shape of the history is part of
the artifact.

</details>

## Acceptance checklist

- [ ] A public GitHub repository named `crunchtime-interview-prep-<yourhandle>` exists.
- [ ] All nineteen paths from The Brief are present, and the scaffolder reports every one as `ok`.
- [ ] `python portfolio_scaffold.py` runs with no arguments and prints an audit.
- [ ] The second build reports `0` entries created.
- [ ] `PLAN` is written out once, and `audit` reads it rather than repeating it.
- [ ] `build` overwrites nothing — you tested that by running it on a folder with real content in it.
- [ ] `README.md` answers all five questions, with specifics rather than boilerplate.
- [ ] `progress.md` follows the study-plan template and would make sense to a peer.
- [ ] This week's five write-ups and five solutions are committed under `frame-writeups/c2-week-01/`.
- [ ] The three homework artifacts are committed where the plan puts them.
- [ ] At least ten commits, each with a message a stranger could read.
- [ ] The licence line distinguishes your work from the GPL-3.0 curriculum it follows.
- [ ] You sent the link to one person in the Code Crunch community and applied at least one thing they suggested.

## Stretch

- **Fail politely on a missing path argument.**

  ```python
  def parse_target(argv: list[str]) -> Path | None:
      """Return the --into path, or None for a rehearsal. Raise on a malformed flag."""
      if "--into" not in argv:
          return None
      position = argv.index("--into") + 1
      if position >= len(argv):
          raise SystemExit("usage: portfolio_scaffold.py [--into PATH]")
      return Path(argv[position]).expanduser()
  ```

  ```text
  usage: portfolio_scaffold.py [--into PATH]
  ```

  `SystemExit` with a string prints the message and exits with status `1`,
  which is exactly what a command-line tool should do with bad arguments — no
  traceback, because a traceback is for a bug in the program, not a mistake
  by the user.

- **Add the week's folder automatically.** Every week needs
  `frame-writeups/c2-week-NN/`. Take the week number as an argument and add
  that entry to the plan at run time. Then decide whether the audit should
  check for *all* weeks up to that number or only the current one, and
  defend the choice — it is a real design question with no obvious answer.

- **Report extra paths, not only missing ones.** An audit that only looks for
  what should be there cannot tell you about the stray `Untitled.md` you
  saved into the repository root at midnight. Walk the tree, subtract the
  plan, and report the difference. Then work out why you probably want that
  as a warning rather than an error.

- **Turn the audit into a Git pre-commit hook.** The exit code is already
  right, so this is mostly plumbing — and it converts a tool you remember to
  run into one you cannot forget.

When your portfolio repository is live, you have finished Week 1. Push, send
the link to one peer for review, then move on to
[Week 2 — Complexity and Hash Maps](../../week-02-complexity-and-hash-maps/).
