# Exercise 2 — System-Design Write-Up (URL Shortener)

> **Type:** Capstone build step + the only new-content drill of the week. **Difficulty:** Junior-level design (matching the Week 12 design intro). **Target time:** 2.5 hours. **Why:** A junior onsite loop includes a system-design round. The capstone requires one written design artifact. This drill produces `system-design/url-shortener.md` — and it is the rehearsal for Challenge 2's design mock.

System design at the junior level is not about distributed-systems mastery. It is about a *framework*: scope the requirements, estimate the scale, propose an API and a data model, make one or two key design decisions explicitly, and reason about the read/write path. This drill walks the canonical junior prompt — a URL shortener at 10K QPS — and you write it up as a ~2–3 page artifact.

Attempt your own scoping first, from the framework below, *before* reading the worked brief. Then compare. The worked brief is your SOLUTIONS file — read it after, not instead of, your own attempt.

---

## The framework (the order you answer any design prompt)

1. **Requirements** — functional (what it does) and non-functional (scale, latency, availability). Scope *before* you design.
2. **Capacity estimation** — back-of-envelope: QPS, storage, bandwidth. Numbers, not vibes.
3. **API** — the handful of endpoints. Request/response shapes.
4. **Data model** — what you store and in what kind of store.
5. **The key decision** — for this problem, the ID scheme: hash vs. counter.
6. **Caching** — what to cache and why.
7. **The read/write path** — trace one write and one read end to end.
8. **Trade-offs** — what you would do differently at 10× the scale.

---

## The worked brief — URL Shortener at 10K QPS

### 1. Requirements

**Functional:**
- `shorten(long_url) → short_url` — given a long URL, return a short one (e.g., `short.ly/aB3dF9`).
- `redirect(short_url) → long_url` — given a short URL, redirect (HTTP 302) to the original.
- (Optional, scope-down candidates: custom aliases, expiration, analytics — *name them, then defer them* to keep the core tight.)

**Non-functional:**
- **Scale:** 10K QPS, read-heavy. Assume a 100:1 read:write ratio (people click short links far more than they create them) → ~100 writes/sec, ~10K reads/sec.
- **Latency:** redirects must be fast (<50 ms) — they are on the critical path of a user clicking a link.
- **Availability:** high — a dead redirect service breaks every link ever issued.

The single most important move in this section: **state the read-heavy ratio.** It is what justifies the caching decision later and signals you scope before you design.

### 2. Capacity estimation

```
Writes:   100/sec  × 86,400 sec/day ≈ 8.6M new URLs/day
Reads:    10,000/sec
5-year storage:  8.6M/day × 365 × 5 ≈ 15.7B URLs
Per record:  short code (7 bytes) + long URL (~500 bytes) + metadata (~100 bytes)
             ≈ ~600 bytes
Total storage:  15.7B × 600 bytes ≈ ~9.4 TB over 5 years
Short-code space:  base62 (a–z, A–Z, 0–9), 7 chars = 62^7 ≈ 3.5 trillion codes
```

The takeaways you state out loud: storage is in the **terabytes** (fits comfortably on a sharded store, not "too big to store"); the **7-character base62 code space (62^7 ≈ 3.5 trillion)** comfortably exceeds the 15.7B URLs we will ever issue, so 7 characters is enough.

### 3. API

```
POST /shorten
  Request:  { "long_url": "https://example.com/very/long/path?x=1" }
  Response: { "short_url": "https://short.ly/aB3dF9" }   (201 Created)

GET /{short_code}
  Response: 302 Found, Location: <long_url>
            404 if the code does not exist
```

REST, two endpoints. The redirect is a 302 (temporary) rather than 301 (permanent) so analytics counts every click and so the mapping can change — name the 301-vs-302 choice; it is a senior tell.

### 4. Data model

A single key→value mapping: `short_code → long_url` (plus `created_at`, optional `expires_at`, optional `owner`).

```
Table: urls
  short_code   VARCHAR(7)  PRIMARY KEY
  long_url     TEXT        NOT NULL
  created_at   TIMESTAMP
  expires_at   TIMESTAMP   NULL
```

The access pattern is a point lookup by `short_code` — that is the only query on the read path. A **key-value store** (or an indexed relational table) is the natural fit; the primary key on `short_code` gives O(1)-ish lookup. At 9.4 TB over five years, the store is sharded by `short_code`.

### 5. The key decision — the ID scheme (hash vs. counter)

This is the heart of the problem and the part interviewers probe. Two ways to generate the 7-character code:

**Option A — hash the long URL** (e.g., MD5/SHA, take the first 7 base62 chars):
- *Pro:* stateless; the same URL maps to the same code (natural dedup).
- *Con:* **collisions.** Two different URLs can hash to the same 7-char prefix. You must check-and-retry (re-hash with a salt) on collision — extra read per write. As the table fills, collisions get more frequent.

**Option B — a global counter** (auto-increment integer, base62-encoded):
- *Pro:* **no collisions** — every code is unique by construction. Simple.
- *Con:* needs a globally-unique counter, which is a coordination point. At 100 writes/sec a single counter is fine; at 10× you'd hand out ranges (e.g., each app server pre-allocates a block of 1,000 IDs from the counter and serves them locally — the "ticket server" / range-allocation pattern).
- *Con:* codes are sequential and guessable; if that matters, base62-encode the counter through a bijective scramble (e.g., a Feistel/XOR permutation) so codes look random but stay collision-free.

**The recommendation to state:** at 10K QPS, **the counter scheme** (Option B) is the cleaner choice — no collision-retry on the write path, and 100 writes/sec is well within a single counter or a simple range-allocator. Name the hash option, name *why you rejected it* (collision handling adds a read to every write), and pick the counter. Making the decision explicitly — and defending the rejection — is exactly what the round grades.

### 6. Caching

The system is read-heavy (100:1), redirects are latency-critical, and the access pattern is "a small set of links get most of the clicks" (a hot/popular-link distribution). That is the textbook case for a **read-through cache** (e.g., an in-memory cache like Redis/Memcached) in front of the store:

- On `redirect`, check the cache first. **Cache hit** → return immediately (sub-millisecond). **Cache miss** → read the store, populate the cache, return.
- Eviction: **LRU** — popular links stay hot, cold links fall out. (LRU is the cache-replacement policy you implemented conceptually in the catalog; name it.)
- The cache absorbs the bulk of the 10K read QPS, so the store sees only the misses — which is what makes the <50 ms latency target achievable.

### 7. The read/write path

**Write (`shorten`):**
1. Client `POST /shorten` with the long URL.
2. App server takes the next ID from the counter / range allocator.
3. Base62-encode the ID → the 7-char short code.
4. Write `(short_code, long_url, created_at)` to the store.
5. Return `short.ly/{short_code}`.

**Read (`redirect`):**
1. Client `GET /{short_code}`.
2. App server checks the cache for `short_code`.
3. **Hit:** return `302 → long_url` (sub-ms).
4. **Miss:** read the store; if found, populate the cache and return `302 → long_url`; if not, `404`.

That is the whole system, traced end to end.

### 8. Trade-offs (at 10× the scale)

- **Counter coordination** becomes the bottleneck → move to range-allocation (each server pre-allocates ID blocks), or a distributed ID generator (e.g., a Snowflake-style scheme).
- **Single store** → shard by `short_code` prefix; add read replicas for the read-heavy load.
- **Cache** → distribute it; a cache cluster with consistent hashing.
- **Single region** → multi-region with the cache near the user, since redirect latency is the SLA.

Stating "here is what I'd change at 10×" without over-building for it now is the junior-to-mid signal: you scoped for the stated 10K QPS and you know where it breaks next.

---

## Acceptance criteria

- [ ] `system-design/url-shortener.md` exists in the repo, ~2–3 pages.
- [ ] All eight framework sections are present and in order.
- [ ] The read-heavy ratio is stated and used to justify the cache.
- [ ] The capacity estimation has real numbers (QPS, storage, code-space).
- [ ] The hash-vs-counter decision is made explicitly, with the rejected option's reason stated.
- [ ] One write path and one read path are each traced end to end.
- [ ] The "at 10× scale" trade-offs are named without over-building the base design.

---

## What to commit

- `system-design/url-shortener.md` — your write-up (your own scoping, refined against this brief).
- Optionally a hand-drawn or ASCII high-level diagram (`client → app server → cache → store`); a diagram in the write-up is a strong recruiter-scan signal.

If you finish early, draft a second design from Challenge 2's prompt list (pastebin, rate limiter, news feed at small scale) — a second design write-up signals the first was not a one-off.

---

Next: [Exercise 3 — Recruiter-Prep Pack](./exercise-03-recruiter-prep-pack.md) — resume, target list, and outreach templates.
