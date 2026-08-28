# Problem 6 — The Phase-1 Retrospective

<!-- no-runnable-file: this problem's deliverable is a written retrospective about the learner's own four weeks, not a program -->

> **Topic:** closing Phase 1 — an honest account of what is in your hands and what is not
> **Lecture:** [02 — The Mock Interview Protocol](../lecture-notes/02-the-mock-interview-protocol.md), §9
> **Difficulty:** Easy to write, hard to write honestly
> **Target time:** 60 minutes
> **Why this one:** this is the artifact future-you reads before Mock #3 in Week 14 and Mock #4 in Week 15. At that point, past-you's honest assessment of where the gaps were will be more useful than re-running any of the drills. Write it for that reader.

## The Brief

Phase 1 is over. Four weeks, four patterns, one recorded mock interview.

- Week 1 — two-pointer, and the FRAME method itself
- Week 2 — complexity and hash maps
- Week 3 — sliding window
- Week 4 — fast and slow pointers, and Mock #1

A retrospective is a short, honest write-up of what actually happened, written
while it is still fresh. Not a summary of what the course covered — you can read
that anywhere. A retrospective is about *you*: which things went in, which
things did not, and what you are going to do about it.

Read this Monday, not Sunday. Knowing the seven questions in advance changes
what you notice during the week, and that is the point of telling you now.

**Why the honesty matters mechanically, not morally.** In Week 14 you will have
two weeks left and a limited amount of time to spend. The only thing that makes
that time well spent is an accurate list of your weak patterns. A retrospective
that says "going well, need more practice" gives future-you nothing to act on,
and future-you will then spend a week re-drilling something already automatic
because it feels productive. The cost of a flattering retrospective is paid
later, by you, in the week before your interviews.

**Length: 500 to 700 words**, across seven questions. That is 70 to 100 words
each — enough for a specific answer, not enough for a general one.

## Starter

Create `study-plan/phase-1-retrospective.md` in your portfolio repo and paste
this in. Answer every `TODO`.

```markdown
# Phase 1 — Retrospective

**Weeks covered:** 1-4 (two-pointer, hash maps, sliding window, fast/slow)
**Written:** TODO (date)
**Mock #1:** TODO (date, flavor, link to the self-feedback note)

## 1. Which of the four patterns is most automatic in my hands?

TODO: name it, then name ONE specific problem from that pattern you can solve
cold in under 15 minutes. If you cannot name a specific problem, the pattern is
not the automatic one — pick again.

## 2. Which is least automatic?

TODO: name it, then name ONE specific problem where you still hesitate at the
point of choosing the pattern.

## 3. What has visibly improved across the four weeks of recordings?

TODO: watch, or at least skim, all of them. One behavior that has clearly
improved, and one that clearly has not. Timestamps if you have them.

## 4. What did Mock #1 show?

TODO: one thing the recording showed that you did not expect. One thing it
confirmed that you already suspected.

## 5. Where is pattern-matching in my hands now?

TODO: pick one word — fluent, mechanical, or rote — and defend it in two
sentences. The definitions are below in The Solution; read them before choosing.

## 6. My one behavior change for Mock #2 (Week 9)

TODO: one sentence. Specific. Testable. Copy it from your Mock #1 self-feedback
note rather than inventing a new one here — if it has changed since you wrote
that, say why.

## 7. Where am I with binary search, honestly?

TODO: Phase 2 opens with it next week. Honest options include: "comfortable on
sorted arrays, never tried the parametric version"; "I always get the loop
bounds wrong"; "I have not written one since university". Say which.

## The one thing future-me should read first

TODO: one sentence at the end, pointing Week-14 you at whichever answer above
matters most.
```

## Requirements

1. The file exists at `study-plan/phase-1-retrospective.md` in your portfolio
   repo.
2. All seven questions are answered, in order, under their own headings.
3. It is between 500 and 700 words.
4. Questions 1 and 2 each name a **specific problem**, not just a pattern.
5. Question 3 is based on actually looking at the recordings, not on memory.
6. Question 6's behaviour change is one sentence, specific and testable.
7. There is a closing line pointing future-you at the most important answer.
8. It is committed and pushed, because an artifact you cannot find in Week 14 is
   not an artifact.

## Constraints

- **500 to 700 words, which is about 70 to 100 per question.** Short enough that
  you cannot pad, long enough that a one-word answer will look obviously thin
  next to the others. The length is doing work: it is the smallest size at which
  vagueness becomes visible.

- **Questions 1 and 2 must name a specific problem, not a pattern.** "Sliding
  window is my strongest" is unfalsifiable. "I can do Week 3's shortest-kit-span
  cold in twelve minutes with the Frame step narrated" is a claim you could be
  held to, and holding yourself to claims is the whole exercise.

- **Question 3 requires you to actually watch.** Memory is generous and
  recordings are not — you already learned this during Mock #1's second pass.
  Skim all four weeks at 2x if you must, but look. An answer written from memory
  will be about how you *felt*, and the retrospective is supposed to be about
  what you *did*.

- **Question 6 must match your Mock #1 self-feedback note.** If you invent a
  fresh behaviour change here, you now have two and you will follow neither. If
  it genuinely changed after you thought about it more, say so and say why —
  that is a legitimate reason and a documented one.

- **No plans in this document beyond question 6.** A retrospective that turns
  into a study plan stops being a record of what happened. One behaviour change
  is the plan. Everything else here is evidence.

## Expected output

There is no program here, so what follows is a worked excerpt rather than
captured stdout: questions 2 and 3 from a retrospective that would be useful to
its author in Week 14. The details are invented; yours must not be.

```text
## 2. Which is least automatic?

Sliding window, and specifically the variable-size shape where the window has
to shrink. I can write the fixed-size version without thinking. On Week 3's
shortest-catchment drill I sat for four minutes before committing to a pattern,
because "shortest" made me reach for binary search first. I do not have a
reliable tell for "shrink from the left while the invariant holds" — I recognise
it after I have started writing, not before.

## 3. What has visibly improved across the four weeks?

Improved: I now say the complexity claim out loud without being prompted. In
Week 1's recordings I said it twice out of five drills, and both times at the
very end after a pause. In Week 4 I said it in all five, and in exercise 5 I
said it before writing any code, as part of choosing the approach.

Not improved: I still go silent while typing. Week 1, drill 3: 41 seconds of
silence at 06:10. Week 4, exercise 4: 55 seconds at 09:30. It has got slightly
worse, and I think it is because the problems got longer rather than because my
habit changed.
```

Three things make that excerpt useful in ten weeks' time. It names the exact
sub-shape of the weak pattern rather than the pattern. It cites timestamps, so
the claim is checkable. And it reports a regression without flinching, which is
the part most people leave out.

## Steps

1. **Read this page on Monday.** The questions change what you notice during the
   week, which is most of their value. Answering them on Sunday from a blank
   memory is a much weaker exercise.
2. **Sunday, first: gather.** Open your four weeks of FRAME write-ups and your
   four weeks of recordings. Put the Mock #1 self-feedback note beside them.
   Nothing to write yet.
3. **Skim all four weeks of recordings.** 2x is fine. You are looking for two
   things only: one behaviour that has clearly changed and one that has not.
   Note timestamps as you go — you will not find them again later.
4. **Answer questions 1 and 2 by looking, not remembering.** Go through your
   write-ups and find the drills where you hesitated. Hesitation is usually
   visible in the write-up as a Research-constraints section that is longer than
   the others, or an Assess-options section written after the code.
5. **Answer 3 and 4 from the recordings and the self-feedback note.**
6. **Read the three definitions in The Solution before answering 5.** The words
   are used precisely here and the distinction is the useful part.
7. **Copy question 6 from your Mock #1 note.** Do not invent a new one.
8. **Answer 7 in one honest sentence.** Nobody is grading it, and Week 5 starts
   in a day.
9. **Cut to 700 words, then write the closing line.** The closing line is the
   one future-you reads first, so write it last, once you know what the document
   actually says.
10. **Commit and push.**

## The Solution

There is no program here and no correct set of answers — the deliverable is an
honest account of your own four weeks. What can be published is the vocabulary
question 5 depends on, and a worked example of the two answers people most often
get wrong.

**The three words in question 5, defined precisely.**

- **Rote** — automatic without thinking. You see a keyword, the pattern fires,
  and you start writing. This is fast and it is dangerous: under pressure it
  produces confident wrong matches, because the keyword fired and the structure
  was never checked. The quiz's phone-tree question and its build-dependency
  question are both built to catch rote matching.
- **Mechanical** — automatic *with* a check. The pattern comes to mind quickly,
  and then you verify the structural property before committing: one outgoing
  edge per node, contiguous slice, sorted input. This is the target. It is fast
  enough for a 45-minute interview and it does not misfire.
- **Fluent** — mechanical, plus able to bend. You recognise the pattern, check
  it, and can also say what would have to change about the problem for a
  different pattern to be right. This is where you want to be by Week 15, and
  almost nobody is there at the end of Phase 1.

Most people finishing Phase 1 are somewhere between rote and mechanical, and
being able to say *which* — and on which patterns — is what makes the answer
worth reading later.

```markdown
## 5. Where is pattern-matching in my hands now?

Mechanical on fast/slow and on hash maps; rote on sliding window. On fast/slow I
now check the structural property out loud — one outgoing edge per node — before
naming the pattern, and in Week 4's quiz that check is what stopped me matching
the build-dependency question. On sliding window I still fire on the word
"contiguous" and start writing, which is exactly how I got the shortest-catchment
drill wrong the first time.

## 6. My one behavior change for Mock #2 (Week 9)

I will narrate every pause longer than five seconds, out loud, starting with
"let me think about X for a moment" — same sentence as in my Mock #1 note,
unchanged.
```

**Why naming the pattern-by-pattern state beats one overall verdict.** "I am
mechanical" is an average, and averages hide exactly the thing you need. Two
patterns mechanical and one rote is a completely different study plan from three
patterns evenly mediocre, and only the first version tells Week-14 you where to
spend a day.

**Why question 6 says "unchanged".** It is a small word doing real work. It tells
future-you that the behaviour change was thought about twice and survived, which
is a much stronger signal than a change invented in a hurry on Sunday night.

**Why the retrospective ends with a pointer.** In Week 14 you will open this
file with about four minutes of attention. The closing line is what makes those
four minutes land on the right paragraph. Write it as an instruction to a
stranger, because in ten weeks that is roughly what you will be.

**What a bad retrospective looks like, so you can recognise yours.** All seven
answers about the same length, no specific problem named anywhere, question 3
answered from memory, question 5 answered "mechanical" with no defence, and a
behaviour change that is not testable. It reads fine. It is worth nothing in
Week 14, and the only person who loses is the person who wrote it.

## Download and run

There is nothing to download and nothing to run — the deliverable is your own
account of your own four weeks.

From your portfolio repo:

```bash
wc -w study-plan/phase-1-retrospective.md
```

Confirm it is between 500 and 700 words, then commit and push, because an
artifact you cannot find in Week 14 is not an artifact:

```bash
git add study-plan/phase-1-retrospective.md
git commit -m "Add Phase 1 retrospective"
git push
```

## Common bugs to catch

- **Flattery.** Symptom: every answer is positive, and question 3's "has not
  improved" half is missing or hedged. This is the most common failure and it is
  the expensive one. Fix: go back to the recordings. There is always something
  that has not improved.

- **Patterns named without problems.** Symptom: questions 1 and 2 name four
  patterns and no problems. Fix: open your write-ups and find the actual drills.
  If you cannot find one you can solve cold, that is itself the answer to
  question 1 and you should say so.

- **Question 3 answered from memory.** Symptom: no timestamps, and the answer is
  about how you felt rather than what you did. You already know from Mock #1's
  second pass that memory and recording disagree. Watch.

- **A new behaviour change invented for question 6.** Symptom: it does not match
  your Mock #1 note. Two behaviour changes means zero behaviour changes. Fix:
  copy the original, or explain the revision.

- **Question 5 answered "mechanical" with no defence.** Symptom: one word and
  nothing after it. Everyone thinks they are mechanical. The two sentences of
  evidence are the whole answer.

- **Dishonesty on question 7.** Symptom: "comfortable with binary search" from
  somebody who last wrote one at university. Week 5 starts in a day and the
  lecture is pitched at whatever you say here. Nobody is grading it; the only
  person affected is you, next week.

- **A retrospective that turns into a plan.** Symptom: 300 words of "in Phase 2
  I will…". Cut it. One behaviour change, and the rest is evidence.

## Under the hood

<details>
<summary>Under the hood — why retrospectives drift positive, and what the four-week point is really measuring</summary>

**Retrospectives drift positive for a reason that has nothing to do with
character.** You are reconstructing four weeks from memory, and memory
reconstructs toward the story you currently believe. If you believe Phase 1 went
well, the drills you remember are the ones that went well; the four minutes of
silence before choosing a pattern is not stored as an event at all, because at
the time it did not feel like one. This is why question 3 forces you back to the
recordings. The recording is the only part of this document that is not being
generated by the same brain that is grading it.

**Four weeks is roughly where the first honest plateau shows up.** The first two
weeks of any new skill improve quickly, because the improvement is mostly
learning the vocabulary and the format. Weeks three and four are where the
actual difficulty appears and progress feels like it stops. It has not — but the
gains have moved from "I know what a sliding window is" to "I recognise one in
twenty seconds instead of ninety", and that second kind of gain is nearly
invisible from the inside. Expect the retrospective to feel worse than the four
weeks actually were.

**What Mock #1 is a baseline for.** Nothing in Phase 1 is measured against other
people, and Mock #1's absolute quality is close to irrelevant. What matters is
the delta to Mock #4 in Week 15, and a delta needs two points. That is the only
reason Mock #1 is graded honestly rather than kindly: a flattering baseline
makes the improvement look smaller than it was, which is a strange way to be
unkind to yourself.

**Why the retrospective is a homework problem rather than a suggestion.** Written
reflection that is optional does not happen, and written reflection that happens
weeks later is memory rather than record. Putting it in the same week as the
mock, with a word count and a checklist, is the only reliable way to get a
document that exists and is specific. The same reasoning is why the mock's
immediate-notes step has a five-minute timer.

**One thing that is genuinely worth doing but is not on the checklist.** Read
your Week 1 FRAME write-up, all the way through, before you write this. It is
four weeks old, it will read as if someone else wrote it, and the difference
between that person and you is the thing this document is trying to measure. It
takes ten minutes and it will change several of your answers.

</details>

## Acceptance checklist

- [ ] `study-plan/phase-1-retrospective.md` exists, is committed, and is pushed.
- [ ] All seven questions are answered under their own headings, in order.
- [ ] It is between 500 and 700 words.
- [ ] Questions 1 and 2 each name a specific problem, not just a pattern.
- [ ] Question 3 cites at least one timestamp from an actual recording.
- [ ] Question 3 names something that has **not** improved.
- [ ] Question 5 picks one of rote, mechanical or fluent, and defends it in two
      sentences.
- [ ] Question 6 matches your Mock #1 self-feedback note, or explains the change.
- [ ] Question 7 is honest.
- [ ] There is a closing line pointing future-you at the most important answer.

## Stretch

- **Add a one-paragraph note about Mock #1 specifically**, cross-referenced from
  your `frame-writeups/c2-week-04/mock-01-self-feedback.md`. The
  [mini-project](../mini-project/README.md) asks for this on Sunday, and doing
  it here keeps the two documents pointing at each other.

- **Write the sentence you would want to be able to say in Week 15.** One line,
  about where your pattern-matching will be by then. Then note what would have
  to be true for it to be sayable. That is a plan disguised as a prediction, and
  it is the one piece of forward-looking content this document earns.

  ```text
  Week 15: "I recognise the pattern within 30 seconds on all eight Phase-1
  and Phase-2 families, and I check the structural property before committing."
  For that to be true: sliding window has to move from rote to mechanical,
  which means drilling the shrink-shaped variants specifically, not more
  windows in general.
  ```

- **Diary the four weeks in one line each.** Not required, and unreasonably
  useful in Week 14:

  ```text
  W1  learned the format; forgot to state complexity in 3 of 5 drills
  W2  hash maps clicked immediately; complexity claims got much better
  W3  hardest week; sliding window still not reliable
  W4  fast/slow clicked; first mock was worse than I expected and that is fine
  ```

That closes the homework, and with the [quiz](../quiz.md) and the
[mini-project](../mini-project/README.md) it closes Phase 1. Next:
[Week 5 — Binary Search Beyond Sorted Arrays](../../week-05-binary-search/).
