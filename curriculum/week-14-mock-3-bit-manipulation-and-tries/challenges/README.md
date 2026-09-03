# Week 14 — Challenges

Two challenges. Both are required this week — Challenge 1 is the centerpiece of the mock week, and Challenge 2 is the senior-signal bit problem.

| # | Challenge | Pattern | Difficulty | Target solve time |
|---|-----------|---------|------------|------------------:|
| 1 | [Mock #3 — Timed Round](./challenge-01-mock-3-timed-round.md) | Full-loop mock under near-real conditions | — (a mock, not a problem) | 45 min hard clock + 90 min review |
| 2 | [The Ledger Adder](./challenge-02-ledger-adder.md) | Addition assembled from AND, XOR and shift, on a 16-bit board | Medium | 60 min including the FRAME write-up |

Challenge 1 is the week. It is not an algorithm problem — it is the protocol for running Mock #3 as a recorded full loop under near-real conditions: video on, a hard 45-minute clock, no peeking. The deliverable is a recording, a two-pass self-feedback note, and the trajectory comparison across Mock #1 → #2 → #3.

Challenge 2 is the bit problem that most cleanly separates strong candidates: add two integers without using `+` or `-`, simulating a 32-bit adder with XOR for the sum-without-carry and `(a & b) << 1` for the carry — and handling Python's unbounded-int subtlety with a `& 0xFFFFFFFF` mask. The masking detail is a genuine senior signal.

---

## What a complete challenge write-up looks like

For Challenge 2 (the algorithm problem), the deliverable is:

1. **A FRAME write-up** — under `frame-writeups/c2-week-14/challenges/`. Full five sections; the Research constraints section opens with the 30-second pattern-recognition memo from the challenge file.
2. **A working implementation** — committed as `challenges/sum-of-two-integers.py` in your portfolio. Must pass the test cases listed in the challenge file.
3. **A recording** — minimum 10 minutes, walking through the Research constraints → Assess options → Make the solution narration. The masking subtlety should be narrated explicitly.

For Challenge 1 (the mock), the deliverable is the recording link, the immediate notes, the pass-1 timestamps, and the self-feedback write-up — see the challenge file for the exact artifact list.

---

## A note on the mock as the keystone of the week

Mock #3 is the highest-signal artifact you will produce this week — higher than any single bit exercise. Three reasons:

1. **It is the first full-loop simulation.** A real onsite is three or four coding rounds plus a behavioral round. Mock #3 is the first time the coding round and the Week 13 behavioral preparation can meet under one clock (the optional behavioral add-on in Lecture 3 §8).
2. **The trajectory is what a senior reads.** Mock #1 → #2 → #3 is a record of whether you can self-correct. An engineer who names a behavior change after each mock and *actually makes it* is demonstrating the single most predictive trait of someone who will grow on the job.
3. **The bit material is the vehicle, not the destination.** The bit tricks are an afternoon; the recorded mock under near-real pressure is the week. If you ship only one thing this week, ship a clean Mock #3 with a watched recording and a named behavior change.

If Challenge 2 must slip, slip it — but do not slip Mock #3. The bit problem is recoverable next week; the mock rep is not.
