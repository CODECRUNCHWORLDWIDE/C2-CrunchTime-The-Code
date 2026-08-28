# Exercise 5 — The Paving Reach

> **Topic:** binary search on the **answer** — bisecting the range of possible answers when nothing in the input is sorted and nothing is being looked up
> **Lecture:** [02 — Binary Search on the Answer](../lecture-notes/02-binary-search-on-the-answer.md)
> **Difficulty:** Medium
> **Target time:** 30 minutes
> **Why this one:** the highest-yield thing you will learn this week. Nothing in this problem mentions a sorted list, an index, or a search — and the answer is a binary search anyway. Most candidates can write the loop when a prompt says "sorted array"; far fewer spot it when the prompt says "find the cheapest machine that finishes on time". This page is that spot, drilled.

## The Brief

A highway crew is repaving a road. The road has been cut into numbered
**sections**, and each section has a length in metres.

The paving train works one night at a time, and the town's contract says it may
only touch **one section per night**. It lays as much of that section as its
nightly **reach** allows, then shuts down — finished or not. So a section
longer than the reach takes several nights, and a section shorter than the
reach still uses up a whole night.

```
sections: 30  12  21  5  18        nights available: 6

with a reach of 21 metres:
  30m -> 2 nights   12m -> 1   21m -> 1   5m -> 1   18m -> 1      total 6  fits
with a reach of 20 metres:
  30m -> 2 nights   12m -> 1   21m -> 2   5m -> 1   18m -> 1      total 7  too slow
```

The crew rents the train by its nightly reach, in whole metres, and a bigger
reach costs more. Find the **smallest reach** that still finishes inside the
nights available.

Here is the thing to notice, and it is the whole exercise. There is no list to
search. But the answer is a number, that number is somewhere between 1 metre
and the longest section, and the reaches behave in a very particular way:

```
reach:      1    2   ...   19   20   21   22   23  ...  30
finishes?   no   no  ...   no   no   yes  yes  yes ...  yes
```

Once a reach is fast enough, every bigger reach is fast enough too. Never the
other way round. So the "no"s and the "yes"es cannot be interleaved — there is
exactly **one place where it flips**, and that place is the answer. Finding a
single flip in a range is precisely what binary search does, and it never
cared whether the range was a list.

Two contract decisions, neither of them the obvious default:

- If **no** reach can finish in time, return `None`. Nothing promises the crew
  has as many nights as sections, and one section always needs at least one
  night, so a budget smaller than the section count is impossible at any reach.
- If there are **no sections at all**, return `0`. No train needed. Not `1`,
  not `None` — the job is already done.

## Starter

Save this as `exercise-05-paving-reach.py` and fill in every `TODO`.

```python
"""exercise-05-paving-reach.py — the smallest nightly paving reach.

Binary search on the ANSWER: bisect the range of reaches, using "does this
reach finish in time?" as the comparison.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

# ---- Given data ----
SECTIONS: list[int] = [30, 12, 21, 5, 18]


# ---- Your task ----
def nights_needed(sections: list[int], reach: int) -> int:
    """Return how many nights a train of this reach takes on these sections.

    Args:
        sections: Section lengths in metres.
        reach: The nightly reach in metres, at least 1.

    Returns:
        The sum of ceil(section / reach) over every section.
    """
    # TODO: integer ceiling only: (length + reach - 1) // reach
    # TODO: never math.ceil(length / reach) — see Common bugs to catch
    ...


def min_nightly_reach(sections: list[int], nights: int) -> int | None:
    """Return the cheapest nightly reach that clears the road in time.

    Args:
        sections: Section lengths in metres, in any order.
        nights: How many nights the crew has before the road reopens.

    Returns:
        The smallest whole-metre reach that finishes within `nights`, 0 when
        there is nothing to pave, or None when no reach is fast enough.
    """
    # TODO: the two contract branches first — empty road, impossible budget
    # TODO: lo = 1, hi = max(sections). Why is that hi provably enough?
    # TODO: half-open search: hi = mid when the reach works, else lo = mid + 1
    ...


# ---- Self-check ----
if __name__ == "__main__":
    for budget in (6, 5, 4):
        answer = min_nightly_reach(SECTIONS, budget)
        if answer is None:
            print(f"{budget} nights -> no reach finishes in time")
        else:
            print(f"{budget} nights -> reach {answer}m, which uses {nights_needed(SECTIONS, answer)} nights")

    assert min_nightly_reach(SECTIONS, 6) == 21
    assert min_nightly_reach(SECTIONS, 5) == 30
    assert min_nightly_reach(SECTIONS, 4) is None
    assert min_nightly_reach([4, 4], 3) == 4
    assert min_nightly_reach([7], 3) == 3
    assert min_nightly_reach([9, 9, 9], 3) == 9
    assert min_nightly_reach([1_000_000_000], 1_000_000_000) == 1
    assert min_nightly_reach([], 0) == 0
    assert min_nightly_reach([12], 0) is None
    assert SECTIONS[0] == 30  # the section list was never rearranged
    print("All checks passed.")
```

Three ideas you need before you start.

**The answer space.** Not the input — the set of answers the question could
have. Here it is every whole number of metres from 1 up to the longest
section. Bisecting *that* is the move, and it is why this pattern has a name
of its own.

**The predicate.** A yes/no question you can answer about any candidate
answer. Here: *at this reach, does the crew finish within the nights they
have?* Answering it costs one pass over the sections — much cheaper than
solving the original question.

**Monotone.** The predicate's answers must go one way and stay there. Raise
the reach and no section can take *more* nights than before, so the total can
only fall or stay flat, so a "yes" can never turn back into a "no". That is
the licence to bisect, and it is a claim you must be able to state in one
sentence rather than assume.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-05-binary-search/exercises/exercise-05-paving-reach.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `nights_needed(sections, reach)` returns the total nights, computed with
   the integer ceiling `(length + reach - 1) // reach`.
2. `min_nightly_reach(sections, nights)` returns the smallest whole-metre
   reach that finishes within the budget.
3. It returns `0` for an empty section list, before anything calls `max`.
4. It returns `None` when the budget is smaller than the number of sections.
5. The search interval is `lo = 1` to `hi = max(sections)`, and you can prove
   `hi` always works.
6. The search uses the half-open package: guard `lo < hi`, `hi = mid` when the
   reach is fast enough, `lo = mid + 1` when it is not.
7. `math.ceil` appears nowhere in your solution.
8. Both functions keep their type hints and docstrings.

## Constraints

- **`0 <= len(sections) <= 100_000`.** The empty list is in range on purpose —
  it is one of the two contract branches. A hundred thousand sections keeps
  each feasibility check to a single pass; anything quadratic inside the
  predicate is ten billion operations per check, times thirty checks, and will
  not finish.

- **`1 <= sections[i] <= 10**9`.** A billion-metre section is what rejects the
  obvious brute force. Trying reach 1, then 2, then 3 until one works is up to
  a billion predicate calls; halving the same range is about thirty. **This
  bound is the reason the problem is a search and not a loop.** It also puts
  the division near the edge of what floating point handles exactly, which is
  why the integer ceiling is a requirement rather than a preference.

- **`0 <= nights <= 10**9`.** The budget may be **smaller** than the number of
  sections, which is the impossible case, and it may be enormous, in which case
  the answer is `1`. Both ends are real inputs and both are in the self-check.

- **Sections are never reordered or split.** One section per night, in
  whatever order they are given. That is what makes the cost a *sum of
  ceilings* rather than a division of the total — and the difference between
  those two is the trap this problem is built around.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-05-paving-reach.py
6 nights -> reach 21m, which uses 6 nights
5 nights -> reach 30m, which uses 5 nights
4 nights -> no reach finishes in time
All checks passed.
```

The middle row is worth a moment. With five sections and five nights, every
section must finish in one night, so the reach has to cover the longest one —
30 metres. That is exactly why `hi = max(sections)` is a *provable* upper
bound and not a hopeful guess: at that reach the total is always the number of
sections, which is the smallest total any reach can achieve.

## Steps

1. Save the starter and run it. `min_nightly_reach` returns `Ellipsis`, the
   first `print` shows something odd, and the first assert fails. Expected.
2. Write `nights_needed` first and test it alone at reach 21 (expect 6) and
   reach 20 (expect 7) on the sample sections.
3. Do the two contract branches next, before any search: empty list returns
   `0`; `len(sections) > nights` returns `None`. The second one is not
   defensive padding — it is the branch that produces `None`, and it has to
   run before `max` is called.
4. Set `lo, hi = 1, max(sections)`. Say out loud why `hi` is guaranteed to
   work before you type it.
5. Write the loop. While `lo < hi`: at the midpoint reach, if the crew
   finishes in time then that reach might be the answer, so `hi = mid`;
   otherwise it is too slow, so `lo = mid + 1`.
6. Return `lo`. There is no early return and no equality test anywhere — this
   search converges on a boundary rather than hunting for a value.
7. Run it, then hand-trace `sections = [4, 4], nights = 3` and work out why
   the answer is `4` and not the tempting `3`.
8. Trace the empty list and `[12]` with `0` nights and confirm neither one
   reaches the loop.

## The Solution

```python
"""exercise-05-paving-reach-solution.py - the smallest nightly paving reach.

Binary search on the ANSWER. Nothing in the input is sorted and nothing is
being looked up; what gets bisected is the interval of reaches the crew
could rent, using "does this reach finish in time?" as the comparator.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
SECTIONS: list[int] = [30, 12, 21, 5, 18]


# ---- Your task ----
def nights_needed(sections: list[int], reach: int) -> int:
    """Return how many nights a train of this reach takes on these sections.

    Args:
        sections: Section lengths in metres.
        reach: The nightly reach in metres, at least 1.

    Returns:
        The sum of ceil(section / reach) over every section.
    """
    return sum((length + reach - 1) // reach for length in sections)


def min_nightly_reach(sections: list[int], nights: int) -> int | None:
    """Return the cheapest nightly reach that clears the road in time.

    Args:
        sections: Section lengths in metres, in any order.
        nights: How many nights the crew has before the road reopens.

    Returns:
        The smallest whole-metre reach that finishes within `nights`, 0 when
        there is nothing to pave, or None when no reach is fast enough.
    """
    if not sections:
        return 0
    if len(sections) > nights:
        return None  # one section per night means this can never be met

    lo, hi = 1, max(sections)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nights_needed(sections, mid) <= nights:
            hi = mid  # mid works, so the answer is mid or smaller
        else:
            lo = mid + 1  # mid is too slow, so the answer is bigger
    return lo


# ---- Self-check ----
if __name__ == "__main__":
    for budget in (6, 5, 4):
        answer = min_nightly_reach(SECTIONS, budget)
        if answer is None:
            print(f"{budget} nights -> no reach finishes in time")
        else:
            print(f"{budget} nights -> reach {answer}m, which uses {nights_needed(SECTIONS, answer)} nights")

    assert min_nightly_reach(SECTIONS, 6) == 21
    assert min_nightly_reach(SECTIONS, 5) == 30
    assert min_nightly_reach(SECTIONS, 4) is None
    assert min_nightly_reach([4, 4], 3) == 4
    assert min_nightly_reach([7], 3) == 3
    assert min_nightly_reach([9, 9, 9], 3) == 9
    assert min_nightly_reach([1_000_000_000], 1_000_000_000) == 1
    assert min_nightly_reach([], 0) == 0
    assert min_nightly_reach([12], 0) is None
    assert SECTIONS[0] == 30  # the section list was never rearranged
    print("All checks passed.")
```

**Say the reframe out loud, in four parts, before writing anything.** It is
the same four parts every time, and interviewers grade it harder than the code:

> *Reframe:* find the smallest reach `w` such that the crew finishes within
> `nights` nights.
> *Interval:* `lo = 1`, because a reach of zero never advances; `hi =
> max(sections)`, because at that reach every section finishes in one night,
> giving a total of `len(sections)` — the smallest total any reach can
> achieve.
> *Predicate:* `nights_needed(sections, w) <= nights`. Monotone in `w`,
> because raising the reach never increases any section's night count.
> *Return:* the post-loop `lo`, which is the first reach where the predicate
> holds.

**`hi = max(sections)` is proved, not guessed.** At that reach every section
fits in one night, so the total is exactly the number of sections — and no
reach can ever do better than one night per section, because of the
one-section-per-night rule. So if `max(sections)` cannot meet the budget,
nothing can. That is the same fact the `None` guard tests, which is why the
guard and the upper bound belong to each other.

**The `None` branch is the feasibility check the lecture tells you to run
before the loop.** On most parametric problems that check is a formality
because the top of the interval always works. Here it is the entire
no-solution case, and skipping it does not crash — the search just runs, every
midpoint fails, `lo` climbs to `max(sections)`, and you confidently return a
reach that does not work.

**The empty list must be handled before `max` is called.** `max([])` raises,
and the guard is one line. That ordering is not politeness; it is the
difference between a contract branch and a crash.

**`(length + reach - 1) // reach` is the integer ceiling.** Adding one less
than the divisor before dividing pushes any non-zero remainder up to the next
whole number, and leaves exact multiples alone. It is all integer arithmetic,
so it is exact at every size. Say why you avoided `math.ceil` in one sentence:
floating point has about sixteen digits of precision, real section counts and
lengths can exceed that, and a ceiling that is wrong by one produces a reach
that passes your tests and fails in the field.

**`[4, 4]` with three nights is the counterexample to keep.** The tempting
closed form is "spread the work evenly": `ceil(8 / 3) = 3`. But at reach 3
each section takes `ceil(4/3) = 2` nights, four in total, over budget. At
reach 4 each takes one, two in total. Ceilings do not average — the
one-section-per-night rule means the cost is a sum of ceilings, and
`ceil(a/w) + ceil(b/w)` is not `ceil((a+b)/w)`. If your first instinct was the
average, this input is why the search exists.

**Half-open, because this is a "smallest such that" search.** `hi = mid` on
true keeps the candidate; `lo = mid + 1` on false discards it. Writing
`hi = mid - 1` steps over the boundary value and returns one metre too many —
the classic off-by-one on this shape, and it never crashes.

## Download and run

Download
[exercise-05-paving-reach-solution.py](./exercise-05-paving-reach-solution.py)
and run it:

```bash
python exercise-05-paving-reach-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-05-paving-reach.py`.

## Common bugs to catch

- **`ValueError: max() iterable argument is empty`.** You called
  `max(sections)` before handling the empty road:

  ```text
  Traceback (most recent call last):
      return max([])
  ValueError: max() iterable argument is empty
  ```

  The contract says an empty section list returns `0`. That branch has to come
  first, on the very first line of the function.

- **`ZeroDivisionError: integer division or modulo by zero`.** You set
  `lo = 0`, so the first midpoint can be a reach of zero metres:

  ```text
  Traceback (most recent call last):
      return (section + reach - 1) // reach
             ~~~~~~~~~~~~~~~~~~~~~~^^~~~~~~
  ZeroDivisionError: integer division or modulo by zero
  ```

  A train with no reach lays nothing, so zero is not a candidate answer at
  all. `lo = 1`.

- **`min_nightly_reach(SECTIONS, 4)` returns `30` instead of `None`.** The
  feasibility guard is missing. Every midpoint fails, `lo` climbs to the top
  of the interval, and the function returns the dearest train on the rate card
  as though it worked. Nothing crashes, which is what makes this the most
  dangerous bug on the page.

- **`min_nightly_reach([], 0)` returns `1`.** You guarded `max` but not the
  contract. With no sections the predicate is true at every reach, so an
  unguarded search converges on `lo = 1`. The answer is `0`: no sections, no
  train.

- **`min_nightly_reach([4, 4], 3)` returns `3`.** You answered
  `ceil(sum / nights)` instead of searching. It is the right shape of answer
  and the wrong number, and it is wrong precisely because ceilings do not
  average.

- **The answer is always one metre too big.** You wrote `hi = mid - 1` in a
  half-open loop, or `>` instead of `>=` somewhere in the comparison. Trace
  `sections = [7], nights = 3`: the answer is `3`, and the bug returns `4`.

- **`nights_needed` returns a night count and the branch reads
  `if nights_needed(...):`.** Any non-zero count is truthy, so the branch is
  always taken and the search converges on `lo` regardless of the input. Keep
  the comparison — `<= nights` — in the `if`.

- **`math.ceil(length / reach)` anywhere.** At the top of the constraint range
  the division stops being exact, and the ceiling can come out one too low.
  Here is the failure, made visible with a number just past the point where
  a float can hold every integer:

  ```text
  >>> import math
  >>> math.ceil((2**53 + 1) / 1)
  9007199254740992
  >>> -(-(2**53 + 1) // 1)
  9007199254740993
  ```

  The float answer is one too small, and there is no exception — just a wrong
  number. Integer arithmetic has no such edge.

## Under the hood

<details>
<summary>Under the hood — the cost, the mirror shape, and where this pattern shows up</summary>

**The cost, and why it has two different logarithms in it.**

Time is `O(n log M)`, where `n` is the number of sections and `M` is the
longest one. The search runs about `log2(M)` times — thirty at the top of the
constraint range — and each iteration calls a predicate that walks all `n`
sections. Space is `O(1)`: three integers in the search, one accumulator in
the predicate, nothing allocated per iteration.

Compare the brute force honestly. Trying reach 1, 2, 3, … until one works is
`O(n · M)` — the same predicate, called up to a billion times instead of
thirty. The predicate did not get cheaper; the number of calls did. That is
the entire contribution of this pattern, and it is worth saying in those
words.

An early exit inside the predicate — stop as soon as the running total passes
the budget — cuts the constant on infeasible midpoints. It changes no
asymptotics and is worth having anyway.

**The mirror: maximise the minimum.**

This page minimises a threshold. The mirror problem maximises one: *make the
worst-off worker as well-off as possible*. The machinery is identical and two
things flip. The predicate's monotonicity runs the other way — true, true,
true, then false — so you keep `lo = mid` on true and shrink with
`hi = mid - 1` on false. And because `lo = mid` keeps the midpoint, the
midpoint has to **round up**: `mid = lo + (hi - lo + 1) // 2`. Without the
round-up, `lo` and `mid` collide when two candidates remain and the loop spins
forever.

You will write that mirror twice more this week — in
[Challenge 2](../challenges/challenge-02-signal-mast-spacing.md) and in the
mini-project's fifth problem. Recognising the two directions as one pattern
with a flipped comparison, rather than as two templates to memorise, is the
thing that makes them stick.

**Where the pattern shows up outside practice problems.**

- Capacity planning: the smallest number of machines that keeps the queue
  under a target latency.
- Rate limiting: the largest sustainable requests-per-second that keeps error
  rates acceptable.
- Image processing: the threshold that leaves at least *k* pixels above it.
- Compilers: the smallest register count that lets a function be scheduled
  without spilling.

In every one of them the giveaway is the same sentence shape — "the smallest
`x` such that a property holds" or "the largest `x` such that it still holds"
— plus a property that cannot un-hold as `x` moves in one direction. When you
hear that shape in a prompt, you are already most of the way to the answer.

</details>

## Acceptance checklist

- [ ] `python exercise-05-paving-reach.py` prints three rows then
      `All checks passed.`
- [ ] The output matches the expected output character for character.
- [ ] You can deliver the four-part reframe — reframe, interval, predicate,
      return — in about thirty seconds.
- [ ] You can state the monotonicity claim in one sentence.
- [ ] Both contract branches run before the loop, and the empty branch runs
      before `max`.
- [ ] `lo = 1` and `hi = max(sections)`, and you can prove `hi` works.
- [ ] The integer ceiling is used; `math.ceil` appears nowhere.
- [ ] You traced `[4, 4]` with three nights and understand why `3` fails.
- [ ] Committed to Git with a message like
      `Add Week 5 exercise 5: paving reach`.

## Stretch

- **Return the schedule, not just the number.** The foreman wants the nightly
  plan.

  ```python
  def paving_plan(sections: list[int], reach: int) -> list[int]:
      """Return the metres laid on each night, in order, at a given reach."""
      plan = []
      for length in sections:
          left = length
          while left > 0:
              tonight = min(reach, left)
              plan.append(tonight)
              left -= tonight
      return plan
  ```

  ```text
  reach 21: [21, 9, 12, 21, 5, 18]  -> 6 nights
  ```

  Check that `len(plan)` always equals `nights_needed(sections, reach)`. Two
  independent routes to the same number is the cheapest correctness test there
  is.

- **Add an early exit to the predicate and measure it.** Stop accumulating as
  soon as the total passes the budget.

  ```python
  def finishes_in_time(sections: list[int], reach: int, nights: int) -> bool:
      """Return True when this reach clears the road within the budget."""
      total = 0
      for length in sections:
          total += (length + reach - 1) // reach
          if total > nights:
              return False
      return True
  ```

  ```text
  reach 20 on 100_000 sections: predicate stopped after 7 sections
  ```

  The complexity is unchanged and the constant is not. Being able to say which
  of those two you improved is the point of the exercise.

- **Loosen the contract and watch the answer change.** Suppose the train may
  carry on into the next section on the same night — no one-section-per-night
  rule. Work out the new cost function, then check whether
  `hi = max(sections)` is still a valid upper bound. It is not, and finding
  out *why* teaches more about bounds than any amount of re-reading.

That is all five drills. Take the [quiz](../quiz.md), then start the
[challenges](../challenges/README.md), the [homework](../homework/README.md),
and the [mini-project](../mini-project/README.md).
