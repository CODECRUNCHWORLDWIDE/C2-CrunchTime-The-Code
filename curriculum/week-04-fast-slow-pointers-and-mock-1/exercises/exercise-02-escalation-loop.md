# Exercise 2 — The Escalation Loop

> **Topic:** fast and slow pointers — Floyd's detection plus the cycle-entrance lemma, with the distance counted on the way
> **Lecture:** [01 — Floyd's Tortoise and Hare](../lecture-notes/01-floyds-tortoise-and-hare.md), §4
> **Difficulty:** Medium
> **Target time:** 45 minutes, including saying the lemma out loud until it sounds natural
> **Why this one:** detecting a loop is mechanical. Finding where the loop *starts* is the piece of reasoning that separates people who memorised a loop shape from people who understand it. The distance is asked for on purpose: it is free to compute and impossible to fake.

## The Brief

An on-call rota is a chain of slots. A page that nobody answers escalates to
exactly one other slot. In a rota that is set up correctly the last slot
escalates to nothing, and at that point a director's phone rings.

This rota has been misconfigured. Some slot escalates back into a slot the page
has already been through, so the page circles a small group of people forever
and nobody outside that group ever hears it.

Back to the footpath and the running track from
[Exercise 1](./exercise-01-conveyor-loop.md). The page walks the footpath, gets
on the track, and never leaves. Exercise 1 measured the track. This page asks
something harder: **which step is the one where the footpath joins the track**,
and **how many steps of footpath came before it**.

That first slot on the track is the **entrance**. It is the first slot the page
will ever visit twice. The platform team needs two things from you: the
entrance itself, so they know which escalation rule is wrong, and the hop
count, so they know how many correctly wired slots sit in front of it and how
far down the rota to start reading.

Return them together as a pair. Return `None` if the rota terminates.

One warning that this whole page exists for: the place where the two pointers
meet is **not** the entrance. It is somewhere on the track, but usually not the
join. Getting from the meeting point to the entrance is a second, separate
walk, and it works for a reason you should be able to say out loud.

## Starter

Create `exercise-02-escalation-loop.py` and paste this in. Fill in every
`TODO`.

```python
"""exercise-02-escalation-loop.py — where does the paging loop start?

Fill in every TODO, then run the file. The self-checks at the bottom print
one line per rota and then "All checks passed." when the module is right.
"""

from __future__ import annotations


class Rota:
    """One on-call slot. It escalates to exactly one other slot, or to none."""

    def __init__(self, slot: str, escalates_to: "Rota | None" = None) -> None:
        self.slot = slot
        self.escalates_to = escalates_to


def build_rota(labels: list[str], loop_to: int | None = None) -> list[Rota]:
    """Wire a rota from a list of labels and hand back every slot.

    Args:
        labels: One label per slot, in escalation order. Labels may repeat.
        loop_to: Index the last slot escalates back to, or None for a rota
            that reaches the top and stops.

    Returns:
        The slots, in order. Empty when `labels` is empty.
    """
    slots = [Rota(label) for label in labels]
    for earlier, later in zip(slots, slots[1:]):
        earlier.escalates_to = later
    if slots and loop_to is not None:
        slots[-1].escalates_to = slots[loop_to]
    return slots


def find_escalation_loop(start: Rota | None) -> tuple[Rota, int] | None:
    """Return the loop's entrance and how many hops sit in front of it.

    Args:
        start: The slot a page begins at, or None for no rota at all.

    Returns:
        A pair of (entrance slot, hops from `start` to it), or None when the
        rota terminates and the page reaches a director.
    """
    # TODO 1: phase one is Exercise 1's detection loop, unchanged. Walk
    #         `slow` by one and `fast` by two until they meet, or until
    #         `fast` runs out of rota.
    # TODO 2: if `fast` ran out, the rota is fine. Return None.
    # TODO 3: phase two. Put `finder` back at `start`, leave `slow` where it
    #         stopped, and walk BOTH one slot at a time, counting, until
    #         they land on the same slot. Return that slot and the count.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        ("L1 -> L2 -> L3 -> L4 -> L2", ["L1", "L2", "L3", "L4"], 1, 1, 1),
        (
            "L1 -> ... -> L6 -> L3",
            ["L1", "L2", "L3", "L4", "L5", "L6"],
            2,
            2,
            2,
        ),
        ("A -> A", ["A"], 0, 0, 0),
        ("A -> B -> C -> D -> A", ["A", "B", "C", "D"], 0, 0, 0),
        ("four slots, one label", ["weekend-primary"] * 4, 1, 1, 1),
    ]

    for wiring, labels, loop_to, entrance_index, hops in CASES:
        slots = build_rota(labels, loop_to)
        result = find_escalation_loop(slots[0])
        assert result is not None, f"{wiring}: this rota does loop"
        entrance, reported = result
        assert entrance is slots[entrance_index], f"{wiring}: wrong slot"
        assert reported == hops, f"{wiring}: got {reported} hops, wanted {hops}"
        print(f"{wiring:<28} entrance {entrance.slot}, {reported} hop(s) in front")

    TERMINATING = [
        ("L1 -> L2 -> L3 -> None", ["L1", "L2", "L3"]),
        ("A -> None", ["A"]),
        ("(no rota at all)", []),
        ("dup -> dup -> dup -> None", ["dup", "dup", "dup"]),
    ]

    for wiring, labels in TERMINATING:
        slots = build_rota(labels, None)
        start = slots[0] if slots else None
        assert find_escalation_loop(start) is None, f"{wiring}: no loop here"
        print(f"{wiring:<28} no loop")

    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-04-fast-slow-pointers-and-mock-1/exercises/exercise-02-escalation-loop.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `find_escalation_loop(start)` returns a pair of `(entrance slot, hops)`, or
   `None`. It never returns `(None, 0)`.
2. The entrance is the **first slot inside the loop**, not the last slot before
   it and not the slot where the two pointers met.
3. `hops` counts escalation steps from `start` to the entrance, so a start slot
   that is already inside the loop gives `0`.
4. A terminating rota returns `None`, and `find_escalation_loop(None)` returns
   `None` without raising.
5. There is **no branch** for "the start is already in the loop". The second
   phase produces `0` on its own. If you wrote one, delete it and prove to
   yourself the answer is unchanged.
6. Slots are compared with `is`, never by `slot` label.
7. Fixed memory: three pointers and a counter. No `set`, no `dict`, no list.

## Constraints

- **Up to 200,000 slots, and the memory you use must not grow with that
  number.** The checker runs inside the pager daemon, which is given a few
  kilobytes of working memory per health check because it has to keep running
  while everything else on the box is on fire. Two hundred thousand slot
  objects in a `set` does not fit in that budget. As in Exercise 1, the reason
  the visited set loses is availability, not speed — it is the same O(n) time.

- **Slot labels are free text and repeat.** Two different rotations can both be
  labelled `weekend-primary`, because the label is what a human typed into a
  form. One of the checks builds a four-slot rota where *every* label is the
  same string, and the assertion compares by identity. A label-based solution
  reports the first slot as the entrance and is wrong.

- **The start slot may itself be inside the loop.** That is not an error and it
  must not be special-cased away. It is the shape you get when the whole rota
  is one closed ring, which is a real misconfiguration and not a rare one.

- **Every slot escalates to exactly one other slot, or to none.** One way out
  per slot is what makes "step twice" meaningful. A rota where a page fans out
  to three people at once is a different problem needing a different pattern.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python exercise-02-escalation-loop.py
L1 -> L2 -> L3 -> L4 -> L2   entrance L2, 1 hop(s) in front
L1 -> ... -> L6 -> L3        entrance L3, 2 hop(s) in front
A -> A                       entrance A, 0 hop(s) in front
A -> B -> C -> D -> A        entrance A, 0 hop(s) in front
four slots, one label        entrance weekend-primary, 1 hop(s) in front
L1 -> L2 -> L3 -> None       no loop
A -> None                    no loop
(no rota at all)             no loop
dup -> dup -> dup -> None    no loop
All checks passed.
```

Line two is the important one. In `L1 -> ... -> L6 -> L3` the pointers meet at
`L5`, which is on the track and is not the join. The answer is `L3` with two
hops in front of it. If your program prints `L5` there, you stopped after phase
one.

## Steps

1. **Frame.** Restate the ask. Say out loud that the entrance is the first slot
   *inside* the loop. Confirm the terminating case returns `None` rather than a
   pair holding `None`. Then predict, before writing anything, that `A -> A`
   will come out as zero hops with no special case — and write that prediction
   down so you can check it later.
2. **Research constraints.** Name the daemon's memory budget, name the repeated
   labels, and note the case where the start is already inside the loop.
3. **Assess options.** The visited set is honestly *easier* here: walk once
   putting each slot in a dictionary against its position, and the first repeat
   gives you both the entrance and the hop count with no lemma at all. Say that
   out loud. Then say why it loses: a few kilobytes of daemon memory.
4. **Make the solution, phase one.** Paste Exercise 1's detection loop. It is
   unchanged apart from the attribute name. Return `None` in the `else`.
5. **Make the solution, phase two.** Put `finder` at `start`, leave `slow`
   alone, walk both by one, count. Return the pair.
6. **Examine.** Trace `L1 -> L2 -> L3 -> L4 -> L5 -> L6 -> L3` by hand.
   Phase one: slow=L1, fast=L1. Turn 1: slow=L2, fast=L3. Turn 2: slow=L3,
   fast=L5. Turn 3: slow=L4, fast=L3. Turn 4: slow=L5, fast=L5 — they meet at
   **L5**.
   Phase two: finder=L1, slow=L5, hops=0. Step: finder=L2, slow=L6, hops=1.
   Step: finder=L3, slow=L3, hops=2. Same slot. Answer `(L3, 2)`.
   Say out loud that the meeting point and the entrance are different slots on
   this input. That single sentence is the thing being tested.
7. **Examine, cost.** Phase one runs at most `T + C` turns, phase two exactly
   `T`, and both are bounded by the number of slots — O(n) time. Three pointers
   and an integer — O(1) space. Best, average and worst are all the same.

## The Solution

```python
"""exercise-02-escalation-loop-solution.py — where does the paging loop start?

Phase 1 is Exercise 1's tortoise and hare: it lands both pointers on the
same slot somewhere inside the loop. Phase 2 restarts a third pointer at
the beginning and walks it alongside the slow one, one slot each, until
they collide. The collision is the loop's entrance, and the number of
steps it took is the hop count the platform team asked for.

The rotas are built in this file, so it runs on its own with no imports.

The self-checks at the bottom print one line per rota, then
"All checks passed."
"""

from __future__ import annotations


class Rota:
    """One on-call slot. It escalates to exactly one other slot, or to none."""

    def __init__(self, slot: str, escalates_to: "Rota | None" = None) -> None:
        self.slot = slot
        self.escalates_to = escalates_to


def build_rota(labels: list[str], loop_to: int | None = None) -> list[Rota]:
    """Wire a rota from a list of labels and hand back every slot.

    Args:
        labels: One label per slot, in escalation order. Labels may repeat.
        loop_to: Index the last slot escalates back to, or None for a rota
            that reaches the top and stops.

    Returns:
        The slots, in order. Empty when `labels` is empty. The caller reads
        `slots[0]` for the starting slot and uses the rest to check answers
        by identity rather than by label.
    """
    slots = [Rota(label) for label in labels]
    for earlier, later in zip(slots, slots[1:]):
        earlier.escalates_to = later
    if slots and loop_to is not None:
        slots[-1].escalates_to = slots[loop_to]
    return slots


def find_escalation_loop(start: Rota | None) -> tuple[Rota, int] | None:
    """Return the loop's entrance and how many hops sit in front of it.

    Args:
        start: The slot a page begins at, or None for no rota at all.

    Returns:
        A pair of (entrance slot, hops from `start` to it), or None when the
        rota terminates and the page reaches a director.
    """
    slow = start
    fast = start
    while fast is not None and fast.escalates_to is not None:
        slow = slow.escalates_to
        fast = fast.escalates_to.escalates_to
        if slow is fast:
            break
    else:
        return None

    finder = start
    hops = 0
    while finder is not slow:
        finder = finder.escalates_to
        slow = slow.escalates_to
        hops += 1
    return finder, hops


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        ("L1 -> L2 -> L3 -> L4 -> L2", ["L1", "L2", "L3", "L4"], 1, 1, 1),
        (
            "L1 -> ... -> L6 -> L3",
            ["L1", "L2", "L3", "L4", "L5", "L6"],
            2,
            2,
            2,
        ),
        ("A -> A", ["A"], 0, 0, 0),
        ("A -> B -> C -> D -> A", ["A", "B", "C", "D"], 0, 0, 0),
        ("four slots, one label", ["weekend-primary"] * 4, 1, 1, 1),
    ]

    for wiring, labels, loop_to, entrance_index, hops in CASES:
        slots = build_rota(labels, loop_to)
        result = find_escalation_loop(slots[0])
        assert result is not None, f"{wiring}: this rota does loop"
        entrance, reported = result
        assert entrance is slots[entrance_index], f"{wiring}: wrong slot"
        assert reported == hops, f"{wiring}: got {reported} hops, wanted {hops}"
        print(f"{wiring:<28} entrance {entrance.slot}, {reported} hop(s) in front")

    TERMINATING = [
        ("L1 -> L2 -> L3 -> None", ["L1", "L2", "L3"]),
        ("A -> None", ["A"]),
        ("(no rota at all)", []),
        ("dup -> dup -> dup -> None", ["dup", "dup", "dup"]),
    ]

    for wiring, labels in TERMINATING:
        slots = build_rota(labels, None)
        start = slots[0] if slots else None
        assert find_escalation_loop(start) is None, f"{wiring}: no loop here"
        print(f"{wiring:<28} no loop")

    print("All checks passed.")
```

**The lemma, in the order you should say it.** Call `T` the number of slots
before the loop and `C` the number of slots in it.

When the pointers meet, slow has taken some number of steps — call it `k` — and
fast has taken `2k`, because it moved twice as often. They are standing on the
same slot, so the extra distance fast covered is a whole number of laps:
`2k - k = k`, and therefore `k` is a multiple of `C`.

Now think about where slow is. Its first `T` steps got it to the entrance. The
remaining `k - T` steps were taken on the track. So slow is sitting `k - T`
places past the entrance.

Walk slow `T` more places. It is now `(k - T) + T = k` places past the
entrance, and `k` is a whole number of laps, so it is *back on* the entrance.
Meanwhile a fresh pointer starting at the beginning also reaches the entrance
in exactly `T` steps. Both arrive at the same place after the same number of
steps, so if you walk them together they must collide there — and the number of
steps that took is `T`, which is exactly the hop count the platform team asked
for.

Read that aloud twice. In an interview it takes about forty seconds and it is
the whole reason this problem is asked.

**Phase two costs nothing extra.** The walk was going to happen anyway; adding
`hops += 1` to it turns a slot into a slot *and* a distance. That is why the
distance is in the contract: it proves you understood the lemma rather than
copying a two-loop shape, because a copied shape has no idea what `T` means.

**`slow` is not reset, and `finder` is.** This is the line people get backwards.
Slow stays exactly where it stopped, `k - T` past the entrance. Only `finder`
goes back to the beginning. If you reset both, they are equal on the first
comparison and you return the start slot with zero hops for every rota in the
world.

**The zero case falls out, as predicted.** For `A -> A`, phase one meets on its
first turn with slow on `A`. Phase two compares `finder` — also `A` — against
`slow`, finds them equal before the body ever runs, and returns `(A, 0)`. No
branch fired. That is the prediction from Frame, checked in Examine, and
checking a prediction you wrote down earlier is a much stronger signal than
getting the right answer by luck.

**Phase two must never run on a rota that terminates.** If phase one ended by
its guard, `slow` is not on any loop and the second walk marches off the end of
the rota and crashes. The `else` returning `None` is what prevents it, and it
is placed before phase two rather than after it for that reason.

## Run it

Copy the worked answer on this page into `exercise-02-escalation-loop.py` and run it:

```bash
python exercise-02-escalation-loop.py
```

It is the same program you are writing, under a name that will not collide with
your own `exercise-02-escalation-loop.py`.

To grade your own file against the week's larger cases:

```bash
C2_WEEK04_SOLUTIONS=exercise-02-escalation-loop pytest timed_runner.py -v -k escalation
```

See [`timed_runner.py`](./timed_runner.py) for the full case list.

## Common bugs to catch

- **Returning the meeting point.** No exception; just a wrong slot and a wrong
  number, on most inputs. `L1 -> ... -> L6 -> L3` gives `(L5, 4)` instead of
  `(L3, 2)`. Both halves are wrong at once, which is a useful tell: if the hop
  count is too big *and* the slot is too far along, you skipped phase two.

- **`AttributeError: 'NoneType' object has no attribute 'escalates_to'`.** You
  ran phase two on a rota with no loop:

  ```text
  Traceback (most recent call last):
      finder = finder.escalates_to; slow = slow.escalates_to
                                           ^^^^^^^^^^^^^^^^^
  AttributeError: 'NoneType' object has no attribute 'escalates_to'
  ```

  Phase one ended by its guard, so `slow` is sitting on the last slot with
  nothing after it. Return `None` in the `else` before phase two can start.

- **Resetting `slow` as well as `finder`.** Both are then at `start`, the first
  comparison is true, and the answer is always `(start, 0)`. It looks right on
  `A -> A` and on `A -> B -> C -> D -> A`, which is exactly what makes it
  dangerous — two of the five checks pass.

- **Counting the endpoint instead of the steps.** `hops` counts *moves*, so it
  is incremented inside the loop body, after both pointers advance. Starting it
  at `1`, or adding one at the end, makes `A -> A` report `1` when the start
  slot *is* the entrance.

- **`TypeError: cannot unpack non-iterable NoneType object`.** A caller wrote
  `entrance, hops = find_escalation_loop(start)` on a rota that does not loop:

  ```text
  Traceback (most recent call last):
      entrance, hops = find_escalation_loop(start)
      ^^^^^^^^^^^^^^
  TypeError: cannot unpack non-iterable NoneType object
  ```

  That crash is the contract working. Returning `(None, 0)` instead would have
  let the caller carry on and report a misconfiguration at slot `None`.

- **Comparing labels.** Four slots all labelled `weekend-primary` are four
  different slots. `finder is not slow` is right; `finder.slot != slow.slot`
  stops on the first one and returns zero hops.

## Under the hood

<details>
<summary>Under the hood — the same lemma written with modular arithmetic, and what happens at other speeds</summary>

**The one-line version.** Slow is at position `k - T` around a ring of length
`C`, and `k ≡ 0 (mod C)`, so slow is at `-T (mod C)` — that is, `T` short of
the entrance, going forwards. A pointer at the start is also `T` short of the
entrance. Same distance, same speed, therefore they arrive together. Everything
above is that sentence unpacked for someone meeting it the first time.

**Why `k` is the *first* multiple of `C`, and why it does not matter.** In fact
`k` is the smallest multiple of `C` that is at least `T`, but the proof never
uses which multiple it is — only that it is one. That is worth noticing,
because candidates sometimes try to compute `n` in `k = nC` and get stuck. You
never need it.

**Speeds other than 1 and 2 break phase two.** With fast at three times slow,
the meeting satisfies `3k - k = 2k ≡ 0 (mod C)`, so `2k` is a multiple of `C`
but `k` need not be — and the walk-from-the-start trick fails. This is the real
reason the ratio is fixed at two, and it is a good answer to "could you use a
different speed?": *for detection yes, for the entrance no.*

**The dictionary version, written out, so you know what you rejected.**

```python
def find_with_a_dictionary(start):
    seen = {}
    here, steps = start, 0
    while here is not None:
        if id(here) in seen:
            return here, seen[id(here)]
        seen[id(here)] = steps
        here, steps = here.escalates_to, steps + 1
    return None
```

Nine lines, no lemma, same O(n) time, and it hands back the hop count as the
stored position. It is genuinely the better choice on a server. Being able to
write it and *then* say why the daemon cannot run it is a stronger answer than
pretending Floyd's is better in every way.

Note `id(here)` rather than the slot itself: `Rota` has no `__hash__` problem
here, but keying by identity is the habit that keeps repeated labels from
merging two slots into one dictionary entry.

</details>

## Acceptance checklist

- [ ] `python exercise-02-escalation-loop.py` prints nine lines and then `All checks passed.`
- [ ] Every line matches the Expected output character for character.
- [ ] `slow` is not re-initialised at the start of phase two.
- [ ] The terminating case returns `None` **before** phase two runs.
- [ ] There is no branch for "the start is inside the loop".
- [ ] Slots are compared with `is`; nothing compares `slot` labels.
- [ ] You can say the lemma out loud in under a minute, without notes.
- [ ] A FRAME write-up sits at `frame-writeups/c2-week-04/exercise-02-escalation-loop.md`
      with a recording of at least 15 minutes, and it traces
      `L1 -> ... -> L6 -> L3` showing the meeting point is not the entrance.

## Stretch

- **Report the loop's length too, so the platform team gets the whole shape.**
  Bolt Exercise 1's counting walk onto the end of phase two:

  ```python
  def escalation_shape(start: Rota | None) -> tuple[Rota, int, int] | None:
      """Return (entrance, hops in front of it, slots in the loop)."""
      found = find_escalation_loop(start)
      if found is None:
          return None
      entrance, hops = found
      walker, size = entrance.escalates_to, 1
      while walker is not entrance:
          walker, size = walker.escalates_to, size + 1
      return entrance, hops, size
  ```

  ```text
  L1 -> L2 -> L3 -> L4 -> L2   entrance L2, 1 hop, loop of 3
  L1 -> ... -> L6 -> L3        entrance L3, 2 hops, loop of 4
  ```

- **Name the slot that closes the loop.** The team needs to change exactly one
  escalation rule, and it is not the entrance's — it is the rule belonging to
  the slot that escalates *into* the entrance. Walk the loop until the next
  slot is the entrance and return that one.

  ```text
  L1 -> L2 -> L3 -> L4 -> L2   fix the rule on L4
  ```

- **Write the dictionary version from Under the hood and time both** on a rota
  of 200,000 slots with the loop at the very end. Then measure the memory with
  `tracemalloc`. Seeing the two numbers side by side — same milliseconds, wildly
  different bytes — is what makes the space argument stop being an abstraction.
When the lemma sounds natural out loud, move on to
[Exercise 3 — The Mid-Roll Break](./exercise-03-midroll-break.md).
