# Mini-Project — Top-k + Two-Heap, Fully UMPIRE-Narrated

> The week's deliverable: two compact portfolio artifacts that demonstrate fluency across the two highest-leverage Week-8 templates — the size-k top-k heap and the two-heap running-statistic pattern — with full UMPIRE narration end-to-end. The pair is the discriminating element — Mock #2 grades both templates separately, and shipping one of each forces you to articulate the structural differences out loud.

**Estimated time:** 10 hours, split across Thursday-Saturday.

This mini-project is *narration-heavy* rather than *content-heavy*. You will produce two UMPIRE write-ups, each fully delivered in all six sections, each anchored by a 30-second pattern-recognition memo at the top. The two write-ups must be navigable as a pair — cross-references between them are part of the rubric.

---

## Why this matters

Three reasons.

1. **Phase 2 is graded on Match.** Phase 1 spent four weeks installing the UMPIRE habit; the Implement step was the primary work. Phase 2 patterns are heavier and the Match step matters more — recognition cost is no longer "30 seconds to name the pattern" but "60 seconds to name the algorithm choice (size-k / k-closest / two-heap / k-way merge / scheduler / lazy deletion), defend the size bound or balance invariant, and reject one wrong alternative." This mini-project is the third in C2 to grade two parallel write-ups as a *pair* (W6 BFS pair, W7 DFS pair, W8 heap pair).

2. **Top-k and two-heap are the two structural shapes of every interview heap question.** Half of all FAANG heap problems are top-k variants; the other half are running-statistic variants. The pair forces you to articulate the differences: when is the heap bounded vs unbounded, when is one heap enough vs two, when does the size invariant matter vs the balance invariant. After two write-ups side-by-side, the disambiguation is reflexive.

3. **The full UMPIRE narration is the rubric.** Drills are graded on Match + Implement; the mini-project adds Plan, Review, Evaluate, *and* cross-references. By Sunday you should be able to produce a full UMPIRE narration on a heap problem in 20-25 minutes, recorded, without rehearsal.

---

## What you ship

Three files: two problem write-ups plus a short overview.

```
umpire-writeups/c2-week-08/mini-project/
├── README.md                                              ← short overview + index + reflection
├── problem-01-topk-top-k-frequent-words.md                ← top-k + heap-of-tuples
└── problem-02-twoheap-sliding-window-median.md            ← two-heap + lazy deletion
```

Each write-up is the full UMPIRE format from Week 1, **plus a leading 30-second pattern-recognition memo at the top**.

The two problems are chosen so that:

- **Problem 1 (top-k + heap-of-tuples):** the algorithm is a size-k heap with a *conflicting-direction* tiebreaker (count is max-first; word is min-first on ties). This forces you to write either a custom-comparator wrapper or a two-pass `sort-then-truncate` solution — and to defend the choice. A subtle variant that catches candidates who only practice plain top-k.

- **Problem 2 (two-heap + lazy deletion):** the algorithm is the two-heap running median *under a sliding window* — meaning expired elements must be removed from the heaps. The Match move is recognizing that "running median under a sliding window" composes the two-heap pattern (Lecture 3 §1) with lazy deletion (Lecture 3 §4).

The two problems together cover every Week-8 idiom: size-k bound, heap-of-tuples with custom tiebreakers, two-heap balance, lazy deletion. After this pair, the recognition for any heap problem should reduce to: *which of these idioms applies?*

---

## The 30-second pattern-recognition memo (the signature element)

At the top of each write-up, immediately after the title, place a single bordered block.

### For Problem 1 (top-k)

```markdown
> **30-second pattern-recognition memo (top-k):**
> This is a top-k problem because [k-largest / k-most-frequent / k-closest signal].
> Sub-shape: [size-k min-heap / size-k max-heap by negation].
> Tuple shape: [bare key / (priority, tiebreaker, payload)].
> Tiebreaker: [counter / secondary key / unnecessary (numeric)].
> Why not sort: [O(n log n) vs O(n log k); k << n].
> Why not quickselect: [one sentence — expected vs worst-case, stream-friendliness].
```

Six lines. Read aloud, ~25 seconds.

### For Problem 2 (two-heap)

```markdown
> **30-second pattern-recognition memo (two-heap):**
> This is a two-heap problem because [running median / running percentile / order statistic on a stream].
> Heap shape: [max-heap of lower half (negated) + min-heap of upper half].
> Balance invariant: [|lower| - |upper| in {0, 1}, lower bigger when they differ].
> Median read: [O(1) — direct array reads on lower[0] and upper[0]].
> Lazy deletion: [needed? yes/no — and why].
> Why not sorted list: [O(n) per add vs O(log n)].
```

Six lines. Read aloud, ~25 seconds.

Example for Problem 1 (Top K Frequent Words):

> **30-second pattern-recognition memo (top-k):**
> This is a top-k problem because we want the k most frequent words from a list, with a deterministic tiebreaker.
> Sub-shape: size-k MIN-heap; the heap holds the k most-frequent seen so far; the min of the heap is the eviction bar.
> Tuple shape: `(count, word)` — but with a TWIST: count is max-first (the heap keeps largest), word is min-first on ties (alphabetical, smaller wins).
> Tiebreaker: conflict — count direction and word direction oppose. Cleanest fix: sort `Counter.items()` by `(-count, word)` and take the first `k`. Pure-heap version requires a custom `__lt__`.
> Why not sort: for `n <= 10⁴`, sort-then-truncate is `O(n log n)`; heap is `O(n log k)`. Both fast enough; the heap is the template rep.
> Why not quickselect: not stream-friendly; the prompt does not need stream support.

Example for Problem 2 (Sliding Window Median):

> **30-second pattern-recognition memo (two-heap):**
> This is a two-heap problem because we maintain a median under a sliding window of size `k`.
> Heap shape: max-heap `lower` (negated) of the smaller half of the current window; min-heap `upper` of the larger half.
> Balance invariant: `|len(lower) - len(upper)| <= 1`; `lower` is larger when they differ.
> Median read: `O(1)` — `-lower[0]` (odd k) or average of `-lower[0]` and `upper[0]` (even k).
> Lazy deletion: needed — when the window slides, the leftmost element is expired but may sit deep in a heap. Mark it stale; clean the top on the next median query.
> Why not sorted list with bisect: insert is `O(k)` (list-shift); the two-heap is `O(log k)`.

Two write-ups, two memos. By the second, the cadence is automatic.

---

## Per-problem rubric

Each write-up's grade comes from five axes:

| Axis | Weight | "Great" looks like |
|------|------:|--------------------|
| 30-second memo at the top | 25% | Six lines, all required elements named, hits cadence on read-aloud (≤30s) |
| Match section (expanded body) | 25% | Explicit comparison against the *other* template; one-paragraph "why this algorithm and not the other"; rejection of one wrong pattern (sort / quickselect / single-heap) |
| Plan + Implement | 20% | Clean code; the canonical template visible; the heap setup (initial seed, bound, invariant restore) is a single named function or block |
| Review | 15% | Trace on at least two examples; one common bug called out and avoided |
| Evaluate (five-piece from W2) | 15% | Time / space / best-avg-worst / tradeoff / improvement, with the `O(n log k)` or `O(log n)` defense sentence and explicit rejection of one alternative |

A grade of "great" on both write-ups is the bar. The cross-references between Problems 1 and 2 are graded separately as the navigation rubric — see below.

---

## The two problems

### Problem 1 — Top K Frequent Words (LeetCode 692) — TOP-K

**Spec.** Given a list of words (lowercase strings; some words may repeat) and an integer `k`, return the `k` most frequent words.

The answer should be sorted by frequency from highest to lowest. If two words have the same frequency, the lexicographically smaller word comes first.

**Examples:**

- Input: `words = ["i", "love", "leetcode", "i", "love", "coding"], k = 2` → Output: `["i", "love"]` (both appear twice; "i" < "love" alphabetically — but both are in the top-2 by frequency so both are output).
- Input: `words = ["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], k = 4` → Output: `["the", "is", "sunny", "day"]`.

**Constraints (LeetCode):**

- `1 <= len(words) <= 500`.
- `1 <= len(words[i]) <= 10`.
- Words consist of lowercase English letters only.
- `k` is in the valid range `[1, distinct(words)]`.

**Why included.** The canonical "conflicting-direction tiebreaker" problem in the top-k family. Forces you to write:

1. The frequency counter (`collections.Counter(words)`).
2. The recognition that count and word have *opposite* tiebreaker directions — count wants max-first, word wants min-first.
3. One of two valid implementations:
   - **Implementation A:** Sort `counts.items()` by `(-count, word)`; take the first `k`. `O(n log n)` time, `O(n)` space.
   - **Implementation B:** Size-k heap with a custom `__lt__` that handles the direction conflict. `O(n log k)`, more code, more cognitive load.
4. The defense of the choice.

The senior insight is that **for `n <= 500`, the asymptotic difference is invisible** — both algorithms run in microseconds. The choice is on code clarity, not on speed. Implementation A is the simpler answer; Implementation B is the template rep. Name both; defend one.

### Full UMPIRE narration for Problem 1

**[U — Understand]** (write 2-3 paragraphs)

Restate the problem in your own words. Confirm:

- The answer is sorted by frequency, descending.
- Ties in frequency are broken by alphabetical order, ascending.
- Words are lowercase strings; comparison is the default string `__lt__`.
- `k` is guaranteed to be valid; no edge case for `k > distinct(words)`.

Walk an example by hand. For `words = ["i", "love", "leetcode", "i", "love", "coding"], k = 2`: counts = `{"i": 2, "love": 2, "leetcode": 1, "coding": 1}`. Top 2 by count: `"i"` and `"love"` (both count 2). Order: count is the same, so alphabetical: `"i" < "love"`. Output: `["i", "love"]`.

**[M — Match]** (write 3-4 paragraphs)

Top-k with a conflicting-direction tiebreaker. Restate the memo elements:

- Sub-shape: size-k heap. But the *direction* conflict (count: max-first; word: min-first on ties) complicates the pure-heap version.
- Two implementations: sort-and-truncate (`O(n log n)`) or size-k heap with custom comparator (`O(n log k)`).
- For `n <= 500`, asymptotic difference is invisible; the choice is on clarity.
- Why not quickselect: not stream-friendly; the prompt's input is in-memory; no benefit.

Compare against Problem 2 (two-heap median). The structural parallel: both use a heap-based template; the differences are (a) bounded (Problem 1, size k) vs unbounded (Problem 2, full stream), (b) one heap vs two heaps, (c) the *invariant* — size bound (Problem 1) vs balance (Problem 2). Naming this parallel out loud is the senior signal.

**[P — Plan]** (write the algorithm in 4-6 bullets, no code yet)

**Implementation A — sort and truncate (simpler):**

1. Build `counts = collections.Counter(words)`.
2. Sort `counts.items()` by the key `(-count, word)`.
3. Take the first `k` entries; return their words.

**Implementation B — size-k heap with custom comparator (template rep):**

1. Build `counts`.
2. Define a wrapper class with `__lt__` that reverses the count direction and preserves the word direction.
3. Size-k heap by the wrapper; iterate; return the words in the final heap, sorted.

Edge cases: `k == len(counts)` (return everything); all distinct words (each count is 1; alphabetical order).

**[I — Implement]** (code with brief narration)

Implementation A is the cleaner answer. Implementation B is the template rep.

```python
import heapq
from collections import Counter
from typing import List


def top_k_frequent_words_sort(words: List[str], k: int) -> List[str]:
    """Implementation A: sort and truncate. O(n log n) time, O(n) space."""
    counts = Counter(words)
    # Sort by (-count, word) — descending count, ascending word on ties.
    items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return [word for word, _ in items[:k]]


# Implementation B (template rep): size-k heap with custom comparator.

class Entry:
    """Wrap (count, word) with reversed count comparison for max-heap-by-count
    semantics in a min-heap-as-eviction-pool model.

    The eviction pool is a size-k MIN-heap; the entry to evict is the LOWEST
    by (count_asc, word_desc): low count is evicted, and on ties the LARGER
    word is evicted (so the smaller word survives -- which is what the spec
    wants for ties at the boundary).
    """

    def __init__(self, count: int, word: str) -> None:
        self.count = count
        self.word = word

    def __lt__(self, other: "Entry") -> bool:
        if self.count != other.count:
            return self.count < other.count       # min-heap by count
        return self.word > other.word             # REVERSED on ties

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Entry) and self.count == other.count and self.word == other.word


def top_k_frequent_words_heap(words: List[str], k: int) -> List[str]:
    """Implementation B: size-k heap. O(n log k) time, O(k) space."""
    counts = Counter(words)
    h: List[Entry] = []
    for word, count in counts.items():
        entry = Entry(count, word)
        if len(h) < k:
            heapq.heappush(h, entry)
        elif entry.count > h[0].count or (entry.count == h[0].count and entry.word < h[0].word):
            heapq.heappushpop(h, entry)
    # The heap holds the k most-frequent; sort the output by (-count, word).
    return [e.word for e in sorted(h, key=lambda e: (-e.count, e.word))]
```

The Implementation A version is six lines; B is closer to 25. The senior framing in the write-up: "I would write A in an interview; I am writing B here to demonstrate the template."

**[R — Review]** (trace at least two examples)

Trace 1 — `words = ["i", "love", "leetcode", "i", "love", "coding"], k = 2`. counts = `{"i": 2, "love": 2, "leetcode": 1, "coding": 1}`. Sort by `(-count, word)`: `[("i", 2), ("love", 2), ("coding", 1), ("leetcode", 1)]`. Take first 2: `["i", "love"]`. Correct.

Trace 2 — `words = ["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], k = 4`. counts = `{"the": 4, "is": 3, "sunny": 2, "day": 1}`. Sort by `(-count, word)`: `[("the", 4), ("is", 3), ("sunny", 2), ("day", 1)]`. Take first 4: `["the", "is", "sunny", "day"]`. Correct.

Common bug avoided: forgetting that the output must be *sorted* by frequency. The heap layout is not sorted; if you skip the final `sorted` step in Implementation B, the order is implementation-defined.

**[E — Evaluate]** (the five-piece)

- **Time**:
  - Implementation A: `O(n log n)` from the sort.
  - Implementation B: `O(n log k)` from the heap.
- **Space**:
  - Both: `O(n)` for the `Counter`. The heap in B is bounded at `O(k)`.
- **Best**: same as average.
- **Worst**: same as average.
- **Tradeoff**: Implementation A is shorter and reads cleaner; Implementation B is the template rep and is faster when `k << n`. For `n <= 500`, the difference is invisible.
- **Improvement**: quickselect would give `O(n)` expected — but the *tiebreaker direction conflict* makes it hard to implement cleanly. Mention as a third path; not the right answer for this spec.

Defense sentence:

> "**Implementation A is `O(n log n)`** from the sort; **Implementation B is `O(n log k)`** from the heap. For `n <= 500`, both run in microseconds. The choice is on clarity: A is six lines and obvious; B is the template rep. The senior framing: name both, defend A for clarity. The interesting structural feature is the *direction conflict* in the tiebreaker — count wants max-first, word wants min-first; B handles it via a custom `__lt__`."

---

### Problem 2 — Sliding Window Median (LeetCode 480) — TWO-HEAP + LAZY DELETION

**Spec.** You are given an integer array `nums` and an integer `k`. There is a sliding window of size `k` moving from the leftmost element of `nums` to the rightmost. As the window slides, return the median of each window.

The answer is a list of `len(nums) - k + 1` floats.

**Examples:**

- Input: `nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3`. Output: `[1, -1, -1, 3, 5, 6]` (the median of each window of size 3).
- Input: `nums = [1, 2, 3, 4, 2, 3, 1, 4, 2], k = 3`. Output: `[2, 3, 3, 3, 2, 3, 2]`.

**Constraints (LeetCode):**

- `1 <= k <= len(nums) <= 10⁵`.
- `-2³¹ <= nums[i] <= 2³¹ - 1`.

**Why included.** The canonical composition of the two-heap pattern (Lecture 3 §1) with lazy deletion (Lecture 3 §4). Forces you to write:

1. The two-heap median template (Exercise 3, exactly).
2. The slide-and-expire logic — when the window moves, the leftmost element is no longer part of the current window and must be "removed" from whichever heap it sits in.
3. Lazy deletion — mark the expired element stale in a `Counter` (handles duplicates); on each median query, clean the heap tops by skipping stale entries.
4. The balance invariant — `|lower_active| - |upper_active| <= 1`, where "active" counts non-stale entries.

The senior insight is that **eager deletion would be `O(k)` per slide** (linear scan to find and remove the element). **Lazy deletion makes each slide amortized `O(log k)`** — the stale element is marked in constant time and discarded only when it surfaces to the heap top.

### Full UMPIRE narration for Problem 2

(Use the same UMPIRE-section structure as Problem 1. Below is the abbreviated version; full write-up should match Problem 1's section depth.)

**[U]** Restate. Sliding window of size `k`; report median after each slide. Edge case `k = 1`: the median of a single-element window is that element. Edge case `k = len(nums)`: only one window; one median.

**[M]** Two-heap pattern + lazy deletion. Algorithm choice: the two-heap median from Exercise 3, plus a `Counter` of stale entries; clean the heap tops at the start of each median query. Compare against Problem 1: same heap *family* but different sub-pattern (size-k bounded vs unbounded; one heap vs two; size invariant vs balance invariant). The structural parallel: both rest on `heapq` operations; both have a clear invariant; both have a defense sentence. The differences are the discriminators graded on Mock #2.

**[P]** Five bullets:

1. Initialize `lower` (max-heap, negated), `upper` (min-heap), `stale = Counter()`, `result = []`.
2. For each new element `nums[i]`: add to the appropriate heap (push-then-rebalance from Exercise 3).
3. If `i >= k`: mark `nums[i - k]` stale (the expiring element) and decrement the active-size of its heap. The "active size" is the number of non-stale entries in each heap; track via two counters or compute on the fly.
4. After each insertion (and stale-marking once the window is full), clean the tops of both heaps by popping any stale entries.
5. If `i >= k - 1`: compute the median from the cleaned tops and append to `result`.

**[I]**

```python
import heapq
from collections import Counter
from typing import List


def median_sliding_window(nums: List[int], k: int) -> List[float]:
    """Sliding window median via two-heap + lazy deletion."""
    lower: List[int] = []     # max-heap (negated)
    upper: List[int] = []     # min-heap
    stale: Counter = Counter()
    balance = 0               # active lower count - active upper count
    result: List[float] = []

    def prune(h: List[int], sign: int) -> None:
        """Remove stale entries from the top of h. sign is +1 for upper, -1 for lower."""
        while h and stale[sign * h[0]] > 0:
            stale[sign * h[0]] -= 1
            heapq.heappop(h)

    for i, x in enumerate(nums):
        # Step 1: insert.
        if not lower or x <= -lower[0]:
            heapq.heappush(lower, -x)
            balance += 1
        else:
            heapq.heappush(upper, x)
            balance -= 1

        # Step 2: expire (once the window is full).
        if i >= k:
            old = nums[i - k]
            stale[old] += 1
            if old <= -lower[0] if lower else False:
                balance -= 1
            else:
                balance += 1

        # Step 3: rebalance.
        if balance > 1:
            heapq.heappush(upper, -heapq.heappop(lower))
            balance -= 2
        elif balance < 0:
            heapq.heappush(lower, -heapq.heappop(upper))
            balance += 2

        # Step 4: prune stale tops.
        prune(lower, -1)
        prune(upper, +1)

        # Step 5: emit median once the window is full.
        if i >= k - 1:
            if k % 2 == 1:
                result.append(float(-lower[0]))
            else:
                result.append((-lower[0] + upper[0]) / 2.0)

    return result
```

About 45 lines. The bookkeeping (`balance`, `stale`, `prune`) is more involved than the bare two-heap from Exercise 3; that is the cost of the sliding-window composition.

**[R]** Trace on `nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3`. The trace is mechanical but useful to verify; do it in the write-up at least for the first three windows.

- i=0, x=1: lower=[-1] (negated). balance=1. i<k=3; no expire. balance=1; no rebalance needed (balance in {0,1}). prune (no stales). i < k-1; no emit.
- i=1, x=3: 3 > 1; push to upper. upper=[3]. balance=0. No expire. balance=0; no rebalance. No emit.
- i=2, x=-1: -1 <= 1; push to lower. lower=[-1, -1] (root -1). balance=1. No expire. balance=1; OK. Emit median: k odd; median = -lower[0] = 1.0. result=[1.0]. Correct.
- i=3, x=-3: -3 <= 1; push to lower. balance=2. Expire nums[0] = 1; 1 <= -lower_root? Yes; balance -= 1 = 1. stale[1] = 1. Rebalance? balance=1; OK. Prune lower: lower_root is -1 (max of lower = 1); stale[1]=1; pop it; stale[1]=0. lower=[-3, -1]. Emit: k=3, odd; median = -lower[0] = 3? Wait — lower stores -1 and -(-3)=3; the root (min of negated) is -3, so max of lower = 3. Hmm — let me re-trace ... [the trace continues].

The point of the trace is to catch bookkeeping bugs — the `balance` tracking and the stale-counter discipline are the hardest parts. Do at least two example traces in the Review.

Common bug avoided: forgetting that `stale[old] += 1` does *not* immediately remove `old` from the heap. It only marks it for deferred removal. Forgetting the `prune` call after each insert/expire is the most common bug.

**[E]** **Time `O(n log k)`** per slide amortized: each element is pushed at most once (`O(log k)`) and popped at most twice (real + stale; `O(log k)`). Total over `n` slides: `O(n log k)`. **Space `O(k)`** for the heaps and `O(k)` for the stale counter; total `O(k)`. **Tradeoff vs sorted-list with bisect**: `bisect.insort` is `O(k)` per add (list-shift cost); slow at `k = 10⁵`. The two-heap + lazy deletion is the canonical answer. **Tradeoff vs `sorted.SortedList` from the `sortedcontainers` library**: `O(log k)` per add and remove; cleaner code; allowed in some interviews but the `heapq` version is the "from-first-principles" answer interviewers grade.

---

## Cross-references rubric

The two write-ups are graded as a *pair*. At the bottom of each write-up, include a "Cross-references" section that points to:

- The relevant lecture section (Problem 1 → Lecture 1 §4 on top-k template + Lecture 2 §2 on tiebreakers; Problem 2 → Lecture 3 §1 on two-heap + §4 on lazy deletion).
- The relevant exercise (Problem 1 → Exercise 1 on plain top-k; Problem 2 → Exercise 3 on two-heap median).
- The *other* mini-project problem. Specifically, the cross-reference text should be a 1-2 sentence comparison: "*Problem 2 uses two heaps with a balance invariant; the structural parallel with Problem 1 is the heap-based template — the differences are (a) bounded vs unbounded heap, (b) one heap vs two, (c) size invariant vs balance invariant.*"

The cross-references are what make the pair navigable as a portfolio artifact. A reviewer (or interviewer) should be able to read Problem 1, click through to Problem 2, and immediately see the structural relationship.

---

## File-level template

Each problem write-up follows this skeleton. Save as `problem-NN-<slug>.md`.

```markdown
# Problem NN — <name> (<LC reference>)

> **30-second pattern-recognition memo [top-k / two-heap]:**
> [six lines as above]

## Problem

[Spec + 2-3 examples.]

## Why this template

[1 paragraph: what makes this template distinct from the other; one sentence comparing against the other mini-project problem.]

## UMPIRE write-up

### Understand
### Match
[Expanded body — comparison against the other template, rejection of one wrong pattern.]
### Plan
### Implement
[Code with brief inline narration.]
### Review
[Trace on 2 examples + 1 common bug avoided.]
### Evaluate
[5-piece from W2, with the time-defense sentence cleanly delivered.]

## Cross-references

- Lecture: [link to relevant section]
- Exercise: [link to relevant exercise]
- Sister mini-project problem: [link with 1-2 sentence comparison]

## What I would do differently next time

[Optional but recommended: 1-2 sentences.]
```

---

## Acceptance criteria

- [ ] Both write-ups present in `umpire-writeups/c2-week-08/mini-project/`.
- [ ] Each write-up has a leading 30-second memo following the schema above.
- [ ] **Problem 1 uses the top-k memo schema; Problem 2 uses the two-heap memo schema.**
- [ ] Each write-up has all six UMPIRE sections fully written out (no "see exercise" placeholders).
- [ ] Each write-up has a trace on at least two examples in the Review section.
- [ ] Each write-up has a Cross-references section linking to the other mini-project problem with a 1-2 sentence comparison.
- [ ] Both `.py` solution files (extracted from the Implement sections) are present and pass their respective LeetCode test cases.

---

## Suggested order of operations

### Thursday — drafting (1.5h)

1. Open the mini-project folder. Create three empty files (the two problem write-ups + this README).
2. For each problem, write only the **30-second memo** at the top. Do not write the rest yet. Read each memo aloud; sharpen until it hits 25-30 seconds.
3. Commit "Mini-project memos drafted."

### Friday — Problem 1 (3h)

4. Write up Problem 1 in full UMPIRE. Allow 3 hours — the in-depth Understand and Match are the time-consuming parts. The "conflicting-direction tiebreaker" Match move is the senior signal; spend the time getting that paragraph right.
5. Trace at least two examples in Review.
6. Code + commit.

### Saturday — Problem 2 (3h)

7. Write up Problem 2 in full UMPIRE. Cross-reference back to Problem 1 in the Match section ("size-k bounded vs unbounded; one heap vs two; size invariant vs balance invariant" — the structural parallel).
8. Trace at least two examples in Review.
9. Code + commit.

### Sunday — polish + push (0.5h)

10. Add cross-references at the bottom of each write-up.
11. Re-read both memos aloud one last time; sharpen anything that runs over 30 seconds.
12. Score yourself against the per-problem rubric. If anything is "vague" or "missing the boundary defense," sharpen it.
13. Push.

---

## What "great" looks like (final rubric)

A learner who has shipped this mini-project *well* has:

- Both memos under 30 seconds when read aloud.
- Match sections that explicitly compare the two templates (top-k vs two-heap; bounded vs unbounded; one heap vs two).
- Implement sections with the heap setup (initial seed, bound, invariant restore) clearly visible as a named function or labeled block.
- Cross-references at the bottom of each write-up linking to the other.
- Recordings ≥ 20 minutes each, with the full UMPIRE narration.

A learner who has shipped this mini-project *poorly* has:

- Memos that run 60+ seconds — too verbose, missing the cadence.
- Match sections that name "heap" but do not specify the sub-shape or invariant.
- Implement sections without a clearly extracted size bound (Problem 1) or balance discipline (Problem 2).
- No cross-references; each write-up reads as a stand-alone with no awareness of the other.

If you catch yourself producing the "poorly" shape, the fix is to re-read [Lecture 1 §7](../02-lecture-notes/01-heapq-and-top-k.md) (the 30-second recognition signals) and [Lecture 3 §7](../02-lecture-notes/03-two-heap-and-k-way-merge.md) (the complete decision tree) and re-do whichever write-up is weaker.

---

## Why one of each specifically

Two reasons.

1. **One top-k + one two-heap is the diet of a real heap interview.** Phase 2 onsites typically ask one heap problem; that problem is either a "find k-something" (50% of the time) or a "running statistic on a stream" (50% of the time). Shipping one of each guarantees you have practiced the at-bat for whichever you draw.

2. **The syllabus mandates exactly this composition.** From the Week 8 line in `SYLLABUS.md`: *"Mini-project: A top-k problem (k-largest, k-frequent, k-closest family) and a two-heap problem (median, running statistic, sliding-window statistic). Both UMPIRE-narrated."* The composition is the contract.

If you finish before Sunday with energy to spare, add a third write-up from the LeetCode Heap tag at your discretion — for example, "Find K Pairs with Smallest Sums" (LC 373) is a great stretch because the senior insight is that **a heap of pairs can be primed lazily** rather than enumerating all `n²` pairs upfront. The acceptance criterion is *two* — anything beyond is bonus.

---

When done: push everything, then move on to [Week 9 — Mock Interview #2](../../week-09-mock-interview-2/).

Phase 2's fourth week is closed. Your portfolio now contains two canonical heap write-ups; that section will be referenced again in Mock #2 (Week 9) and in the capstone (Week 15).
