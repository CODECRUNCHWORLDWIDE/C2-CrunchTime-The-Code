# Lecture 2 — Lists, Tuples and the Dynamic Array

**Reading time:** ~40 minutes. REPL open.

---

## 1. One picture, and everything follows from it

A Python list is a **contiguous block of pointers, with spare capacity at the end.**

```
   capacity = 8, length = 5
   +----+----+----+----+----+----+----+----+
   | p0 | p1 | p2 | p3 | p4 |    |    |    |
   +----+----+----+----+----+----+----+----+
     ^                   ^     ^
     index 0             len-1  spare room for appends
```

Three consequences, and you can derive the whole cost table from them:

1. **Contiguous** → the address of element `i` is a multiply-and-add. Indexing is `O(1)`.
2. **Spare capacity at the end** → appending is usually just a pointer write. `O(1)`, amortized.
3. **Nothing spare at the front** → inserting or removing at index 0 must shift every other element. `O(n)`.

Note that the block holds **pointers**, not the objects themselves. That is why a list can hold mixed types, and why `list(L)` is a *shallow* copy — it duplicates the pointers, not the things they point at.

---

## 2. Amortized `O(1)` append, derived properly

When you append to a full list, CPython allocates a bigger block, copies the pointers over, and frees the old one. That single append is `O(n)`.

So why do we call it `O(1)`?

Because the new capacity is chosen **proportionally** to the current size (CPython grows by roughly 12.5% plus a small constant). Growing from empty to `n` elements triggers resizes at geometrically-spaced sizes, and the total copying work across all of them is a geometric series that sums to `O(n)`. Spread over `n` appends, that is `O(1)` each.

The distinction that matters: **amortized `O(1)` is a guarantee about the total, not about any individual call.** A real-time system that cannot tolerate one slow append does care. An interview answer does not, but the interviewer wants to hear that you know the difference.

**The sentence:**

> Append is amortized O(1). An individual append can be O(n) when the array resizes, but because capacity grows geometrically, n appends cost O(n) in total.

**Contrast with `insert(0, x)`.** No amount of spare capacity at the end helps you at the front. Every element must shift right by one. That is `O(n)` per call, `O(n²)` for `n` calls, and there is no amortization argument that rescues it.

---

## 3. The cost table, and why each row is what it is

| Operation | Cost | Because |
|---|---|---|
| `L[i]`, `L[i] = x` | `O(1)` | Contiguous — address arithmetic |
| `len(L)` | `O(1)` | Stored |
| `L.append(x)` | amortized `O(1)` | Spare capacity at the end |
| `L.pop()` | `O(1)` | Removes from the end, nothing shifts |
| `L.pop(0)` | `O(n)` | Shifts all `n-1` remaining elements left |
| `L.insert(i, x)` | `O(n - i)` | Shifts everything from `i` rightward |
| `del L[i]` | `O(n - i)` | Same shift, other direction |
| `L.remove(x)` | `O(n)` | Linear search, then the shift |
| `x in L` | `O(n)` | **Linear scan.** No index exists |
| `L.index(x)` | `O(n)` | Same scan |
| `L[a:b]` | `O(b - a)` time and space | Allocates and copies |
| `L1 + L2` | `O(n + m)` | New list, both copied |
| `L.extend(other)` | amortized `O(k)` | `k` appends |
| `L.reverse()` | `O(n)` time, `O(1)` space | In place, swap from both ends |
| `L.sort()` | `O(n log n)` time, `O(n)` space | Timsort |
| `min/max/sum(L)` | `O(n)` | One pass |
| `list(L)`, `L.copy()` | `O(n)` | Shallow copy |

**The row that costs people rounds is `x in L`.** It reads like a set membership test and costs like a loop. Inside another loop it silently produces `O(n²)`:

```python
# O(n * m) — the `in` is a scan
dupes = [x for x in a if x in b]

# O(n + m) — build once, then O(1) lookups
b_set = set(b)
dupes = [x for x in a if x in b_set]
```

You pay `O(m)` time and `O(m)` space to build `b_set`. Say that trade out loud; it is the whole point of the rewrite.

---

## 4. When a list is the wrong container: `collections.deque`

If you need cheap operations at **both** ends, a list cannot give it to you. A `deque` can.

```python
from collections import deque

q = deque([1, 2, 3])
q.append(4)        # O(1) — right
q.appendleft(0)    # O(1) — left, genuinely
q.pop()            # O(1)
q.popleft()        # O(1)
q[1]               # O(n) for a middle index — this is the trade
```

A `deque` is a doubly-linked list of fixed-size blocks. That buys `O(1)` at both ends and costs `O(1)` random access.

**This is not academic.** BFS (Week 6) processes a queue front-to-back. Written with a list:

```python
queue = [start]
while queue:
    node = queue.pop(0)      # O(n) every iteration -> O(n^2) overall
```

Written with a deque:

```python
queue = deque([start])
while queue:
    node = queue.popleft()   # O(1) -> O(n) overall
```

Same algorithm. One is quadratic. Interviewers notice this specific line.

---

## 5. Slicing copies (again), and shallow vs deep

```python
L[a:b]     # O(b - a) time and space — a new list
L[:]       # O(n) — full shallow copy
L[::-1]    # O(n) — reversed copy
L[::2]     # O(n/2) — every other element
```

The same trap as strings: slicing inside a loop adds a factor of `n`. Pass indices.

**Shallow copy** duplicates the outer list's pointers. The inner objects are shared:

```python
grid = [[1, 2], [3, 4]]
copy = grid[:]          # shallow
copy[0][0] = 99         # grid is now [[99, 2], [3, 4]] — SAME inner list
copy[0] = [7, 8]        # grid is unchanged — this replaces the pointer
```

For an independent nested structure you need a comprehension per level (`[row[:] for row in grid]`, `O(n·m)`) or `copy.deepcopy` (also `O(n·m)`, plus cycle tracking).

---

## 6. The aliasing traps

Three bugs. Each has cost someone an interview.

**Trap 1 — `*` on a list of mutables.**

```python
grid = [[0] * 3] * 2
grid[0][0] = 9
# grid == [[9, 0, 0], [9, 0, 0]]   -- both rows are the SAME list
```

`[[0] * 3]` builds one row. `* 2` copies the **pointer** to that row twice. The fix:

```python
grid = [[0] * 3 for _ in range(2)]   # two independent rows
```

`[0] * 3` on its own is fine — ints are immutable, so sharing them is harmless. The rule is: **`* n` is safe for immutables, a bug for mutables.**

**Trap 2 — mutable default argument.**

```python
def add(x, acc=[]):     # the list is created ONCE, at definition time
    acc.append(x)
    return acc

add(1)   # [1]
add(2)   # [1, 2]   -- not [2]
```

Fix: `def add(x, acc=None): acc = [] if acc is None else acc`.

**Trap 3 — mutating while iterating.**

```python
for x in L:
    if bad(x):
        L.remove(x)     # skips elements; the index moves under you
```

Build a new list instead: `L = [x for x in L if not bad(x)]`, `O(n)`.

---

## 7. Sorting

```python
L.sort()                    # in place, returns None, O(n log n) time, O(n) space
sorted(iterable)            # returns a new list, same costs
```

CPython uses **Timsort**, which has two properties you can rely on and should mention:

**It is stable.** Equal elements keep their original relative order. That is a language guarantee, and it lets you sort by multiple keys without a comparator — sort by the secondary key first, then the primary:

```python
records.sort(key=lambda r: r.name)     # secondary
records.sort(key=lambda r: r.score)    # primary; stability preserves name order within a score
```

Or do it in one pass with a tuple key, which is usually clearer:

```python
records.sort(key=lambda r: (-r.score, r.name))   # score descending, then name ascending
```

Negating a number is how you reverse *one* component of a tuple key. It only works for numbers; for a string component you must sort twice.

**It is adaptive.** Already-sorted or reverse-sorted input runs in `O(n)`. If a problem says "nearly sorted," that is a sentence worth saying.

**The `key` function runs once per element**, not once per comparison — `n` calls, not `n log n`. This is why `key=` beats `functools.cmp_to_key` on cost as well as readability.

**Do not claim `O(1)` space after sorting.** `sorted()` allocates a new list — `O(n)`. Even `L.sort()`, which is in place, uses `O(n)` auxiliary space in the worst case for Timsort's merge buffer. If a problem demands `O(1)` space, sorting is usually off the table, and saying so is the correct Research-constraints move.

---

## 8. Comprehensions and generators

```python
squares = [x * x for x in nums]       # list comp: O(n) time, O(n) space
squares = (x * x for x in nums)       # generator: O(n) time when consumed, O(1) space
total   = sum(x * x for x in nums)    # O(n) time, O(1) space — nothing materializes
```

The time is the same. The **space** is not. A list comprehension builds the whole list; a generator expression yields one item at a time.

Use a generator when you are feeding a consumer (`sum`, `max`, `any`, `all`, `join`) and never need the list itself. Use a list comprehension when you need to index it, re-iterate it, or take its length.

```python
any(x < 0 for x in nums)      # O(n) worst, O(1) space, short-circuits on the first True
all(x > 0 for x in nums)      # same, short-circuits on the first False
```

`any` and `all` short-circuit. That makes them the right way to express "does any element satisfy…" — best case `O(1)`, worst case `O(n)`.

Dict and set comprehensions exist too, and cost the same as building the container:

```python
{w: len(w) for w in words}         # O(total chars)
{w for w in words if len(w) > 3}   # O(n)
```

---

## 9. Tuples, and why they matter

A tuple is an immutable sequence. Costs match a list for reads and are irrelevant for writes, because there are none.

| Operation | Cost |
|---|---|
| `t[i]`, `len(t)` | `O(1)` |
| `t[a:b]` | `O(b - a)` |
| `t1 + t2` | `O(n + m)` — new tuple |
| `x in t` | `O(n)` |
| `hash(t)` | `O(n)`, and only if every element is hashable |

The reason tuples earn a section in an interview-prep course is **hashability**. Because a tuple cannot change, its hash cannot change, so it can be a dict key or a set member. A list can never be either.

This is what makes the two most common idioms in the course legal:

```python
visited = set()
visited.add((row, col))                # grid coordinates as a set member

groups = defaultdict(list)
groups[tuple(sorted(word))].append(word)   # anagram key
```

**Unpacking** is `O(k)` in the number of names and reads better than indexing:

```python
lo, hi = 0, len(L) - 1
a, b = b, a                            # swap, no temp variable
for i, ch in enumerate(s): ...         # index and value together
for name, score in pairs: ...
first, *rest = L                       # O(n) — `rest` is a new list
```

`enumerate` and `zip` are both `O(1)` space — they are lazy iterators, not materialized lists.

---

## 10. Choosing a container

| You need | Use | Why |
|---|---|---|
| Indexed access, append at the end | `list` | `O(1)` both |
| Cheap at both ends (a queue) | `deque` | `O(1)` popleft; a list is `O(n)` |
| Membership tests | `set` | `O(1)` vs `O(n)` |
| Key → value | `dict` | `O(1)` average |
| A hashable sequence (dict key) | `tuple` | Lists are not hashable |
| Repeated min/max extraction | `heapq` on a list | `O(log n)` per operation |
| Counting occurrences | `Counter` | `O(n)` construction, does it for you |

The Research constraints step of FRAME is partly this table. "I need to test membership `n` times, so I will pay `O(n)` once to build a set rather than `O(n)` per test" is exactly the sentence that separates a strong candidate from a passing one.

---

## 11. Check yourself

**1.** Derive amortized `O(1)` append from geometric growth. Say it in two sentences.

<details>
<summary>Answer</summary>

A single append is `O(n)` when the backing array is full and has to be reallocated and copied. But capacity grows **geometrically**, so the resizes are geometrically spaced and their total copying cost across `n` appends sums to `O(n)` — `O(1)` each, amortized.

</details>

**2.** Why is `L.pop()` `O(1)` but `L.pop(0)` `O(n)`?

<details>
<summary>Answer</summary>

A list is a contiguous array. `pop()` removes the last element and nothing moves. `pop(0)` removes the first, and every remaining element shifts left one slot.

</details>

**3.** What does `[[0] * 3] * 2` build? Why? What do you write instead?

<details>
<summary>Answer</summary>

Two rows that are the **same list object**. `*` copies the pointer, not the list, so after `grid[0][0] = 9` the value is `[[9, 0, 0], [9, 0, 0]]`. Write `[[0] * 3 for _ in range(2)]`, which evaluates the inner list once per row.

</details>

**4.** `L[:]` on a list of lists — what is shared, what is not?

<details>
<summary>Answer</summary>

The outer list is new; the inner lists are the **same objects**. Appending to the copy leaves the original alone, but mutating `copy[0]` mutates `original[0]` too — a slice is a shallow copy. `copy.deepcopy` is what makes the whole structure independent, and it costs a full traversal.

</details>

**5.** You need a FIFO queue. Which container, and what happens if you pick the other one?

<details>
<summary>Answer</summary>

`collections.deque`, dequeuing with `popleft()` — `O(1)`. With a plain list and `pop(0)`, each dequeue shifts every remaining element, so each is `O(n)` and a full traversal becomes `O(n²)`.

</details>

**6.** Sort by score descending, then name ascending, in one call. Write it.

<details>
<summary>Answer</summary>

`records.sort(key=lambda r: (-r.score, r.name))`. Negating reverses one numeric component of a tuple key while the rest stay ascending. (Two stable passes — secondary key first — also works, and is the answer when the descending component is a string, which cannot be negated.)

</details>

**7.** You call `sorted(L)` and claim `O(1)` space. What is wrong?

<details>
<summary>Answer</summary>

`sorted()` returns a **new list**, so it is `O(n)` space by definition. Even in-place `L.sort()` uses `O(n)` auxiliary space in the worst case for Timsort's merge buffer. If a problem demands `O(1)` space, sorting is off the table.

</details>

**8.** `[x * x for x in nums]` vs `(x * x for x in nums)` — same time, different what?

<details>
<summary>Answer</summary>

Space. The list comprehension materializes all `n` results at once: `O(n)`. The generator expression yields them one at a time: `O(1)`, provided the consumer does not store them.

</details>

**9.** Why can `(row, col)` be a set member but `[row, col]` cannot?

<details>
<summary>Answer</summary>

Hashable means immutable **all the way down**. A tuple is immutable at the top level, and hashing it hashes each element in turn — which works for `(row, col)` and fails on a list, because a list is unhashable. It is the same reason a list can never be a dict key.

</details>

**10.** `L.sort()` on an already-sorted list of `n` elements. What does Timsort cost?

<details>
<summary>Answer</summary>

`O(n)`. Timsort finds the existing ascending run in its first pass and has nothing left to merge. Best case on already-sorted or reverse-sorted input is linear; the `O(n log n)` bound is the worst case, not the cost of every call.

</details>

---

## Up Next

[Lecture 3 — Dicts, Sets and the Hash Table](03-dicts-sets-and-the-hash-table.md) — where `O(1)` is an average, not a promise.
