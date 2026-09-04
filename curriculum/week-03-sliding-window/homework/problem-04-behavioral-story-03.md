# Problem 4 — Behavioral Story 3

<!-- no-runnable-file: this problem's deliverable is a written and spoken story about your own experience, not a program -->

> **Topic:** the STAR story, aimed at the one question this week has been preparing you to answer
> **Lecture:** [01 — The Sliding Window Pattern](../lecture-notes/01-the-sliding-window-pattern.md)
> **Difficulty:** Easy
> **Target time:** 45 minutes
> **Why this one:** the story bank continues, and this week's topic hands you the right story. Recognising that two problems share a shape, and reusing the solution, is *exactly* what pattern matching is — and it is a thing you have done at work or in a project, whether or not you have ever called it that. Interviewers ask about it because it is the cheapest available proxy for whether someone gets faster over time.

## The Brief

Every technical interview has a second half where nobody asks you to write
code. They ask what you have done. Those answers are scored, they are scored
against a rubric, and the rubric rewards structure.

The structure is **STAR**, and it is four parts:

- **Situation.** Where you were and what was going on. Two or three sentences,
  no more. This is scene-setting, not the story.
- **Task.** What you specifically were responsible for. Not the team — you.
  This is the part people skip, and skipping it makes the whole story vague.
- **Action.** What you actually did, step by step, in the first person. This is
  the longest part and it should be at least half the words.
- **Result.** What changed. A number if you have one; a concrete outcome if you
  do not.

**Your question this week:**

> *"Tell me about a time you noticed a pattern across multiple problems and
> applied it."*

That question is not really about patterns. It is about whether you build
reusable understanding or start from scratch every time, which is the single
biggest difference between an engineer who gets faster over five years and one
who does not.

You have material. It does not have to be algorithms — in fact it is often
better if it is not. Three shapes that work:

- **A repeated bug.** You fixed the same class of failure three times in
  different places, noticed it was one problem, and fixed the cause instead of
  the symptoms.
- **A copy-pasted routine.** You spotted the same fifteen lines in four files,
  understood what actually varied between them, and turned the variation into a
  parameter.
- **A process, not code.** Every deployment failed the same way. Every new
  starter asked the same three questions. You saw the shape and changed the
  system rather than handling each instance.

This week's drills are themselves a legitimate source, and Exercise 5 is the
clearest one: the at-most-K template solved five problems that arrive wearing
different costumes. If you use it, be honest that it is coursework — an
interviewer respects "I noticed this while studying" far more than a vague
industrial anecdote that turns out to be thin under one follow-up question.

**Your job.** Write one STAR story, 200 to 400 words, and read it aloud twice.

The reading aloud is not optional and it is not a formality. Written prose and
spoken prose fail differently: sentences that scan fine on a page turn into
seventeen-word tangles in your mouth, and you only find out by using your mouth.

## Starter

Create `behavioral/story-03.md` in your portfolio repo and paste this in. Fill
in every `TODO`.

```markdown
# Story 3 — Noticing a pattern across problems

**Question:** "Tell me about a time you noticed a pattern across multiple
problems and applied it."

**One-line summary:** TODO — the whole story in one sentence, so you can find
it later without re-reading it.

## Situation

TODO — two or three sentences. Where, when, what was going on. Enough context
that the rest makes sense, and not one word more.

## Task

TODO — what *you* were responsible for. First person, singular. If this
paragraph says "we", rewrite it until it says "I".

## Action

TODO — the longest section, at least half your words. What you noticed, how
you noticed it, what you did about it, and in what order. Include the moment
of recognition explicitly: what made you realise these were the same problem
rather than three different ones?

TODO — and include one thing that did not go smoothly. A story with no
friction in it reads as rehearsed.

## Result

TODO — what changed. A number if you have one. If you do not have a number,
a concrete before-and-after: what used to take a day, what happens now, what
somebody else can now do without you.

## Notes to self

- Read aloud on: TODO (date), TODO (date)
- Spoken length: TODO — aim for 90 seconds to 2 minutes
- Weakest sentence when read aloud: TODO
- Follow-up I would struggle with: TODO
```

There is no code on this page and no `-solution.py` beside it, because the
deliverable is a story about your own experience. Nobody can publish that for
you. The starter above is the closest thing to a stub a written deliverable
has: a shape with the thinking removed.

## Requirements

1. A file `behavioral/story-03.md` exists in your portfolio repo.
2. It answers the question above, not a nearby one.
3. It uses all four STAR headings, in order.
4. It is between 200 and 400 words, excluding the notes section.
5. The Action section is at least half the word count.
6. The Task section says "I", not "we".
7. It names the moment of recognition explicitly — what made you see one
   problem instead of several.
8. It includes at least one thing that did not go smoothly.
9. It ends with a Result containing either a number or a concrete
   before-and-after.
10. You have read it aloud at least twice, and the notes section records the
    dates and the spoken length.

## Constraints

- **200 to 400 words.** Under 200 and there is not enough detail for a follow-up
  question to land anywhere; the interviewer has to interrogate you to get the
  story, which reads as reluctance. Over 400 and you are talking for more than
  two minutes without a breath, which is where interviewers stop listening and
  start waiting. The band is chosen to match the 90-second-to-2-minute spoken
  target, at ordinary speaking pace.

- **The Action section is at least half of it.** This is where the evidence
  lives. A story that spends 300 words on Situation and 40 on Action has told
  the interviewer about a context, not about you. If your Action is thin, you
  probably picked a story where you were a bystander — pick another.

- **First person, singular, in Task and Action.** Not because your team did not
  matter, but because the interview is assessing you and "we" makes your
  contribution unrecoverable. Say what the team did in Situation if you need
  to, then say what you did.

- **One thing that did not go smoothly.** A frictionless story is either
  untrue or uninteresting, and experienced interviewers treat it as a signal to
  probe harder. Naming the snag yourself is both more credible and, in
  practice, a much more comfortable conversation.

- **Read aloud, twice, on two different occasions.** The second reading catches
  what the first one made you tolerate. This is the constraint people skip and
  it is the one that most changes the delivery.

## Expected output

There is no program here, so there is no captured run. What "done" looks like
is a story that survives being spoken. Record yourself once and check it
against this:

```text
$ wc -w behavioral/story-03.md
     312 behavioral/story-03.md

spoken length          : 1m 47s
Action share of words  : 58%
"we" in Task section   : 0
snag named             : yes
Result contains        : "from about 40 minutes a release to under 5"
```

The last line is what a good Result looks like: specific, checkable, and
comprehensible to somebody who knows nothing about your codebase. "It improved
things considerably" is not a result, it is a feeling about a result.

## Steps

1. Spend ten minutes on candidates, not one. Write down three situations where
   you noticed a repeat. Do not evaluate them yet — the third one is often the
   best, and you will not reach it if you commit to the first.
2. Pick the one where your Action section will be longest. That is the
   selection rule; everything else is secondary.
3. Write Situation and Task in five minutes, deliberately fast. They should be
   short and they are not where the value is.
4. Write Action slowly. Include the moment of recognition as its own sentence —
   *"the third time I wrote the same guard, I went back and looked at the other
   two"* — because that sentence is what the question is actually asking about.
5. Add the snag. One or two sentences. What you tried that did not work, or
   what the abstraction got wrong at first.
6. Write Result last, and go and look up a real number if one exists. Ten
   minutes in a commit log or a dashboard is worth more than any amount of
   rewriting.
7. Read it aloud. Time it. Mark every sentence you stumbled on.
8. Fix the stumbles by cutting, not by rewording. Long sentences are the cause;
   shorter ones are the fix.
9. Read it aloud again the next day and fill in the notes section.

## The Solution

There is no published answer here, because the answer is your own experience
and nobody else can write it. What can be published is the standard the story
is held to — so here is the same rubric an interviewer uses, turned into
something you can grade yourself against.

```text
Grade your own draft, honestly, on five axes:

1. Specificity      Could a stranger picture the situation? Are there real
                    names for real things — a system, a file, a process — or
                    only categories like "the codebase" and "the team"?

2. Ownership        Does the Task section say what YOU were responsible for?
                    Count the "we"s. In Task and Action, the target is zero.

3. Recognition      Is there a sentence that says how you noticed? Not that
                    you noticed — how. This is the question being asked and
                    it is the sentence most drafts are missing.

4. Friction         Is there one thing that did not work? A story with no
                    snag invites the interviewer to go looking for one.

5. Result           Is there a number, or a concrete before-and-after that
                    someone outside your team could understand?
```

**Why the recognition sentence is the graded one.** The question is "tell me
about a time you noticed a pattern", and most answers describe the pattern and
skip the noticing. But the noticing is the skill. Anyone can apply a template
they were handed; the interesting claim is that you *derived* one from
instances. So the story needs a specific trigger: the third repetition, the
code review comment, the moment you went to write something and recognised your
own handwriting. One sentence, and it carries the whole answer.

**Why Situation should be short.** Most people over-invest here because it is
the easiest part to write. It is also the part the interviewer cares least
about — they need just enough context to follow the Action, and every extra
sentence is a sentence not spent on evidence about you. Three sentences is
usually plenty; five is almost always too many.

**Why the snag makes the story stronger, not weaker.** Two reasons. It is more
credible, because real work has friction and experienced interviewers know it.
And it gives you control of the follow-up: an interviewer who was going to
probe for weakness now finds you already went there, and the conversation moves
on to what you learned rather than what you are hiding.

**Why the Result needs a number.** Not because numbers are impressive, but
because they are *checkable*, and checkability is what separates a claim from
an impression. "Faster" is an impression. "From about forty minutes a release
to under five" is a claim you are visibly willing to be asked about. If you
genuinely have no number, a concrete before-and-after does the same job:
somebody else can now do it without you; the failure has not recurred in six
months.

**On reading it aloud.** Written English tolerates subordinate clauses that
spoken English does not. The test is simple: if you run out of breath, the
sentence is too long. Cut it into two. Do that three or four times and the
whole story gets easier to say, which makes you sound more comfortable, which
is itself part of what is being scored.

## Run it

There is no file to download and nothing to run, so the sibling `.py` that
every other page in this week ships does not exist here. The page declares that
exemption on its own line, near the top, which is how the course's test knows
this is deliberate rather than missing.

Your equivalent of running it is reading it aloud with a timer:

```bash
wc -w behavioral/story-03.md
```

Then read, and time yourself. Between 200 and 400 words should land between 90
seconds and two minutes. If it does not, the problem is usually that you are
reading rather than telling — which is worth knowing before an interview rather
than during one.

## Common bugs to catch

- **The story answers a different question.** You told a good story about
  debugging, or about a difficult colleague, and it does not mention noticing a
  repeat. Interviewers do not usually stop you; they mark it down and move on.
  Re-read the question after your draft and check it word by word.

- **Situation is half the story.** The commonest structural failure. Count the
  words in each section; if Action is not the largest, you have written a
  context and not an answer.

- **"We" everywhere in Action.** Now nobody knows what you did. Rewrite each
  sentence with "I" and see which ones you cannot honestly convert — those are
  the sentences telling you this might be the wrong story.

- **No recognition sentence.** You described the pattern and never said how you
  spotted it. This is the single most common omission and it is the one the
  question was aimed at.

- **A Result with no evidence.** "It made things much better" tells the
  interviewer nothing they can follow up on, and a claim nobody can check is a
  claim nobody credits.

- **Never read aloud.** You will find out in the interview which sentences do
  not survive being spoken. That is an expensive place to find out.

- **The story is 900 words.** You wrote an essay. Cut Situation first, then
  every sentence in Action that does not describe a decision you made.

## Under the hood

<details>
<summary>Under the hood — why behavioral answers are structured at all, and what a bar-raiser is listening for</summary>

**STAR exists because unstructured answers are not comparable.**

An interviewer is not really assessing whether your story is impressive. They
are filling in a rubric, and the rubric has rows for things like ownership,
impact and self-awareness. A rambling answer might contain evidence for all
three, but the interviewer has to go hunting for it while also listening, and
what does not get found does not get scored.

STAR is a courtesy to the person marking. It puts each kind of evidence in a
predictable place. That is the whole mechanism, and understanding it explains
the rules: Task exists so ownership has somewhere to live, Result exists so
impact does, and the snag exists so self-awareness does.

**What follow-up questions are for.**

A prepared story is expected. Everybody has them, and nobody is fooled. What
distinguishes candidates is the second and third question, which are
deliberately outside the rehearsed script:

- *"What would you do differently?"* — testing self-awareness. Have an answer
  ready that is a real trade-off rather than false modesty.
- *"Who disagreed with you?"* — testing whether the story is real. Frictionless
  stories have no dissenters, which is itself the tell.
- *"How did you measure that?"* — testing whether the number is yours or
  borrowed. Know where your number came from.

Preparing the *story* is table stakes. Preparing for the three questions after
it is where the difference is, and you can do it in ten minutes with a peer.

**Where this week's material genuinely fits.**

The pattern-recognition question maps onto this week unusually well, because
the whole week is about recognising that differently-dressed problems share a
shape. The at-most-K template from Exercise 5 solves the cold-chain load, the
tasting flights and the courier's zone count — three domains, one loop.

If you use coursework as your story, say so plainly. "While working through an
interview-prep curriculum I noticed..." is fine and is much stronger than a
vague professional anecdote that collapses under one follow-up. Interviewers
mark down evasiveness far more reliably than they mark down inexperience.

**Three stories, deliberately different, is the target for the bank.**

By the end of C2 you want a small set that between them cover: a technical
depth story, a conflict or disagreement story, and a failure story. This is
number three. Keeping them in one folder with one-line summaries at the top
means that when a question arrives in an unfamiliar shape, you can reach for
the nearest one rather than improvising from nothing.

</details>

## Acceptance checklist

- [ ] `behavioral/story-03.md` exists in your portfolio repo.
- [ ] It answers the pattern-recognition question, not a nearby one.
- [ ] All four STAR headings are present, in order.
- [ ] 200 to 400 words, excluding the notes section.
- [ ] The Action section is at least half the word count.
- [ ] The Task section contains no "we".
- [ ] There is one explicit sentence saying **how** you noticed the pattern.
- [ ] There is one thing that did not go smoothly.
- [ ] The Result contains a number or a concrete before-and-after.
- [ ] Read aloud twice, on two different days, with both dates in the notes.
- [ ] Spoken length is between 90 seconds and two minutes.
- [ ] You have answers ready for the three follow-up questions in *Under the hood*.
- [ ] Committed to Git with a message like `Add Week 3 homework 4: behavioral story 3`.

## Stretch

- **Write the three follow-up answers out.** Two or three sentences each, under
  the notes section. Ten minutes, and it is the highest-return ten minutes on
  this page.

- **Tell it to a peer in the org without reading it.** Then ask them to tell it
  back. What they leave out is what you under-emphasised; what they get wrong
  is what you were unclear about. This is a much better signal than asking
  whether the story was good, which nobody answers honestly.

- **Write the same story in 90 words.** Interviewers sometimes ask for the short
  version, and cutting to a third forces you to find out which sentence is
  actually carrying the answer. Keep both versions in the file.

- **Start Story 4 now while the habit is warm.** Question: *"Tell me about a
  time you were wrong about something technical."* That is the failure story,
  it is the hardest of the three, and having a draft before Week 4 means you
  can improve it rather than invent it under pressure.

Next: [Problem 5 — The Rolling Error Rate](./problem-05-rolling-error-rate.md).
