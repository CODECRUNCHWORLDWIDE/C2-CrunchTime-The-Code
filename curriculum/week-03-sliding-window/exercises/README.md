# Week 3 — Exercises (FRAME Drills)

Five sliding-window problems. For each, you will:

1. Read the prompt.
2. Solve the problem yourself **with FRAME** in under 30 minutes, recorder running.
3. Write up your solution using the [`frame_template.md`](../../week-01-the-frame-method-and-thinking-aloud/exercises/frame_template.md) from Week 1.
4. Write your own pytest file for the examples in the drill, plus at least one case you invented, and make it pass.

**This week the *Research constraints* section is graded as strictly as *Make the solution* and *Examine (cost)*.** Every write-up must include the **30-second pattern-recognition memo** — three to five sentences an interviewer would hear in the first half-minute. The memo names: (a) sliding window, (b) fixed versus variable, (c) the invariant, (d) the auxiliary state. Drill it.

**Total time estimate:** about six hours for all five, an hour to ninety minutes each.

## The five drills (in order)

| # | Problem | Sub-shape | Difficulty |
|---|---------|-----------|------------|
| 1 | [The Busiest Staffing Block](exercise-01-staffing-block.md) | Fixed-size, running sum | Easy |
| 2 | [The Longest Clean Run](exercise-02-longest-clean-run.md) | Variable, shape A | Medium |
| 3 | [The Rota Window](exercise-03-rota-window.md) | Fixed-size, frequency invariant | Medium |
| 4 | [The Shortest Catchment](exercise-04-shortest-catchment.md) | Variable, shape B | Medium |
| 5 | [The Cold-Chain Load](exercise-05-cold-chain-load.md) | Variable, shape A, at-most-K distinct | Medium |

## Read the contracts, not the shapes

The five drills deliberately **disagree with each other** on the small print.

- Exercise 1 breaks ties toward the **latest** start. Exercise 2 breaks them toward the **earliest**. Exercise 5 goes back to the latest.
- Exercise 2 returns a **half-open span**. Exercise 4 returns a `(start, length)` pair. Exercise 5 returns `(start, count)`. Exercise 3 returns a bare integer.
- Exercise 1 signals "no answer" with `None`. Exercise 5 uses `(-1, 0)`. Exercise 3 uses `0`, which is also a legitimate answer.

None of this is decoration. A candidate who pattern-matches to "sliding window" and then writes the loop from memory will get several of these wrong, and each wrong one is a silent failure — code that runs and returns something plausible. Reading the contract *before* writing the loop is the habit these five drills exist to build.

## How to work each drill

- **Open a timer.** 30 minutes per drill.
- **Open a recorder.** A phone voice memo is fine.
- **Open the drill file.** Read the prompt; do not scroll past it.
- **Start FRAME.** Out loud. The whole way through.
- **Save your solution** as `drill_NN_solution.py` in your portfolio repo, in a `c2-week-03/` subfolder.
- **Write up using the template.** Save as `drill-NN-<slug>.md` in your portfolio repo. The Research constraints section now requires the 30-second pattern-recognition memo.
- **Run your tests.** `pytest c2-week-03/ -v`.

When done, your portfolio looks like:

```
crunchtime-interview-prep-<you>/
└── frame-writeups/
    ├── c2-week-01/                     (from Week 1)
    ├── c2-week-02/                     (from Week 2)
    └── c2-week-03/                     (new this week)
        ├── exercise-01-staffing-block.md
        ├── drill_01_solution.py
        ├── exercise-02-longest-clean-run.md
        ├── drill_02_solution.py
        ├── exercise-03-rota-window.md
        ├── drill_03_solution.py
        ├── exercise-04-shortest-catchment.md
        ├── drill_04_solution.py
        ├── exercise-05-cold-chain-load.md
        └── drill_05_solution.py
```

## A note on the recognition discipline this week

In Weeks 1 and 2 you said the pattern name and moved on. This week we want a **specific, repeatable sentence** in Research constraints — the kind a senior interviewer marks as a positive signal. The shape:

> "This is a sliding-window problem because [contiguity signal from the prompt]. The window is [fixed-size with k = ... / variable-size]. The invariant I will maintain is [property]. The auxiliary state is [running sum / frequency table / last-index map / frequency table plus a matched count]."

Listen back to your Exercise 1 and Exercise 5 Research constraints sections side by side. Exercise 5 should be a faster, more confident version of the same sentence shape. If it is not, your portfolio is missing a week of progress.
