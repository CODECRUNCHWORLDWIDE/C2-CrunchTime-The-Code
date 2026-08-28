# Homework Problem 5 — Deciding Without the Full Picture

> **Topic:** behavioral story #5 — "tell me about a time you had to decide with incomplete information", in STAR form
> **Lecture:** [02 — Binary Search on the Answer](../lecture-notes/02-binary-search-on-the-answer.md)
> **Difficulty:** Easy to start, hard to finish well
> **Target time:** 45 minutes
> **Why this one:** every binary-search iteration is a decision made on partial evidence — you see one midpoint and commit to discarding half the possibilities. Interviewers ask the human version of that question in almost every loop, and the candidates who answer it well are the ones who wrote the story down before the room, not in it.

<!-- no-runnable-file: the deliverable here is a written story about something that actually happened to you, saved in your portfolio repo. There is no program to run, and a script that printed a story would defeat the purpose. The worked example under The Solution is a model of the shape, not an answer to submit. -->

## The Brief

The prompt is one sentence, and you will hear a version of it in most
interview loops:

> **"Tell me about a time you had to make a decision with incomplete
> information."**

What the interviewer is listening for is not bravery. It is **method**. Did you
work out what you actually knew, name the thing you could not know, choose
something you could reverse cheaply if you were wrong, and then go back and
check?

Write it in **STAR**, which is four short parts:

- **Situation** — where you were and what was going on. Two or three sentences.
- **Task** — what you specifically had to decide. One or two sentences.
- **Action** — what *you* did, step by step. This is most of the story.
- **Result** — what happened, with a number if you have one, and what you would
  do differently.

Two hundred to four hundred words. Long enough to have detail in it; short
enough to say out loud in ninety seconds.

**It has to be true.** Not polished into something it was not, not borrowed
from a teammate, not invented. Interviewers ask follow-up questions — "what
did the other option look like?", "who disagreed?" — and a story you did not
live falls apart on the second one. If nothing from work fits, use a course
project, an org event you helped run, a house move, a repair you had to
authorise without a full diagnosis. Ordinary situations make good answers.

There is a bonus connection worth drawing at the end, and it is the reason this
prompt lands in binary-search week. Every iteration of the loop you spent this
week writing is a decision under uncertainty: you see one value, you cannot see
the rest, and you commit to throwing away half of what is left. The commitment
is safe because of an *invariant* — the answer is still in the half you kept.
Good decisions in the real world have the same shape: not "I guessed right",
but "I made sure the thing I could not see could not hurt me".

## Starter

There is no file to run. Create `behavioral/story-05.md` in your portfolio
repo and paste this skeleton in.

```markdown
# Story 05 — Deciding without the full picture

**Prompt:** Tell me about a time you had to make a decision with incomplete
information.

## Situation

<!-- TODO: 2-3 sentences. Where, when, who else was involved. Concrete nouns. -->

## Task

<!-- TODO: 1-2 sentences. The decision that was yours to make, and the deadline. -->

## Action

<!-- TODO: the bulk of the story. Say "I", not "we". Cover, in order:
     - what you knew for certain
     - what you could not know, and why not
     - what you did to shrink the unknown cheaply, if anything
     - the call you made, and why that one
     - what you put in place in case you were wrong -->

## Result

<!-- TODO: what happened. A number if you have one. Then one sentence on what
     you would do differently, which is the part most candidates skip. -->

## The binary-search connection

<!-- TODO: optional, 1-2 sentences. What was your invariant - the thing that
     stayed true whichever way the unknown resolved? -->

---

Word count: <!-- TODO -->  |  Read aloud: <!-- TODO: date, twice -->
```

Fill in every `TODO`, then read the whole thing out loud twice. The second
read is where the sentences that only work on paper get found.

## Requirements

1. A file `behavioral/story-05.md` exists in your portfolio repo and is
   committed.
2. It answers the prompt above, about something that actually happened to you.
3. It is in STAR order, with the four headings visible.
4. It is between 200 and 400 words, excluding the headings.
5. The **Action** section is the longest of the four, and it says "I" rather
   than "we" wherever the action was yours.
6. It names, explicitly, the thing you could not know at the time.
7. The **Result** ends with one sentence on what you would do differently.
8. You read it aloud at least twice, and noted the date in the file.

## Constraints

- **True, not composed.** An interviewer's follow-up questions go two or three
  levels deep, and invented detail collapses there. A smaller true story beats
  a large borrowed one every time.

- **Two hundred to four hundred words, and the bound has a reason.** Under two
  hundred and there is no detail for a follow-up question to grip; over four
  hundred and you are talking for more than two minutes without a check-in,
  which is the single most common way a good story lands badly.

- **"I", not "we", in the Action.** Teams are real and interviewers know it —
  but the question is what *you* did. A story told entirely in "we" leaves the
  listener unable to score you, and their fallback is to assume the smallest
  contribution consistent with the words.

- **One story, not a category.** "I often have to decide without full
  information" is not an answer; it is a description of a job. Pick one day,
  one decision, one outcome.

- **The decision must have been genuinely open.** A story where the right
  answer was obvious and you simply did it is not a story about incomplete
  information. If you cannot name the option you rejected, pick a different
  incident.

## Expected output

There is no program, so what follows is what "finished" looks like at the
terminal — a real session, checking the file exists, counting the words, and
committing it:

```text
$ wc -w behavioral/story-05.md
     318 behavioral/story-05.md
$ git add behavioral/story-05.md
$ git commit -m "Add behavioral story 5: deciding without the full picture"
[main 4c1e9a2] Add behavioral story 5: deciding without the full picture
 1 file changed, 41 insertions(+)
```

Your word count will differ. What should not differ is that the number falls
between 200 and 400, and that the file is committed rather than sitting
unsaved in an editor.

## Steps

1. **Make a list before you write.** Five minutes, no editing: every time you
   can remember having to move before you had the full picture. Aim for four or
   five candidates.
2. **Score them against the last constraint.** For each one, can you name the
   option you rejected? Cross out the ones where you cannot.
3. **Pick the one with a number in it.** A result you can measure — hours,
   pounds, defect count, people affected — is worth more than a better story
   with no evidence in it.
4. **Draft the Action first, not the Situation.** The middle is the part with
   content; the setup is easier to write once you know what it is setting up.
5. **Write down the unknown explicitly.** One sentence, starting "What I could
   not know at the time was…". If that sentence is hard to write, the story is
   probably not about incomplete information.
6. **Add the reversibility.** What did you do to make being wrong cheap? A
   staged rollout, a note in the ticket, a person you told, a date you set to
   revisit. This is the sentence that separates a decision from a gamble.
7. **Fill in Situation, Task and Result.** Keep the Situation to three
   sentences; it is scene-setting, not the story.
8. **Cut to length.** First draft long, then cut. Adverbs and job titles go
   first.
9. **Read it aloud twice**, note the date in the file, and commit.

## The Solution

A worked example. This is a model of the **shape**, built from an ordinary,
invented situation so that nothing here is a story you could submit — yours has
to be your own. Read it for structure, then throw it away.

```markdown
# Story 05 — Deciding without the full picture

**Prompt:** Tell me about a time you had to make a decision with incomplete
information.

## Situation

Our community ran a weekend workshop for around sixty people, and I was
handling the venue. Ten days before, the building manager emailed to say the
main room's projector had failed and a replacement "should" arrive in time —
no date, no order number.

## Task

I had to decide, that week, whether to keep the room or move the workshop to a
smaller hall across the road that seated forty-five but had a working screen.
Moving meant emailing sixty people and cutting fifteen places.

## Action

I wrote down what I actually knew: the small hall was free and confirmed; the
main room was booked and its equipment was not confirmed; forty-eight people
had said yes so far. What I could not know was whether the projector would
arrive, and the manager could not tell me because the order was with a supplier
who had not replied.

Rather than guess, I tried to shrink the unknown cheaply. I asked the manager
one specific question — had the supplier given *any* dispatch confirmation? —
because a yes would have settled it. The answer was no, which told me the
optimistic case had no evidence behind it.

So I made the call that was cheapest to be wrong about. I held the main room,
and I borrowed a portable projector from a member for the price of a taxi
fare. That way a late delivery cost us nothing, an early one meant a spare
machine in the corner, and nobody lost a place.

## Result

The replacement did not arrive until the following week. We ran the workshop
in the main room with the borrowed projector, all sixty attended, and the only
cost was about fifteen pounds of travel.

What I would do differently: I waited two days before asking the dispatch
question. Asking it the same afternoon would have given me the same answer
sooner and a calmer week.

## The binary-search connection

The invariant was "everyone keeps their place, whichever way the delivery
goes" — I chose the option that stayed valid under both outcomes rather than
betting on one. That is the same move as keeping the half of the interval that
provably still contains the answer.

---

Word count: 318  |  Read aloud: 2026-08-27, twice
```

**Why this shape works, part by part.**

**The Situation is three sentences and contains a date.** "Ten days before"
does more work than any adjective could: it tells the listener there was real
time pressure without the word "pressure" appearing.

**The Task names the cost of each option.** Sixty emails and fifteen lost
places. An interviewer cannot judge a decision without knowing what was at
stake, and candidates routinely leave this out because they lived it and
forget the listener did not.

**The Action opens with an inventory.** Three facts, stated flatly, before any
action is taken. That is the "what did I actually know" step, and it is the
single most transferable habit in the story — it is also, structurally, the
same thing you do when you write down the interval bounds before a search.

**It names the unknown in one sentence, and says why it was unknown.** Not
"there was uncertainty" but "the supplier had not replied". Vague uncertainty
sounds like an excuse; a named unknown sounds like an assessment.

**It shows an attempt to shrink the unknown before deciding.** One cheap
question that could have settled the matter. This is the detail that separates
a considered decision from a coin flip, and it is what most candidates skip
entirely — they jump from "I did not know" straight to "so I decided".

**The chosen option is the reversible one, and the story says so.** Fifteen
pounds bought immunity to being wrong. When you can present a decision as
"cheap to be wrong about" rather than "correct", you are describing judgement
rather than luck — and judgement is the thing being scored.

**The Result has a number and an unprompted improvement.** "Two days late in
asking" is a small, specific, real self-criticism. It is far more convincing
than a large abstract one, and it ends the story on reflection rather than on
a victory lap.

## Download and run

There is no file to download for this problem, and that is deliberate: the
deliverable is a piece of writing about your own experience, and no program
can produce it.

What you can run is the check that it is finished and safe:

```bash
wc -w behavioral/story-05.md
git add behavioral/story-05.md
git commit -m "Add behavioral story 5: deciding without the full picture"
```

A story that only exists in an unsaved editor tab is a story you will lose the
week before your interviews, which is precisely when you need it.

## Common bugs to catch

- **The story is told entirely in "we".** The interviewer is scoring one
  person. Go through the Action line by line and change every "we" back to "I"
  wherever the action really was yours — and leave it as "we" where it
  genuinely was not, because that honesty reads well too.

- **There is no named unknown.** If the sentence "what I could not know at the
  time was…" cannot be completed, this is a story about a difficult decision,
  not an uncertain one. They are different questions and interviewers ask both.

- **The decision is presented as correct rather than as cheap to reverse.**
  "I made the right call" invites the follow-up "and if you had been wrong?"
  Answer it before it is asked.

- **The Result has no number.** Hours, money, people, defects, days — anything
  countable. Without one, the listener has only your assessment of your own
  work, which is exactly the thing they are trying to verify independently.

- **The Situation is half the word count.** Scene-setting is not the story. If
  Situation plus Task is longer than Action, cut the setup.

- **It runs to six hundred words.** Read it aloud and time it. Past about two
  minutes without a pause you have stopped answering and started presenting,
  and the interviewer's next question will be an interruption.

- **"What I would do differently" is missing, or is a humblebrag.** "I would
  have been even more thorough" is not a reflection. A real one names something
  small, specific and fixable — like waiting two days to ask a question that
  took a minute.

- **The story is borrowed.** It survives the first question and not the third.
  This is the one bug on the page with no fix other than picking a different
  story.

## Under the hood

<details>
<summary>Under the hood — what STAR is for, and why this prompt is asked so often</summary>

**STAR is a compression format, not a script.**

The four parts exist because untrained answers to behavioral questions fail in
predictable ways: they never establish stakes, they wander through context, they
describe a team's work in the passive voice, and they end without saying what
happened. Situation, Task, Action, Result is simply the minimum structure that
forecloses all four failures. It is not the only structure that works, and an
interviewer is not ticking the letters off — they are checking whether they
could repeat your story back to a hiring panel afterwards.

**Why "decide with incomplete information" is on nearly every rubric.**

Because it is the normal condition of the work. Almost no engineering decision
is made with complete information: you ship without knowing the real traffic
shape, you choose a library without reading all of it, you estimate before the
requirements settle. A candidate who can only describe decisions made with full
knowledge is describing a job that does not exist.

The rubric behind the question usually has three lines on it: did they
distinguish what was known from what was assumed; did they act to reduce the
unknown before committing; did they limit the cost of being wrong. Write the
story so that all three are visible without the interviewer having to dig.

**The connection to this week is real, not decorative.**

A binary search commits to discarding half of everything on the evidence of one
value. That is only safe because of the invariant — "the answer is still inside
the interval I kept" — which is established before the loop and preserved by
every branch. The engineering equivalent of an invariant is the thing that stays
true whichever way the unknown resolves: nobody loses their place, the migration
can be rolled back, the flag can be turned off. Candidates who frame decisions
that way sound different from candidates who frame them as good guesses, and
the difference is visible in about two sentences.

Reusing your own technical vocabulary in a behavioral answer is a small,
genuine signal that the two halves of your work are connected. Do it once, at
the end, and do not overdo it.

</details>

## Acceptance checklist

- [ ] `behavioral/story-05.md` exists in your portfolio repo and is committed.
- [ ] It is a true story about something that happened to you.
- [ ] STAR headings are present and in order.
- [ ] Word count is between 200 and 400.
- [ ] The Action is the longest section and is written in "I".
- [ ] The sentence "what I could not know at the time was…" is completed
      explicitly.
- [ ] The story shows one cheap attempt to shrink the unknown before deciding.
- [ ] The Result carries a number.
- [ ] The last sentence says what you would do differently, specifically.
- [ ] You read it aloud twice and noted the date in the file.

## Stretch

- **Add the invariant sentence to your other four stories.** Go back through
  `behavioral/story-01.md` to `story-04.md` and ask of each: what stayed true
  whichever way things went? Some will not have one — those are the decisions
  that were gambles, and knowing which of your stories are which is worth an
  hour.

- **Write the ninety-second spoken version.** Not a summary — a different
  artifact, with contractions in it and no headings, that sounds like a person
  talking. Record it, listen back at normal speed, and count how many times you
  say "basically" or "sort of". Most people are surprised.

- **Prepare the three follow-ups.** For your story, write one-paragraph answers
  to: *what did the option you rejected look like?*, *who disagreed with you,
  and what did they say?*, and *how would you know sooner next time?* Those are
  the questions that actually come, and having thought about them once is the
  difference between an answer and a stall.

Next:
[Homework Problem 6 — Autocomplete at Scale](./problem-06-autocomplete-at-scale.md).
