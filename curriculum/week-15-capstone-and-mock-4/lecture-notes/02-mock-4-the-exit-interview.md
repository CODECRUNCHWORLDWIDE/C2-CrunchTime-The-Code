# Lecture 2 — Mock #4, the Exit Interview

> **Duration:** ~1.5 hours.
> **Outcome:** You can run the course's final mock under full real-interview conditions — a 90-second behavioral open, an uncurated technical problem under a hard 45-minute clock, a behavioral question close, all recorded — and write a self-feedback note that explicitly measures whether the behavior changes from Mocks #1–#3 stuck.

This is the fourth and final mock of the course. Mock #1 (Week 4) taught you to run UMPIRE under a camera. Mock #2 (Week 9) added a harder pattern set and a peer interviewer. Mock #3 (Week 14) added the behavioral round and a system-design-adjacent prompt. Mock #4 is the **exit interview**: the closest simulation of a real onsite loop you will run before the real thing, and the measurement of whether everything you have built actually holds under pressure.

The protocol from Week 4 Lecture 2 (the three flavors, the pre-mock checklist, the two-pass watching, the one-behavior-change rule) is the foundation. Re-read it if it is not fresh. This lecture covers what is *different* about Mock #4: the behavioral bookends, the no-solo rule, and the self-feedback note that closes the loop on three mocks of accumulated behavior changes.

---

## 1. What is different about Mock #4

Three things change from the earlier mocks.

### Difference 1 — no solo flavor

Mock #1 allowed a solo-against-a-camera flavor as a fallback. Mocks #2, #3, and #4 do not. By Week 15 you must have a mock partner — a cohort peer, or a Pramp / interviewing.io match. The reason: the behavioral bookends require a *human* to react to. You cannot practice "tell me about yourself" against a camera and learn anything about how it lands; you need a face that nods or frowns, a follow-up question you did not script, the small social pressure of a real listener. If you have no partner, the Monday task is to find one — the [community channel](../../community/) and Pramp both exist for this.

### Difference 2 — the behavioral bookends

Earlier mocks were technical-only (Mock #3 added a behavioral round as a separate segment). Mock #4 *wraps* the technical problem in behavioral, the way a real onsite slot does:

- **The open (90 seconds):** "Tell me about yourself." Your self-introduction. Not your resume read aloud — a 90-second narrative arc: who you are, the thread that connects your experience, what you are looking for, and a one-sentence bridge to "and that is why I have been doing focused interview prep, which we can get into."
- **The technical middle (40 minutes):** the uncurated UMPIRE problem under the hard clock. This is the part you have drilled three times.
- **The close (5 minutes):** one behavioral question — "tell me about a time you disagreed with a teammate," or "tell me about a hard bug," or "why this company" — answered in STAR shape with a specific Result.

The bookends are where most candidates who are technically ready still fumble. A clean Match memo means nothing if the candidate opened with a rambling three-minute autobiography or closed with a behavioral answer that had no Result. Mock #4 tests the *whole slot*, not just the algorithm.

### Difference 3 — it measures, it does not teach

Mocks #1–#3 each produced one new behavior change. Mock #4 produces a different artifact: a *verdict on whether the prior three changes stuck*. You walk into Mock #4 with three specific behavior changes you have been practicing (e.g., "narrate every pause over 5 seconds," "deliver the Match memo in under 30 seconds," "start Evaluate by the 35-minute mark"). The self-feedback note's primary job is to check, with timestamps from the recording, whether each one held under the pressure of the exit mock. If a change that was solid in Mock #3 cracked in Mock #4, that is the single most important finding — it means the change is not yet a reflex, only a conscious effort that fails under load.

---

## 2. The pre-mock checklist (Thursday)

Run this the day before. Most of it is the Week-4 checklist; the new items are the behavioral prep.

- [ ] **Recording rig tested.** Screen + face + audio. A 30-second test recording played back. (Same as every mock.)
- [ ] **Partner confirmed** for a 90-minute slot (45 each direction plus buffer), or Pramp match booked.
- [ ] **The three prior behavior changes written on a card** where you can see them — but not where the interviewer can. These are what you are measuring; you want them top-of-mind without reading them aloud mid-mock.
- [ ] **The 90-second self-intro rehearsed once, out loud, timed.** Not memorized word-for-word — rehearsed as a structure so it lands at 90 seconds, not 30 and not 180. The most common failure is rambling past two minutes.
- [ ] **One behavioral story ready in STAR shape** with a specific Result, in case the close asks something you can map to it. You built 3–5 stories in Week 14; have at least one loaded.
- [ ] **Coding environment chosen** — CoderPad sandbox or shared VS Code, not your personal IDE. (Same as every mock.)
- [ ] **Quiet 60 minutes reserved**, Do Not Disturb on, water within reach.

---

## 3. The 45-minute structure (with bookends)

The technical middle keeps the Week-4 allocation; the bookends are added on either side.

| Phase | Wall-clock | What's happening |
|------:|:----------:|------------------|
| Open | 90 sec | **Behavioral open.** "Tell me about yourself." The 90-second narrative arc. |
| 0:00 – 0:03 | 3 min | **U.** Read aloud. Restate. Clarifying questions. One example. |
| 0:03 – 0:05 | 2 min | **M.** Name the pattern. The 30-second Match memo. |
| 0:05 – 0:10 | 5 min | **P.** Sketch the approach, the data structures, the loop shape. |
| 0:10 – 0:28 | 18 min | **I.** Write the code. Narrate each line. Narrate every pause. |
| 0:28 – 0:38 | 10 min | **R.** Trace on two examples. Find at least one bug. |
| 0:38 – 0:43 | 5 min | **E.** Time, space, tradeoffs, one improvement. |
| Close | 5 min | **Behavioral close.** One STAR question. Specific Result. |

The technical middle is slightly compressed (40 minutes instead of 45) to make room for the bookends, which mirrors a real onsite slot where the interviewer spends a few minutes on intro and a few on questions. Practice the *whole arc* — a candidate who nails the algorithm but opens flat and closes without a Result has not practiced the thing a real interview measures.

---

## 4. The 90-second self-introduction

The open is a narrative, not a resume read. The structure that works:

1. **Who you are now** (one sentence): "I'm a software engineer with three years of backend experience, most recently building data pipelines at [company]."
2. **The thread** (two sentences): the through-line that connects your experience. Not a list of jobs — the *theme*. "I've consistently been the person who takes the ambiguous, half-specified problem and turns it into a shipped system — at [company A] that was the billing migration, at [company B] it was the search-relevance rewrite."
3. **What you're looking for** (one sentence): "I'm looking for a role where I can go deeper on distributed systems and own a service end to end."
4. **The bridge** (one sentence): "And to make sure my fundamentals are sharp for that, I've spent the last few months on focused algorithm and system-design prep — happy to dig into any of it."

Four pieces, roughly 90 seconds, no rambling. The two most common failures: (a) reciting the resume chronologically with no thread, which is boring and forgettable; (b) running long — three minutes of autobiography that loses the listener. Rehearse it once, timed, so it lands at 90.

The senior signal in the open is the **thread**. Anyone can list jobs. A candidate who names the through-line ("I'm the person who turns ambiguity into shipped systems") gives the interviewer a frame to remember them by. Find your thread.

---

## 5. The behavioral close — STAR with a specific Result

The close is one behavioral question, answered in STAR shape. The structure is from Week 14; the discriminator at Mock #4 is the **Result** — specific, and quantified where possible.

> **S** (Situation, ~15 sec): "On the billing migration, two weeks before launch we found the new system double-charged about 2% of customers in a specific edge case."
>
> **T** (Task, ~10 sec): "I owned the reconciliation logic, so it was on me to find the root cause and fix it without slipping the launch."
>
> **A** (Action, ~30 sec): "I built a shadow-comparison job that ran the old and new systems in parallel on production traffic, diffed the outputs, and surfaced the 2% as a specific rounding mismatch in multi-currency invoices. I fixed the rounding, added a regression test for the multi-currency case, and re-ran the shadow job for a week to confirm zero diffs."
>
> **R** (Result, ~15 sec): "We launched on time with zero double-charges in the first month, and the shadow-comparison job became the standard pre-launch check for the team's next three migrations."

The Result has two specifics: "zero double-charges in the first month" (the immediate outcome) and "became the standard check for the next three migrations" (the lasting impact). A Result that is "and it worked out fine" is the most common behavioral failure. Drill the Result until it is specific.

---

## 6. The self-feedback note — measuring whether the changes stuck

The Mock #4 self-feedback note has the Week-4 structure (what I felt, what the recording shows, the Match memo graded, the thinking-aloud graded, the recovery graded), **plus a new top section**: the verdict on the three prior behavior changes.

```markdown
# Mock #4 — Self-Feedback (Exit Mock)

**Date:** YYYY-MM-DD
**Problem:** [name + LeetCode link]
**Flavor:** A (peer) / B (platform)
**Behavioral open:** [delivered / fumbled — note]
**Behavioral close:** [question asked; STAR Result specific? Y/N]
**Outcome:** [solved / solved with bug / didn't finish]

## Prior behavior changes — did they stick? (the headline section)

| Change (from Mock #N) | Held under Mock #4 pressure? | Evidence (timestamp) |
|-----------------------|------------------------------|----------------------|
| Narrate pauses over 5 sec | Yes | 14:20 — narrated a 12-sec pause cleanly |
| Match memo under 30 sec | Partial | 03:10 — ran 50 sec; added an unasked comparison |
| Start Evaluate by 35:00 | No | started E at 41:00; R ran long |

## What the recording shows
[5–8 timestamped observations]

## The behavioral bookends — graded
[Open: did the thread land? Close: was the Result specific?]

## ONE thing to keep drilling post-course
[The change that cracked under Mock #4 pressure. This is the one you take into the real loop.]
```

The headline table is the point. It turns "I think I'm getting better" into a measured verdict: of the three changes you have been practicing, which held under the hardest mock of the course, and which cracked. The one that cracked is the one you carry into the real interviews — name it explicitly in the "one thing to keep drilling" section.

---

## 7. Watching the recording — the same two-pass protocol

The two-pass watching protocol from Week 4 §7 is unchanged: pass 1 at 1.5× with timestamps; pass 2 at 1.0× on only the flagged moments, writing observation-then-prescription. The one addition for Mock #4: **flag the bookends specifically**. Most candidates, watching back, are surprised by how the open landed (often flatter than it felt) and how the close ran (often without a clear Result). Watch the first 90 seconds and the last 5 minutes with particular attention; they are the parts you have practiced least.

---

## 8. The exit-mock mindset

A note on framing. By Mock #4 you may be tempted to treat it as a victory lap — "I've done three, I know this." Resist that. The exit mock is the most valuable *because* it is the last controlled environment before the stakes are real. Every behavior change that cracks here is one you would rather catch now than in a real onsite where the offer is on the line. Go into Mock #4 hunting for the crack, not for the win. The win is the offer, three weeks from now, in a real loop — and you make that win more likely by being ruthlessly honest about what Mock #4 reveals.

---

## 9. Closing — the loop closes here

Three takeaways:

1. **Mock #4 tests the whole slot, not just the algorithm.** The behavioral open and close are where technically-ready candidates still fumble. Practice the 90-second self-intro and the STAR close as deliberately as you practice the Match memo.
2. **The self-feedback note measures, it does not just describe.** The headline table — did each of the three prior behavior changes hold under exit-mock pressure? — is the point. Name the one that cracked; it is what you carry into the real loop.
3. **The exit mock is the last controlled rep.** Treat it as the place to find the crack, not to take the victory lap. The honesty here is what makes the real loop go well.

The portfolio (Lecture 1) proves the process exists. The mock (this lecture) proves it holds under pressure. Lecture 3 builds the pack that puts the portfolio in front of someone who can hire you.

[Back to the README](../README.md). On to [Lecture 3 — The Recruiter-Prep Pack](./03-the-recruiter-prep-pack.md).
