# Exercise 1 — Ferry Ramp Manifests

> **Topic:** the memoization-first route — plain recursion, then `functools.cache`, then a bottom-up table
> **Lecture:** [01 — The DP Pipeline and 1D States](../lecture-notes/01-the-dp-pipeline-and-1d-states.md)
> **Difficulty:** Beginner
> **Target time:** 40 minutes
> **Why this one:** it is the smallest problem where the naive answer is genuinely unusable and the fix is one line. You will watch a recursion make seventy-eight thousand calls, add a decorator, and watch the same recursion make nineteen. Every other page this week assumes you have seen that number change.

## The Brief

The Kelbray Sound car ferry loads through a single ramp at the stern. The deck
crew does not wave vehicles on one at a time. They wave them on in **stints**:
one stint sends 1, 2 or 3 vehicles up the ramp together, and three abreast is
the widest the ramp takes.

So a deck that holds four vehicles can be filled in several different ways. A
stint of 1, then 1, then 1, then 1. Or 1, then 3. Or 3, then 1. Or 2, then 2.
Two plans count as different when the **list of stint sizes** differs, so
"1 then 2" and "2 then 1" are two plans, not one — the crew really does do
different work in each case.

The purser does not want a single number. She wants a **planning table**: how
many plans fill a deck of 0 vehicles, how many fill a deck of 1, of 2, and so
on up to the deck she actually has. She uses the small entries to sanity-check
the big one.

Here is the whole idea in one sentence, and it is the sentence you should be
able to say before you write any Python:

> **A plan that loads `k` vehicles ends with a last stint, and that last stint
> was of size 1, 2 or 3 — so the number of plans for `k` is the number of plans
> for `k-1` plus the number for `k-2` plus the number for `k-3`.**

That sentence is called a **recurrence**: a rule that describes a bigger answer
in terms of smaller answers of the same shape. Say it in English first, every
single time. The Python is a translation of the English, and a translation is
much easier to check than an invention.

One more thing before you start. `plans[0]` is **1**, not 0. There is exactly
one way to load an empty deck: send nobody up the ramp. That is the empty plan,
and it is a plan. If you set `plans[0] = 0` the whole table collapses to zeros,
which is the fastest way to fail this exercise.

## Starter

Create `exercise-01-ferry-ramp-manifests.py` and paste this in. Fill in every
`TODO`.

```python
"""exercise-01-ferry-ramp-manifests.py — the ramp loading table.

Count the distinct stint sequences that load a deck exactly, for every deck
size from 0 up to the capacity you are given.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from __future__ import annotations

import functools

STINT_SIZES = (1, 2, 3)


def count_calls(func):
    """Wrap `func` so `func.calls` counts how many times its body ran."""

    @functools.wraps(func)
    def wrapper(*args):
        wrapper.calls += 1
        return func(*args)

    wrapper.calls = 0
    return wrapper


@count_calls
def naive_plan_count(remaining: int) -> int:
    """Count loading plans for `remaining` vehicles, remembering nothing."""
    # TODO: base case first. Zero vehicles left means one finished plan.
    # TODO: otherwise add up the counts for remaining - 1, - 2 and - 3,
    #       skipping any stint bigger than what is left.
    ...


@functools.cache
@count_calls
def cached_plan_count(remaining: int) -> int:
    """The same recursion, with every answer written down the first time."""
    # TODO: copy the body of naive_plan_count, changing only the name it
    #       calls. Do not change the logic. The decorator is the whole fix.
    ...


def plan_counts(capacity: int) -> list[int]:
    """Return the loading-plan count for every deck size from 0 to capacity.

    Args:
        capacity: How many vehicles the deck holds. Never negative.

    Returns:
        A list of length capacity + 1. Entry k is the number of plans that
        load exactly k vehicles.

    Raises:
        ValueError: If capacity is negative.
    """
    # TODO: raise ValueError on a negative capacity
    # TODO: build a list of capacity + 1 zeros, set entry 0 to 1
    # TODO: walk deck sizes upwards, summing the in-range predecessors
    ...


if __name__ == "__main__":
    assert plan_counts(0) == [1]
    assert plan_counts(3) == [1, 1, 2, 4]
    assert plan_counts(5) == [1, 1, 2, 4, 7, 13]

    naive_plan_count.calls = 0
    cached_plan_count.cache_clear()
    cached_plan_count.__wrapped__.calls = 0
    assert naive_plan_count(18) == cached_plan_count(18) == plan_counts(18)[-1]
    print("naive calls :", naive_plan_count.calls)
    print("cached calls:", cached_plan_count.__wrapped__.calls)
    print("All checks passed.")
```

Four words you need before you start.

**Recurrence.** The rule that builds a bigger answer out of smaller answers of
the same shape. Here it is "one plus two plus three steps back".

**Base case.** The smallest input, whose answer you write down rather than
derive. Here it is `remaining == 0`, and the answer is 1.

**Memoize.** To remember an answer the first time you work it out, so the
second request is a lookup rather than a re-derivation. `functools.cache` does
this for you: it keeps a dictionary from the function's arguments to what the
function returned.

**Table.** A list (or list of lists) holding the answer for every state, filled
in an order that guarantees each entry's predecessors are already there. Filling
a table is called **tabulation**, and it is the same recurrence run bottom-up
instead of top-down.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-11-dynamic-programming-i/exercises/exercise-01-ferry-ramp-manifests.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `naive_plan_count(remaining)` returns the plan count using recursion only —
   no cache, no table, no cleverness.
2. `cached_plan_count(remaining)` has a **body identical** to
   `naive_plan_count`'s except for the name it calls itself by. The only
   difference between the two functions is the `functools.cache` decorator.
3. `plan_counts(capacity)` returns a list of length `capacity + 1`, where entry
   `k` is the number of plans loading exactly `k` vehicles.
4. `plan_counts(0)` returns `[1]`.
5. `plan_counts(4)` returns `[1, 1, 2, 4, 7]`. A two-term recurrence returns
   `5` in that last slot; the third term is the whole difference.
6. `plan_counts(-1)` raises `ValueError`. It does not return `[]` and it does
   not return `[1]`.
7. Every count is an exact Python `int`. No floats, no rounding, no modulus.

## Constraints

- **`0 <= capacity <= 5000`.** The lower bound is because a negative deck is a
  caller's bug, not an input to interpret. The upper bound is about the size of
  the numbers, not the speed of the loop: `plan_counts(5000)` has a final entry
  of roughly nineteen hundred digits, and adding numbers that long is no longer
  the cheap constant-time operation this exercise is teaching. Past 5000 the
  interesting cost stops being the algorithm and starts being big-integer
  arithmetic, which is a different lesson.

- **Return the whole table, not the final number.** This is the rule that makes
  the exercise what it is. If you were allowed to return only `plans[capacity]`
  you could keep three variables and roll them forward, using constant space.
  The purser wants every row, so the space you use is the answer you were asked
  for, and there is nothing to reduce. Being able to say *why* a space reduction
  is unavailable is worth as much as being able to do one.

- **Guard the index, do not rely on Python's negative indexing.** When `k` is
  1, `plans[k - 3]` is `plans[-2]`, and in Python that is a real element near
  the end of the list. It will not raise. It will quietly hand you a wrong
  number, and every entry after it will be wrong too. Write `if size <= deck`.

- **Do not call `naive_plan_count` on anything above about 30.** At 18 it makes
  around seventy-eight thousand calls; each extra vehicle multiplies that by
  roughly 1.8, so 30 is about twenty million calls and 40 is about four billion.
  The bound is not a rule of the problem — it is the reason the rest of the week
  exists.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13:

```text
$ python exercise-01-ferry-ramp-manifests.py
deck  plans
   0  1
   1  1
   2  2
   3  4
   4  7
   5  13
   6  24
   7  44
   8  81

plan_counts(18)[-1]      = 35890
naive recursion  calls  = 78652
cached recursion calls  = 19
bottom-up table  reads  = 51
plan_counts(300)[-1] has 80 digits
plan_counts(-1) raises ValueError: capacity must not be negative, got -1
All checks passed.
```

The three numbers in the middle are the point of the page. The same recurrence,
asked for the same answer, costs 78,652 calls with no memory, 19 calls with a
one-line cache, and 51 table reads bottom-up. Nothing about the mathematics
changed between those three lines.

## Steps

1. Create the file, paste the starter, and run it. You get a `TypeError` from
   the first assert, because `plan_counts` returns `None`. That is the correct
   starting point.
2. Write `naive_plan_count` first. Base case, then the sum over stint sizes.
   Test it by hand: `naive_plan_count(4)` must be 7. Write the seven plans out
   on paper if it is not.
3. Write `cached_plan_count` by copying that body and changing the recursive
   call's name. Resist the urge to improve it. The exercise is proving that the
   decorator alone is the fix.
4. Run the file with just those two done, and print the two call counts. Look at
   them for a moment before moving on.
5. Now write `plan_counts`. Allocate `capacity + 1` zeros, set entry 0 to 1, and
   walk upwards. Every predecessor you read is already correct because you are
   walking in increasing order — that ordering is the whole content of
   "bottom-up".
6. Run again. When `All checks passed.` prints, open a REPL with
   `python -i exercise-01-ferry-ramp-manifests.py` and try `plan_counts(4)` next
   to your paper list of seven plans.

## The Solution

```python
"""exercise-01-ferry-ramp-manifests-solution.py — the ramp loading table.

The Kelbray Sound ferry loads through one stern ramp, in stints of 1, 2 or 3
vehicles. `plan_counts(capacity)` returns the whole prefix table: how many
distinct stint sequences load exactly k vehicles, for every k from 0 to
`capacity`.

The file shows the same count three ways, in the order you should write them:

    1. a plain recursion, which recomputes the same answers over and over,
    2. the same recursion with `functools.cache` bolted on,
    3. a bottom-up table, which is what the contract actually asks for.

Running it prints the table, then the call counts that make the difference
between (1) and (2) visible, then a consistency check at scale.
"""

from __future__ import annotations

import functools

# A stint moves one, two or three vehicles. Three abreast is the widest the
# ramp takes, so the recurrence has three terms and not two.
STINT_SIZES = (1, 2, 3)


def count_calls(func):
    """Wrap `func` so `func.calls` counts how many times its body ran."""

    @functools.wraps(func)
    def wrapper(*args):
        wrapper.calls += 1
        return func(*args)

    wrapper.calls = 0
    return wrapper


@count_calls
def naive_plan_count(remaining: int) -> int:
    """Count loading plans for `remaining` vehicles, remembering nothing.

    Correct, and unusably slow. Every call re-derives answers it has already
    derived, because nothing is written down between calls.
    """
    if remaining == 0:
        return 1
    return sum(
        naive_plan_count(remaining - size)
        for size in STINT_SIZES
        if size <= remaining
    )


@functools.cache
@count_calls
def cached_plan_count(remaining: int) -> int:
    """The same recursion, with every answer written down the first time.

    `functools.cache` sits outside the counter, so `cached_plan_count.calls`
    counts only the calls that actually reached the body — the misses.
    """
    if remaining == 0:
        return 1
    return sum(
        cached_plan_count(remaining - size)
        for size in STINT_SIZES
        if size <= remaining
    )


def plan_counts(capacity: int) -> list[int]:
    """Return the loading-plan count for every deck size from 0 to capacity.

    Args:
        capacity: How many vehicles the deck holds. Never negative.

    Returns:
        A list of length `capacity + 1`. Entry k is the number of distinct
        stint sequences that load exactly k vehicles. Entry 0 is 1, because
        the empty sequence loads nothing and is a plan.

    Raises:
        ValueError: If `capacity` is negative.
    """
    if capacity < 0:
        raise ValueError(f"capacity must not be negative, got {capacity}")

    plans = [0] * (capacity + 1)
    plans[0] = 1
    for deck in range(1, capacity + 1):
        total = 0
        for size in STINT_SIZES:
            if size <= deck:  # guard, or plans[-1] silently reads the last entry
                total += plans[deck - size]
        plans[deck] = total
    return plans


def _report() -> None:
    """Print the table, the call counts, and the scale check."""
    table = plan_counts(8)
    print("deck  plans")
    for deck, count in enumerate(table):
        print(f"{deck:>4}  {count}")

    probe = 18
    naive_plan_count.calls = 0
    cached_plan_count.cache_clear()
    cached_plan_count.__wrapped__.calls = 0

    naive_answer = naive_plan_count(probe)
    cached_answer = cached_plan_count(probe)

    print()
    print(f"plan_counts({probe})[-1]      = {plan_counts(probe)[-1]}")
    print(f"naive recursion  calls  = {naive_plan_count.calls}")
    print(f"cached recursion calls  = {cached_plan_count.__wrapped__.calls}")
    print(f"bottom-up table  reads  = {3 * probe - 3}")

    assert naive_answer == cached_answer == plan_counts(probe)[-1]

    assert plan_counts(0) == [1]
    assert plan_counts(1) == [1, 1]
    assert plan_counts(2) == [1, 1, 2]
    assert plan_counts(3) == [1, 1, 2, 4]
    assert plan_counts(4) == [1, 1, 2, 4, 7]  # a two-term recurrence says 5
    assert plan_counts(5) == [1, 1, 2, 4, 7, 13]

    big = plan_counts(300)
    assert len(big) == 301
    assert all(isinstance(value, int) for value in big)
    assert big[300] == big[299] + big[298] + big[297]
    print(f"plan_counts(300)[-1] has {len(str(big[300]))} digits")

    try:
        plan_counts(-1)
    except ValueError as problem:
        print(f"plan_counts(-1) raises ValueError: {problem}")

    print("All checks passed.")


if __name__ == "__main__":
    _report()
```

**The recurrence is one English sentence, and everything else is bookkeeping.**
A plan for `k` vehicles ends with a last stint of 1, 2 or 3. Cut that last
stint off and what is left is a complete plan for `k-1`, `k-2` or `k-3`. No plan
gets counted twice, because a plan has exactly one last stint. No plan gets
missed, because every plan has one. That is the whole proof, and it is short
enough to say out loud in an interview.

**The naive version is correct. That is what makes it dangerous.** It passes
every small test. Nothing about it looks wrong. It fails only on size, and it
fails by taking longer than anyone will wait. `naive_plan_count(18)` reaches its
body 78,652 times to produce 35,890 — more calls than the answer it computes,
because the answer counts plans and the calls count re-derivations of the same
handful of numbers.

**`functools.cache` is a dictionary from arguments to results.** The first time
`cached_plan_count(15)` runs, it does the work and stores 15 → the result. Every
later request for 15 is a dictionary lookup. There are only 19 distinct
arguments the recursion can ever be called with when it starts at 18 — the
integers 0 through 18 — so the body runs 19 times, once per distinct state.
That number is not a coincidence. **The cost of a memoized recursion is the
number of distinct states, times the work each one does.**

**The decorator order matters.** `@functools.cache` is written above
`@count_calls`, so the cache is the outer layer and the counter is inside it.
A cache hit never reaches the counter. That is exactly what we want to measure:
19 counts means 19 misses, and every other call was served from the dictionary
without running any code of ours.

**Bottom-up is the same recurrence with the recursion unwound by hand.**
Instead of asking for `k` and letting the machine discover it needs `k-1` first,
you fill in 1, then 2, then 3, in an order you chose. Two things fall out of
that. There is no call stack, so a deck of 5000 is no deeper than a deck of 5 —
the recursive version would hit Python's recursion limit long before 5000. And
the loop reads three entries per deck size, so the cost is visible on the page
rather than hidden in a decorator: `3 * capacity - 3` reads, which is 51 at
capacity 18.

**The guard is not defensive coding, it is a correctness fix.** `plans[deck -
size]` with `deck = 1` and `size = 3` is `plans[-2]`. Python answers that
question happily — negative indexes count from the end — so a missing guard
produces no error, just wrong numbers everywhere. This is the single most
common way this exercise goes wrong.

**`plan_counts(300)` ends in an 80-digit integer, and that is fine.** Python's
integers grow to whatever size they need. There is no overflow to worry about
and no modulus in the contract to hide it. It is worth seeing once, because in
most other languages this table would have silently wrapped around long before
entry 300.

## Run it

Copy the worked answer on this page into `exercise-01-ferry-ramp-manifests.py` and run it:

```bash
python exercise-01-ferry-ramp-manifests.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-01-ferry-ramp-manifests.py`.

## Common bugs to catch

- **Every entry after index 0 is wrong, and nothing raised.** You dropped the
  `if size <= deck` guard:

  ```text
  >>> plans = [0, 0, 0, 0]
  >>> plans[0] = 1
  >>> plans[1 - 3]
  0
  ```

  `plans[-2]` is a real element. Later, when the table has been partly filled,
  that stale element is not even zero — it is some earlier count — so the errors
  are not consistently in one direction and you cannot spot them by eye.

- **The whole table is zeros.** You left `plans[0]` at 0. Every entry is a sum
  of entries that are all zero, so the zero propagates the length of the list
  without a single error message. Set the base case *before* the loop and check
  `plans[0] == 1` in a REPL before you check anything else.

- **`plan_counts(4)` returns `[1, 1, 2, 4, 5]`.** You wrote a two-term
  recurrence and built Fibonacci. Index 4 is the first place a two-term and a
  three-term recurrence disagree, which is why the requirement names that exact
  value. Count the four-vehicle plans on paper: 1111, 112, 121, 211, 22, 13, 31.
  Seven.

- **`RecursionError` from the cached version.**

  ```text
  RecursionError: maximum recursion depth exceeded
  ```

  Memoizing makes a recursion fast; it does not make it shallow.
  `cached_plan_count(5000)` still stacks 5000 frames on the way down before the
  first base case returns, and CPython's default limit is 1000. The bottom-up
  table has no stack at all, which is one of the concrete things tabulation
  buys you.

- **`TypeError: unhashable type: 'list'`.** You tried to memoize a function
  that takes the table as an argument:

  ```text
  Traceback (most recent call last):
    File "exercise-01-ferry-ramp-manifests.py", line 41, in <module>
      cached_plan_count(18, [])
  TypeError: unhashable type: 'list'
  ```

  `functools.cache` uses the arguments as dictionary keys, and a list cannot be
  a dictionary key because it can change after it is stored. Pass integers, or
  pass a tuple.

- **`cached_plan_count.calls` raises `AttributeError`.**

  ```text
  AttributeError: 'functools._lru_cache_wrapper' object has no attribute 'calls'
  ```

  The name `cached_plan_count` now refers to the *cache* wrapper, which knows
  nothing about your counter. The counting wrapper is underneath it, reachable
  as `cached_plan_count.__wrapped__`. This is worth understanding rather than
  memorising: decorators stack, and the outermost one is the name you get.

- **The counts look identical.** You forgot `cached_plan_count.cache_clear()`
  between runs, so a warm cache from an earlier call served everything and the
  counter never moved. A cache is state, and state survives across calls.

## Under the hood

<details>
<summary>Under the hood — where 78,652 comes from, and why 19 is the right number</summary>

**Counting the naive calls.** Let `C(n)` be the number of times the body runs
for `naive_plan_count(n)`. The body runs once for `n` itself and then once for
each sub-call, so:

```text
C(0) = 1
C(n) = 1 + C(n-1) + C(n-2) + C(n-3)     (dropping out-of-range terms)
```

That is the same three-term shape as the answer itself, which is why the call
count grows at the same rate as the answer: about 1.8393 times per extra
vehicle. That constant is the *tribonacci constant*, the real root of
`x³ = x² + x + 1`, in the same way that Fibonacci's growth rate is the golden
ratio. So the naive version is `O(1.84ⁿ)` — exponential, and the base being
1.84 rather than 2 buys you a couple of extra vehicles and nothing more.

**Counting the memoized calls.** The recursion can only ever be called with an
integer between 0 and `n`. There are `n + 1` such integers. Each one reaches
the body at most once, because the second request is a cache hit. So the body
runs at most `n + 1` times, which at `n = 18` is 19. The general statement:

```text
memoized cost = (number of distinct states) × (work per state)
```

Here the work per state is a sum of three terms, so the whole thing is `O(n)`.
Learn to compute those two factors separately — it is how you produce a
complexity bound for a DP you have never seen before, in about ten seconds.

**`functools.cache` versus `functools.lru_cache`.** `cache` arrived in Python
3.9 and is exactly `lru_cache(maxsize=None)`: an unbounded dictionary, with no
eviction and no bookkeeping to decide what to evict. `lru_cache(maxsize=128)`
keeps only the 128 most recently used entries, which for a DP is usually wrong —
evicting a state you will need again turns your `O(n)` back into something
worse. For dynamic programming, use `cache`.

Both attach useful things to the wrapper: `cache_clear()` empties it and
`cache_info()` reports hits and misses. Swapping the counter for `cache_info()`
is a good way to check your reading of this page:

```python
cached_plan_count.cache_clear()
cached_plan_count(18)
print(cached_plan_count.cache_info())
```

**Memoization versus tabulation, honestly.** Memoization is easier to write,
because you write the recurrence the way you said it in English and let the
machine work out the order. It computes only the states it actually needs,
which matters when the state space is large but sparsely visited. Against it:
a call stack that can overflow, function-call overhead on every state, and a
cache dictionary that is bigger than an equivalent list.

Tabulation costs you one extra decision — the fill order — and pays you back
with no stack, no per-state call overhead, and the option of throwing away rows
you will not read again. When a problem asks for the whole table, as this one
does, tabulation is also just the honest shape of the answer.

The professional route is the one this file takes: recursion to get it right,
cache to make it fast, table when you need the extra properties. Doing it in
that order means you are never debugging a wrong recurrence and an awkward fill
order at the same time.

</details>

## Acceptance checklist

- [ ] `python exercise-01-ferry-ramp-manifests.py` prints the two call counts and `All checks passed.`
- [ ] `plan_counts(0) == [1]` and `plan_counts(4) == [1, 1, 2, 4, 7]`.
- [ ] `plan_counts(-1)` raises `ValueError`.
- [ ] `naive_plan_count` and `cached_plan_count` have identical bodies apart from the name they call.
- [ ] The bottom-up loop has an explicit guard, not a negative index.
- [ ] `plan_counts(300)` returns 301 entries and the last one is an exact `int`.
- [ ] You can say the recurrence out loud in one English sentence before showing the code.
- [ ] Committed to Git with a message like `Add Week 11 exercise 1: ferry ramp manifests`.

## Stretch

- **Change the ramp width and watch the table change.** Make `STINT_SIZES` a
  parameter instead of a module constant.

  ```python
  def plan_counts_for(capacity: int, sizes: tuple[int, ...]) -> list[int]:
      """The same table, for any set of allowed stint sizes."""
      plans = [0] * (capacity + 1)
      plans[0] = 1
      for deck in range(1, capacity + 1):
          plans[deck] = sum(plans[deck - s] for s in sizes if s <= deck)
      return plans

  print(plan_counts_for(8, (1, 2)))
  print(plan_counts_for(8, (2, 3, 5)))
  ```

  ```text
  [1, 1, 2, 3, 5, 8, 13, 21, 34]
  [1, 0, 1, 1, 0, 2, 2, 2, 3]
  ```

  The first line is Fibonacci, which tells you climbing-stairs problems and this
  one are the same problem wearing different clothes. The second has a `0` at
  index 1 and index 4 — with planks of 2, 3 and 5 there is genuinely no way to
  fill a deck of one, and the table says so without a special case.

- **Roll the table into three variables, then explain why you are not allowed
  to.**

  ```python
  def final_plan_count(capacity: int) -> int:
      """Only the last entry, in constant space."""
      a, b, c = 0, 0, 1  # counts for capacity-3, capacity-2, capacity-1
      for _ in range(capacity):
          a, b, c = b, c, a + b + c
      return c

  print(final_plan_count(18), plan_counts(18)[-1])
  ```

  ```text
  35890 35890
  ```

  Same answer, three integers of memory instead of nineteen. This is a **space
  reduction**, and it is legal only because the recurrence reads three entries
  back and no further. It is *not* legal under this exercise's contract, because
  the purser asked for the table. Recognising when the contract forbids the
  optimisation is the senior half of this skill.

- **Print the plans, not the count, for a small deck.**

  ```python
  def plans_for(deck: int) -> list[tuple[int, ...]]:
      """Every stint sequence loading exactly `deck` vehicles."""
      if deck == 0:
          return [()]
      return [
          (size,) + rest
          for size in STINT_SIZES
          if size <= deck
          for rest in plans_for(deck - size)
      ]

  for plan in plans_for(4):
      print(plan)
  ```

  ```text
  (1, 1, 1, 1)
  (1, 1, 2)
  (1, 2, 1)
  (1, 3)
  (2, 1, 1)
  (2, 2)
  (3, 1)
  ```

  Seven, as promised. Notice you cannot memoize this one usefully — the output
  is as big as the answer it describes, so there is nothing small to cache.
  Counting is cheap; listing is not. That difference decides a lot of interview
  problems.
When your table is right, move on to
[Exercise 2 — The Survey Station Walk](./exercise-02-survey-station-walk.md).
