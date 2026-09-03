# Problem 2 — The Courier's Zone Count

> **Topic:** the counting window, and the subtraction that turns "at most K" into "exactly K"
> **Lecture:** [01 — The Sliding Window Pattern](../lecture-notes/01-the-sliding-window-pattern.md)
> **Difficulty:** Medium
> **Target time:** 60 minutes
> **Why this one:** the one sliding-window shape none of the five drills covers, and the single highest-yield reformulation in the family. No window counts "exactly K" directly. The way through is to write a window that counts "at most K", call it twice, and subtract — and the reason that works is a genuinely satisfying argument you should be able to give in two sentences.

## The Brief

A courier's shift is logged as a list of **delivery-zone codes**, one per stop,
in the order the stops were visited. `["N", "N", "E", "S", "E"]` is a five-stop
shift: two stops in the north zone, then east, then south, then east again.

A **route segment** is any contiguous run of one or more stops. Segments are
identified by *where they are*, not by what is in them — so two runs through the
same zones at different points in the shift are billed separately, and a run of
five stops contains fifteen segments, not fifteen different sets of zones.

Regional accounting bills the segments that touch **exactly `k` distinct
zones**.

**Your job.** Return how many route segments touch exactly `k` distinct zones.

### Why no single window can do this

Start with what you know. Exercise 5 built a window that keeps *at most* `k`
distinct classes inside it. Turning that into a counter is one line: once the
promise holds at `right`, every segment ending at `right` and starting anywhere
from `left` onwards also holds it — because dropping stops off the left can
never *raise* the distinct count. So there are exactly `right - left + 1` of
them, and you can add that number in one go instead of listing them.

Now try to do the same for "exactly `k`". You cannot, and it is worth being
precise about why. The window would have to hold a `left` such that
`stops[left..right]` has exactly `k` zones — but the segments starting *after*
that `left` may have fewer than `k`, and the ones starting before may have more.
The qualifying starts are a **band in the middle**, not a run from `left` to
`right`, and a single window with one left edge cannot describe a band.

You could track two left edges. Many people do, and it works. But there is a
much cleaner move.

### The identity

```text
exactly(k) = at_most(k) - at_most(k - 1)
```

Read it as a sentence. `at_most(k)` counts every segment whose zone count is
`k` or fewer. `at_most(k - 1)` counts every segment whose zone count is `k - 1`
or fewer. Every segment counted by the second is also counted by the first, so
subtracting leaves exactly the segments whose zone count is neither at most
`k - 1` nor above `k` — which is to say, exactly `k`.

So you write **one** function, the at-most-K counting window, and call it
twice.

**The contract.** Return an integer. If `k` is `0`, or the stop list is empty,
return `0`. Note the trap hiding in the identity: at `k = 1` the subtraction
needs `at_most(0)`, and a helper that walks off the end or loops forever on a
limit of zero will take the whole problem down with it. That is the graded edge
of this page.

## Starter

Create `problem-02-courier-zone-count.py` and paste this in. Fill in every
`TODO`.

```python
"""problem-02-courier-zone-count.py — counting exactly-K segments.

Count the route segments touching exactly k distinct zones, by writing an
at-most-K counting window once and calling it twice.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""


def at_most(stops: list[str], limit: int) -> int:
    """Return how many segments touch at most `limit` distinct zones.

    Args:
        stops: Zone codes, one per stop, in visit order.
        limit: The largest number of distinct zones a segment may touch.

    Returns:
        The number of contiguous runs of one or more stops within the limit.
        Zero when the limit is zero or negative, because no run of one or more
        stops touches zero zones.
    """
    # TODO: the limit may be 0 — or lower, if a caller passes k - 1 at k = 0.
    #       Answer it here rather than letting the loop try.
    # TODO: a frequency table, `left` at 0, a running total at 0.
    # TODO: walk `right` over the stops, adding to the table.
    # TODO: while the table has more than `limit` keys, drop stops[left]:
    #       decrement, delete the key on zero, advance left.
    # TODO: the combine step — one line. Every segment ending at `right` and
    #       starting at or after `left` qualifies. How many is that?
    ...


def segments_with_exactly_k_zones(stops: list[str], k: int) -> int:
    """Return how many route segments touch exactly k distinct zones.

    Args:
        stops: Zone codes, one per stop, in visit order.
        k: The exact number of distinct zones a billable segment touches.

    Returns:
        The count of qualifying segments. Zero when k is zero or the shift is
        empty.
    """
    # TODO: the two contract zeros.
    # TODO: the identity. Two calls and a minus sign.
    ...


def count_by_enumeration(stops: list[str], k: int) -> int:
    """Count the same thing the slow, obvious way. Used only to check.

    Args:
        stops: Zone codes, one per stop, in visit order.
        k: The exact number of distinct zones a billable segment touches.

    Returns:
        The same number, reached by looking at every segment in turn.
    """
    # TODO: every start, every end, count the distinct zones between them.
    #       This is the O(n^2) version the constraints reject — write it
    #       anyway, because the self-check uses it to disagree with you.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    shift = ["N", "N", "E", "S", "E"]
    print(f"shift {shift}, k=2")
    print(f"  at_most(2)            : {at_most(shift, 2)}")
    print(f"  at_most(1)            : {at_most(shift, 1)}")
    print(f"  exactly 2 zones       : {segments_with_exactly_k_zones(shift, 2)}")
    print(f"  same, by enumeration  : {count_by_enumeration(shift, 2)}")
    print()

    cases: list[tuple[list[str], int]] = [
        (["N", "N", "E", "S", "E"], 2),
        (["N", "E", "N"], 1),
        (["W", "X", "Y", "Z"], 4),
        (["W", "W", "W"], 1),
        (["W", "X"], 3),
        (["W"], 0),
        ([], 1),
    ]
    for stops, k in cases:
        print(f"k={k}  stops {str(stops):<26} -> {segments_with_exactly_k_zones(stops, k)}")
    print()

    assert segments_with_exactly_k_zones(["N", "N", "E", "S", "E"], 2) == 5
    assert segments_with_exactly_k_zones(["N", "E", "N"], 1) == 3
    assert segments_with_exactly_k_zones(["W", "X", "Y", "Z"], 4) == 1
    assert segments_with_exactly_k_zones(["W", "W", "W"], 1) == 6
    assert segments_with_exactly_k_zones(["W", "X"], 3) == 0
    assert segments_with_exactly_k_zones(["W"], 0) == 0
    assert segments_with_exactly_k_zones([], 1) == 0

    assert at_most(["N", "N", "E", "S", "E"], 2) == 11
    assert at_most(["N", "N", "E", "S", "E"], 1) == 6
    assert at_most(["N", "E", "N"], 0) == 0

    # The identity and the enumeration must agree on every case, at every k.
    for stops, _ in cases:
        for k in range(0, 6):
            assert segments_with_exactly_k_zones(stops, k) == count_by_enumeration(stops, k)

    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-03-sliding-window/homework/problem-02-courier-zone-count.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `segments_with_exactly_k_zones(stops, k)` returns an integer.
2. `at_most` is written **once** and called twice. No second window.
3. `at_most(stops, 0)` returns `0`, and so does any negative limit.
4. `k == 0` returns `0`. An empty shift returns `0`.
5. The combine step in `at_most` is a single addition of `right - left + 1`.
   No inner loop enumerating segments.
6. Every count that reaches zero has its key deleted.
7. `count_by_enumeration` gives the same answers by brute force, and the
   self-check compares them at every `k` from 0 to 5.
8. Every function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(stops) <= 200_000`.** A courier's shift over a long period. The
  bound is chosen to force the counting formulation rather than merely to
  discourage enumeration: there are `n(n + 1) / 2` segments, which is about
  `2 x 10^10` here. **You cannot list what you have to count** — not slowly,
  not at all. That sentence is the whole reason the combine step is one
  addition instead of an inner loop.

- **`0 <= k <= 40`, and `k = 0` is legal.** A courier does not touch forty
  zones in a shift, so the bound is generous; what it is really doing is making
  `k = 0` a case you must answer. It is also the case that drives
  `at_most(k - 1)` to `at_most(-1)`, which is the graded edge. Handle it in the
  helper, once, rather than special-casing the caller.

- **Zone codes come from a set of at most 80 codes.** A regional network has a
  fixed map. The frequency table therefore holds at most `min(limit + 1, 80)`
  entries, so the space claim is `O(1)` rather than a vague `O(n)`.

- **The answer can be large.** With 200,000 stops all in one zone,
  `at_most(1)` is about `2 x 10^10`, which fits a Python `int` without comment
  and would overflow a 32-bit counter. One sentence about what a C++ or Java
  translation would need is worth having ready.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-02-courier-zone-count.py
shift ['N', 'N', 'E', 'S', 'E'], k=2
  at_most(2)            : 11
  at_most(1)            : 6
  exactly 2 zones       : 5
  same, by enumeration  : 5

k=2  stops ['N', 'N', 'E', 'S', 'E']  -> 5
k=1  stops ['N', 'E', 'N']            -> 3
k=4  stops ['W', 'X', 'Y', 'Z']       -> 1
k=1  stops ['W', 'W', 'W']            -> 6
k=3  stops ['W', 'X']                 -> 0
k=0  stops ['W']                      -> 0
k=1  stops []                         -> 0

All checks passed.
```

Check the top block by hand once, because believing the identity is most of the
work. The five qualifying segments in `["N", "N", "E", "S", "E"]` at `k = 2`
are stops 0–2, 1–2, 2–3, 3–4 and 2–4. Count them yourself. Then confirm the
same number falls out of `11 - 6`, and notice that neither of those two numbers
is the answer to anything the customer asked.

## Steps

1. Create the file, paste the starter, and run it. Correct starting point.
2. Write `at_most` first, and write its guard first of all. A limit of zero or
   below returns `0` — a segment has at least one stop, so it touches at least
   one zone, so nothing can satisfy a limit of zero.
3. Build the window. It is Exercise 5's, unchanged: increment, shrink while
   `len(counts) > limit`, delete keys on zero.
4. Write the combine step. One line, after the shrink: `total += right - left + 1`.
   Before you move on, say out loud why that number is right — the argument is
   in *The Solution*, but try it yourself first on `["N", "N", "E"]` with
   `limit = 2`.
5. Write `segments_with_exactly_k_zones`. Two guards and one subtraction.
6. Write `count_by_enumeration`. It is three lines and it is the most valuable
   thing on the page, because it was built from a different idea and will
   disagree with you if you are wrong.
7. Run it. When the cross-check passes at every `k` from 0 to 5, on all seven
   shifts, you have something you can trust.

## The Solution

```python
"""problem-02-courier-zone-count-solution.py — counting exactly-K segments.

A courier's shift is a list of delivery-zone codes, one per stop. Regional
accounting bills the route segments that touch exactly k distinct zones, and a
segment is any contiguous run of one or more stops.

No single window counts "exactly k" directly, because a window that is
currently at k distinct zones may later be at k + 1 and the segments it
already contributed cannot be taken back. The way through is an identity:

    exactly(k) = at_most(k) - at_most(k - 1)

`at_most` is a counting window. Once its invariant holds at `right`, every
segment that ends at `right` and starts anywhere in [left, right] also holds
it, so the step adds `right - left + 1` in one go rather than enumerating.

The self-checks are the starter's, unchanged. When they all pass the file
prints "All checks passed."
"""


def at_most(stops: list[str], limit: int) -> int:
    """Return how many segments touch at most `limit` distinct zones.

    Args:
        stops: Zone codes, one per stop, in visit order.
        limit: The largest number of distinct zones a segment may touch.

    Returns:
        The number of contiguous runs of one or more stops within the limit.
        Zero when the limit is zero or negative, because no run of one or more
        stops touches zero zones.
    """
    if limit <= 0:
        return 0

    counts: dict[str, int] = {}
    left = 0
    total = 0

    for right, zone in enumerate(stops):
        counts[zone] = counts.get(zone, 0) + 1

        while len(counts) > limit:
            leaving = stops[left]
            counts[leaving] -= 1
            if counts[leaving] == 0:
                del counts[leaving]
            left += 1

        # Every segment ending here and starting at or after `left` qualifies.
        total += right - left + 1

    return total


def segments_with_exactly_k_zones(stops: list[str], k: int) -> int:
    """Return how many route segments touch exactly k distinct zones.

    Args:
        stops: Zone codes, one per stop, in visit order.
        k: The exact number of distinct zones a billable segment touches.

    Returns:
        The count of qualifying segments. Zero when k is zero or the shift is
        empty.
    """
    if k == 0 or not stops:
        return 0
    return at_most(stops, k) - at_most(stops, k - 1)


def count_by_enumeration(stops: list[str], k: int) -> int:
    """Count the same thing the slow, obvious way. Used only to check.

    Args:
        stops: Zone codes, one per stop, in visit order.
        k: The exact number of distinct zones a billable segment touches.

    Returns:
        The same number, reached by looking at every segment in turn.
    """
    if k == 0:
        return 0
    return sum(
        1
        for i in range(len(stops))
        for j in range(i + 1, len(stops) + 1)
        if len(set(stops[i:j])) == k
    )


# ---- Self-check ----
if __name__ == "__main__":
    shift = ["N", "N", "E", "S", "E"]
    print(f"shift {shift}, k=2")
    print(f"  at_most(2)            : {at_most(shift, 2)}")
    print(f"  at_most(1)            : {at_most(shift, 1)}")
    print(f"  exactly 2 zones       : {segments_with_exactly_k_zones(shift, 2)}")
    print(f"  same, by enumeration  : {count_by_enumeration(shift, 2)}")
    print()

    cases: list[tuple[list[str], int]] = [
        (["N", "N", "E", "S", "E"], 2),
        (["N", "E", "N"], 1),
        (["W", "X", "Y", "Z"], 4),
        (["W", "W", "W"], 1),
        (["W", "X"], 3),
        (["W"], 0),
        ([], 1),
    ]
    for stops, k in cases:
        print(f"k={k}  stops {str(stops):<26} -> {segments_with_exactly_k_zones(stops, k)}")
    print()

    assert segments_with_exactly_k_zones(["N", "N", "E", "S", "E"], 2) == 5
    assert segments_with_exactly_k_zones(["N", "E", "N"], 1) == 3
    assert segments_with_exactly_k_zones(["W", "X", "Y", "Z"], 4) == 1
    assert segments_with_exactly_k_zones(["W", "W", "W"], 1) == 6
    assert segments_with_exactly_k_zones(["W", "X"], 3) == 0
    assert segments_with_exactly_k_zones(["W"], 0) == 0
    assert segments_with_exactly_k_zones([], 1) == 0

    assert at_most(["N", "N", "E", "S", "E"], 2) == 11
    assert at_most(["N", "N", "E", "S", "E"], 1) == 6
    assert at_most(["N", "E", "N"], 0) == 0

    # The identity and the enumeration must agree on every case, at every k.
    for stops, _ in cases:
        for k in range(0, 6):
            assert segments_with_exactly_k_zones(stops, k) == count_by_enumeration(stops, k)

    print("All checks passed.")
```

**The combine step is one line, and its justification is the whole problem.**

```python
total += right - left + 1
```

Here is the argument, and it is worth being able to give it in two sentences.
At the moment that line runs, the shrink has finished, so `stops[left..right]`
touches at most `limit` zones. Now take any start `s` between `left` and
`right`: the segment `stops[s..right]` is a *sub-segment* of one that already
satisfies the limit, and dropping stops from the left can never increase the
number of distinct zones — so it satisfies the limit too.

That gives you every segment ending at `right` that qualifies, and there are
`right - left + 1` of them. Segments ending at `right` and starting *before*
`left` do not qualify, because if they did, the shrink would not have moved
`left` there.

Sum that over every `right` and you have counted every qualifying segment
exactly once, because each segment has exactly one right-hand end.

**Where the argument stops working.** It leans entirely on the promise
surviving a shrink. "At most `k` distinct" survives; so does "sum at most `c`"
with non-negative numbers. "**At least** `k` distinct" does not — shrinking
breaks it — so the counting trick does not transfer, and a prompt phrased with
"at least" should make you stop and check rather than reach for this line.

**The identity, and why subtracting is legitimate.**

```python
return at_most(stops, k) - at_most(stops, k - 1)
```

Every segment has one definite number of distinct zones, call it `d`. The
segment is counted by `at_most(j)` for every `j >= d` and by none below. So it
contributes 1 to `at_most(k)` when `d <= k`, and 1 to `at_most(k - 1)` when
`d <= k - 1`. Subtract, and its net contribution is 1 exactly when `d <= k` and
not `d <= k - 1` — which is `d == k`. Every other segment contributes 0.

Two things follow that are worth saying out loud. Both calls must be over the
**same input**, or the segments being counted are not the same segments and the
subtraction is meaningless. And the difference cannot be computed inside a
single pass by tracking two left edges and subtracting as you go — you can make
that work, but it is a different algorithm with two invariants to maintain
simultaneously, and the whole appeal of the identity is that it needs one.

**The guard belongs in the helper, not the caller.**

```python
if limit <= 0:
    return 0
```

At `k = 1` the identity calls `at_most(stops, 0)`. Answering it in the helper
means the caller never has to know that the edge exists. Answering it in the
caller means every future caller has to remember. And it is not merely
defensive: `at_most(stops, 0)` genuinely *is* zero, for a reason you can state
— a segment holds at least one stop, a stop is in exactly one zone, so no
segment touches zero zones. The guard is the right answer, not a shortcut past
a bad one.

Without it, the shrink condition `len(counts) > 0` is true the moment anything
is added, so `left` marches past `right`, `right - left + 1` goes to zero, and
you add nothing — which happens to give the right total by accident. That is
worse than an error, because it works until the day the combine step changes.

**`k == 0` and the empty shift are contract decisions.** Zero zones is not a
question about the data, it is a question about what the caller meant, and the
contract says the answer is `0`. The empty shift has no segments at all, so `0`
is forced rather than chosen.

**Why the enumeration check earns its place.** `count_by_enumeration` is built
from a completely different idea — look at every segment, count its zones — and
the self-check runs both at every `k` from 0 to 5 on all seven shifts. Two
implementations that share no reasoning are unlikely to be wrong the same way,
which is what makes this the most effective testing habit in the course. It is
also `O(n^2)`, which is exactly why it only ever runs on five-stop shifts.

**Cost.** `at_most` is `O(n)` by the usual amortised argument, so
`segments_with_exactly_k_zones` is two passes, `O(n)`. Space is
`O(min(k + 1, 80))`, which the zone bound makes `O(1)`. There is no early exit
— every segment must be accounted for — so best, average and worst are the
same.

## Download and run

Download
[problem-02-courier-zone-count-solution.py](./problem-02-courier-zone-count-solution.py)
and run it:

```bash
python problem-02-courier-zone-count-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `problem-02-courier-zone-count.py`.

## Common bugs to catch

- **`IndexError: list index out of range` at `k = 1`.**

  ```text
  Traceback (most recent call last):
      leaving = stops[left]
                ~~~~~^^^^^^
  IndexError: list index out of range
  ```

  You called `at_most` with a limit of `0` and let the loop try. The shrink
  condition never clears, `left` runs past the end of the list, and the read
  fails. This is the graded edge of the problem, and it only shows up at
  `k = 1`, which is easy to leave untested.

- **`segments_with_exactly_k_zones(["W", "W", "W"], 1)` returns `3` instead of
  `6`.** You counted only the longest qualifying segment ending at each `right`
  — adding `1` per step instead of `right - left + 1`. The answer looks
  plausible and is a third of the truth. Enumerate the six segments of a
  three-stop shift on paper: three of length 1, two of length 2, one of length
  3.

- **`IndexError` inside the shrink on a shift that is plainly not empty.** You
  did not delete keys whose count reached zero, so `len(counts)` keeps counting
  zones that have already left the window. Same bug as Exercise 5, same
  symptom.

- **The answer is negative.** You subtracted the wrong way round —
  `at_most(k - 1) - at_most(k)`. A count cannot be negative, which makes this
  one of the friendlier bugs: the sign tells you immediately.

- **`TypeError: '>' not supported between instances of 'int' and 'NoneType'`.**

  ```text
  Traceback (most recent call last):
      while len(counts) > limit:
            ~~~~~~~~~~~~^~~~~~~
  TypeError: '>' not supported between instances of 'int' and 'NoneType'
  ```

  `at_most` fell off the end and returned `None`, and you passed that back into
  something expecting a number. Usually a `return total` indented into the
  `for`.

- **Calling `at_most` on two different lists.** Filtering or copying the stops
  between the two calls breaks the identity, because the two counts are then
  over different segment sets and their difference means nothing.

- **Enumerating inside the window.** An inner `for` that walks from `left` to
  `right` gives correct answers and makes the whole thing `O(n^2)`, which the
  size bound rejects. Requirement 5 is checkable by reading.

## Under the hood

<details>
<summary>Under the hood — the inclusion-exclusion behind the identity, and where else it turns up</summary>

**This is inclusion–exclusion, in its simplest possible form.**

Define `A_j` as the set of segments touching at most `j` distinct zones. The
sets are nested: `A_0` is a subset of `A_1`, which is a subset of `A_2`, and so
on. The segments touching *exactly* `k` are `A_k` with `A_(k-1)` removed, and
because the second is entirely inside the first, the size of the difference is
just the difference of the sizes.

That last clause is doing real work and it is where the technique fails when
people over-generalise it. `|A \ B| = |A| - |B|` holds only when `B` is a
subset of `A`. If the two counts were "at most `k` zones" and "at most `k`
stops", subtracting would be meaningless — the sets overlap without nesting,
and you would be double-subtracting the intersection. The identity works here
precisely because the family is nested by construction.

**The general recipe, worth writing in your notes.**

> When a predicate is hard to count directly but *monotone in a parameter* —
> that is, satisfying it at `k` implies satisfying it at every larger `k` —
> count the monotone version twice and subtract.

The monotonicity is the licence. "At most `k` distinct" is monotone in `k`. "At
most sum `c`" is monotone in `c`, so the same trick counts subarrays with a sum
in a given range. "Exactly `k` odd numbers" reduces the same way, by counting
"at most `k` odd numbers" twice. All three are the same move.

**A range, for free.** Once you have `at_most`, counting segments whose zone
count falls in a range `[lo, hi]` is `at_most(hi) - at_most(lo - 1)`. The
"exactly" case is just the range where `lo == hi`. Noticing that the more
general operation costs nothing extra is a small pleasure and occasionally
useful in an interview, where the follow-up question is often exactly that
generalisation.

**Two windows in one pass, and why the page does not do it.**

You *can* count "exactly `k`" in a single pass by maintaining two left edges —
one for the at-most-`k` boundary and one for the at-most-`(k-1)` boundary — and
adding their difference at every step. It is a legitimate solution, it is one
pass instead of two, and it is roughly twice as much code with two invariants
to keep true simultaneously.

The two-call version is the same asymptotic cost, half the reasoning, and the
helper you write is reusable for every other question in the family. When two
solutions have the same complexity, prefer the one with fewer things that can
independently be wrong. That is a defensible engineering position and a good
thing to say out loud rather than apologise for.

**The overflow remark, in full.** `at_most(1)` on 200,000 identical stops is
`200000 * 200001 / 2`, about `2 x 10^10`. Python's `int` grows to fit, so the
only cost is that arithmetic on large values is slower than on machine words. A
Java or C++ translation needs a 64-bit type for the accumulator — and the
accumulator is the one people forget, because each individual `right - left + 1`
is small. Silent overflow in a running total wraps to a negative number and
produces an answer that looks like a plausible near-miss.

</details>

## Acceptance checklist

- [ ] `python problem-02-courier-zone-count.py` prints both blocks then `All checks passed.`
- [ ] The output matches the Expected output block character for character.
- [ ] `at_most` is written once and called twice.
- [ ] `at_most(stops, 0)` returns `0`, and you can say why that is the right answer rather than a guard.
- [ ] The combine step is one addition, with no inner loop.
- [ ] You verified the five qualifying segments of the first shift by hand.
- [ ] You can state, in two sentences, why `right - left + 1` is the correct number to add.
- [ ] You can state why the identity needs both calls on the same input.
- [ ] The cross-check against `count_by_enumeration` passes at every `k` from 0 to 5.
- [ ] Every function has type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 3 homework 2: the courier's zone count`.

## Stretch

- **Count a range of zone counts.** One function, and "exactly" becomes the
  special case where the two bounds are equal.

  ```python
  def segments_in_zone_range(stops: list[str], lo: int, hi: int) -> int:
      """Return how many segments touch between lo and hi distinct zones, inclusive."""
      if hi < lo or hi <= 0:
          return 0
      return at_most(stops, hi) - at_most(stops, lo - 1)
  ```

  ```text
  ["N", "N", "E", "S", "E"] range 1..2 -> 11
  ["N", "N", "E", "S", "E"] range 2..3 -> 9
  ```

  Check the first against `at_most(2)` and satisfy yourself it is not a
  coincidence.

- **Apply the identity to a sum instead of a count.** Count the segments whose
  total delivery time is exactly `t` minutes, using an at-most-sum window over
  non-negative durations. The window changes; the identity does not. Note where
  the non-negativity requirement comes back in — it is the same monotonicity
  argument as Exercise 4.

- **Write the two-pointer single-pass version.** Maintain both left edges and
  add their difference each step. Get it passing the same cross-check, then
  compare the two files side by side and decide which one you would rather be
  handed at midnight. Write the answer down; that judgement is the deliverable.
Next: [Problem 3 — When the Window Fails](./problem-03-when-the-window-fails.md).
