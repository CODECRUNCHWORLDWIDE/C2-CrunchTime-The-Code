# Week 6 — Homework

Six problems, about five hours. Four are code, each with its own page and a
runnable worked answer beside it; two are the week's writing warm-ups. Everything
commits to your portfolio repo.

The four coding problems cover the four corners of the week: grid components,
multi-source, an implicit state graph, and two searches read together.

| # | Problem | Sub-shape | Est. time |
|---|---------|-----------|----------:|
| 1 | [Scrap Heaps](./problem-01-scrap-heaps.md) | Grid BFS — separate components, and measuring each | 45 min |
| 2 | [Worst-Served Bay](./problem-02-worst-served-bay.md) | Multi-source grid BFS, where the answer is the worst square | 45 min |
| 3 | [The Shim Dial](./problem-03-shim-dial.md) | BFS on a graph nobody wrote down | 45 min |
| 4 | [Cairn Routes](./problem-04-cairn-routes.md) | Two searches, and the arithmetic that reads the answer | 60 min |
| 5 | [Behavioural story #6](#problem-5--behavioural-story-6) | Writing | 45 min |
| 6 | [System-design warm-up #6](#problem-6--system-design-warm-up-6) | Writing | 45 min |

Each coding problem's page carries the brief, the constraints, a real captured
run, the full solution and the bugs it is built to prevent. Run any worked answer
directly:

```bash
python problem-01-scrap-heaps.py
```

Problems 1 and 2 are the grid pair — one counts components, the other measures
the worst case across a whole map from many sources. Problem 3 is the recognition
problem of the week: the graph is a *machine*, and seeing that a dial setting is
a node is the entire difficulty. Problem 4 is the hardest and the best preparation
for [Challenge 1](../challenges/challenge-01-trunk-splice.md), because the search
stops being where the answer comes from.

---

## Problem 5 — Behavioural story #6

The story bank continues.

**Acceptance:**

- A file `behavioral/story-06.md` in your portfolio repo.
- Topic: **"Tell me about a time you had to choose between two approaches with
  different trade-offs."**
- Format: Situation, Task, Action, Result.
- 200–400 words.
- Read it aloud at least twice.

**Bonus credit** for connecting it to the meta-skill of this week. Every graph
problem is "breadth-first or depth-first?", and that is a decision with explicit
trade-offs: breadth-first finds shortest paths and holds a whole level in memory;
depth-first is cheaper in memory, natural for cycle detection, and gives no
distance guarantee. If your story's structure matches that structure, say so —
interviewers notice when a candidate finds the connection between their
behavioural answer and their technical one.

---

## Problem 6 — System-design warm-up #6

The sixth 300-word warm-up.

**Acceptance:**

- A file `system-design/notes-week-06.md` with a 300-word answer to: **"How would
  you design a web crawler that respects `robots.txt`, handles about ten billion
  URLs, and finishes one full crawl per month?"**
- Write it before looking anything up. What you would say in an interview today
  is the thing being practised.
- Afterwards, read one free article on crawler architecture and note three things
  you would add.

The connection to this week is direct: a crawler is breadth-first search over the
URL graph at planetary scale. The "frontier" is the queue. The visited set is the
interesting part — ten billion URLs will not fit in memory, so it becomes a
sharded store or a probabilistic filter, and the trade-off is that a probabilistic
filter can claim to have seen a page it has not. Naming both the shape and that
engineering reality is what a strong answer sounds like.

---

## Time budget

| Problem | Time |
|---------|-----:|
| 1 — Scrap Heaps | 45 min |
| 2 — Worst-Served Bay | 45 min |
| 3 — The Shim Dial | 45 min |
| 4 — Cairn Routes | 60 min |
| 5 — Behavioural story #6 | 45 min |
| 6 — System-design warm-up #6 | 45 min |
| **Total** | **4h 45m** |

---

## Rubric (5 axes, 4 points each)

| Axis | What "great" looks like |
|------|--------------------------|
| Frame the problem | The memo names the shape — grid, node graph, implicit state graph — the seed, and what the answer is. |
| Reason about options | Four to six bullets before any code, with depth-first search named and rejected for a stated reason, or accepted for one. |
| Assemble the solution | A `deque`, marked seen on enqueue, type hints throughout. |
| Measure it | A trace on at least two examples, one of them an unreachable case. |
| Evaluate the cost | Time, space, best/average/worst, the trade-off and the improvement — in the problem's own numbers, not abstract n. |

Twenty points per coding problem, eighty for the four. Score yourself honestly;
the number is only useful if it is true.

When the set is done, push and move on to the
[mini-project](../mini-project/README.md).
