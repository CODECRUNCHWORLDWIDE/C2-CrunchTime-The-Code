# Week 9 — Exercises

Three exercises. Each is UMPIRE-narrated, recorded, and graded against the test cases in the file itself. Worked solutions live in [`SOLUTIONS.md`](./SOLUTIONS.md) — consult only after attempting each exercise.

| # | Exercise | Pattern | Difficulty | Target solve time |
|---|----------|---------|------------|------------------:|
| 1 | [Implement Trie (Prefix Tree)](./exercise-01-implement-trie.py) (LC 208) | Dict-of-dict trie; `insert / search / starts_with` | Medium | 20 min |
| 2 | [Word Break](./exercise-02-word-break.py) (LC 139) | Trie + memoization composition | Medium | 35 min |
| 3 | [Longest Common Prefix](./exercise-03-longest-common-prefix.py) (LC 14) | Three solutions; vertical / horizontal / trie | Easy | 25 min |

Do them in order. Exercise 1 cements the dict-of-dict template on the canonical three operations. Exercise 2 forces you to compose the trie with memoization — the high-leverage pattern for the broader trie family (Word Break II, Concatenated Words, Word Squares). Exercise 3 is the recognition rep — three valid solutions, articulate why you would default to vertical scan but mention the trie.

Each starter file contains:

- The problem statement
- The required function signature with type hints
- An empty body marked `# TODO`
- A self-test block at the bottom
- A UMPIRE checklist

Run a single exercise:

```bash
python3 exercises/exercise-01-implement-trie.py
```

Or run all under `pytest` if you prefer that harness:

```bash
pytest exercises/ -v
```

(Both forms work — the test block uses bare `assert` so plain `python3` execution is fine.)

## A note on what is being graded

Phase 1 graded you mostly on *correctness*. Phase 2 adds the *defense* axis: for every trie exercise, your write-up must state which template you used (dict-of-dict / class / trie + memo / trie-on-grid), why, and what the failure mode of a *hash set* alternative would have been. The recording catches whether you say it; the write-up catches whether you can write it.

For Week 9 specifically, the defense includes:

- **Why a trie and not `set[str]`.** State the prefix-query discriminator out loud: "the hash set cannot answer prefix queries in less than `O(n L)`; the trie answers them in `O(P)`."
- **Why dict-of-dict over the `TrieNode` class** (or vice versa). State the cue: per-node state means class form; pure structure means dict form.
- **The `END` sentinel rule** when using the dict-of-dict form — what character you picked and why it cannot appear in the input.
- **For Exercise 3:** state which of the three solutions you would default to and why. The expected answer is "vertical scan for the one-shot LC 14 input; trie for the multi-query generalization."

Defense is the difference between "the code works" and "the code is robust." Interviewers test for the latter. Drill on the latter.

---

After all three exercises pass, move on to [the challenge](../challenges/challenge-01-word-search-ii.md) — Word Search II, the canonical trie-on-grid application of the week.
