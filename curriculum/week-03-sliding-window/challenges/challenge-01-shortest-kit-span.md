# Challenge 1 — The Shortest Kit Span

> **Topic:** the shrinking window with a frequency invariant, made fast by carrying one integer instead of comparing tables
> **Lecture:** [02 — The Shrinking and Growing Mechanics](../lecture-notes/02-the-shrinking-and-growing-mechanics.md)
> **Difficulty:** Hard
> **Target time:** 2 hours
> **Why this one:** the hardest common shape in the sliding-window family, and the one whose invariant takes longer to say than the code takes to write. Most people reach something that looks right. Far fewer can explain, in thirty seconds, *why a single integer is the correct state to carry* instead of a table comparison. That explanation is the discriminator, and it is what this page is really teaching.

## The Brief

A parts conveyor feeds an assembly cell. Components come past in a fixed order
and the line logs each one's part code — `"bolt"`, `"nut"`, `"washer"`,
`"clip"`, and so on.

A **kit** is defined by a **bill of materials**: a list of part codes, where
repeats mean "this many of that part". A bill of `["nut", "nut", "bolt"]` calls
for two nuts and one bolt. To build a kit, the operator stops the belt over a
**contiguous stretch** of conveyor and pulls out everything the bill asks for.

Two things about that stretch matter, and they are what make this problem
different from Exercise 3.

**Surplus is fine.** If the stretch holds three bolts and the bill wants one,
the extra two are simply left on the belt. They do not disqualify anything.

**Irrelevant parts are fine too.** If a `"clip"` sits in the middle of the
stretch and the bill never mentions clips, that is not a problem — but it *is*
a cost, because the clip is inside the stretch and so the stretch is longer
than it would otherwise be. That is the difference between a stretch that
**contains** the bill and one that **consists of** the bill. Exercise 3 wanted
the second. This wants the first.

Because surplus is allowed, the window is no longer a fixed width. It grows on
the right until the bill is covered, and then shrinks from the left as far as it
can while the bill is *still* covered — the shape from Exercise 4, with a table
in place of a running total.

**Your job.** Return the **shortest stretch of conveyor that contains the whole
bill**, counting duplicates, as `(start, length)`.

### The key insight: why a single integer is the right state

Here is the obvious way, and why it is not good enough.

Keep a frequency table for the window. At every shrink step, ask: does the
window's table cover the bill's table? That is a **multiset-containment
check**, and answering it means one probe per distinct code in the bill — up to
500 of them, by the catalogue bound below. The shrink loop can run up to `n`
times across the algorithm, so the whole thing is `O(500n)`, which is around
`2 x 10^8` dictionary probes on the larger inputs. Slow enough to matter. But
the real objection is not speed: it is that the question *"is the bill
covered?"* gets re-derived from scratch at every single step, when the answer
barely changes.

So maintain the answer instead of recomputing it. Track **how many distinct part
codes from the bill are currently satisfied inside the window**. Call that
integer `matched`, and let `distinct_wanted` be the number of distinct codes the
bill names. Then:

> **The invariant:** `matched == distinct_wanted` exactly when the window
> contains every code in the bill with at least the multiplicity the bill
> requires.

Now "is the bill covered?" is one integer comparison. And `matched` is cheap to
keep true: across a whole pass, each distinct code can push it up at most once
per time its count reaches the requirement and pull it down at most once per
time the count falls below, so the total number of updates is bounded by the
bill, not by the conveyor.

Two comparison operators carry the entire trick, and each is one character:

- Increment `matched` only when a code's window count becomes **exactly equal**
  to its requirement. Going from two bolts to three when the bill wants one
  must not increment again.
- Decrement `matched` only when a code's window count becomes **strictly less**
  than its requirement. Going from three bolts to two when the bill wants one
  must not decrement.

Get those two right and the rest is bookkeeping. Get either wrong and you will
have a solution that is correct on your first two test cases and wrong on the
third.

**The contract.** Ties on length go to the **largest** start — the belt runs
forward, so stopping later means less back-tracking. An empty bill returns
`(0, 0)`: nothing is required, so the empty stretch at the head of the belt
suffices. A bill no stretch can cover returns `None`. Those last two are
different answers to different questions, and telling them apart is part of the
problem.

## Starter

Create `challenge-01-shortest-kit-span.py` and paste this in. Fill in every
`TODO`.

```python
"""challenge-01-shortest-kit-span.py — the shortest kit span.

Find the shortest contiguous stretch of conveyor containing every part on the
bill, counting duplicates, and return where it is.

Fill in every TODO, then run the file. The self-checks at the bottom print
"All checks passed." when the module is correct.
"""

from collections import Counter


def shortest_kit_span(conveyor: list[str], bill: list[str]) -> tuple[int, int] | None:
    """Return the shortest stretch of conveyor containing the whole bill.

    Args:
        conveyor: Part codes in the order they arrive at the cell.
        bill: The bill of materials. Repeats mean "this many of that part".

    Returns:
        (start, length) for the shortest covering stretch. Ties go to the
        larger start. An empty bill returns (0, 0); a bill no stretch can
        cover returns None.
    """
    # TODO: the two contract answers first — an empty bill, and a bill that
    #       cannot possibly fit. They are different values; read the docstring.
    # TODO: build `wanted` from the bill and remember how many DISTINCT codes
    #       it names. That second number is what `matched` races against.
    # TODO: a window table, `left` at 0, `matched` at 0, `best` unset.
    # TODO: walk `right` over the conveyor. Add the part to the window table.
    #       Increment `matched` ONLY when this code's count becomes EXACTLY
    #       its requirement.
    # TODO: while matched == distinct_wanted:
    #         - record a candidate carrying LENGTH and START, ordered so one
    #           comparison settles both rules;
    #         - THEN drop conveyor[left]: decrement, and decrement `matched`
    #           ONLY when the count falls STRICTLY BELOW the requirement;
    #         - advance left.
    # TODO: unpack the winner into the order the contract asks for.
    ...


def covers(stretch: list[str], bill: list[str]) -> bool:
    """Return True when `stretch` holds every part in `bill`, counting repeats.

    Args:
        stretch: The parts inside a candidate window.
        bill: The bill of materials.

    Returns:
        True when the stretch's counts meet or beat the bill's, for every code
        the bill names.
    """
    # TODO: count the stretch, then check every code the bill names.
    ...


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[str], list[str]]] = [
        (["bolt", "clip", "washer", "nut", "bolt", "washer", "nut", "clip"], ["bolt", "nut", "washer"]),
        (["nut", "bolt", "nut", "nut", "bolt"], ["nut", "nut"]),
        (["bolt", "bolt", "nut"], ["bolt", "nut"]),
        (["washer", "clip", "bolt"], ["bolt", "washer"]),
        (["bolt", "bolt", "bolt"], ["bolt", "nut"]),
        (["nut", "bolt"], ["nut", "nut"]),
        (["bolt"], []),
        ([], ["bolt"]),
    ]
    for conveyor, bill in cases:
        answer = shortest_kit_span(conveyor, bill)
        shown = f"bill {str(bill):<26} belt {str(conveyor):<74}"
        if answer is None:
            print(f"{shown} -> None")
        else:
            start, length = answer
            print(f"{shown} -> ({start}, {length}) = {conveyor[start : start + length]}")
    print()

    assert shortest_kit_span(["bolt", "clip", "washer", "nut", "bolt", "washer", "nut", "clip"], ["bolt", "nut", "washer"]) == (4, 3)
    assert shortest_kit_span(["nut", "bolt", "nut", "nut", "bolt"], ["nut", "nut"]) == (2, 2)
    assert shortest_kit_span(["bolt", "bolt", "nut"], ["bolt", "nut"]) == (1, 2)
    assert shortest_kit_span(["washer", "clip", "bolt"], ["bolt", "washer"]) == (0, 3)
    assert shortest_kit_span(["bolt", "bolt", "bolt"], ["bolt", "nut"]) is None
    assert shortest_kit_span(["nut", "bolt"], ["nut", "nut"]) is None
    assert shortest_kit_span(["bolt"], []) == (0, 0)
    assert shortest_kit_span([], ["bolt"]) is None

    # Brute force agrees, on the examples and on a generated adversarial log.
    scarce = ["bolt"] * 40 + ["nut"] + ["bolt"] * 40
    for conveyor, bill in cases + [(scarce, ["bolt", "nut"]), (scarce, ["nut", "nut"])]:
        spans = [
            (j - i, -i)
            for i in range(len(conveyor))
            for j in range(i + 1, len(conveyor) + 1)
            if covers(conveyor[i:j], bill)
        ]
        if not bill:
            expected: tuple[int, int] | None = (0, 0)
        elif not spans:
            expected = None
        else:
            length, negated_start = min(spans)
            expected = (-negated_start, length)
        assert shortest_kit_span(conveyor, bill) == expected

    print("All checks passed.")
```

Two terms you need before you start.

**Multiset containment.** One collection covers another when it has at least as
many of every item. `["bolt", "bolt", "nut"]` covers `["bolt", "nut"]` and does
not cover `["nut", "nut"]`. It is *not* the same as set containment, which
would only ask whether the codes appear at all.

**Maintain versus recompute.** Two ways of knowing something inside a loop. You
can work it out again at each step, or you can keep it true as you go and only
touch it when something relevant changes. Both are correct; only the second
scales. Recognising which one you have written is a habit worth building, and
this problem is the cleanest example of the difference in the whole course.

**No setup needed — you can solve this one in the browser.** Open the starter in the [online code editor](/ide#src=C2-CrunchTime-The-Code/curriculum/week-03-sliding-window/challenges/challenge-01-shortest-kit-span.md) and run it there. Nothing to install, nothing to configure, and your work stays on your own machine.

## Requirements

1. `shortest_kit_span(conveyor, bill)` returns `(start, length)` or `None`.
2. Duplicates in the bill are real requirements.
   `shortest_kit_span(["nut", "bolt", "nut", "nut", "bolt"], ["nut", "nut"])`
   is `(2, 2)`.
3. Surplus and irrelevant parts inside a stretch are permitted.
   `shortest_kit_span(["washer", "clip", "bolt"], ["bolt", "washer"])` is
   `(0, 3)`.
4. Ties on length go to the **largest** start.
5. An empty bill returns `(0, 0)`. An uncoverable bill returns `None`.
6. Coverage is tested in constant time per step, via a `matched` integer. No
   whole-table comparison inside the loop.
7. Inside the shrink loop the order is **record, remove, advance**.
8. `covers` is used only by the self-check, never by the solution.
9. Both functions keep their type hints and their docstrings.

## Constraints

- **`0 <= len(conveyor) <= 400_000`.** A shift's worth of components on a fast
  line. The bound rejects the obvious brute force — "for every start, walk
  forward until the bill is covered" — which is `O(n · len(bill))` and lands
  around `10^10` operations on the larger inputs.

- **`0 <= len(bill) <= 50_000`.** A bill longer than the conveyor is legal
  input and returns `None` without any window work at all. Guarding it costs
  one line and lets you say something true in the brief rather than discovering
  it in a loop.

- **Part codes are drawn from a catalogue of at most 500 distinct codes, and
  this is the bound that makes the challenge a challenge.** With 500 possible
  codes, checking coverage by comparing the window's whole table against the
  bill's costs up to 500 probes *per shrink step*, and the shrink loop runs up
  to `n` times — so the naive version is `O(500n)`, roughly `2 x 10^8` probes
  here. Name the bound, then name what it costs you, then name the fix. That
  three-step sequence is the interview answer, and it is worth rehearsing as a
  sequence rather than as three separate facts.

- **A code the bill names may be missing entirely, or present but too few
  times.** Both make the bill uncoverable, both return `None`, and they are
  genuinely different failure modes. A solution that checks "is every required
  code present?" rather than "present *often enough*?" gets the first right and
  the second wrong, so test them separately.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2:

```text
$ python challenge-01-shortest-kit-span.py
bill ['bolt', 'nut', 'washer']  belt ['bolt', 'clip', 'washer', 'nut', 'bolt', 'washer', 'nut', 'clip']         -> (4, 3) = ['bolt', 'washer', 'nut']
bill ['nut', 'nut']             belt ['nut', 'bolt', 'nut', 'nut', 'bolt']                                      -> (2, 2) = ['nut', 'nut']
bill ['bolt', 'nut']            belt ['bolt', 'bolt', 'nut']                                                    -> (1, 2) = ['bolt', 'nut']
bill ['bolt', 'washer']         belt ['washer', 'clip', 'bolt']                                                 -> (0, 3) = ['washer', 'clip', 'bolt']
bill ['bolt', 'nut']            belt ['bolt', 'bolt', 'bolt']                                                   -> None
bill ['nut', 'nut']             belt ['nut', 'bolt']                                                            -> None
bill []                         belt ['bolt']                                                                   -> (0, 0) = []
bill ['bolt']                   belt []                                                                         -> None

All checks passed.
```

The first row is the graded one. Five stretches cover the bill with no slack at
either end — indices 0–3 and 1–4 at length 4, then 2–4, 3–5 and 4–6 at length
3. Three of them tie at the minimum. The tie-break takes the largest start, so
`(4, 3)`, which is `["bolt", "washer", "nut"]`. A solution that keeps the first
minimum it meets returns `(2, 3)`: a covering stretch of the right length, and
the wrong answer.

The third row is the state-bug test. The surplus `"bolt"` at index 0 must be
trimmed and the `"bolt"` at index 1 must not be. If you decrement `matched` on
*every* removal rather than only when the count falls below the requirement,
the window gives up at index 1 and you get `(0, 3)`.

## Steps

1. Create the file, paste the starter, and run it. Every row errors or prints
   `None`. Correct starting point.
2. Write the two contract answers first. `not bill` returns `(0, 0)`;
   `len(bill) > len(conveyor)` returns `None`. Say out loud why they are
   different values before you type them.
3. Build `wanted = Counter(bill)` and take `distinct_wanted = len(wanted)`.
   That second number is the finish line `matched` is racing toward, and it is
   the count of *distinct* codes, not the length of the bill.
4. Set up `on_belt`, `left`, `matched = 0` and `best = None`.
5. Write the grow step. Add the part to `on_belt`. Then the increment, and read
   it twice: `if part in wanted and on_belt[part] == wanted[part]`. The `in`
   guard keeps irrelevant parts from touching `matched` at all; the `==` is the
   first of the two operators.
6. Write the shrink as `while matched == distinct_wanted`. Not `if` — after one
   removal the window may still cover the bill, and every one of those is a
   shorter candidate.
7. Inside it: record, then remove, then advance. Build the candidate as a
   two-part tuple with the start negated, so one `<` settles both the length
   rule and the tie-break.
8. The decrement is the second operator:
   `if dropped in wanted and on_belt[dropped] < wanted[dropped]`. Strictly
   less. Not `<=`.
9. Write `covers` last. It is the self-check's opinion, not yours — the point
   of it is that a brute force built from a *different* idea agrees with your
   fast one.
10. Trace the first case by hand before you trust anything. Eight steps, and
    the interesting ones are `right = 4` through `right = 6`, where the window
    slides along at length 3 and the tie-break fires three times.

## The Solution

```python
"""challenge-01-shortest-kit-span-solution.py — the shortest kit span.

A parts conveyor feeds an assembly cell. A kit is defined by a bill of
materials, and repeats in the bill are real requirements. The operator stops
the belt over a contiguous stretch and pulls the whole bill out of it. Surplus
and irrelevant parts inside the stretch are allowed; they only make it longer.

The state that makes this fast is a single integer. `matched` counts how many
distinct part codes from the bill are currently satisfied in the window, so
"does this stretch cover the bill?" is one equality test rather than a walk
over the bill's whole table. Two comparison operators carry the whole trick:
increment only on exact equality, decrement only on a strict shortfall.

The self-checks are the starter's, unchanged. When they all pass the file
prints "All checks passed."
"""

from collections import Counter


def shortest_kit_span(conveyor: list[str], bill: list[str]) -> tuple[int, int] | None:
    """Return the shortest stretch of conveyor containing the whole bill.

    Args:
        conveyor: Part codes in the order they arrive at the cell.
        bill: The bill of materials. Repeats mean "this many of that part".

    Returns:
        (start, length) for the shortest covering stretch. Ties go to the
        larger start. An empty bill returns (0, 0); a bill no stretch can
        cover returns None.
    """
    if not bill:
        return (0, 0)
    if len(bill) > len(conveyor):
        return None

    wanted = Counter(bill)
    distinct_wanted = len(wanted)

    on_belt: dict[str, int] = {}
    left = 0
    matched = 0
    best: tuple[int, int] | None = None

    for right, part in enumerate(conveyor):
        on_belt[part] = on_belt.get(part, 0) + 1
        if part in wanted and on_belt[part] == wanted[part]:
            matched += 1

        while matched == distinct_wanted:
            # Shorter wins; then the later start. Negating the start lets one
            # tuple comparison say both rules at once.
            candidate = (right - left + 1, -left)
            if best is None or candidate < best:
                best = candidate

            dropped = conveyor[left]
            on_belt[dropped] -= 1
            if dropped in wanted and on_belt[dropped] < wanted[dropped]:
                matched -= 1
            left += 1

    if best is None:
        return None
    length, negated_start = best
    return (-negated_start, length)


def covers(stretch: list[str], bill: list[str]) -> bool:
    """Return True when `stretch` holds every part in `bill`, counting repeats.

    Args:
        stretch: The parts inside a candidate window.
        bill: The bill of materials.

    Returns:
        True when the stretch's counts meet or beat the bill's, for every code
        the bill names.
    """
    have = Counter(stretch)
    return all(have[code] >= needed for code, needed in Counter(bill).items())


# ---- Self-check ----
if __name__ == "__main__":
    cases: list[tuple[list[str], list[str]]] = [
        (["bolt", "clip", "washer", "nut", "bolt", "washer", "nut", "clip"], ["bolt", "nut", "washer"]),
        (["nut", "bolt", "nut", "nut", "bolt"], ["nut", "nut"]),
        (["bolt", "bolt", "nut"], ["bolt", "nut"]),
        (["washer", "clip", "bolt"], ["bolt", "washer"]),
        (["bolt", "bolt", "bolt"], ["bolt", "nut"]),
        (["nut", "bolt"], ["nut", "nut"]),
        (["bolt"], []),
        ([], ["bolt"]),
    ]
    for conveyor, bill in cases:
        answer = shortest_kit_span(conveyor, bill)
        shown = f"bill {str(bill):<26} belt {str(conveyor):<74}"
        if answer is None:
            print(f"{shown} -> None")
        else:
            start, length = answer
            print(f"{shown} -> ({start}, {length}) = {conveyor[start : start + length]}")
    print()

    assert shortest_kit_span(["bolt", "clip", "washer", "nut", "bolt", "washer", "nut", "clip"], ["bolt", "nut", "washer"]) == (4, 3)
    assert shortest_kit_span(["nut", "bolt", "nut", "nut", "bolt"], ["nut", "nut"]) == (2, 2)
    assert shortest_kit_span(["bolt", "bolt", "nut"], ["bolt", "nut"]) == (1, 2)
    assert shortest_kit_span(["washer", "clip", "bolt"], ["bolt", "washer"]) == (0, 3)
    assert shortest_kit_span(["bolt", "bolt", "bolt"], ["bolt", "nut"]) is None
    assert shortest_kit_span(["nut", "bolt"], ["nut", "nut"]) is None
    assert shortest_kit_span(["bolt"], []) == (0, 0)
    assert shortest_kit_span([], ["bolt"]) is None

    # Brute force agrees, on the examples and on a generated adversarial log.
    scarce = ["bolt"] * 40 + ["nut"] + ["bolt"] * 40
    for conveyor, bill in cases + [(scarce, ["bolt", "nut"]), (scarce, ["nut", "nut"])]:
        spans = [
            (j - i, -i)
            for i in range(len(conveyor))
            for j in range(i + 1, len(conveyor) + 1)
            if covers(conveyor[i:j], bill)
        ]
        if not bill:
            expected: tuple[int, int] | None = (0, 0)
        elif not spans:
            expected = None
        else:
            length, negated_start = min(spans)
            expected = (-negated_start, length)
        assert shortest_kit_span(conveyor, bill) == expected

    print("All checks passed.")
```

**The two early returns are different answers because the questions are
different.**

```python
if not bill:
    return (0, 0)
if len(bill) > len(conveyor):
    return None
```

An empty bill is *satisfiable* — the empty stretch satisfies it — so the answer
is a span. An oversized bill is *unsatisfiable*, so the answer is the absence
of a span. Collapsing them into one value loses information the caller needs.
Deciding this in the brief rather than in the loop is the habit; a prompt that
does not tell you is a prompt where you ask.

**`distinct_wanted` counts codes, not parts.**

```python
wanted = Counter(bill)
distinct_wanted = len(wanted)
```

For `["nut", "nut", "bolt"]` the bill has three parts and two distinct codes,
and `matched` races against the two. This is easy to get wrong in a way that
produces a loop which never enters the shrink, because `matched` can never
reach a number bigger than the number of codes it counts.

**The increment, one character at a time.**

```python
if part in wanted and on_belt[part] == wanted[part]:
    matched += 1
```

The `in wanted` guard means clips and other irrelevant parts never touch
`matched` — they are allowed in the window and they are not part of the
question. The `==` is the important half. Use `>=` and a fourth bolt would
increment `matched` again on a bill that wanted one, `matched` would sail past
`distinct_wanted`, the shrink condition `matched == distinct_wanted` would stop
matching, and the window would grow forever. Exactly equal means the increment
fires on the *transition* into satisfaction, once, which is the only moment
anything actually changed.

**The decrement, the same idea reflected.**

```python
if dropped in wanted and on_belt[dropped] < wanted[dropped]:
    matched -= 1
```

Strictly less than. Going from three bolts to two, on a bill that wants one,
changes nothing about whether the bill is covered — so `matched` must not move.
Use `<=` and it fires on a window that is still perfectly valid, and you stop
shrinking early. The `["bolt", "bolt", "nut"]` case exists to catch precisely
this, and it is the most common state bug on the page.

Both operators are the same rule stated twice: **`matched` changes only on the
transition**, never while a code is comfortably over or comfortably under.

**Record, remove, advance.**

```python
candidate = (right - left + 1, -left)
if best is None or candidate < best:
    best = candidate
dropped = conveyor[left]
...
left += 1
```

The window you are measuring is the one that exists at that instant. Remove
first and you have measured a stretch that no longer covers the bill. This is
the same ordering rule as Exercise 4 and it is worth saying out loud every time
you write a shrinking window.

The candidate negates the start so a single `<` says both rules: shorter wins,
and among equal lengths the later start wins. Three nested `if`s get the same
answer and give you three places to make a mistake.

**`while`, not `if`.** After one removal the window may still cover the bill —
if you dropped a surplus part, or an irrelevant one — and each of those is a
strictly shorter covering stretch you are obliged to consider. The first case
exercises this directly: at `right = 4` the loop drops a clip, notices the
window still covers the bill, and records a shorter candidate on the very next
turn.

**Why it is `O(n + m)`.** This is the paragraph to have ready, and it is worth
rehearsing until it is one breath:

> The outer loop advances `right` exactly `n` times. The shrink loop advances
> `left`, and `left` carries forward across outer iterations rather than
> resetting — so across the entire algorithm `left` advances at most `n` times,
> not `n` times per outer step. Every table update is `O(1)` on average. The
> `matched` integer changes at most twice per distinct code in the bill, which
> contributes `O(m)`. Total: `O(n + m)` time, `O(m + c)` space, where `c` is
> the catalogue size.

Delivering that cleanly is the difference between "I solved it" and "I
understand why it is fast", and the second one is what is being scored.

**`covers` is deliberately not used by the solution.** The self-check builds a
brute force from a completely different idea — count the stretch, compare every
code — and asserts the two agree on every example plus a generated adversarial
log. Checking a clever implementation against a stupid one is the single most
effective testing habit in this course, because the two are unlikely to be
wrong in the same way.

## Download and run

Download
[challenge-01-shortest-kit-span-solution.py](./challenge-01-shortest-kit-span-solution.py)
and run it:

```bash
python challenge-01-shortest-kit-span-solution.py
```

It is the same program you are writing, under a name that will not collide with
your own `challenge-01-shortest-kit-span.py`.

## Common bugs to catch

- **`shortest_kit_span(["nut", "bolt", "nut", "nut", "bolt"], ["nut", "nut"])`
  returns `(0, 1)`.** You treated the bill as a set of required codes rather
  than a multiset. One nut satisfied "nut is present", and the bill wanted two.
  No traceback; the single most common failure on this page.

- **`shortest_kit_span(["bolt", "bolt", "nut"], ["bolt", "nut"])` returns
  `(0, 3)` instead of `(1, 2)`.** You decremented `matched` on every removal.
  Dropping the surplus bolt at index 0 left one bolt, which still satisfies a
  bill wanting one, so `matched` should not have moved. Use `<`, not `<=`.

- **The loop never terminates, or the answer is the whole conveyor.** You
  incremented `matched` with `>=` instead of `==`. Once `matched` overshoots
  `distinct_wanted`, the equality test in the shrink condition never becomes
  true again and nothing is ever recorded.

- **`shortest_kit_span([...], ["bolt", "nut", "washer"])` returns `(2, 3)`
  instead of `(4, 3)`.** You ignored the tie-break and kept the first minimum
  you found. Three stretches tie at length 3; the contract wants the last.

- **`TypeError: '<' not supported between instances of 'tuple' and 'NoneType'`.**

  ```text
  Traceback (most recent call last):
      if candidate < best:
         ^^^^^^^^^^^^^^^^
  TypeError: '<' not supported between instances of 'tuple' and 'NoneType'
  ```

  You compared before checking for an incumbent. `if best is None or candidate
  < best` short-circuits, so the comparison never runs on the first candidate —
  but only if the `None` check comes first.

- **`KeyError`.**

  ```text
  Traceback (most recent call last):
      if on_belt[part] == wanted[part]:
                          ~~~~~~^^^^^^
  KeyError: 'clip'
  ```

  You dropped the `part in wanted` guard, so an irrelevant part went looking
  for a requirement that does not exist. `Counter` would have returned `0` here
  rather than raising, which is worse: `on_belt["clip"] == 0` is false so
  nothing visibly breaks, until a code with a genuine zero requirement quietly
  behaves like a satisfied one.

- **`IndexError: list index out of range` inside the shrink.**

  ```text
  Traceback (most recent call last):
      dropped = conveyor[left]
                ~~~~~~~~^^^^^^
  IndexError: list index out of range
  ```

  Your shrink condition stayed true after the window emptied. Almost always the
  `>=` increment bug wearing a different symptom, or a missing
  `not bill` guard letting `distinct_wanted` be `0`, which makes
  `matched == distinct_wanted` true before anything has been added.

- **Confusing the two "nothing" answers.** An empty bill returns `(0, 0)`; an
  uncoverable bill returns `None`. The contract says so for a reason.

- **Comparing whole tables inside the loop.** No exception, correct answers, and
  the challenge not met. Requirement 6 is checkable by reading: if a `==`
  between two counters appears inside the `for`, the matched integer is not
  doing its job.

## Under the hood

<details>
<summary>Under the hood — the amortised bound on `matched`, and where this trick generalises</summary>

**Why `matched` is cheap, counted properly.**

It is not obvious that maintaining `matched` is cheaper than recomputing
coverage, so it is worth doing the arithmetic.

Each distinct code `c` in the bill has a count in the window that goes up when
`c` enters and down when `c` leaves. `matched` changes only when that count
crosses the threshold `wanted[c]` — upward through it, or downward through it.
Between two consecutive upward crossings there must be a downward one, and vice
versa, so the crossings alternate.

How many can there be? Every upward crossing is caused by an insertion of `c`,
and there are at most as many insertions of `c` as there are copies of `c` on
the conveyor. Summed over all codes, that is at most `n` upward crossings and
at most `n` downward ones across the whole algorithm — and in practice far
fewer. So `matched` costs `O(n)` total to maintain, amortised `O(1)` per step,
against `O(c)` per step for the table comparison, where `c` is the catalogue
size.

The deeper point is not the constant factor. It is that the invariant is
*maintained* rather than *re-derived*, which means the loop carries the meaning
of the problem rather than recomputing it. That is the property an interviewer
listens for.

**Space, stated precisely.**

`wanted` holds at most `min(len(bill), 500)` entries. `on_belt` holds at most
`min(n, 500)`. So space is `O(m + c)` where `c` is the catalogue bound, and
with `c` fixed at 500 that is `O(m)` — or `O(1)` if you are willing to treat
the catalogue as a constant, which you should say out loud rather than assume.

**Where the same move turns up again.**

The matched-count trick is the general way to maintain any predicate that
decomposes into **independent per-key conditions**. The pattern is always the
same three parts: a per-key condition, a counter of how many keys currently
satisfy it, and updates that fire only on the transition.

You will meet it in three more places in this course. The
[mini-project's Problem 6](../mini-project/README.md) is this exact shape with
the tie-break inverted — deliberately, to test whether you carry the pattern or
the solution. Week 9's advanced-string work uses the same counter over a trie's
terminal nodes. And Week 10's union-find keeps a "number of components" integer
by exactly this reasoning: never recount, only adjust on the merge.

**Two alternative approaches worth being able to name.**

*Pre-filtering.* Walk the conveyor once and keep only the indices whose codes
appear in the bill. Slide the window over that shorter list, mapping back to
original indices at the end. It changes nothing asymptotically and can be a
large constant-factor win when the bill names a handful of codes from a
catalogue of 500. Say it anyway; knowing the difference between an asymptotic
improvement and a constant-factor one is worth a point.

*`Counter` containment.* Python 3.10 added `<=` to `Counter`, so
`wanted <= Counter(window)` is a legal coverage test and reads beautifully. It
is also `O(m)` per call, so it is the naive version with nicer syntax. Being
able to say "that expression is correct and it is the thing the constraint
rejects" is a better answer than not knowing the operator exists.

**Re-derive, do not re-read.** When you come back to this problem — in the
mastery pathway, or the week before a real interview — work it out again from
the invariant rather than opening your old solution. Memorised solutions
evaporate under pressure. Re-derived ones do not, because what you memorised
was the reasoning.

</details>

## Acceptance checklist

- [ ] `python challenge-01-shortest-kit-span.py` prints eight rows then `All checks passed.`
- [ ] The output matches the Expected output block character for character.
- [ ] The increment uses `==` and the decrement uses `<`, and you can say why each is not the looser operator.
- [ ] `shortest_kit_span([...], ["bolt", "nut", "washer"])` returns `(4, 3)`, not `(2, 3)`.
- [ ] An empty bill returns `(0, 0)` and an uncoverable bill returns `None`.
- [ ] No whole-table comparison appears inside the loop.
- [ ] Your shrink loop records before it removes.
- [ ] The brute-force check passes on the generated 81-part adversarial log.
- [ ] You can deliver the "why `O(n + m)`" paragraph in one breath, without notes.
- [ ] You have written down which of the two operators you got wrong first. Almost everyone gets one of them wrong, and the note is worth more than the solution.
- [ ] Committed to Git with a message like `Add Week 3 challenge 1: the shortest kit span`.

## Stretch

- **Generate your own adversarial cases.** Two are worth writing before you
  trust anything, and the file already ships the first:

  ```python
  scarce = ["bolt"] * 10_000 + ["nut"] + ["bolt"] * 10_000
  print(shortest_kit_span(scarce, ["bolt", "nut"]))
  ```

  ```text
  (10000, 2)
  ```

  A long conveyor with one scarce part catches shrink loops that are quadratic
  in disguise: if your `left` resets anywhere, this will take visible seconds
  instead of no time at all. The second case is a bill that is *almost*
  satisfiable — put `q - 1` copies of a code on the belt while the bill asks for
  `q` — which catches solutions that check presence rather than sufficiency.

- **Return the parts as well as the position.**

  ```python
  def shortest_kit_span_detail(conveyor: list[str], bill: list[str]) -> tuple[int, int, list[str]] | None:
      """Return (start, length, parts) for the shortest covering stretch."""
      answer = shortest_kit_span(conveyor, bill)
      if answer is None:
          return None
      start, length = answer
      return (start, length, conveyor[start : start + length])
  ```

  ```text
  (["bolt", "clip", "washer", "nut", "bolt", "washer", "nut", "clip"], ["bolt", "nut", "washer"])
    -> (4, 3, ['bolt', 'washer', 'nut'])
  ```

- **Allow substitutions.** Extend the bill so some codes are interchangeable — a
  `"m8-bolt"` may stand in for a `"bolt"`. The window mechanics do not change at
  all; what changes is that `wanted` is keyed on *groups* rather than codes, and
  the increment compares a group's total against the group's requirement. Ten
  lines of difference and a genuinely harder invariant to state out loud. C2
  does not cover it formally; bookmark it as the next step up.
Next: [Challenge 2 — The Repaving Stretch](./challenge-02-repaving-stretch.md).
