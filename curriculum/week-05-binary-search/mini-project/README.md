# Mini-Project — Five Binary-Search Write-Ups (Including Two "Search on Answer" Variants)

> The week's deliverable: a single, compact portfolio artifact that demonstrates **boundary-defense fluency** across the five canonical binary-search shapes, plus a 30-second pattern-recognition memo per problem. The parametric-cadence memos on Problems 4 and 5 are the discriminating element — interviewers grade Research constraints harder than candidates expect, and parametric recognition is the senior-level marker.

**Estimated time:** 10 hours, split across Thursday-Saturday.

This mini-project is *content-heavy* rather than *infrastructure-heavy*. You will produce five FRAME write-ups, each anchored by a 30-second pattern-recognition memo at the top. The Research constraints memos are the artifact's signature element; the rest of each write-up is standard FRAME.

All five problems below are **new** — none of them is a drill in a costume. Every one changes the contract from the version your hands already know: a nearest-match instead of an exact match, a pair instead of an index, a coverage predicate instead of a packing predicate, a maximised minimum instead of a minimised maximum. That is deliberate. A write-up you can produce from memory teaches you nothing.

---

## Why this matters

Three reasons.

1. **Phase 2 is graded on Research constraints.** Phase 1 spent four weeks installing the FRAME habit; the Make step was the primary work. Phase 2 patterns are heavier and the Research constraints step matters more — the recognition cost is no longer "30 seconds to name the pattern" but "60 seconds to name the variant, defend the boundary, and (for parametric) prove monotonicity." This mini-project is the first one in C2 that grades the four-element parametric cadence as strictly as Make the solution.

2. **Binary search has more confusable variants than any earlier pattern.** Classic (variant 1), lower bound (variant 2), upper bound (variant 3), rotated, binary search on values, parametric on the answer — six recognized shapes, each with its own template. Five write-ups force you to articulate the differences out loud. By the fifth, the disambiguation is reflexive.

3. **The "search on answer" variants are interview-distinguishing.** Most candidates pass the classic binary-search test. Few recognize parametric search on a prompt that does not mention "binary search" or "log n." If you ship Week 5 with parametric in your hands, you are statistically distinguishable from the median candidate at the same level. This mini-project demands two such write-ups.

---

## What you ship

Six files: five problem write-ups plus a short overview.

```
frame-writeups/c2-week-05/mini-project/
├── README.md                              ← short overview + index
├── problem-01-frequency-slot.md           ← variant 1: closed interval, nearest match
├── problem-02-shift-start.md              ← rotated: locate the wrap point
├── problem-03-waitlist-cursor.md          ← variant 2: lower bound / insertion point
├── problem-04-sprinkler-reach.md          ← parametric: minimise a threshold
└── problem-05-delivery-zones.md           ← parametric: maximise the minimum
```

Each write-up is the full FRAME format from Week 1, **plus a leading 30-second pattern-recognition memo at the top** — and for problems 4 and 5, the four-element parametric cadence (reframe, interval, predicate, return).

Problems 1-3 share a *family* with Drills 1-3 but not a contract; you may lean on those write-ups for the boundary vocabulary, and you may not copy them. The mini-project rubric is stricter: it also demands an explicit comparison against another variant, which the drills do not.

---

## The 30-second pattern-recognition memo (the signature element)

At the top of every write-up, immediately after the title, place a single bordered block.

### For classic binary-search problems (Problems 1-3)

```markdown
> **30-second pattern-recognition memo:**
> This is a binary-search problem because [sorted-structure / target / log-n signal].
> The variant is [classic find-any / lower bound / upper bound / rotated / search on values].
> The boundary convention is [closed `[lo, hi]` with `<=` / half-open `[lo, hi)` with `<`].
> The shrink rules are: [one line each for the less-than and greater-than branches].
> The post-loop assertion is: [what `lo` represents when the loop exits].
> Why not [alternative]: [one sentence].
```

Six lines. Read aloud, ~25 seconds.

### For parametric problems (Problems 4-5)

```markdown
> **30-second pattern-recognition memo (parametric):**
> Reframe: find the [smallest / largest] `k` in [interval] such that [predicate].
> Interval: `lo = ...` because [one-line justification]; `hi = ...` because [one-line justification].
> Predicate: `feasible(k)` returns True iff [property]. Monotone in `k` because [one-line reason].
> Return: post-loop `lo` is the answer because [post-loop invariant].
> Why not [alternative]: [one sentence].
```

Six lines. Read aloud, ~30 seconds.

Example for Problem 1 (The Frequency Slot):

> **30-second pattern-recognition memo:**
> This is a binary-search problem because the channel table is sorted ascending and the scanner must answer one lookup per keypress in `O(log n)`.
> The variant is **lower bound**, used as scaffolding for a nearest-match: the insertion point tells me the only two candidates that can win.
> The boundary convention is half-open `[lo, hi)` with `while lo < hi`.
> The shrink rules are: `frequencies[mid] < wanted → lo = mid + 1`; otherwise `hi = mid`.
> The post-loop assertion is: `lo` is the first index whose frequency is `>= wanted`, so the nearest channel is `lo` or `lo - 1` and nothing else.
> Why not a linear scan over the table: `O(n)` per keypress on a table that is already sorted, when the order is free to use.

Example for Problem 4 (The Sprinkler Reach):

> **30-second pattern-recognition memo (parametric):**
> Reframe: find the smallest radius `r` in `[0, span]` such that every plant sits within `r` metres of some hydrant.
> Interval: `lo = 0` because a plant standing exactly on a hydrant needs no reach at all; `hi = max(abs(plants[0] - hydrants[0]), abs(plants[-1] - hydrants[0]))`, the distance from the farthest plant to the *first* hydrant — feasible by construction, because at that radius that one hydrant already waters everything, and computable in `O(1)` since both lists are sorted.
> Predicate: `feasible(r)` returns True iff every plant has a hydrant within `r`. Monotone because widening the radius never uncovers a plant that was already covered.
> Return: post-loop `lo` is the smallest radius satisfying the predicate — the cheapest sprinkler head that waters the whole row.
> Why not compute each plant's nearest hydrant directly and take the maximum: that is also correct and is `O(n + m)` with a two-pointer merge, which is *better*. Say so out loud, then solve it parametrically anyway because the rubric is the cadence — and note in Examine (cost) that recognising the cheaper direct solution is itself the senior move.

Five write-ups, five memos. By the fifth, the cadence is automatic.

---

## Per-problem rubric

Each write-up's grade comes from five axes:

| Axis | Weight | "Great" looks like |
|------|------:|--------------------|
| 30-second memo at the top | 30% | Six lines, all required elements named, hits cadence on read-aloud (≤30s) |
| Research constraints section (expanded body) | 25% | Explicit comparison against at least one other variant; explicit rejection of one wrong pattern (e.g., "not parametric because the predicate is not monotone" or "not classic because the sequence is unsorted") |
| Make the solution + Examine (verify) | 20% | Clean code; trace on at least two examples; one common bug called out and avoided |
| Examine (cost) (five-piece from W2) | 15% | Time / space / best-avg-worst / tradeoff / improvement, with the `O(log n)` or `O(n log M)` defense sentence |
| Cross-references | 10% | Each write-up links to the relevant lecture section and at least one *other* mini-project write-up |

A grade of "great" on all five write-ups is the bar.

---

## The five problems

### Problem 1 — The Frequency Slot

**Domain.** A handheld radio scanner stores its channel table as frequencies in kHz, **sorted ascending, all distinct**. The user dials a frequency; the scanner jumps to the closest channel it actually holds.

**Contract.**

```python
def nearest_channel(frequencies: list[int], wanted: int) -> int | None:
    """Return the index of the channel whose frequency is closest to `wanted`.
    On a tie, the LOWER frequency wins. Return None if the table is empty."""
```

**Constraints.**

- `0 <= len(frequencies) <= 500_000`. A full band plan. The scanner re-runs this on every turn of the dial, so `O(n)` per turn is the difference between a responsive knob and a laggy one — that is the bound that rejects the scan.
- `1 <= frequencies[i] <= 3_000_000`. Frequencies are positive, but `wanted` may fall **outside** the table on either side; both ends are legal input and are where the off-by-one lives.
- The table is strictly ascending, so no two channels share a frequency and the tie-break is always between two *different* channels.

**Examples.** Work with `frequencies = [881, 894, 902, 917, 940]`.

- `wanted = 917` → `3`. Exact hit.
- `wanted = 910` → `3`. `917` is 7 away, `902` is 8 away.
- `wanted = 909` → `2`. `902` is 7 away, `917` is 8 away. The mirror of the previous case, one kHz apart — this pair is what proves your comparison, not your loop.
- `wanted = 898` → `1`. **The tie.** `894` and `902` are both 4 away; the contract says the lower frequency wins. If you return `2` here, your search is right and your tie-break is missing.
- `wanted = 700` → `0`. Below the whole table. The insertion point is `0`, so there is no `lo - 1` candidate — guard it.
- `wanted = 1200` → `4`. Above the whole table. The insertion point is `len(frequencies)` — do not index there.
- `frequencies = [1000], wanted = 1` → `0`. Single channel.
- `frequencies = [], wanted = 900` → `None`. **The degenerate case.**

**Why included.** The textbook variant with one honest complication. Your memo must make the boundary convention explicit in one sentence, and your Research constraints section must explain why you reached for **lower bound** rather than classic find-any: an exact-match search returns nothing useful on a miss, and every input here that misses still has an answer.

**Stretch in your write-up:** compare against the closed-interval find-any template from [Exercise 1](../exercises/exercise-01-ladder-seat.md). Same family, different convention, and Exercise 1's array runs *descending*. Articulating why you chose half-open here and closed there is the **boundary-defense** skill the rubric grades.

### Problem 2 — The Shift Start

**Domain.** A night-shift roster records each worker's clock-in as **minutes past midnight**, in the order they arrived, so the sequence is **strictly increasing in arrival order**. The roster is stored in a fixed-size ring, and when the ring wraps the dump you receive is a **rotation** of the arrival order.

**Contract.**

```python
def shift_start(clock_ins: list[int]) -> tuple[int, int] | None:
    """clock_ins is a rotation of a strictly increasing list of clock-in minutes.
    Return (physical_index, minute) of the EARLIEST clock-in — the row where the
    shift actually began. Return None if the roster is empty."""
```

**Constraints.**

- `0 <= len(clock_ins) <= 1_000_000`. A month of rosters. `O(n)` would be fine once, but the payroll job runs it per roster per night; the bound plus the volume is what rejects `min()`.
- `0 <= clock_ins[i] <= 1_439`, **strictly increasing in arrival order**, so all values are distinct. Distinctness is what makes the discriminator sound; without it the wrap point is not even well defined, which is the case you meet in [Homework Problem 4](../homework/README.md).
- The dump may be **un-rotated** — the ring has not wrapped yet — and the algorithm must handle that without a "is it rotated?" branch.

**Examples.**

- `clock_ins = [1305, 1340, 1412, 22, 405, 640, 1150]` → `(3, 22)`. The shift began at 00:22, sitting in physical slot 3. Trace: `lo=0, hi=6, mid=3` — `22 > 1150`? No → `hi=3`. `lo=0, hi=3, mid=1` — `1340 > 22`? Yes → `lo=2`. `lo=2, hi=3, mid=2` — `1412 > 22`? Yes → `lo=3`. `lo == hi == 3`.
- `clock_ins = [22, 405, 640]` → `(0, 22)`. **The degenerate case:** not rotated at all. `p = 0` must fall out of the loop, not out of a special case.
- `clock_ins = [640, 22]` → `(1, 22)`. Two rows, wrapped. The smallest input that punishes reading the answer off slot 0.
- `clock_ins = [22, 640]` → `(0, 22)`. Two rows, not wrapped. The mirror.
- `clock_ins = [500]` → `(0, 500)`. One row: the loop never runs and `lo` is already the answer.
- `clock_ins = []` → `None`. Guard before you index.

**Why included.** The discriminator here is `clock_ins[mid]` against `clock_ins[hi]`, **not** against `clock_ins[lo]`. On an un-rotated dump, comparing against `lo` sends you right every time and lands on the last row instead of the first. Your memo must name the comparison and say why the other one fails.

**Stretch in your write-up:** compare against [Exercise 3](../exercises/exercise-03-ring-buffer-probe.md). Exercise 3 uses the wrap point as a *step* on the way to an age position; here the wrap point **is** the whole answer. Same search, different reason for running it — name the relationship in one sentence.

### Problem 3 — The Waitlist Cursor

**Domain.** A box office keeps the seat numbers it has already sold in one **ascending, duplicate-free** list. When a patron asks for a seat, the clerk needs to know two things at once: whether it is gone, and — if it is free — where it would slot into the list.

**Contract.**

```python
def seat_cursor(sold: list[int], wanted: int) -> tuple[int, bool]:
    """sold is ascending with no duplicates. Return (index, already_sold) where
    index is the position of `wanted` if present, otherwise the position at
    which it would be inserted to keep the list ascending. Never returns None."""
```

**Constraints.**

- `0 <= len(sold) <= 1_000_000`. A stadium season. The box office runs this per keystroke of the seat field.
- `1 <= sold[i] <= 2_000_000` and `1 <= wanted <= 2_000_000`. Seat numbers are positive, but `wanted` may sit before every sold seat or after all of them, and `index == len(sold)` is a **legal return** — it is the "append at the end" cursor. That is the value your absent-check must not index into.
- The list is strictly ascending. Duplicates are impossible because a seat cannot be sold twice, which is why one lower-bound search settles both halves of the answer.

**Examples.** Work with `sold = [4, 9, 12, 20, 33]`.

- `wanted = 12` → `(2, True)`. Present.
- `wanted = 13` → `(3, False)`. Absent; 13 slots between 12 and 20.
- `wanted = 4` → `(0, True)`. Present at the very front. `index = 0` is a real answer, not a failure code.
- `wanted = 33` → `(4, True)`. Present at the very back.
- `wanted = 1` → `(0, False)`. Before everything. Same index as the `wanted = 4` case, different flag — which is exactly why the flag exists.
- `wanted = 40` → `(5, False)`. **After everything.** `index == len(sold)`, and `sold[index]` would raise. Order your absent-check so the bounds test comes first.
- `sold = [], wanted = 7` → `(0, False)`. **The degenerate case.** The empty list needs no special branch: the loop never runs, `lo` is `0`, and the bounds test short-circuits the flag.

**Why included.** The cleanest exercise of the half-open convention, and the one place this week where the return type forces you to state the post-loop assertion precisely: `lo` is the first index whose seat is `>= wanted`, and the flag is `lo < len(sold) and sold[lo] == wanted`. Write that second expression in the order given and say why the order matters.

**Stretch in your write-up:** compare against `bisect.bisect_left`, which computes exactly the index half of this answer. Why do interviewers ask candidates to write the loop instead of calling the library? Because the writing is the boundary discipline. Put that in Examine (cost) as the interview-meta point — and note that the library would still leave you to write the flag.

### Problem 4 — The Sprinkler Reach — PARAMETRIC

**Domain.** A market garden runs one long irrigation row. Plants sit at fixed positions along the row, measured in metres from the gate; hydrants sit at their own fixed positions along the same row. Both lists arrive **sorted ascending**. Every hydrant gets the same sprinkler head, and a head of radius `r` waters everything within `r` metres of its hydrant, in both directions.

**Contract.**

```python
def min_sprinkler_radius(plants: list[int], hydrants: list[int]) -> int | None:
    """Both lists are sorted ascending, in metres. Return the smallest whole-metre
    radius r such that every plant is within r of some hydrant.
    Return 0 if there are no plants. Return None if there are plants but no hydrants."""
```

Two contract decisions that are not the obvious defaults:

- **No plants returns `0`, even when there are also no hydrants.** Nothing to water, no reach needed.
- **Plants with no hydrants returns `None`, not a huge number.** There is no radius that works, and saying so is different from saying "a very large one."

**Constraints.**

- `0 <= len(plants) <= 200_000` and `0 <= len(hydrants) <= 200_000`. Both empty lists are in range on purpose; they are the two contract branches above.
- `0 <= plants[i] <= 10**9` and `0 <= hydrants[j] <= 10**9`. Positions run to a billion, so the answer interval is about a billion wide — roughly 30 iterations, not a handful. It also means the predicate must not build a per-metre coverage array: that would be `10**9` booleans and is the trap this bound exists to set.
- Both lists arrive sorted. If you sort them yourself you have paid `O(n log n)` for order you were handed.

**Examples.**

- `plants = [2, 9, 14, 20], hydrants = [5, 12]` → `8`. The plant at 20 is 8 metres from the hydrant at 12, and every other plant is closer to one of the two hydrants: 2→3, 9→4, 14→2. At `r = 7` the plant at 20 goes dry.
- `plants = [2, 9, 14, 20], hydrants = [5, 12, 19]` → `3`. **The example that punishes checking only the hydrant to a plant's left.** The plant at 9 is 4 metres from the hydrant at 5 but only 3 from the one at 12, so a leftward-only predicate answers 4 — and the plant at 2 has no hydrant to its left at all, so a leftward-only predicate has no answer for it whatsoever. Each plant must be measured against the hydrant **before it and the one after it**, then the smaller of the two taken.
- `plants = [1, 2, 3], hydrants = [100]` → `99`. One hydrant, far away. The answer is large and the interval must be wide enough to hold it.
- `plants = [5], hydrants = [5]` → `0`. **A radius of zero is a legal answer.** A search that starts at `lo = 1` returns `1` here and is wrong by one on the easiest possible input.
- `plants = [], hydrants = [5, 12]` → `0`. No plants.
- `plants = [], hydrants = []` → `0`. **The degenerate case.** Still no plants, so still no reach — the missing hydrants do not matter.
- `plants = [3], hydrants = []` → `None`. **The no-solution case.** A plant with nowhere to draw from.

**Why included.** The coverage predicate is a different shape from the packing predicates in Exercise 5 and the homework: it is a *merge*, not an accumulator. Your write-up must add three things over the drill write-ups:

1. **A monotonicity proof** longer than one sentence — work it out on the first example, showing `feasible(7) → False`, `feasible(8) → True`, `feasible(9) → True`, and say why no larger radius can ever flip back.
2. **A failure-mode example** — walk through what the algorithm returns if you set `hi` too small (say `hi = max(plants) // 2`) and show that it silently produces a radius that does not water the row. A wrong bound does not crash; it lies.
3. **A compare-to-Problem-5 paragraph** — this is "minimise the threshold"; Problem 5 is "maximise the minimum." Same template, mirrored direction. Name the structural parallel.

### Problem 5 — The Delivery Zones — PARAMETRIC

**Domain.** A depot delivers along one street. The houses sit in order, and each house has a number of parcels waiting. The street is divided among **exactly** `couriers` couriers; each courier takes a **contiguous block** of houses, and every courier must be given **at least one house**.

Couriers are paid per parcel, so the depot wants the worst-off courier to do as well as possible.

**Contract.**

```python
def fairest_zone_split(houses: list[int], couriers: int) -> int | None:
    """houses are parcel counts, in street order. Split into exactly `couriers`
    contiguous non-empty zones. Return the LARGEST achievable value of the
    SMALLEST zone total. Return 0 for an empty street with zero couriers.
    Return None when the split is impossible."""
```

**Constraints.**

- `0 <= len(houses) <= 100_000`. The predicate is one `O(n)` greedy sweep; anything that re-scans per zone is `O(n²)` and will not finish here.
- `0 <= houses[i] <= 5_000`. Parcel counts may be **zero** — a house with nothing waiting today. Non-negativity is load-bearing: it is what lets the greedy predicate dump the leftover houses into the last zone without ever reducing that zone's total. Say that out loud; it is the step that makes the greedy correct rather than merely plausible.
- `0 <= couriers <= 100_000`. Courier counts above the house count are legal input and return `None`.

**Examples.** Work with `houses = [4, 1, 7, 3, 6, 2]` — six houses, 23 parcels total.

- `couriers = 3` → `5`. The optimal cut is `[4, 1] | [7] | [3, 6, 2]` → 5, 7, 11; the smallest zone carries 5. At a target of 6 the greedy sweep can only close two zones, so 5 is the boundary.
- `couriers = 2` → `11`. The optimal cut is `[4, 1, 7] | [3, 6, 2]` → 12, 11.
- `couriers = 4` → `3`. The optimal cut is `[4] | [1, 7] | [3] | [6, 2]` → 4, 8, 3, 8.
- `couriers = 6` → `1`. One house each; the worst-off courier gets the house holding a single parcel. The answer has bottomed out at `min(houses)`.
- `couriers = 1` → `23`. One courier takes the street; the smallest (and only) zone is the whole total.
- `couriers = 7` → `None`. **The no-solution case.** Seven couriers, six houses.
- `couriers = 0` → `None`. Zero couriers cannot cover a non-empty street.
- `houses = [0, 0, 5], couriers = 3` → `0`. **The example that punishes `lo = 1`.** Two zones must contain only empty houses, so the smallest zone total is zero — and zero is a legal answer, not a failure.
- `houses = [], couriers = 0` → `0`. **The degenerate case.**
- `houses = [], couriers = 1` → `None`.

**Why included.** The canonical *maximise-the-minimum* shape — the structural mirror of Problem 4. The predicate is `can_split(d) = (the greedy sweep closes at least `couriers` zones, each totalling at least d)`, and it is monotone in the **opposite** direction: as `d` rises, `can_split` eventually turns False and never turns back. So you search for the **largest** `d` where it is True, which is the upper-bound template — round-up mid, `lo = mid` on True, `hi = mid - 1` on False.

**The technique.** Sweep the houses left to right accumulating a running total; the moment the running total reaches `d`, close a zone and reset the accumulator to zero. Count the zones you closed. Feasible iff `count >= couriers` — greater is fine, because any surplus zones can be merged back into their neighbours without dropping any zone below `d`, and any trailing houses that never reached `d` are appended to the final zone, which only raises it. Search interval: `lo = 0`, `hi = sum(houses)`.

**Why this matters.** Maximise-the-minimum is the second of the four parametric shapes ([Lecture 2 §8](../lecture-notes/02-binary-search-on-the-answer.md)). Most candidates can do the minimise-the-threshold shape after some practice; the mirrored one catches them out because the boundary direction is flipped and the round-up `mid` is easy to forget. After this problem you have practised both directions and the four-element cadence is robust.

**Acceptance:**

- The 30-second parametric memo at the top.
- Explicit statement of which template (lower-bound or upper-bound) you use, and why the predicate's monotonicity direction forces that choice.
- A worked trace of `can_split` on `houses = [4, 1, 7, 3, 6, 2]` at `d = 5` (closes three zones — feasible) and at `d = 6` (closes two — infeasible), showing the accumulator resetting.
- One sentence on why the round-up `mid` formula is mandatory here and would be an infinite loop in Problem 4.

---

## File-level template

Each problem write-up follows this skeleton. Save as `problem-NN-<slug>.md`.

```markdown
# Problem NN — <name>

> **30-second pattern-recognition memo [optional: (parametric)]:**
> [six lines as above]

## Problem

[Spec + 2-3 examples, in your own words.]

## Why this variant

[1 paragraph: what makes this variant distinct from the others in the family.]

## FRAME write-up

### Frame
### Research constraints
[Expanded body — comparison against at least one other variant.]
### Assess options
### Make the solution
[Code with brief inline narration.]
### Examine (verify)
[Trace on 2 examples + 1 common bug avoided.]
### Examine (cost)
[5-piece from W2; with the time-defense sentence cleanly delivered.]

## Cross-references

- Lecture: [link]
- Drill: [link, if applicable]
- Related mini-project problem: [link to another problem in this folder]

## What I would do differently next time

[Optional but recommended: 1-2 sentences.]
```

---

## Acceptance criteria

- [ ] All five write-ups present in `frame-writeups/c2-week-05/mini-project/`.
- [ ] Each write-up has a leading 30-second memo following the schema above.
- [ ] **Problems 4 and 5 use the parametric memo schema** (four-element cadence), not the classic schema.
- [ ] Problem 5 explicitly states which boundary template (lower-bound or upper-bound) and why.
- [ ] Each write-up has a trace on at least two examples in the Examine (verify) section.
- [ ] Each write-up cross-references at least one other write-up in this folder.
- [ ] All five `.py` solution files are present and pass the example tables above, including every degenerate and no-solution row.

---

## Suggested order of operations

### Thursday — drafting (1.5h)

1. Open the mini-project folder. Create six empty files (the five problem write-ups + the README).
2. For each problem, write only the **30-second memo** at the top. Do not write the rest yet. Read each memo aloud; sharpen until it hits 25-30 seconds.
3. Commit "Mini-project memos drafted."

### Friday — Problems 1, 2, 3 (3h)

4. Write up Problems 1, 2, 3. These are classic variants and should be fast after the drills — but note that all three change the return type, so re-read each contract before you write the signature.
5. For each, trace at least two examples in Examine (verify). Make one of the two a degenerate case.
6. Commit each as you finish.

### Saturday — Problems 4, 5 (3h)

7. Problem 4: derive the coverage predicate yourself rather than adapting Exercise 5's accumulator — they are different shapes, and noticing that is half the exercise.
8. Problem 5: this is the flipped direction. Allow 90 minutes for the first attempt, and expect the round-up `mid` to bite you once.
9. Re-read all five memos aloud one last time. Sharpen anything that runs over 30 seconds.

### Sunday — polish + push (0.5h)

10. Add cross-references (each write-up links to ≥1 other).
11. Score yourself against the per-problem rubric. If anything is "vague" or "missing the boundary defense," sharpen it.
12. Push.

---

## What "great" looks like (final rubric)

A learner who has shipped this mini-project *well* has:

- All five memos under 30 seconds when read aloud.
- **Both parametric memos** explicitly state the monotonicity claim in one sentence.
- Problem 5's boundary template choice (lower-bound vs upper-bound) explicitly justified by the monotonicity direction.
- At least one "why not [alternative]" rejection per write-up — including, on Problem 4, the honest admission that a direct two-pointer computation beats the parametric one.
- Cross-references that form a small navigable web (Problem 4 ↔ Problem 5, Problem 1 ↔ Problem 3, etc.).

A learner who has shipped this mini-project *poorly* has:

- Memos that run 60+ seconds — too verbose, missing the cadence.
- Parametric memos without an explicit monotonicity claim.
- Problem 5 written as if the direction were the same as Problem 4; failing to recognise the maximise-the-minimum mirror.
- Degenerate rows quietly dropped from the tests because they were annoying.
- No cross-references; each write-up reads as a stand-alone with no awareness of the others.

If you catch yourself producing the "poorly" shape, the fix is to re-read [Lecture 2 §8](../lecture-notes/02-binary-search-on-the-answer.md) (the four parametric patterns) and re-do Problem 5 from scratch.

---

## Why five problems specifically

Two reasons.

1. **Three classic plus two parametric is the diet of a real binary-search interview.** A Phase-2 onsite typically asks one classic and one parametric variant. Five problems gives you five at-bats on the memo cadence and two at-bats on the parametric four-element form — enough for the muscle memory to install, not so many that the artifact bloats.

2. **The syllabus mandates exactly this composition.** From the Week 5 line in `SYLLABUS.md`: *"Mini-project: Solve 5 binary-search problems including 2 'search on answer' variants."* The composition is the contract.

If you finish before Sunday with energy to spare, the best sixth problem is one you write **yourself**: pick a system you actually use, find a monotone threshold inside it, and pose the problem in the format above. Authoring a problem is the strongest possible evidence that you own the pattern. The acceptance criterion is *five* — anything beyond is bonus.

---

When done: push everything, then move on to [Week 6 — Graphs Part 1: BFS](../../week-06-bfs/).

Phase 2's first week is closed. Your portfolio now contains five binary-search write-ups spanning both the index family and the answer-space family; that section will be referenced again in Mock #2 (Week 9) and in the capstone (Week 15).
