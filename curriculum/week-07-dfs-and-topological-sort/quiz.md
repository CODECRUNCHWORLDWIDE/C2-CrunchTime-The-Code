# Week 7 — Pattern-Recognition Quiz

Ten short prompts. **Do not solve them.** For each, decide whether it is DFS / topological sort / something else — and if DFS, name the sub-shape (recursive / iterative / three-color / post-order) and any invariant required (visited / parent pointer / color array / in-degree). One-line justification per answer. Lectures closed. Time yourself — 45 seconds per question is the target.

Answer key at the bottom.

---

**Q1.** "Given an `n × n` symmetric matrix where `M[i][j] == 1` means cities `i` and `j` are connected, return the number of connected components (provinces)."

**Q2.** "Given a directed graph as an adjacency list, return `True` if it contains a cycle, else `False`."

**Q3.** "Given `numCourses` and a list of `[a, b]` prerequisites (`b` before `a`), return any valid order in which the courses can be taken, or `[]` if no valid order exists."

**Q4.** "Given the root of a binary tree, return its level-order traversal — a list of lists where the `i`-th inner list contains the values at depth `i`."

**Q5.** "Given a 2-D grid where `1` is land and `0` is water, return the area of the largest island (a maximal 4-connected region of `1`s)."

**Q6.** "Given a list of strings sorted lexicographically in an unknown alien language's alphabet, return the order of the letters in that alphabet."

**Q7.** "Given an undirected graph and a `source` and `destination`, return the *shortest* number of edges in a path from source to destination."

**Q8.** "Given an undirected graph, return all 'bridge' edges — edges whose removal disconnects the graph."

**Q9.** "Given a binary search tree, return `True` if it is a valid BST (every left subtree's values are less than the node, every right subtree's values are greater), else `False`."

**Q10.** "Given an array of integers, return all unique permutations of its elements."

---

## Answer key

<details>
<summary>Click after attempting all ten</summary>

1. **DFS for connectivity, recursive.** Adjacency-matrix DFS; the answer counts the number of fresh DFS starts. Visited is a `set[int]`. The matrix is symmetric → undirected graph → no cycle-detection invariant needed (we are only counting components). `O(n²)` time, `O(n)` space. Exercise 1 exactly.

2. **DFS with the three-color invariant.** Directed cycle detection. White (`0`) / gray (`1`) / black (`2`); a directed edge to a gray node is a back-edge → cycle. The parent-pointer technique does *not* apply to directed graphs. `O(V + E)` time. Lecture 3 §2.

3. **Topological sort — Kahn's algorithm.** In-degree array; queue of zero-in-degree courses; cycle detection by exhaustion (`len(order) != numCourses`). Edge `b → a` for `[a, b]`. `O(V + E)` time. Exercise 3 exactly.

4. **NOT DFS — BFS with level tracking.** "Level-order" is the BFS signature; the outer `for _ in range(len(queue))` loop consumes one level per outer iteration. Returning DFS pre-order would visit siblings far apart, not by level. The Week-6 idiom; recognizing it as *not* a Week-7 problem is the negative-space discriminator.

5. **DFS for connectivity, with a "weight" return.** Grid-DFS over 4-connected `1`-cells; each DFS call returns the size of its component; track the max across all DFS starts. The trick is post-order aggregation: each call returns `1 + sum(child_sizes)`. `O(R × C)`. LC 695.

6. **Topological sort on a derived edge set.** Alien Dictionary — Challenge 2. The Match move: extract pairwise edges from adjacent words (first differing character → edge), then Kahn's. The recognition step is the senior signal; the algorithm itself is the same Kahn template from Exercise 3.

7. **NOT DFS — BFS.** "Shortest number of edges" on an unweighted graph is the canonical BFS signal (Week 6 Lecture 1). DFS would find *a* path but not the shortest. This is a negative-space question — the trap is that the problem reads like DFS until you notice "shortest."

8. **DFS with Tarjan's low-link.** Critical Connections — Challenge 1. `disc[u]` (discovery time) and `low[u]` (smallest discovery time reachable from `u`'s subtree via at most one back-edge). Edge `(u, v)` is a bridge iff `low[v] > disc[u]`. `O(V + E)` time. The naive `O(E × (V + E))` "remove each edge, check connectivity" is too slow.

9. **DFS on a tree, in-order or with bounds.** Two approaches: in-order traversal (the values must come out sorted) or recursive DFS with `(lo, hi)` bounds passed in (every node's value must satisfy `lo < val < hi`; recursion narrows the bounds). Both `O(N)`. The bounds approach is cleaner; the in-order approach catches more edge cases (duplicates, ints overflow). LC 98.

10. **NOT pure DFS — backtracking.** Generating all permutations requires the "undo" step (mark an element used, recurse, unmark). Backtracking is DFS-shaped but with an explicit unwinding step that pure DFS does not have. Covered next week (Week 8). The trap is that backtracking looks identical to recursive DFS until you notice the "generate all configurations" framing.

</details>

---

## How to score

| Score | Meaning |
|------:|---------|
| 9-10 | DFS / topo recognition is interview-ready, including the negative-space rejections. Move on. |
| 7-8 | Good — re-read [Lecture 1 §8](./lecture-notes/01-recursive-dfs.md) and [Lecture 3 §8](./lecture-notes/03-topological-sort.md) for the sub-shape questions you missed. Most learners miss Q4 or Q7 first time; that is normal. |
| 5-6 | Redo Exercises 2 and 3 with stricter Match sections. The iterative-DFS and topological-sort recognition needs more reps before Mock #2. |
| <5 | The pattern recognition is not yet automatic. Re-read all three lectures, re-do all three exercises with the visited-set invariant stated aloud, then retake the quiz. |

This quiz is about **fluency**, not difficulty. The discriminating questions are Q4 and Q7 — both "looks like DFS but is BFS" questions. Recognizing the negative space is the senior-level skill being measured.

The negative-space questions (Q4, Q7, Q10) are the discriminators. Q7 in particular is a trap: "shortest path" on an unweighted graph is BFS, not DFS — and getting this wrong on a graph problem in Mock #2 is a meaningful score loss. Q10 is also a trap: permutation generation is backtracking, which is DFS-shaped but not pure DFS.

When done, the [homework](./homework.md) is next.
