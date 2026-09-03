# Week 14 — Homework

Six problems, all original, all with a runnable worked answer beside this page.
Allow about four and a half hours. Do each with the lectures closed; open the
worked answer only after your own version runs, or after fifteen minutes stuck
on one step.

Mock #3 is on Friday, so this set is deliberately shorter and more mechanical
than most weeks. The point is recognition speed, not depth.

| # | Problem | Sub-shape | Est. time |
|---|---------|-----------|----------:|
| 1 | [The Triple-Logged Fault](#problem-1--the-triple-logged-fault) | When the XOR fold stops working, and what replaces it | 45 min |
| 2 | [The Lamp Distance](#problem-2--the-lamp-distance) | Popcount, and the one line that turns it into a distance | 35 min |
| 3 | [The Reversed Loom](#problem-3--the-reversed-loom) | Bit layout — the walk and the fold | 45 min |
| 4 | [The Common Prefix Range](#problem-4--the-common-prefix-range) | A structural observation that replaces a loop | 45 min |
| 5 | [The Missing Ticket](#problem-5--the-missing-ticket) | Two right answers, and the constraint that separates them | 30 min |
| 6 | [The Paired Ribbon Swap](#problem-6--the-paired-ribbon-swap) | Two masks, two shifts, every pair at once | 40 min |

Every worked answer runs on its own with no arguments and no packages, and ends
by printing `All checks passed.` Run one like this:

```bash
python problem-01-triple-logged-fault-solution.py
```

---

## Problem 1 — The Triple-Logged Fault

**The brief.** A relay tester writes every fault code **three** times. One code
in this log appears only once, because an engineer wrote it in by hand. Find it,
in linear time and constant space.

**The data.** Ten entries: three codes logged three times each, plus `0x0051`.

**Constraints.** Constant space, which rules out a counter. Zero can be the lone
code.

**Answer.** The XOR fold from
[Exercise 1](../exercises/exercise-01-relay-fold.md) **does not work**, and being
clear about why is half the problem: XOR cancels in *pairs*, so three copies
leave one behind, and folding the whole log gives you the XOR of every distinct
code.

What works is counting per **bit position** rather than per code. Every bit of a
tripled code contributes three to that position's total, and three divides by
three. So the positions whose totals are **not** divisible by three are exactly
where the lone code has a bit. Reassemble those bits.

That generalises: for codes appearing `k` times, count per position and take the
total mod `k`. The XOR fold is the `k = 2` case of the same idea, done faster.

The file ships the fold so you can watch it fail — on this log it returns
`0x3481`, which is the XOR of the distinct codes and not anybody's answer.

**Signatures.** `lone_fault(codes, repeats=3)`, `position_totals(codes)`,
`lone_fault_by_folding(codes)`.

**Watch for.** Reaching for the fold because it worked last time. Assuming a
non-zero result means success. The per-position count is `O(n × width)`, which is
still linear in the log — say so rather than calling it `O(n)` and hoping.

**Worked answer.** [`problem-01-triple-logged-fault-solution.py`](./problem-01-triple-logged-fault-solution.py)

---

## Problem 2 — The Lamp Distance

**The brief.** Two indicator panels are supposed to show the same register. When
they disagree, report **in how many lamp positions** — not whether, but how far
apart.

**The data.** Five pairs of readings, from identical to completely opposite.

**Constraints.** Negative registers are refused, because a negative Python
integer has no finite binary width and the counting loop would not terminate.

**Answer.** XOR joins the two halves of this problem in one line. `a ^ b` lights
a bit exactly where the two registers disagree, so **the distance is the lamp
count of the XOR**. Once that sentence is written down there is no second
algorithm to write.

The counting itself is `n &= n - 1`, which clears the lowest lit lamp and
nothing else — so the loop turns once per **lit** lamp rather than once per
position. The file counts turns both ways: a register with two lamps lit costs 2
turns against 16 tested.

**Signatures.** `lamps_lit(value)`, `lamps_lit_by_position(value)`,
`lamp_distance(first, second)`, `worst_pair(readings)`.

**Watch for.** Comparing the registers position by position, which is correct and
misses the whole point. `n &= n - 1` on a negative value never terminates. The
distance obeys the triangle inequality, which is worth asserting because it is
what makes "distance" the right word.

**Worked answer.** [`problem-02-lamp-distance-solution.py`](./problem-02-lamp-distance-solution.py)

---

## Problem 3 — The Reversed Loom

**The brief.** A ribbon loom was made up back to front — the sensor's lowest line
reaches the display's highest lamp, and so on. Every reading arrives with its
bits reversed. Reverse them back.

**The data.** Seven readings, including two that are unchanged by the fault.

**Constraints.** Sixteen bits, and the register is unsigned.

**Answer.** Two ways, and both are worth writing.

The **walk**: take bits off the bottom of the reading and push them onto the
bottom of the answer, sixteen times. The answer grows upwards while the reading
shrinks downwards, and that is what performs the reversal. This is the answer to
give at a panel.

The **fold**: swap halves, then quarters, then eighths, down to single bits. Four
masked steps instead of sixteen, and the same four lines would be five for a
32-bit register. This is the answer to *mention*.

**Signatures.** `unloom(value)`, `unloom_by_folding(value)`,
`unloom_steps(value)`, `symmetric(value)`.

**Watch for.** Building the answer by shifting *right* — the direction is the
whole trick. Testing on symmetric readings only: `1100000000000011` is unchanged
by the fault, so it proves nothing. The strongest check needs no known-good
answer at all: **reversing twice gives back the original**, on every value.

**Worked answer.** [`problem-03-reversed-loom-solution.py`](./problem-03-reversed-loom-solution.py)

---

## Problem 4 — The Common Prefix Range

**The brief.** A meter runs through every count from `low` to `high`. A latching
board ANDs them all together. Report what is left — **without** looping through
the range, which can be the whole 16-bit space.

**The data.** Eight ranges, from a single count to the entire register space.

**Constraints.** `low` above `high` is refused rather than silently swapped.

**Answer.** One structural observation replaces the loop: **the AND of a range is
the common high-bit prefix of its two ends, with every lower bit zeroed.**

Why: take any bit position below the point where `low` and `high` first differ.
Somewhere inside the range that bit flips to 0 — it must, because the range
crosses a boundary at that position — and once a column holds a zero, the AND of
that column is zero. Above the first difference, both ends agree and so does
everything between them.

So: shift both ends right until they are equal, then shift back left by the same
count. On the whole 16-bit space that is 16 operations against 65,536.

`5 to 7` latches **4**: 101, 110, 111 agree on the 4 and disagree below it.

**Signatures.** `check_range(low, high)`, `latched(low, high)`,
`latched_by_looping(low, high)`, `common_prefix(low, high)`.

**Watch for.** Looping "just for small ranges", which is the habit the problem
exists to break. An off-by-one in the shift count — the check that catches it is
the sweep over every small range, not the eight in the data. The answer's low
bits must be exactly the ones the shifting cleared, which is a property worth
asserting.

**Worked answer.** [`problem-04-common-prefix-range-solution.py`](./problem-04-common-prefix-range-solution.py)

---

## Problem 5 — The Missing Ticket

**The brief.** A cloakroom issues tickets 0 to n. Every ticket but one comes
back. Find the missing number.

**The data.** Nine returns from ten tickets.

**Constraints.** A ticket returned twice, or one never issued, is refused — the
arithmetic would otherwise produce a confident number that means nothing.

**Answer.** Two right answers, and the interesting part is what separates them.

The **sum**: add 0 to n with the closed form, subtract what came back. One line —
and it builds a number as large as the whole range, which on a fixed-width
register can overflow.

The **fold**: XOR every returned ticket *and* every number from 0 to n together.
Each returned ticket cancels against its own position in the range, and what
survives had nothing to cancel against. Nothing ever grows.

**Python's integers do not overflow, so here both are safe and the sum is
simpler.** The fold is the answer that stays safe when the register is 32 bits
wide. Being able to say *which constraint* makes the difference is the thing
being drilled — "use XOR because it is clever" is not the answer.

**Signatures.** `check_returns(returned)`, `missing_by_folding(returned)`,
`missing_by_summing(returned)`, `fold_trail(returned)`.

**Watch for.** Bounding the range loop at `len(returned)` rather than
`len(returned) + 1` — it works whenever the missing ticket is not the last one.
The missing ticket can be either end. No returns at all means ticket 0 is
missing, which is a real case.

**Worked answer.** [`problem-05-missing-ticket-solution.py`](./problem-05-missing-ticket-solution.py)

---

## Problem 6 — The Paired Ribbon Swap

**The brief.** A ribbon cable was crimped with each **pair** of lines swapped —
0 with 1, 2 with 3, and so on. Put them back.

**The data.** Seven registers, including three the fault does not change at all.

**Constraints.** Sixteen bits, unsigned.

**Answer.** Two masks and two shifts, done at once:

```text
0x5555  0101...0101  keeps the even lines, shifted up one
0xAAAA  1010...1010  keeps the odd lines, shifted down one
                     OR the two together
```

A loop over pairs is correct and is the answer to write first. The masked version
does every pair at once in constant time regardless of register width — and it is
the same shape as Problem 3's folding reversal, which is not a coincidence and is
worth a sentence in the write-up.

**Signatures.** `uncrimp(value)`, `uncrimp_by_looping(value)`,
`crossed_pairs(value)`, `unharmed(value)`.

**Watch for.** The two masks the wrong way round, which produces a plausible
answer on symmetric data. Testing with all-zeroes or all-ones — the fault leaves
them **unchanged**, so they are the worst possible readings to test a ribbon
with, and `unharmed` exists to name them.

Two properties need no known-good answer and are worth more than any example:
swapping twice returns the original, and the swap never changes how many lines
are live.

**Worked answer.** [`problem-06-paired-ribbon-swap-solution.py`](./problem-06-paired-ribbon-swap-solution.py)

---

## Rubric (5 axes, 4 points each)

| Axis | What "great" looks like |
|------|--------------------------|
| Frame the problem | The memo names the operation and what it does to a single bit column, before any code. |
| Reason about options | The obvious answer named first, then the bit answer, with the constraint that makes the second worth having — width, space, or the size of the range. |
| Assemble the solution | Masks named as constants rather than written inline; every width assumption stated; type hints throughout. |
| Measure it | A property that needs no known-good answer — reversing twice, swapping twice, agreeing with a slow version across a sweep — not six hand-picked examples. |
| Evaluate the cost | Time, space, best/average/worst, the trade-off and the improvement, in the register's own width rather than abstract n. |

Twenty points per problem, 120 for the set. Score yourself honestly; the number
is only useful if it is true.

---

## How to submit

Commit your write-ups under `frame-writeups/c2-week-14/homework/`, one file per
problem:

```
frame-writeups/c2-week-14/homework/
├── problem-1-triple-logged-fault.md
├── problem-2-lamp-distance.md
├── problem-3-reversed-loom.md
├── problem-4-common-prefix-range.md
├── problem-5-missing-ticket.md
└── problem-6-paired-ribbon-swap.md
```

Each file is 100–200 lines: the five FRAME sections plus a five-line memo at the
top. The code is part of the Assemble section, not a separate file.

When the set is done, push and move on to the
[mini-project](../mini-project/README.md) — and to Mock #3 on Friday.

---

## Time budget

| Problem | Solve | Write-up | Total |
|---------|------:|---------:|------:|
| 1 — Triple-Logged Fault | 30 min | 15 min | 45 min |
| 2 — Lamp Distance | 20 min | 15 min | 35 min |
| 3 — Reversed Loom | 30 min | 15 min | 45 min |
| 4 — Common Prefix Range | 30 min | 15 min | 45 min |
| 5 — Missing Ticket | 15 min | 15 min | 30 min |
| 6 — Paired Ribbon Swap | 25 min | 15 min | 40 min |

About four hours. Problems 1 and 5 are the two that matter most for Mock #3, and
for the same reason: each has an answer that *nearly* works, and the mark is for
knowing which constraint rules it out.
