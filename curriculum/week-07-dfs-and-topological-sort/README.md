# Week 7 — Depth-First Search and Topological Sort

```
┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐
│ F │  │ R │  │ A │  │ M │  │ E │
└───┘  └───┘  └───┘  └───┘  └───┘
```

> *Week 6 installed breadth-first search — the queue, the visited set, the argument that levels only ever grow. Week 7 installs its twin: **depth-first search** — go all the way down one arm before you touch the second, the three colours that tell you whether you have walked into your own path, and the trick of doing the work on the way back up. By Sunday you can write the recursive walk, the explicit-stack walk and Kahn's algorithm from memory, and say out loud why each one is the right tool for the question in front of you.*

Welcome to Week 7 of **C2 · CrunchTime — The Code**, the third week of Phase 2.
This week installs depth-first search and its three highest-value uses:
**connectivity** (the easy one), **loop detection** (the grey set), and
**topological sort** (waiting counts, and the post-order trick).

Depth-first search has a reputation for being the harder of the pair, and that
is partly fair. The code is shorter than breadth-first search. What is heavier
is the *state you are carrying* — where you are, as opposed to where you have
been — and the bugs are quieter. A wrong depth-first answer usually looks
completely reasonable.

By Sunday of Week 7 you will:

- **Recognise** a depth-first problem in thirty seconds and name the shape in
  the next sentence: connectivity, does-a-path-exist, loop detection,
  topological sort.
- **Write** the recursive walk from memory, say what the visited set is
  protecting, and explain why the cost is `O(V + E)` — one look at every node,
  one look at every edge, and then it is done.
- **Write** the explicit-stack walk, and defend it properly. CPython's default
  recursion limit is 1,000 frames. Raising it is not the fix, and
  [Exercise 2](./exercises/exercise-02-conveyor-reachability.md) is the page
  that shows you the real `RecursionError` and argues it out.
- **Use the three colours** — white for untouched, grey for "on the path under
  my feet", black for finished — to find a loop in a directed graph, and say
  the invariant out loud: *an arrow into a grey node is a loop; an arrow into a
  black node is ordinary and proves nothing.*
- **Produce a topological order both ways.** Kahn's algorithm counts what each
  node is waiting on and releases the ones waiting on nothing; the depth-first
  version appends each node when it finishes. Same answer, different shape,
  different free by-products. Defend the choice.
- Have solved **five exercises**, one challenge, six homework problems and the
  mini-project, each with a FRAME write-up.

---

## Learning objectives

By the end of this week, you will be able to:

- **Match** a depth-first problem in thirty seconds from its signals: "any
  path", "all the pieces", "connected", "is there a circular dependency", "in
  what order can these be done", "given these prerequisites".
- **Tell depth-first from breadth-first in one sentence.** Depth-first for
  connectivity, loops, topological order and any-path. Breadth-first for
  shortest path, level by level, and spreading from many sources at once. Both
  cost `O(V + E)`; the choice is about the shape of the answer, not the speed.
- **Implement** three templates without notes: the recursive walk with a
  visited set, the explicit-stack walk that survives a graph deeper than the
  recursion limit, and Kahn's algorithm with waiting counts and a ready set.
- **Apply the three colours** to a directed graph, and explain why the
  undirected trick — "ignore the edge I came in on" — does not transfer.
- **Build a topological order from a post-order walk** and defend it: a node
  goes on the list only once everything below it is already on it, so the list
  comes out in order with nothing to reverse and no counting.
- **Choose between Kahn and the post-order walk.** Kahn is iterative, gives you
  the waves for free, and detects a loop by noticing it ran out of ready work.
  The post-order walk is shorter and gives loop detection free if you carry the
  colours, but has no notion of "at the same time" in it.
- **Recognise when depth-first search does not apply** — shortest path on an
  unweighted graph is breadth-first (Week 6), shortest path with weights is
  Dijkstra (Week 10), level-by-level output is breadth-first.
- **Apply depth-first search to a tree**, the special case where there are no
  loops and the visited set disappears, because a tree has exactly one way in
  to every node.

## Standards this week meets

| Bar | What this week is measured against |
| --- | --- |
| University | `CS 1332` — Depth-first traversal, cycle detection, and topological ordering of a dependency graph. |
| Industry | Say whether a plan can be run at all before anybody starts it: build the dependency graph out of what you were handed, give the order the stages may be switched on and which of them can go at once, and when the requirements are circular report the chain itself rather than a bare failure. |
| Beyond the bar | Two homework problems ship the plausible wrong answer beside the correct one and make the learner run it — the recursive walk that raises `RecursionError` on the largest input the constraints allow, and the parent-only check that gives a broken index a clean bill of health — because neither failure announces itself — `homework/README.md` |

---

## Prerequisites

- **Weeks 1-6 complete.** You can deliver FRAME without notes on a queue and
  visited-set problem.
- **Comfortable with Python recursion.** This is the week where recursion
  limits stop being trivia. Run
  `python -c "import sys; print(sys.getrecursionlimit())"` once — it prints
  `1000` — and keep that number in mind all week.
- **Comfortable with `dict[node, list[node]]`.** The adjacency list is this
  week's graph. Handed an edge list, your first line is usually
  `adj = collections.defaultdict(list)`, then one loop.
- **Comfortable with `collections.deque` and `heapq`.** Kahn's algorithm needs
  a ready set; a `deque` gives you any legal order and a heap gives you one
  specific, testable order.

---

## Topics covered

- The recursive walk — the three-line body, and the visited set as the thing
  that makes it terminate
- The explicit-stack walk — why the pending work moves off the call stack and
  onto the heap, and why raising the recursion limit is not the fix
- The **three colours** — white, grey, black — and loop detection in a directed
  graph
- **Loop detection in an undirected graph** — the parent-pointer technique, and
  why it is a different problem
- **Topological sort via Kahn's algorithm** — waiting counts, the ready set,
  and detecting a loop by running out of work
- **Topological sort via a post-order walk** — finish a node, then append it
- **Waves** — Kahn drained in rounds, and why the number of waves is the length
  of the longest chain
- **Depth-first search on a tree** — no loops, no visited set, and the bounds
  carried down instead
- **Pre-order against post-order** — computing on the way down against
  computing on the way up
- **Why depth-first search does not find shortest paths**, and what
  breadth-first adds

---

## Weekly schedule (intensive · 36h)

| Day | Focus | Lectures | Exercises | Challenges | Quiz/Read | Homework | Mini-Project | Self-Study | Daily Total |
|-----|-------|---------:|----------:|-----------:|----------:|---------:|-------------:|-----------:|------------:|
| Monday | Recursive walk + connectivity; exercises 1-2 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Tuesday | Explicit stack + the three colours; exercise 3 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Wednesday | Topological sort both ways; exercises 4-5 | 2h | 2h | 0h | 0.5h | 1h | 0h | 0.5h | 6h |
| Thursday | Mini-project drafting; challenge ramp | 0h | 1h | 1h | 0.5h | 1h | 1.5h | 1h | 6h |
| Friday | Challenge 1 — chokepoint mains | 0h | 0h | 2h | 0.5h | 1h | 1.5h | 1h | 6h |
| Saturday | Mini-project — the two write-ups | 0h | 0h | 0h | 0.5h | 1h | 3h | 0h | 4.5h |
| Sunday | Quiz + retrospective + push | 0h | 0h | 0h | 0.5h | 0h | 4h | 0h | 4.5h |
| **Total** | | **6h** | **7h** | **3h** | **3h** | **6h** | **10h** | **3.5h** | **38.5h** |

(The week budgets about 36 hours; the table sums a little higher to absorb the
Phase 2 ramp. Drop half an hour from Self-Study if 36 is your hard ceiling.)

**Mastery (10h a week):** spread the same content over three calendar weeks.
The mini-project lands in calendar Week 22 of the mastery pathway. See the
[mastery study plan](../study-plans/mastery-1-year.md).

---

## How to navigate this week

| File | What's inside |
|------|---------------|
| [README.md](./README.md) | This overview |
| [resources.md](./resources.md) | Free readings, references and the week's glossary additions |
| [lecture-notes/01-recursive-dfs.md](./lecture-notes/01-recursive-dfs.md) | The recursive walk, visited-set discipline, pre-order against post-order, the four bug patterns |
| [lecture-notes/02-iterative-dfs.md](./lecture-notes/02-iterative-dfs.md) | The explicit-stack walk — the version that survives a graph deeper than the recursion limit |
| [lecture-notes/03-topological-sort.md](./lecture-notes/03-topological-sort.md) | Post-order topological sort, Kahn's algorithm, the three colours, loop detection in a directed graph |
| [exercises/README.md](./exercises/README.md) | Index of the five exercises |
| [exercises/exercise-01-repeater-clusters.md](./exercises/exercise-01-repeater-clusters.md) | Connectivity on a link table — the recursive walk, warmed up |
| [exercises/exercise-02-conveyor-reachability.md](./exercises/exercise-02-conveyor-reachability.md) | The explicit stack, and the real `RecursionError` that makes the case for it |
| [exercises/exercise-03-batch-loop-audit.md](./exercises/exercise-03-batch-loop-audit.md) | The three colours, and reporting the loop rather than just its existence |
| [exercises/exercise-04-refit-order.md](./exercises/exercise-04-refit-order.md) | Kahn's algorithm — waiting counts, a ready heap, and what the leftovers mean |
| [exercises/exercise-05-firmware-install-order.md](./exercises/exercise-05-firmware-install-order.md) | Topological sort the other way — finish a node, then append it |
| [challenges/README.md](./challenges/README.md) | Index of the two challenges |
| [challenges/challenge-01-chokepoint-mains.md](./challenges/challenge-01-chokepoint-mains.md) | Discovery times and low-links — the pipes whose failure splits the network |
| [challenges/challenge-02-consist-reconstruction.md](./challenges/challenge-02-consist-reconstruction.md) | Derive the constraints, then sort them — and say whether the answer is forced |
| [quiz.md](./quiz.md) | Ten pattern-recognition prompts, key at the bottom |
| [homework/README.md](./homework/README.md) | Six problems, about five hours: connectivity, loop detection, a reverse-topological question, a tree walk, plus the behavioural and design warm-ups |
| [mini-project/README.md](./mini-project/README.md) | **The restart planner** — one graph, four questions, and the week's two FRAME write-ups |

Every problem page carries its own answer, under `## The Solution`, with a
runnable file beside it. There is no separate solutions document anywhere in
this course: a separate answers file drifts out of step with its problems, and
the moment it does it teaches something false with complete confidence.

---

## Stretch goals

- **Skim twenty titles from a practice platform's depth-first tag** and, for
  each, predict in five seconds: connectivity, loop, topological order, tree
  walk, or backtracking? Do not solve any of them. This drills recognition,
  which is the thing Phase 2 grades.
- **Re-derive the recursive template from scratch** without re-reading
  Lecture 1. If you cannot, you do not own it yet. Re-read and re-derive until
  you can.
- **Find one production story where this week's material is load-bearing.**
  Build-system dependency resolution is a topological sort. A garbage
  collector's reachability pass is a depth-first walk over the object graph. A
  module loader's "circular import" error is the grey set. Pick one, read for
  twenty minutes, and write a paragraph. That question — *where does this live
  in real systems?* — lifts you out of the practice-problem frame faster than
  another exercise will.
- **Read one paragraph on strongly connected components.** It is the natural
  next step after loop detection and post-order, and it is out of scope this
  week. C5 covers it.

---

## What "done" looks like for Week 7

A learner who has shipped Week 7 has, in their portfolio repo:

- Five FRAME write-ups for the exercises, with recordings of ten minutes or
  more.
- One FRAME write-up for the chokepoint mains challenge.
- The quiz answered, with the score recorded.
- The six homework problems committed, including the behavioural story and the
  design memo.
- **Two mini-project write-ups** — one on the depth-first half, one on the
  topological half — under `frame-writeups/c2-week-07/mini-project/`, each
  rejecting the other's approach out loud and linking to it.
- A push log showing daily commits, Monday to Sunday.

If all of that is present and pushed, the third week of Phase 2 is closed.

---

## A note on the Phase 2 ramp

Week 7 is, content-wise, *the* graph week. With breadth-first search from
Week 6 behind you, you now hold the two walks that anchor every graph problem
in the standard repertoire. Week 8 moves to heaps and priority queues, Week 9
is Mock #2 — at least one graph problem is graded — and Week 10 returns to
graphs with weights and union-find.

If you are ahead by Friday, the right stretch is **not** another exercise. It is
to polish the Week 6 mini-project alongside this one, because the two together
are the graph half of your portfolio and the Phase 2 retrospective in Week 9 is
much easier when both are finished.

If you are behind by Wednesday, do
[Exercise 4](./exercises/exercise-04-refit-order.md) before
[Exercise 5](./exercises/exercise-05-firmware-install-order.md) and leave
Exercise 5 for the weekend. Topological sort is the most heavily graded Phase 2
pattern in Mock #2, and Kahn's version is the one that comes up.

---

## Up next

[Week 8 — Heaps and Priority Queues](../week-08-heaps-and-priority-queues/) —
once your two mini-project write-ups are pushed, your grey-set invariant is
clean, and you can write Kahn's algorithm from memory without opening the
lecture.

---

*If you find errors in this material, please open an issue or send a PR. Future
learners will thank you.*
