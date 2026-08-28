# Week 6 — Homework

Six problems. ~5 hours total. Each commits to your portfolio repo. Two grid-BFS, two node-BFS, one bidirectional-BFS stretch, plus the behavioral and design warm-ups.

---

## Problem 1 — Number of Islands (LeetCode 200) (45 min)

The canonical "connected components on a grid" problem. Standard grid-BFS (or DFS — both acceptable; defend your choice).

**Problem.** Given an `m × n` 2-D binary grid where `1` is land and `0` is water, return the number of islands. An island is a maximal connected region of land cells (4-directionally connected).

**The insight.** Walk the grid; when finding an unvisited land cell, run BFS (or DFS) from it to mark its entire connected component. Increment the island counter once per component.

**Acceptance:**

- A file `frame-writeups/c2-week-06/hw-01-number-of-islands.md` with the FRAME write-up.
- Research constraints section states **grid-BFS** (or grid-DFS) and explicitly defends the choice (BFS — predictable memory; DFS — cleaner recursive code).
- Examine (../cost) section justifies **`O(R × C)` time, `O(R × C)` space** (the visited set, or the queue/stack).
- Recording ≥ 15 minutes.
- Tests passing on: `grid=[[1,1,1,1,0],[1,1,0,1,0],[1,1,0,0,0],[0,0,0,0,0]] → 1`, `grid=[[1,1,0,0,0],[1,1,0,0,0],[0,0,1,0,0],[0,0,0,1,1]] → 3`, `grid=[[0]] → 0`, `grid=[[1]] → 1`.

This problem and Exercise 3 share the grid-BFS skeleton. Your Research constraints section should call out the structural parallel — both walk the grid in a single outer pass, both use the same neighbor function; the only difference is what we are counting.

---

## Problem 2 — 0-1 Matrix (LeetCode 542) (45 min)

A multi-source grid-BFS problem — the structural cousin of Exercise 3.

**Problem.** Given an `m × n` binary matrix `mat`, return a matrix of the same size where `result[r][c]` is the distance from `(r, c)` to the nearest `0` (using 4-directional moves).

**The insight.** Seed the queue with **every** `0` cell at distance 0. Multi-source BFS expands outward; each `1` cell is reached at its minimum distance from any `0`. Same template as rotting oranges; the answer is the per-cell distance instead of a single max.

**Acceptance:**

- File `frame-writeups/c2-week-06/hw-02-zero-one-matrix.md`.
- Research constraints section names **multi-source grid-BFS** explicitly and compares against Exercise 3.
- Working code with tests: `mat=[[0,0,0],[0,1,0],[0,0,0]] → [[0,0,0],[0,1,0],[0,0,0]]`, `mat=[[0,0,0],[0,1,0],[1,1,1]] → [[0,0,0],[0,1,0],[1,2,1]]`, `mat=[[1,1,1],[1,1,1],[1,1,0]] → [[4,3,2],[3,2,1],[2,1,0]]`.

This is the cleanest "multi-source returns distance map, not max" variant. After Problems 1 and 2, the multi-source idiom should be reflexive for any "distance to nearest X" problem.

---

## Problem 3 — Open the Lock (LeetCode 752) (45 min)

A node-BFS problem on an implicit graph with forbidden states — the structural cousin of Exercise 4.

**Problem.** A lock has 4 wheels, each with digits `0-9`. The wheels can rotate freely (and wrap: `0` → `9` and vice versa). Given an initial state `'0000'`, a target combination, and a list of `deadends` (states the lock cannot be in), return the minimum number of moves to reach the target, or `-1` if impossible.

**The insight.** Nodes are 4-character strings; each node has 8 neighbors (each of the 4 digits can rotate up or down). Deadends are pre-blocked (treat as if "already visited"). Single-source BFS from `'0000'` with level tracking; the answer is a level count.

**Acceptance:**

- File `frame-writeups/c2-week-06/hw-03-open-the-lock.md`.
- Research constraints section names **node-BFS on an implicit graph** explicitly.
- Make the solution section pre-loads `deadends` into the visited set as a single line.
- Tests: `deadends=["0201","0101","0102","1212","2002"], target="0202" → 6`, `deadends=["8888"], target="0009" → 1`, `deadends=["8887","8889","8878","8898","8788","8988","7888","9888"], target="8888" → -1`, `deadends=["0000"], target="8888" → -1`.

Reading the spec, the trap is the deadends — without pre-loading them into visited, BFS will expand through them. The clean code is `visited = set(../deadends)` then immediately check `if start in visited: return -1`.

---

## Problem 4 — Word Ladder II (LeetCode 126) (60 min) — STRETCH

The "return all shortest sequences" variant of Exercise 4. Harder than the basic Word Ladder — requires reconstructing every shortest path, not just the length.

**Problem.** Same setup as Exercise 4, but return **every shortest transformation sequence**, in any order. Each sequence is a list of words. Return `[]` if no path exists.

**The insight.** Run BFS to compute the shortest *distance* to each word. Then perform a DFS (or reverse-BFS) from `endWord` back to `beginWord`, only following edges that strictly decrease the distance — this enumerates exactly the shortest paths.

**Acceptance:**

- File `frame-writeups/c2-week-06/hw-04-word-ladder-ii.md`.
- Research constraints section names the **two-phase approach** (BFS for distances + DFS for path reconstruction).
- Examine (../cost) section addresses the **output-sensitive complexity** — the number of shortest paths can itself be exponential in `N`, so the algorithm is `O(N × L² + k × L)` where `k` is the number of paths.
- Tests: `begin="hit", end="cog", list=["hot","dot","dog","lot","log","cog"] → [["hit","hot","dot","dog","cog"], ["hit","hot","lot","log","cog"]]`, `begin="hit", end="cog", list=["hot","dot","dog","lot","log"] → []`.

This problem is **stretch** for time-constrained learners. If you are behind, skip it and do Problem 5 (../behavioral) first. The senior signal is recognizing that the BFS computes distances and the DFS reconstructs paths — separating them keeps the algorithm clean.

---

## Problem 5 — Behavioral story #6 (45 min)

The story bank continues.

**Acceptance:**

- A file `behavioral/story-06.md` in your portfolio repo.
- Topic: **"Tell me about a time you had to choose between two approaches with different trade-offs."**
- Format: STAR (Situation, Task, Action, Result).
- 200-400 words.
- Read it aloud at least twice.
- Bonus credit: the story should connect to the *meta-skill* of BFS vs DFS. Every graph problem is "BFS or DFS?" — a decision with explicit trade-offs (BFS: shortest path, more memory; DFS: cycle detection, easier to code recursively). The connection is: every BFS-vs-DFS choice is a "two-approaches-different-tradeoffs" decision. Behavioral interviewers love when the candidate finds a structural connection to the technical skills.

---

## Problem 6 — System-design ground zero #6 (45 min)

Sixth 300-word warm-up.

**Acceptance:**

- A file `system-design/notes-week-06.md` containing a 300-word answer to: **"How would you design a web crawler that respects `robots.txt`, handles ~10 billion URLs, and finishes one full crawl per month?"**
- Do not look up the canonical answer first. Write what you would say in an interview today.
- After writing, search "web crawler architecture" and read one free article (try the Apache Nutch documentation or Mercator paper summary). Note three things you would add — *especially* if it mentions BFS over the URL frontier.

The connection to this week: web crawlers are BFS-over-the-URL-graph at planetary scale. The "URL frontier" is a queue; the "visited set" is a bloom filter or sharded DB (because the actual set is too large for memory). The interview-tell on this prompt is mentioning both the BFS framing and the engineering reality (the crawler is "BFS but on a distributed queue with a probabilistic visited filter").

---

## Time budget

| Problem | Time |
|--------:|----:|
| 1 — Number of Islands | 45 min |
| 2 — 0-1 Matrix | 45 min |
| 3 — Open the Lock | 45 min |
| 4 — Word Ladder II (../stretch) | 60 min |
| 5 — Behavioral story #6 | 45 min |
| 6 — System-design warm-up #6 | 45 min |
| **Total** | **4h 45min** (5h 45m with stretch) |

---

By the end of Week 6 your portfolio repo's commit history should show ~75-95 commits total (the cumulative count through Week 5 + ~12-15 commits this week, including the mini-project's two write-ups and the Minimum Knight Moves challenge write-up). The cadence is the artifact; keep the streak.

Up next: [Week 7 — DFS](../../week-07-dfs-and-topological-sort/).
