# Mini-Project — DFS + Topological Sort, Fully UMPIRE-Narrated

> The week's deliverable: two compact portfolio artifacts that demonstrate fluency across DFS connectivity / cycle detection and topological sort, with full UMPIRE narration end-to-end. The pair is the discriminating element — Mock #2 grades both templates separately, and shipping one of each forces you to articulate the structural differences out loud.

**Estimated time:** 10 hours, split across Thursday-Saturday.

This mini-project is *narration-heavy* rather than *content-heavy*. You will produce two UMPIRE write-ups, each fully delivered in all six sections, each anchored by a 30-second pattern-recognition memo at the top. The two write-ups must be navigable as a pair — cross-references between them are part of the rubric.

---

## Why this matters

Three reasons.

1. **Phase 2 is graded on Match.** Phase 1 spent four weeks installing the UMPIRE habit; the Implement step was the primary work. Phase 2 patterns are heavier and the Match step matters more — recognition cost is no longer "30 seconds to name the pattern" but "60 seconds to name the algorithm choice (recursive DFS vs iterative DFS vs Kahn vs three-color), defend the visited-set or in-degree invariant, and reject one wrong alternative." This mini-project is the second in C2 to grade two parallel write-ups as a *pair* (the first was Week 6's BFS pair).

2. **DFS and topological sort are the two structural shapes of every directed-graph interview.** Every directed-graph problem you will ever see in an interview is one of them — or a composition of both (e.g., Find Eventual Safe States). The pair forces you to articulate the differences: where does the visited set come from, what does the post-order do, what does the in-degree array buy you. After two write-ups side-by-side, the disambiguation is reflexive.

3. **The full UMPIRE narration is the rubric.** Drills are graded on Match + Implement; the mini-project adds Plan, Review, Evaluate, *and* cross-references. By Sunday you should be able to produce a full UMPIRE narration on a DFS or topo problem in 20-25 minutes, recorded, without rehearsal.

---

## What you ship

Three files: two problem write-ups plus a short overview.

```
umpire-writeups/c2-week-07/mini-project/
├── README.md                                              ← short overview + index + reflection
├── problem-01-dfs-pacific-atlantic-water-flow.md          ← DFS, multi-source-from-boundaries, grid
└── problem-02-topo-course-schedule-iv.md                  ← topological sort + transitive closure
```

Each write-up is the full UMPIRE format from Week 1, **plus a leading 30-second pattern-recognition memo at the top**.

The two problems are chosen so that:

- **Problem 1 (DFS):** the algorithm is recursive grid-DFS seeded from the *boundaries inward*; the answer is a set of cells. This forces you to write the "multi-source from a derived set of sources" DFS idiom — a subtle variation that catches candidates who only practice "single-source DFS from `(0, 0)`."
- **Problem 2 (Topological sort):** the algorithm is Kahn's algorithm plus a transitive-closure follow-up. The Match move is recognizing that "is A a prerequisite of B?" is asking for the *transitive closure* of the DAG, which a topo-sort-plus-DP can answer in `O(V × (V + E))`.

The two problems together cover every Week-7 idiom: recursive DFS, multi-source DFS-from-boundaries (a non-trivial Match recognition), Kahn's topological sort, transitive closure, cycle detection on the input edge set. After this pair, the recognition for any DFS / topo problem should reduce to: *which of these idioms applies?*

---

## The 30-second pattern-recognition memo (the signature element)

At the top of each write-up, immediately after the title, place a single bordered block.

### For Problem 1 (DFS)

```markdown
> **30-second pattern-recognition memo (DFS):**
> This is a DFS problem because [connectivity / cycle / any-path signal].
> Sub-shape: [recursive / iterative / three-color].
> Seed: [single-source / multi-source from <set>].
> Visited: [set of <node IDs>].
> Invariant: [the visited-set discipline / parent pointer / three-color invariant].
> Why not BFS: [one sentence].
```

Six lines. Read aloud, ~25 seconds.

### For Problem 2 (Topological Sort)

```markdown
> **30-second pattern-recognition memo (topological sort):**
> This is a topological-sort problem because [valid sequence / prerequisites / build order signal].
> Algorithm choice: [Kahn / DFS post-order]; reason: [iterative-safety / SCCs available / etc.].
> Edge model: [direct from input / derived; the construction is …].
> Cycle handling: [`len(order) != V` return `[]` / three-color back-edge abort].
> Why not single-source DFS: [one sentence].
```

Six lines. Read aloud, ~25 seconds.

Example for Problem 1 (Pacific Atlantic Water Flow):

> **30-second pattern-recognition memo (DFS):**
> This is a DFS problem because we need the set of cells from which water can reach *both* the Pacific and Atlantic boundaries.
> Sub-shape: **recursive grid-DFS**, run twice — once from Pacific boundary cells, once from Atlantic.
> Seed: **multi-source** — every cell on the relevant boundary is a source.
> Visited: two `set[(int, int)]` — `pac_visited` and `atl_visited`.
> Invariant: visited-set discipline; mark on entry; recurse into uphill (`>=`) neighbors.
> Why not BFS: same asymptotic; recursive grid-DFS is shorter, no level tracking required.

Example for Problem 2 (Course Schedule IV):

> **30-second pattern-recognition memo (topological sort):**
> This is a topological-sort problem because the prerequisite check `is_prereq(a, b)` is the transitive closure of the DAG.
> Algorithm choice: **Kahn** + DP on the topological order; reason: iterative, no recursion-limit risk; `V <= 100` so `O(V × (V + E))` is fine.
> Edge model: directly from `prerequisites` input — `[a, b]` is edge `a → b`.
> Cycle handling: the problem guarantees DAG; defensively check `len(order) == V`.
> Why not single-source DFS per query: `O(Q × (V + E))` for Q queries is slower than precomputing the transitive closure once.

Two write-ups, two memos. By the second, the cadence is automatic.

---

## Per-problem rubric

Each write-up's grade comes from five axes:

| Axis | Weight | "Great" looks like |
|------|------:|--------------------|
| 30-second memo at the top | 25% | Six lines, all required elements named, hits cadence on read-aloud (≤30s) |
| Match section (expanded body) | 25% | Explicit comparison against the *other* template; one-paragraph "why this algorithm and not the other"; rejection of one wrong pattern (BFS, Dijkstra, brute force) |
| Plan + Implement | 20% | Clean code; the canonical template visible; the `neighbors_fn` or `in_degree` setup is a single named function or block |
| Review | 15% | Trace on at least two examples; one common bug called out and avoided |
| Evaluate (five-piece from W2) | 15% | Time / space / best-avg-worst / tradeoff / improvement, with the `O(V + E)` defense sentence and explicit rejection of one alternative |

A grade of "great" on both write-ups is the bar. The cross-references between Problems 1 and 2 are graded separately as the navigation rubric — see below.

---

## The two problems

### Problem 1 — Pacific Atlantic Water Flow (LeetCode 417) — DFS

**Spec.** You are given an `m × n` integer matrix `heights` representing the heights of cells. The Pacific Ocean touches the top and left edges of the matrix; the Atlantic Ocean touches the bottom and right edges. Water can flow from a cell to a neighboring (4-directional) cell with height *less than or equal to* the current cell.

Return a list of cells `[r, c]` from which water can reach *both* oceans.

**Examples:**

- Input:
  ```
  heights = [[1,2,2,3,5],
             [3,2,3,4,4],
             [2,4,5,3,1],
             [6,7,1,4,5],
             [5,1,1,2,4]]
  ```
  Output: `[[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]` (in any order).

- Input: `heights = [[1]]` → `[[0, 0]]` (the single cell touches every boundary).

**Why included.** The canonical "reverse the question" DFS problem with a multi-source seed from boundaries. Forces you to write:

1. The multi-source DFS seed (walk the boundary, enqueue every boundary cell).
2. The grid-DFS neighbor function (4 directions, bounds check, *uphill* check — `heights[nr][nc] >= heights[r][c]`).
3. The set intersection (cells in both `pac_visited` and `atl_visited`).

The senior insight is that *running DFS from each source cell and asking "can it reach an ocean?"* would be `O((R × C)²)`; instead, we **reverse the question**: from each ocean's boundary, run DFS over cells that can flow *into* the ocean (which means walking uphill in the original problem). The intersection of the two reachable sets is the answer. `O(R × C)`.

### Full UMPIRE narration for Problem 1

**[U — Understand]** (write 2-3 paragraphs)

Restate the problem in your own words. Confirm:

- Water flows from a cell to a neighbor with height *less than or equal to* the current cell.
- The Pacific touches the top and left edges; the Atlantic touches the bottom and right edges.
- The answer is the set of cells from which water can reach *both* oceans.
- 4-directional moves.

Walk an example by hand. For the 5×5 example, trace cell `(2, 2)` (height 5): can it reach the Pacific? It can flow to `(2, 1)` (height 4), then to `(1, 1)` (height 2), then to `(0, 1)` (height 2) — done, Pacific. Can it reach the Atlantic? It can flow to `(2, 3)` (height 3), then to `(2, 4)` (height 1) — done, Atlantic. So `(2, 2)` is in the answer.

**[M — Match]** (write 3-4 paragraphs)

Multi-source grid-DFS from boundaries inward. Restate the memo elements:

- Sub-shape: grid-DFS. Nodes are `(r, c)`; edges are 4-directional moves.
- Seed: multi-source from every Pacific boundary cell, then a second DFS from every Atlantic boundary cell.
- Visited: two separate `set[(int, int)]` — `pac_visited` and `atl_visited`.
- Why the *reversed* question: walking *outward* from each source cell and checking ocean-reachability is `O((R × C)²)`. Walking *inward* from the boundary is `O(R × C)` — each cell is visited at most twice (once per ocean).
- Why not BFS: same asymptotic; DFS is shorter and recursion-limit risk is bounded by `R + C ≤ 400` (well below 1000).
- Why not Dijkstra: edges are unit-cost.

Compare against Problem 2 (topological sort). The structural parallel: both use a graph-traversal template; the differences are (a) the input shape (grid vs adjacency list), (b) the algorithm (DFS-multi-source vs Kahn-with-DP), (c) the answer extraction (set intersection vs transitive-closure lookup). Naming this parallel out loud is the senior signal.

**[P — Plan]** (write the algorithm in 4-6 bullets, no code yet)

1. Walk the boundary; seed `pac_starts = {boundary cells touching Pacific}` and `atl_starts = {boundary cells touching Atlantic}`.
2. Run DFS from every cell in `pac_starts`, marking reachable cells in `pac_visited`. Neighbor predicate: `heights[nr][nc] >= heights[r][c]` (uphill).
3. Run DFS from every cell in `atl_starts`, marking reachable cells in `atl_visited`.
4. Return the intersection of the two sets as a list of `[r, c]` pairs.

Edge cases: 1×1 grid (the cell touches every boundary); rectangular grid (m != n).

**[I — Implement]** (code with brief narration)

```python
from typing import List


def pacific_atlantic(heights: List[List[int]]) -> List[List[int]]:
    """Return cells from which water can reach both Pacific and Atlantic."""
    if not heights or not heights[0]:
        return []
    m, n = len(heights), len(heights[0])
    pac: set[tuple[int, int]] = set()
    atl: set[tuple[int, int]] = set()
    DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def dfs(r: int, c: int, visited: set[tuple[int, int]]) -> None:
        visited.add((r, c))
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < m
                and 0 <= nc < n
                and (nr, nc) not in visited
                and heights[nr][nc] >= heights[r][c]
            ):
                dfs(nr, nc, visited)

    for c in range(n):
        dfs(0, c, pac)
        dfs(m - 1, c, atl)
    for r in range(m):
        dfs(r, 0, pac)
        dfs(r, n - 1, atl)
    return [[r, c] for (r, c) in pac & atl]
```

The seed loops are the boundary scan (lines 14-18). The DFS neighbor predicate `heights[nr][nc] >= heights[r][c]` encodes "walk uphill from the ocean inward" — the *reversed* question. The answer is the set intersection on line 19.

**[R — Review]** (trace at least two examples)

Trace 1 — the 5×5 example. Pacific seeds: `(0, 0..4), (1..4, 0)` → 9 cells. DFS from `(0, 0)` height 1: neighbor `(0, 1)` height 2 (uphill, in) → mark; etc. After all Pacific DFS calls, `pac` contains every cell reachable from a Pacific-boundary cell when walking uphill. Atlantic similarly. The intersection contains exactly the cells that drain into both oceans.

Trace 2 — `[[1]]`. The 1×1 grid. Pacific seed: `(0, 0)`. DFS from `(0, 0)` marks `(0, 0)`. Atlantic seed: `(0, 0)`. Same. Intersection: `{(0, 0)}`. Return `[[0, 0]]`. ✓

Common bug avoided: using a single visited set for both oceans. That would mark cells visited-by-Pacific as also visited-by-Atlantic and the intersection would be empty. Two separate sets are mandatory.

**[E — Evaluate]** (the five-piece)

- **Time**: `O(m × n)`. Each cell is entered at most twice (once per ocean's DFS); each entry examines 4 neighbors in `O(1)`. Total `O(m × n)`.
- **Space**: `O(m × n)` for the two visited sets; recursion stack up to `O(m × n)` in the pathological case.
- **Best**: `O(m × n)` — mandatory grid scan.
- **Worst**: `O(m × n)`.
- **Tradeoff**: brute-force "for each cell, DFS outward and check if it reaches both oceans" is `O((m × n)²)` — wildly worse. The "reverse the question" insight is what reduces the complexity by a factor of `m × n`.
- **Improvement**: none asymptotically. Possible constant-factor: BFS instead of DFS to bound recursion depth, but `m × n ≤ 40000` and depth is well below the recursion limit.

Defense sentence:

> "`O(m × n) time, O(m × n) space`. The senior insight is **reversing the question** — instead of asking 'from this cell, can water reach the ocean?' (`O((m × n)²)`), we ask 'from the ocean boundary, walking uphill, which cells are reachable?' (`O(m × n)`). The set intersection of the two ocean-reachable sets is the answer. The two-visited-sets discipline is the implementation invariant that makes the intersection well-defined."

### Problem 2 — Course Schedule IV (LeetCode 1462) — TOPOLOGICAL SORT

**Spec.** You are given `numCourses` courses labeled `0..numCourses-1` and a list of `prerequisites` where `[a, b]` means "course `a` must be taken before course `b`." (Note: this is the *reverse* of LC 207/210's convention.) You are also given a list of `queries` where `[u, v]` asks "is course `u` a prerequisite (direct or indirect) of course `v`?"

The graph is guaranteed to be a DAG. Return a list of booleans, one per query.

Per the spec: `2 <= numCourses <= 100`; `0 <= queries.length <= 10⁴`.

**Examples:**

- `numCourses = 2`, `prerequisites = [[1, 0]]` (course 1 before course 0), `queries = [[0, 1], [1, 0]]` → `[False, True]`.
- `numCourses = 3`, `prerequisites = [[1, 2], [1, 0], [2, 0]]`, `queries = [[1, 0], [1, 2]]` → `[True, True]`.

**Why included.** The canonical "topological sort + transitive closure" problem. The Match move is recognizing that "is `u` a prerequisite (direct or indirect) of `v`?" is the *transitive closure* question, which can be answered in `O(V × (V + E))` after a topological sort. The alternative — running DFS from each query's `u` — is `O(Q × (V + E))` = `O(10⁴ × 10⁴) = 10⁸`, marginal. The topo-sort approach is `O(V × (V + E) + Q)` = `O(100 × 10⁴ + 10⁴) = 10⁶` — fast.

The senior signal: recognize that *precomputing reachability* once is asymptotically better than answering each query independently when `Q >> V`.

### Full UMPIRE narration for Problem 2

(Use the same UMPIRE-section structure as Problem 1. Below is the abbreviated version; full write-up should match Problem 1's section depth.)

**[U]** Restate. `[a, b]` means "a before b" (note the convention reversal from LC 210). Queries ask transitive reachability. The graph is a DAG by spec. Walk an example: with prerequisites `[[1,2],[1,0],[2,0]]`, course 1 is a prerequisite of 2 (direct), 1 is a prerequisite of 0 (direct and via 2), 2 is a prerequisite of 0 (direct). So `(1, 0)` is `True`, `(1, 2)` is `True`.

**[M]** Topological sort + transitive closure. Algorithm choice: **Kahn** for the topo sort (iterative, no recursion-limit risk; `V <= 100` so either works); then a DP pass in topological order to compute `reachable[u]: set[int]` for each `u`. The DP: `reachable[u] = {u's direct successors} ∪ {reachable[v] for each direct successor v}`. Process in topological order so that `reachable[v]` is already known when we compute `reachable[u]` for `u` before `v` — wait, we need the *reverse* topological order: when we compute `reachable[u]`, all of `u`'s direct successors must already have their `reachable` sets computed. Reverse topological order satisfies this. Alternative: use the forward topological order but accumulate in the opposite direction; this is symmetric. Compare against Problem 1: same graph-traversal-then-aggregate shape; the differences are (a) the input shape (prerequisite list vs grid heights), (b) the aggregation (set union from descendants vs set intersection of two reachable sets), (c) the algorithm choice (Kahn vs grid-DFS). The structural parallel: both precompute a global structure that turns query work from `O(query_count × V)` into `O(1)` per query.

**[P]** Four bullets:

1. Build the adjacency list `adj` and `in_degree` array.
2. Run Kahn's algorithm to produce a topological order.
3. Walk the topological order in *reverse*; for each `u`, compute `reachable[u] = {direct successors} ∪ {reachable[v] for v in direct successors}`.
4. For each query `[u, v]`, return `v in reachable[u]`.

**[I]**

```python
from collections import defaultdict, deque
from typing import List


def check_if_prerequisite(num_courses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
    """Return per-query whether u is a transitive prerequisite of v."""
    adj: dict[int, list[int]] = defaultdict(list)
    in_degree: List[int] = [0] * num_courses
    for a, b in prerequisites:
        adj[a].append(b)
        in_degree[b] += 1
    # Kahn's topological sort.
    queue: deque[int] = deque(c for c in range(num_courses) if in_degree[c] == 0)
    topo: List[int] = []
    while queue:
        u = queue.popleft()
        topo.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    # DP: reachable[u] computed in reverse topological order.
    reachable: dict[int, set[int]] = {u: set() for u in range(num_courses)}
    for u in reversed(topo):
        for v in adj[u]:
            reachable[u].add(v)
            reachable[u].update(reachable[v])
    return [v in reachable[u] for u, v in queries]
```

The Kahn loop is lines 8-15. The DP pass is lines 17-20 — `reversed(topo)` ensures every `v` has `reachable[v]` computed by the time we look it up. The query answers are read off `reachable` in line 21.

**[R]** Trace on `numCourses=3, prereqs=[[1,2],[1,0],[2,0]]`.

- adj: `{1: [2, 0], 2: [0]}` (course 1 precedes 2 and 0; course 2 precedes 0).
- in_degree: `[2, 0, 1]` (course 0 has two prereqs; course 1 has none; course 2 has one).
- Kahn: start with course 1; topo=[1]. Process: decrement in_degree[2]→0, queue 2; decrement in_degree[0]→1. Pop 2; topo=[1, 2]. Decrement in_degree[0]→0, queue 0. Pop 0; topo=[1, 2, 0]. Done.
- DP in reverse(topo) = [0, 2, 1]:
  - u=0: adj[0]=[]. reachable[0]={}.
  - u=2: adj[2]=[0]. reachable[2]={0} ∪ reachable[0]={0} = {0}.
  - u=1: adj[1]=[2, 0]. reachable[1]={2, 0} ∪ reachable[2]={0} ∪ reachable[0]={} = {0, 2}.
- Query (1, 0): 0 in reachable[1]={0, 2} → True. ✓
- Query (1, 2): 2 in reachable[1]={0, 2} → True. ✓

Trace 2: trivial case — `numCourses=2, prereqs=[]`, queries `[(0, 1)]`. adj is empty; topo=[0, 1] or [1, 0]. reachable[0]={} and reachable[1]={}. Query: 1 in {} → False. ✓

**[E]** **Time `O(V × (V + E) + Q)`**: Kahn is `O(V + E)`; the DP pass visits each edge once but the *union* operation `reachable[u].update(reachable[v])` is `O(|reachable[v]|)` per union, summing to `O(V)` per node and `O(V²)` total. Adding edges: `O(E)`. Total `O(V × V + E + Q) = O(V² + E + Q)`. **Space `O(V² + E)`** for the reachable map. Tradeoff vs per-query DFS: `O(Q × (V + E))`; if `Q >> V`, the precomputed transitive closure wins. Best `O(V + E + Q)` (DAG with few edges and shallow depth); worst `O(V² + Q)`.

---

## Cross-references rubric

The two write-ups are graded as a *pair*. At the bottom of each write-up, include a "Cross-references" section that points to:

- The relevant lecture section (Problem 1 → Lecture 1 §6 on tree-DFS / grid-DFS; Problem 2 → Lecture 3 §4 on Kahn's).
- The relevant exercise (Problem 1 → Exercise 1 on recursive DFS; Problem 2 → Exercise 3 on Kahn).
- The *other* mini-project problem. Specifically, the cross-reference text should be a 1-2 sentence comparison: "*Problem 2 uses Kahn's algorithm for topological sort, then a DP pass in reverse-topological order to compute reachability; the structural parallel with Problem 1 is the 'precompute a global structure once, then answer many queries in O(1)' pattern — Problem 1 precomputes the two ocean-reachable sets via DFS; Problem 2 precomputes the transitive closure via Kahn + DP.*"

The cross-references are what make the pair navigable as a portfolio artifact. A reviewer (or interviewer) should be able to read Problem 1, click through to Problem 2, and immediately see the structural relationship.

---

## File-level template

Each problem write-up follows this skeleton. Save as `problem-NN-<slug>.md`.

```markdown
# Problem NN — <name> (<LC reference>)

> **30-second pattern-recognition memo [DFS / topological sort]:**
> [six lines as above]

## Problem

[Spec + 2-3 examples.]

## Why this template

[1 paragraph: what makes this template distinct from the other; one sentence comparing against the other mini-project problem.]

## UMPIRE write-up

### Understand
### Match
[Expanded body — comparison against the other template, rejection of one wrong pattern.]
### Plan
### Implement
[Code with brief inline narration.]
### Review
[Trace on 2 examples + 1 common bug avoided.]
### Evaluate
[5-piece from W2, with the time-defense sentence cleanly delivered.]

## Cross-references

- Lecture: [link to relevant section]
- Exercise: [link to relevant exercise]
- Sister mini-project problem: [link with 1-2 sentence comparison]

## What I would do differently next time

[Optional but recommended: 1-2 sentences.]
```

---

## Acceptance criteria

- [ ] Both write-ups present in `umpire-writeups/c2-week-07/mini-project/`.
- [ ] Each write-up has a leading 30-second memo following the schema above.
- [ ] **Problem 1 uses the DFS memo schema; Problem 2 uses the topological-sort memo schema.**
- [ ] Each write-up has all six UMPIRE sections fully written out (no "see exercise" placeholders).
- [ ] Each write-up has a trace on at least two examples in the Review section.
- [ ] Each write-up has a Cross-references section linking to the other mini-project problem with a 1-2 sentence comparison.
- [ ] Both `.py` solution files are present and pass their respective test cases.

---

## Suggested order of operations

### Thursday — drafting (1.5h)

1. Open the mini-project folder. Create three empty files (the two problem write-ups + this README).
2. For each problem, write only the **30-second memo** at the top. Do not write the rest yet. Read each memo aloud; sharpen until it hits 25-30 seconds.
3. Commit "Mini-project memos drafted."

### Friday — Problem 1 (3h)

4. Write up Problem 1 in full UMPIRE. Allow 3 hours — the in-depth Understand and Match are the time-consuming parts. The "reverse the question" Match move is the senior signal; spend the time getting that paragraph right.
5. Trace at least two examples in Review.
6. Code + commit.

### Saturday — Problem 2 (3h)

7. Write up Problem 2 in full UMPIRE. Cross-reference back to Problem 1 in the Match section ("precompute once, query many" — the structural parallel).
8. Trace at least two examples in Review.
9. Code + commit.

### Sunday — polish + push (0.5h)

10. Add cross-references at the bottom of each write-up.
11. Re-read both memos aloud one last time; sharpen anything that runs over 30 seconds.
12. Score yourself against the per-problem rubric. If anything is "vague" or "missing the boundary defense," sharpen it.
13. Push.

---

## What "great" looks like (final rubric)

A learner who has shipped this mini-project *well* has:

- Both memos under 30 seconds when read aloud.
- Match sections that explicitly compare the two templates (DFS vs Kahn, recursive vs iterative).
- Implement sections with the `neighbors_fn` (Problem 1) or `in_degree` initialization (Problem 2) clearly visible as a named function or labeled block.
- Cross-references at the bottom of each write-up linking to the other.
- Recordings ≥ 20 minutes each, with the full UMPIRE narration.

A learner who has shipped this mini-project *poorly* has:

- Memos that run 60+ seconds — too verbose, missing the cadence.
- Match sections that name "DFS" but do not specify the sub-shape or invariant.
- Implement sections without a clearly extracted `neighbors_fn` or `in_degree` setup.
- No cross-references; each write-up reads as a stand-alone with no awareness of the other.

If you catch yourself producing the "poorly" shape, the fix is to re-read [Lecture 1 §8](../lecture-notes/01-recursive-dfs.md) (the 30-second recognition signals) and [Lecture 3 §8](../lecture-notes/03-topological-sort.md) (the topo decision tree) and re-do whichever write-up is weaker.

---

## Why one of each specifically

Two reasons.

1. **One DFS + one topo is the diet of a real directed-graph interview.** Phase 2 onsites typically ask one DFS or topological-sort problem; that problem is either a "connectivity / any-path" (50% of the time) or a "topological order / cycle detection" (50% of the time). Shipping one of each guarantees you have practiced the at-bat for whichever you draw.

2. **The syllabus mandates exactly this composition.** From the Week 7 line in `SYLLABUS.md`: *"Mini-project: A DFS problem (e.g., connectivity, reachability, or grid-DFS) and a topological-sort problem (course schedule / build-order family). Both UMPIRE-narrated."* The composition is the contract.

If you finish before Sunday with energy to spare, add a third write-up from the LeetCode Topological Sort tag at your discretion — for example, "Parallel Courses" (LC 1136) is a great stretch because the senior insight is that **the number of semesters is the *depth* of the DAG**, computed naturally by Kahn's algorithm with a level counter. The acceptance criterion is *two* — anything beyond is bonus.

---

When done: push everything, then move on to [Week 8 — Backtracking](../../week-08/).

Phase 2's third week is closed. Your portfolio now contains two canonical DFS / topological-sort write-ups; that section will be referenced again in Mock #2 (Week 9) and in the capstone (Week 15).
