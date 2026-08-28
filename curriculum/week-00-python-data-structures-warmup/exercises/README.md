# Week 0 — Exercises

Six warm-up drills. Every one is **written for this course** — there is nothing to look up and no external problem number, on purpose. Week 0 measures whether you can reason about the cost of code you wrote. Pattern recognition starts in Week 1.

**How to work these.** For each drill:

1. Write the obvious solution first. Do not optimize yet.
2. Write down its time and space complexity **before** you run it.
3. Run the timing harness. If the measured growth contradicts your claim, your claim was wrong — find out why.
4. Rewrite it correctly, and state the improvement in the five-slot sentence.

No recording, no portfolio commit, no FRAME write-up this week. Those start in Week 1.

**Setup.** Everything runs on the standard library:

```python
import timeit
from collections import Counter, defaultdict, deque
```

---

## Exercise 0 — The measurement harness

Write this first; the other five drills use it.

```python
import timeit

def growth(fn, sizes=(1_000, 2_000, 4_000, 8_000)):
    """Print the runtime of fn(n) at each size and the ratio to the previous size.

    A ratio near 2 means linear. A ratio near 4 means quadratic.
    A ratio near 1 means the work did not depend on n at all.
    """
    prev = None
    for n in sizes:
        t = timeit.timeit(lambda: fn(n), number=1)
        ratio = f"{t / prev:.2f}x" if prev else "-"
        print(f"n={n:>6}  {t:.4f}s  {ratio}")
        prev = t
```

**Read the ratio column, not the seconds.** Absolute times depend on your machine and tell you nothing. Doubling `n` and seeing the time double is linear; seeing it quadruple is quadratic. This is the only tool you need to falsify a complexity claim, and you will use it all week.

**Self-check:** run `growth(lambda n: sum(range(n)))`. You should see ratios near 2.

---

## Exercise 1 — Falsify the string concatenation claim

**Target time:** 15 minutes.

Write two functions that each build a string of `n` characters:

- `build_concat(n)` — starts from `""` and uses `+=` in a loop.
- `build_join(n)` — appends to a list and calls `"".join(...)` once.

Before running anything, write down the complexity you expect for each.

Then run both under `growth()` at sizes `(10_000, 20_000, 40_000, 80_000)`.

**What you are checking.** You should see `build_join` at roughly 2x per doubling. `build_concat` may *also* look linear — that is CPython's refcount-1 optimization firing, and it is the point of the drill.

Now defeat the optimization by keeping a second reference alive:

```python
def build_concat_pinned(n):
    out = ""
    keep = []
    for i in range(n):
        out += "a"
        if i % 100 == 0:
            keep.append(out)      # a second reference — in-place resize can no longer apply
    return out
```

Run that one too. The ratios should move toward 4x.

**Deliverable.** Three ratio tables and two sentences: what complexity you claimed, and what you would say in an interview about `+=` in a loop given what you just measured.

---

## Exercise 2 — The front of the list

**Target time:** 15 minutes.

Implement the same FIFO queue twice — process `n` items in, `n` items out:

- `queue_list(n)` — a `list`, using `append` and `pop(0)`.
- `queue_deque(n)` — a `collections.deque`, using `append` and `popleft`.

Predict both complexities, then measure at `(2_000, 4_000, 8_000, 16_000)`.

**Then answer, in writing:**

1. Which is quadratic, and which specific line makes it so?
2. `deque` gives up something to get `O(1)` at both ends. What, and why does BFS not care?
3. A colleague says "just use `pop()` instead of `pop(0)`." What breaks?

---

## Exercise 3 — Membership, and the price of the set

**Target time:** 20 minutes.

Given two lists `a` and `b` of length `n`, return the elements of `a` that also appear in `b`, preserving `a`'s order and without duplicates in the output.

Write it twice:

- `common_list(a, b)` — using `x in b` directly.
- `common_set(a, b)` — building a set from `b` first.

Measure both. Then:

1. State each complexity in time **and** space.
2. At what rough size of `b` does building the set stop being worth it, if you only ever test **one** element? Reason it out; then measure to check.
3. Your output must have no duplicates. Adding that requirement changes the space claim — how, and by how much?

**The sentence to produce.** One sentence naming both costs and the trade, in the shape Lecture 3 gives you. This is the sentence you will say in a real interview more than any other.

---

## Exercise 4 — Grid initialization, and the aliasing bug

**Target time:** 10 minutes. Short, and it catches more people than it should.

```python
def make_grid_a(rows, cols):
    return [[0] * cols] * rows

def make_grid_b(rows, cols):
    return [[0] * cols for _ in range(rows)]
```

1. Run each on `(3, 4)`, set `grid[0][0] = 9`, and print the whole grid. Explain the difference in terms of what `*` copies.
2. Which one costs `O(rows · cols)` space, and which one costs less? What is the *actual* space of the buggy one?
3. `[0] * cols` is itself a `*` on a list. Why is that one safe?
4. Write a one-line assertion that would have caught the bug in a test.

---

## Exercise 5 — Frequency, four ways

**Target time:** 20 minutes.

Count character frequencies in a lowercase-ASCII string. Implement all four:

- `freq_dict(s)` — a plain dict with an `if k in d` check.
- `freq_get(s)` — a plain dict with `d.get(k, 0) + 1`.
- `freq_default(s)` — a `defaultdict(int)`.
- `freq_array(s)` — a 26-element list indexed by `ord(ch) - ord('a')`.

1. All four are `O(n)` time. State the **space** complexity of each, precisely. Two of them differ from the other two — say which and why.
2. Measure all four. They are the same asymptotically; the constant factors are not. Rank them and explain the ranking.
3. `freq_array` is `O(1)` space. Defend that claim out loud against an interviewer who says "but it's 26 slots, that's not constant."
4. When is `freq_array` the wrong choice?

---

## Exercise 6 — Fix the accidentally-quadratic function

**Target time:** 25 minutes. The capstone of the week.

This function is correct and slow. It takes a list of words and returns, for each word, how many *later* words are anagrams of it.

```python
def anagram_counts_slow(words):
    result = []
    for i in range(len(words)):
        count = 0
        for j in range(i + 1, len(words)):
            if sorted(words[i]) == sorted(words[j]):
                count += 1
        result.append(count)
    return result
```

1. State its exact complexity in terms of `n` (word count) and `L` (max word length). There are **three** nested costs here, not two — find all three.
2. Name every wasted operation. There is more than one kind of waste.
3. Rewrite it. Target `O(n · L log L)` time. State your new space cost and where it goes.
4. Measure both at `(500, 1_000, 2_000)` words. Confirm the ratios match your claims.
5. Write the full five-slot Examine sentence for your rewrite, including the alternative you rejected.

**Hint, if you need one after 10 minutes:** the outer loop asks the same question `n` times. What if you answered it once, for every word at once, before the loop?

---

## Done?

Take [the self-check](../quiz.md) cold. 18/20 or better and you are ready.

Then: [Week 1 — The FRAME Method](../../week-01-the-frame-method-and-thinking-aloud/README.md).
