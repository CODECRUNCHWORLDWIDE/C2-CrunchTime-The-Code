# Exercise 5 — The Cold-Chain Load

> **Topic:** the at-most-K-distinct window — a growing window whose state is a frequency table and whose limit arrives as a parameter
> **Lecture:** [02 — The Shrinking and Growing Mechanics](../lecture-notes/02-the-shrinking-and-growing-mechanics.md)
> **Difficulty:** Medium
> **Target time:** 60 minutes
> **Why this one:** the most reusable template of the week. "The longest stretch containing at most `K` different things" is an entire family of interview problems wearing different costumes. Write it once with `k` as a parameter and you have written all of them. The page also puts the two zero cases — an empty conveyor and a van with no compartments — in your way on purpose.

## The Brief

A depot loads a refrigerated van straight off a conveyor belt. Every package
carries a **temperature class** printed on it — `"ambient"`, `"chilled"`,
`"frozen"`, and a few others.

The van has `k` compartments. Each compartment gets set to exactly one
temperature class, and once it is set it will hold any number of packages of
that class — but only that class. So a van with two compartments can carry
frozen and chilled goods together in any quantity, and cannot carry a third
class at all.

The loader takes packages off the conveyor in a **contiguous run**. No skipping
— the belt does not reverse and the loader does not reach past anything. Every
package in the run has to go into some compartment. Putting those two facts
together gives you the rule:

> A run is loadable exactly when it contains **at most `k` distinct classes**.

Notice what the limit is *not* on. It is not on how many packages you take —
take a thousand frozen boxes if you like. It is on how many *different* classes
appear among them. A run of forty packages that are all `"chilled"` needs one
compartment.

**Your job.** Return the longest loadable run as `(start, count)`: the index of
its first package and how many packages it holds.

The technique is the growing window from Exercise 2, with a different thing
inside it. Instead of a dictionary remembering *where* each item was last seen,
keep a **frequency table**: how many of each class are currently inside the
window. Then "how many distinct classes are in the window" is just how many
keys the table has, and the promise you are keeping is `len(counts) <= k`.

Push the right edge out one package at a time. When the table grows past `k`
keys, the promise is broken, so pull the left edge in — one package at a time —
until it holds again. Then measure.

One line decides whether this works, and it is the same trap as Exercise 3 in a
different disguise. When you remove a package from the left and that class's
count falls to **zero**, you must **delete the key**. A key sitting at zero
still counts toward `len(counts)`, so the promise never comes back true, the
left edge keeps marching, and it walks straight off the end of the conveyor.

**The contract.** Ties on length go to the **largest** start — the depot
prefers to clear the newest end of the belt first. If the conveyor is empty, or
`k` is `0`, return `(-1, 0)`. That is a deliberately impossible position paired
with a zero count, so a caller can tell it apart from a real answer at a
glance.

## Starter

Create `exercise-05-cold-chain-load.py` and paste this in. Fill in every
`TODO`.

```python
"""exercise-05-cold-chain-load.py — the longest loadable run.

Find the longest contiguous run of packages spanning at most k temperature
classes, and return where it is.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""


def longest_load(classes: list[str], k: int) -> tuple[int, int]:
    """Return the longest run of packages spanning at most k classes.

    Args:
        classes: Temperature class of each package, in conveyor order.
        k: How many compartments the van has, so how many distinct classes a
            single run may contain.

    Returns:
        (start, count) for the longest loadable run. Ties go to the larger
        start. (-1, 0) when the conveyor is empty or the van has no
        compartments.
    """
    # TODO: guard the two "no answer" cases first, and return the contract's
    #       own sentinel rather than inventing one.
    # TODO: a frequency table, a `left` edge at 0, and `best` seeded with the
    #       sentinel so an unset answer is already the right shape.
    # TODO: walk `right` over the conveyor with enumerate, adding to the table.
    # TODO: while the table has more than k keys, drop classes[left]:
    #         decrement, DELETE THE KEY IF IT REACHES ZERO, then advance left.
    # TODO: the promise now holds again, so record — and the tie-break decides
    #       which comparison operator that record uses.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[str], int]] = [
        (["chilled", "frozen", "chilled", "ambient", "ambient", "frozen"], 2),
        (["chilled", "frozen", "chilled", "ambient"], 2),
        (["dry", "dry", "cold", "cold", "cold"], 1),
        (["ambient", "frozen"], 5),
        (["ambient"], 0),
        ([], 3),
    ]
    for conveyor, compartments in cases:
        start, count = longest_load(conveyor, compartments)
        run = conveyor[start : start + count] if start >= 0 else []
        print(f"k={compartments}  {str(conveyor):<62} -> ({start}, {count}) {run}")
    print()

    assert longest_load(["chilled", "frozen", "chilled", "ambient", "ambient", "frozen"], 2) == (3, 3)
    assert longest_load(["chilled", "frozen", "chilled", "ambient"], 2) == (0, 3)
    assert longest_load(["dry", "dry", "cold", "cold", "cold"], 1) == (2, 3)
    assert longest_load(["ambient", "frozen"], 5) == (0, 2)
    assert longest_load(["ambient"], 0) == (-1, 0)
    assert longest_load([], 3) == (-1, 0)

    # The run that comes back is loadable, and no longer run is.
    for conveyor, compartments in cases:
        start, count = longest_load(conveyor, compartments)
        if start < 0:
            continue
        assert len(set(conveyor[start : start + count])) <= compartments
        for i in range(len(conveyor)):
            for j in range(i + 1, len(conveyor) + 1):
                if len(set(conveyor[i:j])) <= compartments:
                    assert j - i <= count

    print("All checks passed.")
```

Two things you need before you start.

**Frequency table.** A dictionary from a thing to how many of it you are
currently holding. `counts.get(package, 0) + 1` is the safe way to add one
without needing the key to exist first. The number of *distinct* things is
`len(counts)`, which is why the key must go when the count hits zero — you are
using the size of the dictionary as your answer to a question about the window.

**Template.** A solution shape you write once, with the varying part as a
parameter, and then reuse. `k` here is the parameter. Hard-coding
`while len(counts) > 2` gives you a correct answer to this exact page and
nothing you can carry anywhere else.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-03-sliding-window/exercises/exercise-05-cold-chain-load.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `longest_load(classes, k)` returns `(start, count)` — a position and a
   length.
2. The limit is on **distinct classes**, not on package count.
3. Ties on length go to the **larger** start.
   `longest_load(["chilled", "frozen", "chilled", "ambient", "ambient", "frozen"], 2)`
   is `(3, 3)`, not `(0, 3)`.
4. An empty conveyor returns `(-1, 0)`. `k == 0` returns `(-1, 0)`.
5. Every count that reaches zero has its key deleted.
6. `k` is used as a parameter. No literal compartment count appears in the loop.
7. The answer is recorded **after** the shrink, not inside it.
8. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(classes) <= 250_000`.** A large depot moves a few hundred
  thousand parcels a day, so the bound is realistic *and* it rejects the brute
  force. "For every start, walk right until the class count exceeds `k`" is
  `O(n^2)` in the worst case — about `6 x 10^10` steps here — and will not
  finish. The window gets the same answer by never throwing away the work it
  has already done.

- **`0 <= k <= 20`, and `k = 0` is legal on purpose.** Vans in this fleet have
  at most twenty compartments, so the frequency table never exceeds `k + 1`
  entries and the space claim is `O(k)`, which given the bound is `O(1)`. The
  interesting half is the zero. `k = 0` is the only input that drives the
  shrink loop until the window is completely empty, which is exactly where an
  unguarded `right - left + 1` reports a length of zero for a window that does
  not exist — and then records it at some arbitrary start. The contract says
  `(-1, 0)`; the guard is what makes your code say it too.

- **Class labels come from a fixed vocabulary of at most 8 strings.** A depot
  handles a handful of temperature regimes, not an open-ended set. One
  consequence is worth testing: when `k >= 8` the promise can never be broken,
  the shrink loop never executes once, and the answer is always the whole
  conveyor. A loop body that has never run is a loop body you have not tested,
  so put that case in deliberately.

- **Maintain the table, do not recompute it.** `len(set(classes[left:right + 1]))`
  is a correct test and a wrong solution: it is `O(n)` per step, so the whole
  function becomes quadratic and the size bound rejects it.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-05-cold-chain-load.py
k=2  ['chilled', 'frozen', 'chilled', 'ambient', 'ambient', 'frozen'] -> (3, 3) ['ambient', 'ambient', 'frozen']
k=2  ['chilled', 'frozen', 'chilled', 'ambient']                    -> (0, 3) ['chilled', 'frozen', 'chilled']
k=1  ['dry', 'dry', 'cold', 'cold', 'cold']                         -> (2, 3) ['cold', 'cold', 'cold']
k=5  ['ambient', 'frozen']                                          -> (0, 2) ['ambient', 'frozen']
k=0  ['ambient']                                                    -> (-1, 0) []
k=3  []                                                             -> (-1, 0) []

All checks passed.
```

The first row is the graded one. Three different runs reach length 3 —
packages 0–2, 2–4 and 3–5 — and nothing reaches 4. The tie-break sends you to
the largest start, so `(3, 3)`. A solution using a strict `>` on the length
comparison stops at the first of the three and returns `(0, 3)`, which is a
loadable run of the right length and the wrong answer.

The second row is the deletion test. When `"ambient"` arrives at index 3 the
window holds three classes and has to shrink twice: dropping `"chilled"` at
index 0 leaves its count at 1, so the key stays and the window is still too
wide; dropping `"frozen"` at index 1 takes its count to zero, the key goes, and
the promise holds again. Skip the deletion and the loop never escapes.

## Steps

1. Create the file, paste the starter, and run it. Every row errors on
   unpacking `None`. Correct starting point.
2. Write the guard. Both cases, one line, returning the contract's sentinel.
3. Seed `best = (-1, 0)`. Seeding it this way means the "nothing found" answer
   is already correct before the loop starts, so there is no special case at
   the end.
4. Write the outer loop and the increment.
   `counts[package] = counts.get(package, 0) + 1`.
5. Write the shrink as a `while len(counts) > k`. Inside it: read the class
   leaving, decrement, delete on zero, advance. All four, in that order.
6. Record **after** the `while`, not inside it. This is the growing shape — the
   window is only worth measuring once the promise holds again.
7. Choose the comparison operator from the tie-break. Read Requirement 3 again
   before you type it.
8. Trace the second case by hand. Four steps, and the interesting one is the
   double shrink at index 3. Write out the table at each step, keys and values.

## The Solution

```python
"""exercise-05-cold-chain-load-solution.py — the longest loadable run.

A depot loads a refrigerated van straight off a conveyor. Each compartment is
set to exactly one temperature class, so a contiguous run of packages is
loadable exactly when it holds at most k distinct classes.

This is the at-most-K-distinct template, and it is the most reusable shape of
the week: a frequency table inside the window, a shrink loop that runs while
the table is too wide, and a record taken once the invariant holds again.
`k` is a parameter, never a hard-coded number.

The self-checks are the starter's, unchanged. When they all pass the file
prints "All checks passed."
"""


def longest_load(classes: list[str], k: int) -> tuple[int, int]:
    """Return the longest run of packages spanning at most k classes.

    Args:
        classes: Temperature class of each package, in conveyor order.
        k: How many compartments the van has, so how many distinct classes a
            single run may contain.

    Returns:
        (start, count) for the longest loadable run. Ties go to the larger
        start. (-1, 0) when the conveyor is empty or the van has no
        compartments.
    """
    if not classes or k == 0:
        return (-1, 0)

    counts: dict[str, int] = {}
    left = 0
    best = (-1, 0)

    for right, package in enumerate(classes):
        counts[package] = counts.get(package, 0) + 1

        while len(counts) > k:
            leaving = classes[left]
            counts[leaving] -= 1
            if counts[leaving] == 0:
                del counts[leaving]
            left += 1

        # The invariant holds again, so this window is a real candidate. The
        # >= is the tie-break: a run of equal length but a later start wins.
        if right - left + 1 >= best[1]:
            best = (left, right - left + 1)

    return best


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[str], int]] = [
        (["chilled", "frozen", "chilled", "ambient", "ambient", "frozen"], 2),
        (["chilled", "frozen", "chilled", "ambient"], 2),
        (["dry", "dry", "cold", "cold", "cold"], 1),
        (["ambient", "frozen"], 5),
        (["ambient"], 0),
        ([], 3),
    ]
    for conveyor, compartments in cases:
        start, count = longest_load(conveyor, compartments)
        run = conveyor[start : start + count] if start >= 0 else []
        print(f"k={compartments}  {str(conveyor):<62} -> ({start}, {count}) {run}")
    print()

    assert longest_load(["chilled", "frozen", "chilled", "ambient", "ambient", "frozen"], 2) == (3, 3)
    assert longest_load(["chilled", "frozen", "chilled", "ambient"], 2) == (0, 3)
    assert longest_load(["dry", "dry", "cold", "cold", "cold"], 1) == (2, 3)
    assert longest_load(["ambient", "frozen"], 5) == (0, 2)
    assert longest_load(["ambient"], 0) == (-1, 0)
    assert longest_load([], 3) == (-1, 0)

    # The run that comes back is loadable, and no longer run is.
    for conveyor, compartments in cases:
        start, count = longest_load(conveyor, compartments)
        if start < 0:
            continue
        assert len(set(conveyor[start : start + count])) <= compartments
        for i in range(len(conveyor)):
            for j in range(i + 1, len(conveyor) + 1):
                if len(set(conveyor[i:j])) <= compartments:
                    assert j - i <= count

    print("All checks passed.")
```

**The guard and the seed are the same decision, made twice.**

```python
if not classes or k == 0:
    return (-1, 0)
...
best = (-1, 0)
```

The guard handles the two inputs that have no answer at all. The seed means
that if the loop somehow records nothing, the value already sitting in `best`
is the correct one. Together they remove every special case from the end of the
function — there is no "if we found nothing" branch, because there cannot be a
state where the answer is unset.

Why guard `k == 0` at all, rather than letting the loop fall out naturally? Try
it. With `k = 0` the shrink condition `len(counts) > 0` is true the moment
anything is added, so `left` marches until it passes `right`, at which point
`right - left + 1` is `0`. Then the record line fires with a length of zero and
a start index that is one past the current package — a position that is not
where anything is. The loop does not crash. It records a phantom window at a
meaningless index. That is a much worse failure than an exception, and it is
why the guard is in the contract rather than left implicit.

**The shrink is four lines and the third is the exercise.**

```python
while len(counts) > k:
    leaving = classes[left]
    counts[leaving] -= 1
    if counts[leaving] == 0:
        del counts[leaving]
    left += 1
```

`len(counts)` is being used as the answer to "how many distinct classes are in
the window". That is only true if the table contains exactly the classes that
are actually present. A key sitting at zero is a class that has left, still
being counted, and the effect is not a slightly wrong answer — it is a shrink
condition that can never clear. The window empties, `left` runs past `right`,
and on the next iteration `classes[left]` raises `IndexError` on a conveyor
that plainly had packages in it.

Read the loop condition once more: `while`, not `if`. A single package arriving
can require several removals, as the second test case shows. The `while` also
happens to be the whole correctness argument — it says "keep going until the
promise is true", which is stronger than "try once".

**`>=`, and that is the graded character.**

```python
if right - left + 1 >= best[1]:
    best = (left, right - left + 1)
```

The contract sends ties to the *larger* start, so a run of equal length that
starts later must displace the incumbent. Because the loop visits windows in
increasing order of `right`, and each recorded window's start is
non-decreasing, `>=` naturally keeps the last of any tied group. Exercise 2
needs the opposite operator for the opposite tie-break, and the two pages
disagree on purpose: read the rule, do not remember the symbol.

**Record after the shrink, because this is the growing shape.** At the moment
the record line runs, the promise holds and the window is the longest one
ending at `right` that could possibly be loadable. Recording *inside* the
shrink would measure windows that still violate the limit — that is the
shrinking shape's structure, and it belongs to Exercise 4. If you find yourself
unsure which shape a problem is, ask what you want: longest means shrink while
broken and record after; shortest means shrink while satisfied and record
inside.

**Why this is linear.** `right` advances exactly `n` times. `left` only moves
forward and never passes `right`, so it advances at most `n` times across the
*whole* function — not per iteration. Every dictionary operation is constant on
average. The `while` inside the `for` does not make this quadratic, and the
reason is that `left` carries forward between outer steps rather than resetting.

**`k` stays a parameter, and that is the point of the page.** The at-most-K
template is one of the highest-yield shapes in interviews precisely because so
many prompts are it in costume: at most two fruit types, at most `k` distinct
characters, at most three product lines. Writing
`while len(counts) > 2` gets you one problem. Writing `while len(counts) > k`
gets you the family.

## Run it

Copy the worked answer on this page into `exercise-05-cold-chain-load.py` and run it:

```bash
python exercise-05-cold-chain-load.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-05-cold-chain-load.py`.

## Common bugs to catch

- **`IndexError: list index out of range` on a conveyor that is plainly not
  empty.**

  ```text
  Traceback (most recent call last):
      leaving = classes[left]
                ~~~~~~~^^^^^^
  IndexError: list index out of range
  ```

  You did not delete keys whose count reached zero. `len(counts)` keeps
  counting classes that are no longer in the window, the shrink condition never
  clears, and `left` walks off the end. This is the single most common failure
  on this drill. Reproduce it on purpose with
  `["chilled", "frozen", "chilled", "ambient"]` and `k = 2` so you recognise
  the shape.

- **`longest_load([...], 2)` returns `(0, 3)` instead of `(3, 3)`.** You used
  `>` on the record. All three tied runs are length 3 and the contract wants
  the last of them. No traceback; a perfectly loadable run, and the wrong one.

- **`longest_load(["ambient"], 0)` returns `(1, 0)` or `(0, 0)`.** You dropped
  the `k == 0` guard. The shrink emptied the window, and the record line wrote
  down a length-zero run at whatever `left` had reached. Nothing raised.

- **`KeyError` on the delete.**

  ```text
  Traceback (most recent call last):
      del counts[leaving]
      ^^^^^^^^^^^^^^^^^^^
  KeyError: 'chilled'
  ```

  You deleted unconditionally instead of only on zero. The second time a class
  leaves the window there is no longer a key to remove.

- **Recording inside the shrink loop.** You get answers that are too short, and
  on some inputs no answer at all, because you are measuring windows that still
  break the promise. That structure belongs to Exercise 4. Ask yourself whether
  you want the longest or the shortest, and let that pick the shape.

- **Hard-coding the compartment count.** `while len(counts) > 2` passes the
  first two tests and fails the rest. Requirement 6 is checkable by reading.

- **Off-by-one on the run length.** `right - left + 1`, not `right - left`.
  Both endpoints are inside the window. Check it against
  `(["ambient", "frozen"], 5)`, which must give a count of 2.

- **Rebuilding distinctness from scratch.**
  `len(set(classes[left:right + 1])) <= k` is a correct condition and a
  quadratic solution. No exception, right answers, wrong shape.

## Under the hood

<details>
<summary>Under the hood — the template's other costumes, and why the deletion discipline is sometimes optional</summary>

**Cost, stated precisely.**

Time is `O(n)`, amortised, by the usual argument: `right` advances `n` times,
`left` advances at most `n` times across the whole run, every dictionary
operation is `O(1)` on average. Best, average and worst are all `O(n)` — there
is no early exit, since a longer run could appear at any point.

Space is `O(k)`: the table holds at most `k + 1` entries, transiently, before
the shrink restores the promise. With `k <= 20` that is `O(1)`. Note the tighter
statement available here — `O(min(k + 1, 8))`, since the vocabulary is bounded
too. Knowing which of two bounds binds on a given input is the sort of
precision that separates a memorised complexity claim from a understood one.

**The same template, four costumes.**

| Prompt | The only change |
| --- | --- |
| Longest run with at most `k` distinct classes | this page |
| Longest run with at most 2 distinct fruit types | `k` is fixed at 2 |
| Longest substring with at most `k` distinct characters | the list is a string |
| Longest run where no class appears more than `m` times | the shrink watches one count, not `len` |

The last row is the one worth dwelling on, because it is the one people get
wrong. It is *not* this template with a different number. The promise there is
about **multiplicity** — how many times one class appears — rather than
**distinctness** — how many different classes appear. The shrink condition
becomes `while counts[package] > m`, and it looks at exactly one count: the
class you just added, because it is the only one whose count went up and
therefore the only one that could have broken anything.

That change has a pleasing consequence. In the multiplicity version you never
call `len(counts)`, so a key sitting at zero is harmless and the deletion
discipline becomes **optional**. Two problems, nearly identical code, and a
rule that is load-bearing in one and irrelevant in the other. The
[mini-project's Problem 2](../mini-project/README.md) is that variant, and
noticing why the deletion stops mattering is the point of it.

**The counting cousin.** Change the last line from a comparison to
`total += right - left + 1` and you stop asking "which is the longest run" and
start asking "how many runs qualify". The justification for that one line is
the whole trick: once the promise holds at `right`, every run that ends at
`right` and starts anywhere from `left` onwards also holds it, because dropping
packages off the left can never *raise* the distinct count. So there are
exactly `right - left + 1` of them and you can add them all at once instead of
listing them. That shape is the [mini-project's Problem 5](../mini-project/README.md),
and [homework Problem 2](../homework/problem-02-courier-zone-count.md)
subtracts two of them from each other to answer an "exactly K" question.

Worth knowing where that stops working: the argument depends on the promise
surviving a shrink. For "at most `k` distinct" it does. For "at least `k`
distinct" it does not — shrinking can break that one — so the counting trick
does not transfer, and a prompt phrased with "at least" should make you stop
and check rather than reach.

</details>

## Acceptance checklist

- [ ] `python exercise-05-cold-chain-load.py` prints six rows then `All checks passed.`
- [ ] The output matches the Expected output block character for character.
- [ ] `longest_load([...], 2)` returns `(3, 3)` on the first case, and you can say why.
- [ ] `longest_load(["ambient"], 0)` and `longest_load([], 3)` both return `(-1, 0)`.
- [ ] Every count that reaches zero has its key deleted.
- [ ] The record happens after the shrink loop, not inside it.
- [ ] No literal compartment count appears anywhere in your loop.
- [ ] You can say in one sentence why `k == 0` needs a guard rather than falling out naturally.
- [ ] The function has type hints and a docstring.
- [ ] Committed to Git with a message like `Add Week 3 exercise 5: the cold-chain load`.

## Stretch

- **Swap distinctness for multiplicity.** A van whose compartments have a shelf
  limit: no single class may appear more than `m` times in one run.

  ```python
  def longest_load_within_shelf(classes: list[str], m: int) -> tuple[int, int]:
      """Return (start, count) for the longest run where no class appears more than m times."""
      if not classes or m == 0:
          return (-1, 0)
      counts: dict[str, int] = {}
      left, best = 0, (-1, 0)
      for right, package in enumerate(classes):
          counts[package] = counts.get(package, 0) + 1
          while counts[package] > m:
              counts[classes[left]] -= 1
              left += 1
          if right - left + 1 >= best[1]:
              best = (left, right - left + 1)
      return best
  ```

  ```text
  (["chilled", "frozen", "chilled", "ambient", "ambient", "frozen"], 2) -> (0, 6)
  (["dry", "dry", "cold", "cold", "cold"], 1)                          -> (1, 2)
  ```

  Count how many lines actually changed. Two. Then note in your portfolio that
  the deletion disappeared and work out why it is safe to drop it — the answer
  is in *Under the hood*, but guess first.

- **Count instead of measuring.** Replace the comparison with
  `total += right - left + 1` and return the total. That is every loadable run,
  not the longest one.

  ```text
  (["chilled", "frozen", "chilled", "ambient", "ambient", "frozen"], 2) -> 15
  ```

  Verify it by brute force on a six-package conveyor before you believe it. The
  formula is doing a lot of work in very little space.

- **Return the classes as well.** `set(classes[start:start + count])` at the
  end, once, is `O(count)` once rather than per step. Be ready to say why that
  is a different thing from the `set` call the constraints forbid.
That is all five drills. Take the [quiz](../quiz.md), then work the
[challenges](../challenges/README.md), the [homework](../homework/README.md)
and the [mini-project](../mini-project/README.md).
