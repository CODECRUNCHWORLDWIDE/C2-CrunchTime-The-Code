# Week 2 — Complexity Quiz

Ten short prompts. **Do not solve them.** For each, state the *time complexity* (and *space*, where asked). Lectures closed. Time yourself — 60 seconds per question is the target.

Answer key at the bottom.

---

**Q1.** What is the time complexity of the following?

```python
def f(arr):
    for x in arr:
        for y in arr:
            print(x, y)
```

**Q2.** What is the time complexity of the following?

```python
def f(arr):
    arr.sort()
    for x in arr:
        print(x)
```

**Q3.** What is the time complexity (average) of the following?

```python
def f(nums, target):
    seen = set()
    for x in nums:
        if target - x in seen:
            return True
        seen.add(x)
    return False
```

State both **time** and **space**.

**Q4.** Given a constraint of `n ≤ 10⁶`, which of these complexity classes will finish within a typical interview's "time limit" of ~1 second on modern hardware?

A. O(n²)   B. O(n log n)   C. O(n)   D. O(n²) with a constant factor of 1/100

**Q5.** What is the time complexity of the following?

```python
def f(arr):
    n = len(arr)
    i = 1
    while i < n:
        i *= 2
```

**Q6.** True or false: `list.append(x)` is **always** O(1).

**Q7.** What is the worst-case time complexity of looking up a key in a Python `dict`?

**Q8.** What is the time complexity of the following?

```python
def f(arr):
    n = len(arr)
    for i in range(n):
        for j in range(i, n):
            for k in range(j, n):
                print(arr[i], arr[j], arr[k])
```

**Q9.** You have an O(n²) algorithm that uses O(1) space, and an O(n) algorithm that uses O(n) space. Which do you choose for `n = 10⁹`, and why?

**Q10.** What is the time complexity of `set(nums)` for a list of length `n`?

---

## Answer key

<details>
<summary>Click after attempting all ten</summary>

1. **O(n²).** Both loops are over `arr`; n × n iterations. Body is O(1) (a `print`). Total O(n²).

2. **O(n log n).** The sort dominates the linear scan: `O(n log n) + O(n) = O(n log n)`. Take the max of the terms.

3. **O(n) average time, O(n) space.** Single pass through `nums`; each iteration does one O(1) average set lookup and one O(1) average insert. Worst-case O(n²) in pathological hash collisions, but with Python's randomized hash we say O(n) average.

4. **B and C.** O(n) and O(n log n) both finish in well under a second at n = 10⁶ (one million and ~20 million ops respectively). O(n²) is 10¹² ops — hours. Even with a 1/100 constant factor, O(n²) at n = 10⁶ is 10¹⁰ ops — still too slow.

5. **O(log n).** `i` doubles each iteration; exits when `i ≥ n`; that's `log₂ n` iterations.

6. **False.** It is **O(1) amortized**. Individual appends are O(n) when the underlying buffer resizes. Over a long sequence of appends, total work is O(n), so amortized O(1) per call. In an interview answer, "O(1) amortized" is the precise answer.

7. **O(n) worst case.** Every key collides into the same probe chain. Practically unreachable with Python's randomized hash seed on normal inputs, but it's the correct *worst-case* answer. **Average is O(1).** State both in interviews.

8. **O(n³).** Three nested loops; even though their bounds shrink (`i, j, k` are non-decreasing), the total iteration count is `Σ_{i,j,k with i≤j≤k} 1 = C(n+2, 3) ≈ n³/6`. Constant factor 1/6 drops; O(n³).

9. **Depends on memory and time constraints.** Naive answer: at n = 10⁹, **O(n²) is 10¹⁸ ops — completely unfeasible**, so O(n) is the only choice for time. But: O(n) space at n = 10⁹ might be 8 GB or more depending on element size — also potentially unfeasible. The real engineering answer: "neither fits on a single machine; we need an external-memory algorithm or distribution." In an interview, naming that tension wins the engineering-judgment point.

10. **O(n).** Constructing a set hashes each of the n elements and inserts it — n × O(1) average = O(n). (Worst case O(n²) in pathological collisions, but for normal inputs O(n) is right.)

</details>

---

## How to score

| Score | Meaning |
|------:|---------|
| 9–10 | Your complexity intuition is interview-ready. Move on. |
| 7–8 | Good — re-read [Lecture 1](./02-lecture-notes/01-mental-models-for-big-O.md) for the cases you missed. |
| 5–6 | Redo Drills 1, 3, and 5 with the *Evaluate* discipline before Week 3. |
| <5 | Complexity is not yet automatic. Don't move to Week 3 yet — re-read Lecture 1 and Lecture 3, do all five drills again with a stricter Evaluate section. |

This quiz is about **fluency**, not difficulty. Every question is something you should be able to answer in under a minute once the patterns are in muscle memory.

When done, the [homework](./06-homework.md) is next.
