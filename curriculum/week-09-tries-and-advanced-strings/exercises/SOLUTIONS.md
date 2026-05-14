# Week 9 — Worked Solutions

Three worked solutions, each with UMPIRE narration. **Attempt every exercise on your own first.** If you read this file before drafting your own, you forfeit the recognition rep — and recognition is what Phase 2 is grading.

The solutions below are written in the same voice you should be using in your portfolio write-ups. Read them as templates, not as the answer.

---

## Solution 1 — Implement Trie (Prefix Tree) (LC 208)

### Understand

We are given a class to implement with three operations: `insert(word)`, `search(word)`, `starts_with(prefix)`. `insert` and `search` agree on full-word matches; `starts_with` is a prefix-only check. The discriminator between `search` and `starts_with` is whether the terminal sentinel is required at the final node.

Hand-walk on the LC 208 example:

```
t = Trie()
t.insert("apple")
t.search("apple")    -> True   (the terminal marker is at the 'e' node)
t.search("app")      -> False  (no terminal at the 'p' node)
t.starts_with("app") -> True   (the path c -> a -> p exists)
t.insert("app")
t.search("app")      -> True   (now the 'p' node is also a terminal)
```

### Match

Trie pattern; dict-of-dict form. The 30-second memo:

> *Trie problem; canonical insert / search / starts_with API. Dict-of-dict form: root is an empty dict; each level is a dict[str, Any]; `END = "$"` marks terminals (any character outside the input alphabet works). Why not `set[str]`: the set cannot answer `starts_with` in less than `O(n * L)`; the trie answers it in `O(P)`. Time: `O(L)` per operation. Space: `O(N)` where `N` is total inserted character count.*

### Plan

1. `__init__`: `self.root: Dict[str, Any] = {}`.
2. `insert(word)`: walk `self.root`, `setdefault` on each character, mark `END` at the terminal.
3. `search(word)`: walk; on missing child, return False; at the end, return `END in node`.
4. `starts_with(prefix)`: walk; on missing child, return False; at the end, return True.

### Implement

```python
from typing import Any, Dict

END = "$"


class Trie:
    def __init__(self) -> None:
        self.root: Dict[str, Any] = {}

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node[END] = True

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node:
                return False
            node = node[ch]
        return END in node

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node:
                return False
            node = node[ch]
        return True
```

### Review

The two discriminators against common bugs:

- The `END in node` check at the bottom of `search` is what distinguishes it from `starts_with`. Forgetting it makes `search("ap")` return True after `insert("apple")` (Lecture 1, Bug 1).
- `setdefault(ch, {})` is the line that creates children only on `insert`. Using `setdefault` in `search` would silently mutate the trie (Lecture 1, Bug 3).

### Evaluate

- **Time:** `insert` and `search` are `O(L)`; `starts_with` is `O(P)`. The walk visits each character exactly once.
- **Space:** `O(N)` total across all inserted words, where `N = sum(len(w) for w in words)`. With prefix sharing, strictly less than `N`.
- **Trade vs `set[str]`:** the set is `O(L)` expected for exact-match but cannot answer `starts_with` in less than `O(n * L)`. The trie is strictly more capable; default to the trie when prefix queries are anywhere in the spec.

---

## Solution 2 — Word Break (LC 139)

### Understand

We are given a string `s` and a list of dictionary words. We must decide whether `s` can be segmented into a space-separated sequence of dictionary words; reuse is allowed. The output is boolean.

Hand-walk on `s = "applepenapple"`, `word_dict = ["apple", "pen"]`. Segmentation: `apple | pen | apple`. Both pieces are in the dictionary; reuse is allowed; return True.

The trap is `s = "catsandog"`, `word_dict = ["cats", "dog", "sand", "and", "cat"]`. Possible starts: `cat | sandog`? `sandog` is not in the dictionary and cannot itself be segmented. `cats | andog`? Same problem with `andog`. No valid segmentation; return False.

### Match

Trie + memoization composition. The 30-second memo:

> *Word-break problem. Trie + memo composition. The trie indexes the dictionary by prefix; at each starting index `i`, walk the trie from the root over `s[i:]`. Whenever the trie node has `END`, recurse on `i = j` (the post-word index). Memo on `i` to cut overlapping subproblems. Time `O(n^2)` where `n = len(s)`; space `O(n + W*L)` for the memo + trie. Why a trie instead of `set[str]`: the trie keeps the inner loop honest at `O(n - i)` per descent regardless of dictionary size; with a set, the inner loop is `O(W * L)` per starting index.*

### Plan

1. Build the trie from `word_dict`.
2. Recursive helper `can_break(s, i, trie, memo)`:
   - Base case: `i == len(s)` → True.
   - Memo check: if `i in memo`, return `memo[i]`.
   - Walk the trie from `i`: while `s[j] in node`, advance; if `END in node`, recurse on `j`; return True if the recursion returns True.
   - If the walk falls through, memoize False and return False.

### Implement

```python
from typing import Any, Dict, List

END = "$"


def word_break(s: str, word_dict: List[str]) -> bool:
    trie = _build_trie(word_dict)
    memo: Dict[int, bool] = {}
    return _can_break(s, 0, trie, memo)


def _build_trie(words: List[str]) -> Dict[str, Any]:
    root: Dict[str, Any] = {}
    for word in words:
        node = root
        for ch in word:
            node = node.setdefault(ch, {})
        node[END] = True
    return root


def _can_break(s: str, i: int, trie: Dict[str, Any], memo: Dict[int, bool]) -> bool:
    if i == len(s):
        return True
    if i in memo:
        return memo[i]
    node = trie
    j = i
    while j < len(s) and s[j] in node:
        node = node[s[j]]
        j += 1
        if END in node and _can_break(s, j, trie, memo):
            memo[i] = True
            return True
    memo[i] = False
    return False
```

### Review

Trace on `s = "leetcode"`, `word_dict = ["leet", "code"]`:

- `can_break(0)`: walk from root; `l, e, e, t`; at `t`, `END in node`; recurse on `i = 4`.
- `can_break(4)`: walk from root; `c, o, d, e`; at `e`, `END in node`; recurse on `i = 8`.
- `can_break(8)`: `i == len(s)` → True.
- Propagate True; final answer True.

Trace on `s = "catsandog"`, `word_dict = ["cats", "dog", "sand", "and", "cat"]`:

- `can_break(0)`: walk from root; at `t` (j = 3), `END in node` (from "cat"); recurse on `i = 3`.
  - `can_break(3)`: walk from root; `s, a, n, d`; at `d` (j = 7), `END in node` (from "sand"); recurse on `i = 7`.
    - `can_break(7)`: walk from root; `o, g`; at `g` (j = 9), but `s[7..]` is "og" — the walk hits the `o` then needs `g`; `g` is not a child of `o` (the trie has `d -> o -> g` for "dog", not `o -> g`). Actually re-examine: at `i = 7`, `s[7] = 'o'`; the root has `o`? No — the dictionary words are `cats, dog, sand, and, cat`; the root's children are `{c, d, s, a}`. `'o' not in trie` — the walk fails immediately; return False.
  - Continue trying j = 4 (the `s` node from "cats"); `END in node` (from "cats"); recurse on `i = 4`.
    - `can_break(4)`: walk from root; `s[4] = 'a'`; `a` is a child of root (from "and"); walk `a, n, d`; at `d` (j = 7), `END in node`; recurse on `i = 7` — already memoized False.
    - Continue the walk: after `a -> n -> d`, the trie node at `d` has no further children that match `s[7] = 'o'`. Memo `can_break(4) = False`.
  - No more progress at i = 3; memo `can_break(3) = False`.
- Continue from i = 0; the walk from root advances `c -> a -> t -> s`; `END in node` at j = 4 (from "cats"); recurse on `i = 4` — already memoized False.
- No more progress at i = 0; memo `can_break(0) = False`.
- Return False.

### Evaluate

- **Time:** `O(n^2)` where `n = len(s)`. Each position `i` triggers at most one trie descent of length `<= n - i`. Summing: `n + (n-1) + ... + 1 = n(n+1)/2 = O(n^2)`. The memo prevents repeating subproblems.
- **Space:** `O(n + sum(len(w) for w in word_dict))`. `O(n)` for the memo; the rest for the trie.
- **Trade vs hash-set DP:** the hash-set version is `O(n^2)` too if substring extraction is constant-time, but with substring allocation it becomes `O(n^2 * L)`. The trie version avoids the allocation by descending character-by-character. Both are accepted on LC 139; the trie generalizes to LC 140 (Word Break II) where the hash-set version handles poorly.

---

## Solution 3 — Longest Common Prefix (LC 14)

### Understand

We are given a list of strings; return the longest string that is a prefix of every input. Return `""` if no common prefix exists or if any input is empty.

Hand-walk on `["flower", "flow", "flight"]`: `f` is in all three at index 0; `l` at index 1; at index 2, `flower[2] = 'o'`, `flow[2] = 'o'`, `flight[2] = 'i'` — mismatch. LCP is `"fl"`.

### Match

Three valid solutions, with different trade-offs. The 30-second memo:

> *LCP problem; three solutions. Vertical scan walks column-by-column, `O(n * L)`. Horizontal scan does pairwise LCP, `O(n * L)`. Trie walk builds a trie then descends while every node has exactly one child and is not a terminal, `O(N)` where `N` is total character count. For one-shot LC 14, vertical scan is the lightest and what to default to. The trie is the right answer for the incremental / multi-query generalization — "for each new query, return the LCP shared with the dictionary."*

### Plan

Three implementations; pick the discriminating sentence for the write-up.

### Implement

**Vertical:**

```python
from typing import List


def lcp_vertical(strs: List[str]) -> str:
    if not strs:
        return ""
    for i in range(len(strs[0])):
        ch = strs[0][i]
        for s in strs[1:]:
            if i >= len(s) or s[i] != ch:
                return strs[0][:i]
    return strs[0]
```

**Horizontal:**

```python
def lcp_horizontal(strs: List[str]) -> str:
    if not strs:
        return ""
    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix
```

**Trie:**

```python
from typing import Any, Dict, List

END = "$"


def lcp_trie(strs: List[str]) -> str:
    if not strs:
        return ""
    if any(s == "" for s in strs):
        return ""
    root: Dict[str, Any] = {}
    for s in strs:
        node = root
        for ch in s:
            node = node.setdefault(ch, {})
        node[END] = True
    out: List[str] = []
    node = root
    while len(node) == 1 and END not in node:
        ch, child = next(iter(node.items()))
        out.append(ch)
        node = child
    return "".join(out)
```

### Review

The trie walk's stopping condition has two parts. `len(node) == 1` says "exactly one continuation"; `END not in node` says "and that continuation is not the end of a key." Forgetting the second part is the off-by-one trap (Lecture 1, Bug 4): for `["car", "carry"]`, the walk stops at the `r` node because it is a terminal — even though it has one child `y`. The LCP is `"car"`, not `"carr"`.

For `["car", "carry", "carryon"]`, same story — the `r` node is a terminal; LCP is `"car"`.

Verify on the three example cases:

- `["flower", "flow", "flight"]` → vertical stops at i=2 (mismatch `o` vs `i`); LCP is `"fl"`. Horizontal: prefix starts at `"flower"`; first comparison is with `"flow"` — `flow.startswith("flower")` is False; shrink to `"flowe"`; False; `"flow"`; True. Move on; compare `"flow"` and `"flight"`; shrink to `"flo"`; False; `"fl"`; True. Final: `"fl"`. Trie: root has only `f`; `f` has only `l`; `l` has `o` and `i` (two children); stop; result `"fl"`.
- `["dog", "racecar", "car"]` → vertical at i=0: `d` vs `r` mismatch; return `""`. Trie: root has `{d, r, c}` — three children; stop immediately; result `""`.
- `[""]` → trie short-circuits on the empty-string check; result `""`.

### Evaluate

- **Vertical / horizontal:** `O(n * L)` time where `L` is the length of the LCP (vertical bounds early on mismatch; horizontal shrinks the prefix). Space `O(L)` for the output.
- **Trie:** `O(N)` time + `O(N)` space where `N = sum(len(s) for s in strs)`. Heavier in absolute terms; generalizes to the multi-query case.
- **Default:** vertical scan for one-shot LC 14. Trie when the dictionary is reused across many queries or grows over time. The interview senior signal is naming both.

---

## How to use these solutions

Read them only after your own attempts. The point of UMPIRE is the *recognition rep* — the muscle of looking at a problem and saying "trie, dict-of-dict, here is the time bound" before the implementation begins. If you read the SOLUTIONS file first, you skip the recognition rep, and Mock #2 will catch you.

For the mini-project, model your write-ups on these. The Match section is the discriminating part — name the pattern, the sub-shape, and the alternative you rejected. The Implement section is the second-most-discriminating part — the code should match the structure of the solutions here, not just produce the right output.

Once all three exercises are committed and recorded, move to [Challenge 1 — Word Search II](../challenges/challenge-01-word-search-ii.md).
