# Week 8 — Challenges

Two challenges. Do at least the first; the second is a recommended stretch.

| # | Challenge | Sub-shape | Difficulty | Target time |
|---|-----------|-----------|------------|------------:|
| 1 | [The Hut Roll Call](./challenge-01-hut-roll-call-stitch.md) | k-way merge, lazily — the merge as a generator | Medium-Hard | 70 min |
| 2 | [The Dye Vat Rotation](./challenge-02-dye-vat-rotation.md) | Greedy scheduling with two heaps and a cooldown | Medium-Hard | 75 min |

Challenge 1 is mandatory. It is the structural pair to the bounded top-k heap
from Exercise 2 — there the heap's *size* was the argument, here it is *how much
of the input you read at all*. Challenge 2 is optional and recommended; it is the
scheduler shape, where the greedy rule is easy to feel and hard to defend, which
is exactly the kind of thing a mock asks you to defend.

Both have a runnable worked solution beside the page:

```bash
python challenge-01-hut-roll-call-stitch.py
```

Each challenge page contains:

- The brief, with the domain rule that is not a convention.
- The requirements and the constraints, including the alternative to reject.
- A real captured run, so the expected output is something you can check against
  rather than something you have to trust.
- The full solution, the bugs it is built to prevent, and an acceptance
  checklist.

The challenges differ from the exercises in two ways:

1. **You design the shape.** The function names are given; the data structures
   inside them are yours to choose and yours to defend in the write-up.
2. **Longer target time.** Seventy minutes against thirty. The reasoning step is
   harder, there is more than one valid path, and there is more code.

If a challenge takes more than 90 minutes, read the constraints again — the
answer to whatever has you stuck is usually stated there in one line. If it still
takes more than 120, read the solution, then re-attempt it cold the next day. The
point is the repetition, not the suffering.
