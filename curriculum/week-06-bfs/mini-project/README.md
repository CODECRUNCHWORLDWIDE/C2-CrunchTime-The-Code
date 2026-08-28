# Mini-Project — Grid BFS + Node BFS, Fully FRAME-Narrated

> The week's deliverable: two compact portfolio artifacts that demonstrate fluency across the two BFS sub-shapes, with full FRAME narration end-to-end. The pair is the discriminating element — interviewers grade Research constraints on sub-shape recognition harder than candidates expect, and shipping one of each forces you to articulate the structural differences out loud.

**Estimated time:** 10 hours, split across Thursday-Saturday.

This mini-project is *narration-heavy* rather than *content-heavy*. You will produce two FRAME write-ups, each fully delivered in all five sections, each anchored by a 30-second pattern-recognition memo at the top. The two write-ups must be navigable as a pair — cross-references between them are part of the rubric.

---

## Why this matters

Three reasons.

1. **Phase 2 is graded on Research constraints.** Phase 1 spent four weeks installing the FRAME habit; the Make step was the primary work. Phase 2 patterns are heavier and the Research constraints step matters more — recognition cost is no longer "30 seconds to name the pattern" but "60 seconds to name the sub-shape, defend the seed (single vs multi), and name the distance-tracking idiom." This mini-project is the first in C2 to grade two parallel write-ups as a *pair*.

2. **Grid and node are the two structural shapes of every BFS interview.** Every BFS problem you will ever see in an interview is one of the two. The pair forces you to articulate the differences: where does the neighbor function come from, what does the visited set store, what is the input size in big-O? After two write-ups side-by-side, the disambiguation is reflexive.

3. **The full FRAME narration is the rubric.** Drills are graded on Research constraints + Make the solution; the mini-project adds Assess options, Examine (verify), Examine (cost), *and* cross-references. By Sunday you should be able to produce a full FRAME narration on a BFS problem in 20-25 minutes, recorded, without rehearsal.

---

## What you ship

Three files: two problem write-ups plus a short overview.

```
frame-writeups/c2-week-06/mini-project/
├── README.md                                  ← short overview + index + reflection
├── problem-01-grid-bfs-walls-and-gates.md     ← grid-BFS, multi-source, distance map
└── problem-02-node-bfs-open-the-lock.md       ← node-BFS, single-source, level tracking
```

Each write-up is the full FRAME format from Week 1, **plus a leading 30-second pattern-recognition memo at the top**.

The two problems are chosen so that:

- **Problem 1 (grid-BFS):** the seed is multi-source; the answer is a per-cell distance map. This forces you to write the multi-source idiom explicitly.
- **Problem 2 (node-BFS):** the seed is single-source; the graph is implicit; the answer is a level count. This forces you to write a non-trivial `neighbors_fn`.

The two problems together cover every Week 6 idiom: single-source, multi-source, grid sub-shape, node sub-shape, per-node distance, level tracking, implicit graph, explicit visited handling. After this pair, the recognition for any BFS problem should reduce to: *which of these four idioms applies?*

---

## The 30-second pattern-recognition memo (the signature element)

At the top of each write-up, immediately after the title, place a single bordered block.

### For Problem 1 (grid-BFS)

```markdown
> **30-second pattern-recognition memo (grid-BFS):**
> This is a BFS problem because [shortest-distance / minimum-moves signal].
> Sub-shape: **grid-BFS** — nodes are `(r, c)` cells; edges are [4 / 8]-directional.
> Seed: [single-source / multi-source from <set>].
> Distance idiom: [per-node distance / level tracking].
> Visited: [set of (r, c) tuples / mutated grid].
> Why not [alternative — DFS, Dijkstra, simulation]: [one sentence].
```

Six lines. Read aloud, ~25 seconds.

### For Problem 2 (node-BFS)

```markdown
> **30-second pattern-recognition memo (node-BFS):**
> This is a BFS problem because [shortest-distance / minimum-moves signal].
> Sub-shape: **node-BFS** — nodes are [strings / state tuples]; the neighbor function is [`neighbors(n) = ...`].
> Seed: [single-source / multi-source from <set>].
> Distance idiom: [per-node distance / level tracking].
> Visited: [set of node IDs].
> Why not [alternative — DFS, Dijkstra, recursion]: [one sentence].
```

Six lines. Read aloud, ~25 seconds.

Example for Problem 1 (Walls and Gates):

> **30-second pattern-recognition memo (grid-BFS):**
> This is a BFS problem because we want the minimum-distance from every empty cell to the nearest gate.
> Sub-shape: **grid-BFS** — nodes are `(r, c)` cells; edges are 4-directional.
> Seed: **multi-source** from every gate cell (`grid[r][c] == 0`).
> Distance idiom: **per-cell distance** — write the answer into the grid in place.
> Visited: implicit — cells with finite written distance are visited.
> Why not single-source per gate: that is `O(R × C × G)` for `G` gates; multi-source is `O(R × C)`.

Example for Problem 2 (Open the Lock):

> **30-second pattern-recognition memo (node-BFS):**
> This is a BFS problem because we want the minimum number of wheel rotations to reach the target.
> Sub-shape: **node-BFS** — nodes are 4-character strings; `neighbors('1234')` rotates each of the 4 digits up or down, giving 8 neighbors.
> Seed: **single-source** from `'0000'`.
> Distance idiom: **level tracking** — the answer is a level count.
> Visited: a `set[str]` containing initially-blocked `deadends` plus all nodes we reach.
> Why not DFS: DFS finds a path but not the shortest; the problem requires the minimum.

Two write-ups, two memos. By the second, the cadence is automatic.

---

## Per-problem rubric

Each write-up's grade comes from five axes:

| Axis | Weight | "Great" looks like |
|------|------:|--------------------|
| 30-second memo at the top | 25% | Six lines, all required elements named, hits cadence on read-aloud (≤30s) |
| Research constraints section (expanded body) | 25% | Explicit comparison against the *other* sub-shape; one-paragraph "why this sub-shape and not the other"; rejection of one wrong pattern (DFS, Dijkstra, simulation) |
| Assess options + Make the solution | 20% | Clean code; the canonical template visible; the `neighbors_fn` is a single named function or block |
| Examine · verify | 15% | Trace on at least two examples; one common bug called out and avoided |
| Examine · cost (five-piece from W2) | 15% | Time / space / best-avg-worst / tradeoff / improvement, with the `O(V + E)` defense sentence and explicit rejection of one alternative |

A grade of "great" on both write-ups is the bar. The cross-references between Problems 1 and 2 are graded separately as the navigation rubric — see below.

---

## The two problems

### Problem 1 — Walls and Gates (LeetCode 286) — GRID-BFS

**Spec.** You are given a 2-D grid of dimensions `m × n` representing rooms. Each cell has one of three values:

- `-1` — wall.
- `0` — gate.
- `INF` (use `2³¹ - 1 = 2147483647`) — empty room.

Fill in each empty room with the distance to its nearest gate. If a room cannot reach any gate, it stays `INF`.

The rules: 4-directional moves; walls block; the answer must be the *minimum* distance to any gate.

**Examples:**

- Input:
  ```
  [[INF,  -1,   0, INF],
   [INF, INF, INF,  -1],
   [INF,  -1, INF,  -1],
   [  0,  -1, INF, INF]]
  ```
  Output:
  ```
  [[3, -1, 0, 1],
   [2,  2, 1, -1],
   [1, -1, 2, -1],
   [0, -1, 3,  4]]
  ```

**Why included.** The canonical multi-source grid-BFS problem with a distance-map answer (not a single number). Forces you to write:

1. The multi-source seed (walk the grid, enqueue every gate).
2. The grid-BFS neighbor function (4 directions, bounds check, wall check, "is the target empty?" check).
3. The in-place answer write-back (set `grid[nr][nc] = grid[r][c] + 1` upon reaching).

The senior insight is that the *check for "this empty room is the new candidate"* doubles as the visited-set check. Specifically: `if grid[nr][nc] == INF, we have not visited it yet`. This avoids an explicit `visited` set and keeps memory at `O(W)` instead of `O(R × C)`.

### Full FRAME narration for Problem 1

**[F — Frame]** (write 2-3 paragraphs)

Restate the problem in your own words. Confirm:

- "INF" is represented as `2³¹ - 1`.
- Walls are `-1`, gates are `0`, empty rooms are `INF`.
- Moves are 4-directional.
- The answer is written back into the grid in place; no separate output structure.
- An empty room with no path to any gate stays `INF`.

Walk an example by hand. For the 4x4 above, trace `(0, 0)`: starts as INF; the nearest gate is `(0, 2)` via `(0, 1)`-wall — must route around. Shortest: `(0,0) → (1,0) → (1,1) → (1,2) → (0,2)` = 4 steps. Wait — actually `(0,0) → (1,0) → (2,0) → … hmm`. Or via `(0,0) → (1,0) → (1,1) → (1,2) → (0,2)`. The example output says `grid[0][0] = 3`, so the actual shortest is 3. Recount: `(0,0) → (1,0) → (1,1) → (1,2) → (0,2)` is 4 moves, not 3. Maybe `(0,0) → (1,0)` is move 1 from `(0,0)`-side, and from gate-side `(0,2) → (1,2) → (1,1) → (1,0)` is 3 moves to reach `(1,0)`, and `(0,0)` is one more. So `grid[0][0] = 3` after the gate at `(3, 0)` reaches via the left column: `(3, 0) → (2, 0)` — wait `(2, 0) = INF` and `(2, 1) = -1`. Hmm — actually `(3, 0)` is the gate. Let me check the grid again. `(0, 0)` to gate `(3, 0)`: via `(1, 0), (2, 0), (3, 0)` — but `(3, 0)` is the gate, so distance = 3. That matches. The example is correct.

This is the kind of careful Frame work that the rubric grades.

**[R — Research constraints]** (write 3-4 paragraphs)

Multi-source grid-BFS. Restate the memo elements:

- Sub-shape: grid-BFS. Nodes are `(r, c)`; edges are 4-directional moves to non-wall cells.
- Seed: multi-source from every gate.
- Distance idiom: in-place write-back (the grid is the answer; `INF` means unvisited).
- Visited: implicit (cells with finite values).
- Why not single-source from each gate: `O(R × C × G)` vs `O(R × C)`. Same algorithm; multi-source seed is the difference.
- Why not DFS: DFS does not guarantee shortest distance — it finds *a* path but not the minimum.
- Why not Dijkstra: edges are unit-cost; Dijkstra adds log-factor with no benefit.

Compare against Problem 2 (node-BFS). The structural parallel: both use the same BFS template; the differences are (a) the input shape (grid vs implicit string graph), (b) the neighbor function (4-direction offset vs digit-rotation), (c) the visited representation (grid mutation vs explicit set). Naming this parallel out loud is the senior signal.

**[A — Assess options]** (write the algorithm in 4-6 bullets, no code yet)

1. Walk the `m × n` grid; for every cell with `grid[r][c] == 0`, push `(r, c)` onto the queue.
2. While the queue is non-empty: dequeue `(r, c)`.
3. For each of the four 4-directional neighbors `(nr, nc)`: if in bounds and `grid[nr][nc] == INF`, set `grid[nr][nc] = grid[r][c] + 1` and enqueue `(nr, nc)`.
4. After the loop, every reachable empty room has been written with its shortest distance; unreachable rooms stay `INF`.

Edge cases: empty grid (return immediately); no gates (return immediately); grid with only gates and walls (BFS terminates immediately).

**[M — Make the solution]** (code with brief narration)

```python
from collections import deque

INF = 2147483647

def walls_and_gates(rooms: list[list[int]]) -> None:
    """Modify rooms in place: fill each empty room with distance to nearest gate."""
    if not rooms or not rooms[0]:
        return
    m, n = len(rooms), len(rooms[0])
    queue = deque()
    for r in range(m):
        for c in range(n):
            if rooms[r][c] == 0:
                queue.append((r, c))
    DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        r, c = queue.popleft()
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and rooms[nr][nc] == INF:
                rooms[nr][nc] = rooms[r][c] + 1
                queue.append((nr, nc))
```

The seed loop is lines 8-11. The BFS loop is lines 13-19. The visited check is implicit: `rooms[nr][nc] == INF` means "not yet reached." The write-back on line 17 simultaneously marks visited and records distance.

**[E — Examine · verify]** (trace at least two examples)

Trace 1 — the 4x4 example. Seed: gates are `(0, 2)` and `(3, 0)`. Queue starts `[(0, 2), (3, 0)]`. Dequeue `(0, 2)`. Neighbors: `(-1, 2)` oob, `(1, 2) = INF` → write 1, enqueue; `(0, 1) = -1` wall; `(0, 3) = INF` → write 1, enqueue. Dequeue `(3, 0)`. Neighbors: `(2, 0) = INF` → write 1, enqueue; `(4, 0)` oob; `(3, -1)` oob; `(3, 1) = -1` wall. Continue BFS — every reachable empty room gets the minimum distance from the closer gate. After BFS, walk the grid: any remaining `INF` cells are unreachable.

Trace 2 — a grid with no gates. The seed loop finds no zeros; the queue starts empty; the loop never runs; the grid is unchanged.

Common bug avoided: using a separate `visited` set in addition to the in-place write-back. Doubles memory; not needed. The "is this cell INF?" check is the visited check.

**[E — Examine · cost]** (the five-piece)

- **Time**: `O(m × n)`. The seed loop is `O(m × n)`. The BFS visits each empty cell at most once; each visit is 4-neighbor enumeration in `O(1)`. Total `O(m × n)`.
- **Space**: `O(m × n)` for the queue worst case (the queue can hold up to one level, which is bounded by the grid size).
- **Best**: `O(m × n)` (the seed loop alone is mandatory).
- **Worst**: `O(m × n)`.
- **Tradeoff**: single-source BFS per gate is `O(m × n × g)` where `g` is the number of gates — strictly worse. Naive "for each empty room, BFS to the nearest gate" is `O((m × n)²)` — much worse. Multi-source BFS is the standard fast solution.
- **Improvement**: none asymptotically. One micro-optimization: skip enqueuing cells whose new distance equals the current (no-op write).

Defense sentence:

> "`O(m × n) time, O(m × n) space`. Multi-source BFS visits every cell exactly once; the seed is `O(m × n)` for one grid scan, and the BFS adds another `O(m × n)`. Tradeoff: single-source BFS per gate is `O(m × n × g)`; naive per-empty-cell is `O((m × n)²)`. Multi-source is strictly optimal for the 'distance to nearest source' family. The senior signal is that the *seed shape* (multi-source) is what bounds the complexity, not the BFS body."

### Problem 2 — Open the Lock (LeetCode 752) — NODE-BFS

**Spec.** (Same as Homework Problem 3.) A 4-wheel lock with digits `0-9` per wheel. Each wheel can rotate freely up or down (and wraps: `0 ↔ 9`). Given a list of `deadends` (forbidden states) and a `target`, return the minimum number of moves to reach the target from `'0000'`, or `-1` if impossible.

**Examples:**

- `deadends = ["0201","0101","0102","1212","2002"]`, `target = "0202"` → `6`.
- `deadends = ["8888"]`, `target = "0009"` → `1`.
- `deadends = ["8887","8889","8878","8898","8788","8988","7888","9888"]`, `target = "8888"` → `-1`.
- `deadends = ["0000"]`, `target = "8888"` → `-1`.

**Why included.** The canonical node-BFS problem on an implicit graph with non-trivial state. The 8-neighbor function (each of 4 digits up or down) is the cleanest interview-grade `neighbors_fn` you can write. Forces you to:

1. State that the graph is implicit and the nodes are 4-character strings.
2. Write the neighbor function: 4 positions × 2 directions = 8 neighbors per state.
3. Pre-load the visited set with `deadends` — a one-line technique that distinguishes a clean implementation from a bug-prone one.
4. Use level tracking because the answer is a level count.

### Full FRAME narration for Problem 2

(Use the same FRAME-section structure as Problem 1. Below is the abbreviated version; full write-up should match Problem 1's section depth.)

**[F]** Restate. Wheels rotate freely, including wraparound (`0` → `9`). Deadends are forbidden states the lock cannot pass through (treat as "already visited / blocked"). The answer is the minimum number of rotation moves; one move = one wheel rotates by one digit. Confirm the early-exit case: if `'0000'` itself is a deadend, return `-1`. Walk an example by hand at `target = "0202"`: each digit moves twice from `0`, but the rotations interleave around deadends. The answer is 6.

**[R]** Node-BFS on an implicit graph. Sub-shape: nodes are 4-character strings; edges connect states differing by one wheel rotation. Seed: single-source from `'0000'`. Distance idiom: level tracking (the answer is a count). Visited: a `set[str]` initialized with `deadends`. Why not DFS: shortest path requires BFS. Why not generating the whole 10⁴ state space: BFS lazily explores reachable states; the visited set bounds memory. Compare against Problem 1: same template, different sub-shape — Problem 1's `neighbors_fn` was a 4-direction offset on a grid; Problem 2's `neighbors_fn` is digit rotation on a string. The structural parallel: both compile to the same `O(V + E)` BFS shape with different `neighbors_fn`.

**[A]** Four bullets:

1. Pre-load `visited = set(deadends)`. If `'0000' in visited`, return `-1`.
2. If `target == '0000'`, return `0`.
3. BFS with level tracking. Queue `deque(['0000'])`. `level = 0`. Outer loop: snapshot `len(queue)`. Process that many. For each state, return `level` if state equals target. Else generate 8 neighbors, filter against visited, enqueue unvisited. Increment level.
4. Loop exits → return `-1`.

**[M]**

```python
from collections import deque

def open_lock(deadends: list[str], target: str) -> int:
    """Return min rotations from '0000' to target, or -1 if impossible."""
    visited = set(deadends)
    start = "0000"
    if start in visited:
        return -1
    if start == target:
        return 0
    queue = deque([start])
    visited.add(start)
    level = 0
    while queue:
        level += 1
        for _ in range(len(queue)):
            state = queue.popleft()
            for i in range(4):
                d = int(state[i])
                for delta in (-1, 1):
                    nd = (d + delta) % 10
                    new_state = state[:i] + str(nd) + state[i+1:]
                    if new_state == target:
                        return level
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append(new_state)
    return -1
```

The `neighbors_fn` is lines 16-20: four digit positions, two delta directions, modulo-10 wraparound. The visited handling on line 5 pre-loads deadends as a single line — a clean technique for "treat these as already visited." The level-tracking idiom is the outer `for _ in range(len(queue))` on line 14.

**[E · verify]** Trace on `deadends=["0201","0101","0102","1212","2002"]`, `target="0202"`. Visited starts with the 5 deadends. Queue=['0000']. Level 1: 8 neighbors of '0000'. Filter out deadends (e.g., `'1212'` not directly adjacent — actually neighbors of '0000' are `['9000', '1000', '0900', '0100', '0090', '0010', '0009', '0001']`). All 8 are non-deadend (note `'0101'` is two steps away, not one). Enqueue all. Level 2: 8 expansions per state, with duplicates dropped via visited. Continue until level 6 reaches `'0202'`. Return 6.

Trace on `deadends=["0000"]`: early exit, return `-1`. ✓

Trace on `target="0000"`: early return 0. ✓

**[E · cost]** **Time `O(N + D)`** where `N = 10⁴` is the state space and `D` is `len(deadends)`. BFS visits each state at most once; each visit generates 8 neighbors in `O(L)` where `L = 4` (string slicing). **Space `O(N)`** for the visited set. Tradeoff: DFS would not guarantee shortest. Naive simulation (try all rotation sequences up to length k) is exponential. Bidirectional BFS halves the visited set in the worst case — worth mentioning. Best `O(1)` (`'0000'` is target or deadend); worst `O(N)`.

---

## Cross-references rubric

The two write-ups are graded as a *pair*. At the bottom of each write-up, include a "Cross-references" section that points to:

- The relevant lecture section (Problem 1 → Lecture 2 §4 on multi-source; Problem 2 → Lecture 1 §6 and Lecture 2 §2 on node-BFS).
- The relevant drill (Problem 1 → Exercise 3 on multi-source; Problem 2 → Exercise 4 on node-BFS).
- The *other* mini-project problem. Specifically, the cross-reference text should be a 1-2 sentence comparison: "*Problem 2 uses the same BFS template as Problem 1, but the neighbor function is over digit-rotation on a 4-character string rather than 4-direction offsets on a grid; the level-tracking idiom replaces the in-place write-back because the answer is a count, not a distance map.*"

The cross-references are what make the pair navigable as a portfolio artifact. A reviewer (or interviewer) should be able to read Problem 1, click through to Problem 2, and immediately see the structural relationship.

---

## File-level template

Each problem write-up follows this skeleton. Save as `problem-NN-<slug>.md`.

```markdown
# Problem NN — <name> (<LC reference>)

> **30-second pattern-recognition memo [grid-BFS / node-BFS]:**
> [six lines as above]

## Problem

[Spec + 2-3 examples.]

## Why this sub-shape

[1 paragraph: what makes this sub-shape distinct from the other; one sentence comparing against the other mini-project problem.]

## FRAME write-up

### Frame
### Research constraints
[Expanded body — comparison against the other sub-shape, rejection of one wrong pattern.]
### Assess options
### Make the solution
[Code with brief inline narration.]
### Examine · verify
[Trace on 2 examples + 1 common bug avoided.]
### Examine · cost
[5-piece from W2, with the time-defense sentence cleanly delivered.]

## Cross-references

- Lecture: [link to relevant section]
- Drill: [link to relevant drill]
- Sister mini-project problem: [link with 1-2 sentence comparison]

## What I would do differently next time

[Optional but recommended: 1-2 sentences.]
```

---

## Acceptance criteria

- [ ] Both write-ups present in `frame-writeups/c2-week-06/mini-project/`.
- [ ] Each write-up has a leading 30-second memo following the schema above.
- [ ] **Problem 1 uses the grid-BFS memo schema; Problem 2 uses the node-BFS memo schema.**
- [ ] Each write-up has all five FRAME sections (Frame · Research constraints · Assess options · Make the solution · Examine) fully written out (no "see drill" placeholders).
- [ ] Each write-up has a trace on at least two examples in the Examine (verify) section.
- [ ] Each write-up has a Cross-references section linking to the other mini-project problem with a 1-2 sentence comparison.
- [ ] Both `.py` solution files are present and pass their respective test cases.

---

## Suggested order of operations

### Thursday — drafting (1.5h)

1. Open the mini-project folder. Create three empty files (the two problem write-ups + this README).
2. For each problem, write only the **30-second memo** at the top. Do not write the rest yet. Read each memo aloud; sharpen until it hits 25-30 seconds.
3. Commit "Mini-project memos drafted."

### Friday — Problem 1 (3h)

4. Write up Problem 1 in full FRAME. Allow 3 hours — the in-depth Frame and Research constraints are the time-consuming parts.
5. Trace at least two examples in Examine (verify).
6. Code + commit.

### Saturday — Problem 2 (3h)

7. Write up Problem 2 in full FRAME. Cross-reference back to Problem 1 in the Research constraints section ("same template, different `neighbors_fn`").
8. Trace at least two examples in Examine (verify).
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
- Research constraints sections that explicitly compare the two sub-shapes.
- Make the solution sections with the `neighbors_fn` clearly visible as a named function or labeled block.
- Cross-references at the bottom of each write-up linking to the other.
- Recordings ≥ 20 minutes each, with the full FRAME narration.

A learner who has shipped this mini-project *poorly* has:

- Memos that run 60+ seconds — too verbose, missing the cadence.
- Research constraints sections that name "BFS" but do not specify the sub-shape.
- Make the solution sections without a clearly extracted `neighbors_fn`.
- No cross-references; each write-up reads as a stand-alone with no awareness of the other.

If you catch yourself producing the "poorly" shape, the fix is to re-read Lecture 2 §11 (the sub-shape decision flow) and re-do whichever write-up is weaker.

---

## Why one of each specifically

Two reasons.

1. **One grid + one node is the diet of a real BFS interview.** Phase 2 onsites typically ask one BFS problem; that problem is either a grid (50% of the time) or a node (50% of the time). Shipping one of each guarantees you have practiced the at-bat for whichever you draw.

2. **The syllabus mandates exactly this composition.** From the Week 6 line in `SYLLABUS.md`: *"Mini-project: A grid BFS problem (e.g., shortest path with obstacles) and a node BFS problem (word ladder family). Both FRAME-narrated."* The composition is the contract.

If you finish before Sunday with energy to spare, add a third write-up from the LeetCode BFS tag at your discretion — for example, "Bus Routes" (LC 815) is a great stretch because the senior insight is *modeling nodes as routes, not stops*, which is a recognition-level skill not exercised in the drills. The acceptance criterion is *two* — anything beyond is bonus.

---

When done: push everything, then move on to [Week 7 — DFS](../../week-07-dfs-and-topological-sort/).

Phase 2's second week is closed. Your portfolio now contains two canonical BFS write-ups; that section will be referenced again in Mock #2 (Week 9) and in the capstone (Week 15).
