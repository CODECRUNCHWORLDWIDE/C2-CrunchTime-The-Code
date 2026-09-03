# Mini-Project — Mock Interview #1

<!-- no-runnable-file: the deliverable is a timed, recorded interview and a self-feedback write-up, not a program. There is no answer to publish here, because the artifact is a recording of the learner solving an unseen problem under a clock. -->

> **Topic:** the first recorded mock interview — the protocol, the clock, the recording, and the self-feedback that turns it into one change
> **Lecture:** [02 — The Mock Interview Protocol](../lecture-notes/02-the-mock-interview-protocol.md)
> **Difficulty:** Uncomfortable rather than hard
> **Target time:** 11 hours across Thursday to Sunday, of which exactly 45 minutes is the mock itself
> **Why this one:** three weeks of drills have built the patterns. This is where you find out which of them are actually in your hands and which are still on paper. Reading about FRAME is one thing; running it on an unseen problem, on a clock, with a recorder on your face, and then *watching yourself do it* — that is a different thing entirely, and there is no substitute for it.

## The Brief

This week's deliverable is not a program. It is a **45-minute recording of you
solving a problem you have never seen**, under interview conditions, plus a
written note that grades the recording honestly.

That is unusual enough to state plainly: there is no code to hand in for this
page, and no published answer, because the artifact is *you*.

**Why it works.** Drills are gentle in three ways at once. You are alone, the
clock is informal, and the problem is curated — you knew it was going to be a
sliding-window problem because it was in the sliding-window folder. A mock
removes all three softenings at the same time, and what happens next is data
you cannot get any other way.

Three things shift the moment those constraints land, and you should expect at
least one of them:

1. **You speed up.** You skip straight past choosing an approach and start
   writing code that fits a pattern you never actually checked.
2. **You go quiet.** Thinking out loud feels strange when somebody is listening,
   so you revert to silent problem-solving — the exact habit three weeks of
   drills have been unlearning.
3. **You get clumsy at recovering.** When the first approach hits a wall,
   drill-you would shrug and back out. Mock-you keeps pushing, because backing
   out feels like losing.

**The recording is the part people want to skip, and it is the part that
works.** Memory is generous. Recordings are not. In the first pass you will
discover you said things you do not remember saying and did not say things you
would have sworn you said. Calibrating what it *felt* like against what you
*did* is the entire mechanism.

**Mock #1 is a floor, not a ceiling.** It will be worse than you hope. That is
expected and it is fine. Mock #4 in Week 15 is what counts, and the distance
between the two is what this course is optimising. Mock #1's value is that it
gives that distance a starting point.

## Starter

There is no code to paste. What there is instead is a folder in your portfolio
repo, created on **Monday**, with one placeholder file committed so that the
work has somewhere to land.

```bash
mkdir -p mocks/mock-01
cat > mocks/mock-01/recording-link.md <<'EOF'
# Mock #1 recording

[Video — 45 min](<your private view-only link>)

Problem: TODO — name and link
Flavor: TODO — A (peer) / B (platform) / C (solo)
Date: TODO — YYYY-MM-DD
EOF
git add mocks/mock-01/recording-link.md
git commit -m "Track mock #1 deliverables"
```

Then the checklist that actually matters, and it is a Monday job. Every line of
it can fail, and every line of it takes minutes to fix on Monday and cannot be
fixed at all at 14:55 on Friday.

```text
[ ] Recording tool installed and tested — OBS, QuickTime, or your meeting app.
[ ] A 30-second test recording made and PLAYED BACK. Face visible? Screen
    sharp? Voice clear? Any background noise an interviewer would hear?
[ ] Coding environment chosen and bookmarked. Not your own configured editor —
    the friction of an unfamiliar shell is part of what is being tested.
[ ] A drawing tab open, for sketching a chain before writing code.
[ ] 55 minutes of quiet booked on the calendar. Notifications off, phone face
    down, door shut.
[ ] Water within reach. You will get thirsty, and a sip is a legitimate way to
    buy three seconds of thinking time.
[ ] Partner confirmed, platform slot booked, or the solo date written down.
```

**A warm-up you can run in the browser.** Before Friday, do one 10-minute
recorded pass on a problem you have already solved, so that the strangeness of
being recorded is out of the way before it costs you anything. Any of this
week's drills will do — open one in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-04-fast-slow-pointers-and-mock-1/exercises/exercise-01-conveyor-loop.md), start the recorder, and narrate. Nothing to install, nothing to
configure, and your work stays on your own machine.

## Requirements

1. A **45-minute recording** of you solving a problem you had not seen before,
   uploaded somewhere with a link you can share.
2. `mocks/mock-01/recording-link.md`, committed, with a working link and the
   problem, flavour and date filled in.
3. `mocks/mock-01/immediate-notes.md`, committed, written **within 30 minutes**
   of the clock stopping.
4. `mocks/mock-01/timestamps.md`, committed, with 10 to 15 observations from the
   first watching pass.
5. `frame-writeups/c2-week-04/mock-01-self-feedback.md`, committed, 600 to 800
   words, following the structure in The Solution below.
6. The self-feedback note contains **one** behaviour change for Mock #2, in one
   sentence, specific and testable.
7. The self-feedback note names at least **two specific failures**, each with a
   wall-clock timestamp.
8. The problem was genuinely unseen.

## Constraints

- **45 minutes, and the clock is hard.** When it hits 45 you stop, even
  mid-line. The recording can keep running for a wrap-up, but the solve ends.
  Real interviews end whether or not you are finished, and practising with a
  soft clock trains you to run over — which is the one failure mode that
  guarantees the Examine step never happens.

- **The problem must be one you have not seen.** This is the constraint that
  makes the exercise mean anything. A remembered problem tests recall, and
  recall is exactly what pattern recognition is supposed to replace. It is
  self-attested, and the recording tells on you anyway: your reaction in the
  first thirty seconds is visible.

- **Medium difficulty, not Easy and not Hard.** Easy sits below interview pace
  and produces a recording where nothing interesting happens. Hard, at Mock #1,
  usually produces 45 minutes of being stuck, which is a real interview
  experience but a poor first data point. You want a problem you can plausibly
  finish and might not.

- **The recording is mandatory, all three tracks if you can manage it — screen,
  voice, and face.** If your setup can only do two, keep screen and voice. The
  face track shows things the other two cannot, chiefly whether you are looking
  at the problem or at your hands, but it is not worth losing the mock over.

- **Do not commit the video file.** Even compressed, 45 minutes is hundreds of
  megabytes and git will hold it forever. The link is the artifact.

- **Solo mode is acceptable for Mock #1 only.** Mocks 2, 3 and 4 need a real
  partner or a platform. By Week 9 you should have found one — start looking
  this week, because that is the part with a lead time.

## Expected output

There is no program, so what follows is a worked excerpt rather than captured
stdout: a real-shaped piece of `timestamps.md` from a first watching pass, and
the two lines of `immediate-notes.md` that fed it.

```text
--- immediate-notes.md, written 6 minutes after the clock stopped ---

Felt rushed the whole way through. I think I started coding before I had
actually decided on the approach — I remember saying "so this is basically a
hash map problem" and then just going. Definitely went silent at some point in
the middle, no idea how long. Caught a bug near the end and fixed it without
saying anything about it. Never got to complexity out loud.

--- timestamps.md, first pass at 1.5x ---

[00:40]  Read the prompt aloud. Good.
[01:10]  Asked one clarifying question, then answered it myself before the
         interviewer could. Did not wait.
[02:05]  Named the pattern in 8 seconds and started typing at 02:20. No
         structural check, no example walked.
[06:10]  Silence begins.
[06:51]  Silence ends. 41 seconds, typing throughout.
[11:30]  Realised the loop guard was wrong. Fixed it silently. Interviewer saw
         the diff, heard nothing.
[19:45]  Interviewer asked "what happens if the list is empty?" — I had not
         considered it. Good catch by them, bad miss by me.
[27:00]  Started tracing an example. First trace of the whole session.
[31:20]  Second bug found by the trace. Said this one out loud. Better.
[38:00]  Interviewer prompted for complexity. I had not started it.
[41:30]  Gave time complexity. Never gave space.
[44:50]  Stopped mid-sentence on the clock. Correct.
```

Notice what makes those useful: every line has a timestamp, the silences are
measured rather than described, and the two entries that record something going
*well* are as specific as the ones that do not.

## Steps

1. **Monday — set up the rig, one hour.** Work down the checklist in Starter,
   in order. Make the 30-second test recording and *play it back*. Book the
   slot. Message a partner. Create `mocks/mock-01/` and commit the placeholder.
2. **Tuesday or Wednesday — the pre-mock, thirty minutes.** Pick a problem you
   have already solved. Ten-minute timer, recorder on, narrate FRAME start to
   finish. Watch it back. The only goal is to spend your "I am being recorded"
   awkwardness on a problem that does not matter.
3. **Thursday — final prep, ninety minutes.** Re-read
   [Lecture 2](../lecture-notes/02-the-mock-interview-protocol.md), especially
   its pre-mock checklist and its 45-minute shape. Confirm the rig still works.
   Confirm the partner is still confirmed.
4. **Friday — the mock.** Show up. Hit record. Run FRAME out loud, all five
   steps. Stop at 45 minutes.
5. **Friday, immediately after — the five-minute window.** This is the
   most-skipped step in the whole protocol and it is irrecoverable. Open a file,
   set a five-minute timer, and free-write what is still fresh. What surprised
   you? What felt automatic? What felt clumsy? Did you go silent? Do not grade
   anything — just capture. Save as `mocks/mock-01/immediate-notes.md` and
   commit. Then upload the recording and fill in `recording-link.md`.
6. **Saturday, first pass — the whole recording at 1.5x, about 30 wall-clock
   minutes.** Keep a file open and drop a timestamped line every time you notice
   a *pattern* — not every "um". Aim for 10 to 15. Save as
   `mocks/mock-01/timestamps.md` and commit.
7. **Saturday, second pass — only the flagged moments, at normal speed.** For
   each one write a sentence describing what happened and a sentence prescribing
   what to do instead. Observation, then prescription. Do not editorialise, do
   not catastrophise.
8. **Saturday — write the self-feedback note**, using the structure in The
   Solution. Then score it against the rubric there, and sharpen anything that
   reads as vague or generous.
9. **Sunday — close Phase 1.** Add a paragraph to
   [the retrospective](../homework/problem-06-phase-1-retrospective.md) about
   what Mock #1 specifically showed, and cross-reference the self-feedback note.

## The Solution

There is no published answer here, and that is not an omission — the deliverable
is a recording of you solving an unseen problem, so any answer this page could
publish would either be about a different problem or would spoil the one you are
about to be given. What *can* be published is the structure of the self-feedback
note, which is the graded artifact, plus the rubric it is graded against.

```markdown
# Mock #1 — Self-Feedback

**Date:** YYYY-MM-DD
**Problem:** [name and link]
**Flavor:** A (peer) / B (platform) / C (solo)
**Duration:** 45 minutes, hard stop
**Outcome:** [solved / solved with a bug / did not finish]
**Recording:** [link]

## What I felt during the mock

[3-5 sentences, honest, from the immediate notes. "I felt rushed during the
approach." "I went silent for about two minutes around the 18-minute mark."
"I caught the off-by-one but never said what the fix was."]

## What the recording shows

[5-8 observations from the second pass, each with a wall-clock timestamp.
This section exists to be compared against the one above it.]

## Choosing the approach — graded

[Was the pattern named in under 30 seconds? Did it name the pattern, the
algorithm, the auxiliary state, and one thing it was NOT? Did a structural
check happen before the commitment, or did a keyword fire? Quote yourself from
the recording if you can.]

## Thinking aloud — graded

[Did I go silent? When, and for how long, measured? Did I narrate any pauses?]

## Recovery — graded

[When the first approach hit a wall, did I say so out loud and back out, or did
I keep pushing quietly?]

## Examine — graded

[Did I trace an example before declaring it done? Did I give time AND space
complexity? Did I name what the rejected approach was better at?]

## ONE behavior change for Mock #2

[One sentence. Specific. Testable. "I will narrate every pause longer than five
seconds" is good. "I will be more confident" is not — it cannot be checked.]

## What I am NOT going to change

[One or two things you noticed and are deliberately leaving alone. This section
prevents over-correction, which is the failure mode of taking feedback well.]
```

**The structure is the rubric.** Grade yourself against these five axes, and be
harder on yourself than feels comfortable:

| Axis | Weight | What "great" looks like |
|---|---:|---|
| Honesty | 30% | At least two specific failures named, from the recording. Vague optimism is the red flag. |
| Specificity | 25% | Every observation carries a timestamp. "I went silent" is bad; "18:30–20:15, silent typing through the loop body" is good. |
| Approach critique | 15% | The pattern choice's length, content and cadence are all graded. Pull the actual words. |
| Thinking-aloud critique | 15% | Silences are measured, not described. Narrated pauses are noted as the win they are. |
| Behaviour change is testable | 15% | One sentence, checkable by watching the next recording. |

**Why the "what I felt" section comes before "what the recording shows".** So
you can compare them. The distance between the two is the single most useful
thing this exercise produces, and putting the felt version second would let the
recording quietly overwrite the memory before you had measured the gap.

**Why silences must be measured rather than described.** "I went quiet for a
bit" is unfalsifiable and cannot be improved against. "41 seconds, 06:10 to
06:51" can be checked in Mock #2, and that is the entire difference between a
note and a baseline.

**Why exactly one behaviour change.** You will find ten things wrong. You will
want to fix all of them by Week 9. You will fix none. One specific, testable
change, repeated until it is automatic, is how this actually moves — and it is
the same discipline as the "exactly three additions" rule in
[Problem 5](../homework/problem-05-system-design-warmup.md).

**Why there is a section for what you are *not* changing.** Over-correction is
the failure mode of people who take feedback seriously. If you noticed you say
"um" a lot, the right decision is usually to leave it: it is polish, not
substance, and spending Mock #2 monitoring your filler words costs you the
attention that should be on the problem. Writing the decision down is what stops
it drifting back.

**Why one mock and not two.** The self-feedback discipline is the high-leverage
half, and doing it well once beats doing it badly twice. By Mock #2 in Week 9
you will also have five more weeks of patterns, so the second mock differs from
the first on both axes at once. One mock. A real one. Full feedback. Move on.

## Download and run

There is nothing to download and nothing to run — the artifact is a recording of
you, and the only file that could be published here would be someone else's
answer to a problem you have not been given yet.

What you can run, and should, is the week's drill harness — before Friday, so
that the patterns are as warm as they are going to get:

```bash
cd ../exercises
C2_WEEK04_SOLUTIONS=my_week04_solutions pytest timed_runner.py -v
```

That grades your own five drills and both challenges against the week's larger
and nastier cases. See [`timed_runner.py`](../exercises/timed_runner.py) for the
full case list and for how to point it at whichever module holds your work.

And on the day, this is the only command that matters:

```bash
# Start the recorder. Then set the clock.
#   45:00 — hard stop
```

## Common bugs to catch

- **Skipping the five-minute window.** The commonest failure and the only
  unrecoverable one. By evening the freshness is gone and `immediate-notes.md`
  becomes a reconstruction rather than a record — which defeats the entire
  point of comparing it against the recording later. Set the timer before you
  close the laptop.

- **Self-feedback that flatters.** Symptom: "went well overall, just need more
  practice." Nothing in that sentence can be acted on. If you catch yourself
  writing it, go and re-watch one of the rough segments at normal speed and try
  again.

- **Observations with no timestamps.** Symptom: "I felt rushed." Unfalsifiable,
  and useless in Week 9 when you want to know whether it got better. Every line
  in the recording-shows section gets a clock reference.

- **A behaviour change that cannot be tested.** Symptom: "be more confident",
  "talk more", "solve faster". None of those can be checked by watching a
  recording. Rewrite until the change is something an observer could tick off.

- **Picking a problem you have seen.** Symptom: the first two minutes of the
  recording are smooth in a way the rest is not. You have tested your memory,
  not your pattern recognition, and the whole 45 minutes measures nothing.

- **Letting the clock slide.** Symptom: the recording is 58 minutes long.
  Finishing late is finishing not-at-all in a real loop, and — worse — the extra
  minutes always come out of the Examine step, which is the part most candidates
  already skip.

- **Committing the video.** Symptom: a repository that takes four minutes to
  clone. Upload it, link it, and keep the repo text.

- **Doing the mock and stopping there.** Symptom: a recording, no write-up. The
  recording without the self-feedback is 45 minutes spent for almost nothing —
  the value is in the watching, not in the doing.

## Under the hood

<details>
<summary>Under the hood — why watching yourself is so unpleasant, and what the research actually says</summary>

**The first viewing is the worst one, reliably.** Watching a recording of
yourself is called self-confrontation in the psychology literature, and the
consistent finding across performance training is that the first exposure
produces a strong negative reaction that fades quickly with repetition. People
hate the sound of their own voice — partly a genuine acoustic effect, because
you normally hear yourself through bone conduction, which adds low frequencies
the recording does not have. Knowing that the first watch is the hardest is
worth something on Saturday morning.

**Why the second pass has to be at normal speed.** The first pass at 1.5x is for
finding *where* things happened; you are scanning. The second pass is for
hearing *what* happened, and speech at 1.5x systematically flattens hesitation,
pace and tone — the exact things you are grading. Do not merge the two passes to
save time. They are looking for different things.

**Observation before prescription, and why the order matters.** Writing "I went
silent because I was panicking" merges a fact with a theory, and the theory is
usually wrong and always harder to act on. "18:30 to 20:15, silent" is a fact.
"Next time, say what I am thinking about before I start typing" is a
prescription. Keeping them in separate sentences is what makes the second one
checkable.

**The one-change rule is not modesty, it is arithmetic.** Deliberate change to a
performed behaviour needs attention, and attention during a 45-minute problem is
already fully committed to the problem. One change can be held in the background
and eventually becomes automatic. Three cannot, and the usual result is that
none of them happen and the problem gets solved worse as well.

**What mocks measure that drills cannot.** Drills measure whether you can do the
thing. Mocks measure whether you can do the thing *while also* narrating,
managing a clock, and handling being watched. Those are separate capacities and
they do not transfer automatically — which is why "I'll do mocks once I've
drilled more" is backwards. The drills make the pattern cheap so that the mock
has spare attention to spend on everything else.

**Where the recording pays off later.** In Week 15, before Mock #4, you will
watch Mock #1 again. That comparison is the clearest evidence you will get that
the course worked, and it is only available if Mock #1 was recorded honestly —
including the parts you would rather not have on film. A polished baseline makes
the improvement look smaller than it was.

</details>

## Acceptance checklist

- [ ] A 45-minute recording exists and is uploaded somewhere accessible.
- [ ] `mocks/mock-01/recording-link.md` is committed, with a working link and
      the problem, flavour and date filled in.
- [ ] `mocks/mock-01/immediate-notes.md` was written within 30 minutes of the
      clock stopping, and is committed.
- [ ] `mocks/mock-01/timestamps.md` has 10 to 15 observations from the first
      pass, and is committed.
- [ ] `frame-writeups/c2-week-04/mock-01-self-feedback.md` is committed, 600 to
      800 words, following the published structure.
- [ ] The self-feedback names at least two specific failures, each with a
      timestamp.
- [ ] The behaviour change is one sentence and could be checked by watching the
      next recording.
- [ ] There is a "what I am not going to change" section, and it is not empty.
- [ ] The problem was genuinely unseen.
- [ ] The raw video is **not** in git.
- [ ] You scored yourself against the five-axis rubric and sharpened anything
      vague.

## Stretch

- **Interview someone else.** If you ran Flavor A, you already have. If you did
  not, find one person and give them 45 minutes as the interviewer. Sitting on
  the other side of the table is the fastest way to discover which candidate
  behaviours are actually visible — and how obvious silent coding looks from
  outside.

- **Transcribe your first two minutes, word for word.** It takes ten minutes and
  it is uncomfortable. What you are looking for is how many words went by before
  you said anything about the *structure* of the problem, and whether the
  clarifying question you asked was answered by the interviewer or by you.

  ```text
  0:00-0:38  reading aloud
  0:38-0:52  restating, mostly accurate
  0:52-1:04  asked "can the list be empty?" and answered it myself at 0:58
  1:04-1:12  named a pattern
  1:12-      typing
  ```

- **Book Mock #2 now.** Not the session — the partner. The scarce resource in
  Week 9 is somebody else's calendar, and the people who end up doing Mock #2
  solo are the ones who started looking in Week 9. One message this week.

- **Write the one-line prediction.** In your self-feedback, before you finish,
  add a sentence predicting what Mock #2's recording will show about your one
  behaviour change. Then, in Week 9, check it. Predictions you wrote down and
  then verified are worth far more than either half alone — the same move the
  drills ask for when they tell you to predict the degenerate case in Frame and
  check it in Examine.

---

Phase 1 closes here. Push everything, send the self-feedback link — not the
video — to one peer for a second opinion, then start
[Week 5 — Binary Search Beyond Sorted Arrays](../../week-05-binary-search/).

The next time you do this, you will have eight more weeks of patterns under you.
