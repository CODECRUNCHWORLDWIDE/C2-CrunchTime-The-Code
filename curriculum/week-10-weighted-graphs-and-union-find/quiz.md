# Week 10 — Pattern-Recognition Quiz

Ten short prompts. **Do not solve them.** For each, decide which Week-10 algorithm applies — Dijkstra, Bellman-Ford, Floyd-Warshall, MST (Kruskal or Prim), DSU, or none of the above — and if Dijkstra-flavored, name the sub-shape (vanilla Dijkstra / Dijkstra-with-state / Bellman-Ford-with-hop-bound). One-line justification per answer. Lectures closed. Time yourself — 45 seconds per question is the target.

Answer key at the bottom.

---

**Q1.** "Given a directed weighted graph with non-negative weights and a source vertex `s`, return the shortest distance from `s` to every other vertex."

**Q2.** "Given a directed weighted graph that may contain negative edges and a source vertex `s`, return the shortest distance from `s` to every other vertex, or report that a negative cycle is reachable."

**Q3.** "Given an `n x n` matrix where `n <= 200` representing distances between cities, find the shortest path between every pair of cities."

**Q4.** "Given a list of `n` points on a 2D plane, find the minimum total cost to connect all of them, where the cost between two points is the Manhattan distance."

**Q5.** "Given a graph with `n` cities and an array of flights (with prices), find the cheapest fare from `src` to `dst` using **at most `k` intermediate stops**."

**Q6.** "Given an undirected graph as a list of `n` vertices and an array of edges (some of which may be redundant), find the single redundant edge such that removing it makes the graph a tree."

**Q7.** "Given a list of accounts, where each account is `[name, email1, email2, ...]`, merge all accounts that share at least one email and return the merged list."

**Q8.** "Given an unweighted graph and two vertices `s` and `t`, return the shortest number of edges from `s` to `t`."

**Q9.** "Given a list of `n` words, group them into equivalence classes under the relation 'two words are equivalent if they share a character at the same position.'"

**Q10.** "Given an `m x n` grid of 0s and 1s representing land and water, and a sequence of operations that add land cells one at a time, return the number of islands after each operation."

---

## Answer key

<details>
<summary>Click after attempting all ten</summary>

1. **Dijkstra (heap-based, single source).** The textbook case. Non-negative weights + single source = Dijkstra. `O((V + E) log V)`. Exercise 1 exactly.

2. **Bellman-Ford with negative-cycle detection.** Negative edges allowed = Bellman-Ford. The "or report that a negative cycle exists" is the `V`-th pass after the `V - 1` relaxation passes. `O(V E)`. Lecture 2 §1.

3. **Floyd-Warshall.** All-pairs shortest paths with `V <= 200` = Floyd-Warshall. `O(V^3) = 8 * 10^6` operations — fast in Python. The three-nested-loop DP with `k` outermost. Lecture 2 §3.

4. **MST (Kruskal preferred for the cleanest illustration; Prim acceptable).** "Minimum total cost to connect all of them" = spanning tree minimization. The graph is dense (`E = O(n^2)` for points on a plane), so Prim is asymptotically competitive; Kruskal with a sort by Manhattan distance is the cleaner answer. LC 1584. Lecture 2 §4-6.

5. **Bellman-Ford bounded by `K + 1` passes, OR modified Dijkstra with state `(node, hops)`.** Hop-constrained shortest path. Bellman-Ford is safer to write under pressure; Dijkstra-with-state can be faster on real inputs. Exercise 2 / Challenge 1 exactly. Lecture 2 §2.

6. **DSU (redundant connection sub-shape).** Iterate edges in order; the first edge whose `union(u, v)` returns `False` (already in the same component) is the redundant one. LC 684. The DSU half of the mini-project. Lecture 3 §4.

7. **DSU (account merge sub-shape).** Map emails to account indices; union accounts that share an email; group emails by their account's root. LC 721. Lecture 3 §4.

8. **Not a Week-10 algorithm — BFS from Week 6.** Unweighted = BFS. The trap is reaching for Dijkstra (which works but is overkill); BFS is `O(V + E)` and simpler. Negative-space rejection.

9. **DSU.** The relation "share a character at the same position" is symmetric and induces equivalence classes after transitive closure. DSU over the `n` words; for each pair `(i, j)`, union if they share a character at the same position. `O(n^2 L)` for the comparison + `O(n^2 alpha(n))` for the unions. The trap is reaching for BFS-on-a-virtual-graph; DSU is shorter and cleaner.

10. **DSU (streaming-islands sub-shape).** LC 305 — Number of Islands II. Each new cell starts as its own component (`count += 1`); each successful union with an existing adjacent land cell decrements the count. The streaming variant is what makes DSU the only clean choice — BFS would re-run on the full grid per operation. Lecture 3 §4.

</details>

---

## How to score

| Score | Meaning |
|------:|---------|
| 9-10 | Weighted-graph / DSU recognition is interview-ready, including the negative-space rejections (Q8). Move on. |
| 7-8 | Good — re-read [Lecture 1 §5](./lecture-notes/01-dijkstra-and-the-shortest-path-picker.md) and [Lecture 3 §4](./lecture-notes/03-union-find-and-the-dsu-triggers.md) for the sub-shape questions you missed. Most learners miss Q8 (BFS rejection) or Q9 (DSU on a virtual graph) first time; that is normal. |
| 5-6 | Redo Exercises 2 and 3 with stricter Match sections. The Bellman-Ford and DSU recognition needs more reps before Mock #2. |
| <5 | The pattern recognition is not yet automatic. Re-read all three lectures, re-do all three exercises with the algorithm choice stated aloud, then retake the quiz. |

This quiz is about **fluency**, not difficulty. The discriminating questions are Q8 (negative-space — BFS not Dijkstra), Q9 (DSU on a virtual graph), and Q10 (streaming DSU). Q8 is the most-missed; senior candidates over-apply Dijkstra to any graph problem.

Q1 (Dijkstra) and Q5 (Bellman-Ford with hop bound) are the cleanest direct-template questions. Q3 and Q4 test recognition of the "small `V` -> Floyd-Warshall" and "connect all -> MST" reflexes.

When done, the [homework](./homework.md) is next.
