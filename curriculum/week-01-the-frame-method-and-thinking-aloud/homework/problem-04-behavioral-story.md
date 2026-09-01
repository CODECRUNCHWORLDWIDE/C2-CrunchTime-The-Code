# Problem 4 — Behavioral Story

> **Topic:** the STAR format, and a program that checks a story has the shape before you check whether it is any good
> **Lecture:** [01 — What Interviewers Actually Score](../lecture-notes/01-what-interviewers-actually-score.md)
> **Difficulty:** Easy
> **Target time:** 45 minutes
> **Why this one:** the course does not cover behavioral properly until Week 13, and that is exactly why the story bank starts now. A story you wrote in Week 1 and reread nine times is worth more than four stories written the week before an onsite. Spaced repetition is the whole argument.

## The Brief

Write one behavioral story, in STAR format, answering the question **"Tell me
about a time you debugged a hard problem."**

**STAR** is four sections, and each one answers a different question:

- **Situation** — where were you, and what was going on? Two or three
  sentences of context, no more. The listener needs enough to follow you and
  nothing else.
- **Task** — what were *you* responsible for? Not the team. You. This is the
  section people skip, and skipping it is why so many stories leave the
  listener unsure what the speaker actually did.
- **Action** — what did you do, step by step? This is the longest section and
  it is the one being graded. Concrete verbs, in order.
- **Result** — what happened? A number if you have one. What you learned if
  you do not.

Then write a program that checks the story's **shape** — not its quality, its
shape. Four headings, present, in that order, none of them empty, and a total
between two hundred and four hundred words.

Why bother with a program for something you could check by eye? Because by
Week 13 you will have twelve of these, written over three months, and the one
you dash off at midnight in Week 9 will be missing its Task section. Structure
is exactly the kind of thing that is boring to check and expensive to get
wrong, which is the definition of something to automate.

## Starter

Save this as `problem-04-behavioral-story.py` and fill in the `TODO`s.

```python
"""problem-04-behavioral-story.py — checking a STAR story's shape.

Four headings, in order, none of them empty, and a length somebody will sit
through.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

STAR = ["Situation", "Task", "Action", "Result"]
MIN_WORDS = 200
MAX_WORDS = 400


def split_sections(story: str) -> dict[str, str]:
    """Split a Markdown story into its `## Heading` sections."""
    # TODO: walk the lines. A line starting "## " opens a new section; every
    #       other line belongs to the section currently open.
    # TODO: text before the FIRST "## " heading is discarded
    # TODO: do not forget to store the last section when the lines run out
    ...


def word_count(story: str) -> int:
    """Count words in the story's section bodies, ignoring headings."""
    # TODO: sum the words under the headings. The headings are structure,
    #       not story, so they do not count.
    ...


def check_story(story: str) -> list[tuple[str, bool, str]]:
    """Run every structural check over a STAR story."""
    # TODO: four checks, in this order, each a (name, passed, detail) triple:
    #       all four headings present / in STAR order / none empty / in budget
    # TODO: never index a section that might be missing — the first check
    #       exists precisely because it can be
    ...


# ---- Self-check ----
if __name__ == "__main__":
    stub = "## Situation\n\n## Task\nx\n## Action\ny\n## Result\nz"
    for name, passed, detail in check_story(stub):
        print(f"{'pass' if passed else 'FAIL'}  {name}  {detail}")

    assert split_sections("## Task\nhello") == {"Task": "hello"}
    assert word_count("# Title only") == 0
    assert check_story(stub)[2][1] is False
    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-01-the-frame-method-and-thinking-aloud/homework/problem-04-behavioral-story.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `behavioral/story-01.md` exists in your portfolio repo, in STAR format,
   answering the debugging question.
2. The story is between 200 and 400 words, counted under the headings.
3. You read it aloud at least twice and rewrote every sentence that did not
   sound natural.
4. `split_sections` returns a dict from heading text to body, discarding
   anything before the first `## ` heading.
5. `word_count` counts only the section bodies, never the heading lines.
6. `check_story` returns four `(name, passed, detail)` triples, always in the
   same order, whatever is wrong with the story.
7. `check_story` never raises on a malformed story — a missing section is a
   failed check, not a crash.
8. Every function keeps its type hints and its docstring.

## Constraints

- **Two hundred to four hundred words.** Under two hundred and the Action
  section cannot hold enough detail to show what you did — the answer becomes
  a summary of a story rather than the story. Over four hundred and you are
  speaking for more than three minutes, which in an interview is long enough
  for the listener to lose the thread and long enough that you have crowded
  out their follow-up questions. Both bounds are about the *listener*, not
  about you.

- **The headings are structure and are not counted.** Otherwise a story
  scrapes past the lower bound on the strength of the word "Situation". More
  generally: when you measure something, be precise about which part you are
  measuring, because the part you accidentally include is the part that gets
  gamed.

- **`check_story` reports, it never raises.** A checker that crashes on the
  input it was written to catch is useless. The first check exists because a
  section can be missing, so nothing after it may assume the section is there.
  This is a real constraint on how you write the other three checks, not
  advice.

- **The four results always come back in the same order.** A report you can
  compare between runs is worth much more than one you have to read
  carefully every time. Same order, always, even when the first check failed.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13:

```text
$ python problem-04-behavioral-story-solution.py
pass  four headings present     all four
pass  headings in STAR order    Situation then Task then Action then Result
pass  no empty section          all four have text
pass  200-400 words             260 words
All checks passed.
```

Run it against a story with a missing Task section and the shape of the report
does not change — only the verdicts do:

```text
FAIL  four headings present     missing ['Task']
FAIL  headings in STAR order    Situation then Action then Result
pass  no empty section          all four have text
FAIL  200-400 words             140 words
```

Note the third line still says `pass`. Every section that *is* present has
text in it, which is true and is what the check was asked. A check that
reported `FAIL` there — on the grounds that something else was wrong — would
be answering a question nobody asked, and would make the report harder to act
on rather than easier.

## Steps

1. Pick your story before you write any code. Twenty of your forty-five
   minutes belong to the writing.
2. Do not reach for the most impressive bug you have ever fixed. Reach for one
   you remember clearly enough to say what you tried *and what did not work*.
   The failed attempt is the part that makes a debugging story a debugging
   story.
3. Write it in `behavioral/story-01.md` with the four `## ` headings.
4. Read it aloud. Mark every sentence you stumbled on and rewrite it. Read it
   aloud again.
5. Save the starter and run it. `AssertionError`.
6. Write `split_sections` first. The pattern is: a `heading` variable holding
   the current section name and a `body` list collecting lines. When a new
   heading arrives, store what you have and start over. **When the loop ends,
   store the last one** — this is the bug everybody writes.
7. Write `word_count` on top of `split_sections`.
8. Write `check_story`. Four checks, in order, each one building a triple.
   Never index a section without knowing it is there.
9. Run it on your own story. Fix whichever check fails.

## The Solution

```python
"""problem-04-behavioral-story-solution.py — checking a STAR story's shape.

A behavioural story is graded on structure before it is graded on content, so
the structure is worth checking mechanically: four headings, in order, none of
them empty, and a length somebody will sit through.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

STAR = ["Situation", "Task", "Action", "Result"]
MIN_WORDS = 200
MAX_WORDS = 400


def split_sections(story: str) -> dict[str, str]:
    """Split a Markdown story into its `## Heading` sections.

    Args:
        story: The story file's text. Headings are `## ` lines.

    Returns:
        A dict from heading text to the body under it. Text before the first
        `## ` heading is discarded, because a STAR story's content lives
        under its headings.
    """
    sections: dict[str, str] = {}
    heading = None
    body: list[str] = []
    for line in story.splitlines():
        if line.startswith("## "):
            if heading is not None:
                sections[heading] = "\n".join(body).strip()
            heading = line[3:].strip()
            body = []
        elif heading is not None:
            body.append(line)
    if heading is not None:
        sections[heading] = "\n".join(body).strip()
    return sections


def word_count(story: str) -> int:
    """Count words in the story's section bodies, ignoring headings.

    Args:
        story: The story file's text.

    Returns:
        How many whitespace-separated words sit under the headings. The
        headings themselves are structure, not story, so they do not count.
    """
    return sum(len(body.split()) for body in split_sections(story).values())


def check_story(story: str) -> list[tuple[str, bool, str]]:
    """Run every structural check over a STAR story.

    Args:
        story: The story file's text.

    Returns:
        One (check name, passed, detail) triple per check, in a fixed order:
        the four headings present, the headings in STAR order, no empty
        section, and the word count inside its budget.
    """
    sections = split_sections(story)
    found = [name for name in sections if name in STAR]
    results: list[tuple[str, bool, str]] = []

    missing = [name for name in STAR if name not in sections]
    results.append(("four headings present", not missing, f"missing {missing}" if missing else "all four"))

    results.append(("headings in STAR order", found == STAR, " then ".join(found) if found else "none found"))

    empty = [name for name in STAR if name in sections and not sections[name]]
    results.append(("no empty section", not empty, f"empty {empty}" if empty else "all four have text"))

    count = word_count(story)
    in_budget = MIN_WORDS <= count <= MAX_WORDS
    results.append((f"{MIN_WORDS}-{MAX_WORDS} words", in_budget, f"{count} words"))

    return results


# ---- Self-check ----
if __name__ == "__main__":
    # Built by joining, not as one triple-quoted block, so that no line of
    # this file begins with "## " at column 0 - a heading marker in column 0
    # inside a code block confuses tools that scan Markdown for sections.
    STORY = "\n\n".join(
        [
            "# Story 1 - a hard bug I debugged",
            "## Situation",
            "word " * 60,
            "## Task",
            "word " * 60,
            "## Action",
            "word " * 80,
            "## Result",
            "word " * 60,
        ]
    )

    for name, passed, detail in check_story(STORY):
        print(f"{'pass' if passed else 'FAIL'}  {name:<24}  {detail}")

    assert split_sections("## Task\nhello") == {"Task": "hello"}
    assert split_sections("no headings here") == {}
    assert word_count("## Task\none two three") == 3
    assert word_count("# Title only") == 0

    checks = check_story(STORY)
    assert [passed for _, passed, _ in checks] == [True, True, True, True]

    out_of_order = "## Task\nx\n## Situation\ny\n## Action\nz\n## Result\nw"
    assert check_story(out_of_order)[1][1] is False

    stub = "## Situation\n\n## Task\nx\n## Action\ny\n## Result\nz"
    assert check_story(stub)[2][1] is False
    assert check_story(stub)[3][1] is False
    print("All checks passed.")
```

**`split_sections` is a small state machine, and the state is `heading`.**
While `heading` is `None` you are before the first section, so lines are
thrown away — that is what discards the `# Story 1` title. Once a heading has
been seen, every non-heading line joins the current body. When a new heading
arrives, the previous body is stored and the collector resets.

**The line after the loop is the whole bug everybody writes.** The last
section is only stored when the *next* heading arrives, and for the last
section there is no next heading. So `sections[heading] = ...` has to happen
once more after the loop ends. Leave it out and the Result section vanishes,
which the "four headings present" check then reports as missing — a confusing
symptom for a bug that has nothing to do with the heading.

**Order is checked by comparing lists, not by walking indexes.**
`found == STAR` is one expression and it says the whole rule: the STAR
headings, in this order, and no fifth one interleaved. Note that `found` is
built by filtering `sections` — and dicts in Python 3.7 and later keep their
insertion order, so `found` really is the order the headings appeared in the
file. That guarantee is what makes the one-line comparison legitimate rather
than lucky.

**Every check is written so that it cannot raise on a missing section.** The
"present" check uses `not in`. The "order" check builds `found` from what is
actually there. The "empty" check has `name in sections and` before it touches
`sections[name]`. That last `and` is doing real work: without it, a story
missing its Task section raises `KeyError: 'Task'` from the checker whose
entire job is to tell you the Task section is missing.

**The detail string is what makes the report usable.** `missing ['Task']` and
`140 words` tell you what to do; `False` does not. Whenever you write a check
that can fail, ask what the person reading the failure needs to know, and
return that alongside the verdict.

**`word_count` reuses `split_sections` instead of re-splitting.** It costs a
second pass over a four-hundred-word string, which is nothing, and it means
there is exactly one definition in the program of what a section is. When two
functions both claim to know how to parse a file, one of them is eventually
wrong.

## Download and run

Download
[problem-04-behavioral-story-solution.py](./problem-04-behavioral-story-solution.py)
and run it:

```bash
python problem-04-behavioral-story-solution.py
```

To check your own story, read the file in and pass the text to `check_story`:

```python
from pathlib import Path
for name, passed, detail in check_story(Path("behavioral/story-01.md").read_text(encoding="utf-8")):
    print(f"{'pass' if passed else 'FAIL'}  {name:<24}  {detail}")
```

## Common bugs to catch

- **`KeyError: 'Task'` from the checker itself.** You read a section without
  checking it was there:

  ```text
  Traceback (most recent call last):
      check("## Situation\nx")
      return [n for n in STAR if not sections[n]]
                                   ~~~~~~~~^^^
  KeyError: 'Task'
  ```

  The checker crashed on precisely the input it exists to diagnose. Guard with
  `name in sections and ...`, or use `sections.get(name, "")`.

- **The Result section is always missing.** No exception. You stored each
  section when the next heading arrived and forgot to store the last one after
  the loop. Every story you check will report `missing ['Result']`, whatever
  is in it, which is a good clue: a checker that is wrong about *every* input
  is broken in the checker, not in the input.

- **A bare `AssertionError` on the word count.** You counted the whole file
  instead of the bodies:

  ```text
      headings counted too -> 7
  ```

  ```text
  Traceback (most recent call last):
      assert word_count(story) == 3
           ^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  On `"## Situation\none two\n## Task\nthree"` the bodies hold three words and
  the whole file holds seven — the four extra are `##`, `Situation`, `##` and
  `Task`. Four words of free credit per story is enough to push a thin story
  over a bound.

- **`## Situation` and `##Situation` treated the same.** They are not.
  `line.startswith("## ")` requires the space, which is correct Markdown and
  also correct here — but it means a heading typed without the space is
  silently treated as body text. Whether that should be an error is a real
  design question; decide it rather than discovering it.

- **The title counted as a section.** `# Story 1` starts with `#` but not with
  `## `, so it is skipped. If you tested `line.startswith("#")` instead, your
  dict gains a `Story 1` entry, `found` is unaffected because it filters to
  STAR names, and the word count is quietly wrong. A bug that only shows up in
  one of three outputs is the kind worth having a test for.

- **An empty section reported as present.** It *is* present — that is why
  these are two separate checks rather than one. Resist merging them; the
  report is more useful when each line answers exactly one question.

## Under the hood

<details>
<summary>Under the hood — why STAR works, and what a state machine is</summary>

**Why the format helps rather than constrains.**

Under pressure, people telling a work story drift. They give three minutes of
setup, mention the interesting part in one clause, and finish with "and yeah,
we fixed it." The interviewer learns nothing about what the *candidate* did,
because the story never separated the speaker from the team.

STAR forces the separation. Task is a section on its own precisely so that you
have to say what you were responsible for, out loud, before you describe what
was done. Action is the longest section because it is the one being graded.
Result exists so the story has an ending rather than a stop.

The format is not the point. The discipline is. Once you have written six of
these you will stop needing the headings, and the shape will still be there.

**On picking a story.**

Reach for one you remember in detail, not the most impressive one. A
debugging story is graded on the *process* — what you observed, what you
hypothesised, what you tried, what ruled things out. A story about a
catastrophic outage you fixed by luck teaches the listener nothing about how
you think.

The single most valuable ingredient is a wrong turn. "I assumed it was the
database, spent an hour there, and the thing that changed my mind was noticing
the errors only happened on one host" is a better answer than a straight line
to the fix, because interviews are trying to find out how you behave when you
are wrong, which is most of engineering.

**You just wrote a state machine.**

`split_sections` holds one piece of state — which heading is currently open —
and every line either changes that state or is consumed by it. That is a
**state machine**, and it is the standard shape for parsing anything
line-oriented: log files, config files, `.ini` files, Markdown.

The three parts are always the same, and the third is always the one people
forget:

1. Something that changes state (a heading line).
2. Something consumed in the current state (a body line).
3. **Flushing whatever is still open when the input ends.**

Anywhere you accumulate items and emit them on a boundary, ask what happens to
the last group. There is no boundary after it.

**Why the checks are data rather than prints.**

`check_story` returns triples instead of printing them. That means the same
function can drive a terminal report, a table in a web page, an exit code for
a Git hook, or a test. A function that prints can only ever do one of those.

Separating *deciding* from *displaying* is one of the highest-value habits
there is, and it costs nothing at the time — you write `return results`
instead of `print(...)`, and the caller does the formatting.

</details>

## Acceptance checklist

- [ ] `behavioral/story-01.md` exists in your portfolio repo, answering the debugging question in STAR format.
- [ ] The story is between 200 and 400 words, counted under the headings.
- [ ] The Action section is the longest of the four.
- [ ] The story contains at least one thing you tried that did not work.
- [ ] You read it aloud twice and rewrote every sentence you stumbled on.
- [ ] `python problem-04-behavioral-story.py` prints four report lines, then `All checks passed.`
- [ ] `split_sections` stores the last section after the loop ends.
- [ ] `check_story` does not raise on a story with a section missing.
- [ ] The four checks always come back in the same order.
- [ ] You ran the checker against your own story and it passes all four.
- [ ] Every function has type hints and a docstring.

Do not have a great story yet? Use a small one. Behavioral practice is about
*structure*, not heroism, and refining a small story is more valuable than
telling a large one badly.

## Stretch

- **Warn about the balance, not just the total.**

  ```python
  def section_balance(story: str) -> list[tuple[str, int]]:
      """Return each STAR section's word count, in STAR order."""
      sections = split_sections(story)
      return [(name, len(sections.get(name, "").split())) for name in STAR]
  ```

  ```text
  [('Situation', 60), ('Task', 60), ('Action', 80), ('Result', 60)]
  ```

  Then add a check: Action should be the longest section. Most weak stories
  fail that one, and it is a far better signal than the total word count —
  a four-hundred-word story with a sixty-word Action is a four-hundred-word
  story about somebody else.

- **Check a whole folder of stories at once.** By Week 13 you will have
  twelve. Walk `behavioral/`, run `check_story` on each, and print one line
  per story with the number of checks it passed. Then make it exit non-zero
  when any story fails, so it can run as a Git hook.

- **Count the sentences that start with "we".** A story where most Action
  sentences begin with "we" is a story about a team. Interviewers notice. So
  should your checker — though decide carefully what threshold is fair, since
  some "we" is honest and a story with none is suspicious in the other
  direction.

Next: [Problem 5 — System-Design Warm-Up](./problem-05-system-design-warmup.md).
