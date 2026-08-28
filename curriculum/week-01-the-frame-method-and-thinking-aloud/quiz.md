# Week 1 — Pattern-Recognition Quiz

Ten short prompts. **Do not solve them.** For each, name the pattern and a one-line justification. Lectures closed. Time yourself — 30 seconds per question is the target.

Every prompt is a story, not a spec. That is on purpose: in a real interview nobody says "this is a two-pointer problem," and the work of stripping a story down to its shape is the first half of **Assess options**. Read for the *structure* — is the input sorted, is there one sequence or two, does the answer want a pair, a span, or a rearrangement?

Answer key at the bottom.

---

**Q1.** "A hardware store's bin of bolts is arranged lightest to heaviest. A customer wants exactly two bolts whose combined mass hits a figure they've written down. Which two?"

**Q2.** "Museum accession codes are printed with dots every few characters so curators can read them aloud. Tell me whether a code reads identically from either end once the dots are ignored."

**Q3.** "The community darkroom takes bookings as start and end times. Tell me whether one photographer could keep every booking on today's list without ever being in two places at once."

**Q4.** "A tide gauge repeats its previous reading whenever the sensor freezes. Squeeze out those repeats, in the same buffer, and tell me how many readings you threw away."

**Q5.** "A mail-forwarding chain points each old address at a newer one. Tell me whether the chain ever loops back on itself."

**Q6.** "A courier's route log lists every stop made today, in order. Find the shortest unbroken run of stops that touches all four distribution hubs at least once."

**Q7.** "Two seismographs each recorded a time-ordered list of tremors. Produce a single time-ordered list of everything both machines saw."

**Q8.** "A co-op's disputed balance has to be explained by exactly three ledger entries adding up to it. List every distinct way that can be done."

**Q9.** "An anemometer logs a gust speed every second. For every rolling sixty-second window, report the strongest gust in that window."

**Q10.** "A support agent has a customer's charge history in the order the charges were made — not sorted. Find the two charges that sum to a disputed refund, and tell me where they sit in the history."

---

## Answer key

<details>
<summary>Click after attempting all ten</summary>

1. **Two-pointer (converging).** Sorted + pair + target sum — textbook. O(n), one pointer at each end, steer on the sum.
2. **Two-pointer (converging).** Pointers from each end, skip the separators, compare what's left. Watch the guards on the skip loops.
3. **(Out of scope this week — intervals.)** The *intervals* pattern, covered in Week 10. Acceptable Week-1 answer: "I'd sort by start time, then check whether any booking starts before the previous one ends." That's the right instinct.
4. **Two-pointer (same-direction).** Read pointer scans every reading; write pointer advances only when a reading survives. Note "in the same buffer" — that's the O(1)-space requirement in disguise. This is [Exercise 4](exercises/exercise-04-stuck-gauge.md).
5. **(Out of scope this week — fast/slow pointers.)** Week 4. Acceptable Week-1 answer: "Two pointers, one advancing twice as fast; if they ever meet, there's a loop."
6. **(Out of scope this week — sliding window.)** Week 3. *Not* two-pointer despite using two indices: the answer is the **span between** the indices, and the window grows and shrinks depending on whether all four hubs are currently covered.
7. **Two-pointer (two-input).** One pointer per log, emit the earlier timestamp each step. Ask what happens on a tie before writing the comparison.
8. **Pin + two-pointer (converging).** Sort, pin each entry in turn, converge over the remainder for the pair that completes it. O(n²). This is [Challenge 1](challenges/challenge-01-settlement-trio.md) — note that the target is an arbitrary figure, not zero.
9. **(Out of scope this week — sliding window with a monotonic deque.)** Weeks 3 and 9. Acceptable Week-1 answer: "A deque holding candidates in decreasing order keeps the window maximum available in O(1); each reading enters and leaves at most once."
10. **Hash map — *not* two-pointer.** Unsorted, and the positions in the original history are what's being asked for, so sorting would destroy the answer. Complement lookup in one pass. Covered in Week 2.

**If you missed 10 but got 1**, that is the single most valuable miss on this quiz — those two prompts describe nearly the same arithmetic and demand completely different algorithms. The discriminator is one word: *sorted*.

</details>

---

## How to score

| Score | Meaning |
|------:|---------|
| 9–10 | You can recognize a two-pointer problem at sight. Move on. |
| 7–8 | Good — re-read the cases you missed in [Lecture 3](lecture-notes/03-arrays-and-two-pointers.md). |
| 5–6 | Re-read Lecture 3 and re-do Exercises 1, 3, and 4 before Week 2. |
| <5 | The pattern recognition isn't yet automatic. Don't move to Week 2 yet — repeat the drills, re-record yourself. |

This quiz is **not** about solving the problems. It's about recognizing the pattern instantly. That speed is what survives interview pressure.

When done, the [homework](homework/README.md) is next.
