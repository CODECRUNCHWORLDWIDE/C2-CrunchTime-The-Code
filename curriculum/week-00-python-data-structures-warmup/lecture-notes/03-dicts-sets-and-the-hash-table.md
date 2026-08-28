# Lecture 3 — Dicts, Sets and the Hash Table

**Reading time:** ~40 minutes. REPL open.

This is the highest-leverage lecture in Week 0. More interview solutions turn on "use a hash map" than on any other single idea, and more candidates state its complexity sloppily than any other.

---

## 1. How a dict actually works

A dict stores entries in an array of slots. To find where key `k` lives:

1. Compute `hash(k)` — for built-in types this is `O(1)` for numbers and `O(len)` for strings, cached after the first call.
2. Take the low bits of that hash to get a slot index.
3. If the slot holds a different key (a **collision**), probe to another slot by a deterministic rule until you find the key or an empty slot.

Two facts fall out:

- **Average case `O(1)`.** With a good hash and a load factor kept below ~2/3 (CPython resizes to maintain this), the expected number of probes is a small constant, independent of `n`.
- **Worst case `O(n)`.** If every key hashes to the same slot, every lookup degenerates to a linear scan of the probe sequence.

**How to say it.** Not "dict lookup is O(1)." Say:

> Dict lookup is O(1) average. Worst case is O(n) if every key collides, which requires either adversarial input or a pathological hash function — not a concern here.

That is one extra sentence and it is the difference between sounding like you memorized a fact and sounding like you understand the structure.

**Order is guaranteed.** Since Python 3.7, dicts preserve insertion order as a **language guarantee**, not a CPython implementation detail. You may rely on it. (It was true in CPython 3.6 as an accident of the implementation; 3.7 made it official.) This matters when a problem asks for "first occurrence" or "in the order they appeared" — you get it free, no `OrderedDict` needed.

---

## 2. The dict cost table

| Operation | Average | Worst | Space |
|---|---|---|---|
| `d[k]` (get) | `O(1)` | `O(n)` | `O(1)` |
| `d[k] = v` (set) | `O(1)` | `O(n)` | `O(1)` amortized |
| `k in d` | `O(1)` | `O(n)` | `O(1)` |
| `del d[k]` | `O(1)` | `O(n)` | `O(1)` |
| `d.get(k, default)` | `O(1)` | `O(n)` | `O(1)` |
| `d.setdefault(k, v)` | `O(1)` | `O(n)` | `O(1)` |
| `d.pop(k)` | `O(1)` | `O(n)` | `O(1)` |
| `len(d)` | `O(1)` | `O(1)` | `O(1)` |
| Iterate `d` | `O(n)` | `O(n)` | `O(1)` |
| `d.keys()` / `.values()` / `.items()` | `O(1)` to create | | `O(1)` |
| `dict(d)` / `d.copy()` | `O(n)` | | `O(n)` shallow |
| `d1 \| d2` | `O(n + m)` | | `O(n + m)` |

**Views are lazy.** `d.items()` does not build a list — it returns a view object in `O(1)` and `O(1)` space. Iterating the view is `O(n)`. The view also stays live: if you mutate `d`, the view reflects it. Do not mutate a dict while iterating its view; that raises `RuntimeError`.

**Whole-dict space is `O(n)`** with a meaningful constant factor — a dict of `n` entries costs several times what a list of `n` items costs, because of the slot array, the hashes, and the spare capacity. Only worth mentioning if the interviewer asks about memory pressure.

---

## 3. The four ways to handle a missing key

All four are `O(1)` average. Choosing well is a readability signal, and interviewers do read for it.

```python
# 1. Explicit check — verbose, but fine
if k in d:
    v = d[k]
else:
    v = 0

# 2. get with a default — best when you only READ
v = d.get(k, 0)

# 3. setdefault — reads AND inserts the default. One lookup, not two
d.setdefault(k, []).append(x)

# 4. defaultdict — the default is built automatically on any miss
from collections import defaultdict
d = defaultdict(list)
d[k].append(x)
```

**The distinction that matters.** `d.get(k, [])` does **not** store anything — `d.get(k, []).append(x)` appends to a throwaway list and silently does nothing. `setdefault` and `defaultdict` do store. This is a real bug people ship.

**One `defaultdict` gotcha:** merely *reading* a missing key inserts it.

```python
d = defaultdict(int)
if d[k] > 0:      # this INSERTS k with value 0
    ...
len(d)            # grew, surprisingly
```

Use `d.get(k, 0)` when you only want to look.

---

## 4. `Counter` — the frequency map you should not hand-roll

```python
from collections import Counter

counts = Counter("mississippi")
# Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})
```

| Operation | Cost |
|---|---|
| `Counter(iterable)` | `O(n)` time, `O(k)` space for `k` distinct items |
| `counts[x]` | `O(1)` average — missing keys return `0`, no `KeyError` |
| `counts.most_common(k)` | `O(n log k)` — uses a size-`k` heap |
| `counts.most_common()` | `O(n log n)` — no argument means a full sort |
| `a + b`, `a - b`, `a & b`, `a \| b` | `O(n + m)` |
| `counts.total()` | `O(k)` (Python 3.10+) |

The `most_common(k)` complexity is worth memorizing. `O(n log k)` — not `O(n log n)` — because it keeps a heap of size `k` rather than sorting everything. Week 8 makes you build that heap by hand; here, just know the cost and that the difference is real when `k << n`.

**Counter arithmetic** is occasionally the entire solution. `a - b` keeps only positive counts, which answers "can I build `a` from `b`" in one line:

```python
def can_build(target, pool):
    return not (Counter(target) - Counter(pool))     # O(n + m)
```

**Two frequency maps are equal iff the strings are anagrams**, and that comparison is `O(k)`:

```python
Counter(a) == Counter(b)          # O(n + m) total, beats sorting's O(n log n)
```

So why does anyone sort for anagrams? Because `tuple(sorted(w))` is *hashable* and can be a **dict key**, while a `Counter` cannot. When you need to *group* anagrams you need a key; when you only need to *compare two*, `Counter` wins on cost. Knowing which of those the problem asks for is the Research constraints step.

---

## 5. Sets

A set is a dict without values. Same hash table, same guarantees.

| Operation | Average | Worst |
|---|---|---|
| `s.add(x)` | `O(1)` | `O(n)` |
| `s.remove(x)` | `O(1)` | `O(n)` — raises `KeyError` if absent |
| `s.discard(x)` | `O(1)` | `O(n)` — silent if absent |
| `x in s` | `O(1)` | `O(n)` |
| `len(s)` | `O(1)` | `O(1)` |
| `set(iterable)` | `O(n)` | | 

Set algebra — note that the costs are **not** all the same:

| Operation | Cost | Why |
|---|---|---|
| `s \| t` (union) | `O(len(s) + len(t))` | Must touch everything |
| `s & t` (intersection) | `O(min(len(s), len(t)))` | Iterates the **smaller**, probes the larger |
| `s - t` (difference) | `O(len(s))` | Iterates `s` only |
| `s ^ t` (symmetric difference) | `O(len(s) + len(t))` | |
| `s <= t` (subset) | `O(len(s))` | |

Intersection being `O(min(...))` is a genuinely useful asymmetry. Intersecting a 10-element set with a million-element set is 10 probes, not a million.

**`frozenset`** is the immutable, hashable set. Use it when a set must be a dict key or a member of another set:

```python
seen_groups = set()
seen_groups.add(frozenset({1, 2, 3}))     # fine
seen_groups.add({1, 2, 3})                # TypeError: unhashable type: 'set'
```

---

## 6. The swap that wins rounds

This is the single most reusable optimization in interview coding.

```python
# O(n * m): `in` on a list is a linear scan
common = [x for x in a if x in b]

# O(n + m): pay O(m) once to build the set, then O(1) per test
b_set = set(b)
common = [x for x in a if x in b_set]
```

**Say the trade explicitly.** Not "I'll use a set because it's faster." Say:

> Membership on a list is O(n), so the nested version is O(n·m). Building a set costs O(m) time and O(m) space up front, after which each test is O(1) average — so the whole thing becomes O(n + m) time at the cost of O(m) space.

The space acknowledgement is the part candidates skip and interviewers are listening for.

**When *not* to do it.** If you test membership only once or twice, building the set is not worth it. And if the data is already sorted, binary search gives you `O(log n)` lookups with `O(1)` extra space — Week 5's argument.

---

## 7. What is hashable, exactly

A dict key or set member must be hashable. **Hashable means immutable, all the way down.**

| Hashable | Not hashable |
|---|---|
| `int`, `float`, `bool`, `str`, `bytes`, `None` | `list` |
| `tuple` — **only if every element is hashable** | `dict` |
| `frozenset` | `set` |
| Your own class — by default, hashed by identity | `bytearray` |

```python
hash((1, 2, 3))        # fine
hash((1, [2]))         # TypeError — the tuple contains a list
```

`(1, [2])` **is** a tuple and **is** immutable at the top level, but it is not hashable, because hashing it would require hashing the list inside. "Immutable all the way down" is the actual rule, and it is the precise answer to "why can't a list be a dict key?"

The two idioms this unlocks, used constantly from Week 6 onward:

```python
visited = set()
visited.add((row, col))                    # grid coordinate

groups = defaultdict(list)
groups[tuple(sorted(word))].append(word)   # canonical anagram key
```

**A note on `1 == 1.0 == True`.** All three hash equal and compare equal, so they collapse to one dict key:

```python
{1: 'a', 1.0: 'b', True: 'c'}      # {1: 'c'} — one entry
```

Rarely relevant, occasionally the explanation for a baffling bug.

---

## 8. The three canonical hash-map shapes

Almost every hash-map interview problem is one of these. Week 2 names them formally; recognize them now.

**Shape 1 — complement lookup.** "Have I already seen the thing that pairs with this?"

```python
seen = {}                        # value -> index
for i, x in enumerate(nums):
    if target - x in seen:       # O(1)
        return [seen[target - x], i]
    seen[x] = i
# O(n) time, O(n) space, one pass
```

**Shape 2 — frequency counting.** "How many times does each thing occur?"

```python
counts = Counter(nums)           # O(n) time, O(k) space
```

**Shape 3 — set membership / dedup.** "Have I seen this at all?"

```python
seen = set()
for x in nums:
    if x in seen:                # O(1)
        return True
    seen.add(x)
return False
# O(n) time, O(n) space
```

Each one trades `O(n)` space for an order-of-magnitude in time. Each one has an `O(n²)`/`O(1)`-space alternative, and each one is the right answer unless the problem explicitly constrains space. Naming the alternative and the trade — out loud — is the Examine (cost) step.

---

## 9. Worked example, with the full Examine sentence

**Task.** Given a list of words, return the groups of words that are anagrams of each other, each group in the order the words appeared.

```python
from collections import defaultdict

def group_anagrams(words):
    groups = defaultdict(list)
    for w in words:
        key = tuple(sorted(w))       # O(L log L) for a word of length L
        groups[key].append(w)        # O(1) average
    return list(groups.values())     # insertion order — guaranteed since 3.7
```

> **Time O(n · L log L)** where `n` is the number of words and `L` the max word length — we sort each word once to build its key, and each dict insert is O(1) average. **Space O(n · L)** auxiliary for the keys and grouped words; the output is also O(n · L). The alternative key was a `Counter` per word at O(L), which is asymptotically better — but a Counter is not hashable, so I would need `tuple(sorted(counter.items()))` to use it as a key, which reintroduces a sort over the distinct characters. For lowercase ASCII I could use a fixed 26-tuple of counts instead, giving O(n · L) overall; I chose the sorted-tuple key for clarity and would switch if L were large.

That is what a complete Examine looks like. It states both complexities, names the alternative, and gives the condition under which the choice flips.

---

## 10. Check yourself

1. Why is dict lookup `O(1)` average and `O(n)` worst? Say both sentences.
2. When did insertion order become a *guarantee*, and may you rely on it?
3. `d.get(k, []).append(x)` — what does it do, and why is it a bug?
4. `defaultdict(int)` — how can merely reading a key change `len(d)`?
5. `counts.most_common(k)` — `O(n log k)` or `O(n log n)`? Why?
6. `Counter(a) == Counter(b)` vs `sorted(a) == sorted(b)` for anagrams — costs, and when you must use the second.
7. Why is `s & t` cheaper than `s | t`?
8. `hash((1, [2]))` raises. The tuple is immutable. Explain precisely.
9. Rewrite `[x for x in a if x in b]` to be linear, and state the trade in one sentence.
10. Name the three hash-map shapes and the space each one costs.

---

## Up Next

- [The cheat sheet](../CHEATSHEET.md) — read it end to end now that the reasoning is in place.
- [The exercises](../exercises/README.md) — six drills, all original to this course.
- [The self-check](../quiz.md) — 20 questions. Then [Week 1](../../week-01-the-frame-method-and-thinking-aloud/README.md).
