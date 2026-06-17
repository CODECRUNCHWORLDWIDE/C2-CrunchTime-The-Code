# Challenge 1 — Word Search II (LeetCode 212)

> **Difficulty:** Hard. **Target solve time:** 60 minutes including UMPIRE write-up.

The canonical trie-on-grid problem. Every Phase-2 onsite at a FAANG-tier company includes at least one variant of this; the senior signal is the *defense of the algorithm choice* over the naive per-word DFS baseline.

---

## Problem spec

You are given an `m x n` `board` of characters and a list of strings `words`. Return all words that exist in the board. A word is considered "on the board" if it can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring (not diagonal). The same letter cell may not be used more than once in a single word.

```
Input:
  board = [
    ['o','a','a','n'],
    ['e','t','a','e'],
    ['i','h','k','r'],
    ['i','f','l','v'],
  ]
  words = ["oath", "pea", "eat", "rain"]

Output: ["eat", "oath"]
```

**Constraints (LeetCode):**

- `m == len(board)`, `n == len(board[0])`, with `1 <= m, n <= 12`.
- `board[i][j]` is a lowercase English letter.
- `1 <= len(words) <= 3 * 10^4`.
- `1 <= len(word) <= 10`.
- `words[i]` consists of lowercase English letters.
- All strings in `words` are unique.
- The answer is returned in any order.

---

## Why this is the canonical trie-on-grid problem

Three reasons.

1. **The brute-force solution is `O(W * m * n * 4^L)`** — run a DFS per word, starting from every cell. For 50 words of length 10 on a 12x12 grid, that is `50 * 144 * 4^10 ≈ 7.5 * 10^9`. Times out on LeetCode for the upper-constraint cases.

2. **The trie solution is `O(m * n * 4^L)`** — strictly faster by a factor of `W`. The trie indexes the dictionary so that *one* DFS per starting cell handles every word; the DFS descends the trie in lockstep with the grid walk, pruning whenever the current cell's character is not a child of the current trie node. For the same constraints: `144 * 4^10 ≈ 1.5 * 10^8` — three orders of magnitude faster than the brute force, and well under the 10-second LeetCode timeout.

3. **There are three subtle implementation bugs** that show up in interviews. Knowing the bug list ahead of time is part of the senior preparation.

---

## 30-second pattern-recognition memo

Use this exact shape at the top of your write-up.

```markdown
> **30-second pattern-recognition memo (trie-on-grid):**
> This is a dictionary-on-grid problem because we are given a fixed dictionary
> and asked which entries can be formed on a 2-D grid by sequentially adjacent
> cells. Trie + DFS composition. The trie indexes the dictionary; the DFS walks
> the grid in lockstep with descent in the trie. Why not per-word DFS:
> O(W * m * n * 4^L) vs O(m * n * 4^L); the trie shares prefix work across
> words. Edge model: mark cells visited; unmark on backtrack. Pruning: stop the
> descent when the current cell's char is not a child of the current trie node.
> De-duplication: stash the word at the END sentinel; remove the END marker
> after emitting to avoid duplicates.
```

Read aloud; should hit 25-30 seconds.

---

## The intended algorithm

```python
from typing import Any, Dict, List


END = "$"


def find_words(board: List[List[str]], words: List[str]) -> List[str]:
    """Return all words from `words` that can be formed on `board`."""
    if not board or not board[0] or not words:
        return []

    trie = _build_trie(words)
    rows, cols = len(board), len(board[0])
    out: List[str] = []

    for r in range(rows):
        for c in range(cols):
            _dfs(board, r, c, trie, out)

    return out


def _build_trie(words: List[str]) -> Dict[str, Any]:
    """Build a trie; stash the original word at the END sentinel for emit."""
    root: Dict[str, Any] = {}
    for word in words:
        node = root
        for ch in word:
            node = node.setdefault(ch, {})
        node[END] = word  # stash the word for emit on match
    return root


def _dfs(
    board: List[List[str]],
    r: int,
    c: int,
    node: Dict[str, Any],
    out: List[str],
) -> None:
    """Recursive DFS in lockstep with trie descent."""
    ch = board[r][c]
    if ch not in node:
        return
    child = node[ch]
    if END in child:
        out.append(child[END])
        del child[END]  # de-dupe; do not emit the same word twice

    board[r][c] = "#"  # mark visited in place

    rows, cols = len(board), len(board[0])
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
            _dfs(board, nr, nc, child, out)

    board[r][c] = ch  # restore on backtrack
```

---

## Walk-through

Input as above. The trie has paths `o -> a -> t -> h ($: "oath")`, `p -> e -> a ($: "pea")`, `e -> a -> t ($: "eat")`, `r -> a -> i -> n ($: "rain")`.

Run `_dfs` from each cell. Most cells fail immediately because the cell's character is not at the trie root (root's children are `{o, p, e, r}`). The interesting starts are:

- `(0, 0)` = `'o'`: descend; `_dfs((0, 0), trie["o"])`. Mark visited. Try neighbors: `(0, 1)` = `'a'` — `a` is a child of `o`; descend. Try neighbors: `(1, 1)` = `'t'` — `t` is a child of `a`; descend. Try neighbors: `(2, 1)` = `'h'` — `h` is a child of `t`; descend. The new node has `END: "oath"`; emit `"oath"`, delete `END`. Continue exploring (no more children); unwind, unmark.

- Eventually the DFS reaches a cell whose character starts the path for `"eat"` — at `(1, 0)` = `'e'`. Descend; `a` at `(1, 1)`; `t` at... wait, `(1, 1)` is `'t'`, not `'a'`. Try `(0, 0)` = `'o'` — not `'a'`. Try `(2, 0)` = `'i'` — not `'a'`. The DFS from `(1, 0)` fails to extend past `e`. But from `(1, 3)` = `'e'`: descend. Neighbors: `(0, 3)` = `'n'` — not in trie; `(2, 3)` = `'r'` — not in trie; `(1, 2)` = `'a'` — yes. Descend. Neighbors: `(0, 2)` = `'a'` — not in trie at this node; `(2, 2)` = `'k'` — not in trie; `(1, 1)` = `'t'` — yes. Descend. The new node has `END: "eat"`; emit `"eat"`.

- `"pea"` and `"rain"` are not findable (no `'p'` on the board; the `'r'` is at `(2, 3)` but the neighbors `'a, i, n'` are not in the right adjacent positions).

Final output: `["oath", "eat"]` (order may vary; LC accepts any order).

---

## Complexity defense

Say it out loud:

> "**Time is `O(m * n * 4^L)`** where `L` is the maximum word length. The DFS starts at every cell (`m * n` starts); each DFS explores at most `4^L` paths (each step has at most 3 unvisited neighbors after the first, but the bound is conservative at `4^L`). The trie pruning means most starting cells fail immediately at depth 0. **Space is `O(N)`** where `N = sum(len(w) for w in words)` for the trie. The recursion depth is bounded by `L`. **Trade against per-word DFS:** the per-word approach is `O(W * m * n * 4^L)` — a factor of `W` worse. For LC 212 constraints (`W` up to `3 * 10^4`), the per-word approach times out; the trie approach passes."

---

## Three subtle bugs

These are graded. Knowing them up front shortens your debug cycle by 20 minutes.

### Bug 1 — Not de-duplicating emitted words

If the same word can be formed on the board through *two* different cell paths, the naive DFS emits it twice. The LC 212 spec requires each word once.

The fix is one of:

- **Stash the word at `END` and `del child[END]` after emit.** This is the approach used above. Slightly mutates the trie; safe because the trie is local to this function call.
- **Use a `set[str]` for `out`, then convert to list at the end.** Simpler but slightly slower due to hashing.
- **Track an "already emitted" set externally and check before append.**

The `del child[END]` form is the most idiomatic and the cleanest in the write-up. The mutation is local; the trie is rebuilt next call.

### Bug 2 — Restoring the cell after backtrack

Marking `board[r][c] = "#"` and forgetting to restore it later means subsequent DFS calls from other starting cells see the wrong board. The bug is invisible on small inputs and devastating on grids with shared characters.

The fix is the `board[r][c] = ch` line at the end of `_dfs`. The `ch` variable captures the original character before the mutation.

### Bug 3 — Pruning the trie after the descent

A senior-grade optimization. After emitting a word, you can prune the trie by removing dead branches. Specifically, after `del child[END]`, if `child` is now empty, you can also delete the corresponding key from `node`'s children — pruning the entire branch. This is iterative: walk back up after pruning a leaf and remove parent entries if they too are now empty.

For LC 212 grading, this optimization is not required. For senior-grade write-ups, mention it as the "in-place pruning" extension: "We could further prune `child` from `node` if `child` is now empty after the `del`, freeing memory and shortening subsequent DFS pruning."

---

## Recommended write-up structure

Under `umpire-writeups/c2-week-09/challenges/word-search-ii.md`:

```markdown
# Word Search II — UMPIRE Write-up

> **30-second pattern-recognition memo (trie-on-grid):**
> [the memo from above, verbatim]

## Understand
... restate the problem, walk one example, note the constraints.

## Match
... trie + DFS composition; defend over per-word DFS; cite Lecture 1 and Lecture 2.

## Plan
... build the trie; for each cell, DFS in lockstep; emit on END; mark/restore visited.

## Implement
... the code above, with comments.

## Review
... trace on the LC 212 example; verify the two outputs; walk one negative case (where a word
is *not* on the board, e.g., "pea" in this example).

## Evaluate
... O(m * n * 4^L) time, O(N) space; trade against per-word DFS; mention pruning as a stretch.
```

A clean write-up should be under 500 lines and read aloud in 10-12 minutes. Recording at that length is expected.

---

## Variants to mention in the Evaluate section

For senior signal, mention at least one of these variants:

- **Diagonal adjacency allowed.** The neighbor loop becomes 8 directions instead of 4; the asymptotic bound becomes `O(m * n * 8^L)`. Otherwise identical.
- **Word reuse allowed.** No visited mask; each cell can be reused. This is no longer a backtracking problem — it is now a "is this word a path in the grid graph"; the DFS does not need to unmark.
- **Each cell yields all length-`L` words it can start, with early termination.** A streaming variant; useful when the words list is huge but only the first few hits are needed.

Naming the variants — even briefly — earns senior signal. The interviewer's follow-up is often "and what changes if we...," and being ready with the answer compresses the back-and-forth.

---

## Acceptance criteria

A complete challenge write-up has, at minimum:

- The 30-second pattern-recognition memo at the top.
- Full UMPIRE — six sections.
- The implementation in your portfolio repo at `challenges/word-search-ii.py`.
- A recording of at least 10 minutes walking through Match → Plan → Implement.
- A test run showing all LC 212 sample cases pass.
- One mention of either the de-dup approach, the visited-restore discipline, or the pruning optimization in the Review section.

After the write-up is pushed, move on to [Challenge 2 — Replace Words](./challenge-02-replace-words.md) if time permits, or skip to the [mini-project](../07-mini-project/00-overview.md).
