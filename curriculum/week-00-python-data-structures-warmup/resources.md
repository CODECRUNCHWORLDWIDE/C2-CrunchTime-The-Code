# Week 0 — Resources

Every resource is **free** and **publicly accessible**. Week 0 leans almost entirely on primary sources, because for a cost model the primary source is the only one that stays true across versions.

## Required (about 90 minutes total)

- **TimeComplexity — the Python wiki's official cost table**: <https://wiki.python.org/moin/TimeComplexity> — the canonical reference for `list`, `deque`, `set`, and `dict`. Short. Read the whole thing. This is the source the cheat sheet is checked against.
- **Built-in Types — `str` methods**: <https://docs.python.org/3/library/stdtypes.html#string-methods> — do not read end to end. Skim the method list once so you know what exists, then look up `split`, `join`, `find`, `startswith` properly.
- **`collections` — `deque`, `defaultdict`, `Counter`**: <https://docs.python.org/3/library/collections.html> — read the `deque` and `Counter` sections in full. Both have complexity notes in the prose that most people never read.

## On why the costs are what they are

- **`listobject.c` — the growth rule**: <https://github.com/python/cpython/blob/main/Objects/listobject.c> — search the file for `list_resize`. The comment above it states the over-allocation pattern in one paragraph. Reading actual CPython source once is worth more than ten blog posts about it, and it is more approachable than people expect.
- **`dictobject.c` — the layout**: <https://github.com/python/cpython/blob/main/Objects/dictobject.c> — the header comment explains the split-table design and the load factor. Skim it; do not try to read the whole file.
- **PEP 468 and the 3.7 ordering guarantee**: <https://docs.python.org/3/whatsnew/3.7.html> — search for "dict". The one-line note that insertion order is now "an official part of the Python language spec" is the citation to use when someone tells you not to rely on it.

## On complexity itself

- **Big-O Cheat Sheet**: <https://www.bigocheatsheet.com/> — the standard poster. Useful for the graph at the top. Its data-structure table is language-agnostic and does **not** match CPython exactly; when the two disagree, the Python wiki wins.
- **Amortized analysis — Wikipedia**: <https://en.wikipedia.org/wiki/Amortized_analysis> — read the "Dynamic array" example. It is the exact argument behind `list.append`, worked out formally. Twenty minutes.
- **Timsort — Wikipedia**: <https://en.wikipedia.org/wiki/Timsort> — read the introduction and the "Minimum run size" section. Enough to justify "adaptive and stable" out loud.
- **`listsort.txt` — Tim Peters' own description**: <https://github.com/python/cpython/blob/main/Objects/listsort.txt> — the algorithm explained by the person who wrote it. Optional, excellent, and unusually readable for a design document.

## Practice platforms (optional this week)

Week 0 has no external problems on purpose. If you want extra reps on syntax before Week 1:

- **Exercism — Python track** (free, MIT-licensed exercises): <https://exercism.org/tracks/python> — the early exercises are exactly the right level for a warm-up, and the mentoring is free.
- **Python Morsels — free tier**: <https://www.pythonmorsels.com/> — short exercises focused on idiom rather than algorithms.

## Glossary

Keep this open. Every term here is used unqualified from Week 1 onward.

| Term | One-line definition |
|---|---|
| **Amortized** | The average cost per operation over a sequence, when individual operations vary. A claim about the total, not any single call |
| **Auxiliary space** | Memory your algorithm allocates beyond the input and the output |
| **Output space** | The size of the returned result; report it separately when it can dominate |
| **Contiguous** | Stored in one unbroken block, so element `i` is found by address arithmetic — the reason list indexing is `O(1)` |
| **Dynamic array** | An array with spare capacity that reallocates geometrically when full. Python's `list` |
| **Load factor** | Entries divided by slots in a hash table. CPython resizes to keep it under about 2/3 |
| **Collision** | Two keys landing in the same hash slot; resolved by probing |
| **Probing** | Walking a deterministic sequence of alternate slots after a collision |
| **Hashable** | Immutable all the way down, so `hash()` is stable. Required for dict keys and set members |
| **Interning** | Reusing one object for identical short strings, so equality can short-circuit to a pointer check |
| **Shallow copy** | Duplicates the container's pointers; the pointed-at objects stay shared |
| **Deep copy** | Duplicates the container and everything reachable from it |
| **Aliasing** | Two names referring to the same object, so mutating through one is visible through the other |
| **Stable sort** | Equal elements keep their original relative order. Timsort is stable; you may rely on it |
| **Adaptive sort** | Runs faster on partly-ordered input. Timsort is `O(n)` on sorted input |
| **Lazy / view** | Produces values on demand rather than materializing them. `.items()`, `enumerate`, `zip`, generator expressions |
| **Short-circuit** | Stops as soon as the answer is determined. `any`, `all`, `and`, `or` |
| **Two-way algorithm** | Crochemore–Perrin substring search; what CPython 3.10+ uses for long needles, giving `O(n + m)` |

## What you will be glad you read

Two things, both short:

1. **The Python wiki TimeComplexity page**, in full. Ten minutes, and it is the only table in this course you should trust over the cheat sheet if they ever disagree.
2. **The `list_resize` comment in `listobject.c`.** Two minutes. Seeing the actual growth rule in the actual source turns "amortized O(1)" from a phrase you repeat into a thing you understand.

---

*Broken link? Open an issue.*
