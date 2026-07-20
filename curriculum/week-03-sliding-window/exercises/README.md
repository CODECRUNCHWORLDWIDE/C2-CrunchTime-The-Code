# Week 3 — Exercises (UMPIRE Drills)

Five sliding-window problems. For each, you will:

1. Read the prompt.
2. Solve the problem yourself **with UMPIRE** in <30 minutes per problem, recorder running.
3. Write up your solution using the [`umpire_template.md`](../../week-01-the-umpire-method-and-thinking-aloud/exercises/umpire_template.md) from Week 1.
4. Run [`timed_runner.py`](timed_runner.py) against your code to verify it passes.

**This week the *Match* section is graded as strictly as *Implement* and *Evaluate*.** Every write-up must include the **30-second pattern-recognition memo** — three to five sentences that an interviewer would hear in the first half-minute. The memo names: (a) sliding window, (b) fixed vs variable, (c) the invariant, (d) the auxiliary state. Drill it.

**Total time estimate:** ~6 hours for all five (1–1.5 hr each).

## The five drills (in order)

| # | Problem | Sub-shape | Difficulty |
|---|---------|-----------|------------|
| 1 | [Fixed Window Average](drill-01-fixed-window-average.md) | Fixed-size | Easy |
| 2 | [Longest Substring Without Repeating Characters](drill-02-longest-substring-no-repeat.md) | Variable, shape A | Medium |
| 3 | [Permutation in String](drill-03-permutation-in-string.md) | Fixed-size, frequency invariant | Medium |
| 4 | [Minimum Size Subarray Sum](drill-04-min-size-subarray-sum.md) | Variable, shape B | Medium |
| 5 | [Fruit Into Baskets](drill-05-fruit-into-baskets.md) | Variable, shape A (at most 2 distinct) | Medium |

## How to work each drill

- **Open a timer.** 30 minutes per drill.
- **Open a recorder.** Phone voice memo is fine.
- **Open the drill file.** Read the prompt; do not scroll past it.
- **Start UMPIRE.** Out loud. The whole way through.
- **Save your solution** as `drill_NN_solution.py` in your portfolio repo, in a `c2-week-03/` subfolder.
- **Write up using the template.** Save as `drill-NN-<slug>.md` in your portfolio repo. The Match section now requires the 30-second pattern-recognition memo.
- **Run the tests.** `pytest exercises/timed_runner.py -v`.

When done, your portfolio looks like:

```
crunchtime-interview-prep-<you>/
└── umpire-writeups/
    ├── c2-week-01/                       (from Week 1)
    ├── c2-week-02/                       (from Week 2)
    └── c2-week-03/                       (new this week)
        ├── drill-01-fixed-window-average.md
        ├── drill_01_solution.py
        ├── drill-02-longest-substring-no-repeat.md
        ├── drill_02_solution.py
        ├── drill-03-permutation-in-string.md
        ├── drill_03_solution.py
        ├── drill-04-min-size-subarray-sum.md
        ├── drill_04_solution.py
        ├── drill-05-fruit-into-baskets.md
        └── drill_05_solution.py
```

## A note on the Match discipline this week

In Weeks 1–2 you said the pattern name and moved on. This week we want a **specific, repeatable sentence** in Match — the kind a senior interviewer marks as a positive signal. The shape:

> "This is a sliding-window problem because [contiguity signal from the prompt]. The window is [fixed-size with k = ... / variable-size]. The invariant I'll maintain is [property]. The auxiliary state is [sum / Counter / set / Counter + need-formed]."

Listen back to your Drill 1 and Drill 5 recordings of your Match sections side by side. Drill 5 should be a faster, more confident version of the same sentence shape. If it isn't, your portfolio is missing a week of progress.
