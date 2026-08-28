# Exercise 1 — The Conveyor Loop

> **Topic:** fast and slow pointers — Floyd's tortoise and hare, then a counting walk to measure what it found
> **Lecture:** [01 — Floyd's Tortoise and Hare](../lecture-notes/01-floyds-tortoise-and-hare.md)
> **Difficulty:** Easy
> **Target time:** 30 minutes, including narrating FRAME out loud with the recorder running
> **Why this one:** it is the plainest possible use of the week's pattern, and it adds the one extra step that turns "there is a loop" into a number somebody can act on. Every other page this week is this page plus something. If the six lines of the detection loop are not automatic, nothing later in the week will be.

## The Brief

A parcel sorter is a row of chutes. A parcel drops into the first chute, that
chute tips it into exactly one other chute, and so on. In a sorter that is
wired correctly the last chute tips into nothing at all, and the parcel drops
out into the outbound bin.

Someone has miswired this one. One chute now tips back into a chute the parcel
has already been through. The parcel goes round and round and never comes out.

Picture a running track with a footpath leading up to it. Walk along the
footpath and you arrive at the track. After that, no matter how far you walk,
you are going in circles.

The maintenance crew already knows something is wrong. What they need from you
is **how many chutes are in the circle**, because that is how many they have to
pull off the frame and re-stencil. The footpath does not count. Only the track.

So: given the chute a parcel is dropped into, return the number of chutes in
the loop. Return `0` if a parcel dropped in here eventually falls out the end.

Two words before you start.

**Pointer.** Here a pointer is just a variable holding one chute. Moving it
along means `here = here.forwards_to`. Nothing fancier than that.

**Identity.** Two chutes can carry the same stencilled label. `is` asks *are
these the very same chute*; `==` asks *do these two look alike*. On this page
only `is` means anything, because the labels are unreliable and the objects are
not.

## Starter

Create `exercise-01-conveyor-loop.py` and paste this in. Fill in every `TODO`.

```python
"""exercise-01-conveyor-loop.py — how many chutes are in the loop?

Fill in every TODO, then run the file. The self-checks at the bottom print
one line per wiring and then "All checks passed." when the module is right.
"""

from __future__ import annotations


class Chute:
    """One chute in a parcel sorter. Exactly one outgoing edge, or none."""

    def __init__(self, chute_id: str, forwards_to: "Chute | None" = None) -> None:
        self.chute_id = chute_id
        self.forwards_to = forwards_to


def build_sorter(ids: list[str], loop_to: int | None = None) -> Chute | None:
    """Wire a sorter from a list of stencilled ids.

    Args:
        ids: One id per chute, in order. Ids may repeat.
        loop_to: Index the last chute forwards back to, or None for a
            correctly wired sorter that ends in the outbound bin.

    Returns:
        The entry chute, or None when there are no chutes at all.
    """
    if not ids:
        return None
    chutes = [Chute(chute_id) for chute_id in ids]
    for earlier, later in zip(chutes, chutes[1:]):
        earlier.forwards_to = later
    if loop_to is not None:
        chutes[-1].forwards_to = chutes[loop_to]
    return chutes[0]


def loop_size(entry: Chute | None) -> int:
    """Return how many chutes are in the loop reachable from `entry`.

    Args:
        entry: The chute a parcel is dropped into, or None for no sorter.

    Returns:
        The number of chutes in the loop, or 0 when a parcel entering here
        eventually falls out the end.
    """
    # TODO 1: walk `slow` one chute per turn and `fast` two, until either
    #         they land on the same chute or `fast` runs out of sorter.
    # TODO 2: if `fast` ran out, there is no loop. Return 0.
    # TODO 3: `slow` is now standing somewhere inside the loop. Walk once
    #         around from there, counting, and return the count.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        ("IN -> S1 -> S2 -> S3 -> S1", ["IN", "S1", "S2", "S3"], 1, 3),
        ("IN -> IN", ["IN"], 0, 1),
        ("A -> B -> A", ["A", "B"], 0, 2),
        ("IN -> S1 -> OUT", ["IN", "S1", "OUT"], None, 0),
        ("(no sorter at all)", [], None, 0),
        ("S-12 -> S-12' -> OUT", ["S-12", "S-12", "OUT"], None, 0),
        ("S-12 -> S-12' -> S-12", ["S-12", "S-12"], 0, 2),
        ("A -> B -> C -> D -> E -> E", ["A", "B", "C", "D", "E"], 4, 1),
    ]

    for wiring, ids, loop_to, expected in CASES:
        found = loop_size(build_sorter(ids, loop_to))
        assert found == expected, f"{wiring}: got {found}, wanted {expected}"
        print(f"{wiring:<28} loop of {found}")

    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-04-fast-slow-pointers-and-mock-1/exercises/exercise-01-conveyor-loop.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `loop_size(entry)` returns an **integer count of the chutes in the loop**,
   not a boolean and not the number of chutes you walked past.
2. A sorter that ends in the outbound bin returns `0`.
3. `loop_size(None)` returns `0`. It does not raise.
4. A chute wired to itself returns `1`. That is the smallest loop there is.
5. Chutes are compared with `is`, never with `==` and never by `chute_id`.
6. The function uses a **fixed** number of variables — no `set`, no `dict`,
   no list of chutes seen so far.
7. `loop_size` keeps its type hints and its docstring.

## Constraints

- **Up to 500,000 chutes, and the memory you use must not grow with that
  number.** A half-million-entry `set` of chute objects costs tens of megabytes
  in CPython. The sorter's controller has 64 KB of scratch memory in total. So
  the obvious solution — remember every chute you have seen, stop when you see
  one twice — is not *slow* here. It simply does not fit. Say that distinction
  out loud; "there is nowhere to put it" and "it is slower" are different
  sentences, and an interviewer hears which one you said.

- **Stencilled labels repeat, so identity is the only comparison that means
  anything.** Two physically different chutes can both read `S-12` after a
  refurbishment, because the stencil is painted on the frame and frames get
  swapped. This is why one of the checks wires two chutes both labelled `S-12`
  into a sorter with **no** loop: a solution that collects labels in a set
  reports a loop that is not there.

- **Every chute has exactly one `forwards_to`, and it is either another chute
  or `None`.** That one-way-out property is the whole reason this pattern is
  legal. If a chute could tip into two chutes you would have a branching graph,
  "step twice" would have no single meaning, and you would need a search
  instead — see Week 7.

- **Loop length is at least 1.** A chute may tip into itself. Your counting
  walk has to survive that, and it is the case people get wrong.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-01-conveyor-loop-solution.py
IN -> S1 -> S2 -> S3 -> S1   loop of 3
IN -> IN                     loop of 1
A -> B -> A                  loop of 2
IN -> S1 -> OUT              loop of 0
(no sorter at all)           loop of 0
S-12 -> S-12' -> OUT         loop of 0
S-12 -> S-12' -> S-12        loop of 2
A -> B -> C -> D -> E -> E   loop of 1
All checks passed.
```

Look at line two. `IN -> IN` is one chute tipping into itself, and the answer
is `1`, not `0`. Look at line one as well: the sorter has four chutes and the
answer is `3`, because `IN` is the footpath and not the track.

## Steps

1. **Frame.** Say the problem back in your own words with the recorder
   running. Confirm three things out loud: the answer is a count of loop
   chutes; `None` means zero rather than an error; a self-loop is a loop of
   one. Walk `IN -> S1 -> S2 -> S3 -> S1` by hand and say why the answer is
   three and not four.
2. **Research constraints.** Name the bound that rejects the remember-
   everything approach, and name it precisely: 64 KB of controller memory, not
   "it would be slow". Note that labels repeat, so identity is the comparison.
3. **Assess options.** Two candidates. The visited set is O(n) time and O(n)
   space and would even hand you the loop size for free by subtracting
   positions — say what it is *good* at before you reject it. Floyd's is O(n)
   time and O(1) space, and after it stops you still need one more walk to turn
   its answer into a number.
4. **Make the solution, part one.** Write only the detection loop. Run the
   file. Every case still fails, because you have not returned anything yet,
   but you can `print(slow.chute_id)` after the loop and see for yourself that
   the pointer really is inside the ring.
5. **Make the solution, part two.** Add the counting walk. Start the walker at
   `slow.forwards_to` with the count already at `1`, so the first step is taken
   before the first comparison. Run again and watch `IN -> IN` — that is the
   case this initialisation exists for.
6. **Examine.** Trace `IN -> S1 -> S2 -> S3 -> S1` on paper.
   Detection: slow=IN, fast=IN. Turn 1: slow=S1, fast=S2. Turn 2: slow=S2,
   fast=S1. Turn 3: slow=S3, fast=S3 — they meet. Counting from S3: S1 is one,
   S2 is two, S3 is three and the walker is home. Answer 3.
   Then say the cost out loud: O(n) time, O(1) space, and the same in the best,
   average and worst case, because no wiring changes the amount of work.

## The Solution

```python
"""exercise-01-conveyor-loop-solution.py — how many chutes are in the loop?

Two walks. The first sends a slow pointer one chute at a time and a fast
pointer two at a time until they land on the same chute, which proves there
is a loop and puts you inside it. The second walks once around from there,
counting.

The sorters are built in this file, so it runs on its own with no imports.

The self-checks at the bottom print one line per wiring, then
"All checks passed."
"""

from __future__ import annotations


class Chute:
    """One chute in a parcel sorter. Exactly one outgoing edge, or none."""

    def __init__(self, chute_id: str, forwards_to: "Chute | None" = None) -> None:
        self.chute_id = chute_id
        self.forwards_to = forwards_to


def build_sorter(ids: list[str], loop_to: int | None = None) -> Chute | None:
    """Wire a sorter from a list of stencilled ids.

    Args:
        ids: One id per chute, in order. Ids may repeat.
        loop_to: Index the last chute forwards back to, or None for a
            correctly wired sorter that ends in the outbound bin.

    Returns:
        The entry chute, or None when there are no chutes at all.
    """
    if not ids:
        return None
    chutes = [Chute(chute_id) for chute_id in ids]
    for earlier, later in zip(chutes, chutes[1:]):
        earlier.forwards_to = later
    if loop_to is not None:
        chutes[-1].forwards_to = chutes[loop_to]
    return chutes[0]


def loop_size(entry: Chute | None) -> int:
    """Return how many chutes are in the loop reachable from `entry`.

    Args:
        entry: The chute a parcel is dropped into, or None for no sorter.

    Returns:
        The number of chutes in the loop, or 0 when a parcel entering here
        eventually falls out the end.
    """
    slow = entry
    fast = entry
    while fast is not None and fast.forwards_to is not None:
        slow = slow.forwards_to
        fast = fast.forwards_to.forwards_to
        if slow is fast:
            break
    else:
        return 0

    count = 1
    walker = slow.forwards_to
    while walker is not slow:
        walker = walker.forwards_to
        count += 1
    return count


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        ("IN -> S1 -> S2 -> S3 -> S1", ["IN", "S1", "S2", "S3"], 1, 3),
        ("IN -> IN", ["IN"], 0, 1),
        ("A -> B -> A", ["A", "B"], 0, 2),
        ("IN -> S1 -> OUT", ["IN", "S1", "OUT"], None, 0),
        ("(no sorter at all)", [], None, 0),
        ("S-12 -> S-12' -> OUT", ["S-12", "S-12", "OUT"], None, 0),
        ("S-12 -> S-12' -> S-12", ["S-12", "S-12"], 0, 2),
        ("A -> B -> C -> D -> E -> E", ["A", "B", "C", "D", "E"], 4, 1),
    ]

    for wiring, ids, loop_to, expected in CASES:
        found = loop_size(build_sorter(ids, loop_to))
        assert found == expected, f"{wiring}: got {found}, wanted {expected}"
        print(f"{wiring:<28} loop of {found}")

    print("All checks passed.")
```

**Why two pointers at different speeds ever meet.** Once both pointers are
inside the ring, think about the *gap* between them, measured the way the
parcel travels. Every turn the slow one closes one place and the fast one opens
two, so the gap shrinks by exactly one place per turn. A whole number that goes
down by one each turn and can never drop below zero has to hit zero. That is
the whole proof, and it is why the speeds are one and two: the fast pointer is
exactly one place quicker per turn, so it closes the gap one place per turn and
cannot jump over the slow one.

**The guard has two halves and both are load-bearing.**

```python
while fast is not None and fast.forwards_to is not None:
```

The line inside reads `fast.forwards_to.forwards_to`, which touches two links.
So both must exist before you step. `and` stops as soon as its left side is
false, so when `entry` is `None` the second half is never evaluated and nothing
crashes. That is also why there is no special case for the empty sorter: the
guard fails on its first word and the function falls straight through to
`return 0`.

**`while ... else` is how the two endings stay apart.** A `while` loop's `else`
runs only when the loop finished by its guard going false — never when it
finished by `break`. Here the guard going false means the parcel fell out the
end, which is exactly the no-loop case, so `return 0` belongs there. Leaving by
`break` means the pointers met, which is exactly the loop case, so the counting
walk belongs after the loop. Two endings, two places, and no flag variable to
keep in step.

**The meeting chute is inside the loop, and that is why counting works.** Slow
cannot be caught before it enters the ring, because fast is always ahead of it
and fast got there first. So when they meet, both are on the track. Walking
forward from a chute on the track can only bring you back to that same chute,
and the number of steps that takes is the length of the track.

**The counting walk takes its first step before it compares.**

```python
    count = 1
    walker = slow.forwards_to
    while walker is not slow:
```

Written the other way — `walker = slow` with `count = 0` — the comparison is
already true, the body never runs, and you return `0` for every loop in
existence. The self-loop `IN -> IN` exposes this immediately, which is why it
is second in the check list rather than buried at the bottom.

**Nothing here grows with the sorter.** Two pointers, one walker, one integer.
That is the O(1)-space claim, and it is the sentence the crew's 64 KB
controller is paying for.

## Download and run

Download
[exercise-01-conveyor-loop-solution.py](./exercise-01-conveyor-loop-solution.py)
and run it:

```bash
python exercise-01-conveyor-loop-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-01-conveyor-loop.py`.

To grade your own file against the week's larger, nastier cases, point the
harness at it:

```bash
C2_WEEK04_SOLUTIONS=exercise-01-conveyor-loop pytest timed_runner.py -v -k loop_size
```

See [`timed_runner.py`](./timed_runner.py) for what it checks and how to point
it at a module of your own.

## Common bugs to catch

- **`AttributeError: 'NoneType' object has no attribute 'forwards_to'`.** You
  wrote `while fast is not None:` and left off the second half of the guard:

  ```text
  Traceback (most recent call last):
      fast = fast.forwards_to.forwards_to
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AttributeError: 'NoneType' object has no attribute 'forwards_to'
  ```

  `fast` was the last chute, `fast.forwards_to` was `None`, and asking `None`
  for its `forwards_to` is the crash. Notice *which* sorters this breaks on:
  the correctly wired ones. A loop has no end to fall off, so this bug hides on
  every input the crew is worried about and fires on every input they are not.

- **Comparing at the top of the loop instead of after the step.** Both pointers
  start on `entry`, so a check placed before the first advance is true
  immediately and every sorter — including the correct ones — reports a loop.
  There is no traceback; you just get wrong numbers, which is worse. Advance
  first, compare second.

- **Counting the footpath.** `IN -> S1 -> S2 -> S3 -> S1` returns `4` if you
  count the chutes you walked past rather than the chutes in the ring. The fix
  is not to count differently, it is to *start* differently: begin the count at
  the meeting chute, which is guaranteed to be on the track.

- **A counting walk that returns `0` on a self-loop.** `walker = slow` with
  `while walker is not slow` never enters the body. No exception, just a `1`
  that came back as a `0`. Initialise `walker = slow.forwards_to` and
  `count = 1`.

- **`AttributeError: 'Chute' object has no attribute 'forward_to'`.** A missing
  `s`. Python 3.13 hands you the fix inside the message:

  ```text
  AttributeError: 'Chute' object has no attribute 'forward_to'. Did you mean: 'forwards_to'?
  ```

- **Comparing labels instead of chutes.** `Chute` does not define `__eq__`, so
  `slow == fast` quietly falls back to identity and appears to work — until you
  "improve" it into `slow.chute_id == fast.chute_id`. Then the two chutes
  stencilled `S-12` look like one chute, and `S-12 -> S-12' -> OUT` reports a
  loop of 2 in a sorter with no loop at all. That case is in the self-check for
  exactly this reason.

## Under the hood

<details>
<summary>Under the hood — why the speeds are 1 and 2, and the other cycle algorithm</summary>

**Any pair of speeds one apart works just as well.** Slow at 2 and fast at 3
closes the gap by one place per turn too. Speeds 1 and 2 are chosen for two
reasons. Stepping by one is the cheapest step there is, and — more
importantly — slow ends up somewhere the *second* phase can use.
[Exercise 2](./exercise-02-escalation-loop.md) depends on slow having walked
exactly half of what fast walked, and that is only true at 1 and 2.

Speeds further apart still detect a loop, but the gap now shrinks by two or
three per turn and can step straight over zero. It lands on zero eventually
anyway, because the gap is counted around a ring of length `C` and repeatedly
subtracting a fixed amount modulo `C` visits every multiple of
`gcd(difference, C)`, which includes zero. True, harder to say out loud, and it
buys nothing. Use 1 and 2.

**How long detection takes, precisely.** Let `T` be the footpath length and `C`
the ring length. Slow needs `T` turns to reach the ring. From then on the gap
is at most `C - 1` and shrinks by one per turn, so they meet within another
`C - 1` turns. Detection is therefore at most `T + C` turns, which is at most
the number of chutes. The counting walk is exactly `C` more. Two walks, still
O(n).

**Brent's algorithm is the other answer.** Instead of a hare at double speed,
Brent's keeps the tortoise still and lets the hare run in bursts of 1, 2, 4, 8,
… steps, teleporting the tortoise to the hare at the start of each burst. It
produces the ring length directly, with no second walk, and it makes fewer
successor calls on average than Floyd's — which matters when a single step is
expensive, as it is in integer factorisation. It is almost never asked for in
an interview. Know it exists, name it if someone asks whether Floyd's is
optimal, and move on.

**Where this algorithm actually earns its keep.** Not in parcel sorters.
Floyd's real home is Pollard's rho method for factoring large integers, where
the chain is produced by a formula and storing what you have seen is impossible
because the state space is astronomically large.
[Exercise 4](./exercise-04-wear-level-rotation.md) is a stripped-down version
of exactly that.

</details>

## Acceptance checklist

- [ ] `python exercise-01-conveyor-loop.py` prints eight lines and then `All checks passed.`
- [ ] Every line matches the Expected output character for character.
- [ ] No `set`, no `dict`, no list of visited chutes anywhere in `loop_size`.
- [ ] The guard tests `fast` **and** `fast.forwards_to` before stepping.
- [ ] The counting walk starts at `slow.forwards_to` with the count at `1`.
- [ ] Chutes are compared with `is`; nothing compares `chute_id`.
- [ ] There is no special case for `entry is None` — or, if you wrote one, you
      can say out loud why it is redundant.
- [ ] A FRAME write-up sits at `frame-writeups/c2-week-04/exercise-01-conveyor-loop.md`
      in your portfolio repo, with a recording of at least 10 minutes.
- [ ] The write-up's Research-constraints section says why the visited set is
      rejected in the words "there is nowhere to put it", not "it is slower".

## Stretch

- **Report the footpath as well as the ring.** The crew also wants to know how
  many chutes sit in front of the loop, so they know how far down the frame to
  start looking. That is Floyd's second phase, and it is the whole of
  [Exercise 2](./exercise-02-escalation-loop.md) — try it before you read that
  page:

  ```python
  def loop_shape(entry: Chute | None) -> tuple[int, int]:
      """Return (chutes before the loop, chutes in the loop)."""
      slow = fast = entry
      while fast is not None and fast.forwards_to is not None:
          slow = slow.forwards_to
          fast = fast.forwards_to.forwards_to
          if slow is fast:
              break
      else:
          return 0, 0
      finder, tail = entry, 0
      while finder is not slow:
          finder, slow = finder.forwards_to, slow.forwards_to
          tail += 1
      walker, count = finder.forwards_to, 1
      while walker is not finder:
          walker, count = walker.forwards_to, count + 1
      return tail, count
  ```

  ```text
  IN -> S1 -> S2 -> S3 -> S1   1 before, 3 in the loop
  A -> B -> C -> D -> E -> E   4 before, 1 in the loop
  ```

- **Count every chute the parcel ever touches, footpath and ring together.**
  That is `tail + loop` from the version above. It is worth doing because the
  naive answer — "walk until you repeat, and count" — is the O(n)-space
  solution wearing a different hat. Getting the same number without storing
  anything is the point of the whole week.

  ```text
  IN -> S1 -> S2 -> S3 -> S1   4 chutes touched
  ```

- **Break the loop.** Add a function that finds the chute whose `forwards_to`
  closes the ring, sets it to `None`, and hands the sorter back repaired. Then
  check with `loop_size` that the sorter really is clean.

  ```text
  before: loop of 3
  after : loop of 0
  ```

  That repair is the seed of this week's
  [second challenge](../challenges/challenge-02-feedline-weld.md), which ties a
  loop on purpose and then unties it.

**Practice elsewhere.** The same pattern appears as
[LeetCode 141 · Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/)
if you want a judge to run against. That contract only asks whether a loop
exists, so it will not exercise the counting walk or the repeated-label trap.
Solve this one first.

When the sorter is measured, move on to
[Exercise 2 — The Escalation Loop](./exercise-02-escalation-loop.md).
