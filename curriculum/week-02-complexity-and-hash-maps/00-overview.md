# Week 2 — Complexity & Hash Maps

```
┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐
│ U │  │ M │  │ P │  │ I │  │ R │  │ E │
└───┘  └───┘  └───┘  └───┘  └───┘  └───┘
```

> *Last week we taught you to talk while you code. This week we teach you to talk about cost while you code.* By Sunday you can state the time and space complexity of any solution you write — out loud, in the same sentence, with confidence — and you have a second pattern in your library.

Welcome to Week 2 of **C2 · CrunchTime — The Code**. The week is built around two ideas you'll use in every interview from now on:

1. **Complexity is a sentence you say out loud, not an afterthought.** The UMPIRE *Evaluate* step has a standard shape. We'll drill it until it's reflex.
2. **The hash map is the answer when sorted-array two-pointer isn't.** It is the second pattern of the course and the most commonly used data structure in modern interview problems.

By Sunday of Week 2 you will:

- State **time and space complexity for any solution** in a single, standard sentence: *"Each iteration is O(1) average on the hash map; n iterations total; therefore O(n) time, O(n) space."*
- Reach for a **hash map** instinctively when a problem says "unsorted," "frequency," "count," "first/last seen," or "complement."
- Have re-done **all five Week 1 drills** with explicit complexity sections — the mini-project.
- Have solved **five new hash-map drills**, two stretch challenges, the quiz, and the homework, all UMPIRE-narrated.
- Be able to defend **two-pointer over hash map** (or vice versa) in 20 seconds when asked.

---

## Learning objectives

By the end of this week, you will be able to:

- **Name** the six common complexity classes — O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ) — and *describe what each feels like* for n = 10, 100, 1000, and 10⁶.
- **Distinguish** best-case, average-case, and worst-case complexity, and know when each one matters in an interview answer.
- **Reason about space complexity** as a peer to time complexity, never an afterthought.
- **Explain amortized analysis** at the level of `list.append` and `dict[key]` lookups — the two cases you will be asked about most.
- **Match** a problem to the hash-map pattern using the canonical signals: unsorted input, frequency / counting, complement lookup, "have I seen this before?"
- **Justify** a hash-map choice over two-pointer (and vice versa) on the time / space tradeoff axis.
- **Write** a UMPIRE *Evaluate* section that another engineer would read and learn from — not a one-liner, a structured tradeoff.
- **Re-do** your five Week 1 write-ups with the new Evaluate discipline; the upgrade is visible.

---

## Prerequisites

- **Week 1 complete.** You can run UMPIRE on a two-pointer problem without notes. If you can't, repeat Week 1 — Week 2 *requires* that fluency.
- **Comfortable with Python `dict` and `set`.** Membership tests, iteration, `dict.get(k, default)`, `collections.Counter`, `collections.defaultdict`. We use them daily this week.
- **Portfolio repo exists** with Week 1 contents committed (mini-project from W1). You will be editing those files.
- **45 minutes of out-loud time per drill.** Same as Week 1 — vocalization is not optional in this course.

---

## Topics covered

- The six complexity classes — and the n-versus-runtime table you carry in your head
- Time complexity vs space complexity — both deserve a sentence
- Best case, average case, worst case — when to mention which
- Amortized analysis — the `list.append` story, the `dict` story
- The "what does adding a nested loop do" calibration drill
- The hash map as a *pattern*, not just a data structure
- Counting / frequency tables — the anagram family
- Two-sum (unsorted) — the canonical hash-map problem
- Caching past values during one pass — "have I seen this before?"
- Stating complexity out loud — the standard UMPIRE *Evaluate* sentence
- When to defend a hash-map choice over two-pointer (and vice versa)

---

## Weekly schedule (intensive · 36h)

| Day | Focus | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project | Self-Study | Daily Total |
|-----|-------|---------:|----------:|-----------:|----------:|---------:|-------------:|-----------:|------------:|
| Monday | Complexity mental models; drills 1-2 | 2h | 1.5h | 0h | 0.5h | 1h | 0h | 0.5h | 5.5h |
| Tuesday | Hash-map pattern; drills 3-4 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Wednesday | Stating complexity out loud; drill 5 | 2h | 2h | 1h | 0.5h | 1h | 0h | 0h | 6.5h |
| Thursday | Challenges + W1 rewrite begins | 0h | 1.5h | 1h | 0.5h | 1h | 2h | 0.5h | 6.5h |
| Friday | Stretch + W1 rewrite continues | 0h | 1h | 1h | 0.5h | 1h | 2h | 0.5h | 6h |
| Saturday | Mini-project deep work | 0h | 0h | 1h | 0h | 1h | 3h | 0h | 5h |
| Sunday | Pattern-recognition quiz + reflection | 0h | 0h | 0h | 0.5h | 0h | 0h | 0h | 0.5h |
| **Total** | | **6h** | **8h** | **4h** | **3h** | **6h** | **7h** | **2h** | **36h** |

**Mastery (10h/wk):** spread the same content over three calendar weeks. See the [mastery study plan](../study-plans/mastery-1-year.md) for Week 2's block.

---

## How to navigate this week

| File | What's inside |
|------|---------------|
| [README.md](./00-overview.md) | This overview |
| [resources.md](./01-resources.md) | Free readings on complexity + the Python dict implementation + glossary |
| [lecture-notes/01-mental-models-for-big-O.md](./02-lecture-notes/01-mental-models-for-big-O.md) | The six classes, the n-vs-runtime table, the nested-loop calibration drill |
| [lecture-notes/02-the-hash-map-pattern.md](./02-lecture-notes/02-the-hash-map-pattern.md) | The pattern's signals; counting; two-sum unsorted; single-pass caching |
| [lecture-notes/03-stating-complexity-out-loud.md](./02-lecture-notes/03-stating-complexity-out-loud.md) | The standard *Evaluate* sentence; the two-pointer-vs-hash-map debate |
| [exercises/README.md](./03-exercises/00-overview.md) | Index of the five hash-map drills |
| [exercises/drill-01-two-sum-unsorted.md](./03-exercises/drill-01-two-sum-unsorted.md) | The canonical hash-map problem |
| [exercises/drill-02-contains-duplicate.md](./03-exercises/drill-02-contains-duplicate.md) | Set membership, the simplest hash-set use |
| [exercises/drill-03-group-anagrams.md](./03-exercises/drill-03-group-anagrams.md) | Counting / frequency keys; `dict[tuple]` |
| [exercises/drill-04-valid-sudoku-rows.md](./03-exercises/drill-04-valid-sudoku-rows.md) | Constraint checking with sets |
| [exercises/drill-05-longest-consecutive-sequence.md](./03-exercises/drill-05-longest-consecutive-sequence.md) | O(n) via set; the "don't fall for O(n log n)" trap |
| [exercises/timed_runner.py](./03-exercises/timed_runner.py) | Pytest harness for grading your solutions |
| [challenges/README.md](./04-challenges/00-overview.md) | Index of weekly challenges |
| [challenges/challenge-01-subarray-sum-equals-k.md](./04-challenges/challenge-01-subarray-sum-equals-k.md) | Prefix-sum + hash map — *the* mid-level interview discriminator |
| [challenges/challenge-02-lru-cache.md](./04-challenges/challenge-02-lru-cache.md) | OrderedDict / hash-map + doubly-linked-list design |
| [quiz.md](./05-quiz.md) | 10 complexity questions |
| [homework.md](./06-homework.md) | Six practice problems (~5 hrs) |
| [mini-project/README.md](./07-mini-project/00-overview.md) | Re-do Week 1's five drills with full complexity sections |

---

## Stretch goals

- **Read the CPython `dict` implementation overview.** Knowing *why* a Python dict is O(1) average — and not always — separates good engineers from "just memorized it."
- **Time your own code.** Use `time.perf_counter()` or `%timeit` to *measure* the difference between an O(n²) loop and an O(n) hash-map version on n = 10⁴ inputs. Theory becomes muscle memory when you watch it.
- **Re-read Lecture 2 from Week 1.** UMPIRE doesn't get easier; it gets automatic. Drill it.

---

## Up next

[Week 3 — Sliding Window](../week-03/) — once your Week-2 mini-project is pushed and your Evaluate sections are tight.

---

*If you find errors in this material, please open an issue or send a PR. Future learners will thank you.*
