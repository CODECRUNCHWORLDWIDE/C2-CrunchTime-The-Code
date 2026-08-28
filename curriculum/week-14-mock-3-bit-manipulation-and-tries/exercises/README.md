# Week 14 — Exercises

Three exercises, one per bit sub-shape. Each is FRAME-narrated, recorded, and graded against the test cases in the file itself. Worked solutions live in [`SOLUTIONS.md`](./SOLUTIONS.md) — consult only after attempting each exercise.

| # | Exercise | Pattern | Difficulty | Target solve time |
|---|----------|---------|------------|------------------:|
| 1 | [Single Number](./exercise-01-single-number.py) (LC 136) | XOR fold | Easy | 15 min |
| 2 | [Counting Bits](./exercise-02-counting-bits.py) (LC 338) | Bit DP — `dp[i] = dp[i >> 1] + (i & 1)` | Easy/Medium | 20 min |
| 3 | [Maximum XOR of Two Numbers in an Array](./exercise-03-maximum-xor.py) (LC 421) | Binary trie (the bridge) | Medium | 40 min |

Do them in order. Exercise 1 cements the XOR fold and the four identities on the canonical problem. Exercise 2 forces the bit-DP recurrence — the recognition that an answer can be built from a strictly smaller subproblem in `O(1)`. Exercise 3 is the week's keystone: the binary trie that bridges bit manipulation to the Week 9 trie family, and the highest-yield single artifact of the week.

Each starter file contains:

- The full problem statement with constraints and examples (real LC numbers)
- The required function signature with type hints
- An empty body marked `# TODO`
- A FRAME checklist in the module docstring
- A self-test block at the bottom using bare `assert`

Run a single exercise:

```bash
python3 exercises/exercise-01-single-number.py
```

Or run all under `pytest` if you prefer that harness:

```bash
pytest exercises/ -v
```

(Both forms work — the test block uses bare `assert` so plain `python3` execution is fine. The starters target Python 3.11; Exercise 2's self-test cross-checks against `int.bit_count()`, which requires Python 3.10+.)

## A note on what is being graded

Phase 1 graded you mostly on *correctness*. By Phase 4, the axes are **Research constraints**, **the defense**, and **interview-readiness** — because this is a mock week. For every bit exercise, your write-up and your recording must:

- **Name the sub-shape out loud** — XOR fold / bitmask enumeration / bit DP / binary trie — within 30 seconds of reading the prompt.
- **Defend the choice over the obvious alternative.** For Exercise 1, the alternative is a hash map (`O(n)` space); state that the constant-space constraint rules it out. For Exercise 2, the alternative is a per-element popcount (`O(n log n)`); state that the recurrence makes it `O(n)`. For Exercise 3, the alternative is the `O(n**2)` brute force over all pairs; state that the binary trie drops it to `O(n · 32)`.
- **State the complexity bound before the interviewer asks.** This is the interview-readiness axis — in Mock #3 next, an unprompted complexity statement is a senior tell.

Defense is the difference between "the code works" and "the code is the *right* code, and I can prove it." Mock #3 grades the latter.

---

After all three exercises pass, move to [the challenges](../challenges/README.md) — the Mock #3 timed round, and the Sum of Two Integers (LC 371) full-FRAME write-up.
