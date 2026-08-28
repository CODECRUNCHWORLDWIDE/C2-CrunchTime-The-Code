# Problem 4 — Behavioral Story #4

<!-- no-runnable-file: this problem's deliverable is a written story about the learner's own life, not a program -->

> **Topic:** the story bank — a STAR answer to the growth question every interview loop asks
> **Lecture:** [02 — The Mock Interview Protocol](../lecture-notes/02-the-mock-interview-protocol.md), §5 and §8
> **Difficulty:** Easy to write badly, hard to write well
> **Target time:** 45 minutes, including reading it aloud twice
> **Why this one:** this week you watched a recording of yourself and wrote down what was wrong with it. That is *exactly* the behaviour this interview question is fishing for, and you have a fresh example of it. Write the story now, while the feeling is still available.

## The Brief

Every interview loop has a behavioural round, and every behavioural round asks
some version of one question: **"Tell me about a time you got difficult
feedback and acted on it."**

It sounds soft. It is not. What the interviewer is checking is whether you can
hear something unwelcome, keep working, and change what you do. Someone who
cannot is expensive to work with, no matter how well they code.

The trap is that the obvious answer sounds good and says nothing: *"I take
feedback well and I'm always looking to improve."* That is a claim about your
character. Nobody is graded on claims. You are graded on a specific thing that
happened, with a specific change that followed it, and a specific result you
can point at.

**STAR** is the shape that keeps you honest. Four parts, in order:

- **Situation** — where you were and what was going on. Two sentences.
- **Task** — what you were responsible for. One sentence.
- **Action** — what *you* did, step by step. This is the long part and it is
  the part being graded.
- **Result** — what changed, ideally with a number or a before-and-after.

The most common failure is spending three quarters of the words on Situation
because it is the easiest part to write, and then rushing Action. Watch for it.

**Your topic this week.** Write a story about difficult feedback you received
and acted on. It must be true and it must be yours.

**And the connection this week hands you.** Mock #1 gave you a recording of
yourself, you watched it, and you wrote down one specific thing to change. That
is the same loop — receive an unwelcome observation, extract one change, apply
it — run on yourself, weekly, on purpose. Getting that into the story naturally,
usually in the Result or in a closing sentence, is the engineering-mindset
signal a behavioural interviewer is listening for. *"I do this to my own
performance every week"* lands far harder than *"I'm open to feedback."*

## Starter

Create `behavioral/story-04.md` in your portfolio repo and paste this in. Fill
in every `TODO`.

```markdown
# Story 4 — Difficult feedback, acted on

**Question this answers:** "Tell me about a time you got difficult feedback and
acted on it."
**Length:** 200-400 words.
**Last read aloud:** TODO (date)

## Situation

TODO: two sentences. Where were you, what was the project, who else was
involved? Enough for a stranger to picture it. No more.

## Task

TODO: one sentence. What were you on the hook for?

## Action

TODO: the long part, and the graded one. What did the feedback actually say —
quote it if you can remember the words. What was your first reaction, honestly?
What did you do next, in order? Name the specific change you made, not the
attitude you adopted.

## Result

TODO: what changed. A number, a before-and-after, or a thing that stopped
happening. If the result was partly bad, say so — a story where everything
worked out perfectly reads as fiction.

## What I would say out loud

TODO: the same story compressed to about 90 seconds of speech. Not bullet
points. Full sentences, the way you would actually say them.
```

## Requirements

1. The file exists at `behavioral/story-04.md` in your portfolio repo.
2. It answers **"Tell me about a time you got difficult feedback and acted on
   it."**
3. It follows STAR, with the four headings in that order.
4. It is between 200 and 400 words, not counting the spoken version.
5. The **Action** section is the longest of the four.
6. The story is true, and it is about you rather than about your team.
7. You have read it aloud at least twice, and the date of the last read is in
   the file.

## Constraints

- **200 to 400 words, because that is roughly 90 to 150 seconds spoken.** A
  behavioural answer much shorter than 90 seconds reads as evasive; much longer
  than two minutes and the interviewer stops tracking the thread. The word count
  is not arbitrary — it is a speaking length wearing a written costume, which is
  why the last section of the template is the spoken version.

- **The Action section must be the longest.** This is a constraint rather than
  advice because the natural drift is the other way. Situation is the easiest
  part to write and the least informative part to read. If your Situation is
  longer than your Action, cut Situation in half before doing anything else.

- **First person singular.** "We decided" tells the interviewer nothing about
  you. Where the work really was shared, say what your part was. This is not
  about claiming credit; it is that a story with no "I" in it cannot be
  evidence about you.

- **One piece of feedback, one change.** Not three. A story that lists several
  improvements dilutes all of them and usually means none were specific. Pick
  the one you can describe most concretely.

- **The feedback has to have been genuinely unwelcome.** "My manager suggested I
  might enjoy learning Kubernetes" is not difficult feedback. If the story has
  no moment where you felt defensive, it is not answering the question that was
  asked — and the interviewer will hear the gap.

## Expected output

There is no program here, so what follows is a worked excerpt rather than
captured stdout: the **Action** and **Result** sections of a story that would
score well. Names and details are invented; yours must not be.

```text
## Action

The feedback was one sentence in a review: "Your PRs are correct but they are
very hard to review." My first reaction was that this was a complaint about
other people's patience, and I said so, to a friend, at some length.

Then I went and looked. I pulled my last ten pull requests and measured them.
The median was 640 changed lines across nine files, and six of the ten mixed a
refactor with a behaviour change in the same diff. The reviewer was not being
slow. I had been handing them two jobs at once and calling it one.

I changed one thing. From that point every refactor went in its own pull
request, merged first, and the behaviour change went in a second one on top.
It made my own work slower — two branches, two reviews, more rebasing.

## Result

Over the next two months my median PR went from 640 lines to 180, and median
time-to-first-review went from about 26 hours to under 5. The same reviewer
started picking my PRs up without being asked. I still do the two-PR split, and
it is the habit I would keep if I could only keep one.
```

Three things to notice. The feedback is quoted, so it is specific. The first
reaction is admitted rather than tidied away, which is what makes the rest
believable. And the change is one concrete practice with a cost attached — not
an attitude.

## Steps

1. **Pick the story before you write anything.** Give yourself five minutes and
   list three times you were told something you did not want to hear. Choose the
   one where you can still name the specific change that followed. If none of
   the three has a specific change, that is worth knowing about yourself, and
   Mock #1 has just handed you a fourth candidate.
2. **Write Action first.** Skip Situation entirely on the first pass. Action is
   the graded section and it is the one that decides whether the story is worth
   telling; if it comes out thin, change stories now rather than after you have
   polished two paragraphs of scene-setting.
3. **Write Result second, and look for a number.** Not every story has one. If
   yours does not, find a before-and-after you can state as a fact — something
   that used to happen and stopped.
4. **Write Situation and Task last, and keep them to three sentences between
   them.** You now know exactly how much context the Action needs, which is the
   only way to get this length right.
5. **Cut to 400 words.** Almost every first draft is over. Cut from Situation.
6. **Write the spoken version.** Not a summary — the same story in the words you
   would actually use, contractions and all.
7. **Read it aloud twice, out loud, at speaking pace.** Time it. Anything you
   stumble over is a sentence you would not really say; rewrite it the way you
   said it the second time. Put today's date in the file.
8. **Connect it to this week, if it fits.** One closing sentence about watching
   your own Mock #1 recording and extracting one change. Do not force it — a
   bolted-on connection is worse than none.

## The Solution

There is no program to publish here, and no single right answer: the deliverable
is a true story about your own life. What *can* be published is the shape a good
answer has, so here it is as a filled-in template you can compare yours against.

```markdown
# Story 4 — Difficult feedback, acted on

**Question this answers:** "Tell me about a time you got difficult feedback and
acted on it."
**Length:** 310 words.
**Last read aloud:** 2026-08-25

## Situation

I was six months into my first job, on a three-person team maintaining the
service that priced our shipping quotes. I was shipping steadily and I thought
it was going well.

## Task

I owned the quote-validation rules and every change to them went through me.

## Action

The feedback was one sentence in a review: "Your PRs are correct but they are
very hard to review." My first reaction was that this was a complaint about
other people's patience, and I said so, to a friend, at some length.

Then I went and looked. I pulled my last ten pull requests and measured them.
The median was 640 changed lines across nine files, and six of the ten mixed a
refactor with a behaviour change in the same diff. The reviewer was not being
slow. I had been handing them two jobs at once and calling it one.

I changed one thing. From that point every refactor went in its own pull
request, merged first, and the behaviour change went in a second one on top. It
made my own work slower — two branches, two reviews, more rebasing.

## Result

Over the next two months my median PR went from 640 lines to 180, and median
time-to-first-review went from about 26 hours to under 5. The same reviewer
started picking my PRs up without being asked. I still do the two-PR split, and
it is the habit I would keep if I could only keep one.

I have since made a habit of the wider move: this week I recorded myself solving
a problem under interview conditions, watched it back, and pulled out one thing
to change. Same loop, run on myself, on a schedule.

## What I would say out loud

So, about six months into my first job — small team, I owned the quote
validation rules. I got a review comment that said my PRs were correct but hard
to review, and honestly my first reaction was that that was someone else's
problem. But I went and actually measured my last ten PRs, and the median was
640 lines, and most of them had a refactor and a behaviour change tangled
together. So I split them: refactor first, merged on its own, then the change.
Two months later my median PR was 180 lines and review time went from about a
day to under five hours. I still work that way.
```

**Why the first reaction is in the story.** Admitting you were defensive costs
nothing and buys everything. Every interviewer has been defensive about
feedback; a story where the candidate received criticism gracefully and
immediately improved reads as sanded down. The defensiveness is what makes the
measurement that follows it credible.

**Why there is a measurement at all.** "I went and looked" is the hinge of the
whole story. It turns a disagreement about tone into a question with an answer,
and it is the most engineering thing in the paragraph. If your Action has a
moment where you replaced an opinion with a number, put it in the middle where
it cannot be missed.

**Why the change has a cost.** "It made my own work slower" is the line that
proves the change was real. A change with no downside is usually a change nobody
had to make.

**Why the Result is partly modest.** Two numbers and one observation, and no
claim that the team was transformed. Results that are too large invite
follow-up questions you cannot answer.

**Why the spoken version is different from the written one.** Read them side by
side. The spoken one has contractions, one sentence fragment, and no headings.
It is 140 words against 310 because speech is slower and because half of the
written detail is there to help *you* remember, not to be said. Writing the two
separately is what stops you reciting a document at somebody.

## Download and run

There is nothing to download and nothing to run — the deliverable is your own
story, written in your own words, and publishing a file for you to copy would
defeat the entire exercise.

Instead, do this from your portfolio repo:

```bash
wc -w behavioral/story-04.md
```

Confirm it is between 200 and 400 words with the spoken section removed, then
read it aloud once more and commit it:

```bash
git add behavioral/story-04.md
git commit -m "Add Week 4 behavioral story: difficult feedback"
```

## Common bugs to catch

- **A Situation longer than the Action.** The most common shape of a weak
  story. Symptom: two full paragraphs before anything happens. Fix: cut
  Situation to two sentences, and trust the interviewer to ask if they need
  more.

- **No "I" anywhere.** Symptom: every sentence in the Action begins "we". The
  interviewer learns about your team and nothing about you. Fix: go through the
  Action and name your specific part of each "we".

- **The feedback was not difficult.** Symptom: nothing in the story stung, and
  there is no moment of resistance. You have answered a different question —
  probably "tell me about a time you learned something new". Fix: pick a
  different story.

- **A change with no cost and no detail.** Symptom: "I became more careful
  about code quality." That is an attitude, and attitudes are unfalsifiable.
  Fix: name the practice, the first time you did it, and what it cost you.

- **A Result with no evidence.** Symptom: "the team was much happier
  afterwards." Fix: find a number, or a thing that used to happen and stopped.
  If neither exists, say what you would measure now — that is a better answer
  than an invented outcome.

- **A forced link to this week.** Symptom: a final paragraph about mock
  interviews that has nothing to do with the story above it. Fix: cut it. The
  connection only helps when the story is genuinely about the same loop.

- **Never read aloud.** Symptom: sentences with three subordinate clauses that
  you cannot get through in one breath. This is the bug the "read it aloud
  twice" requirement exists for, and it is invisible on the page.

## Under the hood

<details>
<summary>Under the hood — why behavioural rounds exist, and what a rubric actually looks like</summary>

**Behavioural rounds are trying to predict one thing: what you will be like
after the honeymoon.** Technical rounds test what you can do on a good day.
Behavioural rounds are trying to find out what happens on a bad one — when the
design you argued for turns out to be wrong, when the deadline moves, when
somebody senior tells you your work is not good enough. Past behaviour is a
weak predictor, but it is the best one available in 45 minutes.

**Most large companies grade against a written rubric, and the axes are
boringly consistent.** Typically: is the story *specific* (named project, named
change, not a general policy); is the candidate's *own contribution* clear; is
there *evidence* of the outcome; and did the candidate *change something*
rather than merely feel something. Notice that none of those axes reward
sounding positive. They reward being checkable.

**The STAR shape is old and not sacred.** It comes out of structured-interview
research from the 1970s and 1980s, where the finding was that interviews
predict performance much better when every candidate is asked the same
questions and graded against the same anchors. STAR is one such structure;
others exist. What matters is not the four letters but that your answer has a
concrete situation, your own actions, and a checkable outcome — in an order the
listener can follow without effort.

**Why a story bank rather than improvising.** You will be asked perhaps eight
behavioural questions across a loop, and there are only so many distinct things
that have happened to you. Six or seven well-built stories, each of which can
answer two or three question types, covers almost everything. Building them one
per week — which is what these homework problems are doing — means by Week 13
you have a bank instead of a panic. Week 13's lecture covers the mapping from
questions to stories in detail.

**Where the meta-skill from this week actually pays off.** The self-feedback
discipline you practised on Mock #1 — watch, name one specific thing, change
it — is the same loop this question is asking about. It is not a coincidence
that this story is due the same week as the mock. If you can describe that loop
as something you do routinely, and give one example from work and one from your
own practice, you are answering a question most candidates answer with a
sentiment.

</details>

## Acceptance checklist

- [ ] `behavioral/story-04.md` exists in your portfolio repo and is committed.
- [ ] It answers "Tell me about a time you got difficult feedback and acted on
      it."
- [ ] The four STAR headings appear in order.
- [ ] It is between 200 and 400 words, excluding the spoken version.
- [ ] The Action section is the longest of the four.
- [ ] The feedback is quoted or closely paraphrased, not summarised as a mood.
- [ ] The change you made is one specific practice, and its cost is stated.
- [ ] The Result contains a number or a stated before-and-after.
- [ ] There is a separate spoken version, in speaking words.
- [ ] You have read it aloud at least twice, and the date is in the file.

## Stretch

- **Write the 30-second version as well as the 90-second one.** Some
  interviewers ask for a quick example and move on. Cutting your own story to a
  third of its length forces you to find the one sentence that carries it.

  ```text
  90 seconds  full story, situation through result
  30 seconds  the feedback, the measurement, the change, one number
  ```

- **Map this story to the other questions it can answer.** Most good stories
  answer three or four. This one plausibly covers "tell me about a time you were
  wrong", "tell me about a time you changed how your team worked", and "what is
  a habit you have that you would recommend". Write the mapping into the file so
  future-you can find it fast.

- **Record yourself telling it, then watch the recording.** You did exactly this
  to a coding problem this week, and the same two-pass protocol from
  [Lecture 2 §7](../lecture-notes/02-the-mock-interview-protocol.md) works here.
  Watch for the same three things: filler, pace, and whether the Action section
  actually got the airtime it gets on the page. Most people's spoken Action is
  half the length of their written one.

Next: [Problem 5 — System-Design Ground Zero #4](./problem-05-system-design-warmup.md).
