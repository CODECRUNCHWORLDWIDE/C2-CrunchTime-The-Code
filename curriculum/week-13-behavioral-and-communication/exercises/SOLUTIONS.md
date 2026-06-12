# Week 13 — Exercise Solutions

Exemplar STAR answers and per-exercise rubrics. **Draft your own answer first.** These exemplars are drawn from fictional-but-realistic experiences to model *structure*, not to be copied — your stories must be your own and true. Read each exemplar for the shape: short Situation, owned Task, first-person Action that carries the weight, landed and (where the category demands) quantified Result.

Each section ends with the rubric your own answer is graded against. Score yourself honestly; the gaps you find here are the gaps an interviewer would find live.

---

## §1 — Conflict / Disagreement

### Exemplar answer (≈1:50 spoken)

> **Situation.** On a course project building a group scheduling app, my teammate wanted to store all the availability data as one big JSON blob per user. I thought that would make conflict-detection queries slow and painful to write.
>
> **Task.** I was the one writing the conflict-detection logic, so I had to either build it on top of his data model or make the case for a different one.
>
> **Action.** Instead of just arguing for a relational schema, I asked him what was driving the blob choice — it turned out he'd been burned by a migration-heavy schema in a previous class and wanted to avoid the overhead, which was a fair concern for a four-week project. So I didn't dismiss it. I built a quick prototype both ways and timed the core query: the blob version took about 300ms per check and the relational version under 5ms, and the relational query was half the lines of code. I showed him both, side by side, and proposed a middle path — a simple two-table schema with no migrations framework, just raw SQL, which kept his "no overhead" requirement while fixing the performance.
>
> **Result.** He agreed, we shipped the two-table version, and conflict detection stayed instant even with the whole class's data loaded for the demo. The bigger thing I took from it: the fastest way to win a technical disagreement is to find the other person's actual constraint and solve for it, not to argue harder for my own preference.

### Why this scores well

- The Situation is two sentences. The Task is one, in "I," and establishes ownership.
- The Action *engages the other side* — it asks what drove his choice and takes the concern seriously — which is the senior move for a conflict story. It then brings data (the timing) and proposes a resolution that honors both positions.
- The Result is concrete (300ms → 5ms, stayed instant at demo) and carries a lesson *about handling disagreement*, which is what the category scores.
- No "we was right." The resolution is better than either starting point.

### Common failure modes this exemplar avoids

- **The "I was right" story:** the exemplar never claims the teammate was simply wrong; it honors his real constraint.
- **All-setup, no-action:** the Situation is short; the Action carries the airtime.
- **Unlanded Result:** it ends on a number and a lesson, not "and it worked out."

### Rubric for Exercise 1

| Dimension | Weight | What "yes" looks like |
|-----------|-------:|----------------------|
| Category fit | 20% | Clearly a Conflict story; the disagreement is genuine, not manufactured |
| Engages the other side | 25% | At least one beat where you take the other position seriously (ask why, acknowledge a fair point, address their actual concern) |
| STAR structure + airtime | 20% | Short Situation, owned Task, Action ≈60%, Result landed |
| "I" discipline | 15% | Action is first-person; team credited without erasing your contribution |
| Result + lesson | 20% | Concrete outcome *and* a lesson about handling disagreement |

---

## §2 — Failure / Mistake

### Exemplar answer (≈1:55 spoken)

> **Situation.** During my internship I owned a nightly data-export job. About three weeks in, I pushed a change to its date filter and didn't test it against the edge case of month boundaries.
>
> **Task.** The job was mine end to end, so when it broke, it was on me to catch it, fix it, and make sure it couldn't happen again.
>
> **Action.** The job silently exported an empty file on the first of the month, and nobody noticed for two days because there was no alerting — which was also my gap. When the downstream team flagged the missing data, I owned it immediately rather than looking for a way to explain it away. I traced the bug to an off-by-one in the date range, fixed it, and back-filled the two missing days. Then I did the more important thing: I added a sanity check that fails the job loudly if the export row count drops to zero, and I wrote a small test suite covering the month-boundary and year-boundary cases I'd missed.
>
> **Result.** The back-fill restored the data the same afternoon, and the row-count alarm I added caught a completely unrelated upstream failure about a month later — before the downstream team even noticed. The lasting change: I now never ship a change to a data pipeline without a test for the boundary cases and an alert on the output, and I've carried that habit into every job since.

### Why this scores well

- It is a *real* failure with *real* stakes (two days of missing data, a downstream team affected) — not a humble-brag.
- It **owns** the mistake plainly ("which was also my gap," "it was on me") with zero blame-shifting.
- The Result names a *specific* change (boundary tests + output alerting), not a vague "I learned to be careful." And it shows the change paying off later (caught an unrelated failure), which is the strongest possible proof the lesson stuck.
- The tone is composed — the candidate discusses their own failure calmly, which is itself part of what the question tests.

### Common failure modes this exemplar avoids

- **The fake failure:** this is a genuine bug with consequences, not "I'm a perfectionist."
- **Blame-shifting:** the candidate owns both the bug *and* the missing alerting, even though "nobody set up alerting" could have been an excuse.
- **The vague lesson:** the change is specific and checkable, and it is shown working later.

### Rubric for Exercise 2

| Dimension | Weight | What "yes" looks like |
|-----------|-------:|----------------------|
| Real failure, real stakes | 25% | A genuine mistake with consequences; not a disguised brag |
| Ownership | 25% | Owns their piece plainly; no blame-shifting, even where an excuse was available |
| STAR structure + airtime | 15% | Short Situation, owned Task, Action ≈60%, Result landed |
| Composure | 10% | The failure is discussed calmly, without excessive self-flagellation or defensiveness |
| Specific change | 25% | The Result names a concrete change made afterward — not "I learned to be careful" |

---

## §3 — Leadership / Initiative

### Exemplar answer (≈1:50 spoken)

> **Situation.** On my team's repo, the CI build had crept up to about nine minutes, and everyone complained about it, but it wasn't anyone's job to fix — so nobody did.
>
> **Task.** I decided to take it on myself. No one assigned it; I just got tired of the wait and figured I could help everyone if I dug in.
>
> **Action.** I started by profiling the build to find where the time actually went, instead of guessing. The bottleneck was that we reinstalled all dependencies from scratch on every run and ran the full test suite serially. I set up dependency caching, which cut the install step from about four minutes to twenty seconds, and I parallelized the test suite across four workers. Then — because I wanted the fix to stick and not just be *my* fix — I wrote a short doc explaining the caching setup so the next person touching CI wouldn't accidentally break it, and I walked two teammates through it.
>
> **Result.** The build dropped from about nine minutes to ninety seconds — roughly a six-times speedup — which, across a team of eight merging several times a day, gave back a real chunk of waiting time every day. The doc I wrote became the team's reference for CI changes, and two people later told me it was the thing that finally made them comfortable touching the pipeline.

### Why this scores well

- The Situation establishes that **no one was assigned** — the initiative is unprompted, which is the heart of the category. No title required.
- *The candidate is the engine.* Every step in the Action is something they personally drove.
- The Result is **quantified** (9 min → 90 sec, ~6×) *and* has a concrete observable (the doc became the team reference). This exercise specifically drilled quantification, and the exemplar delivers both forms.
- The "wrote a doc so it would stick" beat shows leadership *beyond* the immediate fix — making the improvement durable for the team — which elevates it from "I did a task" to "I led."

### Common failure modes this exemplar avoids

- **Waiting for a title:** the candidate had no formal lead role and still tells a strong leadership story.
- **The unquantified Result:** it lands a hard number *and* a concrete observable.
- **The pure solo story:** the doc-and-walkthrough beat shows the candidate thinking about the team, not just shipping a personal win.

### Rubric for Exercise 3

| Dimension | Weight | What "yes" looks like |
|-----------|-------:|----------------------|
| Unprompted initiative | 25% | Clear that no one assigned this; the candidate stepped in |
| Candidate is the engine | 20% | The Action is driven by *you*, not the team |
| Quantified Result | 25% | A number or a concrete observable — not an adjective |
| STAR structure + airtime | 15% | Short Situation, owned Task, Action ≈60%, Result landed |
| Durability / team impact | 15% | Evidence the initiative outlasted the moment (a doc, a process, an unblocked teammate) |

---

## How to score yourself across all three

For each exercise, total the rubric weights you can honestly check. A story at 90%+ is bank-ready. A story at 70–89% needs one revision pass — usually the Result or the "I" discipline. Below 70%, re-draft from a different experience; the story may not be a good fit for the category.

The pattern most learners need more reps on after these three exercises is **landing the Result**. The Action tends to come naturally once you have a real story; the discipline of always closing on a concrete, quantified outcome — and never trailing off into "and it went well" — is the muscle that separates a bank-ready story from a rough one. Drill the Result in writing, then drill it aloud, then time it.

All three of these exercises produce stories you should carry into the mini-project story bank. A polished conflict, failure, and leadership story are three of your twelve slots, already done.
