# Week 2 — Exercises (FRAME Drills)

Five hash-map problems. For each, you will:

1. Read the prompt.
2. Solve the problem yourself **with FRAME** in under 30 minutes, recorder running.
3. Write up your solution using [`frame_template.md`](../../week-01-the-frame-method-and-thinking-aloud/exercises/frame_template.md) — the same template as Week 1, reused.
4. Write your own tests from the examples in the drill file, plus at least two adversarial cases of your own.

**This week the *Examine (cost)* section is graded as strictly as the *Make the solution* section.** Follow the five-piece structure from [Lecture 3](../lecture-notes/03-stating-complexity-out-loud.md): time / space / best-average-worst / tradeoff / improvement. Every write-up. No exceptions.

**Total time estimate:** ~6 hours for all five, 1 to 1.5 hours each.

## The five drills (in order)

| # | Problem | Sub-shape | Difficulty |
|---|---------|-----------|------------|
| 1 | [The Refund Pair](exercise-01-refund-pair.md) | Complement lookup | Easy |
| 2 | [The Repeated Badge](exercise-02-badge-rescan.md) | Set membership | Easy |
| 3 | [Stage Twins](exercise-03-stage-twins.md) | Canonical key / frequency | Medium |
| 4 | [The On-Call Grid](exercise-04-on-call-grid.md) | Set membership × 3 axes | Medium |
| 5 | [The Longest Dock Run](exercise-05-longest-dock-run.md) | Set membership + root trick | Medium |

They are ordered so each one adds exactly one thing. Exercise 1 introduces the map with a payload; Exercise 2 strips the payload away; Exercise 3 makes you invent the key; Exercise 4 makes you run three structures at once; Exercise 5 makes you defend a complexity claim that looks wrong. Do them in order.

## A note on the contracts

Every drill this week specifies its **empty case**, its **no-answer case**, and its **tie-break**, and several of them return `None` rather than a falsy sentinel. That is deliberate. Half of interview failure is solving the problem you assumed rather than the one you were given, and these drills are built so that assuming costs you a visible, specific example. If you find yourself reading a spec line twice, that line is doing its job.

## How to work each drill

- **Open a timer.** 30 minutes per drill.
- **Open a recorder.** A phone voice memo is fine.
- **Open the drill file.** Read the prompt and the constraints. Do not scroll past the examples until you have restated the problem out loud.
- **Start FRAME.** Out loud. The whole way through.
- **Save your solution** as `drill_NN_solution.py` in your portfolio repo, in a `c2-week-02/` subfolder.
- **Write up using the template.** Save as `drill-NN-<slug>.md`. Pay special attention to Examine (cost); it is graded this week.
- **Run your tests.** Every drill lists examples that were chosen to break a specific wrong approach — turn each one into an assertion.

When you are done, your portfolio looks like this:

```
crunchtime-interview-prep-<you>/
└── frame-writeups/
    ├── c2-week-01/                    (from Week 1)
    └── c2-week-02/                    (new this week)
        ├── exercise-01-refund-pair.md
        ├── drill_01_solution.py
        ├── exercise-02-badge-rescan.md
        ├── drill_02_solution.py
        ├── exercise-03-stage-twins.md
        ├── drill_03_solution.py
        ├── exercise-04-on-call-grid.md
        ├── drill_04_solution.py
        ├── exercise-05-longest-dock-run.md
        └── drill_05_solution.py
```

## A note on the Examine (cost) discipline

By Exercise 5 your Examine (cost) section should be a confident two-minute monologue. If you are still terse by Exercise 5, go back and redo Exercise 1's Examine (cost) section — the problem is not that Exercise 5 was hard, it is that you never built the habit on the easy one.

Listen to your Exercise 1 and Exercise 5 recordings back to back. Exercise 5's Examine (cost) should be markedly stronger. If it is not, your portfolio is missing a week of progress even though it has a week of commits.
