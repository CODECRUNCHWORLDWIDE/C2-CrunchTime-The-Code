# Week 7 — Exercises

Three exercises. Each is UMPIRE-narrated, recorded, and graded against the test cases in the file itself. Worked solutions live in [`SOLUTIONS.md`](./SOLUTIONS.md) — consult only after attempting each exercise.

| # | Exercise | Pattern | Difficulty | Target solve time |
|---|----------|---------|------------|------------------:|
| 1 | [Number of Provinces](./exercise-01-number-of-provinces.py) (LC 547) | Recursive DFS on an adjacency matrix; connectivity | Easy/Medium | 20 min |
| 2 | [Has Path](./exercise-02-has-path.py) (LC 1971) | Iterative DFS with explicit stack; path existence | Medium | 25 min |
| 3 | [Course Schedule II](./exercise-03-course-schedule-ii.py) (LC 210) | Topological sort — Kahn's algorithm | Medium | 30 min |

Do them in order. Exercise 1 cements the recursive DFS template on a directed-but-undirected-in-practice graph (the adjacency matrix is symmetric). Exercise 2 forces you to write iterative DFS with the explicit stack — the version that survives Python's recursion limit. Exercise 3 is the canonical Phase-2 topological-sort problem; expect it on Mock #2.

Each starter file contains:

- The problem statement
- The required function signature with type hints
- An empty body marked `# TODO`
- A `pytest`-style test block at the bottom
- A self-check checklist (UMPIRE)

Run a single exercise:

```bash
python3 exercises/exercise-01-number-of-provinces.py
```

Or run all under `pytest` if you prefer that harness:

```bash
pytest exercises/ -v
```

(Both forms work — the test block uses bare `assert` so plain `python3` execution is fine.)

## A note on what is being graded

Phase 1 graded you mostly on *correctness*. Phase 2 adds the *defense* axis: for every DFS exercise, your write-up must state which template you used (recursive / iterative / Kahn / three-color), why, and what the failure mode of the *other* template would have been. The recording catches whether you say it; the write-up catches whether you can write it.

Defense is the difference between "the code works" and "the code is robust." Interviewers test for the latter. Drill on the latter.

---

After all three exercises pass, move on to [the challenge](../04-challenges/challenge-01-critical-connections.md) — Critical Connections in a Network, the canonical hard DFS application of the week.
