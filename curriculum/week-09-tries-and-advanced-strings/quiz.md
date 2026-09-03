# Week 9 — Pattern-Recognition Quiz

Ten short prompts. **Do not solve them.** For each, decide whether it is a trie problem, a KMP/Z problem, an Aho-Corasick problem, or none of the above — and if trie, name the sub-shape (`insert/search/starts_with` / autocomplete / word-break / trie-on-grid / shortest-prefix). One-line justification per answer. Lectures closed. Time yourself — 45 seconds per question is the target.

Answer key at the bottom.

---

**Q1.** "Implement a data structure that supports inserting strings and answering `starts_with(prefix)` queries."

**Q2.** "Given a string `haystack` and a string `needle`, find the index of the first occurrence of `needle` in `haystack`, or `-1`. `len(haystack) = 10^6`, `len(needle) = 10^3`."

**Q3.** "Given an `m x n` grid of characters and a list of 500 words, return all words that can be formed by sequentially adjacent cells of the grid."

**Q4.** "Given a string `s` and a dictionary of words, return True if `s` can be segmented into a space-separated sequence of dictionary words."

**Q5.** "Given an array of strings, return their longest common prefix."

**Q6.** "Given a long article and a list of 200 banned phrases, return the count of total banned-phrase occurrences (with overlap counted)."

**Q7.** "Given two strings `s` and `t`, return True if `t` is an anagram of `s`."

**Q8.** "Given a dictionary of word roots and a sentence, replace each word in the sentence by the shortest root in the dictionary that is a prefix of the word."

**Q9.** "Given a list of strings, design a data structure that, given a query prefix, returns the top-3 most-frequently-inserted strings sharing that prefix."

**Q10.** "Given a string `s`, find the longest substring of `s` that appears at least twice."

---

## Answer key

<details>
<summary>Click after attempting all ten</summary>

1. **Trie — `insert / search / starts_with`.** The textbook trie problem. The `starts_with` capability is the discriminating cue — a hash set cannot answer it in less than `O(n L)`. Default to dict-of-dict form. Exercise 1 exactly.

2. **KMP (or Z).** The naive scanner is `O(n m) = 10^9` — too slow. KMP gives `O(n + m) ≈ 10^6 + 10^3 = 10^6`, three orders of magnitude faster. Mention that CPython 3.10+'s `haystack.find(needle)` already uses the two-way + bitap hybrid and is linear-time in production. Lecture 3 §8.

3. **Trie + DFS on grid (the cold store aisle sweep.** The dictionary-on-grid trigger. Trie of words + DFS per cell that walks the grid and descends the trie in lockstep. The naive per-word DFS is `O(W * m * n * 4^L)`; the trie variant is `O(m * n * 4^L)`. Challenge 1 exactly.

4. **Trie + memoization (the stripped manifest line.** The "given a dictionary, can `s` be segmented" trigger. Build a trie of the dictionary; recurse with a memo on the start position. Time `O(n^2)`. Exercise 2 exactly. The alternative is hash-set DP — same asymptotics, but the trie generalizes to the stripped manifest line, every split.

5. **Trie walk *or* vertical scan.** Both are valid. Default to vertical scan for the one-shot; mention the trie walk as the right answer for the incremental / multi-query generalization. Exercise 3 exactly. The trie walk's stopping condition is "exactly one child *and* not a terminal" — forgetting the second clause is the off-by-one trap.

6. **Aho-Corasick.** Multiple patterns, one long text, counting all occurrences. KMP per pattern is `O(n * W + m)`; Aho-Corasick is `O(n + m + z)` where `z` is the number of matches. Mention the algorithm by name; you are not expected to implement it in entry-level interviews. Lecture 2 §3.

7. **Not a trie / not KMP / not Aho-Corasick.** Anagram is a counting / sort problem. `Counter(s) == Counter(t)` is the one-liner; `sorted(s) == sorted(t)` is the other. The trie / KMP / Aho-Corasick family is for prefix or substring matching, not for counting. Negative-space discriminator.

8. **Trie of roots; shortest-prefix walk (the berth ledger shorthand.** Per query word, walk the trie character by character and stop at the first `END`. Challenge 2 exactly. The variant "longest root" tracks the most recent `END` instead of stopping at the first.

9. **Trie + heap composition (Design Search Autocomplete,).** Per node, store the top-k by frequency among the keys with this prefix. The trie answers "give me all keys with this prefix" in `O(P)`; the per-node heap (or sorted list) answers "the top-3 of those" in `O(1)`. Phase-3 stretch; mention by name for the senior signal.

10. **Trie-of-suffixes *or* suffix array.** Not a strict-Week-9 problem; the strict tool is a suffix array (out of scope until Phase 3). A trie of all suffixes (the **suffix trie**) answers the question — the deepest node with at least two leaves in its subtree gives the longest repeated substring. Mention the trie of suffixes as an interview-acceptable answer; the optimal answer (suffix array) is Phase-3 material.

</details>

---

## How to score

| Score | Meaning |
|------:|---------|
| 9-10 | Trie / KMP / Aho-Corasick recognition is interview-ready, including the negative-space rejections. Move on. |
| 7-8 | Good — re-read [Lecture 1 §9](./lecture-notes/01-trie-basics-and-autocomplete.md) and [Lecture 3 §6](./lecture-notes/03-kmp-and-z-algorithm.md) for the sub-shape questions you missed. Most learners miss Q7 (anagram) or Q10 (suffix trie) first time; that is normal. |
| 5-6 | Redo Exercises 2 and 3 with stricter Research constraints sections. The word-break and LCP recognition needs more reps before Mock #2. |
| <5 | The pattern recognition is not yet automatic. Re-read all three lectures, re-do all three exercises with the data-structure choice stated aloud, then retake the quiz. |

This quiz is about **fluency**, not difficulty. The discriminating questions are Q7, Q9, and Q10 — Q7 is the negative-space rejection (anagram is *not* a trie problem); Q9 is the trie + heap composition (Phase-3 stretch, but the recognition cue is Week-9 material); Q10 is the suffix-trie observation (stretch). Recognizing the right tool — *and the wrong ones* — is the senior-level skill being measured.

Q5 (LCP) and Q8 (shortest root) are the cleanest direct-template questions. Q2 and Q6 test the substring family (KMP for one pattern; Aho-Corasick for many).

When done, the [homework](./homework/README.md) is next.
