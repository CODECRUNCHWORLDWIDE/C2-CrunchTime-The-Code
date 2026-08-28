# Week 8 — Exercises

Three exercises. Each is FRAME-narrated, recorded, and graded against the test cases in the file itself. Worked solutions live in [`SOLUTIONS.md`](./SOLUTIONS.md) — consult only after attempting each exercise.

| # | Exercise | Pattern | Difficulty | Target solve time |
|---|----------|---------|------------|------------------:|
| 1 | [Kth Largest Element in an Array](./exercise-01-kth-largest.py) (LC 215) | Size-k min-heap; top-k template | Easy/Medium | 20 min |
| 2 | [K Closest Points to Origin](./exercise-02-k-closest-points.py) (LC 973) | Size-k max-heap (negated); heap-of-tuples | Medium | 25 min |
| 3 | [Find Median from Data Stream](./exercise-03-median-from-stream.py) (LC 295) | Two-heap pattern; balance invariant | Hard | 30 min |

Do them in order. Exercise 1 cements the size-k min-heap template on plain integers. Exercise 2 forces you to write the heap-of-tuples idiom with a distance key and a max-heap-by-negation. Exercise 3 is the canonical Phase-2 two-heap problem; expect a variant on Mock #2.

Each starter file contains:

- The problem statement
- The required function signature with type hints
- An empty body marked `# TODO`
- A self-test block at the bottom
- A FRAME checklist

Run a single exercise:

```bash
python3 exercises/exercise-01-kth-largest.py
```

Or run all under `pytest` if you prefer that harness:

```bash
pytest exercises/ -v
```

(Both forms work — the test block uses bare `assert` so plain `python3` execution is fine.)

## A note on what is being graded

Phase 1 graded you mostly on *correctness*. Phase 2 adds the *defense* axis: for every heap exercise, your write-up must state which template you used (size-k / k-closest / two-heap / k-way merge / lazy deletion), why, and what the failure mode of the *other* template would have been. The recording catches whether you say it; the write-up catches whether you can write it.

For Week 8 specifically, the defense includes:

- **Why a heap and not `sorted(...)`.** State the `O(n log k)` vs `O(n log n)` discriminator out loud.
- **Why a min-heap (not max) for top-k largest.** State the eviction-bar framing: "the heap holds the k largest; the min of the heap is the bar for new candidates."
- **The tiebreaker rule** when using heap-of-tuples with non-comparable payloads.

Defense is the difference between "the code works" and "the code is robust." Interviewers test for the latter. Drill on the latter.

---

After all three exercises pass, move on to [the challenge](../challenges/challenge-01-merge-k-sorted-lists.md) — Merge k Sorted Lists, the canonical k-way-merge application of the week.
