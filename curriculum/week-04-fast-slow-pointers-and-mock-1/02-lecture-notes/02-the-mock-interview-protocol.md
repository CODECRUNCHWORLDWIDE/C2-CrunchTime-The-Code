# Lecture 2 — The Mock Interview Protocol

> **Duration:** ~2 hours.
> **Outcome:** You can set up a mock interview with a peer or solo against a camera, run it under realistic constraints, record the entire session, watch the recording without flinching, and write a self-feedback note that produces *one specific behavior change* for Mock #2.

Three weeks of patterns have built half of the interview skill. This lecture is the other half: the *meta-skill* of running interviews under pressure, recording yourself, watching the recording, and extracting *one specific change* for next time. By Sunday this lecture's content will have produced your first portfolio artifact that isn't code — a 45-minute recording, plus a 600-word self-feedback note.

This is the lecture most candidates skip. They tell themselves "I'll do mocks once I've drilled more." That's backwards. Mocks reveal which patterns aren't actually in your hands yet — *that's the whole point*. You will discover, in Mock #1, that things you thought you knew aren't yet automatic. That's not a setback. That's the data.

---

## 1. Why mock interviews are different from drills

In a drill, you are alone, the clock is informal, the prompt is curated, and the recording is optional. In a mock interview, *one* of those changes:

- **Someone is watching** (a peer, an interviewer-roleplay, or — in solo mode — a camera that is functionally identical to "someone watching" because you cannot hide from the recording).
- **The clock is hard.** 45 minutes. The interview ends when the clock hits zero whether or not you've solved it.
- **The prompt is uncurated.** You don't get to pick a sliding-window problem; you get whatever shows up. The pattern-recognition skill from Weeks 1–3 is now tested for real.
- **The recording is mandatory.** No "I'll do it without recording this time." That defeats the purpose of the mock.

Three things shift in your behavior the moment those four constraints kick in:

1. **You speed up.** You skip Match. You jump to Implement. You write code that fits a pattern you didn't actually verify.
2. **You go quiet.** Thinking-aloud feels weird when someone's listening. You revert to silent problem-solving — which is the *exact* behavior we've spent three weeks unlearning.
3. **You get clumsy with the recovery.** When you realize your first approach won't work, drill-mode you would casually backtrack. Mock-mode you panics, tries to make it work anyway, and writes brittle code under time pressure.

Mock #1 will produce at least one of those three failure modes for you. Probably all three. That's normal. The self-feedback write-up is where you turn that data into *one specific behavior change* for Mock #2 in Week 9.

---

## 2. The protocol — three flavors

You have three options for Mock #1. In descending order of fidelity to a real interview:

### Flavor A — Peer-to-peer mock (highest fidelity)

You and another C2 learner (or any technical peer) interview each other. One of you is the interviewer; the other is the candidate. Then you swap.

**Setup:**

- **Schedule.** 90 minutes total — 45 each direction, plus 10-minute buffer.
- **Platform.** Zoom / Meet / Teams. Both cameras on. Screen-share required.
- **Coding environment.** CoderPad (free sandbox), VS Code Live Share, or a shared Excalidraw board if the problem is whiteboard-heavy. *Do not use a personal IDE on your local machine.* The friction of an interview shell is part of the test.
- **Recording.** The candidate records on their side via OBS / QuickTime / built-in recorder. The interviewer's recording is optional but useful.
- **Problem source.** The interviewer picks one problem the candidate has *not* seen. Pull from LeetCode Medium tagged "Linked List," "Two Pointers," "Hash Map," or "Sliding Window." That's our pattern coverage so far.

**During the mock:**

- The interviewer reads the prompt aloud, answers clarifying questions sparingly, and otherwise stays quiet.
- The candidate runs UMPIRE out loud, all six steps.
- The interviewer gives no help during the solve. If the candidate is stuck for more than 5 minutes, the interviewer can give *one* small hint.
- The clock is hard. At 45 minutes the candidate stops, even mid-line.

**After:** the interviewer gives 5 minutes of verbal feedback. Then swap roles.

### Flavor B — Platform mock (medium fidelity)

Use **Pramp** or **interviewing.io**. You're matched with a stranger; one of you interviews the other. The platforms enforce the protocol — coding environment, timer, problem selection. Recording is on you (run OBS on the side).

This is the most "interview-like" option because it's with a stranger. The downside: scheduling friction; Pramp matches require booking 24+ hours in advance.

### Flavor C — Solo mock (acceptable fallback)

No peer available, can't schedule a Pramp match in time, want to run a controlled mock anyway. The setup:

- **Pick a problem you haven't seen.** Use a random Medium from LeetCode's "Linked List" or "Two Pointers" tag. Use a random-problem button if available.
- **Camera on. Recorder running.** Treat the camera as if it's an interviewer. Make eye contact with the lens periodically. Do not look at your screen the entire time.
- **45-minute timer.** Hard stop.
- **Out loud the entire time.** Every step of UMPIRE, every line of code, every doubt, every recovery.
- **No looking up the answer mid-solve.** If you're stuck, narrate the stuck: *"I've been stuck for 4 minutes on the cycle-entrance proof; let me write the code I have and explain what's missing."*
- **Record screen + face + audio.** All three. If your setup can only do two of three, prioritize screen + audio; the face track is high-leverage but not strictly required for Mock #1.

Solo mode is acceptable for Mock #1 *only*. Mocks #2 (Week 9), #3 (Week 14), and #4 (Week 15) require a peer or platform partner — by Week 9 you should have a mock partner in the cohort.

---

## 3. The pre-mock checklist (Monday)

Run this checklist the *first* day of Week 4. If anything fails, you have until Friday to fix it. Do not discover a broken microphone on Friday at 14:55.

- [ ] **Recording tool installed and tested.** OBS, QuickTime, Zoom built-in, whichever you'll use.
- [ ] **30-second test recording made.** Play it back. Is your face visible? Is your screen sharp? Is your voice clear? Can you hear background noise that would distract an interviewer (kitchen sounds, traffic, roommates)?
- [ ] **Coding environment chosen.** CoderPad sandbox bookmarked, or VS Code window template ready.
- [ ] **Excalidraw / whiteboard tab open in browser.** For diagramming a linked list before you code it.
- [ ] **Quiet space for 45+10 minutes reserved.** Do not Disturb on. Phone face down. Door closed if applicable.
- [ ] **Water glass within reach.** You will get thirsty. Take a sip when you need to pause and think.
- [ ] **Peer scheduled** (Flavor A) or **Pramp slot booked** (Flavor B) or **calendar block claimed** (Flavor C).
- [ ] **One 10-minute "pre-pre-mock"** — pick the easiest problem you can think of, set a 10-minute timer, run UMPIRE while recording, watch it back. The goal: get the awkward "I'm being recorded" feeling out of the way *before* Friday.

---

## 4. The 45-minute structure (during the mock)

The clock starts when the interviewer (or you, in solo mode) reads the prompt. Recommended time allocation:

| Phase | Wall-clock | What's happening |
|------:|:----------:|------------------|
| 0:00 – 0:03 | 3 min | **U.** Read aloud. Restate. Ask one or two clarifying questions. Walk through one example. |
| 0:03 – 0:05 | 2 min | **M.** Name the pattern. Deliver the 30-second pattern-recognition memo from Week 3. |
| 0:05 – 0:10 | 5 min | **P.** Sketch the approach. Talk through the data structures and the loop shape. Optionally diagram on Excalidraw. |
| 0:10 – 0:25 | 15 min | **I.** Write the code. Narrate each line. Pause to think when needed; *narrate the pause*. |
| 0:25 – 0:35 | 10 min | **R.** Trace on at least two examples. Find at least one bug. (You will. Everyone does.) |
| 0:35 – 0:43 | 8 min | **E.** Time and space. Tradeoffs. Improvements. The five-piece structure from Week 2. |
| 0:43 – 0:45 | 2 min | Wrap-up. Summarize. Thank the interviewer. |

These numbers are guidelines, not rules. Real interviews are messier. If U takes 5 minutes because the prompt is ambiguous, that's fine — that's a U-step win, not a loss. If I takes 25 minutes because the problem is hard, that's also fine — but it means R and E are compressed. Practice the *structure*, not the literal minutes.

---

## 5. What "good" sounds like during the mock

Three patterns of speech are the interview tells. Listen for them in your recording.

### Tell 1: the Match memo, delivered cleanly in 30 seconds

> *"This is a fast/slow pointers problem because we're walking a linked list and looking for a cycle. The pattern is Floyd's tortoise and hare. The auxiliary state is just two pointers — `slow` and `fast`. The reason this isn't 'hash set of visited nodes' is that the interview tell here is `O(1)` space, and Floyd's is the canonical `O(1)`-space cycle algorithm. I'll walk slow by one node and fast by two; if they meet, there's a cycle; if fast reaches None, no cycle."*

That paragraph, read aloud, is ~25 seconds. It hits the pattern name, the algorithm, the auxiliary state, and one negative-space rejection. That is *the* Match cadence we've been building.

### Tell 2: narrating the pause

When you stop to think, say so:

> *"Hold on — I want to think about whether the loop guard needs `fast.next` or just `fast`."* [3-second pause] *"Yes, both, because the next line dereferences `fast.next.next`."*

The pause itself is fine. *Silent* thinking is the problem. Interviewers can't grade silence. Narrate the pause and they can grade the thinking that fills it.

### Tell 3: the recovery move

When you realize your approach is wrong:

> *"Wait. I've assumed the list is a singly-linked list, but I haven't checked. Let me re-read the prompt."* [reads] *"OK, singly-linked, confirmed. My approach is fine — I was second-guessing for no reason."*

Or:

> *"Hmm. The example I just traced — my code returns None, but the expected answer is the third node. I have a bug. Let me re-read the cycle-detection loop."* [reads] *"I see — I'm comparing before advancing, but I should advance first. Fix: move the comparison after both advances."*

The recovery is not a *sign of weakness*. It is a *sign of strength*. Interviewers grade recovery positively, not negatively. Practice making the recovery audible.

---

## 6. The post-mock window — the first 5 minutes after the clock stops

This is the most-skipped step in the whole protocol. Most candidates finish, close the laptop, decompress, eat lunch, and forget the details by evening.

Don't. Do this instead, *immediately* after the clock stops:

- **Open a text file. Set a 5-minute timer. Free-write what's still fresh.** What surprised you? What felt automatic? What felt clumsy? What did the interviewer ask that you didn't expect? Did you deliver the Match memo cleanly? Did you fall silent at any point?
- **Don't grade yet.** Just notes. Raw observations. The grading is Saturday's job.
- **Save the file as `mini-project/mock-01-immediate-notes.md`.** Three paragraphs, no structure. Pure brain-dump.

This step takes 5 minutes and is worth more than the next 5 hours of "I should review the mock" procrastination. The freshness is irrecoverable; capture it.

---

## 7. Watching the recording — Saturday's protocol

You will not enjoy this. The first time you watch yourself solve a coding problem, you will be amazed and horrified in equal measure. Most candidates:

- Hate the sound of their own voice.
- Notice every "um," "like," and "uh."
- See themselves looking down at the keyboard the entire time.
- Catch themselves saying something they thought they didn't say.

That is *all normal*. Past it is the data.

The two-pass watching protocol:

### Pass 1 — at 1.5×, the whole recording, with a timestamp doc open

Watch the whole 45 minutes at 1.5× (so 30 wall-clock minutes). Keep a doc open with this template:

```
# Mock #1 — Pass 1 timestamps

[mm:ss]  Observation
[mm:ss]  Observation
...
```

Drop one line per noticeable moment. Not every "um" — the *patterns*. Examples:

```
04:30  Match section was 90 seconds, not 30. Too long.
07:15  Said "let me think" but then went silent for 45 seconds. Should have narrated.
12:40  Wrote the loop guard correctly first try. Good.
18:00  Realized the off-by-one but didn't say it out loud — fixed it silently.
24:00  Lost the thread of the trace, restarted twice.
```

10–15 timestamps total. Pass 1 done.

### Pass 2 — at 1.0×, only the timestamps you flagged

Now watch only the segments you flagged, at normal speed, with the goal of writing the actual feedback. For each flagged moment, write a sentence about *what happened* and *what to do differently*.

Don't editorialize. Don't moralize. Don't catastrophize. Just describe:

> *04:30 — Match section ran 90 seconds. I added a paragraph comparing the problem to two-pointer, which wasn't asked for. Next time: deliver the 5-line memo, stop, wait for the interviewer to ask follow-ups.*

> *18:00 — Found the off-by-one but stayed silent during the fix. Interviewer saw the code change but didn't hear the reasoning. Next time: say "I see — index is off by one because the loop ends *after* the swap" before changing the code.*

That's the discipline. Observation, then prescription. Five to ten of those, and you have the raw material for the self-feedback write-up.

---

## 8. The self-feedback write-up

This is the deliverable. The file goes at `umpire-writeups/c2-week-04/mock-01-self-feedback.md` in your portfolio repo. Suggested structure (600–800 words):

```markdown
# Mock #1 — Self-Feedback

**Date:** YYYY-MM-DD
**Problem:** [name + LeetCode link]
**Flavor:** A (peer) / B (Pramp) / C (solo)
**Duration:** 45 minutes
**Outcome:** [solved correctly / solved with bug / didn't finish / etc.]

## What I felt during the mock

[3–5 sentences. Honest. "I felt rushed during Match." "I went silent for two minutes at the 18-minute mark." "I caught the off-by-one but didn't articulate the fix."]

## What the recording shows

[5–8 specific observations from your pass-2 timestamps. Each with a wall-clock timestamp.]

## The Match memo — graded

[Was it under 30 seconds? Did it name the pattern, the algorithm, the auxiliary state, and one negative-space rejection? Pull the actual transcript from your recording if you can.]

## The thinking-aloud — graded

[Did I go silent? When? For how long? Did I narrate pauses?]

## The recovery moves — graded

[When my first approach hit a wall, did I narrate the recovery? Or did I silently flail?]

## The Evaluate section — graded

[Did I produce the five-piece structure from Week 2? Did I deliver the amortized-O(n) / O(1)-space defense sentence cleanly?]

## ONE behavior change for Mock #2

[One sentence. Specific. Testable. "I will narrate every pause longer than 5 seconds" is good. "I will be more confident" is bad — not testable.]

## What I'm not going to do

[One or two things you noticed but are *not* going to change. The point of this section is to prevent over-correction. If you noticed you said "um" a lot, you might decide: "I'm not going to focus on filler words; that's a polish issue, not a substance issue."]
```

That structure is the rubric. It is also the artifact a senior engineer would read in 4 minutes and form a clear impression of your self-awareness.

---

## 9. The "one behavior change" rule

You will notice ten things wrong with your Mock #1. You will be tempted to fix all of them by Mock #2. Don't.

Pick **one**. Make it specific. Make it testable. Examples of well-formed behavior changes:

- *"I will deliver the Match memo in under 30 seconds, even if I have to cut content."*
- *"I will narrate every pause longer than 5 seconds with 'let me think about X for a moment.'"*
- *"I will start the Evaluate section out loud no later than the 35-minute mark, even if Implement isn't fully done."*
- *"I will diagram the linked list on Excalidraw before writing any code."*

Examples of poorly-formed behavior changes (avoid):

- *"I will be more confident."* — not testable.
- *"I will talk more."* — vague.
- *"I will solve faster."* — not under your direct control.
- *"I will fix all the things I noticed."* — too many; you'll fix none.

One change. Specific. Testable. Repeat that until it's reflexive.

---

## 10. Anti-patterns and how to spot them in your recording

Six patterns of poor behavior to scan for in pass 1.

### Anti-pattern 1: silent coding

You start writing code and stop talking. The screen shows progress; the audio shows nothing. Symptom: 30+ seconds of typing with no commentary.

### Anti-pattern 2: skipping Match

You read the prompt, you understand it, and you immediately start writing code. The interviewer has no idea what pattern you've identified. Symptom: I starts within 2 minutes of U.

### Anti-pattern 3: implementing without planning

You write the loop guard, then the body, then realize the body needs a different loop. You rewrite. You rewrite again. Symptom: code is rewritten more than once before any successful run.

### Anti-pattern 4: not tracing in Review

You declare the code done. You don't actually run a trace. You hope it's right. Symptom: R is < 2 minutes; no examples actually walked end-to-end.

### Anti-pattern 5: skipping Evaluate

You finish at 42 minutes and call it done. You never state time/space/tradeoff. Symptom: E is 0 minutes.

### Anti-pattern 6: defending broken code

You realize at minute 30 that the approach won't work. You keep going anyway, because backing out feels like failure. Symptom: code at minute 45 has known bugs that were visible at minute 30.

If pass 1 of your recording shows three or more of these, your Mock #2 plan writes itself: pick the worst one, make a specific behavior change.

---

## 11. After Mock #1 — the rest of Phase 1

Friday's mock + Saturday's self-feedback + Sunday's reflection is the closing arc of Phase 1. By Sunday night your portfolio repo should contain:

```
crunchtime-interview-prep-<you>/
├── umpire-writeups/
│   ├── c2-week-01/
│   ├── c2-week-02/
│   ├── c2-week-03/
│   └── c2-week-04/
│       ├── drill-01-linked-list-cycle.md
│       ├── drill-02-cycle-start.md
│       ├── drill-03-middle-of-list.md
│       ├── drill-04-happy-number.md
│       ├── challenge-01-reorder-linked-list.md
│       └── mock-01-self-feedback.md
├── mocks/
│   └── mock-01/
│       ├── recording-link.md      # link to the video, since the file is too big to commit
│       ├── immediate-notes.md     # 5-minute brain dump
│       └── timestamps.md          # pass-1 timestamps
├── study-plan/
│   └── phase-1-retrospective.md
└── behavioral/
    └── (Week 1–3 stories)
```

That tree is Phase 1's deliverable. If it's there and clean, you have proven you can run UMPIRE on four patterns and survive a recorded mock. You are ready for Phase 2.

---

## 12. Self-check

Without notes, answer:

1. **What are the three flavors of Mock #1, in descending fidelity order?** (Peer-to-peer, platform like Pramp, solo against a camera.)
2. **What's the recommended time allocation for the 45 minutes?** (Roughly: 3 U, 2 M, 5 P, 15 I, 10 R, 8 E, 2 wrap. Adjust as needed.)
3. **What's the two-pass watching protocol?** (Pass 1: full recording at 1.5× with timestamps. Pass 2: only flagged timestamps at 1.0× with prescriptions.)
4. **What's the one-behavior-change rule?** (Pick exactly one specific, testable behavior to change for Mock #2. Don't try to fix everything.)
5. **Name three of the six anti-patterns.** (Silent coding, skipping Match, implementing without planning, not tracing in Review, skipping Evaluate, defending broken code.)
6. **What's the 5-minute post-mock window for?** (Capturing raw observations while they're fresh, *before* the analytical work of Saturday.)

If you can answer all six without hesitation, you are ready for Mock #1. Set up the recording rig Monday. Schedule the slot Friday. Watch Saturday. Write Sunday.

---

## Further reading

- **The Wikipedia article on "self-confrontation"** — psychology term for watching recordings of yourself. The literature is small but consistent: first viewing is hardest; subsequent viewings calibrate.
- **Any short blog post on "How to watch yourself on video without flinching"** — performing-arts community has good material. Pick one. The advice generalizes.
- **interviewing.io's free blog**: <https://interviewing.io/blog> — the "lessons from 10,000 mock interviews" articles are gold. Read two before Friday.

Next: [exercises/README.md](../03-exercises/00-overview.md) to start the drills, or [mini-project/README.md](../07-mini-project/00-overview.md) to scope Mock #1.
