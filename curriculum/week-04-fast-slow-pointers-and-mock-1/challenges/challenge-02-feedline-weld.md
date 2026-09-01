# Challenge 2 — The Feed-Line Weld

> **Topic:** turning a problem with no loop into a problem with one, then using the week's cycle machinery on it
> **Lecture:** [01 — Floyd's Tortoise and Hare](../lecture-notes/01-floyds-tortoise-and-hare.md), §3 and §4
> **Difficulty:** Medium to Hard
> **Target time:** 90 minutes, and a recording of at least 30 minutes
> **Why this one:** every other page this week hands you a loop. This one hands you two chains with no loop anywhere, and the move is to *build* a loop on purpose so that everything you already know applies. Recognising that a problem can be converted into one you have already solved is the most transferable skill in the course.

## The Brief

A food plant has two intake conveyors. Line A comes from the cold store; line B
comes from the packing hall. Somewhere downstream the two lines are **welded**
together, and from the weld onwards there is a single shared discharge run that
both lines feed into.

The conveyors are chains of pans. Each pan feeds exactly one other pan, or —
at the very end of the discharge run — nothing at all.

Nobody has an up-to-date drawing of the plant. What the engineers have is the
first pan of each line and the ability to walk forward. What they need is:

- **the weld** — the first pan that both lines pass over, and
- **two lead-in counts** — how many pans line A passes over before the weld,
  and how many line B passes over before it.

The lead-ins are what the maintenance rota is built from, so they matter as
much as the weld itself.

Return the three together. Return `None` if the two lines never meet — the
plant has two independent discharge runs and there is nothing to find.

**Here is the difficulty.** There is no loop anywhere in this plant. Both lines
terminate. So none of this week's machinery applies… unless you make it apply.

Think about what you would do with a garden hose and a second hose. If you want
to know where they join, and you can only walk forwards along a hose, you tie
the far end of the first one onto the near end of the second. Now the shared
part is a **ring**: walk long enough and you come back round. And the first pan
of that ring — the entrance, from
[Exercise 2](../exercises/exercise-02-escalation-loop.md) — is exactly the
weld.

Then you untie the knot, because a diagnostic that leaves the plant rewired is
not a diagnostic. It is a second fault.

## Starter

Create `challenge-02-feedline-weld.py` and paste this in. Fill in every `TODO`.

```python
"""challenge-02-feedline-weld.py — where do two feed lines join?

Fill in every TODO, then run the file. The self-checks at the bottom print
one line per plant and then "All checks passed." when the module is right.
"""

from __future__ import annotations


class Pan:
    """One pan on a conveyor. It feeds exactly one other pan, or none."""

    def __init__(self, tag: str, feeds_to: "Pan | None" = None) -> None:
        self.tag = tag
        self.feeds_to = feeds_to


def build_lines(
    lead_a: list[str], lead_b: list[str], shared: list[str]
) -> tuple[Pan | None, Pan | None, list[Pan]]:
    """Wire two feed lines that join onto one shared discharge run.

    Args:
        lead_a: Tags for the pans only line A passes over, in order.
        lead_b: Tags for the pans only line B passes over, in order.
        shared: Tags for the pans both lines pass over. Empty means the two
            lines never meet.

    Returns:
        A triple of (first pan of A, first pan of B, the shared pans). Either
        head is None when that line has no pans at all.
    """
    pans_a = [Pan(tag) for tag in lead_a]
    pans_b = [Pan(tag) for tag in lead_b]
    pans_shared = [Pan(tag) for tag in shared]

    for run in (pans_a, pans_b, pans_shared):
        for earlier, later in zip(run, run[1:]):
            earlier.feeds_to = later
    if pans_shared:
        if pans_a:
            pans_a[-1].feeds_to = pans_shared[0]
        if pans_b:
            pans_b[-1].feeds_to = pans_shared[0]

    head_a = (pans_a or pans_shared or [None])[0]
    head_b = (pans_b or pans_shared or [None])[0]
    return head_a, head_b, pans_shared


def _last_pan(first: Pan) -> Pan:
    """Return the pan at the end of a run that is known to terminate."""
    # TODO 1: walk until `feeds_to` is None and hand that pan back.
    ...


def _ring_entrance(first: Pan) -> tuple[Pan, int] | None:
    """Return the first pan of the ring reachable from `first`, and its lead.

    Args:
        first: Where to start walking.

    Returns:
        A pair of (first pan of the ring, pans in front of it), or None when
        the run has no ring and simply ends.
    """
    # TODO 2: this is Exercise 2 with `feeds_to` instead of `escalates_to`.
    #         Copy it. Do not rewrite it from memory.
    ...


def find_weld(line_a: Pan | None, line_b: Pan | None) -> tuple[Pan, int, int] | None:
    """Return the weld the two feed lines share, and each line's lead-in.

    Args:
        line_a: The first pan of one feed line, or None for no line.
        line_b: The first pan of the other feed line, or None for no line.

    Returns:
        A triple of (weld pan, pans in front of it on line A, pans in front
        of it on line B), or None when the two lines never meet. Both lines
        are left wired exactly as they were found.
    """
    # TODO 3: no line means no weld.
    # TODO 4: tie the end of line A onto the head of line B. The shared run
    #         is now a ring.
    # TODO 5: find the ring's entrance, then UNTIE the knot before you do
    #         anything else with the answer.
    # TODO 6: the entrance is the weld and the ring's lead is line A's
    #         lead-in. Walk line B to the weld to count line B's.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        ("A:2 B:3 shared:2", ["a1", "a2"], ["b1", "b2", "b3"], ["w1", "w2"], (2, 3)),
        ("A:0 B:2 shared:1", [], ["b1", "b2"], ["w1"], (0, 2)),
        ("A:1 B:0 shared:3", ["a1"], [], ["w1", "w2", "w3"], (1, 0)),
        ("same head, shared:4", [], [], ["w1", "w2", "w3", "w4"], (0, 0)),
        ("A:3 B:1 shared:1", ["P", "P", "P"], ["P"], ["P"], (3, 1)),
    ]

    for label, lead_a, lead_b, shared, expected in CASES:
        head_a, head_b, pans_shared = build_lines(lead_a, lead_b, shared)
        result = find_weld(head_a, head_b)
        assert result is not None, f"{label}: these lines do meet"
        weld, found_a, found_b = result
        assert weld is pans_shared[0], f"{label}: wrong pan, compare by identity"
        assert (found_a, found_b) == expected, f"{label}: got {(found_a, found_b)}"
        assert _last_pan(head_a) is pans_shared[-1], f"{label}: line A was left tied"
        print(f"{label:<20} weld {weld.tag}, lead-ins {found_a} and {found_b}")

    SEPARATE = [
        ("two runs, no weld", ["a1", "a2"], ["b1", "b2", "b3"]),
        ("one pan each", ["a1"], ["b1"]),
    ]

    for label, lead_a, lead_b in SEPARATE:
        head_a, head_b, _ = build_lines(lead_a, lead_b, [])
        assert find_weld(head_a, head_b) is None, f"{label}: no weld here"
        assert _last_pan(head_a).tag == lead_a[-1], f"{label}: line A was left tied"
        print(f"{label:<20} no weld")

    assert find_weld(None, build_lines([], ["b1"], [])[1]) is None
    print(f"{'no line A at all':<20} no weld")

    print("All checks passed.")
```

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-04-fast-slow-pointers-and-mock-1/challenges/challenge-02-feedline-weld.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `find_weld(line_a, line_b)` returns a triple of
   `(weld pan, line A's lead-in, line B's lead-in)`, or `None`.
2. The weld is the **first** shared pan, not any later one and not the end of
   the discharge run.
3. Two lines that start at the same pan give lead-ins of `0` and `0`.
4. Either head being `None` gives `None`, without raising.
5. **Both lines are left wired exactly as they were found.** The check list
   asserts it after every case, including the ones that return `None`.
6. Pans are compared with `is`, never by `tag`.
7. Fixed memory: a handful of pan variables and counters. No `set`, no `dict`,
   no list of pans.
8. Every function keeps its type hints and its docstring.

## Constraints

- **Up to 100,000 pans per line, and the memory you use must not grow with that
  number.** The probe runs on the plant's programmable controller alongside the
  code that is actually driving the motors, and it gets a few kilobytes. The
  obvious solution — walk line A putting every pan into a set, then walk line B
  until you hit one that is already in it — is O(n) time and O(n) space, and it
  is genuinely the clearest program you could write here. It is rejected on
  memory alone. Say that out loud. It is the fourth time this week and the
  sentence should be automatic by now.

- **Neither line contains a loop when you receive it.** Both terminate. That is
  what makes this a composition problem rather than a detection problem — and
  it is why you have to make a loop yourself before the week's tools apply.

- **The plant must be left exactly as it was found, on every path out of the
  function.** This is not a nicety. The knot you tie joins the end of the
  discharge run back onto line B's first pan, and a controller that starts a
  motor while that knot is tied will run pans round in circles until something
  jams. Leaving it tied is a worse bug than getting the wrong answer, because
  the wrong answer is visible and the knot is not.

- **Pan tags repeat freely.** Tags are stencilled per section and sections
  repeat across the plant. One of the checks builds a plant where every single
  pan is tagged `P`, and the assertion compares by identity.

- **Lead-ins can be zero on either side, or both.** A line whose first pan is
  already the weld is a normal plant, not an edge case to guard against.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python challenge-02-feedline-weld-solution.py
A:2 B:3 shared:2     weld w1, lead-ins 2 and 3
A:0 B:2 shared:1     weld w1, lead-ins 0 and 2
A:1 B:0 shared:3     weld w1, lead-ins 1 and 0
same head, shared:4  weld w1, lead-ins 0 and 0
A:3 B:1 shared:1     weld P, lead-ins 3 and 1
two runs, no weld    no weld
one pan each         no weld
no line A at all     no weld
All checks passed.
```

The `A:3 B:1 shared:1` line is the one that punishes tag comparison: every pan
in that plant is tagged `P`, and the answer is still `P` with lead-ins 3 and 1.
The two `no weld` lines matter just as much — each is followed by an assertion
that line A still ends where it used to.

## Steps

1. **Frame.** Restate. Say out loud that there is no loop anywhere in the
   input. Confirm the return shape: a triple, or `None`, never a triple
   containing `None`. Confirm that both lead-ins can be zero. Confirm that
   the plant must come back unmodified — and write that down, because it is the
   requirement people satisfy on the happy path and forget on the `None` path.
2. **Research constraints.** Name the controller's memory budget and what it
   rejects. Name the repeated tags. Name the restore requirement as a *safety*
   requirement rather than a tidiness one.
3. **Assess options, and this is the graded step.** Three candidates, and you
   should say all three:
   - **The visited set.** Walk A into a set, walk B until a pan is in it.
     Clearest program, O(n) memory, rejected.
   - **Measure and align.** Count both lines, then start the longer one ahead
     by the difference and walk both together until they meet. O(1) memory and
     it works. It is a perfectly good answer and worth naming.
   - **Tie a knot and use Floyd's.** Join A's end to B's head; the shared run
     becomes a ring whose entrance is the weld. O(1) memory, and it reuses
     machinery you already have.

   Then say why the third one is the one this page teaches: it is the *reduction*
   move — converting an unfamiliar problem into one already solved — and that
   move transfers to problems where the align-and-walk trick does not exist.
4. **Make the solution, the helpers first.** `_last_pan` is four lines.
   `_ring_entrance` is Exercise 2 with one attribute renamed — copy it rather
   than retyping it, and say out loud that you are copying it.
5. **Make the solution, the knot.** Tie, find, untie, *then* look at what you
   found. Put the untie on the line immediately after the find, before any
   branch, so there is no path out of the function that skips it.
6. **Make the solution, line B's lead-in.** The ring walk gave you line A's for
   free. Line B's is a plain count from `line_b` to the weld.
7. **Examine, the ordinary case.** Trace `A:2 B:3 shared:2`. Line A is
   `a1 a2 w1 w2`, line B is `b1 b2 b3 w1 w2`. Tie `w2` onto `b1`. Now walking
   from `a1` gives `a1 a2 w1 w2 b1 b2 b3 w1 …` — a ring of
   `w1 w2 b1 b2 b3` with a lead-in of two. The entrance is `w1`, the lead is 2,
   which is line A's lead-in. Untie. Walk B: `b1 b2 b3` then `w1`, so 3. Answer
   `(w1, 2, 3)`. ✓
8. **Examine, the same-head case.** Both lines start at `w1` and there are no
   lead-in pans at all. `_last_pan(w1)` is `w4`, and tying `w4` onto `w1` makes
   the whole plant one ring. Its entrance is `w1`, its lead is `0`. Untie. Line
   B's count from `w1` to `w1` is `0`. Answer `(w1, 0, 0)`. ✓ No special case
   fired.
9. **Examine, the no-weld case.** Two separate runs. Tying A's end to B's head
   makes one long run that still terminates, so `_ring_entrance` returns `None`.
   Untie, return `None`. ✓ Then check the plant by hand: does A still end where
   it did?
10. **Examine, cost.** O(n) time: one walk to the end of A, at most two walks
    for the ring machinery, one walk down B. O(1) space: five pans and two
    counters.

## The Solution

```python
"""challenge-02-feedline-weld-solution.py — where do two feed lines join?

There is no loop anywhere in this problem, which is exactly why it is hard.
The move is to *make* one: tie the end of line A onto the head of line B and
the shared run becomes a ring. Now the week's cycle machinery applies
unchanged — Floyd's tortoise and hare finds a pan inside the ring, and the
entrance walk turns that into the ring's first pan, which is the weld.

Then untie the knot, because a diagnostic that leaves the plant rewired is
not a diagnostic.

The feed lines are built in this file, so it runs on its own with no imports.

The self-checks at the bottom print one line per plant, then
"All checks passed."
"""

from __future__ import annotations


class Pan:
    """One pan on a conveyor. It feeds exactly one other pan, or none."""

    def __init__(self, tag: str, feeds_to: "Pan | None" = None) -> None:
        self.tag = tag
        self.feeds_to = feeds_to


def build_lines(
    lead_a: list[str], lead_b: list[str], shared: list[str]
) -> tuple[Pan | None, Pan | None, list[Pan]]:
    """Wire two feed lines that join onto one shared discharge run.

    Args:
        lead_a: Tags for the pans only line A passes over, in order.
        lead_b: Tags for the pans only line B passes over, in order.
        shared: Tags for the pans both lines pass over. Empty means the two
            lines never meet.

    Returns:
        A triple of (first pan of A, first pan of B, the shared pans). Either
        head is None when that line has no pans at all.
    """
    pans_a = [Pan(tag) for tag in lead_a]
    pans_b = [Pan(tag) for tag in lead_b]
    pans_shared = [Pan(tag) for tag in shared]

    for run in (pans_a, pans_b, pans_shared):
        for earlier, later in zip(run, run[1:]):
            earlier.feeds_to = later
    if pans_shared:
        if pans_a:
            pans_a[-1].feeds_to = pans_shared[0]
        if pans_b:
            pans_b[-1].feeds_to = pans_shared[0]

    head_a = (pans_a or pans_shared or [None])[0]
    head_b = (pans_b or pans_shared or [None])[0]
    return head_a, head_b, pans_shared


def _last_pan(first: Pan) -> Pan:
    """Return the pan at the end of a run that is known to terminate."""
    last = first
    while last.feeds_to is not None:
        last = last.feeds_to
    return last


def _ring_entrance(first: Pan) -> tuple[Pan, int] | None:
    """Return the first pan of the ring reachable from `first`, and its lead.

    Args:
        first: Where to start walking.

    Returns:
        A pair of (first pan of the ring, pans in front of it), or None when
        the run has no ring and simply ends.
    """
    slow = first
    fast = first
    while fast is not None and fast.feeds_to is not None:
        slow = slow.feeds_to
        fast = fast.feeds_to.feeds_to
        if slow is fast:
            break
    else:
        return None

    finder = first
    lead = 0
    while finder is not slow:
        finder = finder.feeds_to
        slow = slow.feeds_to
        lead += 1
    return finder, lead


def find_weld(line_a: Pan | None, line_b: Pan | None) -> tuple[Pan, int, int] | None:
    """Return the weld the two feed lines share, and each line's lead-in.

    Args:
        line_a: The first pan of one feed line, or None for no line.
        line_b: The first pan of the other feed line, or None for no line.

    Returns:
        A triple of (weld pan, pans in front of it on line A, pans in front
        of it on line B), or None when the two lines never meet. Both lines
        are left wired exactly as they were found.
    """
    if line_a is None or line_b is None:
        return None

    tail_a = _last_pan(line_a)
    tail_a.feeds_to = line_b  # Tie the knot: the shared run becomes a ring.
    found = _ring_entrance(line_a)
    tail_a.feeds_to = None  # Untie it before doing anything else.

    if found is None:
        return None
    weld, lead_a = found

    lead_b = 0
    pan = line_b
    while pan is not weld:
        pan = pan.feeds_to
        lead_b += 1
    return weld, lead_a, lead_b


# ---- Self-check ----
if __name__ == "__main__":
    CASES = [
        ("A:2 B:3 shared:2", ["a1", "a2"], ["b1", "b2", "b3"], ["w1", "w2"], (2, 3)),
        ("A:0 B:2 shared:1", [], ["b1", "b2"], ["w1"], (0, 2)),
        ("A:1 B:0 shared:3", ["a1"], [], ["w1", "w2", "w3"], (1, 0)),
        ("same head, shared:4", [], [], ["w1", "w2", "w3", "w4"], (0, 0)),
        ("A:3 B:1 shared:1", ["P", "P", "P"], ["P"], ["P"], (3, 1)),
    ]

    for label, lead_a, lead_b, shared, expected in CASES:
        head_a, head_b, pans_shared = build_lines(lead_a, lead_b, shared)
        result = find_weld(head_a, head_b)
        assert result is not None, f"{label}: these lines do meet"
        weld, found_a, found_b = result
        assert weld is pans_shared[0], f"{label}: wrong pan, compare by identity"
        assert (found_a, found_b) == expected, f"{label}: got {(found_a, found_b)}"
        assert _last_pan(head_a) is pans_shared[-1], f"{label}: line A was left tied"
        print(f"{label:<20} weld {weld.tag}, lead-ins {found_a} and {found_b}")

    SEPARATE = [
        ("two runs, no weld", ["a1", "a2"], ["b1", "b2", "b3"]),
        ("one pan each", ["a1"], ["b1"]),
    ]

    for label, lead_a, lead_b in SEPARATE:
        head_a, head_b, _ = build_lines(lead_a, lead_b, [])
        assert find_weld(head_a, head_b) is None, f"{label}: no weld here"
        assert _last_pan(head_a).tag == lead_a[-1], f"{label}: line A was left tied"
        print(f"{label:<20} no weld")

    assert find_weld(None, build_lines([], ["b1"], [])[1]) is None
    print(f"{'no line A at all':<20} no weld")

    print("All checks passed.")
```

**The reduction is the whole idea, and it deserves a sentence you can say out
loud.** *There is no ring, so I will make one; the shared run is exactly the
part that becomes a ring; therefore the ring's first pan is exactly the weld.*
Everything after that is machinery from Exercises 1 and 2, unchanged.

**Why tying A's end onto B's head produces exactly the right ring.** Follow the
pans. Starting at line A's first pan you walk A's lead-in, then the shared run
to its very end. That end is now tied to line B's first pan, so you continue
into B's lead-in — and B's lead-in ends by feeding into the shared run's first
pan, which is the weld. You are back somewhere you have been. The ring is
therefore *the shared run followed by line B's lead-in*, and the first pan of
that ring is the first shared pan. That is the weld, by definition.

**And the lead-in comes free.** The ring's lead-in — the pans in front of the
ring, counted from where you started walking — is line A's lead-in, because
that is precisely the part of the walk before the first shared pan. Exercise
2's phase two counts it while it is already walking, so you get the weld and
one of the two numbers from a single call.

**Line B's count is a plain walk, and it has to be.** The knot destroyed the
symmetry: A's lead-in came out of the ring machinery because A is where you
started walking. B's did not, so you count it the ordinary way once the knot is
untied. Four lines, no cleverness, and trying to be clever here is how people
end up counting from inside the ring.

**Untie before you branch.**

```python
    tail_a.feeds_to = line_b  # Tie the knot: the shared run becomes a ring.
    found = _ring_entrance(line_a)
    tail_a.feeds_to = None  # Untie it before doing anything else.
```

Three lines in a row, with nothing between them that can return early or raise.
That is deliberate. The obvious mistake is to write `if found is None: return
None` *before* the untie, which leaves the plant knotted on exactly the input
where nothing was found — the case you are least likely to test by hand.

Nothing between the tie and the untie can raise, so `try` / `finally` is not
needed here. If the code between them ever grew to something that could raise —
a lookup, a division, a call into someone else's module — `finally` would
become the right answer, because the knot must come out whatever happens. Say
that distinction out loud rather than reaching for `finally` by reflex; knowing
*why* you do not need it is a stronger answer than using it anyway.

**`_last_pan` walks a run that is known to terminate, and the docstring says
so.** If either line already contained a loop, that helper would never return.
The constraint rules it out, and writing the assumption into the docstring is
how the next person finds out.

**Nothing here grows with the plant.** `tail_a`, `weld`, `pan`, plus whatever
`_ring_entrance` holds, plus two counters. The controller's few kilobytes are
honoured.

## Download and run

Download
[challenge-02-feedline-weld-solution.py](./challenge-02-feedline-weld-solution.py)
and run it:

```bash
python challenge-02-feedline-weld-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `challenge-02-feedline-weld.py`.

To grade your own file against the week's larger cases:

```bash
C2_WEEK04_SOLUTIONS=challenge-02-feedline-weld pytest ../exercises/timed_runner.py -v -k weld
```

See [`timed_runner.py`](../exercises/timed_runner.py) for the full case list.

## Common bugs to catch

- **Leaving the knot tied on the `None` path.** You returned before untying.
  The self-check catches it, because `_last_pan` on a knotted plant never
  finishes and the harness stops at its timeout — or, if you wrote your own
  walk with a guard, you get this:

  ```text
  AssertionError: the diagnostic left the plant rewired
  ```

  Untie on the line straight after the find, before any `if`.

- **Returning the end of the discharge run instead of the weld.** You used
  Exercise 1's detection and stopped at the meeting point rather than running
  Exercise 2's entrance phase. The meeting point is somewhere inside the ring
  and is almost never its first pan.

- **`AttributeError: 'NoneType' object has no attribute 'feeds_to'`.** Two
  likely causes. Either `_last_pan` was handed a `None` head, or the ring
  machinery's phase two ran on a plant with no ring:

  ```text
  Traceback (most recent call last):
      finder = finder.feeds_to; slow = slow.feeds_to
                                       ^^^^^^^^^^^^^
  AttributeError: 'NoneType' object has no attribute 'feeds_to'
  ```

  Check that `_ring_entrance` returns `None` in its `else` before phase two,
  and that `find_weld` rejects a `None` head first thing.

- **Counting line B from the wrong end.** `lead_b` counts pans strictly in
  front of the weld, so it stops the moment `pan is weld` and never counts the
  weld itself. The `same head` case is the one that catches an off-by-one: both
  answers must be `0`.

- **Comparing tags.** In the `A:3 B:1 shared:1` plant every pan is tagged `P`,
  so `pan.tag == weld.tag` is true on the very first pan and line B's lead-in
  comes back `0` instead of `1`. Identity is the only thing that means anything
  here — the same rule as Exercises 1, 2, 3 and 5.

- **Tying B's end to A's head instead.** It also produces a ring, and its
  entrance is also the weld — but the lead-in that falls out is now line B's,
  not line A's, and if you kept the same variable names you have silently
  swapped the two numbers in the answer. Either direction is fine as long as
  you know which one you tied.

- **`AssertionError: line A was left tied`.** The check list asserts, after
  every single case, that line A still ends at the discharge run's last pan.
  This is the assertion that catches the knot you forgot, and it fires on the
  case *after* the one that caused it — which is a useful thing to have seen
  once, because that is how state bugs behave in real code.

## Under the hood

<details>
<summary>Under the hood — the align-and-walk alternative, and why two chains can never cross more than once</summary>

**The other O(1)-space answer, written out.** Count both lines, start the
longer one ahead by the difference, then walk both in lockstep until they land
on the same pan:

```python
def find_weld_by_aligning(line_a, line_b):
    """The alternative: measure both runs, then walk them in step."""
    def length(first):
        count, pan = 0, first
        while pan is not None:
            count, pan = count + 1, pan.feeds_to
        return count

    len_a, len_b = length(line_a), length(line_b)
    walk_a, walk_b = line_a, line_b
    lead_a = lead_b = 0
    for _ in range(len_a - len_b if len_a > len_b else 0):
        walk_a, lead_a = walk_a.feeds_to, lead_a + 1
    for _ in range(len_b - len_a if len_b > len_a else 0):
        walk_b, lead_b = walk_b.feeds_to, lead_b + 1
    while walk_a is not walk_b:
        walk_a, walk_b = walk_a.feeds_to, walk_b.feeds_to
        lead_a, lead_b = lead_a + 1, lead_b + 1
    return None if walk_a is None else (walk_a, lead_a, lead_b)
```

It is the same O(n) time and O(1) space, it never modifies the plant, and on a
plant where modification is forbidden outright it is the answer you must give.
So why does this page teach the knot? Because the knot is the *reduction*
move — "make this into a problem I have already solved" — and that generalises
to problems where no clever alignment exists. Know both. In an interview, name
both and say which the constraints prefer.

There is also a third answer, the one people show off with: walk both pointers
forward, and whenever one falls off the end, restart it at the *other* line's
head. Both pointers then travel `len_a + len_b` pans in total and must arrive
at the weld together. It is beautiful and it does not produce the two lead-in
counts without extra bookkeeping, which is exactly why this page asks for them.

**Two terminating chains can meet at most once, and that is why "the weld" is
well defined.** Each pan feeds exactly one other pan. So the moment the two
lines share a single pan, they share every pan after it — there is no way for
them to diverge again, because divergence would need a pan with two outgoing
edges. That one-way-out property, the same one that makes Floyd's legal all
week, is also what makes the question have a unique answer. Say it out loud in
Frame; it is the sort of observation that reads as *understood the structure*.

**Why the ring is not just the shared run.** People expect the ring to be the
shared part, and it is not — it is the shared part *plus line B's lead-in*,
because the knot routes you back through B before you return to the weld. The
entrance is still the weld, which is all that matters, but if you try to read
line B's lead-in off the ring's *length* you will get `shared + lead_b` and be
confused. Measure line B by walking it.

**A real-world echo.** This is how you find where two versions of a file
diverged in a chain of revisions, and it is the same shape as finding the
lowest common ancestor of two nodes in a tree when every node knows only its
parent. Chains that merge and never split are common; the pattern is worth
recognising by shape rather than by story.

</details>

## Acceptance checklist

- [ ] `python challenge-02-feedline-weld.py` prints eight lines and then `All checks passed.`
- [ ] Every line matches the Expected output character for character.
- [ ] The untie happens immediately after the find, before any branch.
- [ ] Every case, including the `None` ones, leaves both lines wired as found.
- [ ] The `same head` plant returns lead-ins of `0` and `0`, with no special
      case written for it.
- [ ] Pans are compared with `is`; nothing compares `tag`.
- [ ] No `set`, no `dict`, no list of pans anywhere.
- [ ] Your write-up names all three candidate approaches from step 3 and says
      which the constraints choose.
- [ ] A FRAME write-up sits at `frame-writeups/c2-week-04/challenge-02-feedline-weld.md`
      with a recording of at least 30 minutes, and its Assess-options section
      says the word *reduction* out loud.

## Stretch

- **Write the align-and-walk version from Under the hood and check it agrees.**
  Run both against every case in the self-check and assert the answers match.
  Two independent implementations that agree on ten plants is a much stronger
  signal than one implementation that passes ten tests.

  ```text
  A:2 B:3 shared:2     knot (w1, 2, 3)   align (w1, 2, 3)
  same head, shared:4  knot (w1, 0, 0)   align (w1, 0, 0)
  two runs, no weld    knot None         align None
  ```

- **Report how many pans the shared run holds.** The engineers want it for a
  cleaning schedule. Once you have the weld it is a plain walk to the end:

  ```python
  def shared_run_length(weld: Pan) -> int:
      """Count the pans from the weld to the end of the discharge run."""
      count, pan = 0, weld
      while pan is not None:
          count, pan = count + 1, pan.feeds_to
      return count
  ```

  ```text
  A:2 B:3 shared:2     weld w1, shared run of 2
  same head, shared:4  weld w1, shared run of 4
  ```

- **Handle three intake lines.** Find the pan where all three meet, if there is
  one — and notice that two of them meeting says nothing about the third.
  Solving it as "weld A and B, then weld that result with C" is the right
  decomposition, and working out *why* that is correct, using the one-way-out
  property, is the real exercise.

**Practice elsewhere.** The same pattern appears as
[LeetCode 160 · Intersection of Two Linked Lists](https://leetcode.com/problems/intersection-of-two-linked-lists/)
if you want a judge to run against. That contract returns only the node, never
asks for the two lead-in counts, and explicitly forbids modifying the lists —
so the knot solution is not even legal there. Solve this one first, then go and
give the restart-at-the-other-head answer over there.

When both challenges pass, take the [quiz](../quiz.md), work the
[homework](../homework/README.md), and then ship the
[mini-project](../mini-project/README.md) — Mock Interview #1.
