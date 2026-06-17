# Challenge 2 — Replace Words (LeetCode 648)

> **Difficulty:** Medium. **Target solve time:** 40 minutes including UMPIRE write-up.

The canonical "shortest-prefix-root" problem. The trie idiom is direct, but the recognition cue is subtle — the phrase "replace each word by its shortest root in this dictionary" is exactly the trigger for "build a trie, then walk each query character by character until you hit a terminal."

---

## Problem spec

In English, a **derivative** is a word formed by adding a suffix to a shorter word called a **root**. For example, when the root `"help"` is followed by the suffix `"ful"`, we form the derivative `"helpful"`.

Given a dictionary consisting of many roots and a sentence consisting of words separated by spaces, replace every word in the sentence with its shortest root. If a word has more than one valid root, replace it with the **shortest one**. If no root in the dictionary forms it, leave the word unchanged.

Return the modified sentence.

**Constraints (LeetCode):**

- `1 <= len(dictionary) <= 1000`.
- `1 <= len(root) <= 100` for each root in `dictionary`.
- All roots consist of lowercase English letters and are unique.
- `1 <= len(sentence) <= 10^6`.
- `sentence` consists of only lowercase English letters and spaces.
- `1 <= len(word) <= 1000` for each word in `sentence`.

**Examples:**

```
Input:  dictionary = ["cat", "bat", "rat"]
        sentence = "the cattle was rattled by the battery"
Output: "the cat was rat by the bat"
```

```
Input:  dictionary = ["a", "b", "c"]
        sentence = "aadsfasf absbs bbab cadsfafs"
Output: "a a b c"
```

---

## 30-second pattern-recognition memo

```markdown
> **30-second pattern-recognition memo (trie-shortest-prefix):**
> This is a "shortest-prefix-from-dictionary" problem because we are asked to
> replace each word by its shortest dictionary root that is a prefix. Trie of
> roots. Per query word, walk the trie character by character; stop on the
> first END or on a missing child. Why not iterate roots: O(W * L * N) over N
> words in the sentence; trie is O(N * L) total. Edge model: if no root found,
> leave the word unchanged. Output: rejoin with spaces.
```

---

## The intended algorithm

```python
from typing import Any, Dict, List


END = "$"


def replace_words(dictionary: List[str], sentence: str) -> str:
    """Replace each word in `sentence` by its shortest dictionary root."""
    trie = _build_trie(dictionary)
    words = sentence.split(" ")
    out: List[str] = [_shortest_root(word, trie) for word in words]
    return " ".join(out)


def _build_trie(roots: List[str]) -> Dict[str, Any]:
    """Build a trie of roots."""
    root_node: Dict[str, Any] = {}
    for root in roots:
        node = root_node
        for ch in root:
            node = node.setdefault(ch, {})
        node[END] = True
    return root_node


def _shortest_root(word: str, trie: Dict[str, Any]) -> str:
    """Return the shortest trie root that is a prefix of `word`; else `word`."""
    node = trie
    out: List[str] = []
    for ch in word:
        if ch not in node:
            return word
        out.append(ch)
        node = node[ch]
        if END in node:
            return "".join(out)
    return word
```

---

## Walk-through

Input: `dictionary = ["cat", "bat", "rat"]`, `sentence = "the cattle was rattled by the battery"`.

Build the trie: root has children `{c, b, r}`; each has a single subtree ending in `END` at the third character.

Process each word:

- `"the"`: trie root has no `t` child; return `"the"` unchanged.
- `"cattle"`: walk `c -> a -> t`; at `t`, `END in node`; return `"cat"`.
- `"was"`: trie root has no `w` child; return `"was"` unchanged.
- `"rattled"`: walk `r -> a -> t`; `END`; return `"rat"`.
- `"by"`: no `b -> y`. After `b`, the trie node has `{a: ...}`; `y` not in node; return `"by"`.
- `"the"`: same as before; return `"the"`.
- `"battery"`: walk `b -> a -> t`; `END`; return `"bat"`.

Rejoin: `"the cat was rat by the bat"`.

---

## Complexity defense

> "**Time is `O(D + N)`** where `D = sum(len(root) for root in dictionary)` is the trie build cost and `N = len(sentence)` is the total character count of the sentence. Each character of the sentence is examined at most once during the walk; the walk stops on the first `END` or missing child. **Space is `O(D)`** for the trie plus `O(N)` for the split / rejoin. **Trade against iterating roots per word:** that approach is `O(W * L * S)` where `W` is the dictionary size, `L` is the longest root, and `S` is the number of words in the sentence — for the LC 648 upper bound, that is `1000 * 100 * 10^4 = 10^9` — too slow. The trie is `O(D + N)` — about `10^5 + 10^6 = 10^6`, three orders of magnitude faster."

---

## A variant: longest root

A common interviewer follow-up: "What if we wanted the *longest* root instead of the shortest?" The change is minimal — track the most recent `END` seen during the walk, and return the path up to that point at the end of the walk:

```python
def _longest_root(word: str, trie: Dict[str, Any]) -> str:
    node = trie
    out: List[str] = []
    last_end = -1
    for i, ch in enumerate(word):
        if ch not in node:
            break
        out.append(ch)
        node = node[ch]
        if END in node:
            last_end = i + 1
    return "".join(out[:last_end]) if last_end != -1 else word
```

The change is the `last_end` tracker; the rest is identical. Mention this in the Evaluate section.

---

## Recommended write-up structure

Under `umpire-writeups/c2-week-09/challenges/replace-words.md`:

```markdown
# Replace Words — UMPIRE Write-up

> **30-second pattern-recognition memo (trie-shortest-prefix):**
> [the memo from above, verbatim]

## Understand
... restate the problem, walk one example.

## Match
... trie of roots; per query, walk and stop at the first END.

## Plan
... build the trie; split the sentence; walk each word; rejoin.

## Implement
... the code above.

## Review
... trace on the LC 648 example.

## Evaluate
... O(D + N) time, O(D) space; mention the longest-root variant.
```

A clean write-up should be under 300 lines and read aloud in 8-10 minutes.

---

## Acceptance criteria

A complete challenge write-up has, at minimum:

- The 30-second pattern-recognition memo at the top.
- Full UMPIRE — six sections.
- The implementation in your portfolio repo at `challenges/replace-words.py`.
- A test run showing all LC 648 sample cases pass.
- Mention of the longest-root variant in the Evaluate section.

After the write-up is pushed (or if you skip this stretch), move on to the [mini-project](../07-mini-project/00-overview.md).
