# Lecture 3 — The Mock #3 Protocol

> **Duration:** ~2 hours (mostly the mock itself plus the watch-back).
> **Outcome:** You can run Mock #3 under *near-real* conditions — 45 minutes, video on, an uncurated prompt from a peer or platform, no peeking at solutions or notes, no second attempts, hard stop at the clock — record it, watch it with the two-pass protocol, and write a self-feedback note that explicitly compares Mock #3 to Mock #2 and produces one specific behavior change for Mock #4.

This is the third mock. Mock #1 (Week 4) established the baseline and was *solo-eligible* — you could run it against a camera alone. Mock #2 (Week 9) measured the Phase-2 ramp. Mock #3 raises the bar to **near-real conditions**: it must be with a peer or a platform partner (not solo), the prompt is uncurated and unseen, and — the new constraint — **no peeking**. No looking up a solution mid-solve. No glancing at your own notes. No "let me just restart with a cleaner approach." One attempt, one clock, the way a real onsite runs.

You already know the mechanics — the recording rig, the 45-minute structure, the two-pass watch-back, the one-behavior-change rule. This lecture does not re-teach them from scratch; it assumes [Week 4 Lecture 2](../week-04-fast-slow-pointers-and-mock-1/lecture-notes/02-the-mock-interview-protocol.md) is in your hands. What it adds is the **escalation**: what "near-real" means in practice, and how to grade a *trend line* across three mocks rather than a single snapshot.

---

## 1. What "near-real conditions" means

Mock #1's protocol had three softenings still in place: it could be solo (a camera, not a person), the problem could be self-picked (Flavor C), and there was an implicit "do it again if it goes badly." Mock #3 removes all three.

| Constraint | Mock #1 | Mock #3 |
|------------|---------|---------|
| Partner | Solo-eligible (camera) | **Peer or platform required** |
| Prompt | Could self-pick (Flavor C) | **Uncurated, picked by partner/platform** |
| Peeking | Discouraged | **Forbidden** — no solutions, no notes, no restarts |
| Video | Recommended | **Required, on** |
| Attempts | One (but redo-tolerant in spirit) | **One. Hard stop. No second run.** |

The "no peeking" constraint is the heart of it. In a drill you can pause, look something up, and continue. In a real interview you cannot. Mock #3 is the rehearsal for *not having the safety net*. If you get stuck on the bit trick or the trie walk, you narrate the stuck and work it out live — exactly as you would at Google or a startup onsite. The discomfort is the point; it is the closest the course gets to the real thing before the Phase-2 capstone Mock #4.

**Why not fully real?** Because the stakes are still artificial — there is no job on the line, and the partner is a peer, not a hiring committee. "Near-real" is the honest label: every softening removed except the consequence. Mock #4 in Week 15 adds nothing new procedurally; it is the *final measurement* on the same near-real protocol.

---

## 2. The protocol — two flavors (no solo this time)

Mock #3 is **not** solo-eligible. Pick one of two flavors.

### Flavor A — Peer-to-peer (highest fidelity)

You and another C2 learner (or any technical peer) interview each other. By Week 14 you should have a mock partner from the cohort; if not, message the cohort *Monday*.

**Setup:**

- **Schedule.** 90 minutes total — 45 each direction, plus a 10-minute buffer.
- **Platform.** Zoom / Meet / Teams. Both cameras on. Screen-share required.
- **Coding environment.** CoderPad (free sandbox), VS Code Live Share, or a shared editor. *Not* your personal IDE; the friction of an interview shell is part of the test.
- **Recording.** The candidate records on their side (OBS / QuickTime / built-in). Screen + face + audio.
- **Problem source.** The interviewer picks one problem the candidate has *not* seen, drawn from the **full** Phase-1-and-Phase-2 surface — arrays, hashing, sliding window, pointers, search, graphs, DP, backtracking, and yes, possibly bit or trie. Do not let your partner tell you the pattern in advance; the Match step is what Mock #3 grades.

**During the mock:** the interviewer reads the prompt aloud, answers clarifying questions sparingly, gives no help during the solve (at most *one* small hint after 5 minutes of being stuck), and holds the hard 45-minute stop. The candidate runs UMPIRE out loud, all six steps. **No peeking** — if stuck, narrate the stuck and reason live.

**After:** the interviewer gives 5 minutes of verbal feedback. Then swap.

### Flavor B — Platform mock (Pramp / interviewing.io)

Use **Pramp** (<https://www.pramp.com/>) or **interviewing.io** (<https://interviewing.io/>). You are matched with a stranger; one of you interviews the other. The platforms enforce the protocol — environment, timer, problem selection. You handle the recording (run OBS on the side). The stranger-match is, if anything, *higher* fidelity than a peer for the "uncurated and unfamiliar" axis. The cost is scheduling friction; Pramp matches book 24+ hours ahead, so claim the slot Monday.

There is no Flavor C. Mock #3 against a camera alone does not test the social pressure that the "no peeking, someone is watching" constraint is designed to install.

---

## 3. The pre-mock checklist (Monday)

Run this the first day of the week. The rig should be muscle memory by now; verify anyway.

- [ ] **Recording tool tested.** 30-second test recording, played back. Face visible, screen sharp, voice clear, no distracting background noise.
- [ ] **Peer locked in (Flavor A) or Pramp slot booked (Flavor B).** Mock #3 is not solo-eligible. If no partner by Monday, message the cohort *today*.
- [ ] **Coding environment chosen.** CoderPad bookmarked or shared editor ready.
- [ ] **45-minute calendar block claimed**, Do-Not-Disturb on, phone face down, door closed.
- [ ] **The "no peeking" precommitment written.** Before the mock, write one line in `mocks/mock-03/immediate-notes.md`: *"I will not look up solutions, consult my notes, or restart. One attempt."* A precommitment device beats willpower.
- [ ] **The Mock #2 self-feedback re-read.** Pull up `umpire-writeups/c2-week-09/mock-02-self-feedback.md` and re-read the "ONE behavior change" line. Mock #3's first job is to test whether that change stuck.

---

## 4. The 45-minute structure (during the mock)

Identical to Mocks #1 and #2 — the structure does not change, your fluency in it should. The clock starts when the prompt is read.

| Phase | Wall-clock | What's happening |
|------:|:----------:|------------------|
| 0:00 – 0:03 | 3 min | **U.** Read aloud. Restate. Ask one or two clarifying questions. Walk one example. |
| 0:03 – 0:05 | 2 min | **M.** Name the pattern. Deliver the 30-second pattern-recognition memo. |
| 0:05 – 0:10 | 5 min | **P.** Sketch the approach. Talk through data structures and the loop shape. |
| 0:10 – 0:25 | 15 min | **I.** Write the code. Narrate each line. Pause to think when needed; *narrate the pause*. |
| 0:25 – 0:35 | 10 min | **R.** Trace on at least two examples. Find at least one bug. |
| 0:35 – 0:43 | 8 min | **E.** Time and space. Tradeoffs. Improvements. |
| 0:43 – 0:45 | 2 min | Wrap-up. Summarize. Thank the interviewer. |

These are guidelines, not rules. By Mock #3 the structure should feel automatic — the variable under test is whether you hold it under an *uncurated* prompt with *no safety net*. If the prompt is a pattern you have not drilled recently, the Match step (0:03–0:05) is where you earn the rep: name what you see, name what you are unsure about, and commit to an approach rather than freezing.

---

## 5. The trend line — grading three mocks, not one

This is the new analytical work for Mock #3. You now have *three* recordings (Mock #1, #2, #3) and the right question is no longer "how did this one go" but "**which direction is the line moving**." Watch Mock #3 with the Mock #2 self-feedback open beside it, and grade the *deltas* on four axes:

1. **Match-memo tightness.** Mock #1's memo may have run 90 seconds. Is Mock #3's under 30? Pull both transcripts and compare. A tightening memo is the single clearest sign of progress.
2. **Silent-period shrinkage.** Timestamp every silent stretch (>5 seconds of typing or thinking with no narration). Count them and sum their duration. Is the total falling mock over mock?
3. **Recovery audibility.** When your first approach hit a wall, did you narrate the recovery (strength) or silently flail (weakness)? Count audible recoveries. They should be *rising* — not because you make more mistakes, but because you narrate them better.
4. **Evaluate completeness.** Did you reach the Evaluate step before the clock, and deliver the time/space/tradeoff structure? Mocks that run out of time before E are the most common failure; closing that gap is a clear trend.

Write the trend explicitly in the self-feedback note (§7). "Match memo: Mock #1 ~75s, Mock #2 ~45s, Mock #3 ~28s — tightening, target met." That sentence is the highest-signal line in the whole write-up, because it proves the meta-skill is compounding.

---

## 6. The post-mock window and the two-pass watch-back

Unchanged from Week 4; the discipline is the deliverable.

**Immediately after (5 minutes):** open `mocks/mock-03/immediate-notes.md`, set a 5-minute timer, free-write what is fresh. What surprised you? Did you peek (be honest)? Did you deliver the Match memo cleanly under the uncurated prompt? Where did the no-safety-net constraint bite? Pure brain-dump, no grading. The freshness is irrecoverable; capture it within 30 minutes.

**Saturday — Pass 1 (full recording at 1.5×, timestamps):** watch the whole 45 minutes, drop 10–15 timestamped observations into `mocks/mock-03/timestamps.md`. Patterns, not every "um."

**Saturday — Pass 2 (flagged segments at 1.0×, prescriptions):** re-watch only the flagged moments at normal speed. For each, write what happened and what to do differently. These feed the self-feedback note.

If you have not watched Mock #2 recently, watch its rough segments first as a calibration baseline, then watch Mock #3. The comparison is the point.

---

## 7. The self-feedback write-up (the centerpiece)

File: `umpire-writeups/c2-week-14/mock-03-self-feedback.md`. Target 700–900 words (longer than Mock #1's because of the trend-line section). Structure:

```markdown
# Mock #3 — Self-Feedback

**Date:** YYYY-MM-DD
**Problem:** [name + LeetCode link]
**Flavor:** A (peer) / B (Pramp / interviewing.io)
**Duration:** 45 minutes (hard stop)
**Outcome:** [solved correctly / solved with bug / didn't finish]
**No-peeking honored:** [yes / no — if no, say exactly when you broke it]
**Recording:** [link from mocks/mock-03/recording-link.md]

## What I felt during the mock

[3-5 sentences. Honest. Where did the no-safety-net constraint bite hardest?]

## What the recording shows

[5-8 specific observations from your pass-2 timestamps. Each with a wall-clock timestamp.]

## The trend line — Mock #1 -> #2 -> #3

[The new section. Grade the four deltas: Match-memo tightness, silent-period
shrinkage, recovery audibility, Evaluate completeness. Use numbers where you can.
"Match memo: ~75s -> ~45s -> ~28s." This is the highest-signal part.]

## The Match memo — graded

[Under 30 seconds? Pattern, algorithm, auxiliary state, one negative-space
rejection? Pull the transcript.]

## The thinking-aloud — graded

[Silent periods timestamped. Narrated pauses noted as the positive behavior they are.]

## The recovery moves — graded

[When the first approach hit a wall under the no-peeking constraint, did I narrate
the recovery or silently flail?]

## The Evaluate section — graded

[Did I reach E before the clock and deliver the time/space/tradeoff structure?]

## ONE behavior change for Mock #4

[One sentence. Specific. Testable. Should build on — not repeat — the Mock #2 change.]

## What I'm not going to do

[One or two things noticed but NOT changing. Prevents over-correction.]
```

That structure is the rubric. The trend-line section is the element that distinguishes a Mock #3 self-feedback from a Mock #1 one.

---

## 8. The "did the last change stick?" check

Mock #2 ended with one behavior change scoped for Mock #3. Before you scope a *new* change for Mock #4, answer in writing: **did the Mock #2 change actually stick?**

- If **yes** — name the evidence from the Mock #3 recording ("I committed to narrating every pause >5s; the recording shows I did it at 0:14, 0:22, and 0:31"). A change that stuck graduates from "working on it" to "installed." Pick a *new* change for Mock #4.
- If **no** — the change did not stick. Do *not* pick a new one. Carry the same change into Mock #4 and diagnose *why* it did not stick (too vague? not testable? you forgot it mid-solve?). A change that has not stuck after one mock is more valuable to repeat than to abandon.

The discipline is: one change at a time, verified to stick before moving on. Three mocks in, you should have *one or two installed behaviors* and *one in progress* — not ten half-attempted fixes.

---

## 9. Anti-patterns specific to Mock #3

The six anti-patterns from Week 4 (silent coding, skipping Match, implementing without planning, not tracing in Review, skipping Evaluate, defending broken code) still apply. Three more surface under the near-real constraints:

### Anti-pattern 7: peeking and not admitting it

You glance at a hint, your notes, or a half-remembered solution, then carry on as if you solved it unaided. The recording will show the glance; the self-feedback that omits it is worthless. If you peeked, say so, timestamp it, and note what you would have done without the peek. Honesty about a broken constraint is more valuable than a clean-looking but false write-up.

### Anti-pattern 8: freezing on an unfamiliar pattern

The uncurated prompt is a pattern you have not drilled recently. You go silent and stare. The fix is the Match step done *out loud*: "I'm not immediately sure of the pattern — let me restate the constraints and look for tells. Constant space and duplicates would suggest XOR; a prefix question would suggest a trie; this looks like neither, so let me consider..." Narrating the uncertainty is the recovery. Freezing is the failure.

### Anti-pattern 9: abandoning the trend-line analysis

You watch Mock #3 in isolation, grade it as a snapshot, and never compare to Mock #2. The single-snapshot grade is worth a fraction of the trend. If your self-feedback has no "Mock #1 -> #2 -> #3" section, you have done half the work.

---

## 10. Self-check

Without notes, answer:

1. **What three softenings does Mock #3 remove versus Mock #1?** (Solo-eligibility, self-picked prompts, and the redo-tolerant spirit — i.e., near-real means peer/platform required, uncurated prompt, no peeking/restarts.)
2. **Why is Mock #3 not solo-eligible?** (The "someone is watching, no safety net" social pressure is what near-real conditions install; a camera alone does not test it.)
3. **What are the four trend-line axes?** (Match-memo tightness, silent-period shrinkage, recovery audibility, Evaluate completeness.)
4. **What is the "did the last change stick?" rule?** (Verify the Mock #2 change stuck before scoping a new one; if it did not stick, repeat it for Mock #4 rather than abandoning it.)
5. **What do you do if you peeked?** (Admit it, timestamp it, note what you would have done unaided. Honesty about the broken constraint beats a false clean write-up.)

If you can answer all five without hesitation, you are ready for Mock #3. Set up the rig Monday, lock the partner Monday, run the mock Friday, watch Saturday, write Saturday.

---

## Further reading

- **interviewing.io's blog**: <https://interviewing.io/blog> — the "lessons from thousands of mock interviews" articles. Re-read the one on "what separates a hire from a no-hire" before Friday; by Mock #3 you have the vocabulary to apply it to yourself.
- **The Week-4 mock protocol**: [Week 4 Lecture 2](../week-04-fast-slow-pointers-and-mock-1/lecture-notes/02-the-mock-interview-protocol.md) — the full mechanics, re-read §7 (two-pass watching) and §9 (one-behavior-change rule).

Next: [exercises/README.md](../exercises/README.md) to drill the two patterns, or [mini-project/README.md](../mini-project/README.md) to scope Mock #3.
