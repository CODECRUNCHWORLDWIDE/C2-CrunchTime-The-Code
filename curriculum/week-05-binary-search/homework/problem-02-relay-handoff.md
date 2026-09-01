# Homework Problem 2 — The Relay Handoff

> **Topic:** binary search on the answer, minimise-the-maximum, where the budget is a count of blocks rather than a count of days
> **Lecture:** [02 — Binary Search on the Answer](../lecture-notes/02-binary-search-on-the-answer.md)
> **Difficulty:** Medium
> **Target time:** 60 minutes
> **Why this one:** the phrase "minimise the maximum" appears in interview prompts constantly, and it always compiles down to the same loop you wrote in [Problem 1](./problem-01-kiln-firing-schedule.md). The twist here is a predicate that counts blocks and compares with `<=` when the contract says "exactly" — and being able to explain that mismatch is what the problem is really testing.

## The Brief

A courier company runs a long parcel route as a relay. The route is a list of
**legs**, in order, each with a distance in kilometres. The route is split
among **exactly** `riders` riders. Each rider takes a **run of consecutive
legs**, and every rider must get **at least one leg** — a rider with nothing
to do still has to be paid.

Whoever ends up with the longest total has the worst day. Make that longest
total as small as you can, and return it.

```
legs:  8  3  9  4  6  2          three riders

[8, 3] | [9] | [4, 6, 2]   ->  11,  9, 12   worst rider: 12
[8] | [3, 9] | [4, 6, 2]   ->   8, 12, 12   worst rider: 12
[8, 3, 9] | [4] | [6, 2]   ->  20,  4,  8   worst rider: 20
```

The first two arrangements tie at 12, and no arrangement of three riders does
better. So the answer for three riders is `12`.

Notice what "minimise the maximum" does **not** mean: it does not mean making
the riders equal. In the two-rider case the best split is `[8, 3, 9]` and
`[4, 6, 2]` — twenty kilometres against twelve, wildly unequal, and still
optimal, because any other cut makes the longer side longer.

Now the search. Pick a **cap** — a distance no rider may exceed — and ask
whether the route can be covered without breaking it. A cap of 12 works with
three riders. A cap of 11 needs four. And once a cap is big enough, every
bigger cap is too, so there is one flip and it is the answer.

Two contract decisions:

- The split is into **exactly** `riders` non-empty blocks. So `riders` bigger
  than the number of legs is impossible and returns `None`, and so does
  `riders` below 1 on a non-empty route.
- An empty route with zero riders returns `0`. An empty route with any other
  rider count returns `None`.

And one thing worth working out before you write code: your feasibility test
should count the **fewest** blocks a cap allows and check `count <= riders`,
not `count == riders`. Any split into fewer blocks can be cut finer — there
are always legs to cut between, as long as there are enough legs — so
"needs at most this many riders" is the right question and "needs exactly"
is not.

## Starter

Save this as `problem-02-relay-handoff.py` and fill in every `TODO`.

```python
"""problem-02-relay-handoff.py — the fairest relay split.

Binary search on the answer, minimise-the-maximum flavour.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

# ---- Given data ----
ROUTE: list[int] = [8, 3, 9, 4, 6, 2]


# ---- Your task ----
def blocks_needed(legs: list[int], cap: int) -> int:
    """Return the fewest contiguous blocks whose sums all stay within `cap`.

    Args:
        legs: Leg distances in kilometres, in route order.
        cap: The distance no single rider may exceed. At least max(legs).

    Returns:
        The number of blocks the greedy left-to-right sweep closes.
    """
    # TODO: one pass; start a new block when the next leg would break the cap
    # TODO: a route with legs in it always needs at least one block
    ...


def fairest_relay_split(legs: list[int], riders: int) -> int | None:
    """Return the smallest possible distance for the hardest-worked rider.

    Args:
        legs: Leg distances in kilometres, in route order.
        riders: How many riders the route is split among, exactly.

    Returns:
        The minimum achievable largest block sum, 0 for an empty route with
        zero riders, or None when the split cannot be made at all.
    """
    # TODO: the contract branches first — empty route, impossible rider count
    # TODO: lo = max(legs), hi = sum(legs). Why is lo not 1?
    # TODO: smallest-such-that search, comparing the block count with <=
    ...


# ---- Self-check ----
if __name__ == "__main__":
    for team in (1, 2, 3, 5, 7):
        print(f"{team} riders -> {fairest_relay_split(ROUTE, team)}")

    assert fairest_relay_split(ROUTE, 3) == 12
    assert fairest_relay_split(ROUTE, 2) == 20
    assert fairest_relay_split(ROUTE, 4) == 11
    assert fairest_relay_split(ROUTE, 5) == 9
    assert fairest_relay_split(ROUTE, 6) == 9
    assert fairest_relay_split(ROUTE, 1) == 32
    assert fairest_relay_split(ROUTE, 7) is None
    assert fairest_relay_split(ROUTE, 0) is None
    assert fairest_relay_split([0, 0, 0], 2) == 0
    assert fairest_relay_split([5, 0, 5], 2) == 5
    assert fairest_relay_split([], 0) == 0
    assert fairest_relay_split([], 1) is None
    assert ROUTE[0] == 8  # the route was never reordered
    print("All checks passed.")
```

One idea you need before you start.

**The floor of the answer is `max(legs)`.** A leg cannot be split between two
riders, so whoever takes the longest leg rides at least that far, whatever the
arrangement. That makes `max(legs)` the smallest cap worth testing — and, more
importantly, it makes every cap below it *infeasible*, so starting the search
lower would waste iterations testing caps that can never work.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-05-binary-search/homework/problem-02-relay-handoff.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `blocks_needed(legs, cap)` returns the fewest contiguous blocks whose sums
   all stay within `cap`, in one pass.
2. `fairest_relay_split(legs, riders)` returns the smallest achievable value of
   the largest block sum.
3. It returns `None` when `riders > len(legs)`, and when `riders < 1` on a
   non-empty route.
4. It returns `0` for an empty route with zero riders, and `None` for an empty
   route with any other rider count.
5. The interval is `lo = max(legs)` and `hi = sum(legs)`, and you can justify
   both ends.
6. The predicate compares the block count with `<=`, and you can say in one
   sentence why not `==`.
7. The search uses the half-open package: guard `lo < hi`, `hi = mid` on
   success, `lo = mid + 1` on failure.
8. Both functions keep their type hints and docstrings.

## Constraints

- **`0 <= len(legs) <= 100_000`.** A long-haul route. The predicate is one
  sweep, so the search is `O(n log T)` with `T` the route total. A predicate
  that re-scans per block is `O(n²)` and will not finish here.

- **`0 <= legs[i] <= 10_000`.** Distances may be **zero** — two handoffs at the
  same depot, with nothing between them. This is the bound that catches a
  solution which sets `lo = 1`: on an all-zero route the answer is `0`, and
  `lo = 1` returns `1`. Set `lo = max(legs)` and the zero case comes out right
  without a special branch.

- **`0 <= riders <= 100_000`.** Rider counts above the leg count are legal
  input and return `None` — they must not raise. Zero riders on a non-empty
  route is the same kind of answer.

- **Legs are never reordered or split.** The blocks are runs of consecutive
  legs, which is what makes the greedy sweep valid and what makes `max(legs)`
  a genuine floor. Allow reordering and this stops being a binary-search
  problem entirely — it becomes bin packing, which is a much harder thing.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-02-relay-handoff.py
1 riders -> 32
2 riders -> 20
3 riders -> 12
5 riders -> 9
7 riders -> None
All checks passed.
```

The five-rider row is the floor showing itself. The answer has bottomed out at
`max(legs) = 9`, and adding a sixth rider changes nothing: two different rider
counts, one answer, because no split can ever go below the longest single leg.
That is correct rather than a bug, and being able to say why in one sentence
is worth more than the code.

## Steps

1. Save the starter and run it. Both functions return `Ellipsis`. Expected.
2. Write `blocks_needed` first and test it alone on the sample route: at a cap
   of 12 it should give `3`, at 11 it should give `4`, at 20 it should give
   `2`, and at 32 it should give `1`.
3. Check the shape of that sweep carefully. It starts at one block and opens a
   new one whenever the next leg would break the cap. On an all-zero route with
   a cap of zero it must still return `1`, not `0`.
4. Now the contract branches. Empty route: `0` if `riders == 0`, else `None`.
   Non-empty route: `None` when `riders < 1` or `riders > len(legs)`.
5. Set `lo, hi = max(legs), sum(legs)`. Say both justifications out loud before
   typing: the longest leg cannot be split, and one rider taking everything
   always works.
6. Run the smallest-such-that search: `hi = mid` when
   `blocks_needed(legs, mid) <= riders`, else `lo = mid + 1`.
7. Run it, then trace `riders = 3` at caps 11 and 12 by hand and check your
   trace against the walk-through in The Solution.
8. Trace `[5, 0, 5]` with two riders and work out why the zero-length leg rides
   free.

## The Solution

```python
"""problem-02-relay-handoff-solution.py - the fairest relay split.

Binary search on the answer, minimise-the-maximum flavour. The predicate
counts the FEWEST blocks a cap allows and tests `blocks <= riders`, not
`== riders`: a split into fewer blocks can always be cut finer as long as
there are legs left to cut.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""

# ---- Given data ----
ROUTE: list[int] = [8, 3, 9, 4, 6, 2]


# ---- Your task ----
def blocks_needed(legs: list[int], cap: int) -> int:
    """Return the fewest contiguous blocks whose sums all stay within `cap`.

    Args:
        legs: Leg distances in kilometres, in route order.
        cap: The distance no single rider may exceed. At least max(legs).

    Returns:
        The number of blocks the greedy left-to-right sweep closes.
    """
    blocks = 1
    carried = 0
    for leg in legs:
        if carried + leg > cap:
            blocks += 1
            carried = 0
        carried += leg
    return blocks


def fairest_relay_split(legs: list[int], riders: int) -> int | None:
    """Return the smallest possible distance for the hardest-worked rider.

    Args:
        legs: Leg distances in kilometres, in route order.
        riders: How many riders the route is split among, exactly.

    Returns:
        The minimum achievable largest block sum, 0 for an empty route with
        zero riders, or None when the split cannot be made at all.
    """
    if not legs:
        return 0 if riders == 0 else None
    if riders < 1 or riders > len(legs):
        return None

    lo, hi = max(legs), sum(legs)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if blocks_needed(legs, mid) <= riders:
            hi = mid
        else:
            lo = mid + 1
    return lo


# ---- Self-check ----
if __name__ == "__main__":
    for team in (1, 2, 3, 5, 7):
        print(f"{team} riders -> {fairest_relay_split(ROUTE, team)}")

    assert fairest_relay_split(ROUTE, 3) == 12
    assert fairest_relay_split(ROUTE, 2) == 20
    assert fairest_relay_split(ROUTE, 4) == 11
    assert fairest_relay_split(ROUTE, 5) == 9
    assert fairest_relay_split(ROUTE, 6) == 9
    assert fairest_relay_split(ROUTE, 1) == 32
    assert fairest_relay_split(ROUTE, 7) is None
    assert fairest_relay_split(ROUTE, 0) is None
    assert fairest_relay_split([0, 0, 0], 2) == 0
    assert fairest_relay_split([5, 0, 5], 2) == 5
    assert fairest_relay_split([], 0) == 0
    assert fairest_relay_split([], 1) is None
    assert ROUTE[0] == 8  # the route was never reordered
    print("All checks passed.")
```

**The four-part reframe.**

> *Reframe:* find the smallest cap `c` such that the route can be covered by
> at most `riders` contiguous blocks, none exceeding `c`.
> *Interval:* `lo = max(legs)`, because a leg is indivisible so no cap below
> the longest one is achievable; `hi = sum(legs)`, because one rider taking
> everything always works, so the top of the interval is guaranteed feasible.
> *Predicate:* `blocks_needed(legs, c) <= riders`. Monotone in `c`, because
> raising the cap never forces the sweep to open a block it would otherwise
> have kept open.
> *Return:* the post-loop `lo`, the smallest cap that fits inside the rider
> count.

**`<=` rather than `==`, and this is the sentence to have ready.** The
predicate counts the *minimum* number of blocks a cap allows. If that minimum
is smaller than the rider count, the split is still possible: take any block
with more than one leg in it and cut it, which produces one more block and
never makes any block longer. You can keep doing that until you have exactly
`riders` blocks, and there are enough legs to do it because the guard already
established `riders <= len(legs)`. So "needs at most `riders`" and "can be done
with exactly `riders`" are the same condition here, and the `<=` version is
the one that is monotone.

**Why `lo = max(legs)` and not `1`.** Two reasons, and the second is the one
the tests are checking. First, no cap below the longest leg is ever feasible,
so testing them is wasted work. Second, on `[0, 0, 0]` the correct answer is
`0` — and a search starting at `1` cannot return it. Starting at the true floor
makes the degenerate case fall out instead of needing a branch.

**The greedy sweep is optimal, not merely reasonable.** Filling each block as
full as the cap allows before opening the next one can never need more blocks
than some other arrangement: at every point in the route, the greedy sweep has
covered at least as many legs with at least as few blocks as any alternative,
and that advantage cannot be lost later. The claim is worth stating explicitly
in your write-up — "greedy" and "provably optimal" are different words, and
interviewers listen for the second.

**Trace `riders = 3` at the boundary.** With a cap of **11**: `8 + 3 = 11`
fits, `+ 9` breaks it, so block 1 is `[8, 3]`. Then `9 + 4 = 13` breaks it, so
block 2 is `[9]`. Then `4 + 6 = 10`, `+ 2 = 12` breaks it, so block 3 is
`[4, 6]` and block 4 is `[2]`. Four blocks, more than three riders — the cap
fails. With a cap of **12**: `[8, 3]`, then `[9]`, then `4 + 6 + 2 = 12` fits
exactly, so three blocks. It succeeds, and 12 is the first cap that does.

**`[5, 0, 5]` with two riders is the zero-leg case.** The answer is `5`: split
as `[5, 0]` and `[5]`, and the zero-kilometre leg rides free with either
neighbour. A cap of `4` is impossible, because a five-kilometre leg cannot be
divided — which is the floor argument again, in miniature.

**The two-rider answer is deliberately lopsided.** Twenty against twelve. If
your instinct was to balance the halves, notice that moving the `4` across
gives sixteen against sixteen — which sounds fairer and is not achievable,
because the blocks must be *runs of consecutive legs* and `[8, 3, 9]` is
already twenty on its own. Minimising the maximum and equalising are different
objectives, and only one of them is the contract.

## Download and run

Download
[problem-02-relay-handoff-solution.py](./problem-02-relay-handoff-solution.py)
and run it:

```bash
python problem-02-relay-handoff-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `problem-02-relay-handoff.py`.

## Common bugs to catch

- **`ValueError: max() iterable argument is empty`.** You built the interval
  before handling the empty route:

  ```text
  Traceback (most recent call last):
      lo, hi = max(legs), sum(legs)
               ~~~^^^^^^
  ValueError: max() iterable argument is empty
  ```

  `sum([])` is `0` and never raises, so the crash always lands on `max` — which
  is a small reminder that the two builtins disagree about the empty case.

- **`fairest_relay_split([0, 0, 0], 2)` returns `1`.** You set `lo = 1`. Every
  leg is zero, so the longest block is zero, and zero is a legal answer rather
  than a failure. The floor is `max(legs)`, and on this route that is `0`.

- **`fairest_relay_split(ROUTE, 7)` returns `9` instead of `None`.** The
  impossible branch is missing. Seven riders cannot each get one of six legs,
  and the predicate never notices, because `blocks_needed` at any cap is at
  most six and six is comfortably `<= 7`. The guard is the only thing standing
  between you and a confidently wrong answer.

- **The program hangs on every input.** You wrote the predicate as
  `blocks_needed(legs, mid) == riders`. That is not monotone — the count falls
  as the cap rises and skips values on the way — so there is no single flip to
  converge on, and the interval stops shrinking. Compare with `<=`.

- **`blocks_needed` returns `0` on an empty route.** It starts at `blocks = 1`,
  so it always returns at least one, which is right for a route with legs in it
  and wrong for an empty one. The function is never called on an empty route
  here, because the guard runs first — but if you moved the guard, this is what
  would bite.

- **Every answer is one kilometre too big.** You wrote `hi = mid - 1` in a
  half-open loop. This is a smallest-such-that search, so the successful
  midpoint is a candidate and must be kept with `hi = mid`.

- **The right answers, and a large route takes minutes.** Your predicate
  re-scans from the start of the route for every block. It is one sweep with a
  running total; if there are two nested loops in it, that is the bug.

## Under the hood

<details>
<summary>Under the hood — the exact-cost alternative, and the mirror problem</summary>

**Cost.**

Time is `O(n log T)`, where `n` is the number of legs and `T` is the route
total. The search halves an interval of width `T - max(legs)` — about 30
iterations at the top of the constraints — and each iteration sweeps all `n`
legs. Space is `O(1)`.

**The dynamic-programming alternative, and why nobody wants it.**

This problem can be solved exactly with dynamic programming: `best[r][i]` is
the smallest possible maximum when the first `i` legs are split among `r`
riders. The recurrence is a minimum over every place the last block could
start, so filling the table costs `O(riders · n²)` — at a hundred thousand
legs, unimaginable. It also gives you the split itself for free, which the
binary search does not.

That trade is worth naming: bisecting the answer gives you the *value* quickly
and says nothing about *which arrangement* achieves it. When a contract wants
the arrangement too — as
[Challenge 2](../challenges/challenge-02-signal-mast-spacing.md) does — you
recover it by running the predicate once more at the winning value, which is
one extra pass rather than a different algorithm.

**The mirror problem: maximise the minimum.**

Turn the objective around — pay couriers per parcel and make the *worst-off*
courier as well-off as possible — and the machinery is identical with three
flips: the predicate's monotonicity runs the other way, the successful branch
keeps the midpoint with `lo = mid`, and the midpoint must round up. That is
the mini-project's fifth problem, and it is
[Challenge 2](../challenges/challenge-02-signal-mast-spacing.md) in a different
costume. Two directions, one pattern.

**Why greedy fails on the reordering version.**

Everything on this page depends on the blocks being *runs of consecutive legs*.
Allow the dispatcher to hand any subset of legs to any rider and the problem
becomes multiway number partitioning, which is NP-hard: no greedy sweep is
optimal, and no binary search on the answer has a feasibility test you can run
in polynomial time. The constraint that looks like a simplification is in fact
what makes the problem solvable at all — which is a good habit to carry into
Recognise, because a prompt that quietly drops "consecutive" is a different
problem wearing the same words.

</details>

## Acceptance checklist

- [ ] `python problem-02-relay-handoff.py` prints five rows then
      `All checks passed.`
- [ ] The output matches the expected output character for character.
- [ ] You can deliver the four-part reframe in about thirty seconds.
- [ ] You can explain in one sentence why the predicate uses `<=` and not `==`.
- [ ] `lo = max(legs)`, and you can give both reasons for it.
- [ ] Both `None` branches are present: too many riders, and fewer than one.
- [ ] You traced caps 11 and 12 by hand for three riders.
- [ ] Committed to Git with a message like
      `Add Week 5 homework 2: relay handoff`.

## Stretch

- **Return the split, not just the number.** The dispatcher needs to tell the
  riders where to stand.

  ```python
  def relay_plan(legs: list[int], cap: int) -> list[list[int]]:
      """Return the legs each rider covers at a given cap, in route order."""
      plan: list[list[int]] = [[]]
      carried = 0
      for leg in legs:
          if carried + leg > cap:
              plan.append([])
              carried = 0
          plan[-1].append(leg)
          carried += leg
      return plan
  ```

  ```text
  cap 12: [[8, 3], [9], [4, 6, 2]]
  cap 11: [[8, 3], [9], [4, 6], [2]]
  ```

  One more pass at the winning cap recovers the arrangement the search never
  tracked. Note that it produces the *fewest* blocks, which may be fewer than
  `riders` — say what you would do to hand the surplus riders something to do.

- **Add a fixed handover cost.** Every handoff between riders costs two
  kilometres of dead time, charged to the receiving rider. Rewrite the
  predicate, then check whether the interval's bounds still hold.

  ```text
  with handovers: 3 riders -> 14
  ```

  The floor moves, the ceiling does not, and the monotonicity argument needs
  re-checking rather than assuming. Do the re-check out loud.

- **Find the smallest rider count for a target cap.** The inverse question:
  given that no rider may exceed 12 km, how many riders are needed?

  ```python
  def riders_for_cap(legs: list[int], cap: int) -> int | None:
      """Return the fewest riders that keep every rider within `cap`."""
      if legs and cap < max(legs):
          return None
      return blocks_needed(legs, cap) if legs else 0
  ```

  ```text
  cap 12 -> 3 riders
  cap 8  -> None
  ```

  No search at all — the predicate already answers it. Say out loud why one
  direction needs bisection and the other does not.

Next: [Homework Problem 3 — The Ridge Line](./problem-03-ridge-line.md).
