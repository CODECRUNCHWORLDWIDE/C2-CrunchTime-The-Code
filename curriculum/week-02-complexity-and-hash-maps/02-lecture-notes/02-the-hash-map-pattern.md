# Lecture 2 — The Hash Map Pattern

> **Duration:** ~2 hours.
> **Outcome:** You can recognize a hash-map problem within 30 seconds, name the three sub-shapes of the pattern, articulate the O(1)-average-versus-O(n)-space tradeoff out loud, and defend the hash-map choice over two-pointer (or vice versa) on the right axis.

Last week we learned to *talk while we code*. This week we learn to *reach for the right data structure*. The hash map is the most-used pattern in interview problems — more than two pointers, more than sliding window — because it shows up the moment a problem says "unsorted," "count," "frequency," "have I seen this before," or "complement."

By the end of this lecture you should be reaching for `dict` and `set` with the same instinct that, last week, made you reach for `left` and `right`.

---

## 1. What "hash map" means in an interview

In Python, a **hash map** is a `dict`. A **hash set** is a `set`. They are the same underlying mechanism: a hash function maps keys to buckets, with collision-handling to keep lookups close to O(1).

In an interview you can use either word — *hash map*, *hash table*, *dict*, *dictionary*. They mean the same thing. Pick one and stick with it. Most American interviewers say "hash map." Most Python-focused interviewers say "dict." Both are correct.

The two operations you care about, with their costs:

| Operation | Cost |
|-----------|------|
| `d[k] = v` (insert) | O(1) amortized average |
| `d[k]` (lookup) | O(1) average |
| `k in d` (membership) | O(1) average |
| `del d[k]` (delete) | O(1) amortized average |
| `for k in d` (iterate) | O(n) — touches every key |
| `len(d)` | O(1) |

For `set`, replace "key" with "element"; the costs are identical.

**The O(1) average is the entire reason hash maps are useful.** If you can re-express "for each pair `(i, j)`, check something" as "for each `i`, *look up* something derived from `i`," you've gone from O(n²) to O(n) at the cost of O(n) space.

That trade — **O(n²) time → O(n) time + O(n) space** — is the pattern.

---

## 2. When the sorted-array two-pointer doesn't apply, hash map usually does

Week 1's two-pointer pattern is brilliant when the input is sorted. **But many real problems are unsorted, or sorting would scramble information you need to preserve** (e.g., original indices). In those cases the hash map is the go-to.

The decision tree, drilled until it's reflex:

```
Problem: "find pair / count / lookup / frequency"

├── Input sorted?
│   └── Yes ──→ converging two-pointer (Week 1)         O(n) time, O(1) space
│
├── Input unsorted, sorting would help?
│   └── Yes ──→ sort first, then two-pointer            O(n log n) time, O(1) space
│
└── Input unsorted, indices matter or sorting too slow?
    └── Yes ──→ hash map                                O(n) time, O(n) space
```

In an interview, after Match, your Plan step should *name which branch of this tree* you took and why.

---

## 3. The three sub-shapes of the hash-map pattern

Just like two-pointer had three sub-shapes (converging, same-direction, two-input), the hash-map pattern has three.

| Sub-shape | What it looks like | Use case |
|-----------|--------------------|----------|
| **Complement lookup** | For each element, look up its complement; cache as you go | Two-sum unsorted, "has seen target − x?" |
| **Frequency / counting** | Build a `dict` of `value → count` (or `Counter`); use the counts | Anagrams, top-K-frequent, duplicates |
| **Set membership** | Build a `set` of seen / forbidden / required elements; query in O(1) | Contains-duplicate, longest-consecutive, valid-sudoku |

Most hash-map problems are one of these three. Knowing which one buys you a fast Plan step.

---

## 4. Sub-shape 1: Complement lookup (the two-sum family)

The canonical interview problem. Given an unsorted array `nums` and target `t`, return indices of two numbers summing to `t`.

### The naive O(n²) version

```python
def two_sum_naive(nums, target):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```

For every pair `(i, j)`, check if they sum to `target`. **O(n²) time, O(1) space.** Works; in an interview at n > 10⁴ it will time out.

### The hash-map O(n) version

```python
def two_sum(nums, target):
    seen = {}                              # value → index
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return [seen[complement], i]   # earlier index first
        seen[x] = i
    return []
```

The trick: instead of asking "for each pair `(i, j)`, do they sum to target?", ask "for each element `x`, have I seen `target − x` already?"

- Walk through the array once.
- For each `x`, compute `complement = target - x`.
- Look it up in the hash map (O(1) average).
- If found → return both indices.
- If not → cache the current value with its index, move on.

**O(n) time, O(n) space.** Single pass. The hash map *replaces* the inner loop.

### Recognition signals for complement lookup

- "Find pair / triple summing to target" with unsorted input
- "Find pair whose difference is k"
- "Find x such that some derived value is in the array"
- "Have I seen something before that completes this?"

### Variants to recognize

- **Two-sum** — pairs summing to target. (Drill 1 this week.)
- **Two-sum with difference k** — `seen` stores values; check both `x + k` and `x - k`.
- **Subarray sum equals k** — prefix sums + hash map of seen prefix sums. (Challenge 1.)
- **Continuous subarray sum is multiple of k** — prefix sums modulo k + hash map.
- **First element with X property** — "first non-repeated character" is two passes over the same `Counter`.

---

## 5. Sub-shape 2: Frequency / counting (the anagram family)

The second canonical use: build a *count* of each value, then act on the counts.

### Canonical problem: are two strings anagrams of each other?

```python
def is_anagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in t:
        if ch not in counts or counts[ch] == 0:
            return False
        counts[ch] -= 1
    return True
```

**O(n) time, O(k) space**, where k is the size of the alphabet (often O(1) for ASCII — 256 characters at most).

### `collections.Counter` shortcut

Python's `Counter` makes this a one-liner:

```python
from collections import Counter

def is_anagram(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)
```

In an interview, **either version is fine.** The hand-rolled version shows you understand the mechanism. The `Counter` version shows you know the standard library. Most interviewers prefer the latter for production code and the former when probing your understanding. When in doubt, mention both: *"I can use Counter for brevity, but under the hood it's a dict of value → count — same complexity."*

### Canonical problem: group anagrams together

```python
from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))   # canonical form
        groups[key].append(s)
    return list(groups.values())
```

The key insight: **two strings are anagrams iff their sorted-character tuples are equal.** Use that tuple as the dict key. Each string maps to its bucket in O(k log k) where k is string length; total **O(n · k log k)** time, **O(n · k)** space. Drill 3.

### Recognition signals for counting / frequency

- "Are these two collections the same multiset?"
- "Top K most frequent"
- "First non-repeating character"
- "Find the majority element"
- "Group by some equivalence relation" (use the canonical form as the dict key)

### Variants

- **Top K frequent elements** (Week 9, with a heap).
- **First non-repeating character** — one pass to count, second pass to find the first whose count is 1.
- **Find all anagrams in a string** — combines counting with sliding window (Week 3).

---

## 6. Sub-shape 3: Set membership (the "have I seen this?" family)

When you don't need a value associated with a key, just *presence*, use a `set`. Smaller memory footprint than a dict; same O(1) average lookup.

### Canonical problem: does the array contain a duplicate?

```python
def contains_duplicate(nums: list[int]) -> bool:
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False
```

**O(n) time, O(n) space.** The two-pointer version requires sorting first, which costs O(n log n). When the input is unsorted and you only need a yes/no, the set is strictly better. Drill 2.

### Canonical problem: longest consecutive sequence

```python
def longest_consecutive(nums: list[int]) -> int:
    nums_set = set(nums)
    best = 0
    for x in nums_set:
        if x - 1 not in nums_set:        # x is a "sequence start"
            length = 1
            while x + length in nums_set:
                length += 1
            best = max(best, length)
    return best
```

The trick: **only start counting from a sequence's smallest element.** That ensures each element is touched at most twice (once when we check `x - 1 not in set`, once when extending). **O(n) time, O(n) space.** Drill 5.

The naive sort-then-scan is O(n log n). The hash-set version is O(n). That gap is the entire point of the drill.

### Recognition signals for set membership

- "Does the array contain a duplicate?"
- "Find the longest consecutive sequence in any order"
- "Validate Sudoku rows / columns / boxes" (Drill 4)
- "Is X in the forbidden list?" inside a tight loop
- "Have I visited this node before?" (graph traversal, Weeks 6-7)

---

## 7. Caching past values during one pass — the "single-pass" idiom

A pattern that ties the three sub-shapes together: **as you walk through the input, build up a hash map of what you've seen so far, and query it on the current element.** This idiom — *cache as you go* — is the most common shape of hash-map solutions.

The two-sum solution is the canonical example. Pseudocode:

```
seen = {}            # or set()
for each element x in input:
    answer-question-using(seen, x)
    seen[x] = something
```

This shape:

- Single pass through the input → O(n) time
- Hash-map operations are O(1) average → no inner loop
- Space O(n) worst case (the hash map can grow to hold all inputs)

When you see a problem that *feels* like it needs two nested loops over the same input, **try the single-pass cache shape first.** It will work surprisingly often.

---

## 8. Worked example — Subarray sum equals k

This is one of the most discriminating mid-level interview problems. We will not solve it in full here (it's Challenge 1), but we will narrate the *pattern match*.

**Problem.** Given an array of integers `nums` and an integer `k`, return the number of contiguous (non-empty) subarrays whose sum equals `k`.

**The naive O(n²) approach.** For each starting index `i`, compute running sum for each ending index `j ≥ i`; count matches.

**The hash-map O(n) approach.** Let `S_i = nums[0] + nums[1] + ... + nums[i-1]` be the *prefix sum* up to index `i`. A subarray `nums[i..j]` sums to `k` iff `S_{j+1} − S_i = k`, iff `S_i = S_{j+1} − k`.

So: walk through the prefix sums; at each `S_j`, count how many previous prefix sums equal `S_j − k`. That count comes from a hash map of seen prefix sums.

```python
def subarray_sum_count(nums, k):
    counts = {0: 1}          # empty prefix has sum 0
    running = 0
    answer = 0
    for x in nums:
        running += x
        answer += counts.get(running - k, 0)
        counts[running] = counts.get(running, 0) + 1
    return answer
```

**O(n) time, O(n) space.** Single pass. The hash-map idiom replaces the inner loop *and* tracks frequency — both sub-shapes at once.

Why this matters: the prefix-sum + hash-map combo shows up in subarray-property problems constantly. Recognizing it within 30 seconds is the interview tell. We'll drill it in Challenge 1.

---

## 9. The "I'll just use a set" temptation (and when it's wrong)

Sometimes a `set` doesn't carry enough information. Examples:

- **Two-sum needs indices**, not just values. Use a `dict` mapping value → index.
- **Group anagrams** needs to *collect* the originals per key. Use `defaultdict(list)`.
- **First non-repeating character** needs counts, not membership. Use a `Counter`.

The rule of thumb: **`set` for presence; `dict` for presence + payload.** When the problem says "return the *first* X" or "return *all* Xs," you usually need payload. When it says "are there any duplicates / collisions / overlaps?", a set suffices.

---

## 10. Common bugs in hash-map code

- **Forgetting `defaultdict` and crashing on missing keys.** `d[k] += 1` errors if `k` isn't there. Use `d[k] = d.get(k, 0) + 1` or `defaultdict(int)` or `Counter`.
- **Mutating a dict while iterating it.** `for k in d: del d[k]` raises `RuntimeError: dictionary changed size during iteration`. Make a list of keys to remove first, or build a new dict.
- **Using a mutable object as a key.** `{[1,2]: 'value'}` raises `TypeError: unhashable type: 'list'`. Use `tuple([1,2])` instead. Lists are unhashable; tuples and frozensets are hashable.
- **Comparing two dicts forgetting that key order doesn't matter.** `{'a': 1, 'b': 2} == {'b': 2, 'a': 1}` is True — equality in Python dicts ignores insertion order. Don't write defensive sort-the-keys code.
- **Claiming O(1) when the operation is actually O(k)** for a key of length k. Hashing a string is O(length-of-string), not O(1). For typical interview inputs this is rolled into the constant; but if the question is "hash a 10MB string," say so.
- **Allocating the hash map in the wrong scope.** If you `seen = set()` inside a loop, you create a fresh empty set each iteration. Hoist it out.

---

## 11. Self-check

Without notes, answer:

1. **Name the three sub-shapes of the hash-map pattern.** (Complement lookup; frequency / counting; set membership.)
2. **For each, name a canonical problem and its time / space complexity.**
3. **What's the difference between when you reach for two-pointer and when you reach for a hash map?** (Sorted → two-pointer; unsorted and you need O(n) time → hash map; willing to trade O(1) space for two-pointer's lower memory.)
4. **Why is `dict.get(k, 0)` preferable to `d[k]` when `k` may not exist?**
5. **What's the time complexity of `for k, v in d.items()`?** (O(n).)
6. **Trace `two_sum([3, 2, 4], 6)` step by step.** (At i=2, complement 2 is in `seen` with index 1, return `[1, 2]`.)
7. **When does set membership lose to two-pointer?** (When the problem requires O(1) space *and* offers sorted input.)

If you can answer all seven, proceed to [Lecture 3 — Stating Complexity Out Loud](./03-stating-complexity-out-loud.md).

---

## Further reading

- **"Fluent Python" by Luciano Ramalho — Chapter 3 (Dictionaries and Sets)** — library copy is fine.
- **CPython `dictobject.c` header comment** — read it once; it's elegant.
- **Raymond Hettinger's "Modern Dictionaries" PyCon talk** — free on YouTube.

Next: [Lecture 3 — Stating Complexity Out Loud](./03-stating-complexity-out-loud.md).
