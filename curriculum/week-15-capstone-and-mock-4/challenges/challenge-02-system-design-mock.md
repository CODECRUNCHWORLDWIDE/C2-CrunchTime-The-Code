# Challenge 2 — The System-Design Mock

> Format: a 45-minute timed design round on a prompt you have not written up · Time: 45 minutes on the clock, plus about 30 minutes to write up and self-grade · Difficulty: junior level — scoping, estimation, a clear high-level design and trade-offs, not distributed-systems mastery · Why this one: it is the round most early-career candidates have practised least, and the only one where the whole grade is how you reason out loud.

<!-- deliverable-page: the answer is a recorded design round and its self-grade, not a program -->

## The Brief

A junior onsite loop includes a system-design round. It is almost always the
round with the least preparation behind it, partly because it feels unteachable
and partly because there is no obvious way to practise it alone.

There is. [Exercise 2](../exercises/exercise-02-system-design-writeup.md) produced
a design write-up as a *studied* artifact, with time to think. This challenge runs
a design round as a *timed mock* on a fresh prompt, which is the rep that
actually transfers — the real round is timed and the prompt is unseen.

Run it standalone, or fold it into [Challenge 1](./challenge-01-mock-4-full-loop.md)
as that loop's design round.

The deliverable is a recording, the diagram you drew, and your self-grade against
the rubric.

## Starter

The prompts, the phase clock and the rubric are the starter.
They are under Requirements below. Read the framework and the rubric now;
read the worked sketch under `## The Solution` only after your round.

## Requirements

1. One 45-minute recorded round on a prompt you have **not** written up before.
2. A diagram, drawn during the round rather than after it.
3. A self-grade against the rubric below.
4. A written note on the one phase you overran and what you would cut next time.

### The prompts — pick one

1. **Design a pastebin.** Users paste text, get a short URL, and anyone with the URL can read the paste. (Closest cousin to the URL shortener — good if you want to reuse the ID-scheme reasoning.)
2. **Design a rate limiter.** A service that allows at most N requests per user per time window, used as a gate in front of an API. (Algorithm-flavored: token bucket vs. sliding window.)
3. **Design a news feed at small scale.** Users follow other users; the feed shows recent posts from the people they follow, newest first. (Fan-out-on-write vs. fan-out-on-read is the key decision.)

---

### The framework, with a clock

| Phase | Wall-clock | What to do |
|------:|:----------:|------------|
| **Requirements** | 0:00 – 0:08 | Functional + non-functional. Ask clarifying questions. Scope DOWN — defer the optional features out loud. State the scale (QPS) and the read:write ratio. |
| **Estimation** | 0:08 – 0:15 | Back-of-envelope: QPS, storage, bandwidth. Real numbers. |
| **High-level design** | 0:15 – 0:28 | Draw the boxes: client → app servers → cache → store. Name the API. Name the data model. |
| **Deep-dive** | 0:28 – 0:40 | The one or two key decisions for *this* problem (see below). Defend the choice; name the rejected option. |
| **Trade-offs** | 0:40 – 0:45 | What breaks at 10× scale and what you'd change. Wrap up. |

The single most graded move: **scope the requirements and state the read:write ratio before you touch a database.** Jumping to "I'll use Postgres" in minute one is the round-killer — it shows you design before you scope.

---

### The key decision per prompt

- **Pastebin:** the ID scheme (hash vs. counter — identical reasoning to the URL shortener), plus where the paste *body* lives (a blob store, not the metadata DB, because pastes can be large).
- **Rate limiter:** the algorithm — **token bucket** (a bucket refills at a fixed rate; each request takes a token; reject when empty) vs. **sliding-window log/counter** (count requests in the trailing window). Token bucket is simpler and allows bursts; sliding window is more precise but stores more. Name both; pick token bucket for the common case; state where the counter lives (an in-memory store like Redis, keyed by user).
- **News feed:** **fan-out-on-write** (when a user posts, push it into every follower's precomputed feed — fast reads, expensive for users with many followers) vs. **fan-out-on-read** (assemble the feed at read time by querying the people a user follows — cheap writes, slower reads). At small scale, fan-out-on-read is simpler and fine; name the write-fan-out as the scale-up path and the "celebrity problem" (a user with millions of followers) as the reason real systems do a hybrid.

---

### Rubric

Total possible: 100; passing: 70.

| Dimension | Points | What "full credit" looks like |
|-----------|-------:|-------------------------------|
| Requirements scoped first | 20 | Functional + non-functional; clarifying questions asked; optional features deferred; scale + read:write ratio stated |
| Capacity estimation | 15 | Real numbers — QPS, storage, payload sizes — not hand-waving |
| High-level design | 20 | The boxes drawn (client → servers → cache → store); API + data model named |
| The key decision defended | 25 | The prompt's central trade-off named, a choice made, the rejected option's reason stated |
| Trade-offs at scale | 10 | What breaks at 10× and what you'd change, without over-building the base |
| Narration | 10 | Reasoned out loud throughout; no long silent stretches |

The heaviest weight is on **the key decision defended** — that is the senior tell in a design round: not that you reached an answer, but that you considered the alternative and can say why you rejected it.

---

## Constraints

- **45-minute hard clock**, video on, narrate throughout (a design round is graded almost entirely on how you reason out loud).
- **Pick one prompt you have NOT written up.** If you did the URL shortener in Exercise 2, pick a different one here.
- **A whiteboard surface** — Excalidraw (<https://excalidraw.com/>), a tablet, or paper. Drawing the high-level design is expected.

---

- **Scope before you name a database.** Requirements and the read-to-write ratio
  come first. "I'll use Postgres" in minute one is the round-killer, because it
  shows you design before you scope.
- **Real numbers in the estimation phase.** "A lot of traffic" is not an
  estimate. Say the QPS, the storage, the bandwidth, and be wrong by an order of
  magnitude rather than silent.
- **Name the rejected option.** Every deep-dive has two credible answers, and
  picking one without naming the other reads as not knowing there was a choice.
- **Draw.** A design round with no diagram is a conversation, and it is graded as
  one.
- **Stop at 45 minutes** even mid-sentence. The wrap-up phase exists because real
  rounds end on the clock, and practising the ending is part of the exercise.

## Expected output

What the round should produce:

```text
round length        45 min, hard stop
requirements        0:00-0:08   functional, non-functional, scope cut out loud
estimation          0:08-0:15   QPS, storage, bandwidth, in numbers
high-level design   0:15-0:28   boxes drawn, API named, data model named
deep-dive           0:28-0:40   one or two decisions, with the rejected option
trade-offs          0:40-0:45   what breaks at 10x, and what you would change

artifacts           one recording, one diagram, one self-grade
```

The phase you overrun is the finding. Nearly everybody overruns the high-level
design and arrives at the deep-dive with six minutes left — and the deep-dive is
the phase that carries most of the grade. Knowing that about yourself before the
real round is most of what this challenge is for.

## Steps

1. Pick a prompt you have not written up. If you did the URL shortener in
   Exercise 2, do not pick the pastebin either — it is the same reasoning.
2. Set up: video on, whiteboard surface ready, timer visible.
3. Run the 45 minutes narrating throughout. Say the clock out loud at each phase
   boundary; it is what keeps the pacing honest.
4. Stop on the clock.
5. Self-grade against the rubric before watching the recording — your memory of a
   round and the recording of it disagree, and the gap is informative.
6. Watch it, note where each phase actually ended, and write the one-phase note.
7. Compare with the worked sketch below.

## The Solution

A design round has no single right answer, so the worked answer here is the
**deep-dive** — the phase that carries the grade and the phase most often reached
with no time left.

To calibrate the depth expected, here is the deep-dive for the rate limiter, compressed:

> *"Requirements: allow at most N=100 requests per user per minute, reject the rest with HTTP 429, used as a gate in front of an API at ~10K QPS total. Non-functional: low added latency (it's on every request's critical path) and it must be shared across app servers, so the state can't live in one server's memory.*
>
> *Estimation: 10K QPS, each check is one read-modify-write of a small counter → ~10K ops/sec on the rate-limit store, tiny payloads. The store holds one bucket per active user — millions of small keys, well within an in-memory store.*
>
> *High-level: client → API gateway → token-bucket check against a shared Redis → allow (forward) or 429. Each user has a bucket `{tokens, last_refill}`. On a request: refill tokens based on elapsed time since `last_refill` (rate × elapsed, capped at N), then if tokens ≥ 1, decrement and allow, else reject.*
>
> *Deep-dive — why token bucket over sliding-window log: the log stores a timestamp per request (memory grows with traffic); the token bucket stores two numbers per user regardless of traffic, and it naturally allows short bursts up to N, which is usually desirable. The trade-off: the bucket is slightly less precise at window boundaries than an exact log. For a gate, that's fine.*
>
> *Concurrency: the read-modify-write on the bucket must be atomic across app servers, or two simultaneous requests both see one token left and both pass. Solve with an atomic Redis operation (a Lua script, or `INCR` with expiry for the simpler fixed-window variant).*
>
> *Trade-offs at 10×: a single Redis becomes the bottleneck → shard buckets by user-id hash; or push an approximate limiter to each app server (local token buckets that sync periodically) to cut the per-request network hop, trading precision for latency."*

That is ~3 minutes spoken and it hits requirements → estimation → design → the key decision (bucket vs. log) with a defended rejection → a concurrency subtlety → scale trade-offs. That is the target depth for a junior round.

---

Notice what that sketch does and does not do. It names both algorithms, picks
one, says why, and says where the state lives. It does not enumerate every
possible design; it commits, and then says what would change the commitment.
That is the shape to reproduce for whichever prompt you pick.

## How to deliver it

Record the round with video on — a design round is partly about how you use the
board, and audio alone loses that.

Export the diagram as an image or a link and commit it with the notes:

- `system-design/<prompt>.md` — the written version of your design (the URL shortener from Exercise 2 plus this second one gives the repo two design write-ups).
- A recording link (in `mocks/` or alongside the design) of you talking through the 45 minutes.
- A self-grade against the rubric, with the one thing to improve for the next design round.

---

## Common bugs to catch

- **Naming a datastore before scoping.** Symptom: eight minutes of design against
  requirements nobody agreed. The most common single failure in this round.
- **Estimating in adjectives.** Symptom: "high traffic", "quite a lot of
  storage". Be wrong in numbers rather than vague in words.
- **Designing for scale nobody asked for.** Symptom: sharding and a message queue
  on a system with 10,000 users. Scoping down out loud scores; over-building does
  not.
- **A deep-dive with one option in it.** Symptom: a confident choice that reads as
  the only thing you know.
- **No diagram.** Symptom: a round that sounds fine on the recording and left
  nothing behind.
- **Running long on the high-level design.** Symptom: six minutes for the
  deep-dive and no trade-offs at all. It is the standard overrun; watch for it
  specifically.
- **Self-grading from memory.** Symptom: a grade that is kinder than the
  recording. Grade first, then watch, and keep both.

## Acceptance checklist

Challenge 2 is complete when:

- [ ] A design round on a fresh prompt was run under the 45-minute clock, narrated and recorded.
- [ ] The written design is committed under `system-design/`, with all five framework phases present.
- [ ] The key decision is made explicitly with the rejected option's reason stated.
- [ ] A self-grade against the rubric is recorded.

That is the last challenge. Move to the [quiz](../quiz.md) — the final readiness self-assessment — then the [homework](../homework/README.md): the personalized go-forward study plan.

## Stretch

- Run a second round on a different prompt a week later and compare the phase
  timings. The content improves slowly; the pacing improves fast, and the pacing
  is what the clock grades.
- Take the prompt you picked and write the 10× version — what breaks first, and
  what you would change. It is the trade-offs phase with time to think, and it
  makes the next round's last five minutes much easier.
- Do the round once with **no diagram allowed**, deliberately. It is much harder,
  and it shows you exactly how much of your reasoning the drawing was carrying.
