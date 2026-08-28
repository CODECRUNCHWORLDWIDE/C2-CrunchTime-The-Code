# Week 9 — Homework

Six practice problems plus the rubric. Allow ~5 hours total. Do the problems on your own with the lectures *closed*; consult the lecture or the resources only after a 15-minute stuck-period on a single problem.

The problems are chosen to drill the six Week-9 sub-patterns: trie API, autocomplete, word-break variant, KMP, trie + DFS, and trie-shortest-prefix. By Sunday, the recognition step on each should be reflexive.

| # | Problem | Pattern | Source | Est. time |
|---|---------|---------|--------|----------:|
| 1 | Design Add and Search Words Data Structure | Trie + wildcard recursion | LeetCode 211 | 45 min |
| 2 | Longest Word in Dictionary | Trie + BFS / DFS over the trie | LeetCode 720 | 35 min |
| 3 | Repeated Substring Pattern | KMP failure-function application | LeetCode 459 | 40 min |
| 4 | Stream of Characters | Reverse-trie + streaming match | LeetCode 1032 | 50 min |
| 5 | Concatenated Words | Trie + DP composition | LeetCode 472 | 60 min |
| 6 | Implement Magic Dictionary | Trie + one-character-edit recursion | LeetCode 676 | 40 min |

Problems 1, 2, and 6 are the high-yield trie drills; problem 3 is the KMP rep; problem 4 is the streaming/reverse-trie composition; problem 5 is the trie + DP composition that combines two Week-9 primitives.

---

## Problem 1 — Design Add and Search Words Data Structure (LC 211)

**Spec.** Design a data structure that supports two operations: `add_word(../word)` adds a word; `search(../word)` returns True if any added word matches `word`, where `word` may contain the character `'.'` matching any single character.

**Constraints.** `1 <= len(../word) <= 25`; `add_word` consists of lowercase letters; `search` may contain `'.'`; up to `10^4` calls.

**Pattern.** Trie + wildcard recursion. The `'.'` triggers a recursive descent into every child at that level.

**Hint.** `class WordDictionary: def __init__(../self): self.root: Dict[str, Any] = {}`. `add_word` is the canonical insert. `search` is a recursive helper that, at each level, either descends on the specific character or — if the character is `'.'` — iterates every child and recurses, returning True if any branch returns True.

**Acceptance.** Function signature `class WordDictionary: def add_word(self, word: str) -> None; def search(self, word: str) -> bool`. Time: `O(../L)` for `add_word`; `O(26^d * L)` worst case for `search` where `d` is the number of `'.'` characters. Space: `O(../N)` for the trie.

**Variant.** What if the alphabet were Unicode? The `26` becomes the alphabet size; the asymptotic is unchanged. Mention in the write-up.

---

## Problem 2 — Longest Word in Dictionary (LC 720)

**Spec.** Given a list of strings, return the longest word in the list that can be built one character at a time by other words from the list. If more than one tie, return the lexicographically smallest.

**Constraints.** `1 <= len(../words) <= 1000`; `1 <= len(../word) <= 30`.

**Pattern.** Trie + BFS or DFS over the trie. Sort the words first to break ties; then for each word, check whether every prefix is in the trie (i.e., every prefix has `END` marked).

**Hint.** Sort by `(../-len(w), w)`; build the trie; iterate sorted words; for each word, walk the trie and check `END in node` at every step except the root. The first word that passes the check is the answer.

**Acceptance.** Function signature `longest_word(words: List[str]) -> str`. Time: `O(N log N + N L)` where `N = len(../words)` and `L` is the longest word length. Space: `O(sum of lengths)`.

**Variant.** Alternative without sorting: BFS over the trie, level by level, tracking the longest fully-marked path. The BFS version is one pass over the trie and asymptotically slightly faster on dense inputs; the sort version is shorter to write.

---

## Problem 3 — Repeated Substring Pattern (LC 459)

**Spec.** Given a string `s`, return True if `s` can be constructed by taking a substring of it and appending multiple copies of that substring together.

**Constraints.** `1 <= len(../s) <= 10^4`; lowercase English letters.

**Pattern.** KMP failure-function application. Build `fail` on `s`; let `n = len(../s)`. Then `s` is a repeat iff `n % (n - fail[n - 1]) == 0` and `fail[n - 1] > 0`.

**Hint.** The period of a string is `n - fail[n - 1]` (the difference between the string length and the longest proper prefix-suffix). The string is a repeat iff the period divides the length.

**Acceptance.** Function signature `repeated_substring_pattern(s: str) -> bool`. Time: `O(../n)`. Space: `O(../n)` for the failure array.

**Variant.** The folk-trick alternative: `s in (s + s)[1:-1]` is `O(../n)` in CPython 3.10+ thanks to the two-way matcher; mention as the production answer. The KMP version is the explicit-defense form.

---

## Problem 4 — Stream of Characters (LC 1032)

**Spec.** Design a data structure with two methods: `__init__(../words)` initializes with a list of words; `query(../letter)` records `letter` and returns True if any suffix of the current stream is in `words`.

**Constraints.** `1 <= len(../words) <= 2000`; `1 <= len(../word) <= 200`; up to `4 * 10^4` query calls.

**Pattern.** Reverse-trie. Build a trie of the *reversed* words; on each query, walk the reversed accumulated stream against the trie and return True if any path reaches an `END`.

**Hint.** Storing reversed words lets us match suffixes by walking the stream backwards. The query buffer grows; truncate it to the longest word's length to bound memory.

**Acceptance.** Function signature `class StreamChecker: def __init__(self, words: List[str]); def query(self, letter: str) -> bool`. Time per query: `O(../L)` where `L` is the longest word. Space: `O(W L)` for the trie + `O(../L)` for the buffer.

**Variant.** Aho-Corasick is the heavier-weight answer: build an Aho-Corasick automaton from the patterns, then process the stream character by character. Mention by name; do not implement.

---

## Problem 5 — Concatenated Words (LC 472)

**Spec.** Given a list of strings, return all strings that can be formed by concatenating at least two other strings from the list.

**Constraints.** `1 <= len(../words) <= 10^4`; `1 <= sum(../len(w) for w in words) <= 10^5`; lowercase English letters.

**Pattern.** Trie + DP. For each word, run the Word Break check (Exercise 2) against the trie of all *other* words; if it segments into at least two pieces, include it.

**Hint.** Build the trie once from all words. For each word `w`, run a modified Word Break that requires segmentation into at least *two* pieces (not just one); collect the words for which the modified check returns True. The "at least two pieces" requires not counting the word itself as a one-piece trivial segmentation; the cleanest fix is to require `i > 0 or j < len(../w)` at the recursive emit.

**Acceptance.** Function signature `find_all_concatenated_words(words: List[str]) -> List[str]`. Time: `O(../sum(len(w))^2)`. Space: `O(../sum(len(w)))`.

**Variant.** Sorting words by length first lets the DP build up smaller-word answers before checking longer words; this is a recognition optimization that earns senior signal in the write-up.

---

## Problem 6 — Implement Magic Dictionary (LC 676)

**Spec.** Design a data structure that supports `build_dict(../dict)` and `search(../word)`. `search(../word)` returns True iff there is *exactly one* character in `word` that can be replaced to make the result a stored word.

**Constraints.** `1 <= len(../words) <= 100`; `1 <= len(../word) <= 100`; up to `100` searches.

**Pattern.** Trie + one-character-edit recursion. The recursion tracks "edits used so far" (0 or 1); on a character match it descends with the same edit count; on a mismatch it descends into every other child (consuming the one allowed edit).

**Hint.** Recursive helper `match(node, i, edits_used)`: base case `i == len(../word)` returns True iff `END in node` and `edits_used == 1`. On character match, recurse with the same `edits_used`. If `edits_used == 0`, also try every other child with `edits_used = 1`.

**Acceptance.** Function signature `class MagicDictionary: def build_dict(self, dict: List[str]) -> None; def search(self, word: str) -> bool`. Time per `search`: `O(L * 26)` worst case where `L = len(../word)`. Space: `O(sum of dictionary word lengths)`.

**Variant.** Two-character-edit (../Levenshtein-1) is the natural generalization; same recursion with an `edits_used` budget of up to 2 and a richer branching (insert / delete / substitute). Out of scope but worth mentioning.

---

## Rubric

For each problem, your write-up is graded on five dimensions:

| Dimension | Weight | What "yes" looks like |
|-----------|-------:|----------------------|
| Research constraints (pattern recognition) | 25% | 30-second memo at the top; pattern named in one of the six families; alternative rejected with reason |
| Assess options | 15% | Numbered steps; data structure choice stated; recursion / iteration form noted |
| Make the solution (../correctness) | 25% | All LC sample cases pass; no off-by-one; the canonical bug list checked |
| Make the solution (../style) | 10% | Type hints everywhere; docstrings on every function; PEP 8; idiomatic Python |
| Examine (../defense) | 25% | Time + space bounds with derivation; one variant mentioned; trade against the alternative algorithm stated |

The Research constraints weight is the highest for a reason. Phase 2 grades recognition heavily; you can have a working implementation and still lose the rep if you cannot defend the choice over the alternative.

---

## Suggested order

1. **Problem 1** first — it cements the trie API with a new operation (`search` with wildcards). This is the highest recognition density of the six.
2. **Problem 6** second — Magic Dictionary is structurally similar to Problem 1 (trie + recursion) and the lift is small once Problem 1 is fluent.
3. **Problem 2** third — Longest Word in Dictionary is a clean trie-walk problem; do it as a recognition rep on the `END`-at-every-step pattern.
4. **Problem 3** fourth — Repeated Substring Pattern is the KMP rep. Aim for 40 minutes; the failure-function bookkeeping is the entire trick.
5. **Problem 4** fifth — Stream of Characters is the trick-stretch (../reverse-trie); leave 50 minutes.
6. **Problem 5** last — Concatenated Words is the composition; the longest at 60 minutes. Save for the latter half of the week.

If time runs out, prioritize Problems 1, 3, and 5. They are the three patterns most likely to appear on Mock #2.

---

## Acceptance

The week's homework is complete when:

- All six problems have a committed implementation under `homework/c2-week-09/`.
- All six problems have a FRAME write-up under `frame-writeups/c2-week-09/homework/`.
- The quiz is taken and scored.
- The score is in the retrospective: which sub-pattern needs the most reps before Mock #2.

The retrospective is the single most useful artifact this week. The pattern most candidates need more reps on after W9 is "KMP recognition under interview pressure" — the failure-function defense is short but easy to flub on the spot. Drill it in writing, then drill it aloud.
