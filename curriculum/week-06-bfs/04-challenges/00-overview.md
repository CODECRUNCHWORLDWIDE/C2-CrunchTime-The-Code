# Week 6 — Challenges

One challenge this week. It is the canonical hard BFS problem of the standard interview repertoire — the kind of problem that, when solved cleanly, signals senior-level BFS fluency on an *infinite implicit graph*.

| # | Challenge | Pattern | Difficulty | Target solve time |
|---|-----------|---------|------------|------------------:|
| 1 | [Minimum Knight Moves](./challenge-01-minimum-knight-moves.md) | BFS on an infinite implicit graph + symmetry pruning + (optionally) bidirectional BFS | Hard | 90 min |

The challenge composes the node-BFS template (from Drill 4) with two non-obvious optimizations: **search-region bounding** (the knight cannot need more than `|x| + |y|` moves, so search within that radius) and **coordinate symmetry** (`(x, y)` and `(|x|, |y|)` yield the same answer). The boundary defense for this problem is the strictest of the week — read the prompt twice, draw the search region by hand, and commit to a pruning strategy before writing code.

Why this matters: Minimum Knight Moves is a "BFS on an infinite graph" problem — a class that includes some of the hardest interview questions (sliding puzzles, optimal-step-count games, infinite-board navigation). If you can deliver UMPIRE on it cleanly in 90 minutes the first time and 45 minutes the second time, you have demonstrated a level of BFS mastery few candidates reach in a 15-week prep cycle.

If you find yourself stuck past the 60-minute mark, **stop and re-read Lecture 2 §7 (bidirectional BFS) and the "Pitfall 4 — unbounded queue on infinite graphs" subsection of Lecture 2 §9**. Then restart Plan with the search-region bound written explicitly. The algorithm cannot be derived without the bound; trying to write code before the bound is the source of every wrong attempt.

The challenge has structural cousins in the homework — **Open the Lock (LC 752)** and **Bus Routes (LC 815)** — both "BFS on an implicit graph with non-trivial state." Doing one of the homework problems first, as a warm-up, is acceptable.
