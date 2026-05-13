# Mini-Project — Mock Interview #1

> The week's deliverable, the **first inflection point** of C2 · CrunchTime — The Code. Three weeks of drills have built the patterns. This week you put yourself on a clock, in front of a recorder, with a real (or simulated) interviewer, and discover what's actually in your hands versus what's still on paper.

**Estimated time:** 11 hours total, split across Thursday–Sunday.

This mini-project is *experience-heavy* rather than write-up-heavy. The bulk of your deliverable is a 45-minute recording of yourself solving a problem under interview conditions, plus a structured self-feedback note that grades the recording honestly against the UMPIRE rubric. The write-up is short. The recording is the artifact.

---

## Why this matters

Three reasons.

1. **Mocks reveal which patterns aren't actually in your hands yet.** Drills are gentle: curated problems, informal clock, optional recording. Mocks remove all three softenings simultaneously. The result is data — which behaviors hold up under pressure, which collapse. That data is irreplaceable; reading about UMPIRE won't produce it.

2. **The recording is the unflinching mirror.** Memory is generous; recordings are not. You will discover, in pass 1 of watching, that you said things you don't remember saying — and didn't say things you swear you said. Calibrating your *felt experience* against your *actual behavior* is what mock interviews are for. Drills can't do this.

3. **Mock #1 is the floor, not the ceiling.** It will be worse than you hope. That's expected. Mock #4 in Week 15 is what counts — the path from Mock #1 to Mock #4 is what this course optimizes. Mock #1's value is *establishing the baseline* against which Mocks 2/3/4 are measured.

---

## What you ship

Three artifacts. The recording is the centerpiece; the two write-ups frame it.

```
crunchtime-interview-prep-<you>/
├── mocks/
│   └── mock-01/
│       ├── recording-link.md           # link to the video (URL, since the file is too big to commit)
│       ├── immediate-notes.md          # 5-minute brain dump captured right after the mock
│       └── timestamps.md               # pass-1 timestamps from watching the recording
└── umpire-writeups/
    └── c2-week-04/
        └── mock-01-self-feedback.md    # the structured self-feedback, 600-800 words
```

`recording-link.md` should be a one-line file:

```markdown
# Mock #1 recording

[Video — 45 min](https://drive.google.com/file/d/.../view) (private link, view-only)

Problem: [problem name + LeetCode link]
Flavor: A (peer) / B (Pramp) / C (solo)
Date: YYYY-MM-DD
```

The recording itself lives on Google Drive, Loom, unlisted YouTube, or any host where you can grant view access. Do **not** commit the raw video file; even compressed, a 45-minute capture is hundreds of MB to several GB, far past what git wants to track. The link is the artifact.

---

## The protocol — choose your flavor

Three flavors, in descending order of fidelity. Pick one based on what you can actually pull off this week.

### Flavor A — Peer-to-peer (recommended)

You and another C2 learner (or any technical peer) interview each other. 45 minutes each way, with a buffer. Both record their candidate sessions.

### Flavor B — Pramp / interviewing.io

Use **Pramp** (free, peer-matched, you interview them then they interview you): <https://www.pramp.com/>. Or **interviewing.io** (anonymous mocks, free tier limited but exists): <https://interviewing.io/>. The platforms enforce the protocol; you handle the recording.

### Flavor C — Solo against a camera

No peer available. Set up: camera on, recorder running, problem picked from a random-Medium button. 45-minute timer. Talk to the camera as if it's an interviewer. *This is acceptable for Mock #1 only.* Mocks 2/3/4 require a peer or platform partner — by Week 9 you should have a mock partner.

See [Lecture 2 §2](../lecture-notes/02-the-mock-interview-protocol.md) for the full protocol on each flavor.

---

## The problem — how to pick

Don't pick a problem you've solved before. The point is uncurated pattern recognition under pressure.

**Acceptable sources for Mock #1:**

- A peer/interviewer picks for you (Flavor A) — they get to surprise you. Best.
- Pramp / interviewing.io picks for you (Flavor B) — also great.
- A random Medium from LeetCode tagged "Linked List," "Two Pointers," "Hash Map," or "Sliding Window" (Flavor C). These are the four patterns from Phase 1. The random-button is fine; the goal is uncuration.

**Difficulty:** Medium. Easy is below interview pace; Hard is above what you can reasonably finish in 45 minutes for Mock #1.

**If your peer picks the problem:** ask them *not* to tell you the pattern in advance. The Match step is the most-graded part of the rubric this week; you need to do that work yourself, not be handed the answer.

---

## The 45-minute structure (during the mock)

Recommended time allocation. Real interviews are messier; this is the *shape*, not literal minutes.

| Phase | Wall-clock | What's happening |
|------:|:----------:|------------------|
| 0:00 – 0:03 | 3 min | **U.** Read aloud. Restate. Ask one or two clarifying questions. Walk through one example. |
| 0:03 – 0:05 | 2 min | **M.** Name the pattern. Deliver the 30-second pattern-recognition memo. |
| 0:05 – 0:10 | 5 min | **P.** Sketch the approach. Talk through data structures and the loop shape. Optionally diagram on Excalidraw. |
| 0:10 – 0:25 | 15 min | **I.** Write the code. Narrate each line. Pause to think when needed; *narrate the pause*. |
| 0:25 – 0:35 | 10 min | **R.** Trace on at least two examples. Find at least one bug. (You will.) |
| 0:35 – 0:43 | 8 min | **E.** Time and space. Tradeoffs. Improvements. Five-piece structure from Week 2. |
| 0:43 – 0:45 | 2 min | Wrap-up. Summarize. Thank the interviewer. |

The clock is hard. At 45 minutes, stop, even mid-line. The recording continues for any final wrap-up but the *solve* ends at 45.

---

## The post-mock window (the most-skipped step)

The first 5 minutes after the recording stops are the highest-leverage 5 minutes of the entire week. Do not skip them.

1. Open a text file.
2. Set a 5-minute timer.
3. Free-write what's fresh. What surprised you? What felt automatic? What felt clumsy? Did you deliver the Match memo cleanly? Did you go silent at any point?
4. Save as `mocks/mock-01/immediate-notes.md`. Push.

That file is three paragraphs, no structure, pure brain-dump. Don't grade yet; just capture.

This step is irrecoverable — wait until evening and the freshness is gone. The five minutes are non-negotiable.

---

## Watching the recording (Saturday)

Two-pass protocol. See [Lecture 2 §7](../lecture-notes/02-the-mock-interview-protocol.md) for full detail.

### Pass 1 — at 1.5×, full recording, timestamps doc

Watch the whole 45 minutes at 1.5× (≈30 wall-clock minutes). Drop a timestamped observation every time you notice a *pattern* (not every "um"). Aim for 10–15 timestamps total.

```
[mm:ss]  Observation
```

Save as `mocks/mock-01/timestamps.md`. Push.

### Pass 2 — at 1.0×, only flagged segments

Watch only the segments you flagged in pass 1. For each, write a sentence describing what happened and a sentence prescribing what to do differently. These prescriptions feed directly into the self-feedback write-up.

---

## The self-feedback write-up (the centerpiece)

File: `umpire-writeups/c2-week-04/mock-01-self-feedback.md`. Target: 600–800 words. Structure:

```markdown
# Mock #1 — Self-Feedback

**Date:** YYYY-MM-DD
**Problem:** [name + LeetCode link]
**Flavor:** A (peer) / B (Pramp) / C (solo)
**Duration:** 45 minutes (hard stop)
**Outcome:** [solved correctly / solved with bug / didn't finish / etc.]
**Recording:** [link from `mocks/mock-01/recording-link.md`]

## What I felt during the mock

[3-5 sentences. Honest. "I felt rushed during Match." "I went silent for two minutes at the 18-minute mark." "I caught the off-by-one but didn't articulate the fix."]

## What the recording shows

[5-8 specific observations from your pass-2 timestamps. Each with a wall-clock timestamp.]

## The Match memo — graded

[Was it under 30 seconds? Did it name the pattern, the algorithm, the auxiliary state, and one negative-space rejection? Quote the actual transcript from your recording if you can.]

## The thinking-aloud — graded

[Did I go silent? When? For how long? Did I narrate pauses?]

## The recovery moves — graded

[When my first approach hit a wall, did I narrate the recovery? Or did I silently flail?]

## The Evaluate section — graded

[Did I produce the five-piece structure from Week 2? Did I deliver the amortized-O(n) / O(1)-space defense sentence cleanly?]

## ONE behavior change for Mock #2

[One sentence. Specific. Testable. "I will narrate every pause longer than 5 seconds" is good. "I will be more confident" is bad - not testable.]

## What I'm not going to do

[One or two things you noticed but are NOT going to change. The point of this section is to prevent over-correction.]
```

The structure is the rubric. It is also the artifact a senior engineer would read in 4 minutes and form a clear impression of your self-awareness. Make it readable in that 4 minutes.

---

## Acceptance criteria

- [ ] **45-minute recording uploaded** to an accessible host (private YouTube unlisted, Google Drive, Loom, etc.).
- [ ] `mocks/mock-01/recording-link.md` committed with the working link.
- [ ] `mocks/mock-01/immediate-notes.md` committed — captured **within 30 minutes** of the mock ending (the freshness window).
- [ ] `mocks/mock-01/timestamps.md` committed with 10–15 pass-1 observations.
- [ ] `umpire-writeups/c2-week-04/mock-01-self-feedback.md` committed, following the structure above, 600–800 words.
- [ ] The self-feedback write-up has a **specific, testable behavior change** in the "ONE behavior change" section. (Not "be more confident.")
- [ ] The mock used **a problem you had not seen before**. (Self-attested; the interview tell is the recording — your reactions to the prompt at minute 0:30 will reveal whether you knew it.)

---

## The grading rubric (apply to yourself)

You are grading yourself. Apply this rubric to your own self-feedback write-up.

| Axis | Weight | "Great" looks like |
|------|------:|--------------------|
| Honesty | 30% | Self-feedback names at least 2 specific failures from the recording. Vague optimism is a red flag. |
| Specificity | 25% | Every observation has a wall-clock timestamp. "I went silent" is bad; "0:18:30 - 0:20:15: silent typing during the loop body" is great. |
| Match-memo critique | 15% | The memo's length, content, and cadence are explicitly graded. Pull the transcript. |
| Thinking-aloud critique | 15% | Silent periods are timestamped. Narrated pauses are noted as the positive behavior they are. |
| Behavior change is testable | 15% | One sentence, specific, measurable. "I will deliver the Match memo in under 30 seconds, even if I have to cut content" is the cadence. |

If you score yourself "great" on all five axes, push and move on to Phase 2.

---

## Suggested order of operations

### Monday — set up the rig (1h)

1. Install/test OBS or QuickTime. Make a 30-second test recording. Play it back. Fix anything broken.
2. Schedule the mock slot for Friday or Saturday. Block 90 minutes on the calendar (45 mock + 45 buffer/setup/notes).
3. If Flavor A: message a peer, lock in a time. If Flavor B: book a Pramp slot. If Flavor C: pick the day, write it down.
4. Open `mocks/mock-01/` in your portfolio repo. Create empty `recording-link.md`. Commit the empty file as a placeholder ("Track mock #1 deliverables").

### Tuesday or Wednesday — pre-pre-mock (0.5h)

5. Pick an easy problem you've solved before. 10-minute timer. Record yourself solving it. Watch the recording. The goal: get the "I'm being recorded" awkwardness out of the way *before* Friday.

### Thursday — final prep (1.5h)

6. Re-read [Lecture 2](../lecture-notes/02-the-mock-interview-protocol.md), especially §3 (pre-mock checklist) and §4 (45-minute structure).
7. Confirm the recording rig still works. Confirm the peer is confirmed. Confirm the time slot is on the calendar with a Do-Not-Disturb override.

### Friday — Mock #1 (2.5h, of which 45 minutes is the mock)

8. Show up. Hit record. Run UMPIRE. 45 minutes. Hard stop.
9. **Within 30 minutes:** the 5-minute post-mock free-write into `immediate-notes.md`. Commit.
10. Upload the recording. Update `recording-link.md` with the URL. Commit.

### Saturday — watch + write (3h)

11. Pass 1: full recording at 1.5×. Drop 10–15 timestamps into `timestamps.md`. Commit.
12. Pass 2: flagged segments at 1.0×. Write the self-feedback note. Commit.
13. Re-read your self-feedback. Score it yourself against the rubric above. If anything is "vague" or "optimistic," sharpen it.

### Sunday — reflection (0.5h)

14. Add a one-paragraph note to your `study-plan/phase-1-retrospective.md` from homework Problem 6: *"What Mock #1 specifically showed me."* Cross-reference the self-feedback note.

---

## What "great" looks like (final rubric)

A learner who has shipped Mock #1 *well* has:

- Recording uploaded and accessible.
- Self-feedback that **explicitly identifies a failure mode**, by name, with timestamps.
- One specific behavior change scoped for Mock #2.
- Calibrated expectations: knows Mock #1 is the floor, not the ceiling.
- Committed all four artifacts before Sunday at 23:59.

A learner who has shipped Mock #1 *poorly* has:

- Self-feedback that is too generous ("went well overall, just need more practice"). This is the most common failure mode. Be harder on yourself.
- No timestamps. ("I felt rushed" without a clock reference is unfalsifiable.)
- A behavior change that is not testable ("be more confident").
- Skipped the immediate-notes step. (No 5-minute brain dump.)

If you catch yourself writing self-feedback that sounds like flattery, *re-watch one of the rough segments at 1.0× and try again.*

---

## Why one mock is enough this week

You might be tempted to do two mocks this week — the first as practice, the second "for real." Don't. One is enough. The reason: the self-feedback discipline is the high-leverage part, and doing it well for one mock is more valuable than doing it badly for two. By Mock #2 in Week 9, you'll have *also* had four more weeks of pattern drills, so the second mock is meaningfully different from the first by both vector (more patterns) and meta-skill (better self-feedback).

One mock. Real one. Full feedback. Move on.

---

When you're done: push everything, send the self-feedback link (not the video) to one peer for review, then move on to [Week 5 — Binary Search Beyond Sorted Arrays](../../week-05/).

Phase 1 closes here. The next time you do a mock, you'll have eight weeks of additional patterns under you. Welcome to Phase 2.
