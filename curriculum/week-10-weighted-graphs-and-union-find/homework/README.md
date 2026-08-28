# Week 10 — Homework

Six practice problems plus the rubric. Allow ~5 hours total. Do the problems on your own with the lectures *closed*; consult the lecture or the resources only after a 15-minute stuck-period on a single problem.

The problems are chosen to drill the six Week-10 sub-patterns: heap-Dijkstra, Bellman-Ford variant, MST disguise, DSU components, DSU account-merge, and DSU edge-case (cycle detection). By Sunday, the recognition step on each should be reflexive.

| # | Problem | Pattern | Source | Est. time |
|---|---------|---------|--------|----------:|
| 1 | Accounts Merge | DSU + account-merge sub-shape | LeetCode 721 | 60 min |
| 2 | Path With Minimum Effort | Dijkstra on a grid (binary-search alternative) | LeetCode 1631 | 50 min |
| 3 | Min Cost to Connect All Points | MST (Kruskal or Prim) on a complete graph | LeetCode 1584 | 45 min |
| 4 | Graph Valid Tree | DSU + edge-count check | LeetCode 261 | 30 min |
| 5 | Find the City With the Smallest Number of Neighbors at a Threshold Distance | Floyd-Warshall | LeetCode 1334 | 50 min |
| 6 | Path With Maximum Probability | Dijkstra with a max-heap (multiplicative weights) | LeetCode 1514 | 45 min |

Problems 1, 4, and 6 are the high-yield DSU and Dijkstra drills; problem 2 is the grid-Dijkstra rep; problem 3 is the MST disguise; problem 5 is the rare Floyd-Warshall rep.

---

## Problem 1 — Accounts Merge (LC 721)

**Spec.** Given a list of `accounts`, where each `account` is `[name, email1, email2, ...]`, merge accounts that share at least one email. Return the merged list with emails sorted within each account.

**Constraints.** `1 <= len(../accounts) <= 1000`; `2 <= len(../account) <= 10`; emails are lowercase strings with valid format.

**Pattern.** DSU + account-merge sub-shape (Lecture 3 §4).

**Hint.** Two phases: (../a) map each email to an account index, unioning the current account with any earlier account that owns the email; (../b) group emails by `uf.find(../account_index)` and assemble the output with the original name at the front, emails sorted.

**Acceptance.** Function signature `accounts_merge(accounts: List[List[str]]) -> List[List[str]]`. Time: `O(N alpha(../N))` where `N` is total email count. Space: `O(../N)`.

**Variant.** The alternative is BFS on a graph of "accounts that share an email" — same asymptotic but more complex. Mention by name in the write-up.

---

## Problem 2 — Path With Minimum Effort (LC 1631)

**Spec.** Given a 2D grid of heights, find a path from top-left to bottom-right minimizing the *maximum* absolute height difference between consecutive cells on the path.

**Constraints.** `1 <= rows, cols <= 100`; `0 <= heights[i][j] <= 10^6`.

**Pattern.** Dijkstra on a grid where the "distance" is the *max* of edge weights along the path, not the *sum*. The relaxation becomes `new_max = max(d, abs(h[r][c] - h[nr][nc]))` instead of `d + weight`. Otherwise the algorithm is the canonical heap-Dijkstra.

**Hint.** Treat the grid as a graph; vertices are `(r, c)` pairs; edges connect orthogonally adjacent cells; weights are absolute height differences. Run heap-Dijkstra with the max-of-edges relaxation.

**Acceptance.** Function signature `minimum_effort_path(heights: List[List[int]]) -> int`. Time: `O(R C log(R C))` where `R, C` are grid dimensions. Space: `O(R C)`.

**Variant.** Binary search + BFS is an alternative: binary-search on the answer, BFS to check feasibility. Same asymptotic; slightly more code; the Dijkstra variant is preferred.

---

## Problem 3 — Min Cost to Connect All Points (LC 1584)

**Spec.** Given `n` points on a 2D plane, return the minimum cost to connect all points into a single connected component, where the cost between two points is the Manhattan distance `|x1 - x2| + |y1 - y2|`.

**Constraints.** `1 <= n <= 1000`; `-10^6 <= x, y <= 10^6`.

**Pattern.** MST on a complete graph where edge weights are Manhattan distances. Kruskal with DSU is the standard reach; Prim is competitive because `E = n(../n-1)/2` is dense.

**Hint.** Generate all `n(../n-1)/2` edges as `(weight, i, j)` triples; sort by weight; run Kruskal. The complete-graph cost is the price of dense connectivity; for very large `n`, generate edges lazily.

**Acceptance.** Function signature `min_cost_connect_points(points: List[List[int]]) -> int`. Time: `O(n^2 log n)` dominated by the sort. Space: `O(../n^2)` for the edge list.

**Variant.** For large `n`, the linear-time MST algorithm (../Karger-Klein-Tarjan) and the "Manhattan distance MST in `O(n log n)`" specialized algorithm (../Guibas-Stolfi) are both Phase-3 stretch. Mention by name.

---

## Problem 4 — Graph Valid Tree (LC 261)

**Spec.** Given `n` vertices labeled `0..n-1` and an edge list, determine whether the graph is a valid tree (connected and acyclic).

**Constraints.** `1 <= n <= 2000`; `0 <= len(../edges) <= 5000`.

**Pattern.** DSU + edge-count check. A tree has exactly `n - 1` edges and is connected. With DSU: if `len(../edges) != n - 1`, return False immediately. Otherwise, union every edge; if any `union` returns False (../cycle), return False. Finally, check `uf.components == 1`.

**Hint.** The two checks must both pass: `len(../edges) == n - 1` *and* all unions succeed (i.e., no cycle was ever encountered). The `components == 1` check is equivalent to "all unions succeeded" when there are exactly `n - 1` edges.

**Acceptance.** Function signature `valid_tree(n: int, edges: List[List[int]]) -> bool`. Time: `O(E alpha(../V))`. Space: `O(../V)`.

**Variant.** BFS or DFS counting vertices reached + checking for back edges is the BFS-flavored alternative. Same asymptotic; the DSU is shorter to write.

---

## Problem 5 — Find the City With the Smallest Number of Neighbors (LC 1334)

**Spec.** Given `n` cities with `m` weighted edges and a `distanceThreshold`, find the city with the smallest number of other cities reachable within `distanceThreshold`. If multiple, return the city with the largest index.

**Constraints.** `2 <= n <= 100`; `1 <= m <= n * (n - 1) / 2`; `1 <= edge[i].length == 3`; weights up to `10^4`.

**Pattern.** All-pairs shortest paths. `n <= 100`, so `O(../n^3) = 10^6` is trivially fast — Floyd-Warshall is the cleanest reach.

**Hint.** Initialize `dist[i][j] = inf` for `i != j` and `dist[i][i] = 0`. Set `dist[i][j] = w` for each edge. Run Floyd-Warshall. For each city `i`, count `j != i` with `dist[i][j] <= distanceThreshold`. Return the city with the smallest count, breaking ties by larger index.

**Acceptance.** Function signature `find_the_city(n: int, edges: List[List[int]], distance_threshold: int) -> int`. Time: `O(../n^3)`. Space: `O(../n^2)`.

**Variant.** Running Dijkstra from each vertex is also correct — `O(n * (V + E) log V)`. For `n = 100` this is `~ 10^5 * 7 ≈ 7 * 10^5` vs Floyd-Warshall's `10^6`; comparable. Floyd-Warshall is shorter to write.

---

## Problem 6 — Path With Maximum Probability (LC 1514)

**Spec.** Given a graph where each edge has a "success probability" in `[0, 1]`, find the path from `start` to `end` maximizing the product of edge probabilities.

**Constraints.** `2 <= n <= 10^4`; `0 <= len(../edges) <= 2 * 10^4`.

**Pattern.** Dijkstra with a **max-heap** (or negate-and-use-min-heap). The relaxation is *multiplicative*: `new_prob = d * prob[edge]`; we pick the largest.

**Hint.** Initialize `prob[start] = 1.0`, all others `0.0`. Heap stores `(-d, node)` to use Python's min-heap as a max-heap. Relaxation: `new_prob = d * weight`; if `new_prob > prob[neighbor]`, update.

**Acceptance.** Function signature `max_probability(n: int, edges: List[List[int]], succ_prob: List[float], start: int, end: int) -> float`. Time: `O((V + E) log V)`. Space: `O(V + E)`.

**Variant.** The Bellman-Ford variant works for negative-log transformation: take `-log(../p)` of each weight; minimize the sum; the original probability is `exp(../-sum)`. Same asymptotic; Dijkstra is faster for this problem since all log-weights are non-negative.

---

## Rubric

For each problem, your write-up is graded on five dimensions:

| Dimension | Weight | What "yes" looks like |
|-----------|-------:|----------------------|
| Research constraints (pattern recognition) | 25% | 30-second memo at the top; pattern named in one of the six families; alternative rejected with reason |
| Assess options | 15% | Numbered steps; data structure choice stated; algorithm form noted |
| Make the solution (../correctness) | 25% | All LC sample cases pass; no off-by-one; the canonical bug list checked |
| Make the solution (../style) | 10% | Type hints everywhere; docstrings on every function; PEP 8; idiomatic Python |
| Examine (../defense) | 25% | Time + space bounds with derivation; one variant mentioned; trade against the alternative algorithm stated |

The Research constraints weight is the highest for a reason. Phase 2 grades recognition heavily; you can have a working implementation and still lose the rep if you cannot defend the choice over the alternative.

---

## Suggested order

1. **Problem 4** first — Graph Valid Tree is the highest-recognition-density DSU rep. The `n - 1` edges + no cycles + one component composition cements the Lecture 3 template.
2. **Problem 1** second — Accounts Merge is the canonical DSU disguise. The two-phase structure (union then group) is the template for the rest of Phase 2's DSU problems.
3. **Problem 6** third — Path With Maximum Probability is the Dijkstra variant with multiplicative weights. Quick rep on the heap-priority pattern.
4. **Problem 2** fourth — Path With Minimum Effort is the grid-Dijkstra rep with a non-standard relaxation. Take time on the max-of-edges vs sum-of-edges distinction.
5. **Problem 3** fifth — Min Cost to Connect All Points is the MST disguise. The "connect all" cue is the recognition rep.
6. **Problem 5** last — Find the City is the Floyd-Warshall rep. Save for the latter half of the week; the three-nested-loop is short but the loop-order discipline is the work.

If time runs out, prioritize Problems 1, 4, and 6. They are the three patterns most likely to appear on Mock #2.

---

## Acceptance

The week's homework is complete when:

- All six problems have a committed implementation under `homework/c2-week-10/`.
- All six problems have a FRAME write-up under `frame-writeups/c2-week-10/homework/`.
- The quiz is taken and scored.
- The score is in the retrospective: which sub-pattern needs the most reps before Mock #2.

The retrospective is the single most useful artifact this week. The pattern most candidates need more reps on after W10 is "Bellman-Ford with the snapshot idiom under interview pressure" — the snapshot is short but easy to flub on the spot. Drill it in writing, then drill it aloud.
