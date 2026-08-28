# Mini-Project — Dijkstra + DSU, Fully FRAME-Narrated

> The week's deliverable: two compact portfolio artifacts that demonstrate fluency across the two highest-leverage Week-10 patterns — heap-based Dijkstra on a single-source shortest-path problem and Union-Find on a cycle-detection problem — with full FRAME narration end-to-end. The pair is the discriminating element — Mock #2 grades the *shortest-path family* and the *components-and-merge family* separately, and shipping one of each forces you to articulate the structural difference out loud.

**Estimated time:** 10 hours, split across Thursday-Saturday.

This mini-project is *narration-heavy* rather than *content-heavy*. You will produce two FRAME write-ups, each fully delivered in all five sections, each anchored by a 30-second pattern-recognition memo at the top. The two write-ups must be navigable as a pair — cross-references between them are part of the rubric.

---

## Why this matters

Three reasons.

1. **Phase 2 is graded on Research constraints.** Phase 1 spent four weeks installing the FRAME habit; Make the solution was the primary work. Phase 2 patterns are heavier and the Research constraints step matters more — recognition cost is no longer "30 seconds to name the pattern" but "60 seconds to name the algorithm choice (Dijkstra / Bellman-Ford / DSU / MST), defend the asymptotic improvement over the naive baseline, and reject one wrong alternative." This mini-project is the fifth in C2 to grade two parallel write-ups as a *pair* (W6 BFS pair, W7 DFS pair, W8 heap pair, W9 string pair, W10 graph-and-DSU pair).

2. **Dijkstra and DSU are the two structural shapes of every interview weighted-graph question.** Half of all FAANG weighted-graph problems are shortest-path variants (Dijkstra, Bellman-Ford, Floyd-Warshall); the other half are components / merge / equivalence variants (DSU, with MST as a derived application). The pair forces you to articulate the differences: when do you want the algorithm first (Dijkstra) versus the data structure first (DSU); when does prefix sharing buy you anything (it does not — that was W9); when does amortized near-constant `find` buy you the algorithm (Kruskal MST).

3. **The full FRAME narration is the rubric.** Drills are graded on Research constraints + Make the solution; the mini-project adds Frame, Assess options, Examine, *and* cross-references. By Sunday you should be able to produce a full FRAME narration on a weighted-graph or DSU problem in 20-25 minutes, recorded, without rehearsal.

---

## What you ship

Three files: two problem write-ups plus a short overview.

```
frame-writeups/c2-week-10/mini-project/
├── README.md                                              ← short overview + index + reflection
├── problem-01-dijkstra-network-delay-time.md              ← heap-Dijkstra on LC 743
└── problem-02-dsu-redundant-connection.md                 ← DSU on LC 684
```

Each write-up is the full FRAME format from Week 1, **plus a leading 30-second pattern-recognition memo at the top**.

The two problems are chosen so that:

- **Problem 1 (heap-Dijkstra):** the algorithm is the canonical heap-based single-source shortest-paths from LC 743, narrated as if you were demoing the algorithm choice. The discriminator is the lazy-delete guard — articulating "the `heapq` has no decrease-key; the `if d > dist[node]: continue` guard skips stale entries on pop" is the defense.

- **Problem 2 (DSU + redundant connection):** the algorithm is Union-Find on LC 684 (Redundant Connection). The Research constraints move is recognizing that the "find the redundant edge" prompt is exactly the cycle-detection sub-shape of DSU; the defense is "the first edge whose `union(u, v)` returns False is the redundant one — that union would have closed a cycle."

The two problems together cover every Week-10 idiom: heap-priority-queue mechanics, lazy-delete, the "settle once" invariant, DSU class form, path compression, union by rank, cycle detection. After this pair, the recognition for any weighted-graph or DSU problem should reduce to: *shortest path or components?*

---

## The 30-second pattern-recognition memo (the signature element)

At the top of each write-up, immediately after the title, place a single bordered block.

### For Problem 1 (heap-Dijkstra)

```markdown
> **30-second pattern-recognition memo (Dijkstra):**
> This is a shortest-path problem because [the prompt asks for the minimum
> time / distance / cost from a source / to all reachable nodes].
> Weights are [non-negative -> Dijkstra; otherwise -> Bellman-Ford].
> Sub-shape: [heap-Dijkstra with `heapq`; lazy-delete guard].
> Why not BFS: [weights are non-uniform; BFS only works on unweighted].
> Why not Bellman-Ford: [weights non-negative; Dijkstra is faster by log V].
```

### For Problem 2 (DSU)

```markdown
> **30-second pattern-recognition memo (DSU):**
> This is a DSU problem because [the prompt asks about merging / components
> / equivalence / cycle detection / redundant edges].
> Sub-shape: [components-count / cycle-detection / account-merge /
> streaming-islands].
> Optimizations: [path compression in find + union by rank in union ->
> amortized O(alpha(n))].
> Why not BFS/DFS: [streaming queries / amortized near-constant per
> operation / simpler for the "iterate edges and union" formulation].
> The trigger word: [merge / connect / equivalent / redundant / group].
```

Read each aloud; both should hit 25-30 seconds.

---

## FRAME structure for each write-up

The full five-section format, with Examine split into its verify and cost halves. The Research constraints section opens with the 30-second memo above.

### Frame

Restate the problem in your own words. Walk one example by hand. Note the constraints. Specifically address:

- For Problem 1 — restate the input format (`times`, `n`, `k`), the output (max distance or `-1`), and the reachability check that produces the `-1` return.
- For Problem 2 — restate the input format (a list of edges on `n` vertices with one redundant), the output (the redundant edge), and the spec detail that the *last* such edge in the input is the answer.

### Research constraints

Open with the 30-second memo. Then in 2-3 sentences:

- Name the pattern: heap-Dijkstra (Problem 1) or DSU cycle-detection (Problem 2).
- Name the sub-shape: lazy-delete with `heapq` (Problem 1) or path-compression-plus-union-by-rank UnionFind class (Problem 2).
- Reject the alternative: BFS or Bellman-Ford for Problem 1; BFS-based cycle-detection for Problem 2.

### Assess options

Numbered steps; 4-6 lines each. State the data structure first. State the loop / recursion structure second. State the termination condition third.

For Problem 1: build adjacency list; init `dist` and heap; relax loop with lazy-delete guard; return `max(dist.values())` or `-1`.

For Problem 2: build UnionFind on `n + 1` (LC 684 uses 1-indexed vertices); iterate edges in order; return the first edge whose `union` returns False.

### Make the solution

The code. Type hints on every function. Docstrings on every public method. Comments only where the line is non-obvious — the lazy-delete guard deserves a comment; the `setdefault` form does not.

### Examine · verify

Trace the implementation by hand on at least two inputs:

- One positive example (the canonical "it works" case).
- One edge case (single-vertex graph for Problem 1; small graph with the redundant edge as the first edge for Problem 2).

For Problem 2, the second trace must include the moment of `union` returning False — otherwise the cycle-detection work is invisible.

### Examine · cost

Time and space bounds with derivation. The derivation is mandatory, not the bound alone.

- Problem 1: `O((V + E) log V)` derived from "`V` heap pops + `E` heap pushes, each `O(log V)`."
- Problem 2: `O(N alpha(N))` derived from "`N` edges, each triggering a constant number of `find` + `union` calls; each call is amortized `O(alpha(N))`."

Mention at least one variant in each Examine · cost section. For Problem 1: Bellman-Ford (when negative weights), Floyd-Warshall (all-pairs). For Problem 2: BFS-based cycle-detection (correct but `O(V + E)` per query; DSU is better for streaming).

---

## Cross-references between the two write-ups

The pair must be navigable. At minimum:

- The Problem 1 write-up cites the Problem 2 write-up in the Examine · cost section: "Compare to the DSU write-up — both algorithms are near-linear in the input size, but Dijkstra *processes* a graph (relaxes edges until convergence), whereas DSU *maintains* a graph (answers `find` / `union` queries online). The algorithmic registers are complementary, not interchangeable."
- The Problem 2 write-up cites the Problem 1 write-up in the Research constraints section: "Unlike the Dijkstra problem, this is a structural / topological question about the graph — there are no edge weights and no source vertex. The right tool is a data structure (DSU), not an algorithm (Dijkstra)."

The cross-references are a small detail but they earn senior signal — they show you can navigate the *taxonomy* of graph algorithms, not just the individual templates.

---

## Starter files

Two starters are provided. Implement against them in your portfolio (not in this repo); the starters here are the spec, not the deliverable.

### Problem 1 starter

See [`problem-01-dijkstra-starter.py`](./problem-01-dijkstra-starter.py). The starter has the function signature, the `defaultdict` and `heapq` imports, the test harness, and the docstring spec. Fill in the heap-Dijkstra body.

### Problem 2 starter

See [`problem-02-dsu-starter.py`](./problem-02-dsu-starter.py). The starter has the `UnionFind` class skeleton, the `find_redundant_connection` function stub, the test harness, and the docstring spec. Fill in `find`, `union`, and `find_redundant_connection`.

---

## Rubric

Each write-up is graded on the 30-second memo plus the five FRAME sections, with Examine split into verify and cost. Total possible: 100 points; passing: 70.

### Problem 1 (heap-Dijkstra) rubric

| Dimension | Points | What "full credit" looks like |
|-----------|-------:|----------------------|
| 30-second memo at the top | 10 | All five lines present; the non-negative-weights discriminator is stated |
| Frame | 10 | Two examples walked; the reachability check producing the `-1` return is stated |
| Research constraints | 20 | Dijkstra pattern named; heap-based form justified; BFS and Bellman-Ford rejected with reasons |
| Assess options | 10 | Steps numbered; data structure choice (`heapq` + `defaultdict`) stated; lazy-delete guard explained |
| Make the solution | 25 | All test cases pass; type hints on every function; PEP 8; idiomatic Python |
| Examine · verify | 10 | One positive trace + one edge case; both walked |
| Examine · cost | 15 | `O((V + E) log V)` derived; trade vs Bellman-Ford and Floyd-Warshall stated; one variant mentioned |

### Problem 2 (DSU) rubric

| Dimension | Points | What "full credit" looks like |
|-----------|-------:|----------------------|
| 30-second memo at the top | 10 | All five lines present; the optimizations (path compression + union by rank) are named |
| Frame | 10 | Two examples walked; the LC 684 spec detail (last redundant edge in input) is addressed |
| Research constraints | 20 | DSU pattern named; cycle-detection sub-shape identified; BFS-based alternative rejected |
| Assess options | 10 | UnionFind class outlined; iteration over edges; the `union` return value as the signal |
| Make the solution | 25 | All test cases pass; path compression and union by rank implemented correctly; type hints |
| Examine · verify | 15 | One positive trace + one trace where the redundant edge is detected on the first cycle-closing union |
| Examine · cost | 10 | `O(N alpha(N))` derived; the `alpha(N) <= 4` defense; BFS variant named |

### Cross-reference rubric

| Dimension | Points | What "full credit" looks like |
|-----------|-------:|----------------------|
| Problem 1 cites Problem 2 in Examine · cost | 5 | Sentence comparing Dijkstra's processing register to DSU's maintenance register |
| Problem 2 cites Problem 1 in Research constraints | 5 | Sentence rejecting Dijkstra ("no edge weights, no source; the right tool is a data structure") |

Sum: 100 (Problem 1) + 100 (Problem 2) + 10 (cross-refs) = 210 / 2 = **105 average**.

A passing write-up scores at least 70 on each.

---

## Acceptance

The mini-project is complete when:

- Both write-ups are committed under `frame-writeups/c2-week-10/mini-project/`.
- Both have the 30-second memo at the top.
- The cross-references in both directions are present.
- Both have recordings of at least 10 minutes each.
- The implementations pass the test cases in the starters.

Push everything by Sunday end-of-day. Phase 2's sixth week is closed on the push.

---

## Self-reflection (in the mini-project README)

End the README.md for `frame-writeups/c2-week-10/mini-project/README.md` with a short reflection — 4-6 sentences — addressing:

1. Which template (Dijkstra or DSU) felt more natural? Why?
2. What was the hardest part of the lazy-delete guard or path compression to articulate aloud?
3. What is the one thing you want to drill before Mock #2?

The reflection is the portfolio-grade artifact. Future you will thank present you for writing it.

---

## After the mini-project

Move on to [Week 11 — Dynamic Programming Foundations](../../week-11-dp-foundations/). The Dijkstra and DSU intuition stay with you through the rest of Phase 2; you will use them again in the W12 retrospective and (for the systems-team interviews) in Mock #3.
