# Week 5 — Challenges

One challenge this week. It is the hardest binary-search shape in the course — the kind of problem that, when solved cleanly, signals senior-level binary-search fluency.

| # | Challenge | Pattern | Difficulty | Target solve time |
|---|-----------|---------|------------|------------------:|
| 1 | [The Merged Book Boundary](challenge-01-order-book-boundary.md) | Binary search on a **partition predicate** — the lower-bound idea applied to a split across two sorted sequences | Hard | 90 min |

The challenge composes the lower-bound template (from Drills 1-2) with a non-obvious *partition predicate*. The boundary defense for this problem is the strictest of the week — read the prompt twice, draw the partition out by hand, and commit to a convention before writing code.

Why this matters: the two-sorted-sequences partition search is the binary-search shape most often asked at senior onsites, not because the algorithm is novel but because it tests three independent skills at once — honouring an asymptotic spec when a simpler slower alternative is sitting right there, *inventing* the predicate rather than being handed it, and defending the boundary (sentinels, the swap, the clamp, `<=` versus `<`) all in one problem. If you can deliver FRAME on it cleanly in 90 minutes the first time and 45 minutes the second, you have reached a level few candidates hit in a 15-week prep cycle.

If you find yourself stuck past the 60-minute mark, **stop and re-read Lecture 1 §6 (lower bound) and Lecture 2 §3 (the three-step recipe)**. Then restart Assess options with the partition predicate written out by hand. The algorithm cannot be derived without the picture; trying to write code before the picture is the source of every wrong attempt.

The challenge has a structural cousin in the homework — [Problem 3, The Ridge Line](../homework/README.md) — which applies the same "invent the predicate on a sequence that is not sorted" move in a much easier shape. If the challenge feels overwhelming, do the Ridge Line first as a warm-up, then return.
