# Week 7 — Challenges

Two challenges this week. One is the canonical hard DFS problem of the standard interview repertoire (graded for completion); the second is an optional topological-sort stretch (graded only if you finish the first with time to spare).

| # | Challenge | Pattern | Difficulty | Target solve time | Required? |
|---|-----------|---------|------------|------------------:|:---------:|
| 1 | [Critical Connections in a Network](./challenge-01-critical-connections.md) | DFS post-order with Tarjan's low-link; bridge detection | Hard | 90 min | yes |
| 2 | [Alien Dictionary](./challenge-02-alien-dictionary.md) | Topological sort on a derived edge set | Hard | 75 min | optional |

The challenges compose the templates from Lectures 1-3:

- **Challenge 1** builds on the recursive DFS template and the post-order discipline from Lecture 3. The low-link computation is a "compute on the way up" pattern — the same shape as DFS post-order topological sort, but the work-on-finish produces a numerical value instead of an emit.
- **Challenge 2** builds on Kahn's algorithm from Lecture 3 §4. The stretch is in *deriving* the edge set — the input is a list of strings sorted in an unknown language's alphabet; you must extract the pairwise letter-ordering constraints before running topological sort.

If you find yourself stuck past the 60-minute mark on Challenge 1, **stop and re-read Lecture 3 §6 (Course Schedule II worked example) and Lecture 1 §11 (worked example end-to-end)**. The low-link computation cannot be derived without the DFS post-order discipline; trying to write code before the post-order shape is the source of every wrong attempt.

Challenge 2 is **optional** for time-constrained learners. If you only have time for one challenge this week, do Challenge 1 — it is the one Mock #2 most often draws from. Challenge 2 is the natural follow-up if you finish early; it forces a "model the problem as a graph" recognition step that strengthens the Match-step muscle.

Both challenges have structural cousins in the homework: Number of Connected Components (HW 1) shares the connectivity template with Exercise 1; Validate Binary Search Tree (HW 4) shares the tree-DFS template with Exercise 1; Course Schedule (HW 2) shares the Kahn template with Exercise 3.
