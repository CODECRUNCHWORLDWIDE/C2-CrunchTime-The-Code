# Exercise 4 — The Wear-Level Rotation

> **Topic:** fast and slow pointers on a functional graph — the same three phases, with integers where the objects used to be
> **Lecture:** [01 — Floyd's Tortoise and Hare](../lecture-notes/01-floyds-tortoise-and-hare.md), §6
> **Difficulty:** Easy to Medium
> **Target time:** 40 minutes with full FRAME narration, including saying the functional-graph insight out loud
> **Why this one:** the algorithm is already in your hands. What is not in your hands is *noticing that it applies* when the problem contains no chain, no objects, no `next` field and nothing that looks like a linked list. That noticing is the skill Mock #1 will test.

## The Brief

A flash memory chip wears out one block at a time, so a controller spreads
writes around instead of hammering the same block. This particular controller
keeps no bookmark in memory at all. After it writes to slot `s`, it works out
the next slot with a formula:

```text
next_slot(s) = (s * s + 1) % slots
```

Start it at slot `seed` and it writes to `seed`, then to `next_slot(seed)`,
then to `next_slot` of that, and so on forever.

Here is the thing about a rule like that. There are only so many slots, and
every slot has exactly one slot that comes after it. So a walk that goes on
forever through a finite set of places, never branching, **has** to come back to
somewhere it has already been — and once it does, it repeats the same round
forever. It is the footpath and the running track again, with numbers instead
of chutes.

The firmware team needs two numbers before they can ship the part:

- the **tail** — how many slots get written once at the very start of the
  device's life and are then never touched again, and
- the **rotation** — how many slots are in the round the controller settles
  into. Those are the blocks that wear out, so this number decides the
  warranty.

Return them as a pair, tail first.

If `seed` is already inside the rotation, the tail is `0`. That is not an error
and it is not rare.

**The insight, stated plainly, because it is the point of the page.** There is
no linked list in this problem. But `next_slot` gives every slot exactly one
successor, and *that is all a linked list ever was*. The "nodes" are slot
numbers. The "next pointer" is arithmetic. The "loop" is a number you see
twice. Every technique from Exercises 1 and 2 works here unchanged, and nothing
in the problem statement will tell you so.

A structure where every state has exactly one successor has a name: a
**functional graph**. Say that name out loud when you recognise one.

## Starter

Create `exercise-04-wear-level-rotation.py` and paste this in. Fill in every
`TODO`.

```python
"""exercise-04-wear-level-rotation.py — the shape of a write walk.

Fill in every TODO, then run the file. The self-checks at the bottom print
one line per walk and then "All checks passed." when the module is right.
"""

from __future__ import annotations


def next_slot(s: int, slots: int) -> int:
    """Return the controller's successor slot for slot `s`.

    Args:
        s: The slot just written to.
        slots: How many erase blocks the part has.

    Returns:
        The slot the next write lands on: (s * s + 1) % slots.
    """
    # TODO 1: one arithmetic expression. No loop, no recursion.
    ...


def rotation_shape(seed: int, slots: int) -> tuple[int, int]:
    """Return the tail length and the rotation length of the write walk.

    Args:
        seed: The slot the controller starts at.
        slots: How many erase blocks the part has.

    Returns:
        A pair of (tail length, rotation length). The tail is how many slots
        are written once at the start of the device's life and then never
        revisited; the rotation is how many slots repeat forever after that.
        The tail is 0 when `seed` is already inside the rotation.
    """
    # TODO 2: phase one. Step `slow` once and `fast` twice until they hold
    #         the same number. There is no guard here and that is on
    #         purpose — say out loud why the walk cannot end.
    # TODO 3: phase two. Put `finder` back at `seed`, leave `slow` alone,
    #         step both once at a time and count. That count is the tail.
    # TODO 4: phase three. Walk once around from the rotation's first slot,
    #         counting. Take the first step BEFORE the first comparison.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    SUCCESSORS = [(0, 12, 1), (5, 12, 2), (11, 12, 2), (7, 1000, 50), (999, 1000, 2)]
    for s, slots, expected in SUCCESSORS:
        found = next_slot(s, slots)
        assert found == expected, f"next_slot({s}, {slots}): got {found}"

    CASES = [
        ("seed 0, 12 slots", 0, 12, (2, 2)),
        ("seed 5, 12 slots", 5, 12, (0, 2)),
        ("seed 4, 12 slots", 4, 12, (1, 2)),
        ("seed 3, 12 slots", 3, 12, (2, 2)),
        ("seed 0, 3 slots", 0, 3, (2, 1)),
        ("seed 0, 2 slots", 0, 2, (0, 2)),
        ("seed 7, 1000 slots", 7, 1000, (5, 6)),
        ("seed 12345, 2^20 slots", 12_345, 1_048_576, (12, 2)),
    ]

    for label, seed, slots, expected in CASES:
        found = rotation_shape(seed, slots)
        assert found == expected, f"{label}: got {found}, wanted {expected}"
        tail, rotation = found
        print(f"{label:<24} tail {tail:>2}, rotation {rotation}")

    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-04-fast-slow-pointers-and-mock-1/exercises/exercise-04-wear-level-rotation.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `next_slot(s, slots)` is one arithmetic expression. No loop, no recursion.
2. `rotation_shape(seed, slots)` returns a pair, **tail first**, then rotation.
3. The tail is `0` when `seed` is already inside the rotation.
4. The rotation is at least `1`. A slot that is its own successor is a rotation
   of one.
5. There is **no** "no rotation found" branch and no `None` return. There is
   always a rotation; write code that says so.
6. Slots are integers, so the comparison is `==`. Not `is`.
7. Fixed memory: a handful of integers. No `set`, no `dict`, no list of slots
   seen so far, and no recursion.
8. Both functions keep their type hints and their docstrings.

## Constraints

- **Between 2 and 1,048,576 slots, and the memory you use must not grow with
  that number.** Two reasons, both worth saying. First, a `set` of visited slot
  numbers can grow to the full slot count; at 2²⁰ Python integers that is tens
  of megabytes, and this controller has 32 KB of RAM — so the bound is what
  rejects the remember-everything solution. Second, the walk itself is bounded
  by the slot count, and 2²⁰ keeps the worst case fast enough to sit in a test
  suite that runs on every commit.

- **`0 <= seed < slots`.** The controller has to start on a real block.

- **There is always a rotation, so phase one needs no guard.** The set of slots
  is finite and every slot has exactly one successor, so the walk can neither
  run off the end nor branch. It must revisit something. Say this in Frame.
  Candidates who paste a linked-list solution write a `return None` branch that
  can never execute, and unreachable code in an interview reads as *did not
  understand the structure*.

- **Slots are integers, so compare with `==`.** This is the deliberate opposite
  of Exercises 1 and 2. CPython keeps one copy of each small integer, roughly
  −5 to 256, so `is` appears to work below 257 and then silently stops matching.
  That is why one of the checks uses a thousand slots: a solution written with
  `is` passes on `slots = 12` and hangs forever on `slots = 1000`.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-04-wear-level-rotation.py
seed 0, 12 slots         tail  2, rotation 2
seed 5, 12 slots         tail  0, rotation 2
seed 4, 12 slots         tail  1, rotation 2
seed 3, 12 slots         tail  2, rotation 2
seed 0, 3 slots          tail  2, rotation 1
seed 0, 2 slots          tail  0, rotation 2
seed 7, 1000 slots       tail  5, rotation 6
seed 12345, 2^20 slots   tail 12, rotation 2
All checks passed.
```

The `seed 0, 3 slots` line is the one to look at hardest. A rotation of `1` is
a slot whose successor is itself — every write after the second lands on the
same physical block. That is the worst possible wear-levelling result and it is
precisely why the firmware team asked for this number.

## Steps

1. **Frame.** Restate the two numbers and the order they come in. Confirm the
   tail is `0` when the seed is already inside the rotation. Then say the
   sentence that matters: *a rotation always exists, so there is no `None`
   case.* Walk `seed = 0, slots = 12` out loud: `0 -> 1 -> 2 -> 5 -> 2 -> 5 …`,
   so tail 2 and rotation 2.
2. **Research constraints.** Name the 32 KB controller. Name the integer
   comparison and why it is the opposite of the last two drills. Name the
   finite state space as the reason phase one has no guard.
3. **Assess options.** A dictionary mapping each slot to the step it was first
   written at hands you both answers by subtraction, in about six lines. It is
   honestly the nicer program. It costs memory proportional to `tail +
   rotation`, and the controller does not have it. Say which one you would ship
   on a server — the honest answer is the dictionary — and then say why not
   here.
4. **Make the solution, `next_slot`.** One line. Run the file; the successor
   checks pass and the shape checks still fail.
5. **Make the solution, phase one.** `while True`, step, step twice, compare.
   Narrate the missing guard as a consequence of the argument you made in
   Research constraints, not as an oversight.
6. **Make the solution, phases two and three.** Phase two is Exercise 2's
   entrance walk with `==` instead of `is`. Phase three is Exercise 1's
   counting walk, same substitution. You are not inventing anything here; you
   are translating.
7. **Examine.** Trace `seed = 3, slots = 12`. The sequence is
   `3, 10, 5, 2, 5, 2, …`.
   Phase one: slow=3, fast=3. Turn 1: slow=10, fast=5 (two steps: 3→10→5). Turn
   2: slow=5, fast=5 (two steps: 5→2→5). They meet at 5.
   Phase two: finder=3, slow=5, tail=0. Step: finder=10, slow=2, tail=1. Step:
   finder=5, slow=5, tail=2. The rotation starts at 5, after 2 discarded slots.
   Phase three: walker=2, rotation=1. Not 5, so step: walker=5, rotation=2.
   Home. Answer `(2, 2)`.
   Then trace `seed = 0, slots = 3` and confirm you get a rotation of `1`, not
   `0`.
8. **Examine, cost.** O(tail + rotation) time, which is at most O(slots), with
   each step one multiply and one modulo. O(1) space — five integers.

## The Solution

```python
"""exercise-04-wear-level-rotation-solution.py — the shape of a write walk.

There is no chain of objects here. There is a formula, and a formula that
gives every slot exactly one successor is a chain all the same: the "nodes"
are slot numbers and the "next pointer" is the arithmetic.

Three phases. Phase 1 meets the two pointers somewhere inside the rotation.
Phase 2 turns that meeting point into the rotation's first slot and counts
the tail on the way. Phase 3 walks once around to measure the rotation.

The self-checks at the bottom print one line per walk, then
"All checks passed."
"""

from __future__ import annotations


def next_slot(s: int, slots: int) -> int:
    """Return the controller's successor slot for slot `s`.

    Args:
        s: The slot just written to.
        slots: How many erase blocks the part has.

    Returns:
        The slot the next write lands on: (s * s + 1) % slots.
    """
    return (s * s + 1) % slots


def rotation_shape(seed: int, slots: int) -> tuple[int, int]:
    """Return the tail length and the rotation length of the write walk.

    Args:
        seed: The slot the controller starts at.
        slots: How many erase blocks the part has.

    Returns:
        A pair of (tail length, rotation length). The tail is how many slots
        are written once at the start of the device's life and then never
        revisited; the rotation is how many slots repeat forever after that.
        The tail is 0 when `seed` is already inside the rotation.
    """
    slow = seed
    fast = seed
    while True:  # No guard: a finite walk with one successor per slot cannot end.
        slow = next_slot(slow, slots)
        fast = next_slot(next_slot(fast, slots), slots)
        if slow == fast:
            break

    finder = seed
    tail = 0
    while finder != slow:
        finder = next_slot(finder, slots)
        slow = next_slot(slow, slots)
        tail += 1

    walker = next_slot(finder, slots)
    rotation = 1
    while walker != finder:
        walker = next_slot(walker, slots)
        rotation += 1

    return tail, rotation


# ---- Self-check ----
if __name__ == "__main__":
    SUCCESSORS = [(0, 12, 1), (5, 12, 2), (11, 12, 2), (7, 1000, 50), (999, 1000, 2)]
    for s, slots, expected in SUCCESSORS:
        found = next_slot(s, slots)
        assert found == expected, f"next_slot({s}, {slots}): got {found}"

    CASES = [
        ("seed 0, 12 slots", 0, 12, (2, 2)),
        ("seed 5, 12 slots", 5, 12, (0, 2)),
        ("seed 4, 12 slots", 4, 12, (1, 2)),
        ("seed 3, 12 slots", 3, 12, (2, 2)),
        ("seed 0, 3 slots", 0, 3, (2, 1)),
        ("seed 0, 2 slots", 0, 2, (0, 2)),
        ("seed 7, 1000 slots", 7, 1000, (5, 6)),
        ("seed 12345, 2^20 slots", 12_345, 1_048_576, (12, 2)),
    ]

    for label, seed, slots, expected in CASES:
        found = rotation_shape(seed, slots)
        assert found == expected, f"{label}: got {found}, wanted {expected}"
        tail, rotation = found
        print(f"{label:<24} tail {tail:>2}, rotation {rotation}")

    print("All checks passed.")
```

**The recognition, first, because everything else is translation.** Nothing in
the brief says linked list. But `next_slot` gives every slot in `[0, slots)`
exactly one successor and no choices, which is the definition of a functional
graph — and walking a functional graph is walking a chain. Once you have said
that sentence, the rest of the page is Exercises 1 and 2 with `is` swapped for
`==` and `.forwards_to` swapped for `next_slot(...)`.

**Phase one has no guard, and the absence is an argument.**

```python
    while True:  # No guard: a finite walk with one successor per slot cannot end.
```

The walk cannot fall off the end, because there is no end — every slot has a
successor. It cannot branch, because every slot has exactly *one*. And it
cannot go on forever without repeating, because there are only `slots`
different places to be. So it must repeat, so the pointers must meet, so the
loop must exit. Writing `if slow is None: return None` here is not defensive
programming; it is code that can never run, and it tells a reader you were
copying rather than thinking.

**Phase two is the same lemma as Exercise 2, and it is worth re-deriving here
rather than trusting it.** Slow has taken `k` steps and fast `2k`, both landing
on the same slot, so the difference `k` is a whole number of laps. Slow's first
`tail` steps got it to the rotation's first slot, so slow is `k - tail` places
past it. Walk slow `tail` more places and it has gone `k` places past the
entrance, which is a whole number of laps, which means it is back on the
entrance. A pointer starting at `seed` also reaches the entrance in exactly
`tail` steps. Same place, same number of steps, so walking them together
collides there — and the number of steps is the tail.

**Phase three takes its first step before it compares.**

```python
    walker = next_slot(finder, slots)
    rotation = 1
    while walker != finder:
```

Written the other way round, a rotation of length one reports zero, because the
comparison is true before the body has run. The `seed = 0, slots = 3` case
exists to catch that, and a fixed point is not a curiosity — it is the shape
the firmware team most needs to know about.

**`==`, not `is`, and this is the exact inverse of the last two pages.** These
are numbers. CPython keeps a single shared copy of the small ones, so `is`
happens to work while you are testing with twelve slots, then silently stops
matching once the numbers get big and the loop never ends. Say out loud, every
time you start one of these problems, which world you are in: *objects, so `is`*
or *values, so `==`*.

**Nothing here grows with the part.** Five integers: `slow`, `fast`, `finder`,
`walker`, and one counter at a time. That is the 32 KB budget honoured.

## Run it

Copy the worked answer on this page into `exercise-04-wear-level-rotation.py` and run it:

```bash
python exercise-04-wear-level-rotation.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-04-wear-level-rotation.py`.

To grade your own file against the week's larger cases, including the ones
above CPython's cached-integer range:

```bash
C2_WEEK04_SOLUTIONS=exercise-04-wear-level-rotation pytest timed_runner.py -v -k "next_slot or rotation"
```

See [`timed_runner.py`](./timed_runner.py) for the full case list.

## Common bugs to catch

- **Writing a "no rotation" branch.** There is no such case. It is unreachable
  code, it never fires, and in a recorded mock it is the moment an interviewer
  decides you were reciting rather than reasoning.

- **Comparing before stepping.** `slow` and `fast` both start at `seed`, so a
  check at the top of phase one is true immediately and you report a rotation
  of nothing. Step first, compare second — the same rule as Exercise 1.

- **Reporting the meeting point's position as the tail.** For `seed = 3,
  slots = 12` the meeting happens after two turns and the tail is also 2, which
  is a coincidence and will convince you that you are right. Check against
  `seed = 7, slots = 1000`, where the meeting turn is 6 and the tail is 5.

- **A phase-three loop that returns `0` on a fixed point.** `walker = finder`
  with `while walker != finder` never enters the body. `seed = 0, slots = 3` is
  in the check list for exactly this.

- **Using `is` instead of `==`.** There is no traceback. The program simply
  never finishes, because two equal integers above 256 are two different
  objects and the comparison never fires. If your file hangs on a
  thousand-slot case and passes on the twelve-slot ones, this is the bug and
  you do not need to look anywhere else.

- **`ZeroDivisionError: integer modulo by zero`.** You called `next_slot` with
  `slots = 0`:

  ```text
  Traceback (most recent call last):
      return (s * s + 1) % slots
             ~~~~~~~~~~~~^~~~~~~
  ZeroDivisionError: integer modulo by zero
  ```

  The constraint says at least two slots, and this is what enforcing it in the
  caller buys you.

- **Recursing `next_slot`, or writing the walk recursively.** It is one
  arithmetic expression. A recursive walk costs a stack frame per step, which
  is O(tail + rotation) memory and breaks the bound the whole page is about —
  and at 2²⁰ slots it raises `RecursionError` long before that.

## Under the hood

<details>
<summary>Under the hood — what the shape of a random function looks like, and where this drill comes from</summary>

**The tail and the rotation are both about √slots, on average.** If you pick a
successor function at random, the walk from a random seed has an expected tail
and an expected rotation each of roughly `√(π · slots / 8)`. For a million
slots that is about six hundred — not a million. This is the birthday paradox
wearing a different hat: you expect a repeat after about the square root of the
number of possibilities, not after most of them.

Two consequences follow. Floyd's finishes in about `√slots` steps in practice
rather than `slots`, and — much more importantly — the remember-everything
solution needs about `√slots` entries rather than `slots`, which is why people
who have never met the memory bound think the dictionary is fine. On a million
slots it usually is. The bound in the constraints is chosen for the worst case,
which the firmware team has to ship against.

**Why `s² + 1` and not something friendlier.** Squaring folds the number line
onto itself: `s` and `slots - s` have the same square modulo `slots`, so the
map is not one-to-one, so the walk really does have a tail. Compare `s + 1`,
which is a permutation — every slot has exactly one predecessor as well as one
successor — and a permutation has *no* tail at all from any seed. If you want
to see the difference, run your solution against a `next_slot` of
`(s + 1) % slots` and watch every tail come back `0`.

**This drill is Pollard's rho with the label filed off.** In 1975 John Pollard
published a factoring method that iterates exactly `f(x) = (x² + c) mod n` and
uses Floyd's to find a repeat. When the walk repeats, the greatest common
divisor of the difference and `n` is often a real factor of `n`. The successor
function on this page is the same one, and that is not a coincidence — it is
the standard example of a function nobody can afford to remember the outputs
of, because `n` is hundreds of digits long.

**Where else the same recognition pays off.** Any time one thing names exactly
one other thing. A list `handoff` where `handoff[i]` is another index. A
pseudo-random generator whose next value depends only on its current one. A
state machine with one transition per state.
[Homework Problem 1](../homework/problem-01-loopback-self-test.md) is the first
of those, and it will look like an array question right up until you notice it
is not.

</details>

## Acceptance checklist

- [ ] `python exercise-04-wear-level-rotation.py` prints eight lines and then `All checks passed.`
- [ ] Every line matches the Expected output character for character.
- [ ] Phase one has no guard, and you can say in one sentence why not.
- [ ] There is no `None` return and no "no rotation" branch anywhere.
- [ ] Phase three starts at `next_slot(finder, slots)` with the count at `1`.
- [ ] Every comparison between slots uses `==`, and you said out loud why this
      page is the opposite of Exercises 1 and 2.
- [ ] No `set`, no `dict`, no list, no recursion.
- [ ] A FRAME write-up sits at `frame-writeups/c2-week-04/exercise-04-wear-level-rotation.md`
      with a recording of at least 12 minutes, and its Assess-options section
      names the functional-graph insight explicitly.

## Stretch

- **Write the dictionary version and see what you gave up.** Six lines, no
  lemma, both answers by subtraction:

  ```python
  def rotation_shape_with_a_dictionary(seed: int, slots: int) -> tuple[int, int]:
      """The O(n)-space version: remember where each slot was first written."""
      seen: dict[int, int] = {}
      here, step = seed, 0
      while here not in seen:
          seen[here] = step
          here, step = next_slot(here, slots), step + 1
      return seen[here], step - seen[here]
  ```

  ```text
  seed 0, 12 slots         tail  2, rotation 2
  seed 0, 3 slots          tail  2, rotation 1
  seed 7, 1000 slots       tail  5, rotation 6
  ```

  Same answers, shorter code, and it needs a dictionary the controller cannot
  hold. Run both on 2²⁰ slots under `tracemalloc` and put the two numbers in
  your notes.

- **Swap the successor function for a permutation and watch the tail vanish.**
  Try `(s + 1) % slots` and then `(3 * s + 1) % slots` for an odd `slots`:

  ```text
  (s + 1) % 12, seed 0      tail  0, rotation 12
  (3s + 1) % 11, seed 0     tail  0, rotation 5
  ```

  Every tail is `0`, because in a permutation every slot has exactly one
  predecessor too, so nothing can be abandoned. That is a real property with a
  name — a permutation's functional graph is all rotations and no tails — and
  noticing it from the output is worth more than reading it here.

- **Find the seed with the longest tail.** Loop over every seed for
  `slots = 1000`, call `rotation_shape`, and report the worst one. It is a
  three-line script on top of what you have, and it is the sort of question a
  firmware team actually asks: *what is the worst start we could ship?*

  ```text
  slots = 1000   worst seed 7, tail 5, rotation 6
  ```
When the functional-graph insight comes out of your mouth without effort, move
on to [Exercise 5 — The Relay Hop Budget](./exercise-05-relay-hop-budget.md).
