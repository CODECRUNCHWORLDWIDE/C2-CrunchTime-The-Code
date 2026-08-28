# Exercise 1 — The Busiest Staffing Block

> **Topic:** a fixed-size sliding window over a list of counts, and the running total that makes it fast
> **Lecture:** [01 — The Sliding Window Pattern](../lecture-notes/01-the-sliding-window-pattern.md)
> **Difficulty:** Easy
> **Target time:** 45 minutes
> **Why this one:** this is the gentlest window there is, and it is where you learn the move the rest of the week depends on — *fix the total up, do not add it up again*. The page also has one twist in its contract, a tie-break, which is there to teach you to read the small print before you write the loop. Miss it and your arithmetic will be perfect and your answer will still be wrong.

## The Brief

A 24-hour urgent-care clinic counts how many patients walk in during each
15-minute interval of the day, and writes the counts down in order. So the log
is a plain list of numbers: the first number is the first quarter of an hour,
the second number is the next one, and so on.

The rota manager staffs the floor in **blocks**. A block is `k` intervals in a
row — not any old `k` intervals, but `k` that sit next to each other. She wants
to know where the pressure is, so she can put more people on the floor there.

Here is the picture. Think of a piece of card with a window cut in it, `k`
intervals wide. Lay the card over the log so the window shows the first `k`
numbers, and add them up. Now slide the card one step to the right. One number
has dropped off the left end of the window, and one new number has appeared at
the right. That is the whole idea, and it is why the pattern is called a
**sliding window**.

The lazy way to get each block's total is to add the `k` numbers up again every
time you slide. It works. It is also enormous waste, because `k - 1` of those
numbers were already in the total you just computed. The fast way is one line:

```text
new total = old total + the number that came in - the number that dropped out
```

That is two arithmetic operations per slide instead of `k`. On this page you
write both versions, and the program prints exactly how much extra work the
lazy one does.

**Your job.** Return the **starting index** of the block of `k` consecutive
intervals with the largest total. A position, not a total.

Two pieces of small print. If several blocks tie on total, return the
**latest** such starting index — the manager staffs the most recent peak,
because the older one has already been absorbed by the shift that is on the
floor right now. And if `k` is bigger than the log, or the log is empty, there
is no block at all, so return `None`.

## Starter

Create `exercise-01-staffing-block.py` and paste this in. Fill in every `TODO`.

```python
"""exercise-01-staffing-block.py — the busiest staffing block.

Find the block of k consecutive intervals with the most walk-ins, without
adding the same numbers up over and over.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""


def busiest_block(arrivals: list[int], k: int) -> int | None:
    """Return the start index of the k-interval block with the most arrivals.

    Args:
        arrivals: Walk-in counts, one per 15-minute interval, in time order.
        k: How many consecutive intervals a staffing block covers.

    Returns:
        The start index of the busiest block, ties going to the latest such
        start. None when the block does not fit inside the log.
    """
    # TODO: guard the no-block case first.
    # TODO: build the first window's total from arrivals[:k], and seed the
    #       best-so-far FROM THAT TOTAL, not from zero.
    # TODO: slide. Each step: add the number coming in, subtract the one going
    #       out, work out the window's start index, and compare.
    ...


def busiest_block_rescan(arrivals: list[int], k: int) -> int | None:
    """The same answer, computed the expensive way. Kept only for comparison.

    Args:
        arrivals: Walk-in counts, one per 15-minute interval, in time order.
        k: How many consecutive intervals a staffing block covers.

    Returns:
        The same value `busiest_block` returns, reached by adding every block
        up from scratch.
    """
    # TODO: for every valid start, add up arrivals[start:start + k] and compare.
    #       Write this one on purpose. It is the version the constraint rejects,
    #       and the self-check uses it to prove your fast version agrees.
    ...


def additions_rescan(n: int, k: int) -> int:
    """How many additions the rescan performs on a log of n intervals.

    Args:
        n: Length of the log.
        k: Block size.

    Returns:
        One addition fewer than k for every block, times the number of blocks.
    """
    # TODO: adding k numbers costs k - 1 additions. How many blocks are there?
    ...


def additions_sliding(n: int, k: int) -> int:
    """How many additions the sliding window performs on a log of n intervals.

    Args:
        n: Length of the log.
        k: Block size.

    Returns:
        The cost of the first block, plus one add and one subtract per slide.
    """
    # TODO: the first window, then two operations for each of the n - k slides.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    log = [4, 1, 7, 2, 5, 3, 3, 6]
    totals = [sum(log[i : i + 3]) for i in range(len(log) - 2)]
    print(f"log {log}, k=3")
    print(f"  block totals : {totals}")
    print(f"  busiest block starts at index {busiest_block(log, 3)}")
    print()

    print(f"four-way tie at 9 in [1, 8, 1, 1, 8, 1], k=2 -> {busiest_block([1, 8, 1, 1, 8, 1], 2)}")
    print(f"all-zero log [0, 0, 0], k=2                  -> {busiest_block([0, 0, 0], 2)}")
    print(f"block longer than the log [5, 5], k=3        -> {busiest_block([5, 5], 3)}")
    print()

    n, k = 2_000, 500
    rescan, sliding = additions_rescan(n, k), additions_sliding(n, k)
    print(f"additions on a {n}-interval log with k={k}")
    print(f"  rescan  : {rescan:>9,}")
    print(f"  sliding : {sliding:>9,}")
    print(f"  the rescan does {rescan // sliding} times the work for the same answer")
    print()

    assert busiest_block([4, 1, 7, 2, 5, 3, 3, 6], 3) == 2
    assert busiest_block([1, 8, 1, 1, 8, 1], 2) == 4
    assert busiest_block([2, 0, 2, 0, 2], 2) == 3
    assert busiest_block([0, 0, 0], 2) == 1
    assert busiest_block([9], 1) == 0
    assert busiest_block([5, 5], 3) is None
    assert busiest_block([], 1) is None

    for case, size in [([4, 1, 7, 2, 5, 3, 3, 6], 3), ([1, 8, 1, 1, 8, 1], 2), ([2, 0, 2, 0, 2], 2), ([0, 0, 0], 2)]:
        assert busiest_block(case, size) == busiest_block_rescan(case, size)

    print("All checks passed.")
```

Three words you need before you start.

**Window.** The stretch of the list you are currently looking at. Here it is
always exactly `k` long. In later problems it grows and shrinks.

**Invariant.** The thing you promise stays true every time round the loop. Here
it is: *`window_total` is the sum of the `k` intervals ending at `right`.* If
that promise holds at every step, the answer falls out. Break it once — by
adding without subtracting, say — and everything afterwards is quietly wrong.

**Slide.** Moving the window one place to the right. Exactly one number enters
and exactly one leaves, which is why fixing the total up costs two operations
however big `k` is.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-03-sliding-window/exercises/exercise-01-staffing-block.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `busiest_block(arrivals, k)` returns an **index**, not a total.
2. Ties go to the **latest** qualifying start. `busiest_block([1, 8, 1, 1, 8, 1], 2)`
   is `4`, not `0`.
3. `busiest_block` returns `None` — not `-1`, not `0` — when `k > len(arrivals)`.
   An empty log is covered by the same rule.
4. A busiest total of zero is a real answer. `busiest_block([0, 0, 0], 2)` is `1`.
5. `busiest_block` updates its running total incrementally. Nothing inside its
   loop may call `sum`.
6. `busiest_block_rescan` gives the same answers, computed the slow way. The
   self-check compares them on four logs.
7. `additions_rescan(2000, 500)` returns `748_999` and
   `additions_sliding(2000, 500)` returns `3_499`.
8. Every function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(arrivals) <= 400_000`.** A year of 15-minute intervals is about
  35,000, so this covers a decade of logs with room to spare. That size is
  chosen to rule the rescan out rather than merely to discourage it: with `k`
  near `n`, `sum(arrivals[i:i + k])` inside the loop is about `4 x 10^10`
  additions. At the tens of millions of additions a second CPython manages,
  that is over an hour for an answer a single pass gives you instantly.

- **`1 <= k`.** A block of zero intervals is not a shift, so the contract
  excludes it rather than inventing an answer for it. Settling this in the
  brief is cheaper than discovering halfway through the loop that `k = 0` has
  no sensible meaning.

- **`0 <= arrivals[i] <= 2_000`.** Arrivals are counts, so they are never
  negative — but they are **frequently zero**, because at four in the morning
  nobody comes in. That is not decoration. Whole stretches of zeros are what
  catch a solution that seeds `best_total = 0` and only updates on a strict
  improvement: on an all-zero log the update never fires and the function
  returns whatever index it happened to start with. Seed from the first window
  and the problem cannot arise.

- **Update the total, do not rebuild it.** This is a rule about the loop body,
  and it is the whole exercise. One add and one subtract per slide, whatever
  `k` is.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-01-staffing-block.py
placeholder
```

Read the last block of numbers slowly, because it is the argument for the whole
pattern. Same log, same answer, same `k` — and the rescan performs 214 times as
many additions to get there. That ratio grows with `k`: it is roughly `k / 2`.
Double the block size and you double the gap.

## Steps

1. Create the file, paste the starter, and run it before writing anything:
   `python exercise-01-staffing-block.py`. You get a `TypeError` on the
   formatting line, or a bare `AssertionError` further down. That is the
   correct starting point — it proves the self-check is real.
2. Write the guard first. One line: if the block does not fit, there is no
   answer.
3. Build the first window's total with `sum(arrivals[:k])`. This is the one
   place `sum` belongs, because there is no previous total to fix up.
4. Seed `best_total` from that first total and `best_start` from `0`. Not from
   zero, and not from `None`.
5. Write the slide. For each `right` from `k` to the end:
   `window_total += arrivals[right] - arrivals[right - k]`. Say out loud which
   interval just entered and which just left, then check that against the
   indices you typed.
6. Work out the window's start. After adding `arrivals[right]`, the window
   covers `arrivals[right - k + 1 : right + 1]`, so the start is
   `right - k + 1`.
7. Compare. The tie-break decides the operator, and the operator is the whole
   drill. Read Requirement 2 again before you choose.
8. Write `busiest_block_rescan`. Yes, on purpose. Two reasons: the self-check
   uses it to prove your fast version agrees, and writing the slow one is how
   you feel the difference rather than being told about it.
9. Fill in the two cost functions and run the file. Look at the ratio.

## The Solution

```python
placeholder
```

**The guard is one line, and it covers two cases at once.**

```python
if k > len(arrivals):
    return None
```

An empty log needs no separate branch. `k` is at least 1 by the contract and
`len([])` is 0, so `1 > 0` is already true and the empty log leaves through the
same door. When one condition covers two cases, saying so out loud is worth a
point in an interview — it shows you checked rather than got lucky.

**Seeding from the first window is what makes zeros safe.**

```python
window_total = sum(arrivals[:k])
best_total = window_total
best_start = 0
```

Seeding `best_total = 0` looks harmless and is not. On `[0, 0, 0]` with `k = 2`
every block totals zero, so a strict-improvement update never fires, and the
function returns whatever `best_start` was initialised to. The bug is invisible
on any log containing a positive number, which is exactly why it survives
testing. Starting from a real window means there is always an incumbent, and
the incumbent is always a real answer.

**The slide is the pattern, and it is one line.**

```python
window_total += arrivals[right] - arrivals[right - k]
```

`arrivals[right]` is the interval entering on the right. `arrivals[right - k]`
is the one dropping off the left. If you doubt the `- k`, count on your fingers
with `k = 3` and `right = 3`: the window is now intervals 1, 2 and 3, so the one
that left is interval 0, and `3 - 3` is 0. The cost of this line does not depend
on `k` at all, which is the entire reason the function is linear.

**`>=`, not `>`, and that is the graded character.** The contract sends ties to
the *latest* start, so a block that merely ties the incumbent must still take
its place. With `>` all four tie examples return `0` — arithmetic perfect,
answer wrong. Exercise 2 needs the opposite operator, and the two drills
disagree on purpose: you are meant to read the rule rather than memorise a
symbol.

**The start index is `right - k + 1`, and the `+ 1` is where people fall over.**
After the addition, the window's last interval is `right` and it holds `k`
intervals, so it begins `k - 1` places earlier. `right - (k - 1)` is
`right - k + 1`. Writing `right - k` gives an index one too small on every
single step, which reliably produces an answer one off — plausible enough to
survive a glance.

**The rescan is correct and it is still the wrong answer.** Both functions
return the same index on every test. The difference is entirely in the work
done to get there, and the constraint on the input size is what turns
"wasteful" into "does not finish". That distinction is worth carrying: on this
page correctness and efficiency are separate properties, and a problem can be
specified so that only one of them counts as solved.

**The cost functions are arithmetic, not measurements.** Adding `k` numbers
takes `k - 1` additions, and there are `n - k + 1` blocks, so the rescan does
`(n - k + 1)(k - 1)` of them. The window pays `k - 1` once for the first block
and then two operations for each of the `n - k` slides. Counting operations
rather than timing them means the numbers come out the same on every machine,
which is what makes them worth quoting.

## Download and run

Download
[exercise-01-staffing-block-solution.py](./exercise-01-staffing-block-solution.py)
and run it:

```bash
python exercise-01-staffing-block-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-01-staffing-block.py`.

## Common bugs to catch

- **`TypeError: '>' not supported between instances of 'NoneType' and 'int'`.**
  Your function fell off the end without returning:

  ```text
  Traceback (most recent call last):
      if window_total > best_total:
         ^^^^^^^^^^^^^^^^^^^^^^^^^
  TypeError: '>' not supported between instances of 'NoneType' and 'int'
  ```

  A Python function with no `return` on the path it took hands back `None`. The
  usual cause is a `return best_start` indented one level too deep, so it sits
  inside the `for` and only runs when the loop body does.

- **`busiest_block([1, 8, 1, 1, 8, 1], 2)` returns `0` instead of `4`.** You
  wrote `if window_total > best_total`. There is no traceback; the code is
  valid and answers a different question perfectly. Four blocks total 9, and
  the first one keeps the crown because a strict `>` never lets a tie displace
  it. This is the single graded bug of the drill.

- **`busiest_block([0, 0, 0], 2)` returns `0` instead of `1`.** The same
  operator problem, showing up on a log where *every* block ties. If you also
  seeded `best_total = 0`, this case can give the right answer for the wrong
  reason on some logs and the wrong answer on others, which is worse than
  failing outright.

- **`busiest_block([0, 0, 0], 2)` returns `None`.** You treated "the maximum is
  zero" as "there is no maximum". Those are different facts. `None` means the
  block does not fit; a total of zero means three quiet quarter-hours. A caller
  writing `if result:` cannot tell `0` from `None` either, which is why the
  contract picks a value that is not an index at all.

- **`IndexError: list index out of range`.**

  ```text
  Traceback (most recent call last):
      window_total += arrivals[right] - arrivals[right - k]
                      ~~~~~~~~^^^^^^^
  IndexError: list index out of range
  ```

  Your loop ran past the end of the list — usually `range(k, len(arrivals) + 1)`
  instead of `range(k, len(arrivals))`. There is a quieter cousin of this bug:
  start the loop at `0` rather than `k` and `right - k` goes *negative*, which
  does not raise at all. A negative index reads from the end of the list, so
  your morning total silently has last night's arrivals subtracted from it.
  Python will not warn you; only a test will.

- **`AssertionError` on the rescan comparison.** Your two implementations
  disagree, which means one of them has the wrong tie-break. Print both indices
  and the block totals side by side; the disagreement will be on a tie.

- **The answer is consistently one too small.** You wrote `right - k` for the
  start instead of `right - k + 1`. Check it against a case you can count in
  your head: `[9]` with `k = 1` must return `0`.

- **`sum` inside the loop.** No exception, right answers, and the drill not
  done. Requirement 5 is checkable by reading: if `sum` appears anywhere inside
  `busiest_block`'s `for`, the window is a costume rather than a technique.

## Under the hood

<details>
<summary>Under the hood — where the time actually goes, and the one input that breaks the trick</summary>

**The cost, counted rather than asserted.**

Building the first window is `k - 1` additions. Each of the `n - k` slides is
one addition and one subtraction. Total:

```text
(k - 1) + 2(n - k)  =  2n - k - 1
```

which is `O(n)` — and, pleasingly, it gets *cheaper* as `k` grows, because a
bigger window means fewer slides. The rescan is `(n - k + 1)(k - 1)`, which is
`O(n·k)`, and is at its worst when `k` is around `n / 2`.

The ratio between them is roughly `k / 2`. That is why the page prints it at
`k = 500`: 214 is close enough to 250 to show the shape, and the gap between
the two is the fixed cost of the first window, which does not scale.

Space is `O(1)` for the window and `O(k)` for the rescan — because
`arrivals[i:i + k]` *builds a new list of `k` integers* on every iteration and
then throws it away. A slice in Python is a copy, not a view. That allocation
is a real part of why the rescan is slow, and it is invisible in the `O(n·k)`
notation.

**The one input that breaks the trick, and it is not on this page.**

The incremental update assumes that adding and subtracting gets you back
exactly where you would otherwise have been. For Python `int` that is
guaranteed: integers are arbitrary precision, so `a + b - b == a` always.

It is not guaranteed for floats. Slide a window over floating-point readings,
adding and subtracting as you go, and rounding error accumulates across the
whole pass — after a few hundred thousand slides the running total can drift
visibly from the true sum of the current window. The standard fixes are a
**prefix-sum array**, where each window total is the difference of two exactly
stored values, or `math.fsum` per window at the cost of the rescan. Neither is
needed here, because arrivals are counts. Knowing *why* it is not needed is
worth more than the trick itself.

**Why `>=` here and `>` in Exercise 2.**

The comparison operator is not a matter of taste. It is dictated by the
tie-break, and the tie-break comes from the domain. Here the manager wants the
most recent peak, so a later block with an equal total is genuinely preferable
and must displace the incumbent: `>=`. In Exercise 2 the contract prefers the
earliest span, so a tie must be refused: `>`. Two drills, opposite rules,
identical loops.

**A third option you will meet later.** For "the largest value in every window
of size `k`" — a maximum rather than a sum — this trick does not work at all,
because removing an element cannot be undone by arithmetic: once the largest
value leaves the window, nothing you stored tells you what the next largest
was. That problem needs a **monotonic deque**, and it turns up in Week 9.
Noticing which window statistics are cheaply reversible and which are not is a
genuinely useful instinct.

</details>

## Acceptance checklist

- [ ] `python exercise-01-staffing-block.py` prints the three sections then `All checks passed.`
- [ ] The output matches the Expected output block character for character.
- [ ] `busiest_block` returns `None` for `([5, 5], 3)` and for `([], 1)`.
- [ ] `busiest_block([0, 0, 0], 2)` returns `1`, not `0` and not `None`.
- [ ] No call to `sum` appears inside `busiest_block`'s loop.
- [ ] `busiest_block` and `busiest_block_rescan` agree on all four comparison logs.
- [ ] You can say out loud, without looking, which interval `arrivals[right - k]` is.
- [ ] Every function has type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 3 exercise 1: the busiest staffing block`.

## Stretch

- **Return the total as well as the position.**

  ```python
  def busiest_block_detail(arrivals: list[int], k: int) -> tuple[int, int] | None:
      """Return (start, total) for the busiest block, ties going to the latest start."""
      start = busiest_block(arrivals, k)
      if start is None:
          return None
      return (start, sum(arrivals[start : start + k]))
  ```

  ```text
  ([4, 1, 7, 2, 5, 3, 3, 6], 3) -> (2, 14)
  ([5, 5], 3)                   -> None
  ```

  One `sum` at the end, on one window, is `O(k)` once — not `O(k)` per step. Be
  ready to say why that is fine while the same call inside the loop is not.

- **Find the quietest block instead.** Change one comparison and one seed. Then
  ask yourself what the tie-break should be, and notice that the contract does
  not tell you — which means, in a real interview, you ask.

  ```python
  def quietest_block(arrivals: list[int], k: int) -> int | None:
      """Return the start index of the k-interval block with the fewest arrivals."""
      if k > len(arrivals):
          return None
      window_total = sum(arrivals[:k])
      best_total, best_start = window_total, 0
      for right in range(k, len(arrivals)):
          window_total += arrivals[right] - arrivals[right - k]
          if window_total <= best_total:
              best_total, best_start = window_total, right - k + 1
      return best_start
  ```

  ```text
  ([4, 1, 7, 2, 5, 3, 3, 6], 3) -> 3
  ```

  The [mini-project's Problem 1](../mini-project/README.md) is this idea with a
  different return type, so the twenty minutes you spend here come back.

- **Time the two versions on a real log.** Build a list of 200,000 counts, set
  `k = 5000`, and run both under `time.perf_counter`. Predict the ratio from
  the cost functions before you look. Being roughly right about a runtime
  *before* measuring it is a skill, and it is one you can practise in a minute.

**Practice elsewhere.** The same pattern appears as [LeetCode 643 · Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/) if you want a judge to run against. The contract there is different — it returns a value rather than a position, and says nothing about ties — so read it as a second problem, not as this one.

When your window slides, move on to
[Exercise 2 — The Longest Clean Run](./exercise-02-longest-clean-run.md).
