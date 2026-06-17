# Week 2 — Exercises (UMPIRE Drills)

Five hash-map problems. For each, you will:

1. Read the prompt.
2. Solve the problem yourself **with UMPIRE** in <30 minutes per problem, recorder running.
3. Write up your solution using [`umpire_template.md`](../../week-01-the-umpire-method-and-thinking-aloud/03-exercises/umpire_template.md) (the same template as Week 1 — reuse it).
4. Run [`timed_runner.py`](./timed_runner.py) against your code to verify it passes.

**This week the *Evaluate* section is graded as strictly as the *Implement* section.** Follow the five-piece structure from [Lecture 3](../02-lecture-notes/03-stating-complexity-out-loud.md): time / space / best-avg-worst / tradeoff / improvement. Every write-up. No exceptions.

**Total time estimate:** ~6 hours for all five (1-1.5 hr each).

## The five drills (in order)

| # | Problem | Sub-shape | Difficulty |
|---|---------|-----------|------------|
| 1 | [Two Sum (Unsorted)](./drill-01-two-sum-unsorted.md) | Complement lookup | Easy |
| 2 | [Contains Duplicate](./drill-02-contains-duplicate.md) | Set membership | Easy |
| 3 | [Group Anagrams](./drill-03-group-anagrams.md) | Frequency / canonical-key | Medium |
| 4 | [Valid Sudoku — Rows / Cols / Boxes](./drill-04-valid-sudoku-rows.md) | Set membership × 3 | Medium |
| 5 | [Longest Consecutive Sequence](./drill-05-longest-consecutive-sequence.md) | Set membership + clever start | Medium |

## How to work each drill

- **Open a timer.** 30 minutes per drill.
- **Open a recorder.** Phone voice memo is fine.
- **Open the drill file.** Read the prompt; do not scroll past it.
- **Start UMPIRE.** Out loud. The whole way through.
- **Save your solution** as `drill_NN_solution.py` in your portfolio repo, in a `c2-week-02/` subfolder.
- **Write up using the template.** Save as `drill-NN-<slug>.md` in your portfolio repo. Pay special attention to the Evaluate section — it is graded this week.
- **Run the tests.** `pytest exercises/timed_runner.py -v`.

When done, your portfolio looks like:

```
crunchtime-interview-prep-<you>/
└── umpire-writeups/
    ├── c2-week-01/                    (from Week 1)
    └── c2-week-02/                    (new this week)
        ├── drill-01-two-sum-unsorted.md
        ├── drill_01_solution.py
        ├── drill-02-contains-duplicate.md
        ├── drill_02_solution.py
        ├── drill-03-group-anagrams.md
        ├── drill_03_solution.py
        ├── drill-04-valid-sudoku-rows.md
        ├── drill_04_solution.py
        ├── drill-05-longest-consecutive-sequence.md
        └── drill_05_solution.py
```

## A note on the Evaluate discipline

By Drill 5 your Evaluate section should be a confident two-minute monologue. If you're still terse by Drill 5, re-do Drill 1's Evaluate section.

Listen to your Drill 1 and Drill 5 recordings back to back. The Drill 5 Evaluate section should be markedly stronger. If it isn't, your portfolio is missing a week of progress.
