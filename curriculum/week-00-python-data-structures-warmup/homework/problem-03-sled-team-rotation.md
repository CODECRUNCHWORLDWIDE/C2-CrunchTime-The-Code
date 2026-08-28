# Problem 3 — The Sled Team's Rotation

> **Topic:** three ways to answer the same question — rebuild the list, rotate a deque, or do the arithmetic and touch nothing
> **Lecture:** [02 — Lists, Tuples and the Dynamic Array](../lecture-notes/02-lists-tuples-and-the-dynamic-array.md)
> **Difficulty:** Beginner
> **Target time:** 20 minutes
> **Why this one:** the cheapest version of a job is often the one that builds nothing at all. Rotating a list of six dogs costs a new list of six. Working out who is at the front costs one `%`. Spotting that difference is a habit, and the place to build it is somewhere the wasteful version is obviously fine — because the same choice, inside a loop over a million positions, is not.

## The Brief

A six-dog sled team runs in a fixed order, lead dog first:

```python
["Nika", "Bram", "Oso", "Pilot", "Skua", "Tuk"]
```

Leading is the hard job, so the team rotates. On day 1 the second dog leads and
everyone shifts up one, with yesterday's lead going to the back. On day 2 the
third dog leads. On day 6 the team is back where it started.

You are writing three functions, and they all answer the same question in
different ways.

**Rebuild the list.** `team[cut:] + team[:cut]` takes the back part and the
front part and glues them together — a new list, in the rotated order.

**Rotate a deque.** `deque.rotate(n)` moves everything round without building
anything. It counts the *other* way, though: `rotate(1)` moves the last dog to
the front, so rotating forward by `steps` is `rotate(-steps)`.

**Do the arithmetic.** If all you want to know is who is leading, you do not
need the rotated order at all. `team[day % len(team)]` is the answer, and it
touches nothing.

`%` — the remainder — is what makes all three handle a big number of days.
`13 % 6` is `1`, because thirteen days is two full loops and one more. It also
handles going backwards: `-1 % 6` is `5` in Python, which is exactly the dog
you want when you rotate one place the other way. That is worth checking in a
REPL if you have met a language where it is not.

## Starter

Create `problem-03-sled-team-rotation.py` in your practice folder and paste
this in. Fill in every `TODO`.

```python
"""problem-03-sled-team-rotation.py — who runs at the front today.

Three ways to answer that, and only one of them is free. Rotating a list
builds a new list. Rotating a deque moves a pointer. Working out the lead
with one modulo touches nothing at all.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from collections import deque

TEAM: list[str] = ["Nika", "Bram", "Oso", "Pilot", "Skua", "Tuk"]


def rotate_list(team: list[str], steps: int) -> list[str]:
    """Return a NEW running order with the team rotated forward.

    Args:
        team: The running order, lead dog first.
        steps: How many places to move forward. May be bigger than the team
            and may be negative.

    Returns:
        A new list. The team handed in is not changed.
    """
    # TODO: guard the empty team, take steps % len(team), then two slices
    ...


def rotate_deque(team: list[str], steps: int) -> list[str]:
    """Return the same running order, rotated with a deque."""
    # TODO: deque(team), rotate the other way, back to a list
    ...


def lead_on_day(team: list[str], day: int) -> str | None:
    """Return the dog leading on a given day, without rotating anything."""
    # TODO: one index and one modulo. None on an empty team.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    for day in (0, 1, 2, 13):
        order = rotate_list(TEAM, day)
        print(f"day {day:>2}  lead {lead_on_day(TEAM, day):<6} order: {', '.join(order)}")

    for steps in range(-8, 9):
        assert rotate_list(TEAM, steps) == rotate_deque(TEAM, steps)
        assert rotate_list(TEAM, steps)[0] == lead_on_day(TEAM, steps)

    assert rotate_list(TEAM, 0) == TEAM
    assert rotate_list(TEAM, 6) == TEAM
    assert rotate_list(TEAM, 2)[0] == "Oso"
    assert rotate_list(TEAM, -1)[0] == "Tuk"
    assert lead_on_day(TEAM, 13) == "Bram"
    assert rotate_list([], 3) == []
    assert lead_on_day([], 3) is None
    assert TEAM[0] == "Nika"  # the running order is untouched
    print("All checks passed.")
```

Two things you need before you start.

**`%` in Python always gives a result with the sign of the right-hand side.**
So `-1 % 6` is `5`, not `-1`. That single fact is why none of these functions
needs an `if steps < 0` branch, and it is not true in C or Java, where `-1 % 6`
is `-1`.

**The loop of asserts over `range(-8, 9)`** checks all three functions agree at
seventeen different step counts, including negatives and numbers larger than
the team. That is a small property test: rather than checking three chosen
answers, it checks that three independent implementations say the same thing
everywhere. When they disagree, one of them is wrong and you have to work out
which — which is more useful than being told.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/courses/ide#src=C2-CrunchTime-The-Code/curriculum/week-00-python-data-structures-warmup/homework/problem-03-sled-team-rotation.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `rotate_list(team, steps)` returns a new list rotated forward by `steps`,
   for any integer `steps`, and does not change `team`.
2. `rotate_deque` returns the same list as `rotate_list` for every step count.
3. `lead_on_day(team, day)` returns the lead dog without building a rotated
   list.
4. `rotate_list([], n)` returns `[]` and `lead_on_day([], n)` returns `None`.
   Neither raises.
5. `rotate_list(team, 0)` and `rotate_list(team, len(team))` both equal `team`.
6. `TEAM` is unchanged. Every function keeps its type hints and its docstring.

## Constraints

- **Take the remainder before slicing.** `team[8:]` on a six-dog team is `[]`
  and `team[:8]` is the whole team, so rotating by 8 without the `%` gives you
  the team back unrotated — a wrong answer with no error. `steps % len(team)`
  turns 8 into 2 and -1 into 5.

- **Guard the empty team first.** `steps % 0` raises
  `ZeroDivisionError: integer modulo by zero`. An empty team is a real input —
  it is what you get before anybody has been harnessed — and the guard is one
  line.

- **`rotate_list` returns a new list and changes nothing.** The team's running
  order is the master record. A function that rotated it in place would mean
  the record depends on how many times you asked a question, which is how a
  reporting function ends up owning data it was only meant to read.

- **`lead_on_day` must not rotate.** Building six names to read one is
  `O(n)` time and `O(n)` memory for an answer that costs `O(1)`. At six dogs
  the waste is invisible and the habit is the point: when a question asks for
  one element of a transformed sequence, ask whether you can index into the
  original instead.

- **A season is at most 400 days and a team at most 16 dogs.** Those are the
  real numbers — the long-distance races run under two weeks, a big team is
  fourteen dogs, and 400 covers training. They matter because they tell you
  `day` can be much larger than the team, which is what makes the `%` load-
  bearing rather than decorative.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python problem-03-sled-team-rotation.py
@@STDOUT:problem-03-sled-team-rotation-solution.py@@
```

Day 13 and day 1 print the same order, because `13 % 6` is `1` — two full loops
and one day more. If day 13 prints the team unrotated, your `%` is missing and
the slices ran off both ends.

## Steps

1. Create the file, paste the starter, and run it. It fails at the first
   `', '.join(None)`.
2. Write `rotate_list`. Guard the empty team, take the remainder, then two
   slices and a `+`.
3. Run it and check day 13 against day 1 by eye before the asserts do.
4. Write `rotate_deque`. Try `ring.rotate(steps)` first, run the file, and read
   which assert fails — the two implementations disagree, which is the
   property test doing its job. Then flip the sign.
5. Write `lead_on_day`.
6. When it passes, delete the `%` from `rotate_list` and run it again. Six of
   the seventeen property asserts fail. Put it back.

## The Solution

```python
@@CODE:problem-03-sled-team-rotation-solution.py@@
```

**One remainder makes every step count legal.**

```python
cut = steps % len(team)
return team[cut:] + team[:cut]
```

`cut` is where the new front begins. For a six-dog team, `steps` of `2`, `8`
and `-4` all give `cut = 2`, so all three produce the same order — which is
correct, because rotating a ring by any of those lands in the same place. That
is the whole reason the remainder belongs here and not in a wrapper: the
function's contract says "any integer", and one line delivers it.

The two slices copy every dog exactly once, so `rotate_list` is `O(n)` time and
`O(n)` space. There is no cheaper way to *produce a rotated list*, because
producing `n` items costs `n`. The next function is cheaper only because it
does not produce one.

**`rotate_deque` counts the other way, and that is worth reading twice.**
`deque.rotate(1)` takes the item off the right-hand end and puts it on the
left — everything shifts *right*. Rotating forward, the way a sled team does,
is `rotate(-steps)`. Nothing about that is arbitrary; it matches
`deque.rotate` being the ring-buffer version of `insert(0, pop())`. But it is
exactly the kind of sign that is guessed wrong, which is why the property test
compares the two implementations rather than trusting either.

Note what `rotate` costs. On a deque it moves pointers rather than elements, so
rotating by `k` is `O(k)`, not `O(n)` — cheap when `k` is small even if the
deque is huge. Then `list(ring)` copies the whole thing back out, `O(n)`, and
that copy is the expensive part of this function. Building a deque to rotate a
list you already have is usually not worth it; keeping the data in a deque all
along is.

**`lead_on_day` does the whole job with one `%` and one index.**

```python
return team[day % len(team)]
```

`O(1)` time, `O(1)` space, nothing built. Look at what the other two functions
do to answer the same question: they construct all six names so that you can
read the first one. This is the smallest possible version of a decision you
will make constantly — *do I need the transformed collection, or one thing out
of it?* — and the answer changes what your solution costs by a whole factor of
`n`.

**Both empty-team guards are in the asserts for a reason.** `steps % 0` raises
`ZeroDivisionError`, and `team[day % 0]` would too. The two functions return
`[]` and `None`, which are the honest answers: an empty team has an empty
running order and has nobody at the front.

## Download and run

Download
[problem-03-sled-team-rotation-solution.py](./problem-03-sled-team-rotation-solution.py)
and run it:

```bash
python problem-03-sled-team-rotation-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `problem-03-sled-team-rotation.py`.

## Common bugs to catch

- **Day 13 prints the team unrotated.** The `%` is missing. `team[13:]` is `[]`
  and `team[:13]` is the whole team, so the two slices glue back to the
  original. No error, and the answer looks like a team that forgot to rotate.

- **`ZeroDivisionError: integer modulo by zero`.** You took the remainder
  before checking for an empty team:

  ```text
  Traceback (most recent call last):
      cut = steps % len(team)
            ~~~~~~^~~~~~~~~~~
  ZeroDivisionError: integer modulo by zero
  ```

  Guard first. This is the only input that can make any of the three functions
  raise.

- **`rotate_deque` disagrees with `rotate_list` for every non-zero step.** The
  sign is the wrong way round. `deque.rotate(n)` moves items towards the right;
  forward rotation is `rotate(-steps)`. The property test catches this at
  `steps = -8` before you have looked at any output, which is why it is a loop
  rather than three hand-picked cases.

- **`AttributeError: 'list' object has no attribute 'rotate'`.** You called it
  on the list:

  ```text
  AttributeError: 'list' object has no attribute 'rotate'
  ```

  Build the deque first. A list has no rotate, and the closest thing —
  `team.insert(0, team.pop())` — is `O(n)` per step for the reason Exercise 2
  spent a page on.

- **`TypeError: 'str' object cannot be interpreted as an integer`.** You passed
  the day through as text:

  ```text
  TypeError: 'str' object cannot be interpreted as an integer
  ```

  `deque.rotate` wants a number. If the day came from a file or an argument, it
  is text until you convert it.

- **`lead_on_day` builds the rotated list and reads `[0]`.** It gives the right
  answer and misses the point of the function. If your version contains a slice
  or a `deque`, it is the wrong version.

- **`TEAM` changed.** You wrote `team.sort()`, `team.reverse()`, or
  `team[:] = rotated` somewhere. The last assert exists for this: a reporting
  function that quietly reorders the caller's list is a bug even when every
  value it returned was right.

## Under the hood

<details>
<summary>Under the hood — what rotate actually moves, and why % has the sign it does</summary>

**`deque.rotate` moves the ends, not the middle.** A deque is a chain of
fixed-size blocks with a marker at each end. Rotating by `k` unlinks `k` items
from one end and links them onto the other, so the cost is `O(k)` — and CPython
takes whichever direction is shorter, so rotating a 1000-item deque by 999 is
about as cheap as rotating it by 1. The items in the middle are never touched.

Rotating a **list** cannot work that way, because a list is one contiguous row
with a fixed starting address. There is no marker to move, so every element has
to be written to a new position: `O(n)`, whatever `k` is.

**Why `-1 % 6` is `5`.** Python defines the remainder to have the sign of the
divisor, so `a % n` is always in `0 … n-1` for positive `n`. C and Java define
it to have the sign of the dividend, so `-1 % 6` is `-1` there and every
wrap-round needs `((a % n) + n) % n`.

Python's choice is the one that makes ring arithmetic work with no ceremony,
and it is the same reason `//` rounds towards negative infinity rather than
towards zero: the two are defined together so that `a == (a // n) * n + a % n`
always holds.

```python
-1 % 6      # 5
-1 // 6     # -1
(-1 // 6) * 6 + (-1 % 6)   # -1, as promised
```

**The rotation identity.** Rotating by `k` and then by `m` is the same as
rotating by `k + m`, and rotating by `len(team)` is the identity. That is what
makes the property test in the starter meaningful: it is checking an algebraic
fact about the operation, not a list of examples somebody chose.

**Where this comes back.** Ring buffers, round-robin scheduling, and the
"rotate an array in place with three reversals" trick all rest on the same
remainder arithmetic. The three-reversal version — reverse the whole thing,
then reverse each part — rotates in `O(n)` time and `O(1)` extra space, which
beats the two-slice version's `O(n)` extra memory. Worth deriving on paper
once; it is a classic interview follow-up to exactly this question.

</details>

## Acceptance checklist

- [ ] `python problem-03-sled-team-rotation.py` prints four day lines then
      `All checks passed.`
- [ ] Day 13 and day 1 print the same order.
- [ ] All seventeen property asserts pass, negatives included.
- [ ] `lead_on_day` contains no slice and no deque.
- [ ] The empty team is guarded in both functions.
- [ ] `TEAM` is in its original order at the end.
- [ ] You can say what `-1 % 6` is in Python and why.

## Stretch

- **Rotate in place with three reversals, and use no extra list at all.**

  ```python
  def rotate_in_place(team: list[str], steps: int) -> None:
      """Rotate the caller's own list forward, using O(1) extra space."""
      if not team:
          return
      cut = steps % len(team)
      team.reverse()
      team[:len(team) - cut] = reversed(team[:len(team) - cut])
      team[len(team) - cut:] = reversed(team[len(team) - cut:])
  ```

  ```text
  ['Oso', 'Pilot', 'Skua', 'Tuk', 'Nika', 'Bram']
  ```

  The same answer as `rotate_list(TEAM, 2)`, with no new list returned — though
  read the slice assignments closely, because `reversed(team[:k])` still builds
  a temporary. Making it genuinely `O(1)` means writing the swap loop by hand.
  Do that, and you have the classic in-place rotation.

- **Ask which day a given dog leads next.**

  ```python
  def next_lead_day(team: list[str], dog: str, today: int) -> int | None:
      """Return the next day on or after `today` when `dog` leads."""
      if dog not in team:
          return None
      position = team.index(dog)
      return today + (position - today) % len(team)
  ```

  ```text
  Oso leads next on day 2
  Tuk leads next on day 5
  Nika leads next on day 6
  ```

  The same remainder, running the other way: instead of "who is at position
  `day`", it asks "which day lands on this position". Asked on day 0, `Nika`
  answers 6 rather than 0 — the rule says *on or after today*, and today's lead
  has already led. Whether that is right is a specification question, and
  noticing that you have to ask it is the exercise.

- **Check the identity rather than the examples.**

  ```python
  for first in range(-3, 4):
      for second in range(-3, 4):
          once = rotate_list(rotate_list(TEAM, first), second)
          together = rotate_list(TEAM, first + second)
          assert once == together
  print("rotation composes for 49 pairs")
  ```

  ```text
  rotation composes for 49 pairs
  ```

  Forty-nine checks, three lines, and no example data invented by hand. When a
  function obeys a law, testing the law finds bugs that three chosen cases
  will not.

Next: [Problem 4 — The Library's Returns Cart](./problem-04-returns-cart.md).
