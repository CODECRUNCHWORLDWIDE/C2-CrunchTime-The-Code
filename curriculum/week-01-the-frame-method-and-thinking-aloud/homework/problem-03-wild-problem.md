# Problem 3 — A Problem You Have Never Seen

> **Topic:** running the whole FRAME method, out loud, on a problem nobody prepared you for
> **Lecture:** [02 — The FRAME Method](../lecture-notes/02-the-frame-method.md)
> **Difficulty:** Medium
> **Target time:** 90 minutes
> **Why this one:** every other problem this week came with a lecture attached. This one does not, and that is the whole point. Pattern recognition is only a skill if it works on something you have not been told the answer to. If you only ever solve problems you have already heard of, you are testing your memory and calling it preparation.

<!-- no-runnable-file: the problem is one the learner chooses from a practice site, so there is no answer this course could publish. What is graded is the recording and the FRAME write-up, and The Solution below is the model write-up rather than a program. -->

## The Brief

Pick **one** problem you have never seen before, from any free practice site,
tagged "Two Pointers" and marked Easy or Medium. Solve it with a full FRAME
pass, out loud, with a recorder running.

Three rules about the picking, and they matter more than the solving.

**It must be genuinely unfamiliar.** If you recognise the title, pick another.
If you recognise it three minutes in, say so on the recording and keep going —
that is honest and it is useful data — but pick a second one afterwards.

**Do not read anybody's solution first.** Not the editorial, not the
discussion tab, not a video. The moment you do, this exercise stops measuring
anything. If you are stuck at forty minutes, take a hint rather than a
solution: read only the problem's *tags*, or the first sentence of the top
comment, and note on the recording that you did.

**Write the tests yourself.** The judge's "accepted" is not the deliverable.
Your own test cases are, because choosing test cases is where Research
constraints gets paid off — the degenerate case, the no-solution case, and one
that punishes the obvious wrong approach.

What you hand in is a recording of at least fifteen minutes and a FRAME
write-up at `frame-writeups/c2-week-01/wild-01-<problem-slug>.md`, following
[`frame_template.md`](../exercises/frame_template.md).

The write-up has to answer two questions the drills never asked you:

- **How long did Assess options take?** Not how long the whole solve took —
  how long you spent between finishing Research constraints and committing to
  an approach.
- **Did you back out?** Did you name a pattern, start on it, and have to
  abandon it? If so, what was the signal that told you, and how long did it
  take you to notice?

Neither answer is meant to be flattering. Backing out is normal. Backing out
after twenty-five minutes instead of five is the thing to fix.

## Starter

There is no code starter, because the problem is yours to choose. What there
is instead is a script for the first ninety seconds, which is the part people
waste.

```text
[00:00]  Read the prompt out loud, slowly, all the way to the end.
         Do not skim to the examples. Do not start typing.

[00:30]  Say what the input is and what the output is, in your own words.
         "I'm given ___ , and I have to give back ___ ."

[00:50]  Say three things the prompt does NOT tell you, as questions.
         Can it be empty? Can it have duplicates? Is it sorted?

[01:10]  Work one small example by hand, out loud, with real values.
         Then work a second one that you expect to have no answer.

[01:30]  Only now say: "This looks like a ___ problem, because ___ ."
```

Set a timer for thirty minutes before you start. When it goes off, say the
time out loud on the recording and carry on — the timer is there to make the
pacing audible, not to stop you.

Copy [`frame_template.md`](../exercises/frame_template.md) into your portfolio
repo as `wild-01-<problem-slug>.md` and fill it in **after** the solve, from
the recording, not during it.

## Requirements

1. The problem is one you had never seen, from a free practice site, tagged
   two pointers, Easy or Medium.
2. A recording exists, at least fifteen minutes long. Any audio quality.
3. A FRAME write-up exists at
   `frame-writeups/c2-week-01/wild-01-<problem-slug>.md`, with all five
   sections filled in.
4. The write-up names the problem by title, number and link — and reproduces
   none of its text. Restate the problem in your own words.
5. Your solution passes your own tests, which you wrote, including a
   degenerate case and a no-solution case.
6. The write-up answers the two questions in the brief: how long Assess
   options took, and whether you backed out of an approach.
7. The write-up records at least one thing you would do differently.

## Constraints

- **Ninety minutes total, and thirty of them on the solve.** The rest is
  choosing the problem, writing your own tests, and writing it up. If the
  solve eats the whole ninety minutes you have learned something real about
  your pace, and the write-up still has to happen — do it shorter rather than
  not at all.

- **You may take a hint; you may not take a solution.** The line is: anything
  that tells you *which pattern* is fair, anything that tells you *the
  algorithm* is not. Note on the recording the moment you cross it either way.
  A candidate who takes a hint gracefully at the right time scores better than
  one who is silently stuck for ten minutes, and the same is true here.

- **Restate, never copy.** Your write-up describes the problem in your own
  words and links to the original. This is the same rule the course holds
  itself to — see [CONTENT-POLICY.md](../../../CONTENT-POLICY.md) — and the
  reason is the same: a repository you can publish, fork and print is only
  possible if everything in it is yours.

- **Write your own test cases before you look at the judge's.** The judge's
  visible examples are a sample, not a specification. Working out what the
  degenerate case is *yourself* is the part of Research constraints that
  transfers to interviews, where there is no judge at all.

## Expected output

There is no program here, so there is no captured run. What "done" looks like
is a write-up whose Examine section reads like this — this is from a solve of
a merge-two-sorted-inputs problem, and it is the shape to aim for rather than
a model answer to copy:

```text
E — Examine

Traced [10, 40, 40, 90] and [25, 40, 70] by hand. Output
[10, 25, 40, 40, 40, 70, 90]. The two primary 40s land before the secondary
one, which is what the <= in my comparison decides — I checked that by
flipping it to < and watching the order change.

Edge cases I ran: both empty -> []. One empty -> the other, unchanged. All
ties -> everything, in input order. Single element each -> two elements.

Bug I caught: my first version dropped the leftovers. The while loop ends as
soon as either input is exhausted, and I had no extend() after it. Found it
on the [10, 40, 40, 90] trace at 14 minutes, not from the judge.

Time O(m + n): every iteration advances exactly one pointer and neither ever
moves backward. Space O(m + n), all of it the output; O(1) auxiliary.

Assess options took 4 minutes. I considered concatenate-and-sort first
(O((m+n) log(m+n))) and rejected it because both inputs are already sorted
and that throws the ordering away and buys it back at a cost.

I did not back out. The two-sorted-inputs signal fired in about 20 seconds,
which is faster than exercise 1 and I think that is the drills working.
```

Notice what is in there: real values, a bug found by the candidate rather than
by the judge, a rejected alternative with a reason, and two honest numbers at
the end. Notice also what is *not* in there — no line of the original
problem's text.

## Steps

1. Open the practice site, filter to the two-pointer tag, Easy or Medium.
   Scroll until you find a title you do not recognise. Do not read the
   discussion tab. **Close every other tab.**
2. Start the recorder. Start a thirty-minute timer.
3. Run the ninety-second script above. Out loud, all of it, before typing.
4. Solve it. Narrate every step. When you get stuck, narrate being stuck —
   "I'm going to sit with this for a minute" is a sentence worth practising.
5. Before you submit to the judge, write your own tests and run them. Include
   the empty case, the no-solution case, and one case built to break the
   approach you nearly took.
6. Submit. If the judge rejects it, that is more useful than acceptance —
   note *what* it rejected on and whether your own tests could have caught it.
7. Stop the recorder. Listen back at 1.5× while you write the write-up.
8. Commit the write-up and your solution to
   `frame-writeups/c2-week-01/`.

## The Solution

There is no published answer here, because the problem is yours. What is
published instead is the model **write-up**, which is the deliverable this
problem is graded on. Copy this shape into
`frame-writeups/c2-week-01/wild-01-<problem-slug>.md`:

```markdown
# Wild problem 1 — <your one-sentence restatement>

> **Source:** [<Site> <number> · <Title>](<the problem URL>)
> **Attempted:** <date> · **Solve time:** <minutes> · **Recording:** <where it lives>

## F — Frame

- **Input:** <type, shape, what the values mean>
- **Output:** <type, format, and what comes back when there is no answer>
- **Restated:** <the problem in your own words, two sentences, no quotation>
- **Questions I would have asked an interviewer:**
  - <one about the input shape>
  - <one about ties or multiple answers>
  - <one about what "no answer" looks like>
- **Worked by hand:** `<input>` → `<output>`, because <reason>.
  And a case with no answer: `<input>` → `<output>`.

## R — Research constraints

- **Bounds:** <sizes and value ranges, and what each one rules out>
- **Edge cases I listed before coding:** <empty, single, all-equal, no-answer>
- **What makes this hard:** <one sentence — the thing that stops the obvious
  approach from working>

## A — Assess options

- **Simple approach:** <the obvious one>, costing <time> / <space>.
- **Considered and rejected:** <alternative>, because <reason>.
- **Chose:** <approach>, because <reason tied to the bounds above>.
- **Time spent on this step:** <minutes>.
- **Did I back out of anything?** <yes, and the signal that told me / no>

## M — Make the solution

    def solve(...):
        """<what it does>"""
        ...

(Indented four spaces here so this template can live inside a fenced block.
In your own file, use a normal fenced python block.)

## E — Examine

- **Traced:** <input> → <output>, showing the values that matter.
- **Edge cases run:** <each one, and what came back>
- **Bug I caught myself:** <what it was, how the trace surfaced it>
- **Time:** O(<n>) because <reason>. **Space:** O(<1 or n>) because <reason>.
- **Improvement I would make with more time:** <one thing>

## Self-feedback

- Pattern recognised in <seconds>.
- One thing I did well: <...>
- One thing to change next time: <...>
```

**The Source line is the whole of what crosses over from the original.**
Title, number, link. Everything under it is yours, written from your
understanding rather than from their page. If you cannot restate the problem
in two sentences without looking at it, you have not finished Frame — go back
and read it again rather than paraphrasing it in the write-up.

**The two questions in Assess options are the ones this problem exists to
ask.** Every drill this week told you the pattern in its title. Here nobody
did, so the time between "I know what the problem is" and "I know how I am
attacking it" is a real measurement of your pattern recognition. Write the
number down even when it embarrasses you — especially then, because the
number is what you compare against in Week 4.

**"Did I back out" has no wrong answer, only a wrong response.** Naming a
pattern, starting on it, and abandoning it is normal and happens to strong
candidates constantly. What separates them is *how fast the signal arrives*.
Usually it is a concrete thing — an example your approach cannot handle, a
loop with no obvious termination, a data structure you keep wanting and do not
have. Write down what the signal was, because next time you want to notice it
sooner.

**Examine is written from the recording, not from memory.** Listen back and
write down what you actually said. The gap between what you remember
explaining and what you actually explained is usually large, and closing it is
most of what this problem teaches.

## Download and run

There is no program to download for this one — the problem is one you choose,
so no answer ships with the course. Two things beside this page are worth
having open while you work:

- [`frame_template.md`](../exercises/frame_template.md) — copy it into your
  portfolio repo as `wild-01-<problem-slug>.md`.
- [`timed_runner.py`](../exercises/timed_runner.py) — the harness the drills
  use, if you want the same shape for your own test cases.

Check your own work by re-reading the write-up a day later and asking whether
you could re-derive the solution from it in sixty seconds. If not, the
write-up is not finished.

## Common bugs to catch

These are failures of process rather than of code, and every one of them has a
symptom you can catch in the moment.

- **You recognised the problem and kept going anyway.** Symptom: the recording
  is nine minutes long and you never asked a question. You measured your
  memory. Pick another problem; the first minute is the only expensive part.

- **You opened the discussion tab "just to check the constraints".** Symptom:
  you know the intended complexity before you have finished Frame. There is no
  way back from this within one problem, so name it on the recording and pick
  another. The rule is not moralism — the exercise simply stops producing data.

- **Silence.** Symptom: long stretches of the recording with nothing on them.
  This is the failure mode from
  [Lecture 1](../lecture-notes/01-what-interviewers-actually-score.md), and it
  is the one that costs real interviews. Practise the sentence "I'm going to
  sit with this for a moment and think about whether the input being sorted
  buys me anything" — narrating a pause is not the same as filling it.

- **You submitted to the judge before writing your own tests.** Symptom: your
  write-up's Examine section says "accepted" and nothing else. The judge tells
  you *that* something was wrong, never *what you failed to think of*. In an
  interview there is no judge, so the habit you need is the one where you
  produce the failing case yourself.

- **The write-up quotes the original problem.** Symptom: a paragraph in your
  write-up you could not have written without the tab open. Restate it, or
  link to it — those are the two options, and the second one is free.

- **The write-up was written during the solve.** Symptom: it reads perfectly
  and has no bug in it. You were composing prose instead of solving, and the
  narration on the recording will be thin as a result. Solve first, write
  afterwards.

- **Assess options is blank.** Symptom: the write-up jumps from constraints to
  code. You did have an alternative — everybody's first instinct on an array
  problem is a nested loop — you just did not say it out loud. Naming the
  approach you rejected is worth more than the one you took.

## Under the hood

<details>
<summary>Under the hood — why unfamiliar problems measure something different, and how to pick well</summary>

**What this problem measures that the drills cannot.**

The five exercises this week each told you the pattern in the page title.
That is deliberate — you cannot practise the *execution* of a method while
also being unsure what you are executing it on. But it means none of them
measured recognition, which is the skill that actually decides interviews.

The gap has a name in learning research: **transfer**. Knowing something in
the context you learned it is one thing; recognising it in a context nobody
labelled is a much harder and much more valuable thing. Every week of this
course ends with one problem that nobody labelled, for exactly this reason.

**How to pick a genuinely unfamiliar problem.**

Filter to the tag, sort by anything except popularity, and take the first
title you do not recognise. Popular problems are popular because they are in
everybody's list of favourites, which means you have very likely absorbed
their solutions second-hand from a video thumbnail or a comment you scrolled
past.

Avoid, this week, anything whose title contains "container", "palindrome",
"two sum", "remove duplicates" or "trapping" — those are the shapes the five
exercises and two challenges already drilled, so they would measure your
memory of *this course*.

**On taking hints.**

The interview version of this question is settled: a candidate who says "I've
been going down this path for five minutes and I don't think it's leading
anywhere — could you tell me if I'm in the right area?" scores better than one
who grinds silently for fifteen. Interviewers are not scoring independence,
they are scoring collaboration and judgement, and knowing when you are stuck
is judgement.

Alone at your desk the equivalent is reading only the tags. Give yourself a
rule before you start — "at forty minutes I read the tags, at sixty I stop and
write up what I have" — and follow it. A rule decided in advance is worth far
more than one negotiated with yourself at minute forty-one.

**Why "how long did Assess options take" is the number to track.**

Frame and Research constraints get faster with practice in a boring, linear
way. Make the solution gets faster as you write more Python. Assess options is
the one that improves in steps, because it depends on how many patterns you
have available and how strongly each one is cued.

Tracking it week by week gives you a curve. In Week 1 it might be six minutes
and end in the wrong pattern. By Week 8, with eight patterns drilled, it
should be under a minute on anything in your library — and, more usefully,
you should be able to say "this is none of the eight" quickly, which is
itself a skill.

</details>

## Acceptance checklist

- [ ] The problem was genuinely unfamiliar, from a free practice site, tagged two pointers, Easy or Medium.
- [ ] You did not read anybody's solution before or during the solve.
- [ ] A recording of at least fifteen minutes exists.
- [ ] `frame-writeups/c2-week-01/wild-01-<problem-slug>.md` exists, with all five FRAME sections filled in.
- [ ] The write-up links the problem by title, number and link, and quotes none of its text.
- [ ] You wrote your own tests — including the empty case, the no-solution case, and one built to break the approach you nearly took — and they pass.
- [ ] The write-up says how long Assess options took.
- [ ] The write-up says whether you backed out of an approach, and what the signal was.
- [ ] The write-up names one thing you would do differently.
- [ ] Committed to your portfolio repo with a message a stranger could read.

## Stretch

- **Do a second one, and time only the recognition.** Read the prompt, say the
  pattern out loud, stop the clock, and do not solve it. Ten problems like
  that take twenty minutes and drill the exact skill Assess options needs. Log
  the seconds for each; the list is more useful than any single number.

- **Solve one where the pattern does not apply.** Pick something tagged
  "sliding window" instead. Practise saying "this uses two indices and is
  *not* a two-pointer problem, because the answer is the span between them
  rather than a pair or a partition" — recognising a near-miss is worth as
  much as recognising a hit, and
  [Lecture 3](../lecture-notes/03-arrays-and-two-pointers.md) section 5 is
  built around exactly this confusion.

- **Hand your write-up to somebody who has not seen the problem** and ask them
  to reconstruct the algorithm from your Examine section alone, without
  reading your code. If they can, the write-up is strong. If they cannot, it
  is the explanation that needs work — and in the room, the explanation is
  what you are graded on.

Next: [Problem 4 — Behavioral Story](./problem-04-behavioral-story.md).
