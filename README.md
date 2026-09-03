# C2 · CrunchTime — The Code · Course Syllabus

> A free, open-source **technical interview preparation** course built in the open. From "what is a list?" to "I just whiteboarded a graph problem and got the offer." Powered by the **FRAME Method** — the explicit problem-solving framework that turns coding interviews into a conversation you can control.

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Built in the open](https://img.shields.io/badge/built-in%20the%20open-2DD4BF.svg)](https://github.com/CODECRUNCHWORLDWIDE)
[![Two pathways](https://img.shields.io/badge/pathways-15--week_intensive_|_1--year_mastery-2DD4BF.svg)](README.md)

---

## What this is

**CrunchTime — The Code** is a complete, free technical-interview preparation curriculum. It teaches you to:

- **Recognize patterns**, not memorize problems.
- **Talk through your solution** under pressure using the FRAME Method.
- **Reason about complexity** without hand-waving.
- **Write clean code** a senior engineer would accept in a code review.
- **Handle behavioral interviews**, system-design conversations, and live whiteboard rounds.
- **Build engineering judgment**, not just a count of problems solved.

It is **not** "grind 500 problems and hope." It is a structured program with two formats — a 15-week intensive and a 1-year mastery pathway — that turns interview prep into a measurable skill.

---

## Standards & equivalency

> C2 stands in for a university's data-structures and algorithms sequence, and for its technical-interview course.

**University equivalent.** Four of them, not one. **Data Structures** — `COP 3530`, `CS 1332`, `CS 61B`, `CS 2110`. **Design and Analysis of Algorithms** — `COP 4534`, `CS 4820`, `CS 3210`, `6.006`. **Scalable Systems Design** — `CS 4750`, `CIS 4930`, `6.5840`, `15-440`, `CSE 452`. **Technical Interview Preparation** — `CIS 4930`, `CS 9`, `CMSC 389O`, `COMPSCI 243`.

Coverage: **full** against Technical Interview Preparation, **partial** against the other three. Partial has a precise meaning here, and it is not "most of it". It means the topic list is taught and assessed while a named part of the university treatment is not. C2 teaches the structures and the algorithms as things you must recognise, implement, cost and defend out loud under a clock — it does not ask you to prove them, and the three places where a university section proves what C2 only states are the rows marked `lighter` below, declared again at the end of this section. Against Scalable Systems Design, partial is a matter of scope rather than depth: C2 covers the junior design round an interview loop actually contains — estimate the load, choose a data model, name the bottleneck, defend the trade-off — and not a term of distributed systems.

C2 carries no credit, no transcript entry, no accreditation and no proctored exam. The equivalence is one of **content and skill**: the outcomes below are taught here at the same depth or deeper except where a row says otherwise, and every one of them is assessed. What a registrar records is not something an open repository can give you.

| University outcome | Where this course teaches it | Depth |
| --- | --- | --- |
| **Data Structures** — arrays, strings and the dynamic array, with the cost of every operation on them | [Week 00](curriculum/week-00-python-data-structures-warmup/) | same |
| **Data Structures** — hash tables: what hashing buys, what a collision costs, and when the map is the answer | [Week 02](curriculum/week-02-complexity-and-hash-maps/) | deeper |
| **Data Structures** — linked lists, and the pointer techniques that traverse one in constant extra space | [Week 04](curriculum/week-04-fast-slow-pointers-and-mock-1/) | same |
| **Data Structures** — queues and stacks, including replacing recursion with an explicit stack | [Week 07](curriculum/week-07-dfs-and-topological-sort/) | same |
| **Data Structures** — trees and their traversals, recursive and iterative | [Week 07](curriculum/week-07-dfs-and-topological-sort/) | same |
| **Data Structures** — heaps and priority queues, and the bounded top-K structure built on one | [Week 08](curriculum/week-08-heaps-and-priority-queues/) | deeper |
| **Data Structures** — tries and the prefix walk, a node class weighed against dict-of-dicts | [Week 09](curriculum/week-09-tries-and-advanced-strings/) | deeper |
| **Data Structures** — graphs, their representations, and traversal over both grids and adjacency lists | [Week 06](curriculum/week-06-bfs/) | same |
| **Data Structures** — disjoint-set union with path compression and union by rank | [Week 10](curriculum/week-10-weighted-graphs-and-union-find/) | deeper |
| **Data Structures** — state the time and space cost of every structure you choose, and justify the choice | [Week 02](curriculum/week-02-complexity-and-hash-maps/) | same |
| **Data Structures** — amortised analysis: the doubling argument behind the dynamic array, the inverse-Ackermann bound on union-find | [Week 10](curriculum/week-10-weighted-graphs-and-union-find/) | lighter |
| **Algorithms** — asymptotic analysis, and comparing algorithms by growth rather than by clock | [Week 02](curriculum/week-02-complexity-and-hash-maps/) | same |
| **Algorithms** — divide and conquer, and binary search including search over a monotone answer space | [Week 05](curriculum/week-05-binary-search/) | deeper |
| **Algorithms** — breadth-first and depth-first search, cycle detection, connected components and topological sort | [Week 07](curriculum/week-07-dfs-and-topological-sort/) | same |
| **Algorithms** — greedy methods, and the shortest-path and minimum-spanning-tree algorithms built on them | [Week 10](curriculum/week-10-weighted-graphs-and-union-find/) | same |
| **Algorithms** — dynamic programming: state, transition, base case, evaluation order, and space reduction | [Week 11](curriculum/week-11-dynamic-programming-i/) | same |
| **Algorithms** — exhaustive search with pruning: backtracking over subsets, permutations, partitions and grids | [Week 12](curriculum/week-12-backtracking-and-combinatorics/) | deeper |
| **Algorithms** — string algorithms: the KMP failure function, the Z-algorithm, Aho-Corasick | [Week 09](curriculum/week-09-tries-and-advanced-strings/) | deeper |
| **Algorithms** — bit-level algorithms: XOR identities, masks, and subset enumeration | [Week 14](curriculum/week-14-mock-3-bit-manipulation-and-tries/) | same |
| **Algorithms** — proof technique: induction, exchange arguments, and loop invariants proven rather than stated | [Week 11](curriculum/week-11-dynamic-programming-i/) | lighter |
| **Algorithms** — the complexity-theory half: NP-completeness, reductions, and what intractability means | [Week 12](curriculum/week-12-backtracking-and-combinatorics/) | lighter |
| **Scalable Systems** — back-of-envelope capacity estimation: requests per second, storage, bandwidth | [Week 15](curriculum/week-15-capstone-and-mock-4/) | same |
| **Scalable Systems** — choose a data model and a storage shape for a service, and defend the choice | [Week 15](curriculum/week-15-capstone-and-mock-4/) | same |
| **Scalable Systems** — find the bottleneck on a read path, and pick the index or cache that removes it | [Week 05](curriculum/week-05-binary-search/) | same |
| **Scalable Systems** — counting and aggregation workloads at scale, and what the naive version costs | [Week 02](curriculum/week-02-complexity-and-hash-maps/) | same |
| **Scalable Systems** — hold the design conversation itself: scope down out loud, state the trade-off, say what you deferred | [Week 15](curriculum/week-15-capstone-and-mock-4/) | deeper |
| **Technical Interview** — a repeatable method for an unseen problem, executed out loud | [Week 01](curriculum/week-01-the-frame-method-and-thinking-aloud/) | deeper |
| **Technical Interview** — recognise which pattern a prompt wants inside the first minute of reading it | [Week 03](curriculum/week-03-sliding-window/) | deeper |
| **Technical Interview** — write correct code under a clock, on a shared screen, without an editor helping | [Week 14](curriculum/week-14-mock-3-bit-manipulation-and-tries/) | deeper |
| **Technical Interview** — the behavioural round: the eight categories, STAR answers, and a rehearsed story bank | [Week 13](curriculum/week-13-behavioral-and-communication/) | deeper |
| **Technical Interview** — mock interviews with structured feedback and a measurable trajectory across them | [Week 04](curriculum/week-04-fast-slow-pointers-and-mock-1/) | deeper |
| **Technical Interview** — the mechanics around the loop: resume, target list, outreach, follow-up | [Week 15](curriculum/week-15-capstone-and-mock-4/) | deeper |

Every row above points at a week that **assigns work** on that outcome — a drill, a challenge, homework, a quiz item, a mini-project or the capstone — not merely a week that mentions it.

**The industry bar.** What an employer expects of somebody paid to do this work, and where this course makes the learner do it. Several of C2's deliverables are not programs — a behavioural story bank, a recorded mock, a written design — so where the practice is not code, the row says what the equivalent practice is in the medium the deliverable actually uses.

| What the job expects | Where this course does it |
| --- | --- |
| Work lands as a commit in a repository you own, not a file on your desktop | [`resources/git-github-workflow.md`](resources/git-github-workflow.md), and the portfolio repository is created in Week 01 at [`curriculum/week-01-the-frame-method-and-thinking-aloud/homework/problem-01-portfolio-setup.md`](curriculum/week-01-the-frame-method-and-thinking-aloud/homework/problem-01-portfolio-setup.md) |
| You read code you did not write and form a judgement on it | [`curriculum/week-04-fast-slow-pointers-and-mock-1/lecture-notes/02-the-mock-interview-protocol.md`](curriculum/week-04-fast-slow-pointers-and-mock-1/lecture-notes/02-the-mock-interview-protocol.md) — you take the interviewer's chair for a peer on a problem they have not seen, read what they write as they write it, and grade it against the rubric |
| Tests exist, and the command to run them is written down | [`curriculum/week-01-the-frame-method-and-thinking-aloud/exercises/timed_runner.py`](curriculum/week-01-the-frame-method-and-thinking-aloud/exercises/timed_runner.py) — a pytest harness you point at your own module and run with `pytest timed_runner.py -v`; every published answer file also carries its own case list and asserts it |
| You read a real traceback instead of guessing | the `Common bugs to catch` section carried by every problem page, quoting output captured from a real run |
| Dependencies are isolated per project | [`resources/setup-guides/`](resources/setup-guides/) |
| Tooling used the way a team uses it — a formatter, a linter, a type checker and a test runner, configured once and run over everything | [`resources/coding-standards.md`](resources/coding-standards.md). C2's capstone is write-ups and recordings rather than a running service, so the tool run is local and covers every file, not a build gate in front of a deployment |
| Code that reads the way the rest of the codebase reads | [`resources/coding-standards.md`](resources/coding-standards.md), applied to every published answer file in the tree |
| Work that is not code is still held to a standard and still reviewed | the behavioural artifacts at [`curriculum/week-13-behavioral-and-communication/exercises/star_template.md`](curriculum/week-13-behavioral-and-communication/exercises/star_template.md) and the written design at [`curriculum/week-15-capstone-and-mock-4/exercises/exercise-02-system-design-writeup.md`](curriculum/week-15-capstone-and-mock-4/exercises/exercise-02-system-design-writeup.md), each graded against a published rubric rather than left to taste |
| The output is portfolio-grade: a stranger can read it and know what you can do | [`projects/capstone/README.md`](projects/capstone/README.md) |

**Beyond both bars.** Clearing the two floors is entry, not success. Open any of these and check it in under a minute.

| What we add | Which bar it beats | Where it lives |
| --- | --- | --- |
| Every assigned problem publishes its worked answer on its own page, visible, with a runnable file beside it — no answer key held back until a deadline | both | [`curriculum/week-02-complexity-and-hash-maps/exercises/`](curriculum/week-02-complexity-and-hash-maps/exercises/) |
| `Under the hood` blocks carry the internals a lecture stops short of, folded so a learner may skip every one and still finish the week | university | [`curriculum/week-05-binary-search/exercises/exercise-02-scan-window.md`](curriculum/week-05-binary-search/exercises/exercise-02-scan-window.md) |
| The learner finishes holding a public repository somebody can clone and read, not a grade only a registrar can see | both | [`projects/capstone/`](projects/capstone/) |
| Four recorded mock interviews graded against a published rubric, with the Mock #1 to Mock #4 trajectory as a deliverable in its own right — a section grades the answer, this grades the improvement | industry | [`curriculum/week-14-mock-3-bit-manipulation-and-tries/challenges/challenge-01-mock-3-timed-round.md`](curriculum/week-14-mock-3-bit-manipulation-and-tries/challenges/challenge-01-mock-3-timed-round.md) |
| A behavioural story bank — twelve rehearsed stories against the eight question categories, with a coverage matrix — which no data-structures or algorithms section teaches and every hiring loop tests | industry | [`curriculum/week-13-behavioral-and-communication/exercises/`](curriculum/week-13-behavioral-and-communication/exercises/) |
| A pattern-recognition quiz every week, timed at thirty seconds a question, with its answer key published in the same file | university | [`curriculum/week-03-sliding-window/quiz.md`](curriculum/week-03-sliding-window/quiz.md) |
| The same material at two paces — a fifteen-week run or a year at a working professional's hours — because we are not bound to a term | university | [`curriculum/study-plans/mastery-1-year.md`](curriculum/study-plans/mastery-1-year.md) |

**Gaps we declare.** Three, and they are the three the ledger records: C2 does not teach proof technique — induction, exchange arguments, and loop invariants proven rather than stated; it states amortised bounds where they matter, such as the dynamic array's doubling and union-find's inverse-Ackermann bound, without deriving them; and it does not teach the complexity-theory half of an algorithms course — NP-completeness, reductions and intractability. Separately, the Scalable Systems Design claim is scoped to the junior design round described above, not to distributed systems.

---

## Pick your pathway

| | **Intensive** | **Mastery** |
|---|---|---|
| **Duration** | 15 weeks | 52 weeks (1 year) |
| **Time / week** | ~36 hours (full-time) | ~10 hours (working professional) |
| **Total time** | ~540 hours | ~520 hours |
| **Target audience** | Bootcamp grads, career switchers, learners between jobs, people with an interview cycle starting in 4 months | Working engineers preparing for next year's hiring season, learners balancing classes, anyone who wants depth over speed |
| **Outcome** | Interview-ready at FAANG / strong startups | Interview-ready *plus* genuine algorithmic intuition you keep for years |
| **Start with** | [`curriculum/study-plans/intensive-15-week.md`](curriculum/study-plans/intensive-15-week.md) | [`curriculum/study-plans/mastery-1-year.md`](curriculum/study-plans/mastery-1-year.md) |

The course material is **the same** in both — only the *pace* differs. The 1-year pathway lets each concept marinate longer, includes extra deliberate-practice sessions, and adds a community study-group rhythm.

---

## The FRAME Method

Every problem in every week of this course is solved with the same five steps, out loud, in the same order. Most candidates fail interviews not because they couldn't solve the problem — they fail because they couldn't *explain themselves*. FRAME fixes that.

```
F   FRAME                 — restate the problem, define inputs and outputs, ask clarifying questions
R   RESEARCH CONSTRAINTS  — identify limits, edge cases, and what makes the problem difficult
A   ASSESS OPTIONS        — describe a simple approach, then compare better ones and their tradeoffs
M   MAKE THE SOLUTION     — write clean, incremental code while explaining key decisions
E   EXAMINE               — walk through tests, edge cases, complexity, and possible improvements
```

Every lecture, every exercise, every mock interview reinforces this framework. By Week 4 it's automatic. By Week 10 you can do it under pressure.

> **Why we built this around FRAME instead of "just solving problems":** because the difference between a junior engineer who passes interviews and one who doesn't is rarely *how many problems they've seen*. It's whether they can think out loud, recover from a wrong direction, and prove they care about correctness, complexity, and clarity. FRAME makes those visible.

---

## What you will be able to do at the end

After completing C2 (either pathway), you will be able to:

- **Solve a fresh medium-difficulty algorithm problem** end-to-end in 30–35 minutes while narrating the FRAME Method out loud.
- **Recognize the 14 core problem patterns** within the first minute of reading a prompt: arrays / two pointers, sliding window, fast-and-slow pointers, binary search, BFS, DFS, backtracking, top-K, intervals, dynamic programming (1D and 2D), greedy, bit manipulation, design.
- **State big-O complexity** for time *and* space, both upper and lower bounds when relevant.
- **Hold a 45-minute system-design conversation** at the junior-to-mid level — load estimation, basic distribution, database choices, caching.
- **Handle 8 categories of behavioral question** ("tell me about a time…") with a structured STAR-format answer you've rehearsed and refined.
- **Whiteboard cleanly** without an IDE: pseudocode that runs, naming that reads, complexity that's correct.
- **Pass a mock onsite** at the 70th percentile or above against our open rubric.
- **Choose the right data structure** for any of 50+ canonical problem variants.
- **Reason about test cases** — happy path, edge cases, stress, malicious input — before writing a line of code.

The capstone deliverable is a **public interview-prep portfolio repo** demonstrating FRAME for 60+ problems, 4 recorded mock interviews, a system-design write-up, and a personalized study plan you carry into your real interviews.

---

## Prerequisites

C2 is built on top of, or to run in parallel with, **C1 · Code Crunch Convos**.

- **Comfortable Python 3.11+:** functions, classes, lists, dicts, sets, tuples, list comprehensions, basic exception handling.
- **Comfortable Git/GitHub:** clone, commit, branch, push, open a PR.
- **A computer with Python installed** and an editor (VS Code recommended; any will do).
- **You actually want to do interviews.** This is a 500-hour commitment. If you're not going to interview, take C1 + C3 (portfolio) instead — they're a better use of your time.

If you can't do those, finish **C1 Weeks 1–7** first. C2 will not slow down to re-teach Python syntax.

---

## What this course is NOT

- **Every problem here is ours.** The drills, the challenges, the homework and their test cases were written for this course, so none of them can be looked up and recalled instead of solved. If you want a judge to run against once you have finished a week, use whatever you like — we do not send you anywhere, and nothing in the course depends on an outside site.
- **Not vendor-locked.** No required paid subscriptions. No "must use Replit." Local Python, your editor, free practice sites.
- **Not "the answer key."** We deliberately don't ship pre-written solutions for the problems we recommend. We teach the *method*; you produce the *answers*. That's how interview skill actually transfers.
- **Not language wars.** We use Python because it reads close to pseudocode and that's an interview superpower. The patterns transfer to Java, JavaScript, C++, Go directly — Week 12 includes a "switch your interview language" appendix.
- **Not a substitute for therapy.** Interviewing is psychologically hard. We give you frameworks for nerves, rejection, and impostor syndrome — but we are not a mental health resource. Talk to a professional if you need one.

---

## Weekly cadence

Same standard Code Crunch shape across both pathways. Times scale to your pace:

| Component | Intensive (per wk) | Mastery (per wk) |
|-----------|------------------:|----------------:|
| Lectures / readings | 6h | 2h |
| Hands-on exercises (FRAME drills) | 8h | 2h |
| Pattern challenges | 4h | 1.5h |
| Pattern recognition quiz | 1h | 0.5h |
| Mock interview & review | 3h | 1h |
| Homework problems | 6h | 1.5h |
| Mini-project / portfolio work | 7h | 1h |
| Behavioral & system-design study | 1h | 0.5h |
| **Total / week** | **36h** | **10h** |

The mastery pathway *re-runs* the intensive material across a year — each week of intensive content becomes roughly 3.5 calendar weeks of mastery work, with extra rest, repetition, and reinforcement.

---

## What you ship

By the end of C2 you will publish a public GitHub repo (`crunchtime-interview-prep-<yourhandle>`) containing:

1. **60+ problem write-ups** in the FRAME format. Not just "here is the code" — full *Frame / Research constraints / Assess options / Make the solution / Examine* sections for every problem, ready to skim before a real interview.
2. **4 recorded mock interviews** (audio at minimum; video preferred): one each at Weeks 4, 8, 12, 15 (intensive) — or quarters (mastery). Each annotated with what went well and what to fix.
3. **A system-design write-up** for one mid-scale problem (e.g., a URL shortener at 10K QPS) at the junior+ level.
4. **A personalized study plan** for the 4 weeks leading up to your real interviews — what to drill, what to skip, what to rehearse.
5. **A "behavioral story bank"** of 12+ refined STAR-format anecdotes covering the canonical behavioral categories.
6. **A recruiter-prep pack:** resume reviewed, LinkedIn polished, GitHub README upgraded, target company list, outreach template, follow-up template.

That portfolio is *the* artifact you point recruiters and hiring managers at.

---

## Tools we use (all free, all open-source)

| Tool | Role |
|------|------|
| **Python 3.11+** | The implementation language for every solution |
| **VS Code** + Python extension | Editor (any works) |
| **Excalidraw / tldraw** | Free whiteboarding, for digital "draw this graph" practice |
| **OBS Studio** | Free recording for mock interviews |
| **Discord or Zoom** | For peer mock interviews; both have free tiers |
| **Pytest** | Unit testing your solutions |
| **GitHub** | Hosting your portfolio repo |
| **An online judge** | Entirely optional. Every problem you are assigned here is our own and runs locally |
| **HackerRank, Codeforces, AtCoder** | Other free practice grounds we point at |
| **`/usr/bin/time` and `cProfile`** | When you need to actually measure complexity, not just guess |

---

## Certifications & milestones

C2 is **not accredited**. We don't pretend to be. But we issue **open-source verifiable milestone badges** that you can pin to your GitHub profile and resume:

| Badge | Earned by |
|-------|-----------|
| **FRAME Apprentice** | Completing Weeks 1–4 (or Mastery Q1) — basics + first 5 patterns |
| **Pattern Practitioner** | Completing Weeks 5–9 (or Mastery Q2) — 10 of 14 patterns + first mock |
| **System Thinker** | Completing the Week-12 system-design module |
| **Mock Veteran** | Submitting 4 recorded mocks against the open rubric |
| **CrunchTime Graduate** | Capstone portfolio merged into the public showcase repo |

Each badge is a signed JSON manifest in your portfolio repo plus a Markdown badge for your README. They are *self-asserted but verifiable* — anyone can check your portfolio against the rubric. We do not sell certificates. We do not charge fees. The portfolio is the credential.

---

## License and originality

**GPL-3.0.** See [LICENSE](LICENSE). Fork freely, teach, remix, print, translate, sell a course built on it. PR improvements back so the next learner benefits.

That promise only holds because **every problem in this course is written for this course** — statements, constraints, examples, and test cases alike. Nothing is restated or reskinned from another platform. The rule and its reasoning are in [CONTENT-POLICY.md](CONTENT-POLICY.md), and it is binding on every contribution.

Where a learner may want an online judge to run against, we link out by problem name and number only. That is all that crosses over.

> **All problems, examples, constraints and test cases in this course are original work**, written for this course and published under GPL-3.0.

---

## Next track after C2

- **[C13 · Hack the Interview](../C13-HACK-THE-INTERVIEW/)** — companion track focused on the *hiring process itself*: negotiation, comp research, offer evaluation, multi-offer decisions, on-call expectations.
- **[C3 · Crunch Labs Portfolio](../C3-CRUNCH-LABS-PORTFOLIO/)** — what to build alongside C2 to have a portfolio recruiters actually scroll through.
- **[C16 · Crunch Pro Web Backend](../C16-CRUNCH-PRO-WEB-BACKEND/)** — once hired, the next-tier engineering skill.

---

*C2 is part of the Code Crunch open-source curriculum.* [Master catalog ↗](https://codecrunchglobal.vercel.app/courses.html) · [Branding ↗](assets/brand/BRAND.md)

---

## Program at a glance

**Format:** 15 weeks · ~36 hrs/week intensive (or 52 weeks at ~10 hrs/week mastery) · C1 graduate → interview-ready engineer · powered by the FRAME Method

A technical-interview preparation course. Same material in both pathways; only the pace differs. Every problem is solved out loud with the five FRAME steps: Frame the problem, Research constraints, Assess options, Make the solution, and Examine the result.

**Prerequisites.** Comfortable Python 3.11+ (functions, classes, lists, dicts, sets, tuples, comprehensions, basic exceptions) and comfortable Git/GitHub (clone, commit, branch, push, PR). You must actually intend to interview — this is a ~500-hour commitment. If you can't do those, finish **C1 Weeks 1–7** first; C2 will not slow down to re-teach syntax.

**Start at [Week 0](curriculum/week-00-python-data-structures-warmup/README.md) unless you can skip it.** Week 0 is an 8-hour warm-up on the *cost model* of Python's built-ins — strings, lists, tuples, dicts, sets — with time and space complexity for every operation, plus [the cheat sheet](curriculum/week-00-python-data-structures-warmup/CHEATSHEET.md) you will keep open all course. Take its [20-question self-check](curriculum/week-00-python-data-structures-warmup/quiz.md) cold: score 18/20 and go straight to Week 1. Week 0 does not count toward the 15 and is not part of the hour budget below.

**Every problem in this course is original.** Statements, constraints, examples, and test cases are written for C2 — nothing is restated or reskinned from another platform. See [CONTENT-POLICY.md](CONTENT-POLICY.md).

**Assessment is honor-based.** C2 is not accredited and issues no proctored exams. Milestone badges (FRAME Apprentice, Pattern Practitioner, System Thinker, Mock Veteran, CrunchTime Graduate) are self-asserted but verifiable — signed JSON manifests anyone can check against the open rubric. The portfolio is the credential; we do not sell certificates.

---

### Weekly breakdown

Each week ships a mini-project into your public `crunchtime-interview-prep-<handle>` portfolio repo.

| Week | Topic | Mini-project |
|------|-------|--------------|
| 01 | The FRAME Method & Thinking Aloud (arrays / two pointers) | Portfolio repo set up; 5 array problems, fully FRAME-narrated |
| 02 | Complexity & Hash Maps | Re-do the Week-1 drills with explicit complexity sections |
| 03 | Sliding Window | 6 sliding-window write-ups, each with a 30-second pattern-match memo |
| 04 | Fast-and-Slow Pointers + Mock #1 | Mock Interview #1 recorded, watched, self-critiqued |
| 05 | Binary Search | 5 binary-search write-ups including 2 "search on answer" variants |
| 06 | Graphs I — BFS | One grid-BFS and one node-BFS write-up |
| 07 | Graphs II — DFS & Topological Sort | One DFS (cycle/connectivity) and one topological-sort write-up |
| 08 | Heaps & Priority Queues | One top-K and one two-heap write-up |
| 09 | Tries & Advanced Strings | One trie (the gate tag tree) and one KMP `strStr` write-up |
| 10 | Weighted Graphs & Union-Find | One Dijkstra (the hut relay timing) and one DSU (the radiator loop check) write-up |
| 11 | Dynamic Programming I | One 1D DP (house robber) and one 2D DP (unique paths) write-up |
| 12 | Backtracking & Combinatorics | Palindrome partitioning and a sudoku solver, choose-explore-unchoose narrated |
| 13 | Behavioral & Communication | Story bank of 12+ STAR anecdotes with a coverage matrix |
| 14 | Mock #3, Bit Manipulation & Tries | Mock #3 recording + one XOR-trick and one binary-trie write-up |
| 15 | Capstone + Mock #4 | Portfolio published, Mock #4 recorded, personalized go-forward study plan |

---

### Weekly load

| Component | Intensive (per wk) | Mastery (per wk) |
|-----------|------------------:|----------------:|
| Lectures / readings | 6h | 2h |
| Hands-on FRAME drills | 8h | 2h |
| Pattern challenges | 4h | 1.5h |
| Pattern recognition quiz | 1h | 0.5h |
| Mock interview & review | 3h | 1h |
| Homework problems | 6h | 1.5h |
| Mini-project / portfolio | 7h | 1h |
| Behavioral & design | 1h | 0.5h |
| **Total / week** | **36h** | **10h** |

---

**Outcome:** interview-ready — solve a fresh medium-difficulty problem end-to-end in 30–35 minutes while narrating FRAME out loud, recognize all 14 core patterns within the first minute, reason about time and space complexity without hand-waving, hold a junior-to-mid system-design conversation, handle behavioral rounds with a rehearsed STAR story bank, and pass a mock onsite at the 70th percentile or above — all proven by a public portfolio of 60+ FRAME write-ups, 4 recorded mocks, a system-design write-up, and a personalized study plan.

---

## Week by week

**15 weeks intensive (~540 hrs) OR 52 weeks mastery (~520 hrs) · Powered by the FRAME Method**

The same material runs in two formats. Pick your pace; the content does not change. The intensive packs the program into 15 full-time weeks for people with a hiring cycle ahead of them. The mastery pathway spreads the same content over a year for working engineers and learners who need depth over speed.

---

### Program at a glance

| Phase | Intensive weeks | Mastery quarter | Outcome |
|-------|-----------------|-----------------|---------|
| **Phase 1 — Foundations** | 01 – 04 | Q1 (W1–13) | FRAME Method internalized + 4 fundamental patterns |
| **Phase 2 — Core Patterns** | 05 – 09 | Q2 (W14–26) | 10 of the 14 core patterns + first mock interview |
| **Phase 3 — Advanced Patterns** | 10 – 12 | Q3 (W27–39) | DP, graphs, design, advanced edge cases |
| **Phase 4 — Capstone & Onsite Prep** | 13 – 15 | Q4 (W40–52) | 4 recorded mocks, behavioral mastery, real interviews |

---

### Phase 1 — Foundations (Weeks 1–4 intensive · Q1 mastery)

#### [Week 1 — The FRAME Method & Thinking Aloud](curriculum/week-01-the-frame-method-and-thinking-aloud/)

The five steps. Why "out loud" matters. The 10-minute FRAME drill. Reading a problem prompt the way an interviewer wrote it. Surfacing assumptions. Negotiating constraints. The very first pattern: **arrays & two pointers**.

- **Mini-project:** Solve and write up 5 array problems using FRAME, fully narrated. Push to GitHub.

#### [Week 2 — Complexity & Hash Maps](curriculum/week-02-complexity-and-hash-maps/)

How to estimate complexity without looking it up. Common bounds: O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ). Space matters too. The "what does adding a nested loop do" calibration. **Pattern: hash maps for O(1) lookup.**

- **Mini-project:** Re-do your Week-1 problems with explicit complexity sections in the FRAME write-up.

#### Week 3 — Recognizing the Sliding Window

When a "compute something over every contiguous subarray" prompt is *actually* a sliding-window problem. Fixed vs. variable window. The pattern's invariants. **Pattern: sliding window.**

- **Mini-project:** Solve 6 sliding-window problems. Document for each: how you matched the pattern in 30 seconds.

#### Week 4 — Fast-and-Slow Pointers + First Mock

The "linked list cycle" family. Floyd's tortoise and hare. Midpoint finding. Then: your **first recorded mock interview** against a peer (or solo if needed, on Excalidraw). Self-evaluation. **Pattern: fast-and-slow pointers.**

- **Mini-project:** Mock #1 recorded and posted to your portfolio repo with self-feedback notes.

---

### Phase 2 — Core Patterns (Weeks 5–9 intensive · Q2 mastery)

#### Week 5 — Binary Search Beyond Sorted Arrays

The classic search; the "binary search on answer" idiom (parametric search); rotated arrays. **Pattern: binary search.**

- **Mini-project:** Solve 5 binary-search problems including 2 "search on answer" variants.

#### Week 6 — Graphs Part 1: BFS

Building adjacency lists from edges. BFS as level-order. Shortest path on unweighted graphs. The visited set as an invariant. **Pattern: BFS.**

- **Mini-project:** A grid BFS problem (e.g., shortest path with obstacles) and a node BFS problem (word ladder family). Both FRAME-narrated.

#### Week 7 — Graphs Part 2: DFS

Recursive and iterative DFS. Detecting cycles. Topological sort. Connected components. Iterative DFS with an explicit stack — and why interviewers ask. **Pattern: DFS.**

- **Mini-project:** Solve a course-prerequisites problem (topological sort) with full FRAME.

#### [Week 8 — Heaps & Priority Queues](curriculum/week-08-heaps-and-priority-queues/)

Min-heap and max-heap properties. `heapq` and the min-heap-as-list invariant. The size-k top-K template and why it is `O(n log k)` rather than `O(n log n)`. Heap of tuples with a distance key; max-heap by negation. Two-heap streaming median, k-way merge, lazy deletion. **Pattern: heaps / top-K.**

- **Mini-project:** One top-K write-up and one two-heap write-up.

#### [Week 9 — Tries & Advanced Strings](curriculum/week-09-tries-and-advanced-strings/)

Trie construction, search, and prefix walk — dict-of-dicts versus a node class, and how to defend the choice. Autocomplete. Word break with memoization. The KMP failure function and the Z-algorithm. Aho-Corasick, read-only. **Patterns: trie + string matching.**

- **Mini-project:** One trie write-up and one KMP `strStr` write-up.

---

### Phase 3 — Advanced Patterns (Weeks 10–12 intensive · Q3 mastery)

#### [Week 10 — Weighted Graphs & Union-Find](curriculum/week-10-weighted-graphs-and-union-find/)

Dijkstra with a heap, including the stale-pop guard. Bellman-Ford and the negative-edge case. Floyd-Warshall. Minimum spanning trees via Kruskal and Prim. Union-find with path compression and union by rank, and the inverse-Ackermann amortized bound. The trigger phrases that mean DSU. **Patterns: shortest path + DSU.**

- **Mini-project:** One Dijkstra write-up and one union-find write-up.

#### [Week 11 — Dynamic Programming I](curriculum/week-11-dynamic-programming-i/)

The two DP triggers and the four-step pipeline: state, transition, base case, evaluation order. 1-D counting and segmentation DP. 2-D grid and string-pair DP. Rolling-row space reduction. Recognizing when DP does *not* apply. **Pattern: DP.**

- **Mini-project:** One 1-D DP write-up and one 2-D DP write-up.

#### [Week 12 — Backtracking & Combinatorics](curriculum/week-12-backtracking-and-combinatorics/)

The choose / recurse / unchoose template and the decision-tree model. Subsets, permutations, combinations. Pruning families and sort-plus-index-skip deduplication. String partitioning. Grid backtracking and constraint satisfaction. Why backtracking does not memoize. **Pattern: backtracking.**

- **Mini-project:** Palindrome partitioning and a constraint-satisfaction solver, choose-explore-unchoose narrated.

---

### Phase 4 — Capstone & Onsite Prep (Weeks 13–15 intensive · Q4 mastery)

#### Week 13 — Behavioral & Communication

The 8 categories of behavioral question. STAR-format answers. The "story bank" approach: 12 anecdotes, rehearsed and refined. Recovering from a wrong direction mid-interview. The follow-up email.

- **Mini-project:** Story bank with 12 STAR-format anecdotes. Cross-reference each to the question types it covers.

#### Week 14 — Mock #3 + Patterns Bit Manipulation, Tries

The remaining patterns: bit manipulation (XOR tricks, bitmask DP) and tries (prefix matching). Mock #3 at near-real conditions: 45 minutes, video on, no peeking. **Patterns: bit manipulation, tries.**

- **Mini-project:** Mock #3 recorded; XOR trick and trie write-ups.

#### Week 15 — Capstone + Mock #4

Final mock under full real-interview conditions. Portfolio polish. Recruiter-prep pack: resume, LinkedIn, target list, outreach template. **The deliverable:** a public portfolio anyone can scroll through and see FRAME for 60+ problems.

- **Capstone:** Portfolio repo published. Mock #4 recorded. Recruiter-prep pack complete. You go interview.

---

### What you ship (capstone deliverables)

A single public GitHub repository, **`crunchtime-interview-prep-<yourhandle>`**, containing:

```
crunchtime-interview-prep-<you>/
├── README.md                    ← your interview-prep portfolio cover
├── frame-writeups/
│   ├── 01-two-sum.md            ← 60+ problem write-ups in FRAME format
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
    ├── frame-apprentice.json
    ├── pattern-practitioner.json
    └── crunchtime-graduate.json
```

This repo is what you point recruiters and hiring managers at. It is also a reusable artifact — when your friend starts interviewing in six months, you fork the structure to them.

---

### Skills progression chart

```text
W1   ─ FRAME introduced + arrays / two pointers
W2   │ complexity mastery + hash maps
W3   ─ sliding window
W4   ─ fast/slow pointers + MOCK #1
W5   │ binary search
W6   ─ BFS
W7   ─ DFS
W8   │ heaps + priority queues
W9   ─ tries + advanced strings + MOCK #2
W10  ─ weighted graphs + union-find
W11  │ dynamic programming
W12  ─ backtracking + combinatorics
W13  ─ behavioral / STAR
W14  │ bit manipulation, tries + MOCK #3
W15  ─ CAPSTONE + MOCK #4 → real interviews
```

---

### Resources (free, open, non-paywalled)

The course is independent of any one practice platform. Recommended grounds, all free:

| Platform | Free tier | Good for |
|----------|-----------|----------|
| A large free problem archive | Thousands of problems | The most variety at medium difficulty, if you want volume after a week |
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

### Adapting the syllabus

- **University semester (15 weeks × 9 hrs/wk):** Use the intensive structure but drop one mini-project and one challenge per week. Keep mocks.
- **High-school CS club (1 hr/week class + homework):** Use the mastery pathway, but plan for 18 months instead of 12. Two learners should pair-mock-interview each session.
- **Part of a bootcamp:** C2 pairs naturally with C1's Weeks 6–15. Run them concurrently; bootcamp ends with a portfolio that includes C2's interview-prep repo.

---

### What you won't learn here (intentionally)

- **Compensation negotiation, offer mechanics, on-call expectations** — see [C13 · Hack the Interview](curriculum/../../C13-HACK-THE-INTERVIEW/).
- **Building a portfolio of *projects* (not just problem write-ups)** — see [C3 · Crunch Labs Portfolio](curriculum/../../C3-CRUNCH-LABS-PORTFOLIO/).
- **Production engineering skills you'd use after the interview** — see [C16](curriculum/../../C16-CRUNCH-PRO-WEB-BACKEND/) and [C17](curriculum/../../C17-CRUNCH-PRO-PYTHON-ADVANCED/).
- **Competitive programming at the Codeforces-master level** — out of scope. We aim at *hiring* interviews, not contests.

---

## Curriculum map

This folder contains every weekly module and study plan for C2. Start here:

1. **Pick your pathway** in [`SYLLABUS.md`](README.md).
2. **Read your study plan** — [`study-plans/intensive-15-week.md`](curriculum/study-plans/intensive-15-week.md) **or** [`study-plans/mastery-1-year.md`](curriculum/study-plans/mastery-1-year.md).
3. **Open Week 1** — [`week-01-the-frame-method-and-thinking-aloud/`](curriculum/week-01-the-frame-method-and-thinking-aloud/).

---

### Weeks (intensive numbering; mastery maps via SYLLABUS)

0. [Week 0 — Python Data Structures Warm-Up](curriculum/week-00-python-data-structures-warmup/) — *optional; skippable via its self-check*
1. [Week 1 — The FRAME Method & Thinking Aloud](curriculum/week-01-the-frame-method-and-thinking-aloud/) — *two pointers*
2. [Week 2 — Complexity & Hash Maps](curriculum/week-02-complexity-and-hash-maps/)
3. [Week 3 — Sliding Window](curriculum/week-03-sliding-window/)
4. [Week 4 — Fast/Slow Pointers + Mock #1](curriculum/week-04-fast-slow-pointers-and-mock-1/)
5. [Week 5 — Binary Search](curriculum/week-05-binary-search/)
6. [Week 6 — Graphs I: BFS](curriculum/week-06-bfs/)
7. [Week 7 — Graphs II: DFS & Topological Sort](curriculum/week-07-dfs-and-topological-sort/)
8. [Week 8 — Heaps & Priority Queues](curriculum/week-08-heaps-and-priority-queues/)
9. [Week 9 — Tries & Advanced Strings + Mock #2](curriculum/week-09-tries-and-advanced-strings/)
10. [Week 10 — Weighted Graphs & Union-Find](curriculum/week-10-weighted-graphs-and-union-find/)
11. [Week 11 — Dynamic Programming I](curriculum/week-11-dynamic-programming-i/)
12. [Week 12 — Backtracking & Combinatorics](curriculum/week-12-backtracking-and-combinatorics/)
13. [Week 13 — Behavioral & Communication](curriculum/week-13-behavioral-and-communication/)
14. [Week 14 — Mock #3, Bit Manipulation & Tries](curriculum/week-14-mock-3-bit-manipulation-and-tries/)
15. [Week 15 — Capstone + Mock #4](curriculum/week-15-capstone-and-mock-4/)

### Study plans

- [`study-plans/intensive-15-week.md`](curriculum/study-plans/intensive-15-week.md) — 36 hrs/wk, 4 months
- [`study-plans/mastery-1-year.md`](curriculum/study-plans/mastery-1-year.md) — 10 hrs/wk, 12 months

### Standard week layout

Same as every Code Crunch track:

```
week-NN-topic/
├── README.md
├── resources.md
├── lecture-notes/
├── exercises/         ← FRAME drills
├── challenges/        ← stretch problems
├── quiz.md            ← pattern-recognition quiz
├── homework.md
└── mini-project/      ← portfolio contribution
```

Each week's `mini-project` adds to your single, growing portfolio repository (`crunchtime-interview-prep-<you>`).

### Quality bar

C2 weeks aim for the same depth as [C1 Week 1](curriculum/../../C1-Code-Crunch-Convos/curriculum/week-01-python-foundations/) and the more recent [C16 Week 1](curriculum/../../C16-CRUNCH-PRO-WEB-BACKEND/curriculum/week-01-http-and-the-modern-python-web/) / [C17 Week 1](curriculum/../../C17-CRUNCH-PRO-PYTHON-ADVANCED/curriculum/week-01-cpython-internals-and-the-mental-model/). See those as references for what every C2 week should match.
