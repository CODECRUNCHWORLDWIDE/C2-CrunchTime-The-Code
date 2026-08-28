# The Built-In Complexity Cheat Sheet

Print this. Keep it open every week of the course. Every number here is CPython 3.11+.

Two rules before the tables:

1. **`n` always means "the size of the thing the operation touches."** For `a + b` on strings, the cost is `O(len(a) + len(b))` — not `O(n)` for some vague `n`. Say which `n` you mean out loud. Interviewers dock you for the vague version.
2. **Average is not worst.** Hash operations are `O(1)` *average* and `O(n)` *worst*. In an interview, say "`O(1)` average, `O(n)` worst under adversarial collisions, which is not a real concern here." That one sentence separates you from the candidate who just says "hash map is O(1)."

---

## Strings — immutable

Every operation that "changes" a string builds a new one. There is no in-place string edit in Python. That single fact drives most string-complexity mistakes.

| Operation | Time | Extra space | Note |
|---|---|---|---|
| `s[i]` | `O(1)` | `O(1)` | Returns a new 1-char string |
| `len(s)` | `O(1)` | `O(1)` | Stored, not counted |
| `s[a:b]` | `O(b - a)` | `O(b - a)` | **Slicing copies.** The classic hidden `O(n)` |
| `s[::-1]` | `O(n)` | `O(n)` | Reverse is a full copy |
| `a + b` | `O(len(a) + len(b))` | same | Builds a third string |
| `s += t` in a loop | **`O(n²)` total** | `O(n)` | See the join idiom below |
| `''.join(parts)` | `O(total chars)` | `O(total chars)` | The correct way to build |
| `s.split()` / `.split(sep)` | `O(n)` | `O(n)` | |
| `sub in s`, `s.find(sub)` | `O(n · m)` worst | `O(1)` | `n = len(s)`, `m = len(sub)` |
| `s.count(sub)` | `O(n · m)` | `O(1)` | |
| `s.replace(a, b)` | `O(n · m)` | `O(n)` | New string |
| `.upper() .lower() .strip()` | `O(n)` | `O(n)` | New string |
| `s.startswith/endswith(p)` | `O(len(p))` | `O(1)` | Cheaper than slicing to compare |
| `ord(c)` / `chr(i)` | `O(1)` | `O(1)` | |
| `a == b` | `O(min(len(a), len(b)))` | `O(1)` | Early exit on first mismatch |
| `sorted(s)` | `O(n log n)` | `O(n)` | Returns a **list**, not a string |

**On substring search.** The contract is `O(n · m)` worst case, and that is what you should state. CPython 3.10+ switches to a two-way (Crochemore–Perrin) algorithm for longer needles, so in practice you get `O(n + m)`. Say the worst case, then mention the implementation detail — never lead with it.

**The join idiom.** This is the single most common complexity bug in warm-up code:

```python
# O(n^2): each += builds a whole new string
out = ""
for ch in chars:
    out += ch

# O(n): collect, then join once
parts = []
for ch in chars:
    parts.append(ch)
out = "".join(parts)
```

CPython has an optimization that *sometimes* makes `+=` amortized `O(n)` when the string has exactly one reference. It is an implementation detail, it silently stops applying, and no interviewer will credit it. Use `join`.

---

## Lists — dynamic array

A list is a contiguous array of pointers with spare capacity on the end. Everything below follows from that one sentence: cheap at the end, expensive at the front, cheap to index, expensive to search.

| Operation | Time | Extra space | Note |
|---|---|---|---|
| `L[i]` get / set | `O(1)` | `O(1)` | Contiguous — this is the whole point |
| `len(L)` | `O(1)` | `O(1)` | |
| `L.append(x)` | **amortized `O(1)`** | `O(1)` | Single resize is `O(n)`; see below |
| `L.pop()` | `O(1)` | `O(1)` | From the **end** |
| `L.pop(0)` | `O(n)` | `O(1)` | Shifts every element left |
| `L.insert(0, x)` | `O(n)` | `O(1)` | Shifts every element right |
| `L.insert(i, x)` / `del L[i]` | `O(n - i)` | `O(1)` | |
| `L.remove(x)` | `O(n)` | `O(1)` | Search, then shift |
| `x in L` | `O(n)` | `O(1)` | **Not** a hash lookup. Use a set |
| `L.index(x)` | `O(n)` | `O(1)` | |
| `L[a:b]` | `O(b - a)` | `O(b - a)` | Copies |
| `L1 + L2` | `O(n + m)` | `O(n + m)` | |
| `L.extend(other)` | amortized `O(k)` | `O(k)` | `k = len(other)` |
| `L * k` | `O(n · k)` | `O(n · k)` | Watch the aliasing trap below |
| `L.sort()` / `sorted(L)` | `O(n log n)` | `O(n)` | Timsort. `O(n)` on already-sorted input |
| `L.reverse()` | `O(n)` | `O(1)` | In place |
| `min/max/sum(L)` | `O(n)` | `O(1)` | |
| `L.count(x)` | `O(n)` | `O(1)` | |
| `list(L)` / `L.copy()` | `O(n)` | `O(n)` | **Shallow** |

**Amortized append, said properly.** When the array fills, CPython allocates a larger block (growth factor ≈ 1.125 plus a constant) and copies. Any single append can be `O(n)`; the total cost of `n` appends is `O(n)`, so each is `O(1)` amortized. The sentence to say out loud: *"Append is amortized O(1) — individual resizes are O(n), but the geometric growth means n appends cost O(n) total."*

**The aliasing trap.** `*` copies references, not objects:

```python
grid = [[0] * 3] * 2      # WRONG — both rows are the SAME list
grid[0][0] = 9            # grid is now [[9, 0, 0], [9, 0, 0]]

grid = [[0] * 3 for _ in range(2)]   # RIGHT — two independent rows
```

`[0] * 3` is fine (ints are immutable). `[list] * n` is the bug.

**When a list is the wrong tool.** If you need cheap operations at *both* ends, use `collections.deque`.

| `deque` operation | Time | Note |
|---|---|---|
| `append` / `appendleft` | `O(1)` | Both ends, genuinely |
| `pop` / `popleft` | `O(1)` | This is why BFS uses a deque |
| `d[i]` for middle `i` | `O(n)` | Block-linked, not contiguous |

A `deque` trades `O(1)` random access for `O(1)` front operations. A queue built on `list.pop(0)` is `O(n²)` overall and will cost you the round.

---

## Tuples — immutable sequence

| Operation | Time | Note |
|---|---|---|
| `t[i]`, `len(t)` | `O(1)` | |
| `t[a:b]` | `O(b - a)` | Copies |
| `t1 + t2` | `O(n + m)` | New tuple |
| `x in t` | `O(n)` | Linear, like a list |
| `hash(t)` | `O(n)` | Only if every element is hashable |

The reason tuples matter in this course is **hashability**. A tuple of hashables can be a dict key or a set member; a list never can. That is what makes `tuple(sorted(word))` the canonical anagram key and `(row, col)` the canonical grid-visited key.

---

## Dicts — hash table

Open addressing, with insertion order guaranteed since Python 3.7 (it is a language guarantee now, not an implementation detail — you may rely on it).

| Operation | Time (average) | Time (worst) | Extra space |
|---|---|---|---|
| `d[k]` get / set | `O(1)` | `O(n)` | `O(1)` |
| `k in d` | `O(1)` | `O(n)` | `O(1)` |
| `del d[k]` | `O(1)` | `O(n)` | `O(1)` |
| `d.get(k, default)` | `O(1)` | `O(n)` | `O(1)` |
| `d.setdefault(k, v)` | `O(1)` | `O(n)` | `O(1)` |
| `len(d)` | `O(1)` | `O(1)` | `O(1)` |
| Iterate `d` / `.keys()` / `.items()` | `O(n)` | `O(n)` | `O(1)` — views are lazy |
| `d.copy()` / `dict(d)` | `O(n)` | `O(n)` | `O(n)` — shallow |
| `d1 \| d2` (merge) | `O(n + m)` | | `O(n + m)` |

Whole-dict space is `O(n)`, with real constant-factor overhead — a dict of `n` entries costs several times what a list of `n` items costs. Mention that only if asked about memory pressure.

**The worst case is real but not your problem.** `O(n)` happens when every key collides. With Python's built-in hashes and non-adversarial input it does not occur. Say it, dismiss it, move on.

**The three helpers worth knowing cold:**

```python
from collections import defaultdict, Counter

freq = defaultdict(int)          # missing key -> 0, no KeyError
for ch in s:
    freq[ch] += 1

groups = defaultdict(list)       # missing key -> [], no setdefault dance
for word in words:
    groups[tuple(sorted(word))].append(word)

counts = Counter(s)              # O(n) construction, does the above for you
counts.most_common(k)            # O(n log k) — uses a size-k heap
counts.most_common()             # O(n log n) — no argument means full sort
```

`Counter` also supports `+ - & |` between counters, each `O(n + m)`. `counts_a - counts_b` keeps only positive counts — occasionally the whole solution to a "can we build this from that" problem.

---

## Sets — hash table without values

| Operation | Time (average) | Note |
|---|---|---|
| `add` / `remove` / `discard` | `O(1)` | `remove` raises on missing; `discard` does not |
| `x in s` | `O(1)` | The reason sets exist |
| `len(s)` | `O(1)` | |
| `s \| t` (union) | `O(len(s) + len(t))` | |
| `s & t` (intersection) | `O(min(len(s), len(t)))` | Iterates the smaller one |
| `s - t` (difference) | `O(len(s))` | |
| `s ^ t` (symmetric difference) | `O(len(s) + len(t))` | |
| `s <= t` (subset) | `O(len(s))` | |
| `set(iterable)` | `O(n)` | |

Worst case for the single-element operations is `O(n)`, same caveat as dicts.

**`frozenset`** is the immutable, hashable version. Use it when a *set* needs to be a dict key or live inside another set.

**The swap that wins rounds.** Turning `x in some_list` (`O(n)`) into `x in some_set` (`O(1)`) converts an `O(n²)` loop into `O(n)`. It costs `O(n)` time and `O(n)` space to build the set. State that trade explicitly — the space cost is the thing interviewers want to hear you acknowledge.

---

## Heaps — `heapq` on a plain list

| Operation | Time | Note |
|---|---|---|
| `heapq.heapify(L)` | `O(n)` | In place. **Not** `O(n log n)` — this surprises people |
| `heapq.heappush(h, x)` | `O(log n)` | |
| `heapq.heappop(h)` | `O(log n)` | Smallest |
| `h[0]` | `O(1)` | Peek without popping |
| `heapq.heappushpop(h, x)` | `O(log n)` | One sift, not two |
| `heapq.nlargest(k, L)` | `O(n log k)` | |

`heapq` is a **min-heap only**. For a max-heap, push `-x`, or push `(-key, item)` tuples. Week 8 goes deep; this row exists so the cheat sheet is complete.

---

## What is hashable

A dict key or set member must be hashable. Hashable means immutable, all the way down.

| Hashable | Not hashable |
|---|---|
| `int`, `float`, `bool`, `str`, `bytes` | `list` |
| `tuple` — **only if every element is** | `dict` |
| `frozenset` | `set` |
| `None` | `bytearray` |

```python
seen = set()
seen.add((row, col))              # fine — tuple of ints
seen.add([row, col])              # TypeError: unhashable type: 'list'
seen.add(tuple(sorted(word)))     # the anagram-key idiom
```

`tuple([1, [2]])` is a tuple but is **not** hashable — it contains a list. "Immutable all the way down" is the actual rule.

---

## Sorting

| Call | Time | Space | Note |
|---|---|---|---|
| `L.sort()` | `O(n log n)` | `O(n)` | In place, returns `None` |
| `sorted(iterable)` | `O(n log n)` | `O(n)` | Returns a new list |
| `sorted(L, key=f)` | `O(n log n)` calls to `f` | `O(n)` | `f` runs **once per element**, not per comparison |
| `sorted(L, reverse=True)` | `O(n log n)` | `O(n)` | |

Timsort is **stable** — equal elements keep their original relative order. That is a guarantee you can rely on, and it is how you sort by two keys without writing a comparator:

```python
records.sort(key=lambda r: r.name)      # secondary key first
records.sort(key=lambda r: r.score)     # primary key second — stability preserves name order
records.sort(key=lambda r: (-r.score, r.name))   # or do it in one pass with a tuple key
```

Timsort is `O(n)` on already-sorted or reverse-sorted input. If a problem says "the array is nearly sorted," that is worth a sentence.

---

## The five costs people forget to state

Say these out loud when they apply. Each one is a place candidates silently lose points.

1. **Slicing copies.** `s[1:]` inside a loop turns `O(n)` into `O(n²)`. Pass indices instead.
2. **`sorted()` allocates.** Claiming `O(1)` space after calling `sorted()` is wrong — it is `O(n)`.
3. **Recursion uses stack space.** A recursive DFS on `n` nodes is `O(n)` space in the worst case even with no explicit data structure.
4. **The output can dominate.** Returning all subsets is `O(2ⁿ)` space no matter how clever the algorithm. Distinguish *auxiliary* space from *output* space and say which you mean.
5. **Building the hash structure costs.** "Use a set for `O(1)` lookup" is `O(n)` time and `O(n)` space up front. For a single lookup on a sorted array, binary search wins.

---

## The complexity sentence

Every Examine (cost) step in this course uses this shape. Fill in all five slots:

> **Time `O(_)`** because `_`. **Space `O(_)`** auxiliary, `O(_)` including output, because `_`. The alternative was `_`, which is `O(_)` — I chose this one because `_`.

Worked, on "two-sum with a hash map":

> **Time O(n)** because we make one pass and each dict lookup is O(1) average. **Space O(n)** auxiliary because the dict holds up to n entries; output is O(1). The alternative was the nested-loop scan at O(n²) time and O(1) space — I traded O(n) space for a factor of n in time, which is the right trade unless memory is constrained.

---

## Up Next

- [Lecture 1 — Strings](lecture-notes/01-strings-and-immutability.md)
- [Lecture 2 — Lists, Tuples and the Dynamic Array](lecture-notes/02-lists-tuples-and-the-dynamic-array.md)
- [Lecture 3 — Dicts, Sets and the Hash Table](lecture-notes/03-dicts-sets-and-the-hash-table.md)
- [Week 0 self-check](quiz.md) — if you pass it cold, skip to [Week 1](../week-01-the-frame-method-and-thinking-aloud/README.md)
