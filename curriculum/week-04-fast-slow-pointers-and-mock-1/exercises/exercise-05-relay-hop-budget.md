# Exercise 5 — The Relay Hop Budget

> **Topic:** fast and slow pointers — measure the loop first, then answer with arithmetic instead of walking
> **Lecture:** [01 — Floyd's Tortoise and Hare](../lecture-notes/01-floyds-tortoise-and-hare.md), §3 and §4
> **Difficulty:** Medium
> **Target time:** 45 minutes with full FRAME narration
> **Why this one:** the first four drills ask you to *describe* a loop. This one asks you to *use* it. The number in the prompt is far too big to walk, so the loop's shape stops being an answer and becomes a tool — which is what cycle detection is actually for outside of interview questions.

## The Brief

A radio relay network is a chain of masts. Each mast repeats whatever it hears
onward to exactly one other mast, and the last mast in a healthy run repeats
down to the ground station, where the message is finally read.

Every packet carries a **hop budget**: a number that counts how many more times
it may be repeated. One hop is one mast handing the packet to the next.

Field engineers use this to probe a network they cannot see. They inject a
packet with a specific budget and ask: **which mast is holding it when the
budget runs out?** If the packet reached the ground station before the budget
was spent, the answer is "nothing is holding it" — it was delivered.

That would be a boring question if you could just count. The budget is stored
in a 64-bit field, and the engineers deliberately use enormous values —
`1,000,000,000,000,000,000` is a normal probe — because a huge budget is how
you find out what the network settles into after a long time. Stepping a
billion billion times is not a program anybody will wait for.

Here is the way through. Some of these networks loop: a mast repeats back to a
mast the packet has already been through, so the packet goes round and round.
That is the footpath and the running track from
[Exercise 1](./exercise-01-conveyor-loop.md) again, and this time you need both
numbers — how long the footpath is, and how long the track is.

Once you know those two numbers, a gigantic budget stops being a problem.
Suppose the footpath is 1 mast long and the track is 3 masts round. Hop
1,000,000,000,000,000,000 is 1 hop of footpath followed by
999,999,999,999,999,999 hops of track, and going round a 3-mast track
999,999,999,999,999,999 times lands you exactly where 0 laps would, because
that number divides by 3. So the answer is the mast at the start of the track.
No walking required — one remainder.

Write `hop_landing(first, budget)`. It returns the mast holding the packet
after exactly `budget` hops, or `None` if the packet was delivered before the
budget ran out.

**Word you need.** The **remainder** operator `%` gives what is left over after
dividing. `17 % 5` is `2`, because 17 is three fives with two left. Going
`17` places around a 5-place ring lands you in the same spot as going `2`
places, and that single fact is the whole trick on this page.

## Starter

Create `exercise-05-relay-hop-budget.py` and paste this in. Fill in every
`TODO`.

```python
"""exercise-05-relay-hop-budget.py — where is the packet when the budget runs out?

Fill in every TODO, then run the file. The self-checks at the bottom print
one line per network and then "All checks passed." when the module is right.
"""

from __future__ import annotations


class Mast:
    """One relay mast. It repeats to exactly one other mast, or to none."""

    def __init__(self, call_sign: str, repeats_to: "Mast | None" = None) -> None:
        self.call_sign = call_sign
        self.repeats_to = repeats_to


def build_network(call_signs: list[str], loop_to: int | None = None) -> list[Mast]:
    """Wire a relay run from a list of call signs and hand back every mast.

    Args:
        call_signs: One call sign per mast, in repeat order. Signs repeat
            across regions, so they are not identifiers.
        loop_to: Index the last mast repeats back to, or None for a run that
            ends at the ground station.

    Returns:
        The masts, in order. Empty when `call_signs` is empty.
    """
    masts = [Mast(call_sign) for call_sign in call_signs]
    for earlier, later in zip(masts, masts[1:]):
        earlier.repeats_to = later
    if masts and loop_to is not None:
        masts[-1].repeats_to = masts[loop_to]
    return masts


def hop_landing(first: Mast | None, budget: int) -> Mast | None:
    """Return the mast holding the packet after exactly `budget` hops.

    Args:
        first: The mast the packet is injected at, or None for no network.
        budget: How many times the packet is repeated onward. Zero means the
            packet has not moved yet.

    Returns:
        The mast holding the packet when the budget runs out, or None when
        the packet reached the ground station before the budget ran out.

    Raises:
        ValueError: If `budget` is negative.
    """
    # TODO 1: reject a negative budget, and answer None for no network.
    # TODO 2: Exercise 1's detection loop, unchanged.
    # TODO 3: if there is no loop, the run ends. Walk it, at most once, and
    #         return None the moment the packet leaves the network.
    # TODO 4: there is a loop. Phase two gives you the lead-in length, and a
    #         lap gives you the ring length.
    # TODO 5: turn `budget` into a small number of steps with one remainder,
    #         then walk that far. Careful: a budget inside the lead-in must
    #         not be reduced at all.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    HUGE = 10 ** 18

    LOOPING = [
        ("R1 -> R2 -> R3 -> R4 -> R2", ["R1", "R2", "R3", "R4"], 1, 0, 0),
        ("R1 -> R2 -> R3 -> R4 -> R2", ["R1", "R2", "R3", "R4"], 1, 1, 1),
        ("R1 -> R2 -> R3 -> R4 -> R2", ["R1", "R2", "R3", "R4"], 1, HUGE, 1),
        ("R1 -> R2 -> R3 -> R4 -> R2", ["R1", "R2", "R3", "R4"], 1, HUGE + 1, 2),
        ("SOLO -> SOLO", ["SOLO"], 0, HUGE, 0),
        ("KX-7 -> KX-7' -> KX-7", ["KX-7", "KX-7"], 0, 5, 1),
    ]

    for wiring, signs, loop_to, budget, expected_index in LOOPING:
        masts = build_network(signs, loop_to)
        landed = hop_landing(masts[0], budget)
        assert landed is masts[expected_index], f"{wiring}, budget {budget}"
        print(f"{wiring:<28} budget {budget:>19}  ->  {landed.call_sign}")

    ENDING = [
        ("G1 -> G2 -> G3 -> ground", ["G1", "G2", "G3"], 2, 2),
        ("G1 -> G2 -> G3 -> ground", ["G1", "G2", "G3"], 3, None),
        ("G1 -> ground", ["G1"], 0, 0),
        ("G1 -> ground", ["G1"], 1, None),
    ]

    for wiring, signs, budget, expected_index in ENDING:
        masts = build_network(signs, None)
        landed = hop_landing(masts[0], budget)
        if expected_index is None:
            assert landed is None, f"{wiring}, budget {budget}: packet has left"
            print(f"{wiring:<28} budget {budget:>19}  ->  delivered")
        else:
            assert landed is masts[expected_index], f"{wiring}, budget {budget}"
            print(f"{wiring:<28} budget {budget:>19}  ->  {landed.call_sign}")

    assert hop_landing(None, 4) is None, "no network, nowhere to land"

    try:
        hop_landing(build_network(["G1"])[0], -1)
    except ValueError as caught:
        print(f"{'budget of -1':<28} raises ValueError: {caught}")
    else:  # pragma: no cover - the assert above is the real check
        raise AssertionError("a negative budget must raise")

    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-04-fast-slow-pointers-and-mock-1/exercises/exercise-05-relay-hop-budget.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `hop_landing(first, budget)` returns the `Mast` holding the packet after
   exactly `budget` hops, or `None` if it was delivered first.
2. `budget = 0` returns `first`. The packet has not moved.
3. A negative budget raises `ValueError`. There is no such thing as minus one
   hop, and a caller who computed one has an off-by-one that should be heard
   about now.
4. `hop_landing(None, budget)` returns `None` for any legal budget.
5. The number of steps your code takes must **not** depend on `budget`. It
   depends only on the number of masts.
6. Masts are compared with `is`, never by `call_sign`.
7. Fixed memory: a handful of pointers and integers. No `set`, no `dict`, no
   list of masts.
8. `hop_landing` keeps its type hints and its docstring.

## Constraints

- **The budget fits in a 64-bit field, so it can be as large as about
  9,200,000,000,000,000,000.** This bound is the whole point of the problem. A
  loop that steps once per hop would need roughly three hundred years at a
  billion steps a second, so the simulate-every-hop solution is not slow, it is
  never going to finish. This is the first constraint this week that rejects an
  approach on *time* rather than on memory — note the difference out loud,
  because the last four pages all rejected things on memory and it is easy to
  reach for the same sentence.

- **Up to 200,000 masts, and the memory you use must not grow with that
  number.** The probe runs on a handheld the engineers carry up the tower. Same
  argument as [Exercise 1](./exercise-01-conveyor-loop.md): a set of visited
  masts does not fit, and would not help with the budget anyway.

- **Call signs repeat across regions.** Two masts a thousand kilometres apart
  can both be `KX-7`, because call signs are assigned per region and regions
  reuse them. One of the checks wires two masts both called `KX-7` into a
  two-mast loop and asserts which one by identity.

- **Every mast repeats to exactly one other mast, or to none.** One way out per
  mast is what makes the whole week's pattern legal here.

- **A run with no loop is a real and common shape.** Most healthy networks
  terminate at the ground station, and on those the answer for a large budget
  is `None`. Your code must reach that answer without walking `budget` times —
  it walks the run once at most and stops the moment the packet leaves.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-05-relay-hop-budget-solution.py
R1 -> R2 -> R3 -> R4 -> R2   budget                   0  ->  R1
R1 -> R2 -> R3 -> R4 -> R2   budget                   1  ->  R2
R1 -> R2 -> R3 -> R4 -> R2   budget 1000000000000000000  ->  R2
R1 -> R2 -> R3 -> R4 -> R2   budget 1000000000000000001  ->  R3
SOLO -> SOLO                 budget 1000000000000000000  ->  SOLO
KX-7 -> KX-7' -> KX-7        budget                   5  ->  KX-7
G1 -> G2 -> G3 -> ground     budget                   2  ->  G3
G1 -> G2 -> G3 -> ground     budget                   3  ->  delivered
G1 -> ground                 budget                   0  ->  G1
G1 -> ground                 budget                   1  ->  delivered
budget of -1                 raises ValueError: a hop budget counts hops made, so it cannot be negative
All checks passed.
```

Lines three and four are the ones worth staring at. The same network and two
budgets one apart give different masts, because one lap of a 3-mast ring is
three hops and those two budgets differ by one. If your program prints the same
mast for both, your remainder is being taken over the wrong number.

## Steps

1. **Frame.** Restate the ask. Confirm `budget = 0` returns the first mast.
   Confirm that "delivered" is `None` rather than an error. Say out loud that
   the answer must not depend on how long the budget is, only on the network,
   and write that prediction down so you can check it at the end.
2. **Research constraints.** Name the 64-bit budget as the reason the obvious
   walk is impossible, and be careful to say *time*, not memory — that is a
   change from the last four drills.
3. **Assess options.** One walk per hop: correct, one line, will not finish.
   Store every mast the packet visits with the hop number and look up
   `budget`: correct, still needs `budget` steps in the worst case, and O(n)
   memory besides. Measure the shape, then use a remainder: O(n) time, fixed
   memory, and the budget only appears inside one arithmetic expression.
4. **Make the solution, the terminating case first.** It is the easy half and
   it is easy to forget. If there is no loop, walk forward at most once through
   the run and return `None` the moment you fall off the end.
5. **Make the solution, the looping case.** Phase one detects, phase two gives
   the lead-in, one lap gives the ring. All three are copied from Exercises 1
   and 2.
6. **Make the solution, the arithmetic.** This is the only new line:

   ```python
   steps = budget if budget < lead else lead + (budget - lead) % ring
   ```

   Say why the `if` is there before you write it. A budget that runs out while
   the packet is still on the footpath has nothing to do with the ring, and
   folding it with a remainder would be nonsense.
7. **Examine.** Trace `R1 -> R2 -> R3 -> R4 -> R2` with `budget = 10`. The
   lead-in is 1 mast (`R1`) and the ring is 3 (`R2 R3 R4`). `10` is not less
   than `1`, so `steps = 1 + (10 - 1) % 3 = 1 + 0 = 1`. Walk one mast from
   `R1`: `R2`. Check it the slow way — hop the packet ten times by hand:
   `R2 R3 R4 R2 R3 R4 R2 R3 R4 R2`. `R2`. ✓
8. **Examine, cost.** O(n) time, where `n` is the number of masts and *not* the
   budget: phase one is at most `lead + ring` steps, phase two exactly `lead`,
   the lap exactly `ring`, and the final walk at most `lead + ring - 1`. O(1)
   space. Then check the prediction you wrote in Frame: the budget appears
   exactly once, inside a remainder, and never as a loop bound.

## The Solution

```python
"""exercise-05-relay-hop-budget-solution.py — where is the packet when the
budget runs out?

Walking the budget one hop at a time is the obvious answer and it is far too
slow: the budget is a 64-bit counter. So measure the network's shape first.
A relay run that loops has a straight lead-in of `lead` masts and then a ring
of `ring` masts. Once those two numbers are known, every hop past the lead-in
is arithmetic: hop number `budget` lands at position `lead + (budget - lead)
% ring`, and that position is a short walk from the first mast.

The networks are built in this file, so it runs on its own with no imports.

The self-checks at the bottom print one line per network, then
"All checks passed."
"""

from __future__ import annotations


class Mast:
    """One relay mast. It repeats to exactly one other mast, or to none."""

    def __init__(self, call_sign: str, repeats_to: "Mast | None" = None) -> None:
        self.call_sign = call_sign
        self.repeats_to = repeats_to


def build_network(call_signs: list[str], loop_to: int | None = None) -> list[Mast]:
    """Wire a relay run from a list of call signs and hand back every mast.

    Args:
        call_signs: One call sign per mast, in repeat order. Signs repeat
            across regions, so they are not identifiers.
        loop_to: Index the last mast repeats back to, or None for a run that
            ends at the ground station.

    Returns:
        The masts, in order. Empty when `call_signs` is empty.
    """
    masts = [Mast(call_sign) for call_sign in call_signs]
    for earlier, later in zip(masts, masts[1:]):
        earlier.repeats_to = later
    if masts and loop_to is not None:
        masts[-1].repeats_to = masts[loop_to]
    return masts


def hop_landing(first: Mast | None, budget: int) -> Mast | None:
    """Return the mast holding the packet after exactly `budget` hops.

    Args:
        first: The mast the packet is injected at, or None for no network.
        budget: How many times the packet is repeated onward. Zero means the
            packet has not moved yet.

    Returns:
        The mast holding the packet when the budget runs out, or None when
        the packet reached the ground station before the budget ran out.

    Raises:
        ValueError: If `budget` is negative.
    """
    if budget < 0:
        raise ValueError("a hop budget counts hops made, so it cannot be negative")
    if first is None:
        return None

    slow = first
    fast = first
    while fast is not None and fast.repeats_to is not None:
        slow = slow.repeats_to
        fast = fast.repeats_to.repeats_to
        if slow is fast:
            break
    else:
        # The run ends at the ground station. Walk it, and stop early if the
        # packet leaves the network before the budget is spent.
        here = first
        for _ in range(budget):
            here = here.repeats_to
            if here is None:
                return None
        return here

    finder = first
    lead = 0
    while finder is not slow:
        finder = finder.repeats_to
        slow = slow.repeats_to
        lead += 1

    walker = finder.repeats_to
    ring = 1
    while walker is not finder:
        walker = walker.repeats_to
        ring += 1

    steps = budget if budget < lead else lead + (budget - lead) % ring
    here = first
    for _ in range(steps):
        here = here.repeats_to
    return here


# ---- Self-check ----
if __name__ == "__main__":
    HUGE = 10 ** 18

    LOOPING = [
        ("R1 -> R2 -> R3 -> R4 -> R2", ["R1", "R2", "R3", "R4"], 1, 0, 0),
        ("R1 -> R2 -> R3 -> R4 -> R2", ["R1", "R2", "R3", "R4"], 1, 1, 1),
        ("R1 -> R2 -> R3 -> R4 -> R2", ["R1", "R2", "R3", "R4"], 1, HUGE, 1),
        ("R1 -> R2 -> R3 -> R4 -> R2", ["R1", "R2", "R3", "R4"], 1, HUGE + 1, 2),
        ("SOLO -> SOLO", ["SOLO"], 0, HUGE, 0),
        ("KX-7 -> KX-7' -> KX-7", ["KX-7", "KX-7"], 0, 5, 1),
    ]

    for wiring, signs, loop_to, budget, expected_index in LOOPING:
        masts = build_network(signs, loop_to)
        landed = hop_landing(masts[0], budget)
        assert landed is masts[expected_index], f"{wiring}, budget {budget}"
        print(f"{wiring:<28} budget {budget:>19}  ->  {landed.call_sign}")

    ENDING = [
        ("G1 -> G2 -> G3 -> ground", ["G1", "G2", "G3"], 2, 2),
        ("G1 -> G2 -> G3 -> ground", ["G1", "G2", "G3"], 3, None),
        ("G1 -> ground", ["G1"], 0, 0),
        ("G1 -> ground", ["G1"], 1, None),
    ]

    for wiring, signs, budget, expected_index in ENDING:
        masts = build_network(signs, None)
        landed = hop_landing(masts[0], budget)
        if expected_index is None:
            assert landed is None, f"{wiring}, budget {budget}: packet has left"
            print(f"{wiring:<28} budget {budget:>19}  ->  delivered")
        else:
            assert landed is masts[expected_index], f"{wiring}, budget {budget}"
            print(f"{wiring:<28} budget {budget:>19}  ->  {landed.call_sign}")

    assert hop_landing(None, 4) is None, "no network, nowhere to land"

    try:
        hop_landing(build_network(["G1"])[0], -1)
    except ValueError as caught:
        print(f"{'budget of -1':<28} raises ValueError: {caught}")
    else:  # pragma: no cover - the assert above is the real check
        raise AssertionError("a negative budget must raise")

    print("All checks passed.")
```

**The shape of the network is the answer to every budget at once.** That is the
idea worth taking away. Exercises 1 and 2 treated `lead` and `ring` as the
deliverable. Here they are working parts: two numbers that turn an
unanswerable question — where is the packet after a billion billion hops? —
into one remainder. Any time a problem hands you an absurd number of repetitions
of something that has to loop, this is the move.

**The one new line, read slowly.**

```python
    steps = budget if budget < lead else lead + (budget - lead) % ring
```

If the budget runs out before the packet even reaches the ring, there is
nothing to fold — walk `budget` masts and stop. Otherwise, spend `lead` hops
getting onto the ring, and the remaining `budget - lead` hops are laps. Going
`budget - lead` places around a ring of `ring` places ends up in the same spot
as going `(budget - lead) % ring` places, because whole laps put you back where
you started. So the packet is `lead + (budget - lead) % ring` masts from the
front, and that is a short walk.

**Why `(budget - lead) % ring` and not `budget % ring`.** Because the ring does
not start at the first mast. Folding the whole budget would be measuring laps
from the wrong starting line. Subtract the footpath first, fold what is left,
then add the footpath back. On the `R1 -> R2 -> R3 -> R4 -> R2` network with
`budget = 10`, the right answer is `R2` and `10 % 3 = 1` would send you to
`R2` too — by luck. Try `budget = 11`: the right answer is `R3` and
`11 % 3 = 2` also gives `R3`. The luck runs out the moment the lead-in is not
1; try a two-mast lead-in and the two formulas separate.

**The terminating half is not a special case bolted on — it is a different
question.** A run that ends has no ring, so there is nothing to fold and no
remainder to take. It also has a genuinely different answer: `None`, meaning
delivered. The `while ... else` splits the two apart at exactly the right place,
the same way it did in Exercise 1, and the `for _ in range(budget)` inside it
is safe despite the enormous budget because the walk returns as soon as it
falls off the end. `range` in Python 3 does not build a list; it hands out
numbers one at a time, so `range(10 ** 18)` costs nothing to create.

**`budget` is checked before `first`.** A negative budget is a caller bug
whatever the network looks like, so it is rejected first and unconditionally.
Answering `None` for a bad budget on an empty network, and raising on the same
bad budget when the network is not empty, would be a contract that behaves
differently depending on data the caller cannot see.

**Nothing here grows with the network or with the budget.** Four pointers and
three integers. The budget lives entirely inside one arithmetic expression and
never becomes the length of anything.

## Download and run

Download
[exercise-05-relay-hop-budget-solution.py](./exercise-05-relay-hop-budget-solution.py)
and run it:

```bash
python exercise-05-relay-hop-budget-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-05-relay-hop-budget.py`.

To grade your own file against the week's larger cases:

```bash
C2_WEEK04_SOLUTIONS=exercise-05-relay-hop-budget pytest timed_runner.py -v -k hop_landing
```

See [`timed_runner.py`](./timed_runner.py) for the full case list.

## Common bugs to catch

- **Walking the budget.** `for _ in range(budget): here = here.repeats_to` is
  correct and will never finish. There is no traceback and no error message —
  the test harness just stops at its sixty-second timeout, which is the least
  informative failure there is. If a case with a small budget passes and the
  same network with a big one hangs, this is it.

- **`ZeroDivisionError: integer modulo by zero`.** Your ring came back as `0`:

  ```text
  Traceback (most recent call last):
      steps = lead + (budget - lead) % ring
                     ~~~~~~~~~~~~~~~~^~~~~~
  ZeroDivisionError: integer modulo by zero
  ```

  A ring is never zero masts long — the smallest is a mast repeating to itself.
  You almost certainly wrote the lap as `walker = finder` with `ring = 0`
  instead of taking the first step first. `SOLO -> SOLO` is the case that
  catches it.

- **Folding the whole budget instead of what is left after the lead-in.**
  `lead + budget % ring` looks close enough and is wrong whenever the lead-in
  is longer than one mast. It also happens to be right on several small
  examples, which is why the check list includes a four-mast network rather
  than only self-loops.

- **Forgetting that a budget shorter than the lead-in must not be folded.**
  Without the `if`, `budget = 0` on the `R1 -> R2 -> R3 -> R4 -> R2` network
  computes `1 + (0 - 1) % 3`, and Python's remainder on a negative number gives
  `2`, so you get `steps = 3` and answer `R4` for a packet that has not moved.
  No exception, just a confidently wrong mast.

- **`AttributeError: 'NoneType' object has no attribute 'repeats_to'`.** The
  final walk ran off the end:

  ```text
  Traceback (most recent call last):
      here = here.repeats_to
             ^^^^^^^^^^^^^^^
  AttributeError: 'NoneType' object has no attribute 'repeats_to'
  ```

  That means you took the looping branch on a run that terminates, or your
  `steps` came out larger than the network. Check that the `while ... else`
  returns before the ring code can start.

- **Returning the first mast for a delivered packet.** A run that ends and a
  budget past its end must give `None`, not the last mast and not the first.
  `G1 -> ground` with `budget = 1` is the smallest case, and it is in the list
  for that reason.

- **Comparing call signs.** `KX-7 -> KX-7' -> KX-7` has two masts with the same
  name in a two-mast ring, and the check asserts the second one by identity.

## Under the hood

<details>
<summary>Under the hood — the same trick under other names, and why Python's negative remainder saved you</summary>

**This is modular exponentiation's simpler cousin.** The general shape is: an
operation repeats, the state space is finite, therefore the states cycle,
therefore question about step `N` reduces to a question about `N` modulo the
cycle length. You meet the same move in three other places at least:

- **Last digit of a power.** The last digit of `7ⁿ` cycles 7, 9, 3, 1, so
  `7¹⁰⁰⁰` ends in the same digit as `7⁴`.
- **Day of the week.** Days cycle every 7, so "what day is it in a million
  days" is one remainder.
- **Pseudo-random generators.** A generator with a fixed state size must
  eventually repeat, and its **period** is the ring length. Asking for the
  billionth output is asking this exact question.

Naming the family out loud — "this is a finite state space, so the answer is
periodic" — is worth more in an interview than the code, because it is what
transfers.

**Python's `%` is never negative, and here that hid a bug rather than fixing
one.** In Python, `(-1) % 3` is `2`, not `-1`, because the result always takes
the sign of the divisor. That is usually a kindness. On this page it is a trap:
without the `if budget < lead` guard, a small budget produces a plausible
positive index instead of an obviously wrong negative one, so the bug survives
a glance. In C the same expression gives `-1` and the program crashes
immediately. Neither language is wrong; the lesson is that a language which
tidies up an invalid intermediate value makes the invalid case harder to
notice, so you have to notice it yourself.

**Why the final walk is not folded into the earlier ones.** You could keep a
pointer at the front during phase two and stop it at the right place, saving
one pass. It would be a third of the passes and about a third of the clarity,
and all four passes are already O(n), so the total is O(n) either way. Prefer
four readable walks to one clever one, and say so out loud — knowing when *not*
to optimise is graded too.

**What happens when the network is a single ring with no footpath.** `lead` is
`0`, the `if` is never taken because no budget is less than zero, and the
formula collapses to `budget % ring`. The general case degrades to the simple
case with no branch of its own, which is the sign that the formula is the right
shape rather than a patchwork.

</details>

## Acceptance checklist

- [ ] `python exercise-05-relay-hop-budget.py` prints eleven lines and then `All checks passed.`
- [ ] Every line matches the Expected output character for character.
- [ ] `budget` never appears as the bound of a loop that can actually run that
      many times.
- [ ] A negative budget raises `ValueError` before anything else happens.
- [ ] The terminating run returns `None` without walking more than once.
- [ ] The lap starts at `finder.repeats_to` with the count at `1`.
- [ ] The remainder is taken over `budget - lead`, not over `budget`.
- [ ] Masts are compared with `is`; nothing compares `call_sign`.
- [ ] A FRAME write-up sits at `frame-writeups/c2-week-04/exercise-05-relay-hop-budget.md`
      with a recording of at least 12 minutes, and its Research-constraints
      section says the rejection here is about **time**, unlike the four drills
      before it.

## Stretch

- **Answer many budgets on one network without re-measuring it.** Measure the
  shape once, hand back a small function that answers any budget in constant
  time after that:

  ```python
  def hop_probe(first: Mast | None):
      """Measure the network once, then answer any budget with arithmetic."""
      landmarks = [first]
      here = first
      while here is not None and here.repeats_to is not None:
          if any(here.repeats_to is mast for mast in landmarks):
              break
          here = here.repeats_to
          landmarks.append(here)
      return lambda budget: hop_landing(first, budget)
  ```

  Then decide whether that helper is worth having. It is not, as written — it
  builds a list, which the handheld cannot afford. Fixing it to store only
  `lead` and `ring` is the actual exercise, and noticing that the obvious
  version broke the memory bound is the point.

- **Report how many full laps the packet completed.** The engineers want it for
  a wear estimate. It is `(budget - lead) // ring` when the budget reaches the
  ring, and zero otherwise:

  ```text
  R1 -> R2 -> R3 -> R4 -> R2   budget 10                     3 full laps
  R1 -> R2 -> R3 -> R4 -> R2   budget 1000000000000000000    333333333333333333 full laps
  ```

- **Ask the reverse question.** Given a mast, what is the smallest budget that
  lands a packet on it? On the footpath that is its position; on the ring it is
  its position, and every position plus a whole number of laps works too. State
  the answer as "smallest budget, and the period after that", and notice that
  masts on the footpath have no period at all — you can only land on them once.
When all five drills pass, move on to
[Challenge 1 — Booklet Imposition](../challenges/challenge-01-booklet-imposition.md).
