# C2 · CrunchTime — The Code — Full Syllabus

**15 weeks intensive (~540 hrs) OR 52 weeks mastery (~520 hrs) · Powered by the UMPIRE Method**

The same material runs in two formats. Pick your pace; the content does not change. The intensive packs the program into 15 full-time weeks for people with a hiring cycle ahead of them. The mastery pathway spreads the same content over a year for working engineers and learners who need depth over speed.

---

## Program at a glance

| Phase | Intensive weeks | Mastery quarter | Outcome |
|-------|-----------------|-----------------|---------|
| **Phase 1 — Foundations** | 01 – 04 | Q1 (W1–13) | UMPIRE Method internalized + 4 fundamental patterns |
| **Phase 2 — Core Patterns** | 05 – 09 | Q2 (W14–26) | 10 of the 14 core patterns + first mock interview |
| **Phase 3 — Advanced Patterns** | 10 – 12 | Q3 (W27–39) | DP, graphs, design, advanced edge cases |
| **Phase 4 — Capstone & Onsite Prep** | 13 – 15 | Q4 (W40–52) | 4 recorded mocks, behavioral mastery, real interviews |

---

## Phase 1 — Foundations (Weeks 1–4 intensive · Q1 mastery)

### [Week 1 — The UMPIRE Method & Thinking Aloud](week-01-the-umpire-method-and-thinking-aloud/)

The six steps. Why "out loud" matters. The 10-minute UMPIRE drill. Reading a problem prompt the way an interviewer wrote it. Surfacing assumptions. Negotiating constraints. The very first pattern: **arrays & two pointers**.

- **Mini-project:** Solve and write up 5 array problems using UMPIRE, fully narrated. Push to GitHub.

### [Week 2 — Complexity & Hash Maps](week-02-complexity-and-hash-maps/)

How to estimate complexity without looking it up. Common bounds: O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ). Space matters too. The "what does adding a nested loop do" calibration. **Pattern: hash maps for O(1) lookup.**

- **Mini-project:** Re-do your Week-1 problems with explicit complexity sections in the UMPIRE write-up.

### Week 3 — Recognizing the Sliding Window

When a "compute something over every contiguous subarray" prompt is *actually* a sliding-window problem. Fixed vs. variable window. The pattern's invariants. **Pattern: sliding window.**

- **Mini-project:** Solve 6 sliding-window problems. Document for each: how you matched the pattern in 30 seconds.

### Week 4 — Fast-and-Slow Pointers + First Mock

The "linked list cycle" family. Floyd's tortoise and hare. Midpoint finding. Then: your **first recorded mock interview** against a peer (or solo if needed, on Excalidraw). Self-evaluation. **Pattern: fast-and-slow pointers.**

- **Mini-project:** Mock #1 recorded and posted to your portfolio repo with self-feedback notes.

---

## Phase 2 — Core Patterns (Weeks 5–9 intensive · Q2 mastery)

### Week 5 — Binary Search Beyond Sorted Arrays

The classic search; the "binary search on answer" idiom (parametric search); rotated arrays. **Pattern: binary search.**

- **Mini-project:** Solve 5 binary-search problems including 2 "search on answer" variants.

### Week 6 — Graphs Part 1: BFS

Building adjacency lists from edges. BFS as level-order. Shortest path on unweighted graphs. The visited set as an invariant. **Pattern: BFS.**

- **Mini-project:** A grid BFS problem (e.g., shortest path with obstacles) and a node BFS problem (word ladder family). Both UMPIRE-narrated.

### Week 7 — Graphs Part 2: DFS

Recursive and iterative DFS. Detecting cycles. Topological sort. Connected components. Iterative DFS with an explicit stack — and why interviewers ask. **Pattern: DFS.**

- **Mini-project:** Solve a course-prerequisites problem (topological sort) with full UMPIRE.

### Week 8 — Backtracking

The "decision tree" model. Pruning. Constraint propagation. N-Queens, subsets, permutations, sudoku. **Pattern: backtracking.**

- **Mini-project:** Implement subsets and permutations from scratch, narrate the recursion tree on a whiteboard.

### Week 9 — Top-K & Heaps + Mock #2

Min-heap and max-heap properties. `heapq` in Python. Top-K element problems. Streaming median. **Then: Mock #2** at midpoint pace. **Pattern: top-K / heap.**

- **Mini-project:** Mock #2 recorded; "top K frequent elements" written up.

---

## Phase 3 — Advanced Patterns (Weeks 10–12 intensive · Q3 mastery)

### Week 10 — Intervals + Greedy

Merging intervals. Insert intervals. Meeting rooms. The "sort first" heuristic. Greedy proof sketches. **Patterns: intervals + greedy.**

- **Mini-project:** Solve 4 interval problems; for each, explain why a greedy choice is provably optimal (or where it isn't).

### Week 11 — Dynamic Programming 1D

The 1D DP mindset: state, transition, base case, order of evaluation. Climbing stairs, coin change, longest increasing subsequence. From recursion + memo → tabulation. **Pattern: DP 1D.**

- **Mini-project:** Take one problem; solve it three ways (recursive, top-down memoized, bottom-up). Compare complexity and code clarity.

### Week 12 — Dynamic Programming 2D + System Design Intro

Grid DP. Edit distance, knapsack, longest common subsequence. Then: the system-design rhythm — load estimation, basic distribution, database choice, cache placement. Junior-level only. **Patterns: DP 2D + design.**

- **Mini-project:** Design a URL shortener at 10K QPS in writing. ~3 pages.

---

## Phase 4 — Capstone & Onsite Prep (Weeks 13–15 intensive · Q4 mastery)

### Week 13 — Behavioral & Communication

The 8 categories of behavioral question. STAR-format answers. The "story bank" approach: 12 anecdotes, rehearsed and refined. Recovering from a wrong direction mid-interview. The follow-up email.

- **Mini-project:** Story bank with 12 STAR-format anecdotes. Cross-reference each to the question types it covers.

### Week 14 — Mock #3 + Patterns Bit Manipulation, Tries

The remaining patterns: bit manipulation (XOR tricks, bitmask DP) and tries (prefix matching). Mock #3 at near-real conditions: 45 minutes, video on, no peeking. **Patterns: bit manipulation, tries.**

- **Mini-project:** Mock #3 recorded; XOR trick and trie write-ups.

### Week 15 — Capstone + Mock #4

Final mock under full real-interview conditions. Portfolio polish. Recruiter-prep pack: resume, LinkedIn, target list, outreach template. **The deliverable:** a public portfolio anyone can scroll through and see UMPIRE for 60+ problems.

- **Capstone:** Portfolio repo published. Mock #4 recorded. Recruiter-prep pack complete. You go interview.

---

## What you ship (capstone deliverables)

A single public GitHub repository, **`crunchtime-interview-prep-<yourhandle>`**, containing:

```
crunchtime-interview-prep-<you>/
├── README.md                    ← your interview-prep portfolio cover
├── umpire-writeups/
│   ├── 01-two-sum.md            ← 60+ problem write-ups in UMPIRE format
│   ├── 02-best-time-to-buy.md
│   └── …
├── mocks/
│   ├── mock-01-week-04.md       ← link to recording + self-feedback
│   ├── mock-02-week-09.md
│   ├── mock-03-week-14.md
│   └── mock-04-week-15.md
├── system-design/
│   └── url-shortener.md
├── behavioral/
│   └── story-bank.md            ← your 12 STAR anecdotes
├── recruiter-prep/
│   ├── resume-v3.pdf
│   ├── target-companies.md
│   ├── outreach-template.md
│   └── follow-up-template.md
├── study-plan/
│   └── pre-onsite-4-weeks.md    ← your personalized last-mile plan
└── badges/
    ├── umpire-apprentice.json
    ├── pattern-practitioner.json
    └── crunchtime-graduate.json
```

This repo is what you point recruiters and hiring managers at. It is also a reusable artifact — when your friend starts interviewing in six months, you fork the structure to them.

---

## How the weekly load adds up

Same as every Code Crunch track, but the intensive and mastery columns differ:

| Component | Intensive (per wk) | Mastery (per wk) |
|-----------|------------------:|----------------:|
| Lectures / readings | 6h | 2h |
| Hands-on UMPIRE drills | 8h | 2h |
| Pattern challenges | 4h | 1.5h |
| Pattern recognition quiz | 1h | 0.5h |
| Mock interview & review | 3h | 1h |
| Homework problems | 6h | 1.5h |
| Mini-project / portfolio | 7h | 1h |
| Behavioral & design | 1h | 0.5h |
| **Total / week** | **36h** | **10h** |

---

## Skills progression chart

```text
W1   ─ UMPIRE introduced + arrays / two pointers
W2   │ complexity mastery + hash maps
W3   ─ sliding window
W4   ─ fast/slow pointers + MOCK #1
W5   │ binary search
W6   ─ BFS
W7   ─ DFS
W8   │ backtracking
W9   ─ top-K + MOCK #2
W10  ─ intervals + greedy
W11  │ DP 1D
W12  ─ DP 2D + system design intro
W13  ─ behavioral / STAR
W14  │ bit manipulation, tries + MOCK #3
W15  ─ CAPSTONE + MOCK #4 → real interviews
```

---

## Resources (free, open, non-paywalled)

The course is independent of any one practice platform. Recommended grounds, all free:

| Platform | Free tier | Good for |
|----------|-----------|----------|
| LeetCode | Free problems (~2000) | Most variety of medium-difficulty problems |
| HackerRank | Fully free | Strong tutorials on specific topics |
| Codeforces | Fully free | Contest culture, time pressure |
| AtCoder | Fully free | Beginner-to-expert problem sets |
| Exercism | Fully free | Mentored solutions in many languages |

For mock interviews:

- **Pramp** — peer-to-peer, free.
- **interviewing.io** — has a free tier for some demographics.
- **A friend who also uses C2** — best option; mutual feedback is the entire point.

For system design:

- **The Grokking System Design** book *PDF excerpts only* (free chapters published online).
- **High Scalability blog**: <http://highscalability.com>
- **AWS architecture center** (free, vendor-flavored): <https://aws.amazon.com/architecture/>

---

## Adapting the syllabus

- **University semester (15 weeks × 9 hrs/wk):** Use the intensive structure but drop one mini-project and one challenge per week. Keep mocks.
- **High-school CS club (1 hr/week class + homework):** Use the mastery pathway, but plan for 18 months instead of 12. Two learners should pair-mock-interview each session.
- **Part of a bootcamp:** C2 pairs naturally with C1's Weeks 6–15. Run them concurrently; bootcamp ends with a portfolio that includes C2's interview-prep repo.

---

## What you won't learn here (intentionally)

- **Compensation negotiation, offer mechanics, on-call expectations** — see [C13 · Hack the Interview](../../C13-HACK-THE-INTERVIEW/).
- **Building a portfolio of *projects* (not just problem write-ups)** — see [C3 · Crunch Labs Portfolio](../../C3-CRUNCH-LABS-PORTFOLIO/).
- **Production engineering skills you'd use after the interview** — see [C16](../../C16-CRUNCH-PRO-WEB-BACKEND/) and [C17](../../C17-CRUNCH-PRO-PYTHON-ADVANCED/).
- **Competitive programming at the Codeforces-master level** — out of scope. We aim at *hiring* interviews, not contests.

---

## License

GPL-3.0. Fork, teach, remix. Improvements via PR welcome.
