# Week 0 — Mini-Project: Your Own Cost Table

**Time:** 1 hour. **Deliverable:** one file, `my_cost_table.md`, in a scratch folder.

---

## The idea

You have just read a cheat sheet full of complexity claims you took on trust. This project makes you **verify** them, and produces a version of the table in your own words that you will actually remember — because you measured it.

Nobody remembers a table they read. People remember a table they built.

---

## What to build

A markdown file with one row per operation, for **at least twelve** operations spanning all four containers (`str`, `list`, `dict`, `set`). For each row:

| Column | What goes in it |
|---|---|
| Operation | The exact expression, e.g. `L.pop(0)` |
| Claimed | The complexity from [the cheat sheet](../CHEATSHEET.md) |
| Measured | Your ratio column at four doubling sizes |
| Verdict | Confirmed / contradicted |
| Why | One sentence from the **memory model**, not from the table |

The "Why" column is the point of the exercise. `L.pop(0)` is not `O(n)` because a table says so. It is `O(n)` because a list is a contiguous array and removing the front element forces every remaining element to shift left one slot. Write the reason, not the fact.

---

## Required rows

At least these six, plus six of your own choosing:

1. `L.append(x)` — and show it is amortized, not worst-case, `O(1)`
2. `L.pop(0)` versus `deque.popleft()` — side by side
3. `x in L` versus `x in set(L)` — including the cost of building the set
4. `s += ch` in a loop versus `"".join(parts)`
5. `s[a:b]` — show that it is `O(k)` in space as well as time
6. `heapq.heapify(L)` — show it is `O(n)`, not `O(n log n)`

Row 6 is the interesting one. `heapify` looks like `n` insertions at `O(log n)` each. It is not. If your measurement says linear and your intuition said `n log n`, write down why the intuition fails — that is the most valuable sentence in the file.

---

## Method

Use the `growth()` harness from [Exercise 0](../exercises/README.md). Four doubling sizes, minimum.

**Read the ratio column, not the seconds.** Absolute times are machine-specific and meaningless. A ratio near 2 per doubling is linear; near 4 is quadratic; near 1 is constant; slightly above 2 is `n log n` and is genuinely hard to distinguish from linear at small `n` — say so honestly rather than over-claiming.

**Pick sizes large enough to see the trend.** At `n = 100` everything looks constant. Start where a single run takes at least 10 milliseconds.

---

## Self-check rubric

Grade your own file. It is done when all five are true:

- [ ] Twelve or more rows, spanning all four containers.
- [ ] Every "Why" cell explains from the **memory layout** (contiguous array / hash slots / immutable object), not by restating the complexity.
- [ ] At least one row where your prediction was **wrong**, with the reason you were wrong written out. If every prediction was right, you did not pick hard enough operations — add `heapify`, `most_common(k)`, and `set & set` with very different sizes.
- [ ] Amortized append is explained as a statement about the total, not about a single call.
- [ ] The file distinguishes auxiliary space from output space at least once.

---

## Stretch (optional)

Add a row for an operation whose complexity you could **not** confirm by measurement, and explain why measurement failed. Good candidates: dict worst-case `O(n)` (you cannot trigger it without adversarial keys), and CPython's `+=` refcount optimization (it appears and disappears depending on whether a second reference exists). Understanding *why* a claim resists measurement is worth as much as measuring one that does not.

---

## Up Next

[Week 1 — The FRAME Method & Thinking Aloud](../../week-01-the-frame-method-and-thinking-aloud/README.md). Bring the cost table; Week 2 grades complexity for real.
