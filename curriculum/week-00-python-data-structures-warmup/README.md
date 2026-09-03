# Week 0 — Python Data Structures Warm-Up

> *You cannot reason about the complexity of your algorithm if you do not know the complexity of the line you just wrote.* Week 0 fixes that, before we touch a single pattern.

This week is a **warm-up, not a prerequisite gate**. It exists because the most common way to lose a technical interview is not failing to find the algorithm — it is finding the right algorithm and then implementing it with an accidental `O(n²)` inside, or being unable to answer "why is that lookup O(1)?"

Week 0 covers the four built-ins you will use in every one of the next 19 weeks — **strings, lists, dicts, sets** (plus tuples, which exist to make the other three work) — at the level of *what it costs*, not *what it does*.

**You may skip this week.** Take the [self-check](quiz.md) cold. Score 18/20 or better and go straight to [Week 1](../week-01-the-frame-method-and-thinking-aloud/README.md). Score below that and this week is 8 hours that will save you thirty.

By the end of Week 0 you will:

- Know the time **and space** cost of every common operation on `str`, `list`, `tuple`, `dict`, `set` — from memory, not from a lookup.
- Be able to explain *why* each cost is what it is, from the underlying memory layout.
- Recognize the five hidden-cost traps (slicing, string concatenation, `list.pop(0)`, `x in list`, recursion stack) on sight.
- State a complexity out loud in the five-slot sentence this course grades on.
- Have the [cheat sheet](CHEATSHEET.md) internalized well enough that you stop needing it.

---

## Learning objectives

By the end of this week, you will be able to:

- **State** the time and space complexity of any built-in operation on `str`, `list`, `tuple`, `dict`, or `set`, and justify it from the data structure's memory layout.
- **Distinguish** average-case from worst-case cost for hash-backed operations, and say the distinction out loud the way an interviewer wants to hear it.
- **Distinguish** auxiliary space from output space, and name which one you are reporting.
- **Explain** why strings are immutable in Python and what that costs — including why `+=` in a loop is `O(n²)` and what to write instead.
- **Explain** amortized `O(1)` append from the geometric-growth argument, not as a memorized phrase.
- **Choose** between a list, a `deque`, a dict, a set, and a `Counter` for a stated access pattern, and defend the choice on cost.
- **Identify** what is hashable and why, and apply the tuple-key and `frozenset` idioms.
- **Detect** the aliasing traps: `[[0] * n] * m`, shallow copy, and mutable default arguments.
- **Rewrite** an accidentally-quadratic warm-up solution as a linear one, and quantify the improvement.

## Standards this week meets

| Bar | What this week is measured against |
| --- | --- |
| University | `CS 61B` — The built-in collections and what each one costs, which a second course assumes you already have. |
| Industry | Find the operation inside working code that costs more than it looks — a slice, a membership test against a list, a concatenation in a loop — and justify the replacement in review with the growth you measured rather than the complexity you remember. |
| Beyond the bar | The week ships a harness that counts the work itself — elements copied, elements shifted, comparisons, hash probes — instead of timing it, so the cost table you publish reproduces exactly on somebody else's laptop under load — `mini-project/growth_lab.py` |

---

## Prerequisites

- **Python 3.11+ installed**, and you can run a script.
- You have written a `for` loop, an `if`, and a function before. That is genuinely all.
- If you cannot do that, do **C1 Weeks 1–4** first. Week 0 teaches the *cost model* of Python's built-ins; it does not teach Python syntax from zero.

This week needs no Git, no portfolio repo, and no recording. Those start in Week 1.

---

## Topics covered

**Strings**
- Immutability, and what it costs
- Indexing, slicing, and why slicing is the most-missed `O(n)` in the language
- `split`, `join`, and the join idiom that kills accidental `O(n²)`
- Substring search: the `O(n · m)` contract and the CPython reality
- `ord` / `chr`, case operations, `startswith` vs slicing
- Building strings correctly

**Lists and tuples**
- The dynamic array: contiguous storage, spare capacity, and everything that follows
- Amortized `O(1)` append, derived from geometric growth
- Why the front of a list is expensive and `collections.deque` is not
- Slicing copies; shallow copy vs deep copy
- `sort` and `sorted`: Timsort, stability, the `key` function, tuple keys
- Comprehensions and generator expressions — and the space difference between them
- Tuples, hashability, and unpacking
- The aliasing traps

**Dicts and sets**
- The hash table: why `O(1)` average and `O(n)` worst
- Guaranteed insertion order since 3.7 and when to rely on it
- `get`, `setdefault`, `defaultdict`, `Counter` — and which to reach for
- Views (`.keys()`, `.values()`, `.items()`) are lazy
- Set algebra and its per-operation costs
- `frozenset`, tuple keys, and what "immutable all the way down" means
- The `list` → `set` swap that turns `O(n²)` into `O(n)`, and the space you pay for it

**Complexity, throughout**
- Best / average / worst
- Auxiliary vs output space
- The recursion stack as space
- The five-slot complexity sentence

---

## Weekly schedule (intensive · 8h)

Week 0 is deliberately light. It is a warm-up, not a phase.

| Day | Focus | Lectures | Exercises | Quiz | Mini-Project | Daily Total |
|-----|-------|---------:|----------:|-----:|-------------:|------------:|
| Day 1 | Strings; the cost model | 1h | 1h | 0h | 0h | 2h |
| Day 2 | Lists, tuples, deque | 1h | 1h | 0h | 0h | 2h |
| Day 3 | Dicts, sets, Counter | 1h | 1h | 0h | 0h | 2h |
| Day 4 | Cheat sheet drill; self-check; mini-project | 0h | 0.5h | 0.5h | 1h | 2h |
| | | **3h** | **3.5h** | **0.5h** | **1h** | **8h** |

Mastery pathway: same 8 hours, spread across two weeks at 4h/week.

---

## This week's files

| File | What it is |
|---|---|
| [CHEATSHEET.md](CHEATSHEET.md) | **The deliverable of this week.** Every complexity, one page. Print it |
| [lecture-notes/01-strings-and-immutability.md](lecture-notes/01-strings-and-immutability.md) | Strings and the cost of immutability |
| [lecture-notes/02-lists-tuples-and-the-dynamic-array.md](lecture-notes/02-lists-tuples-and-the-dynamic-array.md) | Lists, tuples, deque, sorting |
| [lecture-notes/03-dicts-sets-and-the-hash-table.md](lecture-notes/03-dicts-sets-and-the-hash-table.md) | Dicts, sets, Counter, hashability |
| [exercises/](exercises/README.md) | Six warm-up drills — every one is written for this course |
| [quiz.md](quiz.md) | The 20-question self-check. Take it cold to decide whether to skip |
| [homework.md](homework/README.md) | Complexity-annotation practice |
| [mini-project/](mini-project/README.md) | Build and benchmark your own cost table |
| [resources.md](resources.md) | Free reading, all of it primary sources |

---

## A note on the problems in this week

Every drill in Week 0 is **written for this course**. There are no external problem numbers here and nothing to look up, on purpose — the point is to measure the cost of code you wrote, not to recognize a known problem. Pattern recognition starts in Week 1.

---

## Self-check before you move on

You are ready for Week 1 when you can answer all of these without hesitating:

1. Why is `s += ch` in a loop `O(n²)`, and what do you write instead?
2. Why is `L.append(x)` amortized `O(1)` when a resize is `O(n)`?
3. Why is `L.pop(0)` `O(n)` but `d.popleft()` `O(1)`?
4. What is the worst case of `d[k]`, when does it happen, and should you worry?
5. What does `[[0] * 3] * 2` build, and why is it a bug?
6. Why can a tuple be a dict key but a list cannot? Give the exact rule.
7. `heapq.heapify(L)` — `O(n)` or `O(n log n)`? Why?
8. You call `sorted(L)` and then claim `O(1)` space. What did you get wrong?
9. What is the difference between auxiliary space and output space, and which do you report?
10. Say the five-slot complexity sentence for "find a duplicate using a set."

---

## Up Next

[Week 1 — The FRAME Method & Thinking Aloud](../week-01-the-frame-method-and-thinking-aloud/README.md) — the five-step method you will use on every problem for the rest of the course.
