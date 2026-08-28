# Problem 5 — System-Design Ground Zero #4

<!-- no-runnable-file: this problem's deliverable is a 300-word design write-up, not a program -->

> **Topic:** the fourth system-design warm-up — detecting that something has *stopped* happening
> **Lecture:** [02 — The Mock Interview Protocol](../lecture-notes/02-the-mock-interview-protocol.md), §5
> **Difficulty:** Easy to answer, hard to answer well
> **Target time:** 45 minutes — about 25 writing, 20 reading afterwards
> **Why this one:** it is the same family of thinking as this week's pattern. Cycle detection asks "does this keep going forever?" Idle detection asks "has this stopped?" Both are questions about a process you cannot watch directly, answered by keeping a small amount of state and checking it on a schedule.

## The Brief

The question, and you answer it in about 300 words:

> **"How would you design a system that detects, in real time, when a user's
> session has gone idle — no activity in 30 minutes?"**

The rule for these warm-ups is fixed and it matters: **do not look up the
canonical answer first.** Write what you would actually say in an interview
today, with the knowledge you have right now. Then go and read, and note what
you would add.

That order is the entire exercise. Reading first produces a good essay and
teaches you nothing about where your gaps are. Writing first produces a worse
essay and a precise list of the things you did not think of — which is the
thing you are actually collecting.

**What "idle" makes hard, in plain terms.** Imagine a room with ten thousand
people in it, and you have to notice the moment any one of them stops talking
for thirty minutes. You could walk round the room every minute checking
everyone — expensive, and you do it ten thousand times a minute to catch
perhaps three people. Or you could give each person an egg timer, reset it every
time they speak, and wait for a ding — cheap to reset, but now you are holding
ten thousand egg timers.

That tension — **scan everything periodically** versus **hold a timer per
thing** — is the design decision, and an answer that names it is already better
than most.

**The connection to this week.** Detecting that something has not happened is
the passive twin of cycle detection. In both cases you cannot see the whole
process; you keep a small piece of state and check a condition against it. In
Floyd's the state is two pointers and the condition is "did they meet". Here
the state is a last-seen timestamp and the condition is "is now minus last-seen
past the threshold". Same mental model, and worth one sentence in your answer.

## Starter

Create `system-design/notes-week-04.md` in your portfolio repo and paste this
in. Fill in every `TODO`.

```markdown
# Week 4 — System-design warm-up

**Question:** How would you design a system that detects, in real time, when a
user's session has gone idle (no activity in 30 minutes)?

**Written before reading anything:** TODO (date)

## My answer, cold

TODO: about 300 words. Write it as you would say it. Cover, at minimum:
  - what counts as "activity", and where you record it
  - what you store per session, and how big that is
  - how the idle condition is actually noticed
  - what "real time" is allowed to mean here, in seconds
  - one thing that goes wrong at scale

## What I read afterwards

TODO: two searches, one article each.
  - "session timeout sliding window" -> link, one line on what it said
  - "TTL cache for sessions" -> link, one line on what it said

## Three things I would add

TODO: exactly three. Be specific. "Use Redis" is not one of them; "use a Redis
key with a 30-minute TTL, refreshed on each request, and subscribe to the
expiry event" is.

## What I got right, cold

TODO: one or two. Worth recording — the point of this series is to watch this
section grow across the weeks.
```

## Requirements

1. The file exists at `system-design/notes-week-04.md` in your portfolio repo.
2. The cold answer is about 300 words — call it 250 to 400.
3. It was written **before** you searched for anything, and the file says the
   date.
4. It names what counts as activity, what you store per session, and how the
   idle condition is noticed.
5. It states what "real time" is allowed to mean here as a number of seconds.
6. You then read one free article on each of two searches, and linked both.
7. There are **exactly three** things you would add, each specific enough to
   implement.
8. There is a short "what I got right" section.

## Constraints

- **Write cold, and the file has to say when.** The date is there to keep you
  honest with yourself. The value of this series is the gap between the cold
  answer and the read-afterwards answer, and that gap only exists if the cold
  answer really was cold.

- **About 300 words, because that is roughly the length of a spoken opening.**
  This is a warm-up, not a design document. In a real system-design round your
  first pass at the whiteboard is two or three minutes before the interviewer
  starts steering, and 300 words is about that. Practising at the right length
  is the point.

- **Exactly three additions, no more.** Four means you did not choose. The
  discipline of picking the three most load-bearing things you missed is the
  same discipline as the one-behaviour-change rule for
  [Mock #1](../mini-project/README.md), and for the same reason: a list of ten
  improvements gets none of them.

- **No naming a product as an answer.** "Use Redis" is a shopping decision, not
  a design. Say what property you need — expiry you do not have to poll for,
  say — and then name the product as an example of something that has it. An
  interviewer who does not use your favourite product needs to be able to follow
  you anyway.

- **You must state what "real time" means in seconds.** The phrase is in the
  question and it is the ambiguity the question is built around. Thirty minutes
  plus five seconds and thirty minutes plus five minutes are wildly different
  systems at wildly different costs, and a candidate who does not ask has
  skipped the most important clarifying question available.

## Expected output

There is no program here, so what follows is a worked excerpt rather than
captured stdout: the *"three things I would add"* section of a strong write-up,
which is the section that shows whether the reading did anything.

```text
## Three things I would add

1. Store the session as a single key with a 30-minute time-to-live, refreshed
   on every request, and subscribe to the store's key-expiry notification
   instead of polling. That turns "notice the absence of something" into
   "receive an event", which is the whole shape of the problem. I had invented
   a per-minute sweep; this is strictly better and I did not know it existed.

2. Do not trust the expiry event as the only signal. Expiry notifications are
   usually best-effort — they can be dropped on failover or under load — so keep
   a slow sweep, every few minutes, as a backstop that catches anything the
   event stream missed. I had one mechanism; the real answer has a fast one and
   a slow one, and the slow one exists because the fast one lies occasionally.

3. Name the clock problem explicitly. Two servers with a two-second skew will
   disagree about whether a session expired, and if the write path and the sweep
   run on different machines you get sessions that expire and un-expire. Either
   have the store own the clock, or record activity as a monotonic sequence
   number rather than a wall-clock timestamp.
```

Notice what those three have in common. Each names a mechanism precisely enough
to build, each says what the cold answer had instead, and none of them is a
product name standing in for a decision.

## Steps

1. **Set a 25-minute timer and write the cold answer. Do not open a search
   box.** If you get stuck, write down the thing you are stuck on — a gap you
   can name is worth more than a paragraph you copied.
2. **Before you finish, make sure you answered the ambiguity.** How late is a
   detection allowed to be? Say a number. If you did not think about it while
   writing, add a sentence now and note that you added it — that is a real
   finding about how you approach an underspecified question.
3. **Stop. Save. Put the date in.** The cold answer is now fixed and you do not
   edit it again.
4. **Search "session timeout sliding window" and read one free article.** You
   are looking for how the reset-on-activity idea is actually implemented, and
   what a sliding window costs compared with a fixed one.
5. **Search "TTL cache for sessions" and read one free article.** You are
   looking for expiry that you do not have to poll for, and — importantly — for
   what its guarantees are *not*.
6. **Write exactly three additions.** For each, say what the cold answer had
   instead. The contrast is what makes it a lesson rather than a note.
7. **Write what you got right.** Genuinely — this section is the reason the
   series is worth doing four times. By Week 13 it should be most of the page.
8. **Commit it.**

## The Solution

There is no program here, and no single correct design — the deliverable is your
own answer, cold, plus what you learned when you went and read. What can be
published is a strong version of the cold answer, so you have something to
compare shape against rather than content.

```markdown
## My answer, cold

First, what counts as activity. I would say: any authenticated request that
reaches the application, excluding health checks and background polling from the
client, because a browser tab that refreshes a dashboard every 10 seconds should
not keep a session alive forever. That exclusion is a product decision and I
would confirm it before building anything.

What I store per session is one record: session id, user id, and a last-seen
timestamp. That is small — call it 100 bytes — so a million live sessions is
about 100 MB, which fits in one in-memory store and does not need to be a
database.

How the idle condition gets noticed is the real decision, and there are two
shapes. One: a sweep. Every minute, walk the sessions and mark anything whose
last-seen is more than 30 minutes ago. Simple, and the cost is proportional to
all sessions rather than to the ones actually expiring. Two: a timer per
session, reset on activity, which is cheap to check and expensive to reset —
every single request touches a timer.

I would start with the sweep, because it is one moving part and the write path
stays a single field update. To keep the sweep cheap I would keep sessions in
last-seen order, so it only has to look at the oldest ones and can stop as soon
as it finds one that is still fresh.

"Real time" needs a number. I would ask for it, and propose 60 seconds: a
session is detected as idle within a minute of the 30-minute mark. That lets the
sweep run once a minute rather than continuously.

What breaks at scale is the write path. If every request updates a timestamp,
a busy user writes hundreds of times a minute for no benefit. I would only
refresh the timestamp if it is more than a minute stale.
```

**Why the "what counts as activity" paragraph is first.** It is the question the
problem statement does not answer, and the one where a wrong assumption makes
every later decision wrong. Starting with the ambiguity rather than the
architecture is a Frame move, and it is graded in a design round the same way it
is graded in a coding round.

**Why the storage estimate is there.** Three numbers — 100 bytes, a million
sessions, 100 MB — settle a question that would otherwise be argued about: does
this need a database? It does not. One arithmetic sentence removes a whole
branch of the design, and doing that early is a senior habit.

**Why both mechanisms are named before one is chosen.** The answer describes the
sweep and the per-session timer, says what each costs, and then picks with a
reason. An answer that presents one design as obvious cannot be reasoned with;
an answer that presents the tradeoff can be steered by the interviewer, which is
what they are there to do.

**Why the sorted-by-last-seen detail matters.** It turns the sweep from
"proportional to all sessions" into "proportional to the ones that actually
expired", which is the difference between a design that works at a million
sessions and one that does not. It is also the sort of concrete improvement that
is hard to invent under pressure and easy to remember once you have seen it.

**Why "real time" gets a number.** Sixty seconds is not the only right answer;
naming a number at all is. The interviewer now knows what you are optimising
and can push back — "what if the security team wants five seconds?" — which is
where the interesting part of the conversation lives.

**Why the last paragraph is about the write path.** The naive design writes on
every request, and the fix — only refresh a stale timestamp — costs one
comparison and removes most of the writes. Ending on a specific scaling problem
with a specific mitigation is a much stronger close than a summary.

## Download and run

There is nothing to download and nothing to run — the deliverable is your own
write-up, and the whole exercise depends on it being written before you read
anyone else's.

From your portfolio repo:

```bash
wc -w system-design/notes-week-04.md
```

Confirm the cold section is roughly 300 words, then commit:

```bash
git add system-design/notes-week-04.md
git commit -m "Add Week 4 system-design warm-up: idle session detection"
```

## Common bugs to catch

- **Reading first.** Symptom: the cold answer mentions key-expiry events and
  clock skew. Those are things you learn by reading, not by thinking, and their
  presence means the exercise was skipped. There is nothing to fix in the file;
  just do it in the right order next week.

- **No definition of "activity".** Symptom: the answer goes straight to storage.
  Every later decision then rests on an assumption nobody stated, and in a real
  round the interviewer will find it and the design will unravel.

- **No number for "real time".** Symptom: the phrase is repeated rather than
  resolved. This is the single most common miss on this question.

- **A product name doing the work of a design.** Symptom: "I'd use Redis" and
  then nothing about what property of it you are relying on. Fix: name the
  property — expiry without polling — and then say what has it.

- **The sweep with no ordering.** Symptom: "every minute, check all sessions."
  Correct and expensive. It is fine as a starting point *if* you say it is a
  starting point and name the cost; it is a weak answer if you present it as
  finished.

- **More than three additions.** Symptom: a list of six. You did not choose,
  which means you did not rank, which means you have not decided what the
  important part was.

- **A "what I got right" section left empty.** Symptom: an honest first attempt
  graded as if it were worthless. Something was right. Say what, because the
  growth in this section is the only evidence you are collecting across the four
  weeks.

## Under the hood

<details>
<summary>Under the hood — why "detect the absence of something" is a whole class of problem</summary>

**Absence is harder than presence, and the reason is structural.** An event that
happens can carry itself to you — it arrives, you handle it. An event that fails
to happen carries nothing. Somebody has to go and look, or somebody has to have
set a timer in advance. There is no third option, and every design in this space
is one of those two wearing different clothes.

That is why the sweep-versus-timer tension shows up everywhere: session idle
detection, TCP keepalives, heartbeat monitoring between services, cache
expiry, dead-letter queues, watchdog timers in embedded firmware. Recognising a
new problem as a member of this family is worth more than any single design.

**The timing-wheel is the trick that makes per-thing timers cheap.** Holding a
million individual timers sounds impossible, and it is if each one is its own
scheduled task. A timing wheel is an array of buckets, one per tick, where each
thing is filed into the bucket for the tick it expires at. Resetting a timer is
moving it between two buckets — O(1). Firing is emptying one bucket per tick,
regardless of how many timers exist. It is the structure inside most kernels'
timer implementations and inside several message brokers' delayed-delivery
features, and it is a genuinely good thing to be able to sketch.

**Sliding versus fixed windows, precisely.** A *sliding* expiry resets the
30-minute clock on every activity, so a session survives as long as the user
keeps using it. A *fixed* expiry ends the session 30 minutes after it started,
regardless. Real systems usually run both — a sliding idle timeout and a fixed
absolute timeout — because the sliding one alone lets a session live forever,
which is a security problem rather than a design one. If your cold answer only
had the sliding one, that is a very common gap and worth being one of your
three.

**Expiry notifications are best-effort almost everywhere, and this surprises
people.** Systems that fire an event when a key expires usually document the
event as fire-and-forget: not persisted, not retried, dropped if no subscriber
is connected, and in some configurations delivered only when something happens
to touch the key. Building a billing or security decision on top of one, with no
backstop, is a well-known way to discover this at three in the morning. The
sweep does not go away when you add events; it slows down.

**Where this connects back to the week.** Both cycle detection and idle
detection answer a question about an unbounded process using a bounded amount of
state, checked against a condition. Floyd's holds two pointers and asks "have
they met". Idle detection holds one timestamp and asks "is the gap too big".
Neither can afford to remember the whole history, and in both cases the design
work is choosing what small thing to keep. That framing — *what is the smallest
state that answers this question?* — is worth carrying into Phase 2.

</details>

## Acceptance checklist

- [ ] `system-design/notes-week-04.md` exists in your portfolio repo and is
      committed.
- [ ] The cold answer is 250 to 400 words and was written before any searching.
- [ ] The file records the date the cold answer was written.
- [ ] The cold answer says what counts as activity.
- [ ] The cold answer gives a number of seconds for "real time".
- [ ] The cold answer names at least one thing that breaks at scale.
- [ ] Two searches were done and one article per search is linked.
- [ ] There are exactly three additions, each specific enough to implement.
- [ ] No product name stands in for a design decision.
- [ ] There is a non-empty "what I got right, cold" section.

## Stretch

- **Sketch the timing wheel.** Draw the array of buckets, show where a session
  sits, and show what happens when it is reset. Ten minutes with a pen, and it
  turns a term you read into a structure you could implement.

  ```text
  tick:   0    1    2    3   ...  29
  bucket [ ]  [ ]  [s7] [ ]  ...  [s1,s4]
  reset s7 -> move it from bucket 2 to bucket (now + 30) mod 30
  ```

- **Work out the write amplification with real numbers.** A million sessions, an
  average of ten requests a minute each, one timestamp write per request: ten
  million writes a minute. Now apply the "only refresh if more than a minute
  stale" rule and recompute. The size of the difference is the argument, and
  having done the arithmetic once means you can do it out loud under pressure.

- **Ask the harder follow-up on yourself.** *What if a session must be detected
  as idle within one second?* Everything changes: the sweep is now sixty times
  more expensive, the timer approach starts to win, and clock skew stops being
  a footnote. Write 100 words on how your design shifts. Interviewers love
  changing a number and watching what you do.

Next: [Problem 6 — The Phase-1 Retrospective](./problem-06-phase-1-retrospective.md).
