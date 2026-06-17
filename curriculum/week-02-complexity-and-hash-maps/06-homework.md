# Week 2 — Homework

Six problems. ~5 hours total. Each commits to your portfolio repo.

---

## Problem 1 — UMPIRE on a wild hash-map problem (90 min)

Pick *one* problem you've never seen before, tagged "Hash Table" on any free practice site (LeetCode, HackerRank, Exercism). Difficulty: Easy or Medium. **Do not read other people's solutions before solving.**

Suggested candidates if you need a starter list (all free on LeetCode):

- **First Unique Character in a String** (Easy, LC 387)
- **Intersection of Two Arrays II** (Easy, LC 350)
- **Top K Frequent Elements** (Medium, LC 347) — *uses heap; you may approximate with sort-by-count*
- **4Sum II** (Medium, LC 454) — hash map of pair sums; great training problem
- **Find All Anagrams in a String** (Medium, LC 438) — hash map + sliding window, but solvable with frequency tables alone
- **Longest Substring Without Repeating Characters** (Medium, LC 3) — hash map + window
- **Isomorphic Strings** (Easy, LC 205) — two-way mapping
- **Word Pattern** (Easy, LC 290) — two-way mapping (a sister problem to 205)

**Acceptance:**

- Recording of your full UMPIRE solve, ≥15 minutes.
- UMPIRE write-up in `umpire-writeups/c2-week-02/wild-01-<problem-slug>.md`.
- Tests passing (you write them).
- The write-up's Evaluate section follows the **five-piece structure** from Lecture 3.
- The write-up explicitly notes: how long did Match take? Did you correctly identify the hash-map sub-shape (complement / frequency / set membership)?

---

## Problem 2 — Time the gap (45 min)

This is a *measurement* exercise. The goal: see, in real numbers, what the difference between O(n²) and O(n) actually feels like.

**Acceptance:**

- A file `umpire-writeups/c2-week-02/measurement-01.md` containing:
  1. A small Python script that solves `two_sum_unsorted` two ways: a brute-force nested-loop O(n²) version and the hash-map O(n) version.
  2. A timing table comparing both on `n = 10², 10³, 10⁴, 10⁵`. Use `time.perf_counter()`. Generate random input of each size.
  3. Three observations: at which n did O(n²) become painfully slow? How does each version scale? At what input size would you absolutely *not* ship the O(n²) version?

This is the most pedagogically valuable single exercise of the week. *Watch* a complexity class change runtime. Theory becomes muscle memory when you measure.

---

## Problem 3 — Re-narrate Week 1's Drill 5 (30 min)

Take your **Container With Most Water** write-up from Week 1. Re-do the *Evaluate* section to follow the **five-piece structure** from this week's Lecture 3.

**Acceptance:**

- Edit `umpire-writeups/c2-week-01/drill-05-container-with-most-water.md`.
- The new Evaluate section includes: time, space, best/avg/worst (if relevant), tradeoffs, improvement.
- Add a note at the top of the section: *"Evaluate section rewritten in Week 2 to the five-piece structure."*

This problem is a preview of the **mini-project** (re-do all five Week 1 drills). Doing one of them in homework gets you to the rhythm before the mini-project deep-dives.

---

## Problem 4 — Behavioral story #2 (45 min)

The story bank continues. Spaced repetition matters.

**Acceptance:**

- A file `behavioral/story-02.md` in your portfolio repo.
- Topic: **"Tell me about a time you had to make a tradeoff between two valid approaches."**
- Format: STAR (Situation, Task, Action, Result).
- 200-400 words.
- Read it aloud at least twice. The story should naturally invoke complexity-style thinking: "I considered A, which is faster but uses more memory; I considered B, which is slower but cleaner; I chose B because…" — that's a *real* engineering tradeoff story, and it maps cleanly to the kind of thinking you've been drilling all week.

---

## Problem 5 — System-design ground zero #2 (45 min)

A second 300-word warm-up. Same shape as Week 1, different problem.

**Acceptance:**

- A file `system-design/notes-week-02.md` containing a 300-word answer to: **"How would you design a system that counts the top 10 most-frequent search queries in real time?"**
- Do not look up the canonical answer first. Write what you'd say in an interview today.
- After writing, search "top-K real-time frequency counting" and read one free article. Note three things you'd add — *especially* if it mentions hash maps, heaps, or count-min-sketch (the latter is genuinely interesting and out of scope for now).

---

## Problem 6 — Week 2 reflection (45 min)

A short reflection. 300-400 words at `study-plan/week-02-reflection.md`.

**Answer:**

1. Did your Evaluate sections actually get better this week, or did you cut corners on Drills 4-5? Be honest.
2. Which sub-shape of hash map (complement / frequency / set membership) felt most natural? Which felt forced?
3. The five-piece Evaluate structure — did you find it formulaic and annoying, or useful? Why?
4. What's one specific thing you'll do differently in Week 3 (sliding window)?

---

## Time budget

| Problem | Time |
|--------:|----:|
| 1 — Wild hash-map problem | 90 min |
| 2 — Timing measurement | 45 min |
| 3 — Re-narrate Drill 5 (Week 1) | 30 min |
| 4 — Behavioral story #2 | 45 min |
| 5 — System-design warm-up #2 | 45 min |
| 6 — Week 2 reflection | 45 min |
| **Total** | **5 h** |

---

By the end of Week 2 your portfolio repo's commit history should show ~25-30 commits total (10-15 from Week 1, +10-15 from Week 2). The cadence is the artifact; keep the streak.

Up next: [Week 3 — Sliding Window](../week-03/) (coming soon).
