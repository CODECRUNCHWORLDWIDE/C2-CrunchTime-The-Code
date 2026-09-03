# Week 14 — Pattern-Recognition Quiz

Ten short prompts. **Do not solve them.** For each, classify it as one of:

- **XOR-fold** — reduce by `^`; pairs cancel.
- **bitmask-subset-enumeration** — represent a subset as an `n`-bit integer; loop over `range(1 << n)`.
- **bit-DP** — build `dp[i]` from a strictly smaller subproblem in `O(1)`.
- **binary-trie** — insert numbers MSB-first into a `0`/`1` trie; greedy bit walk.
- **NOT-a-bit-problem** — the natural tool is something else (hash map, two-pointer, sort, etc.).

One-line justification per answer. Lectures closed. Time yourself — 45 seconds per question.

Answer key at the bottom.

---

**Q1.** "Given an array where every element appears twice except one, find the element that appears once, using `O(1)` extra space."

**Q2.** "Given `n`, return an array where the `i`-th entry is the number of set bits in `i`, for all `i` from `0` to `n`, in `O(n)` time."

**Q3.** "Given an array of distinct integers (`len <= 16`), return all possible subsets."

**Q4.** "Given an array of integers, return the maximum value of `nums[i] ^ nums[j]` over all pairs."

**Q5.** "Given an array of integers `nums`, return `True` if any value appears at least twice."

**Q6.** "Given `n` distinct numbers taken from the range `[0, n]`, find the one number that is missing, in `O(1)` space."

**Q7.** "Given `12` cities and a distance matrix, find the shortest route that visits every city exactly once and returns to the start."

**Q8.** "Given two integers, return their sum without using the `+` or `-` operators."

**Q9.** "Given a list of words, build a structure supporting `insert(word)` and `starts_with(prefix)` queries over lowercase letters."

**Q10.** "Given an array, find the two elements that each appear exactly once while every other element appears exactly twice, using `O(1)` space."

---

## Answer key

<details>
<summary>Click after attempting all ten</summary>

1. **XOR-fold (the relay fold.** "Twice except one" + "`O(1)` space" is the textbook XOR-fold signal. Reduce by `^`; pairs cancel via `a ^ a == 0`. Exercise 1 exactly.

2. **bit-DP (the set-bit tally.** "Build entry `i` in `O(n)` total" forces the recurrence `dp[i] = dp[i >> 1] + (i & 1)` — each entry from a strictly smaller one in `O(1)`. The naive per-element popcount is `O(n log n)`. Exercise 2 exactly.

3. **bitmask-subset-enumeration (the glaze sample set.** "All subsets" + small `n` (`16`, so `2**16 = 65536` masks) is the enumeration signal. Loop `mask` over `range(1 << n)`; bit `i` means item `i` is included. Lecture 2 §2.

4. **binary-trie (the pairing register,).** "Maximize the XOR over all pairs" with the `O(n**2)` brute force too slow → insert MSB-first into a binary trie, greedy opposite-bit walk, `O(n · 32)`. Exercise 3 — the bridge problem.

5. **NOT-a-bit-problem.** "Any value appears twice" is a duplicate-detection problem; the natural tool is a `set` (add-and-check) or sort, `O(n)` time / `O(n)` space. There is no XOR cancellation to exploit because elements can appear *more* than twice and you only need a boolean. Negative-space discriminator — do not force a bit trick here.

6. **XOR-fold (the missing ticket.** XOR all indices `0..n` with all values; every present value cancels its index, leaving the missing number. The Gauss-sum `n(n+1)/2 - sum(nums)` is the equally-valid alternative; name both. Lecture 1 §8.

7. **bit-DP — specifically bitmask DP (Travelling Salesman).** Small `n` (`12`) + "visit every city exactly once" → state is the visited *subset* (a bitmask) plus the current city; `dp[mask][last]`. This is recognition-grade: name it, state `O(2**n · n**2)`, and be honest that the full implementation is a stretch, not an interview-cold expectation. Lecture 2 §4.

8. **XOR-adjacent / bit-arithmetic (the ledger adder.** Not a fold, but it lives in the bit family: `a ^ b` is the sum-without-carry, `(a & b) << 1` is the carry; iterate with a 32-bit mask. Closest bucket is "bit problem" — specifically bit-arithmetic, not any of the four standard sub-shapes. Challenge 2. (If you must pick one of the four labels, none fits cleanly — that recognition is itself the point: it is a bit problem but its own shape.)

9. **binary-trie? No — a *character* trie (NOT-a-bit-problem, in the bit sense).** This is the Week 9 dict-of-dict trie over the lowercase alphabet — `insert` / `starts_with`. It is a *trie*, but not a *binary* trie and not a bit-manipulation problem. The discriminator: a binary trie stores the bits of integers (alphabet `{0, 1}`); a character trie stores letters. Recognizing that distinction is the trie-review payoff of the week.

10. **XOR-fold with a twist (the odd tally.** A single fold gives `a ^ b`; isolate any differing bit with `a ^ b` & `-(a ^ b)`, partition the array on that bit, and fold each side. Still the XOR-fold family — the twist is the partition step. Lecture 1 §9.

</details>

---

## How to score

| Score | Meaning |
|------:|---------|
| 9–10 | Bit-pattern recognition is interview-ready, including the negative-space rejections (Q5, Q9). Move on to Mock #3. |
| 7–8 | Good — re-read [Lecture 1 §6–§9](./lecture-notes/01-bit-manipulation-fundamentals-and-xor.md) and [Lecture 2 §4](./lecture-notes/02-bitmasks-and-subset-enumeration-and-bit-dp.md) for the sub-shapes you missed. Most learners miss Q5 (duplicate, not a bit problem) or Q9 (character trie, not binary) first time; that is normal. |
| 5–6 | Redo Exercises 1 and 3 with stricter Research constraints sections. The XOR-fold / binary-trie distinction needs more reps before Mock #3. |
| <5 | The recognition is not yet automatic. Re-read all three lectures, re-do all three exercises with the sub-shape stated aloud, then retake the quiz. |

This quiz is about **fluency**, not difficulty. The discriminating questions are the negative-space ones: **Q5** (duplicate detection is a `set`, not a bit trick), **Q7** (recognizing bitmask DP *and* being honest it is recognition-grade), and **Q9** (a *character* trie is not a *binary* trie — the bit family's bridge structure is specifically the binary one). Recognizing the right tool — *and the wrong ones* — is the senior-level skill being measured.

When done, the [homework](./homework/README.md) is next.
