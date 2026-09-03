# Week 5 — Pattern-Recognition Quiz

Ten short prompts. **Do not solve them.** For each, decide whether it is binary search or not — and if binary search, name the variant (classic / lower bound / upper bound / rotated / parametric / partition predicate). One-line justification per answer. Lectures closed. Time yourself — 45 seconds per question is the target (slightly longer than Phase 1 quizzes; parametric recognition is harder).


---

**Q1.** "A pharmacy stores its batch numbers in one ascending list with no repeats. Given a batch number, return the shelf position holding it, or `None` if the pharmacy does not stock it. `O(log n)` required."

<details>
<summary>Answer</summary>

**Binary search — variant 1 (classic, find any).** "Sorted sequence + exact target + `O(log n)`" is the canonical triple signal. Closed interval `[lo, hi]` with `lo <= hi`; return `mid` on a match, `None` after the loop. This is [Exercise 1](exercises/exercise-01-ladder-seat.md) with one difference worth noticing out loud: Exercise 1's ladder runs **descending**, so its shrink rules are the mirror of the ones this prompt needs. If you wrote Exercise 1's branches from memory here, you walked the wrong way.

</details>

**Q2.** "A feature film is cut into reels, in projection order, each with a running time in minutes. The reels are divided among exactly three projectionists, each taking a contiguous run of reels. Return the shortest possible value of the longest projectionist's shift."

<details>
<summary>Answer</summary>

**Binary search on the answer — parametric, "minimise the maximum."** Reframe: find the smallest `cap` such that `feasible(cap) = (the reels can be cut into at most three contiguous runs, each totalling at most cap)`. Interval `[max(reels), sum(reels)]`: the cap must hold the longest single reel, and one projectionist taking everything always works. Monotone because a larger cap never forces more runs. This is the shape of [Homework Problem 2 — The Relay Handoff](homework/README.md), with the projectionist count fixed at three instead of being an argument.

</details>

**Q3.** "Given a product SKU string, return the longest run of characters inside it that reads the same in both directions."

<details>
<summary>Answer</summary>

**NOT binary search — expand around centre, or DP.** No sorted structure, no monotone predicate on a bounded answer space. The pattern is expand-around-centre for `O(n²)`, or Manacher's algorithm for `O(n)`. Out of scope for Week 5; the point of the question is that you reject it in five seconds rather than hunting for a bisection that is not there.

</details>

**Q4.** "A parcel hub's scan log is non-decreasing by minute and repeats minutes heavily. For one given minute, return the half-open slice bounds of the run of scans that happened in it. `O(log n)` required."

<details>
<summary>Answer</summary>

**Binary search — variants 2 + 3 (lower bound applied twice).** "Sorted with duplicates" plus "give me the whole run" is the lower-bound pair: `start = lower_bound(minute)`, `end = lower_bound(minute + 1)`. Two `O(log n)` searches compose to `O(log n)`. This is [Exercise 2](exercises/exercise-02-scan-window.md). The tempting wrong answer is "find any occurrence, then walk outward" — that is `O(run length)`, and the runs in that log are hundreds of rows long.

</details>

**Q5.** "A pallet manifest holds `n + 1` bin numbers, every one of them in the range `1..n`, and exactly one bin number appears twice. Find that bin number in `O(1)` extra space, without reordering the manifest."

<details>
<summary>Answer</summary>

**NOT binary search** — despite the `O(1)`-space tell, which is there to bait you. The structural pattern is **fast/slow on a functional graph**, from Week 4: define `f(i) = manifest[i]`, and the repeated bin number is the entrance to the cycle. Floyd's, not bisection. The misdirection is genuine, though: there *is* a binary-search-on-the-answer solution here — count how many bin numbers are `<= k` and search for the boundary where that count first exceeds `k` — and it is `O(n log n)`, strictly worse than the `O(n)` cycle walk. Naming both and then choosing correctly is the full-credit answer.

</details>

**Q6.** "A turnstile's ring-buffer dump is a rotation of a strictly increasing sequence of reading ids. Given an id, return how many rows currently in the buffer are older than it, or `None` if the id is not in the buffer. `O(log n)` required."

<details>
<summary>Answer</summary>

**Binary search — rotated sequence, wrap point plus a logical view.** "Rotation of a sorted sequence + `O(log n)`" is the canonical signal. One search locates the wrap point by comparing `slots[mid]` against `slots[hi]`; a second search runs over the logical accessor `t → slots[(p + t) % n]`, and the logical index it lands on **is** the age. This is [Exercise 3](exercises/exercise-03-ring-buffer-probe.md). Note what the prompt asks for: an age, not a slot. A candidate who returns the physical index has recognised the pattern and misread the contract.

</details>

**Q7.** "A repaving crew works one road section per night, laying as much of that section as the rented paving train's nightly reach allows. Given the section lengths and a budget of nights, return the smallest nightly reach that finishes the road in time."

<details>
<summary>Answer</summary>

**Binary search on the answer — parametric, "minimise the threshold."** Reframe: find the smallest reach `w` such that `sum(ceil(section / w)) <= nights`. Interval `[1, max(sections)]`: at the top of that interval every section finishes in one night. Monotone because raising the reach never increases any section's night count. This is [Exercise 5](exercises/exercise-05-paving-reach.md), and it is one of the two discriminating questions on this quiz — the prompt never says "binary search," never says "`O(log n)`," and never shows you a sorted list.

</details>

**Q8.** "An ascending price list and a target total. Return every pair of positions `(i, j)` with `i < j` whose two prices sum to the target."

<details>
<summary>Answer</summary>

**NOT binary search — two-pointer converging** (Week 1), or a hash map if the list were unsorted (Week 2). Binary-searching for `target - prices[i]` at every `i` gives `O(n log n)`, strictly worse than the two-pointer's `O(n)` on a list that is already sorted. The second tell is the output shape: "return **every** pair" is an enumeration, and bisection returns boundaries, not enumerations.

</details>

**Q9.** "A freight rate card lists handling fees and linehaul fees, each already sorted ascending. Any handling fee may be paired with any linehaul fee. Return the `k`-th cheapest pairwise sum without materialising the ten billion sums."

<details>
<summary>Answer</summary>

**Binary search on values, with a counting predicate.** There is no sorted list of sums to index into — there are up to ten billion of them — but `count_at_most(v)` is non-decreasing in `v`, so the predicate `count_at_most(v) >= k` is monotone and the answer is the boundary. The count itself is an `O(n + m)` two-pointer sweep. This is [Exercise 4](exercises/exercise-04-quote-rank.md). The signal to train on: *the answer is a value in a bounded range, and counting things `<= v` is easy.*

</details>

**Q10.** "Two venues each hand you a sorted report of signed position deltas. Return the `k`-th smallest value of the two reports combined, in `O(log(min(m, n)))`."

---

<details>
<summary>Answer</summary>

**Binary search on a partition predicate.** "Two sorted sequences + a rank + `O(log(min(m, n)))`" is the partition signal. Do not search for a value; search for a **split**: choose how many entries come from the shorter report, and the count from the other follows. This is the week's [challenge](challenges/challenge-01-order-book-boundary.md). The asymptotic bound in the prompt is doing real work — it is what rejects the `O(m + n)` merge that would otherwise be the obvious answer.


---

</details>

## How to score

| Score | Meaning |
|------:|---------|
| 9-10 | Binary-search pattern recognition is interview-ready, including parametric and the negative-space rejections. Move on. |
| 7-8 | Good — re-read [Lecture 2 §6](lecture-notes/02-binary-search-on-the-answer.md) for the parametric questions you missed. Most learners miss one of Q2 or Q7; that is normal on the first pass. |
| 5-6 | Redo Drills 4 and 5 with stricter Research constraints sections. The parametric recognition needs more reps before Mock #2. |
| <5 | The pattern recognition is not yet automatic. Re-read both lectures, re-do all five drills with the four-element memo, then retake the quiz. |

This quiz is about **fluency**, not difficulty. The discriminating questions are **Q2 and Q7** — both parametric problems whose prompts never mention "binary search," "logarithmic," or a sorted list. Recognising them is the senior-level skill being measured.

The negative-space questions — **Q3, Q5, and Q8** — are also discriminators. Q5 in particular is a trap: the constraints look like binary search on the answer (`O(1)` space, no reordering), and a bisection solution does exist, but it is a factor of `log n` worse than the cycle walk. Knowing which pattern to *reject*, and being able to say why the rejected one is worse rather than merely different, is as important as knowing which to apply.

When done, the [homework](homework/README.md) is next.
