# Week 6 — Pattern-Recognition Quiz

Ten short prompts. **Do not solve them.** For each, decide whether it's BFS or not — and if BFS, name the sub-shape (grid / node), the seed (single / multi-source), and any high-end variant (level tracking / bidirectional). One-line justification per answer. Lectures closed. Time yourself — 45 seconds per question is the target.

Answer key at the bottom.

---

**Q1.** "Given an `m × n` binary matrix, return the length of the shortest clear path from the top-left to the bottom-right, where cells with value `0` are walkable and 8-directional moves are allowed."

**Q2.** "Given an undirected weighted graph where edge weights are positive integers, return the shortest path (by total weight) from node `s` to node `t`."

**Q3.** "Given a binary tree, return its level-order traversal — a list of lists where the `i`-th inner list contains the values of all nodes at depth `i`."

**Q4.** "Given an `m × n` matrix where each cell is `0` (water) or `1` (land), an island is a maximal connected region of `1`s. Return the number of distinct islands."

**Q5.** "Given an `m × n` grid where each cell is `0` (empty), `1` (fresh orange), or `2` (rotten orange), return the minimum minutes until no fresh orange remains, or -1 if some fresh orange can never become rotten."

**Q6.** "Given two words `beginWord` and `endWord`, and a dictionary `wordList`, return the length of the shortest transformation sequence such that each step changes exactly one letter and every intermediate word is in `wordList`."

**Q7.** "Given a directed acyclic graph (DAG) representing course prerequisites, return any valid order in which the courses can be taken."

**Q8.** "Given an array `nums` and an integer `k`, return the `k` most frequent elements."

**Q9.** "Given a 2-D matrix of `0`s and `1`s, for each cell return the distance to the nearest `0`."

**Q10.** "Given a chess knight at `(0, 0)` on an infinite board and a target `(x, y)`, return the minimum number of knight moves to reach the target."

---

## Answer key

<details>
<summary>Click after attempting all ten</summary>

1. **BFS — grid-BFS, single-source, 8-directional.** "Shortest path" + "binary matrix" + "8-directional" is the canonical Drill 2 signal. Per-node distance idiom. `O(R × C)` time.

2. **NOT BFS — Dijkstra's algorithm.** Weighted graph with positive weights. BFS does not handle weighted edges; Dijkstra uses a priority queue (min-heap) instead of a FIFO queue. Out of scope this week (C5 covers it). The trap is the word "shortest path" alone — without the unweighted property, BFS is wrong.

3. **BFS — node-BFS on a tree with level tracking.** Drill 1 exactly. The level-tracking idiom (`for _ in range(len(queue))`) is the natural fit for level-grouped output. `O(N)` time.

4. **BFS — grid-BFS, single-source per island.** "Connected components" / "islands" is a graph-traversal problem; either BFS or DFS works. The standard implementation: walk the grid, when finding an unvisited land cell, run BFS (or DFS) from it to mark its entire component, count one. `O(R × C)`. Either traversal is acceptable; DFS is cleaner to code recursively.

5. **BFS — multi-source grid-BFS.** Drill 3. The plural "rotten oranges" is the signal: multiple seeds. Seed the queue with all rotten cells at minute 0; the answer is the max distance reached after confirming every fresh orange is reachable. `O(R × C)`.

6. **BFS — node-BFS on an implicit string graph + wildcard-bucket index.** Drill 4. The standard Word Ladder problem. Level-tracking idiom; the answer is a level count. `O(N × L²)` with the bucket index, where `N` is dictionary size and `L` is word length.

7. **NOT pure BFS — topological sort.** Kahn's algorithm uses a BFS-shaped queue, but with extra state (in-degree counts) and a different termination condition. Tarjan's algorithm uses DFS with post-order. Both are covered in Week 7 (DFS). Calling it "BFS" oversimplifies; the right answer is "topological sort via Kahn (BFS-shaped) or Tarjan (DFS-shaped)."

8. **NOT BFS — heap (Week 9).** "Top-K" is the heap pattern. Pure BFS has no role here — there is no graph, no distance, no traversal. The trap is "k" appearing in the prompt; in BFS contexts, "k" might be a level, but here it is a count.

9. **BFS — multi-source grid-BFS.** Identical to Drill 3 in structure: seed the queue with all `0` cells, expand outward, record distance to each `1` cell. The result is the per-cell distance to the nearest `0`. `O(R × C)`. LeetCode 542.

10. **BFS — node-BFS on an infinite implicit graph + symmetry + bounded search region.** The week's challenge. The trap is the infinite graph; the senior move is symmetry reduction to the first quadrant and bounding the visited set to a `(|x| + 4) × (|y| + 4)` rectangle. Bidirectional BFS is the production-grade optimization.

</details>

---

## How to score

| Score | Meaning |
|------:|---------|
| 9-10 | BFS pattern recognition is interview-ready, including the negative-space rejections. Move on. |
| 7-8 | Good — re-read [Lecture 2 §11](./02-lecture-notes/02-grid-bfs-and-graph-bfs.md) for the sub-shape questions you missed. Most learners miss Q2 or Q7 first time; that is normal. |
| 5-6 | Redo Drills 3 and 4 with stricter Match sections. The multi-source and node-BFS recognition needs more reps before Mock #2. |
| <5 | The pattern recognition is not yet automatic. Re-read both lectures, re-do all five drills with the visited-set invariant stated aloud, then retake the quiz. |

This quiz is about **fluency**, not difficulty. The discriminating questions are Q2 and Q7 — both "looks like BFS but is not" questions. Recognizing the negative space is the senior-level skill being measured.

The negative-space questions (Q2, Q7, Q8) are the discriminators. Q2 in particular is a trap: weighted graphs need Dijkstra, not BFS. Saying "BFS for shortest paths" without qualifying "on unweighted graphs" is a missing-half answer. Q7 is also a trap: topological sort *uses* a queue, but the algorithm has extra state and a different termination — naming it "BFS" oversimplifies.

When done, the [homework](./06-homework.md) is next.
