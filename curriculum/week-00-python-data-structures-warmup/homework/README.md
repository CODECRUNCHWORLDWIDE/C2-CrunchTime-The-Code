# Week 0 — Homework

Two hours. No portfolio commit required — Week 0 is a warm-up. Keep the work in a scratch folder; you will want to reread it in Week 2 when complexity becomes graded.

---

## Part 1 — Annotate your own code (45 min)

Take any 30–60 line Python program you have already written. Anything: a school assignment, a script, a toy project. It must be code **you** wrote and have not thought about in complexity terms.

Go through it line by line and add a comment to every line that is **not** `O(../1)`:

```python
words = text.split()                    # O(../n) time, O(../n) space
seen = set()                            # O(../1)
for w in words:                         # O(../n) iterations
    key = "".join(../sorted(w))            # O(L log L) time, O(../L) space, per word
    if key in seen:                     # O(../1) average
        ...
```

Then write, at the top of the file, the total complexity of the whole program in the five-slot sentence.

**What you are looking for.** Almost everyone finds at least one line they assumed was free and is not. Slicing and `x in list` are the usual suspects. Write down what you found.

---

## Part 2 — Predict, then measure (45 min)

Pick **four** of the operations below. For each: write your predicted complexity down *first*, then measure it with the `growth()` harness from [Exercise 0](../exercises/README.md), then reconcile.

| Operation |
|---|
| `L.insert(0, x)` repeated `n` times |
| `d[k] = v` repeated `n` times on a fresh dict |
| `s in big_string` where `s` does not occur |
| `sorted(../L)` on already-sorted input vs on shuffled input |
| `set(../a) & set(../b)` where `len(../a)` is 10 and `len(../b)` is 100,000 |
| `L.remove(../x)` repeated `n` times |
| `"".join(../parts)` vs `+=` in a loop |
| `Counter(../s).most_common(../1)` vs `Counter(../s).most_common()` |

For each, produce three lines:

1. **Predicted:** what you claimed and why, from the memory model.
2. **Measured:** the ratio column.
3. **Reconciled:** they agree, or here is why they do not.

The third line is the one that teaches. If a prediction was wrong, find the reason before moving on — a wrong prediction you did not explain will be wrong again in Week 5.

---

## Part 3 — The container-choice memo (30 min)

For each scenario, name the container, state the cost of the operation that matters, and name the container you rejected and why. Two sentences each, no code.

1. You will look up user records by ID, several million times.
2. You need to process items strictly in arrival order, adding at one end and removing at the other.
3. You need to remember which grid cells you have already visited.
4. You need the three largest values from a stream of ten million numbers, and you cannot hold them all in memory.
5. You need to group words by which letters they contain, ignoring order and repetition.
6. You need to know how many times each word appears, then report the top ten.
7. You need a set of sets — the outer one deduplicating the inner ones.

Answers vary; the *justification* is the graded part. Every answer must name a cost.

---

## Part 4 — Reflection (10 min)

Three sentences:

1. Which complexity in this week surprised you most, and what did you believe before?
2. Which of the five hidden-cost traps have you personally shipped in code?
3. What will you check for in your own code from now on that you did not check for last week?

---

## Up Next

[The mini-project](../mini-project/README.md) — build your own measured cost table, then [Week 1](../../week-01-the-frame-method-and-thinking-aloud/README.md).
