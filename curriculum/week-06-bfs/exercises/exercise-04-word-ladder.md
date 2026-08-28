# Exercise 4 — Word Ladder

> **Pattern:** Node-BFS on an implicit string graph + wildcard-bucket neighbor index
> **Difficulty:** Medium/Hard
> **Target solve time:** 35 minutes (with full FRAME narration)
> **Why fourth:** the canonical node-BFS problem in the standard interview repertoire. The neighbor function is non-trivial — naive `O(N × L)` per word would make BFS `O(N² × L)`, often too slow. The wildcard-bucket index brings it down to `O(N × L²)`. This drill installs both the node-BFS template *and* the auxiliary-data-structure-to-accelerate-neighbor-generation idiom that you will reuse in the challenge and Mock #2.

## Problem statement

Given two words `beginWord` and `endWord`, and a dictionary `wordList`, return the **length of the shortest transformation sequence** from `beginWord` to `endWord` such that:

- Only one letter can be changed at a time.
- Each transformed word must exist in `wordList`.
- The sequence includes `beginWord` and `endWord` (so the answer is the count of words).

Return 0 if no such sequence exists.

**Examples:**

- `beginWord = "hit"`, `endWord = "cog"`, `wordList = ["hot","dot","dog","lot","log","cog"]` → `5` (path `hit → hot → dot → dog → cog`)
- `beginWord = "hit"`, `endWord = "cog"`, `wordList = ["hot","dot","dog","lot","log"]` → `0` (endWord not in list)
- `beginWord = "a"`, `endWord = "c"`, `wordList = ["a","b","c"]` → `2` (path `a → c`)

## FRAME checklist for this drill

- [ ] **F:** Restate. Confirm exactly one letter changes per step. Confirm intermediate words must be in `wordList`. Confirm the answer counts `beginWord` and `endWord`. Confirm `endWord` not in `wordList` → return 0. Confirm `beginWord` may or may not be in `wordList`; both behave the same.
- [ ] **R:** Node-BFS on an implicit string graph with a wildcard-bucket neighbor index. The 30-second memo: *"Words are nodes; an edge connects two words that differ by exactly one letter. The graph is implicit; we build a wildcard-bucket index to make neighbor generation `O(L²)` per word instead of `O(N × L)`. BFS with level tracking — the answer is a level count. Why not DFS: shortest path requires BFS. Why not exhaustive neighbor scan: `O(N²) × L` is too slow for `N >= 5000`; the bucket index drops it to `O(N × L²)`. The bidirectional-BFS optimization is the senior-level stretch."*
- [ ] **A:** Four steps.
  1. **Early exit.** If `endWord not in wordList`, return 0.
  2. **Build the bucket index.** For each word in `wordList`, for each position `i`, the pattern `word[:i] + '*' + word[i+1:]` is a key; map the pattern to the list of words matching it.
  3. **BFS with level tracking.** Queue = `deque([beginWord])`. Visited = `{beginWord}`. `level = 1` (count of `beginWord`). Outer loop: snapshot `len(queue)`, dequeue that many. For each word, if it equals `endWord`, return `level`. Else generate neighbors via the bucket: for each `i`, look up `word[:i] + '*' + word[i+1:]`, enqueue unvisited entries. Increment `level`.
  4. **Termination.** Loop exits with queue empty → return 0.
  Edge case: `beginWord == endWord` — return 1 (path is the single word). Most problem specs say `beginWord != endWord`, but handle defensively.
- [ ] **M:** Write the code, narrating each line. Speak the bucket-index invariant: *"The bucket maps each wildcard pattern to the words matching it; building it is `O(N × L²)` work but pays for itself in linear amortized neighbor cost during BFS."*
- [ ] **E (verify):** Trace on `hit → cog` with `[hot, dot, dog, lot, log, cog]`. Bucket: `*it: [hit]`, `h*t: [hit, hot]`, `hi*: [hit]`, `*ot: [hot, dot, lot]`, `h*t: [hit, hot]`, `ho*: [hot]`, `*ot: [hot, dot, lot]`, `d*t: [dot]`, `do*: [dot, dog]`, `*og: [dog, log, cog]`, `d*g: [dog]`, `do*: [dot, dog]`, etc. Level 1: dequeue hit. Patterns *it, h*t, hi*. Neighbors: hot (via h*t). Enqueue hot. Visited: {hit, hot}. Level 2: dequeue hot. Patterns *ot, h*t, ho*. Neighbors: dot, lot (via *ot, both unvisited). Enqueue. Visited adds {dot, lot}. Level 3: dequeue dot. Patterns *ot, d*t, do*. Neighbors via do*: dog. Enqueue. Visited adds {dog}. Dequeue lot. Patterns *ot, l*t, lo*. Neighbors via lo*: log. Enqueue. Visited adds {log}. Level 4: dequeue dog. Patterns *og, d*g, do*. Neighbors via *og: cog (unvisited). Enqueue. Visited adds {cog}. Dequeue log. Patterns *og, l*g, lo*. Neighbors via *og: cog (visited). Level 5: dequeue cog. `cog == endWord` → return 5. ✓
- [ ] **E (cost):** **Time `O(N × L²)`** where `N` is dictionary size and `L` is word length. Building the bucket: `O(N × L²)`. BFS examines each word at most once; each word's neighbors involve `L` pattern lookups; each pattern bucket has up to `O(N)` entries but each edge is examined at most twice across the BFS, so the amortized total is `O(N × L²)`. **Space `O(N × L²)`** for the bucket — each word generates `L` patterns each of length `L`. Tradeoff: brute-force neighbor enumeration is `O(N × L)` per word, total `O(N² × L)` — strictly worse for `N >= 100`. Bidirectional BFS is the canonical optimization here; mention it. Best `O(L)` (begin == end, immediate return); worst `O(N × L²)`.

## Acceptance criteria

- Code passes the [`timed_runner.py`](timed_runner.py) test cases for `ladder_length`.
- FRAME write-up at `frame-writeups/c2-week-06/exercise-04-word-ladder.md`.
- Your Research constraints section names **node-BFS** explicitly and describes the **wildcard-bucket index** in one sentence.
- Your Make the solution section builds the bucket index *once* before the BFS loop (not inside it).
- Your Make the solution section uses **level tracking** (outer `for _ in range(len(queue))`) — the answer is a level count.
- Your Examine (cost) section mentions **bidirectional BFS** as the production-grade optimization, even if you do not implement it.
- Recording **≥ 25 minutes**.

## Function signature (for the runner)

```python
def ladder_length(beginWord: str, endWord: str, wordList: list[str]) -> int:
    """Return shortest transformation length, or 0 if no path exists."""
    ...
```

## Common bugs you should catch in Examine (verify)

- **Building the bucket inside the BFS loop.** This re-builds the index on every iteration — `O(N² × L²)` total. Build once before the loop.
- **Not checking `endWord in wordList` first.** Without the early exit, BFS runs the whole search and finds no answer, then returns 0. The early check is `O(N)` vs `O(N × L²)` — much cheaper.
- **Off-by-one in the level count.** The answer counts `beginWord` itself, so start `level = 1`. If you start `level = 0`, you will be off by one.
- **Enqueuing words that are not in `wordList`.** Only enqueue words present in the dictionary. The bucket lookup returns only dictionary words by construction; do not generate arbitrary one-letter-different strings.
- **Using `wordList.index(...)` or other `O(N)` lookups.** Convert `wordList` to a `set` once for `O(1)` membership.
- **Reusing the same word's pattern position.** The bucket is built once globally; each pattern maps to multiple words. When generating neighbors, do not include the source word itself in the neighbor list (filter `if w != word`).

## Self-feedback template

1. Did you say **"node-BFS"** in Research constraints (not just "BFS")?
2. Did you describe the **wildcard-bucket index** before writing code?
3. Did you state the time complexity as `O(N × L²)` explicitly?
4. Did you mention **bidirectional BFS** in Examine (cost) as the senior-level optimization?

## Stretch — bidirectional BFS

If you finish with time to spare, re-implement using bidirectional BFS. Two frontiers — one growing from `beginWord`, one from `endWord` — meet in the middle. Expand the smaller frontier on each iteration. The expected speedup is ~4-10× on realistic inputs.

The Examine (cost) section should call out: *"Bidirectional BFS halves the search depth (roughly), giving `O(sqrt(branching)) × N × L²)` effective complexity. The trade is implementation complexity; for `N < 10⁴` single-source BFS is fast enough."*

## What to commit

```
frame-writeups/c2-week-06/
├── exercise-04-word-ladder.md
└── drill_04_solution.py
```

When done, push and move on to [Exercise 5](exercise-05-binary-tree-right-side-view.md).
