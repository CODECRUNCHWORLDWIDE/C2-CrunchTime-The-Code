# Exercise 2 — The Survey Station Walk

> **Topic:** 1-D optimisation DP — the take-or-skip recurrence, with a second objective riding along in the state
> **Lecture:** [01 — The DP Pipeline and 1D States](../lecture-notes/01-the-dp-pipeline-and-1d-states.md)
> **Difficulty:** Intermediate
> **Target time:** 50 minutes
> **Why this one:** Exercise 1 counted things. This one **chooses** things, which is the other half of dynamic programming and the half interviews ask about. It also drills a habit most learners skip: when the contract has a tie-break, the tie-break belongs *inside* the DP, not bolted on afterwards.

## The Brief

A marine survey team walks a line of rock pools along the Kelbray shore, west
to east. A trial dip has already told them roughly how many species each pool
holds. Now they want to plan the real survey.

There is one rule, and it comes from the animals rather than from the
timetable. Properly surveying a pool means wading into it, and that scares
everything out of the pools immediately either side. So **no two neighbouring
pools can both be surveyed.** Pool 3 and pool 5, fine. Pool 3 and pool 4,
never.

The team wants the plan that records the **most species**. And there is a
second rule, because wading is slow and cold: among all the plans that record
the most species, they want the one that uses **the fewest pools**.

That second rule is not decoration. Look at a shore reading `4, 0, 0`. Wading
into pool 0 alone records 4 species from one pool. Wading into pool 0 *and*
pool 2 also records 4 species — pool 2 has nothing in it — but costs a second
cold morning. Both plans record the most species there is to record. Only the
second rule says which one the team should actually walk.

The recurrence in English, before any Python:

> **Walk the pools from west to east. At each pool you have exactly two
> choices. Skip it, and the best you can do is whatever was best up to the
> pool before. Or survey it, and the best you can do is this pool's species
> added to whatever was best up to the pool *two* back — because the pool
> immediately before is now off limits. Take the better of those two.**

"Better" is the whole contract in one word: more species, and on a tie, fewer
pools.

## Starter

Create `exercise-02-survey-station-walk.py` and paste this in. Fill in every
`TODO`.

```python
"""exercise-02-survey-station-walk.py — the take-or-skip walk.

No two neighbouring rock pools may both be surveyed. Record the most species;
on a tie, use the fewest pools.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from __future__ import annotations

import functools

KELBRAY_SHORE = (4, 9, 3, 8, 2, 6, 6, 1)


def better(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    """Pick the better of two (species, pools_used) plans.

    More species wins. On a tie, fewer pools wins. On a tie in both, the
    left-hand plan wins.
    """
    # TODO: three lines. Do not use max() here — max would compare the tuples
    #       box by box and treat MORE pools as better on a tie.
    ...


def best_survey_cached(counts: tuple[int, ...]) -> tuple[int, int]:
    """Top-down: the recurrence said out loud, with every answer remembered."""

    @functools.cache
    def best_from(pool: int) -> tuple[int, int]:
        """The best plan using only pools `pool` and eastwards."""
        # TODO: base case — past the end of the shore there is nothing to do
        # TODO: skip this pool, or take it and jump two along
        # TODO: return better(skip, take)
        ...

    return best_from(0)


def best_survey(counts: tuple[int, ...]) -> tuple[int, int]:
    """Return the best survey plan for a line of rock pools.

    Args:
        counts: Species counts, west to east. Every count is zero or more.

    Returns:
        A pair (species, pools_used).

    Raises:
        ValueError: If any count is negative.
    """
    # TODO: reject negative counts
    # TODO: keep two plans — the best up to the previous pool, and the best
    #       up to the one before that — and roll them forward
    ...


def survey_table(counts: tuple[int, ...]) -> list[tuple[int, int]]:
    """The full bottom-up table. Entry i covers the first i pools."""
    # TODO: allocate len(counts) + 1 entries of (0, 0), then fill upwards
    ...


if __name__ == "__main__":
    for i, plan in enumerate(survey_table(KELBRAY_SHORE)):
        print(i, plan)

    assert best_survey(()) == (0, 0)
    assert best_survey((7, 7)) == (7, 1)
    assert best_survey((4, 0, 0, 4)) == (8, 2)
    assert best_survey(KELBRAY_SHORE) == (24, 4)
    assert best_survey_cached(KELBRAY_SHORE) == best_survey(KELBRAY_SHORE)
    print("All checks passed.")
```

Three words you need before you start.

**State.** The smallest description of "where you are" that is enough to work
out the rest. Here it is a single number: which pool you are standing at. One
number means a **1-D** DP, and the table is a list.

**Objective.** The thing being maximised. Here there are two of them, ranked:
species first, then fewer pools. A ranked pair of objectives is still one
objective — you just compare in two steps.

**Rolling.** Keeping only the few table entries you still need instead of the
whole table. This recurrence never reads further back than two pools, so two
variables are enough.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-11-dynamic-programming-i/exercises/exercise-02-survey-station-walk.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `better(left, right)` returns the plan with more species; on a tie, the one
   with fewer pools; on a tie in both, `left`.
2. `best_survey(counts)` returns a `(species, pools_used)` tuple.
3. `best_survey(())` returns `(0, 0)`. An empty shore is not an error.
4. `best_survey((0,))` returns `(0, 0)`, not `(0, 1)`. A pool with nothing in
   it is not worth wading into.
5. `best_survey((4, 0, 0, 4))` returns `(8, 2)`.
6. `best_survey(KELBRAY_SHORE)` returns `(24, 4)`.
7. `best_survey` uses two rolling variables, not a full list.
8. `survey_table(counts)` returns `len(counts) + 1` entries, and its last entry
   equals `best_survey(counts)`.
9. `best_survey_cached` agrees with `best_survey` on every case.
10. A negative count raises `ValueError`.

## Constraints

- **Counts are zero or more.** A species count is a tally of animals seen; a
  negative tally is a data-entry error upstream, and silently treating it as a
  penalty would let the function paper over a broken input file. Raising is the
  honest response.

- **The shore may be empty, and may be one pool long.** Both are real: a team
  gets a stretch of coast with no pools mapped yet, or exactly one. Handling
  them with the same code as the general case — rather than with two `if`
  statements at the top — is a property of a correctly initialised table, and
  it is worth checking that yours has it.

- **Compare with `better`, never with `max`.** `max((9, 1), (9, 2))` returns
  `(9, 2)`, because tuples compare box by box and 2 is bigger than 1. That is
  the exact opposite of the tie-break you were asked for. Every time your
  objective is not "one number, bigger is better", write the comparison down as
  a named function so it can be read and tested on its own.

- **`best_survey` runs in constant extra space.** The recurrence reads two
  entries back and never further, so two variables carry everything the loop
  needs. `survey_table` exists separately because the walkthrough on this page
  needs the full list — that is a different question, and it gets a different
  function rather than a flag.

- **Up to 200,000 pools.** A shore survey of that length is about 60 km of
  coast at three pools per metre of walking, which is a season's work and a
  realistic upper bound for one dataset. The point of the bound is that it rules
  out anything quadratic: 200,000 squared is forty billion comparisons, and the
  linear walk does 200,000.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13:

```text
$ python exercise-02-survey-station-walk.py
pools considered  best plan (species, pools)
               0  (0, 0)
               1  (4, 1)
               2  (9, 1)
               3  (9, 1)
               4  (17, 2)
               5  (17, 2)
               6  (23, 3)
               7  (23, 3)
               8  (24, 4)

best_survey(()) == (0, 0)
best_survey((0,)) == (0, 0)
best_survey((7,)) == (7, 1)
best_survey((7, 7)) == (7, 1)
best_survey((4, 0, 0, 4)) == (8, 2)
best_survey((0, 0, 0)) == (0, 0)
best_survey((6, 1, 5, 1, 6)) == (17, 3)
best_survey((4, 9, 3, 8, 2, 6, 6, 1)) == (24, 4)

best_survey((3, -1)) raises ValueError: a species count cannot be negative
All checks passed.
```

Read the table down the left before you read anything else. Rows 3 and 5 and 7
do not change from the row above them — those are the pools the plan skips.
Row 8 jumps by only 1 species but adds a pool, and it still wins, because 24
beats 23 and the species total is checked first.

## Steps

1. Create the file, paste the starter, run it. It fails immediately; that is
   the correct start.
2. Write `better` first, and test it on its own in a REPL before anything else
   uses it. `better((9, 1), (9, 2))` must be `(9, 1)`.
3. Write `best_from` inside `best_survey_cached`. The base case is "past the
   end of the shore", and it returns `(0, 0)`. Note that `pool + 2` can run off
   the end — the base case handles that, which is why it says `>=` and not
   `==`.
4. Run with only the cached version done and check it against the four asserts
   by hand. Getting the recurrence right before you worry about the fill order
   is the whole reason the memoized form is written first.
5. Write `survey_table`. Walk `i` from 1 upwards, and for each `i` read
   `table[i - 1]` and `table[i - 2]`. The value at `i - 2` when `i` is 1 does
   not exist, so use `(0, 0)` there.
6. Write `best_survey` last, by deleting the list from `survey_table` and
   keeping the last two entries in two variables. Do it in that order. The
   rolling version is the hardest one to debug from scratch and the easiest one
   to derive from a table that already works.
7. Print the table and read it against the expected output row by row.

## The Solution

```python
"""exercise-02-survey-station-walk-solution.py — the take-or-skip walk.

Rock pools sit in a line along the Kelbray shore. Surveying a pool scares the
wildlife out of the pools either side of it, so no two neighbouring pools can
both be surveyed. Record as many species as possible; among the plans that
record the most, use the fewest pools.

`best_survey` returns `(species, pools_used)`.

The file carries the same rule twice — once as a memoized recursion and once as
a bottom-up table that keeps only two entries — and checks that they agree.
"""

from __future__ import annotations

import functools

# One stretch of shore, west to east. Each number is the species count found
# in a trial dip at that pool.
KELBRAY_SHORE = (4, 9, 3, 8, 2, 6, 6, 1)


def better(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    """Pick the better of two (species, pools_used) plans.

    More species wins. On a tie, fewer pools wins. On a tie in both, the
    left-hand plan wins, so the choice is never left to chance.
    """
    if right[0] > left[0]:
        return right
    if right[0] == left[0] and right[1] < left[1]:
        return right
    return left


def best_survey_cached(counts: tuple[int, ...]) -> tuple[int, int]:
    """Top-down: the recurrence said out loud, with every answer remembered."""

    @functools.cache
    def best_from(pool: int) -> tuple[int, int]:
        """The best plan using only pools `pool` and eastwards."""
        if pool >= len(counts):
            return (0, 0)
        skip = best_from(pool + 1)
        taken_species, taken_pools = best_from(pool + 2)
        take = (taken_species + counts[pool], taken_pools + 1)
        return better(skip, take)

    return best_from(0)


def best_survey(counts: tuple[int, ...]) -> tuple[int, int]:
    """Return the best survey plan for a line of rock pools.

    Args:
        counts: Species counts, west to east. Every count is zero or more.

    Returns:
        A pair (species, pools_used). The species total is the largest
        obtainable without surveying two neighbouring pools; pools_used is
        the smallest number of pools that reaches that total.

    Raises:
        ValueError: If any count is negative.
    """
    if any(count < 0 for count in counts):
        raise ValueError("a species count cannot be negative")

    # two_back is the best plan for the pools before the previous one,
    # one_back is the best plan for everything up to the previous one.
    two_back = (0, 0)
    one_back = (0, 0)
    for count in counts:
        take = (two_back[0] + count, two_back[1] + 1)
        two_back, one_back = one_back, better(one_back, take)
    return one_back


def survey_table(counts: tuple[int, ...]) -> list[tuple[int, int]]:
    """The full bottom-up table, kept for the walkthrough on the page.

    Entry i is the best plan considering the first i pools only, so entry 0
    is the empty plan and the last entry is the answer.
    """
    table: list[tuple[int, int]] = [(0, 0)] * (len(counts) + 1)
    for i in range(1, len(counts) + 1):
        two_back = table[i - 2] if i >= 2 else (0, 0)
        take = (two_back[0] + counts[i - 1], two_back[1] + 1)
        table[i] = better(table[i - 1], take)
    return table


def _report() -> None:
    """Print the table walk, the checks, and the agreement between the two."""
    print("pools considered  best plan (species, pools)")
    for i, plan in enumerate(survey_table(KELBRAY_SHORE)):
        print(f"{i:>16}  {plan}")

    cases: list[tuple[tuple[int, ...], tuple[int, int]]] = [
        ((), (0, 0)),                       # no shore at all
        ((0,), (0, 0)),                     # a barren pool is not worth a dip
        ((7,), (7, 1)),
        ((7, 7), (7, 1)),                   # neighbours: only one may be taken
        ((4, 0, 0, 4), (8, 2)),             # the tie-break earns its keep here
        ((0, 0, 0), (0, 0)),
        ((6, 1, 5, 1, 6), (17, 3)),
        (KELBRAY_SHORE, (24, 4)),
    ]
    print()
    for counts, expected in cases:
        rolled = best_survey(counts)
        recursed = best_survey_cached(counts)
        tabled = survey_table(counts)[-1]
        assert rolled == expected, f"{counts} -> {rolled}, expected {expected}"
        assert recursed == expected, f"cached disagrees on {counts}"
        assert tabled == expected, f"table disagrees on {counts}"
        print(f"best_survey({counts}) == {expected}")

    try:
        best_survey((3, -1))
    except ValueError as problem:
        print(f"\nbest_survey((3, -1)) raises ValueError: {problem}")

    print("All checks passed.")


if __name__ == "__main__":
    _report()
```

**The recurrence is two options and a comparison.** At every pool: skip it, or
take it. Skipping means the answer is whatever was best up to the previous pool.
Taking means this pool's species plus whatever was best two pools back. Nothing
else can happen, so `better(skip, take)` is the complete answer for that pool.
The reason a greedy rule fails here is worth saying out loud: taking the biggest
pool first forbids the two neighbours that might together be bigger. Three pools
reading `1, 2, 2` are enough to show it — greedy grabs the first 2 it sees, in
the middle, which forbids both of its neighbours and finishes on 2. The best
plan takes pools 0 and 2 for 3.

**The state is one number, so this is a 1-D DP.** "Which pool am I at" is
enough to decide the rest. You do not need to know which pools were already
taken, because the only thing the past can forbid is the pool immediately
behind you, and the recurrence handles that by jumping two.

**The tie-break lives inside the state, not outside it.** `better` is applied
at *every* pool, not once at the end. That matters: the plan for the first
three pools of `4, 0, 0, 4` is `(4, 1)` and not `(4, 2)`, and the pool-4 step
builds on it. If you maximised species during the walk and only counted pools
afterwards, you would already have thrown away the information you needed.
**A secondary objective must be part of the comparison from the first step.**

**The memoized version and the table version are the same recurrence facing
different directions.** `best_from(pool)` looks *forwards* — "the best I can
do from here east" — and recursion carries the answer back to the caller. The
table looks *backwards* — "the best plan for the first `i` pools" — and the
loop carries the answer forward. Either is fine. What is not fine is switching
direction halfway through and reading `table[i + 1]` in a loop that has not
filled it yet.

**Two variables replace the whole list because the recurrence never looks
further back than two.** `two_back` and `one_back` step along the shore
together, and the single line

```python
two_back, one_back = one_back, better(one_back, take)
```

does the shuffle in one go. Writing it as two separate assignments is the
classic way to break this: assign `one_back` first and `two_back` picks up the
new value instead of the old one. Python evaluates the whole right-hand side
before assigning any of the left, which is what makes the one-liner safe.

**`functools.cache` is applied to the inner function, not the outer one.**
`best_from` takes one integer, which is hashable, so it caches cleanly. If the
cache sat on `best_survey_cached` it would key on `counts` — a tuple, so still
hashable, but caching whole-problem answers rather than sub-answers, which
memoizes nothing useful. Cache the *subproblem*, always. And because the cache
is created fresh inside each call, two different shores can never contaminate
each other's results.

**Complexity.** Each pool is decided once and the decision is a constant amount
of work, so time is `O(n)` — linear in the number of pools. `best_survey` uses
`O(1)` extra space; `survey_table` uses `O(n)`, and it uses it on purpose,
because its whole job is to hand back the walkthrough.

## Run it

Copy the worked answer on this page into `exercise-02-survey-station-walk.py` and run it:

```bash
python exercise-02-survey-station-walk.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-02-survey-station-walk.py`.

## Common bugs to catch

- **`best_survey((0,))` returns `(0, 1)`.** Your `better` prefers the plan that
  arrived second, or does not check the pool count at all. Surveying a pool with
  nothing in it costs a wade and gains nothing, so the empty plan wins. This is
  the smallest case that tests the tie-break, which is why it is in the asserts.

- **`(9, 2)` where you expected `(9, 1)`.** You reached for `max`:

  ```text
  >>> max((9, 1), (9, 2))
  (9, 2)
  ```

  Tuples compare left to right: the 9s tie, so Python moves to the second box
  and 2 wins. `max` is answering "which tuple is larger" perfectly; that is just
  not the question. You could store the pool count negated — `(9, -1)` versus
  `(9, -2)` — and `max` would then be right, but a named `better` says the rule
  in words and can be unit-tested.

- **`IndexError: tuple index out of range`.**

  ```text
  Traceback (most recent call last):
    File "exercise-02-survey-station-walk.py", line 34, in best_from
      take = (best_from(pool + 2)[0] + counts[pool], ...)
                                       ~~~~~~^^^^^^
  IndexError: tuple index out of range
  ```

  Your base case says `if pool == len(counts)` and `pool + 2` skipped straight
  over it to `len(counts) + 1`. Use `>=`. Any recursion that can step by more
  than one needs a base case that catches *past* the end, not only *at* it.

- **The whole table is right but the last entry is wrong.** You looped `i` from
  0 instead of 1, overwrote `table[0]`, and lost the base case. The table has
  `n + 1` entries for `n` pools precisely so that entry 0 can mean "no pools
  considered yet"; the loop starts at 1 for the same reason.

- **`two_back` and `one_back` both end up holding the same thing.** You wrote:

  ```python
  one_back = better(one_back, take)
  two_back = one_back        # too late — one_back already changed
  ```

  Do the swap in one tuple assignment, or save the old value in a temporary
  first. This bug produces answers that are too *large*, because a pool ends up
  allowed to sit next to its own neighbour.

- **`TypeError: unhashable type: 'list'`.**

  ```text
  TypeError: unhashable type: 'list'
  ```

  You passed a list of counts into something decorated with `functools.cache`.
  The shore is a `tuple` in this exercise for exactly that reason. If your
  caller has a list, convert it once at the boundary: `tuple(counts)`.

- **A `RecursionError` on a long shore.**

  ```text
  RecursionError: maximum recursion depth exceeded
  ```

  `best_survey_cached` recurses once per pool, so 200,000 pools means 200,000
  stack frames and CPython stops at around 1,000. The memoized form is for
  getting the recurrence right; the rolling form is what you would actually
  ship. That is the honest division of labour between them.

## Under the hood

<details>
<summary>Under the hood — why greedy fails here, and what "optimal substructure" is actually claiming</summary>

**The greedy rule that everyone tries first.** Sort the pools by species,
descending; take the biggest, cross out its neighbours, repeat. It is fast, it
is easy, and it is wrong. The smallest counterexample is three pools:

```text
counts = (1, 2, 2)
greedy : the biggest count is 2, and the first one is in the middle.
         Take pool 1, cross out pools 0 and 2. Nothing is left. Total 2.
best   : take pools 0 and 2 → 1 + 2 = 3.
```

Greedy lost one species by grabbing a pool that was tied for biggest and sat in
the worst place. Note how narrow the failure is: change the shore to `(2, 2, 1)`
and greedy takes pool 0, then pool 2, and gets 3 — the right answer. **A rule
that is right most of the time and wrong sometimes is the most expensive kind
of bug**, because the tests you write by hand will pass.

The reason to distrust greedy is not that somebody showed you a counterexample.
It is that greedy has no argument behind it. The DP does, and here it is.

**Optimal substructure, precisely.** The claim the DP relies on is: *the best
plan for the first `i` pools contains, inside it, a best plan for the first
`i-1` or the first `i-2` pools.* Suppose it did not — suppose the best plan for
`i` pools ends by taking pool `i-1`, and the part of it covering the first `i-2`
pools is not itself best. Then swap that part for the genuinely best plan of the
first `i-2` pools. The swap is legal, because nothing in the first `i-2` pools
can be adjacent to pool `i-1` except pool `i-2`, which is excluded in both. And
the swap cannot make the total worse. So the original plan was not best after
all — a contradiction. That argument is called an *exchange argument*, and it
is the standard way to justify a DP recurrence in an interview.

**Overlapping subproblems, precisely.** The other trigger. Without a cache,
`best_from(0)` calls `best_from(1)` and `best_from(2)`; `best_from(1)` calls
`best_from(2)` again. The same state is reached down two different paths, which
is what "overlapping" means. The count grows the way Fibonacci does:
`best_from(0)` on a shore of 30 pools reaches its body 4,356,617 times with no
cache, and exactly 32 times with one — once for each of the 32 states it can
possibly be asked about.

**When the second objective changes the answer.** Because species counts are
never negative, the fewest-pools rule can only ever break a tie caused by a
zero-count pool, or by a pool whose species exactly balance an alternative. On
real survey data that is rare. Rare is not never, and "rare" is what makes it a
good exercise: a bug that fires on one dataset in fifty is far more expensive
than one that fires every time.

**A note on `functools.cache` and closures.** The inner `best_from` is
redefined on every call to `best_survey_cached`, which means a brand-new cache
each time. That costs a little — building the decorated function is not free —
and buys correctness: a cache keyed only on `pool` would be catastrophically
wrong if it survived between two different shores. If you ever move the cached
function to module level, the shore must become part of its arguments.

</details>

## Acceptance checklist

- [ ] `python exercise-02-survey-station-walk.py` prints the nine table rows then `All checks passed.`
- [ ] `better` is a separate, testable function and does not use `max`.
- [ ] `best_survey(())` is `(0, 0)` and `best_survey((0,))` is `(0, 0)`.
- [ ] `best_survey((4, 0, 0, 4))` is `(8, 2)`.
- [ ] `best_survey` keeps two variables, not a list.
- [ ] `survey_table(counts)[-1] == best_survey(counts)` for every case you try.
- [ ] A negative count raises `ValueError`.
- [ ] You can state the recurrence in one English sentence before showing code.
- [ ] Committed to Git with a message like `Add Week 11 exercise 2: survey station walk`.

## Stretch

- **Return the pools, not just the count.** The table already holds enough to
  walk backwards and recover the plan.

  ```python
  def chosen_pools(counts: tuple[int, ...]) -> list[int]:
      """Which pools the best plan surveys, west to east."""
      table = survey_table(counts)
      picked: list[int] = []
      i = len(counts)
      while i > 0:
          if table[i] == table[i - 1]:
              i -= 1                      # this pool was skipped
          else:
              picked.append(i - 1)
              i -= 2                      # taken, so its neighbour is out
      return picked[::-1]

  print(chosen_pools(KELBRAY_SHORE))
  ```

  ```text
  [1, 3, 5, 7]
  ```

  Note what this costs you: reconstruction needs the whole table, so the two
  rolling variables are no longer enough. **Asking for the plan rather than the
  score is what forces you to keep the table.** That trade comes back in the
  mini-project.

- **Make the shore a loop.** Suppose the pools ring a tidal island, so the last
  pool neighbours the first.

  ```python
  def best_ring_survey(counts: tuple[int, ...]) -> tuple[int, int]:
      """The same rule, on a closed ring of pools."""
      if len(counts) <= 1:
          return best_survey(counts)
      return better(best_survey(counts[:-1]), best_survey(counts[1:]))

  print(best_survey((5, 1, 1, 5)), best_ring_survey((5, 1, 1, 5)))
  print(best_survey((9, 1, 1, 9)), best_ring_survey((9, 1, 1, 9)))
  ```

  ```text
  (10, 2) (6, 2)
  (18, 2) (10, 2)
  ```

  The trick is to notice that the first and last pool cannot both be taken, so
  every valid ring plan is a valid line plan on one of two shores: everything
  but the last pool, or everything but the first. Two runs of a function you
  already have, and no new recurrence at all.

- **Let a pool cost something to reach.** Give every pool a wading cost and
  maximise species minus cost.

  ```python
  def best_net_survey(counts: tuple[int, ...], costs: tuple[int, ...]) -> tuple[int, int]:
      """Maximise species minus wading cost; on a tie, fewest pools."""
      two_back, one_back = (0, 0), (0, 0)
      for count, cost in zip(counts, costs):
          take = (two_back[0] + count - cost, two_back[1] + 1)
          two_back, one_back = one_back, better(one_back, take)
      return one_back

  print(best_net_survey(KELBRAY_SHORE, (1, 1, 1, 1, 1, 1, 1, 1)))
  print(best_net_survey(KELBRAY_SHORE, (0, 8, 0, 8, 0, 8, 0, 8)))
  ```

  ```text
  (20, 3)
  (15, 4)
  ```

  The recurrence did not change at all — only the number being added did. That
  is the sign that you learned a shape and not an answer.
When your walk is right, move on to
[Exercise 3 — The Stencil Line](./exercise-03-stencil-line-split.md).
