# Mini-Project — Trie + KMP, Fully FRAME-Narrated

> The week's deliverable: two compact portfolio artifacts that demonstrate fluency across the two highest-leverage Week-9 patterns — the canonical trie operations and the KMP failure-function matcher — with full FRAME narration end-to-end. The pair is the discriminating element — Mock #2 grades the *prefix-tree family* and the *substring-matching family* separately, and shipping one of each forces you to articulate the structural difference out loud.

**Estimated time:** 10 hours, split across Thursday-Saturday.

This mini-project is *narration-heavy* rather than *content-heavy*. You will produce two FRAME write-ups, each fully delivered in all five sections, each anchored by a 30-second pattern-recognition memo at the top. The two write-ups must be navigable as a pair — cross-references between them are part of the rubric.

---

## Why this matters

Three reasons.

1. **Phase 2 is graded on Research constraints.** Phase 1 spent four weeks installing the FRAME habit; Make the solution was the primary work. Phase 2 patterns are heavier and the Research constraints step matters more — recognition cost is no longer "30 seconds to name the pattern" but "60 seconds to name the data-structure choice (trie / hash set / KMP / Z), defend the asymptotic improvement over the naive baseline, and reject one wrong alternative." This mini-project is the fourth in C2 to grade two parallel write-ups as a *pair* (W6 BFS pair, W7 DFS pair, W8 heap pair, W9 string pair).

2. **Trie and KMP are the two structural shapes of every interview string question.** Half of all FAANG string problems are prefix / dictionary variants (trie); the other half are exact-substring variants (KMP / Z / `in`). The pair forces you to articulate the differences: when do you want the data structure first (trie) versus the algorithm first (KMP); when is `O(L)` per query enough versus `O(n + m)` once; when does prefix sharing buy you anything.

3. **The full FRAME narration is the rubric.** Drills are graded on Research constraints + Make the solution; the mini-project adds Frame, Assess options, Examine, *and* cross-references. By Sunday you should be able to produce a full FRAME narration on a string problem in 20-25 minutes, recorded, without rehearsal.

---

## What you ship

Three files: two problem write-ups plus a short overview.

```
frame-writeups/c2-week-09/mini-project/
├── README.md                                              ← short overview + index + reflection
├── problem-01-trie-implement-trie.md                      ← trie + dict-of-dict template
└── problem-02-kmp-strstr-with-failure-function.md         ← KMP + failure-function intuition
```

Each write-up is the full FRAME format from Week 1, **plus a leading 30-second pattern-recognition memo at the top**.

The two problems are chosen so that:

- **Problem 1 (trie + dict-of-dict):** the algorithm is the canonical `insert / search / starts_with` API from LC 208, narrated as if you were demoing the data structure choice. The discriminator is the `starts_with` capability — articulating "the hash set cannot answer prefix queries in less than `O(n L)`; the trie answers them in `O(P)`" is the defense.

- **Problem 2 (KMP + failure function):** the algorithm is `strStr` from LC 28, implemented with the failure function. The Research constraints move is recognizing that the naive `O(nm)` scanner can be replaced by `O(n + m)` via the failure function; the defense is "the text pointer never moves backward" and "the inner-while-loop's amortized cost is `O(n)` total."

The two problems together cover every Week-9 idiom: trie API, prefix-vs-exact-match discriminator, failure-function intuition, linear-time substring matching. After this pair, the recognition for any string problem should reduce to: *prefix tree or exact-substring matcher?*

---

## The 30-second pattern-recognition memo (the signature element)

At the top of each write-up, immediately after the title, place a single bordered block.

### For Problem 1 (trie)

```markdown
> **30-second pattern-recognition memo (trie):**
> This is a trie problem because [the API includes `starts_with` / the problem
> says "given a dictionary" / the prompt asks for prefix queries].
> Sub-shape: [dict-of-dict / TrieNode class].
> Why this form: [no per-node state needed -> dict-of-dict; per-node frequency
> required -> class form].
> END sentinel: [`"$"` because the input alphabet is lowercase ASCII].
> Why not `set[str]`: [O(L) expected for exact-match but cannot answer
> `starts_with` in less than O(n * L); trie answers it in O(P)].
```

### For Problem 2 (KMP)

```markdown
> **30-second pattern-recognition memo (KMP):**
> This is an exact-substring-matching problem because [the prompt asks for
> the first / all occurrences of needle in haystack].
> Sub-shape: [KMP via failure function / Z-algorithm].
> Why KMP: [O(n + m) vs naive O(nm); for n = X, m = Y, the factor of m savings
> is significant / necessary for the constraints].
> Failure-function intuition: [fail[i] is the length of the longest proper
> prefix of pattern[:i+1] that is also a suffix; on a mismatch, jump j to
> fail[j-1] without moving i backward].
> Production alternative: [CPython 3.10+ str.find is already linear via the
> two-way + bitap hybrid; KMP is the interview-grade explicit form].
```

Read each aloud; both should hit 25-30 seconds.

---

## FRAME structure for each write-up

The full five-section format, with Examine split into its verify and cost halves. The Research constraints section opens with the 30-second memo above.

### Frame

Restate the problem in your own words. Walk one example by hand. Note the constraints. Specifically address:

- For Problem 1 — restate the three API operations and the discriminator between `search` and `starts_with` (the `END` flag at the final node).
- For Problem 2 — restate the substring-search problem; state the constraint that makes the naive `O(nm)` insufficient; address the empty-needle edge case.

### Research constraints

Open with the 30-second memo. Then in 2-3 sentences:

- Name the pattern: trie (Problem 1) or KMP (Problem 2).
- Name the sub-shape: dict-of-dict (Problem 1) or failure-function-based matcher (Problem 2).
- Reject the alternative: hash set for Problem 1; naive scanner for Problem 2.

### Assess options

Numbered steps; 4-6 lines each. State the data structure first. State the loop / recursion structure second. State the termination condition third.

For Problem 1: `__init__` makes an empty dict; `insert` walks-and-creates; `search` walks-and-checks-END; `starts_with` walks-only.

For Problem 2: build the failure function in one linear pass; run the matcher in one linear pass; return `i - j + 1` on full match.

### Make the solution

The code. Type hints on every function. Docstrings on every public method. Comments only where the line is non-obvious — KMP's `fail[k - 1]` indexing deserves a comment; the trie's `setdefault(ch, {})` does not.

### Examine · verify

Trace the implementation by hand on at least two inputs:

- One positive example (the canonical "it works" case).
- One edge case (empty input, single character, all-same characters).

For Problem 2, the second trace must include a mismatch that triggers the failure chain — otherwise the KMP work is invisible.

### Examine · cost

Time and space bounds with derivation. The derivation is mandatory, not the bound alone.

- Problem 1: `O(L)` per operation derived from "the walk visits each character exactly once."
- Problem 2: `O(n + m)` derived from "the text pointer `i` is monotonic, advancing `n` times; the pattern pointer `j` increases at most `n` times overall, so the inner-while-loop's total amortized work is `O(n)."

Mention at least one variant in each Examine · cost section. For Problem 1: the `TrieNode` class form, when it is preferred. For Problem 2: the Z-algorithm sibling, and CPython 3.10+'s `str.find` as the production answer.

---

## Cross-references between the two write-ups

The pair must be navigable. At minimum:

- The Problem 1 write-up cites the Problem 2 write-up in the Examine · cost section: "Compare to the KMP write-up — both are linear-time in the input size, but the trie *indexes* the keys (prefix queries are free), whereas KMP *streams* through the text once (no preprocessing of the text)."
- The Problem 2 write-up cites the Problem 1 write-up in the Research constraints section: "Unlike the trie problem, this is a single-text / single-pattern problem with no dictionary; the right tool is an algorithm (KMP), not a data structure (trie)."

The cross-references are a small detail but they earn senior signal — they show you can navigate the *taxonomy* of string algorithms, not just the individual templates.

---

## Starter files

Two starters are provided. Implement against them in your portfolio (not in this repo); the starters here are the spec, not the deliverable.

### Problem 1 starter

See [`problem-01-trie-starter.py`](./problem-01-trie-starter.py). The starter has the class skeleton, the `END` sentinel, the test harness, and the docstring spec. Fill in the three method bodies.

### Problem 2 starter

See [`problem-02-kmp-starter.py`](./problem-02-kmp-starter.py). The starter has the function signatures, the failure-function and matcher stubs, the test harness, and the docstring spec. Fill in the two functions.

---

## Rubric

Each write-up is graded on the 30-second memo plus the five FRAME sections, with Examine split into verify and cost. Total possible: 100 points; passing: 70.

### Problem 1 (trie) rubric

| Dimension | Points | What "full credit" looks like |
|-----------|-------:|----------------------|
| 30-second memo at the top | 10 | All five lines present; the discriminator vs hash set is stated |
| Frame | 10 | Two examples walked; the discriminator between `search` and `starts_with` stated |
| Research constraints | 20 | Trie pattern named; dict-of-dict form justified; hash set rejected with reason |
| Assess options | 10 | Three method bodies sketched; data structure choice stated; `END` sentinel explained |
| Make the solution | 25 | All test cases pass; type hints on every method; PEP 8; idiomatic Python |
| Examine · verify | 10 | One positive trace + one edge case; both walked |
| Examine · cost | 15 | `O(L)` derived; trade vs hash set stated; one variant mentioned |

### Problem 2 (KMP) rubric

| Dimension | Points | What "full credit" looks like |
|-----------|-------:|----------------------|
| 30-second memo at the top | 10 | All five lines present; the production alternative (`str.find`) is mentioned |
| Frame | 10 | Two examples walked; the empty-needle edge case addressed |
| Research constraints | 20 | KMP pattern named; failure-function intuition explained; naive scanner rejected |
| Assess options | 10 | Two passes outlined (build + match); the failure-chain fallback explained |
| Make the solution | 25 | All test cases pass; the off-by-one `fail[k-1]` indexed correctly; type hints |
| Examine · verify | 15 | One positive trace + one mismatch trace; the failure chain walked aloud |
| Examine · cost | 10 | `O(n + m)` derived; the Z-algorithm sibling and `str.find` production answer named |

### Cross-reference rubric

| Dimension | Points | What "full credit" looks like |
|-----------|-------:|----------------------|
| Problem 1 cites Problem 2 in Examine · cost | 5 | Sentence comparing prefix-tree indexing to KMP's text streaming |
| Problem 2 cites Problem 1 in Research constraints | 5 | Sentence rejecting the trie ("no dictionary; the right tool is an algorithm") |

Sum: 90 (Problem 1) + 100 (Problem 2) + 10 (cross-refs) = 200 / 2 = **100 average**.

A passing write-up scores at least 70 on each.

---

## Acceptance

The mini-project is complete when:

- Both write-ups are committed under `frame-writeups/c2-week-09/mini-project/`.
- Both have the 30-second memo at the top.
- The cross-references in both directions are present.
- Both have recordings of at least 10 minutes each.
- The implementations pass the test cases in the starters.

Push everything by Sunday end-of-day. Phase 2's fifth week is closed on the push.

---

## Self-reflection (in the mini-project README)

End the README.md for `frame-writeups/c2-week-09/mini-project/README.md` with a short reflection — 4-6 sentences — addressing:

1. Which template (trie or KMP) felt more natural? Why?
2. What was the hardest part of the KMP failure function to articulate aloud?
3. What is the one thing you want to drill before Mock #2?

The reflection is the portfolio-grade artifact. Future you will thank present you for writing it.

---

## After the mini-project

Move on to [Week 10 — Graph Shortest Paths](../../week-10-graph-shortest-paths/). The trie and KMP intuition stay with you through the rest of Phase 2; you will use them again in the W12 retrospective and (for the strings-team interviews) in Mock #3.
