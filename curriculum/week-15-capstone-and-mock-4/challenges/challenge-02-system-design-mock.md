# Challenge 2 — System-Design Mock (45 minutes, junior level)

> **Format:** A 45-minute timed system-design mock round. **Difficulty:** Junior-level design — scoping, estimation, a clear high-level design, and trade-offs, not distributed-systems mastery. **Time:** 45 min for the round + ~30 min write-up and self-grade.

A junior onsite loop includes a system-design round, and it is the round most early-career candidates have practiced least. Drill 2 produced the URL-shortener write-up as a *studied* artifact; this challenge runs a design round as a *timed mock* on a fresh prompt — the rep that matters, because the real round is timed and unseen. You can run this standalone or fold it into Challenge 1's loop as the design round.

---

## The conditions

- **45-minute hard clock**, video on, narrate throughout (a design round is graded almost entirely on how you reason out loud).
- **Pick one prompt you have NOT written up.** If you did the URL shortener in Drill 2, pick a different one here.
- **A whiteboard surface** — Excalidraw (<https://excalidraw.com/>), a tablet, or paper. Drawing the high-level design is expected.

---

## The prompts (pick one)

1. **Design a pastebin.** Users paste text, get a short URL, and anyone with the URL can read the paste. (Closest cousin to the URL shortener — good if you want to reuse the ID-scheme reasoning.)
2. **Design a rate limiter.** A service that allows at most N requests per user per time window, used as a gate in front of an API. (Algorithm-flavored: token bucket vs. sliding window.)
3. **Design a news feed at small scale.** Users follow other users; the feed shows recent posts from the people they follow, newest first. (Fan-out-on-write vs. fan-out-on-read is the key decision.)

---

## The framework (the order to answer, with a per-phase clock)

| Phase | Wall-clock | What to do |
|------:|:----------:|------------|
| **Requirements** | 0:00 – 0:08 | Functional + non-functional. Ask clarifying questions. Scope DOWN — defer the optional features out loud. State the scale (QPS) and the read:write ratio. |
| **Estimation** | 0:08 – 0:15 | Back-of-envelope: QPS, storage, bandwidth. Real numbers. |
| **High-level design** | 0:15 – 0:28 | Draw the boxes: client → app servers → cache → store. Name the API. Name the data model. |
| **Deep-dive** | 0:28 – 0:40 | The one or two key decisions for *this* problem (see below). Defend the choice; name the rejected option. |
| **Trade-offs** | 0:40 – 0:45 | What breaks at 10× scale and what you'd change. Wrap up. |

The single most graded move: **scope the requirements and state the read:write ratio before you touch a database.** Jumping to "I'll use Postgres" in minute one is the round-killer — it shows you design before you scope.

---

## The key decision per prompt (the deep-dive)

- **Pastebin:** the ID scheme (hash vs. counter — identical reasoning to the URL shortener), plus where the paste *body* lives (a blob store, not the metadata DB, because pastes can be large).
- **Rate limiter:** the algorithm — **token bucket** (a bucket refills at a fixed rate; each request takes a token; reject when empty) vs. **sliding-window log/counter** (count requests in the trailing window). Token bucket is simpler and allows bursts; sliding window is more precise but stores more. Name both; pick token bucket for the common case; state where the counter lives (an in-memory store like Redis, keyed by user).
- **News feed:** **fan-out-on-write** (when a user posts, push it into every follower's precomputed feed — fast reads, expensive for users with many followers) vs. **fan-out-on-read** (assemble the feed at read time by querying the people a user follows — cheap writes, slower reads). At small scale, fan-out-on-read is simpler and fine; name the write-fan-out as the scale-up path and the "celebrity problem" (a user with millions of followers) as the reason real systems do a hybrid.

---

## A worked sketch — rate limiter (token bucket)

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

## Rubric

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

## What to commit

- `system-design/<prompt>.md` — the written version of your design (the URL shortener from Drill 2 plus this second one gives the repo two design write-ups).
- A recording link (in `mocks/` or alongside the design) of you talking through the 45 minutes.
- A self-grade against the rubric, with the one thing to improve for the next design round.

---

## Acceptance

Challenge 2 is complete when:

- A design round on a fresh prompt was run under the 45-minute clock, narrated and recorded.
- The written design is committed under `system-design/`, with all five framework phases present.
- The key decision is made explicitly with the rejected option's reason stated.
- A self-grade against the rubric is recorded.

That is the last challenge. Move to the [quiz](../quiz.md) — the final readiness self-assessment — then the [homework](../homework.md): the personalized go-forward study plan.
