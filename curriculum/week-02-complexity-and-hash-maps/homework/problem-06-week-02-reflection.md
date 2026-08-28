# Homework Problem 6 — Week 2 Reflection

> **Topic:** four honest questions about the week you just had, answered in 300 to 400 words, before you start Week 3
> **Lecture:** [03 — Stating Complexity Out Loud](../lecture-notes/03-stating-complexity-out-loud.md)
> **Difficulty:** the writing is trivial; the honesty is not
> **Target time:** 45 minutes
> **Why this one:** a fifteen-week course only compounds if each week is measured before the next one starts. This is where you find out whether your cost sections actually got better or whether you templated them by Exercise 4 — and finding that out on Sunday is a completely different situation from finding it out in Week 9.

<!-- no-runnable-file: the deliverable is an honest account of your own week, in your own portfolio repository. No program can write it, and a checklist that scored it would defeat the point, because the only thing being measured is whether you told yourself the truth. -->

## The Brief

At the end of a long walk it is worth turning round and looking at the hill. Not
to admire it — to see how steep it actually was, and whether the boots were
right.

That is this problem. Four questions, 300 to 400 words, written before you open
Week 3.

The reason it is graded work rather than an optional nicety: this course is
fifteen weeks, and each week assumes the one before it landed. Week 3's sliding
window is built directly on the amortisation argument you drilled in Exercise 5.
Week 8's heaps are the answer to a problem you already met in Homework Problem 5.
If Week 2 half-landed and you do not notice, Week 3 is harder for a reason you
cannot see, and by Week 6 the cause is far enough back to be invisible.

The four questions, and they are not rhetorical:

1. **Did your cost sections actually get better this week, or did you cut
   corners on Exercises 4 and 5?** Read Exercise 1's write-up and Exercise 5's
   write-up back to back. Be specific about what you see.
2. **Which sub-shape of hash map — complement lookup, canonical key, set
   membership, frequency, two-way mapping — felt most natural? Which felt
   forced?** The one that felt forced is the one to drill.
3. **The five-piece cost structure: formulaic and annoying, or useful? Why?**
   Both answers are legitimate. The reasoning is what matters.
4. **What is one specific thing you will do differently in Week 3?** One. Not
   five. Specific enough that somebody could tell on Wednesday whether you did
   it.

The one rule that makes this worth 45 minutes: **write down the thing you would
rather not.** A reflection that reports a good week is worth nothing to anybody,
including you. If you skipped a recording, say so. If your Exercise 4 cost
section was copied from Exercise 3 with the nouns changed, say that. Nobody is
marking this but you, and the only way it fails is by being flattering.

## Starter

Create `study-plan/week-02-reflection.md` in your portfolio repo and paste this
in. Answer in order.

```markdown
# Week 2 reflection — Complexity and hash maps

*Written [date], before starting Week 3.*

## 1. Did my cost sections actually get better?

[Read Exercise 1's and Exercise 5's write-ups back to back before answering.
Name what is different, or admit that nothing is. If you templated after a
certain drill, say which one.]

## 2. Which hash-map sub-shape felt natural, and which felt forced?

[Complement lookup, canonical key, set membership, frequency, two-way
mapping. Name one of each and say what made the difference -- was it the
structure, or was it the contract around it?]

## 3. The five-piece structure: useful or formulaic?

[Either answer is fine. Say why, and say whether your view changed between
Exercise 1 and Exercise 5.]

## 4. One specific thing I will do differently in Week 3

[One. Specific enough that somebody could check on Wednesday whether you
did it.]

## The thing I would rather not write down

[One sentence. This is the section that makes the rest worth reading.]
```

Two notes before you start.

**Re-read before you answer question 1.** Do not answer it from memory. Open
both write-ups. The gap between what you remember writing and what you actually
wrote is usually the most useful thing on the page.

**Forty-five minutes, not fifteen.** Most of it is re-reading. The writing is
twenty minutes.

## Requirements

1. A file at `study-plan/week-02-reflection.md` in your portfolio repo.
2. Dated, and written before you start Week 3.
3. Between 300 and 400 words.
4. All four questions answered, in order, under their own headings.
5. Question 1 is answered after actually re-reading both write-ups, and names
   something concrete that changed or did not.
6. Question 2 names one sub-shape that felt natural and one that felt forced.
7. Question 4 names exactly **one** change, specific enough to be checkable
   mid-week.
8. A final section naming the thing you would rather not write down.

## Constraints

- **300 to 400 words.** Long enough to be specific, short enough that you write
  it rather than putting it off. A reflection nobody writes is worth less than a
  short one that exists.

- **Question 4 gets one answer, not five.** A list of five intentions is a list
  of five things you will not do. One change, small enough to actually happen,
  is worth more than a manifesto — and you will write another of these at the
  end of Week 3, so there is room.

- **Question 4's answer must be checkable.** "Be more disciplined about
  Examine" is not checkable. "Write the cost section *before* I write the code,
  on all five Week 3 exercises" is: on Wednesday you can look and see whether it
  happened. If a stranger could not tell from your repo whether you did it, it
  is not specific enough.

- **Answer question 1 from the files, not from memory.** People consistently
  remember their later write-ups as better than they are, because the *thinking*
  got better even where the writing did not. Open both.

- **The uncomfortable section is not optional.** It is the section that makes
  the other four honest, because writing it forces the rest to be true. If you
  genuinely had a clean week, say what you nearly skipped and why you did not.

- **Nobody grades this but you.** Which means the only way it fails is by being
  flattering. A reflection that says "I learned a lot and feel more confident"
  is a reflection you will get nothing from in Week 9 when you re-read it
  looking for the moment something started going wrong.

## Expected output

There is no program here, so the output is the reflection. This is what an
honest one looks like — yours will be about your week, and the specificity is
what transfers:

```text
# Week 2 reflection -- Complexity and hash maps

*Written 2026-03-01, before starting Week 3.*

## 1. Did my cost sections actually get better?

Partly, and less than I thought. Exercise 1's section is four short
paragraphs and names the sort-and-two-pointers alternative with its
complexity. Exercise 5's is longer and has the disjointness argument in it,
which Exercise 1 could not have had. But Exercises 3 and 4 are nearly the
same text with the nouns swapped -- both say "no meaningful spread" without
checking, and Exercise 4 does have a real best case at (0,1). I templated
by Wednesday and did not notice until I read them side by side just now.

## 2. Which sub-shape felt natural, and which felt forced?

Set membership was immediate; by Exercise 5 I was reaching for a set before
finishing the problem statement. The canonical key in Exercise 3 felt
forced, and re-reading it I do not think the structure was the problem --
it was that I had to invent the key rather than being handed one. That is a
different skill and I have done it about twice.

## 3. The five-piece structure: useful or formulaic?

Both, and the order matters. It was annoying on Exercise 1 because I had
nothing to put in three of the pieces. By Exercise 5 it was the reason I
noticed I could not defend the O(n) claim -- the tradeoff piece made me
write down the alternative, and writing it down showed me I had not thought
about it. I would keep it.

## 4. One specific thing I will do differently in Week 3

Write the cost section before the code, on all five exercises. If I cannot
state the complexity before implementing, I have not finished Assess
options.

## The thing I would rather not write down

I did not record Exercises 3 or 4 at all, and told myself it was because
they were medium rather than hard.
```

Read what makes that useful. Question 1 is answered from the files and finds
something the writer did not expect. Question 2 diagnoses *why* rather than
naming a preference. Question 3 changes its mind mid-answer. Question 4 is one
thing and it is checkable. And the last line is the one that makes the rest
believable.

## Steps

1. Open Exercise 1's write-up and Exercise 5's write-up side by side. Read both
   cost sections. Do not write anything yet.
2. Now open Exercises 3 and 4. Are they distinguishable from each other? That is
   the question people find uncomfortable, and it is the one worth asking.
3. Answer question 1, naming the specific drill where the quality changed —
   upward or downward.
4. Answer question 2. Push past naming a favourite: say what made the difference.
   "Canonical keys felt forced" is a preference; "canonical keys felt forced
   because I had to invent the key rather than being handed one" is a diagnosis,
   and a diagnosis tells you what to drill.
5. Answer question 3. If your view changed during the week, say where.
6. Answer question 4. Write three candidates, then delete two. Check the survivor
   against the test: could somebody tell on Wednesday?
7. Write the uncomfortable line last, in one sentence, and do not soften it.
8. Commit. Then, and only then, open Week 3.

## The Solution

The finished reflection is the block under **Expected output**. Yours will be
about a different week; what transfers is the four moves below.

**Answer question 1 from the files.** Everybody remembers their later work as
better, because the *thinking* improved even in weeks where the writing did not.
Reading Exercise 1 and Exercise 5 back to back takes four minutes and is the
only way to find out. The common discovery — and it is worth expecting — is that
the first and last are genuinely different and the three in the middle are one
template. That is not a failure; it is a normal thing that happens when a
structure becomes comfortable, and noticing it is what stops it happening again
in Week 3.

**Diagnose, do not report a preference.** "Frequency maps felt natural, canonical
keys felt forced" is an observation. "Canonical keys felt forced because I had
to invent the key, and I have only done that twice" is a diagnosis, and a
diagnosis has an action attached: drill key invention. Every question here is
worth turning from a feeling into a cause, because only the cause tells you what
to do next.

**One change, and make it checkable.** The reason for one is arithmetic: you
will write fifteen of these reflections, and one change a week compounds while
five a week produces a list you stop reading by Week 4. The reason for checkable
is that an intention nobody can verify is an intention you can quietly not have
had. "Write the cost section before the code" passes: on Wednesday, the commit
order says whether you did.

**The uncomfortable line is the load-bearing one.** Not because confession is
virtuous, but because writing it changes what the other four answers can be. It
is very hard to write "I did not record Exercises 3 or 4" and then claim in
question 1 that your Examine discipline was strong. The last section keeps the
first four honest, which is the only property that makes any of this worth
re-reading in Week 9.

**On re-reading these later, which is the actual payoff.** In Week 9, when
something is not landing, the fifteen-week set of reflections is the record that
tells you when it started. A run of "my cost sections are getting shorter" from
Weeks 5 to 8 is a finding you can act on. A run of "good week, feeling
confident" is nothing at all, and the past you who wrote it has left the present
you with no information. That is the whole argument for the honesty constraint,
and it is a selfish argument rather than a moral one.

## Download and run

There is no file to download. The deliverable is an account of your own week.

The check that matters is a re-reading, and it happens later. Set a reminder for
the end of Week 3 and re-read this file then. Two questions:

- Did the one change in question 4 actually happen? The repo will tell you.
- Is the thing you would rather have written down still true?

For a check today, hand the file to somebody in your cohort and ask them what
you should drill next. If they can answer from the reflection alone, it is
specific enough. If they say "sounds like it went well", it is not.

```bash
sed -n '/^## 4/,$p' study-plan/week-02-reflection.md
```

That last section is the one to read aloud. If saying it out loud is
comfortable, it is probably not the true one.

## Common bugs to catch

- **"I learned a lot and feel more confident."** The most common failure, and it
  contains no information. In Week 9 it will tell past-you nothing about
  present-you. Replace every general claim with a specific one — which drill,
  which sub-shape, which day.

- **Answering question 1 from memory.** You will report improvement, because the
  thinking improved. Open both files. The middle three drills are where the
  surprise usually is.

- **Five things in question 4.** A list of five intentions is a list of five
  things that will not happen. Delete four. There is another reflection at the
  end of Week 3.

- **An uncheckable change.** "Be more rigorous" cannot be verified on Wednesday
  and therefore cannot be failed, which is exactly what makes it comfortable to
  write. "Write the cost section before the code, on all five exercises" can be.

- **Naming a preference instead of a cause in question 2.** "I liked sets" tells
  you nothing to do. "Sets were easy because the key was handed to me, and
  inventing a key was the hard part" tells you what to drill.

- **Skipping the uncomfortable section.** Without it, the other four answers
  drift towards the flattering version without you noticing, because nothing is
  holding them to account.

- **Writing it after starting Week 3.** By then Week 3 has coloured your memory
  of Week 2, and the sequence of reflections stops being a clean record. Write
  it before you open the next week's README.

- **Being harsh instead of accurate.** The opposite failure and less common, but
  it exists. "I was terrible at all of it" is as uninformative as "it went
  well". The target is accuracy, not severity.

## Under the hood

<details>
<summary>Under the hood — why written reflection beats remembered reflection, and what the fifteen-file set is for</summary>

**Memory rewrites itself towards the story you are currently telling.** By the
end of Week 3, your memory of Week 2 will have been quietly edited to be
consistent with how Week 3 went. If Week 3 goes well, Week 2 becomes the week
things clicked. If Week 3 goes badly, Week 2 becomes the week you were already
struggling. Neither is a record. A file written on the day, before the next week
starts, is the only version that survives the edit — which is why the timing
constraint is a constraint rather than a suggestion.

**Why four questions and not an open prompt.** "How did the week go?" produces a
paragraph about feelings, reliably. Specific questions produce specific answers,
and specific answers are the only kind you can act on or compare. The four here
are chosen to cover the week's two skills (cost sections, hash-map sub-shapes),
your view of the method itself, and one forward-looking commitment. That last
one is what makes the file useful rather than merely tidy.

**What the fifteen-file set is actually for.** Individually, each reflection is
worth about half an hour. Collectively, they are a longitudinal record of your
own learning, and that is a genuinely rare thing to own. Three specific uses:

- **Diagnosis.** In Week 9, when something is not landing, you can read
  backwards to find where it started. "My cost sections got shorter every week
  from 5 onwards" is actionable. Nobody can reconstruct that from memory.
- **Interview material.** "Tell me about how you learn" is a real question, and
  a candidate who can describe an actual practice with actual findings — "I
  noticed in Week 2 that I had started templating my complexity write-ups, so I
  changed how I ordered the work" — is answering with evidence rather than with
  a claim about themselves.
- **The visible trajectory.** A portfolio where Week 15 looks like Week 1 shows
  a constant skill level over fifteen weeks. The reflections are the narrative
  that makes the trajectory legible, and they cost forty-five minutes a week.

**On the honesty constraint, argued selfishly.** There is a moral version of
this argument and it is not the persuasive one. The persuasive one is that a
flattering reflection is a *corrupted measurement*, and a corrupted measurement
is worse than none, because you will act on it. If Week 2's file says the
Examine discipline was strong when in fact you stopped recording on Wednesday,
then in Week 5 you will look for the problem somewhere else entirely and not
find it. The reflection is an instrument. Fudging an instrument does not make
the machine work better.

**One practical note.** Write the uncomfortable section last, and do not edit
it. First drafts of that sentence are almost always more accurate than second
ones, because the second draft is where the softening happens.

</details>

## Acceptance checklist

- [ ] `study-plan/week-02-reflection.md` exists in your portfolio repo.
- [ ] It is dated and was written **before** you opened Week 3.
- [ ] Between 300 and 400 words.
- [ ] All four questions answered under their own headings, in order.
- [ ] Question 1 was answered after re-reading Exercise 1's and Exercise 5's
      write-ups, and names something concrete.
- [ ] Question 2 names one natural sub-shape and one forced one, with a cause
      rather than a preference.
- [ ] Question 3 says why, and says whether your view changed during the week.
- [ ] Question 4 names exactly one change, and somebody could check on Wednesday
      whether you did it.
- [ ] The final section names the thing you would rather not write down, in one
      unsoftened sentence.
- [ ] Nothing in the file is a general claim you could have written before the
      week started.
- [ ] Committed with a message like `Add Week 2 reflection`.

## Stretch

- **Set a reminder to re-read this at the end of Week 3**, and add two lines
  then: did the change in question 4 happen, and is the uncomfortable sentence
  still true? Two lines a week turns fifteen separate files into one continuous
  record, and the follow-up is where most of the value of the first entry
  actually arrives.

- **Listen to your Exercise 1 and Exercise 5 recordings back to back**, if you
  made them. Exercise 5's cost narration should be markedly more confident. If
  it is not, that is a finding worth a sentence in question 1 — and if you did
  not record either, that is a more useful finding still, and it belongs in the
  last section.

- **Write the one-line version of the whole week**, and keep a running file of
  them. "Week 2: hash maps were easy, inventing keys was not, and I template
  under time pressure." Fifteen of those on one page, read end to end in Week
  15, is the single most useful artifact this course will produce for you — and
  it is one sentence a week.

---

That is the last of Week 2's homework. Back to the
[homework index](./README.md), and then the week's capstone: the
[mini-project](../mini-project/README.md).
