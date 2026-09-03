# Exercise 1 — Reverse the Siding

> **Topic:** two pointers walking toward each other, swapping as they go, and refusing an order that does not make sense
> **Lecture:** [03 — Arrays and Two Pointers](../lecture-notes/03-arrays-and-two-pointers.md)
> **Difficulty:** Easy
> **Target time:** 45 minutes, including a full FRAME narration out loud
> **Why this one:** it is the simplest converging-pointer problem there is — two indices, one swap, one loop. Everything else this week is this shape with something extra bolted on. It also carries the lesson that Python's helpfulness is a hazard: negative indexes and forgiving slices will happily accept an order the contract tells you to refuse, and they will do it silently.

## The Brief

A rail yard has a **siding** — a single dead-end track with a row of freight
cars parked on it. Each car has a **reporting mark** painted on its side, a
short code like `HOP` or `TNK`. The cars are listed nose-to-tail, so position
`0` is the car nearest the buffer stop at the dead end.

The yard controller sends the crew a **flip order**: two positions, `start`
and `end`. The crew reverses the run of cars from `start` through `end`,
**including both of those positions**, and leaves every car outside the run
exactly where it was.

Here is the picture. A siding is a physical track with a wall at one end. The
crew cannot build a second train somewhere else and copy it back — there is
nowhere to put it. All they can do is take two cars and **trade their
places**. So they take the car at each end of the run, swap those two, step
one position inward on each side, and swap again, until the two positions
meet in the middle.

The controller's console is old, and sometimes it sends nonsense: a `start`
that comes after the `end`, an `end` past the last car, a negative position.
**A nonsense order is refused whole.** The crew does not clamp it to
something reasonable, does not apply the part of it that makes sense, and
does not touch the siding at all.

Return the **number of swaps** the crew performed. Not the list, not `None` —
a count. That number is what the yard logs, because it is how the shift gets
billed, and a refused order costs nothing.

```python
def reverse_siding(cars: list[str], start: int, end: int) -> int:
    """Reverse cars[start..end] inclusive, in place, by swapping."""
```

Two words before you start.

**In place.** A function works *in place* when it rearranges the thing you
handed it instead of building you a new one. `cars` goes in one order and
comes back reversed — the same list object, changed. That is the opposite of
most functions you have written, and it is the whole point here.

**Auxiliary space.** This is the memory your function uses *on top of* the
input it was given. Two counters is `O(1)` auxiliary space: it is the same
two counters whether the siding holds five cars or five hundred thousand.
Copying the run into a new list is `O(k)` auxiliary space, because the copy
grows as the run grows.

## Starter

Save this as `exercise-01-reverse-the-siding.py` and fill in the `TODO`s. It
runs as pasted — you will get an `AssertionError`, which is the correct place
to start from, because it proves the self-check is real.

```python
"""exercise-01-reverse-the-siding.py — the yard controller's flip order.

Reverse a run of freight cars on a siding, in place, by swapping pairs.
Refuse a nonsense order whole. Report how many swaps were performed.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""


def reverse_siding(cars: list[str], start: int, end: int) -> int:
    """Reverse cars[start..end] inclusive, in place, by swapping.

    Args:
        cars: The siding, nose-to-tail. Reversed in place when the order is
            valid, and left completely untouched when it is not.
        start: First position of the run to flip.
        end: Last position of the run to flip, inclusive.

    Returns:
        The number of swaps performed. Zero when the order is refused.
    """
    # TODO: refuse the order — return 0 — when start is negative, when end is
    #       not a real position in cars, or when start is not before end
    # TODO: put one pointer on start and one on end, then swap, step both
    #       inward, and count, until the pointers meet or cross
    ...


# ---- Self-check ----
if __name__ == "__main__":
    siding = ["HOP", "TNK", "BOX", "GON", "FLT"]
    print(reverse_siding(siding, 1, 3), siding)

    assert reverse_siding(["HOP", "TNK", "BOX", "GON", "FLT"], 0, 4) == 2
    assert reverse_siding(["HOP", "TNK", "BOX"], 1, 7) == 0
    assert reverse_siding(["HOP", "TNK", "BOX"], -1, 2) == 0
    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-01-the-frame-method-and-thinking-aloud/exercises/exercise-01-reverse-the-siding.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `reverse_siding` reverses `cars[start]` through `cars[end]` **inclusive**,
   in place, and leaves every car outside that run where it was.
2. It returns the number of swaps performed, as an `int`.
3. An order is refused — return `0`, change nothing — when `start < 0`, when
   `end >= len(cars)`, or when `start >= end`.
4. A refused order leaves `cars` exactly as it arrived. Not clamped, not
   partly applied.
5. The function uses `O(1)` auxiliary space. No slice copy of the run, no
   second list, no `reversed()` into a temporary.
6. The function keeps its type hints and its docstring.

## Constraints

- **`0 <= len(cars) <= 100_000`.** One hundred thousand cars is longer than
  any siding that has ever existed, and that is deliberate. The yard
  controller is an embedded box with a few megabytes of memory, so a solution
  that copies the run — `cars[start:end + 1][::-1]` and friends — is spending
  memory it does not have. The bound is what makes `O(1)` auxiliary space a
  requirement rather than a preference.

- **Each reporting mark is 2 to 4 uppercase ASCII letters.** Fixing the mark
  length keeps one swap a constant-cost operation, so when you talk about
  complexity you are talking about *how many swaps*, not about how long a
  string is. If marks could be arbitrarily long, swapping two of them would
  still be `O(1)` in Python — you move two references, not two strings — but
  the conversation would get muddier than this exercise needs.

- **`start` and `end` are arbitrary Python integers — any sign, any size.**
  This bound exists to force you to validate. Python will cheerfully read
  `cars[-1]` as "the last car", and it will hand you a short slice instead of
  an error when you run off the end. The contract does neither of those
  things. Validation is the entire difference between this exercise and a
  one-liner.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13:

```text
$ python exercise-01-reverse-the-siding-solution.py
flipped  start= 1 end= 3  swaps=1  ['HOP', 'TNK', 'BOX', 'GON', 'FLT'] -> ['HOP', 'GON', 'BOX', 'TNK', 'FLT']
flipped  start= 0 end= 4  swaps=2  ['HOP', 'TNK', 'BOX', 'GON', 'FLT'] -> ['FLT', 'GON', 'BOX', 'TNK', 'HOP']
flipped  start= 0 end= 3  swaps=2  ['HOP', 'TNK', 'BOX', 'GON'] -> ['GON', 'BOX', 'TNK', 'HOP']
refused start= 0 end= 0  swaps=0  ['HOP'] -> ['HOP']
refused start= 0 end= 0  swaps=0  [] -> []
refused start= 2 end= 1  swaps=0  ['HOP', 'TNK', 'BOX'] -> ['HOP', 'TNK', 'BOX']
refused start= 1 end= 7  swaps=0  ['HOP', 'TNK', 'BOX'] -> ['HOP', 'TNK', 'BOX']
refused start=-1 end= 2  swaps=0  ['HOP', 'TNK', 'BOX'] -> ['HOP', 'TNK', 'BOX']
All checks passed.
```

Read the first three lines together. Five cars flipped end to end is **two**
swaps, not five — each swap moves two cars, and the car in the middle of an
odd-length run never moves at all. Four cars is also two swaps, because the
pointers cross without ever meeting. The same `while left < right` handles
both, with no special case for odd and even.

Read the last five lines together too. Every one of them is a real order the
old console could send, and every one of them is refused with the siding
untouched. `start = 1, end = 7` is the interesting one: `cars[1:8]` in Python
does not raise — it quietly hands back the two cars that exist — so a
slice-based solution would reverse those two and report success on an order
that should have been thrown away.

## Steps

1. Save the starter and run it. You get `AssertionError`. Good — the check is
   live.
2. Write the refusal test first, before any pointers. Say the three
   conditions out loud as you type them: `start` below zero, `end` at or past
   the length, `start` not before `end`. Run again; the two refusal asserts
   pass and the first line still fails.
3. Put `left` on `start` and `right` on `end`. Loop `while left < right`.
4. Inside the loop, swap with Python's tuple unpacking:
   `cars[left], cars[right] = cars[right], cars[left]`. No temporary variable
   is needed — the right-hand side is evaluated into a pair before anything is
   assigned.
5. Step `left` up by one, `right` down by one, and add one to your counter.
6. Return the counter. Run the file: you want `1` and the flipped siding on
   the first line, then `All checks passed.`
7. Now trace `["HOP", "TNK", "BOX", "GON"]` with `start = 0, end = 3` on
   paper, and say out loud why the loop stops after two swaps rather than
   four.

## The Solution

```python
"""exercise-01-reverse-the-siding-solution.py — the yard controller's flip order.

Reverse a run of freight cars on a siding, in place, by swapping pairs.
Refuse a nonsense order whole. Report how many swaps were performed.

The self-checks at the bottom are the starter's, unchanged. When they all
pass the file prints "All checks passed."
"""


def reverse_siding(cars: list[str], start: int, end: int) -> int:
    """Reverse cars[start..end] inclusive, in place, by swapping.

    Args:
        cars: The siding, nose-to-tail. Reversed in place when the order is
            valid, and left completely untouched when it is not.
        start: First position of the run to flip.
        end: Last position of the run to flip, inclusive.

    Returns:
        The number of swaps performed. Zero when the order is refused.
    """
    if start < 0 or end >= len(cars) or start >= end:
        return 0

    left, right = start, end
    swaps = 0
    while left < right:
        cars[left], cars[right] = cars[right], cars[left]
        left += 1
        right -= 1
        swaps += 1
    return swaps


# ---- Self-check ----
if __name__ == "__main__":
    orders = [
        (["HOP", "TNK", "BOX", "GON", "FLT"], 1, 3),
        (["HOP", "TNK", "BOX", "GON", "FLT"], 0, 4),
        (["HOP", "TNK", "BOX", "GON"], 0, 3),
        (["HOP"], 0, 0),
        ([], 0, 0),
        (["HOP", "TNK", "BOX"], 2, 1),
        (["HOP", "TNK", "BOX"], 1, 7),
        (["HOP", "TNK", "BOX"], -1, 2),
    ]
    for cars, start, end in orders:
        before = list(cars)
        swaps = reverse_siding(cars, start, end)
        verdict = "refused" if swaps == 0 and cars == before else "flipped "
        print(f"{verdict} start={start:>2} end={end:>2}  swaps={swaps}  {before} -> {cars}")

    siding = ["HOP", "TNK", "BOX", "GON", "FLT"]
    assert reverse_siding(siding, 1, 3) == 1
    assert siding == ["HOP", "GON", "BOX", "TNK", "FLT"]
    assert reverse_siding(["HOP", "TNK", "BOX", "GON", "FLT"], 0, 4) == 2
    assert reverse_siding(["HOP", "TNK", "BOX", "GON"], 0, 3) == 2
    assert reverse_siding(["HOP"], 0, 0) == 0
    assert reverse_siding([], 0, 0) == 0
    assert reverse_siding(["HOP", "TNK", "BOX"], 2, 1) == 0
    assert reverse_siding(["HOP", "TNK", "BOX"], 1, 7) == 0
    assert reverse_siding(["HOP", "TNK", "BOX"], -1, 2) == 0

    untouched = ["HOP", "TNK", "BOX"]
    reverse_siding(untouched, 1, 7)
    assert untouched == ["HOP", "TNK", "BOX"]  # a refused order moves nothing
    print("All checks passed.")
```

**The guard is three tests, and each one names a real failure.** `start < 0`
catches the negative position, which Python would otherwise read as counting
back from the end. `end >= len(cars)` catches the run that falls off the
track — note the `>=`, because position `len(cars)` is one past the last car
and does not exist. `start >= end` catches both the transposed order and the
degenerate run of one, which has nothing to swap anyway. Three tests, one
`return 0`, and the siding has not been touched yet — which is what makes
"refused whole" true rather than aspirational.

**The loop condition is `<`, not `<=`, and the swap count is why.** When the
run holds an odd number of cars the two pointers eventually land on the same
car. With `<=` the loop runs once more, swaps that car with itself — which
changes nothing — and adds one to the count. The siding would still be
correct and the number would be wrong, and the number is what the yard bills
on. This is the smallest possible example of a bug that a test on the *data*
never catches.

**The tuple swap needs no temporary.** `cars[left], cars[right] = cars[right], cars[left]`
builds the pair on the right first, then unpacks it into the two slots. In
most languages you would need a third variable to hold one value while you
overwrote it; here the language does that for you, and the line reads as the
sentence "these two trade places."

**Every swap moves two cars, so a run of `k` cars takes `k // 2` swaps.**
Five cars, two swaps, middle car untouched. Four cars, two swaps, pointers
cross. Say that out loud rather than discovering it from the output — it is
the kind of small arithmetic claim an interviewer will ask you to justify,
and "I traced it" is a weaker answer than "each swap places two of the `k`."

**Nothing here allocates.** Two integers, a counter, and a pair of references
that lives for one line. The siding could hold a hundred thousand cars and
the memory the function uses would not move. That is what `O(1)` auxiliary
space means in practice, and the constraint on the input size is there
specifically so that the claim matters.

## Download and run

Download
[exercise-01-reverse-the-siding-solution.py](./exercise-01-reverse-the-siding-solution.py)
and run it:

```bash
python exercise-01-reverse-the-siding-solution.py
```

It is the same program you are writing, under a name that will not collide
with your own `exercise-01-reverse-the-siding.py`.

## Common bugs to catch

- **`IndexError: list index out of range` on the first swap.** You wrote the
  bound test as `end > len(cars)` instead of `end >= len(cars)`:

  ```text
  Traceback (most recent call last):
      reverse_siding(["HOP", "TNK", "BOX"], 0, 3)
      cars[left], cars[right] = cars[right], cars[left]
                                ~~~~^^^^^^^
  IndexError: list index out of range
  ```

  A list of three has positions `0`, `1` and `2`. Position `3` is one past
  the end. `>` lets that order through, and the very first read of
  `cars[right]` raises. This is the friendly version of the bug — the
  unfriendly one is next.

- **A bare `AssertionError`, and the siding is silently wrong.** You left out
  the `start < 0` test:

  ```text
  Traceback (most recent call last):
      assert reverse_siding(cars, -1, 2) == 0
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  No `IndexError`, because `cars[-1]` is a perfectly legal expression that
  means the last car. Your loop happily swapped positions `-1` and `2`, which
  on a three-car siding are the same car — so it swapped that car with
  itself, reported one swap, and returned. Nothing crashed. That is the whole
  reason the negative test has to be written on purpose: the language will
  not raise it for you.

- **A bare `AssertionError` on the swap count, with the siding correct.** You
  wrote `while left <= right`:

  ```text
  Traceback (most recent call last):
      assert reverse_siding(["HOP", "TNK", "BOX", "GON", "FLT"], 1, 3) == 1
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  The run `1..3` holds three cars. The extra iteration swaps the middle car
  with itself and returns `2`. Look at the siding afterwards and it is
  perfect, which is exactly why this bug survives a careless check.

- **A bare `AssertionError` because you returned the list.**

  ```text
  Traceback (most recent call last):
      assert reverse_siding(["HOP", "TNK", "BOX", "GON", "FLT"], 1, 3) == 1
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AssertionError
  ```

  Comparing a list to an integer is not an error in Python — it is simply
  `False`, so you get the same bare message as the bug above and no hint
  about which of the two it was. Read the signature: the yard bills on the
  swap count.

- **The program never finishes.** You forgot `left += 1` or `right -= 1`, so
  the loop condition never changes. There is no exception; the process
  simply sits there. When a run hangs with no output, suspect a loop whose
  variables are not moving before you suspect anything else.

- **Clamping instead of refusing.** `end = min(end, len(cars) - 1)` feels
  helpful and is wrong. The contract says the order is thrown away, and the
  reason is operational rather than pedantic: a controller that sends a bad
  order needs to find out, and a crew that quietly does *something* hides the
  fault until it matters.

## Under the hood

<details>
<summary>Under the hood — why the tuple swap works, and what reversing really costs</summary>

**What the swap line actually does.**

`a, b = b, a` is not a special "swap" feature. It is two ordinary rules
meeting. Python evaluates the entire right-hand side first, producing the
pair `(b, a)`. Only then does it unpack that pair into the targets on the
left, in order. Because both values were read before any assignment
happened, neither can be clobbered on the way.

You can watch it happen:

```python
import dis
dis.dis("a[i], a[j] = a[j], a[i]")
```

The bytecode loads both values, does a `SWAP`, and stores them back — no
temporary name appears anywhere in your namespace, and for the two-element
case CPython does not build a real tuple object at all; it shuffles the
values on its internal stack.

**Why the strings are never copied.**

A Python list does not hold your strings. It holds *references* to them —
addresses, one machine word each. Swapping two entries swaps two addresses.
The reporting marks themselves never move, are never copied, and are never
compared. That is why the length of a mark does not appear in the complexity,
and it is worth being able to say, because in a language with value semantics
the same code really would copy the characters.

**What this costs, precisely.**

A run of `k` cars takes exactly `k // 2` swaps and `k // 2` iterations, so
the work is `O(k)`. That is the floor: you cannot reverse a run without
touching every car in it, because the car at each position has to end up
somewhere else. The validation is `O(1)` — three comparisons and a `len()`,
and `len()` on a list is `O(1)` because CPython stores the length inside the
list object rather than counting.

**The one-liner, and why it is not the answer here.**

```python
cars[start:end + 1] = cars[start:end + 1][::-1]
```

That works, and on a normal-sized list in normal code it is what you would
write. It builds a slice — a new list of `k` references — then reverses that
into a second new list, then assigns it back. Two allocations, `O(k)`
auxiliary space, on a controller that does not have it. It also cannot report
a swap count honestly, because it does not perform swaps; you would have to
compute `k // 2` separately and hope the two never disagree. And it silently
accepts every invalid order, because slices clamp instead of raising.

Three separate reasons, and only the first is about speed. When an
interviewer asks why you did not reach for the built-in, having three is
much better than having one.

</details>

## Acceptance checklist

- [ ] `python exercise-01-reverse-the-siding.py` prints `1` and the flipped siding, then `All checks passed.`
- [ ] Every refusal case returns `0` **and** leaves the list exactly as it arrived.
- [ ] The loop condition is `while left < right`, and you can say why in one sentence about the swap count.
- [ ] No slice of `cars` is taken anywhere, and no second list is created.
- [ ] The function has type hints and a docstring.
- [ ] You traced an odd-length run and an even-length run on paper and got the same swap count the program reports.
- [ ] You narrated a full FRAME pass out loud with a recorder running, and it lasted at least eight minutes. If you finished in three, you skipped Examine.
- [ ] Committed to Git with a message like `Add Week 1 exercise 1: reverse the siding`.
## Stretch

- **Refuse by raising instead of returning zero.** Some callers want a loud
  failure rather than a quiet count.

  ```python
  def reverse_siding_strict(cars: list[str], start: int, end: int) -> int:
      """Reverse cars[start..end] inclusive; raise ValueError on a bad order."""
      if start < 0 or end >= len(cars) or start >= end:
          raise ValueError(f"bad flip order: start={start}, end={end}, cars={len(cars)}")
      return reverse_siding(cars, start, end)
  ```

  ```text
  ValueError: bad flip order: start=1, end=7, cars=3
  ```

  Then argue with yourself about which is right. A return code makes the
  caller check; an exception makes the caller handle. Neither is universally
  better, and being able to say when each wins is a real interview answer.

- **Rotate the run instead of reversing it.** Move every car in the run
  `shift` places toward the buffer stop, wrapping around inside the run only.

  ```python
  def rotate_siding(cars: list[str], start: int, end: int, shift: int) -> None:
      """Rotate cars[start..end] toward position 0 by `shift`, wrapping inside the run."""
      run = end - start + 1
      shift %= run
      cars[start:end + 1] = cars[start + shift:end + 1] + cars[start:start + shift]
  ```

  Call it on `["HOP", "TNK", "BOX", "GON", "FLT"]` with `start=1, end=4,
  shift=2` and print the siding afterwards:

  ```text
  ['HOP', 'GON', 'FLT', 'TNK', 'BOX']
  ```

  That version allocates. Now do it with `O(1)` auxiliary space and no
  slicing, using the three-reversal trick: reverse the first `shift` cars of
  the run, reverse the rest, then reverse the whole run. Work out on paper
  why that lands everything in the right place before you write it.

- **Count the cars that actually moved, rather than the swaps.** On an
  odd-length run those two numbers differ, and on a run where a car would
  swap with itself they differ again. Decide what the yard would want to bill
  on, and defend the choice in one sentence.

When your siding flips correctly, move on to
[Exercise 2 — The Mirror Serial](./exercise-02-mirror-serial.md).
