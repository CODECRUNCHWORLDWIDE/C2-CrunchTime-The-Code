# Week 9 — Resources

Every resource is **free** and **publicly accessible**.

## Required reading (work it into your week)

- **`dict` — Mapping protocol, Python docs**: <https://docs.python.org/3/library/stdtypes.html#mapping-types-dict> — the trie in its dict-of-dict form is *all* dict. Reread the "Mapping Types" section if any of `dict.setdefault`, `dict.get`, or the nested-update semantics feel uncertain.
- **`collections.defaultdict` — Python docs**: <https://docs.python.org/3/library/collections.html#collections.defaultdict> — useful in the `TrieNode` class form when you want children to materialize on first access without writing `if k not in node.children: ...`.
- **Trie — Wikipedia**: <https://en.wikipedia.org/wiki/Trie> — the textbook reference. Read the "Operations" and "Implementation" sections. The drawings in the "Operations" section are the cleanest free trie pictures on the open web.
- **Aho-Corasick algorithm — Wikipedia**: <https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm> — required for the Lecture 2 §3 read. The "Goto function" and "Failure function" sections are the two paragraphs to absorb; the rest is reference. Do not panic at the pseudocode — you are reading for intuition, not implementation.
- **Knuth-Morris-Pratt algorithm — Wikipedia**: <https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm> — required for Lecture 3. The "Failure function" worked example on the string `ABABAC` is the clearest one in free material.
- **Z algorithm — Codeforces blog**: <https://codeforces.com/blog/entry/3107> — required for Lecture 3 §4. A short readable explanation by a competitive-programming author; the worked example is enough to internalize the Z-array.
- **PEP 8 (recurring)**: <https://peps.python.org/pep-0008/>
- **Big-O Cheat Sheet (recurring)**: <https://www.bigocheatsheet.com/>

## On the pattern itself

A trie is described under many names. The recognition skill is mapping the surface form to the underlying pattern:

- **Trie** — the textbook data structure. A rooted tree whose edges are labeled by single characters; paths from the root spell out the stored keys.
- **Prefix tree** — synonym for trie; the more descriptive name. Use whichever the prompt uses.
- **Digital tree, radix tree, retrieval tree** — older or compressed variants. Out of scope; mentioned only so you can name them.
- **Dict-of-dict trie** — the idiomatic Python form. `root: Dict[str, Any] = {}`; nested dicts; `END = "$"` (or `True`) as the terminal sentinel. Less code than the class form; mutates in place.
- **`TrieNode` class trie** — the strongly-typed form. `class TrieNode: children: Dict[str, TrieNode]; is_end: bool`. Preferred when attaching per-node metadata (word frequency, payload, etc.) or porting to a typed language.
- **Compressed trie / Patricia trie / radix tree** — the trie with single-child chains collapsed into edges with multi-character labels. Saves space; out of scope for entry-level interviews; mentioned as a stretch.
- **Autocomplete** — the prefix-walk application. Given a prefix, enumerate all stored keys with that prefix.
- **Longest-common-prefix (LCP)** — the descent application. Walk from the root while every node has exactly one child *and* is not a terminal; the path so far is the LCP.
- **Word break** — the trie + memo composition. Use the trie to enumerate valid word boundaries from each position; memoize on position.
- **Dictionary-on-grid** — the trie + backtracking composition. Walk the grid in DFS, descending the trie character-by-character; backtrack when the current character is not a child.
- **Multi-pattern substring matching** — the Aho-Corasick application. Given a long text and many short patterns, find every occurrence in `O(n + m + z)`.

If a write-up mentions "given a dictionary," "prefix search," "autocomplete," "starts with," "shortest root for each word," "find all words from a list on a grid," or "longest word that begins with a given string" — it is almost certainly a trie problem. If it mentions "find the first occurrence of a substring with `len(haystack) * len(needle)` too large" — it is KMP or Z (or, in production, `str.find`).

## Free practice platforms

- **LeetCode — Trie tag** (free): <https://leetcode.com/tag/trie/>
- **LeetCode — Implement Trie (Prefix Tree)** (LC 208): <https://leetcode.com/problems/implement-trie-prefix-tree/> — the canonical trie problem; Exercise 1 exactly.
- **LeetCode — Word Search II** (LC 212): <https://leetcode.com/problems/word-search-ii/> — the canonical trie-on-grid problem; Challenge 1 exactly.
- **LeetCode — Implement strStr()** (LC 28): <https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/> — the canonical exact-substring-matching problem; KMP reference implementation lives here.
- **LeetCode — String Matching tag** (free): <https://leetcode.com/tag/string-matching/>
- **HackerRank — Tries domain**: <https://www.hackerrank.com/domains/data-structures?filters%5Bsubdomains%5D%5B%5D=trie>
- **Codeforces — Strings tag**: <https://codeforces.com/problemset?tags=strings>
- **CSES Problem Set — String Algorithms section**: <https://cses.fi/problemset/> — the canonical curated set; several problems whose intended solution is a trie, KMP, or Z.

## On the trie API specifically

The three operations you should know cold.

| Operation | Signature | Complexity | One-liner mnemonic |
|-----------|-----------|-----------:|--------------------|
| `insert(word)` | walk + create children | `O(L)` | one node per character |
| `search(word)` | walk; return True iff `is_end` | `O(L)` | mismatch fails fast |
| `starts_with(prefix)` | walk; return True iff path exists | `O(P)` | terminal not required |
| autocomplete(prefix) | walk to prefix; DFS, collect words | `O(P + Q)` | Q = total output size |

Three observations:

1. **`O(L)` worst-case, not expected.** A hash set answers exact-match in `O(L)` *expected* but `O(n)` *worst-case* under collisions. A trie answers in `O(L)` *worst-case* — the path length is the key length, period.
2. **Prefix queries are free.** A hash set cannot answer "does any stored key start with `pre`" without a full scan. A trie answers it in `O(P)` where `P = len(pre)`. This is the discriminating capability.
3. **Insertion order does not matter.** Two tries built from the same set of keys in different orders are identical — the structure is determined entirely by the key set.

### The canonical dict-of-dict trie

```python
from typing import Dict, Any, List

END = "$"  # sentinel character; any character not in the alphabet works

def make_trie(words: List[str]) -> Dict[str, Any]:
    """Build a trie from a list of words."""
    root: Dict[str, Any] = {}
    for word in words:
        node = root
        for ch in word:
            node = node.setdefault(ch, {})
        node[END] = True
    return root


def search(root: Dict[str, Any], word: str) -> bool:
    """Return True if `word` was inserted into the trie."""
    node = root
    for ch in word:
        if ch not in node:
            return False
        node = node[ch]
    return END in node


def starts_with(root: Dict[str, Any], prefix: str) -> bool:
    """Return True if any stored key has `prefix` as a prefix."""
    node = root
    for ch in prefix:
        if ch not in node:
            return False
        node = node[ch]
    return True
```

Twenty lines including the helpers. Memorize the shape. The `setdefault(ch, {})` call in `make_trie` is the line beginners forget — without it, you write the four-line "create-if-missing" boilerplate by hand.

### The canonical `TrieNode` class trie

```python
from typing import Dict, Optional


class TrieNode:
    """Single node in a trie."""

    def __init__(self) -> None:
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end: bool = False


class Trie:
    """Trie with insert, search, and starts_with."""

    def __init__(self) -> None:
        self.root: TrieNode = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        return self._walk(prefix) is not None

    def _walk(self, s: str) -> Optional[TrieNode]:
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node
```

Thirty lines. The class form is more verbose but more readable when you want to attach metadata. For interviews, pick the form that matches the prompt; for portfolio, picking dict-of-dict shows you know idiomatic Python.

## On the autocomplete walk

The canonical implementation.

```python
from typing import Dict, Any, List

END = "$"


def autocomplete(root: Dict[str, Any], prefix: str) -> List[str]:
    """Return all stored keys with `prefix` as a prefix."""
    node = root
    for ch in prefix:
        if ch not in node:
            return []
        node = node[ch]
    out: List[str] = []
    _collect(node, prefix, out)
    return out


def _collect(node: Dict[str, Any], path: str, out: List[str]) -> None:
    """DFS from `node`, accumulating `path`; emit when END is reached."""
    if END in node:
        out.append(path)
    for ch, child in node.items():
        if ch == END:
            continue
        _collect(child, path + ch, out)
```

The walk is `O(P + Q)` where `P = len(prefix)` and `Q = sum(len(w) for w in matches)`. The `O(P)` is the descent to the prefix node; the `O(Q)` is the DFS over the subtree.

Two things beginners get wrong:

1. **Forgetting to skip the `END` key in the DFS loop.** `END = "$"` is stored as a dict key; iterating `node.items()` will produce it; descending into `True` will crash. Skip it explicitly.
2. **Building strings via `path + ch` versus a list-and-join.** For interview code, `path + ch` is fine. For million-character outputs, the list-and-join pattern is `O(n)` not `O(n²)`. Mention the trade-off in the write-up.

## On the word-break composition

The trie + memo pattern.

```python
from typing import Dict, Any, List

END = "$"


def make_trie(words: List[str]) -> Dict[str, Any]:
    root: Dict[str, Any] = {}
    for word in words:
        node = root
        for ch in word:
            node = node.setdefault(ch, {})
        node[END] = True
    return root


def word_break(s: str, words: List[str]) -> bool:
    """Return True if s can be segmented into space-separated words from `words`."""
    trie = make_trie(words)
    memo: Dict[int, bool] = {}
    return _can_break(s, 0, trie, memo)


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

Thirty-five lines. The discipline here is that the trie keeps the inner loop honest at `O(L)` (one descent per character) rather than `O(W L)` (iterating all words from each position). The asymptotic improvement is real when the dictionary has many overlapping prefixes (e.g., `["a", "ap", "app", "appl", "apple"]`).

The time is `O(n²)` where `n = len(s)`: each position `i` does at most one descent of length `n - i`. Space is `O(n + W L)` where `W L` is the trie size.

## On Aho-Corasick (read only, not implemented)

The two paragraphs to absorb.

> **Aho-Corasick** augments a trie of patterns with **failure links** — each node `v` has a failure link to the longest *proper suffix* of `v`'s path that is also a prefix in the trie. With failure links in place, the algorithm processes the input text once, character by character, never moving the text pointer backward: at each character, either descend if a child matches or follow failure links until a child does match (or until reaching the root). Every node visited along the failure links corresponds to a pattern match ending at the current text position. The total work is `O(n + m + z)` where `n` is the text length, `m` is the total pattern length, and `z` is the number of matches reported.

> The classical application is **multi-pattern substring matching** — given one long text and a fixed set of patterns, find every occurrence of every pattern. Use cases include intrusion-detection signature scanners (Snort), spam-filter token matchers, plagiarism detectors, and the original `fgrep` implementation. For LeetCode purposes, recognize the trigger phrase ("many patterns, one text") and mention Aho-Corasick as the right tool; you will rarely be asked to implement it under interview pressure.

You will not implement Aho-Corasick this week. The read-level outcome is: (1) you can name the algorithm when the prompt fits; (2) you can describe the failure-link idea in one sentence; (3) you can defend `O(n + m + z)` over the naive `O(nm + nW)` baseline where `W` is the number of patterns. Three sentences total. That is the interview register.

## On KMP

The canonical reference implementation.

```python
from typing import List


def build_failure(pattern: str) -> List[int]:
    """Build the KMP failure function (a.k.a. prefix function).

    fail[i] = length of the longest proper prefix of pattern[:i+1]
    that is also a suffix of pattern[:i+1].
    """
    fail: List[int] = [0] * len(pattern)
    k = 0
    for i in range(1, len(pattern)):
        while k > 0 and pattern[k] != pattern[i]:
            k = fail[k - 1]
        if pattern[k] == pattern[i]:
            k += 1
        fail[i] = k
    return fail


def kmp_search(text: str, pattern: str) -> int:
    """Return the index of the first occurrence of pattern in text, or -1."""
    if not pattern:
        return 0
    fail = build_failure(pattern)
    j = 0  # index into pattern
    for i, ch in enumerate(text):
        while j > 0 and pattern[j] != ch:
            j = fail[j - 1]
        if pattern[j] == ch:
            j += 1
        if j == len(pattern):
            return i - j + 1
    return -1
```

Thirty lines total. The two loops have one beginner pitfall each:

1. **In `build_failure`, the inner `while` is on `pattern[k]`, not `pattern[i]`.** Reversing this is the canonical bug.
2. **In `kmp_search`, the text pointer `i` never moves backward.** It is the outer `for` loop variable; the inner `while` only adjusts `j`. This is the linear-time guarantee.

Time is `O(n + m)`: each iteration either advances `i` (which monotonically increases to `n`) or decreases `j` (which is bounded by `n + m` over the run). Space is `O(m)` for the failure array.

## On the Z-algorithm

The companion to KMP. Same `O(n + m)`, slightly different bookkeeping. Used most commonly in competitive programming; rarely asked in industry interviews but worth recognizing.

```python
from typing import List


def z_array(s: str) -> List[int]:
    """Build the Z-array: z[i] = length of the longest substring starting at i
    that matches a prefix of s. By convention, z[0] = len(s).
    """
    n = len(s)
    z: List[int] = [0] * n
    z[0] = n
    l, r = 0, 0  # current Z-box: s[l:r+1] matches s[0:r-l+1]
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z


def z_search(text: str, pattern: str) -> int:
    """Return the index of the first occurrence of pattern in text, or -1."""
    if not pattern:
        return 0
    sep = "\x01"  # any character not in the alphabet
    combined = pattern + sep + text
    z = z_array(combined)
    m = len(pattern)
    for i in range(m + 1, len(combined)):
        if z[i] >= m:
            return i - m - 1
    return -1
```

Twenty-five lines. The Z-array of `pattern + sep + text` yields the matches: any position `i` in the `text` portion with `z[i] >= len(pattern)` is the start of a match.

For interview purposes, mention Z as the sibling of KMP. Implementation parity is rarely required; recognition parity is.

## On `str.find` and `in` in CPython

A grounding note that comes up in senior interviews.

CPython 3.10+ uses a tuned hybrid algorithm for `str.find`, `bytes.find`, and the `in` operator on strings. The implementation lives in `Objects/stringlib/fastsearch.h` and is based on a **two-way string-matching algorithm** combined with a **bitap precomputation** for short patterns. The change was added in Python 3.10 (PEP 657 era; the actual implementation is in CPython issue 23690 and the GH-91113 follow-ups) and gives a **linear-time worst-case guarantee** that earlier versions did not have.

The interview-grade takeaway: in production Python 3.10+, `text.find(pattern)` and `pattern in text` are linear-time and tuned. Reaching for a hand-rolled KMP is for the *interview narrative*, not for production code. Senior candidates name both:

> "If this were production, I would use `text.find(pattern)` — CPython 3.10+ guarantees linear time. For the interview, here is the KMP."

That sentence is the discriminator.

## Videos on the pattern (free, no signup)

- **NeetCode — "Implement Trie (Prefix Tree)"** (YouTube — free): search "neetcode trie 208"; the 12-minute walkthrough is enough for the dict-of-dict template.
- **NeetCode — "Word Search II"** (YouTube — free): the canonical trie-on-grid; if you have not seen the pattern in video form, watch this before Challenge 1.
- **William Fiset — "Trie data structure"** (YouTube — free): a slower, more visual walkthrough; good for the autocomplete subtree.
- **MIT 6.006 — Lecture on string matching** (free OCW): <https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/> — Lecture 16 covers KMP and the failure function with the textbook level of rigor.
- **Tushar Roy — "KMP Substring Pattern Search"** (YouTube — free): the clearest free walkthrough of the failure-function construction; about 18 minutes.

## On the dict-of-dict vs class form choice

A short cheat sheet.

| When | Prefer | Why |
|------|--------|-----|
| Small interview problem with no per-node state | dict-of-dict | Less code; more Pythonic |
| Per-node metadata (frequency, payload, index) | `TrieNode` class | Cleaner attribute syntax; type-checker friendlier |
| Porting to Java / C++ later | `TrieNode` class | Mirrors the typed-language form |
| Need to serialize the trie | dict-of-dict | `json.dumps(trie)` works out of the box (if `END` is JSON-safe) |
| Million-key trie in a long-running service | `TrieNode` with `__slots__` | Slot-class memory savings; pre-allocated children dict |
| Memory-tight embedded use | compressed trie (Patricia) | Out of scope for the week |

For Mock #2, default to dict-of-dict unless the prompt clearly wants per-node state. The dict form is faster to write and reads more like the textbook description, which the interviewer can follow without parsing extra class scaffolding.

## Glossary cheat sheet

Keep this tab open. Builds on Weeks 1-8.

| Term | One-line definition |
|------|---------------------|
| **Trie** | A rooted tree whose edges are labeled by single characters; paths spell out the keys |
| **Prefix tree** | Synonym for trie; the more descriptive name |
| **Dict-of-dict trie** | Idiomatic Python trie form; nested dicts; `END = "$"` as terminal sentinel |
| **`TrieNode` class** | Strongly-typed trie form; `children: Dict[str, TrieNode]; is_end: bool` |
| **`insert(word)`** | Walk the trie from the root, creating children as needed; mark `is_end` at the terminal node; `O(L)` |
| **`search(word)`** | Walk the trie; return True iff terminal is reached and `is_end` is True; `O(L)` |
| **`starts_with(prefix)`** | Walk the trie; return True iff the path exists (terminal not required); `O(P)` |
| **Autocomplete walk** | DFS from the prefix node, accumulating characters; emit when `is_end` is True; `O(P + Q)` |
| **Longest-common-prefix** | The path descended while every node has exactly one child and is not terminal |
| **Word break** | Compose a trie + memoization to determine if a string segments into dictionary words |
| **Aho-Corasick** | Trie + failure links for multi-pattern substring matching; `O(n + m + z)`; read only this week |
| **Failure link / suffix link** | In Aho-Corasick, the link from a node to the longest proper suffix that is also a prefix in the trie |
| **KMP** | Knuth-Morris-Pratt; exact-substring matching in `O(n + m)` via the failure function |
| **Failure function (KMP)** | `fail[i] = length of the longest proper prefix of pattern[:i+1] that is also a suffix` |
| **Z-algorithm** | Sibling of KMP; `z[i] = length of the longest substring starting at i that matches a prefix of s` |
| **Z-array** | The output of the Z-algorithm; same `O(n + m)` matching capability as KMP |
| **`str.find` / `in`** | CPython 3.10+ uses two-way + bitap; linear-time worst-case; the production answer for substring search |

## What you will be glad you read

Three things, all short, all this week:

1. **The Wikipedia "Trie" article — `Operations` and `Implementation` sections** — about 15 minutes. The cleanest free trie pictures.
2. **The Wikipedia "Knuth-Morris-Pratt algorithm" worked example on `ABABAC`** — about 10 minutes. Where the failure function "clicks."
3. **Two LeetCode problem statements at the "Trie" tag** — five minutes each. Predict the algorithm before reading the solution. The recognition reps are what build Match-step muscle.

If you read nothing else this week, read those three and skim five problem titles in the LeetCode Trie tag.

---

*Broken link? Open an issue.*
