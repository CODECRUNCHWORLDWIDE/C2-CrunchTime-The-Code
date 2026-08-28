# Exercise 5 — The Longest Dock Run

> **Topic:** a set for membership, plus the amortisation argument that makes a loop-inside-a-loop linear
> **Lecture:** [01 — Mental Models for Big-O](../lecture-notes/01-mental-models-for-big-o.md)
> **Difficulty:** Medium
> **Target time:** 75 minutes
> **Why this one:** the code here is eleven lines and easy. The *defence* is the exercise. Your solution contains a `while` loop inside a `for` loop and is nevertheless `O(n)`, and an interviewer will absolutely ask you why. This is the page where you learn to answer that, and the answer — total work bounded by counting each element once — is the same argument behind `list.append`, behind dict resizing, and behind half the algorithms in the rest of this course.

## The Brief

Picture a street with bike docks numbered along it: 87, 88, 89, and so on.
Overnight, every dock that is working phones home. A flaky one might phone twice.
A dead one does not phone at all.

In the morning you have a bag of numbers in no particular order, and one
question: **what is the longest unbroken stretch of docks where every single
dock phoned in?**

The obvious plan is to sort the numbers and look for gaps. It works. It is also
banned here, and the ban is the point of the exercise — you have to find the
answer without ever putting the numbers in order.

Here is how. Tip every number into a **set**, which can answer "is dock 4020 in
there?" instantly. Now think about what makes a number the *start* of a stretch:
it is the start exactly when the number one below it is missing. Dock 4019
starts a run if 4018 did not phone in. So walk over the numbers, ignore every
one that is not a start, and from each start count forward — 4020? yes. 4021?
yes. 4022? no, stop. Length 3.

That has a loop inside a loop, and it is still linear, because the stretches do
not overlap: each dock gets counted forward through exactly once, by exactly one
start. That sentence is the thing to memorise, and there is a whole section
below on saying it well.

The contract:

Given the unsorted list of dock IDs that reported in, find the **longest run of
consecutive IDs** in which every dock reported. Return the run as
`(first_id, length)`.

If two runs tie on length, return the one with the **smaller first ID**. If the
list is empty, return `None`.

Your solution must run in **`O(n)` expected time.** Sorting is not permitted,
and neither is anything else that reintroduces a `log n` factor.

## Starter

Create `exercise-05-longest-dock-run.py` in your practice repo and paste this
in. Fill in the `TODO`.

```python
"""exercise-05-longest-dock-run.py — the longest run of docks.

Fill in the TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the function is correct.
"""


def longest_dock_run(reported: list[int]) -> tuple[int, int] | None:
    """Return the start and length of the longest run of consecutive docks.

    Args:
        reported: Dock IDs that phoned home overnight, unsorted, possibly
            with repeats.

    Returns:
        (first_id, length) for the longest run of consecutive IDs all
        present, ties broken toward the smaller first_id. None if nothing
        reported.
    """
    # TODO: build a set. Iterate the SET, not the list. Skip any dock whose
    # predecessor is present — it is not the start of a run. From each start,
    # walk forward. Track the best, and get the tie-break right.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[int], tuple[int, int] | None]] = [
        ([4021, 88, 4019, 4020, 87, 700], (4019, 3)),
        ([12, 13, 40, 41], (12, 2)),
        ([50, 50, 51, 50], (50, 2)),
        ([9], (9, 1)),
        ([], None),
        ([5, 3, 1], (1, 1)),
        ([1000, 999, 998, 997, 996, 2, 1], (996, 5)),
        ([1, 2, 3, 4, 5, 6, 7, 8], (1, 8)),
    ]

    for reported, expected in cases:
        found = longest_dock_run(reported)
        assert found == expected, (reported, found, expected)
        counted = f"{len(reported)} reported"
        if found is None:
            print(f"{counted:<12} ->  nothing reported")
        else:
            start, length = found
            docks = f"{length} dock" + ("" if length == 1 else "s")
            print(f"{counted:<12} ->  {docks} from {start}")

    print("All checks passed.")
```

Three words before you start.

**Root.** The smallest member of a run. Dock `x` is a root exactly when `x - 1`
is not in the set. Every run has exactly one root, and only roots start a walk.

**Disjoint.** Two things are disjoint when they share nothing. Runs are
disjoint: a dock belongs to one run and no other. That is the fact that makes
the nested loop linear, and it is the word to reach for when you are asked.

**Amortised.** A cost that is expensive sometimes and cheap usually, and
constant when you spread it over the whole run. That is what is happening to
the inner `while` here: a few iterations of the outer loop do a lot of inner
work and most do none at all, and the total is still bounded by `n`.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-02-complexity-and-hash-maps/exercises/exercise-05-longest-dock-run.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `longest_dock_run` returns `(first_id, length)` — **both** parts. The length
   alone is half an answer.
2. Ties on length break toward the **smaller** first ID.
3. Empty input returns `None`, not `(0, 0)`.
4. Duplicates carry no information. `[50, 50, 51, 50]` is `(50, 2)`.
5. It runs in `O(n)` expected time. No `sorted()`, no `.sort()`, no heap, no
   binary search.
6. It iterates the **set**, not the original list.
7. The answer is deterministic — running it twice on the same input gives the
   same answer, and so does running it on a shuffled copy of that input.
8. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(reported) <= 300_000`.** Be honest about what this bound does and
  does not do. It does **not** reject a sort: `sorted()` on three hundred
  thousand integers finishes in a fraction of a second, and if the bound were
  the only thing standing in the way, the `O(n log n)` solution would be
  perfectly fine. The `O(n)` requirement here is a **spec** requirement, and
  this exercise exists so that you defend it rather than get rescued by a timer.
  What the bound *does* reject is the `O(n^2)` shape — "for each ID, scan the
  whole list looking for `id + 1`" — which is about `9 x 10^10` comparisons.

- **`1 <= reported[i] <= 2_000_000_000`.** Dock IDs are allocated regionally
  across a two-billion-wide space and are extremely sparse. This is the bound
  that forces a hash set: an array of flags indexed by dock ID would need two
  billion slots on a night when four hundred docks reported. Space must be
  proportional to the number of docks, not to the width of the ID space. This is
  Exercise 2's constraint again, two hundred times louder, and it is the sentence
  that belongs in the space half of your cost statement.

- **Duplicates are expected and carry no information.** A dock that reported
  twice is one dock. This is why the first line builds a `set`: deduplication is
  not a tidy-up, it is part of the definition of the answer. It is also what
  makes iterating the set rather than the list a correctness-adjacent decision
  and not just a speed one — see Common bugs.

- **The tie-break is stated because set iteration order cannot be trusted.**
  Without a rule, `[5, 3, 1]` could legitimately answer `(5, 1)`, `(3, 1)` or
  `(1, 1)` depending on how CPython happened to lay out the table, and the
  answer could change when you refactored something unrelated. Specifying the
  smaller first ID makes the function deterministic. A contract that pins down
  what the runtime leaves loose is doing real work.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-05-longest-dock-run-solution.py
6 reported   ->  3 docks from 4019
4 reported   ->  2 docks from 12
4 reported   ->  2 docks from 50
1 reported   ->  1 dock from 9
0 reported   ->  nothing reported
3 reported   ->  1 dock from 1
7 reported   ->  5 docks from 996
8 reported   ->  8 docks from 1
All checks passed.
```

Two rows to look at.

**`[5, 3, 1]` answers `1 dock from 1`.** Three isolated docks, three runs of
length one, a three-way tie. If your comparison is only `length > best_length`,
you keep whichever run the set handed you first — and CPython's iteration order
for small integers is a hash-table artefact, neither the insertion order nor the
sorted order. Your function would look right, pass most cases, and change its
answer under an unrelated edit.

**`[1, 2, 3, 4, 5, 6, 7, 8]` answers `8 docks from 1`.** Every solution gets this
right, which is exactly why it matters: it is the input that separates a correct
`O(n)` solution from a correct `O(n^2)` one. Without the root check, the walk
from 8 does one step, from 7 does two, from 6 does three, and so on — 36 inner
steps for 8 docks. With the root check only `1` is a root, and the total is 8.
Scale that to three hundred thousand and the difference is the whole exercise.

## Steps

1. Create the file, paste the starter, and run it. Every case fails.
2. Write `docks = set(reported)` and the empty guard. Run. Every non-empty case
   now fails on `None`, which is progress.
3. Write the outer loop over `docks` with **only** the root check and a `print`
   of each root. Run it against `[4021, 88, 4019, 4020, 87, 700]`. You should see
   exactly three roots printed — 4019, 87 and 700 — in some order you cannot
   predict. That unpredictability is the reason requirement 7 exists.
4. Add the inner walk and print `(root, length)` for each. Three lines,
   `(4019, 3)`, `(87, 2)`, `(700, 1)`.
5. Now add the best-so-far comparison, with all three conditions. Run. All eight
   cases should pass.
6. Break it on purpose: drop the root check. Everything still passes, and your
   solution is now quadratic. This is the most important thing on the page —
   **the tests cannot tell you about this bug.** Add a counter that increments
   on every inner step, run `list(range(1, 2001))` through both versions, and
   look at the two numbers. Roughly 2,000 against roughly 2,000,000.
7. Practise the `O(n)` defence below out loud until it is thirty seconds and
   confident.

## The Solution

```python
"""exercise-05-longest-dock-run-solution.py — the longest run of docks.

Put every reported ID in a set, then walk forward only from the IDs that start
a run. An ID starts a run when its predecessor is missing. Runs are disjoint,
so the walks together take at most one step per dock, and the whole thing is
O(n) with no sort anywhere.

Time: O(n) expected — n set inserts, one outer pass over the distinct IDs, and
at most n inner steps in total.
Space: O(n) — one set entry per distinct dock, never O(2_000_000_000).

The self-checks at the bottom are the starter's, unchanged. When they all pass
the file prints "All checks passed."
"""


def longest_dock_run(reported: list[int]) -> tuple[int, int] | None:
    """Return the start and length of the longest run of consecutive docks.

    Args:
        reported: Dock IDs that phoned home overnight, unsorted, possibly
            with repeats.

    Returns:
        (first_id, length) for the longest run of consecutive IDs all
        present, ties broken toward the smaller first_id. None if nothing
        reported.
    """
    docks = set(reported)
    if not docks:
        return None

    best: tuple[int, int] | None = None
    for dock in docks:
        if dock - 1 in docks:
            continue  # not the root of its run; some other root will walk it
        length = 1
        while dock + length in docks:
            length += 1
        if best is None or length > best[1] or (length == best[1] and dock < best[0]):
            best = (dock, length)
    return best


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[int], tuple[int, int] | None]] = [
        ([4021, 88, 4019, 4020, 87, 700], (4019, 3)),
        ([12, 13, 40, 41], (12, 2)),
        ([50, 50, 51, 50], (50, 2)),
        ([9], (9, 1)),
        ([], None),
        ([5, 3, 1], (1, 1)),
        ([1000, 999, 998, 997, 996, 2, 1], (996, 5)),
        ([1, 2, 3, 4, 5, 6, 7, 8], (1, 8)),
    ]

    for reported, expected in cases:
        found = longest_dock_run(reported)
        assert found == expected, (reported, found, expected)
        counted = f"{len(reported)} reported"
        if found is None:
            print(f"{counted:<12} ->  nothing reported")
        else:
            start, length = found
            docks = f"{length} dock" + ("" if length == 1 else "s")
            print(f"{counted:<12} ->  {docks} from {start}")

    print("All checks passed.")
```

**One line does the deduplication, and it is part of the answer, not a tidy-up.**

```python
docks = set(reported)
```

A dock that phoned twice is one dock, so the multiset of reports is not the
thing the question is about — the *set* of docks is. Building the set states
that, and it is also what makes membership a lookup instead of a search.

**The root check is the whole trick.**

```python
if dock - 1 in docks:
    continue
```

Read it as English: *if the dock below me also reported, then I am in the middle
of somebody else's run, and they will count me.* Only a dock whose predecessor
is missing starts a walk. Without this line the algorithm is still correct — the
longest run is still found — and it is quadratic, because every member of a long
run walks its own tail.

**The inner walk is bounded, and here is the argument.** The walk from a root
steps forward through the members of that root's run and stops at the first gap.
Runs are **disjoint**: a dock belongs to exactly one run, so it is stepped
through by exactly one root's walk, exactly once. Sum the inner steps over every
root and you get at most one step per distinct dock — at most `n`. Add the outer
loop's `n` iterations and the `n` inserts that built the set, and the entire
algorithm is bounded by about `3n`, which is `O(n)`.

That is the paragraph an interviewer is listening for, and it is the same shape
of argument as "`list.append` is amortised `O(1)`": individual steps vary wildly,
the total is what is bounded. Being able to reason about a *total* rather than a
*worst single step* is the skill, and it recurs constantly from here on.

**Three conditions in the comparison, not one.**

```python
if best is None or length > best[1] or (length == best[1] and dock < best[0]):
```

The first handles "nothing chosen yet". The second is the real ranking. The
third is the tie-break, and it is not optional decoration: without it,
`[5, 3, 1]` returns whichever of the three roots the set iteration reached
first. Set iteration order in CPython depends on the values, the table size and
the insertion history — it is deterministic for a given run but it is not
something the contract can rely on, and it changes if you touch anything.
A function whose answer depends on that is a function that will one day change
its answer for no reason you can find.

**Iterate `docks`, not `reported`.** On a list where one dock reported fifty
thousand times, iterating the list runs the outer loop fifty thousand times for
that dock, and every one of those is a root, and every one re-walks the whole
run. The complexity collapses back to quadratic because of one wrong word. The
set has each dock once, which is exactly the "at most one walk per dock"
property the argument above depends on.

**`length` starts at 1 because the root counts itself.** Then `while dock +
length in docks` asks about the next one along. When the loop exits, `length` is
the *count* of docks in the run — not the last ID, not an offset. Trace
`[9]`: the `while` never runs, `length` stays 1, and the answer is `(9, 1)`,
which is right, because one dock is a run of one.

**The cost, said properly.** *Time `O(n)` expected*: `n` set inserts at `O(1)`
average, one outer iteration per distinct dock, and inner steps totalling at
most `n` by the disjointness argument. *Space `O(n)`*: one set entry per
distinct dock — and pointedly **not** `O(2 x 10^9)`, which is what the flag
array would cost. *Best, average and worst are all `O(n)`*: there is no early
exit, because the longest run could be the last one examined. The set's own
worst case is `O(n)` per lookup under adversarial collisions, which is why the
claim says "expected". *Tradeoff*: sort-then-scan is `O(n log n)` time and,
sorting in place, `O(1)` extra space — genuinely better on memory, and forbidden
here on time. A `Counter` buys nothing at all: the question is membership, not
multiplicity. *Improvement*: none. Every ID must be read, so `O(n)` is the
floor.

## Download and run

Download
[exercise-05-longest-dock-run-solution.py](./exercise-05-longest-dock-run-solution.py)
and run it:

```bash
python exercise-05-longest-dock-run-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-05-longest-dock-run.py`.

## Common bugs to catch

- **`TypeError: 'NoneType' object is not subscriptable`.** You compared against
  `best` before checking whether anything had been chosen yet:

  ```text
  Traceback (most recent call last):
      if length > best[1]:
                  ~~~~^^^
  TypeError: 'NoneType' object is not subscriptable
  ```

  `best is None` has to be the *first* condition in the chain, because `or`
  short-circuits and the later conditions are only safe once it is false.

- **`AssertionError` on `([5, 3, 1], ...)`, got `(3, 1)` or `(5, 1)`.** No
  tie-break:

  ```text
  Traceback (most recent call last):
      assert found == expected, (reported, found, expected)
             ^^^^^^^^^^^^^^^^^
  AssertionError: ([5, 3, 1], (3, 1), (1, 1))
  ```

  Which value you get depends on set iteration order, so this bug can pass on
  one machine and fail on another, or pass today and fail after an unrelated
  edit. Add `(length == best[1] and dock < best[0])`.

- **`AssertionError` on `([], ...)`, got `(0, 0)`.** You initialised `best =
  (0, 0)` instead of `None` and never guarded the empty case. `(0, 0)` is a
  valid-looking run that a caller will happily use, and there is no dock 0.

- **`RuntimeError: Set changed size during iteration`.** You mutated `docks`
  inside the loop, most likely trying to remove docks you had already walked:

  ```text
  Traceback (most recent call last):
      for dock in docks:
  RuntimeError: Set changed size during iteration
  ```

  Removing as you go is a real optimisation, and it needs a copy to iterate:
  `for dock in list(docks)` or, better, leave it alone — the root check already
  gives you the linear bound.

- **The right answer, quadratic.** You dropped `if dock - 1 in docks: continue`.
  Nothing fails. Every self-check passes. The only way to see this bug is to
  count the inner steps, which is step 6 above. Treat "all my tests pass" as
  saying nothing at all about complexity, because it does not.

- **Iterating `reported` instead of `docks`.** Same symptom: correct answers,
  quadratic cost, on any input with many duplicates. One word.

- **Off-by-one on `length`.** Starting at 0, or writing
  `while dock + length + 1 in docks`. Trace `[9]`: the answer must be `(9, 1)`.

- **Returning only the length.** `3` instead of `(4019, 3)`. Read the return
  annotation. Carrying the start is half of this exercise.

- **Reaching for `sorted()` anyway.** It is one line, it is correct, and it is
  disallowed. If you wrote it, you have a good solution to a problem nobody
  asked for.

## Under the hood

<details>
<summary>Under the hood — the O(n) defence in full, and why "there is a loop inside a loop" is not an argument</summary>

**Say this out loud until it is thirty seconds and confident.**

> "Why this is `O(n)` and not `O(n^2)`. The inner walk only runs when the
> current dock is a run root — a dock with no predecessor in the set. Each
> root's walk steps forward through the members of its own run and stops at the
> first gap. Runs are disjoint: a dock belongs to exactly one run, so it is
> stepped through by exactly one root's walk, exactly once. So the total number
> of inner steps summed over every root is bounded by the number of distinct
> docks, which is at most `n`. Add the outer loop's `n` iterations and the `n`
> inserts that built the set, and the whole algorithm is bounded by `3n`, which
> is `O(n)`."

The word doing the work is **disjoint**. If you cannot say why the runs are
disjoint, you have memorised the trick rather than understood it — and "but
there is a loop inside a loop, so isn't that quadratic?" is a follow-up you will
certainly be asked.

The answer to that follow-up: nesting tells you nothing on its own. What matters
is the *total* number of inner iterations across the whole outer loop, not the
worst count for a single outer iteration. Here one outer iteration can do up to
`n` inner steps — a single run containing everything — and precisely because it
did, no other outer iteration does any. The maximum of one iteration and the sum
over all iterations are different quantities, and complexity is about the sum.

**The same argument, three other places you have already met it.**

- **`list.append`.** Usually it writes one slot. Occasionally the list is full,
  and Python allocates a bigger array and copies everything, which is `O(n)`.
  Because the array grows by a factor rather than by a fixed amount, the
  expensive copies get rarer exactly as fast as they get more expensive, and the
  total cost of `n` appends is `O(n)`. That is *amortised* `O(1)` per append.
- **Dict resizing.** Same story, same reason: the table doubles, so the total
  re-filing work across `n` inserts is `O(n)`.
- **Two pointers, from Week 1.** In the converging scan, each iteration moves
  one pointer inward and pointers never move apart, so the total movement is
  bounded by `n` even though no single iteration is bounded by anything useful.

Learn to recognise the shape: *the individual step is unbounded, the total is
bounded by counting something once.* You will use it in Week 3's sliding window,
in Week 10's union-find, and in almost every amortised argument after that.

**Why "expected" and not "worst case".** The set operations are `O(1)` on
average and `O(n)` in the pathological case where every key collides. Python
randomises string hashing per process to make that unconstructible for string
keys; integer hashes are the integers themselves and are not randomised, so an
adversary who chose dock IDs could in principle build a colliding set. It is a
curiosity rather than a threat, but the honest phrase is "`O(n)` expected", and
saying it costs you one word.

**Why the space is `O(n)` and not `O(max ID)`.** The set holds one entry per
distinct dock that reported — four hundred entries on a quiet night — regardless
of the fact that IDs range over two billion values. The array-of-flags design
would allocate two billion slots to store four hundred facts. This is the
central reason hash structures exist, and the ID-range constraint on this page
is there purely so you have to say it.

</details>

## Acceptance checklist

- [ ] `python exercise-05-longest-dock-run.py` prints eight rows then `All checks passed.`
- [ ] The rows match the expected output character for character.
- [ ] The root check `if dock - 1 in docks: continue` is present.
- [ ] The outer loop iterates the **set**, not the list.
- [ ] The comparison has all three conditions, tie-break included.
- [ ] Empty input returns `None`.
- [ ] There is no `sorted`, no `.sort`, no heap and no binary search anywhere.
- [ ] You counted the inner steps with and without the root check, and wrote the
      two numbers down.
- [ ] You can deliver the `O(n)` defence in thirty seconds without notes.
- [ ] Committed to Git with a message like `Add Week 2 exercise 5: longest dock run`.

## Stretch

- **Count the inner steps, so the complexity claim stops being a claim.**

  ```python
  def longest_dock_run_counted(reported: list[int]) -> tuple[tuple[int, int] | None, int]:
      """Same answer, plus how many inner walk steps it took."""
      docks = set(reported)
      if not docks:
          return (None, 0)
      steps = 0
      best: tuple[int, int] | None = None
      for dock in docks:
          if dock - 1 in docks:
              continue
          length = 1
          while dock + length in docks:
              length += 1
              steps += 1
          if best is None or length > best[1] or (length == best[1] and dock < best[0]):
              best = (dock, length)
      return (best, steps)

  print(longest_dock_run_counted(list(range(1, 2001))))
  print(longest_dock_run_counted([n * 3 for n in range(1, 2001)]))
  ```

  ```text
  ((1, 2000), 1999)
  ((3, 1), 0)
  ```

  Two thousand docks, one unbroken run, 1,999 inner steps — under `n`, exactly
  as the argument promised. Two thousand docks with no run at all, zero inner
  steps. Now delete the root check and run the first line again: 1,999,000. That
  is the difference the argument is describing, in a number you produced
  yourself.

- **Return every run, longest first.** The operator would rather see the whole
  picture than the winner.

  ```python
  def all_dock_runs(reported: list[int]) -> list[tuple[int, int]]:
      """Return every run as (first_id, length), longest first, ties by first_id."""
      docks = set(reported)
      runs: list[tuple[int, int]] = []
      for dock in docks:
          if dock - 1 in docks:
              continue
          length = 1
          while dock + length in docks:
              length += 1
          runs.append((dock, length))
      return sorted(runs, key=lambda run: (-run[1], run[0]))

  print(all_dock_runs([4021, 88, 4019, 4020, 87, 700]))
  print(all_dock_runs([]))
  ```

  ```text
  [(4019, 3), (87, 2), (700, 1)]
  []
  ```

  Note that a sort is fine *here*, because it sorts the runs — of which there are
  at most `n` but usually far fewer — rather than the docks. The spec banned
  sorting the input to find the answer; it did not ban sorting a report. Being
  precise about what a constraint actually forbids is worth a mark on its own.

- **Find the longest run of *missing* docks between the reported ones.**

  ```python
  def longest_gap(reported: list[int]) -> tuple[int, int] | None:
      """Return (first_missing_id, length) of the longest all-missing stretch."""
      docks = set(reported)
      if len(docks) < 2:
          return None
      ends = [dock for dock in docks if dock + 1 not in docks]
      best: tuple[int, int] | None = None
      for end in ends:
          nxt = end + 1
          while nxt not in docks and nxt <= max(docks):
              nxt += 1
          length = nxt - end - 1
          if length and (best is None or length > best[1] or
                         (length == best[1] and end + 1 < best[0])):
              best = (end + 1, length)
      return best

  print(longest_gap([4021, 88, 4019, 4020, 87, 700]))
  print(longest_gap([5, 6, 7]))
  ```

  ```text
  (701, 3318)
  None
  ```

  The same shape upside down: a stretch of missing docks starts just after a
  dock whose successor is absent. The answer is the yawning gap between dock 700
  and dock 4019, not the smaller one after 88 — worth checking by hand, because
  the eye goes to the first gap rather than the biggest.

  Two things to notice in the code. It calls `max(docks)` **inside** the loop,
  which is `O(n)` every time and quietly makes the whole function quadratic;
  hoisting it above the loop is the fix, and spotting it is the exercise. And
  the inner `while` here is *not* covered by the disjointness argument, because
  it walks over docks that are absent from the set rather than present in it —
  so the bound has to come from the ID range, not from `n`. An argument that
  worked on one page and does not work on the next is worth ten minutes of your
  attention.

**Practice elsewhere.** The same pattern appears as [LeetCode 128 · Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) if you want a judge to run against. The contract there returns only the length, so it never forces you to carry the run's start or to define a tie-break — and the tie-break is what makes this page's answer deterministic.

---

That is all five exercises. Next, take the [quiz](../quiz.md), then work the
[challenges](../challenges/README.md), the [homework](../homework/README.md),
and the [mini-project](../mini-project/README.md).
