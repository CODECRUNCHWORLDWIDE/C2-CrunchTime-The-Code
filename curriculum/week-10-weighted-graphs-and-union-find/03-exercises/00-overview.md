# Week 10 — Exercises

Three exercises covering the three Week-10 pattern centers: heap-Dijkstra (Network Delay Time), Bellman-Ford with a hop constraint (Cheapest Flights), and the canonical DSU drill (Number of Provinces).

| # | File | Pattern | LC | Target time |
|---|------|---------|---:|------------:|
| 1 | [exercise-01-network-delay-time.py](./exercise-01-network-delay-time.py) | Heap-Dijkstra | 743 | 25 min |
| 2 | [exercise-02-cheapest-flights-bellman-ford.py](./exercise-02-cheapest-flights-bellman-ford.py) | Bellman-Ford (K + 1 passes; snapshot) | 787 | 35 min |
| 3 | [exercise-03-number-of-provinces.py](./exercise-03-number-of-provinces.py) | Union-Find (path compression + union by rank) | 547 | 20 min |

Each `.py` file is **runnable as a script** — it ships with a self-test block at the bottom that runs a battery of asserts. Implement the function bodies; running the file should print `All cases passed.` once your implementation is correct.

The solutions are in [`SOLUTIONS.md`](./SOLUTIONS.md). **Attempt each exercise on your own first.** Reading the solution before drafting your own forfeits the recognition rep, which is what Phase 2 is grading.

## Order of attack

1. **Exercise 1 first** — Network Delay Time is the cleanest heap-Dijkstra rep and the warm-up for the rest of the week. Aim for 25 minutes including the UMPIRE write-up.
2. **Exercise 3 next** — Number of Provinces is the cleanest DSU rep. Aim for 20 minutes. Doing it second cements the Lecture-3 template before you tackle the harder Bellman-Ford exercise.
3. **Exercise 2 last** — Cheapest Flights with the hop constraint is the trickiest of the three, particularly the snapshot bug from Lecture 2 §2. Aim for 35 minutes; leave the slack for the snapshot debugging.

If time runs out, prioritize 1 and 3. The Bellman-Ford rep can be picked up Thursday during the challenge ramp.

## Acceptance

Each exercise is complete when:

- The `.py` file's self-tests pass (`python3 exercise-NN-*.py` prints `All cases passed.`).
- A UMPIRE write-up is committed under `umpire-writeups/c2-week-10/exercises/`.
- The Match section of the write-up names the pattern and rejects at least one alternative algorithm with reason.
