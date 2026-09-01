# Problem 1 — Portfolio Setup

> **Topic:** getting the portfolio repo standing, and grading the one thing about it a reviewer really reads — the commit log
> **Lecture:** [01 — What Interviewers Actually Score](../lecture-notes/01-what-interviewers-actually-score.md)
> **Difficulty:** Easy
> **Target time:** 45 minutes
> **Why this one:** it is the [mini-project](../mini-project/README.md)'s prerequisite, so get it done Thursday. The repository itself is folders. What makes it worth showing anybody is fifteen weeks of commit messages that say what happened, and a commit message is easier to fix before you have written two hundred of them than after.

## The Brief

Create the public repository `crunchtime-interview-prep-<yourhandle>` and put
your first commit in it. The [mini-project](../mini-project/README.md) has the
full layout and a program that builds it; this problem is the half-hour that
gets the thing existing so that Thursday's deep work has somewhere to go.

Then the part you write code for.

A **commit subject** is the first line of a commit message — the bit that
shows up in `git log --oneline` and on GitHub's file list. It is the only part
most people ever read. A recruiter scrolling your history sees a column of
subjects and nothing else, and that column is either a record of a sustained
practice or a column of the word `wip`.

Write a small program that grades a list of commit subjects against four
rules. Each rule is something a reviewer would actually notice:

- **Says nothing.** The whole subject is a filler word — `wip`, `stuff`,
  `update`, `fix`, `changes`, `final`, `misc`. These are not messages; they
  are the absence of one.
- **Too short.** Under fifteen characters cannot describe a change. `Fix typo`
  is eight.
- **Too long.** Over seventy-two characters gets cut off in `git log --oneline`
  and in GitHub's list, so the end of your sentence is invisible where it
  matters most.
- **Trailing full stop.** A subject is a title, and titles do not take a full
  stop. This is a convention rather than a law, but it is a near-universal one
  and breaking it looks like carelessness rather than like a choice.

Report one verdict per commit, in log order, plus the share that would
survive.

## Starter

Save this as `problem-01-portfolio-setup.py` and fill in the `TODO`s.

```python
"""problem-01-portfolio-setup.py — grading your own commit log.

Four rules, applied to the subject line of every commit.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

VAGUE = {"wip", "stuff", "update", "updates", "fix", "fixes", "changes", "final", "misc"}

MIN_LENGTH = 15
MAX_LENGTH = 72


def judge_subject(subject: str) -> str:
    """Judge one commit subject line against the four rules.

    Args:
        subject: The first line of a commit message, as Git stores it.

    Returns:
        "ok", or the first rule it breaks, in the order the rules are
        checked. One reason per subject keeps the report readable.
    """
    # TODO: strip the subject first, then check the four rules in the order
    #       the brief lists them, returning the reason as a string
    # TODO: the vague check has to ignore case and a trailing "." or "!",
    #       because "WIP." is the same non-message as "wip"
    # TODO: every path returns a string. A function that falls off the end
    #       returns None, and None is not a verdict.
    ...


def audit_commit_subjects(subjects: list[str]) -> list[tuple[str, str]]:
    """Judge every commit subject, keeping the log's own order."""
    # TODO: one (subject, verdict) pair per subject
    ...


def pass_rate(findings: list[tuple[str, str]]) -> float:
    """Return the share of subjects judged "ok", as a percentage."""
    # TODO: an empty log scores 0.0 and must not divide by zero
    ...


# ---- Self-check ----
if __name__ == "__main__":
    print(judge_subject("wip"), "|", judge_subject("Add Week 1 exercise 1 FRAME write-up"))

    assert judge_subject("Fix typo") == "too short"
    assert judge_subject("Add Week 1 exercise 1 solution.") == "trailing full stop"
    assert pass_rate([]) == 0.0
    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-01-the-frame-method-and-thinking-aloud/homework/problem-01-portfolio-setup.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. A **public** GitHub repository named
   `crunchtime-interview-prep-<yourhandle>` exists, with at least one commit.
2. It has a `README.md`, a `.gitignore` and a `LICENSE`.
3. `judge_subject` returns exactly one of: `"ok"`, `"says nothing"`,
   `"too short"`, `"too long for one line"`, `"trailing full stop"`.
4. The rules are checked in the order the brief lists them, so a subject that
   breaks two gets the first reason.
5. The vague check ignores case and a trailing `.` or `!`.
6. `audit_commit_subjects` returns one pair per subject, in the input order.
7. `pass_rate` returns `0.0` on an empty log rather than raising.
8. Every function keeps its type hints and its docstring.

## Constraints

- **Fifteen characters is the short bound, and seventy-two is the long one.**
  Neither is arbitrary. Fifteen is about where a subject stops being a label
  and starts being a sentence — `Fix typo` is eight, `Add Week 1 exercise 1
  FRAME write-up` is thirty-six. Seventy-two is the width Git's own tooling
  assumes: `git log --oneline` prefixes seven characters of hash and a space,
  and eighty columns is still the terminal width almost every tool wraps at.

- **One reason per subject, and the order of the checks decides which.**
  Returning a list of every broken rule sounds more helpful and reads worse —
  a report where each line has one verdict can be skimmed, and a report where
  each line has a list cannot. Fixing the first problem usually surfaces the
  next one anyway.

- **The empty log scores `0.0`, not `100.0`.** A repository with no commits
  has not demonstrated anything, so "everything passed" would be a lie of the
  most flattering kind. It is also the case that would otherwise divide by
  zero, which is a nice reminder that the degenerate input and the arithmetic
  hazard are frequently the same input.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13:

```text
$ python problem-01-portfolio-setup-solution.py
BAD  Initial commit                                        too short
ok   Add .gitignore and CC-BY-4.0 licence                  ok
BAD  wip                                                   says nothing
ok   Add Week 1 exercise 1 FRAME write-up                  ok
ok   Add Week 1 exercise 1 solution: reverse the siding    ok
BAD  stuff                                                 says nothing
BAD  Fix the swap count in exercise 1 so a refused ord...  trailing full stop
ok   Add Week 1 exercise 2 FRAME write-up and solution     ok
BAD  Rewrite the portfolio cover so it answers all fiv...  too long for one line
ok   Add behavioral story 1: the overnight cache bug       ok

50% of 10 commits would survive a reviewer.
All checks passed.
```

Two lines are worth arguing with. `Initial commit` is what Git's own tooling
and half the tutorials on the internet suggest, and it is still too short —
what did the initial commit *contain*? And the seventh line is a perfectly
good sentence ruined by one character; that is the cheapest bug on this page
to fix and the easiest to keep making.

Fifty per cent is a realistic first-week score. The point of running this on
your own log is not the number, it is seeing which of the four rules you
personally break.

## Steps

1. Create the repository on GitHub, public. Clone it. Add a one-line
   `README.md`, a `.gitignore` and a `LICENSE`. Commit and push.
2. Save the starter and run it. `AssertionError`.
3. Write `judge_subject`. Strip the subject first, then check the four rules
   in order. Every branch returns a string.
4. Write `audit_commit_subjects` — one line, a comprehension over
   `judge_subject`.
5. Write `pass_rate`, empty-log guard first.
6. Run it. Then run it on your own log:
   `git log --format=%s --reverse` gives you exactly the list the function
   wants.
7. Fix the commits you have not pushed yet, and resolve to write the next
   fifty properly. Rewriting pushed history is not worth it for this.

## The Solution

```python
"""problem-01-portfolio-setup-solution.py — grading your own commit log.

The portfolio repo's value is its history, so the history is worth checking.
Four rules, each one a thing a reviewer would actually notice, applied to the
subject line of every commit.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

VAGUE = {"wip", "stuff", "update", "updates", "fix", "fixes", "changes", "final", "misc"}

MIN_LENGTH = 15
MAX_LENGTH = 72


def judge_subject(subject: str) -> str:
    """Judge one commit subject line against the four rules.

    Args:
        subject: The first line of a commit message, as Git stores it.

    Returns:
        "ok", or the first rule it breaks, in the order the rules are
        checked. One reason per subject keeps the report readable.
    """
    trimmed = subject.strip()
    if trimmed.lower().rstrip(".!") in VAGUE:
        return "says nothing"
    if len(trimmed) < MIN_LENGTH:
        return "too short"
    if len(trimmed) > MAX_LENGTH:
        return "too long for one line"
    if trimmed.endswith("."):
        return "trailing full stop"
    return "ok"


def audit_commit_subjects(subjects: list[str]) -> list[tuple[str, str]]:
    """Judge every commit subject, keeping the log's own order.

    Args:
        subjects: Commit subject lines, newest last, as `git log` prints
            them with --format=%s --reverse.

    Returns:
        One (subject, verdict) pair per subject, in the same order.
    """
    return [(subject, judge_subject(subject)) for subject in subjects]


def pass_rate(findings: list[tuple[str, str]]) -> float:
    """Return the share of subjects judged "ok", as a percentage.

    Args:
        findings: The output of audit_commit_subjects.

    Returns:
        A percentage from 0.0 to 100.0. An empty log scores 0.0, because a
        repository with no commits has not demonstrated anything.
    """
    if not findings:
        return 0.0
    good = sum(1 for _, verdict in findings if verdict == "ok")
    return good * 100 / len(findings)


# ---- Self-check ----
if __name__ == "__main__":
    LOG = [
        "Initial commit",
        "Add .gitignore and CC-BY-4.0 licence",
        "wip",
        "Add Week 1 exercise 1 FRAME write-up",
        "Add Week 1 exercise 1 solution: reverse the siding",
        "stuff",
        "Fix the swap count in exercise 1 so a refused order bills zero.",
        "Add Week 1 exercise 2 FRAME write-up and solution",
        "Rewrite the portfolio cover so it answers all five questions a recruiter asks before they scroll",
        "Add behavioral story 1: the overnight cache bug",
    ]

    findings = audit_commit_subjects(LOG)
    for subject, verdict in findings:
        flag = "ok " if verdict == "ok" else "BAD"
        shown = subject if len(subject) <= 52 else subject[:49] + "..."
        print(f"{flag}  {shown:<52}  {verdict}")

    print()
    print(f"{pass_rate(findings):.0f}% of {len(findings)} commits would survive a reviewer.")

    assert judge_subject("wip") == "says nothing"
    assert judge_subject("WIP.") == "says nothing"
    assert judge_subject("Fix typo") == "too short"
    assert judge_subject("x" * 80) == "too long for one line"
    assert judge_subject("Add Week 1 exercise 1 solution.") == "trailing full stop"
    assert judge_subject("Add Week 1 exercise 1 FRAME write-up") == "ok"
    assert audit_commit_subjects([]) == []
    assert pass_rate([]) == 0.0
    assert pass_rate([("a", "ok"), ("b", "too short")]) == 50.0
    print("All checks passed.")
```

**Early returns turn four rules into four lines.** Each check answers and
leaves. There is no `verdict` variable being reassigned, no `elif` ladder to
read backwards, and no way for two rules to both claim the subject. When you
have a series of independent tests that each produce a final answer, returning
from inside them is clearer than collecting a result and returning it at the
end.

**The order of the checks is the specification, not an accident.** `wip.` is
both "says nothing" and "trailing full stop". The rule that fires first is the
one that gets reported, so the order in the code has to be the order in the
brief. Write them in a different order and the program is still correct
against a different specification — which is the kind of drift that only shows
up when somebody else reads your report and disagrees with it.

**`.rstrip(".!")` before the vague lookup, and `.lower()` before that.**
`WIP.` and `Wip!` and `wip` are the same non-message. Normalising *then*
looking up is the general shape: make the input canonical, then compare
against canonical data. The alternative — putting `"WIP."`, `"Wip!"` and forty
other spellings into the set — is the version that stops working the day
somebody types `WIP ...`.

**A set, not a list, for `VAGUE`.** With nine words the speed difference is
nothing. The reason is that `in` on a set says "membership" and `in` on a list
says "search", and choosing the container that matches the question is a habit
worth having before it matters. Week 2 makes it matter.

**`pass_rate` guards the empty case before it divides.** `good * 100 / len(findings)`
raises `ZeroDivisionError` on an empty log, and the guard both prevents that
and states the more interesting fact: an empty log deserves `0.0`, not an
error and not `100.0`.

## Download and run

Download
[problem-01-portfolio-setup-solution.py](./problem-01-portfolio-setup-solution.py)
and run it:

```bash
python problem-01-portfolio-setup-solution.py
```

To point it at your own repository, feed it the real log:

```bash
git log --format=%s --reverse
```

## Common bugs to catch

- **`ZeroDivisionError: division by zero` on an empty log.**

  ```text
  Traceback (most recent call last):
      pass_rate([])
      return good * 100 / len(findings)
             ~~~~~~~~~~~^~~~~~~~~~~~~~~
  ZeroDivisionError: division by zero
  ```

  A brand-new repository has no commits, so this is not a hypothetical input —
  it is the first one your program will ever see.

- **A bare `AssertionError`, with `None` in the report.** `judge_subject` fell
  off the end without returning:

  ```text
      -> [('Add Week 1 exercise 1 FRAME write-up', None)]
  ```

  ```text
  Traceback (most recent call last):
      assert judge_subject("Add Week 1 exercise 1 FRAME write-up") == "ok"
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  You wrote the four failing branches and forgot the `return "ok"` at the
  bottom. Python hands back `None` from a function that runs off the end, and
  `None` prints happily in an f-string, so the report looks almost right.

- **`WIP.` reported as "trailing full stop".** You looked up the vague set
  without stripping the punctuation, so the first check missed and the fourth
  one caught it. Not an exception, and the verdict is even arguably true — it
  is just not the one the specification asks for.

- **Every subject reported as "too short".** You measured `subject` before
  stripping it, or you compared against the wrong bound. Print
  `len(trimmed)` for one subject and the answer is immediate.

- **The long subject passing.** `> MAX_LENGTH` versus `>= MAX_LENGTH`. Seventy-two
  characters is fine; seventy-three is not. Decide which the bound means and
  write it once.

## Under the hood

<details>
<summary>Under the hood — where the seventy-two comes from, and what a commit message is really for</summary>

**The fifty and the seventy-two.**

The widely-used convention is "subject under 50 characters, body wrapped at
72". Both numbers come from terminals. `git log` indents the body by four
spaces, so 72 + 4 fits inside 80 columns. And `git log --oneline` prefixes an
abbreviated hash, so a subject much past 50 starts colliding with the width of
a side-by-side terminal.

We use 72 as the hard bound rather than 50 because 50 is genuinely tight for a
learning repository, where `Add Week 1 exercise 3 FRAME write-up and solution`
is a perfectly good subject at 52 characters. Picking a bound you will
actually honour beats picking the canonical one and ignoring it.

**Why the subject is separate from the body at all.**

Git treats the first line specially: it is what `--oneline` shows, what GitHub
puts in the file list, what an email subject becomes when a patch is mailed.
The blank line after it is not decoration — it is the delimiter. A message
with no blank line after the first line has no body at all as far as Git is
concerned, and the whole thing becomes one very long subject.

```text
Add Week 1 exercise 3 solution: widest ballast pair

The tie-break is not really a tie-break — the widest pair is unique,
because two valid pairs of equal span force a third, wider pair to exist.
Proof is in the page's Under the hood block.
```

Subject says what. Body says why. The diff already says how.

**Imperative mood, and why it reads oddly at first.**

Git's own convention is "Add the thing", not "Added the thing" or "Adding the
thing". The reason is that Git generates messages in that voice —
`Merge branch 'x'`, `Revert "Add the thing"` — so an imperative subject reads
as an instruction the commit carries out. It is not a rule we check here,
because it is hard to check mechanically and easy to argue about. It is worth
adopting anyway.

**Why not just rewrite the bad history?**

You can. `git rebase -i` will let you reword anything you have not shared. The
reason to leave pushed commits alone is that rewriting them changes their
hashes, which breaks every link anybody has to them and forces a force-push.
For a personal portfolio repository nobody has forked yet, the cost is near
zero and you may as well tidy up. Learn the reflex on this repository, where
the stakes are nothing, so that you already have it when the stakes are a
shared branch.

</details>

## Acceptance checklist

- [ ] A public GitHub repository named `crunchtime-interview-prep-<yourhandle>` exists.
- [ ] It has `README.md`, `.gitignore` and `LICENSE`, and at least one commit.
- [ ] `python problem-01-portfolio-setup.py` prints `says nothing | ok`, then `All checks passed.`
- [ ] `judge_subject` returns a string on every path, including the passing one.
- [ ] The four rules are checked in the brief's order, and you can say which verdict `wip.` gets and why.
- [ ] `pass_rate([])` returns `0.0` without raising.
- [ ] You ran the auditor over your own `git log --format=%s --reverse` and read the result.
- [ ] Every function has type hints and a docstring.

## Stretch

- **Check the body, not just the subject.** A good commit message has a blank
  second line and a body wrapped at 72 columns.

  ```python
  def judge_message(message: str) -> list[str]:
      """Return every structural problem with a full commit message."""
      lines = message.splitlines()
      problems: list[str] = []
      if not lines:
          return ["empty message"]
      subject = judge_subject(lines[0])
      if subject != "ok":
          problems.append(f"subject: {subject}")
      if len(lines) > 1 and lines[1].strip():
          problems.append("no blank line after the subject")
      for number, line in enumerate(lines[2:], start=3):
          if len(line) > 72:
              problems.append(f"line {number} is {len(line)} characters")
      return problems
  ```

  On the message `"Fix typo\nsome body text"`:

  ```text
  ['subject: too short', 'no blank line after the subject']
  ```

  Note the return type changed from one string to a list, because a whole
  message really can have several independent problems while a subject
  usually has one. The specification changed, so the signature did.

- **Read the log yourself.** Use `subprocess.run(["git", "log", "--format=%s"], ...)`
  to fetch the subjects instead of pasting them. Then decide what your program
  should do when it is not inside a Git repository at all — an exception, an
  empty list, or a message?

- **Score a streak, not a rate.** How many commits in a row at the end of the
  log are `ok`? That number rewards fixing your habit going forward, which is
  the behaviour you actually want, rather than rewarding rewriting history.

Next: [Problem 2 — Narration Review](./problem-02-narration-review.md).
