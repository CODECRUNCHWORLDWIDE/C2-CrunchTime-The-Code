# Week 3 — Pattern-Recognition Quiz

Ten short prompts. **Do not solve them.** For each, decide whether it is sliding window or not — and if it is, name the sub-shape: fixed-size, variable shape A ("longest"), variable shape B ("shortest"), or variable shape C ("count"). One-line justification per answer. Lectures closed. Time yourself — 30 seconds per question is the target.

Four of the ten are *not* sliding window. Recognizing those is worth as much as recognizing the six that are; a candidate who reaches for a window on every contiguous-sounding prompt is pattern-matching on vocabulary, not on structure.


---

**Q1.** A wind farm records the megawatt-hours generated in each ten-minute interval, in chronological order. Given the log and a block size `k`, return the largest total generation over any `k` consecutive intervals.

<details>
<summary>Answer</summary>

**Sliding window — fixed-size.** `k` arrives as input, so the window's size is settled before the loop starts. Auxiliary state: one running integer, updated as `total += log[right] - log[right - k]`. `O(n)` time, `O(1)` space. [Exercise 1](exercises/exercise-01-staffing-block.md) is this shape — with the harder contract of returning the *position* and defining a tie-break.

</details>

**Q2.** A rack of servers is logged bottom to top with each unit's power draw in watts, every figure positive. Given a circuit limit `c`, return how many contiguous groups of one or more units draw at most `c` watts in total.

<details>
<summary>Answer</summary>

**Sliding window — variable, shape C (count).** "How many contiguous groups" is the count signal. At each `right`, after shrinking until the total is back within the limit, add `right - left + 1` — the number of valid groups ending at `right`. The shortcut is only legal because the invariant is monotone under shrinking, which is what "every figure positive" buys you. `O(n)` time, `O(1)` space. This is the shape of the [mini-project's Problem 5](mini-project/README.md).

</details>

**Q3.** A cyclist's ride is logged as metres climbed in each minute, all figures non-negative. Given a climb target, return the fewest consecutive minutes in which the rider gains at least that many metres.

<details>
<summary>Answer</summary>

**Sliding window — variable, shape B (shortest).** Contiguous plus "fewest" is shape B: expand until the property holds, shrink *while* it still holds, record inside the shrink. Non-negativity is load-bearing — it is what makes the shrink monotone. `O(n)` time, `O(1)` space. [Exercise 4](exercises/exercise-04-shortest-catchment.md) is this shape.

</details>

**Q4.** A supplier's price list is sorted ascending. Given a budget, return the positions of the two prices that sum to exactly that budget.

<details>
<summary>Answer</summary>

**NOT sliding window — two-pointer, converging.** Sorted input plus a pair summing to a target is Week 1's pattern. The two indices move *toward each other* and do not define a region whose contents the algorithm reasons about. Both patterns use two indices; the geometry of motion is the discriminator. `O(n)` time. If the list were *unsorted*, it would be Week 2's hash-map complement lookup instead — and still not a window.

</details>

**Q5.** A bus route is logged stop by stop with the fare zone each stop belongs to. Given a pass valid for `k` fare zones, return the length of the longest run of consecutive stops the pass covers.

<details>
<summary>Answer</summary>

**Sliding window — variable, shape A (longest, at-most-K distinct).** The general at-most-K-distinct template. Invariant: `len(counts) <= k`. Auxiliary state: a frequency table with keys deleted the instant their count hits zero. `O(n)` time, `O(k)` space. [Exercise 5](exercises/exercise-05-cold-chain-load.md) is this shape; [Exercise 2](exercises/exercise-02-longest-clean-run.md) is the `k = 1`-flavoured special case where the invariant is plain distinctness.

</details>

**Q6.** A ledger records the day's net profit or loss for each trading day; figures may be negative. Given an amount `t`, return how many contiguous ranges of days net exactly `t`.

<details>
<summary>Answer</summary>

**NOT sliding window — prefix sums plus a hash map.** This is the classic "looks like a window but isn't." The negatives kill the monotone-shrink guarantee: dropping a leftmost loss *raises* the running total, so the window can never conclude anything from the total falling below the target. Count prefix sums instead and look up `prefix - t` in a frequency map. `O(n)` time, `O(n)` space. This is the Week 2 challenge shape.

</details>

**Q7.** A pharmacy's dispensing log lists one drug code per dispense, in order. Given a prescription — a list of drug codes, with repeats meaning "this many" — return every position at which the next `len(prescription)` dispenses are exactly that prescription in some order.

<details>
<summary>Answer</summary>

**Sliding window — fixed-size with a frequency invariant.** The window size is `len(prescription)` — derived from an input rather than handed to you, but still fixed before the loop. Invariant: the window's frequency table *equals* the prescription's. The key discipline is deleting a key when its count reaches zero, since `{"A": 1, "B": 0}` does not compare equal to `{"A": 1}`. `O(n)` time. [Exercise 3](exercises/exercise-03-rota-window.md) is this window returning a count; the [mini-project's Problem 3](mini-project/README.md) is the same window returning positions.

</details>

**Q8.** A sequencing run produces a string of DNA bases. Return the longest contiguous stretch of the read that is identical when reversed.

<details>
<summary>Answer</summary>

**NOT sliding window — expand-around-centre, or dynamic programming.** A palindrome has a *centre*, not a monotone window: the property is not maintained incrementally as `left` and `right` advance in the same direction, so neither index can be made to move forward-only. Standard approaches are `O(n²)` expand-around-centre or `O(n)` Manacher's, which is out of scope for C2. Revisited in Week 11.

</details>

**Q9.** A parts conveyor feeds an assembly cell, logging each component's part code. Given a bill of materials, return the shortest contiguous stretch of conveyor that contains the whole bill, counting duplicates.

<details>
<summary>Answer</summary>

**Sliding window — variable, shape B, with a frequency invariant.** This is [Challenge 1 — The Shortest Kit Span](challenges/challenge-01-shortest-kit-span.md). The auxiliary state is a frequency table for the bill, a frequency table for the window, and a **matched count**: an integer holding how many distinct part codes are currently satisfied. Comparing the two tables on every shrink step also works and is asymptotically worse. `O(n + m)` time.

</details>

**Q10.** A market data feed reports one trade price per tick. Given a window size `k`, return the highest price within each window of `k` consecutive ticks.

---

<details>
<summary>Answer</summary>

**Sliding window — fixed-size, with a monotonic deque for the maximum.** The window part is this week; the max-maintenance trick is Week 9. Calling `max(window)` per slide is `O(k)` per step and `O(n·k)` overall, which defeats the purpose. An acceptable Week-3 answer: *"fixed-size sliding window; maintaining the max in `O(1)` needs a monotonic deque, which I will learn properly in Week 9."* Naming the gap is better than bluffing past it.


---

</details>

## How to score

| Score | Meaning |
|------:|---------|
| 9–10 | Sliding-window pattern recognition is interview-ready. Move on. |
| 7–8 | Good — re-read [Lecture 1 §8 and §9](lecture-notes/01-the-sliding-window-pattern.md) for the ones you missed, especially Q4, Q6 and Q8, which are the negative-space questions. |
| 5–6 | Redo Drills 2, 4 and 5 with stricter Research constraints sections — the 30-second memo — before Week 4. |
| <5 | The pattern recognition is not yet automatic. Re-read both lectures and redo all five drills with the recorder running. |

If you missed **Q2** specifically, that is a signal rather than a failure: shape C is the one sub-shape the drills never make you write. Do the [mini-project's Problem 5](mini-project/README.md) before you attempt the homework's exactly-K problem.

This quiz is about **fluency**, not difficulty. Every question is something you should be able to answer in under 30 seconds once the patterns are in muscle memory.

When done, the [homework](homework/README.md) is next.
