# Homework Problem 4 — The Tradeoff Story

> **Topic:** the second story in your bank — "a time you chose between two valid approaches" — told in STAR, out loud, in under two minutes
> **Lecture:** [03 — Stating Complexity Out Loud](../lecture-notes/03-stating-complexity-out-loud.md)
> **Difficulty:** the writing is easy; being specific is not
> **Target time:** 45 minutes
> **Why this one:** the behavioural round is half of most interview loops and the half candidates prepare least. This week's topic hands you the story shape for free — you have spent five days saying "approach A is faster, approach B uses less memory, I chose B because" — and a tradeoff story is that sentence with people in it. Story two of a bank you will keep adding to all course.

<!-- no-runnable-file: the deliverable is a story about your own experience, in your own words, in your own portfolio repository. No program can write it and none should try. -->

## The Brief

An interviewer asks: *"Tell me about a time you had to make a tradeoff between
two valid approaches."*

The word doing the work is **valid**. They are not asking about a time you found
a bug, or a time somebody proposed something silly and you talked them out of
it. They are asking about a time when **both options were defensible**, you had
to pick one, and you can still explain the reasoning.

That is a harder question than it looks, and most answers fail in one of two
ways. Either the second option was never really viable — "we could have done it
by hand, but obviously we automated it" — in which case there was no tradeoff
and no decision. Or the answer stays abstract: "I weighed the pros and cons and
went with the better approach", which contains no information at all.

The format is **STAR**, four parts:

- **Situation** — where you were and what was going on. Two or three sentences.
  Enough context that the rest makes sense, and no more.
- **Task** — what you specifically had to decide. Not what the team did. What
  landed on you.
- **Action** — the two options, why each was defensible, what you weighed, and
  what you chose. This is most of the story.
- **Result** — what happened, with something concrete in it, and what you would
  do differently.

Here is the connection to this week, and it is not decoration. You have spent
five exercises saying: *the hash map is O(n) time and O(n) space; the two-pointer
scan is O(n) time and O(1) space; I chose the scan because the input is already
sorted and the map's memory buys nothing.* That sentence — two real options,
each with its cost, a decision, a reason — is exactly the spine of a good
tradeoff story. Swap the data structures for a library choice, a schema, a
deadline, a rewrite-versus-patch call, and you have your Action section.

The story does not have to be about code. A tradeoff you made organising a
volunteer rota, or choosing what to cut from a project when time ran out, works
just as well, provided both options were real and you can say why.

## Starter

Create `behavioral/story-02.md` in your portfolio repo and paste this in. Fill
in every bracket, then delete the brackets.

```markdown
# Story 02 — A tradeoff between two valid approaches

**Prompt:** "Tell me about a time you had to make a tradeoff between two valid
approaches."

**Situation.** [Where were you, when, and what was the context? Two or three
sentences. Name the project or the setting concretely.]

**Task.** [What did *you* have to decide? Use "I", not "we". Say what made it
a decision rather than an obvious call.]

**Action.** [Option A: what it was, and why it was genuinely defensible.
Option B: same. What did you weigh -- time, memory, maintenance, risk,
whose time, what would break? Who did you talk to? What did you choose, and
what was the deciding factor?]

**Result.** [What happened? Include one concrete detail -- a number, a date,
a thing that shipped or did not. Then: what would you do differently, or
what did the choice cost you that you did not expect?]
```

Two notes before you start.

**Pick the story first, then write.** Spend five minutes listing three
candidates before you commit to one. The first story that comes to mind is
usually the most dramatic, and drama is not what this question rewards —
specificity is.

**Say "I", not "we".** "We decided" tells the interviewer nothing about you. If
the decision was genuinely collective, say what your contribution to it was.

## Requirements

1. A file at `behavioral/story-02.md` in your portfolio repo.
2. The prompt is quoted at the top, so a reader knows what is being answered.
3. All four STAR headings are present, in order.
4. Between 200 and 400 words.
5. **Both** options are described, and both are shown to be genuinely
   defensible. A story where option B was obviously bad is not a tradeoff story.
6. The Action section names the axis you decided on — speed, memory,
   maintenance, risk, time, someone else's time — explicitly.
7. The Result section contains at least one concrete detail: a number, a date, a
   named outcome.
8. The Result section says what you would do differently, or what the choice
   cost you.
9. You read it aloud at least twice, and it lands under two minutes.

## Constraints

- **200 to 400 words.** Under 200 and you have not said enough for anybody to
  judge; over 400 and you are past two minutes spoken, which is where an
  interviewer starts waiting for you to stop. This is the same length discipline
  as the two-minute cost section, and for the same reason: the constraint is the
  listener's attention, not the page.

- **Both options must be defensible.** If option B was never viable, you have
  written a story about noticing something obvious. The interviewer is
  specifically probing whether you can hold two reasonable positions at once and
  choose between them, which is the thing engineering judgment actually is.

- **One concrete detail, minimum, in the Result.** "It went well" is not a
  result. "It shipped three weeks later and we never had to revisit that
  decision" is. "It shipped, and six months on the shortcut I took cost us two
  days" is better still. Specificity is the only thing distinguishing a real
  memory from a plausible invention, and interviewers listen for it.

- **True stories only.** An invented story survives about ninety seconds of
  follow-up questions, and the follow-ups are where behavioural rounds are
  actually decided. A small, true, slightly unglamorous decision beats an
  impressive one you cannot answer questions about.

- **No blame.** If the story involves a disagreement, describe the other
  position fairly enough that its holder would recognise it. An interviewer
  hearing a colleague described uncharitably is being shown how you will
  describe *them* later.

## Expected output

There is no program here, so the output is the story. This is what a finished
one reads like — invent your own; this is a shape, not a template to fill:

```text
# Story 02 -- A tradeoff between two valid approaches

**Prompt:** "Tell me about a time you had to make a tradeoff between two
valid approaches."

**Situation.** Last spring I helped run a two-day student hackathon for about
ninety people. Judging ran on a spreadsheet that four judges edited at once,
and the previous year it had locked up during the final round.

**Task.** With three weeks to go I had to decide whether to build a small
web form that wrote scores to a database, or to keep the spreadsheet and fix
the way judges used it.

**Action.** Both were real options. The web form solved the problem properly:
no concurrent-edit conflicts, and scores could be totalled automatically. It
was maybe fifteen hours of work, and it would be the only piece of the event
nobody else on the team could fix if it broke at nine on a Saturday night.
The spreadsheet was fragile, but every organiser already knew it, and the
actual failure was two judges editing one sheet -- which a separate tab per
judge and one totals tab would fix in an afternoon.

I chose the spreadsheet, and the deciding axis was not effort. It was who
could repair it during the event. I wrote the tabs, tested them with two
organisers pretending to be judges, and wrote a half-page recovery note for
the failure I could still imagine.

**Result.** Judging finished eleven minutes ahead of schedule and nothing
locked up. The cost was real though: totalling still needed a person, and
that person was me, so I missed the closing photos. If I ran it again I would
build the form in the quiet month before the event rather than in the three
weeks before it, because the constraint I was actually solving for was the
calendar, not the tool.
```

Read what makes that work. Both options are described well enough that you can
imagine choosing either. The deciding axis is named out loud and it is *not* the
obvious one — "who can repair it at nine on a Saturday" rather than "which is
less work". There is a number in the result. And the "what I would do
differently" identifies the real constraint rather than apologising.

## Steps

1. List three candidate stories in a scratch file. Any decision where you can
   still name the option you did not take.
2. For each, ask: was the other option genuinely defensible? Cross out any where
   the answer is no. If all three go, list three more — this is normal, and it
   is why the exercise starts with three.
3. Pick the one where you remember the most detail, not the one that sounds most
   impressive.
4. Write the Action section first. It is the substance, and starting with
   Situation tends to produce three paragraphs of scene-setting for a
   one-paragraph decision.
5. Add Situation and Task, and then cut them until they are only what the Action
   needs.
6. Write the Result. Find one number. If you genuinely have none, name a
   concrete outcome instead — a thing that shipped, a date, a problem that did
   or did not recur.
7. Read it aloud, timed. Cut to under two minutes. Read it aloud again, and cut
   anything you stumbled over — a sentence you cannot say smoothly is a sentence
   you rewrote too many times.
8. Commit.

## The Solution

The finished story is the block under **Expected output** above, and it is
deliberately not hidden. Yours will be about something else entirely; what
transfers is the shape and the four moves below.

**The Action section carries the story, and it is the one people underwrite.**
A common failure is three sentences of context, one sentence of decision, and
two of outcome. Invert that. The interviewer wants to hear you *hold two
options at once*, which means both have to be on the page long enough to be
weighed. Roughly half your word count belongs here.

**Name the deciding axis explicitly, and prefer the non-obvious one.** "I chose
it because it was less work" is a weak answer, because effort is the axis
everybody defaults to. "I chose it because of who could repair it during the
event" is strong, because it shows you found the constraint that actually
governed the decision rather than the one that was easiest to measure. This is
the same move as the cost sections you have been writing all week: the
interesting sentence is not *which is faster*, it is *which axis did this
particular situation care about*.

**Describe the option you rejected generously.** If the web form in that story
had been described as "over-engineered", the reader would learn that the writer
dismisses things. Described as genuinely better on the merits and rejected on a
constraint, the same decision reads as judgment. This is exactly the discipline
Homework Problem 3 asks for in prose — the tradeoff paragraph that admits brute
force is *correct* is stronger than one that pretends it is wrong.

**The "what I would do differently" is the highest-value sentence in the
story.** Most candidates end on the win. Ending on what the choice cost, or on
what you now see that you did not, demonstrates that you review your own
decisions — which is the thing this question is really testing. It must be
specific: "I would plan better" is nothing; "I would have built it in the quiet
month, because the constraint was the calendar rather than the tool" is a
finding.

**Why a story bank rather than one story.** Spaced repetition. You are building
a set of four or five real experiences, each written once and then reusable
across many prompts — a tradeoff question, a conflict question, a failure
question and a leadership question can often be answered from the same three
stories with a different emphasis. Writing them cold, well before you need them,
is what stops the behavioural round from being the one you improvise.

## Download and run

There is no file to download. The deliverable is a story about your own
experience, and no program can supply one.

The check that matters is a listening test, not a run. Record yourself telling
it without reading, then play it back:

```bash
# any phone voice memo works; on a laptop, anything that records will do
```

Three things to listen for. Did you get through both options, or did you rush
the one you rejected? Did you say the deciding axis out loud, in one clear
sentence? Did you land under two minutes without hurrying?

Then hand the written version to somebody who was not there and ask them to say
back what the two options were. If they can, it is specific enough.

## Common bugs to catch

- **The second option was never viable.** The most common failure, and it turns
  a tradeoff question into a "time you noticed something obvious" answer. If you
  cannot argue for the option you rejected, you have not got a tradeoff story
  yet — go back to your list of three.

- **"We decided."** The interviewer is hiring you, not your team. Say what you
  contributed to the decision. If it was genuinely collective, say *"I argued
  for X on these grounds; the team went with Y and here is what I took from
  that"* — which is a good story in its own right.

- **No numbers, no dates, no names.** "It went well" is not a result. Without
  one concrete detail, a true story sounds exactly like an invented one, and
  the interviewer has no way to tell them apart.

- **Over 400 words.** Read it aloud with a timer. Over two minutes, an
  interviewer starts steering rather than listening. Cut the Situation first;
  it is almost always twice as long as it needs to be.

- **The deciding axis is left implicit.** If your Action section describes both
  options and then says "so I went with B", the interviewer has to infer your
  reasoning, and they will infer something less flattering than the truth. One
  sentence: *"the axis I decided on was X."*

- **Ending on the win.** No "what I would do differently" means no evidence that
  you review your own decisions. That sentence is the difference between a
  competent answer and a memorable one.

- **Describing a colleague unfairly.** However justified it felt at the time, an
  interviewer hears how you will describe *them* to your next interviewer.
  Describe the other position as its holder would.

- **Inventing the story.** It survives about ninety seconds of follow-ups, and
  follow-ups are where these rounds are decided. A small true decision beats a
  large invented one every time.

## Under the hood

<details>
<summary>Under the hood — what a behavioural round is actually scoring, and why tradeoff questions are the best of them</summary>

**Behavioural rounds score a small number of things, repeatedly.** Most
structured loops assess something close to: ownership (did you drive it, or did
it happen around you?), judgment (did you weigh the right things?),
communication (can somebody who was not there follow you?), and
self-assessment (do you know what you got wrong?). Every prompt is a different
door into those four.

That is why the STAR shape works. Situation and Task establish that you owned
something. Action is where judgment is visible. The whole thing being followable
by a stranger is the communication score. And the last sentence is
self-assessment, which is the one candidates most often skip entirely.

**Tradeoff questions are the most informative prompt in the set**, and worth
preparing best. A "greatest strength" question can be answered from imagination.
A tradeoff question cannot: it needs two real options, real constraints, and a
real decision, and a candidate who has not made decisions has nothing to say.
That is exactly why it gets asked, and why a specific, unglamorous story does
better than an impressive vague one.

**The connection to complexity is real and worth making explicit.** This week's
five-piece cost section is a tradeoff argument with data structures as the
parties: two viable options, each with a measured cost on two axes, a decision,
and a named reason. A behavioural tradeoff story is the same argument with
people, time and risk as the axes. Candidates who are fluent in one and not the
other usually have not noticed they are the same move.

If you want to feel that, take one of this week's cost sections and rewrite it
as four STAR paragraphs. Situation: the constraint said 300,000. Task: pick a
structure. Action: the map is O(n)/O(n), the scan is O(n)/O(1), and here is
what decided it. Result: it ran, and here is what the choice cost. It reads
oddly and it is a genuinely useful five minutes, because it shows you the story
skeleton you already own.

**On the bank, and how many you need.** Four or five stories, written well,
cover most loops: a tradeoff, a conflict or disagreement, a failure or mistake,
a time you learned something quickly, and a time you helped somebody else. Most
prompts are one of those with different framing, and the reframing is easy once
the underlying story is written down and true. What is hard is producing a
specific story under pressure with nothing prepared, which is what happens to
people who treat the behavioural round as the easy one.

**One practical note on recording.** Read-aloud and record-and-listen are
different exercises and you want both. Reading aloud catches sentences that do
not say. Listening back catches pace, filler and the places where you skipped a
step because you knew it and the listener did not. The second is
uncomfortable and it is where most of the improvement is.

</details>

## Acceptance checklist

- [ ] `behavioral/story-02.md` exists in your portfolio repo.
- [ ] The prompt is quoted at the top.
- [ ] All four STAR headings are present, in order.
- [ ] Between 200 and 400 words.
- [ ] Both options are described, and both read as genuinely defensible.
- [ ] The deciding axis is named in one explicit sentence.
- [ ] The Action section is roughly half the word count.
- [ ] The Result contains at least one number, date or named outcome.
- [ ] The Result ends with what you would do differently, and it is specific.
- [ ] You say "I" where the decision was yours.
- [ ] Read aloud twice, timed, and it lands under two minutes.
- [ ] Somebody who was not there can say back what the two options were.
- [ ] Committed with a message like `Add behavioral story 02: tradeoff`.

## Stretch

- **Write the thirty-second version.** Same story, cut to Situation in one
  sentence, both options in two, the decision in one, the result in one. Being
  able to give the short version when an interviewer is short of time, and then
  expand on request, is a separate skill from being able to give the long one —
  and it is the version that gets used when you are the fourth conversation of
  their day.

- **Answer three different prompts from the same story.** Try: *"tell me about a
  time you disagreed with someone"*, *"tell me about a constraint that changed
  your plan"*, and *"tell me about something you would do differently"*. Most
  good stories answer three or four prompts with a shift of emphasis, and
  discovering that is what turns four stories into a bank rather than four
  answers.

- **Take one of this week's exercises and write its cost section as a STAR
  story.** Situation: the constraint said 200,000 charges. Task: choose a
  structure. Action: the nested scan is O(n^2)/O(1) and the map is O(n)/O(n),
  and the bound decided it. Result: it ran in one pass, and it cost O(n) memory.
  It reads strangely on purpose. What it shows you is that the story skeleton
  and the engineering argument are the same skeleton, which is worth knowing
  before an interviewer asks you to switch between them in one hour.

Next: [Homework Problem 5 — Counting the Top Queries](./problem-05-top-queries-design.md).
