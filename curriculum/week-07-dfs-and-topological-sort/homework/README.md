# Week 7 — Homework

Six problems, about five hours. Four are code, each with its own page and a
runnable worked answer beside it; two are the week's writing warm-ups.
Everything commits to your portfolio repo.

The four coding problems walk the week's range: components counted from an edge
list, the cheapest ordering question, an answer that needs *every* branch to
succeed, and a rule about a node's whole subtree rather than its children.

| # | Problem | Sub-shape | Est. time |
|---|---------|-----------|----------:|
| 1 | [Hose Clusters](./problem-01-hose-clusters.md) | Connected components from an edge list | 45 min |
| 2 | [Prep Step Audit](./problem-02-prep-step-audit.md) | Is there a legal order at all — yes or no | 45 min |
| 3 | [Safe Forwarding](./problem-03-safe-forwarding.md) | Every branch must succeed, and the recursion limit decides how | 60 min |
| 4 | [Shelf Index Audit](./problem-04-shelf-index-audit.md) | A rule about ancestors, not parents | 45 min |
| 5 | [Behavioural story #7](#problem-5--behavioural-story-7) | Writing | 45 min |
| 6 | [System-design warm-up #7](#problem-6--system-design-warm-up-7) | Writing | 45 min |

Each coding problem's page carries the brief, the constraints, a real captured
run, the full solution and the bugs it prevents. Run any worked answer directly:

```bash
python problem-01-hose-clusters.py
```

Problems 3 and 4 are the two that matter most, and for the same reason: each
ships the **plausible wrong answer** beside the right one so you can watch it
fail. Problem 3's recursive walk raises `RecursionError` on the largest input the
constraints allow. Problem 4's parent-only check gives a clean bill of health to
an index that is broken. Neither failure announces itself, and both are the kind
a mock will find.

---

## Problem 5 — Behavioural story #7

The story bank continues.

**Acceptance:**

- A file `behavioral/story-07.md` in your portfolio repo.
- Topic: **"Tell me about a time you had to refactor or rewrite a piece of code
  that you, or someone else, wrote earlier."**
- Format: Situation, Task, Action, Result.
- 200–400 words.
- Read it aloud at least twice.

**Bonus credit** for connecting it to this week's meta-skill: recursive against
iterative. A refactor from a recursive walk to an iterative one, motivated by
recursion-limit risk or by production performance, is a textbook engineering
decision — and [Problem 3](./problem-03-safe-forwarding.md) makes you watch that
exact risk turn into a crash. Every "I refactored X" story is a
two-approaches-with-different-trade-offs story, and this is a clean instance of
one you now have first-hand.

---

## Problem 6 — System-design warm-up #7

The seventh 300-word warm-up.

**Acceptance:**

- A file `system-design/notes-week-07.md` with a 300-word answer to: **"How would
  you design a build system that resolves and executes about 50,000 build
  targets in parallel, respecting prerequisite dependencies?"**
- Write it before looking anything up. What you would say in an interview today
  is the thing being practised.
- Afterwards, read one free article on build-system architecture — a major build
  tool's design docs, or the section of the `make` manual on how it reads a
  makefile — and note three things you would add.

The connection to this week is direct: a build system is a topological sort with
a parallel execution layer on top. The build graph is a directed acyclic graph of
targets; the topological order is the legal order of compilation; the ready queue
is the set of targets with no pending prerequisites.

The tell on this prompt is mentioning **both** — the ordering framing *and* the
parallelism. Every target sitting in the ready queue at the same moment can be
built at the same moment, which is exactly what a `-j N` flag does, and it falls
straight out of the counting algorithm rather than being bolted on.

---

## Time budget

| Problem | Time |
|---------|-----:|
| 1 — Hose Clusters | 45 min |
| 2 — Prep Step Audit | 45 min |
| 3 — Safe Forwarding | 60 min |
| 4 — Shelf Index Audit | 45 min |
| 5 — Behavioural story #7 | 45 min |
| 6 — System-design warm-up #7 | 45 min |
| **Total** | **4h 45m** |

---

## Rubric (5 axes, 4 points each)

| Axis | What "great" looks like |
|------|--------------------------|
| Frame the problem | The memo names the shape, what one node means, and — for problems 3 and 4 — the plausible wrong rule and why it is wrong. |
| Reason about options | Four to six bullets before any code, with the recursion bound named *before* the algorithm is chosen rather than mentioned afterwards. |
| Assemble the solution | A visited set with a stated invariant; type hints throughout; iterative where the bound demands it. |
| Measure it | A trace on at least two inputs, one of them the case the wrong version passes. |
| Evaluate the cost | Time, space, best/average/worst, the trade-off and the improvement — including stack depth, which is a space cost people forget to count. |

Twenty points per coding problem, eighty for the four. Score yourself honestly;
the number is only useful if it is true.

When the set is done, push and move on to the
[mini-project](../mini-project/README.md).
