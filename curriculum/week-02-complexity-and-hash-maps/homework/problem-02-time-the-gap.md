# Homework Problem 2 — Time the Gap

> **Topic:** measuring a complexity class instead of believing in it — operation counts to stdout, wall-clock seconds to stderr
> **Lecture:** [01 — Mental Models for Big-O](../lecture-notes/01-mental-models-for-big-o.md)
> **Difficulty:** Easy to write, hard to report honestly
> **Target time:** 45 minutes
> **Why this one:** this is the most pedagogically valuable forty-five minutes of the week. You have spent five exercises being told that `O(n)` beats `O(n^2)`. Here you watch it happen on your own machine, in numbers you produced. Theory becomes muscle memory the moment you measure it yourself — and the honest reporting of the *inconvenient* number at small `n` is worth more than the tidy one.

## The Brief

Somebody tells you a car is faster than a bicycle. You believe them. Now
somebody tells you a car is faster than a bicycle *by a factor that grows with
the distance*, and suddenly you want to see the stopwatch.

That second claim is what big-O is. `O(n^2)` is not "slower". It is "slower by a
factor that grows with the input", and the whole point of the notation is that
the factor keeps growing. A hundred items and the quadratic version might win.
Ten thousand and it has lost by three orders of magnitude. You have been told
this all week. Now measure it.

You already have both implementations from
[Exercise 1](../exercises/exercise-01-refund-pair.md): the nested scan that
compares every pair of charges, and the one-pass hash map. This problem is about
running them side by side and writing down what happens.

Two design decisions make the measurement mean something.

**Make the input adversarial for the nested loop.** If a pair matches early,
both versions return early and you have timed luck rather than work. Generate
charges that are all even with an odd refund total: no two even numbers sum to
an odd one, so no pair can ever complete and both versions run to the end.

**Split what is reproducible from what is not.** Operation counts are identical
on every machine on earth — they are a property of the algorithm. Wall-clock
seconds are a property of your laptop, its thermal state, and what else it was
doing. So the counts go to **stdout** and the seconds go to **stderr**. That
split is not a stylistic flourish: it is why
`python problem-02-time-the-gap-solution.py > counts.txt` saves the table and
leaves the timings on your screen, and it is the same discipline that keeps this
course's expected-output blocks meaningful.

## Starter

Create `problem-02-time-the-gap.py` in your practice repo and paste this in.
Fill in every `TODO`.

```python
"""problem-02-time-the-gap.py — watching a complexity class change.

Fill in every TODO, then run the file. Counts go to stdout, timings to
stderr. Redirect stdout to a file and you will see the split for yourself.
"""

import random
import sys
import time


def unsolvable_charges(n: int, seed: int = 20260221) -> tuple[list[int], int]:
    """Return n charges that no pair can ever complete, plus that total.

    Every charge is even and the refund total is odd, so no two charges can
    sum to it. Neither implementation can exit early, so the comparison
    measures the full scan instead of measuring luck.

    Args:
        n: How many charges to generate.
        seed: Fixed so every run of this file produces the same input.

    Returns:
        (charges, refund_total).
    """
    rng = random.Random(seed)
    charges = [2 * rng.randint(-25_000, 25_000) for _ in range(n)]
    return charges, 1


def find_refund_pair_nested(
    charges: list[int], refund_total: int
) -> tuple[tuple[int, int] | None, int]:
    """The nested scan. O(n^2) time, O(1) space.

    Args:
        charges: Charge amounts in cents.
        refund_total: The disputed refund total.

    Returns:
        (pair or None, number of charge-to-charge comparisons performed).
    """
    # TODO: two loops, and count every comparison you actually perform.
    ...


def find_refund_pair_hashed(
    charges: list[int], refund_total: int
) -> tuple[tuple[int, int] | None, int]:
    """The one-pass hash map. O(n) time, O(n) space.

    Args:
        charges: Charge amounts in cents.
        refund_total: The disputed refund total.

    Returns:
        (pair or None, number of map lookups performed).
    """
    # TODO: Exercise 1's solution, with a counter added.
    ...


def median_seconds(runner, charges: list[int], refund_total: int, runs: int = 3) -> float:
    """Return the median wall-clock time of `runs` calls, in seconds.

    The median, not the first run: the first run pays for warm-up and
    allocation that the comparison does not care about.
    """
    # TODO: time.perf_counter() around each call, then take the middle value.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    sizes = [250, 1_000, 4_000]

    print("n            nested comparisons   hashed lookups     ratio")
    previous: tuple[int, int] | None = None
    for n in sizes:
        charges, refund_total = unsolvable_charges(n)

        nested_pair, nested_ops = find_refund_pair_nested(charges, refund_total)
        hashed_pair, hashed_ops = find_refund_pair_hashed(charges, refund_total)

        assert nested_pair is None, "the generator promised no pair completes"
        assert hashed_pair is None, "both implementations must agree"
        assert nested_ops == n * (n - 1) // 2
        assert hashed_ops == n

        print(f"{n:8d} {nested_ops:20d} {hashed_ops:16d} {nested_ops / hashed_ops:9.1f}")

        print(
            f"n={n}: nested {median_seconds(find_refund_pair_nested, charges, refund_total):.4f}s, "
            f"hashed {median_seconds(find_refund_pair_hashed, charges, refund_total):.4f}s",
            file=sys.stderr,
        )

        if previous is not None:
            grew_by = n / previous[0]
            nested_grew = nested_ops / previous[1]
            print(
                f"         n x{grew_by:.0f}  ->  nested work x{nested_grew:.1f}, "
                f"hashed work x{grew_by:.0f}"
            )
        previous = (n, nested_ops)

    print()
    print("Quadruple n and the linear column quadruples; the quadratic one grows")
    print("about sixteenfold. That is the whole difference between O(n) and O(n^2),")
    print("and it is a fact about the algorithms, not about this machine.")
    print("All checks passed.")
```

Three things before you start.

**`time.perf_counter()`.** The clock to use for measuring elapsed time. It is
monotonic — it never jumps backwards when the system clock is adjusted — and it
has the highest resolution available. Never use `time.time()` for this.

**Median, not first.** The first run of anything pays for imports, allocation
and a cold cache. Run each size three times and take the middle value. That is
not cherry-picking; it is discarding a cost you are not trying to measure.

**stderr.** `print(..., file=sys.stderr)` writes to the error stream, which
appears on your terminal but is not part of stdout. Nothing about your program
crashed — stderr is simply the channel for everything that is not the output.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-02-complexity-and-hash-maps/homework/problem-02-time-the-gap.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. Both implementations return the same answer on every input, and both return
   an operation count alongside it.
2. The nested version's count is exactly `n(n-1)/2` on an unsolvable input —
   every pair, once.
3. The hashed version's count is exactly `n` — one lookup per charge.
4. The generated input is adversarial: no pair can complete, so neither version
   exits early.
5. The generator takes a fixed seed, so the table is identical on every run and
   every machine.
6. Operation counts and growth ratios go to **stdout**; wall-clock seconds go to
   **stderr**.
7. Each timing is a median of at least three runs.
8. Every function keeps its type hints and its docstring.
9. A write-up at `frame-writeups/c2-week-02/measurement-01.md` carries your own
   machine's timing table and three observations. See the checklist.

## Constraints

- **Sizes are 250, 1,000 and 4,000 — quadrupling each time.** Quadrupling is
  chosen over the more usual ten-times steps for a practical reason: the nested
  version at `n = 40_000` would be eight hundred million comparisons and
  minutes of waiting, which nobody will sit through and which would push this
  file past any sensible test timeout. Quadrupling gives you three points, a
  clean prediction (linear grows 4×, quadratic grows 16×) and a run that
  finishes in seconds. Extend the list yourself on your own machine if you want
  to feel where it becomes painful — that is one of the three observations you
  owe the write-up.

- **The refund total is odd and every charge is even.** No two even numbers sum
  to an odd number, so the answer is provably `None` and neither version can
  return early. This is the difference between measuring an algorithm and
  measuring where the answer happened to sit. State it in your write-up; a
  benchmark whose fairness you cannot argue for is not evidence.

- **The seed is fixed.** A benchmark that generates different data on every run
  produces a table you cannot compare against yesterday's. Fix the seed, and
  then any difference you see is a difference in the machine or the code, which
  is what you are trying to observe.

- **Timings never enter stdout.** Wall-clock numbers vary by machine, by thermal
  state, and by what else is running. Anything reproducible goes to stdout;
  anything machine-specific goes to stderr. Break that rule and this page's own
  expected-output block could never be checked, which is the concrete cost of
  mixing the two.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-02-time-the-gap-solution.py
n            nested comparisons   hashed lookups     ratio
     250                31125              250     124.5
    1000               499500             1000     499.5
         n x4  ->  nested work x16.0, hashed work x4
    4000              7998000             4000    1999.5
         n x4  ->  nested work x16.0, hashed work x4

Quadruple n and the linear column quadruples; the quadratic one grows
about sixteenfold. That is the whole difference between O(n) and O(n^2),
and it is a fact about the algorithms, not about this machine.
All checks passed.
```

That is stdout only. The same run also wrote three lines to stderr, which looked
like this on the machine that captured it and will look different on yours:

```text
n=250: nested 0.0014s, hashed 0.0001s
n=1000: nested 0.0268s, hashed 0.0001s
n=4000: nested 0.4137s, hashed 0.0006s
```

Read the ratio column. At 250 charges the nested version does 124 times the
work; at 4,000 it does 2,000 times the work. The ratio is `(n-1)/2`, so it grows
without limit — that is precisely what "`O(n^2)` versus `O(n)`" means, and it is
why the phrase "a bit slower" is the wrong way to describe it.

Then read the growth lines. Quadruple `n`, and the linear column quadruples
while the quadratic column grows about sixteenfold — `4^2`. Those two numbers
*are* the exponents, measured rather than asserted.

## Steps

1. Create the file, paste the starter, and run it. Every assert fails.
2. Fill in `find_refund_pair_nested`. Count inside the inner loop, on the line
   that actually compares. Run and check the count against `n(n-1)/2`; the
   assert does it for you, and if it fails you are counting in the wrong place.
3. Fill in `find_refund_pair_hashed` — Exercise 1's solution with a counter.
   Count once per charge, at the top of the loop.
4. Fill in `median_seconds`. Run. The table should appear on stdout and three
   timing lines on stderr.
5. Prove the split to yourself: run
   `python problem-02-time-the-gap.py > counts.txt`. The table lands in the
   file; the timings stay on your screen. That is the whole lesson of the
   stderr convention, in one command.
6. Now extend `sizes` with `16_000` and run it once. It takes about ten seconds
   for a hundred and twenty-eight million comparisons. Then try `64_000` if you
   have the patience — that is where "painful" lives, and finding it yourself is
   observation one. Put `sizes` back afterwards so the file still matches the
   expected output.
7. Write up `frame-writeups/c2-week-02/measurement-01.md` with your own numbers
   and the three observations.

## The Solution

```python
"""problem-02-time-the-gap-solution.py — watching a complexity class change.

Two solutions to Exercise 1's refund-pair problem, side by side on the same
input: the nested scan that compares every pair, and the one-pass hash map.
Both are instrumented, so they report how many charge-to-charge comparisons
each one actually performed.

The counts go to stdout, because they are the same on every machine and are
the thing the argument rests on. The wall-clock seconds go to stderr, because
they are different on every machine and would make this file's output
unreproducible. That split is worth keeping: it is why
`python problem-02-time-the-gap-solution.py > counts.txt` saves the table and
leaves the timings on your screen.

Time: the nested scan is O(n^2), the hash map is O(n).
Space: the nested scan is O(1), the hash map is O(n).
"""

import random
import sys
import time


def unsolvable_charges(n: int, seed: int = 20260221) -> tuple[list[int], int]:
    """Return n charges that no pair can ever complete, plus that total.

    Every charge is even and the refund total is odd, so no two charges can
    sum to it. Neither implementation can exit early, so the comparison
    measures the full scan instead of measuring luck.

    Args:
        n: How many charges to generate.
        seed: Fixed so every run of this file produces the same input.

    Returns:
        (charges, refund_total).
    """
    rng = random.Random(seed)
    charges = [2 * rng.randint(-25_000, 25_000) for _ in range(n)]
    return charges, 1


def find_refund_pair_nested(
    charges: list[int], refund_total: int
) -> tuple[tuple[int, int] | None, int]:
    """The nested scan. O(n^2) time, O(1) space.

    Args:
        charges: Charge amounts in cents.
        refund_total: The disputed refund total.

    Returns:
        (pair or None, number of charge-to-charge comparisons performed).
    """
    comparisons = 0
    for later in range(len(charges)):
        for earlier in range(later):
            comparisons += 1
            if charges[earlier] + charges[later] == refund_total:
                return ((earlier, later), comparisons)
    return (None, comparisons)


def find_refund_pair_hashed(
    charges: list[int], refund_total: int
) -> tuple[tuple[int, int] | None, int]:
    """The one-pass hash map. O(n) time, O(n) space.

    Args:
        charges: Charge amounts in cents.
        refund_total: The disputed refund total.

    Returns:
        (pair or None, number of map lookups performed).
    """
    lookups = 0
    earliest_at: dict[int, int] = {}
    for position, amount in enumerate(charges):
        lookups += 1
        complement = refund_total - amount
        if complement in earliest_at:
            return ((earliest_at[complement], position), lookups)
        if amount not in earliest_at:
            earliest_at[amount] = position
    return (None, lookups)


def median_seconds(runner, charges: list[int], refund_total: int, runs: int = 3) -> float:
    """Return the median wall-clock time of `runs` calls, in seconds.

    The median, not the first run: the first run pays for warm-up and
    allocation that the comparison does not care about.
    """
    timings = []
    for _ in range(runs):
        started = time.perf_counter()
        runner(charges, refund_total)
        timings.append(time.perf_counter() - started)
    return sorted(timings)[len(timings) // 2]


# ---- Self-check ----
if __name__ == "__main__":
    sizes = [250, 1_000, 4_000]

    print("n            nested comparisons   hashed lookups     ratio")
    previous: tuple[int, int] | None = None
    for n in sizes:
        charges, refund_total = unsolvable_charges(n)

        nested_pair, nested_ops = find_refund_pair_nested(charges, refund_total)
        hashed_pair, hashed_ops = find_refund_pair_hashed(charges, refund_total)

        assert nested_pair is None, "the generator promised no pair completes"
        assert hashed_pair is None, "both implementations must agree"
        assert nested_ops == n * (n - 1) // 2
        assert hashed_ops == n

        print(f"{n:8d} {nested_ops:20d} {hashed_ops:16d} {nested_ops / hashed_ops:9.1f}")

        print(
            f"n={n}: nested {median_seconds(find_refund_pair_nested, charges, refund_total):.4f}s, "
            f"hashed {median_seconds(find_refund_pair_hashed, charges, refund_total):.4f}s",
            file=sys.stderr,
        )

        if previous is not None:
            grew_by = n / previous[0]
            nested_grew = nested_ops / previous[1]
            print(
                f"         n x{grew_by:.0f}  ->  nested work x{nested_grew:.1f}, "
                f"hashed work x{grew_by:.0f}"
            )
        previous = (n, nested_ops)

    print()
    print("Quadruple n and the linear column quadruples; the quadratic one grows")
    print("about sixteenfold. That is the whole difference between O(n) and O(n^2),")
    print("and it is a fact about the algorithms, not about this machine.")
    print("All checks passed.")
```

**The generator is the part that makes the benchmark fair, and it is worth the
most attention.**

```python
charges = [2 * rng.randint(-25_000, 25_000) for _ in range(n)]
return charges, 1
```

Every charge is even; the total is 1, which is odd. Two even numbers always sum
to an even number, so no pair can complete, so neither implementation returns
early. Without that guarantee you are not timing two algorithms — you are timing
where the answer happened to sit in a random list, and the nested version can
look excellent purely because a matching pair appeared near the front.

The fixed seed does the other half of the job. The same three inputs are
generated on every run and every machine, so the table is reproducible and any
change you see is a change you made.

**Counting operations is better evidence than timing them, and the file does
both for a reason.** The counts are exact, identical everywhere, and provably
`n(n-1)/2` against `n` — the asserts check that, which turns the count into a
test rather than a claim. The timings are what convince your gut. Neither alone
is enough: counts without timings never quite feel real, and timings without
counts are impossible to argue about, because somebody can always say "your
machine was busy".

**Why the counts are exactly those formulas.** The nested version compares every
unordered pair once: for each later position it looks at every earlier one, so
`0 + 1 + 2 + ... + (n-1) = n(n-1)/2`. The hashed version does one lookup per
charge, so `n`. The ratio is therefore `(n-1)/2` — a number that grows with the
input and never stops. Saying "the quadratic one is `(n-1)/2` times worse" is a
much sharper sentence than "the quadratic one is worse", and it comes straight
out of the counting.

**stdout versus stderr, and why it is a discipline rather than a preference.**
The counts belong to the algorithms and the seconds belong to your laptop. Mix
them into one stream and the output can never be compared against a recorded
expectation, because a third of it changes on every run. Split them and
`> counts.txt` gives you a file worth committing next to a file you would never
commit. This is the same convention that lets a program ask questions
interactively while still being usable in a pipeline: prompts to stderr, answers
to stdout.

**The median, and what it is protecting against.** The first call to either
function pays for warm-up: bytecode gets specialised, the allocator warms, the
list lands in cache. None of that is what you are measuring. Three runs and the
middle value discards both the cold first run and any single run that got
unlucky with a background process. It is the cheapest possible defence against
the two most common benchmarking mistakes.

**Say the inconvenient number out loud.** At `n = 250` the nested version does
124 times the *work* and is nowhere near 124 times slower — on many machines the
gap at small `n` is far narrower than the count suggests, and on a small enough
input the nested version can genuinely win, because a dict allocation is not
free and a tight loop over a list is very fast. Report that if you measure it. A
candidate who volunteers the number that complicates their story is worth more
than one who reports only the tidy one, and an interviewer can tell the
difference immediately.

**What this does not measure, and you should say so.** Memory. The nested
version is `O(1)` auxiliary space and the hashed version is `O(n)` — at four
thousand charges that is a dict with four thousand entries, tens of kilobytes,
irrelevant. At four hundred million charges it would be the whole story. Time is
one axis and this benchmark measures one axis.

**The cost, said properly.** *The nested version*: `O(n^2)` time, `O(1)` space,
no early exit on this input by construction. *The hashed version*: `O(n)` time,
`O(n)` space, `O(1)` average per lookup, one pass. *The measurement harness
itself*: dominated by the nested version, so roughly `O(n^2)` overall, which is
why the sizes stop at 4,000. *Improvement*: `O(n)` is the floor for the problem,
since every charge must be read.

## Download and run

Download
[problem-02-time-the-gap-solution.py](./problem-02-time-the-gap-solution.py)
and run it:

```bash
python problem-02-time-the-gap-solution.py
```

Then run it again with stdout redirected, and watch the two streams separate:

```bash
python problem-02-time-the-gap-solution.py > counts.txt
```

The table goes into `counts.txt`; the three timing lines stay on your terminal.
That is the whole point of the convention, demonstrated in one command.

It is the same program you are writing, under a name that will not collide with
your own `problem-02-time-the-gap.py`.

## Common bugs to catch

- **`AssertionError` on the nested count.** You counted in the wrong place:

  ```text
  Traceback (most recent call last):
      assert nested_ops == n * (n - 1) // 2
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  Incrementing in the outer loop counts `n`, not `n(n-1)/2`. Incrementing after
  the `if` counts only the matches. The counter goes on the line that performs
  the comparison, inside the inner loop, before the test.

- **`AssertionError: the generator promised no pair completes`.** You changed
  the generator — most likely to `rng.randint(...)` without the `2 *`, or set
  the total to an even number. Two even charges cannot sum to an odd total, and
  that is the only reason this benchmark is fair. Put it back.

- **`TypeError: cannot unpack non-sequence NoneType`.** One of the two functions
  returns only the pair and not the count:

  ```text
  Traceback (most recent call last):
      nested_pair, nested_ops = find_refund_pair_nested(charges, refund_total)
      ^^^^^^^^^^^^^^^^^^^^^^^
  TypeError: cannot unpack non-sequence NoneType
  ```

  Both return a two-tuple on every path, including the "no pair found" path at
  the end.

- **The timings appear in `counts.txt`.** You forgot `file=sys.stderr`. The file
  now contains numbers that change on every run, which makes it worthless as a
  record. This is the mistake the whole convention exists to prevent, and it is
  worth making once on purpose so you recognise it.

- **`TypeError: 'float' object cannot be interpreted as an integer`.** You
  indexed the sorted timings with `runs / 2` instead of `runs // 2`. Integer
  division for indices, always.

- **The run takes minutes.** You extended `sizes` and left it extended. At
  `n = 64_000` the nested version is about two billion comparisons. That is the
  experiment from step 6, and it is not the shipped configuration.

- **Reporting the first run instead of the median.** Your numbers will be
  noticeably worse and noticeably less stable, and you will draw conclusions
  from a warm-up cost. Sort, then take the middle.

- **Concluding that the hash map is always better.** At `n = 250` the count
  ratio is 124 and the *time* ratio on many machines is far smaller, because
  constant factors dominate. The honest conclusion is "the hash map wins by a
  factor that grows without limit, and below some small `n` the constant factors
  make them comparable" — with your own crossover point named, if you measured
  one.

## Under the hood

<details>
<summary>Under the hood — why counting operations beats timing them, and what a benchmark cannot tell you</summary>

**Wall-clock time measures your machine. Operation counts measure your
algorithm.**

A timing run is affected by CPU frequency scaling, thermal throttling, other
processes, cache state, memory pressure, the garbage collector, and — on a
laptop — whether it is plugged in. None of those are properties of your code. An
operation count has none of that noise: it is exact, it is identical everywhere,
and you can assert on it in a test, which is exactly what this file does.

The professional habit is to do both and to know which one you are arguing
from. Counts prove the complexity class. Timings prove that the class matters at
the size you actually have. Neither replaces the other.

**Why `perf_counter` and not `time.time`.** `time.time()` returns the wall
clock, which can be adjusted by NTP mid-measurement and can therefore go
*backwards*, producing a negative duration. `perf_counter()` is monotonic and
has the finest resolution the platform offers. There is also
`process_time()`, which excludes time the process spent asleep — useful when you
are measuring CPU work on a busy machine, and not needed here.

**`timeit` exists and is better for micro-benchmarks.** For code that runs in
microseconds, the loop-and-take-the-median approach here is too coarse:
`timeit` runs the snippet many times, disables the garbage collector, and
reports the best of several repeats. This problem uses `perf_counter` because at
`n = 4000` a single run is already hundreds of milliseconds, and because writing
the harness by hand teaches something that calling `timeit` does not. Reach for
`timeit` when the thing you are timing is small.

**What the constant factor is made of, concretely.** The nested version's inner
step is an addition and a comparison on two integers already in a list — that is
about as cheap as Python gets. The hashed version's step computes a hash, probes
a table, and possibly writes an entry, which is several times more expensive per
operation. So the hash map does `n` expensive things and the nested loop does
`n(n-1)/2` cheap ones. At `n = 250` those can come out close. The crossover
point is real, it is machine-specific, and finding it is a genuinely useful
thing to be able to do.

That is what "big-O ignores constant factors" means in practice: it tells you
what happens as `n` grows and deliberately says nothing about which is faster at
`n = 10`. Both halves are worth knowing, and the second one is where a lot of
"we optimised it and it got slower" stories come from.

**What a benchmark cannot tell you.** It cannot tell you about memory, which is
the axis where the nested version wins here. It cannot tell you about the input
distribution you will actually see — this one is adversarial by construction,
and real charge histories are not. It cannot tell you about cache behaviour on
data much larger than this. And it cannot tell you whether the code is
*correct*, which is why the asserts in this file check the answers as well as
the counts.

**The n-versus-runtime table, which you should be able to say from memory.**
Assume a machine doing roughly `10^8` simple operations per second — pessimistic
for a compiled language, about right for Python on this kind of loop:

| n | `O(n)` | `O(n log n)` | `O(n^2)` |
|---:|---:|---:|---:|
| 1,000 | instant | instant | 10^6 — instant |
| 100,000 | instant | instant | 10^10 — minutes |
| 1,000,000 | instant | about a second | 10^12 — hours |

That table is why a constraint of 200,000 in an interview problem is a
*message*. The interviewer is telling you the quadratic solution will not
finish. Reading bounds that way, out loud, in the *Research constraints* step,
is a habit this week has been building since Exercise 1.

</details>

## Acceptance checklist

- [ ] `python problem-02-time-the-gap.py` prints the table then `All checks passed.`
- [ ] The stdout matches the expected output character for character.
- [ ] Three timing lines appeared on stderr and **not** in the table.
- [ ] `python problem-02-time-the-gap.py > counts.txt` puts the table in the
      file and leaves the timings on screen.
- [ ] The nested count is exactly `n(n-1)/2` and the hashed count exactly `n`.
- [ ] The generator is seeded and provably unsolvable, and you can say why.
- [ ] Each timing is a median of at least three runs.
- [ ] A write-up exists at `frame-writeups/c2-week-02/measurement-01.md`
      containing both implementations, the generator, and **your own machine's**
      timing table — not the numbers from this page.
- [ ] The write-up answers all three observations:
      at which `n` did the nested version become *painful*; going from `n` to
      `4n`, by what factor did each column grow, and does that match the theory;
      at what input size would you refuse to ship the `O(n^2)` version, and what
      would you tell a reviewer who said "but it is simpler"?
- [ ] The write-up has one honest note at the bottom about small `n`, including
      the case where the nested version was *faster*, if you measured it.
- [ ] Committed to Git with a message like `Add Week 2 homework 2: timing measurement`.

## Stretch

- **Find the crossover point — the `n` below which the nested version wins.**

  ```python
  crossover = None
  for n in (2, 4, 8, 16, 32, 64, 128, 256):
      charges, total = unsolvable_charges(n)
      nested = median_seconds(find_refund_pair_nested, charges, total, runs=9)
      hashed = median_seconds(find_refund_pair_hashed, charges, total, runs=9)
      if nested >= hashed and crossover is None:
          crossover = n
  print("nested stops winning somewhere at or below n =", crossover)
  ```

  Your number will differ from anybody else's, and that is the finding. Report
  it with your machine and your Python version, because without those it means
  nothing. If you get no crossover at all, say that too — some machines and some
  Python builds never show one.

- **Count operations at sizes you could never time.** Counts are arithmetic, so
  nothing has to run.

  ```python
  for n in (10**2, 10**4, 10**6, 10**8):
      nested = n * (n - 1) // 2
      print(f"n={n:>11,}  nested {nested:>25,}  hashed {n:>11,}")
  ```

  ```text
  n=        100  nested                     4,950  hashed         100
  n=     10,000  nested                49,995,000  hashed      10,000
  n=  1,000,000  nested       499,999,500,000,000  hashed   1,000,000
  n=100,000,000  nested 4,999,999,950,000,000,000  hashed 100,000,000
  ```

  Five quintillion comparisons. At a hundred million operations a second that is
  about fifteen hundred years. This is the table to have in your head when a
  problem says `1 <= n <= 10^8` — the constraint has already told you the
  quadratic solution is not a candidate, and no amount of tuning changes an
  exponent.

- **Add the memory axis, which this benchmark ignores.**

  ```python
  import tracemalloc

  def peak_kilobytes(runner, charges: list[int], refund_total: int) -> float:
      """Return the peak memory the runner allocated, in kilobytes."""
      tracemalloc.start()
      runner(charges, refund_total)
      _, peak = tracemalloc.get_traced_memory()
      tracemalloc.stop()
      return peak / 1024

  charges, total = unsolvable_charges(4_000)
  print(f"nested peak {peak_kilobytes(find_refund_pair_nested, charges, total):8.1f} KB")
  print(f"hashed peak {peak_kilobytes(find_refund_pair_hashed, charges, total):8.1f} KB")
  ```

  The nested version allocates essentially nothing; the hashed version allocates
  a dict of four thousand entries. That is the tradeoff the whole week has been
  claiming, on the axis this problem otherwise ignores — and it is the sentence
  that turns "the hash map is better" into "the hash map trades `O(n)` memory
  for a whole complexity class, and here is what that memory costs".
Next: [Homework Problem 3 — Re-narrate the Market Awning](./problem-03-renarrate-market-awning.md).
