# Week 5 — Homework

Six problems, about five hours in total. Four of them are code and two are
writing. Two of the four coding problems are **parametric** — binary search on
the answer — because that is the highest-yield interview skill of the week and
two reps is the minimum that makes it stick.

Read each contract slowly before you start. Three of the four coding problems
define a **non-obvious return value** or a **non-obvious empty case**, and
those are the parts the acceptance checklists grade hardest.

| # | Problem | What it drills | Time |
|---|---------|----------------|-----:|
| 1 | [The Kiln Firing Schedule](./problem-01-kiln-firing-schedule.md) | Parametric — minimise a threshold, over an answer space that is not the integers | 60 min |
| 2 | [The Relay Handoff](./problem-02-relay-handoff.md) | Parametric — minimise the maximum over an exact partition | 60 min |
| 3 | [The Ridge Line](./problem-03-ridge-line.md) | Bisecting a sequence that is **not sorted**, on a local rule | 40 min |
| 4 | [The Duplicated Manifest](./problem-04-duplicated-manifest.md) | Rotated search where duplicates break the discriminator, and the worst case degrades to a scan | 45 min |
| 5 | [Deciding Without the Full Picture](./problem-05-deciding-without-the-full-picture.md) | Behavioral story #5, in STAR form | 45 min |
| 6 | [Autocomplete at Scale](./problem-06-autocomplete-at-scale.md) | System-design warm-up #5, 300 words | 45 min |
| | **Total** | | **4h 55m** |

## Do them in this order

Problems 1 and 2 are the parametric pair, and they are deliberately adjacent:
the same predicate machinery with a different budget attached. Do 1 first and
2 immediately after, while the cadence is still warm.

Problem 3 is the structural warm-up for
[Challenge 1](../challenges/challenge-01-order-book-boundary.md) — the same
"invent the rule that halves the problem" move in a much easier shape. If the
challenge felt overwhelming, do this one before going back to it.

Problem 4 is [Exercise 3](../exercises/exercise-03-ring-buffer-probe.md) with
the distinctness guarantee taken away, and it is the one problem this week
whose honest complexity is **not** `O(log n)`. Saying so out loud, and naming
the input that proves it, is the whole point.

Problems 5 and 6 have no program to run. Both pages declare that at the top,
and both still carry a full worked answer under **The Solution** — a model
story and a model design note — so you have something to compare your own
work against.

## What "done" looks like

Every coding problem ships a runnable answer beside its page, named
`<page stem>-solution.py`. Download it, run it, and compare its output against
the page's **Expected output** section before you decide you are finished.

For the two written problems, the deliverable is a file in your portfolio
repo, committed. Read both aloud once. A behavioral answer that reads well on
a page and stumbles out loud is not finished.

By the end of Week 5 your portfolio repo's commit history should show roughly
sixty to eighty commits in total — the cumulative count through Week 4 plus
ten to fifteen this week, including the mini-project write-ups and the two
challenge write-ups. The cadence is the artifact; keep the streak.

Up next: [Week 6 — Graphs Part 1: BFS](../../week-06-bfs/).
