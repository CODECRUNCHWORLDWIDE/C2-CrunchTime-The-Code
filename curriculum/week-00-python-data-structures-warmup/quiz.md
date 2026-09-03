# Week 0 — Self-Check

**20 questions. This is the skip gate.**

Take it **cold**, before reading anything in this week — closed book, no REPL, no cheat sheet. Twenty minutes.

- **18–20 correct** — skip Week 0. Go to [Week 1](../week-01-the-frame-method-and-thinking-aloud/README.md).
- **13–17** — read the lecture you missed questions in, do the matching drills, retake.
- **12 or below** — do the whole week. It is 8 hours and it will save you many more.


---

## Strings

**1.** What are the time and space costs of `s[2:8]` on a string of length `n`?

<details>
<summary>Answer</summary>

`O(b - a)` = `O(6)` here, but in general `O(k)` for a slice of length `k` — in **both** time and space. Slicing copies. The trap is slicing inside a loop, which adds a factor of `n`.

</details>

**2.** Why is this `O(n²)`, and what is the one-line fix?
```python
out = ""
for ch in s:
    out += ch
```

<details>
<summary>Answer</summary>

Each `+=` allocates a new string and copies the whole accumulated result, so iteration `i` copies `i` characters: `1 + 2 + ... + n = O(n²)`. Fix: collect into a list and `"".join(parts)` once — `O(n)`. (CPython's refcount-1 optimization sometimes hides this. Do not rely on it.)

</details>

**3.** What is the worst-case complexity of `"abc" in text`, in terms of `n = len(text)` and `m = 3`?

<details>
<summary>Answer</summary>

`O(n · m)` worst case. That is the contract and what you should say. CPython 3.10+ uses a two-way algorithm for longer needles giving `O(n + m)` in practice — mention that second, never first.

</details>

**4.** What does each of these return?
```python
"  a  b  ".split()
"  a  b  ".split(" ")
```

<details>
<summary>Answer</summary>

`['a', 'b']` and `['', '', 'a', '', 'b', '', '']`. No-argument `split()` collapses runs of whitespace and strips the ends; `split(" ")` splits on every single space.

</details>

**5.** Both lines give the same answer. Why prefer the first?
```python
s.startswith("http")
s[:4] == "http"
```

---

## Lists and tuples

<details>
<summary>Answer</summary>

`startswith` is `O(len(prefix))` and allocates nothing. The slice allocates a copy of the first four characters first, then compares.

</details>

**6.** `L.append(x)` is amortized `O(1)`, but a single append can be `O(n)`. Reconcile those in two sentences.

<details>
<summary>Answer</summary>

A single append is `O(n)` when the backing array is full and must be reallocated and copied. But capacity grows **geometrically**, so the resizes are geometrically spaced and their total copying cost across `n` appends sums to `O(n)` — `O(1)` each, amortized. Amortized is a claim about the total, not about any individual call.

</details>

**7.** Why is `L.pop()` `O(1)` but `L.pop(0)` `O(n)`?

<details>
<summary>Answer</summary>

A list is a contiguous array. `pop()` removes the last element and nothing moves. `pop(0)` removes the first and every remaining element must shift left one slot.

</details>

**8.** What does `[[0] * 3] * 2` build? Set `grid[0][0] = 9` and give the resulting value.

<details>
<summary>Answer</summary>

Two rows that are the **same list object**. After `grid[0][0] = 9`, `grid == [[9, 0, 0], [9, 0, 0]]`. `*` copies the pointer, not the list. Correct version: `[[0] * 3 for _ in range(2)]`.

</details>

**9.** You need a FIFO queue for BFS. Name the container. What is the total complexity if you use a plain list instead?

<details>
<summary>Answer</summary>

`collections.deque`, using `popleft()` — `O(1)`. With a plain list and `pop(0)`, each dequeue is `O(n)` and the traversal becomes `O(n²)` overall.

</details>

**10.** You call `sorted(L)` and then claim your solution is `O(1)` space. What is wrong?

<details>
<summary>Answer</summary>

`sorted()` returns a **new list** — `O(n)` space. Even in-place `L.sort()` uses `O(n)` auxiliary space in the worst case for Timsort's merge buffer. If a problem demands `O(1)` space, sorting is off the table.

</details>

**11.** Sort `records` by `score` descending, then `name` ascending — in a single call.

<details>
<summary>Answer</summary>

`records.sort(key=lambda r: (-r.score, r.name))`. Negation reverses one numeric component of a tuple key. (Two stable passes — secondary key first — also works and is the answer when the component is a string.)

</details>

**12.** `[x * x for x in nums]` and `(x * x for x in nums)` have the same time complexity. What differs, and by how much?

---

## Dicts and sets

<details>
<summary>Answer</summary>

Space. The list comprehension materializes all `n` results: `O(n)`. The generator expression yields one at a time: `O(1)`, provided the consumer does not store them.

</details>

**13.** State the complexity of `d[k]` completely — the way you would say it out loud in an interview.

<details>
<summary>Answer</summary>

"`O(1)` average. Worst case `O(n)` if every key collides, which requires adversarial input or a pathological hash — not a concern here." Both halves, in that order.

</details>

**14.** Since which Python version is dict insertion order a *language guarantee* rather than an implementation detail?

<details>
<summary>Answer</summary>

Python **3.7**. (CPython 3.6 had it as an implementation accident; 3.7 made it a language guarantee, so you may rely on it.)

</details>

**15.** What does this do, and why is it a bug?
```python
d.get(k, []).append(x)
```

<details>
<summary>Answer</summary>

`.get` returns a default without storing it, so `.append(x)` appends to a throwaway list and the dict is never modified. Use `d.setdefault(k, []).append(x)` or a `defaultdict(list)`.

</details>

**16.** `counts.most_common(k)` on a `Counter` with `n` total items — `O(n log k)` or `O(n log n)`? Why?

<details>
<summary>Answer</summary>

`O(n log k)`. It keeps a heap of size `k` rather than sorting all `n` — the win is real when `k << n`. With **no** argument it is `O(n log n)`, a full sort.

</details>

**17.** Why is `s & t` cheaper than `s | t`? Give both complexities.

<details>
<summary>Answer</summary>

Intersection iterates the **smaller** set and probes the larger, so it is `O(min(len(s), len(t)))`. Union must touch every element of both: `O(len(s) + len(t))`.

</details>

**18.** `hash((1, [2]))` raises `TypeError`. The tuple is immutable. Explain precisely.

<details>
<summary>Answer</summary>

Hashable means immutable **all the way down**. The tuple is immutable at the top level, but hashing it requires hashing each element, and the inner list is unhashable. That is also the precise reason a list can never be a dict key.

</details>

**19.** Rewrite this to be linear, and state the trade in one sentence.
```python
common = [x for x in a if x in b]
```

<details>
<summary>Answer</summary>

`b_set = set(b)` then `[x for x in a if x in b_set]`. "Membership on a list is `O(n)`, making the original `O(n·m)`; building the set costs `O(m)` time and `O(m)` space once, after which each test is `O(1)` average — so the whole thing is `O(n + m)` time for `O(m)` space." The space acknowledgement is the part that scores.

</details>

**20.** Distinguish auxiliary space from output space. Which do you report when asked "what's the space complexity?"

---
---

<details>
<summary>Answer</summary>

**Auxiliary** space is what your algorithm allocates beyond the input and the output. **Output** space is the size of the returned result. Report auxiliary by default — but say which one you mean, and state both when the output can dominate (returning all subsets is `O(2ⁿ)` output no matter how clever the algorithm).

---

</details>

## Scoring

| Score | Do this |
|---|---|
| 18–20 | Skip to [Week 1](../week-01-the-frame-method-and-thinking-aloud/README.md). Keep [the cheat sheet](CHEATSHEET.md) open anyway |
| 13–17 | Read the lectures covering your misses; do the matching drills; retake |
| ≤ 12 | Do the full week. Eight hours |

Question-to-lecture map: 1–5 → [Lecture 1](lecture-notes/01-strings-and-immutability.md) · 6–12 → [Lecture 2](lecture-notes/02-lists-tuples-and-the-dynamic-array.md) · 13–19 → [Lecture 3](lecture-notes/03-dicts-sets-and-the-hash-table.md) · 20 → [the cheat sheet](CHEATSHEET.md).
