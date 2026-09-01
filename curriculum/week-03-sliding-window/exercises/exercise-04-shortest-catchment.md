# Exercise 4 — The Shortest Catchment

> **Topic:** a variable-size window that shrinks while the property *holds*, and records the answer inside the shrink
> **Lecture:** [02 — The Shrinking and Growing Mechanics](../lecture-notes/02-the-shrinking-and-growing-mechanics.md)
> **Difficulty:** Medium
> **Target time:** 60 minutes
> **Why this one:** everything so far looked for the *longest* window. This one wants the *shortest*, and that single word turns the loop inside out — you shrink while the promise is true rather than while it is broken, and you write the answer down in the middle of shrinking rather than after it. The second lesson is the tie-break, which forces you to carry more than a length.

## The Brief

A reservoir measures how much water flows in each day and writes it down in
date order, in megalitres. Dry days read `0`, and there are plenty of them.

Before the operators take the reservoir offline for maintenance, they have to
bank a **quota** of water. They want the **shortest run of days in a row** that
delivers it — every day the reservoir stays open is a day the maintenance
crew stands around waiting, so short is what they are paying for.

Compare that with Exercise 2, which wanted the *longest* window. The difference
sounds small and it changes the loop completely, so it is worth being precise
about why.

When you want the **longest** window, the property you care about is something
a window can break by getting bigger — a repeated die, too many distinct
classes. So you push the right edge out, and when the promise breaks you pull
the left edge in *until it is fixed*, and then you measure. You shrink **while
the promise is broken**.

When you want the **shortest** window, it is the other way round. The property
is something a window achieves by getting bigger — enough water. So you push
the right edge out until the promise is finally *true*, and then you pull the
left edge in as far as you can **while it is still true**, measuring at every
step, because each trim gives you a shorter window that still works. You shrink
**while the promise holds**.

There is a quiet assumption underneath that second loop, and it is the most
important sentence on this page. Trimming a day off the left can only make the
total **smaller**. That is only true because inflow is never negative. If a
reading could be negative, dropping it from the left would *raise* the total,
the window could come back into qualification after you had already stopped
trimming, and the whole approach would miss real answers. Sliding window is the
right pattern here because of a fact about the data, not because of the shape of
the question.

**Your job.** Return the shortest qualifying run as `(start, days)` — the index
of its first day, and how many days it covers.

Two pieces of small print. If several runs tie on length, return the one with
the **largest total inflow**: banking more water for the same number of days is
strictly better, so the operators want that one. If two runs tie on both length
and total, return the earlier. And if no run of any length reaches the quota,
return `None`.

## Starter

Create `exercise-04-shortest-catchment.py` and paste this in. Fill in every
`TODO`.

```python
"""exercise-04-shortest-catchment.py — the shortest catchment run.

Find the shortest run of consecutive days whose inflow reaches the quota, and
return where it is.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""


def shortest_catchment(inflow: list[int], quota: int) -> tuple[int, int] | None:
    """Return the shortest run of days whose inflow reaches the quota.

    Args:
        inflow: Daily inflow in megalitres, in date order. Never negative.
        quota: The megalitres that must be banked.

    Returns:
        (start, days) for the shortest qualifying run. Ties go to the run with
        the largest total, then to the earlier start. None when no run of any
        length reaches the quota.
    """
    # TODO: `left` at 0, a `running` total at 0, and `best` unset — use None,
    #       not a zero, because zero days is a shape a bug can produce.
    # TODO: walk `right` over the log with enumerate, adding to `running`.
    # TODO: while `running` still reaches the quota:
    #         - build a candidate that carries LENGTH, TOTAL and START, in an
    #           order that lets one comparison settle all three rules;
    #         - keep it if it beats the incumbent;
    #         - THEN subtract inflow[left] and advance left. Record first.
    # TODO: unpack the winner and return it in the order the contract asks for.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[int], int]] = [
        ([4, 6, 1, 7, 8], 10),
        ([3, 1, 4, 1, 5, 9, 2], 11),
        ([0, 0, 12, 0], 12),
        ([2, 3, 4], 9),
        ([1, 1, 1], 10),
        ([], 1),
    ]
    for inflow, quota in cases:
        answer = shortest_catchment(inflow, quota)
        if answer is None:
            print(f"quota {quota:>2}  log {str(inflow):<22} -> None")
        else:
            start, days = answer
            run = inflow[start : start + days]
            print(f"quota {quota:>2}  log {str(inflow):<22} -> days {start}..{start + days - 1} = {run}, total {sum(run)}")
    print()

    assert shortest_catchment([4, 6, 1, 7, 8], 10) == (3, 2)
    assert shortest_catchment([3, 1, 4, 1, 5, 9, 2], 11) == (4, 2)
    assert shortest_catchment([0, 0, 12, 0], 12) == (2, 1)
    assert shortest_catchment([2, 3, 4], 9) == (0, 3)
    assert shortest_catchment([1, 1, 1], 10) is None
    assert shortest_catchment([], 1) is None

    # Every answer really does reach the quota, and nothing shorter does.
    for inflow, quota in cases:
        answer = shortest_catchment(inflow, quota)
        if answer is None:
            assert all(
                sum(inflow[i:j]) < quota
                for i in range(len(inflow))
                for j in range(i + 1, len(inflow) + 1)
            )
            continue
        start, days = answer
        assert sum(inflow[start : start + days]) >= quota
        for i in range(len(inflow)):
            for j in range(i + 1, len(inflow) + 1):
                if sum(inflow[i:j]) >= quota:
                    assert j - i >= days

    print("All checks passed.")
```

Two things you need before you start.

**Tuple comparison.** Python compares tuples box by box, left to right, and
stops at the first difference. So `(2, -15, 3) < (2, -10, 0)` is `True`: the
first boxes tie, and `-15` is less than `-10`. That is how one `<` can express
three ranking rules at once — put them in priority order, and negate any number
you want to rank *downwards*. You met this in C1 with `sorted(key=...)`; it is
the same trick, used without a sort.

**Monotone.** A quantity that only ever moves one way as you change something.
Here: as you trim days off the left, the running total is monotone
non-increasing. That is what makes "stop as soon as it drops below the quota"
safe — once it drops, more trimming cannot bring it back.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-03-sliding-window/exercises/exercise-04-shortest-catchment.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `shortest_catchment(inflow, quota)` returns `(start, days)` — a position and
   a length, in that order — or `None`.
2. Among runs of equal length, the one with the **largest total** wins.
   `shortest_catchment([4, 6, 1, 7, 8], 10)` is `(3, 2)`, not `(0, 2)`.
3. Among runs tying on both length and total, the **earlier start** wins.
4. No qualifying run returns `None` — not `0`, not `(-1, 0)`.
5. The shrink loop condition uses `>=`, so a total landing exactly on the quota
   still trims.
6. Inside the shrink loop the order is **record, subtract, advance**.
7. The running total is maintained incrementally. Nothing inside the loop may
   call `sum`.
8. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(inflow) <= 500_000`.** Roughly fourteen hundred years of daily
  readings, so this bound is not about realism — it is about ruling out the
  double loop over every start and every end, which is about `1.25 x 10^11`
  additions here and will not finish. Worth naming the middle option too:
  prefix sums plus a binary search per start is `O(n log n)` and *would* finish
  comfortably. The window is `O(n)` and needs no extra array, which is why it
  is the answer we want — but knowing that a second correct approach exists,
  and what it costs, is the part interviewers actually probe.

- **`0 <= inflow[i] <= 10_000`, and non-negativity is the load-bearing one.**
  Everything above about monotone shrinking depends on it. With even one
  negative reading, dropping a day from the left can *raise* the total, the
  "once it drops below, stop" rule becomes false, and the window silently
  misses valid runs. The right tool then is prefix sums plus a hash map, which
  is a different pattern and a different week. Say this sentence out loud
  before you write the loop; it is the sentence that separates "I recognised a
  window" from "I checked that a window applies."

- **Zero is a legal reading, and dry days are common.** Zeros are what catch a
  shrink condition written `running > quota` instead of `running >= quota`: on
  a total that lands exactly on the quota the loop never runs, so the window
  stops trimming one day early and reports a run longer than the real answer.

- **`1 <= quota <= 5_000_000_000`.** The quota may exceed the total inflow of
  the entire log, which is what makes the `None` path real rather than
  theoretical. It may also exceed `2^31`, which costs you nothing in Python
  because integers grow as needed — but it is worth one sentence about what a
  C++ or Java translation would need, because that is a real question in a real
  interview.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-04-shortest-catchment.py
placeholder
```

The first row is the graded one. No single day reaches 10, so the shortest
possible run is two days, and two different two-day runs qualify: days 0–1
totalling exactly 10, and days 3–4 totalling 15. They tie on length. The
tie-break takes the larger total, so the answer is days 3–4 — and a solution
that keeps the *first* window it finds at the minimum length returns `(0, 2)`
and looks entirely reasonable while being wrong.

The third row is the other trap. `[0, 0, 12, 0]` with a quota of 12 lands
exactly on the quota, and the two leading zeros have to be trimmed off. With
`>` instead of `>=` the shrink loop never runs at all and you report a
four-day answer to a one-day question.

## Steps

1. Create the file, paste the starter, and run it. Every row prints `None` and
   the first assert fails. Correct starting point.
2. Set up `left`, `running` and `best`. Make `best` an explicit `None`. Zero is
   not "unset" here, because a buggy solution can genuinely produce a zero-day
   window, and you would not be able to tell the two apart.
3. Write the outer loop and the addition. `running += litres`, nothing else.
4. Write the shrink as a `while`, not an `if`. On `[0, 0, 12, 0]` you have to
   trim twice in one iteration; an `if` trims once and stops.
5. Get the condition right: `while running >= quota`. Read Requirement 5 again.
6. Build the candidate. It needs three numbers — length, total, start — in the
   order the ranking rules come in, with the total negated because bigger is
   better. Write the English sentence next to it in a comment: *shorter wins,
   then bigger total, then earlier start*.
7. Compare with `<` against the incumbent, and only then subtract and advance.
   Requirement 6 is about these three lines being in that order.
8. Unpack at the end. The contract wants `(start, days)`, and your tuple holds
   them in a different order for a reason — the ranking order and the return
   order are not the same thing.
9. Trace `[4, 6, 1, 7, 8]` with quota 10 by hand before you trust the tests.
   Five rows, and the interesting one is the last, where the shrink fires
   twice.

## The Solution

```python
placeholder
```

**One tuple says all three rules.**

```python
candidate = (right - left + 1, -running, left)
```

Read it left to right as the sentence the contract gives you: *shorter wins;
then, among equal lengths, bigger total wins; then, among those, earlier start
wins.* Python compares tuples box by box and stops at the first difference, so
a single `<` settles the whole ranking. The minus sign in front of `running` is
the direction switch: length and start rank upwards, the total ranks downwards,
and negating exactly one of them lets all three live in one comparison.

Writing this as three nested `if`s also works and is three times as easy to get
wrong, because each branch has to remember what the previous ones already
settled.

**Tracking only the length is the graded bug.** A solution that keeps
`best_length` and nothing else cannot tell days 0–1 from days 3–4, because both
are two days long. It keeps whichever it saw first and returns `(0, 2)`. The
tie-break in the contract exists precisely to force the extra field into your
state, and this is the general lesson: *what you have to carry is decided by
the tie-break, not by the question.*

**Record, subtract, advance — in that order.**

```python
if best is None or candidate < best:
    best = candidate
running -= inflow[left]
left += 1
```

The window you are measuring is the one that exists *right now*. Subtract
first and you have measured a window you already destroyed: the length is one
too many, or the total belongs to a window that no longer qualifies. This
ordering is the single most common error in the shrinking shape, and it is
worth saying out loud every time you write one.

**`while`, not `if`.** On `[0, 0, 12, 0]` with a quota of 12, the moment day 2
arrives the window is days 0–2 and already qualifies. It has to trim twice —
once for each leading zero — before it becomes the one-day answer. An `if`
trims once and reports a two-day run. The `while` is also what makes the whole
thing correct in general: after each trim the window may *still* qualify, and
every one of those is a shorter candidate you are obliged to consider.

**`>=`, not `>`.** The quota is a floor to reach, not a bar to clear. A run
totalling exactly the quota qualifies, so the shrink must keep going while the
total is still at or above it. With `>` the loop stops one trim early on every
exact landing, which is why the zeros case exists.

**`best is None` rather than a sentinel number.** `float("inf")` would work for
the length, but `None` is better here for a reason worth internalising: zero
days is a shape a buggy implementation can genuinely produce, so if "unset"
were represented by a number, you could not distinguish "no answer" from "a
wrong answer that happens to look like no answer". The contract returns `None`
for the same reason, one level up — a caller writing `if result:` cannot tell
`0` from "nothing found", and `(start, days)` is never falsy.

**Why the loop is linear despite the `while` inside it.** `right` advances
exactly `n` times. `left` only ever moves forward and never passes `right`, so
across the entire function it advances at most `n` times *in total* — not `n`
times per outer step. The inner loop is bounded across the whole run rather
than per iteration, which is the same amortised argument as Exercise 2, and the
reason it holds is the same: the index it advances never resets.

## Download and run

Download
[exercise-04-shortest-catchment-solution.py](./exercise-04-shortest-catchment-solution.py)
and run it:

```bash
python exercise-04-shortest-catchment-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-04-shortest-catchment.py`.

## Common bugs to catch

- **`shortest_catchment([4, 6, 1, 7, 8], 10)` returns `(0, 2)` instead of
  `(3, 2)`.** You tracked only the length. No traceback; both answers are
  two-day runs that reach the quota, and yours is simply the wrong one of the
  two. This is the graded bug of the drill. The fix is a wider candidate, not a
  different comparison.

- **`shortest_catchment([0, 0, 12, 0], 12)` returns `(0, 3)` or `(0, 4)`.**
  Either `while running > quota` — so the loop never fires on an exact landing
  — or an `if` where a `while` belongs, so it fires once and stops with a
  leading zero still inside.

- **`TypeError: '<' not supported between instances of 'tuple' and 'NoneType'`.**

  ```text
  Traceback (most recent call last):
      if candidate < best:
         ^^^^^^^^^^^^^^^^
  TypeError: '<' not supported between instances of 'tuple' and 'NoneType'
  ```

  You compared before checking whether there is an incumbent. `if best is None
  or candidate < best` short-circuits: Python stops at the first `or` branch
  that is true, so the comparison never runs on the first candidate. Order
  matters in that line.

- **`IndexError: list index out of range`.**

  ```text
  Traceback (most recent call last):
      running -= inflow[left]
                 ~~~~~~^^^^^^
  IndexError: list index out of range
  ```

  Your shrink condition can stay true after the window is empty — usually
  because you wrote `while running >= quota` with a `quota` of `0`, or because
  you forgot to subtract and `running` never falls. The contract guarantees
  `quota >= 1`, which is what makes the loop terminate without a guard; if you
  relax that bound, you need one.

- **`shortest_catchment([1, 1, 1], 10)` returns `0` or `(0, 0)`.** You used a
  falsy sentinel for "no answer". The contract says `None`, because `0` is
  indistinguishable at the call site from a zero-day run, and a zero-day run is
  something a bug produces.

- **The answer's length is one too many.** You subtracted before recording.
  Check the three lines in the shrink body against Requirement 6.

- **Using Exercise 2's condition.** `while running < quota` shrinks toward the
  *longest* window, which is the other shape entirely. If your loop feels like
  it is fighting you, check which direction you are shrinking in before
  changing anything else.

- **Applying this to a log with negatives.** The drill guarantees non-negative
  readings; a real caller might not. Feed it `[5, -3, 5]` with a quota of `7`
  and watch it miss the whole-log answer. Nothing raises. That is the failure
  mode worth seeing once, deliberately.

## Under the hood

<details>
<summary>Under the hood — why non-negativity is the whole argument, and what you use when it fails</summary>

**The correctness argument, stated properly.**

The window is correct because of one lemma: for a fixed `right`, the set of
`left` values for which `sum(inflow[left:right + 1]) >= quota` is a *prefix* of
the possible lefts. That is, if some `left` qualifies, so does every smaller
one. It follows directly from non-negativity — shrinking from the left removes
a non-negative number, so the total can only fall.

Because the qualifying lefts form a prefix, there is a single boundary, and
walking `left` forward until it crosses that boundary finds the shortest
qualifying window ending at `right`. Do that for every `right` and you have
considered every window that could possibly be the answer, without looking at
most of them.

Take non-negativity away and the qualifying lefts stop being a prefix. `[5, -3,
5]` with a quota of 7 has `left = 0` qualifying (total 7) and `left = 1` not
(total 2) — and the algorithm, having found that `left = 1` fails, moves on.
There is no boundary to find, because the predicate is not monotone.

**What you use instead.** Prefix sums plus a hash map. Build
`prefix[i] = sum(inflow[:i])`; then the run `inflow[a:b]` totals
`prefix[b] - prefix[a]`. "Is there a run ending at `b` totalling at least the
quota?" becomes "is there an `a` with `prefix[a] <= prefix[b] - quota?", which
is a lookup rather than a walk. That is `O(n log n)` with a sorted structure,
or `O(n)` for the exact-sum variant with a dictionary. It is Week 2's pattern,
not this one, and recognising which of the two applies is exactly the
discrimination this week is training.

**Cost, stated precisely.**

Time is `O(n)`, amortised: `right` advances `n` times, `left` advances at most
`n` times across the whole run, and every operation in between is constant.
Best, average and worst are all `O(n)` — there is no early exit, because a
shorter run may appear at any point in the log, so you cannot stop before the
end.

Space is `O(1)`: a running total, two indices, and a three-integer best record.
Nothing grows with the input. Contrast the alternatives: the double loop is
`O(n^2)` time and `O(1)` space; prefix sums plus binary search is `O(n log n)`
time and `O(n)` space, and tolerates negatives. The window is strictly best on
both axes *given non-negativity*, and that qualifier is the whole sentence.

**The `2^31` remark, in full.** The quota bound goes to five billion, which
does not fit in a signed 32-bit integer. Python does not care — `int` is
arbitrary precision, and the only cost is that arithmetic on very large values
is slower than on machine words. A C++ or Java translation would need `long
long` or `long` for both the quota and the running total, and the running total
is the one people forget, because it looks like it should be small. Integer
overflow in a running sum is silent, wraps to a negative number, and produces
an answer that looks like a legitimate near-miss.

**Three sub-shapes, one family.** This page is the "shortest" shape. Exercises
2 and 5 are the "longest" shape. There is a third — "how many windows satisfy
the property?" — which shrinks like the longest shape but adds
`right - left + 1` to a total instead of comparing lengths. That one appears in
the [mini-project's Problem 5](../mini-project/README.md) and again in
[homework Problem 2](../homework/problem-02-courier-zone-count.md), where two
of them are subtracted from each other to answer an "exactly K" question.
Recognising which of the three you are in, from the wording of the prompt, is
worth more than any individual implementation.

</details>

## Acceptance checklist

- [ ] `python exercise-04-shortest-catchment.py` prints six rows then `All checks passed.`
- [ ] The output matches the Expected output block character for character.
- [ ] `shortest_catchment([4, 6, 1, 7, 8], 10)` returns `(3, 2)`, and you can say why.
- [ ] `shortest_catchment([0, 0, 12, 0], 12)` returns `(2, 1)`.
- [ ] `shortest_catchment([1, 1, 1], 10)` returns `None`, not `0`.
- [ ] The shrink loop is a `while`, its condition uses `>=`, and its body records before it subtracts.
- [ ] No call to `sum` appears inside your loop.
- [ ] You can state, in one sentence, what breaks if a reading is negative.
- [ ] The function has type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 3 exercise 4: the shortest catchment`.

## Stretch

- **Count the runs whose total is at most a cap.** This is the third sub-shape,
  and the combine step is the whole difference.

  ```python
  def runs_within_cap(inflow: list[int], cap: int) -> int:
      """Return how many runs of one or more days total at most `cap`."""
      left, running, total = 0, 0, 0
      for right, litres in enumerate(inflow):
          running += litres
          while running > cap:
              running -= inflow[left]
              left += 1
          total += right - left + 1
      return total
  ```

  ```text
  [4, 6, 1, 7, 8] cap 10 -> 7
  [0, 0, 12, 0]   cap 12 -> 10
  ```

  The invariant flipped to `running <= cap`, the recording moved back to after
  the shrink, and the answer accumulates instead of competing. Once the
  invariant holds at `right`, every run ending at `right` and starting at or
  after `left` also holds it — which is why one addition replaces an
  enumeration.

- **Return the total alongside the run.** You already computed it; the change
  is in what you unpack.

  ```python
  def shortest_catchment_detail(inflow: list[int], quota: int) -> tuple[int, int, int] | None:
      """Return (start, days, total) for the shortest qualifying run."""
      answer = shortest_catchment(inflow, quota)
      if answer is None:
          return None
      start, days = answer
      return (start, days, sum(inflow[start : start + days]))
  ```

  ```text
  ([4, 6, 1, 7, 8], 10) -> (3, 2, 15)
  ```

- **Break the assumption on purpose.** Run your solution on `[5, -3, 5]` with a
  quota of `7`. It returns `None`; the correct answer is `(0, 3)`. Write that
  case down in your notes with the reason beside it. A pattern you have watched
  fail is a pattern you will not misapply.

**Practice elsewhere.** The same pattern appears as [LeetCode 209 · Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) if you want a judge to run against. The contract there returns a bare length and uses `0` for the impossible case, so it exercises neither the tie-break nor the position tracking.

Next: [Exercise 5 — The Cold-Chain Load](./exercise-05-cold-chain-load.md).
