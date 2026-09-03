# Mini-Project — Trie + KMP, Fully FRAME-Narrated

> The week's deliverable: two compact portfolio artifacts that demonstrate fluency across the two highest-leverage Week-9 patterns — the canonical trie operations and the KMP failure-function matcher — with full FRAME narration end-to-end. The pair is the discriminating element — Mock #2 grades the *prefix-tree family* and the *substring-matching family* separately, and shipping one of each forces you to articulate the structural difference out loud.

**Estimated time:** 10 hours, split across Thursday-Saturday.

This mini-project is *narration-heavy* rather than *content-heavy*. You will produce two FRAME write-ups, each fully delivered in all five sections, each anchored by a 30-second pattern-recognition memo at the top. The two write-ups must be navigable as a pair — cross-references between them are part of the rubric.

---

## The Brief

Three reasons.

1. **Phase 2 is graded on Research constraints.** Phase 1 spent four weeks installing the FRAME habit; Make the solution was the primary work. Phase 2 patterns are heavier and the Research constraints step matters more — recognition cost is no longer "30 seconds to name the pattern" but "60 seconds to name the data-structure choice (trie / hash set / KMP / Z), defend the asymptotic improvement over the naive baseline, and reject one wrong alternative." This mini-project is the fourth in C2 to grade two parallel write-ups as a *pair* (W6 BFS pair, W7 DFS pair, W8 heap pair, W9 string pair).

2. **Trie and KMP are the two structural shapes of every interview string question.** Half of all FAANG string problems are prefix / dictionary variants (trie); the other half are exact-substring variants (KMP / Z / `in`). The pair forces you to articulate the differences: when do you want the data structure first (trie) versus the algorithm first (KMP); when is `O(L)` per query enough versus `O(n + m)` once; when does prefix sharing buy you anything.

3. **The full FRAME narration is the rubric.** Drills are graded on Research constraints + Make the solution; the mini-project adds Frame, Assess options, Examine, *and* cross-references. By Sunday you should be able to produce a full FRAME narration on a string problem in 20-25 minutes, recorded, without rehearsal.

---

## Starter

Two starters sit beside this page. They are the spec, not the deliverable —
implement against them in your portfolio repo, not in this one.

- [`problem-01-trie-starter.py`](./problem-01-trie-starter.py) — the class
  skeleton, the `END` sentinel, the harness and the docstring spec. Fill in the
  three method bodies.
- [`problem-02-kmp-starter.py`](./problem-02-kmp-starter.py) — the two
  signatures, the harness and the docstring spec, including the failure function
  worked by hand on `"abab"`. Fill in the two functions.

Both refuse to run until you fill them in, and both tell you exactly which cases
still fail. `README-solution.py` is the answer to both — read it after your
attempt, not before.

Before any code, though, fill in the memo below from the prompt alone.

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

## Requirements

Three files: two problem write-ups plus a short overview.

```
frame-writeups/c2-week-09/mini-project/
├── README.md                                              ← short overview + index + reflection
├── problem-01-trie-implement-trie.md                      ← trie + dict-of-dict template
└── problem-02-kmp-strstr-with-failure-function.md         ← KMP + failure-function intuition
```

Each write-up is the full FRAME format from Week 1, **plus a leading 30-second pattern-recognition memo at the top**.

The two problems are chosen so that:

- **Problem 1 (trie + dict-of-dict):** the algorithm is the canonical `insert / search / starts_with` API from, narrated as if you were demoing the data structure choice. The discriminator is the `starts_with` capability — articulating "the hash set cannot answer prefix queries in less than `O(n L)`; the trie answers them in `O(P)`" is the defense.

- **Problem 2 (KMP + failure function):** the algorithm is `strStr` from, implemented with the failure function. The Research constraints move is recognizing that the naive `O(nm)` scanner can be replaced by `O(n + m)` via the failure function; the defense is "the text pointer never moves backward" and "the inner-while-loop's amortized cost is `O(n)` total."

The two problems together cover every Week-9 idiom: trie API, prefix-vs-exact-match discriminator, failure-function intuition, linear-time substring matching. After this pair, the recognition for any string problem should reduce to: *prefix tree or exact-substring matcher?*

---

### FRAME structure for each write-up

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

### Cross-references between the two write-ups

The pair must be navigable. At minimum:

- The Problem 1 write-up cites the Problem 2 write-up in the Examine · cost section: "Compare to the KMP write-up — both are linear-time in the input size, but the trie *indexes* the keys (prefix queries are free), whereas KMP *streams* through the text once (no preprocessing of the text)."
- The Problem 2 write-up cites the Problem 1 write-up in the Research constraints section: "Unlike the trie problem, this is a single-text / single-pattern problem with no dictionary; the right tool is an algorithm (KMP), not a data structure (trie)."

The cross-references are a small detail but they earn senior signal — they show you can navigate the *taxonomy* of string algorithms, not just the individual templates.

---

### Rubric

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

## Constraints

- **The two structures answer different questions.** A trie answers "anything
  under this prefix?"; a matcher answers "does this exact run occur?" Your memo
  must say which question the prompt is asking and why the other structure does
  not answer it.
- **`END` is a sentinel object, not a character.** Any real character used as
  the end marker can appear in a code and collide with it.
- **`search` and `starts_with` differ by exactly one check.** Say which one, in
  one sentence. If your write-up cannot, the trie is not yet understood.
- **The text pointer never moves backward in KMP.** That single sentence is the
  `O(n + m)` defence; everything else about the failure function is support for
  it.
- **The failure function is built from the pattern alone**, before the text is
  read. If your build touches the text, it is not the failure function.

## Expected output

Real stdout from the shipped solution, captured on CPython 3.13.2:

```text
$ python README-solution.py
1 - the seed index (trie)
    search 'sage'     -> True
    search 'sag'      -> True
    search 'sa'       -> False
    search 'salsify'  -> True
    search 'beetroot' -> False
    search ''         -> False
    prefix 'sa'       -> True
    prefix 'sal'      -> True
    prefix 'b'        -> True
    prefix 'z'        -> False
    prefix ''         -> True
    prefix 'sages'    -> False
2 - the tide log (KMP)
    failure 'abab'     -> [0, 0, 1, 2]
    failure 'aaaa'     -> [0, 1, 2, 3]
    failure 'abcd'     -> [0, 0, 0, 0]
    failure 'aabaaab'  -> [0, 1, 0, 1, 2, 2, 3]
    failure ''         -> []
    find 'gauge'  in 'tide gauge tide'  -> 5
    find 'aab'    in 'aaaaab'           -> 3
    find 'ababc'  in 'abababc'          -> 2
    find 'abcd'   in 'abc'              -> -1
    find ''       in 'abc'              -> 0
    find 'a'      in ''                 -> -1
    find ''       in ''                 -> 0
    find 'aaa'    in 'aaa'              -> 0

All checks passed.
```

Two rows are worth pausing on. `search 'sa' -> False` beside
`prefix 'sa' -> True` is the discriminator in one line. And
`find 'ababc' in 'abababc' -> 2` is the case a scanner that resets to zero on a
mismatch gets wrong — the fallback is what finds it.

## Steps

1. Read both starters end to end, harnesses included. The harness is the spec,
   so anything it asserts is a requirement whether or not the prose repeats it.
2. Fill in the memo for problem 1 from the prompt alone, before writing code.
3. Implement the trie. Get `search` and `starts_with` differing by exactly one
   check, and be able to say which.
4. Fill in the memo for problem 2. Work the failure function by hand on `"abab"`
   first — the starter shows the four rows — then implement it.
5. Implement the matcher. Test `"ababc"` in `"abababc"` early; it is the case
   that separates a real KMP from a scanner with extra steps.
6. Write both FRAME passes. The Research-constraints section is where the marks
   are: name the question, name the structure, reject the alternative.
7. Cross-reference the two write-ups and push.

## The Solution

```python
"""README-solution.py - both Week 9 mini-project problems, worked.

The prefix tree and the linear-time matcher, written to the two starters'
contracts. Together they are the week's whole recognition question: is this a
PREFIX problem or an EXACT SUBSTRING problem? The two structures answer
different questions and are not interchangeable, which is the thing a write-up
has to say out loud.

Problem 1 - the seed index. A trie, because the counter asks "anything starting
with these letters?" on every keystroke. A set answers that only by walking
every key it holds.

Problem 2 - the tide log. KMP, because the naive scanner restarts the pattern at
every position and the failure function removes the restart. The text pointer
never moves backward; that is the sentence the defence rests on.

Labels are printed in plain capitals rather than Markdown headings: this output
is published inside a fenced block on the page, and a "##" line inside that fence
reads as a new page section to anything splitting the page on headings.

Run it and the self-checks assert every case both harnesses state. When they pass
it prints "All checks passed."
"""

END = "\0end"


# ------------------------------------------------------------ the trie ----


class SeedIndex:
    """A prefix tree over packet codes.

    Dicts all the way down: each node maps one character to the node beneath it,
    and carries END when a complete code stops there.

    Cost, for a code of length L over an alphabet of size A:
        insert       O(L) time, O(L) new nodes worst case
        search       O(L) time, O(1) space
        starts_with  O(P) time for a prefix of length P

    None of the three depends on how many codes are stored, which is the whole
    argument for the structure.
    """

    def __init__(self) -> None:
        self.root: dict = {}

    def insert(self, code: str) -> None:
        """File one packet code."""
        node = self.root
        for ch in code:
            node = node.setdefault(ch, {})
        # END is set on the node the code STOPS at. Without it "sag" would count
        # as stocked merely because "sage" is.
        node[END] = True

    def _descend(self, text: str) -> dict | None:
        """Walk the tree; return the node arrived at, or None if the walk broke."""
        node = self.root
        for ch in text:
            node = node.get(ch)
            if node is None:
                return None
        return node

    def search(self, code: str) -> bool:
        """Is this exact code stocked?"""
        node = self._descend(code)
        # Arriving is not enough. The END check is the difference between this
        # and starts_with, and it is the only difference.
        return node is not None and END in node

    def starts_with(self, prefix: str) -> bool:
        """Is anything stocked under this prefix?"""
        return self._descend(prefix) is not None


# ------------------------------------------------------------- the KMP ----


def failure_function(pattern: str) -> list[int]:
    """Longest proper prefix of pattern[:i+1] that is also a suffix of it.

    Args:
        pattern: The signature being searched for.

    Returns:
        A list the same length as pattern.
    """
    fail = [0] * len(pattern)
    matched = 0
    for i in range(1, len(pattern)):
        # Fall back through the table rather than resetting to zero. Resetting
        # is what makes the naive scanner quadratic; this loop is what makes the
        # whole build linear, because `matched` only ever decreases here and it
        # only ever rose once per character.
        while matched and pattern[i] != pattern[matched]:
            matched = fail[matched - 1]
        if pattern[i] == pattern[matched]:
            matched += 1
        fail[i] = matched
    return fail


def find_first(text: str, pattern: str) -> int:
    """Index of the first occurrence of pattern in text, or -1.

    Args:
        text: The log to scan.
        pattern: The signature to find. An empty pattern matches at 0.

    Returns:
        The starting index, or -1.
    """
    if not pattern:
        return 0
    if len(pattern) > len(text):
        return -1

    fail = failure_function(pattern)
    matched = 0
    for i, ch in enumerate(text):
        while matched and ch != pattern[matched]:
            matched = fail[matched - 1]
        if ch == pattern[matched]:
            matched += 1
        if matched == len(pattern):
            # i is the LAST character of the match, so the start is behind it.
            return i - len(pattern) + 1
    return -1


# ---- Self-check ----
if __name__ == "__main__":
    print("1 - the seed index (trie)")
    index = SeedIndex()
    for code in ("sage", "sag", "salsify", "borage", "beet"):
        index.insert(code)
    for code in ("sage", "sag", "sa", "salsify", "beetroot", ""):
        print(f"    search {code!r:<10} -> {index.search(code)}")
    for prefix in ("sa", "sal", "b", "z", "", "sages"):
        print(f"    prefix {prefix!r:<10} -> {index.starts_with(prefix)}")

    print("2 - the tide log (KMP)")
    for pattern in ("abab", "aaaa", "abcd", "aabaaab", ""):
        print(f"    failure {pattern!r:<10} -> {failure_function(pattern)}")
    for text, pattern in (("tide gauge tide", "gauge"), ("aaaaab", "aab"),
                          ("abababc", "ababc"), ("abc", "abcd"),
                          ("abc", ""), ("", "a"), ("", ""), ("aaa", "aaa")):
        print(f"    find {pattern!r:<8} in {text!r:<18} -> {find_first(text, pattern)}")

    # ---- Problem 1: every case the starter's harness states.
    assert index.search("sage") is True
    assert index.search("sag") is True
    assert index.search("sa") is False          # a prefix is not a code
    assert index.search("salsify") is True
    assert index.search("beetroot") is False    # runs past the end of the tree
    assert index.search("") is False            # nothing was filed empty
    assert index.starts_with("sa") is True
    assert index.starts_with("sal") is True
    assert index.starts_with("b") is True
    assert index.starts_with("z") is False
    assert index.starts_with("") is True        # everything starts with nothing
    assert index.starts_with("sages") is False

    # The discriminator, stated as an assertion: same argument, different answer.
    assert index.starts_with("sa") and not index.search("sa")

    # ---- Problem 2: the table by hand, then the matcher.
    assert failure_function("abab") == [0, 0, 1, 2]
    assert failure_function("aaaa") == [0, 1, 2, 3]
    assert failure_function("abcd") == [0, 0, 0, 0]
    assert failure_function("aabaaab") == [0, 1, 0, 1, 2, 2, 3]
    assert failure_function("") == []

    assert find_first("tide gauge tide", "gauge") == 5
    assert find_first("aaaaab", "aab") == 3
    assert find_first("abababc", "ababc") == 2   # needs the fallback
    assert find_first("abc", "abcd") == -1       # pattern longer than text
    assert find_first("abc", "") == 0            # empty pattern
    assert find_first("", "a") == -1             # empty text
    assert find_first("", "") == 0               # both empty
    assert find_first("aaa", "aaa") == 0         # whole text

    print()
    print("All checks passed.")
```

Both problems in one file. The trie's `search` and `starts_with` are deliberately
written to share a `_descend` helper, so the one line of difference between them
is the only line of difference between them.

## Download and run

Download the solution beside this page and run it:

```bash
python README-solution.py
```

No third-party packages, no arguments, no input. It prints both problems' worked
cases and then `All checks passed.`

The two starters run the same way and report which cases are still failing, so
you can work against them without reading the answer.

## Common bugs to catch

- **`search` returning True for a prefix.** Symptom: `"sag"` reports as stocked
  because `"sage"` was filed. The descent succeeded; the `END` check is missing.
- **Using a real character as the end marker.** Symptom: a code containing that
  character behaves as though it ends early. Use a sentinel that cannot occur.
- **Rebuilding the trie per query.** Symptom: correct answers, `O(n L)` per
  keystroke, and no advantage over the set you were arguing against.
- **A failure function that resets to zero on a mismatch.** Symptom:
  `find_first("abababc", "ababc")` returns `-1` or the wrong index. Fall back
  through the table instead — that fallback *is* the algorithm.
- **Returning the index of the last matched character.** Symptom: every answer
  is `len(pattern) - 1` too large. The match starts behind the character that
  completed it.
- **Forgetting the empty pattern.** Symptom: an exception, or `-1`, where every
  standard library returns `0`.

## Acceptance checklist

The mini-project is complete when:

- Both write-ups are committed under `frame-writeups/c2-week-09/mini-project/`.
- Both have the 30-second memo at the top.
- The cross-references in both directions are present.
- Both have recordings of at least 10 minutes each.
- The implementations pass the test cases in the starters.

Push everything by Sunday end-of-day. Phase 2's fifth week is closed on the push.

---

## Stretch

- Add `delete(code)` to the trie and say what makes it harder than insert: a
  node may only be pruned when it carries no `END` and no children, so the
  deletion has to unwind rather than descend.
- Extend the matcher to return **every** occurrence rather than the first, and
  say what changes at an overlap — `"aa"` in `"aaa"` occurs twice, not once, and
  where you reset `matched` decides whether you see both.
- Take the naive scanner, run it against the KMP one on a worst case like
  `"aaaa...ab"`, and count comparisons rather than seconds. The ratio is the
  argument your Examine (cost) section is making.

## Self-reflection (in the mini-project README)

End the README.md for `frame-writeups/c2-week-09/mini-project/README.md` with a short reflection — 4-6 sentences — addressing:

1. Which template (trie or KMP) felt more natural? Why?
2. What was the hardest part of the KMP failure function to articulate aloud?
3. What is the one thing you want to drill before Mock #2?

The reflection is the portfolio-grade artifact. Future you will thank present you for writing it.

---

## After the mini-project

Move on to [Week 10 — Weighted Graphs and Union-Find](../../week-10-weighted-graphs-and-union-find/). The trie and KMP intuition stay with you through the rest of Phase 2; you will use them again in the W12 retrospective and (for the strings-team interviews) in Mock #3.
