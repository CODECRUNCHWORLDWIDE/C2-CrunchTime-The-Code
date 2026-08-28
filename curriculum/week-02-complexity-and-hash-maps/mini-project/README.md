# Mini-Project — The Complexity Audit

> **Topic:** going back to Week 1's five write-ups and rewriting every cost section to the five-piece structure — then proving the claims in it with a program
> **Lecture:** [03 — Stating Complexity Out Loud](../lecture-notes/03-stating-complexity-out-loud.md)
> **Difficulty:** no single piece is hard; being honest about five old write-ups at once is the work
> **Target time:** 5–7 hours, spread over Thursday to Saturday
> **Why this one:** the first *retrospective* project of the course. Most people accumulate work; the best people upgrade it. And this version does something a pure rewrite cannot — it makes you run the alternatives you are about to dismiss, so that every "the alternative is wrong, not merely slower" in your write-ups has an input attached to it.

<!-- no-runnable-file: what you hand in is five edited write-ups in your own portfolio repository plus a retrospective, which no script can produce for you. The runnable answer is complexity-audit-solution.py, which ships beside this page and is linked from Download and run. It is named after the project rather than after the page because a file called README.py would be a strange thing to ask anybody to download. -->

## The Brief

Imagine telling somebody "that shortcut doesn't work" and being asked "which
turning?" — and having no answer. You are fairly sure. You cannot show them.

That is what most tradeoff paragraphs in a portfolio look like. "I considered
sorting, but it would be slower." Slower than what, on what input, by how much?
An interviewer hears a claim and cannot tell whether you tested it or remembered
it.

This project fixes that, in two halves.

**Half one is editorial.** Go back to your five Week 1 write-ups and rewrite
every cost section to the five-piece structure from Lecture 3: time, space,
best/average/worst, tradeoffs, improvement. You write no new algorithm code. The
artifact is a Week-1 portfolio that visibly looks like Week-2 work.

**Half two is evidence.** Write one program — the audit — that, for each of the
five Week 1 drills, runs the approach you shipped *and* the alternative you
rejected, on the same inputs, and reports where the two disagree. Then paste the
disagreeing input into the write-up.

The interesting result is what the audit finds. For most of the five drills the
rejected alternative is not slower. It is **wrong** — it answers a question
nobody asked, and there is a specific, small input that proves it. "I rejected
the hash map here because it returns the earliest pair and the contract asks for
the widest, and on `[100, 100, 100, 100]` with correction 200 it returns
`(0, 1)` where the answer is `(0, 3)`" is a completely different sentence from
"I rejected the hash map because two pointers are faster." One of them is a
memory. The other is a measurement.

The five drills, and the alternative each one rejects:

| Drill | What you shipped | What you rejected |
|---|---|---|
| [1 — Reverse the Siding](../../week-01-the-frame-method-and-thinking-aloud/exercises/exercise-01-reverse-the-siding.md) | swap in place, count the swaps | slice-assign reversal |
| [2 — The Mirror Serial](../../week-01-the-frame-method-and-thinking-aloud/exercises/exercise-02-mirror-serial.md) | two pointers over the printed serial | filter first, then compare |
| [3 — The Widest Ballast Pair](../../week-01-the-frame-method-and-thinking-aloud/exercises/exercise-03-widest-ballast-pair.md) | converging pointers on a sorted row | this week's complement hash map |
| [4 — The Stuck Gauge](../../week-01-the-frame-method-and-thinking-aloud/exercises/exercise-04-stuck-gauge.md) | read and write pointers, in place | a set of values already seen |
| [5 — The Market Awning](../../week-01-the-frame-method-and-thinking-aloud/exercises/exercise-05-market-awning.md) | converging pointers, move the shorter side | every pair, brute force |

Four of those five alternatives are wrong rather than slow. Work out which one
is the exception before you run anything.

## Starter

Create `complexity-audit.py` in your portfolio repo, in a `c2-week-02/` folder,
and paste this in. Every drill's shipped approach is already written for you —
it is your own Week 1 work, restated — so the `TODO`s are all in the
alternatives and the audit.

```python
"""complexity-audit.py — evidence for five rewritten cost sections.

Fill in every TODO, then run the file. Each audit function returns a list of
human-readable disagreements; an empty list means the alternative agreed on
every input tried.
"""


# ---- Drill 1 — Reverse the Siding ----
def reverse_siding(cars: list[str], start: int, end: int) -> int:
    """Shipped: swap in place. O(n) time, O(1) space, and it counts the swaps."""
    if not (0 <= start < end < len(cars)):
        return 0
    swaps = 0
    left, right = start, end
    while left < right:
        cars[left], cars[right] = cars[right], cars[left]
        swaps += 1
        left += 1
        right -= 1
    return swaps


def reverse_siding_sliced(cars: list[str], start: int, end: int) -> int:
    """Alternative: slice-assign. O(m) auxiliary space, and it cannot count."""
    # TODO: validate the same way, then reverse with a slice assignment.
    # Return what this approach is actually able to report.
    ...


# ---- Drill 2 — The Mirror Serial ----
def first_mirror_break(serial: str) -> int | None:
    """Shipped: two pointers over the printed serial. O(n) time, O(1) space."""
    left, right = 0, len(serial) - 1
    while left < right:
        while left < right and not serial[left].isalnum():
            left += 1
        while left < right and not serial[right].isalnum():
            right -= 1
        if serial[left].lower() != serial[right].lower():
            return left
        left += 1
        right -= 1
    return None


def first_mirror_break_filtered(serial: str) -> int | None:
    """Alternative: filter first, then compare. Renumbers the positions."""
    # TODO: build a lowercased list of the significant characters, then
    # compare it from both ends. Return the index you have available.
    ...


# ---- Drill 3 — The Widest Ballast Pair ----
def widest_ballast_pair(weights: list[int], correction: int) -> tuple[int, int] | None:
    """Shipped: converging pointers on a sorted row. O(n) time, O(1) space."""
    left, right = 0, len(weights) - 1
    while left < right:
        total = weights[left] + weights[right]
        if total == correction:
            return (left, right)
        if total < correction:
            left += 1
        else:
            right -= 1
    return None


def widest_ballast_pair_hashed(
    weights: list[int], correction: int
) -> tuple[int, int] | None:
    """Alternative: this week's complement map. Finds the earliest pair, not the widest."""
    # TODO: Exercise 1's solution, unchanged. That is the point.
    ...


# ---- Drill 4 — The Stuck Gauge ----
def collapse_stuck_readings(levels: list[int]) -> int:
    """Shipped: read and write pointers, in place. Collapses adjacent runs only."""
    if not levels:
        return 0
    write = 1
    for read in range(1, len(levels)):
        if levels[read] != levels[write - 1]:
            levels[write] = levels[read]
            write += 1
    return len(levels) - write


def collapse_stuck_readings_seen(levels: list[int]) -> int:
    """Alternative: a set of values already seen. Drops every repeat, not every run."""
    # TODO: keep a set of values already kept, and skip anything in it.
    # Return the number dropped, same as the shipped version.
    ...


# ---- Drill 5 — The Market Awning ----
def max_curtain_area(pole_heights: list[int]) -> int:
    """Shipped: converging pointers, move the shorter side. O(n) time, O(1) space."""
    left, right = 0, len(pole_heights) - 1
    best = 0
    while left < right:
        height = min(pole_heights[left], pole_heights[right])
        best = max(best, height * (right - left - 1))
        if pole_heights[left] <= pole_heights[right]:
            left += 1
        else:
            right -= 1
    return best


def max_curtain_area_brute(pole_heights: list[int]) -> int:
    """Alternative: every pair. O(n^2) time, O(1) space. Same answer, worse cost."""
    # TODO: two nested loops over i < j.
    ...


# ---- The audit ----
def audit_reverse_siding() -> list[str]:
    """Drill 1: does the slice version answer the question that was asked?"""
    # TODO: run both on the same cars, compare the list AND the return value.
    ...


def audit_mirror_serial() -> list[str]:
    """Drill 2: does filtering first still point at the right printed position?"""
    ...


def audit_ballast_pair() -> list[str]:
    """Drill 3: does the complement map pick the pair this contract asks for?"""
    ...


def audit_stuck_gauge() -> list[str]:
    """Drill 4: does a seen-set collapse runs, or does it deduplicate?"""
    ...


def audit_market_awning() -> list[str]:
    """Drill 5: does the greedy scan ever disagree with checking every pair?"""
    ...


AUDITS = [
    ("1 Reverse the Siding", "slice-assign reversal", audit_reverse_siding),
    ("2 The Mirror Serial", "filter, then compare", audit_mirror_serial),
    ("3 Widest Ballast Pair", "complement hash map", audit_ballast_pair),
    ("4 The Stuck Gauge", "set of values seen", audit_stuck_gauge),
    ("5 The Market Awning", "every pair, brute force", audit_market_awning),
]


if __name__ == "__main__":
    print("Drill                   Rejected alternative      Verdict")
    print("-" * 72)
    wrong = 0
    for drill, alternative, audit in AUDITS:
        disagreements = audit()
        if disagreements:
            wrong += 1
            verdict = f"WRONG on {len(disagreements)} input(s)"
        else:
            verdict = "agrees; only slower"
        print(f"{drill:<23} {alternative:<25} {verdict}")

    print()
    print("Where they disagree, and on what:")
    for drill, _, audit in AUDITS:
        for line in audit():
            print(f"  {drill[0]}. {line}")

    print()
    print(f"{wrong} of {len(AUDITS)} alternatives are wrong rather than merely slower.")
    assert wrong >= 3, "at least three alternatives should be wrong, not just slower"
    print("All checks passed.")
```

Three things before you start.

**Use the drills' own examples as inputs.** Each Week 1 page lists five or six,
chosen to punish specific wrong approaches. They are already the adversarial
cases; you do not have to invent any.

**Compare the right thing.** For the in-place drills, comparing the return value
is not enough — you also have to compare what happened to the list. Drill 4's
comparison has to look at `levels[:kept]`, not at the whole list, because the
tail is scratch and both versions leave different rubbish there.

**Sweep, do not sample, where you cheaply can.** Drill 5's audit can check every
row of four poles with heights 0 to 3 — that is 256 rows, and it takes no time
at all. "It agreed on the six examples" is weak evidence. "It agreed on all 256
four-pole rows" is a different sentence.

**No setup needed — you can build this one in the browser.** Open the starter in the [online code editor](/courses/ide#src=C2-CrunchTime-The-Code/curriculum/week-02-complexity-and-hash-maps/mini-project/README.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. Five files edited in `frame-writeups/c2-week-01/`, one per Week 1 drill. Each
   cost section follows the five-piece structure: time, space,
   best/average/worst, tradeoffs, improvement.
2. Each edited section carries a visible note at the top — *"Cost section
   rewritten in Week 2 to the five-piece structure."* Make the upgrade visible;
   do not hide it.
3. Each of the five names its rejected alternative **with that alternative's
   complexity**, not just its name.
4. At least four of the five say the alternative is **wrong**, not merely
   slower, and each of those quotes a specific disagreeing input taken from your
   audit's output.
5. `complexity-audit.py` runs with no arguments, prints the verdict table and
   the disagreements, and ends with `All checks passed.`
6. Every audit function returns a list of strings, empty when the alternative
   agreed on everything tried.
7. A retrospective at `frame-writeups/c2-week-02/retrospective.md`, 200–400
   words.
8. At least five commits, one per drill is fine.

## Constraints

- **You write no new algorithm.** Both halves of every pair are code you have
  already written or already read this week. The project is deliberately not
  about inventing anything: a retrospective whose real work is a new algorithm
  is a retrospective you will do badly, because your attention will be on the
  new thing.

- **The audit must be deterministic.** No wall-clock timing in the printed
  output, no randomness without a fixed seed. Two runs on two machines must
  produce the same table, because the table is evidence and evidence that
  changes when you look at it is not evidence. Wall-clock measurement has its
  own home this week — [Homework Problem 2](../homework/problem-02-time-the-gap.md)
  — and it deliberately sends its timings to stderr for exactly this reason.

- **Compare like with like.** Both versions get the same input, and where a
  drill mutates its input, each gets its own copy. Handing the second version a
  list the first one already reversed is a way to produce disagreements that
  mean nothing.

- **An alternative that agrees is not a failure of the audit.** Drill 5's brute
  force gives the same answer on every input, and reporting that honestly is
  worth more than manufacturing a disagreement. "Genuinely equivalent, just
  quadratic" is a real finding, and it is the finding that makes the other four
  credible.

- **Do not rewrite the Week 1 problem pages.** They are last week's material and
  they are not yours to edit. What you rewrite is your own write-up in your own
  portfolio repository.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python complexity-audit-solution.py
Drill                   Rejected alternative      Verdict
------------------------------------------------------------------------
1 Reverse the Siding    slice-assign reversal     WRONG on 3 input(s)
2 The Mirror Serial     filter, then compare      WRONG on 1 input(s)
3 Widest Ballast Pair   complement hash map       WRONG on 3 input(s)
4 The Stuck Gauge       set of values seen        WRONG on 2 input(s)
5 The Market Awning     every pair, brute force   agrees; only slower

Where they disagree, and on what:
  1. cars=['HOP', 'TNK', 'BOX', 'GON', 'FLT'] start=1 end=3: shipped returned 1, slice returned 0
  1. cars=['HOP', 'TNK', 'BOX', 'GON', 'FLT'] start=0 end=4: shipped returned 2, slice returned 0
  1. cars=['HOP', 'TNK', 'BOX', 'GON'] start=0 end=3: shipped returned 2, slice returned 0
  2. serial='--G9': shipped 2, filtered 0
  3. weights=[120, 340, 500, 660, 880] correction=1000: shipped (0, 4), hash map (1, 3)
  3. weights=[100, 100, 100, 100] correction=200: shipped (0, 3), hash map (0, 1)
  3. weights=[200, 200, 800, 800] correction=1000: shipped (0, 3), hash map (0, 2)
  4. levels=[300, 300, 305, 300]: shipped kept [300, 305, 300], seen-set kept [300, 305]
  4. levels=[-2, -2, 0, 0, -2]: shipped kept [-2, 0, -2], seen-set kept [-2, 0]

4 of 5 alternatives are wrong rather than merely slower.
All checks passed.
```

Read the whole table before you read anything else.

**Four, not three.** If you guessed that Drill 1's slice version was fine
because the list comes out identical — it does come out identical, every time —
look at the second column of its three disagreements. The lists match; the
*return values* do not. The contract asks for a swap count, and a slice
assignment performs no swaps and can report nothing. It is wrong for a reason
that has nothing to do with memory, which is the reason the Week 1 page's
tradeoff paragraph gives.

**Drill 2 disagrees on exactly one input**, `'--G9'`, and one is enough. The
filtered string renumbers the positions, so the break it finds sits at index 0
while the printed serial's break is at index 2.

**Drill 3 disagrees on three of five**, and one of them,
`[100, 100, 100, 100]`, is the case the Week 1 page flagged as "punishes the
hash-map habit". This week you learned the hash map. This is the audit telling
you where not to use it.

**Drill 5 agrees on all 262 inputs tried.** That row is not a gap in the audit.
It is the control.

## Steps

### Thursday — the audit, and drills 1 to 3 (2h)

1. Write `complexity-audit.py` first, before touching any write-up. The
   alternatives are short; the audit functions are shorter. Run it and read the
   table.
2. Open Drill 1's write-up. Read the existing cost section cold, before you edit
   anything, and write down what is thin about it. That note goes in the
   retrospective.
3. Rewrite it to the five-piece structure, and paste in Drill 1's disagreement
   from the audit. Commit.
4. Same for Drill 2, then Drill 3. Drill 3 is the long one — it is the drill
   where the two-pointer-versus-hash-map decision becomes explicit, and where,
   for once, the hash map is the wrong tool. Give it the most time.

### Friday — drills 4 and 5, and the retrospective (2h)

5. Drill 4. Note that its disagreement is about *which samples survive*, not
   about a count, so quote the kept lists rather than the return value.
6. Drill 5 — and here you have to write the harder paragraph, because there is
   no disagreement to quote. "The alternative is genuinely equivalent and
   quadratic; the greedy scan buys a whole complexity class for the same `O(1)`
   space" is the honest sentence, and manufacturing a downside would be worse
   than having none.
7. Draft the retrospective. Commit.

### Saturday — polish and a second reader (3h)

8. Read all five write-ups end to end. Are the cost sections consistent in
   shape? They should be identical in structure and different in content.
9. Polish the retrospective until it is specific. "I learned a lot" is not a
   retrospective.
10. Send the repo link to one peer and ask: *"reading my Week-1 drills now, can
    you tell I learned complexity in Week 2?"* If they say no, the upgrade is
    not visible enough.
11. Push.

## The Solution

```python
"""complexity-audit-solution.py — evidence for five rewritten cost sections.

The Week 2 mini-project asks you to go back to your five Week 1 write-ups and
rewrite every cost section to the five-piece structure. Four of those five
sections have to name an alternative approach, and for three of them the
honest sentence is not "the alternative is slower" but "the alternative is
wrong".

A sentence like that is cheap to write and expensive to be wrong about. This
file is the evidence: for each of the five drills it runs the shipped approach
and the rejected alternative on the same inputs, and reports where they part
company. Paste the disagreeing input into your write-up. A claim with an input
attached is worth five without one.

Every function here is a Week 1 contract, restated. Nothing in this file is new
algorithm work; the new work is the audit at the bottom.
"""

from collections import Counter


# ---- Drill 1 — Reverse the Siding ----
def reverse_siding(cars: list[str], start: int, end: int) -> int:
    """Shipped: swap in place. O(n) time, O(1) space, and it counts the swaps."""
    if not (0 <= start < end < len(cars)):
        return 0
    swaps = 0
    left, right = start, end
    while left < right:
        cars[left], cars[right] = cars[right], cars[left]
        swaps += 1
        left += 1
        right -= 1
    return swaps


def reverse_siding_sliced(cars: list[str], start: int, end: int) -> int:
    """Alternative: slice-assign. O(m) auxiliary space, and it cannot count."""
    if not (0 <= start < end < len(cars)):
        return 0
    cars[start : end + 1] = cars[start : end + 1][::-1]
    return 0  # there is no swap count to return; nothing was swapped


# ---- Drill 2 — The Mirror Serial ----
def first_mirror_break(serial: str) -> int | None:
    """Shipped: two pointers over the printed serial. O(n) time, O(1) space."""
    left, right = 0, len(serial) - 1
    while left < right:
        while left < right and not serial[left].isalnum():
            left += 1
        while left < right and not serial[right].isalnum():
            right -= 1
        if serial[left].lower() != serial[right].lower():
            return left
        left += 1
        right -= 1
    return None


def first_mirror_break_filtered(serial: str) -> int | None:
    """Alternative: filter first, then compare. Renumbers the positions."""
    significant = [character.lower() for character in serial if character.isalnum()]
    left, right = 0, len(significant) - 1
    while left < right:
        if significant[left] != significant[right]:
            return left  # an index into the filtered string, not the printed one
        left += 1
        right -= 1
    return None


# ---- Drill 3 — The Widest Ballast Pair ----
def widest_ballast_pair(weights: list[int], correction: int) -> tuple[int, int] | None:
    """Shipped: converging pointers on a sorted row. O(n) time, O(1) space."""
    left, right = 0, len(weights) - 1
    while left < right:
        total = weights[left] + weights[right]
        if total == correction:
            return (left, right)
        if total < correction:
            left += 1
        else:
            right -= 1
    return None


def widest_ballast_pair_hashed(
    weights: list[int], correction: int
) -> tuple[int, int] | None:
    """Alternative: this week's complement map. Finds the earliest pair, not the widest."""
    earliest_at: dict[int, int] = {}
    for position, weight in enumerate(weights):
        complement = correction - weight
        if complement in earliest_at:
            return (earliest_at[complement], position)
        if weight not in earliest_at:
            earliest_at[weight] = position
    return None


# ---- Drill 4 — The Stuck Gauge ----
def collapse_stuck_readings(levels: list[int]) -> int:
    """Shipped: read and write pointers, in place. Collapses adjacent runs only."""
    if not levels:
        return 0
    write = 1
    for read in range(1, len(levels)):
        if levels[read] != levels[write - 1]:
            levels[write] = levels[read]
            write += 1
    return len(levels) - write


def collapse_stuck_readings_seen(levels: list[int]) -> int:
    """Alternative: a set of values already seen. Drops every repeat, not every run."""
    if not levels:
        return 0
    seen: set[int] = set()
    write = 0
    for read in range(len(levels)):
        if levels[read] not in seen:
            seen.add(levels[read])
            levels[write] = levels[read]
            write += 1
    return len(levels) - write


# ---- Drill 5 — The Market Awning ----
def max_curtain_area(pole_heights: list[int]) -> int:
    """Shipped: converging pointers, move the shorter side. O(n) time, O(1) space."""
    left, right = 0, len(pole_heights) - 1
    best = 0
    while left < right:
        height = min(pole_heights[left], pole_heights[right])
        best = max(best, height * (right - left - 1))
        if pole_heights[left] <= pole_heights[right]:
            left += 1
        else:
            right -= 1
    return best


def max_curtain_area_brute(pole_heights: list[int]) -> int:
    """Alternative: every pair. O(n^2) time, O(1) space. Same answer, worse cost."""
    best = 0
    for left in range(len(pole_heights)):
        for right in range(left + 1, len(pole_heights)):
            height = min(pole_heights[left], pole_heights[right])
            best = max(best, height * (right - left - 1))
    return best


# ---- The audit ----
def audit_reverse_siding() -> list[str]:
    """Drill 1: does the slice version answer the question that was asked?"""
    disagreements: list[str] = []
    for cars, start, end in [
        (["HOP", "TNK", "BOX", "GON", "FLT"], 1, 3),
        (["HOP", "TNK", "BOX", "GON", "FLT"], 0, 4),
        (["HOP", "TNK", "BOX", "GON"], 0, 3),
        (["HOP"], 0, 0),
        (["HOP", "TNK", "BOX"], 2, 1),
    ]:
        mine, theirs = list(cars), list(cars)
        shipped = reverse_siding(mine, start, end)
        other = reverse_siding_sliced(theirs, start, end)
        if mine != theirs or shipped != other:
            disagreements.append(
                f"cars={cars} start={start} end={end}: "
                f"shipped returned {shipped}, slice returned {other}"
            )
    return disagreements


def audit_mirror_serial() -> list[str]:
    """Drill 2: does filtering first still point at the right printed position?"""
    disagreements: list[str] = []
    for serial in ["RT7-e77-E7tr", "RT7-e77-E8tr", "8a-b-c8", "--G9", "Bb", "-K-", "--  --", ""]:
        shipped = first_mirror_break(serial)
        other = first_mirror_break_filtered(serial)
        if shipped != other:
            disagreements.append(
                f"serial={serial!r}: shipped {shipped}, filtered {other}"
            )
    return disagreements


def audit_ballast_pair() -> list[str]:
    """Drill 3: does the complement map pick the pair this contract asks for?"""
    disagreements: list[str] = []
    for weights, correction in [
        ([120, 340, 500, 660, 880], 1000),
        ([-400, -100, 0, 100, 300], 0),
        ([100, 100, 100, 100], 200),
        ([200, 200, 800, 800], 1000),
        ([150, 150], 300),
    ]:
        shipped = widest_ballast_pair(weights, correction)
        other = widest_ballast_pair_hashed(weights, correction)
        if shipped != other:
            disagreements.append(
                f"weights={weights} correction={correction}: "
                f"shipped {shipped}, hash map {other}"
            )
    return disagreements


def audit_stuck_gauge() -> list[str]:
    """Drill 4: does a seen-set collapse runs, or does it deduplicate?"""
    disagreements: list[str] = []
    for levels in [
        [412, 412, 412, 415, 415, 409],
        [300, 300, 305, 300],
        [777, 777, 777, 777],
        [500, 501, 502],
        [-2, -2, 0, 0, -2],
    ]:
        mine, theirs = list(levels), list(levels)
        dropped_mine = collapse_stuck_readings(mine)
        dropped_theirs = collapse_stuck_readings_seen(theirs)
        kept_mine = mine[: len(levels) - dropped_mine]
        kept_theirs = theirs[: len(levels) - dropped_theirs]
        if kept_mine != kept_theirs:
            disagreements.append(
                f"levels={levels}: shipped kept {kept_mine}, seen-set kept {kept_theirs}"
            )
    return disagreements


def audit_market_awning() -> list[str]:
    """Drill 5: does the greedy scan ever disagree with checking every pair?"""
    disagreements: list[str] = []
    rows = [
        [2, 6, 3, 8, 1, 7, 4],
        [2, 7, 5, 5, 7, 2],
        [5, 5],
        [0, 9, 9, 0],
        [4],
        [],
    ]
    # Plus every row of four poles with heights 0..3, so the claim is checked
    # against 256 rows rather than against six hand-picked ones.
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    rows.append([a, b, c, d])
    for poles in rows:
        shipped = max_curtain_area(poles)
        other = max_curtain_area_brute(poles)
        if shipped != other:
            disagreements.append(f"poles={poles}: shipped {shipped}, brute force {other}")
    return disagreements


AUDITS = [
    ("1 Reverse the Siding", "slice-assign reversal", audit_reverse_siding),
    ("2 The Mirror Serial", "filter, then compare", audit_mirror_serial),
    ("3 Widest Ballast Pair", "complement hash map", audit_ballast_pair),
    ("4 The Stuck Gauge", "set of values seen", audit_stuck_gauge),
    ("5 The Market Awning", "every pair, brute force", audit_market_awning),
]


if __name__ == "__main__":
    print("Drill                   Rejected alternative      Verdict")
    print("-" * 72)
    wrong = 0
    for drill, alternative, audit in AUDITS:
        disagreements = audit()
        if disagreements:
            wrong += 1
            verdict = f"WRONG on {len(disagreements)} input(s)"
        else:
            verdict = "agrees; only slower"
        print(f"{drill:<23} {alternative:<25} {verdict}")

    print()
    print("Where they disagree, and on what:")
    for drill, _, audit in AUDITS:
        for line in audit():
            print(f"  {drill[0]}. {line}")

    print()
    print(f"{wrong} of {len(AUDITS)} alternatives are wrong rather than merely slower.")

    # The mini-project's acceptance checklist asks for at least three.
    assert wrong >= 3, "at least three alternatives should be wrong, not just slower"
    # Counter is imported to make the point that it buys nothing here: the
    # gauge question is about adjacency, and a tally has no idea what is next
    # to what.
    assert Counter([300, 300, 305, 300])[300] == 3
    print("All checks passed.")
```

**The five-piece structure, which every one of your rewritten sections follows.**

```markdown
## E — Examine (cost)

*Cost section rewritten in Week 2 to the five-piece structure.*

**Time.** Each iteration is O(_) on the [structure]; n iterations total, so
**O(_)**, because [reason].

**Space.** I allocate [what] of size at most [bound], so **O(_) auxiliary**.

**Best / average / worst.** [Only where they differ meaningfully — early
termination, hash operations, sort-like algorithms. "No meaningful spread
here" is a better answer than an invented one.]

**Tradeoffs.**
- Alternative: [name] — O(_) time / O(_) space. It [wins when / is wrong
  because], and here is the input: [paste from the audit].
- I chose [mine] because [faster / smaller / simpler / preserves indices /
  answers the question actually asked].

**Improvement.** [Either "none; we are at the lower bound, because every
element must be read" or "could be O(_) if [_]; I did not because [_]".]
```

Spoken out loud that takes about two minutes. Written, about half a page. Both
are the right amount.

**Why the audit finds four and the intuition says three.** The three obvious
ones — Drills 2, 3 and 4 — are wrong because they *answer a different question*:
the filtered serial renumbers positions, the complement map selects a different
pair, the seen-set removes non-adjacent repeats. Drill 1 is wrong for a quieter
reason. The list it produces is correct, byte for byte, on every input. What it
cannot produce is the **return value**, because the contract asks how many swaps
were performed and a slice assignment performs none. A solution that gets the
side effect right and the return value wrong is still wrong, and it is the
easiest kind to miss when you are eyeballing output rather than comparing it.

That is the argument for writing the audit rather than reasoning about it. You
would have written "three of five" in your acceptance checklist, because that is
what the intuition says, and the program says four.

**Why Drill 5's row is the control.** An audit that reported every alternative
as wrong would be an audit nobody should believe — it would look like a tool
built to confirm what its author already thought. Drill 5's brute force agrees
on all 262 inputs, including a full sweep of every four-pole row with heights 0
to 3, because it genuinely computes the same maximum by a slower route. Being
able to point at a row that came back clean is what makes the other four rows
mean something.

**The 256-row sweep is the cheapest rigour available.** Six hand-picked examples
test what you thought of. Every four-pole row with heights 0 to 3 tests what you
did not, and it costs four nested loops and no measurable time. Whenever a
problem has a small input space, sweep it exhaustively — that is a habit worth
more than any individual test you will write this week.

**Why the timings are not here.** Nothing in the printed output depends on the
machine. That is a deliberate constraint, and it is why this project measures
*agreement* rather than *speed*: agreement is reproducible, and speed is not.
The wall-clock half of the week's argument lives in
[Homework Problem 2](../homework/problem-02-time-the-gap.md), which counts
operations to stdout and sends its seconds to stderr for exactly this reason.

**On the retrospective, and what makes one worth reading.** 200–400 words at
`frame-writeups/c2-week-02/retrospective.md`, with four headings: what was
missing before, what is better now, what you will do differently from Week 3
on, and the net effect on the portfolio. The thing that separates a good one
from a generic one is naming actual gaps — *"none of my five sections mentioned
space at all"* — rather than reporting feelings. It is for you, and it is also
for a hiring manager, who sees an engineer who reviews their own output. That
signal is rare.

## Download and run

Download
[complexity-audit-solution.py](./complexity-audit-solution.py) and run it:

```bash
python complexity-audit-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `complexity-audit.py`.

The rest of what you hand in is not a program and cannot be: five edited
write-ups and a retrospective, in your own portfolio repository. Check those the
way a reader would — clone your own repo into a temporary folder, read the five
cost sections end to end, and ask whether they look like they were written in
the same week as each other and a different week from the code above them.

## Common bugs to catch

- **Every drill reports a disagreement, including Drill 5.** You handed both
  versions the same list object and the first one mutated it:

  ```text
  Traceback (most recent call last):
      assert wrong >= 3, "at least three alternatives should be wrong, not just slower"
  ```

  That assert passes with this bug, which is the point — the bug shows up as a
  *suspiciously complete* result rather than as an error. Give each version its
  own `list(...)` copy. An audit that always says "wrong" proves nothing.

- **Drill 4 reports no disagreement.** You compared the return values, and both
  versions happen to return the same count on some inputs. The contract's real
  output is `levels[:kept]`, so that is what the comparison has to look at.
  Comparing the whole list is also wrong, because the tail is scratch and the
  two versions leave different rubbish in it.

- **`AssertionError` on the `wrong >= 3` check.** Your alternatives are too
  faithful — most likely you wrote `widest_ballast_pair_hashed` so that it keeps
  scanning for a wider pair, which quietly turns it into the shipped version.
  The alternative has to be the approach as somebody would actually write it,
  not a corrected version of it. An audit of a straw man teaches nothing; an
  audit of a fixed-up alternative teaches less.

- **`TypeError: 'NoneType' object is not iterable`.** An audit function fell off
  the end without returning:

  ```text
  Traceback (most recent call last):
      for line in audit():
                  ^^^^^^^
  TypeError: 'NoneType' object is not iterable
  ```

  Every audit must return a list, empty when everything agreed. `return []` is a
  result; falling through is a bug.

- **The audit runs twice and prints different disagreements.** You used
  `random` without a seed, or iterated a set and reported in that order. The
  table is evidence. Fix the seed, or sort the disagreements before printing.

- **Rewriting the Week 1 problem pages instead of your write-ups.** The pages in
  `week-01-.../exercises/` are course material. Your write-ups live in your
  portfolio repo under `frame-writeups/c2-week-01/`. Editing the former is both
  the wrong file and, in a fork, a merge conflict waiting to happen.

- **Cost sections that are consistent in shape and identical in content.** If
  all five say "O(n) time, O(1) space, no meaningful spread, the alternative is
  slower", you templated rather than audited. Every one of the five has a
  genuinely different tradeoff story, and four of them have a disagreeing input
  to quote.

## Under the hood

<details>
<summary>Under the hood — why a wrong alternative is a better tradeoff paragraph than a slow one, and how to find one deliberately</summary>

**"Slower" is a weak claim and "wrong" is a strong one.**

A tradeoff paragraph that says "sorting would be `O(n log n)` and mine is
`O(n)`" invites the obvious reply: *at your input size, does it matter?* Often
it does not, and then your paragraph has argued for a preference rather than a
decision.

A paragraph that says "sorting renumbers the positions, and the contract asks me
to return positions" is not a preference. It closes the question. And it
demonstrates something the complexity claim does not: that you read the contract
carefully enough to notice a constraint the alternative violates.

Three of this week's five drills have exactly that structure, and it is not a
coincidence. It is how the Week 1 problems were written — each contract was
varied away from the obvious default (return indices rather than values, the
widest pair rather than any pair, adjacent repeats rather than all repeats)
specifically so that the tempting alternative answers the wrong question.

**How to find the wrong-not-slow alternative on a new problem.** Ask what each
candidate approach *destroys*:

- Sorting destroys positions. Any contract that returns an index is in tension
  with any solution that sorts.
- Filtering destroys positions too, in a subtler way: it renumbers them. Drill 2
  is exactly this.
- A set destroys multiplicity and adjacency. Drill 4 is adjacency; Exercise 3's
  `frozenset` trap this week is multiplicity.
- A hash map destroys order of selection: it finds *a* match, and which one
  depends on the scan, not on the contract. Drill 3 is this.
- An in-place algorithm destroys the original. Any contract that says the
  caller's data must survive is in tension with it.

Run that checklist against your candidates and the "wrong, not slow" cases fall
out. It takes thirty seconds and it is the single highest-yield habit in this
project.

**Why an exhaustive sweep beats more hand-written cases.** Drill 5's audit
checks 256 four-pole rows. You could not write 256 cases by hand, and if you
tried, they would all be cases you thought of — which is precisely the set of
cases your implementation already handles, because you wrote it while thinking
of them. Exhaustive sweeps over a small input space, and randomised
cross-checking against an obviously-correct reference over a large one, are the
two techniques that find bugs you did not imagine. Challenge 1's stretch does
the randomised version; this project does the exhaustive one. Both are worth
having in your hands before Week 3.

**A note on retrospective work and what a portfolio actually shows.** A
portfolio where `c2-week-01/` looks like `c2-week-02/` looks like
`c2-week-15/` does not show learning — it shows a constant skill level over
fifteen weeks, which is not the thing anybody is looking for. The portfolio you
want shows visible upgrades: Week 5 write-ups with edge-case discussions Week 3
could not have had, Week 10 design discussions Week 5 could not have predicted.
This project is the first instance of that pattern. There will be more.

</details>

## Acceptance checklist

- [ ] `python complexity-audit.py` prints the verdict table, the disagreements,
      and `All checks passed.`
- [ ] The table matches the expected output character for character.
- [ ] Drill 5's row reads `agrees; only slower`, and you did not "fix" it.
- [ ] Each version gets its own copy of any input it mutates.
- [ ] Drill 4's comparison looks at `levels[:kept]`, not at the whole list.
- [ ] All five write-ups edited in `frame-writeups/c2-week-01/`, each cost
      section following the five-piece structure.
- [ ] Each edited section carries the visible "rewritten in Week 2" note.
- [ ] Each names its alternative **with that alternative's complexity**.
- [ ] At least four quote a specific disagreeing input from the audit.
- [ ] `frame-writeups/c2-week-02/retrospective.md` committed, 200–400 words,
      naming actual gaps rather than feelings.
- [ ] At least five commits with meaningful messages — `Upgrade Widest Ballast
      Pair cost section to the five-piece structure` beats `update`.
- [ ] The repository is still public and its README still renders cleanly.

## Stretch

- **Count operations instead of only comparing answers**, so the "only slower"
  row gets a number attached to it too.

  ```python
  def curtain_area_steps(pole_heights: list[int]) -> tuple[int, int]:
      """Return (greedy steps, brute-force steps) for the same row of poles."""
      greedy = 0
      left, right = 0, len(pole_heights) - 1
      while left < right:
          greedy += 1
          if pole_heights[left] <= pole_heights[right]:
              left += 1
          else:
              right -= 1
      n = len(pole_heights)
      return (greedy, n * (n - 1) // 2)

  for size in (10, 100, 1000):
      greedy, brute = curtain_area_steps(list(range(size)))
      print(f"{size:5d} poles: greedy {greedy:6d}, brute force {brute:8d}")
  ```

  ```text
     10 poles: greedy      9, brute force       45
    100 poles: greedy     99, brute force     4950
   1000 poles: greedy    999, brute force   499500
  ```

  Ten times the poles, ten times the greedy work, a hundred times the brute
  force. That is `O(n)` against `O(n^2)` in three lines of a table, and it is the
  sentence Drill 5's tradeoff paragraph needed.

- **Add a randomised cross-check to the one drill where both versions are
  supposed to agree.**

  ```python
  import random

  rng = random.Random(20260227)
  mismatches = 0
  for _ in range(2000):
      poles = [rng.randint(0, 12) for _ in range(rng.randint(0, 9))]
      if max_curtain_area(poles) != max_curtain_area_brute(poles):
          mismatches += 1
  print(f"{mismatches} mismatches over 2000 random rows")
  ```

  ```text
  0 mismatches over 2000 random rows
  ```

  Two thousand random rows on top of the 256-row sweep. The greedy scan's
  correctness is the one claim in Week 1 that is genuinely non-obvious — the
  proof that moving the shorter pole never skips a better answer takes a
  paragraph — so it is the claim most worth testing rather than trusting.

- **Audit a sixth thing: your own Week 2 exercises.** Take Exercise 3's
  `frozenset` trap and Exercise 5's missing root check, write each as an
  "alternative", and run them through the same harness. Both are wrong in ways
  this week already told you about, which makes them a good calibration — if
  your harness cannot catch a bug you already know is there, it will not catch
  one you do not.

---

When the five write-ups are pushed and the audit is green, you have finished
Week 2. Next: [Week 3 — Sliding Window](../../week-03-sliding-window/).
