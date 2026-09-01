# Week 9 — Tries and Advanced Strings

```
┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐
│ F │  │ R │  │ A │  │ M │  │ E │
└───┘  └───┘  └───┘  └───┘  └───┘
```

> *Week 8 installed the heap — the `heapq` module, the size-k top-k template, the heap-of-tuples idiom, the two-heap median pattern. Week 9 installs the **trie** — the prefix tree, the dict-of-dict and Node-class forms, the autocomplete walk, the word-break with memoization, and the introductory framing for Aho-Corasick. Then a short, interview-honest tour of **KMP** and the **Z-algorithm** — when to reach for them, what the failure function is doing, and which LeetCode prompts hint at exact substring matching versus prefix queries. By Sunday you can write a trie from scratch in either form, defend `O(L)` insert / lookup against a `HashSet[str]` baseline, run autocomplete from any prefix, and explain in one sentence what KMP's failure function buys over the naive `O(nm)` scanner.*

Welcome to Week 9 of **C2 · CrunchTime — The Code** — the fifth week of Phase 2. Last week installed the priority-queue family. This week installs the **prefix-tree** family and a working interview-level grasp of two linear-time string-matching algorithms.

Tries have a curious place in the interview canon. They are not asked as often as heaps or BFS, but when they *are* asked, they discriminate sharply: candidates who have never built one tend to flounder at the dict-of-dict step and miss the `O(L)` insertion defense. Owning a clean trie template — the empty-dict root, the per-character descent, the `END` sentinel — buys you Mock-#2-passable answers on Implement Trie (LC 208), Word Search II (LC 212), Design Add and Search Words Data Structure (LC 211), Replace Words (LC 648), and a long tail of "given a dictionary, what is the shortest / longest / matching word for some query" problems.

KMP and the Z-algorithm sit in a different register. You will not implement them from scratch under interview pressure unless you are at a string-heavy team. What you *will* be asked is the Research-constraints question: *is this an exact-substring-matching problem, and is `O(n + m)` the bar?* If yes, you name KMP or Z (state the trade-off briefly), then either implement KMP if the interviewer presses or fall back to Python's `in` operator (which uses a tuned hybrid in CPython 3.10+) for production code. Knowing what each algorithm *does* and *when it applies* is the interview-grade outcome of this week; full re-derivation of the failure function is a stretch goal.

By Sunday of Week 9 you will:

- **Recognize** a trie problem in 30 seconds and classify it as **prefix-lookup / autocomplete / word-break / multi-pattern matching / dictionary-on-grid**.
- **Write** a trie in both forms from memory — the dict-of-dict form (concise, idiomatic Python) and the explicit `TrieNode` class form (closer to a Java/C++ port).
- **Walk** a trie to enumerate all keys under a prefix — the autocomplete primitive. State why the walk is `O(P + Q)` where `P` is the prefix length and `Q` is the total output size.
- **Solve** the word-break problem (LC 139) using memoization plus a trie for the dictionary, and defend why the trie keeps the inner loop honest at `O(L)` rather than `O(W L)` over a hash set of words.
- **Read** an Aho-Corasick description and explain the **suffix-link** intuition at a beginner-aware level — enough to recognize "multi-pattern substring matching" as the trigger phrase and to pick the right reading off the resources file. You will not implement Aho-Corasick this week; you will read it.
- **Solve** an exact-substring-matching problem (LC 28 — `strStr`) two ways: the naive `O(nm)` baseline and a KMP implementation cribbed from a reference. Defend the failure-function intuition out loud.
- **Recognize** when to reach for the Z-algorithm versus KMP — both linear, slightly different invariants, mostly interchangeable for LeetCode purposes.
- Have solved **three trie/string exercises** — Implement Trie, Word Break (trie + memo), and Longest Common Prefix (trie variant) — each with a FRAME write-up.
- Have shipped **one challenge** (Word Search II — the canonical trie-on-grid problem) plus an optional stretch (Replace Words — the prefix-replace variant).
- Have shipped the quiz, the homework, and the **mini-project**: one trie write-up (Implement Trie) and one KMP write-up (`strStr` with failure function), fully FRAME-narrated.

---

## Learning objectives

By the end of this week, you will be able to:

- **Match a trie problem to its pattern** in 30 seconds by recognizing the canonical signals: "given a dictionary," "prefix search," "autocomplete," "longest word that is also a prefix," "word ladder over a fixed vocabulary," "find all words from a list on a grid," "replace each word by its root."
- **Distinguish a trie from a hash set** in one sentence: a hash set answers exact-match in `O(L)` expected; a trie answers exact-match in `O(L)` worst-case **and** answers prefix queries in `O(P + Q)` where the hash set cannot answer them at all without a full scan.
- **Implement** the trie in the **dict-of-dict** form — `root: Dict[str, Any] = {}`, with `END = "$"` as the terminal sentinel — and explain why this is the cleanest Python form (less ceremony than a class hierarchy, mutates in place, reads like the textbook description).
- **Implement** the trie in the **`TrieNode` class** form — `class TrieNode: children: Dict[str, TrieNode]; is_end: bool` — and explain when the class form is preferred (when you want to attach per-node metadata, when you want explicit memory bookkeeping, when porting to a strongly-typed language).
- **Walk** a trie to enumerate all keys with a given prefix — DFS from the prefix node, accumulating characters along the path; emit the accumulated string each time `is_end` is true.
- **Implement word-break (LC 139)** with memoization plus a trie for the dictionary. Defend the asymptotic improvement over the hash-set version on inputs with many overlapping prefixes.
- **Read** an Aho-Corasick description without panic. You should be able to name three things after reading: (1) it is a trie augmented with **failure links** that point to the longest proper suffix that is also a prefix in the trie; (2) it processes the input string once, producing all pattern occurrences in `O(n + m + z)` where `z` is the number of matches; (3) its primary application is multi-pattern substring matching (intrusion detection, plagiarism scanners, virus signatures). You will not implement it this week.
- **Implement KMP** at the level of LC 28 — `strStr`. Defend the failure-function intuition: at each mismatch, jump the pattern pointer to the longest proper prefix of `pattern[:j]` that is also a suffix of `pattern[:j]`, and resume from there without ever moving the text pointer backward.
- **Recognize** when KMP applies and when it does not. KMP is the answer when the problem statement says "find the first occurrence of needle in haystack" with `len(haystack) * len(needle)` too large to brute-force. KMP is not the answer when the problem is "are these two strings anagrams" (counting/sort), "is this a palindrome" (two-pointer), or "are these strings equal up to rotation" (concatenate + search — KMP is the inner tool, but the *Research constraints* step is the rotation observation).
- **Recognize** the **Z-algorithm** as a sibling of KMP: same `O(n + m)` time, slightly different bookkeeping. The Z-array of a string `s` is `z[i] = length of the longest substring starting at i that matches a prefix of s`. You will not implement it from scratch; you will read the reference and know when to mention it.

---

## Prerequisites

- **Weeks 1-8 complete.** You have shipped four DFS / heap write-ups; you can deliver FRAME without notes on a graph-traversal or top-k problem.
- **Comfortable with Python `dict` semantics.** A trie in the dict-of-dict form is built entirely out of nested `dict[str, dict]` instances. Mutating a nested dict mutates the parent (since `dict` is a reference type). This is intentional and is the engine of the implementation.
- **Comfortable with recursion.** The trie-walk autocomplete primitive is a small DFS. You wrote larger DFS in Week 7.
- **Comfortable with the difference between *expected* and *worst-case* complexity.** Hash operations are `O(1)` *expected* — `O(n)` worst-case under pathological collisions. Trie operations are `O(L)` *worst-case* — there is no probability-of-failure mode. Interviewers ask candidates to articulate this distinction.
- **Comfortable with the `O(n + m)` framing for string matching.** "Linear in the size of the input" is the bar for KMP, Z, and Aho-Corasick. The naive scanner is `O(nm)`. Recognizing when `nm` is too large is the recognition-step prerequisite.

---

## Topics covered

- The **trie** — a rooted tree whose edges are labeled by single characters and whose paths from the root spell out the keys
- The **dict-of-dict** trie form — `root: Dict[str, Any] = {}`; `END = "$"`; idiomatic Python; mutates in place
- The **`TrieNode` class** trie form — `children: Dict[str, TrieNode]`, `is_end: bool`; preferred when attaching per-node metadata
- **`insert`, `search`, `starts_with`** — the canonical three operations, each `O(L)` where `L` is the key length
- The **autocomplete walk** — DFS from the prefix node, accumulating characters; `O(P + Q)` where `Q` is total output size
- The **longest-common-prefix** problem (LC 14) — three solutions: vertical scan, horizontal scan, trie variant; when each wins
- The **word-break** problem (LC 139) — memoization plus a trie for the dictionary; `O(n²)` time, `O(n + W L)` space where `W` is the dictionary size and `L` is the longest word
- **Aho-Corasick at a beginner-aware level** — trie + suffix links; multi-pattern substring matching; `O(n + m + z)`; **read only**, not implemented this week
- **KMP** — the failure function (longest proper prefix that is also a suffix), the `O(n + m)` scanner, the LC 28 reference implementation
- **The Z-algorithm** — `z[i] = length of longest match between s and s[i:]`; same `O(n + m)`; slightly different bookkeeping; mostly interchangeable with KMP for interview purposes
- **When to reach for which** — trie for prefix / dictionary problems; KMP or Z for exact-substring matching with `nm` too large; Aho-Corasick for multi-pattern matching with many patterns
- **Why `s in t` and `t.find(s)` are usually enough** — CPython 3.10+ uses a tuned hybrid (two-way + bitap) under the hood; the linear-time guarantee was added in 3.10. Reaching for KMP is for the *interview narrative*, not for production code

---

## Weekly schedule (intensive · 36h)

| Day | Focus | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project | Self-Study | Daily Total |
|-----|-------|---------:|----------:|-----------:|----------:|---------:|-------------:|-----------:|------------:|
| Monday | Trie basics; dict-of-dict; exercise 1 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Tuesday | Autocomplete + word-break; exercise 2 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Wednesday | KMP + Z + Aho-Corasick (read); exercise 3 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Thursday | Mini-project drafting; challenge ramp | 0h | 1h | 1h | 0.5h | 1h | 1.5h | 1h | 6h |
| Friday | Challenge (Word Search II) | 0h | 0h | 2h | 0.5h | 1h | 1.5h | 1h | 6h |
| Saturday | Mini-project — trie + KMP write-ups | 0h | 0h | 0h | 0.5h | 1h | 3h | 0h | 4.5h |
| Sunday | Quiz + retro + push | 0h | 0h | 0h | 0.5h | 0h | 4h | 0h | 4.5h |
| **Total** | | **6h** | **7h** | **3h** | **3h** | **6h** | **10h** | **3.5h** | **38.5h** |

(The week budgets ~36 hours; the table sums slightly higher to absorb the Phase-2 ramp. Drop 0.5h from Self-Study if 36h is your hard cap.)

**Mastery (10h/wk):** spread the same content over three calendar weeks. The mini-project lands in calendar Week 27 of the mastery pathway. See the [mastery study plan](../study-plans/mastery-1-year.md).

---

## How to navigate this week

| File | What's inside |
|------|---------------|
| [README.md](./README.md) | This overview |
| [resources.md](./resources.md) | Free readings + trie / KMP / Z references + glossary additions |
| [lecture-notes/01-trie-basics-and-autocomplete.md](./lecture-notes/01-trie-basics-and-autocomplete.md) | The trie, both forms (dict-of-dict and class), insert / search / starts-with, the autocomplete walk, the four common bug patterns |
| [lecture-notes/02-word-break-and-aho-corasick.md](./lecture-notes/02-word-break-and-aho-corasick.md) | Word-break with memoization plus trie, longest-common-prefix three ways, the beginner-aware Aho-Corasick read |
| [lecture-notes/03-kmp-and-z-algorithm.md](./lecture-notes/03-kmp-and-z-algorithm.md) | KMP failure function intuition, the LC 28 reference implementation, the Z-algorithm sibling, when to reach for each |
| [exercises/README.md](./exercises/README.md) | Index of the three trie/string exercises and SOLUTIONS |
| [exercises/exercise-01-implement-trie.py](./exercises/exercise-01-implement-trie.py) | The canonical trie warm-up — LC 208 |
| [exercises/exercise-02-word-break.py](./exercises/exercise-02-word-break.py) | LC 139 with memoization plus a trie for the dictionary |
| [exercises/exercise-03-longest-common-prefix.py](./exercises/exercise-03-longest-common-prefix.py) | LC 14 — three solutions; one is the trie variant |
| [exercises/SOLUTIONS.md](./exercises/SOLUTIONS.md) | Worked solutions with FRAME narration; consult after attempting each exercise |
| [challenges/README.md](./challenges/README.md) | Index of weekly challenges |
| [challenges/challenge-01-word-search-ii.md](./challenges/challenge-01-word-search-ii.md) | LC 212 — the canonical trie-on-grid problem |
| [challenges/challenge-02-replace-words.md](./challenges/challenge-02-replace-words.md) | LC 648 — the prefix-replace variant |
| [quiz.md](./quiz.md) | 10 pattern-recognition questions |
| [homework.md](./homework/README.md) | Six practice problems (~5 hrs) — three trie, two KMP-flavored, one composition |
| [mini-project/README.md](./mini-project/README.md) | **One trie write-up + one KMP write-up, fully FRAME-narrated** — the week's deliverable |

---

## Stretch goals

- **Read the LeetCode "Trie" tag** and skim 20 titles. For each, predict in 5 seconds: prefix-lookup? autocomplete? word-break? dictionary-on-grid? Stretches the Research-constraints muscle.
- **Re-derive the canonical dict-of-dict trie from scratch** without re-reading Lecture 1. If you cannot, you do not yet own the template. Re-read and re-derive until you can.
- **Read the Wikipedia "Aho-Corasick algorithm" article** end-to-end (about 20 minutes). You will not be able to implement it this week, but the "Goto function" and "Failure function" sections build genuine intuition. The Research-constraints payoff at Phase 3 is real.
- **Read the CPython `Objects/stringlib/fastsearch.h`** module header (~50 lines of comments at the top). This is the file behind `str.find` and the `in` operator. It explains the two-way + bitap hybrid that gives CPython 3.10+ its linear-time guarantee. The "why CPython does not just use KMP" question is one of the most discriminating Phase-3 string questions.
- **Implement Aho-Corasick** from a clean reference. This is a Phase-3 stretch — most interviewers will not ask for it, but the implementation is short (about 80 lines) and the suffix-link bookkeeping is the cleanest illustration of the "amortized linear scan" framing.

---

## What "done" looks like for Week 9

A learner who has shipped Week 9 has, in their portfolio repo:

- Three FRAME write-ups for the exercises, with recordings >= 10 minutes.
- One FRAME write-up for the Word Search II challenge.
- The quiz answered (score recorded).
- The homework problems committed.
- **Two mini-project write-ups** (one trie, one KMP), each with a 30-second pattern-recognition memo at the top, under `frame-writeups/c2-week-09/mini-project/`.
- A push log showing daily commits Mon-Sun.

If all of that is present and pushed, Phase 2's fifth week is closed. You are ready for Week 10 — graph shortest paths.

---

## A note on the Phase 2 ramp

Week 9 is the *string-week* sandwiched between two structural weeks (heaps in W8, shortest paths in W10). Tries are a small, sharp tool — three operations, one invariant — and the *Research-constraints recognition* is what separates strong candidates from weak ones. The KMP and Z material is honest about its interview register: you will not write the failure function from scratch under pressure unless the team is string-heavy. What you *will* be asked is "when does an `O(n + m)` matcher beat the naive `O(nm)` scan, and what is the matcher called." Owning that recognition is the work this week.

If you find yourself ahead by Friday, the right stretch is **not** another exercise — it is reading the Aho-Corasick article end-to-end, or skimming the `fastsearch.h` header in CPython. The Phase-2 retrospective at the end of Week 12 will be much easier if W9 leaves you with a sense of *which* string algorithm to mention in interviews, not just *that* there is one.

If you find yourself *behind* by Wednesday, skip Exercise 3 (longest-common-prefix) for now and prioritize Exercise 2 (word-break) — word-break is the most heavily-graded Phase-2 trie problem in Mock #3, and the LCP variant can be picked up in 30 minutes once the trie template is fluent.

---

## Up next

[Week 10 — Graph Shortest Paths](../week-10-graph-shortest-paths/) — once your three trie write-ups are pushed, your KMP intuition is articulate, and you can write a dict-of-dict trie from memory without consulting the lecture.

---

*If you find errors in this material, please open an issue or send a PR. Future learners will thank you.*
