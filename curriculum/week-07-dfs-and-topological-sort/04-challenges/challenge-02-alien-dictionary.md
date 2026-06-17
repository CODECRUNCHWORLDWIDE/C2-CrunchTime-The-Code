# Challenge 2 (optional) — Alien Dictionary (LeetCode 269)

> **Pattern:** Topological sort on a *derived* edge set; recognition-step exercise
> **Difficulty:** Hard
> **Target solve time:** 75 minutes (first time; 35 minutes on revisit)
> **Why hard:** the algorithm is Kahn's algorithm from Lecture 3 §4 — a template you already own. The hard part is **modeling the problem as a graph** in the first place. Given a list of words sorted in an unknown language's alphabet, you must extract the pairwise letter-ordering constraints (the edge set) before topological sort applies. The Match-step recognition — "this is a topological sort problem in disguise" — is the senior signal.

## Problem statement

There is a new alien language that uses the English alphabet. However, the order of the letters is unknown to you.

You are given a list of strings `words` from the alien language's dictionary, sorted lexicographically by the rules of this new language.

Derive the order of letters in this language and return it. If the given input is invalid, return `""`. If there are multiple valid solutions, return any of them.

Per the LC spec: `1 <= words.length <= 100`; `1 <= words[i].length <= 100`; `words[i]` consists of only lowercase English letters.

**Examples:**

- `words = ["wrt","wrf","er","ett","rftt"]` → `"wertf"` (or any valid order — "wertf" satisfies the constraints derived from pairwise comparison.)
- `words = ["z","x"]` → `"zx"`.
- `words = ["z","x","z"]` → `""` (invalid: implies `z < x` and `x < z`, a cycle.)
- `words = ["abc","ab"]` → `""` (invalid: `"abc"` cannot precede `"ab"` if they share the prefix and the longer one is a proper extension — that violates lex order.)

## Acceptance criteria

- [ ] Code passes the test cases at the bottom.
- [ ] Solution is **`O(C + U + min(U, N) × N²)`** time where `C` is the total content of all words, `U` is the unique letters, `N` is the number of words. The graph build dominates in most inputs.
- [ ] Your UMPIRE write-up **identifies the edge-extraction step** as a Match-step move. The 30-second memo must include: *"Edges come from pairwise comparison of adjacent words in the sorted list — the first differing character of word `i` and word `i + 1` gives an edge `word[i][k] → word[i+1][k]`."*
- [ ] Your write-up handles the **invalid-input edge case**: `["abc","ab"]` — the spec-violating prefix case. Without explicit handling, this returns a non-empty string and is graded as wrong.
- [ ] Recording **≥ 40 minutes**.

## The decomposition (the interview tell)

Three structural insights:

**Insight 1 — The edges come from pairwise comparison.** For each adjacent pair of words `words[i]` and `words[i+1]`, scan from left to right to find the first differing character. That character pair gives an edge: `words[i][k] → words[i+1][k]`, meaning "in the alien language, the first letter comes before the second." All other character pairs are irrelevant (they share the prefix or come after the first difference).

**Insight 2 — The invalid-prefix case.** If `words[i+1]` is a proper prefix of `words[i]` (e.g., `words[i] = "abc"`, `words[i+1] = "ab"`), the input is invalid. In a lexicographically sorted list, a proper prefix always sorts *before* its extension; the input violates this and we return `""`.

**Insight 3 — Letters not appearing in any constraint still belong to the alphabet.** A letter that appears only inside words but is never the first-difference character has no incoming or outgoing edges. It must still appear in the output. Initialize the node set with *every letter that appears anywhere*, then add edges from pairwise comparison.

**Technique — Kahn's algorithm.** Once the edge set is built, this is Course Schedule II with letters instead of integers.

```
Example: ["wrt", "wrf", "er", "ett", "rftt"]

Pairwise compare:
  "wrt" vs "wrf": first difference at index 2 -> edge t -> f
  "wrf" vs "er":  first difference at index 0 -> edge w -> e
  "er"  vs "ett": first difference at index 1 -> edge r -> t
  "ett" vs "rftt": first difference at index 0 -> edge e -> r

Letters appearing: {w, r, t, f, e}

Edge set: {(t, f), (w, e), (r, t), (e, r)}

Topological sort:
  in_degree: {w: 0, e: 1, r: 1, t: 1, f: 1}
  queue: [w]
  process w -> e (in_degree[e]=0); queue: [e]
  process e -> r (in_degree[r]=0); queue: [r]
  process r -> t (in_degree[t]=0); queue: [t]
  process t -> f (in_degree[f]=0); queue: [f]
  process f

Result: "wertf"
```

The discriminator: most candidates jump to Kahn's algorithm without articulating *how the edges are derived*. The interview-tell move is **stating the pairwise-comparison rule out loud in Match** before writing any code. Without that step, the algorithm cannot be specified.

## UMPIRE outline

- **U:** Restate. The input is sorted in the alien language's lex order. We must output the letter order. Walk by hand: `["wrt","wrf"]` — first differing character is at index 2, `t` vs `f` — in this language, `t < f`. Confirm the invalid-prefix case (`["abc","ab"]` → `""`). Confirm "letters that appear but are never compared" still go in the output.

- **M:** Topological sort on a derived edge set. The 30-second memo:
  > *"Topological sort in disguise. The nodes are the letters appearing in the input. The edges come from pairwise comparison of adjacent words: for words `i` and `i+1`, the first differing character pair gives an edge `letter_i → letter_{i+1}`. If word `i+1` is a proper prefix of word `i`, the input is invalid → return `''`. Once the graph is built, this is Course Schedule II — Kahn's algorithm yields a valid topological order. Cycle → return `''`. Why Kahn: iterative, no recursion risk; the in-degree array is a clean invariant. Why DFS post-order would also work: yes, but Kahn extends naturally to 'enumerate all valid orders' if a follow-up asks."*

- **P:** Four bullets.
  1. **Collect all letters** from every word into `nodes: set[str]`.
  2. **Build edges** from pairwise comparison of adjacent words. Handle the invalid-prefix case: return `""` if `len(words[i]) > len(words[i+1])` and `words[i+1]` is a prefix of `words[i]`.
  3. **Run Kahn's algorithm** on the derived edge set, with `in_degree` defaulting to 0 for nodes with no incoming edges.
  4. **Cycle check**: if `len(order) != len(nodes)`, return `""`; else return the joined order.

- **I:** Implement. The edge-extraction loop is the most error-prone part — get the index-of-first-difference right and the prefix-validation right.

- **R:** Trace on example 1.
  - nodes = {w, r, t, f, e}
  - Pairwise edges: as derived above.
  - Kahn's: order = "wertf". ✓
  - Trace on `["z","x","z"]`: edges `z → x`, `x → z` — cycle; Kahn returns `len(order) < 2` → `""`. ✓
  - Trace on `["abc","ab"]`: index 0, 1 match; at index 2, `words[1]` ends — invalid prefix → return `""`. ✓
  - Trace on `["z"]`: no pairs to compare; nodes = {z}; Kahn returns `"z"`. ✓

- **E (graded):** **Time `O(C)`** where `C` is the sum of all word lengths — extracting edges scans pairs in `O(L)` and there are `N-1` pairs, total `O(N × L) = O(C)`. **Space `O(U + E)`** where `U` is the unique letters and `E` is the derived edges; `U <= 26` and `E <= N - 1`. The asymptotic is dominated by `C`. Tradeoff: there is no faster algorithm — you have to scan each pair to extract its constraint. The senior signal is that **the recognition step (Match: "topological sort on a derived edge set") is the entire intellectual content**; the implementation is straightforward Kahn.

## Function signature

```python
def alien_order(words: list[str]) -> str:
    """Return a valid letter order in the alien alphabet, or '' if invalid."""
    ...
```

## Test cases to verify

```python
import pytest


def is_valid_order(order: str, words: list[str]) -> bool:
    """Verify that `order` is consistent with the sorted-words constraints."""
    if not order:
        # Empty answer must correspond to invalid input; we trust the caller.
        return True
    position = {c: i for i, c in enumerate(order)}
    # Every letter that appears must be in the order.
    letters = {c for w in words for c in w}
    if letters - set(order):
        return False
    # Every pairwise constraint must be respected.
    for w1, w2 in zip(words, words[1:]):
        for c1, c2 in zip(w1, w2):
            if c1 != c2:
                if position[c1] > position[c2]:
                    return False
                break
        else:
            if len(w1) > len(w2):
                return False
    return True


@pytest.mark.parametrize(
    "words, expect_empty",
    [
        (["wrt", "wrf", "er", "ett", "rftt"], False),
        (["z", "x"], False),
        (["z", "x", "z"], True),
        (["abc", "ab"], True),
        (["a"], False),
        (["ab", "adc"], False),
        (["aac", "aabb"], False),
        (["aa", "ab", "ba"], False),
    ],
)
def test_alien_order(words, expect_empty):
    actual = alien_order(words)
    if expect_empty:
        assert actual == ""
    else:
        assert is_valid_order(actual, words)
```

## Common bugs you should catch in Review

- **Missing the invalid-prefix check.** Returning a non-empty order for `["abc", "ab"]` is a wrong answer. The check must fire *before* attempting topological sort.
- **Failing to include letters with no edges.** A letter like `c` in `["ab", "ac"]` has edge `b → c` but no incoming edge — it must still appear in the output. The `in_degree` array must default to 0 for *every* letter, not just letters that appear as targets of edges.
- **Adding duplicate edges to the in-degree count.** If pairwise comparison yields the same `(c1, c2)` edge twice (e.g., from `["ab", "ac", "ad"]` — actually no, those give different second characters; but synthetic adversarial inputs can repeat), incrementing `in_degree` twice over-counts. Use a `set` to dedupe edges before computing in-degrees.
- **Using DFS post-order without `sys.setrecursionlimit`.** The recursion depth is bounded by the alphabet size (`U ≤ 26`), so this is *not* a real risk here — but if you copy the template from Lecture 3 §3 verbatim, you might raise the limit anyway. State explicitly that the alphabet is small.
- **Returning a multi-character string when the input is one word.** `["a"]` has no pairwise constraints; the output is just `"a"`. Forgetting to handle this case returns `""` (wrong) or returns a partial output.

## The "why is this topological sort?" defense

Out loud, in your Match section:

> "The alien-dictionary problem decomposes into two parts: (1) deriving the graph from the input, and (2) topologically sorting the resulting DAG. Part (2) is Kahn's algorithm from Lecture 3 — a template I already own. Part (1) is the recognition step: I scan adjacent word pairs, find the first differing character, and extract an edge `c1 → c2` from each pair. Letters that appear in the input but never become edge endpoints are still nodes; they go in the output at whatever position the topological sort assigns. The invalid-prefix case (`words[i+1]` is a proper prefix of `words[i]`) violates sortedness and must short-circuit to `''`. The whole algorithm is `O(C)` time where `C` is the total content of all words — dominated by the edge extraction; the topological sort itself is `O(U + E)` with `U <= 26` and `E <= N - 1`."

Memorize the shape. This is a "recognition + apply a known template" problem; the senior signal is naming the decomposition before writing code.

## Why this matters

Alien Dictionary is a representative member of a class of problems where **the input is not obviously a graph** — the candidate must *model* it as a graph before any standard algorithm applies. Other members of this class:

1. **Sequence Reconstruction (LC 444).** Given a target sequence and a list of subsequence constraints, is the target the unique topological order of the subsequence graph? Same modeling step: extract pairwise constraints from the subsequences.
2. **Reconstruct Itinerary (LC 332).** Given a list of flight tickets, find the lexicographically smallest valid itinerary. Modeling: each ticket is an edge; the answer is an Eulerian path. Out of scope but the modeling step is similar.
3. **Find Eventual Safe States (LC 802).** Identify nodes from which every walk terminates. Modeling: reverse the graph and topologically sort the result.

When you revisit Alien Dictionary before Mock #2, **re-derive the edge-extraction rule from scratch** rather than re-reading your old solution. The recognition skill is what compounds.

## Stretch

**Sequence Reconstruction (LC 444).** The "is the topological order *unique*?" variant. The trick: Kahn's algorithm has a unique topological order if and only if the queue *never* has more than one node at a time. If at any point `len(queue) > 1`, multiple valid orders exist.

**Course Schedule IV (LC 1462).** Given the prerequisite graph and a list of queries `(a, b)`, return whether `a` is a prerequisite (direct or indirect) of `b`. The trick: compute the transitive closure of the DAG using DFS or Floyd-Warshall. `O(V³)` for `V = 100` is fine.

**The "all valid orders" extension.** Extend `alien_order` to return *every* valid topological order, not just one. The trick: at each step, when `len(queue) > 1`, branch on the choice of which zero-in-degree letter to take next. Worst-case exponential — but for `U <= 26` it is tractable.

---

This concludes Challenge 2. Take the [quiz](../05-quiz.md), do the [homework](../06-homework.md), then ship the [mini-project](../07-mini-project/00-overview.md) — one DFS write-up and one topological-sort write-up.
